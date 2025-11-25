---
name: debug-assist
description: Collaborative debugging with relevant specialists
tools: Read, Glob, Grep, Bash, TodoWrite, Task
model: inherit
arguments:
  - name: issue
    description: Description of the issue to debug
    required: true
---

# Debug Assist

Get collaborative debugging help from relevant team specialists.

## Instructions

### Step 1: Capture Issue Details

Use `$ARGUMENTS.issue` and gather more context:

```
To help debug, please provide:
1. What's the expected behavior?
2. What's actually happening?
3. Steps to reproduce
4. Any error messages?
5. When did it start? Any recent changes?
```

### Step 2: Classify the Issue

Determine issue type to route to appropriate agents:

- **Frontend Issue** (UI bugs, rendering, state): Frontend Engineer
- **Backend Issue** (API errors, data issues): Backend Engineer
- **Infrastructure Issue** (deployment, performance, timeouts): DevOps Engineer
- **Full Stack** (unclear origin): Full-Stack Engineer first
- **All Issues**: Customer Support for user perspective

### Step 3: Full-Stack Engineer Investigation

Invoke `full-stack-engineer` agent for initial investigation:

1. **Reproduce the Issue**
   - Verify steps to reproduce
   - Identify consistent vs intermittent behavior

2. **Narrow Down the Layer**
   - Frontend vs Backend vs Infrastructure
   - Check network requests, console errors, logs

3. **Initial Hypotheses**
   - Most likely causes
   - Quick checks to validate/invalidate

4. **Suggested Investigation Path**
   - What to check first
   - What logs to examine
   - What tests to run

### Step 4: Domain-Specific Investigation

Based on classification, invoke appropriate specialist:

**Frontend Issue** - Invoke `frontend-engineer`:
- Browser console errors
- React component state
- Network request/response
- CSS/rendering issues
- Hydration problems

**Backend Issue** - Invoke `backend-engineer`:
- Server logs
- Database queries
- API response codes
- Authentication/authorization
- Third-party service status

**Infrastructure Issue** - Invoke `devops-engineer`:
- Deployment logs
- Infrastructure health
- Resource utilization
- Recent deployments
- External service status

### Step 5: Customer Support Perspective

Invoke `customer-support` agent:
- User impact assessment
- Similar reports from other users?
- Workarounds available?
- Communication needs

### Step 6: Compile Debugging Plan

Create a structured debugging plan:

```markdown
## Debug Plan: [Issue Title]

### Issue Summary
- **Reported**: [Description]
- **Expected**: [Behavior]
- **Actual**: [Behavior]
- **Severity**: Critical / High / Medium / Low

### Initial Assessment

**Most Likely Layer**: [Frontend / Backend / Infrastructure]

**Primary Hypotheses**:
1. [Hypothesis 1] - [Confidence: High/Medium/Low]
2. [Hypothesis 2] - [Confidence: High/Medium/Low]
3. [Hypothesis 3] - [Confidence: High/Medium/Low]

---

### Investigation Steps

#### Phase 1: Quick Checks
- [ ] [Check 1] - tests hypothesis [X]
- [ ] [Check 2] - tests hypothesis [Y]

#### Phase 2: Deep Investigation
- [ ] [Investigation 1]
- [ ] [Investigation 2]

#### Phase 3: If Above Fails
- [ ] [Fallback investigation]

---

### Logs to Check
- [ ] [Log location 1]
- [ ] [Log location 2]

### Commands to Run
```bash
# [Description]
[command]

# [Description]
[command]
```

### Files to Examine
- `[file path]` - [reason]
- `[file path]` - [reason]

---

### User Impact
- **Users Affected**: [Estimate]
- **Workaround Available**: [Yes/No - details]
- **Communication Needed**: [Yes/No]

---

### Resolution Tracking

| Hypothesis | Status | Finding |
|------------|--------|---------|
| [Hypothesis 1] | 🔍 Investigating | |
| [Hypothesis 2] | ⏳ Pending | |

### Root Cause
[To be filled after investigation]

### Fix
[To be filled after resolution]

### Prevention
[How to prevent this in the future]
```

## Tips

- Start with the simplest hypothesis
- Check for recent changes that correlate with issue start
- Look at logs with timestamps around the issue
- Don't assume - verify each step
- Document findings even if negative
