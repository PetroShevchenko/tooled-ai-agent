# Course: your first AI agent

Welcome to my course on building your own AI agent.
This course is for anyone who wants to understand, for the first time, how an
AI agent works and write their own tools for it.

Throughout the course we go top-down: first we learn to use the ready-made
`tooled-ai-agent`, then we look at how it works inside, extend it, and finally
prepare it for real-world tasks.

!!! important
    **Prerequisites:**

    - Python basics (functions, classes, dictionaries)
    - Working in a terminal (bash, PowerShell)

<a id="lesson-code"></a>

!!! note
    **How to use the lesson code:** every lesson has a git tag `lesson-NN` that
    pins the code as of that lesson. The latest version is always in `main`.

```bash
git checkout lesson-01    # code of lesson 1
git checkout main         # full version
```

!!! warning
    `git checkout lesson-01` puts the repository into a detached HEAD state.
    If the folder has uncommitted changes, stash them while you look at the lesson:
```bash
git stash          # put your changes aside
git checkout lesson-01
# ... look at the lesson code ...
git checkout main  # go back
git stash pop      # restore your changes
```

!!! note
    The **"Used later"** note shows where a tool or technique will be reused
    in real agents: a Git assistant and an SDD framework.

---

## Part 1. The user

### [Lesson 1. Installation and first run](lessons/01-installation-and-first-run.md)

**Goal:** install the agent, connect a language model and ask the first question.

- Installing as a regular command with `pipx`
- Installing on your platform:
    - **Linux / macOS:** the `install.sh` and `env.sh` scripts
    - **Windows (recommended):** WSL2 (`wsl --install`), then the same as Linux
    - **Windows without WSL:** plain Python commands in PowerShell (`python -m venv`, `pip install -e .`)
- Connecting a model: free (Ollama) or cloud (Vertex AI, API key)
- The first request
- Commands: `/help`, `/models`, `/model`, `/usage`, `/history`, `/search`

**Practice:** ask the agent 3–4 questions, find one of them with `/search`
and open the saved conversation as an `.md` file.

### [Lesson 2. How the agent talks to the model](lessons/02-how-the-agent-talks-to-the-model.md) 🚧

**Goal:** understand what happens during a single model call.

- Project structure
- `config.toml`: where it comes from, how to change it, model profiles
- The `completion()` call and message roles: `system`, `user`, `assistant`
- Tokens, `temperature`, thinking mode and why it affects speed
- Local vs cloud models: speed, quality, cost

**Practice:** add your own model profile, compare two models' answers
to the same question and the difference in `/usage`.

---

## Part 2. How the agent works

### [Lesson 3. Tools (tool calling)](lessons/03-tools-tool-calling.md) 🚧

**Goal:** understand how a model "uses" tools without running any code.

- The model only *asks* for a function call; our code runs it
- Describing a tool with JSON Schema
- The `Tool` class and the `ToolRegistry`
- A walk through the `calculator` tool
- Why every tool description costs tokens in *every* request
- The `/debug` command: raw requests and responses

**Practice:** use `/debug` to find the moment the model asks for the calculator
and the moment it receives the result.

### [Lesson 4. The agent loop](lessons/04-the-agent-loop.md) 🚧

**Goal:** take apart the heart of the agent: the "model → tool → model" loop.

- The `run()` method and the `max_steps` limit
- `tool_call_id` and several calls in one step
- Tool errors are returned to the model
- Conversation history as "memory": why tokens grow with every step, why `/reset`

**Practice:** give the agent a task that needs 3+ steps and watch the history
grow in `/debug`. Set `max_steps = 1` and see what changes.

---

## Part 3. Extending the agent

### [Lesson 5. Your first tool](lessons/05-your-first-tool.md) 🚧

**Goal:** write your own tool and connect it to the agent.

- The `current_time` tool step by step
- Why the `description` matters more than the code
- The tool result is read by the model, not a human: short plain text, no colors
- Testing a tool with `pytest`

**Practice:** write `exchange_rate` (the open National Bank of Ukraine API)
or `get_weather` (Open-Meteo) on your own.

