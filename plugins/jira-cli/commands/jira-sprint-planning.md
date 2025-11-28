# Jira Sprint Planning Command

Sprint planning, backlog grooming, and sprint execution workflows using jira-cli.

## Instructions

Guide users through complete agile sprint ceremonies and workflows using jira-cli.

## Sprint Lifecycle

```
Backlog Grooming → Sprint Planning → Sprint Execution → Daily Standups → Sprint Review → Retrospective → Repeat
```

## Phase 1: Backlog Grooming

Prepare the backlog before sprint planning.

### Review and Prioritize Backlog

**View all backlog items:**
```bash
jira issue list --status "To Do" --plain
```

**View by priority:**
```bash
jira issue list --status "To Do" --priority High,Critical --plain
```

**View unestimated stories:**
```bash
jira issue list --status "To Do" --jql "\"Story Points\" IS EMPTY" --plain
```

### Grooming Checklist

For each backlog item, ensure:

1. **Clear description** - Well-written user story or bug report
   ```bash
   jira issue view PROJ-123 --plain
   ```

2. **Acceptance criteria defined** - What "done" looks like
   ```bash
   jira issue edit PROJ-123 --body "
   ## Acceptance Criteria
   - [ ] User can login with email
   - [ ] Password validation in place
   - [ ] Error messages displayed
   "
   ```

3. **Properly sized** - Story points estimated
   ```bash
   jira issue edit PROJ-123 --custom story_points=5
   ```

4. **Dependencies identified** - Link blocking/blocked issues
   ```bash
   jira issue link PROJ-123 PROJ-100 "is blocked by"
   ```

5. **Questions answered** - No unknowns
   ```bash
   jira issue comment PROJ-123 "Clarified with product: should support OAuth and email/password"
   ```

### Grooming Activities

**Break down large stories:**
```bash
# Create subtasks for large story
jira issue create --type Subtask --parent PROJ-123 --summary "Create database schema"
jira issue create --type Subtask --parent PROJ-123 --summary "Implement API endpoints"
jira issue create --type Subtask --parent PROJ-123 --summary "Add UI components"
```

**Add labels for organization:**
```bash
jira issue edit PROJ-123 --label frontend,high-priority
```

**Update priority based on business value:**
```bash
jira issue edit PROJ-123 --priority High
```

## Phase 2: Sprint Planning

Plan the upcoming sprint iteration.

### Pre-Planning: Check Current Sprint

**View active sprint:**
```bash
jira sprint list --state active --plain
```

**Check sprint progress:**
```bash
jira sprint view <SPRINT_ID> --plain
```

**Identify incomplete items (to carry over):**
```bash
jira issue list --status "In Progress,To Do" --plain
```

### Sprint Planning Meeting

#### Step 1: Set Sprint Goal

Define the sprint objective (document outside Jira or in sprint description):
- What is the primary goal?
- What value will we deliver?
- What will we demo?

#### Step 2: Review Team Capacity

Calculate available capacity:
- Number of team members
- Days in sprint
- Planned time off
- Other commitments

Example: 5 developers × 10 days × 6 hours = 300 story points capacity

#### Step 3: Select Sprint Backlog

**List candidate stories (prioritized backlog):**
```bash
jira issue list --status "To Do" --priority High,Medium --plain
```

**View details for consideration:**
```bash
jira issue view PROJ-123 --plain
```

**Add items to sprint:**
```bash
jira sprint add <SPRINT_ID> PROJ-123 PROJ-124 PROJ-125
```

**Continue until capacity reached.**

#### Step 4: Assign Initial Ownership

**View sprint issues:**
```bash
jira sprint view <SPRINT_ID> --plain
```

**Assign to team members:**
```bash
jira issue assign PROJ-123 developer1@example.com
jira issue assign PROJ-124 developer2@example.com
jira issue assign PROJ-125 @me
```

#### Step 5: Verify Sprint Commitment

**Calculate total story points:**
```bash
# List all sprint issues with story points
jira issue list --jql "sprint = <SPRINT_ID>" --raw
```

Parse and sum story points to verify it matches capacity.

**Check for blockers:**
```bash
jira issue list --status Blocked --plain
```

Resolve blockers before sprint starts.

### Sprint Planning Checklist

- [ ] Sprint goal defined and communicated
- [ ] Team capacity calculated
- [ ] Backlog items selected and added to sprint
- [ ] Total story points ≤ team capacity
- [ ] All items meet Definition of Ready
- [ ] Initial assignments made
- [ ] Dependencies identified and managed
- [ ] No critical blockers
- [ ] Team agrees on commitment

