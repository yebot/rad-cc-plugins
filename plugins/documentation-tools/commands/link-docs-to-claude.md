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

6. **Group related documentation** (optional enhancement):

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

7. **Report results to the user**:

   Provide a summary:
   ```
   📚 Documentation Linking Complete!

   Total markdown files found: X
   Already referenced in CLAUDE.md: Y
   Newly added references: Z

   Updated files:
   - CLAUDE.md (+Z references)
   - path/to/subdirectory/CLAUDE.md (+N references)

   New references added:
   - docs/api/endpoints.md → CLAUDE.md
   - docs/setup.md → CLAUDE.md
   - components/auth/README.md → components/CLAUDE.md
   ```

8. **Suggest next steps**:
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
- [ ] CLAUDE.md files updated using Edit tool
- [ ] Summary report provided to user
- [ ] No duplicate references created
- [ ] No circular references created
- [ ] User informed of next steps
