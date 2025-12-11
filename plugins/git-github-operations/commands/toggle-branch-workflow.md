---
description: Toggle branch-based workflow enforcement on/off - adds/removes instructions from CLAUDE.md
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# Toggle Branch Workflow

You are helping the user enable or disable branch-based workflow enforcement for their project.

## Instructions

### 1. Check Current State

First, determine if branch workflow is currently enabled by looking for the marker:

```bash
grep -l "BRANCH-WORKFLOW-ENABLED" CLAUDE.md CLAUDE.local.md 2>/dev/null
```

- If a file is returned, workflow is **ENABLED** in that file
- If no output, workflow is **DISABLED**

### 2. If Currently DISABLED (Enabling)

Ask the user where to add the workflow instructions:

**Options:**
- `CLAUDE.md` - Shared with team, committed to repo
- `CLAUDE.local.md` - Personal, gitignored, not shared

Then:

1. Read the template from the plugin docs (or use the embedded template below)
2. Check if the target file exists; create it if not
3. Append the workflow instruction block to the file
4. Report success: "Branch workflow ENABLED in [filename]. Commits to main/master will trigger warnings."

**Template to append** (get from plugin `docs/branch-workflow-instructions.md` or use this):

```markdown
<!-- BRANCH-WORKFLOW-ENABLED -->
## Branch-Based Workflow

This project uses a branch-based development workflow. Follow these practices:

### Branch Strategy

- **Protected branches**: `main`, `master` - never commit directly
- **Feature branches**: Create from main for all new work
- **Branch naming**: Use prefixes like `feat/`, `fix/`, `refactor/`, `docs/`

### Workflow Steps

1. **Start new work**: Always create a feature branch
   ```bash
   git checkout main && git pull origin main && git checkout -b feat/your-feature-name
   ```

2. **Stay in sync**: Periodically rebase on main
   ```bash
   git fetch origin && git rebase origin/main
   ```

3. **Push and create PR**: When ready
   ```bash
   git push -u origin feat/your-feature-name
   gh pr create --title "feat: ..." --body "..."
   ```

### Task Tracker Integration

- Reference task IDs in branch names: `feat/TASK-123-description`
- Include task references in commits: `feat: description [TASK-123]`
- Link PRs to tasks in the PR description

### Configuration

- **Sync reminder threshold**: Set `BRANCH_SYNC_HOURS` env var (default: 2h)
- **Disable workflow**: Run `/toggle-branch-workflow`

<!-- /BRANCH-WORKFLOW-ENABLED -->
```

### 3. If Currently ENABLED (Disabling)

1. Identify which file contains the marker
2. Remove the entire section between `<!-- BRANCH-WORKFLOW-ENABLED -->` and `<!-- /BRANCH-WORKFLOW-ENABLED -->` (inclusive)
3. If the file becomes empty (or only whitespace), optionally delete it
4. Report success: "Branch workflow DISABLED. Direct commits to main/master allowed."

### 4. Show Summary

After toggling, display:

```
Branch Workflow Status
----------------------
Status: ENABLED / DISABLED
Config file: CLAUDE.md / CLAUDE.local.md / (none)
Current branch: [branch name]
Protected branches: main, master

Hooks active when enabled:
- PreToolUse: Warns on commits to main/master
- PostToolUse: Reminds about PR after pushing feature branch
- UserPromptSubmit: Reminds to sync with main (every 2h by default)
```

## Important Notes

- The toggle is idempotent - running it when already in desired state is safe
- Always preserve other content in CLAUDE.md when editing
- Use Edit tool to remove sections precisely (not Write to overwrite entire file)
- If user has both CLAUDE.md and CLAUDE.local.md with the marker, warn about conflict
