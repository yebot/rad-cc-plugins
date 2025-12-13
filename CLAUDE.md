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
│   ├── backlog-md-cli/           # Task management with Backlog.md CLI
│   └── astro-content-author/    # Astro content creation and management
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

### Plugin.json Schema (CRITICAL)

**Adding invalid fields or structures causes "Invalid input" validation errors.** Always reference working plugins when unsure.

**Agents array** - each object must have:
```json
{
  "name": "agent-name",
  "source": "./agents/agent-name.md",
  "description": "Brief description"
}
```
- Use `source` (webapp-team style) OR `path` (simbl style) - both work
- All three fields are required

**Skills array** - each object must have:
```json
{
  "name": "skill-name",
  "source": "./skills/skill-name"
}
```
- Points to directory containing `SKILL.md`
- `description` field is optional for skills

**Commands array** - each object must have:
```json
{
  "name": "command-name",
  "source": "./commands/command-name.md",
  "description": "Brief description"
}
```

**Reference plugins for validation**:
- `plugins/webapp-team/plugin.json` - comprehensive example with agents, commands, skills
- `plugins/simbl/plugin.json` - example using `path` instead of `source`

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

### Agent Frontmatter Schema (CRITICAL)

**ONLY use these validated frontmatter fields** in agent `.md` files. Adding non-standard fields causes plugin validation errors ("agents: Invalid input").

**Standard Fields** (always safe):
- `name` - Agent identifier (required)
- `description` - When to use this agent (required)
- `tools` - Comma-separated tool list (required)
- `model` - Always use `inherit` (required)

**Optional Fields** (validated in working plugins):
- `color` - Display color (e.g., `"#2563eb"`, `blue`)
- `role` - Role title for display
- `expertise` - List of expertise areas
- `triggers` - List of trigger conditions

**INVALID Fields** (will cause validation errors):
- ❌ `skills` - Not a valid agent frontmatter field
- ❌ Any other custom fields not listed above

**When in doubt**: Compare your agent frontmatter against working agents in `plugins/webapp-team/agents/` or `plugins/simbl/agents/`.

### Command Definition Format

Commands use YAML frontmatter followed by markdown instructions:

```yaml
---
name: command-name
description: Brief description of what this command does
tools: Bash, Read, Write
model: inherit
---
```

### Model Specification Guidelines

**IMPORTANT**: Always use `model: inherit` in agent and command frontmatter.

**Valid Model Specifications**:
- `model: inherit` - **RECOMMENDED**: Inherits from parent/user settings
- `model: claude-sonnet-4-5-20250929` - Full model ID (rarely needed)
- Omit field entirely - Uses default model

**Invalid Model Specifications** (will cause 404 errors):
- ❌ `model: sonnet` - Not a valid model identifier
- ❌ `model: opus` - Not a valid model identifier
- ❌ `model: haiku` - Not a valid model identifier

**Why `inherit` is preferred**:
- Respects user's model preferences
- Easier to maintain across plugin updates
- Consistent with marketplace standards
- Flexible for different deployment contexts

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

The `backlog-md-cli` plugin demonstrates advanced hook usage:

- `tool-use` events can block or warn on tool calls
- `user-prompt-submit` events can provide contextual reminders
- Hooks use bash commands with filter patterns

### Updating Plugins (Semantic Versioning)

**IMPORTANT**: When making changes to any plugin, always update version numbers using semantic versioning:

#### Version Format: `MAJOR.MINOR.PATCH`

- **PATCH** (`1.0.0` → `1.0.1`): Bug fixes, typo corrections, minor tweaks
  - No breaking changes
  - No new features

- **MINOR** (`1.0.0` → `1.1.0`): New features, new commands, new skills
  - Backward compatible
  - Adds functionality

- **MAJOR** (`1.0.0` → `2.0.0`): Breaking changes
  - Changes to existing APIs or workflows
  - Removal of features
  - Incompatible updates

#### Steps to Update a Plugin

1. **Modify the plugin files** (agents, commands, skills, hooks)

2. **Update version in plugin's `plugin.json`**:
   ```json
   {
     "name": "github-issues",
     "version": "1.1.0",  // Increment appropriately
     ...
   }
   ```

3. **Update version in root `marketplace.json`**:
   ```json
   {
     "plugins": [
       {
         "name": "github-issues",
         "version": "1.1.0",  // Must match plugin.json
         ...
       }
     ]
   }
   ```

4. **Sync to `.claude-plugin/marketplace.json`**:
   ```bash
   cp marketplace.json .claude-plugin/marketplace.json
   ```

5. **Commit and push changes**:
   ```bash
   git add plugins/<plugin-name>/ marketplace.json .claude-plugin/marketplace.json
   git commit -m "feat/fix/chore(<plugin-name>): description"
   git push
   ```

#### Publishing Plugin Updates

**IMPORTANT**: After creating or updating any plugin, **always ask the user** if they want to immediately publish the changes to GitHub so the plugin becomes available to users.

Prompt the user with:
```
Would you like me to stage, commit, and push these plugin changes to GitHub?
This will make the plugin immediately available for users to install/update.

[Yes/No]
```

