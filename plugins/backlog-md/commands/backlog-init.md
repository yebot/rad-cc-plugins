---
description: Initialize or configure Backlog.md in the current project. Safe to run on existing backlogs - will only add missing configuration.
---

# Initialize Backlog.md

Initialize or configure Backlog.md task management in this project. This command is idempotent and safe to run on existing backlogs.

## Instructions

### Step 1: Check Current State

```bash
# Check if backlog directory exists
ls -la backlog/ 2>/dev/null
```

**If backlog exists**: Skip CLI initialization, proceed to configuration steps.
**If backlog doesn't exist**: Run full initialization.

### Step 2: Initialize Backlog (if needed)

Only run if `backlog/` directory doesn't exist:

```bash
# Initialize with project name
backlog init "Project Name"
```

### Step 3: Configure Claude Code Permissions

Check if `.claude/settings.json` exists and has the backlog MCP tools pre-authorized:

```bash
# Check current settings
cat .claude/settings.json 2>/dev/null || echo "No settings file"
```

**Create or update** `.claude/settings.json` to include backlog MCP tools:

```json
{
  "allowedTools": [
    "mcp__backlog__*"
  ]
}
```

**If file exists with other settings**, merge the `allowedTools` array - don't overwrite existing entries:

```json
{
  "existingKey": "existingValue",
  "allowedTools": [
    "existing__tool__pattern",
    "mcp__backlog__*"
  ]
}
```

### Step 4: Configure MCP Server (if needed)

Check if `.mcp.json` has the backlog server configured:

```bash
cat .mcp.json 2>/dev/null || echo "No MCP config"
```

**Create or update** `.mcp.json` to include the backlog server:

```json
{
  "mcpServers": {
    "backlog": {
      "command": "backlog",
      "args": ["mcp", "start"]
    }
  }
}
```

**If file exists**, merge - don't overwrite other MCP servers.

### Step 5: Verify Setup

Run verification checks:

```bash
# Verify backlog structure
ls backlog/tasks/ 2>/dev/null && echo "✓ Tasks directory exists"
ls backlog/config.yml 2>/dev/null && echo "✓ Config exists"

# Verify MCP config
grep -q "backlog" .mcp.json 2>/dev/null && echo "✓ MCP server configured"

# Verify permissions
grep -q "mcp__backlog" .claude/settings.json 2>/dev/null && echo "✓ Permissions configured"
```

### Step 6: Report Status

Present a summary to the user:

```
## Backlog.md Setup Complete

✓ Backlog directory: backlog/
✓ MCP server: configured in .mcp.json
✓ Permissions: mcp__backlog__* pre-authorized

### What's configured:
- All backlog MCP tools are pre-authorized (no approval prompts)
- MCP server will start automatically when needed

### Next steps:
- Run `/board` to see your tasks
- Run `/work <id>` to start working on a task
- Run `/guide` for full plugin documentation
```

## Handling Existing Backlogs

This command is safe to re-run because:

1. **Backlog CLI**: `backlog init` is skipped if `backlog/` exists
2. **Settings merge**: Existing `.claude/settings.json` entries are preserved
3. **MCP merge**: Existing `.mcp.json` servers are preserved
4. **Idempotent**: Running multiple times produces the same result

Use this command to:
- Set up a fresh project
- Add missing configuration to an existing backlog
- Fix permissions after cloning a repo with Backlog.md
- Onboard a new team member to an existing project

## Notes

- Backlog.md stores all data as markdown files in the `backlog/` directory
- Tasks are human-readable files like `task-1 - Feature Name.md`
- All changes are tracked in git automatically
- The `mcp__backlog__*` permission pattern allows all backlog operations without prompts
