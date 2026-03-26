# Minottobot audit report — FinanceCore Ltd — 2026-03-26

## Repos in scope
- (not specified — team-reported data only)

> ⚠️ **No code access** — this audit is based on team-reported data only. Findings could not be verified against the codebase.

## Phase 0 — Quantitative baseline

| # | Question | Answer | Finding |
|---|----------|--------|---------|
| 1 | Team size | 85 engineers, 8 product teams | Central QA guild of 6 — not embedded per team |
| 2 | Total test count | ~12,000 (~30% flaky) | ~3,600 tests are unreliable and likely ignored |
| 3 | Average CI run time | 47 minutes | Significant DX friction; developers avoid re-runs |
| 4 | Deployment frequency | Biweekly, 6-hour process with manual sign-offs | Very low cadence; high coordination cost |
| 5 | Last month's CI success rate % | **Not provided** | ⚠️ Gap — inability to answer is itself a finding |
| 6 | MTTR from production incidents | ~4 hours | High for financial services |
| 7 | Test coverage % | **Not provided** | ⚠️ Gap — no coverage baseline tracked |
| 8 | Tests currently skipped/disabled | **Not provided** | ⚠️ Gap — flakiness suggests many are de-facto disabled |
| 9 | Days since last production incident | **Not provided** | 2 P1 + 1 P2 per month implies recent |
| 10 | Open bugs older than 30 days | **Not provided** | ⚠️ Gap — backlog health unknown |

Five of ten baseline numbers are unknown. For a 20-year-old financial services company with 85 engineers, the absence of these metrics is a structural gap.

---

## Executive summary (3 bullets max, each under 20 words)
- 30% flaky tests and a 47-minute Jenkins pipeline destroy developer trust and feedback loops.
- Biweekly deploys with 6-hour manual sign-offs slow delivery and accumulate release risk.
- Central QA guild model creates ownership gaps; teams treat quality as someone else's problem.

## Area scores (1 = critical · 5 = excellent)
| Area                    | Score | One-line finding                                           |
|-------------------------|-------|------------------------------------------------------------|
| 🔴 CI/CD                |  2/5  | 47-min Jenkins build, biweekly deploys, no team ownership  |
| 🔴 Testing              |  2/5  | 30% flaky tests; no coverage baseline; pyramid unknown     |
| 🟡 Code review          |  3/5  | 3-approval policy exists but hotfix bypass is routine      |
| 🔴 Monitoring           |  2/5  | No monitoring tool named; 4-hour MTTR; 3 incidents/month   |
| 🔴 Developer Experience |  2/5  | 47-min CI, biweekly deploys, CI team silo, legacy Jenkins  |
| 🔴 Ownership & culture  |  2/5  | Central QA guild; quality not embedded in product teams    |

> 🔴 1–2 critical/gap · 🟡 3 functional · 🟢 4–5 good/excellent

---

## Top 3 blockers right now
1. 🚨 **Flaky test epidemic** — 3,600 flaky tests means the CI signal is untrustworthy; developers learn to ignore failures, eroding the entire safety net.
2. 🚨 **47-minute Jenkins pipeline with no team ownership** — a build from 2011, maintained by a separate CI team, blocks fast feedback and prevents product teams from improving their own quality tooling.
3. ⚠️ **Biweekly release cycle with 6-hour manual deployments** — in financial services, infrequent large releases accumulate risk; 6-hour manual sign-offs are a process liability, not a safety net.

---

## Improvement plan

### ⚡ Short term (this sprint)
- Quarantine all known flaky tests into a separate CI stage ("quarantine suite") so the main pipeline signal becomes trustworthy immediately — do not delete, investigate in parallel.
- Instrument the main pipeline with a build time breakdown to identify the slowest stages in Jenkins; visibility is the prerequisite for improvement.
- Add error tracking (Sentry) to both Java Spring Boot services and React frontend — this is the fastest way to reduce MTTR from 4 hours and start catching incidents before users report them.
- Define and publish the 5 most-critical user journeys for FinanceCore Ltd — these become the immediate target for E2E test coverage.

