---
name: gh-project-create
description: Create new GitHub project with guided workflow and field configuration
tools: Bash, AskUserQuestion, TodoWrite
model: inherit
---

# Create GitHub Project

This command guides you through creating a new GitHub Project V2 with proper field configuration and best practices.

## Instructions

Follow this workflow to create a well-structured project:

### Step 1: Gather Project Information

Ask the user for key information:
1. **Project Name**: Clear, descriptive title (e.g., "Q1 2025 Roadmap", "Bug Triage", "Sprint 12")
2. **Project Type**:
   - Agile Sprint (for iterative development)
   - Product Roadmap (for long-term planning)
   - Bug Tracking (for issue triage)
   - Custom (user-defined structure)
3. **Owner**: "@me" (personal) or organization name
4. **Repository Link** (optional): Repository to link to project

### Step 2: Create the Project

Use the gh CLI to create the project:

```bash
gh project create --owner "<owner>" --title "<title>" --format json
```

Parse the output to get the project ID and number:
```bash
# Create project and capture output
PROJECT_JSON=$(gh project create --owner "@me" --title "Q1 2025 Roadmap" --format json)

# Use Python helper to parse JSON safely
PROJECT_ID=$(echo "$PROJECT_JSON" | python3 -c "import json, sys; data=json.load(sys.stdin); print(data.get('id', ''))")

# Get project number from list
PROJECT_LIST=$(gh project list --owner "@me" --format json)
PROJECT_NUMBER=$(echo "$PROJECT_LIST" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for project in data:
    if project.get('title') == 'Q1 2025 Roadmap':
        print(project.get('number', ''))
        break
")
```

### Step 3: Create Core Fields

Based on the project type, create appropriate fields:

**IMPORTANT NOTES**:
- The "Status" field is a **built-in default field** that already exists in new projects. Do NOT create it.
- For SINGLE_SELECT fields, options must be provided at creation time using `--single-select-options`
- Options are comma-separated, no spaces after commas

#### For All Project Types:

**Priority Field** (Status already exists):
```bash
# Priority field with options
gh project field-create $PROJECT_ID --owner "<owner>" \
  --data-type SINGLE_SELECT \
  --name "Priority" \
  --single-select-options "P0 (Critical),P1 (High),P2 (Medium),P3 (Low)"
```

#### Additional Fields by Type:

**Agile Sprint**:
```bash
# Story Points
gh project field-create $PROJECT_ID --owner "<owner>" \
  --data-type NUMBER --name "Story Points"

# Sprint (Iteration)
gh project field-create $PROJECT_ID --owner "<owner>" \
  --data-type ITERATION --name "Sprint"

# Team Member
gh project field-create $PROJECT_ID --owner "<owner>" \
  --data-type SINGLE_SELECT \
  --name "Team Member" \
  --single-select-options "Alice,Bob,Charlie,Diana"
```

**Product Roadmap**:
```bash
# Quarter
gh project field-create $PROJECT_ID --owner "<owner>" \
  --data-type SINGLE_SELECT \
  --name "Quarter" \
  --single-select-options "Q1 2025,Q2 2025,Q3 2025,Q4 2025"

# Launch Date
gh project field-create $PROJECT_ID --owner "<owner>" \
  --data-type DATE --name "Launch Date"

# Impact (customer count)
gh project field-create $PROJECT_ID --owner "<owner>" \
  --data-type NUMBER --name "Impact"

# Owner
gh project field-create $PROJECT_ID --owner "<owner>" \
  --data-type TEXT --name "Owner"
```

**Bug Tracking**:
```bash
# Severity
gh project field-create $PROJECT_ID --owner "<owner>" \
  --data-type SINGLE_SELECT \
  --name "Severity" \
  --single-select-options "Critical,High,Medium,Low"

# Component
gh project field-create $PROJECT_ID --owner "<owner>" \
  --data-type SINGLE_SELECT \
  --name "Component" \
  --single-select-options "Frontend,Backend,API,Database,Infrastructure"

# Affected Users
gh project field-create $PROJECT_ID --owner "<owner>" \
  --data-type NUMBER --name "Affected Users"

# Reported Date
gh project field-create $PROJECT_ID --owner "<owner>" \
  --data-type DATE --name "Reported Date"
```

