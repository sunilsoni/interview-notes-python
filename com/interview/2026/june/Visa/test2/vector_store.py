from typing import List
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings


class VectorStoreBuilder:
    """
    Builds a vector index from LangChain Documents using OpenAI embeddings.
    """

    def __init__(self):
        self.vector_store = None
        self.embedding_model = OpenAIEmbeddings(model="text-embedding-ada-002")

    def build_index(self, documents: List[Document]):
        """
        Converts input documents to embeddings and creates vector index.

        Args:
            documents (List[Document]): source documents

        Raises:
            ValueError: if no input documents
        """
        if not documents:
            raise ValueError("Cannot build index: No input documents provided.")

        self.vector_store = FAISS.from_documents(documents, self.embedding_model)

        # Depending on your chain setup in rag_pipeline.py, returning the retriever is useful
        return self.vector_store.as_retriever()

    def search(self, query: str, k: int = 5) -> List[Document]:
        """
        Runs similarity search on built index using query.

        Args:
            query (str): natural language input
            k (int): number of results

        Returns:
            List[Document]: matched documents

        Raises:
            ValueError: if index not built yet
        """
        if self.vector_store is None:
            raise ValueError("Cannot search: Index not built yet.")

        return self.vector_store.similarity_search(query, k=k)