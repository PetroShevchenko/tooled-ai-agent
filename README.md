# tooled-ai-agent

![tooled-ai-agent](docs/assets/images/tooled-ai-agent-banner-1280x300.webp)

[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

**Your first AI agent in plain Python — no frameworks, and you can add your own tools in minutes.**

tooled-ai-agent is a learning project: a step-by-step course on building an AI agent
in Python from scratch. There is no magic inside — just a loop and some JSON.
You get a small, readable codebase that you can extend with your own tools.

Let's build it together, brick by brick — learning, making mistakes, and fixing them.

## Main features

- 🧠 **Any model** via [LiteLLM](https://github.com/BerriAI/litellm): **Gemini**, **OpenAI**, **Claude**, **DeepSeek**, or a free local model with **Ollama**
- 🔧 **Tools** are plain Python classes — one file per tool
- 📚 **Readable**: the whole agent loop fits on one screen
- 💾 **Every conversation is saved** as Markdown, searchable with `/search`

## Tutorial

A step-by-step course, from the first run to your own tools and MCP:

- 🇬🇧 [English](docs/index.md)
- 🇺🇦 [Українська](docs/index.uk.md)

Each lesson has its own git tag with the code for exactly that stage,
so you only see the code relevant to the lesson:

```bash
git checkout lesson-05-first-tool    # code of lesson 5
git checkout main                    # full version
```

The tutorial is built with [MkDocs](https://www.mkdocs.org). To preview it locally:

```bash
source ./env.sh activate
mkdocs serve        # open http://127.0.0.1:8000
```

## Demo

![tooled-ai-agent demo](demo/demo.gif)

## Quick start

Requirements: Python 3.11+ and [pipx](https://pipx.pypa.io).

1. Install the agent:

   ```bash
   pipx install git+https://github.com/PetroShevchenko/tooled-ai-agent.git
   ```

2. Connect a model — see [Pick a model](#pick-a-model). The easiest free option
   is a [local model](#local-model-free-no-account) with Ollama.

3. Start the agent with the profile you connected:

   ```bash
   tooled -m local     # or: tooled -m gemini, or just `tooled` for the default profile
   ```

## Usage

```bash
tooled              # start with the default profile
tooled -m local     # start with a specific profile
tooled --list       # show all profiles and exit
tooled -c my.toml   # use another config file
```

Commands inside the chat:

| Command | Action |
|---|---|
| `/help` | show help |
| `/models` | list model profiles |
| `/model <name>` | switch model (history is kept) |
| `/reset` | clear history |
| `/usage` | show token usage |
| `/history` | recent sessions |
| `/search <words>` | search questions in all sessions |
| empty line | exit |

### Conversation archive

Every session is saved in two files:

- `.md` — human-readable version
- `.jsonl` — full data, one event per line

Location:

| OS | Folder |
|---|---|
| Linux | `~/.local/share/tooled-ai-agent/sessions/YYYY/MM/` |
| macOS | `~/Library/Application Support/tooled-ai-agent/sessions/YYYY/MM/` |
| Windows | `%LOCALAPPDATA%\tooled-ai-agent\sessions\YYYY\MM\` |

To store sessions elsewhere, set the `TOOLED_AI_AGENT_HOME` environment variable.

## Pick a model

The agent works with any model supported by [LiteLLM](https://docs.litellm.ai/docs/providers).
Each model is a named profile in `config.toml`, which is created on first run at:

- Linux: `~/.config/tooled-ai-agent/config.toml`
- macOS: `~/Library/Application Support/tooled-ai-agent/config.toml`
- Windows: `%LOCALAPPDATA%\tooled-ai-agent\config.toml`

The default config contains the profiles `flash` (default), `pro`, `gemini`, `local` and `deepseek`.
Connect **one** of them using the options below.

### Local model (free, no account)

Install [Ollama](https://ollama.com/download), then:

```bash
ollama pull qwen3
tooled -m local
```

> [!NOTE]
> Speed of a local model depends entirely on your hardware:
>
> - Without a GPU, the model runs on the CPU — an answer may take from several seconds to minutes.
> - The first request is the slowest, because the model is loaded into memory.

If it is too slow, switch to a smaller model:

```bash
ollama pull qwen3:1.7b
```

```toml
[models.local]
model = "ollama_chat/qwen3:1.7b"
```

Or use a cloud model below.

### Gemini API free tier

Get a key at [Google AI Studio](https://aistudio.google.com), then:

```bash
export GEMINI_API_KEY="..."
tooled -m gemini
```

### Gemini on Vertex AI (default profile `flash`)

Install the [gcloud CLI](https://cloud.google.com/sdk/docs/install), sign in and enable the API:

```bash
gcloud auth application-default login
gcloud services enable aiplatform.googleapis.com --project your-project-id
```

Put your Google Cloud project ID into the config:

```toml
[models.flash]
model = "vertex_ai/gemini-3.8-flash"
extra = { vertex_project = "your-project-id", vertex_location = "global", drop_params = true }
```

Start the agent:

```bash
tooled
```

### All providers

| Provider | Cost | Setup | Example `model` |
|---|---|---|---|
| [Ollama](https://ollama.com) | free, local | `ollama pull qwen3` | `ollama_chat/qwen3` |
| [Gemini API](https://aistudio.google.com) | free tier with daily limits | key in `GEMINI_API_KEY` | `gemini/gemini-3.8-flash` |
| [Vertex AI](https://cloud.google.com/vertex-ai) | paid (Google Cloud credits apply) | `gcloud auth application-default login` + project ID in `extra` | `vertex_ai/gemini-3.8-flash` |
| OpenAI | paid | key in `OPENAI_API_KEY` | `openai/gpt-5-mini` |
| Anthropic | paid | key in `ANTHROPIC_API_KEY` | `anthropic/claude-sonnet-5-5` |
| DeepSeek | paid, low cost | key in `DEEPSEEK_API_KEY` | `deepseek/deepseek-chat` |

### Profiles

To add a provider, add a profile to `config.toml`. To change the profile used by
plain `tooled`, change `default` in the `[llm]` section:

```toml
[llm]
default = "local"                    # profile used by plain `tooled`

[models.local]
model = "ollama_chat/qwen3"          # LiteLLM format: provider/model
temperature = 0.2                    # optional

[models.openai]
model = "openai/gpt-5-mini"
extra = { drop_params = true }       # optional
```

`extra` passes any additional parameters to `litellm.completion()` as is.

> [!TIP]
> - Never put API keys in `config.toml` — use environment variables.
> - For Ollama use the `ollama_chat/` prefix: it supports tool calling.
> - Model names change often; check the exact name in your provider's console.
> - Some models don't accept every parameter (e.g. `temperature`). Remove it from
>   the profile or add `drop_params = true` to `extra`.

### Agent settings

```toml
[agent]
max_steps = 10        # safeguard against an infinite loop
verbose = true        # print tool calls
system_prompt = """
You are a helpful assistant. Use the calculator tool for any calculations.
"""
```

## Add your own tool

1. Create a file in `src/tooled_ai_agent/tools/`, for example `current_time.py`:

   ```python
   from datetime import datetime
   from zoneinfo import ZoneInfo

   from ..core.tool import Tool

   class CurrentTimeTool(Tool):
       name = "current_time"
       description = (                     # the model sees ONLY this text
           "Returns the current date and time. "
           "Use it whenever the answer depends on today's date or the current time."
       )
       parameters = {                      # JSON Schema of the arguments
           "type": "object",
           "properties": {
               "timezone": {"type": "string", "description": "IANA time zone, e.g. 'Europe/Kyiv'"}
           },
           "required": [],
       }

       def run(self, timezone: str | None = None) -> str:
           now = datetime.now(ZoneInfo(timezone)) if timezone else datetime.now().astimezone()
           return now.strftime("%Y-%m-%d %H:%M:%S %Z (%A)")
   ```

2. Export it in `src/tooled_ai_agent/tools/__init__.py`:

   ```python
   from .current_time import CurrentTimeTool
   ```

3. Register it in `src/tooled_ai_agent/cli.py`:

   ```python
   tools = ToolRegistry([CalculatorTool(), CurrentTimeTool()])
   ```

Exceptions raised in `run()` are returned to the model as text, so it can correct itself.

## Development

Requirements: Python 3.11+

### Linux / macOS

```bash
git clone https://github.com/PetroShevchenko/tooled-ai-agent.git
cd tooled-ai-agent
./install.sh                 # creates .venv and installs the package with dev and docs extras
source ./env.sh activate     # activates .venv
pytest                       # run tests
```

### Windows

Use WSL2 (recommended) or PowerShell.

#### WSL2

1. Install Ubuntu inside Windows. Run in PowerShell:

   ```powershell
   wsl --install -d ubuntu
   ```

2. Set up WSL2: <kbd>Win</kbd> → **Search** → **WSL Settings**.

3. Open Ubuntu: <kbd>Win</kbd> → **Search** → **Ubuntu**, then follow [Linux / macOS](#linux--macos).

> [!IMPORTANT]
> Virtualization must be enabled in the BIOS setup of your machine, otherwise you will see
> the error "0x80370114 The operation could not be started because a required feature is not installed."

#### PowerShell

1. Install Python and Git:

   ```powershell
   winget install Python.Python.3.12
   winget install Git.Git
   ```

   Close and reopen PowerShell to update the PATH, then check the versions:

   ```powershell
   python --version
   git --version
   ```

2. Clone tooled-ai-agent:

   ```powershell
   cd $HOME\Documents
   git clone https://github.com/PetroShevchenko/tooled-ai-agent.git
   cd tooled-ai-agent
   ```

3. Install for development:

   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   pip install -e ".[dev,docs]"
   $env:LITELLM_LOCAL_MODEL_COST_MAP = "True"   # use the bundled model cost map, no network fetch
   ```

## Contributing

New tools are the best way to contribute: one file in `src/tooled_ai_agent/tools/`,
a short description, a test in `tests/`, and a pull request
(see [Add your own tool](#add-your-own-tool)). Issues labeled **good first issue** contain ideas.

## License

Released under the [MIT License](LICENSE).
