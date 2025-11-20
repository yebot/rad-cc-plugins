---
name: gh-project-status
description: Generate comprehensive status report of project progress and metrics
tools: Bash, Read, Write
model: sonnet
---

# Generate Project Status Report

This command generates comprehensive status reports for GitHub Projects with metrics, insights, and actionable items.

## Instructions

### Step 1: Identify Project and Timeframe

Ask the user:
1. Which project to report on (name or number)
2. Timeframe for analysis (optional):
   - Current sprint/iteration
   - Last 7 days
   - Last 30 days
   - All time (default)

### Step 2: Gather Project Data

Collect comprehensive project information:

```bash
# Get project metadata
PROJECT_DATA=$(gh project view <number> --owner "@me" --format json)
PROJECT_TITLE=$(echo $PROJECT_DATA | jq -r '.title')
PROJECT_URL=$(echo $PROJECT_DATA | jq -r '.url')

# Get all fields
FIELDS=$(gh project field-list <number> --owner "@me" --format json --limit 50)

# Get all items
ITEMS=$(gh project item-list <number> --owner "@me" --format json --limit 100)
TOTAL_ITEMS=$(echo $ITEMS | jq '.items | length')
```

### Step 3: Calculate Core Metrics

#### Status Distribution
```bash
STATUS_METRICS=$(echo $ITEMS | jq -r '
  [.items[].fieldValues[] | select(.name=="Status")] |
  group_by(.name) |
  map({
    status: .[0].name,
    count: length,
    percentage: ((length / ('$TOTAL_ITEMS' | tonumber)) * 100 | floor)
  })
')
```

#### Priority Breakdown
```bash
PRIORITY_METRICS=$(echo $ITEMS | jq -r '
  [.items[].fieldValues[] | select(.name=="Priority")] |
  group_by(.name) |
  map({
    priority: .[0].name,
    count: length
  })
')
```

#### Item Types
```bash
ISSUE_COUNT=$(echo $ITEMS | jq '[.items[] | select(.content.type=="Issue")] | length')
PR_COUNT=$(echo $ITEMS | jq '[.items[] | select(.content.type=="PullRequest")] | length')
DRAFT_COUNT=$(echo $ITEMS | jq '[.items[] | select(.content.type=="DraftIssue")] | length')
```

### Step 4: Identify Critical Items

#### Blockers & High Priority
```bash
# P0 items (critical)
P0_ITEMS=$(echo $ITEMS | jq -r '
  .items[] |
  select(.fieldValues[] | select(.name=="Priority" and .name=="P0")) |
  {
    title: .content.title,
    number: .content.number,
    status: (.fieldValues[] | select(.name=="Status") | .name),
    url: .content.url
  }
')

P0_COUNT=$(echo $P0_ITEMS | jq -s 'length')

# P1 items not in progress
P1_TODO=$(echo $ITEMS | jq -r '
  .items[] |
  select(
    (.fieldValues[] | select(.name=="Priority" and .name=="P1")) and
    (.fieldValues[] | select(.name=="Status" and (.name=="Backlog" or .name=="Todo")))
  ) |
  {
    title: .content.title,
    number: .content.number,
    status: (.fieldValues[] | select(.name=="Status") | .name)
  }
')

P1_TODO_COUNT=$(echo $P1_TODO | jq -s 'length')
```

#### Stale Items
```bash
# Items in progress > 7 days without update
THRESHOLD_DATE=$(date -v-7d +%Y-%m-%d)

STALE_ITEMS=$(echo $ITEMS | jq -r --arg threshold "$THRESHOLD_DATE" '
  .items[] |
  select(
    (.fieldValues[] | select(.name=="Status" and (.name=="In Progress" or .name=="In Review"))) and
    (.content.updatedAt | split("T")[0] < $threshold)
  ) |
  {
    title: .content.title,
    number: .content.number,
    status: (.fieldValues[] | select(.name=="Status") | .name),
    lastUpdated: (.content.updatedAt | split("T")[0]),
    daysSinceUpdate: (now - (.content.updatedAt | fromdateiso8601)) / 86400 | floor
  }
')

STALE_COUNT=$(echo $STALE_ITEMS | jq -s 'length')
```

#### Items in Review
```bash
REVIEW_ITEMS=$(echo $ITEMS | jq -r '
  .items[] |
  select(.fieldValues[] | select(.name=="Status" and .name=="In Review")) |
  {
    title: .content.title,
    number: .content.number,
    type: .content.type,
    url: .content.url
  }
')

REVIEW_COUNT=$(echo $REVIEW_ITEMS | jq -s 'length')
```

### Step 5: Calculate Velocity (if applicable)

If project has Story Points or similar estimation:

