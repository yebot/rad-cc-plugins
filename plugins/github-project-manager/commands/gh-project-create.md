---
name: gh-project-create
description: Create new GitHub project with guided workflow and field configuration
tools: Bash, AskUserQuestion, TodoWrite
model: sonnet
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
PROJECT_ID=$(gh project create --owner "@me" --title "Q1 2025 Roadmap" --format json | jq -r '.id')
PROJECT_NUMBER=$(gh project list --owner "@me" --format json | jq -r '.[] | select(.title=="Q1 2025 Roadmap") | .number')
```

### Step 3: Create Core Fields

Based on the project type, create appropriate fields:

#### For All Project Types:

**Status Field**:
```bash
gh project field-create $PROJECT_ID --owner "<owner>" --data-type SINGLE_SELECT --name "Status"
```

After creation, you'll need to use the GitHub UI or API to add status options. Document the recommended options:
- Agile: Backlog, Todo, In Progress, In Review, Done
- Roadmap: Idea, Planned, In Development, Launched
- Bug Tracking: New, Triaged, In Progress, Fixed, Verified

**Priority Field**:
```bash
gh project field-create $PROJECT_ID --owner "<owner>" --data-type SINGLE_SELECT --name "Priority"
```

Recommended options: P0 (Critical), P1 (High), P2 (Medium), P3 (Low)

#### Additional Fields by Type:

**Agile Sprint**:
```bash
# Story Points
gh project field-create $PROJECT_ID --owner "<owner>" --data-type NUMBER --name "Story Points"

# Sprint (Iteration)
gh project field-create $PROJECT_ID --owner "<owner>" --data-type ITERATION --name "Sprint"

# Team Member
gh project field-create $PROJECT_ID --owner "<owner>" --data-type SINGLE_SELECT --name "Team Member"
```

**Product Roadmap**:
```bash
# Quarter
gh project field-create $PROJECT_ID --owner "<owner>" --data-type SINGLE_SELECT --name "Quarter"

# Launch Date
gh project field-create $PROJECT_ID --owner "<owner>" --data-type DATE --name "Launch Date"

# Impact (customer count)
gh project field-create $PROJECT_ID --owner "<owner>" --data-type NUMBER --name "Impact"

# Owner
gh project field-create $PROJECT_ID --owner "<owner>" --data-type TEXT --name "Owner"
```

**Bug Tracking**:
```bash
# Severity
gh project field-create $PROJECT_ID --owner "<owner>" --data-type SINGLE_SELECT --name "Severity"

# Component
gh project field-create $PROJECT_ID --owner "<owner>" --data-type SINGLE_SELECT --name "Component"

# Affected Users
gh project field-create $PROJECT_ID --owner "<owner>" --data-type NUMBER --name "Affected Users"

# Reported Date
gh project field-create $PROJECT_ID --owner "<owner>" --data-type DATE --name "Reported Date"
```

### Step 4: Link to Repository (if provided)

```bash
gh project link $PROJECT_NUMBER --owner "<owner>" --repo <owner>/<repo-name>
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
- Status (Single Select)
- Priority (Single Select)
- [Additional fields based on type...]

### Next Steps

1. **Configure Field Options** (via GitHub UI):
   - Go to your project settings
   - Edit each Single Select field to add options
   - Recommended Status options: [list]
   - Recommended Priority options: P0, P1, P2, P3

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

- **Field Options**: The gh CLI can create fields but cannot add Single Select options directly. Users must use the GitHub UI to configure dropdown options.
- **Validation**: Verify the project was created successfully by viewing it: `gh project view [number] --owner [owner]`
- **Permissions**: Ensure the user has the 'project' scope: `gh auth status`
  - If missing: `gh auth refresh -s project`

## Definition of Done

- [ ] Project created with unique title
- [ ] Project ID and number captured
- [ ] Core fields (Status, Priority) created
- [ ] Type-specific fields created
- [ ] Repository linked (if applicable)
- [ ] Comprehensive setup summary provided
- [ ] Next steps documented for the user
- [ ] Field option configuration instructions provided

## Error Handling

- If `gh auth` fails: Guide user to run `gh auth refresh -s project`
- If project creation fails: Check for duplicate names, verify owner exists
- If field creation fails: Verify project ID is correct, check permissions
- If linking fails: Verify repository exists and user has access

Remember: A well-structured project from the start saves hours of reorganization later. Take time to set it up right!
