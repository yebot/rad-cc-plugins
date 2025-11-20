# GitHub Project Manager Plugin

Comprehensive project-first workflow management using GitHub Projects V2 via the gh CLI. This plugin replaces traditional issue-centric workflows with modern project management powered by GitHub's Projects V2 system.

## Overview

GitHub is deprecating traditional Issues-first workflows in favor of Projects V2, which offers rich custom fields, multiple views, powerful automation, and better cross-repository support. This plugin provides everything you need to manage projects effectively using the `gh` CLI.

## Why GitHub Projects V2?

**Projects V2 Benefits**:
- 🎯 **Project-First**: Projects are the primary organizing unit, not issues
- 🔧 **Custom Fields**: Rich field types (status, priority, dates, iterations, numbers, text)
- 👁️ **Multiple Views**: Table, board, and roadmap views with custom filters
- 🤖 **Automation**: Built-in workflows for status management
- 📝 **Draft Items**: Create items without creating issues
- 🔗 **Cross-Repository**: Span multiple repos in one project
- 📊 **Better Reporting**: Built-in insights and metrics

## Plugin Components

### Agents

#### project-manager
Elite GitHub Projects V2 management specialist for all project operations.

**Use for**:
- Creating and managing projects
- Adding items (issues, PRs, drafts)
- Updating item fields
- Searching and filtering
- Generating reports
- All general project operations

**Example**: "Add issue #42 to Sprint 5 project and set priority to P1"

#### project-architect
Project structure design and optimization specialist.

**Use for**:
- Designing new project structures
- Recommending field configurations
- Analyzing existing projects
- Planning workflow improvements
- Creating project templates

**Example**: "We're starting Q1 planning, help me design a good project structure"

#### item-orchestrator
Batch operations and item lifecycle management specialist.

**Use for**:
- Bulk field updates
- Backlog triage automation
- Archive/cleanup operations
- Field synchronization
- Item reports and analytics

**Example**: "Archive all items that have been done for over 30 days"

### Commands

#### /gh-project-create
Guided workflow for creating new projects with proper field setup.

**Features**:
- Project type selection (Agile/Roadmap/Bug Tracking)
- Automatic field creation
- Best practice recommendations
- Repository linking

**Usage**: `/gh-project-create`

#### /gh-project-view
Comprehensive project viewing with status reports.

**Features**:
- Project metadata and fields
- Status and priority distributions
- Items requiring attention
- Health metrics
- Drill-down options

**Usage**: `/gh-project-view`

#### /gh-item-add
Add issues, PRs, or draft items to projects with field assignment.

**Features**:
- Add existing issues/PRs
- Create draft items
- Smart field suggestions
- Batch adding support

**Usage**: `/gh-item-add`

#### /gh-project-status
Generate comprehensive status reports with metrics and insights.

**Features**:
- Executive summary
- Status/priority distributions
- Velocity tracking
- Items requiring attention
- Actionable recommendations

**Usage**: `/gh-project-status`

#### /gh-project-triage
Systematic item triage with priority and status assignment.

**Features**:
- Smart priority suggestions
- Interactive or batch mode
- Comprehensive triage reports
- Automation recommendations

**Usage**: `/gh-project-triage`

### Skills

#### project-workflow-patterns
Common workflow patterns and best practices for different team types.

**Includes**:
- Agile Scrum workflow
- Kanban continuous flow
- Bug triage workflow
- Feature roadmap workflow
- Automation patterns

**Use when**: Setting up new projects or optimizing workflows

#### project-field-management
Comprehensive guide to field types, configuration, and management.

**Includes**:
- All field type details
- Best practices per field type
- Field discovery and querying
- Batch operations
- Troubleshooting

**Use when**: Setting up fields or troubleshooting field issues

### Hooks

Contextual assistance and reminders:
- Project operation tips
- Command suggestions
- Best practice reminders
- gh CLI usage hints

## Quick Start

### 1. Prerequisites

Ensure GitHub CLI is installed and authenticated with project scope:

```bash
# Check installation
gh --version

# Check auth status
gh auth status

# If missing 'project' scope:
gh auth refresh -s project
```

### 2. Create Your First Project

```bash
# Use guided creation
/gh-project-create

# Or manually
gh project create --owner "@me" --title "My First Project"
```

### 3. Add Items

```bash
# Use guided addition
/gh-item-add

# Or manually
gh project item-add 1 --owner "@me" --url https://github.com/owner/repo/issues/42
```

