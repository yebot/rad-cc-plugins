# Jira Workflow Transitions Skill

Understanding and navigating Jira workflow states and transitions using jira-cli.

## Overview

Jira workflows define how issues move through different states from creation to completion. This skill helps you understand workflow concepts and effectively transition issues using jira-cli.

## Workflow Fundamentals

### What is a Workflow?

A workflow is a set of **statuses** and **transitions** that an issue moves through during its lifecycle.

**Status**: Current state of an issue (e.g., "To Do", "In Progress", "Done")

**Transition**: Action that moves an issue from one status to another (e.g., "Start Progress", "Resolve")

### Common Workflow Types

**1. Basic Workflow**
```
To Do → In Progress → Done
```

**2. Scrum Workflow**
```
Backlog → To Do → In Progress → In Review → Done → Closed
```

**3. Complex Workflow**
```
Open → In Progress → In Review → Testing → Blocked
                                         ↓
                                        Done → Closed
```

## Standard Workflow States

### Initial States

**Backlog**
- Issues that might be worked on in future
- Not yet committed to a sprint
- May need grooming

**To Do**
- Ready to be worked on
- Accepted into sprint or ready for picking up
- All requirements clear

**Open**
- Newly created issue
- Needs triage or assignment
- May need more information

### Active Work States

**In Progress**
- Actively being worked on
- Assigned to someone
- Development underway

**In Review**
- Code/work completed
- Awaiting peer review or approval
- Pull request open

**Testing / QA**
- Under quality assurance testing
- Verification of acceptance criteria
- May be on staging environment

### Blocked States

**Blocked**
- Cannot proceed
- Waiting on external dependency
- Requires resolution of blocker

**Waiting for Info**
- Need clarification or additional details
- Awaiting stakeholder input
- Cannot proceed without information

### Completion States

**Done**
- Work completed
- Accepted by product owner
- Meets Definition of Done

**Closed**
- Fully resolved and closed
- No further action needed
- Archived state

**Resolved**
- Issue addressed
- May need verification
- Intermediate completion state

### Rejection States

**Won't Fix**
- Decision not to address
- Out of scope
- Not a priority

**Duplicate**
- Same as another issue
- Linked to original issue
- Closed as duplicate

**Cannot Reproduce**
- Bug cannot be reproduced
- Insufficient information
- May reopen if new info emerges

## Transitioning Issues

### Basic Transition

```bash
jira issue move PROJ-123
```

This opens an interactive menu showing available transitions.

### Direct Transition

```bash
jira issue move PROJ-123 "In Progress"
```

Moves directly to specified state if transition is available.

### Transition with Comment

```bash
jira issue move PROJ-123 "Done" --comment "Completed feature implementation. Ready for deployment."
```

Always add comments to provide context about the transition.

### Checking Available Transitions

```bash
jira issue view PROJ-123 --plain
```

Shows current status and available next states.

## Common Transition Patterns

### Starting Work

**From To Do to In Progress:**
```bash
# 1. Assign to yourself
jira issue assign PROJ-123 @me

# 2. Move to In Progress
jira issue move PROJ-123 "In Progress" --comment "Starting work on authentication feature"
```

### Submitting for Review

**From In Progress to In Review:**
```bash
jira issue move PROJ-123 "In Review" --comment "PR created: https://github.com/company/repo/pull/456"
```

### Handling Review Feedback

**From In Review back to In Progress:**
```bash
jira issue move PROJ-123 "In Progress" --comment "Addressing review feedback: refactoring auth logic"
```

### Completing Work

**From In Review to Done:**
```bash
jira issue move PROJ-123 "Done" --comment "PR merged. All acceptance criteria met."
```

### Handling Blockers

**From In Progress to Blocked:**
```bash
jira issue move PROJ-123 "Blocked" --comment "Waiting for API spec from backend team"
jira issue link PROJ-123 PROJ-100 "is blocked by"
```

**From Blocked back to In Progress:**
```bash
jira issue move PROJ-123 "In Progress" --comment "Blocker resolved. Resuming work."
```

### Closing Issues

**From Done to Closed:**
```bash
jira issue move PROJ-123 "Closed" --comment "Verified in production. No issues reported."
```

### Rejecting Issues

**Won't Fix:**
```bash
jira issue move PROJ-123 "Closed" --resolution "Won't Fix" --comment "Decision: Out of scope for current roadmap"
```

**Duplicate:**
```bash
jira issue link PROJ-123 PROJ-100 "duplicates"
jira issue move PROJ-123 "Closed" --resolution "Duplicate" --comment "Duplicate of PROJ-100"
```

**Cannot Reproduce:**
```bash
jira issue move PROJ-123 "Closed" --resolution "Cannot Reproduce" --comment "Unable to reproduce. Please reopen with more details if issue persists."
```

