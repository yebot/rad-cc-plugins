# Start Working on Backlog.md Task

Help the user start work on a Backlog.md task following the proper workflow.

## Instructions

1. **Identify the task**:
   - Ask the user which task they want to work on (by ID or search keyword)
   - If searching: `backlog search "{keyword}" --plain`
   - If by ID: Verify it exists with `backlog task {id} --plain`

2. **View the task**:
   ```bash
   backlog task {id} --plain
   ```
   - Show the task details to the user
   - Confirm this is the correct task

3. **Start the task** (mark as In Progress and assign):
   ```bash
   backlog task edit {id} -s "In Progress" -a @myself
   ```
   - This is the "start task ritual" - never skip it!
   - Verify the change: `backlog task {id} --plain`

4. **Create implementation plan**:
   - Ask the user about their approach OR
   - Analyze the task and propose a plan
   - Create plan with proper newlines:
   ```bash
   backlog task edit {id} --plan $'1. First step\n2. Second step\n3. Third step'
   ```

5. **Present plan for approval**:
   - Show the implementation plan to the user
   - **CRITICAL**: Wait for user approval before coding
   - Say: "I've created the implementation plan. Please review before I proceed with coding."

6. **Only after approval**:
   - Proceed with implementation
   - Remind user to check off ACs as they're completed
   - Remind about adding implementation notes

## Important Reminders

- **NEVER** edit task files directly
- **ALWAYS** use `backlog task edit` commands
- **WAIT** for user approval of plan before coding
- **VERIFY** all changes with `backlog task {id} --plain`

## Definition of Done for This Command

- [ ] Task status changed to "In Progress"
- [ ] Task assigned to user
- [ ] Implementation plan created and added to task
- [ ] Plan presented to user for approval
- [ ] User understands next steps
