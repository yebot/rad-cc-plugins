#!/usr/bin/env python3
"""
Learning Loop Helper Module

Provides utilities for extracting, categorizing, and managing learnings
from Claude Code sessions.

Usage:
    python3 learning_helpers.py [command] [args...]

Commands:
    init                Initialize .learning-loop directory
    extract-commits     Extract learnings from recent commits
    extract-diff        Extract learnings from recent diffs
    categorize          Categorize a learning text
    find-targets        Find target files for a learning
    pending-count       Get count of pending suggestions
    add-suggestion      Add a new suggestion
    list-suggestions    List all pending suggestions
    mark-suggestion     Mark a suggestion status
"""

import json
import sys
import subprocess
import re
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any


class LearningCategory:
    """Learning category constants."""
    CAVEAT = "caveat"
    PATTERN = "pattern"
    ERROR_FIX = "error_fix"
    DEPENDENCY = "dependency"
    COMMAND = "command"
    ARCHITECTURE = "architecture"


class SuggestionStatus:
    """Suggestion status constants."""
    PENDING = "pending"
    APPLIED = "applied"
    SKIPPED = "skipped"
    DISCARDED = "discarded"


class LearningHelpers:
    """Helper functions for learning extraction and suggestion management."""

    STORAGE_DIR = ".learning-loop"
    SUGGESTIONS_FILE = ".learning-loop/pending-suggestions.json"
    HISTORY_FILE = ".learning-loop/history.json"

    # Category detection patterns
    CATEGORY_PATTERNS = {
        LearningCategory.CAVEAT: [
            r'\benv\b', r'\benvironment\b', r'\bconfig\b', r'\bsecret\b',
            r'\bgotcha\b', r'\bwatch out\b', r'\bcareful\b', r'\bmust\b',
            r'\brequired\b', r'\bimportant\b', r'\bnote\b', r'\bwarning\b'
        ],
        LearningCategory.ERROR_FIX: [
            r'\berror\b', r'\bfix\b', r'\bworkaround\b', r'\bhack\b',
            r'\bresolved\b', r'\bsolved\b', r'\bissue\b', r'\bbug\b',
            r'\bfailed\b', r'\bbroken\b'
        ],
        LearningCategory.DEPENDENCY: [
            r'\binstall\b', r'\bdependency\b', r'\bpackage\b', r'\bversion\b',
            r'\bnpm\b', r'\bpip\b', r'\brequires\b', r'\bupgrade\b',
            r'\blibrary\b', r'\bmodule\b'
        ],
        LearningCategory.PATTERN: [
            r'\bpattern\b', r'\bconvention\b', r'\bstyle\b', r'\bnaming\b',
            r'\bstandard\b', r'\bbest practice\b', r'\bapproach\b',
            r'\bprefer\b', r'\balways\b', r'\bnever\b'
        ],
        LearningCategory.COMMAND: [
            r'\bcommand\b', r'\bscript\b', r'\brun\b', r'\bnpm\b',
            r'\bpython\b', r'\bbash\b', r'\bshell\b', r'\bcli\b',
            r'\bexecute\b', r'\bterminal\b'
        ],
        LearningCategory.ARCHITECTURE: [
            r'\barchitecture\b', r'\bdesign\b', r'\bstructure\b',
            r'\bcomponent\b', r'\bmodule\b', r'\blayer\b', r'\bservice\b',
            r'\bapi\b', r'\bendpoint\b'
        ],
    }

    # Section mapping for targets
    SECTION_MAP = {
        LearningCategory.CAVEAT: "## Important Caveats",
        LearningCategory.PATTERN: "## Conventions & Patterns",
        LearningCategory.ERROR_FIX: "## Troubleshooting",
        LearningCategory.DEPENDENCY: "## Dependencies",
        LearningCategory.COMMAND: "## Common Commands",
        LearningCategory.ARCHITECTURE: "## Architecture",
    }

    @staticmethod
    def init_storage() -> Dict[str, Any]:
        """Initialize .learning-loop directory and files."""
        storage_path = Path(LearningHelpers.STORAGE_DIR)
        storage_path.mkdir(exist_ok=True)

        suggestions_path = Path(LearningHelpers.SUGGESTIONS_FILE)
        history_path = Path(LearningHelpers.HISTORY_FILE)

        created = []

        if not suggestions_path.exists():
            initial_suggestions = {
                "suggestions": [],
                "created": datetime.now().isoformat(),
                "updated": datetime.now().isoformat()
            }
            with open(suggestions_path, 'w') as f:
                json.dump(initial_suggestions, f, indent=2)
            created.append(str(suggestions_path))

        if not history_path.exists():
            initial_history = {
                "applied": [],
                "discarded": [],
                "created": datetime.now().isoformat()
            }
            with open(history_path, 'w') as f:
                json.dump(initial_history, f, indent=2)
            created.append(str(history_path))

        return {
            "storage_dir": str(storage_path),
            "created_files": created,
            "status": "initialized"
        }

    @staticmethod
    def extract_from_commits(since: str = "2 hours ago") -> List[Dict]:
        """Extract potential learnings from recent git commits."""
        learnings = []

        try:
            # Get recent commits with messages
            result = subprocess.run(
                ["git", "log", f"--since={since}", "--format=%H|%s|%b|||"],
                capture_output=True, text=True, check=True
            )

            entries = result.stdout.split("|||")

            for entry in entries:
                entry = entry.strip()
                if not entry or "|" not in entry:
                    continue

                parts = entry.split("|", 2)
                if len(parts) < 2:
                    continue

                commit_hash = parts[0][:8]
                subject = parts[1].strip()
                body = parts[2].strip() if len(parts) > 2 else ""

                full_message = f"{subject}\n{body}".strip()

                # Detect category from commit message
                category, confidence = LearningHelpers.categorize_learning(full_message)

                # Boost confidence for certain commit prefixes
                if re.match(r'^(fix|bugfix|hotfix):', subject, re.I):
                    category = LearningCategory.ERROR_FIX
                    confidence = max(confidence, 0.85)
                elif re.match(r'^(feat|feature):', subject, re.I):
                    confidence = max(confidence, 0.6)
                elif re.match(r'^(docs|doc):', subject, re.I):
                    category = LearningCategory.PATTERN
                    confidence = max(confidence, 0.7)
                elif re.match(r'^(chore|deps):', subject, re.I):
                    category = LearningCategory.DEPENDENCY
                    confidence = max(confidence, 0.75)

                if confidence >= 0.5:
                    learnings.append({
                        "source": "commit",
                        "source_ref": commit_hash,
                        "category": category,
                        "content": subject,
                        "details": body if body else None,
                        "confidence": round(confidence, 2),
                        "extracted_at": datetime.now().isoformat()
                    })

        except subprocess.CalledProcessError:
            pass
        except FileNotFoundError:
            # git not available
            pass

        return learnings

    @staticmethod
    def extract_from_diff(base: str = "HEAD~5") -> List[Dict]:
        """Extract learnings from recent code changes."""
        learnings = []

        try:
            # Find files changed multiple times (iterations indicate learning)
            result = subprocess.run(
                ["git", "log", f"{base}..HEAD", "--name-only", "--format="],
                capture_output=True, text=True, check=True
            )

            files = [f.strip() for f in result.stdout.strip().split("\n") if f.strip()]
            file_counts: Dict[str, int] = {}
            for f in files:
                file_counts[f] = file_counts.get(f, 0) + 1

            # Files touched 3+ times might indicate iteration/learning
            iterated_files = [f for f, c in file_counts.items() if c >= 3]
            if iterated_files:
                learnings.append({
                    "source": "diff_analysis",
                    "source_ref": f"{base}..HEAD",
                    "category": LearningCategory.CAVEAT,
                    "content": f"Multiple iterations on: {', '.join(iterated_files[:5])}",
                    "details": "These files were modified multiple times, possibly indicating tricky areas",
                    "confidence": 0.55,
                    "files": iterated_files[:10],
                    "extracted_at": datetime.now().isoformat()
                })

            # Check for TODO/FIXME/HACK comments added
            diff_result = subprocess.run(
                ["git", "diff", base, "--"],
                capture_output=True, text=True
            )

            todo_patterns = [
                (r'\+.*TODO:\s*(.+)', LearningCategory.CAVEAT, 0.8),
                (r'\+.*FIXME:\s*(.+)', LearningCategory.ERROR_FIX, 0.85),
                (r'\+.*HACK:\s*(.+)', LearningCategory.CAVEAT, 0.9),
                (r'\+.*NOTE:\s*(.+)', LearningCategory.CAVEAT, 0.7),
                (r'\+.*XXX:\s*(.+)', LearningCategory.CAVEAT, 0.75),
            ]

            for pattern, category, confidence in todo_patterns:
                matches = re.findall(pattern, diff_result.stdout)
                for match in matches:
                    learnings.append({
                        "source": "diff_comment",
                        "source_ref": f"{base}..HEAD",
                        "category": category,
                        "content": match.strip(),
                        "confidence": confidence,
                        "extracted_at": datetime.now().isoformat()
                    })

            # Check for new dependencies added (package.json, requirements.txt, etc.)
            if "package.json" in diff_result.stdout:
                dep_matches = re.findall(r'\+\s*"([^"]+)":\s*"([^"]+)"', diff_result.stdout)
                for name, version in dep_matches[:5]:  # Limit to avoid noise
                    if not name.startswith("@types/"):  # Skip type definitions
                        learnings.append({
                            "source": "diff_dependency",
                            "source_ref": "package.json",
                            "category": LearningCategory.DEPENDENCY,
                            "content": f"Added dependency: {name}@{version}",
                            "confidence": 0.8,
                            "extracted_at": datetime.now().isoformat()
                        })

        except subprocess.CalledProcessError:
            pass
        except FileNotFoundError:
            pass

        return learnings

    @staticmethod
    def categorize_learning(text: str) -> Tuple[str, float]:
        """Categorize a learning based on content analysis."""
        text_lower = text.lower()

        scores: Dict[str, float] = {cat: 0.0 for cat in LearningHelpers.CATEGORY_PATTERNS}

        for category, patterns in LearningHelpers.CATEGORY_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    scores[category] += 0.15

        # Find highest scoring category
        best_category = max(scores, key=scores.get)
        best_score = scores[best_category]

        # Normalize confidence
        confidence = min(0.95, 0.4 + best_score)

        # Default to caveat if no strong signal
        if best_score < 0.15:
            return LearningCategory.CAVEAT, 0.4

        return best_category, round(confidence, 2)

    @staticmethod
    def find_target_files(category: str, content: str) -> List[Dict]:
        """Find appropriate target files for a learning."""
        targets = []

        # Check for root CLAUDE.md
        if Path("CLAUDE.md").exists():
            targets.append({
                "path": "CLAUDE.md",
                "section": LearningHelpers.SECTION_MAP.get(category, "## Notes"),
                "priority": "primary",
                "type": "claude_md"
            })

        # Find subdirectory CLAUDE.md files
        try:
            result = subprocess.run(
                ["find", ".", "-name", "CLAUDE.md",
                 "-not", "-path", "./node_modules/*",
                 "-not", "-path", "./.git/*"],
                capture_output=True, text=True
            )

            for claude_file in result.stdout.strip().split("\n"):
                if claude_file and claude_file != "./CLAUDE.md":
                    dir_name = str(Path(claude_file).parent.name)
                    # Check if content is related to this directory
                    if dir_name.lower() in content.lower():
                        targets.append({
                            "path": claude_file.lstrip("./"),
                            "section": LearningHelpers.SECTION_MAP.get(category, "## Notes"),
                            "priority": "secondary",
                            "type": "claude_md"
                        })
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

        # Find relevant agent files for architecture/pattern learnings
        if category in [LearningCategory.ARCHITECTURE, LearningCategory.PATTERN]:
            try:
                result = subprocess.run(
                    ["find", ".", "-path", "*/agents/*.md",
                     "-not", "-path", "./node_modules/*"],
                    capture_output=True, text=True
                )

                for agent_file in result.stdout.strip().split("\n")[:3]:
                    if agent_file:
                        targets.append({
                            "path": agent_file.lstrip("./"),
                            "section": "## Guardrails",
                            "priority": "tertiary",
                            "type": "agent"
                        })
            except (subprocess.CalledProcessError, FileNotFoundError):
                pass

        return targets

    @staticmethod
    def generate_suggestion_id(content: str) -> str:
        """Generate a unique suggestion ID."""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        content_hash = hashlib.md5(content.encode()).hexdigest()[:6]
        return f"sug_{timestamp}_{content_hash}"

    @staticmethod
    def create_suggestion(learning: Dict, target: Dict) -> Dict:
        """Create a structured suggestion from a learning."""
        category = learning.get("category", LearningCategory.CAVEAT)
        content = learning.get("content", "")

        # Calculate priority
        confidence = learning.get("confidence", 0.5)
        is_primary = target.get("priority") == "primary"
        is_high_impact = category in [LearningCategory.CAVEAT, LearningCategory.ERROR_FIX]

        if confidence >= 0.8 and is_primary and is_high_impact:
            priority = "high"
        elif confidence >= 0.6 or is_primary:
            priority = "medium"
        else:
            priority = "low"

        # Generate diff preview
        section = target.get("section", "## Notes")
        if category == LearningCategory.COMMAND:
            formatted = f"```bash\n{content}\n```"
        elif category == LearningCategory.ERROR_FIX:
            formatted = f"**Issue:** {content}\n**Solution:** [Add solution details]"
        else:
            formatted = f"- {content}"

        diff = f"{section}\n\n+ {formatted}"

        return {
            "id": LearningHelpers.generate_suggestion_id(content),
            "created": datetime.now().isoformat(),
            "learning": learning,
            "target": target,
            "status": SuggestionStatus.PENDING,
            "priority": priority,
            "diff": diff
        }

    @staticmethod
    def save_suggestion(suggestion: Dict) -> Dict:
        """Save a suggestion to pending file."""
        LearningHelpers.init_storage()

        suggestions_path = Path(LearningHelpers.SUGGESTIONS_FILE)
        with open(suggestions_path, 'r') as f:
            data = json.load(f)

        data["suggestions"].append(suggestion)
        data["updated"] = datetime.now().isoformat()

        with open(suggestions_path, 'w') as f:
            json.dump(data, f, indent=2)

        return {"status": "saved", "id": suggestion["id"]}

    @staticmethod
    def get_pending_suggestions() -> List[Dict]:
        """Get all pending suggestions."""
        try:
            with open(LearningHelpers.SUGGESTIONS_FILE, 'r') as f:
                data = json.load(f)
            return [s for s in data.get("suggestions", [])
                    if s.get("status") == SuggestionStatus.PENDING]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @staticmethod
    def get_pending_count() -> int:
        """Get count of pending suggestions."""
        return len(LearningHelpers.get_pending_suggestions())

    @staticmethod
    def mark_suggestion(suggestion_id: str, status: str) -> Dict:
        """Mark a suggestion as applied, skipped, or discarded."""
        try:
            suggestions_path = Path(LearningHelpers.SUGGESTIONS_FILE)
            with open(suggestions_path, 'r') as f:
                data = json.load(f)

            found = False
            for suggestion in data.get("suggestions", []):
                if suggestion.get("id") == suggestion_id:
                    suggestion["status"] = status
                    suggestion["resolved_at"] = datetime.now().isoformat()
                    found = True

                    # If applied or discarded, move to history
                    if status in [SuggestionStatus.APPLIED, SuggestionStatus.DISCARDED]:
                        history_path = Path(LearningHelpers.HISTORY_FILE)
                        if history_path.exists():
                            with open(history_path, 'r') as hf:
                                history = json.load(hf)
                        else:
                            history = {"applied": [], "discarded": []}

                        if status == SuggestionStatus.APPLIED:
                            history["applied"].append(suggestion)
                        else:
                            history["discarded"].append(suggestion)

                        with open(history_path, 'w') as hf:
                            json.dump(history, hf, indent=2)
                    break

            if found:
                data["updated"] = datetime.now().isoformat()
                with open(suggestions_path, 'w') as f:
                    json.dump(data, f, indent=2)
                return {"status": "updated", "id": suggestion_id, "new_status": status}
            else:
                return {"status": "error", "message": f"Suggestion {suggestion_id} not found"}

        except Exception as e:
            return {"status": "error", "message": str(e)}

    @staticmethod
    def clear_resolved() -> Dict:
        """Remove all non-pending suggestions from the file."""
        try:
            suggestions_path = Path(LearningHelpers.SUGGESTIONS_FILE)
            with open(suggestions_path, 'r') as f:
                data = json.load(f)

            original_count = len(data.get("suggestions", []))
            data["suggestions"] = [s for s in data.get("suggestions", [])
                                   if s.get("status") == SuggestionStatus.PENDING]
            removed_count = original_count - len(data["suggestions"])

            data["updated"] = datetime.now().isoformat()
            with open(suggestions_path, 'w') as f:
                json.dump(data, f, indent=2)

            return {"status": "cleared", "removed": removed_count}

        except Exception as e:
            return {"status": "error", "message": str(e)}


