# Complete Backlog.md Task

Verify all Definition of Done items before marking a task as complete.

## Instructions

1. **View the task**:
   ```bash
   backlog task {id} --plain
   ```
   - Show complete task details to verify current state

2. **Verify Definition of Done checklist**:

   ### Via CLI (Required)

   a) **All Acceptance Criteria Checked**:
      - Look at the task output
      - Verify ALL ACs show `- [x]` (checked)
      - If any show `- [ ]` (unchecked):
        - ❌ STOP - Task cannot be marked complete
        - Ask user: "AC #{n} is not complete. Should we check it off or is there more work?"
        - If complete: `backlog task edit {id} --check-ac {n}`
        - If incomplete: Do not proceed

   b) **Implementation Notes Present**:
      - Check if "Implementation Notes" section has content
      - Should be PR-ready description: what was done, how, why
      - If missing or insufficient:
        - ❌ STOP - Task cannot be marked complete
        - Ask user to provide implementation notes
        - Add with: `backlog task edit {id} --notes "..."`

   c) **Status Ready for "Done"**:
      - Current status should be "In Progress" or similar
      - Will change to "Done" after verification

   ### Via Code/Testing (Confirm with User)

   d) **Tests Pass**:
      - Ask: "Have all tests passed?"
      - If no: Do not mark complete until tests pass

   e) **Linting/Type Checking Passes**:
      - Ask: "Does linting and type checking pass?"
      - If no: Fix issues first

   f) **Documentation Updated** (if applicable):
      - Ask: "Is documentation updated if needed?"

   g) **Code Reviewed**:
      - Ask: "Have you self-reviewed the changes?"

   h) **No Regressions**:
      - Ask: "Any regressions or known issues?"
      - If yes: Create follow-up tasks

3. **If ALL checks pass, mark as complete**:
   ```bash
   backlog task edit {id} -s Done
   ```

4. **Verify completion**:
   ```bash
   backlog task {id} --plain
   ```
   - Confirm status is "Done"
   - Confirm all ACs are checked
   - Confirm implementation notes are present

5. **Celebrate and remind**:
   - "✅ Task {id} marked as Done!"
   - "Summary of completed work:"
   - Show the implementation notes
   - Suggest next task if applicable

## Definition of Done Checklist

**DO NOT mark task as Done unless ALL of these are complete:**

### CLI Verifiable
- [ ] All acceptance criteria checked (`--check-ac`)
- [ ] Implementation notes added (`--notes`)
- [ ] Status can be changed to "Done"

### User Confirmed
- [ ] Tests pass
- [ ] Linting/type checking passes
- [ ] Documentation updated (if needed)
- [ ] Code self-reviewed
- [ ] No known regressions

## Common Issues

### Issue: User wants to mark done but ACs aren't all checked

**Response**:
```
❌ Cannot mark task as Done yet.

Current AC status:
- [x] AC #1: {text}
- [ ] AC #2: {text} ❌ NOT COMPLETE
- [x] AC #3: {text}

Either:
1. Complete AC #2 and check it off:
   backlog task edit {id} --check-ac 2

2. Or explain why AC #2 is no longer needed and remove it:
   backlog task edit {id} --remove-ac 2
```

### Issue: User wants to mark done but no implementation notes

**Response**:
```
❌ Cannot mark task as Done yet.

Implementation notes are missing. Please add a summary of what was implemented (like a PR description):

backlog task edit {id} --notes $'Summary of changes:\n- What was implemented\n- Why this approach\n- Testing done\n- Follow-up tasks'
```

### Issue: Tests failing but user wants to mark done

**Response**:
```
❌ Cannot mark task as Done with failing tests.

Please:
1. Fix failing tests, OR
2. Create a follow-up task for test fixes

A task is only "Done" when it's truly complete and shippable.
```

## Workflow Discipline

This command enforces workflow discipline:

- **No shortcuts**: All DoD items must be complete
- **Quality gate**: Prevents incomplete work from being marked done
- **Documentation**: Ensures knowledge is captured in implementation notes
- **Testing**: Confirms work is validated before completion

## Important Reminders

- **NEVER** mark a task as Done without verifying ALL DoD items
- **ALWAYS** use `backlog task edit {id} -s Done` (never edit files directly)
- **VERIFY** the change with `backlog task {id} --plain`
- **EDUCATE** users on why DoD matters (quality, completeness, documentation)

## Definition of Done for This Command

- [ ] Task DoD checklist verified (all items checked)
- [ ] Task status changed to "Done" via CLI
- [ ] Change verified with `backlog task {id} --plain`
- [ ] User sees confirmation of completion
- [ ] Implementation notes displayed to user
