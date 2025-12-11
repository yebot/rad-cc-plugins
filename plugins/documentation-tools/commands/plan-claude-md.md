---
description: Analyze repository structure and recommend optimal Claude Code memory strategy including CLAUDE.md placement, modular rules, and import patterns
allowed-tools:
  - Bash
  - Glob
  - Grep
  - Read
  - Write
---

# Plan Claude Code Memory Strategy

Analyze the repository structure and recommend the optimal memory file strategy for Claude Code. This includes CLAUDE.md placement, `.claude/rules/` modular rules, import patterns, and guidance on personal vs shared memory.

## Claude Code Memory Hierarchy

Before analyzing, understand the complete memory system:

| Memory Type | Location | Purpose | Shared |
|-------------|----------|---------|--------|
| Enterprise policy | `/Library/Application Support/ClaudeCode/CLAUDE.md` | Org-wide standards | All org |
| Project memory | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Team project context | Team (git) |
| Project rules | `./.claude/rules/*.md` | Modular topic-specific rules | Team (git) |
| User memory | `~/.claude/CLAUDE.md` | Personal all-project prefs | Just you |
| User rules | `~/.claude/rules/*.md` | Personal modular rules | Just you |
| Project local | `./CLAUDE.local.md` | Personal project prefs (gitignored) | Just you |

## Instructions

### Phase 1: Repository Analysis

1. **Understand repository structure**:

   ```bash
   # Directory overview
   tree -L 3 -d -I 'node_modules|.git|dist|build|coverage|.next|.nuxt|vendor' | head -100

   # Count directories and files
   find . -type d | grep -v node_modules | grep -v .git | wc -l
   find . -type f \( -name "*.js" -o -name "*.ts" -o -name "*.py" -o -name "*.go" -o -name "*.java" \) | grep -v node_modules | wc -l
   ```

2. **Identify repository type**:
   - **Monorepo**: Look for `packages/`, `apps/`, `services/`, workspace configs
   - **Microservices**: Multiple services with independent deployments
   - **Large library**: Multiple major modules/components
   - **Standard app**: Single unified application

3. **Check for existing memory files**:

   ```bash
   # Find all Claude Code memory files
   find . -name "CLAUDE.md" -o -name "CLAUDE.local.md" -o -path "*/.claude/rules/*.md" 2>/dev/null | grep -v node_modules

   # Check for .claude directory
   ls -la .claude/ 2>/dev/null
   ```

4. **Analyze topic diversity**:
   - Are there distinct concerns (testing, API, security, database)?
   - Are there file-type-specific patterns (all *.ts files follow certain rules)?
   - Would different topics benefit from separate documentation?

5. **Assess architectural boundaries**:
   - Can developers work on one area without needing context from others?
   - Are there clear domain boundaries?
   - Do subdirectories have their own dependencies/configs?

### Phase 2: Decision Analysis

6. **Apply the Memory Strategy Decision Tree**:

```
Repository Analysis
│
├─ Small project (<500 files, <50 dirs)?
│   │
│   ├─ Few distinct topics?
│   │   └─ ✅ Single ./CLAUDE.md
│   │       └─ Use @imports for documentation references
│   │
│   └─ Multiple distinct topics (testing, API, security)?
│       └─ ✅ ./CLAUDE.md + .claude/rules/
│           ├─ testing.md
│           ├─ api.md
│           └─ {topic}.md
│
├─ Medium project (500-1000 files)?
│   │
│   ├─ Topic diversity but unified codebase?
│   │   └─ ✅ ./CLAUDE.md + .claude/rules/{topic}.md
│   │
│   └─ Clear subsystem boundaries?
│       └─ ✅ Multiple CLAUDE.md + optional rules/
│
├─ Large project (>1000 files) or Monorepo?
│   │
│   └─ ✅ Multiple CLAUDE.md files (per package/service)
│       └─ Each can have own .claude/rules/ if needed
│
└─ File-type-specific patterns needed?
    └─ ✅ Path-specific rules in .claude/rules/
        └─ Use paths: frontmatter
```

