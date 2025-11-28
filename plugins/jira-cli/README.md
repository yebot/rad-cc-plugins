# Jira CLI Plugin

Expert Jira CLI assistant for managing issues, sprints, and workflows using [ankitpokhrel/jira-cli](https://github.com/ankitpokhrel/jira-cli).

## Overview

This plugin transforms Claude Code into a Jira CLI expert that can help you manage your Jira projects entirely from the command line with minimal trial and error. It provides comprehensive guidance for:

- Creating and managing issues through their complete lifecycle
- Planning and executing sprints
- Constructing advanced JQL queries
- Navigating Jira workflows
- Integrating Jira with git/CI/CD workflows

## Prerequisites

**Required:**
- [jira-cli](https://github.com/ankitpokhrel/jira-cli) installed and accessible in PATH
- Jira Cloud or Server instance
- Valid Jira credentials (API token for Cloud, username/password for Server)

**Installation:**
```bash
# macOS
brew install ankitpokhrel/jira-cli/jira-cli

# Linux
curl -sL https://raw.githubusercontent.com/ankitpokhrel/jira-cli/main/install.sh | sh

# Go
go install github.com/ankitpokhrel/jira-cli/cmd/jira@latest
```

## Components

### Agents

#### jira-manager
**When to use:** Any time you need to work with Jira issues

**Capabilities:**
- Create, view, edit, and search issues
- Assign and transition issues
- Link related issues
- Manage labels and components
- Parse `--raw` (JSON) and `--plain` (text) output formats

**Proactive behavior:** Automatically activates when users mention Jira tickets, issues, or need to interact with Jira.

**Example usage:**
```
Create a high-priority bug for the login error
Show me all my in-progress issues
Assign PROJ-123 to me and move it to In Review
```

#### jira-sprint-master
**When to use:** Sprint planning, backlog grooming, or agile ceremonies

**Capabilities:**
- List and view sprints
- Add/remove issues from sprints
- Create and manage epics
- View boards and sprint progress
- Generate sprint metrics

**Proactive behavior:** Activates when users mention sprints, epics, boards, or agile workflows.

**Example usage:**
```
Show me the current sprint
Add PROJ-123, PROJ-124, and PROJ-125 to sprint 42
What's the progress on epic PROJ-100?
Generate velocity report for last 3 sprints
```

#### jira-query-builder
**When to use:** Complex issue searches, reports, or data analysis

**Capabilities:**
- Construct advanced JQL queries
- Combine multiple filters and conditions
- Use JQL functions (currentUser(), startOfWeek(), etc.)
- Optimize query performance
- Save and reuse common queries

**Proactive behavior:** Activates when users need complex filtering or custom reports.

**Example usage:**
```
Find all high-priority bugs assigned to me that were created this week
Show me issues in sprint 42 that are still in progress
List all stories without epics
```

### Commands

#### /jira-setup
**Purpose:** Initialize and configure jira-cli authentication and project settings

**What it does:**
- Guides through jira-cli installation
- Sets up authentication (API tokens, basic auth, PAT)
- Configures default project
- Sets up multiple project configurations
- Enables shell completion
- Troubleshoots common setup issues

**When to use:**
- First time using jira-cli
- Adding a new project configuration
- Authentication issues
- Switching Jira instances

#### /jira-issue-workflow
**Purpose:** Complete issue lifecycle management from creation to completion

**What it does:**
- Walks through the entire issue lifecycle
- Provides templates for different issue types
- Explains workflow states and transitions
- Integrates with git commits and PRs
- Handles edge cases (blocking, reopening, etc.)

**When to use:**
- Learning Jira workflows
- Creating issues with proper details
- Understanding when to use each status
- Integrating Jira with development workflow

#### /jira-sprint-planning
**Purpose:** Sprint planning, backlog grooming, and sprint execution workflows

**What it does:**
- Complete sprint ceremony guidance
- Backlog grooming checklists
- Sprint planning steps
- Daily standup reports
- Sprint review metrics
- Retrospective templates

**When to use:**
- Planning a new sprint
- Running sprint ceremonies
- Tracking sprint progress
- Calculating velocity and metrics

### Skills

#### jira-jql-patterns
**Purpose:** Master JQL query construction for advanced filtering

**What you'll learn:**
- JQL syntax and operators
- Common query patterns (my work, time-based, team queries)
- Advanced filtering with functions
- Query optimization techniques
- Saving and reusing queries

**When to use:**
- Need to construct complex queries
- Want to understand JQL syntax
- Looking for query templates
- Optimizing slow queries

#### jira-workflow-transitions
**Purpose:** Understanding and navigating Jira workflow states

**What you'll learn:**
- Workflow fundamentals (statuses and transitions)
- Common workflow patterns (Scrum, Kanban, etc.)
- Best practices for transitioning issues
- Handling special cases (blocking, reopening)
- Workflow automation with git/CI/CD

**When to use:**
- Learning your team's workflow
- Understanding when to transition issues
- Handling blocked or stuck issues
- Setting up workflow automation

## Quick Start

### 1. Setup
```bash
# Install jira-cli (if not already installed)
brew install ankitpokhrel/jira-cli/jira-cli

# Use the setup command
/jira-setup
```

### 2. Common Operations

**View your current work:**
```
Show me my in-progress issues
```

**Create an issue:**
```
Create a bug: Login page returns 500 error, priority High
```

**Work on an issue:**
```
Assign PROJ-123 to me
Move PROJ-123 to In Progress
```

**Search issues:**
```
Find all critical bugs that are not closed
```

**Sprint planning:**
```
Show me the current sprint
Add high-priority backlog items to next sprint
```

## Key Features

### Minimal Trial and Error

The plugin is designed to help you use jira-cli effectively on the first try:

- **Agents know exact command syntax** - No guessing at flags or parameters
- **Output format selection** - Automatically chooses `--plain` for display or `--raw` for parsing
- **Error handling** - Understands common errors and suggests fixes
- **Workflow awareness** - Knows valid transitions for different issue types
- **Context-aware** - Provides relevant information based on your request

### Output Format Intelligence

The agents automatically select the right output format:

- `--plain`: Human-readable text for display to users
- `--raw`: JSON format for parsing and automation
- `--csv`: CSV format for data export

Example:
```bash
# Agent shows you this (plain)
jira issue list --assignee @me --status "In Progress" --plain

# But uses this for automation (raw)
jira issue list --assignee @me --status "In Progress" --raw
```

### JQL Mastery

The jira-query-builder agent constructs sophisticated queries:

```jql
project = PROJ AND
status = "In Progress" AND
assignee = currentUser() AND
(priority IN (High, Critical) OR labels = urgent) AND
created >= -7d
ORDER BY priority DESC, created ASC
```

### Workflow Integration

Integrate Jira with your development workflow:

**Git commit messages:**
```bash
git commit -m "PROJ-123: Add user authentication

Implemented OAuth2 authentication flow.
See PROJ-123 for requirements."
```

**CI/CD pipelines:**
```bash
# Auto-transition on deployment
jira issue move PROJ-123 "Testing" --comment "Deployed to staging by CI/CD"
```

## Usage Patterns

### Pattern 1: Bug Fix Workflow
```
1. "Create a critical bug: API endpoint /users returns 404"
2. "Assign BUG-123 to me"
3. "Move BUG-123 to In Progress"
   # ... fix bug ...
4. "Move BUG-123 to In Review with comment: PR #456"
   # ... PR reviewed and merged ...
5. "Move BUG-123 to Done"
```

### Pattern 2: Sprint Planning
```
1. "/jira-sprint-planning"
2. "Show me high-priority backlog items"
3. "Add PROJ-123, PROJ-124, PROJ-125 to sprint 42"
4. "Assign PROJ-123 to developer@example.com"
5. "Show sprint 42 summary"
```

### Pattern 3: Epic Management
```
1. "Create epic: User Authentication System"
2. "Create stories for epic PROJ-100:"
   - Add OAuth2 support
   - Create login form
   - Add password reset
3. "Show epic PROJ-100 progress"
```

### Pattern 4: Advanced Queries
```
"Find all stories created this month that are:
- Assigned to my team
- Not in any sprint
- Have story points between 3 and 8
- Priority is High or Medium
Order by priority"
```

## Best Practices

### 1. Always Add Context
When transitioning issues, always add comments:
```bash
jira issue move PROJ-123 "In Review" --comment "PR: https://github.com/company/repo/pull/456"
```

### 2. Use Issue Keys in Commits
Reference Jira issues in git commits:
```bash
git commit -m "PROJ-123: Add login validation"
```

### 3. Keep Issues Updated
Update issues regularly to reflect current state:
```bash
jira issue comment PROJ-123 "Completed form validation, working on API integration"
```

### 4. Link Related Work
Connect issues, PRs, and blockers:
```bash
jira issue link PROJ-123 PROJ-100 "is blocked by"
jira issue link PROJ-123 https://docs.example.com/api --type web
```

### 5. Use JQL for Efficiency
Save time with JQL queries:
```bash
alias jira-my-work='jira issue list --jql "assignee = currentUser() AND status NOT IN (Done, Closed)" --plain'
```

## Examples

### Example 1: Create and Work on a Story
```
User: Create a story for implementing dark mode toggle
Agent: [Creates story with proper format]

User: Add acceptance criteria
Agent: [Adds detailed acceptance criteria]

User: Assign to me and add to current sprint
Agent: [Assigns and adds to sprint]

User: Move to In Progress
Agent: [Transitions with comment]
```

### Example 2: Sprint Standup Report
```
User: Generate my standup report
Agent:
Yesterday: Completed PROJ-123, PROJ-124
Today: Working on PROJ-125, PROJ-126
Blockers: PROJ-127 blocked by PROJ-100
```

### Example 3: Epic Progress Report
```
User: What's the status of epic PROJ-100?
Agent:
Epic: User Authentication (PROJ-100)
Total Stories: 8
Completed: 5 (62.5%)
In Progress: 2
To Do: 1
Story Points: 34/55 completed
```

## Troubleshooting

### "jira: command not found"
Install jira-cli using one of the installation methods above, or run `/jira-setup`.

### "unauthorized" or "401" error
Run `/jira-setup` to reconfigure authentication. For Cloud, generate a new API token at https://id.atlassian.com/manage-profile/security/api-tokens

### Issues won't transition
Use interactive mode to see available transitions:
```bash
jira issue move PROJ-123
```

### Slow queries
Add project filter to narrow search:
```jql
project = PROJ AND status = "In Progress"  # Fast
status = "In Progress"  # Slow (searches all projects)
```

## Advanced Usage

### Multiple Project Configurations
```bash
# Create configs
jira init --config ~/.config/.jira/.config.project1.yml
jira init --config ~/.config/.jira/.config.project2.yml

# Use specific config
jira issue list -c ~/.config/.jira/.config.project1.yml

# Create aliases
alias jira-proj1='jira -c ~/.config/.jira/.config.project1.yml'
alias jira-proj2='jira -c ~/.config/.jira/.config.project2.yml'
```

### Automation Scripts
```bash
#!/bin/bash
# daily-status.sh

echo "===== My Work ====="
jira issue list --assignee @me --status "In Progress" --plain

echo -e "\n===== Sprint Progress ====="
jira sprint view <SPRINT_ID> --plain
```

### CI/CD Integration
```bash
#!/bin/bash
# deploy.sh

# Extract issue keys from commits
ISSUES=$(git log --pretty=%B $LAST_TAG..HEAD | grep -oE "PROJ-[0-9]+" | sort -u)

# Transition each issue
for issue in $ISSUES; do
  jira issue move "$issue" "Testing" --comment "Deployed to staging"
done
```

## Tips and Tricks

1. **Use tab completion** - Enable shell completion for faster typing
2. **Create aliases** - Save frequently used commands as shell aliases
3. **Use --no-truncate** - See full content without truncation
4. **Combine with jq** - Parse `--raw` JSON output with jq
5. **Set up team queries** - Share common JQL queries with team

## Contributing

Found a bug or have a suggestion? This plugin is part of the [rad-cc-plugins](https://github.com/your-repo/rad-cc-plugins) marketplace.

## Resources

- [jira-cli Documentation](https://github.com/ankitpokhrel/jira-cli)
- [JQL Reference](https://support.atlassian.com/jira-service-management-cloud/docs/use-advanced-search-with-jira-query-language-jql/)
- [Jira REST API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/)

## License

This plugin is part of the rad-cc-plugins marketplace and follows the same license.

## Version

Current version: 1.0.0

## Author

Tobey Forsman (tobeyforsman@gmail.com)