### Definition of Ready

Before adding to sprint, ensure:
- [ ] User story clearly written
- [ ] Acceptance criteria defined
- [ ] Story pointed/estimated
- [ ] Dependencies identified
- [ ] Technical approach discussed
- [ ] No major unknowns

## Phase 3: Sprint Execution

Day-to-day sprint activities.

### Daily Workflow

**Morning: Check your work:**
```bash
jira issue list --assignee @me --status "In Progress,To Do" --plain
```

**Start working on item:**
```bash
jira issue move PROJ-123 "In Progress" --comment "Starting work on authentication"
```

**Throughout day: Update progress:**
```bash
jira issue comment PROJ-123 "Implemented login form, working on validation"
```

**End of day: Update status:**
```bash
jira issue comment PROJ-123 "Completed form validation, ready for API integration tomorrow"
```

**When blocked:**
```bash
jira issue move PROJ-123 "Blocked" --comment "Waiting for API specification from backend team"
jira issue link PROJ-123 PROJ-100 "is blocked by"
```

### Sprint Monitoring

**Check sprint progress:**
```bash
jira sprint view <SPRINT_ID> --plain
```

**Identify at-risk items:**
```bash
jira issue list --status "To Do" --priority High --plain
```

**Find blocked issues:**
```bash
jira issue list --status Blocked --plain
```

**Check unassigned work:**
```bash
jira issue list --assignee EMPTY --status "To Do" --plain
```

### Mid-Sprint Adjustments

**Add urgent issues (if capacity allows):**
```bash
jira sprint add <SPRINT_ID> PROJ-130
jira issue assign PROJ-130 @me
jira issue move PROJ-130 "In Progress"
```

**Remove items if overcommitted:**
```bash
# Remove from sprint (moves back to backlog)
jira sprint remove <SPRINT_ID> PROJ-125
```

## Phase 4: Daily Standup

Quick daily synchronization.

### Standup Report Generation

**My yesterday/today/blockers:**
```bash
# What I completed yesterday
jira issue list --assignee @me --status Done --jql "updated >= -1d" --plain

# What I'm working on today
jira issue list --assignee @me --status "In Progress" --plain

# My blockers
jira issue list --assignee @me --status Blocked --plain
```

### Team Status

**Overall sprint progress:**
```bash
jira sprint view <SPRINT_ID> --plain
```

**Team workload:**
```bash
jira issue list --status "In Progress" --plain
```

**Blockers across team:**
```bash
jira issue list --status Blocked --plain
```

### Standup Best Practices

1. **Keep it brief** - 15 minutes max
2. **Focus on progress** - What's done, what's next
3. **Identify blockers** - Not problem-solving session
4. **Update Jira before standup** - Issues reflect current state
5. **Follow up separately** - Deep discussions after standup

## Phase 5: Sprint Review

Demonstrate completed work.

### Pre-Review Preparation

**Completed items for demo:**
```bash
jira issue list --status Done --jql "sprint = <SPRINT_ID>" --plain
```

**Verify all done items meet Definition of Done:**
```bash
jira issue view PROJ-123 --plain
```

Check:
- Acceptance criteria met
- Tested and working
- Deployed (if applicable)
- Documented

### Review Metrics

**Sprint completion rate:**
```bash
# Total issues in sprint
jira issue list --jql "sprint = <SPRINT_ID>" --raw

# Completed issues
jira issue list --jql "sprint = <SPRINT_ID> AND status = Done" --raw

# Calculate percentage
```

**Story points completed:**
```bash
# Sum story points of completed issues
jira issue list --jql "sprint = <SPRINT_ID> AND status = Done" --raw | grep storyPoints
```

**Issue breakdown:**
```bash
# By type
jira issue list --jql "sprint = <SPRINT_ID>" --plain | grep -c Story
jira issue list --jql "sprint = <SPRINT_ID>" --plain | grep -c Bug
jira issue list --jql "sprint = <SPRINT_ID>" --plain | grep -c Task
```

### Incomplete Work

**Items not finished:**
```bash
jira issue list --jql "sprint = <SPRINT_ID> AND status != Done" --plain
```

**Move to next sprint or backlog:**
```bash
# Move to next sprint
jira sprint add <NEXT_SPRINT_ID> PROJ-125 PROJ-126

# Or move back to backlog
jira issue edit PROJ-127 --status "To Do"
```

### Review Artifacts

Document:
- Sprint goal achievement (met/not met)
- Velocity (story points completed)
- Completed items
- Demo feedback
- Incomplete items and reasons

