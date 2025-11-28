# Jira Issue Workflow Command

Complete issue lifecycle management from creation to completion using jira-cli.

## Instructions

Guide users through the entire issue lifecycle, from creation to resolution, using jira-cli commands.

## Issue Lifecycle Stages

```
Creation → Assignment → In Progress → Review → Testing → Done → Closed
```

Each stage has specific actions and best practices.

## Stage 1: Issue Creation

### Creating a New Issue

**Interactive creation** (easiest):
```bash
jira issue create
```

This prompts for:
- Issue type (Bug, Story, Task, etc.)
- Summary
- Description
- Priority
- Assignee
- Labels
- Components

**Command-line creation** (for automation):
```bash
jira issue create \
  --type Bug \
  --priority High \
  --summary "Login page returns 500 error" \
  --body "Detailed description of the issue" \
  --assignee user@example.com \
  --label backend,urgent \
  --component Authentication
```

**Quick creation**:
```bash
jira issue create --type Task --summary "Update dependencies" --priority Medium
```

### Best Practices for Issue Creation

1. **Clear, concise summary** - Describes what, not how
   - ✅ "Login page returns 500 error"
   - ❌ "Fix the code in auth.js"

2. **Detailed description** - Include:
   - Steps to reproduce (for bugs)
   - Acceptance criteria (for stories)
   - Context and background
   - Links to related resources

3. **Proper classification**:
   - **Bug**: Something broken that worked before
   - **Story**: New feature or functionality
   - **Task**: Work item that's not a bug or feature
   - **Epic**: Large body of work spanning multiple sprints

4. **Set appropriate priority**:
   - **Critical**: System down, blocking all work
   - **High**: Major feature broken, affects many users
   - **Medium**: Important but has workaround
   - **Low**: Nice to have, minimal impact

### Issue Creation Patterns

**Bug report with template:**
```bash
jira issue create --type Bug --summary "API endpoint /users returns 404" --body "
## Steps to Reproduce
1. Navigate to application
2. Click on Users section
3. Observe 404 error

## Expected Behavior
Should display list of users

## Actual Behavior
Returns 404 Not Found

## Environment
- Browser: Chrome 120
- OS: macOS 14
- Version: 2.1.0

## Additional Context
Started happening after deployment v2.1.0
Error logs show: 'Route not found'
"
```

**Story with acceptance criteria:**
```bash
jira issue create --type Story --summary "Add dark mode toggle" --body "
## User Story
As a user, I want to toggle dark mode so that I can reduce eye strain at night.

## Acceptance Criteria
- [ ] Toggle button in settings menu
- [ ] Persists preference across sessions
- [ ] Applies to all pages
- [ ] Smooth transition animation
- [ ] Respects system preferences by default

## Design
Link to Figma: https://figma.com/design/123
"
```

## Stage 2: Issue Assignment

### Assigning Issues

**Assign to specific user:**
```bash
jira issue assign PROJ-123 user@example.com
```

**Assign to self:**
```bash
jira issue assign PROJ-123 @me
```

**Unassign issue:**
```bash
jira issue assign PROJ-123 x
```

### When to Assign

- **During sprint planning** - Assign stories to team members
- **When starting work** - Assign to yourself before moving to "In Progress"
- **For review** - Reassign to reviewer
- **When blocked** - May unassign and add back to backlog

### Finding Unassigned Issues

```bash
jira issue list --assignee EMPTY --status "To Do" --plain
```

## Stage 3: Moving to In Progress

### Transition Issue to In Progress

**Interactive transition:**
```bash
jira issue move PROJ-123
```

Select "In Progress" from the menu.

**Direct transition:**
```bash
jira issue move PROJ-123 "In Progress"
```

**With comment:**
```bash
jira issue move PROJ-123 "In Progress" --comment "Starting work on this issue"
```

### Before Moving to In Progress

1. **Ensure assignment** - Issue should be assigned to you
2. **Understand requirements** - Read description and acceptance criteria
3. **Check dependencies** - Any blocking issues?
4. **Estimate work** - Add story points if needed

### Viewing Issue Details

```bash
jira issue view PROJ-123 --plain
```

Check:
- Description and acceptance criteria
- Comments and discussion
- Linked issues
- Attachments
- Custom fields

## Stage 4: During Development

### Updating Issue Status

Keep issue updated as work progresses:

**Add comments:**
```bash
jira issue comment PROJ-123 "Implemented authentication logic, now working on UI"
```

