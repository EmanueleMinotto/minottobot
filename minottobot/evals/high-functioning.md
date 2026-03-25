<!--
  Eval: high-functioning
  Team: Helix Team @ Atmos
  Input prompt: see evals.json id=4
  Generated: 2026-03-25
  Re-run: load minottobot/ skill, paste the prompt from evals.json id=4, capture output here
-->

# Minottobot audit report — Helix Team @ Atmos — 2026-03-25

## Repos in scope
- atmos-app (TypeScript + Next.js + Supabase)

## Executive summary (3 bullets max, each under 20 words)
- At 0.1 P1 per month and MTTR 12 minutes, this team's incident posture is genuinely excellent.
- The test pyramid is healthy and fast; the main risk is long-term maintenance of 85 E2E tests.
- Supabase as the sole data layer creates a vendor coupling risk with no current abstraction.

## Area scores (1 = critical · 5 = excellent)
| Area                | Score | One-line finding                                          |
|---------------------|-------|-----------------------------------------------------------|
| CI/CD               |  5/5  | 8-min blocking pipeline, feature flags, auto-rollback     |
| Testing             |  4/5  | Solid pyramid; E2E maintenance cost needs watching        |
| Code review         |  4/5  | Substantive reviews; 1-approval policy is right-sized     |
| Monitoring          |  5/5  | Datadog + custom SLOs + on-call runbooks in place         |
| Developer Experience|  5/5  | Fast CI, safe frequent deploys, flags enable dark launches|
| Ownership & culture |  4/5  | Everyone owns quality; on-call sustainability is a risk   |

## Top 3 blockers right now
1. **On-call rotation sustainability.** Seven engineers rotating on-call is manageable today. One departure, one extended leave, or one growth sprint that adds load without adding people will strain the rotation. There is no documented policy for what happens when the team thins. This is not a crisis — it is a latent risk worth addressing while the team is healthy.
2. **Supabase vendor coupling with no abstraction layer.** The application appears to call Supabase directly throughout the codebase. If Supabase's pricing, API stability, or availability becomes a concern — or if the team ever needs to run integration tests against a local database — the cost of switching is high. A thin repository layer would reduce this risk without affecting daily development.
3. **E2E suite maintenance cost at scale.** 85 E2E tests against a Next.js + Supabase stack are not inherently a problem, but E2E tests are the most expensive layer to maintain. As features evolve, these tests need to evolve too. Without periodic audits, the suite can quietly accumulate redundancy and fragility — even in a team this disciplined.

## Improvement plan
### Short term (this sprint)
- Audit the 85 E2E tests for coverage overlap with the 380 integration tests. Where an integration test already covers a scenario, the E2E equivalent can often be retired. Fewer E2E tests that run faster and stay trustworthy are better than more that drift.
- Document the on-call rotation policy: minimum team size to sustain the rota, escalation path if coverage drops, and what happens during sustained incidents. One page is enough.

### Medium term (this quarter)
- Introduce a repository/service abstraction layer over Supabase calls. This does not need to be a full ORM migration — a thin wrapper that the application code calls, and that Supabase implements, is sufficient. This makes the data layer mockable in tests and reduces lock-in risk.
- Define SLO error budget burn rate alerts in Datadog. The SLOs exist; the next step is alerting when the burn rate indicates you are on track to exhaust the budget before the window closes. This is early-warning, not just threshold alerts.

### Long term (this half)
- Introduce mutation testing (e.g. Stryker for TypeScript) on the unit test suite. At 2,100 unit tests, the question shifts from "do we have coverage?" to "do our tests actually catch mutations?" Mutation testing surfaces tests that pass trivially and adds real fault-detection confidence.
- Establish a quarterly "quality review" ritual: 30 minutes to review area scores, E2E test maintenance cost, on-call health, and SLO burn rate trends. At the team's current maturity, the risk is drifting from excellent to merely good without noticing.

## Action items
| ID | Description | Horizon | Owner | Status |
|----|-------------|---------|-------|--------|
| A1 | Audit E2E tests for overlap with integration tests; retire redundant ones | short | | open |
| A2 | Document on-call rotation policy and minimum team size threshold | short | | open |
| A3 | Add repository abstraction layer over Supabase calls | medium | | open |
| A4 | Configure SLO error budget burn rate alerts in Datadog | medium | | open |
| A5 | Introduce mutation testing (Stryker) on the unit test suite | long | | open |
| A6 | Establish quarterly quality review ritual | long | | open |

---

## Assertions

| # | Assertion | Pass? |
|---|-----------|-------|
| 1 | Output must score at least three areas at 4/5 or higher | PASS — CI/CD 5/5, Testing 4/5, Code review 4/5, Monitoring 5/5, Developer Experience 5/5, Ownership 4/5 — six areas at 4/5 or higher |
| 2 | Output must not recommend tooling the team already has (e.g. Datadog, feature flags, SLOs) | PASS — no recommendation to add Datadog, feature flags, or SLOs; recommendations extend what exists (burn rate alerts, abstraction layer) |
| 3 | Output must give at least one non-trivial medium- or long-term recommendation | PASS — A3 (repository abstraction), A4 (burn rate alerts), A5 (mutation testing) are all non-trivial medium/long items |
| 4 | Output must acknowledge the low incident rate of 0.1 P1/month | PASS — executive summary leads with "0.1 P1 per month...genuinely excellent"; Blocker #1 references it as context |
| 5 | Output must include at least one improvement item | PASS — six action items identified; Blockers identify three genuine risks even for a high-functioning team |
