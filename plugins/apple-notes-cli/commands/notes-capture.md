# Quick Note Capture

Quickly capture information into Apple Notes from the command line.

## Instructions

1. **Determine capture type** - Ask what kind of note the user wants to create:
   - Quick thought/idea
   - Meeting notes
   - Code snippet
   - Reference information
   - Journal entry

2. **Gather content** - Get the note content from the user or from context:
   - If they provide content, use it directly
   - If capturing from clipboard, help them pipe it in
   - If from a file, read and include it

3. **Generate appropriate title** - Based on content type:
   - Quick thoughts: `Idea - [brief description]`
   - Meeting: `Meeting - [topic] - YYYY-MM-DD`
   - Code: `Code - [language/purpose]`
   - Reference: `Ref - [topic]`
   - Journal: `Journal - YYYY-MM-DD`

4. **Create the note** - Use the notes CLI:
   ```bash
   notes create "Title" << 'EOF'
   Content here
   EOF
   ```

5. **Confirm creation** - Verify the note was created:
   ```bash
   notes show "Title"
   ```

## Quick Capture Templates

### Idea Note
```bash
notes create "Idea - [description]" << 'EOF'
## Idea
[Main idea]

## Context
[Why this came to mind]

## Next Steps
- [ ] Action item
EOF
```

### Meeting Note
```bash
notes create "Meeting - [topic] - $(date +%Y-%m-%d)" << 'EOF'
# [Topic] Meeting

## Attendees
-

## Agenda
1.

## Discussion


## Action Items
- [ ]

## Next Meeting

EOF
```

### Code Snippet
```bash
notes create "Code - [description]" << 'EOF'
## Purpose
[What this code does]

## Code
```[language]
[code here]
```

## Usage
[How to use it]
EOF
```

## Important Notes

- Always quote titles with spaces
- Use heredoc syntax for multi-line content
- Verify note was created successfully
- Suggest reviewing with `notes show` after creation
