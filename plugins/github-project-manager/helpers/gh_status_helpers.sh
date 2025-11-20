#!/usr/bin/env bash
# GitHub Project Status Helper Functions
# Source this file to get helper functions for status reporting

# Save items JSON to temp file for processing
save_items_json() {
    local items_json="$1"
    echo "$items_json" > /tmp/gh_project_items.json
}

# Count items by field value
count_by_field() {
    local field_name="$1"
    python3 -c "
import json
with open('/tmp/gh_project_items.json') as f:
    data = json.load(f)
    items = data.get('items', [])

    counts = {}
    for item in items:
        found = False
        for fv in item.get('fieldValues', []):
            if fv.get('name') == '${field_name}':
                value = fv.get('name') or fv.get('text') or str(fv.get('number', 'Unset'))
                counts[value] = counts.get(value, 0) + 1
                found = True
                break
        if not found:
            counts['Unset'] = counts.get('Unset', 0) + 1

    for key in sorted(counts.keys()):
        print(f'{key}: {counts[key]}')
"
}

# Get items by status
filter_by_status() {
    local status="$1"
    python3 -c "
import json
with open('/tmp/gh_project_items.json') as f:
    data = json.load(f)
    items = data.get('items', [])

    for item in items:
        for fv in item.get('fieldValues', []):
            if fv.get('name') == 'Status' and fv.get('name') == '${status}':
                content = item.get('content', {})
                number = content.get('number', 'draft')
                title = content.get('title', 'Untitled')
                print(f'#{number} - {title}')
                break
"
}

# Get high priority items not started
get_urgent_backlog() {
    python3 -c "
import json
with open('/tmp/gh_project_items.json') as f:
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

        if priority in ['P0', 'P1'] and status in ['Backlog', 'Todo']:
            content = item.get('content', {})
            number = content.get('number', 'draft')
            title = content.get('title', 'Untitled')
            print(f'  - #{number} {title} (Priority: {priority}, Status: {status})')
"
}

# Get stale items (not updated in N days)
get_stale_items() {
    local days="${1:-7}"
    python3 -c "
import json
from datetime import datetime, timedelta

with open('/tmp/gh_project_items.json') as f:
    data = json.load(f)
    items = data.get('items', [])
    threshold = datetime.now() - timedelta(days=${days})

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
                    # Parse ISO datetime
                    updated_at = datetime.fromisoformat(updated_str.replace('Z', '+00:00'))
                    if updated_at < threshold:
                        number = content.get('number', 'draft')
                        title = content.get('title', 'Untitled')
                        days_old = (datetime.now() - updated_at).days
                        updated_date = updated_str.split('T')[0]
                        print(f'  - #{number} {title}')
                        print(f'    Last updated: {updated_date} ({days_old} days ago)')
                except:
                    pass
"
}

# Calculate completion percentage for story points
calculate_completion() {
    python3 -c "
import json
with open('/tmp/gh_project_items.json') as f:
    data = json.load(f)
    items = data.get('items', [])

    total_points = 0
    completed_points = 0
    in_progress_points = 0

    for item in items:
        status = None
        points = None

        for fv in item.get('fieldValues', []):
            if fv.get('name') == 'Status':
                status = fv.get('name')
            elif fv.get('name') == 'Story Points':
                points = fv.get('number', 0)

        if points:
            total_points += points
            if status == 'Done':
                completed_points += points
            elif status == 'In Progress':
                in_progress_points += points

    if total_points > 0:
        completion_pct = (completed_points / total_points) * 100
        print(f'Total Points: {total_points}')
        print(f'Completed: {completed_points} ({completion_pct:.1f}%)')
        print(f'In Progress: {in_progress_points}')
        print(f'Remaining: {total_points - completed_points - in_progress_points}')
    else:
        print('No story points data available')
"
}

# Get items missing a field
get_items_missing_field() {
    local field_name="$1"
    python3 -c "
import json
with open('/tmp/gh_project_items.json') as f:
    data = json.load(f)
    items = data.get('items', [])

    count = 0
    for item in items:
        has_field = False
        for fv in item.get('fieldValues', []):
            if fv.get('name') == '${field_name}':
                has_field = True
                break

        if not has_field:
            count += 1
            content = item.get('content', {})
            number = content.get('number', 'draft')
            title = content.get('title', 'Untitled')
            print(f'  - #{number} {title}')

    if count == 0:
        print('  ✅ All items have {field_name} assigned')
"
}

# Count items by type
count_by_type() {
    python3 -c "
import json
with open('/tmp/gh_project_items.json') as f:
    data = json.load(f)
    items = data.get('items', [])

    type_counts = {'Issue': 0, 'PullRequest': 0, 'DraftIssue': 0}

    for item in items:
        item_type = item.get('content', {}).get('type', 'Unknown')
        if item_type in type_counts:
            type_counts[item_type] += 1

    print(f\"Issues: {type_counts['Issue']}\")
    print(f\"Pull Requests: {type_counts['PullRequest']}\")
    print(f\"Draft Items: {type_counts['DraftIssue']}\")
"
}

# Extract field IDs and options from fields JSON
extract_field_info() {
    local fields_json="$1"
    local field_name="$2"

    echo "$fields_json" | python3 -c "
import json, sys
fields = json.load(sys.stdin)
field_name = '${field_name}'

for field in fields:
    if field.get('name') == field_name:
        print(f\"ID: {field.get('id')}\")
        print(f\"Type: {field.get('dataType')}\")
        options = field.get('options', [])
        if options:
            print('Options:')
            for opt in options:
                print(f\"  - {opt.get('name')} (ID: {opt.get('id')})\")
        break
"
}
