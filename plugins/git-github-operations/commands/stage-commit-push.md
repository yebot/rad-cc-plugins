# Stage, Commit, and Push

You are helping the user perform a complete git workflow: staging changes, creating a commit, and pushing to the remote repository.

## Instructions

### 0. Check Branch Workflow Status

Before proceeding, check if branch-based workflow is enabled:

```bash
grep -q "BRANCH-WORKFLOW-ENABLED" CLAUDE.md 2>/dev/null || grep -q "BRANCH-WORKFLOW-ENABLED" CLAUDE.local.md 2>/dev/null
```

If enabled **AND** currently on `main` or `master`:
- Inform the user: "Branch workflow is enabled. You're on [main/master]."
- Ask: "Would you like to create a feature branch first?"
- If yes, suggest a branch name based on the changes and run:
  ```bash
  git checkout -b feat/suggested-name
  ```
- If no, proceed but note the workflow deviation

1. **Check git status**: Run `git status` to see what changes exist
2. **Stage changes**:
   - Ask the user which files to stage, or if they want to stage all changes
   - Use `git add` to stage the selected files
3. **Create commit**:
   - Review the staged changes with `git diff --cached`
   - Ask the user for a commit message, or draft one based on the changes
   - Create the commit with `git commit -m "message"`
4. **Push changes**:
   - Check the current branch with `git branch --show-current`
   - Push to the remote with `git push` (or `git push -u origin <branch>` if not tracking)
   - Confirm the push was successful
5. **Check for GitHub Actions**:
   - After a successful push, check for workflow files that may trigger
   - Provide a direct link to the Actions page if workflows exist

## GitHub Actions Awareness

After pushing, check if the repository has GitHub Actions workflows that will be triggered:

1. **Check for workflow files**:
   ```bash
   ls .github/workflows/*.yml .github/workflows/*.yaml 2>/dev/null
   ```

2. **If workflows exist**, examine them to identify:
   - Which workflows trigger on `push` to the current branch
   - Which workflows trigger on `pull_request` events
   - Any workflows with `workflow_dispatch` (manual triggers)

3. **Provide a direct link to the running action**:
   - Extract the repository owner and name from the remote URL:
     ```bash
     git remote get-url origin | sed -E 's|.*github\.com[:/]([^/]+)/([^/.]+)(\.git)?|\1/\2|'
     ```
   - Generate the Actions URL: `https://github.com/{owner}/{repo}/actions`
   - For the specific workflow run, provide: `https://github.com/{owner}/{repo}/actions/workflows/{workflow-file}`

4. **Example output after push**:
   ```
   Push successful!

   GitHub Actions triggered:
   - ci.yml (runs on push to main)
   - deploy.yml (runs on push to main)

   View running workflows: https://github.com/owner/repo/actions
   ```

## Important Notes and Guidelines

- Always verify what branch you're on before pushing
- Each commit should represent a single logical change
- If there are many small changes, group them into 2-4 meaningful commits
- Always show the user what changes will be committed before creating the commit
- If there are no changes to commit, inform the user
- Commit messages should be concise but descriptive (1-2 lines)
- If there are merge conflicts or issues, report them to the user
- If the push fails (e.g., diverged branches), explain the issue and suggest solutions
- Be careful with force pushes - only suggest if explicitly requested and after warning
- If no GitHub Actions workflows exist, simply skip the Actions notification
