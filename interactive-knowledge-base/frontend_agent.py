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
TYPESCRIPT_FILES_PATH = Path(__file__).parent.parent / "quick-loan-platform" / "lovable-ui" / "src"

"""
Frontend Agent for answering questions about the lovable-ui frontend.
This agent uses LlamaIndex to retrieve relevant information from TypeScript files
and to provide answers based on the retrieved context.
"""
class FrontendAgent:

    def __init__(self):
        # Set up LlamaIndex
        Settings.llm = OpenAI(model=MODEL, temperature=TEMPERATURE)
        Settings.embed_model = OpenAIEmbedding()
        Settings.context_window = 32000

        # Load and index TypeScript files
        self.index = self._create_vector_index(TYPESCRIPT_FILES_PATH)

        # Create a custom query engine with our prompt
        self.query_engine = self.index.as_query_engine(
            similarity_top_k=10,
            # response_mode="tree_summarize"
        )

    def _create_vector_index(self, directory_path):
        """
        Create a vector index from TypeScript files in the specified directory.
        """
        documents = SimpleDirectoryReader(
            input_dir=str(directory_path),
            required_exts=[".ts", ".tsx"],
            recursive=True,
        ).load_data()

        # Create vector index
        return VectorStoreIndex.from_documents(documents)

    def query(self, question):
        """
        Answer a question about the frontend UI.
        """
        response = self.query_engine.query(question)
        return response.response


if __name__ == "__main__":
    # Example usage
    agent = FrontendAgent()

    # Example questions
    questions = [
        "What pages do we have on UI? Provide content of each page.",
        "How is the application form structured? Provide a list of all fields used there.",
        "How is user data validated in the application?",
        "What API calls does the frontend make?",
        "How does the UI handle application status updates?",
    ]

    # Print answers to example questions
    for question in questions:
        print(f"Question: {question}")
        print(f"Answer: {agent.query(question)}")
        print("-" * 100)