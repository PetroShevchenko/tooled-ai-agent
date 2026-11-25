# Course: your first AI agent

This course is for anyone who wants to understand how an AI agent works
and write their own tools for it. We go top-down: first we use the ready-made
`tooled-ai-agent`, then we look at how it works inside, and finally we extend it.

**Prerequisites:** Python basics (functions, classes, dictionaries) and the terminal.

**Lesson code:** starting from lesson 5, every lesson has its own git tag
with the code for exactly that stage:

```bash
git checkout lesson-05-first-tool    # code of lesson 5
git checkout main                    # full version
```

---

## Part 1. The user

### Lesson 1. Installation and first run

**Goal:** install the agent, connect a language model and ask the first question.

- Installing on your platform:
    - **Linux / macOS:** the `install.sh` and `env.sh` scripts
    - **Windows (recommended):** WSL2 (`wsl --install`), then the same as Linux
    - **Windows without WSL:** plain Python commands in PowerShell (`python -m venv`, `pip install -e .`)
- Installing as a regular command with `pipx`
- Connecting a model: free (Ollama) or cloud (Vertex AI, API key)
- The first request
- Commands: `/help`, `/models`, `/model`, `/usage`, `/history`, `/search`

**Practice:** ask the agent 3–4 questions, find one of them with `/search`
and open the saved conversation as an `.md` file.

### Lesson 2. How the agent talks to the model

**Goal:** understand what happens during a single model call.

- Project structure
- `config.toml`: where it comes from, how to change it, model profiles
- The `completion()` call and message roles: `system`, `user`, `assistant`
- Tokens and the `temperature` parameter

**Practice:** add your own model profile, compare two models' answers
to the same question and the difference in `/usage`.

---

## Part 2. How the agent works

### Lesson 3. Tools (tool calling)

**Goal:** understand how a model "uses" tools without running any code.

- The model only *asks* for a function call; our code runs it
- Describing a tool with JSON Schema
- The `Tool` class and the `ToolRegistry`
- A walk through the `calculator` tool
- The `/debug` command: raw requests and responses

**Practice:** use `/debug` to find the moment the model asks for the calculator
and the moment it receives the result.

### Lesson 4. The agent loop

**Goal:** take apart the heart of the agent: the "model → tool → model" loop.

- The `run()` method and the `max_steps` limit
- `tool_call_id` and several calls in one step
- Tool errors are returned to the model
- Conversation history as "memory": why tokens grow with every step, why `/reset`

**Practice:** give the agent a task that needs 3+ steps and watch the history
grow in `/debug`. Set `max_steps = 1` and see what changes.

---

## Part 3. Extending the agent

### Lesson 5. Your first tool

**Goal:** write your own tool and connect it to the agent.

- The `current_time` tool step by step
- Why the `description` matters more than the code
- Testing a tool with `pytest`

**Practice:** write `exchange_rate` (the open National Bank of Ukraine API)
or `get_weather` (Open-Meteo) on your own.

### Lesson 6. Working with files

**Goal:** let the agent read files safely.

- The `list_files` and `read_file` tools
- Sandboxing: access to the working directory only
- Size limits, binary files, ignored folders

**Practice:** ask the agent to explain the code of `tooled-ai-agent` itself.

### Lesson 7. Safety and confirmation

**Goal:** let the agent change files while you stay in control.

- `write_file` with confirmation
- Cancelling a request (Ctrl+C) and rolling back the history
- Prompt injection: why data from files and the web is untrusted text
- A Docker container as a sandbox: the agent sees only the working directory
  and cannot damage files outside it; runs on any OS

**Practice:** try to "trick" the agent through the contents of a file and make sure
the confirmation step protects you. Then run the agent in a container
and check that files outside the working directory are out of its reach.

### Lesson 8. System prompt and agent profiles

**Goal:** turn one engine into different agents.

- How the system prompt changes behaviour
- Agent profiles with `--agent`: its own prompt and its own set of tools
- Long-term memory: the `remember` / `recall` tools

**Practice:** create your own profile, for example a "translator"
or a "code reviewer".

---

## Part 4. Next steps

### Lesson 9. MCP

**Goal:** connect a ready-made MCP server and see its tools appear
next to your own.

### Lesson 10. Final project: a Git agent

**Goal:** build an `--agent git` profile with the `git_status`, `git_diff`
and `git_commit` tools (with confirmation).

---

## Appendices

- How sessions, commands, the spinner and colors work
- Packaging and distribution: `pyproject.toml`, `pipx`, a Docker image
- How to contribute
