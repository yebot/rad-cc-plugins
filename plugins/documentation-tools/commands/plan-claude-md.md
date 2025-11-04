---
description: Analyze repository structure and recommend optimal CLAUDE.md placement strategy
allowed-tools:
  - Bash
  - Glob
  - Grep
  - Read
  - Write
---

# Plan CLAUDE.md Strategy

Analyze the repository structure and recommend optimal CLAUDE.md file placement for context management. Determine whether a single root CLAUDE.md is sufficient or if multiple strategically-placed files would improve Claude Code's effectiveness.

## Instructions

### Phase 1: Repository Analysis

1. **Understand the repository structure at a high level**:

   a) **Get directory structure overview**:
   ```bash
   tree -L 3 -d -I 'node_modules|.git|dist|build|coverage|.next|.nuxt|vendor' | head -100
   ```

   b) **Identify repository type and scale**:
   - Is this a monorepo? (Look for `packages/`, `apps/`, `services/`, workspaces)
   - Is this a large library? (Check for multiple major modules/components)
   - Is this a standard single-app repo?
   - Count total directories: `find . -type d | grep -v node_modules | grep -v .git | wc -l`
   - Estimate codebase size: `find . -type f \( -name "*.js" -o -name "*.ts" -o -name "*.py" -o -name "*.go" -o -name "*.java" -o -name "*.rb" -o -name "*.php" \) | grep -v node_modules | wc -l`

2. **Identify major architectural boundaries**:

   a) **Scan for monorepo indicators**:
   - Look for `packages/`, `apps/`, `services/`, `modules/`, `libs/` directories
   - Check for workspace files: `package.json` (workspaces), `pnpm-workspace.yaml`, `lerna.json`, `nx.json`
   - Read these files to understand workspace structure

   b) **Identify distinct domains/modules**:
   - Use Glob to find top-level source directories: `src/**/`, `lib/**/`, `components/**/`, etc.
   - Look for clear separation of concerns (frontend/backend, api/web, services/core)
   - Identify independent subsystems that could be developed separately

   c) **Assess component independence**:
   - Can developers work on one area without needing context from others?
   - Are there clear boundaries between domains?
   - Do subdirectories have their own dependencies/configs? (e.g., separate package.json files)

3. **Analyze existing documentation patterns**:

   a) **Find existing CLAUDE.md files**:
   ```bash
   find . -name "CLAUDE.md" -o -name "claude.md" | grep -v node_modules
   ```

   b) **Find README files throughout the repo**:
   ```bash
   find . -name "README.md" | grep -v node_modules | head -20
   ```

   c) **Identify documentation concentrations**:
   - Are there subdirectories with substantial documentation already?
   - Do subdirectories have their own docs/ folders?
   - Read a few README files to understand local context needs

4. **Assess workflow patterns**:

   a) **Check for independent build/test configurations**:
   - Multiple `package.json`, `Cargo.toml`, `go.mod`, `pom.xml` files
   - Separate CI/CD configs per directory
   - Independent deployment configs

   b) **Evaluate development isolation**:
   - Would a developer working in `services/auth/` need constant context from `services/payments/`?
   - Are there teams that own specific parts of the codebase?

### Phase 2: Decision Analysis

5. **Apply decision criteria**:

   **Single CLAUDE.md is sufficient when:**
   - ✅ Small to medium codebase (<500 files, <50 directories)
   - ✅ Single unified application with tight coupling
   - ✅ No clear architectural boundaries
   - ✅ All code shares common context and patterns
   - ✅ Simple project structure (e.g., typical web app)
   - ✅ Developers need full repository context for most tasks

   **Multiple CLAUDE.md files are beneficial when:**
   - 📂 **Monorepo**: Multiple packages/apps with independent lifecycles
   - 📂 **Large library**: Distinct modules that can be understood independently
   - 📂 **Microservices**: Separate services with different tech stacks/patterns
   - 📂 **Domain boundaries**: Clear DDD-style bounded contexts
   - 📂 **Team ownership**: Different teams own different parts
   - 📂 **Scale**: >1000 files or >100 directories
   - 📂 **Context overload**: Root CLAUDE.md would be >500 lines to cover everything
   - 📂 **Independent workflows**: Subdirectories have own build/test/deploy cycles

6. **Determine recommendation**:

   Based on the analysis, decide:
   - **Option A**: Single root CLAUDE.md is optimal
   - **Option B**: Multiple CLAUDE.md files recommended with specific locations

### Phase 3: Recommendations

