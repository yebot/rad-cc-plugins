---
description: Organize tasks into epics using parent-child hierarchies. Use when planning large features that span multiple tasks.
---

# Epic Management

Organize related tasks into epics (parent tasks with subtasks) for better project structure and progress tracking.

## Understanding Epics in Backlog.md

Epics are implemented as parent tasks with child subtasks:
- A parent task acts as the epic container
- Child tasks are created with `-p <parent-id>`
- Progress is tracked by subtask completion
- Dependencies can span within and across epics

## Instructions

### Creating a New Epic

1. **Create the parent task** (the epic itself):
   ```bash
   backlog task create "User Authentication System" \
     --desc "Complete authentication implementation including OAuth, session management, and security" \
     --labels epic,auth
   ```

2. **Break down into subtasks**:
   ```bash
   backlog task create -p <epic-id> "Design auth database schema"
   backlog task create -p <epic-id> "Implement session management"
   backlog task create -p <epic-id> "Add OAuth2 providers"
   backlog task create -p <epic-id> "Create login/logout UI"
   backlog task create -p <epic-id> "Add security middleware"
   ```

3. **Set dependencies between subtasks**:
   ```bash
   backlog task edit <subtask-id> --dep <blocking-task-id>
   ```

### Viewing Epic Progress

- **List all subtasks**: `backlog task list -p <epic-id>`
- **View epic details**: `backlog task <epic-id>`
- **Check board**: `backlog board` shows hierarchical view

### Epic Organization Patterns

**Pattern 1: Feature Epic**
```
Epic: User Dashboard
├── task-10: Design dashboard layout
├── task-11: Create dashboard API endpoints
├── task-12: Build dashboard components
└── task-13: Add dashboard tests
```

**Pattern 2: Sprint/Milestone Epic**
```
Epic: Sprint 3 Goals
├── task-20: Fix login bug
├── task-21: Improve search performance
└── task-22: Add export feature
```

## Best Practices

1. Keep epics focused - one major feature or outcome
2. Limit subtasks to 5-10 per epic for manageability
3. Use labels consistently within an epic
4. Set realistic dependencies - don't over-constrain
5. Update epic description as scope evolves