### Step 4: Link to Repository (if provided)

**IMPORTANT**: The `--owner` parameter must match the repository owner:
- For personal repos: Use your GitHub username (not "@me")
- For organization repos: Use the org name

```bash
# Extract owner from repository string (handles owner/repo format)
REPO_OWNER=$(echo "$REPOSITORY" | python3 -c "
import sys
repo = sys.stdin.read().strip()
# Handle owner/repo format
if '/' in repo:
    # Strip any URL prefix if present
    if 'github.com/' in repo:
        repo = repo.split('github.com/')[-1]
    owner = repo.split('/')[0]
    print(owner)
else:
    print(repo)
")

# Link project to repository
gh project link $PROJECT_NUMBER --owner "$REPO_OWNER" --repo "$REPOSITORY"

# Example for specific cases:
# Personal repo: gh project link $PROJECT_NUMBER --owner "your-username" --repo your-username/repo-name
# Organization repo: gh project link $PROJECT_NUMBER --owner "org-name" --repo org-name/repo-name
```

### Step 5: Generate Setup Summary

Provide the user with a comprehensive summary:

```markdown
## Project Created Successfully!

### Project Details
- **Name**: [Project Name]
- **Number**: #[Project Number]
- **Owner**: [Owner]
- **URL**: https://github.com/users/[owner]/projects/[number] (or org URL)

### Fields Created
- Status (Built-in default field - already exists)
- Priority (Single Select with P0-P3 options)
- [Additional fields based on type...]

### Next Steps

1. **Customize Status Field Options** (via GitHub UI):
   - Status field exists by default with basic options
   - Go to project settings to customize options if needed
   - Recommended options by type:
     * Agile: Backlog, Todo, In Progress, In Review, Done
     * Roadmap: Idea, Planned, In Development, Launched
     * Bug Tracking: New, Triaged, In Progress, Fixed, Verified

2. **Create Views**:
   - Board View: Group by Status for kanban workflow
   - Table View: Sort by Priority for backlog management
   - [Additional views based on type...]

3. **Add Items**:
   - Use `/gh-item-add` to add existing issues/PRs
   - Use `gh project item-create` for draft items
   - Or manually add via GitHub UI

4. **Setup Automation** (optional):
   - Configure auto-archive for Done items
   - Set default field values for new items
   - Link to GitHub Actions for status sync

### Project Type: [Type]
[Type-specific guidance on usage, workflow, and best practices]
```

## Important Notes

- **Status Field**: The "Status" field is a built-in default field that already exists in new projects. Do NOT attempt to create it.
- **SINGLE_SELECT Fields**: Options MUST be provided at creation time using `--single-select-options` parameter. Options cannot be added later via CLI.
- **Field Options Format**: Comma-separated, no spaces after commas: `"Option1,Option2,Option3"`
- **Repository Linking**: The `--owner` parameter must match the repository owner exactly (cannot use "@me" for org repos)
- **Validation**: Verify the project was created successfully by viewing it: `gh project view [number] --owner [owner]`
- **Permissions**: Ensure the user has the 'project' scope: `gh auth status`
  - If missing: `gh auth refresh -s project`

## Definition of Done

- [ ] Project created with unique title
- [ ] Project ID and number captured
- [ ] Priority field created with options
- [ ] Type-specific fields created
- [ ] Repository linked (if applicable)
- [ ] Comprehensive setup summary provided
- [ ] Next steps documented for the user
- [ ] Status field customization instructions provided (if needed)

## Error Handling

- If `gh auth` fails: Guide user to run `gh auth refresh -s project`
- If project creation fails: Check for duplicate names, verify owner exists
- If field creation fails: Verify project ID is correct, check permissions
- If linking fails: Verify repository exists and user has access

Remember: A well-structured project from the start saves hours of reorganization later. Take time to set it up right!
