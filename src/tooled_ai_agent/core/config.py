"""Load settings from config.toml."""

from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class LLMConfig:
    """One model profile from section [models.<name>]."""

    name: str  # short profile name, ex. "flash"
    model: str  # name for LiteLLM, ex. "vertex_ai/gemini-3.8-flash"
    temperature: float | None = None
    extra: dict[str, Any] = field(default_factory=dict)  # extra parameters for litellm


@dataclass
class AgentConfig:
    max_steps: int = 10
    verbose: bool = True
    system_prompt: str = "You are a helpful assistant."


@dataclass
class Config:
    models: dict[str, LLMConfig]  # all profiles: name -> settings
    default_model: str  # default profile name
    agent: AgentConfig

    @classmethod
    def load(cls, path: str | Path = "config.toml") -> Config:
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {path.resolve()}")

        with path.open("rb") as f:
            data = tomllib.load(f)

        models_data = data.get("models", {})
        if not models_data:
            raise ValueError("There is no [models.<name>] profile in config.toml.")

        models: dict[str, LLMConfig] = {}
        for name, m in models_data.items():
            if "model" not in m:
                raise ValueError(
                    f"The `model` parameter is missing in the `[models.{name}]` profile."
                )
            models[name] = LLMConfig(
                name=name,
                model=m["model"],
                temperature=m.get("temperature"),
                extra=m.get("extra", {}),
            )

        # Default: [llm] default, otherwise the first profile in the file.
        default = data.get("llm", {}).get("default", next(iter(models)))
        if default not in models:
            raise ValueError(
                f"[llm] default = '{default}', but there is no such profile. "
                f"Available: {', '.join(models)}"
            )

        agent_data = data.get("agent", {})
        agent = AgentConfig(
            max_steps=agent_data.get("max_steps", 10),
            verbose=agent_data.get("verbose", True),
            system_prompt=agent_data.get("system_prompt", AgentConfig.system_prompt).strip(),
        )
        return cls(models=models, default_model=default, agent=agent)

    def get_model(self, name: str | None = None) -> LLMConfig:
        """Returns model profile

        Selection order:
            argument name -> AGENT_MODEL environment variable -> [llm] (default).
        """
        name = name or os.getenv("AGENT_MODEL") or self.default_model
        if name not in self.models:
            raise KeyError(
                f"There is no profile for model '{name}'. Available: {', '.join(self.models)}"
            )
        return self.models[name]
