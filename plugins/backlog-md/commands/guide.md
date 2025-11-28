---
description: Quick reference guide for the backlog-md plugin. Use to learn or refresh your knowledge of available commands, agents, and workflows.
---

# Backlog.md Plugin Guide

Display this guide to help the user understand and use the backlog-md plugin effectively.

## Instructions

Present the following guide content to the user in a clear, readable format. This serves as a quick README for the plugin.

---

## What is Backlog.md?

Backlog.md is a **markdown-native task manager** that stores all project data as human-readable files in your repository. It's Git-friendly, supports MCP integration, and provides a CLI for task management.

**Key benefits**:
- Tasks are markdown files you can read/edit directly
- Everything is version-controlled with your code
- No external services required
- MCP support for AI agent integration

---

## Where Things Live

```
your-project/
└── backlog/
    ├── config.yml          # Project configuration
    ├── tasks/              # All task files
    │   ├── task-1 - Setup auth.md
    │   ├── task-2 - Add API endpoints.md
    │   └── ...
    └── archive/            # Completed/archived tasks
```

---

## Plugin Components

### Commands (Slash Commands)

| Command | Purpose |
|---------|---------|
| `/backlog-init` | Initialize Backlog.md in a project |
| `/board` | View the Kanban board |
| `/work <id>` | Start working on a task with guided completion |
| `/task-create` | Create a new task with full metadata |
| `/task-align` | Align current work with an existing task |
| `/epic` | Create/manage epics with subtasks |
| `/deps` | Manage and visualize dependencies |
| `/learnings` | Record project learnings and retrospectives |
| `/guide` | Show this guide |

### Agents (Automatic Helpers)

| Agent | When It Activates |
|-------|-------------------|
| **backlog-scout** | Exploring project state, finding blocked tasks, planning work order |
| **task-aligner** | Ensuring current work aligns with backlog tasks |
| **unplanned-handler** | Handling scope changes, creating tasks for unplanned work |

### Skills

| Skill | Purpose |
|-------|---------|
| **backlog-workflow** | Expert knowledge for task management patterns |

---

## Essential CLI Commands

### Task Management
```bash
backlog task create "Title"           # Create task
backlog task <id>                      # View task details
backlog task edit <id> --status "In Progress"
backlog task list                      # List all tasks
backlog task list -s "To Do"          # Filter by status
backlog task archive <id>             # Archive completed task
```

### Board & Overview
```bash
backlog board                          # Interactive Kanban board
backlog board export                   # Export to markdown
backlog overview                       # Project statistics
backlog search "keyword"              # Fuzzy search tasks
```

### Task Metadata
```bash
--desc, -d      "Description"         # Task description
--status, -s    "In Progress"         # Status
--priority      high|medium|low       # Priority level
--labels, -l    "api,auth"            # Comma-separated labels
--assignee, -a  "@username"           # Assignee
--ac            "Criterion"           # Acceptance criteria (repeatable)
--dep           "task-1,task-2"       # Dependencies
--plan          "Implementation plan" # Plan text
--notes         "Notes text"          # Implementation notes
--append-notes  "Additional notes"    # Append to existing notes
-p              <parent-id>           # Create as subtask of parent
```

### Acceptance Criteria
```bash
--check-ac 1                          # Mark criterion #1 complete
--uncheck-ac 2                        # Mark criterion #2 incomplete
--remove-ac 3                         # Remove criterion #3
```

---

## Common Workflows

### Starting a New Project
1. Run `/backlog-init` to set up Backlog.md
2. Use `/task-create` to add initial tasks
3. Use `/epic` to organize into larger features
4. Use `/deps` to establish task dependencies

### Daily Work Flow
1. Run `/board` to see current state
2. Use `/work <id>` to start a task
3. Complete the work, checking acceptance criteria
4. Accept next task recommendation or pick another

### When You Discover Unplanned Work
- The **unplanned-handler** agent will offer to create a task
- Or manually use `/task-create` to capture it
- Use `/task-align` to link current work to a task

---

## Tips

- **Multi-line input**: Use `$'Line 1\nLine 2'` syntax in bash
- **View raw task**: `backlog task <id> --plain` for markdown output
- **Web UI**: `backlog browser` opens a local web interface
- **Dependencies**: Tasks with unmet deps show as "Blocked"
- **Subtasks**: Create with `-p <parent-id>` for epic organization

---

## Quick Start

```bash
# 1. Initialize
backlog init "My Project"

# 2. Create first task
backlog task create "Set up development environment" \
  --priority high \
  --ac "Node.js installed" \
  --ac "Dependencies installed" \
  --ac "Dev server runs"

# 3. Start working
/work 1
```

---

**Need more help?** Use the backlog-workflow skill for detailed guidance on specific patterns.
