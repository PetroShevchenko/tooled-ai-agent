#!/usr/bin/env python3

"""Entry point: interaction with an agent at the terminal.

Run:
    ./tooled                  # model by default ([llm] default)
    ./tooled -m local         # profile [models.local]
    ./tooled --list           # show all profiles
    ./tooled -c other.toml    # another setting file
    AGENT_MODEL=pro ./tooled  # profile through environment variable

Chat commands:
    /help           — show help message
    /models         — profile list
    /model <name>   — switch model (stored history)
    /reset          — reset history
    /usage          — show token usage
    /history        — recent sessions
    /search <words> — search questions in all sessions
    empty lines     — exit
"""

import argparse
import shutil
import time
from pathlib import Path
from datetime import datetime
from importlib import resources
from platformdirs import user_config_dir

from .core import Agent, Config, ToolRegistry
from .core.session import SessionLog, list_sessions, search
from .commands import COMMANDS, handle_command, print_models
from .colors import RESET, BOLD, RED, GREEN, DARK_GREEN, YELLOW, BLUE, CYAN, GRAY 
print(f"{GRAY}Loading LLM library...{RESET}\n", flush=True)

from .tools import CalculatorTool, CurrentTimeTool

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Simple AI agent")
    parser.add_argument("-c", "--config",
                    help="config file (default: ~/.config/tooled-ai-agent/config.toml)")
    parser.add_argument("-m", "--model", help="profile name from config.toml")
    parser.add_argument("--list", action="store_true", help="show model profiles and exit")
    return parser.parse_args()

def config_path(cli_path: str | None) -> Path:
    """Config from -c, otherwise ~/.config/tooled-ai-agent/config.toml.
    Creates it from the built-in template on first run."""
    if cli_path:
        return Path(cli_path)
    path = Path(user_config_dir("tooled-ai-agent", appauthor=False)) / "config.toml"
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        template = resources.files("tooled_ai_agent") / "default_config.toml"
        with resources.as_file(template) as src:
            shutil.copy(src, path)
        print(f"{GRAY}Created default config: {path}{RESET}")
    return path

def separator() -> None:
    width = shutil.get_terminal_size().columns
    stamp = datetime.now().strftime("%H:%M:%S")
    print(f"\n{GRAY}{'─' * (width - len(stamp) - 2)} {stamp}{RESET}")

def read_input() -> str | None:
    """Reads a user request.

        Returns the entered text, or None if the user wishes to exit
        (Ctrl+D, or Ctrl+C pressed twice within 2 seconds).
        A single Ctrl+C discards the typed line and prompts for input again.
    """
    last_interrupt = 0.0
    while True:
        try:
            separator()
            return input(f"{BOLD}{GREEN}❯{RESET} ").strip()
        except EOFError: # Ctrl+D — exit
            print()
            return None
        except KeyboardInterrupt: # Ctrl+C
            now = time.monotonic()
            if now - last_interrupt < 2: # second time in 2 seconds — exit
                print()
                return None
            last_interrupt = now
            print(f"\n{GRAY}(press Ctrl+C again to exit){RESET}")

def main():
    args = parse_arguments()
    config = Config.load(config_path(args.config))

    if args.list:
        print_models(config)
        return

    try:
        tools = ToolRegistry([CalculatorTool(), CurrentTimeTool()])
        agent = Agent(config, tools, model=args.model)
        session = SessionLog(agent.llm.name, agent.llm.model)
        agent.session = session
    except KeyError as e:
        sys.exit(f"{RED}{BOLD}Error: {e.args[0]}{RESET}")

    print(f"{GRAY}Model:{RESET} {BOLD}{YELLOW}{agent.llm.name}{RESET} {GRAY}({agent.llm.model}){RESET}")
    print(f"{GRAY}Type {YELLOW}/help{GRAY} for commands, empty line to exit.{RESET}")

    while True:
        task = read_input()
        if not task:
            break

        if task.startswith("/"):
            handle_command(task, agent, session)
            continue

        try:
            session.log_user(task)
            answer = agent.run(task).strip().replace("\n", "\n  ")
            print(f"\n{CYAN}●{RESET} {answer}")
            t = agent.last_tokens
            session.log_answer(answer, t["in"], t["out"])
            print(f"  {GRAY}↑ {t['in']:,} ↓ {t['out']:,} tokens{RESET}")
        except KeyboardInterrupt:
            session.log_event("cancelled", "Request cancelled")
            print(f"\n{YELLOW}Request cancelled.{RESET}")
            continue
        except Exception as e:
            session.log_event("error", f"Error: {e}")
            print(f"{RED}Error:{RESET} {e}\n")

    if session.md_path:
        print(f"{GRAY}Saved: {session.md_path}{RESET}")   

if __name__ == "__main__":
	main()
