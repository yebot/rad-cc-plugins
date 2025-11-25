---
name: webapp-team
version: 0.1.0
description: A virtual web app development team with specialized agents for product development, engineering, design, growth, and operations
author:
  name: Tobey Forsman
  email: tobeyforsman@gmail.com
repository: https://github.com/yebots/rad-cc-plugins
license: MIT
min_claude_code_version: 1.0.0
---

# Webapp Team Plugin

A complete virtual development team in your terminal. This Claude Code plugin simulates a full web application development team with 12 specialized agents covering engineering, product, design, growth, and operations.

## Overview

This plugin provides a virtual team of specialized agents that collaborate to build, design, grow, and operate web applications. Each agent brings domain expertise, follows best practices, and provides their unique perspective on your work.

**Philosophy**:
- User-first: Every decision starts with user value
- Ship fast, iterate: Prefer small, testable increments
- Quality built-in: Security, accessibility, testing from the start
- Data-informed: Measure impact, not just activity
- Collaborate: Best solutions come from multiple perspectives

---

## Team Roster

### Engineering Team (Blue Palette)

| Agent | Role | Color | Category |
|-------|------|-------|----------|
| `full-stack-engineer` | Senior Full-Stack Engineer | `#2563eb` | Critical |
| `frontend-engineer` | Frontend Engineer | `#3b82f6` | Specialist |
| `backend-engineer` | Backend/API Engineer | `#60a5fa` | Specialist |
| `devops-engineer` | DevOps/Platform Engineer | `#93c5fd` | Specialist |
| `qa-engineer` | QA/Test Engineer | `#1e40af` | Specialist |
| `security-engineer` | Security Engineer | `#1e3a8a` | Specialist |

### Product & Design Team (Purple Palette)

| Agent | Role | Color | Category |
|-------|------|-------|----------|
| `product-manager` | Product Manager | `#7c3aed` | Critical |
| `ui-ux-designer` | UI/UX Designer | `#8b5cf6` | Critical |

### Growth & Marketing Team (Green Palette)

| Agent | Role | Color | Category |
|-------|------|-------|----------|
| `growth-marketer` | Growth Marketing Generalist | `#059669` | Critical |
| `content-creator` | Content Creator/Copywriter | `#10b981` | Specialist |
| `data-analyst` | Data/Analytics Specialist | `#f59e0b` | Specialist |

### Operations Team (Orange Palette)

| Agent | Role | Color | Category |
|-------|------|-------|----------|
| `customer-support` | Customer Support Lead | `#d97706` | Specialist |

---

## Quick Start

### Invoke Individual Agents

Use agents directly via natural language:

```
Use the full-stack-engineer agent to review this code
Use the product-manager agent to help define requirements for this feature
Use the ui-ux-designer agent to review the accessibility of this component
```

### Use Team Commands

Slash commands orchestrate multiple agents:

```
/team-consult How should we implement user authentication?
/feature-kickoff Add dark mode to the application
/code-review src/components/LoginForm.tsx
/ship-checklist
```

### Check the Roster

```
/team-roster
```

---

## Commands Reference

| Command | Description |
|---------|-------------|
| `/team-consult <question>` | Consult with relevant agents automatically |
| `/team-roster` | Display all team agents and specialties |
| `/team-standup` | Run virtual standup with PM, Engineer, Designer |
| `/feature-kickoff <feature>` | Plan new feature with full team input |
| `/code-review [target]` | Comprehensive code review from specialists |
| `/ship-checklist` | Pre-launch checklist from all perspectives |
| `/debug-assist <issue>` | Collaborative debugging with relevant agents |
| `/hire-for <role>` | Generate job description and interview plan |

---

## Skills Reference

| Skill | Description | Used By |
|-------|-------------|---------|
| `write-prd` | Create Product Requirements Document | PM, Engineers |
| `estimate-complexity` | Estimate implementation complexity | Engineers |
| `write-test-plan` | Create comprehensive test plan | QA, Engineers |
| `security-checklist` | Security review checklist | Security, Engineers |
| `analytics-plan` | Define analytics tracking plan | Data, Growth, PM |
| `write-user-docs` | Write user-facing documentation | Support, Content |

---

## Configuration

### Enable/Disable Agents

