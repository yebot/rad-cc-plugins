# Validate Backlog.md Structure

Audit the backlog directory for naming violations, structural issues, and metadata inconsistencies.

## Instructions

Launch the `backlog-validator` agent to perform comprehensive validation:

```
Use the backlog-validator agent to:
1. Check all task files match the `task-{id} - {title}.md` pattern
2. Verify CLI can read all task files
3. Detect orphaned or malformed files
4. Identify metadata inconsistencies
5. Generate a comprehensive validation report
6. Recommend remediation steps for any issues found
```

The validator will perform these checks:

## Validation Scope

### Critical Checks (Block Functionality)
- **File Naming Pattern**: All files match `task-{id} - {title}.md`
- **CLI Accessibility**: Can `backlog task list` see all files?
- **Directory Structure**: Required directories exist
- **Task ID Integrity**: No duplicate or missing IDs

### Warning Checks (Impact Workflow)
- **Task Completeness**: Missing acceptance criteria or descriptions
- **Workflow Issues**: Stale "In Progress" tasks, Done tasks with unchecked ACs
- **Metadata Quality**: Tasks without assignees, missing priorities

### Info Checks (Project Health)
- **Status Distribution**: How tasks are distributed across To Do/In Progress/Done
- **Label Usage**: Which labels are most common
- **Assignee Workload**: How work is distributed across team

## Expected Output

The validator will generate a report like:

```markdown
# Backlog.md Validation Report

## Executive Summary
- 📁 Total Files: 47
- ✅ Valid Tasks: 45
- ❌ Violations: 2
- 🏥 Health Score: 95%

## Critical Issues

### Naming Violations
❌ task-23-Fix bug.md
   Expected: task-23 - Fix bug.md
   Issue: Missing spaces around separator

❌ Fix login issue.md
   Expected: task-{id} - Fix login issue.md
   Issue: Missing task ID prefix

## Warnings

### Incomplete Tasks
⚠️  task-15 - Add API endpoint.md
   Missing acceptance criteria

⚠️  task-28 - Refactor components.md
   Status "In Progress" but no recent activity (14 days)

## Recommendations

### Immediate Fixes
1. Fix naming for task-23:
   backlog task edit 23 -t "Fix bug"
   (CLI will update filename automatically)

2. Recreate orphaned task:
   backlog task create "Fix login issue" -d "..."

3. Add ACs to task-15:
   backlog task edit 15 --ac "First criterion"

## Project Health
- To Do: 12 (26%)
- In Progress: 8 (17%)
- Done: 27 (57%)
```

## When to Run Validation

Use this command when:

1. **Troubleshooting Issues**:
   - "Task not showing up in list"
   - "CLI can't find task"
   - "Board not displaying correctly"

2. **After Bulk Operations**:
   - Created multiple tasks
   - Imported tasks from other systems
   - Reorganized backlog structure

3. **Periodic Health Checks**:
   - Weekly validation recommended
   - Before major milestones
   - After team onboarding

4. **Quality Assurance**:
   - Ensuring naming compliance
   - Checking workflow state health
   - Validating metadata quality

## What Gets Validated

### File Naming Pattern
```
Valid:   task-42 - Add authentication.md
Invalid: task-42-Add authentication.md
Invalid: 42 - Add authentication.md
Invalid: task-42.md
```

### Directory Structure
```
Required:
- backlog/tasks/     (all task files)
- backlog/docs/      (documentation)
- backlog/decisions/ (ADRs)
- backlog/drafts/    (draft tasks)
```

### Task Metadata
- Frontmatter exists and is valid YAML
- Required fields present (id, title, status)
- Status values are valid
- Task ID matches filename

## Important Notes

- **Non-destructive**: Validation never modifies files
- **Comprehensive**: Checks multiple layers (naming, metadata, workflow)
- **Actionable**: Provides specific CLI commands to fix issues
- **Educational**: Explains why violations matter

## After Validation

If issues are found:

1. **Review the report** with the user
2. **Prioritize fixes**: Critical > Warning > Info
3. **Offer to help** fix issues using proper CLI commands
4. **Educate** on prevention (use hooks, use agents)
5. **Run validation again** after fixes to confirm

## Definition of Done for This Command

- [ ] backlog-validator agent launched
- [ ] Comprehensive validation performed
- [ ] Report generated and presented to user
- [ ] Issues categorized by severity
- [ ] Remediation commands provided for all issues
- [ ] User understands how to prevent future violations
