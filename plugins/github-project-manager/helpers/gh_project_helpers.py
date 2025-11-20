#!/usr/bin/env python3
"""
GitHub Projects CLI Helper Module

Provides Python-based JSON processing and utilities for gh CLI operations,
eliminating shell escaping issues with jq and providing better error handling.

Usage:
    python3 gh_project_helpers.py [command] [args...]

Examples:
    python3 gh_project_helpers.py parse-project-list '{"projects": [...]}'
    python3 gh_project_helpers.py filter-items --status "In Progress" items.json
    python3 gh_project_helpers.py extract-field-id --field "Priority" fields.json
"""

import json
import sys
import subprocess
import argparse
from typing import Any, Dict, List, Optional, Union
from datetime import datetime, timedelta
from pathlib import Path


class GHProjectError(Exception):
    """Base exception for GitHub Project operations"""
    pass


class GHProjectHelpers:
    """Helper functions for GitHub Projects V2 CLI operations"""

    @staticmethod
    def run_gh_command(command: str, format_json: bool = True) -> Union[Dict, str]:
        """
        Run a gh CLI command and return parsed output.

        Args:
            command: The gh command to run (without 'gh' prefix)
            format_json: Whether to add --format json and parse the output

        Returns:
            Parsed JSON dict if format_json=True, raw string otherwise

        Raises:
            GHProjectError: If command fails
        """
        full_command = f"gh {command}"
        if format_json and "--format json" not in command:
            full_command += " --format json"

        try:
            result = subprocess.run(
                full_command,
                shell=True,
                capture_output=True,
                text=True,
                check=True
            )

            if format_json:
                return json.loads(result.stdout)
            return result.stdout

        except subprocess.CalledProcessError as e:
            error_msg = e.stderr if e.stderr else str(e)
            raise GHProjectError(f"Command failed: {full_command}\nError: {error_msg}")
        except json.JSONDecodeError as e:
            raise GHProjectError(f"Failed to parse JSON output: {e}")

    @staticmethod
    def parse_project_list(json_data: Union[str, List[Dict]]) -> List[Dict]:
        """
        Parse project list JSON and return formatted project info.

        Args:
            json_data: Raw JSON string or parsed list

        Returns:
            List of dicts with project info
        """
        if isinstance(json_data, str):
            data = json.loads(json_data)
        else:
            data = json_data

        projects = []
        for project in data:
            projects.append({
                'number': project.get('number'),
                'id': project.get('id'),
                'title': project.get('title'),
                'url': project.get('url'),
                'created': project.get('createdAt'),
                'updated': project.get('updatedAt')
            })

        return projects

    @staticmethod
    def filter_items(items: List[Dict], filters: Dict[str, Any]) -> List[Dict]:
        """
        Filter project items based on field values.

        Args:
            items: List of project items
            filters: Dict of field_name: expected_value pairs

        Returns:
            Filtered list of items

        Examples:
            filter_items(items, {'Status': 'In Progress', 'Priority': 'P1'})
            filter_items(items, {'Status': ['Backlog', 'Todo']})  # Multiple values
        """
        filtered = []

        for item in items:
            field_values = item.get('fieldValues', [])
            matches = True

            for field_name, expected_value in filters.items():
                # Handle both single value and list of values
                expected_values = expected_value if isinstance(expected_value, list) else [expected_value]

                # Find the field value in this item
                field_found = False
                for field_val in field_values:
                    if field_val.get('name') == field_name:
                        actual_value = field_val.get('name') or field_val.get('text') or field_val.get('number')
                        if actual_value in expected_values:
                            field_found = True
                            break

                if not field_found:
                    matches = False
                    break

            if matches:
                filtered.append(item)

        return filtered

    @staticmethod
    def filter_items_missing_field(items: List[Dict], field_name: str) -> List[Dict]:
        """
        Filter items that are missing a specific field value.

        Args:
            items: List of project items
            field_name: Name of the field to check

        Returns:
            Items without the specified field set
        """
        missing = []

        for item in items:
            field_values = item.get('fieldValues', [])
            has_field = any(fv.get('name') == field_name for fv in field_values)

            if not has_field:
                missing.append(item)

        return missing

    @staticmethod
    def extract_field_info(fields: List[Dict], field_name: str) -> Optional[Dict]:
        """
        Extract field ID and metadata for a specific field.

        Args:
            fields: List of project fields from gh project field-list
            field_name: Name of the field to find

        Returns:
            Dict with field info or None if not found

        Example return:
            {
                'id': 'PVTF_...',
                'name': 'Priority',
                'dataType': 'SINGLE_SELECT',
                'options': [
                    {'id': 'abc123', 'name': 'P0'},
                    {'id': 'def456', 'name': 'P1'}
                ]
            }
        """
        for field in fields:
            if field.get('name') == field_name:
                return {
                    'id': field.get('id'),
                    'name': field.get('name'),
                    'dataType': field.get('dataType'),
                    'options': field.get('options', [])
                }
        return None

    @staticmethod
    def get_option_id(field_info: Dict, option_name: str) -> Optional[str]:
        """
        Get the option ID for a single-select field value.

        Args:
            field_info: Field info dict from extract_field_info()
            option_name: Name of the option (e.g., 'P1', 'In Progress')

        Returns:
            Option ID string or None if not found
        """
        options = field_info.get('options', [])
        for option in options:
            if option.get('name') == option_name:
                return option.get('id')
        return None

    @staticmethod
    def group_items_by_field(items: List[Dict], field_name: str) -> Dict[str, List[Dict]]:
        """
        Group items by a field value (e.g., Status, Priority).

        Args:
            items: List of project items
            field_name: Name of field to group by

        Returns:
            Dict mapping field values to lists of items

        Example:
            {
                'In Progress': [item1, item2],
                'Done': [item3, item4],
                'Backlog': [item5]
            }
        """
        groups = {}

        for item in items:
            field_value = None

            for fv in item.get('fieldValues', []):
                if fv.get('name') == field_name:
                    field_value = fv.get('name') or fv.get('text') or str(fv.get('number', ''))
                    break

            if field_value is None:
                field_value = 'Unset'

            if field_value not in groups:
                groups[field_value] = []

            groups[field_value].append(item)

        return groups

    @staticmethod
    def count_by_field(items: List[Dict], field_name: str) -> Dict[str, int]:
        """
        Count items by field value.

        Args:
            items: List of project items
            field_name: Name of field to count by

        Returns:
            Dict mapping field values to counts
        """
        groups = GHProjectHelpers.group_items_by_field(items, field_name)
        return {key: len(value) for key, value in groups.items()}

    @staticmethod
    def find_stale_items(items: List[Dict], days: int = 7, status_filter: Optional[List[str]] = None) -> List[Dict]:
        """
        Find items that haven't been updated in N days.

        Args:
            items: List of project items
            days: Number of days to consider stale
            status_filter: Only check items with these statuses (optional)

        Returns:
            List of stale items with additional metadata
        """
        threshold = datetime.now() - timedelta(days=days)
        stale = []

        for item in items:
            # Check status filter if provided
            if status_filter:
                item_status = None
                for fv in item.get('fieldValues', []):
                    if fv.get('name') == 'Status':
                        item_status = fv.get('name')
                        break

                if item_status not in status_filter:
                    continue

            # Check update timestamp
            updated_at_str = item.get('content', {}).get('updatedAt')
            if not updated_at_str:
                continue

            try:
                updated_at = datetime.fromisoformat(updated_at_str.replace('Z', '+00:00'))
                if updated_at < threshold:
                    days_stale = (datetime.now() - updated_at).days
                    stale_item = item.copy()
                    stale_item['days_stale'] = days_stale
                    stale_item['last_updated'] = updated_at_str.split('T')[0]
                    stale.append(stale_item)
            except (ValueError, AttributeError):
                continue

        return stale

    @staticmethod
    def format_item_for_display(item: Dict) -> Dict[str, str]:
        """
        Format an item for human-readable display.

        Args:
            item: Project item dict

        Returns:
            Dict with formatted fields
        """
        content = item.get('content', {})

        # Extract field values
        status = None
        priority = None

        for fv in item.get('fieldValues', []):
            if fv.get('name') == 'Status':
                status = fv.get('name')
            elif fv.get('name') == 'Priority':
                priority = fv.get('name')

        return {
            'id': item.get('id'),
            'number': content.get('number', 'draft'),
            'title': content.get('title', 'Untitled'),
            'type': content.get('type', 'Unknown'),
            'status': status or 'Unset',
            'priority': priority or 'Unset',
            'url': content.get('url', ''),
            'updated': content.get('updatedAt', '').split('T')[0] if content.get('updatedAt') else ''
        }

    @staticmethod
    def extract_owner_from_repo(repo: str) -> str:
        """
        Extract owner from repository string.

        Args:
            repo: Repository string (e.g., 'owner/repo', 'https://github.com/owner/repo')

        Returns:
            Owner name

        Examples:
            'owner/repo' -> 'owner'
            'https://github.com/owner/repo' -> 'owner'
        """
        if '/' not in repo:
            raise ValueError(f"Invalid repository format: {repo}")

        # Handle URL format
        if repo.startswith('http'):
            repo = repo.split('github.com/')[-1]

        # Extract owner
        parts = repo.split('/')
        return parts[0]

    @staticmethod
    def suggest_priority(title: str, body: str = "", labels: List[str] = None) -> tuple[str, str]:
        """
        Suggest a priority based on keywords in title, body, and labels.

        Args:
            title: Issue/item title
            body: Issue/item body
            labels: List of label names

        Returns:
            Tuple of (priority, reason)
        """
        if labels is None:
            labels = []

        combined_text = f"{title} {body}".lower()
        label_text = " ".join(labels).lower()

        # P0 indicators
        p0_keywords = ['critical', 'blocking', 'urgent', 'security', 'production down',
                       'data loss', 'outage', 'severe']
        if any(kw in combined_text or kw in label_text for kw in p0_keywords):
            return 'P0', 'Critical keywords detected (blocking, security, urgent)'

        # P1 indicators
        p1_keywords = ['bug', 'error', 'broken', 'failing', 'regression', 'important']
        if any(kw in combined_text or kw in label_text for kw in p1_keywords):
            return 'P1', 'Bug or high-priority keywords detected'

        # P2 indicators
        p2_keywords = ['enhancement', 'feature', 'improve', 'add']
        if any(kw in combined_text or kw in label_text for kw in p2_keywords):
            return 'P2', 'Enhancement or feature keywords detected'

        # Default to P3
        return 'P3', 'Standard priority (no high-urgency indicators)'


