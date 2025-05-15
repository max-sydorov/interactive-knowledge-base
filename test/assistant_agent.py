import os
import asyncio
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import BaseTool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain import hub

# --- Configuration ---
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("Error: OPENAI_API_KEY not found in environment variables.")
    exit()

try:
    with open("system-overview.md", "r", encoding="utf-8") as f:
        INITIAL_CONTEXT = f.read()
except FileNotFoundError:
    print("Error: system-overview.md not found. Please create it.")
    INITIAL_CONTEXT = "No system overview context was provided."

# --- Tool Definition ---
class AskUserTool(BaseTool):
    name: str = "ask_user"
    description: str = (
        "Use this tool when you need more information or clarification from the user "
        "to answer their question based *only* on the provided context. "
        "Input should be a clear question for the user."
    )

    def _run(self, query_from_llm: str) -> str:
        print(f"\n🤖 Assistant (to User): {query_from_llm}")
        human_response = input("👤 Your response: ")
        return human_response

    async def _arun(self, query_from_llm: str) -> str:
        print(f"\n🤖 Assistant (to User): {query_from_llm}")
        human_response = await asyncio.to_thread(input, "👤 Your response: ")
        return human_response

# --- LLM and Agent Setup ---
llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY)
tools = [AskUserTool()]

# Construct the system message content
# This is where an accidental {id} might be hiding if not in INITIAL_CONTEXT
system_message_content = (
    "You are a helpful assistant. Answer questions based ONLY on the provided context. "
    "If you don't know the answer from the context, or need clarification, "
    "you MUST use the 'ask_user' tool. Do not make up information. "
    "When you have the final answer, provide it directly.\n\n"
    "STRICTLY ADHERE TO THE ReAct FORMAT when using tools.\n\n"
    f"Initial Context:\n---\n{INITIAL_CONTEXT}\n---\n\n" # INITIAL_CONTEXT is injected here
    "TOOLS:\n------\n"
    "You have access to the following tools: {tools}\n\n" # Placeholder for create_react_agent
    "To use a tool, please use the following format:\n\n"
    "Thought: Do I need to use a tool? Yes\n"
    "Action: The action to take, should be one of [{tool_names}]\n" # Placeholder for create_react_agent
    "Action Input: The input to the action\n"
    "Observation: The result of the action\n\n"
    "When you have a response to say to the Human based on thought and observation, "
    "or if you do not need to use a tool, you MUST use the format:\n\n"
    "Thought: Do I need to use a tool? No\n"
    "Final Answer: [your response here]"
)

# --- DEBUG PRINT ---
print("-" * 50)
print("DEBUG: INITIAL_CONTEXT content:")
print(INITIAL_CONTEXT)
print("-" * 50)
print("DEBUG: System message content BEFORE templating (this will be part of ChatPromptTemplate):")
print(system_message_content)
print("-" * 50)
# Check if "{id}" is in the system_message_content accidentally
if "{id}" in system_message_content and not "{{id}}" in system_message_content:
    print("WARNING: Found unescaped '{id}' in system_message_content string!")
    print("This is likely the cause of the error.")
print("-" * 50)


prompt_messages = [
    ("system", system_message_content), # The string above is used here
    MessagesPlaceholder(variable_name="chat_history", optional=True),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
]
prompt_template = ChatPromptTemplate.from_messages(prompt_messages)

# DEBUG: Print the input variables expected by the assembled prompt template
# These variables are before create_react_agent partials out "tools" and "tool_names"
print(f"DEBUG: prompt_template.input_variables (before agent processing): {prompt_template.input_variables}")
print("-" * 50)

agent = create_react_agent(llm, tools, prompt_template)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors="Check your output and make sure it conforms to the expected ReAct format. If you think you are correct, try to phrase your response differently.",
    max_iterations=5
)

# --- Main Interaction Loop ---
print("\n🤖 Assistant: Hello! I can answer questions about the system described in system-overview.md.")
print("   If I need more information, I'll ask you.")
print("   Type 'exit' to end the conversation.")

chat_history = []

while True:
    user_query = input("\n👤 You: ")
    if user_query.lower() == 'exit':
        print("🤖 Assistant: Goodbye!")
        break

    try:
        # The input dictionary for invoke should only contain keys that the agent's
        # final prompt expects (typically 'input' and 'chat_history' if used).
        # 'agent_scratchpad' is handled internally.
        # 'id' is not a standard input here.
        response = agent_executor.invoke({
            "input": user_query,
            "chat_history": chat_history
        })
        print(f"\n🤖 Assistant: {response['output']}")
        # chat_history.append(HumanMessage(content=user_query))
        # chat_history.append(AIMessage(content=response['output']))

    except Exception as e:
        print(f"An error occurred: {e}")
        # If the error persists, providing the full traceback again will be helpful.