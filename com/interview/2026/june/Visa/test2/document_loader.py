import json
import os
from typing import List, Dict
from langchain_core.documents import Document


class DocumentLoader:
    """
    Loads and processes OpenAPI specs and live service metadata into LangChain-compatible Documents.
    """

    def __init__(self, openapi_path: str, metadata_path: str):
        self.openapi_path = openapi_path
        self.metadata_path = metadata_path

    def load_openapi_spec(self) -> Dict:
        """
        Loads OpenAPI spec JSON and validates presence of required sections.

        Required fields in OpenAPI spec:
        - openapi (version)
        """
        if not os.path.exists(self.openapi_path):
            raise FileNotFoundError(f"OpenAPI file missing at {self.openapi_path}")

        with open(self.openapi_path, "r", encoding="utf-8") as file:
            spec = json.load(file)

        if "openapi" not in spec:
            raise ValueError("Invalid OpenAPI spec: Missing 'openapi' version field.")

        return spec

    def load_live_service_metadata(self) -> List[Document]:
        """
        Loads service metadata and converts each tenant to a LangChain Document.

        Each document should contain:
        - page_content: full JSON dump of the tenant
        - metadata: tenant_id, base_url, auth, last_updated, feature_flags

        Returns:
            List[Document]: documents per tenant

        Raises:
            FileNotFoundError: if metadata file is missing
        """
        if not os.path.exists(self.metadata_path):
            raise FileNotFoundError(f"Metadata file missing at {self.metadata_path}")

        with open(self.metadata_path, "r", encoding="utf-8") as file:
            metadata = json.load(file)

        documents = []
        # Assuming the root JSON is a list of tenants, or accessible via a 'tenants' key
        tenants = metadata if isinstance(metadata, list) else metadata.get("tenants", [])

        required_keys = ["tenant_id", "base_url", "auth", "feature_flags", "last_updated"]

        for tenant in tenants:
            # Ensure all required metadata fields exist for the tenant
            if not all(key in tenant for key in required_keys):
                continue

            doc_metadata = {key: tenant[key] for key in required_keys}

            doc = Document(
                page_content=json.dumps(tenant),
                metadata=doc_metadata
            )
            documents.append(doc)

        return documents

    def create_documents(self) -> List[Document]:
        """
        Combines OpenAPI and metadata into a single document list.

        From OpenAPI, each operation (GET /x) becomes one Document.
        Each OpenAPI Document's metadata must include "openapi_version".
        From metadata, each tenant becomes one Document.

        Returns:
            List[Document]: combined list
        """
        combined_documents = []

        # 1. Process OpenAPI Specification
        spec = self.load_openapi_spec()
        openapi_version = spec.get("openapi")
        paths = spec.get("paths", {})

        for path, operations in paths.items():
            for method, details in operations.items():
                # Store the endpoint and details contextually in the page content
                content_dict = {
                    "endpoint": f"{method.upper()} {path}",
                    "details": details
                }

                doc = Document(
                    page_content=json.dumps(content_dict),
                    metadata={
                        "openapi_version": openapi_version,
                        "source_type": "openapi_operation"
                    }
                )
                combined_documents.append(doc)

        # 2. Process Service Metadata
        tenant_documents = self.load_live_service_metadata()
        combined_documents.extend(tenant_documents)

        return combined_documents