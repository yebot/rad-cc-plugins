---
description: Save learnings, notes, and implementation details to tasks throughout work cycles. Use to document discoveries, decisions, and progress.
---

# Task Learnings & Notes

Document learnings, implementation notes, and progress on tasks to maintain project knowledge.

## Instructions

### Adding Implementation Notes

Notes capture what you've learned, tried, or decided during work:

```bash
# Set notes (replaces existing)
backlog task edit <task-id> --notes "Discovered that the API requires OAuth2 tokens"

# Append to existing notes (preserves history)
backlog task edit <task-id> --append-notes "Found solution: use refresh token rotation"
```

### Multi-line Notes (Bash/Zsh)

Use ANSI-C quoting for multi-line content:

```bash
backlog task edit <task-id> --notes $'## Progress\n- Completed API research\n- Identified auth requirements\n\n## Blockers\n- Waiting on API credentials\n\n## Next Steps\n- Implement token refresh'
```

### Implementation Plans

Plans document the approach before starting work:

```bash
# Set implementation plan
backlog task edit <task-id> --plan $'1. Research OAuth2 flow\n2. Set up auth middleware\n3. Implement token storage\n4. Add refresh logic\n5. Write tests'
```

### When to Add Learnings

Add notes when you:
- Discover something unexpected
- Make a technical decision
- Encounter and solve a problem
- Find useful resources or documentation
- Complete a milestone within the task
- Need to hand off to another agent/developer

### Viewing Task Documentation

```bash
# View full task with notes and plan
backlog task <task-id>

# Plain text output (good for scripts/AI)
backlog task <task-id> --plain
```

## Knowledge Preservation Patterns

**Progress Tracking**:
```
## Session 1 (2025-01-15)
- Set up project structure
- Installed dependencies

## Session 2 (2025-01-16)
- Implemented core API
- Found issue with rate limiting
```

**Decision Log**:
```
## Decisions
- Using PostgreSQL over MongoDB (better for relational data)
- Chose JWT over sessions (stateless scaling)
- Selected React Query for data fetching
```

**Troubleshooting Log**:
```
## Issues Encountered
1. CORS errors - solved by adding middleware
2. Memory leak - caused by unclosed connections
3. Test failures - mock timing issues
```