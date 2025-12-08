---
description: Quick-capture a new task with auto-priority detection from keywords
---

# Quick-Capture a SIMBL Task

Quickly capture a new task with minimal friction and automatic priority detection.

## Arguments

- `$ARGUMENTS` - Task title (and optionally extra content on following lines)

## Instructions

### Step 1: Parse Input

- The first line/argument is the task **title**
- If user includes extra lines or pasted content, use that as `--content`

### Step 2: Auto-Priority Detection

Scan the title for urgency keywords and assign priority automatically:

| Keywords | Priority |
|----------|----------|
| `urgent`, `broken`, `blocker`, `critical`, `emergency`, `ASAP`, `fire`, `down`, `outage` | p1 |
| `important`, `soon`, `needed`, `high`, `priority` | p2 |
| `nice to have`, `eventually`, `someday`, `low priority`, `when possible`, `backlog` | p4 |
| (no keywords detected) | (no priority - triage later) |

**Case insensitive matching.**

### Step 3: Execute Command

Build and run the simbl command:

```bash
# With auto-detected priority
simbl add "<title>" --priority <N>

# With content
simbl add "<title>" --priority <N> --content "<extra content>"

# No priority detected
simbl add "<title>"
```

### Step 4: Confirm Creation

Report the result:

```
Created task-<id>: <title>
Priority: p<N> (auto-detected from "<keyword>")
```

Or if no priority:

```
Created task-<id>: <title>
No priority set - add one with: simbl tag add <id> p<N>
```

## Examples

### Simple title
```
User: /simbl-add Fix typo in README

Claude:
simbl add "Fix typo in README"

Created task-47: Fix typo in README
No priority set - add one with: simbl tag add task-47 p3
```

### Urgent keyword detected
```
User: /simbl-add URGENT: API returning 500 errors

Claude:
simbl add "URGENT: API returning 500 errors" --priority 1

Created task-48: URGENT: API returning 500 errors
Priority: p1 (auto-detected from "URGENT")
```

### With extra content
```
User: /simbl-add Add rate limiting to API
Need to prevent abuse. Max 100 requests per minute per user.
Should return 429 when exceeded.

Claude:
simbl add "Add rate limiting to API" --content "Need to prevent abuse. Max 100 requests per minute per user.
Should return 429 when exceeded."

Created task-49: Add rate limiting to API
No priority set - add one with: simbl tag add task-49 p3
```

### Important keyword
```
User: /simbl-add Important: Update auth tokens to use JWT

Claude:
simbl add "Important: Update auth tokens to use JWT" --priority 2

Created task-50: Important: Update auth tokens to use JWT
Priority: p2 (auto-detected from "Important")
```

## Notes

- Quick-capture is for speed - detailed tasks can be refined later with `simbl update`
- Auto-priority is a suggestion; user can override with `simbl tag add <id> p<N>`
- For complex tasks with acceptance criteria, use `simbl add` directly with full options