### 4. View Project Status

```bash
/gh-project-status
```

## Common Workflows

### Starting a New Sprint

1. **Create Sprint Project**:
   ```
   /gh-project-create
   Select: Agile Sprint
   ```

2. **Configure Fields**:
   - Status: Backlog, Todo, In Progress, Review, Done
   - Priority: P0, P1, P2, P3
   - Story Points: 1, 2, 3, 5, 8, 13
   - Sprint: 2-week iterations

3. **Add Backlog Items**:
   ```
   Use project-manager agent: "Add all issues with label 'sprint-candidate' to the Sprint 5 project"
   ```

4. **Triage**:
   ```
   /gh-project-triage
   ```

5. **Sprint Planning**:
   - Review `/gh-project-status`
   - Move refined P1/P2 items to current sprint
   - Assign team members

### Managing a Product Roadmap

1. **Create Roadmap Project**:
   ```
   /gh-project-create
   Select: Product Roadmap
   ```

2. **Add Ideas as Drafts**:
   ```
   Use project-manager agent: "Create draft items for Q1 features"
   ```

3. **Quarterly Planning**:
   - Assign priorities
   - Assign quarters
   - Set launch dates
   - Use roadmap view for visualization

4. **Track Progress**:
   ```
   /gh-project-status
   ```

### Bug Triage Process

1. **Create Bug Project**:
   ```
   /gh-project-create
   Select: Bug Tracking
   ```

2. **Link to Repository**:
   - Automatic addition of new bugs

3. **Daily Triage**:
   ```
   /gh-project-triage
   Scope: New bugs only
   ```

4. **Track Resolution**:
   ```
   /gh-project-status
   Focus: Critical/High severity
   ```

## Field Configuration Guide

### Essential Fields (All Projects)

**Status** (Single Select):
- Purpose: Primary workflow state
- Options: Depends on workflow type
- Required: Yes

**Priority** (Single Select):
- Purpose: Item urgency/importance
- Options: P0 (Critical), P1 (High), P2 (Medium), P3 (Low)
- Required: Yes

### Agile Sprint Fields

- **Story Points** (Number): Estimation
- **Sprint** (Iteration): Sprint assignment
- **Team Member** (Single Select): Assignee

### Product Roadmap Fields

- **Quarter** (Single Select): Time period
- **Launch Date** (Date): Target ship date
- **Impact** (Number): Customer count
- **Owner** (Text): PM name

### Bug Tracking Fields

- **Severity** (Single Select): Bug criticality
- **Component** (Single Select): System area
- **Affected Users** (Number): Impact count
- **Reported Date** (Date): When discovered

## Best Practices

### Field Management

1. **Start Minimal**: Begin with Status and Priority only
2. **Add as Needed**: Don't create fields speculatively
3. **Standardize Options**: Use consistent naming across projects
4. **Document Meanings**: Write down what P0 vs P1 means
5. **Regular Cleanup**: Remove unused fields

### Workflow Design

1. **Clear Progression**: Status should flow logically
2. **Limit WIP**: Don't pull too many items to In Progress
3. **Regular Triage**: Weekly backlog refinement
4. **Automate Transitions**: Use GitHub Actions for status updates
5. **Archive Completed**: Keep active views clean

### Priority Assignment

**P0 (Critical)**:
- Production down
- Data loss/corruption
- Security vulnerabilities
- Blocking all users

**P1 (High)**:
- Significant user impact (>25%)
- Important feature broken
- Sprint commitments

**P2 (Medium)**:
- Moderate impact
- Standard features
- Non-blocking bugs

**P3 (Low)**:
- Nice-to-have
- Minor issues
- Future improvements

### Status Definitions

**Backlog**: Not yet refined or scheduled
**Todo**: Refined and ready to start
**In Progress**: Actively being worked
**In Review**: PR open, awaiting review
**Done**: Completed and merged

## Advanced Usage

### Batch Operations

```bash
# Use item-orchestrator agent
"Update all items with 'auth' in the title to P1 priority"
"Archive all done items older than 30 days"
"Set all backlog items without priority to P2"
```

### Custom Reporting

```bash
# Use project-manager agent
"Generate a report showing velocity over last 3 sprints"
"Show me all P0/P1 items not in progress"
"List items by assignee with their point totals"
```

### Project Automation

Set up GitHub Actions workflows:

