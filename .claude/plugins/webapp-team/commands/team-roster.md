---
name: team-roster
description: Display all available team agents and their specialties
tools: Read, Glob
model: inherit
---

# Team Roster

Display all available webapp team agents, their specialties, and when to use them.

## Instructions

Display the following team roster:

```markdown
# Webapp Team Roster

Your virtual web application development team with specialized agents for every aspect of product development.

---

## Engineering Team 🔧

### Critical Roles

| Agent | Role | Color | Specialty |
|-------|------|-------|-----------|
| `full-stack-engineer` | Senior Full-Stack Engineer | 🔵 #2563eb | End-to-end feature development, TypeScript/React/Node.js |

**Full-Stack Engineer**
- End-to-end feature development
- TypeScript/React/Next.js frontend
- Node.js/Python backend
- PostgreSQL/Prisma data modeling
- API design (REST, GraphQL, tRPC)

*Triggers*: Implementation tasks, feature building, debugging, code review

---

### Specialist Roles

| Agent | Role | Color | Specialty |
|-------|------|-------|-----------|
| `frontend-engineer` | Frontend Engineer | 🔵 #3b82f6 | React/Next.js, performance, component libraries |
| `backend-engineer` | Backend/API Engineer | 🔵 #60a5fa | API design, databases, integrations |
| `devops-engineer` | DevOps/Platform Engineer | 🔵 #93c5fd | CI/CD, infrastructure, monitoring |
| `qa-engineer` | QA/Test Engineer | 🔵 #1e40af | Test strategy, automation, quality |
| `security-engineer` | Security Engineer | 🔵 #1e3a8a | Security audits, auth, compliance |

**Frontend Engineer**
- React/Next.js architecture
- State management (Zustand, React Query)
- Performance optimization (Core Web Vitals)
- Component library development

*Triggers*: Frontend architecture, performance issues, component design

**Backend Engineer**
- API design (REST, GraphQL, tRPC)
- Database optimization
- Authentication/authorization patterns
- Third-party integrations

*Triggers*: API design, database schema, integrations, backend architecture

**DevOps Engineer**
- CI/CD pipeline design
- Infrastructure as Code
- Monitoring and alerting
- Disaster recovery

*Triggers*: Deployment issues, infrastructure decisions, monitoring setup

**QA Engineer**
- Test strategy and planning
- E2E test automation (Playwright)
- Bug lifecycle management
- Quality gates

*Triggers*: Test strategy, bug investigation, test automation

**Security Engineer**
- OWASP Top 10 vulnerabilities
- Authentication security
- Data encryption
- Compliance awareness

*Triggers*: Security review, auth implementation, data handling

---

## Product & Design Team 🎨

| Agent | Role | Color | Specialty |
|-------|------|-------|-----------|
| `product-manager` | Product Manager | 🟣 #7c3aed | Requirements, prioritization, roadmap |
| `ui-ux-designer` | UI/UX Designer | 🟣 #8b5cf6 | User flows, accessibility, design systems |

**Product Manager**
- User story writing and acceptance criteria
- Roadmap prioritization (RICE, MoSCoW)
- PRD and spec writing
- Success metrics definition

*Triggers*: Feature planning, prioritization, user stories, requirements

**UI/UX Designer**
- User flow mapping
- Accessibility (WCAG 2.1)
- Mobile-first responsive design
- Design tokens and component libraries

*Triggers*: UI decisions, user flow questions, accessibility, design systems

---

## Growth & Marketing Team 📈

| Agent | Role | Color | Specialty |
|-------|------|-------|-----------|
| `growth-marketer` | Growth Marketing Generalist | 🟢 #059669 | SEO, analytics, conversion optimization |
| `content-creator` | Content Creator/Copywriter | 🟢 #10b981 | Blog posts, landing pages, product copy |
| `data-analyst` | Data/Analytics Specialist | 🟠 #f59e0b | Event tracking, dashboards, A/B testing |

**Growth Marketer**
- SEO (technical and content)
- Paid acquisition (Meta, Google)
- Landing page optimization
- A/B testing strategy

*Triggers*: Growth discussions, analytics setup, SEO, conversion optimization

**Content Creator**
- Blog post writing (SEO-optimized)
- Landing page copy
- Product microcopy (CTAs, error messages)
- Brand voice development

*Triggers*: Copywriting, content strategy, blog posts, email copy

**Data Analyst**
- Event tracking implementation
- Dashboard design
- Cohort and funnel analysis
- Experiment analysis

*Triggers*: Analytics setup, data questions, metric definitions, reporting

---

## Operations Team ⚙️

| Agent | Role | Color | Specialty |
|-------|------|-------|-----------|
| `customer-support` | Customer Support Lead | 🟠 #d97706 | Bug translation, documentation, feedback synthesis |

**Customer Support**
- Ticket triage and prioritization
- Bug report translation
- FAQ and help documentation
- User feedback synthesis

*Triggers*: User feedback, bug clarification, documentation, support workflows

---

## Quick Reference

### How to Invoke Agents

**Direct invocation** (via Task tool):
```
Use the full-stack-engineer agent to review this code
```

**Via @mentions** (in /team-consult):
```
/team-consult @frontend @ux How should we implement this component?
```

### Team Commands

| Command | Description |
|---------|-------------|
| `/team-consult <question>` | Consult with relevant agents |
| `/team-roster` | Display this roster |
| `/team-standup` | Run virtual standup |
| `/feature-kickoff <feature>` | Plan new feature with team input |
| `/code-review <target>` | Get comprehensive code review |
| `/ship-checklist` | Pre-launch checklist from all perspectives |
| `/debug-assist <issue>` | Collaborative debugging |
| `/hire-for <role>` | Create job description and interview plan |

### Team Skills

| Skill | Description |
|-------|-------------|
| `write-prd` | Create Product Requirements Document |
| `estimate-complexity` | Estimate implementation complexity |
| `write-test-plan` | Create comprehensive test plan |
| `security-checklist` | Security review checklist |
| `analytics-plan` | Define analytics tracking plan |
| `write-user-docs` | Write user-facing documentation |

---

## Team Philosophy

This virtual team operates on these principles:

1. **User-first**: Every decision starts with user value
2. **Ship fast, iterate**: Prefer small, testable increments
3. **Quality built-in**: Security, accessibility, testing from the start
4. **Data-informed**: Measure impact, not just activity
5. **Collaborate**: Best solutions come from multiple perspectives
```

## Output

Display the roster formatted for easy reading. Highlight which agents are most commonly used (full-stack-engineer, product-manager, ui-ux-designer).
