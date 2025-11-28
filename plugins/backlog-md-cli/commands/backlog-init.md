# Initialize Backlog.md in Repository

Guide the user through initializing a Backlog.md presence in the current repository with proper directory structure.

## Instructions

1. **Determine repository name**:
   ```bash
   # Get the repository name from git
   basename -s .git `git config --get remote.origin.url` 2>/dev/null || basename "$(pwd)"
   ```

   - This extracts the repo name from the git remote URL
   - Falls back to current directory name if not a git repo

2. **Ask user for backlog name**:

   Use the AskUserQuestion tool to ask:

   - Question: "What should the backlog be named?"
   - Header: "Backlog Name"
   - Options:
     - Label: "Use repository name"
       Description: "Use '{repo_name}' as detected from the repository"
     - Label: "Custom name"
       Description: "Specify a different name for the backlog"

   If user selects "Custom name" or "Other", ask them to provide the custom name.

3. **Ask user for connection preference (MCP vs CLI)**:

   Use the AskUserQuestion tool to ask:

   - Question: "How would you like Claude Code to interact with Backlog.md?"
   - Header: "Connection"
   - Options:
     - Label: "MCP Server"
       Description: "Use Model Context Protocol for direct integration (recommended for Claude Code workflows)"
     - Label: "CLI Commands"
       Description: "Use backlog-md-cli commands via bash (requires CLI installation)"

   **Understanding the options:**

   - **MCP Server**:
     - Direct integration with Claude Code
     - No CLI installation required
     - Claude uses native tools to read/write task files
     - Faster and more seamless workflow
     - Recommended for most users

   - **CLI Commands**:
     - Uses the backlog-md-cli command-line tool
     - Requires separate installation (`npm install -g @backlog-md/cli`)
     - Traditional CLI workflow
     - Good for users who want to use backlog-md-cli outside Claude Code

   **Note the user's preference** for use in subsequent steps.

4. **Verify backlog directory doesn't exist**:
   ```bash
   # Check if backlog directory already exists
   if [ -d "backlog" ]; then
     echo "ERROR: backlog directory already exists"
     exit 1
   fi
   ```

   - If directory exists, warn the user and ask if they want to:
     - Abort initialization
     - Reinitialize (will preserve existing tasks)
     - Delete and start fresh (DANGEROUS - confirm twice)

5. **Create directory structure**:
   ```bash
   # Create the backlog directory hierarchy
   mkdir -p backlog/tasks
   mkdir -p backlog/drafts
   mkdir -p backlog/docs
   mkdir -p backlog/decisions
   ```

6. **Initialize based on connection preference**:

   **If user chose CLI Commands:**
   ```bash
   # Initialize the backlog with the chosen name
   backlog init "{backlog_name}"
   ```

   - Replace `{backlog_name}` with the name chosen by the user
   - This creates the necessary configuration files

   **If backlog CLI is not installed:**
   - Show installation instructions:
     ```bash
     # Install backlog-md-cli
     npm install -g @backlog-md/cli
     # or
     brew install backlog-md-cli
     ```
   - Ask user to install, then retry

   **If user chose MCP Server:**
   - Create a basic `.backlog/config.json` file:
     ```bash
     mkdir -p .backlog
     cat > .backlog/config.json <<EOF
{
  "name": "{backlog_name}",
  "version": "1.0.0",
  "connection": "mcp"
}
EOF
     ```
   - Inform user: "Backlog.md is configured for MCP. Claude Code will interact directly with task files."
   - Note: MCP server configuration is handled in Claude Code settings, not here

7. **Verify initialization**:
   ```bash
   # Verify directory structure
   tree backlog -L 2

   # Or if tree is not available
   find backlog -type d -maxdepth 2
   ```

   - Confirm all directories were created:
     - `backlog/tasks/`
     - `backlog/drafts/`
     - `backlog/docs/`
     - `backlog/decisions/`

8. **Create initial README** (optional but recommended):

   **If user chose CLI Commands:**
   ```bash
   backlog doc create "README" -c "# {backlog_name}

This project uses Backlog.md for task management.

## Quick Start

- Create tasks: \`backlog task create \"Task title\" -d \"Description\"\`
- List tasks: \`backlog task list --plain\`
- Start work: \`backlog task edit {id} -s \"In Progress\" -a @myself\`

See the full documentation for more details."
   ```

   **If user chose MCP Server:**
   ```bash
   cat > backlog/docs/README.md <<EOF
# {backlog_name}

This project uses Backlog.md for task management with MCP integration.

## Quick Start

- Create tasks: Use Claude Code's \`/backlog-create\` command
- List tasks: Claude can read from \`backlog/tasks/\` directly
- Start work: Use \`/backlog-start\` command

Claude Code interacts with task files directly through MCP.

See the full documentation for more details.
EOF
   ```

