# Lesson 1. Installation and first run

!!! abstract "Lesson goal"
    Install the agent, connect a language model and ask the first question.

![A bearded baby builder](../assets/images/baby-builder-bearded.webp)

We were all little once and had to learn everything from the very beginning.
As adults, each of us carries our own baggage of knowledge gained at school, at university and throughout our professional life. It helps us grow and learn new things.

If this lesson suddenly seems too hard, think of babies: they learn everything from scratch, and they can't even use artificial intelligence yet.

Let's start by imagining ourselves as ordinary users (not programmers), but advanced enough to install any Python program on our own.

## 1.1 Installing tooled as a regular program with `pipx`

tooled is the short name of tooled-ai-agent. Open a terminal (bash or PowerShell) on your machine: whether it's Ubuntu, macOS or Windows, the install command works the same everywhere:

```bash
pipx install git+https://github.com/PetroShevchenko/tooled-ai-agent.git
```

If it didn't work, that only means the required packages are not installed on your machine. Check whether Python and git are installed:

```bash
python --version
git --version
```

!!! note
    tooled requires **Python 3.11 or newer**. On Linux and macOS the command may be called `python3`.

How you install the required packages depends on your operating system.

### Windows

If Python and git are not installed yet, install them in PowerShell:

```powershell
winget install --id Python.Python.3.12 --exact
winget install --id Git.Git --exact
```

Close and reopen PowerShell to install pipx:

```powershell
py -3.12 -m pip install --user pipx
py -3.12 -m pipx ensurepath
```

Open a new PowerShell terminal once more and repeat the tooled install command — this time everything should work.

### Ubuntu

Install all the required dependencies at once with the package manager:

```bash
sudo apt update
sudo apt install git python3 pipx -y
pipx ensurepath
```

