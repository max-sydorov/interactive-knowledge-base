from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain.agents import tool
from langchain.agents import AgentExecutor, create_openai_tools_agent
from database_agent import DatabaseAgent

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

    def __init__(self):
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
        system_message = f"""
        You are a knowledge base assistant for the Quick Loan Platform. Your task is to answer questions about the platform
        based on the system overview provided below. If the question is related to the database schema, tables, fields, or SQL queries,
        use the query_database tool to get the answer.

        System Overview:
        {self.system_overview}

        Answer the question based on the system overview. If you don't know the answer, say so.
        If the question is about database schema, tables, fields, or SQL queries, use the query_database tool.
        """

        # Create the prompt template with the system message and user input
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_message),
            ("human", "{input}"),
            ("human", "{agent_scratchpad}")
        ])

        # Create an agent with tools
        self.agent = create_openai_tools_agent(self.llm, self.tools, self.prompt)

        # Create an agent executor with a partial to include system_overview
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=False,
            handle_parsing_errors=True
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
            "input": question
        })

        # Return the output from the agent
        return response["output"]


if __name__ == "__main__":
    # Example usage
    agent = KnowledgeBaseAgent()

    # Example questions
    questions = [
        "What is the Quick Loan Platform?",
        "How does the application process work?",
        "What tables do we have in the database?",
        "What fields do we have in an application?",
        "Can a business have multiple loan applications?",
    ]

    # Print answers to example questions
    for question in questions:
        print(f"Question: {question}")
        print(f"Answer: {agent.query(question)}")
        print("-" * 100)
