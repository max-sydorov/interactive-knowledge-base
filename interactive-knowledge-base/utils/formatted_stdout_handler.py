"""Callback Handler that prints to std out with proper formatting and newlines between agent logs."""

from typing import Any, Optional
from typing_extensions import override
from langchain_core.callbacks.stdout import StdOutCallbackHandler
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.utils import print_text


class FormattedStdOutCallbackHandler(StdOutCallbackHandler):
    """Callback Handler that prints to std out with proper formatting and newlines between agent logs."""

    @override
    def on_agent_action(
        self, action: AgentAction, color: Optional[str] = None, **kwargs: Any
    ) -> Any:
        """Run on agent action with added newlines.

        Args:
            action (AgentAction): The agent action.
            color (Optional[str]): The color to use for the text. Defaults to None.
            **kwargs (Any): Additional keyword arguments.
        """
        print("\n")  # Add extra newline before agent action
        print_text(action.log, color=color or self.color)
        print("\n")  # Add extra newline after agent action

    @override
    def on_tool_end(
        self,
        output: Any,
        color: Optional[str] = None,
        observation_prefix: Optional[str] = None,
        llm_prefix: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Print tool output with proper newlines.

        Args:
            output (Any): The output to print.
            color (Optional[str]): The color to use for the text. Defaults to None.
            observation_prefix (Optional[str]): The observation prefix.
                Defaults to None.
            llm_prefix (Optional[str]): The LLM prefix. Defaults to None.
            **kwargs (Any): Additional keyword arguments.
        """
        output = str(output)
        if observation_prefix is not None:
            print_text(f"\n{observation_prefix}")
        print_text(output, color=color or self.color)
        if llm_prefix is not None:
            print_text(f"\n{llm_prefix}")
        print("\n")  # Add extra newline after tool output

    @override
    def on_agent_finish(
        self, finish: AgentFinish, color: Optional[str] = None, **kwargs: Any
    ) -> None:
        """Run on the agent end with added newlines.

        Args:
            finish (AgentFinish): The agent finish.
            color (Optional[str]): The color to use for the text. Defaults to None.
            **kwargs (Any): Additional keyword arguments.
        """
        print("\n")  # Add extra newline before agent finish
        print_text(finish.log, color=color or self.color, end="\n")
        print("\n")  # Add extra newline after agent finish