```yaml
# .github/workflows/project-automation.yml
name: Project Automation

on:
  pull_request:
    types: [opened, closed]

jobs:
  update-project:
    runs-on: ubuntu-latest
    steps:
      - name: Move to In Review
        if: github.event.action == 'opened'
        run: |
          # Use GitHub GraphQL API to update project item

      - name: Move to Done
        if: github.event.action == 'closed' && github.event.pull_request.merged
        run: |
          # Update to Done status
```

## Troubleshooting

### Authentication Issues

**Problem**: `gh: Resource not accessible by integration`

**Solution**:
```bash
gh auth status
gh auth refresh -s project
```

### Field Updates Fail

**Problem**: Item field update returns error

**Solutions**:
1. Verify field ID is correct
2. For single-select, use option ID not name
3. Check date format (YYYY-MM-DD)
4. Ensure item exists in project

### Can't See Field Options

**Problem**: Single-select field has no options

**Solution**: CLI can create fields but not options. Use GitHub UI:
1. Go to project settings
2. Click field name
3. Add options
4. Save

### Items Not Showing

**Problem**: Added items don't appear in project

**Solutions**:
1. Refresh browser
2. Check view filters
3. Verify item was added successfully
4. Check project permissions

## Comparison: Issues vs Projects

| Feature | GitHub Issues | GitHub Projects V2 |
|---------|---------------|-------------------|
| Organization | Repository-centric | Project-centric |
| Custom Fields | Labels only | Rich field types |
| Views | List only | Table, Board, Roadmap |
| Cross-repo | Limited | Full support |
| Estimation | Via labels | Dedicated fields |
| Sprints | Via milestones | Iteration fields |
| Automation | Limited | Extensive |
| Reporting | Basic | Advanced |

## Migration from github-issues Plugin

If you were using the `github-issues` plugin:

1. **Projects Replace Issues**: Think project-first, not issue-first
2. **Labels → Fields**: Priority labels become Priority field
3. **Milestones → Iterations**: Sprint/release planning via iterations
4. **Multiple Projects**: Separate projects for sprints, roadmap, bugs
5. **Richer Metadata**: More fields for better tracking

**Migration Steps**:
1. Create project with `/gh-project-create`
2. Add existing issues to project
3. Set Status field based on issue state
4. Set Priority based on labels
5. Configure automation for future items

## Resources

### Documentation
- [GitHub Projects V2 Docs](https://docs.github.com/en/issues/planning-and-tracking-with-projects)
- [gh project CLI Reference](https://cli.github.com/manual/gh_project)

### Plugin Support
- Report issues on plugin marketplace repository
- Check CLAUDE.md for usage guidelines
- Use agents for interactive help

### Getting Help

**Within Claude Code**:
- Ask project-manager agent for general help
- Ask project-architect for design questions
- Ask item-orchestrator for batch operation help
- Use `/gh-project-view` to understand project state
- Use `/gh-project-status` for health insights

## Examples

### Example 1: Personal Task Management

```bash
# Create personal todo project
/gh-project-create
Title: My Tasks
Type: Kanban
Owner: @me

# Add tasks as draft items
gh project item-create 1 --owner "@me" \
  --title "Review pull requests" \
  --body "Daily PR review routine"

# View status
/gh-project-view
```

### Example 2: Team Sprint

```bash
# Create sprint project
/gh-project-create
Title: Sprint 12
Type: Agile Sprint

# Triage backlog
/gh-project-triage
Scope: Backlog only

# Plan sprint
Use project-manager agent:
"Move all P1 items from backlog to current sprint iteration"

# Daily standup
/gh-project-view
Filter: In Progress

# Sprint review
/gh-project-status
```

### Example 3: Product Roadmap

```bash
# Create roadmap
/gh-project-create
Title: 2025 Product Roadmap
Type: Product Roadmap

# Add features as drafts
Use project-manager agent:
"Create draft items for the 10 feature ideas in features.md"

# Quarterly planning
Use project-architect agent:
"Help me prioritize and schedule these features across Q1-Q4"

# Track progress
/gh-project-status
Timeframe: This quarter
```

## Version History

- **1.0.0** (2025-01-20): Initial release
  - 3 specialized agents
  - 5 slash commands
  - 2 comprehensive skills
  - Full gh CLI integration
  - Contextual hooks

## Contributing

This plugin is part of the rad-cc-plugins marketplace. Contributions welcome!

## License

MIT License - See marketplace repository for details

---

**Ready to modernize your GitHub workflow?** Install this plugin and start managing projects the modern way with GitHub Projects V2!
