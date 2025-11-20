---
name: gh-item-add
description: Add issues, PRs, or draft items to projects with field assignment
tools: Bash, AskUserQuestion, TodoWrite
model: inherit
---

# Add Item to GitHub Project

This command guides you through adding items to GitHub Projects with proper field configuration.

## Instructions

### Step 1: Identify Target Project

Ask the user which project to add items to:

```bash
# List available projects using Python for safe JSON parsing
gh project list --owner "@me" --format json | python3 -c "
import json, sys
projects = json.load(sys.stdin)
for p in projects:
    print(f\"#{p.get('number')} - {p.get('title')}\")
"

# For organization
gh project list --owner "org-name" --format json | python3 -c "
import json, sys
projects = json.load(sys.stdin)
for p in projects:
    print(f\"#{p.get('number')} - {p.get('title')}\")
"
```

Get the project ID:
```bash
PROJECT_ID=$(gh project list --owner "@me" --format json | python3 -c "
import json, sys
projects = json.load(sys.stdin)
target_number = <number>  # Replace with actual number
for p in projects:
    if p.get('number') == target_number:
        print(p.get('id', ''))
        break
")
```

### Step 2: Determine Item Type

Ask the user what type of item to add:

1. **Existing Issue**: Add issue from this or another repository
2. **Existing PR**: Add pull request from this or another repository
3. **Draft Item**: Create new draft item (no issue created)

### Step 3A: Add Existing Issue or PR

If adding existing issue/PR:

1. **Get the URL or number**:
   - Ask user for issue/PR number or full URL
   - If just number provided, construct URL: `https://github.com/<owner>/<repo>/issues/<number>`

2. **Add to project**:
   ```bash
   gh project item-add <project-number> --owner "<owner>" --url <issue-or-pr-url>
   ```

3. **Capture item ID** from output or query:
   ```bash
   ITEM_ID=$(gh project item-list <project-number> --owner "@me" --format json --limit 100 | python3 -c "
import json, sys
data = json.load(sys.stdin)
target_url = '<url>'  # Replace with actual URL
for item in data.get('items', []):
    if item.get('content', {}).get('url') == target_url:
        print(item.get('id', ''))
        break
")
   ```

### Step 3B: Create Draft Item

If creating draft item:

1. **Get title and body**:
   - Ask user for item title (required)
   - Ask user for item description/body (optional)

2. **Create draft**:
   ```bash
   DRAFT_RESPONSE=$(gh project item-create <project-number> --owner "@me" \
     --title "<title>" \
     --body "<body>" \
     --format json)

   ITEM_ID=$(echo "$DRAFT_RESPONSE" | python3 -c "import json, sys; print(json.load(sys.stdin).get('id', ''))")
   ```

3. **Note**: Draft items can be converted to issues later when ready

### Step 4: Get Project Fields

Fetch available fields for the project:

```bash
FIELDS=$(gh project field-list <project-number> --owner "@me" --format json)

# Show fields to user using Python
echo "$FIELDS" | python3 -c "
import json, sys
fields = json.load(sys.stdin)
for field in fields:
    print(f\"- {field.get('name')} ({field.get('dataType')})\")
"
```

### Step 5: Set Initial Field Values

Ask user which fields to set initially (optional but recommended):

#### Set Status
```bash
# Get Status field ID and options using Python
echo "$FIELDS" > /tmp/gh_fields.json

STATUS_FIELD=$(python3 -c "
import json
with open('/tmp/gh_fields.json') as f:
    fields = json.load(f)
    for field in fields:
        if field.get('name') == 'Status':
            print(field.get('id', ''))
            break
")

# Show options to user
python3 -c "
import json
with open('/tmp/gh_fields.json') as f:
    fields = json.load(f)
    for field in fields:
        if field.get('name') == 'Status':
            for option in field.get('options', []):
                print(f\"{option.get('name')}: {option.get('id')}\")
            break
"

# Then update (after user selects option):
gh project item-edit --id $ITEM_ID --project-id $PROJECT_ID \
  --field-id $STATUS_FIELD --single-select-option-id <option-id>
```

#### Set Priority
```bash
PRIORITY_FIELD=$(python3 -c "
import json
with open('/tmp/gh_fields.json') as f:
    fields = json.load(f)
    for field in fields:
        if field.get('name') == 'Priority':
            print(field.get('id', ''))
            break
")

# Show options
python3 -c "
import json
with open('/tmp/gh_fields.json') as f:
    fields = json.load(f)
    for field in fields:
        if field.get('name') == 'Priority':
            for option in field.get('options', []):
                print(f\"{option.get('name')}: {option.get('id')}\")
            break
"

# Update after selection
gh project item-edit --id $ITEM_ID --project-id $PROJECT_ID \
  --field-id $PRIORITY_FIELD --single-select-option-id <option-id>
```

#### Set Other Fields (as applicable)

**Number field** (e.g., Story Points):
```bash
gh project item-edit --id $ITEM_ID --project-id $PROJECT_ID \
  --field-id <field-id> --number <value>
```

**Date field** (e.g., Due Date):
```bash
gh project item-edit --id $ITEM_ID --project-id $PROJECT_ID \
  --field-id <field-id> --date "YYYY-MM-DD"
```

