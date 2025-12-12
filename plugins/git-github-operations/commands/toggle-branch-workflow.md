---
description: Toggle branch-based workflow enforcement on/off - adds/removes instructions from CLAUDE.md
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Skill
  - AskUserQuestion
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

Also check if worktree mode is enabled:
```bash
grep -l "WORKTREE-MODE" CLAUDE.md CLAUDE.local.md 2>/dev/null
```

### 2. If Currently DISABLED (Enabling)

Ask the user TWO questions using AskUserQuestion:

**Question 1 - Location:**
- `CLAUDE.md` - Shared with team, committed to repo
- `CLAUDE.local.md` - Personal, gitignored, not shared

**Question 2 - Workflow Mode:**
- `Standard` - Traditional branch workflow (checkout between branches)
- `Worktree` - Each feature gets its own directory (parallel development)

Then:

1. **Load the skill**: Use `Skill("git-github-operations:branch-workflow")` to get the templates
2. **Read the target file** using the Read tool (if it exists)
3. **Select the appropriate template** from the skill:
   - Standard mode: Use the "Standard Mode Template" section
   - Worktree mode: Use the "Worktree Mode Template" section
4. **Append the template** to the file content:
   - If file exists: Use the Edit tool with `old_string` as the last line(s) of the file, and `new_string` as those lines plus the template
   - If file doesn't exist: Use the Write tool to create it with the template
5. Report success with the mode enabled

### Templates

Templates are defined in the `branch-workflow` skill. Use `Skill("git-github-operations:branch-workflow")` to access them.

**Standard Mode**:
- Traditional `git checkout -b` workflow
- Switch between branches in same directory
- Good for: Solo developers, simple projects, linear workflows

**Worktree Mode**:
- Each feature branch in separate directory
- Parallel development without context switching
- Good for: Multiple features, PR reviews while developing, team workflows

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
Mode: Standard / Worktree (if enabled)
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
- Worktree mode includes `<!-- WORKTREE-MODE -->` marker for detection
