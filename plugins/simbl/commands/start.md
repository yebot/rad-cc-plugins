---
description: Begin working on a SIMBL task - marks it in-progress and displays context
---

# Start Working on a SIMBL Task

Begin focused work on a specified task by marking it in-progress and displaying its full context.

## Arguments

- `$ARGUMENTS` - Task identifier (e.g., "task-42", "42")

## Instructions

### Step 1: Parse Task ID

Extract the task ID from `$ARGUMENTS`:
- Accept formats: `task-42`, `42`, or just digits
- If user supplies only digits (e.g., "9"), use "task-9" (or "{prefix}-9" if a custom prefix is configured)
- The CLI accepts short form, so passing just the number works

### Step 2: Mark as In-Progress

```bash
simbl tag add <id> in-progress
```

### Step 3: Display Task Context

```bash
simbl show <id>
```

### Step 4: Present to User

Display the task information clearly:

```
Starting work on task-<id>: <title>

**Status**: Now in-progress

**Description**:
<task description>

**Acceptance Criteria**:
<list criteria with checkboxes>

**Tags**: <tags>
```

### Step 5: Confirm Readiness

Ask the user:

> Ready to proceed with this task? Or would you like clarification on anything?

## Error Handling

- **Task not found**: Search for similar tasks and suggest alternatives
- **Already in-progress**: Inform user, show task anyway
- **Invalid ID format**: Show accepted formats

## Example

```
User: /simbl-start 42

Claude: Starting work on task-42: Fix null user crash in getProfile

**Status**: Now in-progress

**Description**:
getProfile() in UserService crashes when user not found.
File: src/services/UserService.ts:45-55

**Acceptance Criteria**:
- [ ] GET /api/users/:id returns 404 for non-existent user
- [ ] Response includes error message
- [ ] Existing tests pass
- [ ] New test covers null case

**Tags**: [p2] [backend] [bug]

Ready to proceed with this task? Or would you like clarification on anything?
```
