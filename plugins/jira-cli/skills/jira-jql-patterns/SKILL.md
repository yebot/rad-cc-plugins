# JQL Patterns Skill

Master JQL (Jira Query Language) query construction for advanced issue filtering and reporting.

## Overview

JQL is Jira's powerful query language for finding issues. This skill provides patterns and templates for constructing effective queries using jira-cli.

## Basic JQL Structure

```
field operator value [AND|OR field operator value]
```

## Essential Field Reference

### Issue Fields

| Field | Type | Example |
|-------|------|---------|
| `project` | Text | `project = PROJ` |
| `key` | Text | `key = PROJ-123` |
| `summary` | Text | `summary ~ "login"` |
| `description` | Text | `description ~ "error"` |
| `status` | Text | `status = "In Progress"` |
| `priority` | Text | `priority IN (High, Critical)` |
| `type` | Text | `type = Bug` |
| `labels` | List | `labels = urgent` |
| `component` | Text | `component = Backend` |
| `fixVersion` | Version | `fixVersion = "1.0"` |
| `resolution` | Text | `resolution = Fixed` |

### People Fields

| Field | Type | Example |
|-------|------|---------|
| `assignee` | User | `assignee = currentUser()` |
| `reporter` | User | `reporter = "user@example.com"` |
| `creator` | User | `creator = currentUser()` |
| `watcher` | User | `watcher = currentUser()` |

### Date Fields

| Field | Type | Example |
|-------|------|---------|
| `created` | Date | `created >= -7d` |
| `updated` | Date | `updated >= startOfWeek()` |
| `resolved` | Date | `resolved >= "2024-01-01"` |
| `duedate` | Date | `duedate <= now()` |

### Agile Fields

| Field | Type | Example |
|-------|------|---------|
| `sprint` | Sprint | `sprint = 123` |
| `"Epic Link"` | Epic | `"Epic Link" = PROJ-100` |
| `"Story Points"` | Number | `"Story Points" > 5` |

## Operators Reference

### Equality

- `=` - Equals
- `!=` - Not equals
- `IN` - In list
- `NOT IN` - Not in list

### Comparison

- `>` - Greater than
- `>=` - Greater than or equal
- `<` - Less than
- `<=` - Less than or equal

### Text Search

- `~` - Contains (case-insensitive)
- `!~` - Does not contain
- `IS` - For checking null/empty
- `IS NOT` - For checking not null/empty

### Special

- `IS EMPTY` - Field has no value
- `IS NOT EMPTY` - Field has value
- `WAS` - Historical value
- `CHANGED` - Field was changed

## JQL Functions

### User Functions

```jql
assignee = currentUser()
reporter = currentUser()
watcher = currentUser()
assignee IN membersOf("developers")
```

### Date Functions

```jql
created >= startOfDay()
created <= endOfDay()
created >= startOfWeek()
created >= startOfMonth()
created >= startOfYear()

updated >= startOfDay(-7)  # 7 days ago
duedate <= endOfWeek(1)     # End of next week
```

### Sprint Functions

```jql
sprint IN openSprints()
sprint IN closedSprints()
sprint IN futureSprints()
```

## Common Query Patterns

### My Work Queries

**Current work:**
```jql
assignee = currentUser() AND status NOT IN (Done, Closed)
```

**Recently completed:**
```jql
assignee = currentUser() AND status = Done AND resolved >= -7d
```

**Reported by me:**
```jql
reporter = currentUser() AND status NOT IN (Done, Closed)
```

**Watching:**
```jql
watcher = currentUser() AND status NOT IN (Done, Closed)
```

### Priority Queries

**Critical and high priority open:**
```jql
priority IN (Critical, High) AND status NOT IN (Done, Closed, Resolved)
```

**Urgent bugs:**
```jql
type = Bug AND priority = Critical AND status NOT IN (Done, Closed)
```

**Prioritized backlog:**
```jql
status = "To Do" AND priority IN (High, Medium) ORDER BY priority DESC
```

### Time-Based Queries

**Created today:**
```jql
created >= startOfDay()
```

**Updated this week:**
```jql
updated >= startOfWeek()
```

**Created in last 30 days:**
```jql
created >= -30d
```

**Overdue issues:**
```jql
duedate < now() AND status NOT IN (Done, Closed)
```

**Due this week:**
```jql
duedate >= startOfWeek() AND duedate <= endOfWeek()
```