## Phase 6: Sprint Retrospective

Reflect and improve.

### Retrospective Data Gathering

**Sprint metrics:**
```bash
# All sprint issues
jira issue list --jql "sprint = <SPRINT_ID>" --plain

# Completed work
jira issue list --jql "sprint = <SPRINT_ID> AND status = Done" --plain

# Issues that were blocked
jira issue list --jql "sprint = <SPRINT_ID> AND status was Blocked" --plain
```

### Retrospective Topics

1. **What went well?**
   - High velocity
   - Good collaboration
   - Smooth deployments

2. **What could be improved?**
   - Too many blockers
   - Underestimated complexity
   - Scope creep

3. **Action items**
   - Create issues for improvements
   ```bash
   jira issue create --type Task --summary "Improve estimation process" --label retrospective-action
   ```

### Track Retrospective Actions

**Create improvement tasks:**
```bash
jira issue create \
  --type Task \
  --summary "Set up automated testing pipeline" \
  --label retrospective-action,process-improvement \
  --assignee teamlead@example.com
```

**Review previous retrospective actions:**
```bash
jira issue list --label retrospective-action --status "To Do,In Progress" --plain
```

## Sprint Metrics and Reporting

### Velocity Tracking

**Last 3 sprints velocity:**
```bash
# Sprint 1
jira issue list --jql "sprint = <SPRINT_1> AND status = Done" --raw | grep storyPoints

# Sprint 2
jira issue list --jql "sprint = <SPRINT_2> AND status = Done" --raw | grep storyPoints

# Sprint 3 (current)
jira issue list --jql "sprint = <SPRINT_3> AND status = Done" --raw | grep storyPoints
```

Calculate average for future planning.

### Burndown Tracking

**Remaining work over time:**
```bash
# At sprint start: Total story points
# Daily: Remaining story points
jira issue list --jql "sprint = <SPRINT_ID> AND status != Done" --raw | grep storyPoints
```

Track daily to create burndown chart externally.

### Quality Metrics

**Bug rate:**
```bash
# Bugs in sprint
jira issue list --jql "sprint = <SPRINT_ID> AND type = Bug" --raw

# Bugs found post-deployment
jira issue list --jql "type = Bug AND created >= -14d AND labels = production" --raw
```

**Rework rate:**
```bash
# Issues returned from review
jira issue list --jql "status was 'In Review' AND status = 'In Progress'" --raw
```

## Epic Management

Epics span multiple sprints.

### Creating Epic

```bash
jira epic create --name "User Authentication System" --summary "Implement complete auth system"
```

### Planning Epic Across Sprints

**View epic details:**
```bash
jira epic view PROJ-100 --plain
```

**List all epic stories:**
```bash
jira issue list --jql "\"Epic Link\" = PROJ-100" --plain
```

**Distribute across sprints:**
```bash
# Sprint 1: Foundation
jira sprint add <SPRINT_1> PROJ-101 PROJ-102

# Sprint 2: Core features
jira sprint add <SPRINT_2> PROJ-103 PROJ-104

# Sprint 3: Polish
jira sprint add <SPRINT_3> PROJ-105 PROJ-106
```

### Epic Progress Tracking

**Completion status:**
```bash
# Total issues in epic
jira issue list --jql "\"Epic Link\" = PROJ-100" --raw

# Completed issues
jira issue list --jql "\"Epic Link\" = PROJ-100 AND status = Done" --raw
```

## Common Sprint Patterns

### Pattern 1: Standard Two-Week Sprint

```bash
# Week 1 Monday: Sprint Planning
jira sprint list --state future --plain  # Get next sprint ID
jira issue list --status "To Do" --priority High --plain  # Review backlog
jira sprint add <SPRINT_ID> PROJ-123 PROJ-124 PROJ-125  # Add to sprint
jira issue assign PROJ-123 @me  # Assign work

# Daily: Standups and updates
jira issue list --assignee @me --status "In Progress" --plain

# Week 2 Friday: Sprint Review & Retrospective
jira sprint view <SPRINT_ID> --plain  # Review progress
jira issue list --jql "sprint = <SPRINT_ID> AND status != Done" --plain  # Incomplete items

# Move incomplete items
jira sprint add <NEXT_SPRINT_ID> PROJ-126
```

### Pattern 2: Continuous Flow (Kanban)

```bash
# Regular backlog grooming
jira issue list --status "To Do" --plain

# Pull work as capacity allows
jira issue assign PROJ-123 @me
jira issue move PROJ-123 "In Progress"

# Track WIP limits
jira issue list --status "In Progress" --plain
```

