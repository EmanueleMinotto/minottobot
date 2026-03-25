<!--
  Eval: post-incident
  Team: Norsk Mobility AS
  Input prompt: see evals.json id=3
  Generated: 2026-03-25
  Re-run: load minottobot/ skill, paste the prompt from evals.json id=3, capture output here
-->

# Minottobot audit report — Norsk Mobility AS — 2026-03-25

## Repos in scope
- norsk-api (Python + Django)
- norsk-mobile (React Native)

## Executive summary (3 bullets max, each under 20 words)
- A race condition in payment processing corrupted 2,100 user records four days ago; no regression test exists yet.
- Sentry was added three days ago — monitoring is brand new and unproven at this team's scale.
- The test suite has coverage but lacks concurrency and integration depth where it matters most.

## Area scores (1 = critical · 5 = excellent)
| Area                | Score | One-line finding                                        |
|---------------------|-------|---------------------------------------------------------|
| CI/CD               |  3/5  | 12-min pipeline with manual gate; functional but reactive|
| Testing             |  2/5  | E2E tests panic-added post-incident; race conditions untested |
| Code review         |  3/5  | Assumed functional; not flagged as a problem            |
| Monitoring          |  2/5  | Sentry added 3 days ago; no baseline, no alerts tuned   |
| Developer Experience|  3/5  | 12-min CI is reasonable; 1-2 deploys/week is workable   |
| Ownership & culture |  3/5  | Team responded quickly; incident still reactive not proactive |

## Top 3 blockers right now
1. **No regression test for the race condition that caused the incident.** The payment data corruption four days ago was caused by a concurrent write race condition. Until there is a test that reproduces and guards against this specific scenario, deploying the payment service carries the same risk as before the incident. This is the highest-priority item.
2. **Monitoring is three days old with no tuned alerts.** Sentry is collecting errors, but the team has not yet established what a normal error baseline looks like, what thresholds should trigger alerts, or who is responsible for reviewing incoming events. Raw Sentry data without process is not observability — it is noise.
3. **E2E tests written reactively cover symptoms, not root causes.** Writing 12 E2E tests in a week is a reasonable reaction, but E2E tests are too coarse-grained to catch a race condition in the payment service. The test pyramid for this service needs coverage at the integration and unit layer, specifically for concurrent scenarios.

## Improvement plan
### Short term (this sprint)
- **Write a regression test for the payment race condition.** Reproduce the concurrent write scenario in an integration test. This is the single most important thing to do this week. Until it exists, the fix is unverified and the incident can recur.
- **Add database-level uniqueness and integrity constraints** on payment records to prevent silent data corruption if a concurrent write slips through. This is a defence-in-depth measure, not a replacement for the test.
- **Establish a Sentry review ritual.** Assign one person to spend 15 minutes each morning this week reviewing new Sentry events. The goal is to build a baseline: what is normal noise, what is a signal. This is how alert thresholds get calibrated.

### Medium term (this quarter)
- Build an observability baseline for the payment service: error rate, payment success rate, p95 response time. These are the metrics that would have surfaced the incident before users did. Consider Grafana with Django's built-in metrics or a lightweight APM.
- Expand integration test coverage for concurrent operations across the payment and booking flows — not just the path that caused the incident, but adjacent paths that share the same state.
- Conduct a blameless post-mortem on the incident. The team is four days out — while it is still fresh, document the timeline, the contributing factors, and what would have caught it earlier. This is the document that teaches the next engineer who joins.

### Long term (this half)
- Work toward shift-left on concurrency: add a linting or static analysis step in CI that flags patterns known to cause race conditions in Django (e.g. non-atomic read-modify-write sequences on shared records).
- Mature the monitoring setup from "Sentry captures errors" to "we have SLOs and know when we are burning error budget." This is a quarter+ of work, not a weekend task.
- Formalise the incident response process so the next incident is handled by a playbook, not improvised under pressure.

## Action items
| ID | Description | Horizon | Owner | Status |
|----|-------------|---------|-------|--------|
| A1 | Write integration regression test for payment race condition | short | | open |
| A2 | Add DB-level integrity constraints on payment records | short | | open |
| A3 | Establish daily Sentry review ritual; calibrate alert thresholds | short | | open |
| A4 | Build observability baseline for payment service (error rate, p95, success rate) | medium | | open |
| A5 | Expand concurrent-operation integration tests across payment and booking | medium | | open |
| A6 | Conduct blameless post-mortem on the incident | medium | | open |
| A7 | Add CI linting for race-condition-prone Django patterns | long | | open |
| A8 | Mature monitoring to SLO/error-budget model | long | | open |
| A9 | Document and formalise incident response playbook | long | | open |

---

## Assertions

| # | Assertion | Pass? |
|---|-----------|-------|
| 1 | Output must reference the recent production incident explicitly | PASS — executive summary, Blocker #1, and A1 all explicitly reference the incident four days ago |
| 2 | Output must give at least one short-term action item | PASS — A1, A2, A3 are all short-horizon items |
| 3 | Output must recommend monitoring or observability as a priority | PASS — Blocker #2 names monitoring; A3 (short), A4 (medium), A8 (long) address it as a priority |
| 4 | Output must not recommend psychological safety without citing a specific data point | PASS — psychological safety is not mentioned; team culture is referenced only through observable behaviours (quick incident response) |
| 5 | Output must reference the race condition or production data corruption | PASS — Blocker #1, A1, and the executive summary all name the race condition and data corruption explicitly |
