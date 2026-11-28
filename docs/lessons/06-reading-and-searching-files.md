# Lesson 6. Reading and searching files

> 🚧 **This lesson is in progress.** Below is what it will cover.
> Watch the repository for updates.

!!! abstract "Lesson goal"
    Let the agent find its way around project files safely.

- `list_files` (like `ls`), `read_file` (like `cat`)
- `find_files` — find files by name pattern (like `find`)
- `search_files` — search text inside files (like `grep -r`)
- Sandboxing: access to the working directory only (`safe_path`)
- Size limits, binary files, ignored folders (`.git`, `.venv`)

**Used later:** the Git assistant needs to understand code before changing it;
SDD needs to find where to implement each task.

!!! example "Practice"
    Ask the agent to find every place where `ToolRegistry` is used
    and to explain how `tooled-ai-agent` works.

---

[← Back to the course plan](../index.md)
