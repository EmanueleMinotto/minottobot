# Engineering Audit Report — Norsk Mobility AS
**Date:** 2026-03-26
**Context:** Post-incident review following payment data corruption event
**Team:** 14 engineers + 2 QA | **Stack:** Python/Django, React Native, PostgreSQL

---

## Scorecard

| Dimension | Score | Signal |
|---|---|---|
| Test Coverage & Quality | 4/10 | E2E tests only added last week; no concurrency tests visible |
| Monitoring & Observability | 3/10 | Sentry added 3 days ago; previously blind |
| CI/CD Pipeline | 5/10 | GH Actions in place, 12-min build, no automated quality gates |
| Deployment Practices | 5/10 | Manual gate is good; frequency reasonable |
| Incident Response Readiness | 2/10 | No prior monitoring; users reported breakage; partial recovery only |
| Data Integrity & Safety | 3/10 | Race condition exposed missing DB-level concurrency guards |
| **Overall** | **3.7/10** | **Significant remediation required** |

---

## Key Findings & Recommendations (condensed)

**Data Integrity (most urgent):** The race condition almost certainly traces to missing `SELECT FOR UPDATE` or optimistic locking on payment record writes. Immediate audit of every read-then-write in the payment service is needed. PostgreSQL PITR (WAL archiving) must be verified and enabled — "partial recovery" means you may not have it.

**Monitoring:** Sentry is a start but covers only errors. No latency, throughput, DB performance, or business metrics (payment success rate). Add `django-prometheus` or Datadog/Grafana Cloud. Add uptime monitoring for critical endpoints.

**Testing:** The 340 unit / 45 integration / 12 E2E ratio leaves the integration layer undertested — exactly where race conditions live. Write a regression test that reproduces the race condition first. Then add concurrency tests and enforce a coverage threshold (~70%) as a CI gate.

**Incident Response:** No runbook, no on-call rotation, users detected the outage. A blameless post-mortem must be completed and shared. Affected users need direct, honest communication.

**CI/CD:** Split into fast (<3 min: lint + unit) and slow (<10 min: integration + E2E) stages. Add `mypy`, `bandit`, `safety`. Add a staging environment so deploys flow CI → staging (auto) → production (manual gate).

**Deployments:** Feature flags for all payment changes. Manual approval gate should enforce a documented checklist, not be a rubber-stamp.
