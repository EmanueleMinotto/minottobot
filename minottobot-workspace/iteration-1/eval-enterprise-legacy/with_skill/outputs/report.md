# Minottobot audit report — FinanceCore Ltd — 2026-03-25

## Repos in scope
- FinanceCore platform (Java Spring Boot microservices + Oracle DB + React frontend)

## Executive summary
- 30% flaky test rate has destroyed pipeline trust; the team reruns instead of fixing.
- A 47-minute Jenkins build and biweekly windows are creating a dangerous release bottleneck.
- No per-team QA ownership means quality is everyone's afterthought and no one's responsibility.

## Area scores (1 = critical · 5 = excellent)

| Area                 | Score | One-line finding                                              |
|----------------------|-------|---------------------------------------------------------------|
| CI/CD                |  2/5  | 47-min build, 15-year-old Jenkins, no path to fast feedback   |
| Testing              |  1/5  | 3,600 ignored flaky tests make the suite actively misleading  |
| Code review          |  3/5  | Policy exists but hotfix bypass is a documented workaround    |
| Monitoring           |  2/5  | 2 P1s/month with 4-hour MTTR signals detection gaps           |
| Developer Experience |  2/5  | Slow CI, biweekly deploys, and manual sign-offs kill velocity |
| Ownership & culture  |  2/5  | Central QA guild of 6 cannot meaningfully serve 85 engineers  |

## Top 3 blockers right now
1. **Flaky test epidemic.** 30% of tests are untrusted. Every ignored failure is a potential P1 hiding in plain sight. This is not a coverage problem — it is a trust and discipline problem.
2. **Release cadence and deployment process.** A 6-hour manual biweekly deploy in financial services is a risk accumulator. Change batching amplifies blast radius and extends MTTR.
3. **QA ownership vacuum.** Six guild members cannot audit, coach, or gate quality for 85 engineers across 8 teams. Quality has no accountable home at the team level.

## Improvement plan

### Short term (this sprint)
- Quarantine all known flaky tests immediately — move them to a separate suite, stop counting them as green, and assign ownership for triage. Do not delete; do not ignore.
- Define and enforce a hotfix policy with a mandatory post-merge review gate. "Hotfix" cannot mean "skips review."
- Run a flaky test triage blitz: dedicate one sprint cycle per team to classifying flaky tests as fix, rewrite, or delete.
- Instrument MTTR and incident detection time explicitly — confirm whether the 4-hour MTTR is detection lag, diagnosis lag, or deployment lag.

### Medium term (this quarter)
- Embed QA ownership per product team. The guild of 6 should shift from execution to enablement: frameworks, standards, coaching, and tooling — not test-writing for other teams.
- Break the 47-minute build. Profile the pipeline and parallelise at the module and test-suite level. Target under 15 minutes for the main feedback loop without replacing Jenkins yet.
- Introduce a deployment frequency goal: move from biweekly to weekly as an intermediate step. Automate the manual sign-off gates where regulatory rules allow it, and document which gates are legally required vs. habitual.
- Establish a test health dashboard visible to all teams: flaky rate, coverage trend, build time, deploy success rate.

### Long term (this half)
- Evaluate Jenkins migration seriously — but treat it as a large, high-risk infrastructure project, not a quick fix. A 15-year-old Jenkins instance in a regulated financial environment will have undocumented dependencies and compliance artefacts attached to it. Any migration to GitHub Actions, GitLab CI, or Buildkite requires a parallel-run period, stakeholder sign-off, and an explicit rollback plan. Do not start this without dedicated resourcing.
- Introduce shift-left quality gates: automated contract testing between microservices, mutation testing pilots on the highest-risk domain modules, and DAST integration into the pipeline.
- Target continuous delivery with on-demand deployments for lower-risk services, reserving release windows for the highest-compliance components. Work with compliance and legal to define what "release window" actually protects.

## Action items

| ID  | Description                                                                 | Horizon | Owner | Status |
|-----|-----------------------------------------------------------------------------|---------|-------|--------|
| A1  | Quarantine flaky tests into a separate suite; freeze green/red accounting   | short   |       | open   |
| A2  | Assign a named owner per flaky test cluster for triage                      | short   |       | open   |
| A3  | Define and enforce a written hotfix review policy with post-merge gate      | short   |       | open   |
| A4  | Instrument incident detection lag vs. diagnosis lag vs. deploy lag          | short   |       | open   |
| A5  | Embed one QA champion per product team (from guild or upskilled dev)        | medium  |       | open   |
| A6  | Profile and parallelise Jenkins pipeline; target sub-15-min feedback loop   | medium  |       | open   |
| A7  | Move to weekly release cadence; map which manual gates are legally required | medium  |       | open   |
| A8  | Ship a live test health dashboard to all 8 teams                            | medium  |       | open   |
| A9  | Evaluate CI migration with full risk/cost/compliance assessment             | long    |       | open   |
| A10 | Pilot mutation testing on highest-risk domain modules                       | long    |       | open   |
| A11 | Define continuous delivery scope with legal and compliance teams            | long    |       | open   |
