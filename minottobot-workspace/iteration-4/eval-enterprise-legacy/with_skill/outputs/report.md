# Minottobot audit report — FinanceCore Ltd — 2026-03-27

## Repos in scope
- FinanceCore Ltd monorepo (Java Spring Boot microservices, Oracle DB, React frontend)

> ⚠️ **No code access** — this audit is based on team-reported data only. Findings could not be verified against the codebase.

## Executive summary (3 bullets max, each under 20 words)
- 30% flaky tests and a 47-minute CI build destroy developer trust and feedback speed.
- Biweekly releases with 6-hour manual deployments create dangerous release bottlenecks for a financial product.
- Quality ownership is fragmented: no per-team QA, hotfix bypasses signal a process that bends under pressure.

## Area scores (1 = critical · 5 = excellent)
| Area                    | Score | One-line finding                                    |
|-------------------------|-------|-----------------------------------------------------|
| 🔴 CI/CD                |  2/5  | 47-min builds; 15-year-old Jenkins; no fast feedback |
| 🔴 Testing              |  2/5  | 30% flaky tests; suite is actively distrusted        |
| 🟡 Code review          |  3/5  | 3-approval policy exists but bypassed for hotfixes   |
| 🟡 Monitoring           |  3/5  | Incidents tracked; MTTR 4h signals visibility gaps   |
| 🟡 Developer Experience |  3/5  | Slow CI and flaky tests erode daily DX               |
| 🟡 Ownership & culture  |  3/5  | Central QA guild; per-team ownership unclear         |

> 🔴 1–2 critical/gap · 🟡 3 functional · 🟢 4–5 good/excellent

## Top 3 blockers right now
1. 🚨 **30% flaky test rate** — the test suite cannot be trusted; developers have learned to ignore failures, masking real regressions in a financial system.
2. 🚨 **47-minute CI build** — feedback is too slow to be actionable; developers cannot iterate safely and are incentivised to batch or skip checks.
3. ⚠️ **Biweekly release window + hotfix bypass** — infrequent releases create pressure that causes teams to skip review gates; a compounding risk in a regulated environment.

## Improvement plan

### ⚡ Short term (this sprint)
- Quarantine all known flaky tests: tag them, exclude from the blocking gate, and open a dedicated remediation backlog. Stop tolerating noise.
- Identify and document the 5 slowest CI job segments in the Jenkins pipeline; create a baseline for improvement targeting.
- Mandate that hotfix PRs require at minimum 1 senior approval and a post-deploy review ticket — no exception path without a trace.

### ◆ Medium term (this quarter)
- Migrate CI pipeline to a modern platform (GitHub Actions or GitLab CI): parallelise test execution to bring build time under 15 minutes.
- Fix or delete flaky tests systematically — target below 5% flakiness rate; enforce via CI flakiness tracking metric.
- Introduce feature flags for new development to decouple deploy from release; this enables more frequent deployments and reduces hotfix pressure.
- Define a per-team quality ownership model: assign a quality champion per product team, supported by the central QA guild rather than replacing it.
- Automate the 6-hour deployment process: eliminate manual sign-off steps in favour of automated smoke tests and a single human approval gate.

### ◎ Long term (this half)
- Move toward weekly or continuous deployment cadence, backed by feature flags and automated rollback capability.
- Rebuild test pyramid balance: audit current test distribution across unit/integration/E2E layers; likely gap is integration coverage for microservice boundaries.
- Instrument production observability to reduce MTTR below 1 hour: structured logging, distributed tracing (OpenTelemetry), and alerting on error-rate thresholds.
- Establish Conventional Commits and OpenAPI documentation as team standards via DFER: introduce as lint warnings, enforce in CI once adoption is stable.
- Run a quality ownership retrospective across all 8 product teams to surface where "QA will catch it" thinking persists and address it structurally.

## Action items
| ID | Description | Horizon | Owner | Status |
|----|-------------|---------|-------|--------|
| A1 | Quarantine flaky tests and open remediation backlog | ⚡ short | QA guild | ○ open |
| A2 | Profile and document 5 slowest CI job segments | ⚡ short | CI team | ○ open |
| A3 | Enforce minimum approval + post-deploy review for hotfixes | ⚡ short | Engineering leads | ○ open |
| A4 | Migrate CI to modern platform with parallelised test execution | ◆ medium | CI team | ○ open |
| A5 | Fix or delete flaky tests; target <5% flakiness rate | ◆ medium | QA guild + dev teams | ○ open |
| A6 | Introduce feature flag system for new development | ◆ medium | Platform team | ○ open |
| A7 | Define per-team quality champion model | ◆ medium | Engineering leadership | ○ open |
| A8 | Automate deployment process; replace manual sign-offs with smoke tests | ◆ medium | CI team + DevOps | ○ open |
| A9 | Move to weekly deployment cadence | ◎ long | Engineering leadership | ○ open |
| A10 | Audit and rebalance test pyramid across all microservices | ◎ long | QA guild | ○ open |
| A11 | Instrument OpenTelemetry tracing and error-rate alerting in production | ◎ long | Platform team | ○ open |
| A12 | Adopt Conventional Commits and OpenAPI via DFER lint pipeline | ◎ long | All teams | ○ open |
| A13 | Run quality ownership retrospective across 8 product teams | ◎ long | Engineering leadership | ○ open |
