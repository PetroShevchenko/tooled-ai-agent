# Lesson 4. The agent loop

> 🚧 **This lesson is in progress.** Below is what it will cover.
> Watch the repository for updates.

!!! abstract "Lesson goal"
    Take apart the heart of the agent: the "model → tool → model" loop.

- The `run()` method and the `max_steps` limit
- `tool_call_id` and several calls in one step
- Tool errors are returned to the model
- Conversation history as "memory": why tokens grow with every step, why `/reset`

!!! example "Practice"
    Give the agent a task that needs 3+ steps and watch the history
    grow in `/debug`. Set `max_steps = 1` and see what changes.

---

[← Back to the course plan](../index.md)
