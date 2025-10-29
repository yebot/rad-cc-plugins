# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a Claude Code plugin marketplace containing custom plugins that extend Claude Code functionality. The repository is structured as a collection of independent plugins, each providing agents, commands, skills, or hooks.

**Author Name**: Tobey Forsman (must be used for all plugin metadata)

## Repository Structure

```
rad-cc-plugins/
├── marketplace.json          # Registry of all plugins in this marketplace
├── plugins/
│   ├── git-github-operations/   # Git workflow automation
│   ├── agent-architect/         # Tools for designing subagents
│   ├── github-issues/           # GitHub Issues management via gh CLI
│   └── backlog-md/              # Task management with Backlog.md CLI
```

## Plugin Architecture

Each plugin follows this structure:

- `plugin.json` - Plugin metadata (name, version, author, components)
- `agents/*.md` - Subagent definitions (frontmatter + instructions)
- `commands/*.md` - Slash commands (prompts for specific workflows)
- `skills/*/SKILL.md` - Reusable skill modules
- `hooks/hooks.json` - Event-triggered shell commands
- `docs/*.md` - Plugin-specific documentation

### Plugin Metadata Requirements

All `plugin.json` files must include:

- `name`: kebab-case plugin identifier
- `version`: Semantic version (e.g., "1.0.0")
- `description`: Clear description of plugin purpose
- `author`: Object with `name` and `email` fields (see example below)
- Component arrays: `agents`, `commands`, `skills` (as applicable)

### Agent Definition Format

Agents use YAML frontmatter followed by markdown instructions:

```yaml
---
name: agent-name
description: When to use this agent. Use PROACTIVELY after X.
tools: Read, Grep, Glob, Bash
model: inherit
color: blue
---
```

See `plugins/agent-architect/templates/claude-code-subagent-template.md` for the complete template.

## Development Workflow

### Creating New Plugins

1. Create directory under `plugins/{plugin-name}/`
2. Create `plugin.json` with required metadata (see Plugin Metadata Requirements)
3. Add components (agents/commands/skills/hooks)
4. Register in root `marketplace.json`

### Creating Agents

Use the `agent-composer` agent for guidance:

```
Use the agent-composer to help design a new agent for X
```

Or copy template from `plugins/agent-architect/templates/claude-code-subagent-template.md`

### Creating Commands

Commands are markdown files with instructions for Claude Code:

- Use clear section headers (## Instructions)
- Include step-by-step workflows
- Show command examples
- Note important warnings
- Include Definition of Done checklist

### Working with Hooks

The `backlog-md` plugin demonstrates advanced hook usage:

- `tool-use` events can block or warn on tool calls
- `user-prompt-submit` events can provide contextual reminders
- Hooks use bash commands with filter patterns

## Marketplace Registry

The `marketplace.json` file lists all available plugins:

```json
{
  "name": "rad-cc-plugins",
  "plugins": [
    {
      "name": "plugin-name",
      "source": "./plugins/plugin-name",
      "description": "Brief description",
      "version": "1.0.0",
      "author": {
        "name": "Tobey Forsman",
        "email": "tobeyforsman@gmail.com"
      }
    }
  ]
}
```

Keep this synchronized when adding/removing plugins.

## Important Patterns

### Multi-line Input (Bash/Zsh)

Use ANSI-C quoting for newlines in CLI commands:

```bash
backlog task edit 42 --plan $'1. First\n2. Second\n3. Third'
backlog task edit 42 --notes $'Line 1\nLine 2'
```

### Agent Delegation

Use "Use PROACTIVELY" in agent descriptions to enable automatic delegation:

```yaml
description: Expert at X. Use PROACTIVELY when Y occurs.
```

### Tool Restrictions

Agents specify only needed tools via `tools:` frontmatter (principle of least privilege).

## Working in This Repository

- No build/compile step - plugins are markdown and JSON
- No tests to run (documentation-based repository)
- Validation: Check JSON syntax and required metadata fields
- Follow naming conventions: kebab-case for files and identifiers
