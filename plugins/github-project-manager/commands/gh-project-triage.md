---
name: gh-project-triage
description: Triage project items and ensure proper status and priority assignment
tools: Bash, AskUserQuestion, TodoWrite
model: sonnet
---

# Triage GitHub Project Items

This command facilitates systematic triage of project items, ensuring all items have proper priority, status, and other critical field assignments.

## Instructions

### Step 1: Initialize Triage Session

Ask the user what scope of triage they want:

1. **Full Triage**: Review all items in the project
2. **Backlog Only**: Focus on Backlog status items
3. **Unprioritized**: Only items missing priority
4. **New Items**: Items added in last N days
5. **Custom Filter**: User-specified criteria

### Step 2: Gather Project Data

```bash
# Get project info
PROJECT_DATA=$(gh project view <number> --owner "@me" --format json)
PROJECT_ID=$(echo $PROJECT_DATA | jq -r '.id')
PROJECT_TITLE=$(echo $PROJECT_DATA | jq -r '.title')

# Get fields and options
FIELDS=$(gh project field-list <number> --owner "@me" --format json)

# Extract field IDs
STATUS_FIELD=$(echo $FIELDS | jq -r '.[] | select(.name=="Status") | .id')
PRIORITY_FIELD=$(echo $FIELDS | jq -r '.[] | select(.name=="Priority") | .id')

# Get field options
STATUS_OPTIONS=$(echo $FIELDS | jq -r '.[] | select(.name=="Status") | .options[] | {name: .name, id: .id}')
PRIORITY_OPTIONS=$(echo $FIELDS | jq -r '.[] | select(.name=="Priority") | .options[] | {name: .name, id: .id}')

# Get all items
ITEMS=$(gh project item-list <number> --owner "@me" --format json --limit 100)
```

### Step 3: Filter Items Based on Triage Scope

```bash
# Example: Unprioritized items
TRIAGE_ITEMS=$(echo $ITEMS | jq -r '
  .items[] |
  select(
    (.fieldValues[] | select(.name=="Priority")) == null
  ) |
  {
    id: .id,
    title: .content.title,
    number: .content.number,
    type: .content.type,
    url: .content.url,
    body: .content.body,
    labels: .content.labels,
    status: (.fieldValues[] | select(.name=="Status") | .name)
  }
')

TRIAGE_COUNT=$(echo $TRIAGE_ITEMS | jq -s 'length')
```

### Step 4: Present Triage Summary

Show user what needs triage:

```markdown
## Triage Summary

**Project**: [Project Title] (#[Number])
**Scope**: [Triage scope selected]
**Items to Triage**: [Count]

### Breakdown
- Unprioritized: [X]
- Without status: [Y]
- Missing estimation: [Z] (if applicable)
- No assignee: [A] (if applicable)

**Proceeding with triage...**
```

### Step 5: Interactive Triage Loop

For each item requiring triage:

#### A. Present Item Details

```markdown
---
## Item [current]/[total]

**Title**: [Item title]
**Number**: #[number] (or "draft")
**Type**: [Issue/PR/Draft]
**Current Status**: [Status or "Not set"]
**Current Priority**: [Priority or "Not set"]
**URL**: [URL if available]

### Description
[First 200 chars of body...]

### Labels
[List issue labels if any]

### Context Hints
[Analyze title/description for priority hints:]
- Contains "critical", "blocking", "urgent" → Suggests P0/P1
- Contains "bug", "error", "broken" → Suggests P1/P2
- Contains "enhancement", "feature" → Suggests P2/P3
- Contains "nice-to-have", "someday" → Suggests P3
```

#### B. Assess Priority

Use intelligent priority suggestion:

