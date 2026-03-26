# Minottobot audit report — Momentum Fintech, Platform Team — 2026-03-26

## Repos in scope
- Platform (PHP + Laravel, Node.js microservices, MySQL) — no direct code inspection performed

## Executive summary
- CI is split across CircleCI and GitHub Actions with no authoritative deployment owner.
- Test suite of ~800 tests has not run in 2 months; trustworthiness is unknown.
- Leadership instability (3 VPs in 18 months) and a 6-month unresolved outage signal deep ownership failure.

## Area scores (1 = critical · 5 = excellent)
| Area                 | Score | One-line finding                                     |
|----------------------|-------|------------------------------------------------------|
| CI/CD                |  1/5  | Two competing CI systems; no clear deployment owner  |
| Testing              |  1/5  | ~800 tests unrun for 2 months; trust unknown         |
| Code review          |  2/5  | Officially required but routinely skipped for urgency|
| Monitoring           |  1/5  | No formal incident tracking; major outage unresolved |
| Developer Experience |  1/5  | Irregular deploys, unclear tooling, fractured team   |
| Ownership & culture  |  1/5  | No product owner, revolving VP, 4 engineers on loan  |

## Top 3 blockers right now
1. **Dual CI ambiguity (CircleCI vs GitHub Actions):** no authoritative deployment pipeline means nobody owns the release gate. This must be resolved before any other quality work can land.
2. **Test suite in unknown state:** ~800 tests unrun for 2 months in a fintech context is an active liability. The suite may be registering false green or silent failure; until it's verified, it provides zero protection.
3. **Unresolved major outage + zero incident tracking:** a 6-month-old unresolved outage with no formal tracking is a systemic risk. Without a postmortem process, the same failure mode will repeat.

## Improvement plan

### Short term (this sprint)
- Declare one authoritative CI/CD pipeline: pick either CircleCI or GitHub Actions (GitHub Actions recommended — better community adoption, active ecosystem, reduces vendor sprawl). Disable or archive the other immediately.
- Run the full test suite and triage results: categorize into passing, failing, and flaky. Do not delete anything yet — the failure map is itself diagnostic evidence.
- Open a formal incident ticket for the 6-month-old outage and assign a named owner.
- Enforce branch protection on the main branch: block merges unless the chosen CI pipeline is green, no exceptions for "urgent" work.

### Medium term (this quarter)
- Establish a lightweight incident tracking process (a shared document or GitHub Issues is enough to start). Define what counts as an incident and require a one-paragraph postmortem for anything affecting production.
- Reduce the test suite to a trusted core: failing tests that cannot be fixed in one sprint should be isolated and tagged `@needs-fix`, not silently ignored.
- Assign a temporary product owner or designate a rotating tech lead to fill the ownership vacuum.
- Establish a code review agreement: define what "urgent" means and what the minimum review bar is even in urgent cases.
- Audit the PHP + Laravel and Node.js microservices split: identify services with no tests and prioritize integration tests for the highest-risk paths (payments, auth, data mutations).

### Long term (this half)
- Stabilize team composition: the 4 engineers on loan should be formally returned or the team's scope re-adjusted to match effective headcount of 7.
- Introduce a blameless postmortem culture with action items tracked to completion.
- Define deployment standards: target at minimum weekly deploys with a clear rollback procedure.
- Address leadership churn resilience: document processes, agreements, and decisions so context survives VP transitions.
- Once the test suite is stable, introduce coverage tracking with a pragmatic threshold (60% to start, rising to 75% within two quarters).

## Action items
| ID | Description | Horizon | Owner | Status |
|----|-------------|---------|-------|--------|
| A1 | Designate GitHub Actions as authoritative CI/CD; disable CircleCI pipeline | short | Platform lead | open |
| A2 | Run full test suite and produce a triage report (passing / failing / flaky) | short | Any engineer | open |
| A3 | Open a formal ticket for the 6-month-old outage and assign a named owner | short | Platform lead | open |
| A4 | Enable branch protection on main: CI must pass before merge, no bypass | short | Platform lead | open |
| A5 | Create a minimal incident tracking process (template + channel) | medium | Platform lead | open |
| A6 | Tag untriageable failing tests `@needs-fix`; establish a green-suite baseline | medium | QA / any engineer | open |
| A7 | Assign a temporary product owner or rotating tech lead | medium | VP of Engineering | open |
| A8 | Define and document the code review agreement including "urgent" exception rules | medium | Platform lead | open |
| A9 | Map PHP + Laravel and Node.js services against test coverage; prioritize critical paths | medium | Senior engineers | open |
| A10 | Resolve on-loan headcount: return engineers or re-scope team charter | long | VP of Engineering | open |
| A11 | Introduce blameless postmortem process with action item tracking | long | Platform lead | open |
| A12 | Define deployment cadence target and rollback procedure | long | Platform lead | open |
| A13 | Document team processes, agreements, and decisions to survive VP transitions | long | Platform team | open |
| A14 | Introduce coverage tracking with a pragmatic threshold (60% to start) | long | Platform lead | open |
