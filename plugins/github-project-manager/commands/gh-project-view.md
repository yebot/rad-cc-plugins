---
name: gh-project-view
description: View project details, items, and status with comprehensive reporting
tools: Bash, Read, Write
model: sonnet
---

# View GitHub Project

This command provides comprehensive views of GitHub Projects with detailed reporting and analysis.

## Instructions

### Step 1: Identify the Project

Ask the user which project they want to view. Options:
1. **By Name**: "Sprint 5", "Q1 Roadmap", etc.
2. **By Number**: Project #3
3. **Interactive**: List all projects and let user choose

If listing projects:
```bash
gh project list --owner "@me" --format json | jq -r '.[] | "#\(.number) - \(.title)"'
```

For organization projects:
```bash
gh project list --owner "org-name" --format json | jq -r '.[] | "#\(.number) - \(.title)"'
```

### Step 2: Get Project Details

Fetch comprehensive project information:

```bash
# Get project metadata
PROJECT_DATA=$(gh project view <number> --owner "<owner>" --format json)

# Parse key details
PROJECT_ID=$(echo $PROJECT_DATA | jq -r '.id')
PROJECT_TITLE=$(echo $PROJECT_DATA | jq -r '.title')
PROJECT_URL=$(echo $PROJECT_DATA | jq -r '.url')
CREATED_AT=$(echo $PROJECT_DATA | jq -r '.createdAt')
UPDATED_AT=$(echo $PROJECT_DATA | jq -r '.updatedAt')
```

### Step 3: Get Project Fields

Fetch all custom fields:

```bash
FIELDS=$(gh project field-list <number> --owner "<owner>" --format json --limit 50)

# Parse field details
echo $FIELDS | jq -r '.[] | "- \(.name) (\(.dataType))"'
```

### Step 4: Get Project Items

Fetch all items with their field values:

```bash
ITEMS=$(gh project item-list <number> --owner "<owner>" --format json --limit 100)

# Count total items
ITEM_COUNT=$(echo $ITEMS | jq '.items | length')
```

### Step 5: Analyze Item Distribution

Generate comprehensive statistics:

#### Status Distribution
```bash
# Group by Status field
STATUS_DIST=$(echo $ITEMS | jq '[
  .items[] |
  .fieldValues[] |
  select(.name=="Status")
] | group_by(.name) | map({
  status: .[0].name,
  count: length
})')

echo $STATUS_DIST | jq -r '.[] | "  \(.status): \(.count)"'
```

#### Priority Distribution
```bash
PRIORITY_DIST=$(echo $ITEMS | jq '[
  .items[] |
  .fieldValues[] |
  select(.name=="Priority")
] | group_by(.name) | map({
  priority: .[0].name,
  count: length
})')

echo $PRIORITY_DIST | jq -r '.[] | "  \(.priority): \(.count)"'
```

#### Item Types
```bash
# Count issues vs PRs vs drafts
ISSUE_COUNT=$(echo $ITEMS | jq '[.items[] | select(.content.type=="Issue")] | length')
PR_COUNT=$(echo $ITEMS | jq '[.items[] | select(.content.type=="PullRequest")] | length')
DRAFT_COUNT=$(echo $ITEMS | jq '[.items[] | select(.content.type=="DraftIssue")] | length')
```

### Step 6: Identify Items Requiring Attention

#### High Priority Items Not Started
```bash
# P0/P1 items in Backlog or Todo
URGENT_BACKLOG=$(echo $ITEMS | jq -r '
  .items[] |
  select(
    (.fieldValues[] | select(.name=="Priority" and (.name=="P0" or .name=="P1"))) and
    (.fieldValues[] | select(.name=="Status" and (.name=="Backlog" or .name=="Todo")))
  ) |
  "  - #\(.content.number // "draft") \(.content.title)"
')
```

