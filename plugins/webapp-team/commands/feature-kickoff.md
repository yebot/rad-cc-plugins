---
name: feature-kickoff
description: Kick off a new feature with full team input
tools: Read, Write, Glob, Grep, TodoWrite, AskUserQuestion, Task
model: inherit
arguments:
  - name: feature
    description: Description of the feature to kick off
    required: true
---

# Feature Kickoff

Kick off a new feature with input from multiple team perspectives to create a comprehensive feature brief.

## Instructions

### Step 1: Capture Feature Description

Use the provided `$ARGUMENTS.feature` or ask the user:

```
What feature would you like to kick off? Please describe:
- What it should do
- Who it's for
- Why it's needed
```

### Step 2: Product Manager Phase

Invoke the `product-manager` agent to create:

1. **User Story**
   - As a [user type]
   - I want to [action]
   - So that [benefit]

2. **Acceptance Criteria**
   - [ ] Criteria 1
   - [ ] Criteria 2
   - [ ] Criteria 3

3. **Success Metrics**
   - Primary metric
   - Secondary metrics

4. **Scope Definition**
   - In scope
   - Out of scope

### Step 3: UI/UX Designer Phase

Invoke the `ui-ux-designer` agent to provide:

1. **User Flow**
   - Entry points
   - Key interactions
   - Exit points

2. **UX Considerations**
   - Accessibility requirements
   - Mobile considerations
   - Edge cases (empty states, errors)

3. **Design Requirements**
   - New components needed
   - Existing components to reuse
   - Animation/interaction notes

### Step 4: Full-Stack Engineer Phase

Invoke the `full-stack-engineer` agent to provide:

1. **Technical Approach**
   - High-level architecture
   - Data model changes
   - API design

2. **Complexity Estimate**
   - T-shirt size (S/M/L/XL)
   - Key complexity drivers
   - Suggested breakdown

3. **Technical Considerations**
   - Dependencies
   - Performance implications
   - Security considerations
   - Testing strategy

### Step 5: Growth Marketer Phase

Invoke the `growth-marketer` agent to provide:

1. **Analytics Requirements**
   - Events to track
   - Funnel definition
   - Success metrics setup

2. **Growth Implications**
   - SEO considerations
   - Conversion opportunities
   - A/B testing opportunities

### Step 6: Compile Feature Brief

Create a comprehensive feature brief:

```markdown
# Feature Brief: [Feature Name]

## Overview
[Brief description]

## User Story
As a [user type], I want to [action], so that [benefit].

## Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

## Success Metrics
- **Primary**: [Metric]
- **Secondary**: [Metric]

## Scope
### In Scope
- [Item]

### Out of Scope
- [Item]

---

## User Flow
[Flow description or diagram]

## UX Requirements
- [Requirement]

## Design Notes
- [Note]

---

## Technical Approach
[Architecture description]

## Complexity: [S/M/L/XL]
**Drivers:**
- [Driver]

## Suggested Breakdown
1. [Task 1] - [Size]
2. [Task 2] - [Size]

## Technical Considerations
- **Dependencies**: [List]
- **Performance**: [Notes]
- **Security**: [Notes]

---

## Analytics Plan
### Events
- `[event_name]` - [when triggered]

### Funnel
1. [Step]
2. [Step]

---

## Open Questions
- [ ] [Question 1]
- [ ] [Question 2]

## Next Steps
1. [Step]
2. [Step]
```

## Output

Save the feature brief to a file or display inline based on user preference.
