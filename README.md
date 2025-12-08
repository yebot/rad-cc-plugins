# Yebot's Claude Code Plugins

![Galaxy Brain](brain.jpg)

A curated marketplace of Claude Code plugins to supercharge your AI-assisted development workflow.

## Plugins (14)

### Project Management

| Plugin | Version | Description |
|--------|---------|-------------|
| **backlog-md** | v1.3.1 | Comprehensive Backlog.md integration with MCP support, specialized subagents for task alignment and planning, and workflow automation hooks |
| **backlog-md-cli** | v1.1.2 | CLI-first workflow orchestration for Git-native project management with strict file naming enforcement |
| **simbl** | v1.0.0 | Lightweight companion for SIMBL CLI backlog manager with task hygiene, quick capture, and reduced context-switching |
| **linear-clerk** | v1.1.0 | Linear integration for backlog, task, and project management using linearis CLI |
| **jira-cli** | v1.0.0 | Comprehensive toolkit for managing Jira issues, sprints, and workflows using ankitpokhrel/jira-cli |

### GitHub

| Plugin | Version | Description |
|--------|---------|-------------|
| **github-project-manager** | v1.1.0 | Comprehensive project-first workflow management using GitHub Projects V2 via gh CLI with automation and field management |
| **github-issues** | v1.1.1 | Elite agent for managing GitHub Issues using the gh CLI |
| **git-github-operations** | v1.0.0 | Streamlined git and GitHub workflow commands |

### Development Teams

| Plugin | Version | Description |
|--------|---------|-------------|
| **webapp-team** | v0.2.0 | Virtual web app development team with 13+ specialized agents for engineering, product, design, growth, and operations |
| **juce-dev-team** | v1.5.0 | Audio plugin development team with DAW compatibility testing, performance profiling, and architecture patterns |

### Content & Documentation

| Plugin | Version | Description |
|--------|---------|-------------|
| **astro-content-author** | v1.0.0 | Comprehensive toolkit for creating and managing content in Astro projects including collections, images, and data fetching |
| **documentation-tools** | v1.4.0 | Utilities for managing repository documentation with CLAUDE.md to AGENTS.md conversion |
| **apple-notes-cli** | v1.0.0 | Manage Apple Notes via command-line with agents for CRUD operations, organization, and export workflows |

### Meta

| Plugin | Version | Description |
|--------|---------|-------------|
| **agent-architect** | v1.0.0 | Tools and templates for designing Claude Code subagents with best practices and reusable patterns |

## Installation

### Add the Marketplace from GitHub

**In Claude Code:**

```
/plugin marketplace add yebot/rad-cc-plugins
```

### Install Plugins

**Install a specific plugin:**

```
/plugin install plugin-name@rad-cc-plugins
```

**Or, browse and install interactively:**

```
/plugin
```

### Get Updates

**To receive the latest plugin updates:**

```
/plugin marketplace update rad-cc-plugins
```

Run this command periodically to get new features, bug fixes, and improvements.

## Development

See [CLAUDE.md](CLAUDE.md) for detailed documentation on plugin architecture and development.
