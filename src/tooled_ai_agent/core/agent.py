"""Agent: agent cycle + conversation history."""

from __future__ import annotations

import json
from typing import Any

from ..colors import GRAY, RED, RESET
from ..spinner import Spinner
from .config import Config, LLMConfig
from .session import SessionLog
from .tool import ToolRegistry


class Agent:
    """LLM agent with tools.

    Cycle:
        the model responds -> if it requests a tool, we execute it and return
        the result -> repeat until the model provides a text response.
    """

    def __init__(self, config: Config, tools: ToolRegistry, model: str | None = None) -> None:
        self.config = config
        self.tools = tools
        self.llm: LLMConfig = config.get_model(model)
        self.messages: list[dict[str, Any]] = []
        self.session_tokens = {"in": 0, "out": 0}
        self.last_tokens = {"in": 0, "out": 0}
        self.session: SessionLog | None = None
        self.reset()

    # ----------------------------------------------------
    # public methods
    # ----------------------------------------------------

    def set_model(self, name: str) -> None:
        """Switches the model. Conversation history is preserved."""
        self.llm = self.config.get_model(name)

    def reset(self) -> None:
        """Clears the history, leaving the system prompt."""
        self.messages = [{"role": "system", "content": self.config.agent.system_prompt}]

    def run(self, task: str) -> str:
        """Performs a single user task and returns the final response."""
        self.last_tokens = {"in": 0, "out": 0}
        start = len(self.messages)  # remember history state
        self.messages.append({"role": "user", "content": task})

        try:
            for step in range(1, self.config.agent.max_steps + 1):
                with Spinner("Thinking"):
                    msg = self._call_llm()
                # We must save the model's response in the history.
                self.messages.append(msg.model_dump(exclude_none=True))

                if not msg.tool_calls:
                    return msg.content or ""

                for call in msg.tool_calls:
                    self._handle_tool_call(step, call)

            return f"{RED}Stopped: step limit exceeded.{RESET}"
        except BaseException:
            del self.messages[start:]  # remove not finished exchange
            raise

    # ----------------------------------------------------
    # internal methods
    # ----------------------------------------------------

    def _call_llm(self) -> Any:
        from litellm import completion

        llm = self.llm
        params: dict[str, Any] = {
            "model": llm.model,
            "messages": self.messages,
            "tools": self.tools.schemas(),
            **llm.extra,
        }
        if llm.temperature is not None:
            params["temperature"] = llm.temperature

        response = completion(**params)

        usage = getattr(response, "usage", None)  # calculate token usage
        if usage:
            for key, value in (("in", usage.prompt_tokens), ("out", usage.completion_tokens)):
                self.last_tokens[key] += value or 0
                self.session_tokens[key] += value or 0

        return response.choices[0].message

    def _handle_tool_call(self, step: int, call: Any) -> None:
        name = call.function.name
        try:
            args = json.loads(call.function.arguments or "{}")
        except json.JSONDecodeError:
            args = {}
            result = f"{RED}Error: arguments are not valid JSON{RESET}"
        else:
            result = self.tools.execute(name, args)

        if self.config.agent.verbose:
            print(f"  {GRAY}⎿ {name}({args}) → {result}{RESET}")
            if self.session:
                self.session.log_tool(name, args, result)

        # tool_call_id links the result to a specific call.
        self.messages.append({"role": "tool", "tool_call_id": call.id, "content": result})
