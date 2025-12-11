---
description: Synchronize all CLAUDE.md files to AGENTS.md files with generic AI agent language
allowed-tools:
  - Bash
  - Glob
  - Task
---

# Sync CLAUDE.md to AGENTS.md

Convert all CLAUDE.md files in the repository to generic AGENTS.md files that work with any AI coding assistant. This command transforms Claude-specific terminology to AI-agnostic language while preserving all technical content, import syntax, and documentation hierarchy.

## What Gets Converted

| Source File | Target File | Convert? |
|-------------|-------------|----------|
| `./CLAUDE.md` | `./AGENTS.md` | ✅ Yes |
| `./.claude/CLAUDE.md` | `./.claude/AGENTS.md` | ✅ Yes |
| `./CLAUDE.local.md` | `./AGENTS.local.md` | ✅ Yes |
| `./.claude/rules/*.md` | N/A | ❌ Skip (implementation-specific) |
| `~/.claude/*` | N/A | ❌ Never (user's personal files) |

**Note:** `.claude/rules/` files are Claude Code-specific configuration and don't need AI-agnostic versions.

## Instructions

### Phase 1: Discover Memory Files

1. **Find all CLAUDE.md and CLAUDE.local.md files**:

   ```bash
   find . \( -name "CLAUDE.md" -o -name "claude.md" -o -name "CLAUDE.local.md" \) -type f | grep -v node_modules | grep -v .git | grep -v dist | grep -v build | grep -v ".claude/rules" | sort
   ```

   **Exclude:**
   - Build/dependency directories
   - `.claude/rules/` files (Claude Code-specific)
   - User memory (`~/.claude/`) - never touch

2. **Display found files**:

   ```
   Found memory files to convert:

   CLAUDE.md files:
   - ./CLAUDE.md
   - ./src/components/CLAUDE.md
   - ./packages/api/CLAUDE.md

   CLAUDE.local.md files:
   - ./CLAUDE.local.md

   Total: X files

   Skipped (not converted):
   - ./.claude/rules/*.md (Claude Code-specific rules)
   ```

### Phase 2: Process Each File

3. **Process files using claude-to-agents-converter agent**:

   **Processing order** (important for link consistency):
   1. Root `./CLAUDE.md` first
   2. Root `./CLAUDE.local.md`
   3. First-level subdirectory CLAUDE.md files
   4. Deeper nested files

   **Agent invocation**:
   ```
   Task(
     subagent_type: "claude-to-agents-converter",
     description: "Convert CLAUDE.md to AGENTS.md",
     prompt: "Convert the file at [FILE_PATH] to its AGENTS.md equivalent. Apply all transformation rules including import syntax (@CLAUDE.md → @AGENTS.md). Report transformations made."
   )
   ```

4. **Track conversion results**:

   ```
   Conversion Progress:
   ✅ ./CLAUDE.md → ./AGENTS.md
   ✅ ./CLAUDE.local.md → ./AGENTS.local.md
   ✅ ./src/components/CLAUDE.md → ./src/components/AGENTS.md
   ⚠️  ./packages/api/CLAUDE.md → (warning: no Claude-specific content found)
   ```

### Phase 3: Transform Import References

5. **Key transformations** (handled by agent):

   | Claude-Specific | Generic |
   |-----------------|---------|
   | `@CLAUDE.md` | `@AGENTS.md` |
   | `@path/to/CLAUDE.md` | `@path/to/AGENTS.md` |
   | `@CLAUDE.local.md` | `@AGENTS.local.md` |
   | `@~/.claude/file.md` | `@~/.ai-agent/file.md` |
   | `.claude/rules/` references | Keep as-is (Claude-specific) |

   **Import syntax transformation examples:**

   Before (CLAUDE.md):
   ```markdown
   See @README.md for overview.
   Child context: @src/components/CLAUDE.md
   Personal prefs: @~/.claude/my-prefs.md
   ```

   After (AGENTS.md):
   ```markdown
   See @README.md for overview.
   Child context: @src/components/AGENTS.md
   Personal prefs: @~/.ai-agent/my-prefs.md
   ```

### Phase 4: Verify and Report

6. **Verify conversions**:

   ```bash
   # Count AGENTS.md files created
   find . \( -name "AGENTS.md" -o -name "AGENTS.local.md" \) -type f | grep -v node_modules | wc -l
   ```

7. **Final report**:

   ```
   📄 CLAUDE.md → AGENTS.md Synchronization Complete!

   Files Processed: X
   ✅ Successfully converted: Y
   ⚠️  Warnings: Z
   ❌ Failed: 0

   Created/Updated files:
   - ./AGENTS.md (3,245 bytes)
   - ./AGENTS.local.md (892 bytes)
   - ./src/components/AGENTS.md (1,892 bytes)
   - ./packages/api/AGENTS.md (2,456 bytes)

   Transformations applied:
   - "Claude Code" → "AI coding assistants"
   - "Claude" → "AI agent" / "AI assistant"
   - @CLAUDE.md imports → @AGENTS.md imports
   - @CLAUDE.local.md → @AGENTS.local.md
   - URLs to claude.ai/code removed
   - /memory command → "memory management command"

   Skipped files:
   - ./.claude/rules/*.md (Claude Code-specific, no conversion needed)

   ✅ All memory files now have AI-agnostic versions!

   Next Steps:
   - Review AGENTS.md files for accuracy
   - Commit both CLAUDE.md and AGENTS.md versions
   - Hooks will auto-sync when CLAUDE.md files are updated
   ```

## Special Handling

### CLAUDE.local.md Files

- Convert to `AGENTS.local.md`
- Preserve gitignore status (both are personal files)
- Transform any CLAUDE-specific references

### Path-Specific Rules References

If a CLAUDE.md references `.claude/rules/` files:

```markdown
# In CLAUDE.md
See @.claude/rules/testing.md for test conventions.
```

Keep these references as-is in AGENTS.md (they're Claude Code-specific configuration):

```markdown
# In AGENTS.md
See @.claude/rules/testing.md for test conventions.
```

### Import Syntax with paths: Frontmatter

If CLAUDE.md has path-specific rule references, preserve the frontmatter:

```markdown
---
paths: src/api/**/*.ts
---
```

This frontmatter is kept in AGENTS.md (generic functionality).

## Error Handling

| Issue | Solution |
|-------|----------|
| No CLAUDE.md files found | Report "No CLAUDE.md files found" |
| Agent conversion fails | Report error, continue with other files |
| AGENTS.md already exists | Overwrite (sync means update) |
| .claude/rules/ files found | Skip with note (Claude Code-specific) |
| User memory referenced | Transform path, don't access |

## Processing Order

**Why order matters:**
- Parent CLAUDE.md files reference child CLAUDE.md files
- Converting parent first ensures @CLAUDE.md → @AGENTS.md transformations are consistent
- Alphabetical subdirectory processing maintains predictability

**Order:**
1. `./CLAUDE.md` (root)
2. `./CLAUDE.local.md` (root local)
3. `./.claude/CLAUDE.md` (if exists)
4. First-level subdirectories alphabetically
5. Deeper nesting levels

## Best Practices

1. **Run after major CLAUDE.md changes**: Especially if you've restructured or added new files

2. **Commit both versions**: Always commit CLAUDE.md and AGENTS.md together

3. **Review first conversion**: Check generated AGENTS.md files for quality

4. **Use hooks for maintenance**: After initial setup, hooks auto-sync on CLAUDE.md updates

5. **Skip rules/ intentionally**: `.claude/rules/` are Claude Code-specific and don't need generic versions

## Definition of Done

- [ ] All CLAUDE.md files found (excluding rules/)
- [ ] All CLAUDE.local.md files found
- [ ] Each file processed by claude-to-agents-converter agent
- [ ] Import syntax transformed (@CLAUDE.md → @AGENTS.md)
- [ ] Conversions completed in correct order
- [ ] Results tracked (success/warning/failure)
- [ ] AGENTS.md and AGENTS.local.md files verified
- [ ] Skipped files noted (rules/)
- [ ] Summary report provided
- [ ] Next steps communicated