By default, all agents are enabled. To use a minimal team, invoke only:
- `full-stack-engineer` - General implementation
- `product-manager` - Requirements and planning
- `ui-ux-designer` - Design and UX

### Project Type Presets

**Startup/MVP**:
- Full-Stack Engineer
- Product Manager
- Growth Marketer

**Enterprise**:
- Full-Stack Engineer (+ Frontend/Backend specialists)
- Product Manager
- Security Engineer
- QA Engineer
- DevOps Engineer

**Content/Marketing Site**:
- Full-Stack Engineer
- UI/UX Designer
- Content Creator
- Growth Marketer (SEO focus)

### Preferred Technology Stack

Agents default to:
- **Language**: TypeScript
- **Frontend**: React/Next.js
- **Backend**: Node.js with Prisma
- **Database**: PostgreSQL
- **Styling**: Tailwind CSS
- **Testing**: Vitest, Playwright

To customize, provide context in your prompts:
```
Use the full-stack-engineer to help with this Django/Python project...
```

---

## Agent Specialties

### Critical Roles (Use Most Often)

**Full-Stack Engineer** (`full-stack-engineer`)
- End-to-end feature development
- TypeScript/React/Next.js frontend
- Node.js/Python backend
- API design and data modeling
- *Triggers*: Implementation, debugging, code review

**Product Manager** (`product-manager`)
- User story writing with acceptance criteria
- Prioritization (RICE, MoSCoW)
- PRD and spec writing
- Success metrics definition
- *Triggers*: Planning, prioritization, requirements

**UI/UX Designer** (`ui-ux-designer`)
- User flow mapping
- Accessibility (WCAG 2.1)
- Design systems
- Mobile-first responsive design
- *Triggers*: UI decisions, accessibility, user flows

**Growth Marketer** (`growth-marketer`)
- SEO (technical and content)
- Analytics setup (GA4, Mixpanel, PostHog)
- A/B testing strategy
- Conversion optimization
- *Triggers*: Growth, analytics, SEO, marketing

### Specialist Roles (Use When Needed)

**Frontend Engineer** - React/Next.js performance, component libraries
**Backend Engineer** - API design, database optimization, integrations
**DevOps Engineer** - CI/CD, infrastructure, monitoring
**QA Engineer** - Test strategy, automation, quality gates
**Security Engineer** - Security audits, auth, compliance
**Content Creator** - Blog posts, landing pages, product copy
**Data Analyst** - Event tracking, dashboards, experiment analysis
**Customer Support** - Bug translation, documentation, feedback synthesis

---

## Hooks

The plugin includes helpful hooks that provide reminders:

- **Pre-commit**: Security and QA reminders before commits
- **New component**: Accessibility and pattern reminders
- **API routes**: Validation and auth reminders
- **Dependency changes**: Security and bundle size alerts
- **PR creation**: Summary and checklist reminders

---

## Examples

See the `examples/` directory for sample outputs:
- `feature-kickoff-example.md` - Sample feature planning output
- `code-review-example.md` - Sample code review output
- `ship-checklist-example.md` - Sample pre-launch checklist

---

## Installation

This plugin is located at `.claude/plugins/webapp-team/`.

### File Structure

```
.claude/plugins/webapp-team/
├── PLUGIN.md              # This file
├── README.md              # User documentation
├── agents/                # Agent definitions
│   ├── full-stack-engineer.md
│   ├── product-manager.md
│   ├── ui-ux-designer.md
│   └── ... (12 agents total)
├── commands/              # Slash commands
│   ├── team-consult.md
│   ├── team-roster.md
│   ├── feature-kickoff.md
│   └── ... (8 commands total)
├── hooks/                 # Event hooks
│   └── hooks.json
├── skills/                # Reusable skills
│   ├── write-prd/
│   ├── estimate-complexity/
│   └── ... (6 skills total)
└── examples/              # Example outputs
```

---

## Contributing

To extend this plugin:

1. **Add new agents**: Create `.md` file in `agents/` with frontmatter
2. **Add new commands**: Create `.md` file in `commands/` with frontmatter
3. **Add new skills**: Create directory in `skills/` with `SKILL.md`
4. **Update hooks**: Modify `hooks/hooks.json`

Follow the existing patterns and frontmatter format.
