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

### Worktrees (Optional)

For working on multiple branches simultaneously, consider git worktrees:
```bash
# Create a worktree for a feature
git worktree add ../project-feat-branch feat/your-feature

# List active worktrees
git worktree list

# Remove when done
git worktree remove ../project-feat-branch
```

See `docs/worktree-patterns.md` in the git-github-operations plugin for more patterns.

### Configuration

- **Sync reminder threshold**: Set `BRANCH_SYNC_HOURS` env var (default: 2 hours)
- **Disable workflow**: Run `/toggle-branch-workflow` to turn off

<!-- /BRANCH-WORKFLOW-ENABLED -->
