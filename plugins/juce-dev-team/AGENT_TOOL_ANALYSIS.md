# Agent Tool Analysis - Principle of Least Privilege

## Current State
All 13 agents have: `Read, Grep, Glob, Bash, Edit, Write`

## Recommended Tool Restrictions

### Implementation Agents (Full Tools)
These agents write code and need edit/write capabilities:
- **technical-lead**: `Read, Grep, Glob, Bash, Edit, Write` ✅ (reviews and modifies code)
- **dsp-engineer**: `Read, Grep, Glob, Bash, Edit, Write` ✅ (implements DSP algorithms)
- **plugin-engineer**: `Read, Grep, Glob, Bash, Edit, Write` ✅ (integrates DSP and UI)
- **ui-engineer**: `Read, Grep, Glob, Bash, Edit, Write` ✅ (creates UI components)
- **test-automation-engineer**: `Read, Grep, Glob, Bash, Edit, Write` ✅ (writes test code)
- **build-engineer**: `Read, Grep, Glob, Bash, Edit, Write` ✅ (modifies build configs)
- **telemetry-engineer**: `Read, Grep, Glob, Bash, Edit, Write` ✅ (implements analytics)
- **security-engineer**: `Read, Grep, Glob, Bash, Edit, Write` ✅ (implements licensing)
- **audio-content-engineer**: `Read, Grep, Glob, Bash, Edit, Write` ✅ (builds content tools)
- **platform-engineer**: `Read, Grep, Glob, Bash, Edit, Write` ✅ (builds standalone hosts)

### Testing/Investigation Agents (Read + Bash Only)
These agents test, run tools, and investigate but don't modify code:
- **qa-engineer**: `Read, Grep, Glob, Bash` ⚠️ (manual testing, running tests)
  - Needs: Read (test plans), Bash (run tests, DAWs)
  - Remove: Edit, Write (doesn't write code)

- **daw-compatibility-engineer**: `Read, Grep, Glob, Bash` ⚠️ (testing in DAWs)
  - Needs: Read (check code), Bash (run tests, auval, pluginval)
  - Remove: Edit, Write (doesn't fix code, delegates to plugin-engineer)

### Support/Documentation Agents (Read Only)
These agents investigate and document but don't modify code:
- **support-engineer**: `Read, Grep, Glob` ⚠️ (investigates user issues)
  - Needs: Read, Grep (read logs, search code)
  - Remove: Bash, Edit, Write (doesn't run tests or modify code)
  - Note: Could add Write for documentation (FAQ.md, KNOWN_ISSUES.md)
  - Suggested: `Read, Grep, Glob, Write` (write docs only)

## Summary of Changes

### Agents to Restrict:
1. **qa-engineer**: Remove `Edit, Write` → `Read, Grep, Glob, Bash`
2. **daw-compatibility-engineer**: Remove `Edit, Write` → `Read, Grep, Glob, Bash`
3. **support-engineer**: Remove `Bash, Edit` → `Read, Grep, Glob, Write` (write docs)

### Agents to Keep As-Is:
All implementation agents (10 agents) keep full tools.

## Rationale

**Testing Agents (qa, daw-compatibility)**:
- Need to READ code and configs
- Need to RUN tests, DAWs, validation tools (Bash)
- DON'T need to MODIFY code (that's what implementation agents do)
- They identify issues and delegate fixes to appropriate engineers

**Support Agent**:
- Need to READ logs, crash reports, code
- Need to WRITE documentation (FAQ, troubleshooting guides)
- DON'T need to RUN tests (delegates to QA)
- DON'T need to EDIT code (delegates to engineers)

This follows the principle of least privilege while maintaining each agent's effectiveness.