**Text field** (e.g., Owner):
```bash
gh project item-edit --id $ITEM_ID --project-id $PROJECT_ID \
  --field-id <field-id> --text "<value>"
```

**Iteration field** (e.g., Sprint):
```bash
# Get iteration ID (complex, may need GraphQL)
gh project item-edit --id $ITEM_ID --project-id $PROJECT_ID \
  --field-id <field-id> --iteration-id <iteration-id>
```

### Step 6: Verify Addition

Confirm the item was added successfully:

```bash
# View the item in the project using Python
gh project item-list <project-number> --owner "@me" --format json --limit 100 | python3 -c "
import json, sys
data = json.load(sys.stdin)
target_id = '$ITEM_ID'

for item in data.get('items', []):
    if item.get('id') == target_id:
        content = item.get('content', {})
        result = {
            'title': content.get('title'),
            'type': content.get('type'),
            'url': content.get('url'),
            'fieldValues': item.get('fieldValues', [])
        }
        print(json.dumps(result, indent=2))
        break
"
```

### Step 7: Provide Summary

Generate a clear summary for the user:

```markdown
## Item Added Successfully!

### Item Details
- **Title**: [Item Title]
- **Type**: [Issue/PR/Draft]
- **URL**: [URL if applicable]
- **Added to**: [Project Name] (#[Project Number])

### Initial Field Values
- Status: [Value]
- Priority: [Value]
- [Other fields set...]

### Next Steps

1. **View in Project**: [Project URL]
2. **Update Additional Fields**: Use project UI or:
   - Set iteration/sprint
   - Add estimation (story points)
   - Assign team member
3. **Start Work**: Move to "In Progress" when ready
4. **Link to PR**: When you create a PR for this issue

### Quick Commands
- View project: `/gh-project-view`
- Update fields: Use project-manager agent
- View item details: `gh issue view <number>` or `gh pr view <number>`
```

## Batch Adding Items

If user wants to add multiple items:

1. **Get list of items to add**:
   - From issue search: `gh issue list --repo owner/repo --label feature --limit 20`
   - From PR list: `gh pr list --repo owner/repo --limit 20`
   - From user input: Array of issue numbers

2. **Loop through items**:
   ```bash
   for ISSUE_NUM in $ISSUES; do
     ISSUE_URL="https://github.com/<owner>/<repo>/issues/$ISSUE_NUM"
     gh project item-add <project-number> --owner "@me" --url $ISSUE_URL
     echo "Added issue #$ISSUE_NUM"
   done
   ```

3. **Set common fields** (if requested):
   - Get all newly added item IDs
   - Apply same field values to all
   - Report batch results

## Smart Field Assignment

Suggest field values based on context:

### Auto-Priority from Issue Labels
```bash
# If issue has 'critical' or 'blocking' label → P0
# If issue has 'bug' or 'urgent' label → P1
# If issue has 'enhancement' label → P2
# Default → P3

LABELS=$(gh issue view <number> --json labels --jq '.labels[].name')
if echo $LABELS | grep -q "critical\|blocking"; then
  SUGGESTED_PRIORITY="P0"
elif echo $LABELS | grep -q "bug\|urgent"; then
  SUGGESTED_PRIORITY="P1"
else
  SUGGESTED_PRIORITY="P2"
fi
```

### Auto-Status from Issue State
```bash
# If issue is OPEN → Backlog or Todo
# If PR is OPEN → In Review
# If closed → Done or Archived

ISSUE_STATE=$(gh issue view <number> --json state --jq '.state')
if [ "$ISSUE_STATE" = "OPEN" ]; then
  SUGGESTED_STATUS="Backlog"
else
  SUGGESTED_STATUS="Done"
fi
```

## Important Notes

- **Item IDs vs Issue Numbers**: Item IDs are project-specific identifiers, different from issue numbers
- **Field IDs**: Must fetch field IDs for each project, they're not universal
- **Option IDs**: Single-select fields require option IDs, not option names
- **Permissions**: Ensure 'project' scope is enabled: `gh auth status`
- **Rate Limits**: When batch adding, respect API rate limits (pause if needed)

## Definition of Done

- [ ] Target project identified
- [ ] Item type determined (issue/PR/draft)
- [ ] Item added to project successfully
- [ ] Item ID captured
- [ ] Initial field values set (at minimum: Status, Priority)
- [ ] Addition verified
- [ ] Comprehensive summary provided
- [ ] Next steps documented

## Error Handling

- If project not found: List available projects, let user choose
- If issue/PR not found: Verify URL/number, check repository access
- If item already in project: Report duplicate, ask if should update fields
- If field update fails: Verify field ID and option ID are correct
- If permission denied: Check project access and gh auth scopes

## Special Cases

### Converting Draft to Issue

When user is ready to convert draft to real issue:

```bash
# This requires GraphQL API call (gh CLI doesn't have direct command)
# Provide instructions for manual conversion via GitHub UI
# Or use gh api graphql with mutation
```

### Linking PR to Issue Item

When adding a PR that closes an issue already in the project:
- Note the relationship
- Suggest linking them in descriptions
- Consider setting up automation for status sync

### Cross-Repository Items

When adding items from different repositories:
- Verify project is linked to target repository: `gh project link`
- If not linked, link it first
- Then add items

Remember: Proper field assignment at addition time saves triage work later. Take the extra minute to set Status and Priority correctly from the start.
