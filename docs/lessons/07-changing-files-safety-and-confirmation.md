# Lesson 7. Changing files, safety and confirmation

> 🚧 **This lesson is in progress.** Below is what it will cover.
> Watch the repository for updates.

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

---

[← Back to the course plan](../index.md)
