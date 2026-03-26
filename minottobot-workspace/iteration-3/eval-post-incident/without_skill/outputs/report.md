# Engineering Quality Audit Report
**Organization:** Norsk Mobility AS
**Date:** 2026-03-26
**Trigger:** Post-incident review following payment data corruption event
**Auditor:** AI Engineering Quality Assessment

---

## Executive Summary

Norsk Mobility AS is a 3-year-old B2C mobility platform that has recently experienced a significant production incident: a race condition in the payment processing service corrupted payment records for approximately 2,100 users. This event, combined with the team's admission that monitoring and E2E testing were effectively absent until days before the audit, reveals a company that has been operating with substantial hidden risk for an extended period.

This report documents the current state of engineering quality across test coverage, CI/CD practices, observability, and process maturity. It identifies root causes, high-priority risks, and a concrete remediation roadmap.

The overall assessment is: **Critical — Immediate remediation required.** The team has responded to the incident with urgency (Sentry, E2E tests), but those responses are reactive and incomplete. Systemic gaps in concurrency safety, observability strategy, and testing philosophy remain unaddressed.

---

## 1. Incident Analysis

### 1.1 What Happened
Four days ago, a race condition in the payment processing service corrupted payment records for 2,100 users. Data recovery is partial and the investigation is ongoing.

### 1.2 Immediate Contributing Factors

**No pre-existing observability.** Sentry was added 3 days ago — meaning at the time of the incident, the team had zero structured error tracking, no alerting, and no way to detect the problem internally. Users discovered the corruption and reported it. This dramatically increases the blast radius of any defect and delays the detection-to-response window.

**No concurrency/integration test coverage for payment flows.** The presence of 340 unit tests, 45 integration tests, and 12 E2E tests (all written in the last week) strongly suggests that payment flows — the highest-risk surface in any B2C platform — were not covered by tests that exercise realistic concurrency patterns or end-to-end workflows prior to the incident.

**Race condition indicates insufficient database-level concurrency safeguards.** Race conditions in payment processing on a PostgreSQL-backed Django application typically arise from one or more of: missing `SELECT FOR UPDATE` locks, improper use of `F()` expressions, non-atomic multi-step update sequences, or missing unique constraints. The fact that this reached production with data corruption at scale suggests no defense-in-depth was in place.

### 1.3 Systemic Root Causes

| Root Cause | Evidence |
|---|---|
| Absence of proactive monitoring | Sentry added only 3 days ago; users reported breakage |
| Testing gaps in critical paths | E2E tests written in the last week only; race condition went undetected |
| Insufficient concurrency awareness | Race condition corrupted 2,100 records |
| No production readiness culture | Monitoring, alerting, and E2E coverage all added reactively |

---

## 2. Test Coverage Assessment

### 2.1 Current State

| Layer | Count | Notes |
|---|---|---|
| Unit | 340 | Reasonable volume, but unit tests cannot catch concurrency bugs |
| Integration | 45 | Low relative to a platform with payments and mobile API surface |
| E2E | 12 | All written in the last 7 days — coverage unknown, quality unvalidated |

**Team size context:** With 14 engineers + 2 QA, a healthy test suite for a B2C payment-processing platform should include substantially more integration tests. The ratio of unit:integration (roughly 7.5:1) is inverted from what is needed for a platform where correctness depends on service interactions, database transactions, and external API integration.

### 2.2 Critical Gaps

**Concurrency tests are almost certainly absent.** Race conditions are not catchable with unit tests or with standard Django `TestCase` / `APITestCase` (which wraps each test in a transaction). Proper concurrency testing requires either:
- Integration tests that spawn concurrent threads/processes against a real (or real-in-memory) database
- Load/stress test scenarios targeting payment endpoints

**Payment flow coverage.** There is no evidence of test coverage on:
- Double-charge prevention
- Concurrent payment submissions for the same user/order
- Partial failure rollback
- Idempotency key validation

**E2E test quality is unknown.** 12 E2E tests written in one week, at a moment of crisis, are at high risk of being incomplete, brittle, or focused on happy-path flows rather than the failure modes that matter. They need audit and structured expansion.

**Mobile API contract testing is not mentioned.** React Native apps are a brittle API consumer — breaking changes propagate to users slowly (app store release cycles). No mention of contract testing (e.g., Pact) is a risk.

### 2.3 Recommendations

