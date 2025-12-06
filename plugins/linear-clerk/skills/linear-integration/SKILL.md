# Linear Integration

Use `linearis` CLI for Linear task management. Issue IDs support both UUID and identifiers like `ABC-123`.

## Quick Start

```bash
linearis issues list -l 10          # Recent issues
linearis issues read ABC-123        # Issue details
linearis issues search "bug"        # Search issues
linearis issues update ABC-123 -s "In Progress"  # Update status
```

## Workflow

1. Check `linearis issues list` before starting work
2. Update issue status when you begin (`In Progress`)
3. Add comments for significant progress
4. Link PRs in comments when opening

---

## Issues

### List Issues

```bash
linearis issues list [options]
```

| Option | Description |
|--------|-------------|
| `-l, --limit <n>` | Limit results (default: 25) |

### Read Issue

```bash
linearis issues read <issueId>
```

### Create Issue

```bash
linearis issues create [options] <title>
```

| Option | Description |
|--------|-------------|
| `-d, --description <desc>` | Issue description |
| `-a, --assignee <id>` | Assign to user ID |
| `-p, --priority <1-4>` | Priority level |
| `--team <team>` | Team key, name, or ID (required if not specified) |
| `--project <project>` | Add to project (name or ID) |
| `--labels <labels>` | Labels (comma-separated names or IDs) |
| `--status <status>` | Status name or ID |
| `--cycle <cycle>` | Cycle name or ID (requires --team) |
| `--project-milestone <milestone>` | Project milestone (requires --project) |
| `--parent-ticket <parentId>` | Parent issue ID or identifier |

### Update Issue

```bash
linearis issues update [options] <issueId>
```

| Option | Description |
|--------|-------------|
| `-t, --title <title>` | New title |
| `-d, --description <desc>` | New description |
| `-s, --state <state>` | New state name or ID |
| `-p, --priority <1-4>` | New priority |
| `--assignee <id>` | New assignee ID |
| `--project <project>` | New project (name or ID) |

**Labels:**

| Option | Description |
|--------|-------------|
| `--labels <labels>` | Labels (comma-separated names or IDs) |
| `--label-by <mode>` | How to apply: `adding` (default) or `overwriting` |
| `--clear-labels` | Remove all labels |

**Relationships:**

| Option | Description |
|--------|-------------|
| `--parent-ticket <id>` | Set parent issue |
| `--clear-parent-ticket` | Clear parent |
| `--project-milestone <milestone>` | Set milestone |
| `--clear-project-milestone` | Clear milestone |
| `--cycle <cycle>` | Set cycle |
| `--clear-cycle` | Clear cycle |

### Search Issues

```bash
linearis issues search [options] <query>
```

| Option | Description |
|--------|-------------|
| `--team <team>` | Filter by team |
| `--assignee <id>` | Filter by assignee ID |
| `--project <project>` | Filter by project |
| `--states <states>` | Filter by states (comma-separated) |
| `-l, --limit <n>` | Limit results (default: 10) |

---

## Comments

### Create Comment

```bash
linearis comments create [options] <issueId>
```

| Option | Description |
|--------|-------------|
| `--body <body>` | Comment body (required) |

---

## Cycles

### List Cycles

```bash
linearis cycles list [options]
```

| Option | Description |
|--------|-------------|
| `--team <team>` | Team key, name, or ID |
| `--active` | Only active cycles |
| `--around-active <n>` | Return active +/- n cycles (requires --team) |

### Read Cycle

```bash
linearis cycles read [options] <cycleIdOrName>
```

| Option | Description |
|--------|-------------|
| `--team <team>` | Team to scope name lookup |
| `--issues-first <n>` | Issues to fetch (default: 50) |

---

## Projects

### List Projects

```bash
linearis projects list [options]
```

| Option | Description |
|--------|-------------|
| `-l, --limit <n>` | Limit results (default: 100) |

---

## Project Milestones

### List Milestones

```bash
linearis project-milestones list [options]
```

| Option | Description |
|--------|-------------|
| `--project <project>` | Project name or ID |
| `-l, --limit <n>` | Limit results (default: 50) |

### Read Milestone

```bash
linearis project-milestones read [options] <milestoneIdOrName>
```

| Option | Description |
|--------|-------------|
| `--project <project>` | Project to scope name lookup |
| `--issues-first <n>` | Issues to fetch (default: 50) |

### Create Milestone

```bash
linearis project-milestones create [options] <name>
```

| Option | Description |
|--------|-------------|
| `--project <project>` | Project name or ID |
| `-d, --description <desc>` | Milestone description |
| `--target-date <date>` | Target date (YYYY-MM-DD) |

### Update Milestone

```bash
linearis project-milestones update [options] <milestoneIdOrName>
```

| Option | Description |
|--------|-------------|
| `--project <project>` | Project to scope name lookup |
| `-n, --name <name>` | New name |
| `-d, --description <desc>` | New description |
| `--target-date <date>` | New target date (YYYY-MM-DD) |
| `--sort-order <n>` | New sort order |

---

## Labels

### List Labels

```bash
linearis labels list [options]
```

| Option | Description |
|--------|-------------|
| `--team <team>` | Filter by team |

---

## Teams

### List Teams

```bash
linearis teams list
```

---

## Users

### List Users

```bash
linearis users list [options]
```

| Option | Description |
|--------|-------------|
| `--active` | Only show active users |

---

## Embeds

### Download File

```bash
linearis embeds download [options] <url>
```

| Option | Description |
|--------|-------------|
| `--output <path>` | Output file path |
| `--overwrite` | Overwrite existing file |
