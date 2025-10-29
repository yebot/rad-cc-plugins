# Triage Open Issues by Priority

Review open issues and ensure all have appropriate priority labels.

## Instructions

1. **Check for priority labels**:
   ```bash
   gh label list
   ```
   - If P1, P2, P3 labels don't exist, create them:
   ```bash
   gh label create P1 --description "Critical priority - blocks core functionality" --color d73a4a
   gh label create P2 --description "High priority - significant impact" --color fbca04
   gh label create P3 --description "Normal priority - standard workflow" --color 0e8a16
   ```

2. **List all open issues**:
   ```bash
   gh issue list --state open --limit 100
   ```
   - Show count of total open issues

3. **Identify issues without priority labels**:
   - Filter the list to find issues missing P1/P2/P3 labels
   - Show these to the user for triage

4. **For each unlabeled issue**:
   - Show issue details: `gh issue view {number}`
   - Assess priority based on:
     - **Impact scope**: How many users are affected?
     - **Severity**: How broken is the functionality?
     - **Urgency**: How time-sensitive is this?
     - **Business criticality**: Does this block revenue or key workflows?
   - Suggest priority level to user:
     - **P1**: Blocking, security vulnerabilities, affects all users, data loss
     - **P2**: Significant impact but has workaround, affects some users
     - **P3**: Nice-to-have, minor bugs, feature requests
   - Apply label after user confirms:
   ```bash
   gh issue edit {number} --add-label "P2"
   ```

5. **Generate priority summary**:
   ```bash
   gh issue list --label P1 --state open
   gh issue list --label P2 --state open
   gh issue list --label P3 --state open
   ```

6. **Report findings**:
   - Show count by priority:
     - P1 (Critical): X issues
     - P2 (High): X issues
     - P3 (Normal): X issues
     - Unlabeled: X issues (should be 0 after triage)
   - **Highlight P1 issues** that need immediate attention
   - List any unassigned P1/P2 issues
   - Suggest action items:
     - Assign critical issues
     - Create PRs for P1 items
     - Schedule P2 items

## Priority Assessment Guidelines

### P1 - Critical Priority
- System is down or unusable
- Security vulnerabilities
- Data loss or corruption
- Blocks all users from core functionality
- Production outage

### P2 - High Priority
- Significant feature broken but workaround exists
- Performance degradation
- Affects subset of users
- Important feature request with clear business value

### P3 - Normal Priority
- Minor bugs with minimal impact
- UI/UX improvements
- Feature requests
- Technical debt
- Documentation updates

## Definition of Done

- [ ] Priority labels verified to exist (or created)
- [ ] All open issues listed and reviewed
- [ ] Every open issue has a priority label (P1/P2/P3)
- [ ] Priority distribution report generated
- [ ] P1 issues highlighted for immediate action
- [ ] Unassigned critical issues noted
- [ ] Action items suggested to user
- [ ] User understands priority breakdown