1. **Immediate:** Audit the 12 E2E tests for payment flow coverage, concurrency scenarios, and rollback behavior.
2. **Short-term:** Write targeted concurrency integration tests for payment processing using `threading.Thread` or `asyncio` with real database transactions.
3. **Short-term:** Expand integration test suite to cover all payment state transitions, with particular emphasis on failure modes.
4. **Medium-term:** Establish test coverage thresholds enforced in CI (minimum line + branch coverage for `payments/` module).
5. **Medium-term:** Evaluate contract testing between the Django API and the React Native app.

---

## 3. CI/CD Assessment

### 3.1 Current State

- **Platform:** GitHub Actions
- **Pipeline duration:** ~12 minutes
- **Gate:** Manual approval before production deploy
- **Deployment frequency:** 1–2 times per week

### 3.2 Strengths

The manual approval gate before production is a positive control — it creates a human checkpoint before changes go live. The deployment frequency (1–2x/week) is low enough to allow careful review, which is appropriate for the current maturity level of the team's safety infrastructure.

### 3.3 Weaknesses

**12-minute CI is acceptable but not audited.** Without knowing what those 12 minutes cover, it is impossible to know whether the pipeline actually catches meaningful defects. If the pipeline primarily runs unit tests, it provides false confidence.

**No mention of static analysis, security scanning, or linting.** A mature CI pipeline for a payment platform should include:
- `bandit` or equivalent for Python security scanning
- `mypy` or `pyright` for type checking
- `eslint` / `prettier` for frontend consistency
- `safety` or `pip-audit` for dependency vulnerability scanning
- SAST tooling for secrets detection (e.g., `truffleHog`, `detect-secrets`)

**No mention of database migration safety checks.** Django migrations are a common source of production incidents. The pipeline should validate that migrations are reversible, do not perform locking operations on large tables, and pass a dry-run against a production-size dataset in staging.

**No staging environment mentioned.** The workflow appears to be: CI passes → manual approval → production. Without a staging environment that mirrors production (including data volume, connection pooling, and concurrency load), manual approval gates are reviewing against artificial conditions.

**Deployment frequency vs. incident recovery.** 1–2 deploys per week is conservative, but without feature flags or blue/green deployment, each deploy is a binary risk event. If a defect reaches production, the team cannot do a targeted rollback of a specific feature — they must roll back the entire release.

### 3.4 Recommendations

1. **Immediate:** Add `bandit`, `safety`/`pip-audit`, and a secrets scanner to the CI pipeline.
2. **Short-term:** Add `mypy` with strict mode for the payments module.
3. **Short-term:** Add a migration safety check step (e.g., `django-migration-linter`).
4. **Short-term:** Provision a staging environment that mirrors production topology.
5. **Medium-term:** Evaluate blue/green or canary deployment to reduce blast radius of each release.
6. **Medium-term:** Add structured test coverage reporting (e.g., `pytest-cov` + coverage gate) to CI.

---

## 4. Observability Assessment

### 4.1 Current State

- **Error tracking:** Sentry (added 3 days ago)
- **Metrics:** Not mentioned
- **Logging:** Not mentioned
- **Alerting:** Not mentioned
- **Uptime/availability monitoring:** Not mentioned

### 4.2 Critical Findings

**The team was flying blind until 3 days ago.** In a B2C payment platform 3 years into operation, the absence of structured error tracking is a severe maturity gap. The fact that users were reporting breakage rather than alerts triggering is the clearest possible signal that production failures have been underreported and underinvestigated for the platform's entire lifetime.

**Sentry alone is not sufficient.** Sentry captures exceptions and some performance data, but it does not provide:
- Infrastructure-level metrics (CPU, memory, database connection pool exhaustion)
- Business-level metrics (payment success rate, cart abandonment, user conversion)
- Latency histograms and SLO tracking
- Database slow query analysis
- Queue depth monitoring (if Celery or similar is in use)

**No structured logging.** Django's default logging is insufficient for forensic investigation of distributed incidents. The ongoing payment corruption investigation is likely being hampered by the absence of structured, queryable logs with request IDs and user context.

**Payment-specific observability is absent.** For a payment processing service, the following should be instrumented as first-class concerns:
- Payment attempt rate
- Payment success/failure rate by provider and reason code
- Duplicate transaction detection events
- Lock contention / retry counts
- Rollback events

### 4.3 Recommendations

