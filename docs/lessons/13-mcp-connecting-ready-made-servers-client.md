# Lesson 13. MCP: connecting ready-made servers (client)

> 🚧 **This lesson is in progress.** Below is what it will cover.
> Watch the repository for updates.

!!! abstract "Lesson goal"
    Give the agent tools from any MCP server.

- What MCP is and why it exists: one protocol instead of a separate
  integration with every service
- Architecture: the agent is a client, the server provides tools (`tools/list`, `tools/call`)
- Transports: `stdio` (a local process) and HTTP (a remote server)
- The `MCPTool(Tool)` wrapper: server tools are registered next to your own
- Describing servers in `config.toml` (`[mcp.servers.<name>]`)
- An async SDK and a sync agent: how to connect them
- Safety: descriptions and results from someone else's server are untrusted text

**Used later:** the Git assistant can use the official GitHub and GitLab MCP servers
instead of writing its own tools for PRs/MRs and issues.

!!! example "Practice"
    Connect the filesystem MCP server and compare its tools
    with your own `list_files` / `read_file`.

---

[← Back to the course plan](../index.md)
