## Engineering Quality Assessment — Norsk Mobility AS

---

### Situation Summary

You experienced a data-corrupting race condition in payment processing that affected 2,100 users, with no monitoring in place to catch it. That is the defining fact of this assessment. Everything else flows from it.

---

### Area Scores (1–5)

| Area | Score | Rationale |
|---|---|---|
| Test Coverage & Strategy | 2/5 | Reasonable unit test count for 14 engineers, but zero concurrency/race condition tests evident, no E2E history, integration test count is thin for a payment-handling platform |
| CI/CD Maturity | 2.5/5 | GitHub Actions with a manual gate is a functional baseline, but 12-minute pipelines with no apparent contract or load testing suggests the pipeline is not catching the right failures |
| Observability | 1.5/5 | Sentry added 3 days ago — users were your monitoring before that. No mention of structured logging, distributed tracing, or uptime checks. Score would be 1 without the Sentry addition |
| Incident Response | 2/5 | Partial data recovery is positive, investigation is ongoing (appropriate), but the absence of runbooks, on-call rotation, or alerting prior to this incident means the process was improvised |
| Data Integrity Practices | 1.5/5 | Race condition corrupting payment records points to missing DB-level constraints, absent pessimistic/optimistic locking patterns, and no transactional boundary enforcement in critical paths |
| Release Practices | 3/5 | 1–2 deploys per week with a manual gate is conservative and not the problem — this is actually appropriate for your stage. The manual gate gave you a moment of control you were not otherwise positioned to use well |

**Overall: 2/5** — You have the scaffolding of engineering practices but critical gaps in the highest-risk areas of your product.

---

### Recommendations by Priority

---

#### Priority 1 — Stop the bleeding (this week)

**1.1 — Audit and harden the payment processing service now, before resuming normal velocity.**

Do not ship new features to the payment service until you have completed a line-by-line review of every place money moves. Specifically:
- Map every code path that reads then writes a payment record.
- Identify all missing `SELECT FOR UPDATE` or equivalent pessimistic locks in PostgreSQL.
- Audit Django ORM usage for patterns like `obj.field += 1; obj.save()` — these are not atomic and will corrupt data under concurrency.
- Enforce atomic transactions with `transaction.atomic()` on all payment mutations.
- Add PostgreSQL-level constraints (unique constraints, check constraints) as a last line of defense that no application bug can bypass.

**1.2 — Add targeted concurrency tests to the payment service before any further deploys.**

Use `threading` or `pytest-xdist` to write tests that hammer payment endpoints concurrently and assert on final state. These tests should run in CI and block deploy if they fail. The goal is not full coverage — it is a regression harness for exactly the class of bug that just hit you.

**1.3 — Set up Sentry alerts properly, not just collection.**

Sentry logging events without alerting is a logbook nobody reads. Configure alert rules for new error types in the payment service with immediate Slack/PagerDuty notification. Add a Sentry release integration so you know which deploy introduced an error.

---

#### Priority 2 — Structural gaps to close in the next 2–4 weeks

**2.1 — Introduce observability with intent, not just error capture.**

Sentry covers exceptions. You need:
- Structured logging (Python `structlog` is idiomatic for Django) with consistent fields: `user_id`, `payment_id`, `request_id`, trace context.
- A metrics layer. For your stack, Prometheus + Grafana or a hosted equivalent (Datadog, Grafana Cloud) is appropriate. Instrument payment initiation, completion, failure rates, and latency as a minimum.
- Uptime monitoring on critical endpoints (Better Uptime, Checkly, or equivalent).

Without metrics, you cannot distinguish "one user had a bad time" from "payment processing is silently failing at 5% rate."

**2.2 — Add database-level migration tests and schema change review to your CI pipeline.**

Django migrations with missing `db_index=True`, missing constraints, or lock-heavy operations on large tables are a common source of production incidents on PostgreSQL. Add `django-test-migrations` or equivalent, and make schema review a required step in your PR process for any migration touching payment or user tables.

**2.3 — Write an incident runbook for payment failures.**

You improvised this incident response. Before the next one:
- Define severity levels (P1 = data corruption or financial impact, P2 = degraded service, P3 = cosmetic).
- Write a P1 runbook: who gets paged, what they check first, when to roll back, when to take the service down, who communicates to users.
- Assign an on-call rotation. 14 engineers with no on-call means nobody is on-call.

**2.4 — Expand integration test coverage around data boundaries.**

45 integration tests for a B2C mobility platform with payment processing is thin. Specifically lacking: tests that verify transactional rollback on failure, tests that assert on DB state (not just API response), and tests that cover the mobile app → backend → payment processor flow end to end. Your 12 new E2E tests are a start; make sure they cover the payment happy path and at least two failure modes.

---

#### Priority 3 — Quality maturity improvements for the next 1–3 months

**3.1 — Add a contract testing layer for the mobile app / backend interface.**

React Native apps with a Django backend are a common source of silent breakage: the backend changes a response shape, the app breaks for users on older versions who haven't updated. Introduce Pact or a simple snapshot-based contract test. This is especially important given you have a mobile app where users control their own update timing.

**3.2 — Introduce load/stress testing for payment-adjacent endpoints.**

The race condition was a concurrency issue. Concurrency issues do not appear at low traffic. Add k6 or Locust to your CI pipeline (or as a scheduled job) to run a realistic concurrency scenario against a staging environment. This does not need to be exhaustive — 50 concurrent payment initiations hitting your staging DB is enough to expose locking gaps.

**3.3 — Formalize your definition of "ready to deploy."**

Your manual approval gate is good. But right now it is a human looking at something without a checklist. Create a written deploy checklist that includes: all CI checks green, Sentry error rate in baseline range for past 24h, no open P1/P2 incidents, DB migrations reviewed. This transforms a habit into a repeatable process that survives team turnover.

**3.4 — Invest in test quality, not just test count.**

340 unit tests is a reasonable number. The question is whether they test the right things. Introduce mutation testing (`mutmut` for Python) on the payment service specifically. If your tests do not catch mutations in your payment logic, they are not providing the safety you think they are.

---

### What is Working

- The manual approval gate before production is the right instinct for your deployment frequency. Do not let anyone talk you into removing it until your observability and automated test quality are significantly higher.
- 1–2 deploys per week is appropriate discipline for a B2C platform at your stage. Faster is not better when you lack the safety net.
- Adding Sentry and writing E2E tests in response to this incident shows the right organizational response. The concern is whether it persists as structural investment or fades once the immediate pressure does.

---

### Closing Assessment

The payment incident was not bad luck. It was the predictable outcome of shipping a concurrent, transactional system without concurrency tests, database-level guards, or observability. The good news is that the fixes are known and implementable. The risk is that the team addresses symptoms (add monitoring, add tests) without addressing the underlying pattern: payment and financial flows need a higher standard of rigor than the rest of the application, and that standard needs to be enforced structurally — in the database schema, in the test suite, in the deploy checklist — not just in individual developer care.

Prioritize data integrity over feature velocity for the next four weeks. The platform is three years old. The trust you are rebuilding with 2,100 affected users will take longer to recover than any feature you delay.
