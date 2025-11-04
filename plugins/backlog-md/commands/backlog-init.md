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

3. **Verify backlog directory doesn't exist**:
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

4. **Create directory structure**:
   ```bash
   # Create the backlog directory hierarchy
   mkdir -p backlog/tasks
   mkdir -p backlog/drafts
   mkdir -p backlog/docs
   mkdir -p backlog/decisions
   ```

5. **Initialize with backlog CLI**:
   ```bash
   # Initialize the backlog with the chosen name
   backlog init "{backlog_name}"
   ```

   - Replace `{backlog_name}` with the name chosen by the user
   - This creates the necessary configuration files

   **If backlog CLI is not installed:**
   - Show installation instructions:
     ```bash
     # Install backlog-md CLI
     npm install -g @backlog-md/cli
     # or
     brew install backlog-md
     ```
   - Ask user to install, then retry

6. **Verify initialization**:
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

7. **Create initial README** (optional but recommended):
   ```bash
   backlog doc create "README" -c "# {backlog_name}

This project uses Backlog.md for task management.

## Quick Start

- Create tasks: \`backlog task create \"Task title\" -d \"Description\"\`
- List tasks: \`backlog task list --plain\`
- Start work: \`backlog task edit {id} -s \"In Progress\" -a @myself\`

See the full documentation for more details."
   ```

8. **Add to .gitignore** (optional):

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

9. **Show initialization summary**:

   Display to the user:
   ```
   ✅ Backlog.md initialized successfully!

   Backlog name: {backlog_name}
   Location: ./backlog

   Directory structure created:
   - backlog/tasks/     (Task files)
   - backlog/drafts/    (Draft tasks)
   - backlog/docs/      (Documentation)
   - backlog/decisions/ (ADRs and decisions)

   Next steps:
   1. Create your first task: `/backlog-create`
   2. View available commands: `backlog --help`
   3. Explore the task board: `backlog board`
   ```

10. **Remind about workflow**:
    - "Use `/backlog-create` to create your first task"
    - "Use `/backlog-start` to begin working on a task"
    - "Use `/backlog-validate` to check backlog health"
    - "All operations should use the backlog CLI - never edit task files directly"

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
- [ ] Directory structure created (tasks, drafts, docs, decisions)
- [ ] `backlog init` command executed successfully
- [ ] Directory structure verified
- [ ] Optional: README documentation created
- [ ] Optional: .gitignore configured
- [ ] Initialization summary displayed to user
- [ ] User understands next steps and available commands
