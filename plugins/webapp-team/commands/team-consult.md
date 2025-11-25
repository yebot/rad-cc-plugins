---
name: team-consult
description: Consult with the full team on any topic - automatically routes to relevant agents
tools: Read, Write, Glob, Grep, Bash, TodoWrite, AskUserQuestion, Task
model: inherit
arguments:
  - name: question
    description: The question or task to consult the team about
    required: true
---

# Team Consult

Consult with your virtual webapp team on any topic. Questions are automatically routed to the most relevant specialists who provide their perspectives.

## Instructions

### Step 1: Analyze Input

Parse `$ARGUMENTS.question` to determine relevant agents. Look for:

**Technical Implementation Keywords**:
- code, implement, build, develop, architecture, refactor → `full-stack-engineer`
- frontend, react, component, CSS, UI → `frontend-engineer`
- backend, API, database, server → `backend-engineer`
- deploy, CI/CD, infrastructure → `devops-engineer`

**User Experience Keywords**:
- design, UX, flow, accessibility, user → `ui-ux-designer`
- requirements, story, prioritize, roadmap → `product-manager`

**Security/Quality Keywords**:
- security, auth, vulnerability, OWASP → `security-engineer`
- test, QA, bug, quality → `qa-engineer`

**Growth/Data Keywords**:
- growth, marketing, SEO, conversion → `growth-marketer`
- analytics, metrics, data, tracking → `data-analyst`

**Content/Support Keywords**:
- content, copy, writing → `content-creator`
- user feedback, support, documentation → `customer-support`

### Step 2: Check for @Mentions

If the user includes @mentions, prioritize those agents:
- `@full-stack` → `full-stack-engineer`
- `@frontend` → `frontend-engineer`
- `@backend` → `backend-engineer`
- `@devops` → `devops-engineer`
- `@pm` or `@product` → `product-manager`
- `@design` or `@ux` → `ui-ux-designer`
- `@security` → `security-engineer`
- `@qa` → `qa-engineer`
- `@growth` → `growth-marketer`
- `@data` → `data-analyst`
- `@content` → `content-creator`
- `@support` → `customer-support`

### Step 3: Select Agents (Max 4)

Choose 3-4 most relevant agents. Order by:
1. Strategy/requirements first (PM, UX)
2. Implementation second (Engineers)
3. Support functions third (QA, Security, Growth)

Avoid including too many agents - that creates noise.

### Step 4: Invoke Agents

For each selected agent, use the Task tool to invoke them with:

```
Context: [Original user question]

Provide your perspective as the [role] on this question. Focus on:
- Key considerations from your domain
- Recommendations
- Potential concerns or risks
- Questions that need answering

Keep your response concise (3-5 key points).
```

### Step 5: Synthesize Responses

Compile agent responses into a structured summary:

```markdown
## Team Consultation: [Topic]

### Consulted Specialists
- [Agent 1] - [Role]
- [Agent 2] - [Role]
- [Agent 3] - [Role]

---

### Consensus Points
Areas where the team agrees:
- [Point 1]
- [Point 2]
- [Point 3]

### Key Perspectives

#### [Agent 1 Role]
[Summary of their input]

**Recommendations**:
- [Recommendation 1]
- [Recommendation 2]

#### [Agent 2 Role]
[Summary of their input]

**Recommendations**:
- [Recommendation 1]
- [Recommendation 2]

[Continue for each agent...]

---

### Trade-offs Identified
| Option | Pros | Cons | Recommended By |
|--------|------|------|----------------|
| [Option A] | [Pros] | [Cons] | [Agent] |
| [Option B] | [Pros] | [Cons] | [Agent] |

### Open Questions
Questions that need resolution:
- [ ] [Question 1] - Ask: [Who to ask]
- [ ] [Question 2] - Ask: [Who to ask]

### Dissenting Opinions
If agents disagree:
- **[Agent 1]** thinks [X] because [reason]
- **[Agent 2]** thinks [Y] because [reason]

---

### Recommended Next Steps
Based on team input:
1. [Action 1]
2. [Action 2]
3. [Action 3]

### Additional Consultation Needed?
[Suggest which other agents might have valuable input if any]
```

## Examples

### Example 1: Technical Question
**Input**: "How should we implement user authentication?"

**Agents Selected**:
1. Security Engineer (security considerations)
2. Full-Stack Engineer (implementation approach)
3. Backend Engineer (API/session design)
4. Product Manager (requirements/user impact)

### Example 2: Feature Question
**Input**: "Should we add dark mode to the app?"

**Agents Selected**:
1. Product Manager (prioritization, user value)
2. UI/UX Designer (design system impact)
3. Frontend Engineer (implementation complexity)
4. Growth Marketer (adoption metrics)

### Example 3: With @Mentions
**Input**: "@security @devops How should we handle secrets in CI/CD?"

**Agents Selected**:
1. Security Engineer (mentioned)
2. DevOps Engineer (mentioned)
3. Full-Stack Engineer (general implementation context)

## Notes

- Keep agent responses focused (3-5 key points each)
- Highlight disagreements - they're valuable
- Suggest follow-up with specific agents if needed
- Don't overload with too many perspectives
