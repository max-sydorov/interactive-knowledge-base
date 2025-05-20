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
SYSTEM_OVERVIEW_PATH = Path(__file__).parent / "system-overview.md"

"""
Knowledge Base Agent for answering questions about the Quick Loan Platform.
This agent uses LangChain and OpenAI to provide answers based on the system overview.
For database-related questions, it delegates to the DatabaseAgent.
"""
class KnowledgeBaseAgent:

    def __init__(self, verbose: bool = False):
        self.verbose = verbose

        # Load the system overview
        self.system_overview = self._load_system_overview(SYSTEM_OVERVIEW_PATH)

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

        # Create the system message with the system overview directly included
        self.system_message = f"""
        You are a knowledge base assistant for the Quick Loan Platform. Your task is to answer questions about the platform
        based on the system overview provided below.

        {self.system_overview}

        When answering questions:
        1. First, try to answer using ONLY the system overview.
        2. If the system overview does not provide a sufficiently detailed or definitive answer, AND the question pertains to:
            a. Database schema, tables, or fields.
            b. Specific data values, counts, or existence of records (e.g., "How many active loans?", "Does customer X have a loan?", "Can a business have multiple loan applications?").
            c. How different pieces of information are linked or structured within the system.
            d. SQL queries.
           Then, you MUST use the `query_database` tool to find the answer.
        3. Provide the answer based on the information retrieved. Do not speculate if the database can provide a factual answer.
        4. If, after consulting the overview and attempting to use the `query_database` tool (if applicable), you still don't know the answer, say so.
        """

        # Create a prompt template for the ReAct agent
        self.react_prompt = PromptTemplate.from_template(
            """
            You are a knowledge base assistant for the Quick Loan Platform. Your task is to answer questions about the platform
            based on the system overview provided below.

            {system_overview}

            TOOLS:
            ------
            You have access to the following tools:

            {tools}

            The available tool names are: {tool_names}

            To use a tool, please use the following format:
            ```
            Thought: I need to use a tool to help me answer the question.
            Action: tool_name
            Action Input: input for the tool
            ```

            The tool will respond with:
            ```
            Observation: tool response
            ```

            After using a tool or if you don't need to use a tool, you MUST respond with:
            ```
            Thought: I know the answer now.
            Final Answer: your final answer here
            ```

            Begin!

            Question: {input}
            {agent_scratchpad}
            """
        )

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

    def _load_system_overview(self, system_overview_path):
        with open(system_overview_path, 'r') as f:
            # Escape curly braces to prevent them from being interpreted as variables
            content = f.read()
            # Replace { with {{ and } with }} to escape them
            content = content.replace('{', '{{').replace('}', '}}')
            return content

    def query(self, question):
        # Use the agent executor to run the agent with the question
        response = self.agent_executor.invoke({
            "system_overview": self.system_overview,
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
