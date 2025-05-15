import os
import sys
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Try to import required packages, with helpful error messages if they're missing
try:
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
    from langchain_core.pydantic_v1 import BaseModel, Field
    from langchain_core.messages import HumanMessage, AIMessage
except ImportError as e:
    print(f"Error: {e}")
    print("\nThis script requires the following packages:")
    print("  - langchain_openai")
    print("  - langchain_core")
    print("\nPlease install them using:")
    print("  pip install langchain langchain-openai langchain-core")
    sys.exit(1)

# Load environment variables from .env file
load_dotenv()

# Define the model to use
MODEL = "gpt-3.5-turbo"

class QueryAnalysisOutput(BaseModel):
    """Output schema for query analysis."""
    can_answer_from_context: bool = Field(description="Whether the query can be answered from the provided context")
    needs_decomposition: bool = Field(description="Whether the query needs to be decomposed into sub-queries")
    sub_queries: List[str] = Field(default_factory=list, description="List of sub-queries if decomposition is needed")
    missing_information: List[str] = Field(default_factory=list, description="Information missing from context that's needed to answer the query")
    tool_needed: Optional[str] = Field(default=None, description="Tool needed to retrieve additional information (None if no tool is needed)")

class LLMAgent:
    """
    A knowledge base assistant that can answer queries based on provided context,
    decompose complex queries, and retrieve additional information when needed.
    """

    def __init__(self, subject: str, initial_context: str):
        """
        Initialize the LLM Agent with a subject and initial context.

        Args:
            subject: The subject domain of the knowledge base
            initial_context: Initial information about the subject
        """
        self.subject = subject
        self.context = initial_context
        self.conversation_history = []

        # Initialize the LLM
        self.llm = ChatOpenAI(
            model_name=MODEL,
            temperature=0
        )

        # Create the query analysis prompt
        self.analysis_prompt = ChatPromptTemplate.from_template("""
        You are an assistant specialized in {subject}.

        Analyze the following query and determine:
        1. If it can be answered directly from the provided context
        2. If it needs to be decomposed into simpler sub-queries
        3. What information might be missing from the context
        4. If a specific tool is needed to retrieve additional information

        Context:
        {context}

        Query: {query}

        Respond with a JSON object that includes:
        - can_answer_from_context (boolean)
        - needs_decomposition (boolean)
        - sub_queries (list of strings, empty if no decomposition needed)
        - missing_information (list of strings, empty if no information is missing)
        - tool_needed (string or null, the name of the tool if needed)
        """)

        # Create the answer generation prompt
        self.answer_prompt = ChatPromptTemplate.from_template("""
        You are an assistant specialized in {subject}.

        Answer the following query based ONLY on the provided context. Be concise and accurate.

        Context:
        {context}

        Query: {query}

        If you cannot answer the query based on the provided context, clearly state that you don't have enough information.
        """)

        # Create the query decomposition prompt
        self.decomposition_prompt = ChatPromptTemplate.from_template("""
        You are an assistant specialized in {subject}.

        The following query is complex and needs to be broken down into simpler sub-queries:

        Query: {query}

        Break this down into 2-5 simpler sub-queries that, when answered and combined, would help answer the original query.
        List each sub-query on a new line.
        """)

    def analyze_query(self, query: str) -> Dict[str, Any]:
        """
        Analyze a query to determine if it can be answered from context,
        needs decomposition, or requires additional information.

        Args:
            query: The user's query

        Returns:
            Analysis results as a dictionary
        """
        # Create the analysis chain
        analysis_chain = (
            self.analysis_prompt 
            | self.llm 
            | JsonOutputParser(pydantic_object=QueryAnalysisOutput)
        )

        # Run the analysis
        return analysis_chain.invoke({
            "subject": self.subject,
            "context": self.context,
            "query": query
        })

    def generate_answer(self, query: str) -> str:
        """
        Generate an answer to a query based on the current context.

        Args:
            query: The user's query

        Returns:
            The generated answer
        """
        # Create the answer chain
        answer_chain = (
            self.answer_prompt 
            | self.llm 
            | StrOutputParser()
        )

        # Generate the answer
        return answer_chain.invoke({
            "subject": self.subject,
            "context": self.context,
            "query": query
        })

    def decompose_query(self, query: str) -> List[str]:
        """
        Decompose a complex query into simpler sub-queries.

        Args:
            query: The complex query to decompose

        Returns:
            List of sub-queries
        """
        # Create the decomposition chain
        decomposition_chain = (
            self.decomposition_prompt 
            | self.llm 
            | StrOutputParser()
        )

        # Get the decomposed queries
        result = decomposition_chain.invoke({
            "subject": self.subject,
            "query": query
        })

        # Split the result into individual sub-queries
        sub_queries = [q.strip() for q in result.split('\n') if q.strip()]
        return sub_queries

    def call_tool_a(self, query: str) -> str:
        """
        Mock implementation of Tool A that retrieves additional information.

        Args:
            query: The query to retrieve information for

        Returns:
            Additional information retrieved by the tool
        """
        # This is a mock implementation - in a real system, this would call an actual tool
        if "history" in query.lower():
            return f"Tool A found: The {self.subject} has a rich history dating back to the 1950s when it was first developed by researchers at MIT."
        elif "applications" in query.lower():
            return f"Tool A found: {self.subject} is widely used in fields such as healthcare, finance, transportation, and education."
        elif "limitations" in query.lower():
            return f"Tool A found: The main limitations of {self.subject} include high computational requirements, potential for bias, and challenges with interpretability."
        else:
            return f"Tool A found: Additional information about {self.subject} related to {query}."

    def process_query(self, query: str) -> str:
        """
        Process a user query and generate a response.

        Args:
            query: The user's query

        Returns:
            The final response
        """
        print(f"\nProcessing query: {query}")

        # Add the query to conversation history
        self.conversation_history.append(HumanMessage(content=query))

        # Analyze the query
        analysis = self.analyze_query(query)
        print(f"Query analysis: {analysis}")

        # If the query can be answered directly from context
        if analysis["can_answer_from_context"]:
            answer = self.generate_answer(query)
            self.conversation_history.append(AIMessage(content=answer))
            return answer

        # If the query needs decomposition
        if analysis["needs_decomposition"]:
            print("Decomposing query...")
            sub_queries = self.decompose_query(query)

            # Process each sub-query
            sub_answers = []
            for sub_query in sub_queries:
                print(f"Processing sub-query: {sub_query}")
                sub_answer = self.process_query(sub_query)
                sub_answers.append(f"Sub-query: {sub_query}\nAnswer: {sub_answer}")

            # Combine sub-answers into the context
            sub_answers_text = "\n\n".join(sub_answers)
            self.context += f"\n\nAdditional information from sub-queries:\n{sub_answers_text}"

            # Generate final answer with updated context
            final_answer = self.generate_answer(query)
            self.conversation_history.append(AIMessage(content=final_answer))
            return final_answer

        # If a tool is needed
        if analysis["tool_needed"]:
            print(f"Calling tool: {analysis['tool_needed']}")
            tool_result = self.call_tool_a(query)

            # Add tool result to context
            self.context += f"\n\n{tool_result}"

            # Generate answer with updated context
            answer = self.generate_answer(query)
            self.conversation_history.append(AIMessage(content=answer))
            return answer

        # If clarification is needed
        if analysis["missing_information"]:
            missing_info = ", ".join(analysis["missing_information"])
            clarification_request = f"I need more information to answer your question. Specifically, could you provide details about: {missing_info}?"
            self.conversation_history.append(AIMessage(content=clarification_request))
            return clarification_request

        # Default case - generate best possible answer with current context
        answer = self.generate_answer(query)
        self.conversation_history.append(AIMessage(content=answer))
        return answer

def main():
    """
    Main function to demonstrate the LLM Agent.
    """
    # Define a subject and initial context
    subject = "Artificial Intelligence"
    initial_context = """
    Artificial Intelligence (AI) refers to the simulation of human intelligence in machines that are programmed to think like humans and mimic their actions. The term may also be applied to any machine that exhibits traits associated with a human mind such as learning and problem-solving.

    The ideal characteristic of artificial intelligence is its ability to rationalize and take actions that have the best chance of achieving a specific goal. Machine learning, a subset of AI, is based on the idea that machines should be able to learn and adapt through experience.

    Deep learning is a subset of machine learning that has networks capable of learning unsupervised from data that is unstructured or unlabeled.
    """

    # Initialize the LLM Agent
    agent = LLMAgent(subject, initial_context)

    print(f"\nLLM Agent initialized for subject: {subject}")
    print("You can now ask questions about Artificial Intelligence.")
    print("Type 'exit' to quit.")

    while True:
        query = input("\nEnter your question: ")

        if query.lower() == 'exit':
            break

        print("\nGenerating response...")
        answer = agent.process_query(query)
        print(f"\nResponse: {answer}")

if __name__ == "__main__":
    main()
