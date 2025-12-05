---
description: Synchronize task status with actual work completed. Use after making changes to update the backlog with current progress, learnings, and acceptance criteria status.
---

# Align Tasks with Work

Synchronize the Backlog.md backlog with actual work completed in the codebase.

## Instructions

### Step 1: Audit All "In Progress" Tasks

**CRITICAL**: Before anything else, audit every task currently marked "In Progress":

```bash
backlog list -s "In Progress" --plain
```

**For EACH "In Progress" task, verify its status is accurate**:

1. Read the task details: `backlog task <id> --plain`
2. Check if the work described is actually still in progress:
   - Look at the relevant files/code mentioned in the task
   - Check git history for related commits
   - Review acceptance criteria - are they met?
3. **If work is complete but status is "In Progress"**:
   - Update to "Done": `backlog task edit <id> -s "Done"`
   - Check off completed acceptance criteria: `--check-ac 1 --check-ac 2`
   - Add completion notes: `--append-notes "Completed: <summary>"`
4. **If work was abandoned or deprioritized**:
   - Move back to "Backlog": `backlog task edit <id> -s "Backlog"`
   - Add notes explaining why
5. **If genuinely still in progress**: Leave as-is, but add progress notes if needed

### Step 2: Review Recent Changes

- Check git status/diff for modified files
- Identify what functionality was added/changed/fixed

### Step 3: Find Related Tasks

- Search backlog for tasks related to the changes
- `backlog search "<keywords from changes>"`

### Step 4: For Each Related Task

a. **Update status** if needed:
   - Started work? → "In Progress"
   - Completed? → "Done"

b. **Check acceptance criteria**:
   - Review each criterion
   - Mark completed ones: `--check-ac <number>`

c. **Add learnings**:
   - Document what was done
   - Note any issues or decisions
   - `--append-notes "Implemented X using Y"`

d. **Update dependencies** if changed:
   - Add new dependencies discovered
   - Remove resolved blockers

### Step 5: Identify Untracked Work

- Any changes that don't match existing tasks?
- Offer to create new tasks for unplanned work

### Step 6: Report Summary

- List all tasks updated (status changes, notes added)
- Show tasks moved to "Done"
- Show remaining "In Progress" tasks (should be actively being worked on)
- Show current project status via `backlog board`

## Example Workflow

```bash
# 1. FIRST: Audit all "In Progress" tasks
backlog list -s "In Progress" --plain

# For each task shown, verify status is accurate:
backlog task 12 --plain  # Read task details
# Check if work is done - if so:
backlog task edit 12 -s "Done" --check-ac 1 --check-ac 2 \
  --append-notes "Completed: Feature fully implemented and tested"

# 2. See what changed recently
git diff --name-only HEAD~1

# 3. Search for related tasks
backlog search "authentication"
backlog search "login"

# 4. Update found tasks
backlog task edit 15 -s "In Progress" --check-ac 1 --check-ac 2 \
  --append-notes "Implemented basic auth flow, tokens working"

# 5. View updated task
backlog task 15 --plain

# 6. Check overall status
backlog board
```

## Alignment Checklist

After any work session, verify:
- [ ] **All "In Progress" tasks audited** - each one verified as genuinely in-progress
- [ ] No completed work is still marked "In Progress"
- [ ] All changed areas have corresponding tasks
- [ ] Task statuses reflect reality
- [ ] Completed work has acceptance criteria checked
- [ ] Implementation notes capture key decisions
- [ ] Unplanned work is tracked or documented