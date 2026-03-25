<!--
  Eval: org-chaos
  Team: Momentum Fintech — Platform team
  Input prompt: see evals.json id=5
  Generated: 2026-03-25
  Re-run: load minottobot/ skill, paste the prompt from evals.json id=5, capture output here
-->

# Minottobot audit report — Momentum Fintech Platform — 2026-03-25

## Repos in scope
- momentum-core (PHP + Laravel)
- momentum-services (Node.js microservices)

## Executive summary (3 bullets max, each under 20 words)
- No clear owner for the platform means decisions stall, incidents accumulate, and engineers get borrowed away.
- Dual CI systems (CircleCI and GitHub Actions) mean no one knows which pipeline is authoritative for production.
- A major outage six months ago is still partially unresolved — the team cannot safely deploy or audit its own state.

## Area scores (1 = critical · 5 = excellent)
| Area                | Score | One-line finding                                          |
|---------------------|-------|-----------------------------------------------------------|
| CI/CD               |  2/5  | Two CI systems, unclear canonical; last deploy 3 weeks ago|
| Testing             |  2/5  | ~800 tests not run in 2 months; trustworthiness unknown   |
| Code review         |  2/5  | Policy exists but skipped under urgency, which is constant|
| Monitoring          |  1/5  | Incidents not tracked; 6-month outage partially unresolved|
| Developer Experience|  1/5  | Unclear tooling, borrowed engineers, no deploy cadence    |
| Ownership & culture |  1/5  | No product owner, 3 VPs in 18 months, 4 engineers on loan |

## Top 3 blockers right now
1. **No one owns the platform.** Three VPs in 18 months means engineering direction has reset repeatedly. Four engineers on loan to other departments means the effective team is seven people, not eleven — and none of them have a product owner to escalate decisions to. Without a named owner, every hard call (which CI system is canonical? who resolves the 6-month outage?) goes unanswered. This is the root cause of everything else on this list.
2. **Two CI systems with no authoritative source of truth for deployments.** CircleCI and GitHub Actions are both running. Nobody knows which one controls what reaches production. This means the team cannot confidently reason about what is deployed, cannot roll back reliably, and cannot trust any CI pass as meaningful. Operating with two CI systems is not double safety — it is ambiguity that makes every deploy a gamble.
3. **Production is effectively unmonitored and the 6-month outage is ongoing.** Incidents are not tracked, which means there is no data on frequency or impact. The major outage six months ago is still partially unresolved, which means production may be in a degraded state right now. Without monitoring, the team cannot tell.

## Improvement plan
### Short term (this sprint)
- **Pick one CI system and disable the other — this week.** Designate a named person ("CI owner" for the next 30 days, whoever has the most context) to make the call: CircleCI or GitHub Actions. Document the decision in the repo. The wrong choice, made and documented, is better than two correct choices that no one trusts. Disable the non-canonical system to prevent it from running silently.
- **Run the test suite and record the result as the official baseline.** ~800 tests have not run in 2 months. Run them now. Document how many pass, how many fail, and how many error. This is the current state of the codebase. It is not good news, but it is real data, which is what decisions need to be made from.
- **Add uptime monitoring for the two most critical production endpoints.** UptimeRobot (free) or a simple health-check endpoint pinged by the CI system takes 20 minutes to set up. It does not resolve the 6-month outage, but it means the team will know when things go completely dark, rather than learning from users.

### Medium term (this quarter)
- Map service ownership: for every microservice in `momentum-services` and every module in `momentum-core`, assign a named owner and publish it in the repository root (an `OWNERS.md`). If no one is willing to claim ownership of a service, that service should be flagged for deprecation.
- Establish a minimum deploy cadence. Three weeks between deploys means changes accumulate, deploy risk compounds, and the team loses confidence in the process. Even deploying a no-op change weekly builds the muscle and keeps the pipeline trusted.
- Begin resolving the 6-month outage with a time-boxed investigation: two engineers, two days, produce a written summary of what is still broken and what it would take to fully resolve it. If it cannot be fixed, it should be decommissioned.

### Long term (this half)
- Consolidate the PHP + Laravel and Node.js dual-stack into a single target architecture. This is a multi-quarter effort; it should begin with a written decision (ADR format) about which stack is the future, and a named engineer to own the migration plan.
- Establish a lightweight incident tracking process. A shared spreadsheet with date, description, resolution, and time-to-resolve is sufficient to start. The goal is to go from "we don't count incidents" to "we know our incident rate and MTTR." That data is what any future VP of Engineering will need on day one.
- Build a code review enforcement step in whichever CI system is chosen: PRs without review cannot be merged. This removes the "urgent" bypass by making bypass technically unavailable.

## Action items
| ID | Description | Horizon | Owner | Status |
|----|-------------|---------|-------|--------|
| A1 | Designate CI owner; pick CircleCI or GitHub Actions; disable the other | short | | open |
| A2 | Run test suite; document pass/fail/error counts as official baseline | short | | open |
| A3 | Add uptime monitoring for 2 critical production endpoints | short | | open |
| A4 | Publish OWNERS.md mapping every service/module to a named owner | medium | | open |
| A5 | Establish minimum weekly deploy cadence | medium | | open |
| A6 | Time-boxed investigation of the 6-month outage (2 engineers, 2 days) | medium | | open |
| A7 | Write ADR for PHP vs Node.js consolidation; assign migration owner | long | | open |
| A8 | Implement incident tracking (spreadsheet minimum) | long | | open |
| A9 | Add CI-enforced code review gate on both repositories | long | | open |

---

## Assertions

| # | Assertion | Pass? |
|---|-----------|-------|
| 1 | Output must address ownership ambiguity explicitly | PASS — Blocker #1 names "no one owns the platform" as the root cause; executive summary leads with it |
| 2 | Output must mention both CI systems by name (CircleCI and GitHub Actions) | PASS — Blocker #2 names both CircleCI and GitHub Actions explicitly; A1 references both |
| 3 | Output must give at least one short-term action item that is actionable despite the chaos | PASS — A1 (pick a CI system), A2 (run tests), A3 (add uptime monitoring) are all executable by any single engineer without organisational approval |
| 4 | Output must score Ownership & culture at 2/5 or lower | PASS — Ownership & culture scored 1/5 |
| 5 | Output must not recommend a full team reorganisation | PASS — no recommendation to restructure the team or reporting lines; recommendations focus on tooling, ownership documentation, and process within the team's control |
