# Minottobot audit report — Norsk Mobility AS — 2026-03-26

## Repos in scope
- norsk-mobility-backend (Python / Django)
- norsk-mobility-mobile (React Native)
- norsk-mobility-db (PostgreSQL)

> No codebase inspection was performed. Findings are based entirely on Phase 0 data provided by the team.

## Executive summary
- Payment race condition corrupted 2,100 records; monitoring and test coverage were both absent at incident time.
- Sentry and E2E tests were both added reactively post-incident, not as proactive quality investments.
- CI exists but the test suite, monitoring baseline, and incident processes are all new and untested under load.

## Area scores (1 = critical · 5 = excellent)
| Area                 | Score | One-line finding                                      |
|----------------------|-------|-------------------------------------------------------|
| CI/CD                |  3/5  | GitHub Actions runs ~12 min; manual gate adds latency |
| Testing              |  2/5  | E2E suite one week old; no concurrency/race tests     |
| Code review          |  3/5  | Manual approval gate exists; depth unknown            |
| Monitoring           |  2/5  | Sentry added 3 days ago; zero baseline established    |
| Developer Experience |  2/5  | Reactive tooling; trust in test suite not yet earned  |
| Ownership & culture  |  2/5  | Users reported the incident before the team knew      |

## Top 3 blockers right now
1. **No concurrency or data-integrity tests for the payment service.** The race condition is still not covered by automated tests. Until it is, the fix cannot be verified and regression is possible.
2. **Monitoring has no baseline or alerts.** Sentry was added 3 days ago. The next incident will still be reported by users first.
3. **E2E tests are 7 days old and written under pressure.** Tests written reactively after an incident are often shallow, brittle, or missing the exact scenario that failed.

## Improvement plan

### Short term (this sprint)
- Write regression test for the payment race condition covering the exact corruption scenario.
- Add integration tests for payment processing: concurrent writes, idempotency, transaction rollback in PostgreSQL.
- Configure Sentry alerts for error spikes, unhandled exceptions, and payment-critical errors.
- Audit the 12 new E2E tests: verify they cover real user flows, remove duplicates, document intent.
- Run a blameless post-mortem and share findings team-wide.

### Medium term (this quarter)
- Build integration test coverage for all Django service boundaries, focusing on PostgreSQL transactions and concurrent operations.
- Establish a test coverage baseline with pytest-cov (track progress, do not chase 100%).
- Add structured logging and Sentry Performance to the payment service.
- Introduce SELECT FOR UPDATE or equivalent locking in payment service hot paths.
- Evaluate replacing the manual deploy gate with automated smoke tests.
- Reduce CI run time below 10 minutes.

### Long term (this half)
- Shift Left: make test-writing a required step in the PR process, not a post-development activity.
- Shift Right: expand Sentry to include React Native mobile crash reporting.
- Establish a quarterly incident review cadence using Sentry data.
- Adopt Conventional Commits for a meaningful audit trail on a payment platform.
- Build a blameless incident culture: shared retros, public post-mortems, team-wide quality ownership.

## Phase 0 data gaps
| Question | Status |
|----------|--------|
| CI success rate % last month | Not provided |
| MTTR from the payment incident | Not provided — investigation ongoing |
| Test coverage % | Not tracked |
| Skipped/disabled tests | Not known |
| Open bugs older than 30 days | Not provided |

## Action items
| ID  | Description | Horizon | Owner | Status |
|-----|-------------|---------|-------|--------|
| A1  | Write regression test for the payment race condition | short | | open |
| A2  | Add integration tests for concurrent writes and DB transactions in payment service | short | | open |
| A3  | Configure Sentry alerts for error spikes and payment-critical errors | short | | open |
| A4  | Audit and document the 12 new E2E tests (intent, coverage, origin) | short | | open |
| A5  | Run a blameless post-mortem and share findings team-wide | short | | open |
| A6  | Establish test coverage baseline with pytest-cov | medium | | open |
| A7  | Add SELECT FOR UPDATE or equivalent locking in payment service hot paths | medium | | open |
| A8  | Add structured logging and Sentry Performance to payment service | medium | | open |
| A9  | Evaluate replacing manual deploy gate with automated smoke tests | medium | | open |
| A10 | Reduce CI run time below 10 minutes | medium | | open |
| A11 | Enable Sentry mobile crash reporting for the React Native app | long | | open |
| A12 | Introduce Conventional Commits standard across all repos | long | | open |
| A13 | Establish quarterly incident review cadence using Sentry data | long | | open |
| A14 | Embed test-writing as a required step in the PR workflow (not post-merge) | long | | open |
