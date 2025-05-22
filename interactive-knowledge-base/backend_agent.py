from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
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
and LangChain with OpenAI to provide answers based on the retrieved context.
"""
class BackendAgent:

    def __init__(self):
        # Initialize the LLM
        self.llm = ChatOpenAI(model=MODEL, temperature=TEMPERATURE)

        # Set up LlamaIndex
        Settings.llm = OpenAI(model=MODEL, temperature=TEMPERATURE)
        Settings.embed_model = OpenAIEmbedding()

        # Load and index Java files
        self.index = self._create_vector_index(JAVA_FILES_PATH)

        # Create the prompt template with separate system and user messages
        system_template = """
        You are a backend expert specializing in the loan application service. 
        You are given a question about the loan application service and relevant code snippets from the service.
        Your task is to answer the question based ONLY on the information in the provided context.
        If the question cannot be answered based on the context, say so.

        Context:
        {context}
        """

        human_template = """
        Question: {question}
        """

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_template),
            ("human", human_template)
        ])

        # Create the chain using the newer RunnableSequence approach
        self.chain = (
            {"context": lambda x: self._retrieve_context(x), "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
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

    def _retrieve_context(self, question):
        """
        Retrieve relevant context from the vector index based on the question.
        """
        query_engine = self.index.as_query_engine(similarity_top_k=10)
        response = query_engine.query(question)
        return response.response

    def query(self, question):
        """
        Answer a question about the loan application service.
        """
        response = self.chain.invoke(question)
        return response.content


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
