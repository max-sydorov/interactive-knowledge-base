import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import BaseTool, Tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain import hub

# --- Configuration ---
# 1. Load environment variables (for API keys)
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("Error: OPENAI_API_KEY not found in environment variables.")
    print("Please set it in a .env file or directly in your environment.")
    exit()

# 2. Read the initial context from system-overview.md
def read_initial_context():
    try:
        # Look for the file in the test directory
        with open("test/system-overview.md", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print("Error: system-overview.md not found in test directory.")
        return "No system overview context was provided."

INITIAL_CONTEXT = read_initial_context()

# --- Tool Definition ---
class UserTool(BaseTool):
    name: str = "user"
    description: str = (
        "Use this tool when you need more information or clarification from the user "
        "to answer their question based *only* on the provided context. "
        "Input should be a clear question for the user."
    )

    def _run(self, query_from_llm: str) -> str:
        """
        Prompts the human user for input.
        The LLM's question (query_from_llm) is shown to the user.
        """
        print(f"\n🤖 Assistant (to User): {query_from_llm}")
        human_response = input("👤 Your response: ")
        return human_response

    async def _arun(self, query_from_llm: str) -> str:
        """Asynchronous version"""
        import asyncio
        print(f"\n🤖 Assistant (to User): {query_from_llm}")
        human_response = await asyncio.to_thread(input, "👤 Your response: ")
        return human_response

# --- LLM and Agent Setup ---
llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY)

tools = [UserTool()]

# Create a prompt template for the ReAct agent
prompt_messages = [
    ("system",
     "You are a helpful assistant. Answer questions based ONLY on the provided context. "
     "If you don't know the answer from the context, or need clarification, "
     "you MUST use the 'user' tool. Do not make up information. "
     "When you have the final answer, provide it directly without 'Final Answer:' prefix, "
     "unless the ReAct thought process requires it to stop generation.\n\n"
     "STRICTLY ADHERE TO THE ReAct FORMAT when using tools.\n\n"
     f"Initial Context:\n---\n{INITIAL_CONTEXT}\n---\n\n"
     "TOOLS:\n------\n"
     "You have access to the following tools: {tools}\n\n"
     "To use a tool, please use the following format:\n\n"
     "Thought: Do I need to use a tool? Yes\n"
     "Action: The action to take, should be one of [{tool_names}]\n"
     "Action Input: The input to the action\n"
     "Observation: The result of the action\n\n"
     "When you have a response to say to the Human based on thought and observation, "
     "or if you do not need to use a tool, you MUST use the format:\n\n"
     "Thought: Do I need to use a tool? No\n"
     "Final Answer: [your response here]"
    ),
    MessagesPlaceholder(variable_name="chat_history", optional=True),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
]
prompt_template = ChatPromptTemplate.from_messages(prompt_messages)

# Create the ReAct agent
agent = create_react_agent(llm, tools, prompt_template)

# Create the agent executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors="Check your output and make sure it conforms to the expected ReAct format.",
    max_iterations=5
)

# --- Main Interaction Loop ---
def main():
    print("🤖 Assistant: Hello! I can answer questions about the system described in the context.")
    print("   If I need more information, I'll ask you.")
    print("   Type 'exit' to end the conversation.")

    while True:
        user_query = input("\n👤 You: ")
        if user_query.lower() == 'exit':
            print("🤖 Assistant: Goodbye!")
            break

        try:
            # The agent_executor.invoke will handle the loop, including tool calls
            # Adding 'id' parameter as required by the prompt template
            response = agent_executor.invoke({
                "input": user_query,
                "id": "conversation_" + str(hash(user_query))  # Generate a unique ID for each query
            })
            # The actual response is in the 'output' key
            print(f"\n🤖 Assistant: {response['output']}")

        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
