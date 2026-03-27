# Minottobot audit report — Swiftly Inc — 2026-03-27

## Repos in scope
- swiftly-inc (Node.js API + React frontend + PostgreSQL)

> ⚠️ **No code access** — this audit is based on team-reported data only. Findings could not be verified against the codebase.

## Executive summary (3 bullets max, each under 20 words)
- Zero tests and daily user-reported incidents signal a team in permanent reactive firefighting mode.
- Deployments are manual, unguarded, and go straight to production with no staging buffer.
- Code review is informal and inconsistent; no shared ownership of quality exists yet.

## Area scores (1 = critical · 5 = excellent)
| Area                    | Score | One-line finding                     |
|-------------------------|-------|--------------------------------------|
| 🔴 CI/CD                |  2/5  | CI exists but only lints; deploys are fully manual |
| 🔴 Testing              |  1/5  | Zero tests across the entire codebase |
| 🔴 Environments         |  1/5  | No staging; local and production only |
| 🔴 Monitoring           |  1/5  | Bugs found by users, not by systems  |
| 🟡 Code review          |  3/5  | Happens informally, no enforced policy |
| 🟡 Ownership & culture  |  3/5  | Small team, good potential; quality not yet shared |

> 🔴 1–2 critical/gap · 🟡 3 functional · 🟢 4–5 good/excellent

## Top 3 blockers right now
1. 🚨 **No monitoring** — 1 incident/day reported by users means the team is always the last to know.
2. 🚨 **Zero tests** — every deploy is a gamble; no automated safety net exists at any layer.
3. ⚠️ **No staging environment** — production is the only place to validate changes, multiplying incident risk.

## Improvement plan

### ⚡ Short term (this sprint)
- Add Sentry (or equivalent) to the Node.js API and React frontend for real-time error tracking in production.
- Set up a basic uptime/health alert (e.g., Better Uptime or a simple Heroku health check) so the team detects outages before users do.
- Write 3–5 unit tests covering the most critical or most frequently broken API endpoints — not for coverage, for momentum.
- Freeze the current ESLint warning count in CI using `--max-warnings=N` to prevent regressions while the baseline is cleaned up.

### ◆ Medium term (this quarter)
- Provision a staging environment (Heroku pipeline review apps are a low-friction starting point for this stack).
- Automate deployments via a GitHub Actions workflow that deploys to staging on merge to `main`, and to production on manual approval.
- Establish a lightweight code review policy: every PR requires at least one approval before merge; no self-merges.
- Begin building out the test pyramid from the bottom: unit tests for the Node.js API using Jest, targeting the 10–15 most critical business logic paths.
- Adopt Conventional Commits to make git history readable and prepare for automated changelogs.

### ◎ Long term (this half)
- Add integration tests covering the API–database layer (e.g., Jest + a test database instance), targeting the paths most likely to produce data bugs.
- Introduce a basic E2E smoke test suite with Playwright covering the top 3 user journeys (signup, core action, billing if applicable).
- Establish a lightweight incident review habit: a 15-minute async post-mortem after each incident, focused on process improvement, not blame.
- Shift code review toward substantive feedback: introduce a lightweight PR template and a team-agreed definition of "ready to merge."
- Evaluate feature flags (e.g., Unleash or a lightweight home-grown toggle) to decouple deploy from release as deployment frequency grows.

## Action items
| ID | Description | Horizon | Owner | Status |
|----|-------------|---------|-------|--------|
| A1 | Add Sentry to API and frontend | ⚡ short | | ○ open |
| A2 | Add uptime/health alert | ⚡ short | | ○ open |
| A3 | Write first 3–5 unit tests for critical endpoints | ⚡ short | | ○ open |
| A4 | Freeze ESLint warning count in CI | ⚡ short | | ○ open |
| A5 | Provision staging environment | ◆ medium | | ○ open |
| A6 | Automate deploy pipeline (staging + production gate) | ◆ medium | | ○ open |
| A7 | Establish code review policy (min 1 approval, no self-merge) | ◆ medium | | ○ open |
| A8 | Build unit test coverage for top 10–15 API paths | ◆ medium | | ○ open |
| A9 | Adopt Conventional Commits | ◆ medium | | ○ open |
| A10 | Add integration tests for API–database layer | ◎ long | | ○ open |
| A11 | Add Playwright E2E smoke tests for top 3 user journeys | ◎ long | | ○ open |
| A12 | Introduce lightweight async incident post-mortems | ◎ long | | ○ open |
| A13 | Introduce PR template and definition of "ready to merge" | ◎ long | | ○ open |
| A14 | Evaluate feature flag tooling | ◎ long | | ○ open |
