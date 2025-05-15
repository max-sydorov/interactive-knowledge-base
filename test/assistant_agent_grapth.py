import os
import sys
import json
from typing import List, Dict, Any, Optional, TypedDict, Annotated, Literal, Union, Tuple
from pathlib import Path
from dotenv import load_dotenv

"""
Assistant Agent using ReAct LangGraph Loop

This module implements an Assistant Agent that uses a ReAct (Reasoning and Acting) pattern
with LangGraph to answer questions about the Quick Loan Platform. The agent reads the initial
context from system-overview.md and answers questions based on that context. If it needs more
information, it uses a "user" tool to get additional context from the user.

The implementation follows these steps:
1. Read the initial context from system-overview.md
2. Set up a LangGraph workflow with an agent node and a user tool node
3. Process user queries through the workflow
4. Either provide a final answer or request more information from the user
"""

# Try to import required packages
try:
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, FunctionMessage
    from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
    from langchain_core.tools import tool
    from langchain.agents.format_scratchpad import format_to_openai_function_messages
    from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
    from langgraph.graph import StateGraph, END
    from langgraph.graph.message import add_messages
except ImportError as e:
    print(f"Error: {e}")
    print("\nThis script requires the following packages:")
    print("  - langchain_openai")
    print("  - langchain_core")
    print("  - langgraph")
    print("\nPlease install them using:")
    print("  pip install langchain-openai langchain-core langgraph")
    sys.exit(1)

# Load environment variables from .env file
load_dotenv()

# Define the model to use
MODEL = "gpt-3.5-turbo"

# Define the state schema
class AgentState(TypedDict):
    messages: List[Any]
    context: str
    scratchpad: List[Any]
    intermediate_steps: List[Tuple[Any, str]]

# Function to read the initial context from system-overview.md
def read_initial_context():
    """Read the initial context from system-overview.md"""
    try:
        with open(Path(__file__).parent / "system-overview.md", "r") as f:
            return f.read()
    except Exception as e:
        print(f"Error reading system-overview.md: {e}")
        return "Error reading initial context."

# Define the user tool
@tool
def user_tool(query: str) -> str:
    """
    Tool to get more information from the user.
    Use this tool when you need additional context or clarification from the user.

    Args:
        query: The specific information or clarification needed from the user

    Returns:
        The user's response
    """
    print(f"\nAgent needs more information: {query}")
    user_response = input("Your response: ")
    return user_response

# Define the function to process the user tool in the graph
def process_user_tool(state: AgentState) -> AgentState:
    """
    Process the user tool in the graph.

    Args:
        state: The current agent state

    Returns:
        Updated agent state with user's response
    """
    # Get the action and input from the agent's response
    action = state.get("action")
    action_input = state.get("action_input", "")

    # Call the user tool
    result = user_tool(action_input)

    # Add the result to the intermediate steps
    new_state = state.copy()
    new_state["intermediate_steps"] = state.get("intermediate_steps", []) + [({"name": "user", "input": action_input}, result)]

    # Add the function call and result to the messages
    new_state["messages"] = add_messages(
        new_state["messages"],
        [
            FunctionMessage(name="user", content=result)
        ]
    )

    return new_state

# Define the tools available to the agent
tools = [user_tool]

# Define the agent function
def agent(state: AgentState) -> Dict[str, Any]:
    """
    Agent function that processes the current state and decides what to do next.
    Uses the ReAct pattern to reason about its actions.

    Args:
        state: The current agent state

    Returns:
        Next action to take
    """
    # Create the prompt template with ReAct instructions
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content="""You are an assistant for the Quick Loan Platform. 
Answer questions based ONLY on the provided context. 
If you don't have enough information to answer, use the 'user' tool to get more information.
Think step by step about what information you need and why.

Context:
{context}"""),
        MessagesPlaceholder(variable_name="messages"),
        MessagesPlaceholder(variable_name="scratchpad"),
    ])

    # Create the LLM with function calling capability
    llm = ChatOpenAI(model_name=MODEL, temperature=0)

    # Set up the agent with tools
    llm_with_tools = llm.bind_tools(tools)

    # Format the scratchpad
    if "scratchpad" not in state or not state["scratchpad"]:
        state["scratchpad"] = []

    # Format intermediate steps for the scratchpad
    if "intermediate_steps" in state and state["intermediate_steps"]:
        state["scratchpad"] = format_to_openai_function_messages(state["intermediate_steps"])

    # Create the chain
    chain = prompt | llm_with_tools | OpenAIFunctionsAgentOutputParser()

    # Run the chain
    output = chain.invoke({
        "context": state["context"],
        "messages": state["messages"],
        "scratchpad": state["scratchpad"]
    })

    # Process the output
    new_state = state.copy()

    # If the agent wants to use a tool
    if output.tool:
        # Return the tool call
        return {
            "action": output.tool,
            "action_input": output.tool_input,
            "messages": state["messages"],
            "scratchpad": state["scratchpad"],
            "intermediate_steps": state.get("intermediate_steps", [])
        }
    # If the agent has a final answer
    else:
        # Add the final answer to the messages
        new_state["messages"] = add_messages(
            new_state["messages"],
            [AIMessage(content=output.content)]
        )

        # Return the final answer
        return {
            "action": "end",
            "response": AIMessage(content=output.content),
            "messages": new_state["messages"],
            "scratchpad": new_state["scratchpad"],
            "intermediate_steps": new_state.get("intermediate_steps", [])
        }

# Define the main function
def main():
    """
    Main function to run the assistant agent.
    """
    # Read the initial context
    initial_context = read_initial_context()

    # Create the workflow
    workflow = StateGraph(AgentState)

    # Add the agent node
    workflow.add_node("agent", agent)

    # Add the user tool node - use process_user_tool instead of user_tool directly
    workflow.add_node("user", process_user_tool)

    # Define the conditional edge function
    def route_agent(state):
        # Check if the agent wants to use a tool or end
        return state["action"]

    # Add the edges with conditional routing
    workflow.add_conditional_edges(
        "agent",
        route_agent,
        {
            "user": "user",
            "end": END
        }
    )
    workflow.add_edge("user", "agent")

    # Set the entry point
    workflow.set_entry_point("agent")

    # Compile the workflow
    app = workflow.compile()

    print("\nAssistant Agent initialized!")
    print("You can now ask questions about the Quick Loan Platform.")
    print("Type 'exit' to quit.")

    while True:
        query = input("\nEnter your question: ")

        if query.lower() == 'exit':
            break

        # Initialize the state with empty scratchpad and intermediate_steps
        state = {
            "messages": [HumanMessage(content=query)],
            "context": initial_context,
            "scratchpad": [],
            "intermediate_steps": []
        }

        # Run the workflow
        for step in app.stream(state):
            if step.get("agent") is not None and step["agent"].get("action") == "end":
                # Print the final response
                print(f"\nResponse: {step['agent']['response'].content}")
                break
            # No need to handle user tool here as it's handled by process_user_tool

if __name__ == "__main__":
    main()
