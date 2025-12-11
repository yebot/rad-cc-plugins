---
description: Link documentation files to Claude Code memory using import syntax (@path) for better context availability
allowed-tools:
  - Bash
  - Glob
  - Grep
  - Read
  - Edit
---

# Link Documentation to Claude Code Memory

Ensure all documentation files in the repository are properly referenced in Claude Code memory files using the modern import syntax (`@path/to/file`).

## Claude Code Import Syntax

Claude Code supports importing files with `@path/to/file` syntax:

```markdown
# In CLAUDE.md
See @README.md for project overview.
Architecture details: @docs/architecture.md
API reference: @docs/api/README.md
```

**Benefits over markdown links:**
- Claude Code loads imported content automatically
- Keeps memory files focused
- Recursive imports supported (max 5 levels)
- Works with relative, absolute, and home directory paths (`@~/...`)

## Instructions

### Phase 1: Discover Memory Files

1. **Find all Claude Code memory files**:

   ```bash
   # Find all memory files
   find . \( -name "CLAUDE.md" -o -name "CLAUDE.local.md" \) 2>/dev/null | grep -v node_modules | grep -v .git

   # Find rules files
   find . -path "*/.claude/rules/*.md" 2>/dev/null | grep -v node_modules

   # Check for .claude directory
   ls -la .claude/ 2>/dev/null
   ls -la .claude/rules/ 2>/dev/null
   ```

2. **Categorize memory files**:

   | Type | Files | Can Modify |
   |------|-------|------------|
   | Project memory | `./CLAUDE.md`, `./.claude/CLAUDE.md` | Yes |
   | Project rules | `./.claude/rules/*.md` | Yes (carefully) |
   | Project local | `./CLAUDE.local.md` | Ask first (personal) |
   | User memory | `~/.claude/*` | Never modify |

   **Important**: Never modify `~/.claude/CLAUDE.md` or `~/.claude/rules/` - those are user's personal files.

### Phase 2: Inventory Documentation Files

3. **Find all markdown documentation**:

   Use Glob to find documentation files:
   ```
   pattern: "**/*.md"
   ```

   **Include:**
   - `docs/**/*.md`
   - `documentation/**/*.md`
   - Architecture documents
   - API documentation
   - How-to guides
   - Technical specifications

   **Exclude:**
   - `node_modules/`, `.git/`, vendor directories
   - Memory files (CLAUDE.md, CLAUDE.local.md)
   - `README.md` at root (usually primary doc)
   - `CHANGELOG.md`, `LICENSE.md`
   - `.claude/rules/*.md` (these ARE memory, not docs to import)
   - Generated/build output files

4. **For each documentation file**:

   a) Read first 20-50 lines to understand purpose
   b) Check if already imported in any memory file:
      ```bash
      grep -r "@path/to/doc.md" . --include="CLAUDE.md" --include="*.md" -l | grep -v node_modules
      ```
   c) Mark unreferenced files for addition

### Phase 3: Add Import References

5. **Determine best memory file for each doc**:

   | Documentation Type | Best Memory Target |
   |-------------------|-------------------|
   | Repository-wide docs | Root `./CLAUDE.md` |
   | API documentation | `./CLAUDE.md` or `.claude/rules/api.md` |
   | Testing guides | `.claude/rules/testing.md` if exists, else `./CLAUDE.md` |
   | Component-specific | Subdirectory `CLAUDE.md` if exists |
   | Setup/config docs | `./CLAUDE.md` |

6. **Add imports using `@path` syntax**:

   a) Read target memory file to understand structure

   b) Find or create documentation section:
      ```markdown
      ## Documentation References

      Project documentation (automatically imported):
      ```

   c) Add imports with context:
      ```markdown
      ## Documentation References

      Architecture and design: @docs/architecture.md
      API specification: @docs/api/openapi.md
      Database schema: @docs/database/schema.md
      Testing guide: @docs/testing.md
      ```

   **Guidelines:**
   - Use `@relative/path` format (not markdown links)
   - Add brief context before or after the import
   - Group related imports together
   - One import per line for clarity

7. **Import format examples**:

   **Simple imports:**
   ```markdown
   See @docs/setup.md for local development setup.
   API reference: @docs/api/README.md
   ```

   **Grouped imports:**
   ```markdown
   ## Architecture Documentation

   System overview: @docs/architecture/overview.md
   Database design: @docs/architecture/database.md
   API design: @docs/architecture/api.md
   ```

   **Inline context:**
   ```markdown
   For authentication details, see @docs/auth/README.md which covers OAuth2 flows and JWT handling.
   ```

### Phase 4: Optimize Hierarchy

