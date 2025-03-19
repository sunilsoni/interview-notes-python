import logging

# Set up logging for debugging and error tracking
logging.basicConfig(level=logging.INFO)


class RAGSystem:
    def __init__(self, vector_db, language_model):
        """
        Initialize the RAG system with a vector database and a language model.
        vector_db: An object with a method `query(embedding)` that returns relevant documents.
        language_model: An object with a method `generate(prompt)` that produces an answer.
        """
        self.vector_db = vector_db
        self.language_model = language_model

    def compute_embedding(self, query):
        """
        Compute the embedding for the query.
        For simplicity, we simulate an embedding as the query in lowercase.
        In practice, you would use a pre-trained embedding model.
        """
        # Here, we simulate the embedding process.
        return query.lower()

    def retrieve_documents(self, query):
        """
        Retrieve relevant documents from the knowledge base using the vector database.
        Includes error handling and logging for edge cases.
        """
        try:
            # Compute embedding for the query.
            embedding = self.compute_embedding(query)
            logging.info("Computed embedding for query.")
            # Query the vector database.
            documents = self.vector_db.query(embedding)
            # Check if any documents were retrieved.
            if not documents:
                logging.warning("No documents retrieved from the knowledge base.")
                return []
            return documents
        except Exception as e:
            logging.error(f"Error during document retrieval: {e}")
            return []  # Fallback to empty list in error cases

    def combine_query_with_context(self, query, documents):
        """
        Combine the original query with the retrieved documents.
        For a basic implementation, we simply concatenate the documents to the query.
        """
        context = " ".join(documents) if documents else ""
        combined_prompt = query + " " + context
        logging.info("Combined query with retrieved context.")
        return combined_prompt

    def generate_answer(self, combined_prompt):
        """
        Generate an answer using the language model given the combined prompt.
        """
        try:
            answer = self.language_model.generate(combined_prompt)
            logging.info("Generated answer from language model.")
            return answer
        except Exception as e:
            logging.error(f"Error during answer generation: {e}")
            return "An error occurred while generating the answer."

    def process_query(self, query):
        """
        The main method to process the RAG workflow:
          1. Retrieve documents.
          2. Combine query with context.
          3. Generate answer using language model.
        """
        # Retrieve documents related to the query
        docs = self.retrieve_documents(query)
        # Combine the user query with retrieved documents
        combined_prompt = self.combine_query_with_context(query, docs)
        # Generate and return the final answer
        return self.generate_answer(combined_prompt)


# --- Simulated Vector Database and Language Model for Testing ---

class DummyVectorDB:
    def __init__(self, documents):
        """
        Initialize the dummy vector database with a list of documents.
        """
        self.documents = documents

    def query(self, embedding):
        """
        Simulate querying by returning documents that contain any word from the embedding.
        For simplicity, this dummy implementation matches if the embedding appears in a document.
        """
        # In real implementation, you would use nearest neighbor search.
        result = [doc for doc in self.documents if embedding in doc.lower()]
        return result


class DummyLanguageModel:
    def generate(self, prompt):
        """
        Simulate a language model generating an answer.
        For demonstration, return a simple confirmation string.
        """
        return f"Generated answer based on prompt: {prompt}"


# --- Testing Framework ---

def run_tests():
    """
    Run a set of tests on the RAG system and output pass/fail results.
    This includes edge cases and handling large data inputs.
    """
    # Create dummy documents for the vector database
    documents = [
        "This is a document about Python programming.",
        "Learn how to implement systems using PySpark DataFrame API.",
        "This document covers Retrieval Augmented Generation techniques.",
        "Additional large data document " * 100  # Simulating a large input document
    ]

    # Instantiate the dummy vector database and language model
    vector_db = DummyVectorDB(documents)
    language_model = DummyLanguageModel()

    # Create an instance of RAGSystem
    rag_system = RAGSystem(vector_db, language_model)

    # Define test cases as a list of dictionaries
    test_cases = [
        {"query": "Tell me about Python", "expected_contains": "python programming"},
        {"query": "Explain PySpark", "expected_contains": "pyspark dataframe"},
        {"query": "What is Retrieval Augmented Generation?", "expected_contains": "retrieval augmented generation"},
        {"query": "Nonexistent topic", "expected_contains": "Nonexistent topic"}  # Expecting no context added
    ]

    # Flag to track overall test status
    all_passed = True

    # Iterate over each test case
    for i, test in enumerate(test_cases, start=1):
        query = test["query"]
        expected_substring = test["expected_contains"].lower()
        result = rag_system.process_query(query)
        # Check if the expected substring is in the generated answer (case-insensitive check)
        if expected_substring in result.lower():
            print(f"Test Case {i}: PASS")
        else:
            print(f"Test Case {i}: FAIL")
            print(f"  Query: {query}")
            print(f"  Expected to contain: {expected_substring}")
            print(f"  Got: {result}")
            all_passed = False

    # Additional test for large input data
    large_query = "Large data test"
    large_result = rag_system.process_query(large_query)
    if isinstance(large_result, str) and len(large_result) > 0:
        print("Large Data Test: PASS")
    else:
        print("Large Data Test: FAIL")
        all_passed = False

    if all_passed:
        print("All tests passed successfully!")
    else:
        print("Some tests failed. Please check the logs for details.")


# --- Main execution block ---

if __name__ == "__main__":
    # Run the test suite
    run_tests()
