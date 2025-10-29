# Close GitHub Issue with Verification

Properly close a GitHub issue with summary comment and verification.

## Instructions

1. **Identify the issue**:
   - Ask: "Which issue number do you want to close?"
   - Or search if user provides keywords: `gh issue list --search "keyword"`

2. **View the issue**:
   ```bash
   gh issue view {number}
   ```
   - Show issue details to user
   - Confirm this is the correct issue to close

3. **Verify resolution**:
   - Ask: "What was done to resolve this?"
   - Ask: "Any follow-up tasks needed?"
   - If follow-up: Suggest creating new issues with `/gh-create-issue`

4. **Add closing comment**:
   ```bash
   gh issue comment {number} --body "Resolution summary here

   -cc"
   ```
   - **CRITICAL**: Always include "-cc" signature on its own line
   - Include what was done, how it was tested, and any relevant details

5. **Close the issue**:
   ```bash
   gh issue close {number}
   ```

6. **Verify closure**:
   ```bash
   gh issue view {number}
   ```
   - Confirm status is "CLOSED"
   - Show closing comment to user

## Important Reminders

- **NEVER** forget the "-cc" signature in comments
- **ALWAYS** add a closing comment before closing (documents resolution)
- **VERIFY** the issue is truly resolved before closing
- **CREATE** follow-up issues if needed before closing

## Definition of Done

- [ ] Correct issue identified and viewed
- [ ] Resolution verified with user
- [ ] Closing comment added with summary
- [ ] Comment includes "-cc" signature
- [ ] Issue status changed to CLOSED
- [ ] Closure verified with `gh issue view`
- [ ] Follow-up tasks created if needed
- [ ] User sees confirmation of closure