### ◆ Medium term (this quarter)
- Migrate CI ownership from the central CI team to each product team's codebase — Jenkinsfiles (or a migration to GitHub Actions/GitLab CI) should live in the repo and be owned by the team that runs them.
- Introduce a parallel fast-feedback pipeline: unit tests only, target under 5 minutes, runs on every PR. Reserve the 47-minute full build for pre-merge or nightly.
- Establish a flaky-test remediation rotation: dedicate one engineer per sprint per team to investigate and fix flaky tests in the quarantine suite. Set a target to reduce flaky count by 50% within the quarter.
- Implement a feature flag system (LaunchDarkly or Unleash) to decouple deploy from release — this is the prerequisite for increasing deployment frequency safely.
- Mandate that each product team has a designated quality champion (not a QA title — a dev who co-owns quality practices). The central QA guild shifts from "doing QA" to "enabling teams."
- Capture and track the 5 missing Phase 0 metrics (CI success rate, coverage %, skipped tests, days since last incident, open bugs >30 days) — you cannot improve what you don't measure.

### ◎ Long term (this half)
- Move from biweekly releases to weekly or on-demand deploys — this requires the feature flag system, team-owned CI, and a healthy test suite all in place first.
- Apply the DFER loop (Deprecate → Fix → Enforce → Repeat) to code quality standards across Java Spring Boot services: introduce lint/static analysis rules as warnings first, clean as you touch, promote to errors in CI over time.
- Build integration test coverage at the microservice boundary layer — Java Spring Boot services calling Oracle DB and communicating with each other represent the highest-value, currently untested layer.
- Establish a blameless incident review process with structured post-mortems; a 4-hour MTTR in financial services is a risk that requires cultural change alongside tooling.
- Define an explicit test pyramid target per team: e.g., 60% unit / 30% integration / 10% E2E, and make it visible in CI dashboards.

---

## Action items
| ID | Description | Horizon | Owner | Status |
|----|-------------|---------|-------|--------|
| A1 | Quarantine flaky tests into separate CI stage | ⚡ short | QA Guild | ○ open |
| A2 | Instrument Jenkins pipeline for build time breakdown per stage | ⚡ short | CI Team | ○ open |
| A3 | Add Sentry to Spring Boot services and React frontend | ⚡ short | Per team | ○ open |
| A4 | Document top 5 critical user journeys for E2E target | ⚡ short | QA Guild + PMs | ○ open |
| A5 | Transfer CI pipeline ownership (Jenkinsfiles) to product teams | ◆ medium | CI Team + Leads | ○ open |
| A6 | Create fast-feedback PR pipeline (unit tests only, <5 min target) | ◆ medium | CI Team | ○ open |
| A7 | Launch flaky-test remediation rotation (1 eng/sprint/team) | ◆ medium | Engineering Leads | ○ open |
| A8 | Evaluate and adopt a feature flag system (LaunchDarkly or Unleash) | ◆ medium | Platform Team | ○ open |
| A9 | Designate a quality champion per product team | ◆ medium | Engineering Leads | ○ open |
| A10 | Capture the 5 missing Phase 0 baseline metrics and publish dashboard | ◆ medium | QA Guild | ○ open |
| A11 | Migrate to weekly or on-demand deploys (pending A6, A7, A8) | ◎ long | Engineering Leads | ○ open |
| A12 | Apply DFER loop to Java Spring Boot static analysis | ◎ long | Per team | ○ open |
| A13 | Build integration test layer for microservice-to-DB boundaries | ◎ long | Per team | ○ open |
| A14 | Establish blameless post-mortem process for production incidents | ◎ long | Engineering Leads | ○ open |
| A15 | Define per-team test pyramid targets and surface in CI dashboards | ◎ long | QA Guild | ○ open |
