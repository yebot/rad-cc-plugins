# Create New Backlog.md Task

Guide the user through creating a well-structured Backlog.md task with proper metadata.

## Instructions

1. **Gather task information**:

   a) **Title** (required):
      - Ask: "What's the task title?" (one-liner summary)
      - Format: Clear, action-oriented
      - Example: "Add user authentication" or "Fix payment processing bug"

   b) **Description** (required):
      - Ask: "What's the description?" (the "why")
      - Should explain: Purpose, goal, and context
      - NOT implementation details

   c) **Acceptance Criteria** (required):
      - Ask: "What are the acceptance criteria?" (the "what")
      - Guide user to write outcome-focused, testable criteria
      - Good: "User can log in with valid credentials"
      - Bad: "Add login() function to auth.ts"
      - Collect multiple ACs (at least 2-3 recommended)

   d) **Optional metadata**:
      - Labels: `backend`, `frontend`, `api`, `bug`, `feature`, etc.
      - Priority: `low`, `medium`, `high`
      - Assignee: `@username`
      - Status: Default is "To Do" (don't change unless user specifies)

2. **Create the task**:
   ```bash
   backlog task create "Title" \
     -d "Description" \
     --ac "First acceptance criterion" \
     --ac "Second acceptance criterion" \
     --ac "Third acceptance criterion" \
     -l label1,label2 \
     --priority medium
   ```

3. **Verify creation**:
   ```bash
   # List most recent task
   backlog task list --plain | tail -5
   ```

   - Confirm the task was created
   - Note the task ID assigned

4. **Validate file naming**:
   ```bash
   # Check the most recent task file
   ls -t backlog/tasks/ | head -1
   ```

   - **CRITICAL**: Verify it matches pattern `task-{id} - {title}.md`
   - If naming is incorrect:
     - ⚠️ ALERT: "File naming violation detected!"
     - Show the incorrect filename
     - Explain the correct pattern
     - This shouldn't happen with CLI, but verify anyway

5. **View the created task**:
   ```bash
   backlog task {id} --plain
   ```
   - Show the complete task to the user
   - Confirm all details are correct

6. **Remind about workflow**:
   - "Task created successfully!"
   - "When you're ready to work on it, use `/backlog-start` or:"
   - `backlog task edit {id} -s "In Progress" -a @myself`
   - "Remember: Add implementation plan only when you start work, not now"

## Important Guidelines

### What to Include During Creation
- ✅ Title (one-liner)
- ✅ Description (the "why")
- ✅ Acceptance Criteria (the "what")
- ✅ Labels, priority, assignee (optional)

### What NOT to Include During Creation
- ❌ Implementation plan (comes later when work starts)
- ❌ Implementation notes (comes at end when work completes)
- ❌ Status other than "To Do" (unless specifically requested)

### Acceptance Criteria Best Practices

Guide users to write good ACs:

**Good ACs** (outcome-focused, testable):
- "User can successfully log in with valid credentials"
- "System processes 1000 requests per second"
- "API returns 404 for non-existent resources"

**Bad ACs** (implementation-focused):
- "Add a login() function to auth.ts"
- "Use bcrypt for password hashing"
- "Install express middleware"

## Multi-line Input

For descriptions with multiple paragraphs:
```bash
backlog task create "Title" \
  -d $'First paragraph explaining context.\n\nSecond paragraph with more details.' \
  --ac "AC 1" \
  --ac "AC 2"
```

## Error Handling

- If `backlog` command not found: Guide user to install Backlog.md
- If creation fails: Show error and suggest fixes
- If naming violation detected: Alert and explain the pattern
- If user provides implementation details: Redirect to ACs instead

## Definition of Done for This Command

- [ ] All required information gathered (title, description, ACs)
- [ ] Task created using CLI
- [ ] Creation verified with `backlog task list`
- [ ] File naming validated (matches `task-{id} - {title}.md`)
- [ ] Task displayed to user for confirmation
- [ ] User understands next steps (use `/backlog-start` when ready)