If the user says yes:
1. Stage the relevant files
2. Create a descriptive commit message
3. Push to the remote repository

**Why this matters**: Plugins are only available to users after they're committed and pushed to the git repository. Uncommitted changes exist only in your local working directory and won't appear when users update their marketplace.

#### When to Update Versions

- **Always** update versions when making user-facing changes
- **Don't** update versions for documentation-only changes (unless docs affect usage)
- **Test** changes locally before incrementing version
- **Document** changes in commit messages

Users will receive updates when they run:
```bash
/plugin marketplace update rad-cc-plugins
```

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

## Plugin Helper Modules Pattern

Some plugins include helper modules for complex operations:

### Python Helper Modules

When plugins need reliable JSON processing or complex logic, create Python helper modules in `plugins/{name}/helpers/`:

**Example**: `github-project-manager/helpers/gh_project_helpers.py`
- Provides reusable Python functions for JSON processing
- Eliminates shell escaping issues with `jq`
- Includes CLI interface for standalone usage
- Can be imported as module or called directly

**Pattern**:
```python
#!/usr/bin/env python3
class PluginHelpers:
    @staticmethod
    def helper_method(data):
        # Implementation
        pass

if __name__ == '__main__':
    # CLI interface
    pass
```

**Usage in commands**:
```bash
# Direct Python processing (no jq escaping issues)
gh project list --format json | python3 -c "
import json, sys
data = json.load(sys.stdin)
# Process data...
"

# Or use helper module
python3 helpers/gh_project_helpers.py filter-items items.json --field Status "In Progress"
```

### Bash Helper Scripts

For reusable bash functions, create sourced helper scripts:

**Example**: `github-project-manager/helpers/gh_status_helpers.sh`
```bash
#!/usr/bin/env bash
source helpers/gh_status_helpers.sh

# Use helper functions
save_items_json "$ITEMS"
count_by_field "Status"
get_stale_items 7
```

**When to use helpers**:
- Complex JSON processing with nested objects
- Repeated operations across multiple commands
- Logic that benefits from proper error handling
- Operations that would be fragile in bash/jq

## Hook Patterns and Use Cases

Hooks enable event-driven workflows. See `plugins/backlog-md/hooks/hooks.json` for a working example.

### Hooks.json Schema (CRITICAL)

**The hooks schema requires a specific nested structure.** Using the wrong format causes validation errors.

**Correct Structure**:
```json
{
  "PreToolUse": [
    {
      "matcher": "Bash(git commit*)",
      "hooks": [
        {
          "type": "command",
          "command": "echo 'Warning message'"
        }
      ]
    }
  ],
  "PostToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "command",
          "command": "echo 'Post-tool notification'"
        }
      ]
    }
  ],
  "UserPromptSubmit": [
    {
      "matcher": "",
      "hooks": [
        {
          "type": "command",
          "command": "echo 'Prompt reminder'"
        }
      ]
    }
  ]
}
```

**Key Requirements**:
- NO wrapper `"hooks": { }` at top level - hook types are at root
- Use `matcher` NOT `filter` for tool matching patterns
- Each hook type item MUST have a `hooks` array inside it
- Each hook in the array needs `type: "command"` and `command` string
- Use `|` for multiple matchers (e.g., `"Write|Edit|MultiEdit"`)
- Empty `matcher: ""` matches all (useful for UserPromptSubmit)

**INVALID Structure** (causes "hooks: Required" errors):
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "filter": "...",
        "command": "bash",
        "args": ["-c", "..."]
      }
    ]
  }
}
```

**Reference**: `plugins/backlog-md/hooks/hooks.json` for working example

### Hook Best Practices

1. **Enforcement**: Use `exit 1` in command to block operations
2. **Guidance**: Use warnings (no exit) to suggest better alternatives
3. **Validation**: Use PostToolUse to check after file modifications
4. **Context**: Use UserPromptSubmit for workflow reminders
5. **Matcher patterns**: Use glob syntax for tools (e.g., `Bash(git *)`, `Write|Edit`)

## Common Development Tasks

### Validate Plugin Structure
```bash
# Check JSON syntax
cat plugins/plugin-name/plugin.json | jq .

# Verify marketplace registration
cat marketplace.json | jq '.plugins[] | select(.name=="plugin-name")'

# Check helper script executability
ls -l plugins/*/helpers/*
```

### Sync Marketplace Registry
```bash
# Always sync after updating marketplace.json
cp marketplace.json .claude-plugin/marketplace.json
```

### Test Plugin Locally
```bash
# Install plugin from local path
/plugin install /path/to/plugin-dir

# Or test specific components
# Agents: Available via Task tool
# Commands: Available as /command-name
# Skills: Available via Skill tool
```

## Working in This Repository

- No build/compile step - plugins are markdown and JSON
- No unit tests - validation through JSON syntax and field checks
- Follow naming conventions: kebab-case for files and identifiers
- All helper scripts should be executable (chmod +x)
- After every successful push to github, provide the user with one-shot commands to update the plugin or marketplace in their other working sessions.