9. **Add to .gitignore** (optional):

   Ask user if they want to ignore certain backlog files:
   - Options:
     - Ignore drafts only (`backlog/drafts/`)
     - Ignore nothing (track everything in git)
     - Custom gitignore rules

   If user wants to ignore drafts:
   ```bash
   # Add to .gitignore
   echo "" >> .gitignore
   echo "# Backlog.md - ignore drafts" >> .gitignore
   echo "backlog/drafts/" >> .gitignore
   ```

10. **Show initialization summary**:

   Display to the user:

   **If user chose CLI Commands:**
   ```
   ✅ Backlog.md initialized successfully!

   Backlog name: {backlog_name}
   Location: ./backlog
   Connection: CLI Commands

   Directory structure created:
   - backlog/tasks/     (Task files)
   - backlog/drafts/    (Draft tasks)
   - backlog/docs/      (Documentation)
   - backlog/decisions/ (ADRs and decisions)

   Next steps:
   1. Create your first task: `backlog task create "Title"`
   2. View available commands: `backlog --help`
   3. Explore the task board: `backlog board`
   4. Use Claude Code commands: `/backlog-create`, `/backlog-start`
   ```

   **If user chose MCP Server:**
   ```
   ✅ Backlog.md initialized successfully!

   Backlog name: {backlog_name}
   Location: ./backlog
   Connection: MCP Server (direct integration)

   Directory structure created:
   - backlog/tasks/     (Task files)
   - backlog/drafts/    (Draft tasks)
   - backlog/docs/      (Documentation)
   - backlog/decisions/ (ADRs and decisions)

   Next steps:
   1. Create your first task: `/backlog-create`
   2. Use `/backlog-start` to begin working on a task
   3. Claude Code will interact with task files directly
   4. No CLI installation needed!
   ```

11. **Remind about workflow**:

   **If user chose CLI Commands:**
   - "Use `backlog task create` or `/backlog-create` to create your first task"
   - "Use `backlog task edit` or `/backlog-start` to begin working on a task"
   - "Use `/backlog-validate` to check backlog health"
   - "All operations should use the backlog CLI - never edit task files directly"

   **If user chose MCP Server:**
   - "Use `/backlog-create` to create your first task"
   - "Use `/backlog-start` to begin working on a task"
   - "Use `/backlog-validate` to check backlog health"
   - "Claude Code will handle task file operations automatically"
   - "Never edit task files directly - use Claude Code commands"

## Important Guidelines

### Directory Structure
- **backlog/tasks/**: Active tasks (tracked in git)
- **backlog/drafts/**: Draft tasks (optionally ignored in git)
- **backlog/docs/**: Project documentation
- **backlog/decisions/**: Architectural Decision Records (ADRs)

### Naming Conventions
- Task files: `task-{id} - {title}.md`
- Never create these manually - always use CLI

### What to Initialize
- ✅ Create directory structure
- ✅ Run `backlog init` command
- ✅ Optionally create README documentation
- ✅ Optionally configure .gitignore

### What NOT to Do
- ❌ Create task files manually
- ❌ Skip the `backlog init` command
- ❌ Initialize if backlog directory already exists (without confirmation)

## Error Handling

| Error | Solution |
|-------|----------|
| backlog directory exists | Confirm with user before proceeding |
| backlog CLI not found | Show installation instructions |
| Not in git repository | Still allow initialization (name defaults to directory) |
| Permission denied | Check directory permissions, suggest sudo if needed |
| backlog init fails | Show error, verify CLI version, check for conflicts |

## Multi-line Content

When creating initial documentation with newlines:
```bash
backlog doc create "Title" -c $'# Heading\n\nParagraph one.\n\nParagraph two.'
```

## Definition of Done for This Command

- [ ] Repository/backlog name determined
- [ ] User confirmed backlog name (custom or default)
- [ ] User selected connection preference (MCP or CLI)
- [ ] Directory structure created (tasks, drafts, docs, decisions)
- [ ] Initialization completed based on connection choice:
  - [ ] CLI: `backlog init` command executed successfully
  - [ ] MCP: `.backlog/config.json` created
- [ ] Directory structure verified
- [ ] Optional: README documentation created (appropriate for connection type)
- [ ] Optional: .gitignore configured
- [ ] Initialization summary displayed to user (showing connection type)
- [ ] User understands next steps and available commands for their connection type