**Update fields:**
```bash
jira issue edit PROJ-123 --priority High
jira issue edit PROJ-123 --label "needs-review"
```

### Linking Related Issues

**Link to blocking issue:**
```bash
jira issue link PROJ-123 PROJ-100 "is blocked by"
```

**Link to related issue:**
```bash
jira issue link PROJ-123 PROJ-124 "relates to"
```

**Add web link:**
```bash
jira issue link PROJ-123 https://docs.example.com/feature --type web
```

### Common Link Types

- `blocks` / `is blocked by`
- `relates to`
- `duplicates` / `is duplicated by`
- `causes` / `is caused by`
- `clones` / `is cloned by`

### Tracking Time (if enabled)

Log work on issue:
```bash
jira issue worklog add PROJ-123 2h "Implemented authentication"
```

## Stage 5: Moving to Review

### Transition to Review

```bash
jira issue move PROJ-123 "In Review" --comment "PR: https://github.com/company/repo/pull/456"
```

### Review Checklist Before Transitioning

- [ ] Code complete and tested locally
- [ ] Unit tests written and passing
- [ ] Documentation updated
- [ ] Pull request created
- [ ] PR link added to issue
- [ ] Reviewers assigned

### Integration with Pull Requests

**Best practice:** Link PR to issue

In PR description:
```markdown
Fixes PROJ-123

## Changes
- Added authentication logic
- Updated user model
- Added tests
```

Or in commit messages:
```bash
git commit -m "PROJ-123: Add user authentication

Implemented OAuth2 authentication flow.
See PROJ-123 for requirements."
```

## Stage 6: Testing and QA

### If Issue Fails Review

**Move back to In Progress:**
```bash
jira issue move PROJ-123 "In Progress" --comment "Addressing review feedback: refactor auth logic"
```

**Address feedback then move back to Review**

### Moving to Testing

```bash
jira issue move PROJ-123 "Testing" --comment "Deployed to staging: https://staging.example.com"
```

### QA Checklist

- [ ] Meets acceptance criteria
- [ ] No regression in existing features
- [ ] Works in all supported environments
- [ ] Performance is acceptable
- [ ] Security best practices followed

## Stage 7: Completion

### Moving to Done

```bash
jira issue move PROJ-123 "Done" --comment "All acceptance criteria met. Deployed to production."
```

### Verification Before Closing

- [ ] All acceptance criteria satisfied
- [ ] Tested and approved
- [ ] Documented (if needed)
- [ ] Deployed (for features/bugs)
- [ ] Stakeholders notified

### Adding Resolution

Some workflows require setting resolution:
```bash
jira issue move PROJ-123 "Closed" --resolution "Fixed"
```

Common resolutions:
- `Fixed` - Bug fixed or feature completed
- `Won't Fix` - Decision not to address
- `Duplicate` - Same as another issue
- `Cannot Reproduce` - Bug not reproducible
- `Done` - Task completed

## Stage 8: Closure and Retrospective

### Closing Issue

```bash
jira issue move PROJ-123 "Closed" --comment "Verified in production. No issues reported."
```

### Post-Closure Activities

1. **Verify in production** - Ensure fix/feature works
2. **Update documentation** - User docs, wiki, etc.
3. **Notify stakeholders** - Let relevant parties know
4. **Link related issues** - If this resolves others
5. **Add retrospective notes** - What went well, what didn't

## Common Workflows

### Bug Fix Workflow

```bash
# 1. Create bug
jira issue create --type Bug --summary "..." --priority High

# 2. Assign to self and start
jira issue assign PROJ-123 @me
jira issue move PROJ-123 "In Progress"

# 3. Fix and create PR
# ... develop fix ...
git commit -m "PROJ-123: Fix login error"

# 4. Move to review with PR link
jira issue move PROJ-123 "In Review" --comment "PR: https://github.com/company/repo/pull/456"

# 5. After PR approval, merge and test
# ... merge PR ...

# 6. Move to testing
jira issue move PROJ-123 "Testing" --comment "Deployed to staging"

# 7. After QA approval
jira issue move PROJ-123 "Done" --comment "Verified on staging"

# 8. After production deployment
jira issue move PROJ-123 "Closed" --comment "Deployed to production in release v2.1.1"
```

### Feature Development Workflow

