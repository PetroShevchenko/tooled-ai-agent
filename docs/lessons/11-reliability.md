# Lesson 11. Reliability

> 🚧 **This lesson is in progress.** Below is what it will cover.
> Watch the repository for updates.

**Goal:** the agent must not crash or hang because of model failures.

- A request timeout instead of waiting forever
- Retries on temporary errors (network, overload)
- Fallback models: switch to another model when a limit is reached (`litellm.Router`)
- Why free tiers run out quickly in agent mode

**Used later:** both agents — long tasks must not stop because of a single failure.

**Practice:** set up a chain of fallback models and simulate a failure of the main one
(for example, a wrong model name).

---

[← Back to the course plan](../index.md)
