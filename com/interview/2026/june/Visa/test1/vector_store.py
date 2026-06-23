from typing import List, Optional

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings


class VectorStoreBuilder:
    """
    Builds a FAISS vector index from LangChain Documents using OpenAI embeddings.
    """

    def __init__(self, embedding_model: Optional[Embeddings] = None):
        self.vector_store = None

        # In real usage, use OpenAI embeddings.
        # In tests, we can pass fake embeddings to avoid API calls.
        self.embedding_model = embedding_model or OpenAIEmbeddings(
            model="text-embedding-ada-002"
        )

    def build_index(self, documents: List[Document]):
        """
        Converts input documents to embeddings and creates FAISS index.

        Raises:
            ValueError: if no input documents
        """

        if not documents:
            raise ValueError("No documents provided to build vector index")

        # FAISS creates embeddings internally using the embedding model
        self.vector_store = FAISS.from_documents(
            documents=documents,
            embedding=self.embedding_model,
        )

        # Return retriever because RAG pipeline can directly use it
        return self.vector_store.as_retriever(search_kwargs={"k": 5})

    def search(self, query: str, k: int = 5) -> List[Document]:
        """
        Runs similarity search on built index using query.

        Raises:
            ValueError: if index not built yet
        """

        if self.vector_store is None:
            raise ValueError("Vector index not built yet. Call build_index() first.")

        if not query or not query.strip():
            raise ValueError("Search query cannot be empty")

        # Return top-k matching documents
        return self.vector_store.similarity_search(query=query, k=k)