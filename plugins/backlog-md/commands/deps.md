---
description: Manage task dependencies and execution sequences. Use to establish blocking relationships and validate dependency chains.
---

# Dependency Management

Create and manage dependencies between tasks to establish execution order and prevent blocked work.

## Instructions

### Adding Dependencies

Dependencies indicate that a task cannot start until its blockers are complete.

```bash
# Add single dependency
backlog task edit <task-id> --dep task-5

# Add multiple dependencies
backlog task edit <task-id> --dep task-1,task-2,task-3

# Create task with dependencies
backlog task create "Deploy to production" --dep task-10,task-11,task-12
```

### Viewing Dependencies

- **Task view**: `backlog task <id>` shows dependencies in the details
- **Board view**: `backlog board` displays dependency indicators
- **List with deps**: Dependencies shown in task listings

### Dependency Validation

Backlog.md automatically validates dependencies:
- **Circular dependency prevention**: Cannot create A→B→C→A chains
- **Existence validation**: Referenced tasks must exist
- **Status tracking**: See which dependencies are blocking

### Dependency Patterns

**Sequential Work**:
```
task-1 (Design) → task-2 (Implement) → task-3 (Test) → task-4 (Deploy)
```

**Parallel with Join**:
```
task-1 (Frontend) ─┐
                   ├→ task-3 (Integration)
task-2 (Backend)  ─┘
```

**Feature Gates**:
```
task-1 (Auth) ─┬→ task-2 (User Profile)
               ├→ task-3 (Settings)
               └→ task-4 (Dashboard)
```

## Execution Sequences

View recommended execution order:
```bash
# Via MCP, use project analytics tools to see execution plans
# The board view also shows dependency-aware ordering
backlog board
```

## Best Practices

1. Only add necessary dependencies - don't over-constrain
2. Keep dependency chains short (max 3-4 levels deep)
3. Review dependencies when tasks are blocked too long
4. Use dependencies for true blockers, not just suggested order