from typing import List

from langchain_core.documents import Document
from langchain_openai import ChatOpenAI

from document_loader import DocumentLoader
from vector_store import VectorStoreBuilder


class RAGPipeline:
    """
    Handles query retrieval and answer generation.
    """

    def __init__(self, openapi_path: str, metadata_path: str):
        self.loader = DocumentLoader(openapi_path, metadata_path)
        self.vector_builder = VectorStoreBuilder()

        # Temperature 0 means more stable answers
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0)

    def build(self):
        """
        Loads documents and builds vector index.
        """

        documents = self.loader.create_documents()
        self.vector_builder.build_index(documents)

    def retrieve(self, query: str, k: int = 5) -> List[Document]:
        """
        Finds top-k relevant documents for the query.
        """

        return self.vector_builder.search(query=query, k=k)

    def answer(self, query: str, k: int = 5) -> str:
        """
        Retrieves relevant docs and asks LLM to generate final answer.
        """

        docs = self.retrieve(query, k)

        context = "\n\n---\n\n".join(
            f"Source: {doc.metadata}\nContent:\n{doc.page_content}"
            for doc in docs
        )

        prompt = f"""
You are an API support assistant.

Answer the developer's question using only the context below.

Developer question:
{query}

Context:
{context}

Rules:
- Be clear and concise.
- Mention endpoint method and path if available.
- Mention required parameters if available.
- Mention auth, base URL, tenant rules, or rate limits if available.
- If the answer is not in the context, say you could not find it in the docs.
"""

        response = self.llm.invoke(prompt)

        return response.content


if __name__ == "__main__":
    pipeline = RAGPipeline(
        openapi_path="openapi.json",
        metadata_path="live_service_metadata.json",
    )

    pipeline.build()

    question = "How do I create a billing record and what's the rate limit?"

    answer = pipeline.answer(question)

    print(answer)