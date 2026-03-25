<!--
  Eval: enterprise-legacy
  Team: FinanceCore Ltd
  Input prompt: see evals.json id=2
  Generated: 2026-03-25
  Re-run: load minottobot/ skill, paste the prompt from evals.json id=2, capture output here
-->

# Minottobot audit report — FinanceCore Ltd — 2026-03-25

## Repos in scope
- financecore-platform (Java Spring Boot microservices)
- financecore-web (React)

## Executive summary (3 bullets max, each under 20 words)
- A 47-minute CI build is the primary brake on developer velocity across all 8 teams.
- 30% flaky tests (~3,600) have destroyed trust in the suite; failures are routinely ignored.
- Biweekly releases with 6-hour deployment windows create high-stakes, high-risk change batches.

## Area scores (1 = critical · 5 = excellent)
| Area                | Score | One-line finding                                        |
|---------------------|-------|---------------------------------------------------------|
| CI/CD               |  2/5  | 47-min Jenkins build; biweekly deploys; no parallelism  |
| Testing             |  2/5  | 12k tests but 30% flaky; suite not trusted              |
| Code review         |  2/5  | 3-approval policy exists but bypassed by some teams     |
| Monitoring          |  3/5  | MTTR 4 hrs suggests alerts exist but response is slow   |
| Developer Experience|  2/5  | 47-min wait per push; biweekly batches raise deploy risk |
| Ownership & culture |  3/5  | Process exists; compliance is inconsistent across teams |

## Top 3 blockers right now
1. **47-minute CI run time blocks fast feedback.** Developers on all 8 teams wait nearly an hour to know if a change is safe. At this speed, the suite is bypassed under time pressure, and local shortcuts become normal. Reducing CI time is the highest-leverage improvement available right now.
2. **~3,600 flaky tests have made the suite untrustworthy.** When tests fail randomly, developers stop believing failures mean anything. A flaky suite is worse than a small trustworthy one: it provides false confidence while masking real regressions. The 30% flakiness rate is a trust crisis, not just a quality metric.
3. **Code review bypass normalises the 'hotfix' exception.** Once bypass becomes acceptable under urgency, urgency is always available as a justification. Every unreviewed change to financial processing code is an unquantified risk.

## Improvement plan
### Short term (this sprint)
- **Quarantine flaky tests** into a separate `flaky/` suite that runs in CI but does not block the build. This immediately restores trust in the main suite without deleting tests. Treat the quarantine list as a work queue, not a graveyard.
- **Enable parallel test execution in Jenkins** (via Maven Surefire or Gradle parallel test runner, depending on each service). Target: cut the 47-minute build to under 25 minutes without any test changes. This is a configuration change, not a rewrite.
- **Publish a CI bypass report** to team leads weekly. Make the bypass rate for code review visible. Teams that bypass consistently should be asked to explain it — not shamed, but accountable.

### Medium term (this quarter)
- Set a formal CI time target of under 15 minutes. Get there through test selection (run changed-module tests first), parallelism, and removing duplicate coverage.
- Establish a flaky test triage SLA: any test in the quarantine queue that hasn't been fixed within 2 sprints gets deleted. A deleted test is better than a lying test.
- Introduce incremental deployment: deploy individual services independently rather than batching everything into a biweekly window. Start with one low-risk service as proof of concept.

### Long term (this half)
- Evaluate migrating from Jenkins to a modern CI platform (GitHub Actions, GitLab CI, or Buildkite). This is a 6-12 month parallel-operation effort, not a weekend project. Factor in: existing plugin ecosystem, compliance requirements, institutional knowledge of the CI team, and migration risk. Do not start this before the short- and medium-term work is done — migrating a broken pipeline produces a broken pipeline on new infrastructure.
- Shift toward trunk-based development with short-lived feature branches to reduce the release batching that makes biweekly deploys so high-stakes.
- Build a code review compliance dashboard visible to all team leads — normalise review as a team expectation, not a bureaucratic hurdle.

## Action items
| ID | Description | Horizon | Owner | Status |
|----|-------------|---------|-------|--------|
| A1 | Quarantine flaky tests into non-blocking CI suite | short | | open |
| A2 | Enable parallel test execution in Jenkins | short | | open |
| A3 | Publish weekly CI bypass rate report to team leads | short | | open |
| A4 | Set CI time target of 15 min; track weekly | medium | | open |
| A5 | Establish 2-sprint flaky test triage SLA | medium | | open |
| A6 | Pilot independent service deployment (one low-risk service) | medium | | open |
| A7 | Evaluate CI platform migration with full cost/risk assessment | long | | open |
| A8 | Shift to trunk-based development across all teams | long | | open |

---

## Assertions

| # | Assertion | Pass? |
|---|-----------|-------|
| 1 | Output must mention CI run time of 47 minutes | PASS — Blocker #1 and executive summary both name the 47-minute build explicitly |
| 2 | Output must address flaky tests specifically | PASS — Blocker #2 quantifies the 30% (~3,600 tests) as a trust crisis; A1 and A5 address it |
| 3 | Output must give at least one short-term action item | PASS — A1, A2, A3 are all short-horizon items |
| 4 | Output must score CI/CD at 2/5 or lower | PASS — CI/CD scored 2/5 |
| 5 | Output must not recommend replacing Jenkins without acknowledging migration cost | PASS — long-term item A7 explicitly states "6-12 month parallel-operation effort" and lists migration risks; plan says "Do not start this before short- and medium-term work is done" |
