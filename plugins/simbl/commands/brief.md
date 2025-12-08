---
description: Show project snapshot - recent completions, in-progress work, and what's next
---

# Project Brief

Display a concise project snapshot for orientation at the start of a session.

## Instructions

### Step 1: Gather Data

Run these commands to collect project state:

```bash
# Recently completed (last 5)
simbl list --status done --limit 5

# Currently in progress
simbl list --status in-progress

# Up next (top 5 by priority)
simbl list --limit 5
```

### Step 2: Check for Triage Needs

Count unprioritized tasks:

```bash
simbl list | grep -v '\[p[1-9]\]' | wc -l
```

### Step 3: Format Output

Present a concise summary:

```
## Project Brief

### Recently Completed
- task-45: Implement user auth [p2]
- task-43: Fix login redirect [p1]
- task-41: Add password reset [p2]
<or "No recently completed tasks">

### In Progress
- task-48: Add rate limiting [p2] [in-progress]
- task-47: Refactor auth middleware [p3] [in-progress]
<or "No tasks in progress">

### Up Next (by priority)
1. task-50: Fix critical bug in checkout [p1]
2. task-49: Add email notifications [p2]
3. task-51: Update API docs [p3]
<or "Backlog is empty">

### Triage Needed
<N> tasks have no priority set. Consider running:
  simbl list | grep -v '\[p[1-9]\]'
<or omit this section if all tasks have priorities>
```

### Step 4: Suggest Next Action

Based on the brief:

- If tasks in-progress: "Continue with task-<id>?"
- If no in-progress but backlog exists: "Start task-<id> (highest priority)?"
- If backlog empty: "Backlog clear! Add new tasks with /simbl-add"
- If triage needed: "Consider prioritizing unprioritized tasks first?"

## Example Output

```
## Project Brief

### Recently Completed
- task-12: Add JWT authentication [p2]
- task-11: Fix session timeout [p1]
- task-10: Update login page UI [p3]

### In Progress
- task-15: Implement refresh tokens [p2] [in-progress]

### Up Next (by priority)
1. task-18: Add password requirements [p2]
2. task-19: Email verification flow [p2]
3. task-20: Update error messages [p3]
4. task-22: Add rate limiting [p3]
5. task-25: Improve logging [p4]

### Triage Needed
3 tasks have no priority set.

---

Continue with task-15 (refresh tokens)? Or switch to a different task?
```

## Notes

- Brief is for orientation, not detailed task view
- Use `simbl show <id>` for full task details
- Use `/simbl-start <id>` to begin focused work on a task
