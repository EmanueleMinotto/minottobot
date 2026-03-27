# Minottobot audit report — Momentum Fintech Platform — 2026-03-27

## Repos in scope
- Platform monorepo (PHP/Laravel + Node.js microservices, MySQL)

> ⚠️ **No code access** — this audit is based on team-reported data only. Findings could not be verified against the codebase.

## Executive summary (3 bullets max, each under 20 words)
- Two competing CI systems with no clear authoritative owner; deployments are unreliable and infrequent.
- 800 tests not run in 2 months; the suite is effectively untrusted and abandoned.
- No incident tracking, no product owner, 3 VPs in 18 months — structural instability is severe.

## Area scores (1 = critical · 5 = excellent)
| Area                    | Score | One-line finding                                      |
|-------------------------|-------|-------------------------------------------------------|
| 🔴 CI/CD                |  1/5  | Two CI systems; no authoritative pipeline for deploys |
| 🔴 Testing              |  1/5  | 800 tests, unrun for 2 months, unknown pass rate      |
| 🔴 Code review          |  2/5  | Officially required but routinely skipped for urgency |
| 🔴 Monitoring           |  1/5  | No incident tracking; major outage unresolved 6 months |
| 🟡 Developer Experience |  3/5  | Mixed stack (Laravel + Node.js) adds cognitive overhead |
| 🔴 Ownership & culture  |  2/5  | No product owner, leadership churn, shared accountability absent |

> 🔴 1–2 critical/gap · 🟡 3 functional · 🟢 4–5 good/excellent

## Top 3 blockers right now
1. 🚨 **Dual CI with no authoritative pipeline** — nobody knows which system gates production deploys; every release is a gamble.
2. 🚨 **Unresolved major outage + zero incident tracking** — a 6-month-old outage with no formal tracking means the failure mode is still live and invisible.
3. ⚠️ **Abandoned test suite** — 800 tests unrun for 2 months; the suite provides no safety net and the team doesn't know it.

## Improvement plan

### ⚡ Short term (this sprint)
- Designate one CI system (GitHub Actions recommended) as the single authoritative pipeline; disable or archive CircleCI for deployment triggers.
- Run the full test suite immediately; triage results into passing, failing, and flaky buckets; document the actual pass rate.
- Open a formal incident record for the unresolved outage and assign an owner — even if the fix is long-term, tracking must start now.
- Add a basic on-call rotation and a minimal incident log (a shared doc is enough for now) to stop flying blind on production health.

### ◆ Medium term (this quarter)
- Enforce CI as a hard merge gate on the authoritative pipeline; make bypass require explicit documented justification.
- Establish a test triage policy: delete tests that cannot be fixed within one sprint; fix or quarantine flaky tests; never merge with a red suite.
- Introduce a lightweight code review SLA — "urgent" bypasses must be followed by a post-merge review within 24 hours, logged in the PR.
- Add error tracking (Sentry or equivalent) to both the Laravel and Node.js services; connect alerts to a shared channel.
- Assign an interim product owner or a rotating engineering lead to represent product priorities until a permanent PO is in place.

### ◎ Long term (this half)
- Build a deployment cadence target (weekly or more frequent) backed by a healthy CI and a trusted test suite — low frequency is a symptom, not the root problem.
- Address the mixed-stack cognitive load: document service boundaries between Laravel and Node.js, establish clear ownership per service, reduce the mental overhead of context-switching.
- Run a structured post-mortem on the 6-month-old outage once it is resolved; use it as a foundation for an incident review culture.
- Introduce the DFER loop (Deprecate → Fix → Enforce → Repeat) for linting and code standards, starting with the Node.js services as a safer proving ground before applying to the Laravel monolith.
- Stabilize organizational context: advocate for a consistent engineering leadership tenure; the 3-VP churn in 18 months is the root cause behind most process gaps.

## Action items
| ID | Description | Horizon | Owner | Status |
|----|-------------|---------|-------|--------|
| A1 | Designate GitHub Actions as sole authoritative CI; decommission CircleCI deploy triggers | ⚡ short | | ○ open |
| A2 | Run full test suite; produce a pass/fail/flaky triage report | ⚡ short | | ○ open |
| A3 | Open a tracked incident record for the unresolved outage; assign an owner | ⚡ short | | ○ open |
| A4 | Create a minimal incident log and on-call rotation | ⚡ short | | ○ open |
| A5 | Enforce CI as a hard merge gate; document bypass policy | ◆ medium | | ○ open |
| A6 | Implement test triage policy; remove or quarantine unfixable tests | ◆ medium | | ○ open |
| A7 | Introduce post-merge review SLA for "urgent" bypass PRs | ◆ medium | | ○ open |
| A8 | Deploy Sentry (or equivalent) for Laravel and Node.js services | ◆ medium | | ○ open |
| A9 | Assign interim product owner or rotating engineering lead | ◆ medium | | ○ open |
| A10 | Set a deployment frequency target backed by CI health metrics | ◎ long | | ○ open |
| A11 | Document Laravel/Node.js service boundaries; assign per-service ownership | ◎ long | | ○ open |
| A12 | Run structured post-mortem on 6-month outage; establish incident review ritual | ◎ long | | ○ open |
| A13 | Roll out DFER linting loop starting with Node.js services | ◎ long | | ○ open |
