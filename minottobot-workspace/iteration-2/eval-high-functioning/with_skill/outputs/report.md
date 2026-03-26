# Minottobot audit report — Atmos / Helix team — 2026-03-26

## Repos in scope
- helix (TypeScript / Next.js / Supabase)

## Executive summary (3 bullets max, each under 20 words)
- Helix is a model engineering team: fast CI, low incidents, excellent deployment and monitoring practices.
- The main risk is invisible: test coverage, skipped tests, and API contracts are untracked.
- At 4.2 deploys/day with a single reviewer, review fatigue and bottleneck risk are worth watching.

## Area scores (1 = critical · 5 = excellent)
| Area                 | Score | One-line finding                              |
|----------------------|-------|-----------------------------------------------|
| CI/CD                |  5/5  | GitHub Actions, 8 min, required, no bypass — exemplary |
| Testing              |  4/5  | Well-shaped pyramid; coverage % and skipped count unknown |
| Code review          |  4/5  | 1 approval, substantive discussion; no mention of review SLA |
| Monitoring           |  5/5  | Datadog with custom SLOs, on-call rotation, runbooks |
| Developer Experience |  4/5  | Feature flags, auto-rollback, modern stack; onboarding not documented |
| Ownership & culture  |  5/5  | Quality is everyone's job; runbooks and on-call rotation confirm it |

## Top 3 blockers right now
1. **Unknown test health metrics** — coverage % and skipped test count are not tracked; silent risk in an otherwise strong setup.
2. **No API contract standards** — TypeScript + Next.js + Supabase warrants OpenAPI or Supabase-typed contracts for cross-service clarity; none mentioned.
3. **Single approval at 4.2 deploys/day** — single reviewer may create bottleneck or fatigue; no post-deploy smoke tests to complement auto-rollback.

## Improvement plan

### Short term (this sprint)
- Add coverage reporting to GitHub Actions CI: configure `c8` or `istanbul` to output coverage summary on every PR. Fail the build if coverage drops below current baseline (don't set a target yet — just track).
- Expose skipped/pending test count in CI output. A rising skipped count is a canary for test rot.
- Adopt Conventional Commits across the team. At 4.2 deploys/day the git log is dense — structured commit messages make automated changelogs and release notes viable.

### Medium term (this quarter)
- Add post-deploy smoke tests: a small Playwright or k6 suite that runs against production immediately after each deploy, covering the 3-5 most critical user flows. Auto-rollback reacts to error spikes — smoke tests catch silent functional regressions before users do.
- Document the onboarding experience for new engineers: local setup, feature flag conventions, how to add a Datadog SLO. This is cheap now and expensive to reconstruct after the team grows.
- Define API contracts: generate OpenAPI specs from Next.js route handlers (using `zod-openapi` or `next-swagger-doc`) and validate Supabase schema types in CI. Contract drift is the silent failure mode of fast-moving teams.

### Long term (this half)
- Evaluate a second approval requirement for high-risk paths (payment flows, auth, data migrations). A single reviewer at 4.2 deploys/day is a cognitive load problem at scale. Consider a lightweight "high-risk PR" label that auto-assigns a second reviewer.
- Invest in mutation testing (Stryker): at 2,100 unit tests, the question shifts from "do tests exist?" to "do tests actually catch regressions?" Mutation testing answers this and surfaces tests that always pass regardless of code changes.
- Build a chaos/resilience practice: with Datadog SLOs and runbooks already in place, the next level is proactive failure injection (game days, simulated service degradation) to validate runbooks before incidents happen.

## Action items
| ID | Description | Horizon | Owner | Status |
|----|-------------|---------|-------|--------|
| A1 | Add coverage reporting (c8/istanbul) to GitHub Actions CI | short | | open |
| A2 | Expose skipped test count in CI summary | short | | open |
| A3 | Adopt Conventional Commits convention across the team | short | | open |
| A4 | Add post-deploy smoke tests (Playwright or k6) for top 3-5 critical flows | medium | | open |
| A5 | Document engineer onboarding: local setup, feature flags, Datadog SLO process | medium | | open |
| A6 | Define API contracts via OpenAPI or Supabase typed schema; validate in CI | medium | | open |
| A7 | Evaluate second-approval requirement for high-risk PR paths | long | | open |
| A8 | Introduce mutation testing (Stryker) to validate test suite effectiveness | long | | open |
| A9 | Run chaos/game-day exercises to validate runbooks before incidents | long | | open |
