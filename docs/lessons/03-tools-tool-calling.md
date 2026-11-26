# Lesson 3. Tools (tool calling)

> 🚧 **This lesson is in progress.** Below is what it will cover.
> Watch the repository for updates.

**Goal:** understand how a model "uses" tools without running any code.

- The model only *asks* for a function call; our code runs it
- Describing a tool with JSON Schema
- The `Tool` class and the `ToolRegistry`
- A walk through the `calculator` tool
- Why every tool description costs tokens in *every* request
- The `/debug` command: raw requests and responses

**Practice:** use `/debug` to find the moment the model asks for the calculator
and the moment it receives the result.

---

[← Back to the course plan](../index.md)
