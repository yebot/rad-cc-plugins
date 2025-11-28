---
description: Start working on a specific task by ID. Automatically sets status, guides implementation, and offers seamless transition to next task upon completion.
---

# Work on Task

Start focused work on a specified task, manage its lifecycle, and transition smoothly to the next task.

## Arguments

- `$ARGUMENTS` - Task identifier (e.g., "task-4", "4", "42")

## Instructions

### Phase 1: Task Initialization

1. **Parse the task identifier** from `$ARGUMENTS`:
   - Accept formats: `task-4`, `4`, `task-42`, `42`
   - Normalize to task ID (extract number if prefixed)

2. **Load the task**:
   ```bash
   backlog task <id>
   ```

3. **Verify task is workable**:
   - Check status is "To Do" or already "In Progress"
   - Check all dependencies are "Done"
   - If blocked, report blockers and suggest working on them first

4. **Set task to "In Progress"** (if not already):
   ```bash
   backlog task edit <id> --status "In Progress"
   ```

5. **Present task context to user**:
   - Display title, description, acceptance criteria
   - Show implementation plan if exists
   - List any prior implementation notes
   - Highlight what "done" looks like

### Phase 2: Implementation Work

1. **Begin implementation** based on:
   - Task description and acceptance criteria
   - Implementation plan (if provided)
   - Project context and codebase patterns

2. **During work, track progress**:
   - Check off acceptance criteria as completed:
     ```bash
     backlog task edit <id> --check-ac <criterion-number>
     ```
   - Append implementation notes for future reference:
     ```bash
     backlog task edit <id> --append-notes $'What was done:\n- Item 1\n- Item 2'
     ```

3. **If discovering new work**:
   - Create subtasks for scope creep
   - Update dependencies as needed
   - Keep original task focused

### Phase 3: Task Completion

When all acceptance criteria are met:

1. **Verify completion**:
   - Review all acceptance criteria are checked
   - Confirm implementation matches requirements
   - Run relevant tests if applicable

2. **Mark task as Done**:
   ```bash
   backlog task edit <id> --status "Done"
   ```

3. **Add completion notes**:
   ```bash
   backlog task edit <id> --append-notes $'Completed: <summary of what was done>'
   ```

### Phase 4: Transition

After completing the task, perform the following:

1. **Offer context compaction**:

   Ask the user:
   > "Task <id> is complete. Would you like me to compact the conversation context before continuing to the next task? This helps maintain performance for longer sessions."

   If yes: Use `/compact` to summarize and compress the conversation context.

2. **Identify the next task**:
   ```bash
   backlog task list --status "To Do" --sort priority
   ```

   Select the next task based on:
   - Highest priority first
   - Dependencies satisfied (blockers completed)
   - Related to just-completed work (if applicable)

3. **Present next task recommendation**:

   > "The next recommended task is **task-<next-id>: <title>** (priority: <priority>)."
   >
   > **Description**: <brief description>
   >
   > **Why this task**: <rationale - highest priority / unblocked / related work>
   >
   > Would you like me to start working on this task now?

4. **If user accepts**:
   - Recursively invoke this workflow for the next task
   - Seamlessly continue the work session

5. **If user declines**:
   - Show the board overview: `backlog board`
   - Offer alternative tasks if requested

## Error Handling

- **Task not found**: Search for similar tasks and suggest alternatives
- **Task already Done**: Inform user, offer to reopen or suggest next task
- **Dependencies not met**: List blocking tasks, offer to work on blockers instead
- **Invalid ID format**: Show accepted formats and ask for correction

## Example Session

```
User: /work 4

Claude: Loading task-4...

**Task 4: Implement user authentication**
Status: To Do → In Progress
Priority: High
Labels: auth, security

**Description:**
Add JWT-based authentication to the API endpoints.

**Acceptance Criteria:**
- [ ] Login endpoint returns JWT token
- [ ] Protected routes require valid token
- [ ] Token refresh mechanism works
- [ ] Logout invalidates token

**Implementation Plan:**
1. Add JWT library dependency
2. Create auth middleware
3. Implement login/logout endpoints
4. Add token refresh logic

Starting implementation...

[... implementation work happens ...]

All acceptance criteria complete. Marking task-4 as Done.

---

Task 4 is complete! Would you like me to compact the conversation
context before continuing to the next task?

[User: Yes]

Context compacted.

The next recommended task is **task-7: Add rate limiting** (priority: high).

**Description:** Implement rate limiting on API endpoints to prevent abuse.

**Why this task:** Highest priority unblocked task, security-related
(follows naturally from auth work).

Would you like me to start working on this task now?
```

## Notes

- Always verify acceptance criteria before marking Done
- Keep implementation notes concise but informative for future reference
- Context compaction is optional but recommended for long sessions
- Next task selection prioritizes unblocked, high-priority work
