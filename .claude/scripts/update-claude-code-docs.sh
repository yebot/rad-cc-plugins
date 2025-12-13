#!/bin/bash
# Fetch Claude Code documentation and save to docs/

set -e

DOCS_DIR="docs"
mkdir -p "$DOCS_DIR"

echo "Fetching Claude Code documentation..."

curl -sL "https://code.claude.com/docs/en/skills.md" -o "$DOCS_DIR/claude-code-skills-reference.md"
echo "✓ claude-code-skills-reference.md"

curl -sL "https://code.claude.com/docs/en/sub-agents.md" -o "$DOCS_DIR/claude-code-sub-agents-reference.md"
echo "✓ claude-code-sub-agents-reference.md"

curl -sL "https://code.claude.com/docs/en/plugins.md" -o "$DOCS_DIR/claude-code-plugins-reference.md"
echo "✓ claude-code-plugins-reference.md"

curl -sL "https://code.claude.com/docs/en/hooks-guide.md" -o "$DOCS_DIR/claude-code-hooks-guide.md"
echo "✓ claude-code-hooks-guide.md"

curl -sL "https://code.claude.com/docs/en/slash-commands.md" -o "$DOCS_DIR/claude-code-slash-commands-reference.md"
echo "✓ claude-code-slash-commands-reference.md"

echo ""
echo "Documentation update complete!"
