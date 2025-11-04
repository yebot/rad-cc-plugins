---
description: Link all documentation files to CLAUDE.md for better context availability
allowed-tools:
  - Bash
  - Glob
  - Grep
  - Read
  - Edit
---

# Link All Documentation to CLAUDE.md

Ensure all documentation files in the repository are properly referenced in CLAUDE.md files for maximum context availability.

## Instructions

1. **Find all CLAUDE.md files in the repository**:
   ```bash
   find . -name "CLAUDE.md" -o -name "claude.md" | grep -v node_modules | grep -v .git
   ```

   - Identify the root CLAUDE.md (typically at repository root)
   - Note any subdirectory CLAUDE.md files
   - These will be the target files for adding documentation references

2. **Inventory all markdown documentation files**:

   Use the Glob tool to find all markdown files:
   ```
   pattern: "**/*.md"
   ```

   **Filter the results to exclude:**
   - `node_modules/` directories
   - `.git/` directories
   - Hidden directories (`.*/`)
   - The CLAUDE.md files themselves
   - Common non-documentation files:
     - `README.md` (usually already referenced)
     - `CHANGELOG.md`
     - `LICENSE.md`
     - Package/build files

   **Focus on documentation files like:**
   - `docs/**/*.md`
   - `documentation/**/*.md`
   - Architecture documents
   - API documentation
   - How-to guides
   - Technical specifications
   - Any `.md` files in project subdirectories

3. **For each documentation file found**:

   a) **Read the file to understand its purpose**:
      - Use the Read tool to examine the first 20-50 lines
      - Identify the document's primary topic/purpose
      - Note any key sections or headings

   b) **Check if it's already referenced in any CLAUDE.md**:
      - Use Grep to search all CLAUDE.md files for the document's path
      - Search for both absolute and relative path references
      - Check for variations (with/without leading `./`, etc.)
      ```bash
      # Example grep pattern
      grep -r "path/to/doc.md" . --include="CLAUDE.md" --include="claude.md"
      ```

   c) **If NOT already referenced**:
      - Mark this file as needing a reference
      - Determine the best CLAUDE.md file to add it to (see step 4)

4. **Determine the best CLAUDE.md file for each unreferenced doc**:

   **Decision logic:**

   - **Root CLAUDE.md**: Use for:
     - Repository-wide documentation
     - Architecture documents
     - Top-level guides
     - Cross-cutting concerns
     - Docs in `docs/` or `documentation/` at root level

   - **Subdirectory CLAUDE.md**: Use for:
     - Documentation specific to that subdirectory's domain
     - Component-specific guides
     - Module-level technical docs
     - When a CLAUDE.md exists in or near the doc's directory

   **When in doubt**: Default to root CLAUDE.md for broader visibility.

5. **Add references to the appropriate CLAUDE.md file(s)**:

   a) **Read the target CLAUDE.md file** to understand its structure

   b) **Find or create an appropriate section** for documentation references:
      - Look for existing sections like:
        - "## Documentation"
        - "## Additional Resources"
        - "## Reference Materials"
        - "## Related Documentation"
      - If none exist, create a new section near the end:
        ```markdown
        ## Related Documentation

        Additional documentation files in this repository:
        ```

   c) **Add the reference with a brief context note**:
      ```markdown
      - [Relative/Path/To/Doc.md](Relative/Path/To/Doc.md) - Brief description of what this doc covers
      ```

   **Guidelines for the brief description:**
   - One line, 5-15 words
   - Describe the purpose or content
   - Use active language
   - Examples:
     - "API endpoint specifications and request/response formats"
     - "Database schema design and migration guide"
     - "Component architecture and design patterns"
     - "Deployment procedures and environment configuration"

   d) **Use the Edit tool** to add the reference to the CLAUDE.md file
      - Add to existing documentation section if present
      - Maintain alphabetical or logical ordering
      - Keep consistent formatting with existing references

6. **Optimize documentation link hierarchy** (handle subdirectory CLAUDE.md files):

   **Scenario**: A parent CLAUDE.md may contain links to documentation that would be more appropriately referenced in a newly created subdirectory CLAUDE.md file (closer to the relevant code).

   a) **For each subdirectory CLAUDE.md file** (if any exist):

      - Identify its directory path (e.g., `components/auth/CLAUDE.md`)
      - Determine its "scope" (the subdirectory it covers)

   b) **Review parent CLAUDE.md files for potentially misplaced references**:

      - Read each parent CLAUDE.md (especially root CLAUDE.md)
      - Examine all documentation references in the "Related Documentation" or similar sections

   c) **Evaluate each reference for relocation**:

      For each documentation link in a parent CLAUDE.md, check:

      - **Is the referenced file within or closely related to a subdirectory that has its own CLAUDE.md?**

        Example scenarios where relocation makes sense:
        - Root CLAUDE.md links to `components/auth/README.md` → Move to `components/auth/CLAUDE.md`
        - Root CLAUDE.md links to `services/api/endpoints.md` → Move to `services/CLAUDE.md` or `services/api/CLAUDE.md`
        - `src/CLAUDE.md` links to `src/utils/helpers/guide.md` → Move to `src/utils/CLAUDE.md`

      - **Would the reference provide more value at the lower level?**

        Consider:
        - Proximity to relevant code
        - Specificity of the documentation (component-specific vs. project-wide)
        - Whether the subdirectory CLAUDE.md is missing critical context

      - **Should it remain at the parent level?**

        Keep references in parent CLAUDE.md if:
        - Documentation covers cross-cutting concerns
        - File provides repository-wide context
        - Documentation spans multiple subdirectories
        - The doc is a top-level architecture/overview document

   d) **Move references when appropriate**:

      For references that should be relocated:

      1. **Read the subdirectory CLAUDE.md** to understand its structure
      2. **Add the reference** to the subdirectory CLAUDE.md:
         - Adjust the relative path from the new location
         - Place in appropriate section (create "## Related Documentation" if needed)
         - Keep the same description or refine it for local context
      3. **Remove the reference** from the parent CLAUDE.md:
         - Use Edit tool to cleanly remove the line
         - Preserve formatting and surrounding references
         - Don't leave empty sections (remove section if last item)

   e) **Document moved references**:

      Keep track of relocations for the summary report:
      ```
      Moved references:
      - docs/auth/oauth.md: CLAUDE.md → components/auth/CLAUDE.md
      - services/api/endpoints.md: CLAUDE.md → services/CLAUDE.md
      ```

   **Important considerations**:
   - Don't create duplicate references (check subdirectory CLAUDE.md first)
   - Relative paths will change when moving between CLAUDE.md files
   - When in doubt, leave the reference in the parent (no harm in redundancy)
   - This is an optimization step—only move references when clearly beneficial

