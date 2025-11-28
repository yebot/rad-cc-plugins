---
description: Synchronize all CLAUDE.md files to AGENTS.md files with generic AI agent language
allowed-tools:
  - Bash
  - Glob
  - Task
---

# Sync CLAUDE.md to AGENTS.md

Convert all CLAUDE.md files in the repository to generic AGENTS.md files that work with any AI coding assistant. This command transforms Claude-specific terminology to AI-agnostic language while preserving all technical content and maintaining documentation hierarchy.

## Instructions

1. **Find all CLAUDE.md files in the repository**:

   ```bash
   find . \( -name "CLAUDE.md" -o -name "claude.md" \) -type f | grep -v node_modules | grep -v .git | grep -v dist | grep -v build | sort
   ```

   - Identify all CLAUDE.md files (case variations)
   - Filter out build/dependency directories
   - Sort for organized processing

2. **Prepare for batch conversion**:

   a) **Display found files to user**:
   ```
   Found CLAUDE.md files:
   - ./CLAUDE.md
   - ./src/components/CLAUDE.md
   - ./packages/api/CLAUDE.md
   - ./services/auth/CLAUDE.md

   Total: X files
   ```

   b) **Confirm scope with user** (if many files):
   - If more than 5 files found, show the list
   - Let user know the conversion will begin
   - Note that AGENTS.md files will be created/updated in same directories

3. **Process each CLAUDE.md file using the claude-to-agents-converter agent**:

   a) **For each CLAUDE.md file found**:

   - Use the Task tool to launch the `claude-to-agents-converter` agent
   - Pass the specific file path to convert
   - Wait for conversion to complete
   - Track the result (success/failure)

   b) **Agent invocation format**:
   ```
   Task(
     subagent_type: "claude-to-agents-converter",
     description: "Convert CLAUDE.md to AGENTS.md",
     prompt: "Convert the CLAUDE.md file at [FILE_PATH] to AGENTS.md. Apply all transformation rules to make the documentation AI-agnostic. Report the transformations made."
   )
   ```

   c) **Process files in order** (root first, then nested):
   - Start with root CLAUDE.md (if exists)
   - Then process subdirectory CLAUDE.md files alphabetically
   - This ensures parent-child link consistency

4. **Track conversion results**:

   Keep a running tally:
   ```
   Conversion Progress:
   ✅ ./CLAUDE.md → ./AGENTS.md
   ✅ ./src/components/CLAUDE.md → ./src/components/AGENTS.md
   ✅ ./packages/api/CLAUDE.md → ./packages/api/AGENTS.md
   ⚠️  ./services/auth/CLAUDE.md → (warning: ...)
   ```

5. **Verify conversions**:

   After all conversions complete:

   a) **Count created/updated files**:
   ```bash
   find . \( -name "AGENTS.md" -o -name "agents.md" \) -type f | grep -v node_modules | grep -v .git | wc -l
   ```

   b) **Quick validation check** (optional):
   - Verify AGENTS.md files exist alongside CLAUDE.md files
   - Check file sizes are similar (content preserved)

6. **Report final results**:

   Provide comprehensive summary:

   ```
   📄 CLAUDE.md → AGENTS.md Synchronization Complete!

   Files Processed: X
   ✅ Successfully converted: Y
   ⚠️  Warnings: Z
   ❌ Failed: 0

   Created/Updated AGENTS.md files:
   - ./AGENTS.md (3,245 bytes)
   - ./src/components/AGENTS.md (1,892 bytes)
   - ./packages/api/AGENTS.md (2,456 bytes)
   - ./services/auth/AGENTS.md (1,234 bytes)

   Common transformations applied:
   - "Claude Code" → "AI coding assistants"
   - "Claude" → "AI agent" / "AI assistant"
   - CLAUDE.md links → AGENTS.md links
   - URLs to claude.ai/code removed

   ✅ All CLAUDE.md files now have corresponding AGENTS.md versions!

   Next Steps:
   - Review AGENTS.md files for accuracy
   - Commit both CLAUDE.md and AGENTS.md to version control
   - AGENTS.md files will auto-sync when CLAUDE.md is updated (via hooks)
   ```

