# Example: Ship Checklist

This is a sample output from `/ship-checklist` for a user profile feature release.

---

# Ship Checklist: User Profile Settings v2.0

**Target Date**: Friday, December 15
**Environment**: Production
**Owner**: Engineering Team

---

## Go/No-Go Summary

| Area | Status | Owner | Notes |
|------|--------|-------|-------|
| Deployment | 🟢 Ready | DevOps | CI/CD green, rollback tested |
| Testing | 🟢 Ready | QA | All tests passing, manual verified |
| Security | 🟢 Ready | Security | Review complete, no blockers |
| Analytics | 🟡 Partial | Growth | 2/3 events implemented |
| Documentation | 🟢 Ready | Support | Help docs updated |
| Product | 🟢 Ready | PM | Acceptance criteria met |

**Legend**: 🟢 Ready | 🟡 Partial | 🔴 Blocked

---

## Detailed Checklists

### Deployment (DevOps Engineer)

- [x] CI/CD pipeline is green
- [x] All environment variables configured
- [x] Database migration tested on staging copy
- [x] Rollback plan documented and tested
- [x] Feature flag configured (profile_v2_enabled)
- [x] Canary deployment setup (10% → 50% → 100%)
- [x] Monitoring dashboards ready

**Deployment Plan**:
1. Deploy to staging: Done
2. Deploy to 10% production: Friday 10am
3. Monitor for 2 hours
4. Expand to 50% if healthy
5. Full rollout by EOD

**Rollback Trigger**:
- Error rate > 1%
- P99 latency > 500ms
- Any Critical bug reported

---

### Testing (QA Engineer)

- [x] Unit tests passing (142/142)
- [x] Integration tests passing (38/38)
- [x] E2E tests passing (24/24)
- [x] Manual smoke test completed
- [x] Regression suite green

**Test Coverage**:
- Profile editing: 100%
- Avatar upload: 95%
- Privacy settings: 100%
- Account deletion: 100%

**Known Issues**:
- None blocking release
- Minor: Avatar crop tool slightly misaligned on Safari (Low priority)

---

### Security (Security Engineer)

- [x] Security review completed
- [x] No new vulnerabilities introduced
- [x] Authentication verified on all endpoints
- [x] Authorization checked for profile access
- [x] File upload validated (type, size, content)
- [x] PII handling reviewed
- [x] GDPR compliance verified (data export, deletion)

**Security Notes**:
- Rate limiting added to profile update endpoint
- Avatar uploads scanned for malware
- Profile data export tested for completeness

---

### Analytics (Growth Marketer)

- [x] `profile_viewed` event implemented
- [x] `profile_updated` event implemented
- [ ] `avatar_uploaded` event - **Not implemented** (non-blocking)
- [x] Dashboard created
- [x] Baseline metrics captured

**Note**: Avatar upload tracking will ship in follow-up. Core funnel tracking is complete.

---

### Documentation (Customer Support)

- [x] Help center article updated
- [x] FAQ entries added
- [x] Support team briefed
- [x] Release notes drafted
- [x] In-app tooltips added for new features

**New Help Articles**:
- "How to update your profile"
- "Changing your profile picture"
- "Managing privacy settings"
- "Downloading or deleting your data"

---

### Product (Product Manager)

- [x] All acceptance criteria met
- [x] Stakeholders notified (Design, Marketing, Support)
- [x] Release notes approved
- [x] Success metrics defined
- [x] Post-launch review scheduled (Monday 10am)

**Acceptance Criteria**:
- [x] User can edit profile fields (name, bio, location)
- [x] User can upload and crop avatar
- [x] User can control profile visibility
- [x] User can export profile data
- [x] User can delete account

---

## Known Issues / Risks

| Issue | Severity | Mitigation |
|-------|----------|------------|
| Safari avatar crop alignment | Low | Fix in follow-up release |
| Large avatar files slow to upload | Medium | Added progress indicator, optimize in v2.1 |
| Missing avatar analytics event | Low | Ship in follow-up |

---

## Rollback Plan

**Trigger Conditions**:
- Error rate exceeds 1% (baseline: 0.2%)
- P99 latency exceeds 500ms (baseline: 180ms)
- Any Critical or High severity bug
- Data integrity issue detected

**Rollback Steps**:
1. Disable feature flag `profile_v2_enabled`
2. Run rollback command: `./scripts/rollback-profile-v2.sh`
3. Notify stakeholders in #releases channel
4. Create incident ticket
5. Communicate to affected users if necessary

**Rollback Time**: < 5 minutes

---

## Post-Launch Tasks

- [ ] Monitor error rates for 24 hours
- [ ] Check analytics data flowing correctly
- [ ] Review user feedback channels
- [ ] Post-launch review meeting (Monday 10am)
- [ ] Close release ticket
- [ ] Plan v2.1 improvements

---

## Approval

| Role | Name | Approved | Date |
|------|------|----------|------|
| Engineering Lead | Alex Chen | [x] | Dec 14 |
| Product Manager | Sam Rivera | [x] | Dec 14 |
| QA Lead | Jordan Lee | [x] | Dec 14 |

---

## Ship Decision

**[x] GO** - All critical items complete, known issues documented and acceptable.

**Next Step**: Begin canary deployment Friday 10am PT.
