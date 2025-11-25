# Webapp Team

> A complete dev team in your terminal

A Claude Code plugin that provides a virtual web application development team with 12 specialized agents covering engineering, product, design, growth, and operations.

## Installation

This plugin is designed to be used locally within Claude Code. Ensure the plugin directory is at:

```
.claude/plugins/webapp-team/
```

## Quick Start

### Ask Your Team

```
/team-consult Should we use server components or client components for this feature?
```

### Plan a Feature

```
/feature-kickoff User authentication with magic links
```

### Get Code Reviewed

```
/code-review src/components/Dashboard.tsx
```

### Pre-Launch Check

```
/ship-checklist
```

### See Your Team

```
/team-roster
```

## The Team

### Engineering (Blue)
| Agent | Specialty |
|-------|-----------|
| `full-stack-engineer` | End-to-end development, TypeScript/React/Node.js |
| `frontend-engineer` | React/Next.js, performance, accessibility |
| `backend-engineer` | APIs, databases, integrations |
| `devops-engineer` | CI/CD, infrastructure, monitoring |
| `qa-engineer` | Testing, automation, quality |
| `security-engineer` | Security audits, auth, compliance |

### Product & Design (Purple)
| Agent | Specialty |
|-------|-----------|
| `product-manager` | Requirements, prioritization, metrics |
| `ui-ux-designer` | User flows, accessibility, design systems |

### Growth & Marketing (Green)
| Agent | Specialty |
|-------|-----------|
| `growth-marketer` | SEO, analytics, conversion optimization |
| `content-creator` | Copywriting, content strategy |
| `data-analyst` | Tracking, dashboards, experiments |

### Operations (Orange)
| Agent | Specialty |
|-------|-----------|
| `customer-support` | Documentation, feedback, bug translation |

## Commands

| Command | What It Does |
|---------|--------------|
| `/team-consult <question>` | Get multi-agent perspectives on any question |
| `/team-roster` | Display all team members |
| `/team-standup` | Run a virtual standup |
| `/feature-kickoff <desc>` | Plan a feature with the full team |
| `/code-review [file]` | Comprehensive code review |
| `/ship-checklist` | Pre-launch checklist |
| `/debug-assist <issue>` | Collaborative debugging |
| `/hire-for <role>` | Job description and interview plan |

## Skills

| Skill | Use For |
|-------|---------|
| `write-prd` | Product Requirements Documents |
| `estimate-complexity` | Implementation estimates |
| `write-test-plan` | Test planning |
| `security-checklist` | Security reviews |
| `analytics-plan` | Analytics tracking plans |
| `write-user-docs` | User documentation |

## Usage Examples

### Direct Agent Invocation

```
Use the product-manager agent to write user stories for a checkout flow
Use the security-engineer agent to review the authentication code
Use the growth-marketer agent to create an analytics plan for the new feature
```

### With @Mentions in Team Consult

```
/team-consult @security @backend How should we handle API authentication?
/team-consult @frontend @ux What's the best approach for this complex form?
```

### Combining Commands

```
# 1. Plan the feature
/feature-kickoff Add real-time notifications

# 2. Review implementation
/code-review src/features/notifications/

# 3. Check before shipping
/ship-checklist
```

## Technology Defaults

Agents default to modern TypeScript web stack:
- TypeScript, React, Next.js
- Node.js, Prisma, PostgreSQL
- Tailwind CSS, Vitest, Playwright

Override by providing context:
```
Use the full-stack-engineer to help with this Python/Django project
```

## Philosophy

1. **User-first** - Every decision starts with user value
2. **Ship fast, iterate** - Small, testable increments
3. **Quality built-in** - Security, accessibility, testing from day one
4. **Data-informed** - Measure impact, not activity
5. **Collaborate** - Best solutions come from multiple perspectives

## File Structure

```
webapp-team/
├── PLUGIN.md           # Full documentation
├── README.md           # This file
├── agents/             # 12 agent definitions
├── commands/           # 8 slash commands
├── hooks/              # Event hooks
├── skills/             # 6 reusable skills
└── examples/           # Sample outputs
```

## Contributing

1. Add agents: Create `.md` in `agents/` with proper frontmatter
2. Add commands: Create `.md` in `commands/` with proper frontmatter
3. Add skills: Create directory in `skills/` with `SKILL.md`
4. Update hooks: Modify `hooks/hooks.json`

## Changelog

### 0.1.0
- Initial release
- 12 specialized agents
- 8 team commands
- 6 reusable skills
- Event hooks for development workflow

## License

MIT