1. **Immediate:** Establish structured JSON logging with correlation IDs for all payment service requests. This directly supports the ongoing incident investigation.
2. **Immediate:** Configure Sentry alerts for payment-related exceptions with immediate (< 5 minutes) notification to on-call.
3. **Short-term:** Deploy a metrics stack (Prometheus + Grafana, or Datadog, or equivalent). Instrument payment success rate as the primary SLO metric.
4. **Short-term:** Set up uptime monitoring (e.g., Better Uptime, Pingdom) with alerting to on-call rotation.
5. **Short-term:** Add database slow query logging and query analysis (PostgreSQL `pg_stat_statements`).
6. **Medium-term:** Define formal SLOs for the payment service (e.g., 99.9% success rate, p95 latency < 2s) and build dashboards and alerts around them.
7. **Medium-term:** Implement distributed tracing (OpenTelemetry) to correlate mobile app requests with backend processing.

---

## 5. Payment Processing Safety Assessment

This section is elevated due to the active incident.

### 5.1 Race Condition Prevention (Django + PostgreSQL)

The incident strongly suggests one or more of the following patterns are present in the codebase:

**Anti-pattern A: Non-atomic read-modify-write**
```python
# DANGEROUS — race condition between read and write
record = PaymentRecord.objects.get(id=payment_id)
record.amount += new_charge
record.save()
```

**Anti-pattern B: Missing SELECT FOR UPDATE**
```python
# DANGEROUS — two concurrent requests can both read the same state
record = PaymentRecord.objects.get(id=payment_id)
# ... decision logic based on record.status ...
record.status = 'processed'
record.save()
```

**Safe patterns that must be in place:**
- `PaymentRecord.objects.select_for_update().get(id=payment_id)` inside an `atomic()` block
- `F()` expressions for numeric updates: `PaymentRecord.objects.filter(id=payment_id).update(amount=F('amount') + new_charge)`
- Idempotency keys on payment creation endpoints
- Database-level unique constraints on (user_id, transaction_reference) or equivalent
- Retry logic with proper lock acquisition, not optimistic retry loops

### 5.2 Recommendations

1. **Immediate:** Audit all payment-related model updates for `select_for_update()` usage and `@transaction.atomic` decoration.
2. **Immediate:** Verify idempotency key implementation on payment creation endpoints.
3. **Immediate:** Review PostgreSQL isolation level — default `READ COMMITTED` may be insufficient; consider `REPEATABLE READ` or explicit locking for critical payment operations.
4. **Short-term:** Add database-level constraints (unique constraints, check constraints) as the last line of defense against data corruption.
5. **Short-term:** Write regression tests specifically for the race condition scenario using concurrent threads.

---

## 6. Process and Culture Assessment

### 6.1 Team Composition

14 engineers + 2 QA for a 3-year-old B2C platform is a reasonable size. The 7:1 engineer-to-QA ratio is workable if engineers take ownership of test quality, but the current test suite composition suggests QA has not been deeply integrated into the development workflow.

### 6.2 Post-Incident Response

The team's reactive additions (Sentry, E2E tests) within days of the incident indicate responsiveness and urgency, which is positive. However, reactive additions under pressure carry their own risks:
- E2E tests written in haste may codify existing incorrect behavior
- Sentry without alert tuning may generate noise that desensitizes the team
- The root cause of the race condition must be found and fixed, not patched around

### 6.3 Missing Processes

| Process | Status | Risk |
|---|---|---|
| On-call rotation | Not mentioned | High — who is responsible for production alerts? |
| Incident runbooks | Not mentioned | High — structured response accelerates recovery |
| Postmortem culture | Not mentioned | High — without postmortems, incidents recur |
| Change management | Manual approval gate only | Medium |
| Security review process | Not mentioned | High — payment data is regulated |
| Data backup and recovery testing | Not mentioned | Critical — partial data recovery from this incident |

### 6.4 Regulatory Considerations

As a payment-processing platform operating in the European market (Norsk = Norwegian), Norsk Mobility AS is subject to:
- **GDPR** — data corruption affecting 2,100 users may trigger a 72-hour breach notification obligation to Datatilsynet (the Norwegian DPA) if personal data was compromised
- **PSD2 / Strong Customer Authentication** — if payments are processed via bank integrations, SCA compliance is mandatory
- **PCI DSS** — if card data is processed, stored, or transmitted, PCI DSS compliance applies

The incident should be reviewed by legal counsel for breach notification obligations immediately if this has not already occurred.

### 6.5 Recommendations

