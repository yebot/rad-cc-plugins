# Git Worktree Patterns

Git worktrees allow you to have multiple branches checked out simultaneously in separate directories. This is useful for parallel development without stashing or switching branches.

## When to Use Worktrees

- Working on multiple features in parallel
- Code review while continuing development
- Testing changes without stashing current work
- Long-running feature branches that need periodic rebasing
- Comparing implementations across branches

## Common Patterns

### Pattern 1: Feature Development

```bash
# Main repo stays on main
cd ~/projects/myproject

# Create worktree for feature
git worktree add ../myproject-feature feat/new-feature

# Work in the worktree
cd ../myproject-feature
# ... make changes, commit, push ...

# Clean up when done
cd ~/projects/myproject
git worktree remove ../myproject-feature
```

### Pattern 2: Parallel Features

```bash
# Structure:
# ~/projects/myproject/          <- main branch
# ~/projects/myproject-feat-a/   <- feature A
# ~/projects/myproject-feat-b/   <- feature B

git worktree add ../myproject-feat-a feat/feature-a
git worktree add ../myproject-feat-b feat/feature-b

# Work on either independently
cd ../myproject-feat-a  # work on feature A
cd ../myproject-feat-b  # work on feature B
```

### Pattern 3: Code Review

```bash
# Create worktree for PR review
git fetch origin
git worktree add ../myproject-review origin/feat/pr-branch

# Review the code
cd ../myproject-review
# ... examine, test, provide feedback ...

# Clean up
cd ~/projects/myproject
git worktree remove ../myproject-review
```

### Pattern 4: Hotfix While Developing

```bash
# Currently working on feature branch
# Need to fix urgent bug on main

# Create worktree for hotfix (without disturbing current work)
git worktree add ../myproject-hotfix -b hotfix/urgent-fix main

# Fix the bug
cd ../myproject-hotfix
# ... make fix, commit, push, create PR ...

# Return to feature work
cd ~/projects/myproject

# Clean up after hotfix merged
git worktree remove ../myproject-hotfix
```

## Best Practices

1. **Naming convention**: Use `{project}-{branch-type}` for worktree directories
2. **Location**: Keep worktrees at the same level as main repo, not inside it
3. **Cleanup**: Remove worktrees when done to avoid confusion
4. **Dependencies**: Each worktree may need its own `node_modules`, `.venv`, etc.
5. **IDE support**: Most IDEs handle worktrees well - open each as a separate project

## Useful Commands

```bash
# List all worktrees
git worktree list

# Add worktree for existing branch
git worktree add ../path branch-name

# Add worktree with new branch
git worktree add ../path -b new-branch base-branch

# Remove worktree
git worktree remove ../path

# Prune stale worktree info (after manual deletion)
git worktree prune
```

## Limitations

- Cannot have two worktrees on the same branch
- Worktrees share the same `.git` directory (and thus refs, stash, etc.)
- Must be careful with `git clean` and similar commands
- Some git operations affect all worktrees (e.g., `git gc`)