7. **For Option A (Single CLAUDE.md):**

   Inform the user:
   ```
   📋 CLAUDE.md Strategy Recommendation: Single File

   Analysis Results:
   - Repository type: [standard app / small library / etc.]
   - Total files: [count]
   - Architectural complexity: [low / moderate]

   ✅ Recommendation: A single CLAUDE.md at the repository root is sufficient.

   Reasoning:
   - [List 2-3 key reasons based on analysis]
   - [e.g., "Codebase is tightly coupled with shared context"]
   - [e.g., "No clear architectural boundaries found"]

   Next Steps:
   1. Ensure root CLAUDE.md exists and is comprehensive
   2. Run `/link-docs-to-claude` to ensure all docs are referenced
   3. Keep CLAUDE.md updated as the project evolves
   ```

8. **For Option B (Multiple CLAUDE.md files):**

   a) **Identify specific locations for CLAUDE.md files**:

   For each recommended location, provide:
   - **Path**: Exact directory path (e.g., `packages/web-app/`)
   - **Scope**: What this CLAUDE.md would cover
   - **Rationale**: Why this location benefits from dedicated context
   - **Key topics**: What should be documented here

   Example structure:
   ```
   Recommended CLAUDE.md locations:

   1. 📍 packages/web-app/CLAUDE.md
      Scope: Frontend web application
      Rationale: Independent React app with own build pipeline
      Key topics: Component architecture, routing, state management

   2. 📍 packages/api/CLAUDE.md
      Scope: Backend API service
      Rationale: Separate Express.js service with own deployment
      Key topics: API endpoints, authentication, database models

   3. 📍 packages/shared/CLAUDE.md
      Scope: Shared utilities and types
      Rationale: Common code used across packages
      Key topics: Utility functions, TypeScript types, constants
   ```

   b) **Create a detailed recommendation report**:

   ```markdown
   📋 CLAUDE.md Strategy Recommendation: Multi-File Approach

   ## Analysis Results

   - Repository type: [monorepo / large library / microservices]
   - Total files: [count]
   - Total directories: [count]
   - Architectural complexity: [high / very high]
   - Major subsystems identified: [count]

   ## Assessment

   ✅ Recommendation: Multiple CLAUDE.md files recommended

   ### Why Multiple Files?
   - [List 3-5 key findings from analysis]
   - [e.g., "Monorepo with 5 independent packages"]
   - [e.g., "Clear domain boundaries between services"]
   - [e.g., "Each package has own dependencies and workflows"]
   - [e.g., "Root CLAUDE.md would exceed 800 lines to cover all context"]

   ### Proposed Structure

   Root: ./CLAUDE.md
   ├── Purpose: Repository overview, monorepo patterns, cross-cutting concerns
   ├── Content: Workspace structure, shared tooling, contribution guidelines
   └── Scope: High-level architecture and repository navigation

   [For each recommended location]:
   Location: [path]
   ├── Purpose: [Brief description]
   ├── Rationale: [Why this location needs dedicated context]
   ├── Scope: [What code/domains it covers]
   └── Key Topics to Document:
       • [Topic 1]
       • [Topic 2]
       • [Topic 3]

   ## Implementation Guide

   ### Standard CLAUDE.md Template Structure

   Each CLAUDE.md file should include these standard sections:

   ```markdown
   # [Module/Package Name]

   [Brief description]

   ## Purpose
   [What this code does and why it exists]

   ## Architecture
   [Key patterns, frameworks, and structure]

   ## Key Concepts
   [Domain-specific concepts and terminology]

   ## Development Workflow
   [How to build, test, run this code]

   ## Related Documentation
   [Links to relevant docs - populated by /link-docs-to-claude]

   ## Integration Points
   [How this integrates with other parts]
   ```

   ### Implementation Steps

   For each recommended CLAUDE.md location, use Claude Code's "!" bash mode to navigate and initialize:

   **Process:**
   1. Navigate to the directory: `!cd path/to/directory`
   2. Run the init command: `/init`
   3. Repeat for each recommended location

   **Recommended initialization order:**
   1. Start with root directory: `!cd ./` then `/init`
   2. Initialize each subdirectory in order listed above
   3. After all files created, run `/link-docs-to-claude` from root

   ## Maintenance Guidelines

   - Keep each CLAUDE.md focused on its specific domain
   - Avoid duplicating information across files
   - Root CLAUDE.md provides navigation and overview
   - Subdirectory CLAUDE.md files provide deep context
   - Update CLAUDE.md files when architecture changes
   - Run `/link-docs-to-claude` periodically to maintain doc references

   ## Expected Benefits

   ✅ **Reduced context overload**: Claude Code loads only relevant context
   ✅ **Faster comprehension**: Focused documentation for specific areas
   ✅ **Better scalability**: Documentation grows with codebase structure
   ✅ **Team alignment**: Clear ownership and documentation boundaries
   ✅ **Improved accuracy**: Context matches developer mental models
   ```