### Pattern 3: Rapid Iteration (One-Week Sprints)

```bash
# Monday: Quick planning
jira sprint add <SPRINT_ID> PROJ-123 PROJ-124 PROJ-125

# Tuesday-Thursday: Execute
jira issue move PROJ-123 "In Progress"
# ... work ...
jira issue move PROJ-123 "Done"

# Friday: Review and retro (combined)
jira sprint view <SPRINT_ID> --plain
```

## Automation and Scripts

### Sprint Start Script

```bash
#!/bin/bash
# sprint-start.sh

SPRINT_ID=$1

echo "Starting Sprint $SPRINT_ID"

# List sprint contents
echo "Sprint Backlog:"
jira sprint view "$SPRINT_ID" --plain

# Check for blockers
echo -e "\nChecking for blockers:"
jira issue list --status Blocked --plain

# Team assignments
echo -e "\nTeam Workload:"
jira issue list --jql "sprint = $SPRINT_ID" --plain
```

### Daily Status Script

```bash
#!/bin/bash
# daily-status.sh

echo "===== My Work ====="
echo "In Progress:"
jira issue list --assignee @me --status "In Progress" --plain

echo -e "\nTo Do:"
jira issue list --assignee @me --status "To Do" --plain

echo -e "\nBlocked:"
jira issue list --assignee @me --status Blocked --plain

echo -e "\n===== Sprint Progress ====="
jira sprint view <SPRINT_ID> --plain
```

### Sprint End Script

```bash
#!/bin/bash
# sprint-end.sh

SPRINT_ID=$1
NEXT_SPRINT_ID=$2

echo "Completing Sprint $SPRINT_ID"

# Completed items
echo "Completed Issues:"
jira issue list --jql "sprint = $SPRINT_ID AND status = Done" --plain

# Incomplete items
echo -e "\nIncomplete Issues:"
INCOMPLETE=$(jira issue list --jql "sprint = $SPRINT_ID AND status != Done" --raw)
echo "$INCOMPLETE"

# Move incomplete to next sprint
echo -e "\nMoving incomplete items to Sprint $NEXT_SPRINT_ID"
# Extract issue keys and move (requires jq)
echo "$INCOMPLETE" | jq -r '.issues[].key' | while read issue; do
  jira sprint add "$NEXT_SPRINT_ID" "$issue"
done
```

## Best Practices

### Sprint Planning

1. **Don't overcommit** - Use 80% of capacity
2. **Balance work types** - Mix of features, bugs, tech debt
3. **Consider dependencies** - Don't block yourself
4. **Include buffer** - Time for unexpected issues
5. **Get team buy-in** - Everyone agrees on commitment

### Sprint Execution

1. **Update Jira daily** - Keep status current
2. **Communicate blockers** - Immediately when stuck
3. **Focus on sprint goal** - Avoid scope creep
4. **Swarm on blockers** - Help unblock teammates
5. **Demo early and often** - Get feedback during sprint

### Sprint Ceremonies

1. **Time-box meetings** - Respect team's time
2. **Come prepared** - Review work before meetings
3. **Stay focused** - Avoid rabbit holes
4. **Document decisions** - Record in Jira or wiki
5. **Action all items** - Every decision becomes a task

## Definition of Done

### Story Level

- [ ] Code complete and reviewed
- [ ] Unit tests written and passing
- [ ] Integration tests passing
- [ ] Documentation updated
- [ ] Deployed to staging
- [ ] QA approved
- [ ] Acceptance criteria met

### Sprint Level

- [ ] Sprint goal achieved
- [ ] All committed stories done
- [ ] Demo completed
- [ ] Stakeholder feedback gathered
- [ ] Retrospective conducted
- [ ] Velocity recorded
- [ ] Next sprint planned

## Troubleshooting

**Sprint not showing:**
- Check board configuration
- Verify sprint is created for correct board
- Ensure you have permissions

**Can't add issues to sprint:**
- Check if issue is in correct project
- Verify issue isn't in another sprint
- Ensure sprint isn't closed

**Sprint metrics incorrect:**
- Verify story points field is configured
- Check custom field names
- May need admin to configure

**Team velocity varies wildly:**
- Review estimation process
- Check for consistent team composition
- Consider external factors (holidays, etc.)

## Next Steps

- Use `jira-query-builder` agent for advanced sprint queries
- Set up automation scripts for common tasks
- Create dashboards for sprint metrics
- Integrate with CI/CD for automated updates
- Establish team norms and Definition of Done