```bash
# Auto-suggest priority based on keywords
TITLE_LOWER=$(echo "$ITEM_TITLE" | tr '[:upper:]' '[:lower:]')
BODY_LOWER=$(echo "$ITEM_BODY" | tr '[:upper:]' '[:lower:]')
COMBINED="$TITLE_LOWER $BODY_LOWER"

if echo "$COMBINED" | grep -qE "critical|blocking|urgent|security|production down|data loss"; then
  SUGGESTED_PRIORITY="P0"
  REASON="Critical keywords detected (blocking, security, urgent)"
elif echo "$COMBINED" | grep -qE "bug|error|broken|failing|regression"; then
  SUGGESTED_PRIORITY="P1"
  REASON="Bug-related keywords detected"
elif echo "$COMBINED" | grep -qE "enhancement|feature|improve"; then
  SUGGESTED_PRIORITY="P2"
  REASON="Enhancement/feature keywords detected"
else
  SUGGESTED_PRIORITY="P3"
  REASON="Standard priority (no high-urgency indicators)"
fi

# Check issue labels for additional hints
if echo "$LABELS" | grep -qE "critical|p0"; then
  SUGGESTED_PRIORITY="P0"
  REASON="Critical label found"
elif echo "$LABELS" | grep -qE "bug|urgent|p1"; then
  SUGGESTED_PRIORITY="P1"
  REASON="Bug/urgent label found"
fi
```

Present suggestion and ask for confirmation:

```markdown
### Suggested Priority: [P0/P1/P2/P3]
**Reasoning**: [Reason based on analysis]

**Priority Criteria**:
- **P0 (Critical)**: Blocking issues, security vulnerabilities, data loss, production outages
- **P1 (High)**: Important bugs, features affecting many users, time-sensitive work
- **P2 (Medium)**: Standard enhancements, non-blocking bugs, improvements
- **P3 (Low)**: Nice-to-have features, minor improvements, future work

**Select Priority**: [P0/P1/P2/P3/Skip]
```

#### C. Assess Status

If status is not set or needs review:

```markdown
### Current Status: [Status or "Not set"]

**Recommended Status**:
- **Backlog**: Not yet refined or scheduled
- **Todo**: Refined and ready to start
- **In Progress**: Actively being worked on
- **In Review**: PR open, awaiting review
- **Done**: Completed and merged/deployed

**Select Status**: [Backlog/Todo/In Progress/In Review/Done/Skip]
```

#### D. Update Item

Apply the selected field values:

```bash
# Update priority
if [ "$SELECTED_PRIORITY" != "Skip" ]; then
  PRIORITY_OPTION_ID=$(echo $PRIORITY_OPTIONS | jq -r ". | select(.name==\"$SELECTED_PRIORITY\") | .id")

  gh project item-edit --id $ITEM_ID --project-id $PROJECT_ID \
    --field-id $PRIORITY_FIELD \
    --single-select-option-id $PRIORITY_OPTION_ID

  echo "✅ Updated priority to $SELECTED_PRIORITY"
fi

# Update status
if [ "$SELECTED_STATUS" != "Skip" ]; then
  STATUS_OPTION_ID=$(echo $STATUS_OPTIONS | jq -r ". | select(.name==\"$SELECTED_STATUS\") | .id")

  gh project item-edit --id $ITEM_ID --project-id $PROJECT_ID \
    --field-id $STATUS_FIELD \
    --single-select-option-id $STATUS_OPTION_ID

  echo "✅ Updated status to $SELECTED_STATUS"
fi
```

#### E. Ask About Additional Fields

If project has other important fields:

```markdown
### Additional Fields (Optional)

- **Story Points**: [1/2/3/5/8/13/Skip]
- **Component**: [Frontend/Backend/DevOps/Skip]
- **Assignee**: [@username or Skip]
- **Sprint/Iteration**: [Current/Next/Later/Skip]

**Skip all additional fields?** [Yes/No]
```

### Step 6: Batch Mode (Alternative)

For experienced users or bulk triage, offer batch mode:

```markdown
## Batch Triage Mode

Applying automatic prioritization based on keywords and labels...

[For each item:]
- #[number] [title]
  → Priority: P[X] (reason: [reason])
  → Status: [Status]

**Preview [X] changes. Proceed?** [Yes/No/Review individually]
```

### Step 7: Generate Triage Report

After completing triage:

