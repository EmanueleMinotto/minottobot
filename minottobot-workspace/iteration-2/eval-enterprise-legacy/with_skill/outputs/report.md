# Minottobot audit report — FinanceCore Ltd — 2026-03-26

## Repos in scope
- No codebase provided (Phase 0 data only — no code reconnaissance performed)

## Executive summary (3 bullets max, each under 20 words)
- 30% flaky tests and a 47-minute Jenkins build are destroying developer trust and feedback loops.
- Biweekly releases with 6-hour manual deployments lock the team into a reactive, high-risk delivery model.
- Central QA guild of 6 serving 85 engineers creates a quality bottleneck and diffuses ownership.

## Area scores (1 = critical · 5 = excellent)
| Area                 | Score | One-line finding                                      |
|----------------------|-------|-------------------------------------------------------|
| CI/CD                |  2/5  | Jenkins from 2011, 47-minute build, no clear gate     |
| Testing              |  2/5  | 12,000 tests but 30% flaky and widely ignored         |
| Code review          |  3/5  | 3-approval policy undermined by hotfix bypass culture  |
| Monitoring           |  ?/5  | No monitoring data provided — unscored                |
| Developer Experience |  2/5  | Slow CI, flaky suite, biweekly release cadence        |
| Ownership & culture  |  2/5  | Central QA guild model externalizes quality ownership  |

## Top 3 blockers right now
1. **Flaky test suite** — 30% (~3,600 tests) are unreliable and ignored, making the entire suite untrustworthy; developers cannot get honest signal from CI.
2. **47-minute Jenkins build** — feedback is too slow to be actionable; developers are disincentivized from running tests locally or iterating quickly on CI results.
3. **Biweekly releases with 6-hour manual deployment** — low deployment frequency concentrates risk, inflates MTTR (currently ~4 hours for P1s), and makes hotfix bypassing of code review a structural habit rather than an exception.

## Improvement plan

### Short term (this sprint)
- Quarantine all known flaky tests: tag them, remove from the required CI gate, and open a dedicated flakiness backlog. This immediately restores trust in the remaining ~8,400 tests.
- Introduce parallel test execution in Jenkins to reduce build time below 15 minutes — identify the slowest test stages and split them across agents.
- Enforce the 3-approval code review policy for hotfixes via Jenkins pipeline gate, with a documented "break-glass" exception requiring post-hoc review within 24 hours; remove the informal bypass.
- Document the current Phase 0 numbers (build time, flaky count, incident rate, MTTR) as a baseline dashboard — this makes improvement measurable and visible to the team.

### Medium term (this quarter)
- Migrate CI ownership from the dedicated CI team to the product teams: each of the 8 teams owns its own pipeline configuration. The CI team shifts to a platform/enablement role.
- Embed quality ownership into each product team: rotate one engineer per team as a quality champion, working with the central QA guild rather than depending on it. The guild's role becomes coaching and tooling, not gatekeeping.
- Introduce a flakiness SLA: any test that fails non-deterministically more than a defined threshold over a rolling window is auto-quarantined. Assign ownership per team.
- Implement feature flags to decouple deployment from release, enabling more frequent, lower-risk deployments and eventually moving off the biweekly window for most changes.
- Audit the 6-hour deployment process step by step: identify the manual sign-off stages and automate anything that can be expressed as a policy check (e.g., automated smoke tests replacing manual verification steps).
- Evaluate contract testing (e.g., Pact) for Java Spring Boot microservice boundaries — given the microservices architecture, inter-service contract gaps are a likely hidden risk.

### Long term (this half)
- Move toward continuous delivery: target weekly releases as an intermediate step, progressively reducing the deployment batch size until the 6-hour manual process is replaced by an automated pipeline with automated rollback.
- Reduce MTTR from ~4 hours: instrument production observability (monitoring was not reported — this is itself a gap) with structured alerting, runbooks per service, and per-team on-call rotation rather than central escalation.
- Rebuild the test pyramid deliberately: with 12,000 tests and high flakiness, the current distribution is likely skewed toward slow integration or E2E tests. Commission a test pyramid audit per team to identify unit test gaps and eliminate duplicated coverage.
- Address the cultural drift on code review: the hotfix bypass habit is a proxy for "quality is someone else's problem." Introduce blameless post-mortems on every P1 to reframe quality as a shared engineering outcome, not a QA deliverable.
- Evaluate Jenkins modernization: a 2011-era Jenkins instance maintained by a dedicated team is institutional risk. Assess migration to GitHub Actions or GitLab CI as a longer-term investment — but only after the higher-urgency items above are stabilized.

## Action items
| ID  | Description                                                               | Horizon | Owner                      | Status |
|-----|---------------------------------------------------------------------------|---------|----------------------------|--------|
| A1  | Quarantine all flaky tests and open per-team flakiness backlog            | short   | QA Guild lead              | open   |
| A2  | Implement parallel test execution in Jenkins to cut build time            | short   | CI team                    | open   |
| A3  | Enforce code review gate for hotfixes with documented break-glass process | short   | Engineering leads          | open   |
| A4  | Document Phase 0 baseline as a shared team dashboard                     | short   | Engineering manager        | open   |
| A5  | Transfer pipeline ownership to product teams; CI team becomes platform    | medium  | CTO / Engineering manager  | open   |
| A6  | Embed quality champion per team; shift QA guild to coaching role          | medium  | QA Guild lead + team leads | open   |
| A7  | Define and automate flakiness SLA per team                                | medium  | Quality champions          | open   |
| A8  | Introduce feature flags to decouple deploy from release                   | medium  | Platform / CI team         | open   |
| A9  | Audit 6-hour deployment process and automate manual sign-off steps        | medium  | CI team + team leads       | open   |
| A10 | Evaluate contract testing (Pact) for Spring Boot microservice boundaries  | medium  | Senior engineers           | open   |
| A11 | Target weekly releases as first step toward continuous delivery           | long    | Engineering manager        | open   |
| A12 | Instrument production observability and define per-team on-call rotation  | long    | Engineering leads          | open   |
| A13 | Conduct test pyramid audit per team; identify and fix coverage gaps       | long    | Quality champions          | open   |
| A14 | Run blameless post-mortems on every P1 to build shared quality ownership  | long    | Engineering manager        | open   |
| A15 | Evaluate Jenkins replacement (GitHub Actions or GitLab CI)                | long    | CI team + CTO              | open   |
