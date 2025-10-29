# Stage, Commit, and Push

You are helping the user perform a complete git workflow: staging changes, creating a commit, and pushing to the remote repository.

## Instructions

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