```bash
# 1. Create story
jira issue create --type Story --summary "Add dark mode toggle" --body "..."

# 2. Break down into subtasks (if needed)
jira issue create --type Subtask --parent PROJ-123 --summary "Create dark mode CSS"
jira issue create --type Subtask --parent PROJ-123 --summary "Add toggle component"
jira issue create --type Subtask --parent PROJ-123 --summary "Persist user preference"

# 3. Work through each subtask
jira issue move PROJ-124 "In Progress"
# ... develop ...
jira issue move PROJ-124 "Done"

# 4. When all subtasks done, complete parent story
jira issue move PROJ-123 "Done"
```

### Blocked Issue Workflow

```bash
# 1. Working on issue, discover blocker
jira issue move PROJ-123 "Blocked" --comment "Blocked by API issue PROJ-100"

# 2. Link to blocking issue
jira issue link PROJ-123 PROJ-100 "is blocked by"

# 3. When blocker resolved
jira issue move PROJ-123 "In Progress" --comment "Blocker resolved, resuming work"
```

## Bulk Operations

### Moving Multiple Issues

For sprint planning or cleanup:

```bash
# Get list of issues
jira issue list --status "To Do" --plain

# Move them (one at a time or use script)
jira issue move PROJ-123 "Backlog"
jira issue move PROJ-124 "Backlog"
jira issue move PROJ-125 "Backlog"
```

### Batch Assignment

```bash
# Assign multiple issues to team member
jira issue assign PROJ-123 developer@example.com
jira issue assign PROJ-124 developer@example.com
jira issue assign PROJ-125 developer@example.com
```

## Viewing Workflow States

### Available Transitions

To see available transitions for an issue:
```bash
jira issue move PROJ-123
```

This shows all possible next states based on current state and workflow configuration.

### Issue History

View all changes to an issue:
```bash
jira issue view PROJ-123 --plain
```

Scroll to history section to see all transitions, edits, and comments.

## Best Practices

1. **Update issues regularly** - Keep status current
2. **Add meaningful comments** - Explain changes and decisions
3. **Link related work** - Connect PRs, issues, and documentation
4. **Follow workflow** - Don't skip states
5. **Use appropriate transitions** - Don't move directly from "To Do" to "Done"
6. **Maintain traceability** - Always reference issue keys in commits/PRs
7. **Close issues promptly** - Don't leave completed work open
8. **Add resolution when closing** - Document why/how resolved

## Automation Integration

### Git Hooks

Add to `.git/hooks/commit-msg`:
```bash
#!/bin/bash
commit_msg_file=$1
commit_msg=$(cat "$commit_msg_file")

# Check if commit message contains issue key
if ! echo "$commit_msg" | grep -qE "PROJ-[0-9]+"; then
  echo "ERROR: Commit message must reference a Jira issue (e.g., PROJ-123)"
  exit 1
fi
```

### CI/CD Integration

In your CI/CD pipeline:
```bash
# Extract issue key from branch or commit
ISSUE_KEY=$(git branch --show-current | grep -oE "PROJ-[0-9]+")

# Add deployment comment
jira issue comment "$ISSUE_KEY" "Deployed to staging by CI/CD pipeline #${BUILD_NUMBER}"

# Optionally transition
jira issue move "$ISSUE_KEY" "Testing" --comment "Automated deployment to staging"
```

## Definition of Done

- [ ] Understand the complete issue lifecycle
- [ ] Can create issues with proper details
- [ ] Can assign issues to self and others
- [ ] Can transition issues through workflow states
- [ ] Can add comments and updates to issues
- [ ] Can link related issues and PRs
- [ ] Can close issues with appropriate resolution
- [ ] Understand when to use each workflow state
- [ ] Know how to handle blocked or problematic issues
- [ ] Can integrate Jira updates with development workflow

## Troubleshooting

**Issue won't transition:**
- Check if you have required fields filled
- Verify you have permission for that transition
- Some transitions require specific roles
- Try interactive mode to see available options

**Can't find issue:**
- Verify issue key is correct (PROJ-123)
- Check if you have access to that project
- Ensure issue hasn't been deleted

**Workflow differs from docs:**
- Workflows are customizable per project
- Run `jira issue move PROJ-123` to see your project's workflow
- Contact Jira admin for workflow documentation

## Next Steps

- Use `/jira-sprint-planning` for sprint management
- Use `jira-query-builder` agent for finding issues
- Integrate with git workflows and CI/CD
- Set up automation for common transitions
- Create templates for different issue types