#### Stale Items (In Progress > 7 days)
```bash
SEVEN_DAYS_AGO=$(date -v-7d +%Y-%m-%d)

STALE_ITEMS=$(echo $ITEMS | jq -r --arg threshold "$SEVEN_DAYS_AGO" '
  .items[] |
  select(
    (.fieldValues[] | select(.name=="Status" and .name=="In Progress")) and
    (.content.updatedAt | split("T")[0] < $threshold)
  ) |
  "  - #\(.content.number // "draft") \(.content.title) (updated: \(.content.updatedAt | split("T")[0]))"
')
```

#### Items in Review
```bash
REVIEW_ITEMS=$(echo $ITEMS | jq -r '
  .items[] |
  select(.fieldValues[] | select(.name=="Status" and .name=="In Review")) |
  "  - #\(.content.number // "draft") \(.content.title)"
')
```

### Step 7: Generate Comprehensive Report

Present results in a clear, scannable format:

```markdown
# Project Report: [Project Title]

**Project #[Number]** | [Owner] | [URL]
Created: [Date] | Last Updated: [Date]

---

## Summary Statistics

- **Total Items**: [count]
- **Issues**: [count]
- **Pull Requests**: [count]
- **Draft Items**: [count]

---

## Item Distribution

### By Status
[Status distribution with counts]

### By Priority
[Priority distribution with counts]

---

## Items by Status

### Backlog ([count])
[List of backlog items with priority indicators]

### In Progress ([count])
[List of in-progress items with assignees if available]

### In Review ([count])
[List of items in review]

### Done ([count])
[Recently completed items]

---

## Items Requiring Attention

### 🚨 High Priority Not Started
[P0/P1 items in Backlog/Todo]

### ⚠️ Stale Items (In Progress > 7 days)
[List with last update dates]

### 👀 Awaiting Review
[Items in Review status]

### 🔍 Missing Priority
[Items without priority assignment]

---

## Field Summary

### Custom Fields
[List all custom fields with their types]

---

## Quick Actions

- Add items: `/gh-item-add`
- Update status: Use project-manager agent
- Triage backlog: `/gh-project-triage`
- Generate status report: `/gh-project-status`

---

## Project Health

[Overall assessment of project health based on metrics]
- Item distribution balance
- Priority coverage
- Stale item count
- Workflow bottlenecks
```

### Step 8: Offer Drill-Down Options

Ask the user if they want to see:
- Specific items by status or priority
- Details of particular items
- Field values for all items
- Items assigned to specific person
- Items in specific iteration/sprint

## View Modes

Support different view modes based on user needs:

### Quick View
- Project title and number
- Total item count
- Status distribution only

### Standard View (default)
- All summary statistics
- Status and priority distributions
- Items requiring attention

### Detailed View
- Everything from standard view
- Individual item listings by status
- Field analysis
- Health metrics
- Recommendations

### Custom View
Ask user what specific information they need:
- Filter by field values
- Show only certain item types
- Focus on specific time ranges
- Compare iterations/sprints

## Important Notes

- Use `--format json` for all gh commands to enable parsing
- Handle missing fields gracefully (not all projects have same fields)
- Limit item fetching to 100 by default, offer pagination for larger projects
- Format dates consistently (YYYY-MM-DD)
- Use emoji sparingly for visual hierarchy
- Make URLs clickable where possible

## Definition of Done

- [ ] Project identified (by name or number)
- [ ] Project metadata retrieved
- [ ] Fields listed and parsed
- [ ] Items fetched and analyzed
- [ ] Status distribution calculated
- [ ] Priority distribution calculated
- [ ] Items requiring attention identified
- [ ] Comprehensive report generated
- [ ] Drill-down options offered
- [ ] Report is clear, scannable, and actionable

## Error Handling

- If project not found: List available projects, ask user to choose
- If no items: Report empty project, offer to add items
- If fields missing: Handle gracefully, report field setup status
- If API rate limit hit: Advise user to wait, show partial results
- If authentication fails: Check `gh auth status`, guide to refresh

## Output Format Options

Ask user preference:
1. **Markdown** (default): Rich formatted text for terminal/web
2. **JSON**: Machine-readable for scripting
3. **CSV**: Export to spreadsheet
4. **Summary**: One-line overview for quick checks

Remember: A good project view provides both overview and insight, enabling users to understand status at a glance and identify action items immediately.