1. **Immediate:** Conduct a formal postmortem for the payment corruption incident with a written report, root cause analysis, and action items.
2. **Immediate:** Establish an on-call rotation with defined escalation paths and paging integration with Sentry.
3. **Immediate:** Consult legal/compliance regarding GDPR notification obligations for the 2,100 affected users.
4. **Short-term:** Write incident runbooks for payment processing failures, database connectivity loss, and service degradation.
5. **Short-term:** Test data backup restoration — can the team fully restore the database from backup, and how long does it take?
6. **Medium-term:** Institute blameless postmortem culture for all P1/P2 incidents.
7. **Medium-term:** Schedule a PCI DSS / GDPR compliance audit if one has not been conducted.

---

## 7. Risk Register

| Risk | Likelihood | Impact | Priority |
|---|---|---|---|
| Second race condition incident in payments | High | Critical | P0 |
| Ongoing data corruption from undetected defects | Medium | Critical | P0 |
| GDPR breach notification non-compliance | Medium | High | P0 |
| Production defect with no alert (Sentry misconfigured) | High | High | P1 |
| E2E tests providing false confidence | High | Medium | P1 |
| Missing DR/backup recovery capability | Unknown | Critical | P1 |
| Mobile API breaking change reaching production | Medium | High | P1 |
| Dependency vulnerability in production | Medium | High | P2 |
| Migration causing production downtime | Low | High | P2 |

---

## 8. Prioritized Remediation Roadmap

### Phase 1 — Immediate (This Week)

These actions address active risk from the incident and prevent recurrence:

1. Complete the race condition root cause analysis; apply `select_for_update()` + `@transaction.atomic` fixes to all identified payment paths
2. Write regression test(s) for the specific race condition scenario
3. Enable Sentry alerts for payment exceptions with immediate on-call paging
4. Establish structured JSON logging with correlation IDs for payment service
5. Consult legal regarding GDPR notification obligations
6. Schedule a formal postmortem meeting with all stakeholders

### Phase 2 — Short-Term (Next 2–4 Weeks)

These actions close the largest systemic gaps:

1. Add `bandit`, `safety`, and secrets scanning to CI
2. Provision a staging environment mirroring production topology
3. Expand integration tests to cover all payment state transitions and failure modes
4. Add `mypy` strict typing to the payments module
5. Deploy Prometheus + Grafana (or equivalent) with payment success rate as primary SLO metric
6. Set up uptime monitoring with paging
7. Test full database backup restoration end-to-end
8. Add `django-migration-linter` to CI
9. Audit the 12 E2E tests for quality, coverage, and correctness

### Phase 3 — Medium-Term (Next 1–3 Months)

These actions raise the engineering baseline to production-grade:

1. Define formal SLOs for the payment service
2. Implement distributed tracing (OpenTelemetry)
3. Evaluate blue/green or canary deployment strategy
4. Institute blameless postmortem process
5. Conduct or commission a PCI DSS / GDPR compliance review
6. Evaluate contract testing for the React Native ↔ Django API boundary
7. Establish test coverage gates in CI (minimum coverage thresholds per module)

---

## 9. Summary Scorecard

| Domain | Score | Notes |
|---|---|---|
| Test Coverage | 3/10 | Volume present but wrong composition; critical paths uncovered |
| CI/CD | 4/10 | Pipeline exists but lacks security, typing, and migration safety |
| Observability | 2/10 | Sentry just added; no metrics, no structured logging, no SLOs |
| Payment Safety | 2/10 | Active incident; race conditions indicate fundamental gaps |
| Process Maturity | 3/10 | No postmortem culture, on-call rotation, or runbooks mentioned |
| **Overall** | **3/10** | **Critical — systemic gaps exposed by incident** |

---

## Closing Note

The payment corruption incident is a serious event, but it is also a forcing function for changes the platform needed regardless. The team's rapid response (Sentry, E2E tests) demonstrates good instincts. The priority now is to convert that urgency into a durable, systematic improvement program — not just patching the immediate hole, but rebuilding the engineering foundation to be worthy of the trust users place in a payment-handling service.

The 2,100 affected users deserve a public and internal commitment that the root cause has been found, fixed, and regression-tested — and that the monitoring, testing, and deployment infrastructure now in place makes a recurrence detectable within minutes rather than days.

---

*Report generated: 2026-03-26*
*Scope: Phase 0 Engineering Quality Audit — Post-Incident Review*
*Classification: Internal*
