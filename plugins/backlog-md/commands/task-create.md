---
description: Create a new task in Backlog.md with full metadata support. Use when you need to track work, bugs, features, or any actionable item.
---

# Create Task

Create a new task in the project backlog with comprehensive metadata.

## Instructions

1. **Gather task information**:
   - Title (required): Clear, actionable description
   - Description: Detailed explanation of what needs to be done
   - Priority: high, medium, or low
   - Labels: Comma-separated tags for categorization
   - Assignee: Who should work on this (use @username format)

2. **Check for duplicates first**:
   - Search existing tasks: `backlog search "<keywords>"`
   - Review similar tasks to avoid duplication

3. **Create the task** using MCP tools or CLI:
   - Via MCP: Use `backlog.task_create` tool
   - Via CLI: `backlog task create "Title" --desc "Description" --priority high --labels feature,api`

4. **Add acceptance criteria** for clarity:
   - Define what "done" looks like
   - Use `--ac "Criterion 1" --ac "Criterion 2"` or add via MCP

5. **Set up dependencies** if this task depends on others:
   - Use `--dep task-1,task-2` or add via MCP tools
   - Dependencies prevent work on tasks until blockers are complete

6. **Organize into epics** if part of a larger feature:
   - Create as a subtask: `backlog task create -p <parent-id> "Subtask title"`
   - This creates a parent-child hierarchy for epic organization

## Task Creation Checklist

Before creating:
- [ ] Searched for duplicates
- [ ] Title is clear and actionable
- [ ] Description explains the "why" not just the "what"
- [ ] Appropriate priority set
- [ ] Labels applied for categorization
- [ ] Dependencies identified
- [ ] Acceptance criteria defined

## Example Commands

```bash
# Simple task
backlog task create "Add user authentication"

# Full task with all metadata
backlog task create "Implement OAuth2 login" \
  --desc "Add Google and GitHub OAuth providers for user authentication" \
  --priority high \
  --labels auth,security,feature \
  --ac "Google OAuth works" \
  --ac "GitHub OAuth works" \
  --ac "Token refresh implemented" \
  --dep task-5,task-8

# Subtask under an epic
backlog task create -p 10 "Add Google OAuth provider"
```