"""Slash commands of the chat."""
from pathlib import Path

from .colors import GRAY, GREEN, RED, RESET, YELLOW
from .core import Agent, Config
from .core.session import SessionLog, list_sessions, search

COMMANDS = [
    ("/help", "show this help"),
    ("/models", "list model profiles"),
    ("/model <name>", "switch model (history is kept)"),
    ("/reset", "clear history"),
    ("/usage", "show token usage"),
    ("/history", "recent sessions"),
    ("/search <words>", "search questions in all sessions"),
    ("empty line", "exit"),
]

def short(path: Path) -> str:
    return str(path).replace(str(Path.home()), "~", 1)

def print_models(config: Config, current: str | None = None) -> None:
    for name, m in config.models.items():
        marks = []
        if name == config.default_model:
            marks.append("by default")
        if name == current:
            marks.append("current")
        suffix = f"  ({', '.join(marks)})" if marks else ""
        print(f"  {name:<10} {m.model}{suffix}")

def show_help() -> None:
    print(f"{GRAY}Available commands:{RESET}")
    for cmd, desc in COMMANDS:
        print(f"  {YELLOW}{cmd:<15}{RESET} {GRAY}{desc}{RESET}")

def handle_command(text: str, agent: Agent, session: SessionLog) -> None:
    cmd, _, arg = text.partition(" ") # "/model local" -> cmd="/model", arg="local"
    arg = arg.strip()

    if cmd == "/help":
        show_help()
    elif cmd == "/models":
        print_models(agent.config, agent.llm.name)
    elif cmd == "/model" and arg:
        try:
            agent.set_model(arg)
            session.log_event("model", f"Switched to {agent.llm.name}", name=agent.llm.name, model=agent.llm.model)
            print(f"{GRAY}Model:{RESET} {YELLOW}{agent.llm.name}{RESET} {GREEN}({agent.llm.model}){RESET}\n")
        except KeyError as e:
            print(f"{RED}{e.args[0]}{RESET}\n")
    elif cmd == "/reset":
        agent.reset()
        session.log_event("reset", "History cleared")
        print("History cleared.\n")
    elif cmd == "/usage":
        s = agent.session_tokens
        print(f"{GRAY}Session:{RESET} ↑ {s['in']:,} in, ↓ {s['out']:,} out, total {s['in'] + s['out']:,}")
    elif cmd == "/history":
        for i, s in enumerate(list_sessions(), 1):
            print(f"  {GRAY}{i:>2}. {s.date}{RESET}  {s.title}")
            print(f"      {GRAY}{s.path}{RESET}")
    elif cmd == "/search" and arg:
        hits = search(arg)
        if not hits:
            print(f"{GRAY}Nothing found.{RESET}")
        for h in hits:
            print(f"  {GRAY}{h.date}{RESET}  {YELLOW}❯{RESET} {h.question}")
            print(f"      {GRAY}{short(h.path)}:{h.line_no}{RESET}")
    else:
        show_help()
