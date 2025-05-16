from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

# Load environment variables
load_dotenv()

MODEL = "gpt-4-turbo"
TEMPERATURE = 0
SCHEMA_PATH = Path(__file__).parent / "schema.sql"

"""
Database Agent for answering questions about the database schema.
This agent uses LangChain and OpenAI to provide answers based on the schema file.
"""
class DatabaseAgent:

    def __init__(self):
        # Load the schema
        self.schema = self._load_schema(SCHEMA_PATH)

        # Initialize the LLM
        self.llm = ChatOpenAI(model=MODEL, temperature=TEMPERATURE)

        # Create the prompt template with separate system and user messages
        system_template = """
        You are a database expert. You are given a SQL schema and a question about the database.
        Your task is to answer the question based ONLY on the information in the schema.
        If the question cannot be answered based on the schema, say so.

        Schema:
        {schema}
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
            {"schema": lambda x: self.schema, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
        )

    def _load_schema(self, schema_path):
        with open(schema_path, 'r') as f:
            return f.read()

    def query(self, question):
        response = self.chain.invoke(question)
        return response.content


if __name__ == "__main__":
    # Example usage
    agent = DatabaseAgent()

    # Example questions
    questions = [
        "What tables do we have in the database?",
        "What fields do we have in an application?",
        "Where do we persist application data?",
        "Can a business have multiple loan applications?",
        "How to submit an application? Where to find the status of an application?",
        "Generate sql query to get application status by user email",
    ]

    # Print answers to example questions
    for question in questions:
        print(f"Question: {question}")
        print(f"Answer: {agent.query(question)}")
        print("-" * 100)
