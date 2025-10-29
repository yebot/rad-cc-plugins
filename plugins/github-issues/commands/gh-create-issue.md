# Create GitHub Issue with Guided Workflow

Help the user create a well-structured GitHub issue with proper priority and metadata.

## Instructions

1. **Gather information**:
   - Ask: "What type of issue? (bug/feature/task/question)"
   - Ask: "What's the title?" (should be descriptive and action-oriented)
   - Ask: "Describe the issue or request"
   - If bug: Ask for steps to reproduce, expected vs actual behavior
   - If feature: Ask for acceptance criteria

2. **Assess priority**:
   - Check if priority labels exist: `gh label list`
   - If missing, create them (P1, P2, P3):
     ```bash
     gh label create P1 --description "Critical priority - blocks core functionality" --color d73a4a
     gh label create P2 --description "High priority - significant impact" --color fbca04
     gh label create P3 --description "Normal priority - standard workflow" --color 0e8a16
     ```
   - Ask: "What's the priority?" or suggest based on description:
     - P1: Blocking, security, affects all users
     - P2: Significant impact but has workaround
     - P3: Normal workflow items

3. **Additional metadata**:
   - Ask: "Any labels to add?" (bug, enhancement, documentation, etc.)
   - Ask: "Assign to anyone?"
   - Ask: "Link to milestone or project?"

4. **Create the issue**:
   ```bash
   gh issue create \
     --title "descriptive title" \
     --body "detailed description" \
     --label "P1,bug" \
     --assignee "@user"
   ```

5. **Confirm creation**:
   - Show the issue number and URL
   - Verify priority label is applied
   - Suggest next steps

## Definition of Done

- [ ] Issue created with descriptive title
- [ ] Issue body is complete and clear
- [ ] Priority label assigned (P1/P2/P3)
- [ ] Additional labels added as appropriate
- [ ] User sees issue number and URL
- [ ] User understands next steps
