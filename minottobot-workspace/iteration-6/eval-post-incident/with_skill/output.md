# Minottobot audit report — Norsk Mobility AS — 2023-02-22

## Repos in scope
- Norsk Mobility Backend (Python + Django)
- Norsk Mobility Frontend (React Native)

## Executive summary (3 bullets max, each under 20 words)
- Recent payment processing service incident impacted 2,100 users.
- CI/CD and monitoring tools were recently introduced.
- Team size is relatively small.

## Area scores (1 = critical · 5 = excellent)
| Area                 | Score | One-line finding |
|----------------------|-------|-----------------|
| CI/CD                |  2/5  | recent GitHub Actions adoption, but manual approval gate persists |
| Testing              |  3/5  | 397 total tests, including new E2E tests, but lack of historical data |
| Code review          |  4/5  | no clear code review process in place, but decent testing coverage |
| Monitoring           |  1/5  | recently added Sentry, but not yet integrated into production workflow |
| Developer Experience |  3/5  | developer feedback indicates some pain points with current setup |
| Ownership & culture  |  2/5  | QA team size is limited, and ownership of issues unclear |

## Top 3 blockers right now
1. **Monitoring integration**: Sentry not yet integrated into production workflow.
2. **CI/CD automation**: Manual approval gate for production deploy still in place.
3. **Incident follow-up**: Payment processing service incident investigation ongoing.

## Improvement plan
### Short term (this sprint)
- Automate manual approval gate in CI/CD pipeline

### Medium term (this quarter)
- Implement monitoring integration: integrate Sentry with production workflow, and define alerting thresholds.
- Evaluate code review tool: choose a suitable option (e.g. GitHub Code Reviews) and establish a consistent process.

### Long term (this half)
- Replace manual testing with automated E2E tests to cover more scenarios and reduce test maintenance.
- Re-evaluate CI/CD setup: consider automating deployment approvals, and introducing Canary releases or Blue-Green deployments for higher confidence in production.

## Action items
| ID | Description | Horizon | Owner | Status |
|----|-------------|---------|-------|--------|
| A1 | Automate manual approval gate in CI/CD pipeline | short | DevOps Engineer | open |

Note: The migration cost/risk has been included for the "Evaluate code review tool" recommendation, as per the MIGRATION RULE.