### [Lesson 6. Reading and searching files](lessons/06-reading-and-searching-files.md) 🚧

**Goal:** let the agent find its way around project files safely.

- `list_files` (like `ls`), `read_file` (like `cat`)
- `find_files` — find files by name pattern (like `find`)
- `search_files` — search text inside files (like `grep -r`)
- Sandboxing: access to the working directory only (`safe_path`)
- Size limits, binary files, ignored folders (`.git`, `.venv`)

**Used later:** the Git assistant needs to understand code before changing it;
SDD needs to find where to implement each task.

**Practice:** ask the agent to find every place where `ToolRegistry` is used
and to explain how `tooled-ai-agent` works.

### [Lesson 7. Changing files, safety and confirmation](lessons/07-changing-files-safety-and-confirmation.md) 🚧

**Goal:** let the agent change files while you stay in control.

- `write_file` — create or overwrite a file
- `edit_file` — replace a fragment instead of rewriting the whole file
- Confirmation: show a diff and ask `[y/n/d]`
- Cancelling a request (Ctrl+C) and rolling back the history
- Prompt injection: why data from files and the web is untrusted text
- A Docker container as a sandbox: the agent sees only the working directory
  and cannot damage files outside it; runs on any OS

**Used later:** confirmation is the safety basis of the Git assistant;
`edit_file` is the main tool for implementing tasks in SDD.

**Practice:** try to "trick" the agent through the contents of a file and make sure
the confirmation step protects you. Then run the agent in a container
and check that files outside the working directory are out of its reach.

### [Lesson 8. Running commands and tests](lessons/08-running-commands-and-tests.md) 🚧

**Goal:** let the agent run commands without losing control.

- `run_command`: an allow list, confirmation, a timeout
- Trimming long output: the first and last lines instead of thousands
- `run_tests`: run `pytest` and return a short summary (passed, failed and why)
- Masking secrets: tokens and passwords must reach neither the model
  nor the session archive

**Used later:** the Git assistant runs git commands and analyses CI logs;
SDD checks every task with tests.

**Practice:** ask the agent to run the project's tests, find why one fails
(break a test on purpose) and suggest a fix.

### [Lesson 9. System prompt, agent profiles and memory](lessons/09-system-prompt-agent-profiles-and-memory.md) 🚧

**Goal:** turn one engine into different agents.

- How the system prompt changes behaviour
- Agent profiles with `--agent`: its own prompt and its own set of tools
  (fewer tools — fewer tokens and fewer wrong choices)
- Long-term memory: the `remember` / `recall` tools

**Practice:** create your own profile, for example a "translator"
or a "code reviewer", with only the tools it needs.

### [Lesson 10. Planning inside the agent loop](lessons/10-planning-inside-the-agent-loop.md) 🚧

**Goal:** teach the agent to ask and plan instead of guessing.

- `ask_user` — the agent asks a clarifying question in the middle of its work
- `todo_add` / `todo_update` / `todo_list` — the agent keeps a task list
  and ticks off finished items, as coding agents do
- When to ask the user and when to decide alone

**Used later:** SDD's requirement-clarification phase and task list;
the Git assistant asks before risky actions.

**Practice:** give the agent a vague task ("make a currency rate tool")
and see which questions it asks and how it splits the work into steps.

---

## Part 4. Preparing for real-world tasks

### [Lesson 11. Reliability](lessons/11-reliability.md) 🚧

**Goal:** the agent must not crash or hang because of model failures.

- A request timeout instead of waiting forever
- Retries on temporary errors (network, overload)
- Fallback models: switch to another model when a limit is reached (`litellm.Router`)
- Why free tiers run out quickly in agent mode

**Used later:** both agents — long tasks must not stop because of a single failure.

**Practice:** set up a chain of fallback models and simulate a failure of the main one
(for example, a wrong model name).

### [Lesson 12. The core as a library: events instead of `print`](lessons/12-the-core-as-a-library-events-instead-of-print.md) 🚧

**Goal:** separate the agent logic from the interface so the same core
works in a terminal, on the web or inside another agent.

