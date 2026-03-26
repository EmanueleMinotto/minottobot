# Minottobot audit report — Helix (Atmos) — 2026-03-25

## Repos in scope
- helix (TypeScript + Next.js + Supabase)

## Executive summary
- Delivery metrics are elite: 4.2 deploys/day, 12-minute MTTR, and 0.1 P1/month are genuinely rare.
- Test suite shape and single-approval review policy carry meaningful risk at this deployment frequency.
- No dedicated QA and no contract/API boundary testing leave compounding gaps as the product scales.

## Area scores (1 = critical · 5 = excellent)
| Area                 | Score | One-line finding                                               |
|----------------------|-------|----------------------------------------------------------------|
| CI/CD                |  5/5  | 8-min pipeline, required gates, automatic rollback — exemplary |
| Testing              |  3/5  | Strong unit count but E2E ratio thin; no contract testing visible |
| Code review          |  3/5  | 1 approval is below par for a 7-person team shipping 4.2×/day  |
| Monitoring           |  5/5  | Custom SLOs, on-call rotation, runbooks — nothing missing here  |
| Developer Experience |  4/5  | Feature flags + fast CI = excellent; local env setup unknown   |
| Ownership & culture  |  4/5  | "Quality is everyone's job" works now; fragile without structure as team grows |

## Top 3 blockers right now
1. Single-approval code review creates a blind-spot risk: one engineer can merge their own work after one peer sign-off, with no second set of eyes on high-blast-radius changes.
2. E2E coverage is thin relative to deployment velocity — 85 tests across a Next.js + Supabase surface means critical user journeys may be exercised only in production.
3. No contract or API boundary testing means Supabase schema changes and any internal service boundaries are validated only through integration tests that may not cover consumer expectations.

## Improvement plan

### Short term (this sprint)
- Raise the PR approval requirement to 2 reviewers for changes touching auth, billing, and data-layer files; keep 1 approval for low-risk surface areas (docs, config, non-critical UI). Use CODEOWNERS to enforce automatically.
- Audit the 85 E2E tests against the product's critical user journeys (sign-up, core B2B workflow, billing). Identify gaps and assign ownership to close the top 3 missing paths this sprint.
- Add a lightweight PR template that prompts authors to declare blast radius, flag DB migrations, and confirm feature-flag coverage — takes under an hour to ship and immediately improves review quality.

### Medium term (this quarter)
- Introduce contract testing (Pact or equivalent) for Supabase RLS policies and any internal API boundaries. At 4.2 deploys/day, a schema drift incident is a when, not an if.
- Establish a formal test ownership model. Without a dedicated QA, every engineer owns quality for their area, but someone needs to own the overall test health dashboard (coverage trends, flake rate, E2E run time). Assign a rotating "QA champion" role per quarter.
- Instrument test flakiness explicitly in CI. Flaky tests are the silent killer of deployment confidence at high frequency — surface them in Datadog alongside your SLOs.

### Long term (this half)
- Define a Quality Engineering charter before the team grows past 10. "Quality is everyone's job" is a strong cultural value but historically degrades under headcount pressure at Series B. A one-page charter codifying standards, test ownership, and escalation paths preserves the culture without requiring a dedicated QA headcount.
- Evaluate synthetic monitoring on critical user journeys in production (e.g., Datadog Synthetics or Playwright cloud). Given the 12-minute MTTR, closing the detection-to-alert gap on user-facing flows end-to-end is the next logical frontier for an already mature monitoring setup.
- Formalize a feature flag lifecycle and retirement process. At 4.2 deploys/day behind flags, flag debt accumulates fast. Stale flags that are never cleaned up become hidden branching logic that degrades testability and cognitive load over 12–18 months.

## Action items
| ID | Description | Horizon | Owner | Status |
|----|-------------|---------|-------|--------|
| A1 | Add CODEOWNERS with 2-approval rule for auth, billing, data-layer paths | short | Eng lead | open |
| A2 | Audit E2E suite against critical user journeys; close top 3 gaps | short | Team rotation | open |
| A3 | Add PR template with blast-radius, migration flag, and feature-flag fields | short | Any engineer | open |
| A4 | Spike and implement contract testing for Supabase schema and API boundaries | medium | Senior engineer | open |
| A5 | Assign rotating QA champion role; own test health dashboard | medium | Eng lead | open |
| A6 | Instrument and surface flaky tests as a Datadog metric | medium | Any engineer | open |
| A7 | Write and ratify a one-page Quality Engineering charter | long | Eng lead + team | open |
| A8 | Evaluate and pilot synthetic monitoring on top 3 user journeys | long | Senior engineer | open |
| A9 | Define feature flag lifecycle policy and implement automated staleness alerts | long | Eng lead | open |
