# Branch Workflow Templates

This skill provides templates for branch-based workflow instructions that get added to CLAUDE.md.

## Standard Mode Template

Use this template when the user chooses **Standard** workflow mode:

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
   git checkout main
   git pull origin main
   git checkout -b feat/your-feature-name
   ```

2. **Make commits**: Commit to your feature branch
   ```bash
   git add .
   git commit -m "feat: description of change"
   ```

3. **Stay in sync**: Periodically rebase on main (hooks will remind you)
   ```bash
   git fetch origin
   git rebase origin/main
   ```

4. **Push and create PR**: When ready for review
   ```bash
   git push -u origin feat/your-feature-name
   gh pr create --title "feat: your feature" --body "Description..."
   ```

5. **After merge**: Clean up local branch
   ```bash
   git checkout main
   git pull origin main
   git branch -d feat/your-feature-name
   ```

### Task Tracker Integration

When working on tracked tasks:
- Reference task IDs in branch names: `feat/TASK-123-add-feature`
- Include task references in commit messages: `feat: add feature [TASK-123]`
- Link PRs to tasks in the PR description
- Update task status when PR is merged

### Configuration

- **Sync reminder threshold**: Set `BRANCH_SYNC_HOURS` env var (default: 2 hours)
- **Disable workflow**: Run `/toggle-branch-workflow` to turn off

<!-- /BRANCH-WORKFLOW-ENABLED -->
```

---

## Worktree Mode Template

Use this template when the user chooses **Worktree** workflow mode:

```markdown
<!-- BRANCH-WORKFLOW-ENABLED -->
<!-- WORKTREE-MODE -->
## Branch-Based Workflow (Worktree Mode)

This project uses a worktree-based development workflow. Each feature gets its own directory, allowing parallel development without branch switching.

### Branch Strategy

- **Protected branches**: `main`, `master` - never commit directly
- **Feature branches**: Create via worktrees from main
- **Branch naming**: Use prefixes like `feat/`, `fix/`, `refactor/`, `docs/`

### Worktree Workflow

1. **Start new work**: Create a worktree for the feature
   ```bash
   # From main repo directory
   git fetch origin
   git worktree add ../$(basename $PWD)-feat-name -b feat/feature-name origin/main
   cd ../$(basename $PWD)-feat-name
   ```

2. **Make commits**: Work in the worktree directory
   ```bash
   git add .
   git commit -m "feat: description of change"
   ```

3. **Stay in sync**: Periodically rebase on main (hooks will remind you)
   ```bash
   git fetch origin
   git rebase origin/main
   ```

4. **Push and create PR**: When ready for review
   ```bash
   git push -u origin feat/feature-name
   gh pr create --title "feat: your feature" --body "Description..."
   ```

5. **After merge**: Clean up worktree and branch
   ```bash
   cd /path/to/main/repo
   git worktree remove ../$(basename $PWD)-feat-name
   git branch -d feat/feature-name
   git pull origin main
   ```

### Worktree Management

```bash
# List all worktrees
git worktree list

# Create worktree for existing remote branch (e.g., PR review)
git worktree add ../project-review origin/feat/some-branch

# Remove worktree when done
git worktree remove ../project-review

# Prune stale worktree references
git worktree prune
```

### Directory Structure

Keep worktrees alongside the main repo:
```
~/projects/
├── myproject/              <- main branch (primary repo)
├── myproject-feat-auth/    <- feature worktree
├── myproject-fix-bug/      <- bugfix worktree
└── myproject-review/       <- PR review worktree
```

### Task Tracker Integration

When working on tracked tasks:
- Reference task IDs in branch names: `feat/TASK-123-add-feature`
- Include task references in commit messages: `feat: add feature [TASK-123]`
- Link PRs to tasks in the PR description
- Update task status when PR is merged

### Configuration

- **Sync reminder threshold**: Set `BRANCH_SYNC_HOURS` env var (default: 2 hours)
- **Disable workflow**: Run `/toggle-branch-workflow` to turn off

<!-- /BRANCH-WORKFLOW-ENABLED -->
```

---

## Mode Comparison

| Feature | Standard | Worktree |
|---------|----------|----------|
| Branch switching | `git checkout` | Separate directories |
| Parallel work | One branch at a time | Multiple branches simultaneously |
| Context switching | Must stash/commit | Just `cd` to other directory |
| Disk usage | Single copy | Copy per worktree |
| Best for | Solo devs, linear work | Teams, PR reviews, parallel features |
