# Export Apple Notes

Export notes to files for backup, sharing, or migration.

## Instructions

1. **Determine export scope**:
   - Single note
   - Multiple notes by pattern
   - All notes

2. **Choose export format**:
   - Markdown (.md) - Recommended
   - Plain text (.txt)
   - Combined single file
   - Individual files per note

3. **Set export location**:
   - Default: `~/Desktop/notes_export/`
   - Or user-specified directory

4. **Execute export**:
   - Create export directory
   - Export notes with proper naming
   - Preserve formatting

5. **Verify and report**:
   - Count exported notes
   - Report any errors
   - Show export location

## Export Commands

### Single Note Export
```bash
mkdir -p ~/Desktop/notes_export
notes show "Note Title" > ~/Desktop/notes_export/note-title.md
```

### Export by Pattern
```bash
mkdir -p ~/Desktop/notes_export

notes list | grep -i "meeting" | while read -r title; do
  # Sanitize filename
  filename=$(echo "$title" | tr ' ' '-' | tr -cd '[:alnum:]-')
  notes show "$title" > ~/Desktop/notes_export/"$filename.md"
  echo "Exported: $title"
done
```

### Export All Notes
```bash
mkdir -p ~/Desktop/notes_export
export_date=$(date +%Y-%m-%d)

notes list | while read -r title; do
  # Create safe filename
  filename=$(echo "$title" | tr ' /' '-' | tr -cd '[:alnum:]-')
  notes show "$title" > ~/Desktop/notes_export/"$filename.md"
done

echo "Export complete: ~/Desktop/notes_export"
ls -la ~/Desktop/notes_export | head -20
```

### Combined Export (Single File)
```bash
output_file=~/Desktop/all_notes_$(date +%Y-%m-%d).md

echo "# Apple Notes Export - $(date +%Y-%m-%d)" > "$output_file"
echo "" >> "$output_file"

notes list | while read -r title; do
  echo "## $title" >> "$output_file"
  echo "" >> "$output_file"
  notes show "$title" >> "$output_file"
  echo "" >> "$output_file"
  echo "---" >> "$output_file"
  echo "" >> "$output_file"
done

echo "Exported to: $output_file"
```

### Export with Index
```bash
mkdir -p ~/Desktop/notes_export
index_file=~/Desktop/notes_export/INDEX.md

echo "# Notes Export Index" > "$index_file"
echo "Exported: $(date)" >> "$index_file"
echo "" >> "$index_file"

notes list | while read -r title; do
  filename=$(echo "$title" | tr ' /' '-' | tr -cd '[:alnum:]-')
  notes show "$title" > ~/Desktop/notes_export/"$filename.md"
  echo "- [$title](./$filename.md)" >> "$index_file"
done
```

## Important Notes

- Sanitize filenames to remove special characters
- Consider note content length for combined exports
- Backup existing export directories before overwriting
- Use UTF-8 encoding for proper character support
- Add export date to directory or filename for versioning
