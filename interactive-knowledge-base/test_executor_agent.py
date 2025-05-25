from langchain_openai import ChatOpenAI
from browser_use import Agent
from dotenv import load_dotenv
import asyncio

# Load environment variables
load_dotenv()

MODEL = "gpt-4-turbo"
TEMPERATURE = 0

"""
Agent for executing test plan.
This agent uses browser_use to automate browser interactions.
"""

llm = ChatOpenAI(model=MODEL, temperature=TEMPERATURE)

async def execute():
    task = """
    Go to http://localhost:3000/,
    submit application,
    check status after
    """

    agent = Agent(
        task=task,
        llm=llm,
    )
    result = await agent.run()
    print(result)

if __name__ == "__main__":
    asyncio.run(execute())
