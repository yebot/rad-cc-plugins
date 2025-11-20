# Python Migration Guide for GitHub Project Manager

## Overview

This plugin has been migrated from using `jq` for JSON processing to using Python. This change eliminates shell escaping issues, improves reliability, and provides better error handling.

## What Changed

### Before (with jq)
```bash
# Had escaping issues with complex expressions
gh project list --owner "@me" --format json | jq -r '.[] | "#\(.number) - \(.title)"'

# Complex filters were error-prone
URGENT=$(echo $ITEMS | jq -r '
  .items[] |
  select(
    (.fieldValues[] | select(.name=="Priority" and (.name=="P0" or .name=="P1"))) and
    (.fieldValues[] | select(.name=="Status" and (.name=="Backlog" or .name=="Todo")))
  ) |
  "  - #\(.content.number // "draft") \(.content.title)"
')
```

### After (with Python)
```bash
# Clean, readable, no escaping issues
gh project list --owner "@me" --format json | python3 -c "
import json, sys
projects = json.load(sys.stdin)
for p in projects:
    print(f\"#{p.get('number')} - {p.get('title')}\")
"

# Complex logic is straightforward
python3 -c "
import json
with open('/tmp/gh_items.json') as f:
    data = json.load(f)
    for item in data.get('items', []):
        priority = None
        status = None
        for fv in item.get('fieldValues', []):
            if fv.get('name') == 'Priority':
                priority = fv.get('name')
            elif fv.get('name') == 'Status':
                status = fv.get('name')

        if priority in ['P0', 'P1'] and status in ['Backlog', 'Todo']:
            content = item.get('content', {})
            number = content.get('number', 'draft')
            title = content.get('title', 'Untitled')
            print(f'  - #{number} {title}')
"
```

## Helper Modules

### Core Python Helper: `gh_project_helpers.py`

Location: `helpers/gh_project_helpers.py`

Provides:
- `GHProjectHelpers` class with methods for common operations
- Filtering items by field values
- Extracting field information
- Grouping and counting
- Finding stale items
- Priority suggestions based on keywords
- CLI interface for standalone usage

#### Usage Examples

**As a module:**
```python
from gh_project_helpers import GHProjectHelpers

helpers = GHProjectHelpers()

# Filter items
filtered = helpers.filter_items(items, {'Status': 'In Progress', 'Priority': 'P1'})

# Extract field info
field_info = helpers.extract_field_info(fields, 'Priority')
option_id = helpers.get_option_id(field_info, 'P1')

# Find stale items
stale = helpers.find_stale_items(items, days=7, status_filter=['In Progress'])

# Suggest priority
priority, reason = helpers.suggest_priority(
    title="Critical bug in production",
    body="Users cannot login",
    labels=["bug", "urgent"]
)
```

**As a CLI tool:**
```bash
# Filter items
python3 helpers/gh_project_helpers.py filter-items items.json --field Status "In Progress"

# Extract field information
python3 helpers/gh_project_helpers.py extract-field fields.json --name "Priority"

# Count by field
python3 helpers/gh_project_helpers.py count-by-field items.json --field Status

# Find stale items
python3 helpers/gh_project_helpers.py find-stale items.json --days 7 --status "In Progress"

# Extract owner from repo string
python3 helpers/gh_project_helpers.py extract-owner "owner/repo"

# Suggest priority
python3 helpers/gh_project_helpers.py suggest-priority \
  --title "Critical bug" \
  --body "Production down" \
  --labels bug critical
```

### Bash Helper Functions: `gh_status_helpers.sh`

Location: `helpers/gh_status_helpers.sh`

Source this file to get convenient bash functions:

```bash
source helpers/gh_status_helpers.sh

# Save items for processing
save_items_json "$ITEMS"

# Count by field
count_by_field "Status"
count_by_field "Priority"

# Filter by status
filter_by_status "In Progress"

# Get high priority items not started
get_urgent_backlog

# Get stale items (default 7 days)
get_stale_items
get_stale_items 14  # 14 days

# Calculate completion (story points)
calculate_completion

# Get items missing a field
get_items_missing_field "Priority"

# Count by type
count_by_type

# Extract field info
extract_field_info "$FIELDS" "Priority"
```

## Migration Patterns

### Pattern 1: Simple Field Extraction

**Before:**
```bash
PROJECT_ID=$(echo $PROJECT_DATA | jq -r '.id')
```

**After:**
```bash
PROJECT_ID=$(echo "$PROJECT_DATA" | python3 -c "import json, sys; print(json.load(sys.stdin).get('id', ''))")
```

### Pattern 2: Filtering Arrays

**Before:**
```bash
ISSUE_COUNT=$(echo $ITEMS | jq '[.items[] | select(.content.type=="Issue")] | length')
```

**After:**
```bash
ISSUE_COUNT=$(echo "$ITEMS" | python3 -c "
import json, sys
data = json.load(sys.stdin)
count = len([i for i in data.get('items', []) if i.get('content', {}).get('type') == 'Issue'])
print(count)
")
```

### Pattern 3: Complex Filtering with Multiple Conditions

**Before:**
```bash
FILTERED=$(echo $ITEMS | jq -r '
  .items[] |
  select(
    (.fieldValues[] | select(.name=="Priority" and .name=="P0")) and
    (.fieldValues[] | select(.name=="Status" and .name=="Backlog"))
  ) |
  .id
')
```

**After:**
```bash
# Save to temp file for cleaner processing
echo "$ITEMS" > /tmp/items.json

FILTERED=$(python3 -c "
import json
with open('/tmp/items.json') as f:
    data = json.load(f)

    for item in data.get('items', []):
        priority = None
        status = None

        for fv in item.get('fieldValues', []):
            if fv.get('name') == 'Priority':
                priority = fv.get('name')
            elif fv.get('name') == 'Status':
                status = fv.get('name')

        if priority == 'P0' and status == 'Backlog':
            print(item.get('id'))
")
```

