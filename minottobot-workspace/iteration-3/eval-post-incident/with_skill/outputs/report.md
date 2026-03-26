# Minottobot audit report — Norsk Mobility AS — 2026-03-26

## Repos in scope
- backend (Python / Django)
- mobile (React Native)
- database (PostgreSQL)

> ⚠️ **No code access** — this audit is based on team-reported data only. Findings could not be verified against the codebase.

## Executive summary (3 bullets max, each under 20 words)
- A race condition corrupted payment records for 2,100 users 4 days ago; investigation ongoing.
- Monitoring (Sentry) and E2E tests were both added reactively, post-incident — not as planned foundations.
- The team is reacting well, but quality processes need to shift from reactive to proactive.

## Area scores (1 = critical · 5 = excellent)
| Area                    | Score | One-line finding                                     |
|-------------------------|-------|------------------------------------------------------|
| 🟡 CI/CD                |  3/5  | GitHub Actions works; manual prod gate adds friction |
| 🔴 Testing              |  2/5  | Payment race condition uncaught; E2E layer brand new |
| 🟡 Code review          |  3/5  | Process assumed present; quality unknown             |
| 🔴 Monitoring           |  2/5  | Sentry added 3 days ago; no performance monitoring   |
| 🟡 Developer Experience |  3/5  | 12-min CI acceptable; no feature flags or gradual rollout |
| 🟡 Ownership & culture  |  3/5  | Post-incident response is healthy; quality was reactive |

> 🔴 1–2 critical/gap · 🟡 3 functional · 🟢 4–5 good/excellent

## Phase 0 data gaps (unanswered questions — each is a finding)
- **CI success rate %:** unknown — could be masking chronic flakiness
- **Test coverage %:** unknown — no baseline exists to evaluate gap in payment paths
- **Skipped/disabled tests:** unknown — hidden debt in the test suite
- **Open bugs older than 30 days:** unknown — no visibility on backlog health

## Top 3 blockers right now
1. 🚨 **No regression test for the payment race condition** — the bug that hit 2,100 users has no automated guard; it can recur silently.
2. ⚠️ **Monitoring covers only errors, not business health** — Sentry catches exceptions but no alert exists for payment failure rates, transaction volumes, or latency spikes.
3. ⚠️ **E2E and integration layers are untested in production-realistic conditions** — 12 E2E tests written last week and 45 integration tests of unknown depth leave critical payment flows unverified.

## Improvement plan

### ⚡ Short term (this sprint)
- Write a regression test that reproduces the payment race condition exactly — commit it before the fix is merged (this is the test that should have existed).
- Audit the 12 new E2E tests: do they cover the payment flow end-to-end? If not, add a payment journey test immediately.
- Configure Sentry to capture payment-related errors with full context (user ID, amount, transaction ID) — right now it catches exceptions but likely lacks domain context.
- Add a Sentry alert for payment error rate exceeding a threshold (e.g., > 1% of payment attempts in 5 minutes).
- Run `coverage` (pytest-cov) on the Django backend and export a baseline report — you need to know where you stand before the next incident.

### ◆ Medium term (this quarter)
- Strengthen the integration test layer for the payment service: test concurrent writes, idempotency, rollback behavior, and retry logic — these are the scenarios that caused the incident.
- Add structured logging to the payment service (request ID, user ID, amount, outcome) to enable forensic investigation without database inspection.
- Add a performance monitoring layer alongside Sentry — consider Datadog or Prometheus + Grafana — to track payment latency, queue depth, and throughput over time.
- Establish a coverage target for the payment domain (suggest 80%+ line coverage as a starting point) and enforce it in GitHub Actions CI.
- Introduce Conventional Commits across both repos — this gives you free changelogs and makes post-incident git archaeology much faster.
- Define and document the CI success rate baseline — add a CI health metric to your weekly team review.

### ◎ Long term (this half)
- Implement feature flags (e.g., Unleash or LaunchDarkly) to enable gradual rollout of payment changes — deploy to 5% of users before full release, giving Sentry and monitoring time to catch issues before they reach everyone.
- Build a post-incident review (PIR) ritual: blameless, structured, published internally — this is how the team turns "we're shaken" into "we're stronger."
- Raise the integration test count significantly (target: the 45 current tests should grow to cover all service boundaries in the payment flow, not just happy paths).
- Evaluate whether the manual approval gate before production can be replaced by automated smoke tests + automatic rollback — removing human gates in favor of automated confidence signals is better DX and faster MTTR.
- Establish a test reliability metric: track flaky test count and treat any flaky test as a P2 bug.

## Action items
| ID  | Description                                                              | Horizon   | Owner | Status  |
|-----|--------------------------------------------------------------------------|-----------|-------|---------|
| A1  | Write regression test reproducing the payment race condition             | ⚡ short  |       | ○ open  |
| A2  | Audit 12 E2E tests — verify payment journey is covered                   | ⚡ short  |       | ○ open  |
| A3  | Configure Sentry with payment domain context (user ID, transaction ID)   | ⚡ short  |       | ○ open  |
| A4  | Add Sentry alert for payment error rate spike                            | ⚡ short  |       | ○ open  |
| A5  | Run pytest-cov and publish baseline coverage report                      | ⚡ short  |       | ○ open  |
| A6  | Add integration tests for payment concurrency, idempotency, rollback     | ◆ medium  |       | ○ open  |
| A7  | Add structured logging to payment service                                | ◆ medium  |       | ○ open  |
| A8  | Introduce performance monitoring (Datadog or Prometheus/Grafana)         | ◆ medium  |       | ○ open  |
| A9  | Enforce 80%+ coverage on payment domain in GitHub Actions CI             | ◆ medium  |       | ○ open  |
| A10 | Adopt Conventional Commits across backend and mobile repos               | ◆ medium  |       | ○ open  |
| A11 | Define CI success rate baseline and add to weekly team review            | ◆ medium  |       | ○ open  |
| A12 | Implement feature flags for gradual payment rollout                      | ◎ long    |       | ○ open  |
| A13 | Establish blameless post-incident review (PIR) ritual                   | ◎ long    |       | ○ open  |
| A14 | Grow integration test count to cover all payment service boundaries      | ◎ long    |       | ○ open  |
| A15 | Replace manual prod approval gate with automated smoke tests + rollback  | ◎ long    |       | ○ open  |
| A16 | Track flaky test count; treat flaky tests as P2 bugs                    | ◎ long    |       | ○ open  |
