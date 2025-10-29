# Generate GitHub Issues Status Report

Create a comprehensive report of current issue status across the repository.

## Instructions

1. **Gather data**:
   ```bash
   # Get all open issues with details
   gh issue list --state open --json number,title,labels,assignees,createdAt --limit 100

   # Get recently closed issues
   gh issue list --state closed --limit 10 --json number,title,closedAt

   # Get repository name
   gh repo view --json nameWithOwner
   ```

2. **Organize by priority**:
   - Count issues by priority label:
     - P1 issues (critical)
     - P2 issues (high)
     - P3 issues (normal)
     - Unlabeled issues (need triage)

3. **Identify key metrics**:
   - Total open issues
   - Issues without assignees
   - Oldest open issues (>30 days)
   - Recent activity (closed this week)

4. **Generate report**:
   Format as markdown with the following structure:

   ```markdown
   # GitHub Issues Status Report

   **Repository**: {repo-name}
   **Generated**: {current-date}

   ## Summary

   - **Total Open**: X issues
   - **P1 (Critical)**: X issues
   - **P2 (High)**: X issues
   - **P3 (Normal)**: X issues
   - **Needs Triage**: X issues (no priority label)
   - **Unassigned**: X issues

   ## Critical Issues (P1)

   - #42: Authentication fails for SSO users (assigned to @alice, opened 2 days ago)
   - #38: Database connection timeout (unassigned, opened 5 days ago)

   ## High Priority Issues (P2)

   - #45: Export feature slow for large datasets (assigned to @bob, opened 1 week ago)
   - #41: Mobile UI alignment issues (unassigned, opened 3 days ago)

   ## Normal Priority Issues (P3)

   {Count only, list if <5 issues}

   ## Needs Triage

   - #47: Feature request for dark mode (no priority, opened today)

   ## Recently Closed

   - #40: Fixed login redirect loop (closed today)
   - #39: Updated documentation for API endpoints (closed yesterday)

   ## Aging Issues (>30 days old)

   - #12: Performance optimization for dashboard (P2, opened 45 days ago)

   ## Action Items

   - [ ] Review and address P1 issues immediately
   - [ ] Triage X unlabeled issues
   - [ ] Assign X unassigned P1/P2 issues
   - [ ] Review aging issues for closure or priority adjustment
   ```

5. **Present to user**:
   - Display the formatted report
   - **Highlight urgent items** (P1 issues, unassigned critical items)
   - Suggest immediate next actions
   - Offer to drill down into specific sections if needed

## Report Customization Options

Ask the user if they want to customize the report:
- Include/exclude closed issues
- Filter by assignee
- Filter by label
- Adjust time window for "recent" activity
- Export to file vs display in terminal

## Definition of Done

- [ ] All data gathered from gh CLI
- [ ] Issues counted and organized by priority
- [ ] Key metrics calculated (unassigned, aging, etc.)
- [ ] Report formatted as clean markdown
- [ ] Priority breakdown included with issue lists
- [ ] Action items generated based on findings
- [ ] Report presented to user
- [ ] Urgent items highlighted
- [ ] User offered follow-up actions