### Pattern 4: Grouping and Counting

**Before:**
```bash
STATUS_DIST=$(echo $ITEMS | jq '[
  .items[] |
  .fieldValues[] |
  select(.name=="Status")
] | group_by(.name) | map({
  status: .[0].name,
  count: length
})')
```

**After:**
```bash
echo "$ITEMS" > /tmp/items.json

python3 -c "
import json
with open('/tmp/items.json') as f:
    data = json.load(f)
    items = data.get('items', [])

    status_counts = {}
    for item in items:
        for fv in item.get('fieldValues', []):
            if fv.get('name') == 'Status':
                status = fv.get('name') or 'Unset'
                status_counts[status] = status_counts.get(status, 0) + 1
                break

    for status, count in sorted(status_counts.items()):
        print(f'{status}: {count}')
"
```

## Benefits of Python Approach

1. **No Shell Escaping Issues**: Python strings are straightforward, no need to escape `!`, `\`, quotes, etc.

2. **Better Error Handling**: Python exceptions provide clear error messages

3. **More Readable**: Multi-line Python code is easier to understand than complex jq filters

4. **Debugging**: Can easily add print statements and inspect variables

5. **Reusable**: Helper functions can be shared across commands

6. **Portable**: Python3 is available on all modern systems

7. **Testable**: Can unit test Python functions independently

## Common Pitfalls and Solutions

### Pitfall 1: Forgetting to Quote Variables

**Wrong:**
```bash
echo $JSON | python3 -c "..."  # May break on spaces
```

**Right:**
```bash
echo "$JSON" | python3 -c "..."  # Always quote
```

### Pitfall 2: Shell Variable in Python String

**Wrong:**
```bash
python3 -c "
import json
target = $ITEM_ID  # Shell variable not expanded in Python
"
```

**Right:**
```bash
python3 -c "
import json
target = '$ITEM_ID'  # Use single quotes or escape
"
```

### Pitfall 3: Not Handling Missing Keys

**Wrong:**
```python
print(item['content']['number'])  # KeyError if missing
```

**Right:**
```python
print(item.get('content', {}).get('number', 'draft'))  # Safe default
```

### Pitfall 4: Date Parsing Inconsistencies

**Wrong:**
```python
updated_at = datetime.fromisoformat(updated_str)  # May fail on Z suffix
```

**Right:**
```python
updated_at = datetime.fromisoformat(updated_str.replace('Z', '+00:00'))
```

## Testing Python Snippets

To test Python snippets before adding to commands:

```bash
# Create test data
gh project item-list 123 --owner "@me" --format json > /tmp/test_items.json

# Test your Python code
python3 -c "
import json
with open('/tmp/test_items.json') as f:
    data = json.load(f)
    # Your code here
    print(len(data.get('items', [])))
"

# Or use the helper module directly
python3 helpers/gh_project_helpers.py count-by-field /tmp/test_items.json --field Status
```

## Performance Considerations

1. **Use temp files for large datasets**: Parsing JSON multiple times is slower than reading from a file

2. **Single Python call for multiple operations**: Instead of multiple `python3 -c` calls, do more work in one call

3. **Use helper module for complex operations**: The module is optimized and reusable

## Future Improvements

Potential enhancements:

1. **Async operations**: Use `asyncio` for parallel gh CLI calls
2. **Caching**: Cache field IDs and project metadata
3. **GraphQL**: Direct GraphQL queries for complex operations
4. **Type hints**: Add full type annotations to helper module
5. **Unit tests**: Add pytest suite for helper functions

## Migration Checklist

When migrating a command from jq to Python:

- [ ] Replace all `jq -r` calls with Python equivalents
- [ ] Quote all shell variables properly
- [ ] Use `.get()` instead of direct key access
- [ ] Handle missing/null values gracefully
- [ ] Test with empty project (no items)
- [ ] Test with project containing draft items
- [ ] Test with items missing fields
- [ ] Verify error messages are clear
- [ ] Update command documentation

## Getting Help

If you encounter issues:

1. Check this guide for common patterns
2. Test Python snippets in isolation
3. Use the helper module's CLI interface for debugging
4. Check temp files (`/tmp/gh_*.json`) if processing fails
5. Add print statements to inspect data structure

## Examples from Real Commands

### gh-project-create: Owner Extraction

```bash
# Extract owner from repository string
REPO_OWNER=$(echo "$REPOSITORY" | python3 -c "
import sys
repo = sys.stdin.read().strip()
if '/' in repo:
    if 'github.com/' in repo:
        repo = repo.split('github.com/')[-1]
    owner = repo.split('/')[0]
    print(owner)
else:
    print(repo)
")
```

### gh-project-view: Status Distribution

```bash
# Save items once
echo "$ITEMS" > /tmp/gh_items.json

# Count by status
python3 -c "
import json
with open('/tmp/gh_items.json') as f:
    data = json.load(f)
    items = data.get('items', [])

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

### gh-project-triage: Priority Suggestion

```bash
# Use helper module for priority suggestion
PRIORITY_SUGGESTION=$(python3 helpers/gh_project_helpers.py suggest-priority \
  --title "$ITEM_TITLE" \
  --body "$ITEM_BODY" \
  --labels $ITEM_LABELS)
```

## Summary

The migration from jq to Python provides:
- ✅ Elimination of shell escaping bugs
- ✅ Better error messages
- ✅ More maintainable code
- ✅ Reusable helper functions
- ✅ Easier debugging and testing
- ✅ Better handling of edge cases

All commands now use consistent Python-based JSON processing for reliability and maintainability.