## Workflow Best Practices

### 1. Always Add Comments

❌ Bad:
```bash
jira issue move PROJ-123 "In Progress"
```

✅ Good:
```bash
jira issue move PROJ-123 "In Progress" --comment "Starting with database schema design"
```

### 2. Update Before Transitioning

```bash
# Update fields first
jira issue edit PROJ-123 --priority High
jira issue assign PROJ-123 @me

# Then transition
jira issue move PROJ-123 "In Progress"
```

### 3. Link Related Work

```bash
# When moving to review, link PR
jira issue move PROJ-123 "In Review" --comment "PR: https://github.com/company/repo/pull/456"

# When blocking, link blocker
jira issue move PROJ-123 "Blocked"
jira issue link PROJ-123 PROJ-100 "is blocked by"
```

### 4. Don't Skip States

❌ Bad (skipping review):
```bash
jira issue move PROJ-123 "Done"  # Directly from In Progress
```

✅ Good (following workflow):
```bash
jira issue move PROJ-123 "In Review"  # From In Progress
# ... review happens ...
jira issue move PROJ-123 "Done"       # From In Review
```

### 5. Verify Before Completion

Before moving to Done:
```bash
# Review issue details
jira issue view PROJ-123 --plain

# Check acceptance criteria met
# Verify tests passing
# Confirm deployment successful

# Then complete
jira issue move PROJ-123 "Done" --comment "All acceptance criteria met. Deployed to production."
```

## Workflow States by Issue Type

### Bug Workflow

```
Open → In Progress → In Review → Testing → Fixed → Closed
                              ↓
                            Cannot Reproduce
                            Won't Fix
```

**Key transitions:**
```bash
# Start fix
jira issue move BUG-123 "In Progress" --comment "Investigating root cause"

# Submit fix
jira issue move BUG-123 "In Review" --comment "Fix PR: ..."

# After QA
jira issue move BUG-123 "Fixed" --comment "Verified on staging"

# After deployment
jira issue move BUG-123 "Closed" --comment "Fix deployed to production"
```

### Story Workflow

```
Backlog → To Do → In Progress → In Review → Done → Closed
```

**Key transitions:**
```bash
# Sprint planning
jira issue move STORY-123 "To Do" --comment "Added to Sprint 42"

# Start development
jira issue move STORY-123 "In Progress"

# Code review
jira issue move STORY-123 "In Review" --comment "PR: ..."

# Accept story
jira issue move STORY-123 "Done" --comment "Demo approved by PO"
```

### Task Workflow

```
To Do → In Progress → Done
```

**Key transitions:**
```bash
# Simple workflow
jira issue move TASK-123 "In Progress"
# ... work ...
jira issue move TASK-123 "Done"
```

### Epic Workflow

```
To Do → In Progress → Done → Closed
```

**Epics transition when child stories complete:**
```bash
# Start epic when first story starts
jira issue move EPIC-100 "In Progress"

# Complete epic when all stories done
jira issue move EPIC-100 "Done" --comment "All stories completed. Feature fully implemented."
```

## Handling Special Cases

### Reopening Issues

**Reopen a closed issue:**
```bash
jira issue move PROJ-123 "Reopened" --comment "Bug has reoccurred. New reproduction steps: ..."
```

Or back to original state:
```bash
jira issue move PROJ-123 "In Progress" --comment "Reopening to address regression"
```

### Moving Between Sprints

```bash
# Issue incomplete at sprint end
jira issue move PROJ-123 "To Do" --comment "Moving to Sprint 43 due to blocker"
jira sprint add <NEXT_SPRINT_ID> PROJ-123
```

### Escalating Priority

```bash
# Change priority
jira issue edit PROJ-123 --priority Critical

# Add urgency label
jira issue edit PROJ-123 --label urgent

# Move up in workflow if needed
jira issue move PROJ-123 "In Progress" --comment "Escalated to critical. Addressing immediately."
```

### Split Issues

When an issue is too large:
```bash
# Create new issues
jira issue create --type Story --summary "Part 1: ..." --parent PROJ-123
jira issue create --type Story --summary "Part 2: ..." --parent PROJ-123

# Close original or mark as epic
jira issue edit PROJ-123 --type Epic
```

## Workflow Automation

### Git Integration

**Pre-commit hook:**
```bash
#!/bin/bash
# Ensure commits reference Jira issue
if ! git log -1 --pretty=%B | grep -qE "PROJ-[0-9]+"; then
  echo "ERROR: Commit must reference Jira issue"
  exit 1
fi
```

