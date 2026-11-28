# Lesson 8. Running commands and tests

> 🚧 **This lesson is in progress.** Below is what it will cover.
> Watch the repository for updates.

!!! abstract "Lesson goal"
    Let the agent run commands without losing control.

- `run_command`: an allow list, confirmation, a timeout
- Trimming long output: the first and last lines instead of thousands
- `run_tests`: run `pytest` and return a short summary (passed, failed and why)
- Masking secrets: tokens and passwords must reach neither the model
  nor the session archive

**Used later:** the Git assistant runs git commands and analyses CI logs;
SDD checks every task with tests.

!!! example "Practice"
    Ask the agent to run the project's tests, find why one fails
    (break a test on purpose) and suggest a fix.

---

[← Back to the course plan](../index.md)
