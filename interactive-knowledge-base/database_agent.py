"""
Database Agent for answering questions about the database schema.
This agent uses LangChain and OpenAI to provide answers based on the schema.sql file.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

# Load environment variables
load_dotenv()

class DatabaseAgent:
    """
    Agent that answers questions about the database schema using LangChain and LLM.
    """

    def __init__(self, schema_path=None):
        """
        Initialize the DatabaseAgent with the schema file.

        Args:
            schema_path (str, optional): Path to the schema.sql file. 
                                        If None, uses the default schema.sql in the same directory.
        """
        # Set default schema path if not provided
        if schema_path is None:
            current_dir = Path(__file__).parent
            schema_path = current_dir / "schema.sql"

        # Load the schema
        self.schema = self._load_schema(schema_path)

        # Initialize the LLM
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0,
        )

        # Create the prompt template
        self.prompt = PromptTemplate(
            input_variables=["schema", "question"],
            template="""
            You are a database expert. You are given a SQL schema and a question about the database.
            Your task is to answer the question based ONLY on the information in the schema.
            If the question cannot be answered based on the schema, say so.

            Schema:
            {schema}

            Question: {question}

            Answer:
            """
        )

        # Create the chain using the newer RunnableSequence approach
        self.chain = (
            {"schema": lambda x: self.schema, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
        )

    def _load_schema(self, schema_path):
        """
        Load the schema from the file.

        Args:
            schema_path (str or Path): Path to the schema file.

        Returns:
            str: The content of the schema file.
        """
        with open(schema_path, 'r') as f:
            return f.read()

    def query(self, question):
        """
        Query the agent with a question about the database.

        Args:
            question (str): The question to ask about the database.

        Returns:
            str: The answer from the LLM.
        """
        response = self.chain.invoke(question)
        return response.content


if __name__ == "__main__":
    # Example usage
    agent = DatabaseAgent()

    # Example questions
    questions = [
        "What tables do we have in the database?",
        "What fields do we have in an application?",
        "How are loan applications related to applicants?",
        "Can a business have multiple loan applications?",
        "Generate sql query to get application status by user email",
    ]

    # Print answers to example questions
    for question in questions:
        print(f"Question: {question}")
        print(f"Answer: {agent.query(question)}")
        print("-" * 50)
