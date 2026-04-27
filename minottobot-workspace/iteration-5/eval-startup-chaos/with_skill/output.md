# Minottobot audit report — Swiftly Inc — 2026-04-27

## Repos in scope
- Node.js API (Node.js)
- React frontend (React)

## Executive summary (3 bullets max, each under 20 words)
- `0` tests with `2-3` daily deploys creates continuous production regression risk.
- Incidents are about `1/day`, user-detected first, with MTTR around `1 hour`.
- Key DORA and quality metrics are still unknown, blocking reliable prioritization.

## Area scores (1 = critical · 5 = excellent)
| Area                    | Score | One-line finding                     |
|-------------------------|-------|--------------------------------------|
| 🔴 CI/CD                |  2/5  | GitHub Actions runs ESLint only; ~2-minute pipeline |
| 🔴 Testing              |  1/5  | 0 tests across Node.js API and React frontend |
| 🔴 Code review          |  2/5  | Reviews happen sometimes; no formal policy or gate |
| 🔴 Monitoring           |  1/5  | ~1 incident/day, users report first, MTTR ~1 hour |
| 🔴 Developer Experience |  2/5  | Local+production only; manual `git push heroku main` deploys |
| 🔴 Ownership & culture  |  2/5  | 4 engineers, no dedicated QA, quality process ad hoc |

> 🔴 1–2 critical/gap · 🟡 3 functional · 🟢 4–5 good/excellent

## Top 3 blockers right now
1. 🚨 **No safety net at release speed** — `0` tests with `2-3` production deploys/day is a direct reliability risk.
2. 🚨 **Detection is externalized to users** — incidents are reported by users first (`~1/day`), despite MTTR near `1 hour` once known.
3. ⚠️ **Observability and planning blind spots** — lead time, change failure rate, CI success %, coverage, skipped tests, flag inventory, and aging bug metrics are missing.

## Improvement plan
### ⚡ Short term (this sprint)
- Capture missing Phase 0 metrics and publish a weekly reliability dashboard.
- Add production error tracking + alert routing for Node.js API and React frontend.
- Enforce branch protection requiring 1 review and passing GitHub Actions checks.
- Add test job to GitHub Actions and block merges on test failure.
- Implement first safety net: 10 unit + 5 integration tests on top incident paths.

### ◆ Medium term (this quarter)
- Add a staging environment and automate deploy from GitHub Actions to Heroku.
- Define test pyramid targets and track coverage + skipped tests in CI.
- Run weekly incident review with runbooks and alert tuning.

### ◎ Long term (this half)
- Introduce feature-flag ownership/removal policy with monthly cleanup.
- Run quarterly DFER quality ratchet on lint and test standards.

## Action items
| ID | Description | Horizon | Owner | Status |
|----|-------------|---------|-------|--------|
| A1 | Complete missing Phase 0 metrics (lead time, change failure rate, CI success %, coverage, skipped tests, flag inventory, days since last incident, open bugs >30 days) | ⚡ short | Tech lead | ○ open |
| A2 | Add production error tracking and alert routing for Node.js API and React frontend | ⚡ short | Backend engineer | ○ open |
| A3 | Add branch protection: require 1 review and passing GitHub Actions checks | ⚡ short | Tech lead | ○ open |
| A4 | Add test execution to GitHub Actions and block merges on failures | ⚡ short | Backend engineer | ○ open |
| A5 | Implement first safety net: 10 unit + 5 integration tests on top incident paths | ⚡ short | Backend engineers | ○ open |
| A6 | Create staging environment and automate deploy from GitHub Actions to Heroku | ◆ medium | Backend engineer | ○ open |
| A7 | Define test pyramid targets and track coverage + skipped tests in CI | ◆ medium | Team | ○ open |
| A8 | Start weekly incident review with runbooks and alert tuning | ◆ medium | Team | ○ open |
| A9 | Introduce feature flags with owner/removal policy and monthly cleanup | ◎ long | Team | ○ open |
| A10 | Run quarterly DFER quality ratchet on lint/test standards | ◎ long | Team | ○ open |
| A11 | Provide accessible Node.js API and React frontend repo paths for evidence-based reconnaissance | ⚡ short | Tech lead | ○ open |

## Delta since 2026-04-27

### Score changes
| Area | Previous | Current | Change |
|------|----------|---------|--------|
| 🔴 CI/CD | 2/5 | 2/5 | — |
| 🔴 Testing | 1/5 | 1/5 | — |
| 🔴 Code review | 2/5 | 2/5 | — |
| 🔴 Monitoring | 1/5 | 1/5 | — |
| 🔴 Developer Experience | 2/5 | 2/5 | — |
| 🔴 Ownership & culture | 2/5 | 2/5 | — |

> Emoji reflects the **current** score: 🔴 1–2 · 🟡 3 · 🟢 4–5

### Blockers
- **Resolved:** none
- **Still open:** no automated safety net; user-detected incidents; missing baseline metrics
- **New:** evidence-based reconnaissance is blocked until in-scope repo paths are accessible

### Action items
| ID | Description | Status change |
|----|-------------|---------------|
| A1 | Complete missing Phase 0 metrics | still open |
| A2 | Add production error tracking and alert routing | still open |
| A3 | Enforce branch protection + required checks | still open |
| A11 | Provide accessible repo paths for reconnaissance | new |

### Repo scope
- Added: none
- Removed: none