# Minottobot audit report — FinanceCore Ltd — 2026-04-27

## Repos in scope
- Spring Boot microservices (Java Spring Boot)
- React frontend (React)

## Executive summary (3 bullets max, each under 20 words)
- Jenkins full build is 47 minutes; deployments are biweekly and take 6 hours manually.
- Approximately 12,000 tests exist, but around 30% are flaky and frequently ignored.
- Reliability is under pressure: 2 P1/month, 1 P2/month, MTTR approximately 4 hours.

## Area scores (1 = critical · 5 = excellent)
| Area                    | Score | One-line finding                     |
|-------------------------|-------|--------------------------------------|
| 🔴 CI/CD                |  1/5  | Jenkins 47 minutes; biweekly 6-hour manual releases. |
| 🔴 Testing              |  1/5  | Approximately 12,000 tests; around 30% flaky, frequently ignored. |
| 🟡 Code review          |  3/5  | Three approvals required; hotfixes bypass policy. |
| 🟡 Monitoring           |  3/5  | 2 P1/month, 1 P2/month, MTTR approximately 4 hours. |
| 🔴 Developer Experience |  1/5  | 47-minute CI and 6-hour deploys slow feedback loops. |
| 🔴 Ownership & culture  |  2/5  | QA guild of 6 supports 85 engineers. |

> 🔴 1–2 critical/gap · 🟡 3 functional · 🟢 4–5 good/excellent

## Top 3 blockers right now
1. 🚨 **Untrusted quality signal** — around 30% flaky tests are frequently ignored, so CI outcomes are not trusted.
2. 🚨 **Slow and manual delivery path** — Jenkins takes 47 minutes and release windows are biweekly with 6-hour manual sign-offs.
3. ⚠️ **Operational risk still high** — 2 P1/month and 1 P2/month with MTTR approximately 4 hours in financial services.

## Improvement plan
### ⚡ Short term (this sprint)
- Stabilize flaky tests by failure cluster; enforce quarantine expiry and owner for every skipped test.
- Split Jenkins into a fast PR gate and a full regression pipeline.
- Keep hotfix lane but require post-merge peer review within 24 hours.
- Start tracking missing baseline metrics: lead time, change failure rate, CI success %, coverage, skipped tests, feature flags, aged bugs.

### ◆ Medium term (this quarter)
- Replace manual deployment sign-offs with automated evidence gates and auditable approvals.
- Rebalance the test pyramid for Java Spring Boot services with integration and contract coverage on critical financial flows.
- Define SLOs and alert routing for Spring Boot microservices and React frontend, tied to incident runbooks.

### ◎ Long term (this half)
- Shift from QA-guild-only model to embedded quality champions per product team.
- Evaluate CI platform migration from Jenkins; migration requires 8–12 weeks of parallel pipelines and CI team overlap risk.
- Reduce release batch size from biweekly to smaller frequent releases once CI/test trust targets are met.

## Action items
| ID | Description | Horizon | Owner | Status |
|----|-------------|---------|-------|--------|
| A12 | Triage flaky tests by failure cluster; reduce flaky rate from around 30% to below 10% | ⚡ short | QA guild lead + service owners | ○ open |
| A13 | Split Jenkins into fast PR checks and full regression runs; target sub-15-minute PR feedback | ⚡ short | CI team | ○ open |
| A14 | Enforce hotfix review policy with emergency merge + mandatory 24-hour retrospective review | ⚡ short | Engineering managers | ○ open |
| A15 | Instrument missing DORA/quality metrics dashboard (lead time, CFR, CI success, coverage, skipped tests, flags, open bugs >30 days) | ⚡ short | CI team + QA guild | ○ open |
| A16 | Automate release approvals and remove manual sign-off steps where audit evidence is available | ◆ medium | Platform/CI team | ○ open |
| A17 | Add integration and contract tests for highest-risk Java Spring Boot financial workflows | ◆ medium | Backend leads | ○ open |
| A18 | Define SLOs, alerting, and MTTR playbooks for Spring Boot microservices and React frontend | ◆ medium | Ops + team leads | ○ open |
| A19 | Introduce per-team quality ownership model with QA champions and shared KPIs | ◎ long | CTO + engineering directors | ○ open |
| A20 | Run Jenkins replacement pilot (e.g., GitHub Actions); plan 8–12 weeks parallel-run migration risk | ◎ long | CI team | ○ open |

## Delta since 2026-04-27

### Score changes
| Area | Previous | Current | Change |
|------|----------|---------|--------|
| 🔴 CI/CD | 2/5 | 1/5 | ↓ -1 |
| 🔴 Testing | 1/5 | 1/5 | — |
| 🟡 Code review | 2/5 | 3/5 | ↑ +1 |
| 🟡 Monitoring | 1/5 | 3/5 | ↑ +2 |
| 🔴 Developer Experience | 2/5 | 1/5 | ↓ -1 |
| 🔴 Ownership & culture | 2/5 | 2/5 | — |

> Emoji reflects the **current** score: 🔴 1–2 · 🟡 3 · 🟢 4–5

### Blockers
- **Resolved:** none confirmed.
- **Still open:** missing baseline metrics and incomplete repo-path evidence remain unresolved.
- **New:** large flaky-test burden (around 30%), biweekly 6-hour manual releases, and recurring P1/P2 incident pressure.

### Action items
| ID | Description | Status change |
|----|-------------|---------------|
| A1 | Complete missing baseline metrics | ○ open → superseded by A15 |
| A11 | Provide accessible repo paths for evidence-based reconnaissance | still open |
| A12 | Flaky test stabilization program | new |
| A13 | Jenkins fast-gate split | new |
| A20 | Jenkins migration pilot with explicit overlap risk | new |

### Repo scope
- Added: Spring Boot microservices (Java Spring Boot) — no previous data to compare
- Added: React frontend (React) — no previous data to compare
- Removed: Node.js API (Node.js) — dropped from scope