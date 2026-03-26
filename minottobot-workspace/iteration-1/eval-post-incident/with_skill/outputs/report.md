# Minottobot audit report — Norsk Mobility AS — 2026-03-25

## Repos in scope
- minottobot (Python/Django backend, React Native mobile app, PostgreSQL)

## Executive summary
- Payment incident exposed zero monitoring and no concurrency test coverage in a financial-critical service.
- Test suite is heavily unit-weighted with 12 E2E tests added reactively post-incident, not proactively.
- Monitoring added 3 days ago is a start; it is not yet a safety net — it needs configuration, alerting, and coverage.

## Area scores (1 = critical · 5 = excellent)

| Area                 | Score | One-line finding                                          |
|----------------------|-------|-----------------------------------------------------------|
| CI/CD                |  3/5  | GitHub Actions pipeline works; 12-min runtime is acceptable, but no automated quality gates beyond tests. |
| Testing              |  2/5  | Inverted pyramid risk: E2E suite is reactive and untested under load; concurrency and integration coverage is thin. |
| Code review          |  3/5  | Manual approval before production is good discipline; review standards unknown. |
| Monitoring           |  1/5  | Sentry added 3 days ago after users reported breakage — alerting, dashboards, and on-call runbooks do not yet exist. |
| Developer Experience |  3/5  | 12-minute CI is reasonable; local dev environment and seeding practices unknown. |
| Ownership & culture  |  3/5  | Team is shaken but engaged — 12 E2E tests shipped in one week shows responsiveness. |

## Top 3 blockers right now
1. No production observability that would have caught the race condition before users reported it — Sentry alone is insufficient for data-integrity failures.
2. Payment processing service has no concurrency or integration tests; the race condition path is still unguarded in CI.
3. No alerting, on-call rotation, or incident runbooks — the next incident will be discovered the same way this one was.

## Improvement plan

### Short term (this sprint)
- Configure Sentry alerts with severity thresholds; assign an on-call rotation immediately.
- Add database-level transaction integrity checks and row-level locking to the payment service; write regression tests that reproduce the race condition.
- Write a minimal incident runbook for payment failures covering detection, escalation, and rollback steps.
- Add a CI quality gate: block merges to main if payment-service integration tests fail.
- Audit PostgreSQL transaction isolation levels across all payment flows; confirm SELECT FOR UPDATE or equivalent is applied.

### Medium term (this quarter)
- Instrument the backend with structured logging and a metrics layer (Prometheus + Grafana or Datadog) targeting p95 latency, error rate, and payment success rate.
- Build out integration test coverage for all critical financial flows (charge, refund, idempotency, retry logic).
- Introduce a test pyramid review: realign toward more integration tests and fewer brittle E2E tests for the mobile layer.
- Define and enforce a code review checklist that explicitly flags concurrency-sensitive code and financial transactions.
- Establish a deployment checklist that includes a rollback plan and database migration safety check before every production deploy.

### Long term (this half)
- Introduce contract testing between the mobile app and the Django API to catch interface regressions before E2E.
- Build a chaos/concurrency test harness for the payment service (e.g., locust-based load tests targeting race conditions).
- Formalize a post-mortem process: blameless, structured, with action items tracked to closure — start with this incident.
- Evaluate feature flags to enable partial rollouts and limit blast radius for payment-related changes.
- Define SLOs for payment success rate, API error rate, and mobile crash rate; tie them to automated alerts.

## Action items

| ID  | Description | Horizon | Owner | Status |
|-----|-------------|---------|-------|--------|
| A1  | Configure Sentry alert rules and assign initial on-call rotation | short | | open |
| A2  | Write regression test reproducing the payment race condition | short | | open |
| A3  | Audit and fix transaction isolation on all payment DB queries | short | | open |
| A4  | Write payment incident runbook (detect, escalate, rollback) | short | | open |
| A5  | Add CI gate blocking merges if payment integration tests fail | short | | open |
| A6  | Add structured logging and metrics to Django payment service | medium | | open |
| A7  | Build Grafana/Datadog dashboard: payment success rate, error rate, latency | medium | | open |
| A8  | Expand integration test suite to cover all financial flows | medium | | open |
| A9  | Define and publish code review checklist with concurrency flag | medium | | open |
| A10 | Add deployment checklist with rollback plan and migration check | medium | | open |
| A11 | Run blameless post-mortem for the payment incident; publish findings | medium | | open |
| A12 | Introduce contract testing between React Native app and Django API | long | | open |
| A13 | Build concurrency/load test harness for payment service | long | | open |
| A14 | Define SLOs for payment success rate, API error rate, crash rate | long | | open |
| A15 | Evaluate and implement feature flags for payment-related deploys | long | | open |
