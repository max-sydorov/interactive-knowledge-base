from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.agents import tool
from langchain.agents import AgentExecutor
from langchain.agents.react.agent import create_react_agent
from database_agent import DatabaseAgent
from backend_agent import BackendAgent
from frontend_agent import FrontendAgent
from database_executor import DatabaseExecutor
from utils.formatted_stdout_handler import FormattedStdOutCallbackHandler

# Load environment variables
load_dotenv()

MODEL = "gpt-4-turbo"
TEMPERATURE = 0
TOP_P = 0 # enforces nucleus sampling with no randomness — it’s a stricter form of deterministic generation
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

        # Initialize the BackendAgent
        self.backend_agent = BackendAgent()

        # Initialize the FrontendAgent
        self.frontend_agent = FrontendAgent()

        # Initialize the DatabaseExecutor
        self.db_executor = DatabaseExecutor()

        # Initialize the LLM
        self.llm = ChatOpenAI(model=MODEL, temperature=TEMPERATURE, top_p=TOP_P)

        # Define the database query tool
        @tool
        def query_database(question: str) -> str:
            """Use this tool for any questions related to database schema, tables, fields, or SQL queries."""
            return self.db_agent.query(question)

        # Define the backend query tool
        @tool
        def query_backend(question: str) -> str:
            """Use this tool for any questions related to the backend service, APIs, application submission process, or Java implementation details."""
            return self.backend_agent.query(question)

        # Define the frontend query tool
        @tool
        def query_frontend(question: str) -> str:
            """Use this tool for any questions related to the frontend UI, pages, components, forms, validation, or TypeScript implementation details."""
            return self.frontend_agent.query(question)

        # Define the database execution tool
        @tool
        def execute_database(query: str) -> str:
            """Use this tool to execute SQL queries against the PostgreSQL database and get the results. 
            Provide the SQL query as input. Be careful with destructive operations (DELETE, DROP, etc.)."""
            return self.db_executor.execute_query(query)

        self.tools = [query_database, query_backend, query_frontend, execute_database]

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
        "How does our application submission process work?",
        "What tables do we have in the database? Provide columns and types for each table.",
        "Generate sql query to get application status by user email",
        "Can a business have multiple loan applications?",
        "Where to find the status of an application?",
        "What APIs do we have? Provide url, request and response payloads in json format.",
        "What validation do we have for the Phone field?",
        "How is user data validated in the application?",
        "What pages do we have on UI? Provide content of each page.",
        "What application fields do we ask?",
        "What is the status of an application for Wilma Mason?",
        "Understand decline logic on the backend. Find the application id for Wilma Mason. Pull necessary application data by applicaiton id. Explain why it was declined.",
        "Generate an e2e test plan to test the declining flow. Provide steps and expected results.",
        "Step 1. Get a list of application fields we ask on UI during app intake."
        "Step 2. Find how UI passes each field value to the backend."
        "Step 3. Find in which table and column backend persist each field value."
        "Step 4. Return a list of UI fields mapped to the database table and column."
    ]

    # Print answers to example questions
    for question in questions:
        print(f"Question: {question}")
        print(f"Answer: {agent.query(question)}")
        print("-" * 100)
