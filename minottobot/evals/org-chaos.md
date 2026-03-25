<!--
  Eval: org-chaos
  Team: Momentum Fintech — Platform team
  Input prompt: see evals.json id=5
  Generated: 2026-03-25
  Re-run: 2026-03-25 (iteration-1, subagent run)
-->

# Minottobot audit report — Momentum Fintech Platform Team — 2026-03-25

## Repos in scope
- Platform monolith + Node.js microservices (PHP/Laravel, Node.js, MySQL)

## Executive summary
- Dual CI systems with no authoritative owner create deployment ambiguity and silent failure risk.
- 800 tests untouched for 2 months and an unresolved major outage signal compounding technical debt.
- Leadership instability (3 VPs in 18 months, no product owner) has eroded accountability across the board.

## Area scores (1 = critical · 5 = excellent)
| Area                 | Score | One-line finding                                              |
|----------------------|-------|---------------------------------------------------------------|
| CI/CD                |  2/5  | Two competing CI systems; authoritative deployment path unknown |
| Testing              |  2/5  | 800 tests, unknown pass rate, not run in 2 months             |
| Code review          |  2/5  | Process exists but is routinely bypassed under "urgent" label |
| Monitoring           |  1/5  | No incident tracking; a major outage remains unresolved at 6 months |
| Developer Experience |  2/5  | Irregular deploys, unclear toolchain ownership, reduced active headcount |
| Ownership & culture  |  2/5  | No product owner, 3 VPs in 18 months, diffuse accountability at every layer |

## Top 3 blockers right now
1. Unknown CI authority — neither CircleCI nor GitHub Actions is confirmed as the deployment source of truth, meaning any deploy carries unverified pipeline risk.
2. Unresolved major outage — an incident open for 6 months with no formal tracking is an active liability, not a historical event.
3. Test suite in unknown state — 800 tests that have not been executed in 2 months cannot be used to gate anything; the safety net is theoretical.

## Improvement plan

### Short term (this sprint)
- Run the full test suite today. Record baseline pass/fail count. Do not fix failures yet — just establish the ground truth number.
- Declare one CI system as authoritative between CircleCI and GitHub Actions. Hold a 30-minute decision meeting with whoever owns infra access. Freeze the losing system's deploy jobs immediately (do not delete — just disable triggers). Document the decision in the repo wiki.
- Add a mandatory "outage log" entry to the shared incident doc for the 6-month outage: date, current status, next action, owner name. One line is enough — the goal is to stop it being invisible.
- Stop treating "urgent" as a code review bypass. Instead, introduce a 1-reviewer fast-track rule: urgent PRs still need one approval, but can merge in under 30 minutes. This keeps the gate without the bottleneck excuse.

### Medium term (this quarter)
- Triage the failing tests and sort into three buckets: fixable now, fixable with refactor, delete (obsolete). Restore the suite to a passing baseline and add it as a required CI check on the authoritative pipeline.
- Implement a lightweight incident register (a shared spreadsheet or Linear label is sufficient). Require a post-incident summary for any outage longer than 1 hour. Retroactively file one entry for the 6-month outage.
- Add branch protection rules on the main branch in GitHub: require at least 1 approved review and a passing CI check before merge. This mechanically enforces the code review policy where culture has failed to.
- Define and document the deployment runbook: who triggers a deploy, from which pipeline, which environment gates are required. Pin it to the repo README.

### Long term (this half)
- Converge to a single CI/CD platform. Evaluate whether CircleCI or GitHub Actions better fits the mixed PHP/Laravel + Node.js stack and migrate all jobs from the retired system. Decommission its configuration files entirely.
- Establish environment parity: local → staging → production with promotion gates at each boundary. Irregular deploys are partly a symptom of no clear staging confidence check.
- Introduce ownership mapping: every service and pipeline job must have a named team member as the designated owner. Review this mapping each quarter. This is the structural fix for the "not my problem" pattern made worse by repeated leadership churn.
- Negotiate a dedicated product owner assignment with leadership. Document the business and risk case: a fintech platform with no product owner has no one accountable for scope, priority, or incident severity decisions.

## Action items
| ID | Description | Horizon | Owner | Status |
|----|-------------|---------|-------|--------|
| A1 | Run full test suite; record baseline pass/fail count | short | | open |
| A2 | Decide between CircleCI and GitHub Actions as authoritative CI; disable deploy triggers on the other | short | | open |
| A3 | Add a named owner and current status entry to the 6-month outage doc | short | | open |
| A4 | Enforce 1-reviewer fast-track rule; remove "urgent" bypass exception | short | | open |
| A5 | Triage test failures into fix / refactor / delete buckets | medium | | open |
| A6 | Add passing CI check + 1 approval as required branch protection rules | medium | | open |
| A7 | Stand up lightweight incident register; file retroactive outage entry | medium | | open |
| A8 | Write and publish deployment runbook in repo README | medium | | open |
| A9 | Converge to single CI/CD platform (CircleCI or GitHub Actions); migrate all jobs, retire the other | long | | open |
| A10 | Define and enforce environment promotion gates (local → staging → prod) | long | | open |
| A11 | Create and publish service ownership map; assign named owners per job | long | | open |
| A12 | Build business case for dedicated product owner; present to leadership | long | | open |

---

## Assertions

| # | Assertion | Pass? |
|---|-----------|-------|
| 1 | Output must address ownership ambiguity explicitly | PASS — Executive summary: "Leadership instability (3 VPs in 18 months, no product owner) has eroded accountability across the board." Ownership & culture 2/5. A11 introduces ownership mapping. |
| 2 | Output must mention both CI systems by name (CircleCI and GitHub Actions) | PASS — Blocker #1: "neither CircleCI nor GitHub Actions is confirmed as the deployment source of truth." Short term: "Declare one CI system as authoritative between CircleCI and GitHub Actions." A2: "Decide between CircleCI and GitHub Actions as authoritative CI." A9: "Converge to single CI/CD platform (CircleCI or GitHub Actions)." |
| 3 | Output must give at least one short-term action item that is actionable despite the chaos | PASS — A1: "Run full test suite; record baseline pass/fail count" and A2: "Declare authoritative CI system" require no external approval or resources. |
| 4 | Output must score Ownership & culture at 2/5 or lower | PASS — Ownership & culture scored 2/5: "No product owner, 3 VPs in 18 months, diffuse accountability at every layer." |
| 5 | Output must not recommend a full team reorganisation | PASS — No team reorganisation recommended; A12 is a business case for a product owner, not an org redesign. |