7. **Determine recommendations**:

   Based on analysis, determine which combination:
   - **Option A**: Single `./CLAUDE.md` only
   - **Option B**: `./CLAUDE.md` + `.claude/rules/` (modular rules)
   - **Option C**: Multiple `./CLAUDE.md` files (monorepo/microservices)
   - **Option D**: Multiple CLAUDE.md + rules/ (complex projects)

### Phase 3: Generate Recommendations

8. **For Option A (Single CLAUDE.md)**:

   ```markdown
   ## Memory Strategy Recommendation: Single File

   **Analysis Results:**
   - Repository type: [standard app / small library]
   - Total files: [count]
   - Architectural complexity: Low

   ### Recommendation

   ✅ A single `./CLAUDE.md` at the repository root is sufficient.

   **Reasoning:**
   - [List 2-3 key reasons]

   ### Recommended Structure

   ```
   ./CLAUDE.md              # All project context
   ./CLAUDE.local.md        # Your personal dev setup (optional, gitignored)
   ```

   ### Using Imports

   Reference documentation using import syntax:
   ```markdown
   # In CLAUDE.md
   See @README.md for project overview.
   API documentation: @docs/api.md
   ```

   ### Next Steps

   1. Run `/init` to create or update CLAUDE.md
   2. Add `@imports` for key documentation files
   3. Create `CLAUDE.local.md` for your personal dev URLs/setup (optional)
   ```

9. **For Option B (CLAUDE.md + Modular Rules)**:

   ```markdown
   ## Memory Strategy Recommendation: Modular Rules

   **Analysis Results:**
   - Repository type: [medium project with topic diversity]
   - Total files: [count]
   - Distinct topics identified: [testing, API, security, etc.]

   ### Recommendation

   ✅ Use `./CLAUDE.md` for overview + `.claude/rules/` for topic-specific rules.

   **Why Modular Rules?**
   - Keeps main CLAUDE.md focused and readable
   - Topic-specific rules are easier to maintain
   - Path-specific rules can target file types

   ### Recommended Structure

   ```
   ./CLAUDE.md                    # Project overview, architecture, commands
   ./.claude/
   ├── CLAUDE.md                  # (optional) Alternative to root CLAUDE.md
   └── rules/
       ├── testing.md             # Test patterns, mocking, coverage
       ├── api.md                 # API conventions, error handling
       ├── database.md            # Query patterns, migrations
       └── security.md            # Auth, validation, secrets
   ./CLAUDE.local.md              # Your personal setup (gitignored)
   ```

   ### Path-Specific Rules Example

   For file-type-specific patterns, use `paths:` frontmatter:

   ```markdown
   ---
   paths: src/api/**/*.ts
   ---

   # API Endpoint Rules

   - Validate all inputs with zod
   - Use standard error response format
   - Include OpenAPI documentation comments
   ```

   ### Suggested Rule Files

   Based on analysis, create these rules:
   [List specific rule files based on detected patterns]

   ### Next Steps

   1. Run `/init` to create/update root CLAUDE.md
   2. Create `.claude/rules/` directory
   3. Create topic-specific rule files
   4. Add path-specific rules where needed
   5. Create `CLAUDE.local.md` for personal setup (optional)
   ```

