---
description: Run a session retrospective to capture learnings and generate improvement suggestions. Use at the end of work sessions or periodically during long sessions.
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
  - AskUserQuestion
---

# Reflect - Session Retrospective

Capture learnings from your work session and generate improvement suggestions for CLAUDE.md, agents, skills, and documentation.

## Instructions

### Phase 1: Initialize

1. **Ensure storage directory exists:**
   ```bash
   python3 plugins/learning-loop/helpers/learning_helpers.py init
   ```

2. **Check for existing pending suggestions:**
   ```bash
   PENDING=$(python3 plugins/learning-loop/helpers/learning_helpers.py pending-count)
   ```

   If pending > 0, inform the user:
   ```
   Note: You have {PENDING} pending suggestions from previous sessions.
   Run /review-suggestions to apply them, or continue to add more.
   ```

### Phase 2: Gather Learnings

3. **Extract learnings from git history:**
   ```bash
   # Recent commits
   git log --oneline -15 --since="3 hours ago"

   # Get commit-based learnings
   python3 plugins/learning-loop/helpers/learning_helpers.py extract-commits --since="3 hours ago"

   # Get diff-based learnings (iterations, TODOs, new deps)
   python3 plugins/learning-loop/helpers/learning_helpers.py extract-diff --base="HEAD~10"
   ```

4. **Check for backlog/simbl task notes (if present):**
   ```bash
   # backlog-md
   if [ -d "backlog/tasks" ]; then
     find backlog/tasks -name "*.md" -mmin -180 -exec grep -l "notes:" {} \;
   fi

   # simbl
   if [ -f ".simbl/tasks.md" ]; then
     grep -A5 "## Notes" .simbl/tasks.md 2>/dev/null | head -20
   fi
   ```

5. **Compile auto-detected learnings:**

   Present findings to user:
   ```markdown
   ## Session Reflection

   ### Auto-Detected Learnings

   Based on your recent work, I found:

   **From Git Commits:**
   - [List commit-extracted learnings]

   **From Code Changes:**
   - [List diff-extracted learnings]

   **From Task Notes:** (if applicable)
   - [List task note learnings]
   ```

### Phase 3: User Input

6. **Ask for additional learnings:**

   Use AskUserQuestion or prompt the user:
   ```
   What else did you discover or learn during this session?

   Consider:
   - Caveats or gotchas you encountered
   - Patterns or conventions you established
   - Errors you resolved (and how)
   - Dependencies you added or updated
   - Useful commands you used

   Enter learnings (one per line), or press Enter to continue with auto-detected items:
   ```

7. **Allow user to review/edit auto-detected learnings:**
   ```
   Review the learnings above. Would you like to:
   - [A] Accept all and continue
   - [E] Edit/remove some before continuing
   - [C] Cancel reflection
   ```

### Phase 4: Categorize and Target

8. **Categorize each learning:**

   For each learning, determine category using the helper:
   ```bash
   python3 plugins/learning-loop/helpers/learning_helpers.py categorize "learning text here"
   ```

   Categories:
   - `caveat` - Gotcha, workaround, required setup
   - `pattern` - Convention, best practice
   - `error_fix` - Solution to error or bug
   - `dependency` - Tool, library, version
   - `command` - Useful shell command
   - `architecture` - Design decision, structure

9. **Find target files for each learning:**
   ```bash
   python3 plugins/learning-loop/helpers/learning_helpers.py find-targets \
     --category "caveat" \
     --content "learning text here"
   ```

### Phase 5: Generate Suggestions

10. **Create suggestions for each learning:**

    For each learning with a valid target:
    ```bash
    python3 plugins/learning-loop/helpers/learning_helpers.py add-suggestion \
      --category "caveat" \
      --content "Must restart server after config changes" \
      --target "CLAUDE.md" \
      --confidence 0.85
    ```

11. **Generate diff previews:**

    For each suggestion, read the target file and determine:
    - Which section to add to (or create)
    - The exact text to add
    - A diff-style preview showing the change

### Phase 6: Report

12. **Present summary to user:**
    ```markdown
    ## Reflection Complete

    **Session:** {date/time}
    **Learnings captured:** {count}
    **Suggestions generated:** {count}

    ### Summary by Priority

    **High Priority ({count}):**
    1. Add caveat about X to CLAUDE.md
    2. Add error fix for Y to CLAUDE.md

    **Medium Priority ({count}):**
    3. Add pattern for Z to CLAUDE.md
    4. Update dependency notes

    **Low Priority ({count}):**
    5. Add command reference

    ### Next Steps

    To review and apply suggestions:
    ```
    /review-suggestions
    ```

    To apply only high-priority suggestions:
    ```
    /review-suggestions --priority high
    ```
    ```

## Definition of Done

- [ ] Storage initialized (.learning-loop/ directory exists)
- [ ] Git history analyzed for learnings
- [ ] Diff analyzed for iterations, TODOs, dependencies
- [ ] Task notes checked (if backlog-md/simbl present)
- [ ] User prompted for additional learnings
- [ ] All learnings categorized
- [ ] Target files identified for each learning
- [ ] Suggestions created with diff previews
- [ ] Suggestions saved to pending-suggestions.json
- [ ] Summary presented to user with next steps

## Error Handling

| Issue | Resolution |
|-------|------------|
| Not a git repository | Skip git extraction, rely on user input |
| No CLAUDE.md found | Suggest creating one, or use README.md |
| Helper script not found | Check plugin installation path |
| No learnings detected | Prompt user for manual input |

## Example Session

```
$ /reflect

## Session Reflection

### Auto-Detected Learnings

**From Git Commits (3):**
- fix: resolve OAuth token refresh issue
- feat: add rate limiting to API endpoints
- chore: update eslint to v9

**From Code Changes (2):**
- Multiple iterations on: src/auth/token.ts (4 changes)
- TODO: Add retry logic for network failures

### Your Input

What else did you discover during this session?
> The OAuth provider requires tokens to be refreshed 5 minutes before expiry, not at expiry
> Always run `npm run build` before `npm test` - tests use compiled output

### Categorization

1. [caveat] OAuth tokens need refresh 5 min before expiry (confidence: 0.9)
2. [command] Run build before test (confidence: 0.85)
3. [error_fix] OAuth token refresh issue resolved (confidence: 0.8)
4. [pattern] Rate limiting pattern for APIs (confidence: 0.7)
5. [dependency] ESLint v9 update (confidence: 0.75)

## Reflection Complete

**Learnings captured:** 5
**Suggestions generated:** 5

### Summary by Priority

**High Priority (2):**
1. Add caveat about OAuth token refresh timing → CLAUDE.md
2. Add error fix for token refresh → CLAUDE.md

**Medium Priority (2):**
3. Add rate limiting pattern → CLAUDE.md
4. Update ESLint dependency note → CLAUDE.md

**Low Priority (1):**
5. Add build-before-test command → CLAUDE.md

To review and apply: /review-suggestions
```
