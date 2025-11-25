---
name: code-review
description: Get comprehensive code review from relevant specialists
tools: Read, Glob, Grep, Bash, TodoWrite, Task
model: inherit
arguments:
  - name: target
    description: File path, directory, or git diff to review
    required: false
---

# Code Review

Get a comprehensive code review from multiple specialist perspectives.

## Instructions

### Step 1: Identify Code to Review

Determine what to review based on `$ARGUMENTS.target`:

1. **If file path provided**: Review that specific file
2. **If directory provided**: Review recent changes in that directory
3. **If no argument**: Review staged or recent uncommitted changes

```bash
# Check for staged changes
git diff --staged --name-only

# Check for unstaged changes
git diff --name-only

# Recent commits
git log --oneline -5
```

### Step 2: Analyze File Types

Categorize the files being reviewed:
- **Frontend** (`.tsx`, `.jsx`, `.css`, `.scss`): Include Frontend Engineer
- **Backend** (`.ts` API routes, `.py`, database files): Include Backend Engineer
- **Both**: Include Full-Stack Engineer
- **All changes**: Include Security Engineer and QA Engineer

### Step 3: Full-Stack Engineer Review

Invoke `full-stack-engineer` agent for:

- **Correctness**: Does the code do what it's supposed to?
- **Maintainability**: Is it readable and well-structured?
- **Type Safety**: Are types correct and complete?
- **Error Handling**: Are errors handled gracefully?
- **Testing**: Is test coverage adequate?

### Step 4: Domain-Specific Review

Based on file types, invoke appropriate specialist:

**For Frontend Files** - Invoke `frontend-engineer`:
- Component structure and composition
- State management approach
- Performance (re-renders, bundle size)
- Accessibility
- Responsive design

**For Backend Files** - Invoke `backend-engineer`:
- API design and contracts
- Database queries and performance
- Input validation
- Error responses
- Logging

### Step 5: Security Engineer Review

Invoke `security-engineer` agent for:

- Authentication/authorization checks
- Input validation and sanitization
- Secrets or sensitive data exposure
- SQL injection or XSS vulnerabilities
- Security header considerations

### Step 6: QA Engineer Review

Invoke `qa-engineer` agent for:

- Test coverage suggestions
- Edge cases to consider
- Integration test recommendations
- Manual testing scenarios
- Quality gate compliance

### Step 7: Compile Review

Create a consolidated review:

```markdown
## Code Review Summary

**Files Reviewed**: [count]
**Overall Assessment**: [Good / Needs Work / Blocker]

---

### Critical Issues (Must Fix)
| Issue | Location | Severity |
|-------|----------|----------|
| [Issue] | `file:line` | Critical |

### Suggestions (Should Fix)
| Suggestion | Location | Impact |
|------------|----------|--------|
| [Suggestion] | `file:line` | High/Medium/Low |

### Minor Comments (Nice to Have)
- [Comment] at `file:line`

---

### Full-Stack Engineer Notes
[Summary]

### [Frontend/Backend] Engineer Notes
[Summary]

### Security Review
- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] Auth checks in place
- [ ] XSS prevention verified

### QA Notes
**Recommended Tests:**
- [ ] [Test scenario]
- [ ] [Test scenario]

---

### Approval Status
- [ ] Full-Stack: Approved / Changes Requested
- [ ] Security: Approved / Changes Requested
- [ ] QA: Approved / Changes Requested
```

## Severity Levels

- **Critical**: Blocks merge - security vulnerability, data loss risk, broken functionality
- **High**: Should fix before merge - bugs, missing error handling, performance issues
- **Medium**: Fix soon - code quality, maintainability concerns
- **Low**: Nice to have - style suggestions, minor improvements