10. **For Option C (Multiple CLAUDE.md files)**:

    ```markdown
    ## Memory Strategy Recommendation: Multi-File Approach

    **Analysis Results:**
    - Repository type: [monorepo / microservices]
    - Total files: [count]
    - Major subsystems: [count]

    ### Recommendation

    ✅ Multiple CLAUDE.md files, one per major subsystem.

    **Why Multiple Files?**
    - [List 3-5 reasons from analysis]

    ### Recommended Structure

    ```
    ./CLAUDE.md                      # Repository overview, cross-cutting concerns
    ./packages/web/CLAUDE.md         # Frontend-specific context
    ./packages/api/CLAUDE.md         # Backend-specific context
    ./packages/shared/CLAUDE.md      # Shared utilities context
    ./CLAUDE.local.md                # Your personal setup (gitignored)
    ```

    ### Location Details

    [For each recommended CLAUDE.md]:
    ```
    📍 [path]/CLAUDE.md
    ├── Purpose: [what it covers]
    ├── Scope: [what code it applies to]
    └── Key Topics:
        • [topic 1]
        • [topic 2]
    ```

    ### Using Imports

    Reference related documentation:
    ```markdown
    # In packages/api/CLAUDE.md
    See @../shared/CLAUDE.md for shared types.
    API spec: @./docs/openapi.yaml
    ```

    ### Initialization Checklist

    - [ ] `cd ./` → `/init` (root)
    - [ ] `cd packages/web/` → `/init`
    - [ ] `cd packages/api/` → `/init`
    [etc.]
    - [ ] Run `/link-docs-to-claude` from root
    ```

11. **For Option D (Multiple CLAUDE.md + Rules)**:

    Combine the guidance from Options B and C for complex projects.

### Phase 4: Additional Guidance

12. **Always include these recommendations**:

    **Personal Memory (`CLAUDE.local.md`)**:
    ```markdown
    ### Personal Project Setup

    Create `./CLAUDE.local.md` for your personal preferences:
    - Local development URLs
    - Your preferred test data
    - Personal debugging shortcuts

    This file is automatically gitignored.

    Example:
    ```markdown
    # My Local Setup

    ## Dev URLs
    - API: http://localhost:3001
    - DB: postgresql://localhost:5432/mydb

    ## Debug Commands
    \`\`\`bash
    DEBUG=api:* npm run dev
    \`\`\`
    ```
    ```

    **User Memory (`~/.claude/CLAUDE.md`)**:
    ```markdown
    ### Personal Preferences (All Projects)

    For preferences that apply to ALL your projects, use `~/.claude/CLAUDE.md`:
    - Code style preferences
    - Preferred tooling shortcuts
    - Your workflow habits

    These are not project-specific and won't be shared with the team.
    ```

    **Import Syntax**:
    ```markdown
    ### Using Imports

    Reference documentation with `@path` syntax instead of markdown links:

    ```markdown
    # Good - uses imports
    See @README.md for project overview.
    Architecture details: @docs/architecture.md

    # Import from user directory
    Personal preferences: @~/.claude/my-prefs.md
    ```

    Benefits:
    - Claude Code loads imported content automatically
    - Keeps CLAUDE.md focused
    - Recursive imports supported (max 5 levels)
    ```

    **Enterprise Considerations**:
    ```markdown
    ### Enterprise/Organization Standards

    If your organization has coding standards that should apply to all developers:
    - Contact IT/DevOps about enterprise policy deployment
    - Location: `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS)
    - Deployed via MDM, Group Policy, or configuration management
    ```

### Phase 5: Validation and Summary

13. **Validate recommendations**:
    - Do recommendations align with architectural boundaries?
    - Is the complexity appropriate for project size?
    - Will this scale as the project grows?

14. **Provide final summary**:

    ```markdown
    ## Summary

    | Aspect | Recommendation |
    |--------|----------------|
    | Main memory | [./CLAUDE.md / multiple locations] |
    | Modular rules | [Yes/No - .claude/rules/] |
    | Path-specific | [Yes/No - which patterns] |
    | Personal local | Recommended (CLAUDE.local.md) |

    ### Effort Estimate
    - Initial setup: [low/medium/high]
    - Maintenance: [low/medium]

    ### Key Benefits
    - [Benefit 1]
    - [Benefit 2]
    - [Benefit 3]
    ```

## Decision Logic Reference

### When to Use `.claude/rules/` vs Multiple CLAUDE.md

| Scenario | Recommendation |
|----------|----------------|
| Same codebase, different topics | `.claude/rules/{topic}.md` |
| Different codebases/packages | Multiple `CLAUDE.md` files |
| File-type-specific rules | `.claude/rules/` with `paths:` |
| Team ownership boundaries | Multiple `CLAUDE.md` files |
| Shared conventions | `.claude/rules/` |