```bash
# Completed items with story points
COMPLETED_POINTS=$(echo $ITEMS | jq '
  [.items[] |
   select(.fieldValues[] | select(.name=="Status" and .name=="Done")) |
   .fieldValues[] |
   select(.name=="Story Points") |
   .number
  ] | add // 0
')

# In progress points
IN_PROGRESS_POINTS=$(echo $ITEMS | jq '
  [.items[] |
   select(.fieldValues[] | select(.name=="Status" and .name=="In Progress")) |
   .fieldValues[] |
   select(.name=="Story Points") |
   .number
  ] | add // 0
')

# Total estimated points
TOTAL_POINTS=$(echo $ITEMS | jq '
  [.items[] |
   .fieldValues[] |
   select(.name=="Story Points") |
   .number
  ] | add // 0
')

# Completion percentage
if [ "$TOTAL_POINTS" -gt 0 ]; then
  COMPLETION_PCT=$(echo "scale=1; ($COMPLETED_POINTS / $TOTAL_POINTS) * 100" | bc)
else
  COMPLETION_PCT="N/A"
fi
```

### Step 6: Analyze Health Indicators

Calculate project health score based on:

```bash
# Work distribution (ideal: balanced across statuses)
# Priority coverage (good: all items have priority)
# Stale item ratio (good: < 10% stale)
# Review bottleneck (warning: > 5 items in review)
# P0/P1 attention (critical: all P0/P1 should be active)

UNPRIORITIZED=$(echo $ITEMS | jq '
  [.items[] |
   select(.fieldValues[] | select(.name=="Priority") | not)
  ] | length
')

UNPRIORITIZED_PCT=$(echo "scale=1; ($UNPRIORITIZED / $TOTAL_ITEMS) * 100" | bc)

# Health score (0-100)
HEALTH_SCORE=100
[ "$STALE_COUNT" -gt $(echo "$TOTAL_ITEMS * 0.1" | bc | cut -d. -f1) ] && HEALTH_SCORE=$((HEALTH_SCORE - 20))
[ "$REVIEW_COUNT" -gt 5 ] && HEALTH_SCORE=$((HEALTH_SCORE - 15))
[ "$P1_TODO_COUNT" -gt 3 ] && HEALTH_SCORE=$((HEALTH_SCORE - 15))
[ "$UNPRIORITIZED" -gt 0 ] && HEALTH_SCORE=$((HEALTH_SCORE - 10))
```

### Step 7: Generate Comprehensive Report

Present the analysis in a clear, executive-friendly format:

```markdown
# Project Status Report
## [Project Title]

**Generated**: [Current Date/Time]
**Project**: #[Number] | [URL]
**Timeframe**: [Specified timeframe or "All time"]

---

## Executive Summary

**Overall Health**: [Excellent/Good/Fair/Poor] ([Health Score]/100)

**Key Metrics**:
- Total Items: [count]
- Completion: [X]% ([Completed]/[Total] points) [if applicable]
- Active Work: [In Progress count] items
- Awaiting Review: [Review count] items
- Blocked/Critical: [P0 count] items

**Status**: [1-2 sentence summary of project state]

---

## 📊 Item Distribution

### By Status
| Status | Count | Percentage |
|--------|-------|------------|
[For each status: | Status | X | Y% |]
| **Total** | **[Total]** | **100%** |

### By Priority
| Priority | Count | In Progress | Done |
|----------|-------|-------------|------|
[For each priority: | PX | X | Y | Z |]

### By Type
- Issues: [count]
- Pull Requests: [count]
- Draft Items: [count]

---

## 🎯 Velocity & Progress

[If story points available:]
- **Sprint Goal**: [X] points
- **Completed**: [Y] points ([Z]%)
- **In Progress**: [A] points
- **Remaining**: [B] points

**Projected Completion**: [On track / At risk / Behind]

[Visual progress bar:]
```
Backlog     Todo     In Progress     Review     Done
   ▓          ▓           ▓            ▓         ████████
  [X]        [Y]         [Z]          [A]        [B]
