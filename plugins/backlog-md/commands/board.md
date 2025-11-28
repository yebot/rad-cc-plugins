---
description: View and interact with the Backlog.md Kanban board. Use to see project status at a glance, track progress across epics, and identify blocked tasks.
---

# Backlog Board

View the project's Kanban board showing all tasks organized by status.

## Instructions

### View the Board

```bash
# Interactive terminal board
backlog board

# Export to markdown file
backlog board export

# Export with version tag
backlog board export --export-version "v1.0.0"
```

### Board Features

The interactive board (`backlog board`) provides:
- **Column view**: Tasks organized by To Do / In Progress / Done
- **Task details**: Press Enter on a task to view details
- **Quick edit**: Press 'E' to edit task in your editor
- **Navigation**: Arrow keys to move between tasks
- **Dependency view**: See blocked tasks and blockers

### Web Interface

For a visual web-based board:
```bash
# Launch web UI (opens browser)
backlog browser

# Custom port
backlog browser --port 8080
```

### Board Analysis

When reviewing the board:

1. **Check "In Progress" column**:
   - Are tasks actually being worked on?
   - Any stale tasks that should move?

2. **Review "To Do" priorities**:
   - High priority items at top?
   - Dependencies resolved for next tasks?

3. **Validate "Done" tasks**:
   - All acceptance criteria met?
   - Ready to archive?

### Export for Sharing

```bash
# Export to default Backlog.md file
backlog board export

# Export with version for release notes
backlog board export --export-version "Sprint 3 Complete"

# Force overwrite
backlog board export --force
```

## Status Interpretation

| Status | Meaning |
|--------|---------|
| To Do | Not started, available for work |
| In Progress | Currently being worked on |
| Done | Completed, may need archiving |
| Blocked | Waiting on dependencies (shown with indicator) |