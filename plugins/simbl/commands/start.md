---
description: Begin working on a SIMBL task - marks it in-progress and displays context
---

# Start Working on a SIMBL Task

Begin focused work on a specified task by marking it in-progress and displaying its full context.

## Arguments

- `$ARGUMENTS` - Task identifier (e.g., "bnc-6", "task-42")

## Instructions

### Step 1: Resolve Full Task ID

**CRITICAL**: The SIMBL CLI requires the full task ID including the prefix (e.g., `bnc-6`, not just `6`).

1. If `$ARGUMENTS` already contains a hyphen (e.g., "bnc-6", "task-42"), use it as-is
2. If `$ARGUMENTS` is just a number (e.g., "6"), you MUST determine the prefix first:

   ```bash
   # Get the prefix from config
   simbl config get prefix 2>/dev/null || echo "task"
   ```

   Then construct the full ID: `{prefix}-{number}`

3. **Fallback**: If config doesn't exist, run `simbl list` to see actual task IDs and infer the prefix pattern from them

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

- **Task not found**:
  - First, check if you used the correct prefix (run `simbl list` to see actual task IDs)
  - If the prefix was wrong, retry with the correct full ID
  - If still not found, suggest similar task numbers
- **Already in-progress**: Inform user, show task anyway
- **Invalid ID format**: Remind user that full task IDs are required (e.g., "bnc-6", not "6")

## Example

```
User: /simbl:start 6

Claude: [Checks if "6" contains hyphen - it doesn't, so fetches prefix]
Claude: [Runs: simbl config get prefix → "bnc"]
Claude: [Constructs full ID: bnc-6]
Claude: [Runs: simbl tag add bnc-6 in-progress]
Claude: [Runs: simbl show bnc-6]

Starting work on bnc-6: Implement peak amplitude analysis

**Status**: Now in-progress

**Description**:
Analyze audio files for peak amplitude during folder scanning.

**Acceptance Criteria**:
- [ ] Peak amplitude extracted during file processing
- [ ] Value stored in manifest
- [ ] Existing tests pass

**Tags**: [p1] [project:server]

Ready to proceed with this task? Or would you like clarification on anything?
```
