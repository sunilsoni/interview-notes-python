import json
import math
import tempfile
from typing import List

from langchain_core.embeddings import Embeddings

from document_loader import DocumentLoader
from vector_store import VectorStoreBuilder


class FakeEmbeddings(Embeddings):
    """
    Simple fake embedding model for local tests.
    It avoids real OpenAI API calls.
    """

    def _embed(self, text: str) -> List[float]:
        vector = [0.0] * 16

        for word in text.lower().split():
            index = abs(hash(word)) % 16
            vector[index] += 1.0

        length = math.sqrt(sum(x * x for x in vector)) or 1.0

        return [x / length for x in vector]

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self._embed(text) for text in texts]

    def embed_query(self, text: str) -> List[float]:
        return self._embed(text)


def check(name: str, condition: bool):
    print(f"{name}: {'PASS' if condition else 'FAIL'}")


def main():
    sample_openapi = {
        "openapi": "3.0.0",
        "info": {
            "title": "Billing API",
            "version": "1.0.0"
        },
        "paths": {
            "/billing/create": {
                "post": {
                    "summary": "Create billing record",
                    "description": "Creates a billing record for an account.",
                    "operationId": "createBilling",
                    "tags": ["billing"],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "required": ["account_id", "amount"]
                                }
                            }
                        }
                    },
                    "responses": {
                        "201": {
                            "description": "Billing record created"
                        }
                    }
                }
            }
        }
    }

    sample_metadata = {
        "tenants": [
            {
                "tenant_id": "tenant-a",
                "base_url": "https://api.internal.example.com",
                "auth": {
                    "type": "Bearer token"
                },
                "feature_flags": {
                    "billing": True
                },
                "last_updated": "2026-06-16",
                "rate_limits": {
                    "POST /billing/create": "100 requests per minute"
                }
            }
        ]
    }

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as openapi_file:
        json.dump(sample_openapi, openapi_file)
        openapi_path = openapi_file.name

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as metadata_file:
        json.dump(sample_metadata, metadata_file)
        metadata_path = metadata_file.name

    loader = DocumentLoader(openapi_path, metadata_path)

    docs = loader.create_documents()

    check("Documents created", len(docs) == 2)

    check(
        "OpenAPI document exists",
        any(doc.metadata.get("source") == "openapi" for doc in docs)
    )

    check(
        "Metadata document exists",
        any(doc.metadata.get("source") == "live_service_metadata" for doc in docs)
    )

    vector_builder = VectorStoreBuilder(embedding_model=FakeEmbeddings())

    vector_builder.build_index(docs)

    results = vector_builder.search("create billing record rate limit", k=2)

    check("Search returns results", len(results) > 0)

    print("\nTop result:")
    print(results[0].page_content)


if __name__ == "__main__":
    main()