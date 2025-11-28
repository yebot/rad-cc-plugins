---
description: Initialize Backlog.md in the current project. Use when starting a new project or setting up task management for the first time.
---

# Initialize Backlog.md

Initialize Backlog.md task management in this project for structured, markdown-native project collaboration.

## Instructions

1. **Check if already initialized**: Look for a `backlog/` directory in the project root
   - If exists, inform the user and ask if they want to reconfigure

2. **Run initialization**: Execute `backlog init` with appropriate options
   - For MCP mode (recommended): `backlog init --mcp`
   - This creates the backlog structure and configures MCP integration

3. **Verify setup**:
   - Confirm `backlog/config.yml` exists
   - Confirm `backlog/tasks/` directory exists
   - Check that MCP is configured in the project's Claude settings

4. **Post-initialization guidance**:
   - Read the workflow overview using the backlog MCP tools
   - Explain the basic commands: creating tasks, viewing the board, managing dependencies
   - Offer to create initial project tasks if the user has requirements

## Example Usage

```bash
# Initialize with MCP support (recommended)
backlog init "My Project Name"

# View the board after initialization
backlog board
```

## Notes

- Backlog.md stores all data as markdown files in the `backlog/` directory
- Tasks are human-readable files like `task-1 - Feature Name.md`
- All changes are tracked in git automatically
- MCP mode enables AI agents to interact via standardized protocol