7. **Handle edge cases**:

   | Issue | Solution |
   |-------|----------|
   | No CLAUDE.md files found | Report "No CLAUDE.md files found in repository" |
   | Agent conversion fails | Report specific file and error, continue with others |
   | AGENTS.md already exists | Overwrite with new conversion (sync means update) |
   | Nested CLAUDE.md hierarchy | Process root first to ensure link consistency |

## Important Guidelines

### Processing Order

**Why order matters:**
- Parent CLAUDE.md files often reference child CLAUDE.md files
- Converting parent first ensures child references are updated consistently
- Alphabetical processing of subdirectories maintains predictable order

**Recommended order:**
1. `./CLAUDE.md` (root - always first)
2. First-level subdirectories (e.g., `./src/CLAUDE.md`, `./packages/CLAUDE.md`)
3. Deeper nesting (e.g., `./src/components/CLAUDE.md`)

### Transformation Consistency

All files should receive identical transformation rules:
- ✅ Same terminology replacements across all files
- ✅ All CLAUDE.md → AGENTS.md link updates
- ✅ Consistent handling of Claude Code specific features
- ✅ Preservation of technical content in all files

### Agent Delegation

- **Always use the Task tool** to invoke the `claude-to-agents-converter` agent
- **Do NOT attempt manual conversion** - the agent has specialized logic
- **Let the agent handle** each file independently for robustness

### Error Handling

If a conversion fails:
- Report the specific file and error
- Continue processing remaining files
- Include failed files in final summary
- Suggest manual review for failed conversions

## Use Cases

### Initial Setup
First time creating AGENTS.md versions of existing CLAUDE.md files:
```
/sync-agents-md
```

### After Bulk CLAUDE.md Updates
Multiple CLAUDE.md files were updated, need to sync all:
```
/sync-agents-md
```

### Recovery
AGENTS.md files got out of sync or were deleted:
```
/sync-agents-md
```

### Verification
Check that all CLAUDE.md files have corresponding AGENTS.md:
```
/sync-agents-md
```

## Best Practices

1. **Run after major CLAUDE.md changes**: If you've restructured or significantly updated CLAUDE.md files

2. **Commit both versions**: Always commit both CLAUDE.md and AGENTS.md to version control together

3. **Review first conversion**: On initial setup, review the generated AGENTS.md files to ensure quality

4. **Use hooks for maintenance**: After initial setup, the hooks will keep files in sync automatically

5. **Periodic sync**: Run occasionally to catch any files that might have been missed

## Example Scenarios

### Scenario 1: New Repository Setup

```
User has been using CLAUDE.md files, wants to add AGENTS.md versions.

1. Run: /sync-agents-md
2. Review generated AGENTS.md files
3. Commit all AGENTS.md files
4. Hooks will maintain sync going forward
```

### Scenario 2: Monorepo with Multiple CLAUDE.md Files

```
Monorepo with CLAUDE.md in:
- ./CLAUDE.md (root)
- ./packages/web/CLAUDE.md
- ./packages/api/CLAUDE.md
- ./packages/shared/CLAUDE.md

1. Run: /sync-agents-md
2. Agent processes all 4 files
3. Creates 4 corresponding AGENTS.md files
4. All child references updated consistently
```

### Scenario 3: AGENTS.md Out of Sync

```
User updated CLAUDE.md files manually, AGENTS.md is outdated.

1. Run: /sync-agents-md
2. All AGENTS.md files overwritten with fresh conversions
3. Sync restored
```

## Definition of Done

- [ ] All CLAUDE.md files found in repository
- [ ] Each CLAUDE.md file processed by claude-to-agents-converter agent
- [ ] Conversions completed in correct order (root first)
- [ ] All successful conversions tracked
- [ ] Any failures or warnings noted
- [ ] AGENTS.md files verified to exist
- [ ] Comprehensive summary report provided
- [ ] User informed of next steps
- [ ] Total file counts match expectations
- [ ] No CLAUDE.md files left without corresponding AGENTS.md
