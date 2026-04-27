# Minottobot audit report — Momentum Fintech (Platform team) — 2026-04-27

## Repos in scope
- Laravel platform codebase (PHP + Laravel)
- Node.js microservices (Node.js)

## Executive summary (3 bullets max, each under 20 words)
- 11 engineers on paper, 4 on loan: only 7 active on platform.
- Around 800 tests exist, but none were run in about 2 months.
- CircleCI/GitHub Actions split and a 6-month unresolved outage create immediate delivery risk.

## Area scores (1 = critical · 5 = excellent)
| Area                    | Score | One-line finding                     |
|-------------------------|-------|--------------------------------------|
| 🔴 CI/CD                |  1/5  | CircleCI and GitHub Actions ownership unclear; deploys are irregular. |
| 🔴 Testing              |  1/5  | ~800 tests unrun for 2 months; pass rate unknown. |
| 🔴 Code review          |  2/5  | Review policy exists; urgent work often bypasses peer review. |
| 🔴 Monitoring           |  1/5  | Incidents untracked; major outage from 6 months still unresolved. |
| 🔴 Developer Experience |  2/5  | 7 active engineers support legacy Laravel and Node.js services. |
| 🔴 Ownership & culture  |  1/5  | Three VPs in 18 months; no product owner. |

> 🔴 1–2 critical/gap · 🟡 3 functional · 🟢 4–5 good/excellent

## Top 3 blockers right now
1. 🚨 **Reliability governance failure** — no formal incident tracking, and the major outage from 6 months ago is still unresolved.
2. 🚨 **Delivery control split** — CircleCI and GitHub Actions both exist, with no clear authoritative deployment path.
3. ⚠️ **Quality signal collapse** — around 800 tests have not been run in about 2 months, so “green” is meaningless.

## Improvement plan
### ⚡ Short term (this sprint)
- Run the full suite in both CircleCI and GitHub Actions and publish an authoritative pass/fail baseline.
- Declare one production deployment authority immediately and block production deploys from the non-authoritative CI.
- Open a formal incident register and assign a single owner for closing the unresolved 6-month outage.
- Enforce emergency review policy: urgent merges require peer review within 24 hours post-merge.
- Instrument missing Phase 0 metrics: CI runtime, lead time, change failure rate, MTTR, CI success rate, coverage, skipped tests, active flags, and old bugs.

### ◆ Medium term (this quarter)
- Consolidate to one CI platform; if replacing CircleCI or GitHub Actions, plan 4–6 weeks of dual-run migration risk and pipeline porting effort.
- Rebalance testing for Laravel + Node.js + MySQL: fast unit gate, integration tests on critical DB/service flows, minimal critical-path E2E.
- Add expiry-based governance for skipped/quarantined tests with named owners and due dates.

### ◎ Long term (this half)
- Re-align staffing to platform load: restore capacity beyond 7 active engineers or explicitly reduce scope.
- Assign a dedicated product owner to reduce urgent bypasses and stabilize prioritization.
- Establish monthly reliability review and quarterly quality KPI governance across Platform.

## Action items
| ID | Description | Horizon | Owner | Status |
|----|-------------|---------|-------|--------|
| A21 | Execute full baseline run in CircleCI and GitHub Actions; publish failure matrix | ⚡ short | Platform lead + CI owner | ○ open |
| A22 | Decide and document authoritative deployment CI for production | ⚡ short | VP Eng delegate + Platform lead | ○ open |
| A23 | Create incident register and assign owner for unresolved outage | ⚡ short | Platform lead | ○ open |
| A24 | Enforce urgent-merge 24h post-merge review rule in branch protections | ⚡ short | Engineering managers | ○ open |
| A25 | Capture and dashboard all missing DORA/quality metrics | ⚡ short | CI owner + QA champion | ○ open |
| A26 | Consolidate CI pipelines to single platform with parallel-run migration plan | ◆ medium | CI owner | ○ open |
| A27 | Rebuild test pyramid coverage for Laravel/Node critical financial paths | ◆ medium | Service owners | ○ open |
| A28 | Implement skip/quarantine expiry policy with owner + deadline | ◆ medium | QA champion + tech leads | ○ open |
| A29 | Assign product owner and stabilize team quality ownership model | ◎ long | VP Engineering | ○ open |
| A30 | Run recurring reliability governance reviews with tracked closure SLAs | ◎ long | Platform lead + leadership | ○ open |

## Delta since 2026-04-27

### Score changes
| Area | Previous | Current | Change |
|------|----------|---------|--------|
| 🔴 CI/CD | 1/5 | 1/5 | — |
| 🔴 Testing | 1/5 | 1/5 | — |
| 🔴 Code review | 3/5 | 2/5 | ↓ -1 |
| 🔴 Monitoring | 3/5 | 1/5 | ↓ -2 |
| 🔴 Developer Experience | 1/5 | 2/5 | ↑ +1 |
| 🔴 Ownership & culture | 2/5 | 1/5 | ↓ -1 |

> Emoji reflects the **current** score: 🔴 1–2 · 🟡 3 · 🟢 4–5

### Blockers
- **Resolved:** none verifiable.
- **Still open:** untrusted testing signal and reliability pain remain core risks.
- **New:** CI authority split (CircleCI vs GitHub Actions), unresolved outage ownership gap, and missing product owner.

### Action items
| ID | Description | Status change |
|----|-------------|---------------|
| A12–A20 | Previous FinanceCore action set | scope changed; status not directly comparable |
| A21 | Baseline both CI systems and publish matrix | new |
| A22 | Declare authoritative deployment system | new |
| A23 | Incident register and outage ownership | new |
| A24 | Urgent-merge post-review enforcement | new |
| A25 | DORA and quality metric instrumentation | new |
| A26 | CI consolidation with migration plan | new |
| A27 | Test pyramid rebalance for Laravel/Node flows | new |
| A28 | Expiry-based skipped test governance | new |
| A29 | Product owner assignment and ownership model | new |
| A30 | Reliability governance review cadence | new |

### Repo scope
- Added: Laravel platform codebase (PHP + Laravel) — no previous data to compare
- Added: Node.js microservices (Node.js) — no previous data to compare
- Removed: Spring Boot microservices — dropped from scope
- Removed: React frontend — dropped from scope