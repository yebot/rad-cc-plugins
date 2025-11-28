---
description: Synchronize task status with actual work completed. Use after making changes to update the backlog with current progress, learnings, and acceptance criteria status.
---

# Align Tasks with Work

Synchronize the Backlog.md backlog with actual work completed in the codebase.

## Instructions

1. **Review recent changes**:
   - Check git status/diff for modified files
   - Identify what functionality was added/changed/fixed

2. **Find related tasks**:
   - Search backlog for tasks related to the changes
   - `backlog search "<keywords from changes>"`

3. **For each related task**:

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

4. **Identify untracked work**:
   - Any changes that don't match existing tasks?
   - Offer to create new tasks for unplanned work

5. **Report summary**:
   - List tasks updated
   - Show current project status

## Example Workflow

```bash
# 1. See what changed
git diff --name-only HEAD~1

# 2. Search for related tasks
backlog search "authentication"
backlog search "login"

# 3. Update found tasks
backlog task edit 15 -s "In Progress" --check-ac 1 --check-ac 2 \
  --append-notes "Implemented basic auth flow, tokens working"

# 4. View updated task
backlog task 15 --plain

# 5. Check overall status
backlog board
```

## Alignment Checklist

After any work session, verify:
- [ ] All changed areas have corresponding tasks
- [ ] Task statuses reflect reality
- [ ] Completed work has acceptance criteria checked
- [ ] Implementation notes capture key decisions
- [ ] Unplanned work is tracked or documented