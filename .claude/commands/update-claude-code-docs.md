---
description: Fetch latest Claude Code documentation from code.claude.com and save to docs/
allowed-tools: Bash(bash:*)
---

# Update Claude Code Documentation

Run the documentation update script:

```bash
bash .claude/scripts/update-claude-code-docs.sh
```

This fetches and saves:
- skills.md → docs/claude-code-skills-reference.md
- sub-agents.md → docs/claude-code-sub-agents-reference.md
- plugins.md → docs/claude-code-plugins-reference.md
- hooks-guide.md → docs/claude-code-hooks-guide.md
- slash-commands.md → docs/claude-code-slash-commands-reference.md
