from pathlib import Path
from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.core.prompts import PromptTemplate
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

# Load environment variables
load_dotenv()

MODEL = "gpt-4-turbo"
TEMPERATURE = 0
JAVA_FILES_PATH = Path(__file__).parent.parent / "quick-loan-platform" / "loan-application-service"

"""
Backend Agent for answering questions about the loan application service.
This agent uses LlamaIndex to retrieve relevant information from Java files
and to provide answers based on the retrieved context.
"""
class BackendAgent:

    def __init__(self):
        # Set up LlamaIndex
        Settings.llm = OpenAI(model=MODEL, temperature=TEMPERATURE)
        Settings.embed_model = OpenAIEmbedding()

        # Load and index Java files
        self.index = self._create_vector_index(JAVA_FILES_PATH)

        # Create a custom query engine with our prompt
        self.query_engine = self.index.as_query_engine(
            similarity_top_k=10,
            # response_mode="tree_summarize"
        )

    def _create_vector_index(self, directory_path):
        """
        Create a vector index from Java files in the specified directory.
        """
        documents = SimpleDirectoryReader(
            input_dir=str(directory_path),
            required_exts=[".java"],
            recursive=True,
        ).load_data()

        # Create vector index
        return VectorStoreIndex.from_documents(documents)

    def query(self, question):
        """
        Answer a question about the loan application service.
        """
        response = self.query_engine.query(question)
        return response.response


if __name__ == "__main__":
    # Example usage
    agent = BackendAgent()

    # Example questions
    questions = [
        "How to submit an application? Where to find the status of an application?",
        "Where do we persist application data?",
        "What APIs do we have? What are their payloads in json format?",
        "How does our application submission process work?",
        "What application decline rules do we have?",
        "What application fields do we ask?",
        "What are the main components of the loan application service?",
        "How is user data validated in the application?",
    ]

    # Print answers to example questions
    for question in questions:
        print(f"Question: {question}")
        print(f"Answer: {agent.query(question)}")
        print("-" * 100)
