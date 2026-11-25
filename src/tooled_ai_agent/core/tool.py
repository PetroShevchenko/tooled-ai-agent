"""Agent tool: base class, registry."""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any

from ..colors import RESET, BOLD, RED, GREEN, YELLOW, BLUE, CYAN, GRAY

class Tool(ABC):
    """Base class for a tool.

    To add a new tool, inherit from this class and define:
      name        — the name visible to the model
      description — when and why it should be called (the model sees ONLY this)
      parameters  — JSON Schema for the arguments
      run()       — the actual logic; returns a string
    """
    name: str
    description: str
    parameters: dict[str, Any]

    @abstractmethod
    def run(self, **kwargs: Any) -> str: ...

    def schema(self) -> dict[str, Any]:
        """Tool description in a format understood by an LLM (OpenAI tools)."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }

class ToolRegistry:
    """Stores tools and executes them by name."""

    def __init__(self, tools: list[Tool] | None = None) -> None:
        self._tools: dict[str, Tool] = {}
        for tool in tools or []:
            self.register(tool)

    def register(self, tool: Tool) -> None:
        if tool.name in self._tools:
            raise ValueError(f"{YELLOW}The tool '{tool.name}' is already registered{RESET}")
        self._tools[tool.name] = tool

    def schemas(self) -> list[dict[str, Any]]:
        return [t.schema() for t in self._tools.values()]

    def execute(self, name: str, args: dict[str, Any]) -> str:
        tool = self._tools.get(name)
        if tool is None:
            return f"{RED}Error: unknown tool '{name}'{RESET}"
        try:
            return tool.run(**args)
        except Exception as e:
            # We return the error to the model as text—it will attempt to correct itself.
            return f"{RED}Execution error {name}: {e}{RESET}"
