---
description: Find tasks that can be worked in parallel with current in-progress work
---

# Find Parallelizable Tasks

Identify tasks that are **not blocked** by in-progress work and could be started immediately in a parallel workflow.

## Instructions

### Step 1: Get In-Progress Task IDs

```bash
simbl list --status in-progress
```

Extract the task IDs (e.g., `bnc-1`, `bnc-6`) from the output.

### Step 2: Get All Pending Tasks

```bash
simbl list
```

This shows backlog tasks (pending/not done).

### Step 3: Filter for Parallelizable Tasks

A task is **parallelizable** if it meets ALL of these criteria:

1. **Not in-progress** - already being worked on
2. **Not blocked by in-progress tasks** - no `depends-on-{id}` tag where `{id}` is in-progress
3. **Not a child of an in-progress task** - no `child-of-{id}` tag where `{id}` is in-progress (children should complete before parent)

**Analysis approach:**
- For each pending task, check its tags for `depends-on-*` and `child-of-*`
- If any of those referenced IDs are in the in-progress list, the task is **blocked**
- Otherwise, it's **available for parallel work**

### Step 4: Prioritize Results

Sort parallelizable tasks by:
1. Priority (p1 > p2 > p3 > etc.)
2. Tasks with fewer dependencies first (simpler to start)

### Step 5: Present Findings

```
## Parallel Work Opportunities

### Currently In Progress
- {id}: {title} [{tags}]

### Available for Parallel Work
These tasks have no dependencies on in-progress work:

1. {id}: {title} [{priority}] [{project}]
   → Can start immediately

2. {id}: {title} [{priority}] [{project}]
   → Can start immediately

### Blocked Tasks (waiting on in-progress)
- {id}: {title} - blocked by {blocking-id}
- {id}: {title} - child of {parent-id}

---

Recommend starting: {highest-priority-available-id}
Use `/simbl:start {id}` to begin.
```

## Example

Given this state:
```
# In Progress
bnc-1 Phase 1: Bounce Server - Core [in-progress]

# Backlog
bnc-6 Implement peak amplitude [depends-on-bnc-3]
bnc-7 Phase 2: Auth & Playlists [depends-on-bnc-1]  ← BLOCKED
bnc-14 Phase 3: iOS Core [depends-on-bnc-4]
bnc-8 Implement PIN generation [child-of-bnc-7]     ← BLOCKED (parent blocked)
```

Output:
```
## Parallel Work Opportunities

### Currently In Progress
- bnc-1: Phase 1: Bounce Server - Core [p1][project:server]

### Available for Parallel Work
1. bnc-14: Phase 3: iOS Core [p1][project:ios]
   → depends-on-bnc-4 (bnc-4 is done) ✓

2. bnc-6: Implement peak amplitude [p1][project:server]
   → depends-on-bnc-3 (bnc-3 is done) ✓

### Blocked Tasks
- bnc-7: Phase 2: Auth & Playlists - blocked by bnc-1 (in-progress)
- bnc-8: Implement PIN generation - child-of-bnc-7 (which is blocked)

---

Recommend starting: bnc-14 (Phase 3: iOS Core)
Use `/simbl:start bnc-14` to begin.
```

## Edge Cases

- **No in-progress tasks**: All unblocked tasks are available
- **All tasks blocked**: Suggest completing current work first
- **No pending tasks**: Backlog is clear

## Notes

- This helps identify work that won't create merge conflicts or dependency issues
- Useful for pairing sessions or when you have capacity to context-switch
- Child tasks should generally wait for parent task structure to stabilize