!!! note
    Python 3.10 on Ubuntu 22.04 is too old for tooled. Upgrade the system or [install a newer Python](https://launchpad.net/~deadsnakes/+archive/ubuntu/ppa).

Open a new terminal and try installing tooled again:

```bash
pipx install git+https://github.com/PetroShevchenko/tooled-ai-agent.git
```

### macOS

If the `brew` command is not available yet, first install [Homebrew](https://brew.sh) and follow the installer's instructions to add brew to your PATH.

Then open a terminal and install all the required dependencies with the brew package manager:

```bash
brew install git pipx
pipx ensurepath
```

Open a new terminal and try installing tooled again:

```bash
pipx install git+https://github.com/PetroShevchenko/tooled-ai-agent.git
```

### First run

Now try starting the agent by simply typing `tooled` in the terminal.
You can even say "Hi" to the agent: it will think for a few seconds about what to answer and finally print a Python traceback with an error message, because you haven't connected any model for the agent to work with yet. How to do that is covered in section [1.3](#13-connecting-a-model).

## 1.2 Installing tooled for development

In the previous section we installed tooled as a ready-made program. pipx put its code into a separate virtual environment, where it is inconvenient to read or change. To work with the source code, you need to install tooled specifically for development.

You can skip this step for now and go straight to [connecting a model](#13-connecting-a-model). But you will have to come back to it as soon as you become interested in the agent's source code.

The installation depends on your operating system.

### Linux / macOS

Open a bash terminal and clone the tooled-ai-agent repository into your home directory or any other place on disk. Then go into the cloned repository and run the `install.sh` script — it will install everything needed for further work. At the end of the installation the script will remind you to activate the virtual environment — so activate it.

```bash
git clone https://github.com/PetroShevchenko/tooled-ai-agent.git
cd tooled-ai-agent
./install.sh                 # creates .venv and installs the package with dev and docs extras
source ./env.sh activate     # activates .venv
```

Once the virtual environment is activated, you can run tooled:

```bash
tooled
```

### Windows

There are two ways to install tooled-ai-agent on Windows:

- install the WSL2 virtual environment and run an Ubuntu bash terminal right inside your Windows system (the recommended way);
- install tooled-ai-agent natively on Windows via PowerShell and use PowerShell for further work.

!!! note "Why WSL2 is recommended"
    I develop tooled-ai-agent on Ubuntu Linux, so it has to be tested on Windows separately. If you choose the second installation method, you will be the person who tests tooled-ai-agent on Windows.

### Windows: WSL2

Open a PowerShell terminal and run:

```powershell
wsl --install -d ubuntu
```

After the installation, the Ubuntu bash terminal should appear right in the running PowerShell, so you can go straight to installing tooled-ai-agent as described in [Linux / macOS](#linux-macos). If Windows asks for permission to make changes or to restart — agree; after the restart the installation will continue.

Next time, however, you will have to open the Ubuntu bash terminal separately: press the Win key, search for Ubuntu and run:

```bash
cd ~/tooled-ai-agent
source ./env.sh activate
tooled
```

If needed, you can change the number of CPU cores, the amount of memory and other resources allocated to WSL2: press the Win key and search for WSL Settings.

!!! important
    Virtualization must be enabled in your computer's BIOS Setup, otherwise when you try to start Ubuntu you will get this error:
    `0x80370114 The operation could not be started because a required feature is not installed.`

### Windows without WSL

Check whether git and Python are installed on your computer:

```powershell
python --version
git --version
```

If not, install them following the instructions in the [Windows](#windows) section above.

Now open PowerShell and clone the tooled-ai-agent repository:

```powershell
cd $HOME\Documents
git clone https://github.com/PetroShevchenko/tooled-ai-agent.git
cd tooled-ai-agent
```

From the tooled-ai-agent directory, run the installation:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev,docs]"
$env:LITELLM_LOCAL_MODEL_COST_MAP = "True"   # use the bundled model cost map, no network fetch
tooled
```

!!! note
    If PowerShell refuses to run `.venv\Scripts\activate` because of the script execution policy, allow local scripts for your user and activate again:
    `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

The `LITELLM_LOCAL_MODEL_COST_MAP` variable only lasts for the current PowerShell session. Next time, go to the tooled-ai-agent directory, activate the environment again and set the variable before running `tooled`.

### The code of the first lesson

The cloned repository contains the latest version of the agent from the `main` branch. The code of each lesson is pinned by a `lesson-NN` git tag. To make your code match this lesson, switch to the `lesson-01` tag (the commands are the same in bash and PowerShell):

```bash
git checkout lesson-01    # code of lesson 1
git checkout main         # back to the latest version
```

The package is installed in editable mode (`pip install -e`), so there's no need to reinstall it after switching — `tooled` runs the code of the selected lesson right away.

!!! warning
    `git checkout lesson-01` puts the repository into the detached HEAD state. To keep your own changes safe, see [How to use the lesson code](../index.md#lesson-code).

## 1.3 Connecting a model

Now it's time to choose and connect an artificial intelligence model. tooled-ai-agent talks to models through [LiteLLM](https://docs.litellm.ai/docs/providers) — a library that supports dozens of providers, including these:

| Provider | Cost | Setup | Example `model` |
|---|---|---|---|
| [Ollama](https://ollama.com) | free, local | `ollama pull qwen3:1.7b` | `ollama_chat/qwen3:1.7b` |
| [Gemini API](https://aistudio.google.com) | free tier with daily limits | key in `GEMINI_API_KEY` | `gemini/gemini-3.8-flash` |
| [Vertex AI](https://cloud.google.com/vertex-ai) | paid (Google Cloud credits apply) | `gcloud auth application-default login` + project ID in `extra` | `vertex_ai/gemini-3.8-flash` |
| [OpenAI](https://openai.com) | paid | key in `OPENAI_API_KEY` | `openai/gpt-5-mini` |
| [Anthropic](https://www.anthropic.com/) | paid | key in `ANTHROPIC_API_KEY` | `anthropic/claude-sonnet-5-5` |
| [DeepSeek](https://www.deepseek.com/en/) | paid, low cost | key in `DEEPSEEK_API_KEY` | `deepseek/deepseek-chat` |

### The config.toml configuration file

Your AI agent doesn't know anything yet about the model you are going to use. To set the default model and be able to switch to other models, you need to write the model information into the config.toml configuration file.

The configuration file is created automatically on the **first run** of `tooled` — the agent prints a `Created default config:` line with the path to the file. The path depends on the operating system:

- Linux: `~/.config/tooled-ai-agent/config.toml`
- macOS: `~/Library/Application Support/tooled-ai-agent/config.toml`
- Windows: `%LOCALAPPDATA%\tooled-ai-agent\config.toml`

config.toml is copied from the default_config.toml template, which is the same on all machines. All your further settings are stored in your own config.toml.

!!! note
    Reinstalling tooled-ai-agent does not change your config.toml — your settings are kept. But new parameters from an updated default_config.toml template won't get into your existing file by themselves either. If you delete config.toml, the agent will create it again from the template on the next run.

Each model is described in config.toml by a separate **profile** — a `[models.<name>]` section:

```toml
[models.local]
model = "ollama_chat/qwen3"
temperature = 0.2
```

The profile the agent uses by default is set in the `[llm]` section with `default = "<name>"`:

```toml
[llm]
default = "local"
```

Profiles for all three options below are already in the template — you only need to change a few existing lines.

!!! warning
    Don't append sections to the end of the file: a TOML section can't be declared twice, and the agent will fail to start with
    `tomllib.TOMLDecodeError: Cannot declare ('llm',) twice`. Find the sections you need in the file and change the existing lines.

Choose one of the three ways to connect a model. Any of them is enough for the first run, and you can set up the others later.

### Local model: ollama_chat/qwen3:1.7b

This is a free model that you install on your own computer, and it uses your machine's hardware. So if your machine is not very powerful, the model will run slowly too. The advantage of such a model is that you can try the agent without signing up anywhere or getting API keys. Let's start with it.

First download and install the [Ollama](https://ollama.com/download) application.

Open a terminal (bash or PowerShell) and download the model with this command (the download time depends on your internet speed):

```bash
ollama pull qwen3:1.7b
```

!!! note
    The 1.7b model is the lightest in the qwen3 family, and it is enough for the first lessons. For more complex multi-step tasks in later lessons you may need a bigger model, for example `qwen3:8b`, if your memory allows.

The Ollama server must be running while you use the agent. On Windows and macOS it is started by the Ollama application, on Linux by a system service or the `ollama serve` command.

Now open config.toml in any text editor, find the `[llm]` and `[models.local]` sections and change the existing lines so that the agent uses the Ollama model by default:

```toml
[llm]
default = "local"                    # profile used by plain `tooled`

[models.local]
model = "ollama_chat/qwen3:1.7b"     # LiteLLM format: provider/model
temperature = 0.2                    # optional
```

!!! success "Done"
    The local model is connected — go to [section 1.4](#14-the-first-request) and try the agent.

### Cloud model with an API key: gemini/gemini-3.8-flash

A cloud model runs on Google's servers, so its speed doesn't depend on how powerful your computer is, and its answers are much better than those of a small local model.

The easiest way to try a cloud model is the Gemini API with an API key. `gemini-3.8-flash` has a free tier with a limited number of requests, which is enough for the course lessons.

1. Open [Google AI Studio](https://aistudio.google.com/apikey), sign in with your Google account and create an API key ([official guide](https://ai.google.dev/gemini-api/docs/api-key)).
2. Make sure the key shows the **Free** tier.

!!! warning "The key is free only if its project has no billing"
    Every API key belongs to a Google Cloud project and gets that project's tier. If a billing account is linked to the project (for example, you already use Vertex AI in it), the key runs on the paid tier. To use it for free, create the key in a separate project with no billing linked.

3. Store the key in the `GEMINI_API_KEY` environment variable. **Don't put the key in config.toml** — the agent reads it only from the environment variable.

Linux / macOS / WSL:

```bash
export GEMINI_API_KEY="your-key"
```

Windows (PowerShell):

```powershell
$env:GEMINI_API_KEY="your-key"
```

The variable lives only in the current terminal: run `tooled` in the same window. To avoid setting it every time, add the `export` line to `~/.bashrc` on Linux and WSL or to `~/.zshrc` on macOS, and on Windows run `setx GEMINI_API_KEY "your-key"` and open a new terminal.

config.toml already has the `[models.gemini]` profile for this model, and it needs no changes. All that's left is to make it the default profile — find the `[llm]` section and change the `default` line:

```toml
[llm]
default = "gemini"

[models.gemini]
model = "gemini/gemini-3.8-flash"
temperature = 0.2
```

!!! success "Done"
    The Gemini API is connected — go to [section 1.4](#14-the-first-request) and try the agent.

### Cloud model via Vertex AI: vertex_ai/gemini-3.8-flash

Vertex AI runs the same `gemini-3.8-flash` model, so the answers are as good as with the free Gemini API. The difference is in the terms of use:

| | Gemini API, free tier | Vertex AI |
|---|---|---|
| Cost | free | pay per token (Google Cloud credits can be used) |
| Rate limits | low: with frequent requests you'll have to wait | much higher |
| Your data | Google may use prompts and responses to improve its products, and people may review them ([Gemini API terms](https://ai.google.dev/gemini-api/terms)) | not used to train models |
| Other features | Gemini API models only | region choice, other models from Model Garden, Google Cloud tools |

The free tier is enough for the course lessons. Choose Vertex AI if the limits get in your way or you send the model work code and data that Google must not use to improve its products.

Vertex AI requires a Google Cloud account with billing linked.

Before configuring the agent, prepare Google Cloud:

1. Create a Google Cloud project, enable billing and the Vertex AI API for it — the steps are described in the [official Vertex AI documentation](https://cloud.google.com/vertex-ai/docs/start/cloud-environment). Note the **project ID**, e.g. `gen-lang-client-XXXXXXXXXX` — it is shown in the [project list](https://console.cloud.google.com/cloud-resource-manager) of the Google Cloud console.
2. Install the [Google Cloud CLI](https://cloud.google.com/sdk/docs/install) (the `gcloud` command).
3. Sign in to your account so the agent can call Vertex AI on your behalf ([more about ADC](https://cloud.google.com/docs/authentication/set-up-adc-local-dev-environment)):

```bash
gcloud auth application-default login
```

Vertex AI needs no API key: LiteLLM finds the credentials saved by `gcloud` on its own.

config.toml already has a profile for this model — **find the `[models.flash]` section** and replace `your-project-id` with your project ID:

```toml
[models.flash]
model = "vertex_ai/gemini-3.8-flash"
extra = { vertex_project = "gen-lang-client-XXXXXXXXXX", vertex_location = "global", drop_params = true }
```

The agent passes the parameters in `extra` to LiteLLM unchanged:

- `vertex_project` — your Google Cloud project ID;
- `vertex_location` — the region that serves the request; `global` lets Google pick an available region;
- `drop_params = true` — LiteLLM silently drops parameters the model doesn't support instead of returning an error.

Other parameters are described in the [LiteLLM documentation for Vertex AI](https://docs.litellm.ai/docs/providers/vertex).

All that's left is to make it the default profile — the `[llm]` section must have `default = "flash"` (the template already has this value).

!!! success "Done"
    Vertex AI is connected — go to [section 1.4](#14-the-first-request) and try the agent.

## 1.4 The first request

Check that the agent sees your model profile:

```bash
tooled --list
```

The profile you set up (`local`, `gemini` or `flash`) should be marked `(by default)`. Now start the agent and say "Hi" to it:

```bash
tooled
```

This time you should get an answer from the model instead of an error. An empty line exits the agent.

To try another profile you have set up without changing `default`, pass it at startup, e.g. `tooled -m gemini`.

## 1.5 Chat commands

Besides regular questions, you can type commands — they start with `/` and are not sent to the model.

| Command | What it does |
|---|---|
| `/help` | shows the list of commands |
| `/models` | lists model profiles from config.toml; the `(by default)` and `(current)` marks show the default and the current model |
| `/model <name>` | switches to another profile, e.g. `/model local`; the conversation history is kept |
| `/reset` | clears the history of the current conversation — the model "forgets" previous questions |
| `/usage` | shows how many tokens the session has used: `↑` — sent to the model, `↓` — received |
| `/history` | shows the 10 most recent saved conversations and the paths to their files |
| `/search <words>` | searches all saved conversations for questions containing **all** the given words |

### Keys

| Keys | What they do |
|---|---|
| empty line (`Enter`) | exits the agent |
| `Ctrl+D` | exits the agent |
| `Ctrl+C` while typing | discards the typed line; pressed again within 2 seconds — exits |
| `Ctrl+C` while waiting for an answer | cancels the request to the model, the agent waits for a new question |

### Command-line options

The model and the configuration file can be chosen before the chat starts:

| Option | What it does |
|---|---|
| `tooled` | starts the chat with the default model (`[llm] default`) |
| `tooled -m <name>`, `--model <name>` | starts the chat with the given profile, e.g. `tooled -m local` |
| `tooled --list` | lists model profiles and exits |
| `tooled -c <file>`, `--config <file>` | uses another configuration file instead of config.toml |
| `tooled -h`, `--help` | shows help on the options |

The profile can also be set with the `AGENT_MODEL` environment variable, for example:

`bash`
```bash
AGENT_MODEL=local tooled
```

`PowerShell`
```powershell
$env:AGENT_MODEL="local"; tooled
```

Priority order: `-m` → `AGENT_MODEL` → `[llm] default`.

`tooled-ai-agent` is the full command name and works exactly like `tooled`.

### Where conversations are saved

Every conversation is saved automatically in two files: `.md` — human-readable, `.jsonl` — full data for programs. The files are created only after the first question, so empty sessions don't clutter the archive. On exit the agent prints a `Saved:` line with the path to the `.md` file.

The archive lives in `sessions/YYYY/MM/` subfolders:

- Linux: `~/.local/share/tooled-ai-agent/sessions/`
- macOS: `~/Library/Application Support/tooled-ai-agent/sessions/`
- Windows: `%LOCALAPPDATA%\tooled-ai-agent\sessions\`

The file name consists of the date, the time and the first question, e.g. `2026-11-24_031305_hello.md`. The archive location can be changed with the `TOOLED_AI_AGENT_HOME` environment variable.

`/search` prints the date, the matching question and the path to the file with the line number — open that file in any editor to reread the whole conversation.

## Troubleshooting

- **`pipx: command not found`** or **`tooled: command not found`** — close and reopen the terminal after `pipx ensurepath`.
- **pipx complains about an incompatible Python version** — tooled requires Python 3.11 or newer (see the note for Ubuntu 22.04).
- **`Connection refused` when talking to the Ollama model** — the Ollama server is not running.
- **`TOMLDecodeError`** — config.toml has a syntax error or a section is declared twice; the line and column are given in the message.
- **`API key not valid`** from the Gemini API — the key was copied incorrectly, or `GEMINI_API_KEY` was set in another terminal.
- **`429`** / **`RESOURCE_EXHAUSTED`** from the Gemini API — the free-tier limit is used up; wait or check the limits in AI Studio.
- **`DefaultCredentialsError`** when calling Vertex AI — you haven't run `gcloud auth application-default login`.
- **`PERMISSION_DENIED`** or **`403`** from Vertex AI — `vertex_project` has the wrong project ID, or billing or the Vertex AI API isn't enabled for the project.

!!! example "Practice"
    Ask the agent 3–4 questions, find one of them with `/search`
    and open the saved conversation as an `.md` file.

---

[← Back to the course plan](../index.md)