- The problem: `Agent` prints tool calls and runs the spinner itself,
  so it cannot be used without a terminal
- Event handlers: `on_thinking`, `on_tool_call`, `on_tool_result`, `on_answer`, `on_error`
- Confirmation as a pluggable handler (`confirm`) instead of `input()` inside the core
- `cli.py` as one of the event "subscribers"
- Creating an agent from code, without `cli.py` and `config.toml`
- The package's public API (`__all__`) and versioning: what may change and what may not

**Used later:** the Git assistant and the SDD framework will be separate projects
that import `tooled-ai-agent` as a library.

**Practice:** write a 20–30 line script that creates an agent in code,
gives it a task and logs every tool call to a file, with no output on screen.

### [Lesson 13. MCP: connecting ready-made servers (client)](lessons/13-mcp-connecting-ready-made-servers-client.md) 🚧

**Goal:** give the agent tools from any MCP server.

- What MCP is and why it exists: one protocol instead of a separate
  integration with every service
- Architecture: the agent is a client, the server provides tools (`tools/list`, `tools/call`)
- Transports: `stdio` (a local process) and HTTP (a remote server)
- The `MCPTool(Tool)` wrapper: server tools are registered next to your own
- Describing servers in `config.toml` (`[mcp.servers.<name>]`)
- An async SDK and a sync agent: how to connect them
- Safety: descriptions and results from someone else's server are untrusted text

**Used later:** the Git assistant can use the official GitHub and GitLab MCP servers
instead of writing its own tools for PRs/MRs and issues.

**Practice:** connect the filesystem MCP server and compare its tools
with your own `list_files` / `read_file`.

### [Lesson 14. MCP: your own server](lessons/14-mcp-your-own-server.md) 🚧

**Goal:** look at the protocol from the other side and make your tools
available to any MCP client.

- An MCP server in Python with the official SDK (FastMCP)
- A server tool is a plain function with type hints and a docstring
- Publishing existing `tooled-ai-agent` tools (`current_time`,
  `exchange_rate`) via MCP without rewriting them
- Checking the server with MCP Inspector
- Connecting the server to your own agent (lesson 13) and to other clients,
  for example Claude Code or VS Code

**Used later:** tools you write for the Git assistant can be used by other agents too.

**Practice:** build an MCP server with the `exchange_rate` tool and call it
from two different clients.

### [Lesson 15. Final project: a Git agent](lessons/15-final-project-a-git-agent.md) 🚧

**Goal:** build an agent for a real task out of everything you have learned.

- An `--agent git` profile with its own prompt and set of tools
- `git_status`, `git_diff`, `git_log` — read-only, no confirmation needed
- `git_commit` — shows the diff and asks for confirmation
- Reuse: file tools, `run_command`, `run_tests`, secret masking, `ask_user`
- What next: growing this into a separate Git assistant (GitHub/GitLab, CI)
  and an SDD framework built on the `tooled-ai-agent` core

**Practice:** ask the agent to review your uncommitted changes,
run the tests and suggest a commit message.

---

## Appendices

- How sessions, commands, the spinner and colors work
- Packaging and distribution: `pyproject.toml`, `pipx`, a Docker image
- How to contribute
- Course tools and where they are used later:

| Tool / mechanism | Lesson | Git assistant | SDD |
|---|---|---|---|
| `list_files`, `read_file`, `find_files`, `search_files` | 6 | ✓ | ✓ |
| `write_file`, `edit_file`, confirmation | 7 | ✓ | ✓ |
| `run_command`, `run_tests`, secret masking | 8 | ✓ | ✓ |
| Agent profiles | 9 | ✓ | ✓ (phase roles) |
| `ask_user`, `todo_*` | 10 | ✓ | ✓ |
| Timeouts, retries, fallback models | 11 | ✓ | ✓ |
| Events, the core as a library | 12 | ✓ | ✓ |
| MCP client | 13 | ✓ (GitHub/GitLab) | — |
| `git_status`, `git_diff`, `git_log`, `git_commit` | 15 | ✓ | ✓ (committing results) |
