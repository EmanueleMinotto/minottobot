# Minottobot audit report — Norsk Mobility AS — 2026-03-27

## Repos in scope
- Norsk Mobility AS (Python/Django + React Native + PostgreSQL)

> ⚠️ **No code access** — this audit is based on team-reported data only. Findings could not be verified against the codebase.

## Executive summary (3 bullets max, each under 20 words)
- Payment race condition corrupted 2,100 user records; monitoring and testing were both absent beforehand.
- E2E tests and Sentry were added reactively post-incident, not as built-in practice.
- CI exists but no shift-left discipline; quality is crisis-driven, not systemic.

## Area scores (1 = critical · 5 = excellent)
| Area                    | Score | One-line finding                     |
|-------------------------|-------|--------------------------------------|
| 🟡 CI/CD                |  3/5  | Pipeline exists; 12 min, manual prod gate |
| 🔴 Testing              |  2/5  | E2E all written last week; no integration tests |
| 🟡 Code review          |  3/5  | Assumed present; thoroughness unknown |
| 🟡 Monitoring           |  3/5  | Sentry added 3 days ago; blind before that |
| 🟡 Developer Experience |  3/5  | Stack is modern; feedback loops immature |
| 🟡 Ownership & culture  |  3/5  | Reactive quality signals; crisis prompted action |

> 🔴 1–2 critical/gap · 🟡 3 functional · 🟢 4–5 good/excellent

## Top 3 blockers right now
1. 🚨 **No integration tests for payment service** — race condition had no layer to catch it; this gap is still open today.
2. ⚠️ **Reactive-only observability** — Sentry and E2E tests were added after the incident; no proactive detection layer exists yet.
3. ⚠️ **Test pyramid severely unbalanced** — 340 unit / 45 integration / 12 E2E (all brand new); critical paths not systematically covered.

## Improvement plan

### ⚡ Short term (this sprint)
- Add integration tests specifically covering the payment processing service, targeting concurrency and data-integrity paths first.
- Configure Sentry alerts for payment-related errors with dedicated on-call notification (not just a dashboard nobody watches).
- Audit the 12 new E2E tests: ensure they cover the broken flow and are reliable before trusting them as a safety net.
- Set up structured logging for the payment service (request IDs, user IDs, operation outcomes) to support the ongoing investigation and future incidents.
- Document the incident timeline and root cause in a blameless post-mortem; share with the full team.

### ◆ Medium term (this quarter)
- Build out the integration test layer systematically: target all service boundaries, especially anywhere money or user data moves.
- Introduce feature flags for payment flows to enable percentage-based rollout and instant kill-switch on regressions.
- Add performance monitoring (response times, DB query latency) alongside Sentry — error tracking alone is not full observability.
- Define a coverage policy: not 100%, but explicit targets for critical paths (payment, auth, data mutations).
- Run a DX survey with the team: identify where developers feel the most friction and what they wish was different.
- Establish Conventional Commits and connect commit messages to ticket IDs — git history is currently an untapped forensics tool.

### ◎ Long term (this half)
- Embed quality ownership into team rituals: test coverage reviewed in sprint retros, not just QA-tracked separately.
- Apply the DFER loop (Deprecate → Fix → Enforce → Repeat) to linting and static analysis to raise code quality incrementally without big-bang effort.
- Evaluate canary releases and gradual rollout for high-risk changes — a 5% rollout of a payment change is far safer than 100% at once.
- Grow the integration test suite toward parity with the unit layer; rebalance the pyramid so unit > integration > E2E by count and by CI run time.
- Reassess CI pipeline speed: 12 minutes is acceptable now, but as the test suite grows it will become a feedback bottleneck — plan ahead.

## Action items
| ID | Description | Horizon | Owner | Status |
|----|-------------|---------|-------|--------|
| A1 | Write integration tests for payment service concurrency paths | ⚡ short | | ○ open |
| A2 | Configure Sentry alerts with on-call routing for payment errors | ⚡ short | | ○ open |
| A3 | Audit and validate the 12 new E2E tests for reliability | ⚡ short | | ○ open |
| A4 | Add structured logging to payment service | ⚡ short | | ○ open |
| A5 | Run blameless post-mortem and share findings with team | ⚡ short | | ○ open |
| A6 | Expand integration test layer to all service boundaries | ◆ medium | | ○ open |
| A7 | Introduce feature flags for payment and high-risk flows | ◆ medium | | ○ open |
| A8 | Add performance monitoring (latency, DB query times) | ◆ medium | | ○ open |
| A9 | Define and document critical-path coverage policy | ◆ medium | | ○ open |
| A10 | Run DX survey with engineering team | ◆ medium | | ○ open |
| A11 | Adopt Conventional Commits with ticket references | ◆ medium | | ○ open |
| A12 | Embed coverage review into sprint retros | ◎ long | | ○ open |
| A13 | Introduce DFER loop for linting and static analysis | ◎ long | | ○ open |
| A14 | Evaluate canary/gradual rollout for high-risk deploys | ◎ long | | ○ open |
| A15 | Rebalance test pyramid as integration suite matures | ◎ long | | ○ open |