9. **Provide initialization checklist (if multiple files recommended)**:

   Create a simple checklist for the user to follow:

   ```markdown
   ## CLAUDE.md Initialization Checklist

   For each location below, use "!" bash mode to navigate and initialize:

   ### Root Directory
   - [ ] `!cd ./`
   - [ ] `/init`

   ### Subdirectories
   - [ ] `!cd packages/web-app/`
   - [ ] `/init`

   - [ ] `!cd packages/api/`
   - [ ] `/init`

   - [ ] `!cd packages/shared/`
   - [ ] `/init`

   [Continue for each recommended location...]

   ### Final Step
   - [ ] Return to root: `!cd ./`
   - [ ] Link documentation: `/link-docs-to-claude`
   ```

   Customize the checklist with the actual recommended paths from your analysis.

### Phase 4: Validation and Summary

10. **Validate recommendations**:

   - Do the recommended locations align with actual architectural boundaries?
   - Are there any edge cases or special considerations?
   - Would this strategy scale with likely repository growth?

11. **Provide final summary**:

   Recap the recommendation with:
   - Clear decision (single vs. multiple)
   - Number of files recommended (if multiple)
   - Estimated effort to implement
   - Expected benefits
   - Any caveats or considerations

## Decision Logic Reference

### Indicators for Single CLAUDE.md

| Indicator | Description |
|-----------|-------------|
| Small scale | <500 files, <50 directories |
| Tight coupling | No clear separation between modules |
| Single app | Standard web app, CLI tool, or small library |
| Shared context | All code needs similar background knowledge |
| Simple structure | Flat or shallow directory hierarchy |

### Indicators for Multiple CLAUDE.md Files

| Indicator | Description |
|-----------|-------------|
| Monorepo | Multiple packages/apps/services |
| Large scale | >1000 files or >100 directories |
| Domain boundaries | Clear DDD-style bounded contexts |
| Team ownership | Different teams own different areas |
| Independent workflows | Separate build/test/deploy per area |
| Tech diversity | Different tech stacks in different areas |
| Context overload | Single file would be >500 lines |
| Documentation concentration | Subdirectories have substantial local docs |

### Recommended CLAUDE.md Placement Patterns

**Monorepo Pattern:**
```
./CLAUDE.md (overview, workspace structure)
./packages/*/CLAUDE.md (per-package context)
```

**Microservices Pattern:**
```
./CLAUDE.md (architecture overview)
./services/*/CLAUDE.md (per-service context)
```

**Large Library Pattern:**
```
./CLAUDE.md (library overview, getting started)
./src/*/CLAUDE.md (per-major-module context)
```

**Full-Stack Pattern:**
```
./CLAUDE.md (project overview)
./frontend/CLAUDE.md (frontend-specific)
./backend/CLAUDE.md (backend-specific)
```

## Important Guidelines

### Analysis Best Practices

- **Be thorough**: Don't rush the analysis phase
- **Look for patterns**: Identify recurring structures
- **Consider growth**: Think about how the repo will evolve
- **Validate boundaries**: Ensure recommended locations make sense
- **Think like a developer**: Where would context be most useful?

### Recommendation Best Practices

- **Be specific**: Provide exact paths, not vague suggestions
- **Explain rationale**: Help users understand the "why"
- **Provide templates**: Make implementation easy
- **Consider maintenance**: Recommend sustainable patterns
- **Balance granularity**: Not too few, not too many files

### Communication Best Practices

- **Be clear and decisive**: Don't hedge unnecessarily
- **Provide actionable steps**: Make it easy to implement
- **Show your work**: Explain how you reached conclusions
- **Use visual formatting**: Make recommendations scannable
- **Offer alternatives**: Note when single vs. multiple is borderline

## Error Handling

| Issue | Solution |
|-------|----------|
| Cannot determine structure | Use `tree` and `find` commands to explore |
| Ambiguous boundaries | Err on side of fewer files, note uncertainty |
| No clear monorepo structure | Check for workspace configs, separate package.json files |
| Very flat structure | Likely single CLAUDE.md is best |
| Extremely large repo | May need >10 CLAUDE.md files, group by major domains |

## Example Outputs

