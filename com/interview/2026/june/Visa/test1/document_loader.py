import json
import os
from typing import List, Dict, Any

from langchain_core.documents import Document


class DocumentLoader:
    """
    Loads OpenAPI specs and live service metadata into LangChain Documents.
    """

    def __init__(self, openapi_path: str, metadata_path: str):
        self.openapi_path = openapi_path
        self.metadata_path = metadata_path

    def _read_json(self, path: str) -> Any:
        # Check file exists before reading
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")

        # Read JSON file safely
        try:
            with open(path, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError as error:
            raise ValueError(f"Invalid JSON file: {path}") from error

    def load_openapi_spec(self) -> Dict:
        """
        Loads OpenAPI spec JSON and validates required sections.

        Required fields:
        - openapi
        - info
        - paths
        """

        spec = self._read_json(self.openapi_path)

        required_fields = ["openapi", "info", "paths"]

        # Check all required fields exist
        missing = [field for field in required_fields if field not in spec]

        if missing:
            raise ValueError(f"OpenAPI spec missing fields: {missing}")

        # paths should be a non-empty dictionary
        if not isinstance(spec["paths"], dict) or not spec["paths"]:
            raise ValueError("OpenAPI spec must contain non-empty 'paths'")

        return spec

    def load_live_service_metadata(self) -> List[Document]:
        """
        Loads service metadata and converts each tenant to a LangChain Document.

        Each tenant must have:
        - tenant_id
        - base_url
        - auth
        - feature_flags
        - last_updated
        """

        metadata_json = self._read_json(self.metadata_path)

        # Support both formats:
        # 1. [ {...}, {...} ]
        # 2. { "tenants": [ {...}, {...} ] }
        tenants = metadata_json.get("tenants", metadata_json) if isinstance(metadata_json, dict) else metadata_json

        if not isinstance(tenants, list):
            raise ValueError("Metadata JSON must be a list or contain a 'tenants' list")

        required_fields = ["tenant_id", "base_url", "auth", "feature_flags", "last_updated"]

        documents = []

        for index, tenant in enumerate(tenants):
            # Every tenant should be a dictionary
            if not isinstance(tenant, dict):
                raise ValueError(f"Tenant at index {index} must be an object")

            # Find missing required fields
            missing = [field for field in required_fields if field not in tenant]

            if missing:
                raise ValueError(f"Tenant at index {index} missing fields: {missing}")

            # Full tenant JSON becomes searchable text
            page_content = json.dumps(tenant, indent=2, sort_keys=True)

            # Metadata helps identify source later
            doc_metadata = {
                "source": "live_service_metadata",
                "doc_type": "tenant_metadata",
                "tenant_id": tenant["tenant_id"],
                "base_url": tenant["base_url"],
                "auth": json.dumps(tenant["auth"], sort_keys=True),
                "feature_flags": json.dumps(tenant["feature_flags"], sort_keys=True),
                "last_updated": tenant["last_updated"],
            }

            documents.append(
                Document(
                    page_content=page_content,
                    metadata=doc_metadata,
                )
            )

        return documents

    def _create_openapi_documents(self, spec: Dict) -> List[Document]:
        """
        Converts each OpenAPI operation into one LangChain Document.

        Example:
        POST /billing/create becomes one Document.
        """

        documents = []

        openapi_version = spec["openapi"]
        valid_methods = {"get", "post", "put", "patch", "delete", "options", "head"}

        for path, path_data in spec["paths"].items():
            if not isinstance(path_data, dict):
                continue

            for method, operation in path_data.items():
                method_lower = method.lower()

                # Skip non-HTTP fields
                if method_lower not in valid_methods:
                    continue

                if not isinstance(operation, dict):
                    continue

                summary = operation.get("summary", "")
                description = operation.get("description", "")
                operation_id = operation.get("operationId", "")
                tags = operation.get("tags", [])
                parameters = operation.get("parameters", [])
                request_body = operation.get("requestBody", {})
                responses = operation.get("responses", {})

                # Make the document easy for vector search
                page_content = f"""
Method: {method_upper(method_lower)}
Path: {path}
Operation ID: {operation_id}
Summary: {summary}
Description: {description}
Tags: {", ".join(tags) if isinstance(tags, list) else tags}

Parameters:
{json.dumps(parameters, indent=2, sort_keys=True)}

Request Body:
{json.dumps(request_body, indent=2, sort_keys=True)}

Responses:
{json.dumps(responses, indent=2, sort_keys=True)}
""".strip()

                documents.append(
                    Document(
                        page_content=page_content,
                        metadata={
                            "source": "openapi",
                            "doc_type": "api_operation",
                            "openapi_version": openapi_version,
                            "method": method_upper(method_lower),
                            "path": path,
                            "operation_id": operation_id,
                        },
                    )
                )

        if not documents:
            raise ValueError("No API operations found in OpenAPI spec")

        return documents

    def create_documents(self) -> List[Document]:
        """
        Combines OpenAPI and metadata into a single document list.
        """

        openapi_spec = self.load_openapi_spec()

        openapi_documents = self._create_openapi_documents(openapi_spec)

        metadata_documents = self.load_live_service_metadata()

        return openapi_documents + metadata_documents


def method_upper(method: str) -> str:
    # Small helper to keep method names consistent
    return method.upper()