8. **Move imports to appropriate level**:

   If root CLAUDE.md imports docs that belong to a subdirectory:

   **Before:**
   ```markdown
   # Root CLAUDE.md
   Component guide: @src/components/auth/guide.md
   ```

   **After (if src/components/auth/CLAUDE.md exists):**
   ```markdown
   # Root CLAUDE.md
   # (removed - now in subdirectory CLAUDE.md)

   # src/components/auth/CLAUDE.md
   Component guide: @./guide.md
   ```

   **Decision criteria for relocation:**
   - Doc is within subdirectory that has its own CLAUDE.md
   - Doc is specific to that subdirectory's domain
   - Moving provides better locality

   **Keep in parent if:**
   - Doc covers cross-cutting concerns
   - Doc spans multiple subdirectories
   - It's an overview/architecture document

9. **Link child CLAUDE.md files**:

   In parent CLAUDE.md, add navigation to child memory files:

   ```markdown
   ## Subdirectory Context

   Additional context for specific areas:
   - @src/components/CLAUDE.md - UI component patterns
   - @packages/api/CLAUDE.md - Backend API service
   - @services/auth/CLAUDE.md - Authentication service
   ```

   **Note:** Use `@path` syntax for child CLAUDE.md links too.

### Phase 5: Handle Special Cases

10. **Rules files (`.claude/rules/`)**:

    Rules files are memory, not documentation to import. However, you CAN:
    - Add imports TO rules files (docs relevant to that topic)
    - Reference rules files from CLAUDE.md using `@.claude/rules/topic.md`

    Example in `.claude/rules/testing.md`:
    ```markdown
    ---
    paths: **/*.test.ts
    ---

    # Testing Rules

    See @docs/testing/patterns.md for detailed examples.

    ## Conventions
    - Use describe/it blocks
    - Mock external services
    ```

11. **CLAUDE.local.md**:

    This is the user's personal file. Before modifying:
    - Ask user permission
    - Only add personal/local references
    - Don't add team documentation here

12. **Large documentation sets**:

    For projects with many docs, use hierarchical imports:

    ```markdown
    # In CLAUDE.md
    ## Documentation

    All documentation is in the docs/ directory:
    - Overview: @docs/README.md (imports other docs)

    # In docs/README.md
    ## Documentation Index

    Architecture: @./architecture/README.md
    API: @./api/README.md
    Guides: @./guides/README.md
    ```

### Phase 6: Report Results

13. **Provide summary**:

    ```
    📚 Documentation Linking Complete!

    Memory files found:
    - Project: ./CLAUDE.md, ./.claude/CLAUDE.md
    - Rules: ./.claude/rules/*.md (3 files)
    - Local: ./CLAUDE.local.md (not modified)

    Documentation files:
    - Total found: 24
    - Already imported: 8
    - Newly imported: 12
    - Skipped (non-doc): 4

    Imports added:
    - ./CLAUDE.md: +8 imports
      - @docs/architecture.md
      - @docs/api/README.md
      ...
    - ./.claude/rules/testing.md: +2 imports
      - @docs/testing/patterns.md
      - @docs/testing/mocking.md

    Child CLAUDE.md links added:
    - @src/components/CLAUDE.md → ./CLAUDE.md
    - @packages/api/CLAUDE.md → ./CLAUDE.md

    References relocated:
    - @src/auth/guide.md: CLAUDE.md → src/auth/CLAUDE.md
    ```

14. **Suggest next steps**:
    - Review added imports for accuracy
    - Run `/memory` to see loaded files
    - Consider creating `.claude/rules/` if topic-specific patterns exist
    - Run periodically to catch new documentation

## Import Syntax Reference

| Syntax | Description |
|--------|-------------|
| `@docs/file.md` | Relative to current file |
| `@./file.md` | Explicitly relative |
| `@../other/file.md` | Parent directory |
| `@~/path/file.md` | User home directory |
| `@/absolute/path.md` | Absolute path |

**Not evaluated inside:**
- Code blocks (` ``` `)
- Inline code (`` ` ``)

## What to Import vs Link

| Content | Use Import (`@path`) | Use Markdown Link |
|---------|---------------------|-------------------|
| Technical docs | ✅ Yes | No |
| API specs | ✅ Yes | No |
| Architecture docs | ✅ Yes | No |
| External URLs | No | ✅ Yes |
| README.md (for navigation) | ✅ Yes | No |
| Child CLAUDE.md files | ✅ Yes | Alternative |

## Definition of Done

- [ ] All memory files discovered (CLAUDE.md, rules/, local)
- [ ] Documentation files inventoried
- [ ] Existing imports identified
- [ ] Unreferenced docs marked
- [ ] Best memory target determined for each doc
- [ ] Imports added using `@path` syntax
- [ ] Imports grouped logically
- [ ] Context provided for each import
- [ ] Hierarchy optimized (subdirectory relocation)
- [ ] Child CLAUDE.md files linked
- [ ] Rules files handled appropriately
- [ ] CLAUDE.local.md respected (not modified without asking)
- [ ] User memory (~/.claude/) not touched
- [ ] Summary report provided
- [ ] Next steps suggested