def main():
    """CLI interface for helper functions"""
    parser = argparse.ArgumentParser(description='GitHub Projects CLI Helper')
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # Filter items command
    filter_parser = subparsers.add_parser('filter-items', help='Filter project items')
    filter_parser.add_argument('items_file', help='JSON file with items')
    filter_parser.add_argument('--field', action='append', nargs=2, metavar=('NAME', 'VALUE'),
                               help='Field filter (can be used multiple times)')

    # Extract field ID command
    field_parser = subparsers.add_parser('extract-field', help='Extract field information')
    field_parser.add_argument('fields_file', help='JSON file with fields')
    field_parser.add_argument('--name', required=True, help='Field name to extract')

    # Count items command
    count_parser = subparsers.add_parser('count-by-field', help='Count items by field value')
    count_parser.add_argument('items_file', help='JSON file with items')
    count_parser.add_argument('--field', required=True, help='Field name to count by')

    # Find stale items command
    stale_parser = subparsers.add_parser('find-stale', help='Find stale items')
    stale_parser.add_argument('items_file', help='JSON file with items')
    stale_parser.add_argument('--days', type=int, default=7, help='Days threshold')
    stale_parser.add_argument('--status', action='append', help='Filter by status')

    # Format items command
    format_parser = subparsers.add_parser('format-items', help='Format items for display')
    format_parser.add_argument('items_file', help='JSON file with items')

    # Extract owner command
    owner_parser = subparsers.add_parser('extract-owner', help='Extract owner from repo string')
    owner_parser.add_argument('repo', help='Repository string')

    # Suggest priority command
    priority_parser = subparsers.add_parser('suggest-priority', help='Suggest priority for item')
    priority_parser.add_argument('--title', required=True, help='Item title')
    priority_parser.add_argument('--body', default='', help='Item body')
    priority_parser.add_argument('--labels', nargs='*', default=[], help='Item labels')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    helpers = GHProjectHelpers()

    try:
        if args.command == 'filter-items':
            with open(args.items_file) as f:
                data = json.load(f)

            items = data.get('items', data) if isinstance(data, dict) else data

            filters = {}
            if args.field:
                filters = {name: value for name, value in args.field}

            filtered = helpers.filter_items(items, filters)
            print(json.dumps(filtered, indent=2))

        elif args.command == 'extract-field':
            with open(args.fields_file) as f:
                fields = json.load(f)

            field_info = helpers.extract_field_info(fields, args.name)
            print(json.dumps(field_info, indent=2))

        elif args.command == 'count-by-field':
            with open(args.items_file) as f:
                data = json.load(f)

            items = data.get('items', data) if isinstance(data, dict) else data
            counts = helpers.count_by_field(items, args.field)
            print(json.dumps(counts, indent=2))

        elif args.command == 'find-stale':
            with open(args.items_file) as f:
                data = json.load(f)

            items = data.get('items', data) if isinstance(data, dict) else data
            stale = helpers.find_stale_items(items, args.days, args.status)
            print(json.dumps(stale, indent=2))

        elif args.command == 'format-items':
            with open(args.items_file) as f:
                data = json.load(f)

            items = data.get('items', data) if isinstance(data, dict) else data
            formatted = [helpers.format_item_for_display(item) for item in items]
            print(json.dumps(formatted, indent=2))

        elif args.command == 'extract-owner':
            owner = helpers.extract_owner_from_repo(args.repo)
            print(owner)

        elif args.command == 'suggest-priority':
            priority, reason = helpers.suggest_priority(args.title, args.body, args.labels)
            print(json.dumps({'priority': priority, 'reason': reason}, indent=2))

        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())