**Stale issues (not updated in 90 days):**
```jql
updated <= -90d AND status NOT IN (Done, Closed)
```

### Team Queries

**Unassigned issues:**
```jql
assignee IS EMPTY AND status = "To Do"
```

**Team workload:**
```jql
assignee IN (user1@example.com, user2@example.com) AND status IN ("In Progress", "To Do")
```

**Blocked issues:**
```jql
status = Blocked OR labels = blocked
```

**Issues needing review:**
```jql
status = "In Review" AND assignee IS NOT EMPTY
```

### Sprint Queries

**Current sprint:**
```jql
sprint IN openSprints()
```

**Current sprint for project:**
```jql
project = PROJ AND sprint IN openSprints()
```

**Specific sprint:**
```jql
sprint = 123
```

**Issues without sprint:**
```jql
type IN (Story, Bug, Task) AND sprint IS EMPTY
```

**Incomplete sprint items:**
```jql
sprint = 123 AND status NOT IN (Done, Closed)
```

### Epic Queries

**All issues in epic:**
```jql
"Epic Link" = PROJ-100
```

**Completed epic issues:**
```jql
"Epic Link" = PROJ-100 AND status = Done
```

**Issues without epic:**
```jql
type = Story AND "Epic Link" IS EMPTY
```

### Bug Tracking Queries

**Open bugs:**
```jql
type = Bug AND status NOT IN (Done, Closed, "Won't Fix")
```

**Critical production bugs:**
```jql
type = Bug AND priority = Critical AND labels = production AND status NOT IN (Done, Closed)
```

**Bugs by component:**
```jql
type = Bug AND component = Backend AND status NOT IN (Done, Closed)
```

**Recently fixed bugs:**
```jql
type = Bug AND status = Done AND resolved >= -7d
```

**Regression bugs:**
```jql
type = Bug AND labels = regression AND status NOT IN (Done, Closed)
```

### Story Queries

**Ready for development:**
```jql
type = Story AND status = "To Do" AND "Story Points" IS NOT EMPTY
```

**Unestimated stories:**
```jql
type = Story AND "Story Points" IS EMPTY AND status = "To Do"
```

**Large stories (need breakdown):**
```jql
type = Story AND "Story Points" >= 13
```

### Component Queries

**Frontend issues:**
```jql
component = Frontend AND status NOT IN (Done, Closed)
```

**Backend bugs:**
```jql
component = Backend AND type = Bug AND status NOT IN (Done, Closed)
```

**Issues without component:**
```jql
component IS EMPTY AND type IN (Story, Bug, Task)
```

### Label Queries

**Technical debt:**
```jql
labels = tech-debt AND status NOT IN (Done, Closed)
```

**Multiple labels:**
```jql
labels IN (urgent, critical) AND status NOT IN (Done, Closed)
```

**Issues without labels:**
```jql
labels IS EMPTY AND type IN (Story, Bug)
```

## Advanced Patterns

### Complex Logic with Parentheses

```jql
project = PROJ AND
(priority = Critical OR labels = urgent) AND
status NOT IN (Done, Closed)
ORDER BY created DESC
```

### Historical Queries

**Issues that were in progress:**
```jql
status WAS "In Progress" DURING (-7d, now())
```

**Issues that changed priority:**
```jql
priority CHANGED DURING (-30d, now())
```

**Issues moved to done this week:**
```jql
status CHANGED TO Done DURING (startOfWeek(), now())
```

### Negative Queries

**Not assigned to specific team:**
```jql
assignee NOT IN membersOf("qa-team")
```

**Exclude certain statuses:**
```jql
status NOT IN (Done, Closed, "Won't Fix", Duplicate)
```

**Not labeled:**
```jql
labels IS EMPTY
```

### Multi-Project Queries

**Across projects:**
```jql
project IN (PROJ1, PROJ2, PROJ3) AND assignee = currentUser()
```

**All projects bugs:**
```jql
type = Bug AND priority = Critical AND status NOT IN (Done, Closed)
```

## Sorting Patterns

### Single Sort

```jql
ORDER BY priority DESC
ORDER BY created ASC
ORDER BY updated DESC
ORDER BY duedate ASC
```

### Multiple Sort

```jql
ORDER BY priority DESC, created ASC
ORDER BY status ASC, priority DESC, updated DESC
ORDER BY duedate ASC, priority DESC
```

