# Lesson 14. MCP: your own server

> 🚧 **This lesson is in progress.** Below is what it will cover.
> Watch the repository for updates.

!!! abstract "Lesson goal"
    Look at the protocol from the other side and make your tools
    available to any MCP client.

- An MCP server in Python with the official SDK (FastMCP)
- A server tool is a plain function with type hints and a docstring
- Publishing existing `tooled-ai-agent` tools (`current_time`,
  `exchange_rate`) via MCP without rewriting them
- Checking the server with MCP Inspector
- Connecting the server to your own agent (lesson 13) and to other clients,
  for example Claude Code or VS Code

**Used later:** tools you write for the Git assistant can be used by other agents too.

!!! example "Practice"
    Build an MCP server with the `exchange_rate` tool and call it
    from two different clients.

---

[← Back to the course plan](../index.md)
