---
name: gh-project-view
description: View project details, items, and status with comprehensive reporting
tools: Bash, Read, Write
model: inherit
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
gh project list --owner "@me" --format json | python3 -c "
import json, sys
projects = json.load(sys.stdin)
for p in projects:
    print(f\"#{p.get('number')} - {p.get('title')}\")
"
```

For organization projects:
```bash
gh project list --owner "org-name" --format json | python3 -c "
import json, sys
projects = json.load(sys.stdin)
for p in projects:
    print(f\"#{p.get('number')} - {p.get('title')}\")
"
```

### Step 2: Get Project Details

Fetch comprehensive project information:

```bash
# Get project metadata
PROJECT_DATA=$(gh project view <number> --owner "<owner>" --format json)

# Parse key details using Python (safer than jq)
PROJECT_ID=$(echo "$PROJECT_DATA" | python3 -c "import json, sys; print(json.load(sys.stdin).get('id', ''))")
PROJECT_TITLE=$(echo "$PROJECT_DATA" | python3 -c "import json, sys; print(json.load(sys.stdin).get('title', ''))")
PROJECT_URL=$(echo "$PROJECT_DATA" | python3 -c "import json, sys; print(json.load(sys.stdin).get('url', ''))")
CREATED_AT=$(echo "$PROJECT_DATA" | python3 -c "import json, sys; print(json.load(sys.stdin).get('createdAt', ''))")
UPDATED_AT=$(echo "$PROJECT_DATA" | python3 -c "import json, sys; print(json.load(sys.stdin).get('updatedAt', ''))")
```

### Step 3: Get Project Fields

Fetch all custom fields:

```bash
FIELDS=$(gh project field-list <number> --owner "<owner>" --format json --limit 50)

# Parse field details using Python
echo "$FIELDS" | python3 -c "
import json, sys
fields = json.load(sys.stdin)
for field in fields:
    print(f\"- {field.get('name')} ({field.get('dataType')})\")
"
```

### Step 4: Get Project Items

Fetch all items with their field values:

```bash
ITEMS=$(gh project item-list <number> --owner "<owner>" --format json --limit 100)

# Count total items using Python
ITEM_COUNT=$(echo "$ITEMS" | python3 -c "import json, sys; data=json.load(sys.stdin); print(len(data.get('items', [])))")
```

### Step 5: Analyze Item Distribution

Generate comprehensive statistics:

#### Status Distribution
```bash
# Save items to temp file for helper processing
echo "$ITEMS" > /tmp/gh_items.json

# Use Python helper to count by field
python3 -c "
import json, sys
with open('/tmp/gh_items.json') as f:
    data = json.load(f)
    items = data.get('items', [])

    # Count by Status
    status_counts = {}
    for item in items:
        for fv in item.get('fieldValues', []):
            if fv.get('name') == 'Status':
                status = fv.get('name') or 'Unset'
                status_counts[status] = status_counts.get(status, 0) + 1
                break

    for status, count in sorted(status_counts.items()):
        print(f'  {status}: {count}')
"
```

#### Priority Distribution
```bash
python3 -c "
import json
with open('/tmp/gh_items.json') as f:
    data = json.load(f)
    items = data.get('items', [])

    # Count by Priority
    priority_counts = {}
    for item in items:
        for fv in item.get('fieldValues', []):
            if fv.get('name') == 'Priority':
                priority = fv.get('name') or 'Unset'
                priority_counts[priority] = priority_counts.get(priority, 0) + 1
                break

    for priority, count in sorted(priority_counts.items()):
        print(f'  {priority}: {count}')
"
```

#### Item Types
```bash
# Count issues vs PRs vs drafts using Python
ISSUE_COUNT=$(python3 -c "import json; data=json.load(open('/tmp/gh_items.json')); print(len([i for i in data.get('items', []) if i.get('content', {}).get('type') == 'Issue']))")
PR_COUNT=$(python3 -c "import json; data=json.load(open('/tmp/gh_items.json')); print(len([i for i in data.get('items', []) if i.get('content', {}).get('type') == 'PullRequest']))")
DRAFT_COUNT=$(python3 -c "import json; data=json.load(open('/tmp/gh_items.json')); print(len([i for i in data.get('items', []) if i.get('content', {}).get('type') == 'DraftIssue']))")
```

### Step 6: Identify Items Requiring Attention

#### High Priority Items Not Started
```bash
# P0/P1 items in Backlog or Todo using Python
python3 -c "
import json
with open('/tmp/gh_items.json') as f:
    data = json.load(f)
    items = data.get('items', [])

    for item in items:
        priority = None
        status = None

        for fv in item.get('fieldValues', []):
            if fv.get('name') == 'Priority':
                priority = fv.get('name')
            elif fv.get('name') == 'Status':
                status = fv.get('name')

        # Check if P0 or P1 and in Backlog or Todo
        if priority in ['P0', 'P1'] and status in ['Backlog', 'Todo']:
            content = item.get('content', {})
            number = content.get('number', 'draft')
            title = content.get('title', 'Untitled')
            print(f'  - #{number} {title}')
"
```

#### Stale Items (In Progress > 7 days)
```bash
THRESHOLD_DATE=$(date -v-7d +%Y-%m-%d 2>/dev/null || date -d '7 days ago' +%Y-%m-%d)

python3 -c "
import json
from datetime import datetime, timedelta

with open('/tmp/gh_items.json') as f:
    data = json.load(f)
    items = data.get('items', [])
    threshold = datetime.now() - timedelta(days=7)

    for item in items:
        status = None
        for fv in item.get('fieldValues', []):
            if fv.get('name') == 'Status':
                status = fv.get('name')
                break

        if status in ['In Progress', 'In Review']:
            content = item.get('content', {})
            updated_str = content.get('updatedAt', '')

            if updated_str:
                try:
                    updated_at = datetime.fromisoformat(updated_str.replace('Z', '+00:00'))
                    if updated_at < threshold:
                        number = content.get('number', 'draft')
                        title = content.get('title', 'Untitled')
                        updated_date = updated_str.split('T')[0]
                        days_old = (datetime.now() - updated_at).days
                        print(f'  - #{number} {title} (updated: {updated_date}, {days_old} days ago)')
                except:
                    pass
"
```

#### Items in Review
```bash
python3 -c "
import json
with open('/tmp/gh_items.json') as f:
    data = json.load(f)
    items = data.get('items', [])

    for item in items:
        status = None
        for fv in item.get('fieldValues', []):
            if fv.get('name') == 'Status':
                status = fv.get('name')
                break

        if status == 'In Review':
            content = item.get('content', {})
            number = content.get('number', 'draft')
            title = content.get('title', 'Untitled')
            print(f'  - #{number} {title}')
"
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
