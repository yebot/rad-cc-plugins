---
name: ship-checklist
description: Pre-launch checklist from all team perspectives
tools: Read, Glob, Grep, Bash, TodoWrite, Task
model: inherit
---

# Ship Checklist

Generate a comprehensive pre-launch checklist with input from all team perspectives.

## Instructions

### Step 1: Gather Context

Understand what's being shipped:

```
What are you preparing to ship?
- Feature name/description
- Target environment (staging/production)
- Any specific concerns?
```

Also check:
- Recent commits and changes
- PR description if available
- Related issues or tickets

### Step 2: DevOps Engineer Checklist

Invoke `devops-engineer` agent for deployment readiness:

```markdown
### Deployment Readiness
- [ ] CI/CD pipeline is green
- [ ] Environment variables configured
- [ ] Database migrations ready (if applicable)
- [ ] Rollback plan documented
- [ ] Deployment runbook updated

### Infrastructure
- [ ] Resource scaling appropriate
- [ ] Monitoring dashboards ready
- [ ] Alerts configured
- [ ] Load testing completed (if high traffic expected)
```

### Step 3: QA Engineer Checklist

Invoke `qa-engineer` agent for testing readiness:

```markdown
### Testing Status
- [ ] Unit tests passing
- [ ] Integration tests passing
- [ ] E2E tests passing
- [ ] Manual smoke test completed
- [ ] Regression suite green

### Test Coverage
- [ ] Happy path tested
- [ ] Error cases tested
- [ ] Edge cases documented
- [ ] Performance acceptable
```

### Step 4: Security Engineer Checklist

Invoke `security-engineer` agent for security review:

```markdown
### Security Review
- [ ] No secrets in code
- [ ] Authentication verified
- [ ] Authorization checked
- [ ] Input validation complete
- [ ] Security headers configured
- [ ] Dependency scan clean
```

### Step 5: Growth Marketer Checklist

Invoke `growth-marketer` agent for analytics and tracking:

```markdown
### Analytics & Tracking
- [ ] Events implemented and tested
- [ ] Funnel tracking verified
- [ ] Success metrics dashboard ready
- [ ] A/B test configured (if applicable)
- [ ] SEO checked (titles, meta, indexability)
```

### Step 6: Customer Support Checklist

Invoke `customer-support` agent for documentation readiness:

```markdown
### Documentation & Support
- [ ] User-facing docs updated
- [ ] FAQ prepared for new features
- [ ] Support team briefed
- [ ] Known issues documented
- [ ] Rollout communication drafted
```

### Step 7: Product Manager Checklist

Invoke `product-manager` agent for launch readiness:

```markdown
### Launch Readiness
- [ ] Acceptance criteria met
- [ ] Stakeholders notified
- [ ] Release notes prepared
- [ ] Success metrics baseline captured
- [ ] Post-launch review scheduled
```

### Step 8: Compile Ship Checklist

Create the final checklist:

```markdown
# Ship Checklist: [Feature/Release Name]

**Target Date**: [Date]
**Environment**: [Staging/Production]
**Owner**: [Name]

---

## Go/No-Go Summary

| Area | Status | Owner |
|------|--------|-------|
| Deployment | ⚪ | DevOps |
| Testing | ⚪ | QA |
| Security | ⚪ | Security |
| Analytics | ⚪ | Growth |
| Documentation | ⚪ | Support |
| Product | ⚪ | PM |

**Legend**: 🟢 Ready | 🟡 Partial | 🔴 Blocked | ⚪ Not Started

---

## Detailed Checklists

### Deployment
[DevOps checklist items]

### Testing
[QA checklist items]

### Security
[Security checklist items]

### Analytics
[Growth checklist items]

### Documentation
[Support checklist items]

### Product
[PM checklist items]

---

## Known Issues / Risks
- [Issue 1]: [Mitigation]
- [Issue 2]: [Mitigation]

## Rollback Plan
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Post-Launch Tasks
- [ ] Monitor error rates for 24h
- [ ] Check analytics data flowing
- [ ] Review user feedback
- [ ] Schedule post-mortem

---

## Approval

| Role | Name | Approved |
|------|------|----------|
| Engineering Lead | | [ ] |
| Product Manager | | [ ] |
| QA Lead | | [ ] |

**Ship Decision**: [ ] GO / [ ] NO-GO
```

## Output

- Display the checklist with current status
- Highlight any blocking items
- Offer to save as a file