7. **Group related documentation** (optional enhancement):

   If multiple documentation files share a common theme or directory:
   - Group them together in the CLAUDE.md
   - Use subheadings or bullet point hierarchy
   - Example:
     ```markdown
     ## Related Documentation

     ### API Documentation
     - [docs/api/endpoints.md](docs/api/endpoints.md) - REST API endpoint reference
     - [docs/api/authentication.md](docs/api/authentication.md) - Auth flows and token management

     ### Development Guides
     - [docs/setup.md](docs/setup.md) - Local development environment setup
     - [docs/testing.md](docs/testing.md) - Testing strategy and guidelines
     ```

8. **Report results to the user**:

   Provide a summary:
   ```
   📚 Documentation Linking Complete!

   Total markdown files found: X
   Already referenced in CLAUDE.md: Y
   Newly added references: Z
   References relocated: M

   Updated files:
   - CLAUDE.md (+Z references, -M moved)
   - path/to/subdirectory/CLAUDE.md (+N references, +M moved in)

   New references added:
   - docs/api/endpoints.md → CLAUDE.md
   - docs/setup.md → CLAUDE.md
   - components/auth/README.md → components/CLAUDE.md

   References relocated for better hierarchy:
   - components/auth/oauth-guide.md: CLAUDE.md → components/auth/CLAUDE.md
   - services/api/endpoints.md: CLAUDE.md → services/CLAUDE.md
   ```

9. **Suggest next steps**:
   - "Review the added references for accuracy"
   - "Consider updating the brief descriptions if needed"
   - "Run this command periodically to catch new documentation"

## Important Guidelines

### What to Reference
- ✅ Technical documentation files
- ✅ Architecture and design docs
- ✅ API specifications
- ✅ How-to guides and tutorials
- ✅ Developer onboarding docs
- ✅ Configuration references

### What to Skip
- ❌ CLAUDE.md files themselves (avoid circular references)
- ❌ README.md at root (usually already referenced or primary doc)
- ❌ CHANGELOG.md (version history, not context)
- ❌ LICENSE.md (legal, not development context)
- ❌ node_modules/ and vendor directories
- ❌ Build output or generated files
- ❌ Package manager files (package.json, etc.)

### Reference Format
- Always use relative paths from the CLAUDE.md location
- Use markdown link syntax: `[display text](path/to/file.md)`
- Include brief, helpful descriptions
- Maintain consistent formatting with existing references

### Best Practices
- Group related documentation together
- Use clear section headers
- Keep descriptions concise but informative
- Alphabetize or logically order references
- Use Edit tool to maintain file formatting
- Don't duplicate references (check first!)

## Error Handling

| Issue | Solution |
|-------|----------|
| No CLAUDE.md found | Create one at root with basic structure |
| CLAUDE.md has no documentation section | Create "## Related Documentation" section |
| Ambiguous best location | Default to root CLAUDE.md, note in description |
| File already referenced | Skip, note in summary |
| Circular reference risk | Never reference CLAUDE.md in itself |
| Binary or non-text .md files | Skip after read attempt fails |

## Example Output Structure

For a CLAUDE.md file after running this command:

```markdown
# Project Name

Project overview and instructions...

## Repository Structure

...existing content...

## Related Documentation

Additional documentation files in this repository:

- [docs/api/endpoints.md](docs/api/endpoints.md) - REST API endpoint specifications
- [docs/api/authentication.md](docs/api/authentication.md) - OAuth2 authentication flow
- [docs/architecture/database.md](docs/architecture/database.md) - Database schema and design patterns
- [docs/deployment.md](docs/deployment.md) - Production deployment procedures
- [docs/setup.md](docs/setup.md) - Local development environment setup
- [docs/testing.md](docs/testing.md) - Testing strategy and CI/CD integration
```

## Definition of Done

- [ ] All CLAUDE.md files identified
- [ ] All markdown documentation files inventoried
- [ ] Each doc checked for existing references
- [ ] Unreferenced docs identified
- [ ] Best CLAUDE.md target determined for each unreferenced doc
- [ ] References added with appropriate brief descriptions
- [ ] Documentation link hierarchy optimized (references moved to subdirectory CLAUDE.md files where appropriate)
- [ ] Relative paths updated correctly for any moved references
- [ ] CLAUDE.md files updated using Edit tool
- [ ] Summary report provided to user
- [ ] No duplicate references created
- [ ] No circular references created
- [ ] User informed of next steps
