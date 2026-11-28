# Lesson 12. The core as a library: events instead of `print`

> 🚧 **This lesson is in progress.** Below is what it will cover.
> Watch the repository for updates.

!!! abstract "Lesson goal"
    Separate the agent logic from the interface so the same core
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

!!! example "Practice"
    Write a 20–30 line script that creates an agent in code,
    gives it a task and logs every tool call to a file, with no output on screen.

---

[← Back to the course plan](../index.md)
