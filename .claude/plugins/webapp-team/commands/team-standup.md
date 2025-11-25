---
name: team-standup
description: Run a virtual standup across relevant team agents
tools: Read, Glob, Grep, TodoWrite, AskUserQuestion, Task
model: inherit
---

# Team Standup

Run a virtual standup with your webapp team to get multiple perspectives on current work, blockers, and priorities.

## Instructions

### Step 1: Gather Context

Ask the user to provide context about their current work:

```
Please share:
1. What have you been working on recently?
2. What are you planning to work on next?
3. Any blockers or concerns?
```

If the user doesn't provide this, check for:
- Recent git commits (`git log --oneline -10`)
- Open TODO items in the codebase
- Recent file changes

### Step 2: Product Manager Perspective

Invoke the `product-manager` agent to provide:
- Priority alignment check
- User impact assessment
- Any scope concerns
- Dependencies to be aware of

### Step 3: Full-Stack Engineer Perspective

Invoke the `full-stack-engineer` agent to provide:
- Technical blockers or concerns
- Architecture considerations
- Technical debt observations
- Testing recommendations

### Step 4: UI/UX Designer Perspective

Invoke the `ui-ux-designer` agent to provide:
- UX considerations for current work
- Accessibility reminders
- Design system alignment
- User flow implications

### Step 5: Synthesize Standup Summary

Create a structured standup summary:

```markdown
## Standup Summary - [Date]

### Current Focus
[Summary of what's being worked on]

### Team Perspectives

**Product Manager:**
- [Key points]

**Full-Stack Engineer:**
- [Key points]

**UI/UX Designer:**
- [Key points]

### Action Items
- [ ] [Action item 1]
- [ ] [Action item 2]

### Blockers
- [Any blockers identified]

### Priorities for Today
1. [Priority 1]
2. [Priority 2]
3. [Priority 3]
```

## Output Format

The standup should be:
- Concise (each perspective 2-4 bullet points)
- Actionable (clear next steps)
- Time-boxed (total ~5 minute read)

## Notes

- Skip agents that aren't relevant to current work
- Highlight disagreements between perspectives
- Flag urgent items that need immediate attention
