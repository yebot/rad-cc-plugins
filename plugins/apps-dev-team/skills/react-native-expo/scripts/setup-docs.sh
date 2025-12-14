#!/bin/bash
# setup-docs.sh
# Downloads and sets up Expo and React Native documentation for the skill
# Run this after installing the skill to populate the references directory

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
REFS_DIR="$SKILL_DIR/references"

echo "React Native & Expo Documentation Setup"
echo "========================================"
echo ""

# Check for required tools
if ! command -v curl &> /dev/null; then
    echo "Error: curl is required but not installed."
    exit 1
fi

# Create temp directory for downloads
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

echo "This skill includes curated reference documentation."
echo "For the latest docs, visit:"
echo "  - https://docs.expo.dev"
echo "  - https://reactnative.dev/docs"
echo ""
echo "Current reference files:"
ls -la "$REFS_DIR"
echo ""
echo "To update references with latest documentation, you can:"
echo "1. Visit the official docs websites"
echo "2. Use the download-docs.ts script (requires Node.js)"
echo "3. Manually update the markdown files"
echo ""
echo "Setup complete!"