```markdown
# Triage Session Complete

**Project**: [Project Title]
**Duration**: [Start time - End time]
**Items Processed**: [Count]

---

## Summary of Changes

### Priority Assignment
- P0 (Critical): [X] items
- P1 (High): [Y] items
- P2 (Medium): [Z] items
- P3 (Low): [A] items
- Skipped: [B] items

### Status Assignment
- Backlog: [X] items
- Todo: [Y] items
- In Progress: [Z] items
- Skipped: [A] items

### Field Updates Total
- [X] items updated
- [Y] items skipped
- [Z] items had errors

---

## Items Still Requiring Attention

[If any items were skipped or errored:]
- #[number] [title] - [Reason for skip/error]

---

## Project Health After Triage

**Priority Coverage**: [X]% of items now have priority
**Status Coverage**: [Y]% of items have appropriate status
**Recommendations**:
[Provide 2-3 recommendations based on triage results]

---

## Next Steps

1. **Review P0/P1 items**: Ensure critical items are scheduled
2. **Sprint planning**: Move refined items from Backlog to Todo
3. **Assign work**: Distribute items to team members
4. **Regular triage**: Schedule weekly triage sessions

**View updated project**: [Project URL]
```

## Triage Best Practices

### Priority Assessment Guidelines

**P0 Criteria** (Critical - Immediate attention):
- Production is down or severely degraded
- Data loss or corruption risk
- Security vulnerability
- Blocking all users from core functionality
- Legal or compliance risk

**P1 Criteria** (High - This week):
- Significant user impact (>25% of users)
- Important feature broken
- High-value customer request
- Sprint commitment
- Dependency for other work

**P2 Criteria** (Medium - This month):
- Moderate user impact
- Standard feature request
- Improvement to existing feature
- Non-blocking bug
- Technical debt with visible impact

**P3 Criteria** (Low - Backlog):
- Nice-to-have feature
- Minor cosmetic issue
- Optimization without user impact
- Long-term improvements
- Ideas for future exploration

### Status Assessment Guidelines

**When to use Backlog**:
- Item needs more information
- Not yet refined or estimated
- Awaiting dependencies
- Future work, not committed

**When to use Todo**:
- Fully refined and ready to start
- Acceptance criteria defined
- No blockers
- Can be pulled into current sprint

**When to use In Progress**:
- Work has actively started
- Assignee is working on it
- PR may or may not exist yet

**When to use In Review**:
- PR is open
- Awaiting code review
- Testing in progress
- Documentation pending

**When to use Done**:
- Code merged
- Tests passing
- Deployed to production (if applicable)
- Acceptance criteria met

## Automation Suggestions

After triage, suggest automation rules:

```markdown
### Recommended Automation

Based on this triage session, consider setting up:

1. **Auto-priority for labeled issues**:
   - Issues with "critical" label → P0
   - Issues with "bug" label → P1
   - Issues with "enhancement" label → P2

2. **Auto-status from PR state**:
   - When PR opens → Move to "In Review"
   - When PR merges → Move to "Done"

3. **Auto-archive**:
   - Items in "Done" for >30 days → Archive

4. **Notifications**:
   - Alert on new P0 items
   - Daily digest of P1 items in Backlog

[Link to automation setup guide]
```

## Important Notes

- **Context Matters**: Item priority depends on project goals and current sprint
- **Team Alignment**: Ensure team agrees on priority definitions
- **Regular Cadence**: Weekly triage prevents backlog chaos
- **Don't Over-Triage**: It's okay to leave P3 items rough until needed
- **Save Time**: Use batch mode for obvious cases, interactive for complex items
- **Document Decisions**: Add comments to items explaining priority rationale

## Definition of Done

- [ ] Triage scope determined
- [ ] Items fetched and filtered
- [ ] Each item assessed for priority
- [ ] Each item assessed for status
- [ ] Field values updated successfully
- [ ] Changes verified
- [ ] Triage report generated
- [ ] Remaining items noted
- [ ] Next steps provided
- [ ] Automation suggestions offered

## Error Handling

- If item update fails: Log error, continue to next item, report at end
- If field options missing: Alert user, skip that field for affected items
- If user cancels mid-triage: Save progress, provide partial report
- If API rate limit: Pause, wait, resume from last item

Remember: Good triage is the foundation of effective project management. Taking time to properly prioritize and organize items saves hours of confusion and misprioritized work later.
