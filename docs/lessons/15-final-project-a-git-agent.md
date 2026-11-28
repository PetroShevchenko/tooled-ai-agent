# Lesson 15. Final project: a Git agent

> 🚧 **This lesson is in progress.** Below is what it will cover.
> Watch the repository for updates.

!!! abstract "Lesson goal"
    Build an agent for a real task out of everything you have learned.

- An `--agent git` profile with its own prompt and set of tools
- `git_status`, `git_diff`, `git_log` — read-only, no confirmation needed
- `git_commit` — shows the diff and asks for confirmation
- Reuse: file tools, `run_command`, `run_tests`, secret masking, `ask_user`
- What next: growing this into a separate Git assistant (GitHub/GitLab, CI)
  and an SDD framework built on the `tooled-ai-agent` core

!!! example "Practice"
    Ask the agent to review your uncommitted changes,
    run the tests and suggest a commit message.

---

[← Back to the course plan](../index.md)