### Path-Specific Rules Patterns

| Pattern | Use Case |
|---------|----------|
| `src/api/**/*.ts` | API endpoint rules |
| `**/*.test.ts` | Testing conventions |
| `src/components/**/*.tsx` | React component rules |
| `{src,lib}/**/*.ts` | All TypeScript rules |
| `migrations/**/*` | Database migration rules |

### Recommended Rule File Topics

| File | Contents |
|------|----------|
| `testing.md` | Test patterns, mocking, coverage requirements |
| `api.md` | Endpoint conventions, error handling, validation |
| `database.md` | Query patterns, migrations, ORM usage |
| `security.md` | Authentication, authorization, secrets |
| `code-style.md` | Formatting, naming, patterns |
| `components.md` | UI component patterns (React, Vue, etc.) |

## Example Outputs

### Example 1: Small Project

```
## Memory Strategy Recommendation: Single File

**Analysis Results:**
- Repository type: Standard Next.js application
- Total files: 156
- Architectural complexity: Low

### Recommendation

✅ A single `./CLAUDE.md` at the repository root is sufficient.

**Reasoning:**
- Small, tightly-coupled codebase
- No clear topic separation needed
- All developers work across the full stack

### Recommended Structure

```
./CLAUDE.md              # All project context
./CLAUDE.local.md        # Your dev setup (optional)
```

### Next Steps

1. Run `/init` to create CLAUDE.md
2. Add `@imports` for key docs
3. Optionally create CLAUDE.local.md for your local URLs
```

### Example 2: Medium Project with Topic Diversity

```
## Memory Strategy Recommendation: Modular Rules

**Analysis Results:**
- Repository type: Express.js API with PostgreSQL
- Total files: 487
- Topics identified: API design, testing, database, authentication

### Recommendation

✅ Use `./CLAUDE.md` + `.claude/rules/` for modular organization.

### Recommended Structure

```
./CLAUDE.md
./.claude/rules/
├── api-design.md           # REST conventions, versioning
├── testing.md              # Jest patterns, mocking
├── database.md             # Prisma patterns, migrations
└── auth.md                 # JWT handling, permissions
./CLAUDE.local.md           # Your local setup
```

### Path-Specific Rule

Create `.claude/rules/api-validation.md`:
```markdown
---
paths: src/routes/**/*.ts, src/controllers/**/*.ts
---

# API Validation Rules

- Validate all request bodies with zod
- Return consistent error format
```
```

### Example 3: Monorepo

```
## Memory Strategy Recommendation: Multi-File Approach

**Analysis Results:**
- Repository type: Turborepo monorepo
- Total files: 2,341
- Packages: 5 (web, api, mobile, admin, shared)

### Recommendation

✅ Multiple CLAUDE.md files + optional rules per package.

### Recommended Structure

```
./CLAUDE.md                      # Monorepo overview
./apps/web/CLAUDE.md             # Next.js frontend
./apps/api/CLAUDE.md             # Express backend
./apps/api/.claude/rules/        # API-specific rules (optional)
│   └── endpoints.md
./packages/shared/CLAUDE.md      # Shared utilities
./CLAUDE.local.md                # Your setup
```
```

## Definition of Done

- [ ] Repository structure analyzed
- [ ] Repository type identified
- [ ] Scale metrics gathered
- [ ] Topic diversity assessed
- [ ] Existing memory files discovered
- [ ] Decision tree applied
- [ ] Appropriate strategy selected (A/B/C/D)
- [ ] Specific recommendations provided
- [ ] Rule files suggested (if applicable)
- [ ] Path-specific patterns identified (if applicable)
- [ ] CLAUDE.local.md guidance included
- [ ] Import syntax explained
- [ ] User memory mentioned
- [ ] Implementation steps provided
- [ ] Summary with effort estimate delivered
