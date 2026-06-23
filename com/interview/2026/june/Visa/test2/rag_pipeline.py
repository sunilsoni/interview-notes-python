import os
from langchain_openai import ChatOpenAI
from document_loader import DocumentLoader
from vector_store import VectorStoreBuilder


class RAGPipeline:
    """
    Coordinates document ingestion, vector retrieval, and answer generation.
    """

    def __init__(self, openapi_path: str, metadata_path: str):
        self.loader = DocumentLoader(openapi_path, metadata_path)
        self.vector_store_builder = VectorStoreBuilder()
        # Initializing the LLM specified in the task parameters
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.2)

    def setup(self):
        """
        Executes the 'Ingest Docs' and 'Embed & Index' pipeline stages.
        """
        print("Loading and preprocessing documents...")
        docs = self.loader.create_documents()

        print(f"Embedding {len(docs)} documents and building FAISS index...")
        self.vector_store_builder.build_index(docs)
        print("Pipeline setup complete. Ready for queries.")

    def query(self, user_question: str) -> str:
        """
        Accepts a developer query, retrieves relevant context, and generates a response.
        """
        # 1. Retrieve the top relevant chunks
        retrieved_docs = self.vector_store_builder.search(user_question, k=5)

        # 2. Format context for the LLM
        context = "\n\n".join([f"Document {i + 1}:\n{doc.page_content}"
                               for i, doc in enumerate(retrieved_docs)])

        # 3. Construct the prompt
        prompt = f"""
        You are an expert API support engineer. Use the provided internal documentation context 
        (which includes OpenAPI endpoints and tenant-specific metadata) to answer the developer's question.

        Instructions:
        - Return a clear, actionable answer.
        - Include references to specific endpoints, required parameters, and tenant-specific rules or rate limits if applicable.
        - If the answer is not contained within the context, state that you do not have that information.

        Context:
        {context}

        Developer Question: 
        {user_question}

        Answer:
        """

        # 4. Generate Answer
        response = self.llm.invoke(prompt)
        return response.content


# Example Usage
if __name__ == "__main__":
    # Ensure OPENAI_API_KEY is set in your environment variables before running
    pipeline = RAGPipeline(
        openapi_path="openapi.json",
        metadata_path="live_service_metadata.json"
    )

    pipeline.setup()

    sample_query = "How do I create a billing record, and what's the rate limit?"
    answer = pipeline.query(sample_query)

    print("\n--- Final Output ---")
    print(answer)