from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.agents import tool
from langchain.agents import AgentExecutor
from langchain.agents.react.agent import create_react_agent
from database_agent import DatabaseAgent
from utils.formatted_stdout_handler import FormattedStdOutCallbackHandler

# Load environment variables
load_dotenv()

MODEL = "gpt-4-turbo"
TEMPERATURE = 0
AGENT_PROMPT_PATH = Path(__file__).parent / "knowledge_base_agent_prompt.md"

"""
Knowledge Base Agent for answering questions about the Quick Loan Platform.
This agent uses LangChain and OpenAI to provide answers based on the system overview.
For database-related questions, it delegates to the DatabaseAgent.
"""
class KnowledgeBaseAgent:

    def __init__(self, verbose: bool = False):
        self.verbose = verbose

        # Load the agent prompt
        self.agent_prompt = self._load_agent_prompt(AGENT_PROMPT_PATH)

        # Initialize the DatabaseAgent
        self.db_agent = DatabaseAgent()

        # Initialize the LLM
        self.llm = ChatOpenAI(model=MODEL, temperature=TEMPERATURE)

        # Define the database query tool
        @tool
        def query_database(question: str) -> str:
            """Use this tool for any questions related to database schema, tables, fields, or SQL queries."""
            return self.db_agent.query(question)

        self.tools = [query_database]

        # Create a prompt template for the ReAct agent using the loaded prompt
        self.react_prompt = PromptTemplate.from_template(self.agent_prompt)

        # Create a ReAct agent with tools
        self.agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.react_prompt
        )

        # Create an agent executor with custom callback handler for better log formatting
        callbacks = [FormattedStdOutCallbackHandler()] if verbose else []
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=verbose,
            handle_parsing_errors=True,
            max_iterations=10,  # Limit the number of iterations to prevent infinite loops
            max_execution_time=60,  # Limit execution time to 60 seconds
            callbacks=callbacks
        )


    def _load_agent_prompt(self, agent_prompt_path):
        with open(agent_prompt_path, 'r') as f:
            # Read the content without escaping curly braces
            # since we want to keep the template variables
            return f.read()

    def query(self, question):
        # Use the agent executor to run the agent with the question
        response = self.agent_executor.invoke({
            "input": question
        })

        # Return the output from the agent
        return response["output"]


if __name__ == "__main__":
    # Example usage
    agent = KnowledgeBaseAgent(verbose = True)

    # Example questions
    questions = [
        "What is the Quick Loan Platform?",
        "How does the application process work?",
        "What tables do we have in the database?",
        "Can a business have multiple loan applications?",
        "How to submit an application? Where to find the status of an application?",
        "Generate sql query to get application status by user email",
    ]

    # Print answers to example questions
    for question in questions:
        print(f"Question: {question}")
        print(f"Answer: {agent.query(question)}")
        print("-" * 100)