### Example 1: Small Project (Single File)

```
📋 CLAUDE.md Strategy Recommendation: Single File

Analysis Results:
- Repository type: Standard web application
- Total files: 234
- Total directories: 28
- Architectural complexity: Low

✅ Recommendation: A single CLAUDE.md at the repository root is sufficient.

Reasoning:
- Small, tightly-coupled codebase with shared patterns
- No clear architectural boundaries between components
- All developers need full context for most tasks
- Current structure is simple and well-organized

Next Steps:
1. Ensure root CLAUDE.md exists and covers key patterns
2. Run `/link-docs-to-claude` to reference all docs
3. Keep CLAUDE.md updated as project grows
```

### Example 2: Monorepo (Multiple Files)

```
📋 CLAUDE.md Strategy Recommendation: Multi-File Approach

Analysis Results:
- Repository type: Monorepo (Turborepo workspace)
- Total files: 2,847
- Total directories: 312
- Architectural complexity: High
- Major subsystems identified: 5 packages

✅ Recommendation: Multiple CLAUDE.md files (6 total)

Why Multiple Files?
- Monorepo with 5 independent packages (web, api, mobile, admin, shared)
- Each package has own dependencies, build config, and team ownership
- Different tech stacks (React, Node.js, React Native)
- Root CLAUDE.md would need 1000+ lines to cover everything
- Developers typically work within single package boundaries

Proposed Structure:

Root: ./CLAUDE.md
├── Purpose: Monorepo overview, tooling, workspace management
├── Content: Turborepo config, shared scripts, CI/CD, contribution guide
└── Scope: Cross-package patterns and repository navigation

Location: apps/web/CLAUDE.md
├── Purpose: Customer-facing web application
├── Rationale: Independent Next.js app with own deployment pipeline
├── Scope: Frontend components, pages, routing, state management
└── Key Topics:
    • Next.js app router patterns
    • Component architecture and design system
    • API integration with backend
    • Authentication and user flows

Location: apps/api/CLAUDE.md
├── Purpose: Backend API service
├── Rationale: Separate Express.js service with own database
├── Scope: REST endpoints, business logic, database models
└── Key Topics:
    • API endpoint structure and patterns
    • Database schema and migrations
    • Authentication/authorization
    • Background jobs and queues

Location: apps/mobile/CLAUDE.md
├── Purpose: Mobile application
├── Rationale: React Native app with platform-specific patterns
├── Scope: Mobile screens, navigation, native modules
└── Key Topics:
    • React Native patterns
    • Native module integration
    • Push notifications
    • App store deployment

Location: apps/admin/CLAUDE.md
├── Purpose: Admin dashboard
├── Rationale: Separate React app for internal users
├── Scope: Admin UI, data management, analytics
└── Key Topics:
    • Admin component patterns
    • Data tables and forms
    • User management
    • Reporting features

Location: packages/shared/CLAUDE.md
├── Purpose: Shared code library
├── Rationale: Common utilities and types used across apps
├── Scope: Utility functions, TypeScript types, constants, UI components
└── Key Topics:
    • Shared TypeScript types
    • Utility function library
    • Shared UI components
    • Configuration constants

## CLAUDE.md Initialization Checklist

For each location below, use "!" bash mode to navigate and initialize:

### Root Directory
- [ ] `!cd ./`
- [ ] `/init`

### Subdirectories
- [ ] `!cd apps/web/`
- [ ] `/init`

- [ ] `!cd apps/api/`
- [ ] `/init`

- [ ] `!cd apps/mobile/`
- [ ] `/init`

- [ ] `!cd apps/admin/`
- [ ] `/init`

- [ ] `!cd packages/shared/`
- [ ] `/init`

### Final Step
- [ ] Return to root: `!cd ./`
- [ ] Link documentation: `/link-docs-to-claude`
```

## Definition of Done

- [ ] Repository structure analyzed comprehensively
- [ ] Repository type identified (monorepo, library, standard app, etc.)
- [ ] Scale metrics gathered (file count, directory count)
- [ ] Architectural boundaries identified
- [ ] Existing documentation patterns assessed
- [ ] Workflow patterns evaluated
- [ ] Decision criteria applied systematically
- [ ] Clear recommendation made (single vs. multiple)
- [ ] Specific locations identified (if multiple recommended)
- [ ] Rationale provided for each recommended location
- [ ] Implementation guide created (templates, steps, or script)
- [ ] Expected benefits communicated
- [ ] User provided with actionable next steps
- [ ] Validation performed on recommendations
- [ ] Final summary delivered clearly