```

---

## ⚠️ Items Requiring Attention

### 🚨 Critical (P0) - [count]
[If any P0 items exist, list them with status:]
- #[number] [title] - Status: [status]
[Otherwise: ✅ No critical items]

### ⏰ High Priority Not Started (P1) - [count]
[If any P1 in Backlog/Todo:]
- #[number] [title] - [status]
[Otherwise: ✅ All P1 items are in progress or done]

### 🐌 Stale Items (>7 days) - [count]
[If any stale items:]
- #[number] [title] - In Progress for [X] days
[Otherwise: ✅ No stale items]

### 👀 Awaiting Review - [count]
[If items in review:]
- #[number] [title] - [type] - [URL]
[Otherwise: ✅ No items in review]

### 🏷️ Missing Priority - [count]
[If unprioritized items exist:]
- [X]% of items lack priority assignment
- Action: Run `/gh-project-triage` to assign priorities
[Otherwise: ✅ All items prioritized]

---

## 📈 Trends & Insights

### Work Distribution
[Analysis of status distribution:]
- Healthy backlog: [Yes/No] ([X] items ready for work)
- Work in progress: [Appropriate/Too high/Too low] ([Y] items)
- Review bottleneck: [Yes/No] ([Z] items awaiting review)

### Priority Balance
- Critical items: [Appropriate/High] attention
- High priority: [Well-managed/Needs attention]
- Backlog refinement: [Current/Overdue]

### Completion Rate
[If velocity data available:]
- Current sprint: [X]% complete
- Average velocity: [Y] points/sprint
- Projected completion: [Date or "On track"]

---

## 🎬 Recommended Actions

1. **Immediate** (Do today):
   [List urgent actions based on analysis, e.g.:]
   - Review and prioritize [X] P0 items
   - Unblock [Y] stale items in progress
   - Review [Z] PRs awaiting review

2. **Short-term** (This week):
   [List important actions:]
   - Triage [X] unprioritized items
   - Start work on [Y] P1 items in backlog
   - Archive [Z] completed items from last sprint

3. **Ongoing**:
   - Maintain < 5 items in review
   - Keep P0/P1 items actively progressing
   - Regular backlog refinement (weekly)

---

## 📅 Next Review

**Recommended**: [Date - 1 week from now]

**Focus areas for next review**:
- P0 item resolution
- Velocity trend
- Stale item reduction

---

## Quick Actions

- View project: [URL]
- Triage backlog: `/gh-project-triage`
- Add items: `/gh-item-add`
- Update items: Use project-manager agent

---

*Report generated by GitHub Project Manager plugin*
```

### Step 8: Offer Drill-Down Options

After presenting the report, ask if the user wants:
- Detailed list of items in specific status
- Individual item analysis
- Trend comparison (if historical data available)
- Export report to file
- Share report (formatted for team distribution)

## Advanced Analysis

### Cycle Time Analysis
If timestamp data available, calculate:
- Average time from Todo → Done
- Average time in each status
- Bottleneck identification

### Burndown Chart (text-based)
For sprint projects with story points:
```
Sprint Burndown (Story Points)

40 |•
35 | •
30 |  ••
25 |    ••
20 |      •••
15 |         ••
10 |           ••
 5 |             •
 0 |______________•____
   D1 D3 D5 D7 D9 D11 D13

Ideal: --- | Actual: •••
```

### Team Contribution
If assignee data available:
```
Items by Team Member:
- Alice: 8 (5 done, 2 in progress, 1 in review)
- Bob: 6 (4 done, 2 in progress)
- Charlie: 5 (3 done, 2 in review)
- Unassigned: 12
```

## Export Options

### Markdown File
```bash
# Save report to file
cat > "project-status-$(date +%Y-%m-%d).md" <<EOF
[Report content]
EOF
```

### CSV Export
```bash
# Export items to CSV
echo $ITEMS | jq -r '
  ["Title", "Number", "Status", "Priority", "Type", "URL"],
  (.items[] | [
    .content.title,
    .content.number // "draft",
    (.fieldValues[] | select(.name=="Status") | .name),
    (.fieldValues[] | select(.name=="Priority") | .name // "Unset"),
    .content.type,
    .content.url // ""
  ]) | @csv
' > project-items.csv
```

## Important Notes

- **Refresh Data**: Fetch latest data at report time
- **Caching**: For large projects, consider caching field IDs
- **Pagination**: Handle projects with >100 items
- **Privacy**: Don't expose sensitive item details in team reports
- **Frequency**: Weekly status reports are typical
- **Stakeholder Version**: Create executive summary for non-technical stakeholders

## Definition of Done

- [ ] Project identified and data fetched
- [ ] Core metrics calculated (status, priority, types)
- [ ] Critical items identified (P0, stale, blocked)
- [ ] Velocity calculated (if applicable)
- [ ] Health score determined
- [ ] Comprehensive report generated
- [ ] Actionable recommendations provided
- [ ] Drill-down options offered
- [ ] Export option offered if requested

## Error Handling

- If no items: Report empty project, suggest adding items
- If missing fields: Handle gracefully, note in report
- If API limits hit: Show partial results, suggest retry
- If calculations fail: Use fallback values, note in report

Remember: A great status report tells a story - where we are, how we got here, and what we should do next. Make it scannable, actionable, and insightful.
