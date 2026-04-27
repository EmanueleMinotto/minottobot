# Minottobot audit report — Norsk Mobility AS — 2026-04-27

## Repos in scope
- Backend payment platform (Python + Django)
- Mobile app (React Native)
- Data layer (PostgreSQL)

## Executive summary (3 bullets max, each under 20 words)
- On 2026-04-23, a race condition corrupted payment records for 2,100 users.
- GitHub Actions runs in ~12 minutes, but production deploys remain 1-2 times weekly.
- Test suite has 397 tests; all 12 E2E tests were added last week.

## Area scores (1 = critical · 5 = excellent)
| Area                    | Score | One-line finding |
|-------------------------|-------|--------------------------------------|
| 🟡 CI/CD                |  3/5  | GitHub Actions ~12m; manual production approval gate. |
| 🔴 Testing              |  2/5  | 340 unit, 45 integration, 12 E2E added last week. |
| 🔴 Code review          |  2/5  | Review quality, lead time, and CI success are unknown. |
| 🔴 Monitoring           |  2/5  | Sentry added 2026-04-24; before that, users found failures. |
| 🟡 Developer Experience |  3/5  | Deploys 1-2/week; major delivery metrics remain untracked. |
| 🟡 Ownership & culture  |  3/5  | 14 engineers and 2 QA indicate shared-quality strain. |

> 🔴 1–2 critical/gap · 🟡 3 functional · 🟢 4–5 good/excellent

## Top 3 blockers right now
1. 🚨 **Payment reliability breach** — On 2026-04-23, a payment-processing race condition corrupted records for 2,100 users; recovery is still ongoing.
2. ⚠️ **Observability maturity gap** — Sentry was introduced only on 2026-04-24; prior detection depended on user reports.
3. ⚠️ **Missing operating metrics** — Lead time, change failure rate, CI success rate, MTTR, coverage, skipped tests, flag age, and >30-day bug count are unknown.

## Improvement plan
### ⚡ Short term (this sprint)
- Add Django/PostgreSQL concurrency integration tests for payment write paths and idempotency.
- Add one high-value E2E payment regression covering the exact 2026-04-23 failure path.
- Define and publish incident runbook with MTTR capture per incident.
- Instrument baseline DORA/quality dashboard from GitHub Actions + Sentry + issue tracker.

### ◆ Medium term (this quarter)
- Rebalance test pyramid: expand integration/contract coverage for payment boundaries before scaling E2E volume.
- Enforce skipped-test policy with owner, ticket, and expiry date.
- Add PR review checklist for high-risk domains (payments, money movement, migrations).
- Introduce monthly quality review: CI trends, flaky rate, incident causes, old-bug burn-down.

### ◎ Long term (this half)
- Establish shared quality ownership model: each squad owns reliability KPIs, QA coaches strategy.
- Build proactive shift-right practice: alert hygiene, service-level objectives, and quarterly game days.
- Standardize engineering conventions (OpenAPI coverage, commit convention, release hygiene) across backend and mobile.

## Action items
| ID | Description | Horizon | Owner | Status |
|----|-------------|---------|-------|--------|
| A21 | Add race-condition integration tests for Django payment transaction paths | ⚡ short | Backend lead | ○ open |
| A22 | Add incident-regression E2E for payment corruption scenario | ⚡ short | QA lead + mobile lead | ○ open |
| A23 | Publish incident runbook and require MTTR logging on every incident | ⚡ short | Engineering manager | ○ open |
| A24 | Start DORA and quality metric dashboard (lead time, CFR, CI success, MTTR, coverage) | ⚡ short | CI owner | ○ open |
| A25 | Add skipped-test expiry governance with owner and ticket linkage | ◆ medium | QA lead | ○ open |
| A26 | Add payment-domain PR checklist with mandatory dual review | ◆ medium | Backend lead | ○ open |
| A27 | Launch monthly reliability review ritual with action tracking | ◎ long | CTO staff engineer | ○ open |
| A28 | Roll out standards baseline (OpenAPI, commit conventions, release hygiene) | ◎ long | Architecture group | ○ open |

## Delta since 2026-04-27

### Score changes
| Area | Previous | Current | Change |
|------|----------|---------|--------|
| 🟡 CI/CD | 1/5 | 3/5 | ↑ +2 |
| 🔴 Testing | 1/5 | 2/5 | ↑ +1 |
| 🔴 Code review | 3/5 | 2/5 | ↓ -1 |
| 🔴 Monitoring | 3/5 | 2/5 | ↓ -1 |
| 🟡 Developer Experience | 1/5 | 3/5 | ↑ +2 |
| 🟡 Ownership & culture | 2/5 | 3/5 | ↑ +1 |

> Emoji reflects the **current** score: 🔴 1–2 · 🟡 3 · 🟢 4–5

### Blockers
- **Resolved:** none confirmed.
- **Still open:** delivery risk tied to test trust and release safety.
- **New:** payment-data corruption incident affecting 2,100 users.

### Action items
| ID | Description | Status change |
|----|-------------|---------------|
| A12-A20 | Prior FinanceCore Ltd actions | dropped from scope |
| A21 | Concurrency integration tests for payments | new |
| A22 | Incident-regression E2E for payments | new |
| A23 | Incident runbook + MTTR logging | new |
| A24 | DORA/quality metrics dashboard | new |
| A25 | Skipped-test expiry governance | new |
| A26 | Payment PR dual-review checklist | new |
| A27 | Monthly reliability review ritual | new |
| A28 | Standards baseline rollout | new |

### Repo scope
- Added: Backend payment platform (Python + Django) — no previous data to compare
- Added: Mobile app (React Native) — no previous data to compare
- Added: Data layer (PostgreSQL) — no previous data to compare
- Removed: Spring Boot microservices — dropped from scope
- Removed: React frontend — dropped from scope