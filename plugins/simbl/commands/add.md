---
description: Quick-capture a new task with auto-priority detection from keywords
---

# Quick-Capture a SIMBL Task

Quickly capture a new task with minimal friction and automatic priority detection.

## Arguments

- `$ARGUMENTS` - Task title (and optionally extra content on following lines)

## Instructions

### Step 1: Parse Input

- The first line/argument can loosely be assumed to be the task **title**
- If user includes extra lines or pasted content, assume this will be part of the `--content`

**Title Length & Content Extraction:**

If the supplied argument string is **over 90 characters** OR **contains an example** (code snippets, sample data, specific scenarios):

1. Extract a succinct title (under 80 characters) that captures the core task
2. Move the remaining detail into `--content`

This keeps titles scannable while preserving full context in the task body. DO NOT explain why title extraction is needed.

**Multiple Task Expansion:**

If the input clearly describes multiple distinct tasks, you may create separate tasks. However, **each task MUST include full context in its `--content`** - do not assume context carries over between tasks. Each task should be independently actionable without referencing the others.

### Step 2: Auto-Priority Detection

Scan the title for urgency keywords and assign priority automatically:

| Keywords                                                                                 | Priority                     |
| ---------------------------------------------------------------------------------------- | ---------------------------- |
| `urgent`, `broken`, `blocker`, `critical`, `emergency`, `ASAP`, `fire`, `down`, `outage` | p1                           |
| `important`, `soon`, `needed`, `high`, `priority`                                        | p2                           |
| `nice to have`, `eventually`, `someday`, `low priority`, `when possible`, `backlog`      | p4                           |
| (no keywords detected)                                                                   | (no priority - triage later) |

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

### Long argument (over 90 chars) - title extracted

```
User: /simbl-add We need to add a caching layer to the user profile endpoint because it's getting hit too frequently and causing database load issues

Claude:
simbl add "Add caching layer to user profile endpoint" --content "We need to add a caching layer to the user profile endpoint because it's getting hit too frequently and causing database load issues"

Created task-51: Add caching layer to user profile endpoint
No priority set - add one with: simbl tag add task-51 p3
```

### Argument with example - title extracted

```
User: /simbl-add Fix the date parsing bug, for example when user enters "2024-13-01" it crashes instead of showing validation error

Claude:
simbl add "Fix date parsing validation bug" --content "Fix the date parsing bug, for example when user enters \"2024-13-01\" it crashes instead of showing validation error"

Created task-52: Fix date parsing validation bug
No priority set - add one with: simbl tag add task-52 p3
```

## Notes

- Quick-capture is for speed - detailed tasks can be refined later with `simbl update`
- Auto-priority is a suggestion; user can override with `simbl tag add <id> p<N>`
- For complex tasks with acceptance criteria, use `simbl add` directly with full options