**Post-merge hook:**
```bash
#!/bin/bash
# Auto-transition after merge
ISSUE_KEY=$(git log -1 --pretty=%B | grep -oE "PROJ-[0-9]+")
if [ -n "$ISSUE_KEY" ]; then
  jira issue move "$ISSUE_KEY" "Testing" --comment "Merged to main. Ready for QA."
fi
```

### CI/CD Integration

**On deployment:**
```bash
#!/bin/bash
# Extract issue keys from commits since last deploy
ISSUES=$(git log --pretty=%B $LAST_TAG..HEAD | grep -oE "PROJ-[0-9]+" | sort -u)

# Transition each issue
for issue in $ISSUES; do
  jira issue move "$issue" "Testing" --comment "Deployed to staging by CI/CD pipeline"
done
```

### Scheduled Status Updates

**Daily reminder script:**
```bash
#!/bin/bash
# Find stale "In Progress" issues
jira issue list --jql "\
  status = 'In Progress' AND \
  updated <= -3d AND \
  assignee = currentUser() \
" --plain

echo "Reminder: Update status on above issues"
```

## Troubleshooting Transitions

### Issue Won't Transition

**Problem:** Transition not available

**Solutions:**
1. Check current status
   ```bash
   jira issue view PROJ-123 --plain
   ```

2. View available transitions
   ```bash
   jira issue move PROJ-123  # Interactive mode shows options
   ```

3. Check required fields
   - Some transitions require fields to be filled
   - Use interactive mode to see requirements

4. Verify permissions
   - You may not have permission for certain transitions
   - Contact Jira admin if needed

### Missing Transition

**Problem:** Expected transition not showing

**Possible causes:**
- Workflow doesn't include that transition
- Conditional transition based on field values
- Permission restrictions
- Issue type has different workflow

**Solution:**
```bash
# Check what transitions are available
jira issue move PROJ-123

# Ask admin about workflow configuration
```

### Stuck in Status

**Problem:** Issue stuck in a status

**Solutions:**
1. Check for blockers
   ```bash
   jira issue view PROJ-123 --plain
   ```

2. Add comment explaining situation
   ```bash
   jira issue comment PROJ-123 "Stuck waiting for X. Escalating to Y."
   ```

3. Link blocking issues
   ```bash
   jira issue link PROJ-123 PROJ-100 "is blocked by"
   ```

4. Move to Blocked status
   ```bash
   jira issue move PROJ-123 "Blocked" --comment "Cannot proceed due to X"
   ```

### Accidental Transition

**Problem:** Moved to wrong status

**Solution:**
```bash
# Move back to correct status
jira issue move PROJ-123 "In Progress" --comment "Moved back to In Progress. Was accidentally marked as Done."
```

## Workflow Metrics

### Cycle Time

Time from "In Progress" to "Done":
```bash
# Issues completed this week
jira issue list --jql "\
  status = Done AND \
  resolved >= startOfWeek() \
" --raw
```

Calculate: `resolved_date - in_progress_date`

### Lead Time

Time from "To Do" to "Done":
```bash
# All resolved issues
jira issue list --jql "resolved >= startOfMonth()" --raw
```

Calculate: `resolved_date - created_date`

### Status Distribution

```bash
# Count issues by status
jira issue list --status "In Progress" --raw | grep -c key
jira issue list --status "In Review" --raw | grep -c key
jira issue list --status "Done" --raw | grep -c key
```

### Blocked Issue Tracking

```bash
# Currently blocked
jira issue list --status Blocked --plain

# How long blocked
jira issue list --jql "status = Blocked" --raw
```

## Custom Workflows

Organizations often customize workflows. To understand your workflow:

1. **View current issue state:**
   ```bash
   jira issue view PROJ-123 --plain
   ```

2. **See available transitions:**
   ```bash
   jira issue move PROJ-123  # Interactive mode
   ```

3. **Check workflow diagram:**
   - Ask Jira admin for workflow documentation
   - Or view in Jira UI: Project Settings → Workflows

4. **Document for team:**
   Create a workflow guide specific to your project

## When to Use This Skill

- Learning Jira workflow concepts
- Transitioning issues appropriately
- Handling blocked or stuck issues
- Integrating workflows with git/CI/CD
- Troubleshooting transition issues
- Understanding team's specific workflow

## Best Practices Summary

1. **Always add meaningful comments** when transitioning
2. **Follow the workflow** - don't skip states
3. **Update issue details** before transitioning
4. **Link related work** (PRs, blockers, etc.)
5. **Use appropriate transitions** for issue type
6. **Verify completion** before marking Done
7. **Handle blockers explicitly** - don't leave hanging
8. **Document custom workflows** for team reference

## Next Steps

- Document your team's specific workflows
- Create scripts for common transition patterns
- Set up automation for workflow events
- Define clear Definition of Done for each state
- Establish team norms around transitions