def main():
    """CLI interface for learning helpers."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Learning Loop Helper - Extract and manage learnings',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Init command
    subparsers.add_parser('init', help='Initialize .learning-loop storage')

    # Extract from commits
    extract_commits = subparsers.add_parser('extract-commits',
                                            help='Extract learnings from commits')
    extract_commits.add_argument('--since', default='2 hours ago',
                                 help='Time range (default: "2 hours ago")')

    # Extract from diff
    extract_diff = subparsers.add_parser('extract-diff',
                                         help='Extract learnings from diff')
    extract_diff.add_argument('--base', default='HEAD~5',
                              help='Base commit (default: HEAD~5)')

    # Categorize
    categorize = subparsers.add_parser('categorize',
                                       help='Categorize a learning text')
    categorize.add_argument('text', help='Text to categorize')

    # Find targets
    find_targets = subparsers.add_parser('find-targets',
                                         help='Find target files for learning')
    find_targets.add_argument('--category', required=True,
                              help='Learning category')
    find_targets.add_argument('--content', required=True,
                              help='Learning content')

    # Pending count
    subparsers.add_parser('pending-count', help='Get pending suggestion count')

    # List suggestions
    subparsers.add_parser('list-suggestions', help='List all pending suggestions')

    # Add suggestion
    add_suggestion = subparsers.add_parser('add-suggestion',
                                           help='Add a new suggestion')
    add_suggestion.add_argument('--category', required=True,
                                help='Learning category')
    add_suggestion.add_argument('--content', required=True,
                                help='Learning content')
    add_suggestion.add_argument('--target', default='CLAUDE.md',
                                help='Target file path')
    add_suggestion.add_argument('--confidence', type=float, default=0.7,
                                help='Confidence score (0-1)')

    # Mark suggestion
    mark_suggestion = subparsers.add_parser('mark-suggestion',
                                            help='Mark suggestion status')
    mark_suggestion.add_argument('id', help='Suggestion ID')
    mark_suggestion.add_argument('status',
                                 choices=['pending', 'applied', 'skipped', 'discarded'],
                                 help='New status')

    # Clear resolved
    subparsers.add_parser('clear-resolved',
                          help='Remove resolved suggestions from pending file')

    args = parser.parse_args()

    # Execute command
    if args.command == 'init':
        result = LearningHelpers.init_storage()
        print(json.dumps(result, indent=2))

    elif args.command == 'extract-commits':
        learnings = LearningHelpers.extract_from_commits(args.since)
        print(json.dumps(learnings, indent=2))

    elif args.command == 'extract-diff':
        learnings = LearningHelpers.extract_from_diff(args.base)
        print(json.dumps(learnings, indent=2))

    elif args.command == 'categorize':
        category, confidence = LearningHelpers.categorize_learning(args.text)
        print(json.dumps({"category": category, "confidence": confidence}, indent=2))

    elif args.command == 'find-targets':
        targets = LearningHelpers.find_target_files(args.category, args.content)
        print(json.dumps(targets, indent=2))

    elif args.command == 'pending-count':
        print(LearningHelpers.get_pending_count())

    elif args.command == 'list-suggestions':
        suggestions = LearningHelpers.get_pending_suggestions()
        print(json.dumps(suggestions, indent=2))

    elif args.command == 'add-suggestion':
        learning = {
            "source": "user",
            "category": args.category,
            "content": args.content,
            "confidence": args.confidence,
            "extracted_at": datetime.now().isoformat()
        }
        targets = LearningHelpers.find_target_files(args.category, args.content)
        target = next((t for t in targets if t["path"] == args.target),
                      targets[0] if targets else {"path": args.target, "section": "## Notes"})
        suggestion = LearningHelpers.create_suggestion(learning, target)
        result = LearningHelpers.save_suggestion(suggestion)
        print(json.dumps(result, indent=2))

    elif args.command == 'mark-suggestion':
        result = LearningHelpers.mark_suggestion(args.id, args.status)
        print(json.dumps(result, indent=2))

    elif args.command == 'clear-resolved':
        result = LearningHelpers.clear_resolved()
        print(json.dumps(result, indent=2))

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