## Using with jira-cli

### Basic Query

```bash
jira issue list --jql "assignee = currentUser() AND status = 'In Progress'"
```

### Multi-line for Readability

```bash
jira issue list --jql "\
  project = PROJ AND \
  status IN ('In Progress', 'In Review') AND \
  assignee = currentUser() AND \
  created >= -7d \
  ORDER BY priority DESC"
```

### With Output Formats

```bash
# Human readable
jira issue list --jql "..." --plain

# JSON for parsing
jira issue list --jql "..." --raw

# CSV for export
jira issue list --jql "..." --csv
```

## Report Patterns

### Sprint Velocity

```jql
sprint = 123 AND status = Done
```

Sum story points from results.

### Bug Trend

```jql
type = Bug AND created >= -30d
```

```jql
type = Bug AND resolved >= -30d
```

Compare created vs resolved.

### Team Performance

```jql
assignee IN membersOf("dev-team") AND
status = Done AND
resolved >= startOfWeek()
```

### Epic Progress

```jql
"Epic Link" = PROJ-100
```

```jql
"Epic Link" = PROJ-100 AND status = Done
```

Calculate percentage complete.

### Technical Debt Tracking

```jql
labels = tech-debt AND
status NOT IN (Done, Closed) AND
created <= -90d
ORDER BY priority DESC, created ASC
```

## Query Optimization Tips

### 1. Narrow by Project First

❌ Slow:
```jql
status = "In Progress"
```

✅ Fast:
```jql
project = PROJ AND status = "In Progress"
```

### 2. Use Specific Operators

❌ Slow:
```jql
summary ~ ".*login.*"
```

✅ Fast:
```jql
summary ~ "login"
```

### 3. Limit Results

```bash
jira issue list --jql "..." --limit 100
```

### 4. Use IS EMPTY Instead of Negation

❌ Slower:
```jql
assignee != null
```

✅ Faster:
```jql
assignee IS NOT EMPTY
```

## Common Mistakes

### Mistake 1: Missing Quotes

❌ Wrong:
```jql
status = In Progress
```

✅ Correct:
```jql
status = "In Progress"
```

### Mistake 2: Wrong Function

❌ Wrong:
```jql
assignee = me
```

✅ Correct:
```jql
assignee = currentUser()
```

### Mistake 3: Wrong Field Name

❌ Wrong:
```jql
epic = PROJ-100
```

✅ Correct:
```jql
"Epic Link" = PROJ-100
```

### Mistake 4: Wrong Date Format

❌ Wrong:
```jql
created > 7d
```

✅ Correct:
```jql
created >= -7d
```

## Debugging Queries

### Step 1: Simplify

Start with basic query:
```jql
project = PROJ
```

### Step 2: Add Conditions Incrementally

```jql
project = PROJ AND status = "In Progress"
```

```jql
project = PROJ AND status = "In Progress" AND assignee = currentUser()
```

### Step 3: Test Each Addition

Run query after each change to identify issues.

### Step 4: Check Field Names

Verify custom field names in Jira UI.

### Step 5: Use --debug

```bash
jira issue list --jql "..." --debug
```

## Saving Common Queries

### Shell Aliases

```bash
alias jira-my-work='jira issue list --jql "assignee = currentUser() AND status NOT IN (Done, Closed)" --plain'
alias jira-urgent='jira issue list --jql "priority IN (Critical, High) AND status NOT IN (Done, Closed)" --plain'
alias jira-sprint='jira issue list --jql "sprint IN openSprints()" --plain'
```

### Script Functions

```bash
# Add to ~/.bashrc or ~/.zshrc
jira-find() {
  local query="$1"
  jira issue list --jql "summary ~ \"$query\" OR description ~ \"$query\"" --plain
}

jira-my-bugs() {
  jira issue list --jql "assignee = currentUser() AND type = Bug AND status NOT IN (Done, Closed)" --plain
}

jira-overdue() {
  jira issue list --jql "duedate < now() AND status NOT IN (Done, Closed)" --plain
}
```

## When to Use This Skill

- User needs complex issue filtering
- Generating reports or metrics
- Finding issues across projects
- Historical queries
- Performance optimization needed
- Combining multiple criteria

## Next Steps

After mastering JQL:
1. Create saved queries for common needs
2. Integrate queries into automation scripts
3. Build dashboards based on queries
4. Share query templates with team
5. Document organization-specific patterns
