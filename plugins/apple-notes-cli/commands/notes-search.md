# Search Apple Notes

Find notes by title patterns or content keywords.

## Instructions

1. **Get search query** - Ask what the user is looking for:
   - Specific note title
   - Topic or keyword
   - Date range
   - Category or tag

2. **Search by title** - First search note titles:
   ```bash
   notes list | grep -i "[query]"
   ```

3. **Search by content** - If title search insufficient, search note contents:
   ```bash
   # Get all notes and search each one
   for title in $(notes list); do
     content=$(notes show "$title" 2>/dev/null)
     if echo "$content" | grep -qi "[query]"; then
       echo "Found in: $title"
     fi
   done
   ```

4. **Display results** - Show matching notes with context:
   - List matching note titles
   - Optionally show preview of content
   - Highlight the matching terms

5. **Offer next actions**:
   - View full content of a specific note
   - Narrow search with additional terms
   - Export results

## Search Patterns

### Case-insensitive title search
```bash
notes list | grep -i "keyword"
```

### Multiple keywords (AND)
```bash
notes list | grep -i "keyword1" | grep -i "keyword2"
```

### Date-based search
```bash
# Notes from January 2024
notes list | grep "2024-01"

# Notes from this year
notes list | grep "$(date +%Y)"
```

### Pattern matching
```bash
# Notes starting with "Meeting"
notes list | grep "^Meeting"

# Notes containing a project name
notes list | grep -i "\[ProjectName\]"
```

## Full-text Search Script

For comprehensive content search:

```bash
#!/bin/bash
query="$1"
echo "Searching for: $query"
echo "========================"

notes list | while read -r title; do
  content=$(notes show "$title" 2>/dev/null)
  if echo "$content" | grep -qi "$query"; then
    echo ""
    echo "📝 $title"
    echo "---"
    echo "$content" | grep -i "$query" | head -3
  fi
done
```

## Important Notes

- Title search is fast; content search examines each note
- Use specific keywords for better results
- Regex patterns are supported in grep
- Consider case sensitivity when searching
