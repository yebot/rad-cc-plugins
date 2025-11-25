---
name: hire-for
description: Get job description and interview plan for a role
tools: Read, Write, Glob, Grep, TodoWrite, AskUserQuestion, Task
model: inherit
arguments:
  - name: role
    description: The role to create hiring materials for
    required: true
---

# Hire For

Generate a comprehensive job description and interview plan for a role.

## Instructions

### Step 1: Identify Role

Use `$ARGUMENTS.role` to determine the role. Map to team expertise:

- **Engineering roles**: Full-Stack, Frontend, Backend, DevOps, Security, QA
- **Product roles**: Product Manager
- **Design roles**: UI/UX Designer
- **Growth roles**: Growth Marketer, Content Creator, Data Analyst
- **Support roles**: Customer Support

### Step 2: Product Manager Input

Invoke `product-manager` agent to define:

1. **Role Requirements**
   - Why we're hiring
   - Team structure and reporting
   - Key responsibilities
   - Success criteria (30/60/90 day goals)

2. **Candidate Profile**
   - Must-have qualifications
   - Nice-to-have qualifications
   - Culture fit indicators

### Step 3: Specialist Input

Invoke the relevant specialist agent for the role:

**Technical Roles** - Invoke matching engineer agent:
- Required technical skills
- Tech stack proficiency expectations
- Technical interview questions
- Take-home assignment ideas

**Product/Design Roles** - Invoke `product-manager` or `ui-ux-designer`:
- Portfolio expectations
- Case study prompts
- Design challenge ideas

**Growth Roles** - Invoke `growth-marketer` or `data-analyst`:
- Analytics proficiency requirements
- Campaign experience expectations
- Data analysis exercise ideas

### Step 4: Generate Job Description

Create the job posting:

```markdown
# [Role Title]

## About Us
[Company description - to be filled by user]

## About the Role
[Role context and why it matters]

## What You'll Do
- [Responsibility 1]
- [Responsibility 2]
- [Responsibility 3]
- [Responsibility 4]
- [Responsibility 5]

## What You'll Bring

### Must Have
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

### Nice to Have
- [Nice-to-have 1]
- [Nice-to-have 2]

## Tech Stack / Tools
- [Tool/Tech 1]
- [Tool/Tech 2]

## What We Offer
[Benefits - to be filled by user]

## Interview Process
1. [Step 1]
2. [Step 2]
3. [Step 3]
4. [Step 4]

---

*[Company name] is an equal opportunity employer.*
```

### Step 5: Create Interview Plan

Generate the interview structure:

```markdown
# Interview Plan: [Role Title]

## Overview
- **Total Process Length**: [X] weeks
- **Interview Stages**: [X]
- **Decision Timeline**: [X] days after final

---

## Stage 1: Initial Screen (30 min)

**Interviewer**: Recruiter / Hiring Manager

**Goals**:
- Verify basic qualifications
- Assess communication skills
- Explain role and company
- Gauge interest and availability

**Questions**:
1. Tell me about your background and what brings you here
2. [Role-specific question]
3. What are you looking for in your next role?
4. [Logistics: timeline, compensation expectations]

**Scorecard**:
- [ ] Communication: Clear and articulate
- [ ] Relevant experience: Matches requirements
- [ ] Interest level: Genuinely interested
- [ ] Cultural fit indicators: Positive

---

## Stage 2: Technical / Skills Interview (60 min)

**Interviewer**: [Relevant team member]

**Goals**:
- Assess core technical/functional skills
- Understand problem-solving approach
- Evaluate depth of experience

**Questions**:
1. [Technical question 1]
2. [Technical question 2]
3. [Scenario-based question]

**Exercise** (if applicable):
[Description of live coding, design exercise, or case study]

**Scorecard**:
- [ ] Technical proficiency: [1-5]
- [ ] Problem-solving: [1-5]
- [ ] Communication of technical concepts: [1-5]

---

## Stage 3: Take-Home Assignment (Optional)

**Time limit**: [X] hours

**Assignment**:
[Description of take-home project]

**Evaluation Criteria**:
- [ ] Functionality: Does it work?
- [ ] Code quality: Is it well-structured?
- [ ] Communication: Is it documented?

---

## Stage 4: Team Interview (45 min each)

**Interviewers**: [2-3 team members]

**Goals**:
- Assess collaboration style
- Evaluate cultural fit
- Different perspectives on candidate

**Focus Areas**:
- Interviewer 1: [Focus area]
- Interviewer 2: [Focus area]
- Interviewer 3: [Focus area]

---

## Stage 5: Final Interview (45 min)

**Interviewer**: [Senior leader / Founder]

**Goals**:
- Final culture assessment
- Answer candidate questions
- Sell the opportunity

**Questions**:
1. [Values-based question]
2. [Growth/ambition question]
3. What questions do you have for me?

---

## Evaluation & Decision

### Skills Matrix

| Skill | Must Have | Candidate Score |
|-------|-----------|-----------------|
| [Skill 1] | Yes | |
| [Skill 2] | Yes | |
| [Skill 3] | Nice | |

### Overall Assessment

- **Technical/Functional**: [1-5]
- **Communication**: [1-5]
- **Culture Fit**: [1-5]
- **Growth Potential**: [1-5]

### Recommendation
[ ] Strong Hire
[ ] Hire
[ ] No Hire
[ ] Strong No Hire

### Notes
[Summary of key findings and concerns]
```

## Output

- Job description ready to post
- Complete interview plan
- Scorecard templates for each stage
