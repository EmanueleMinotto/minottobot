# Minottobot audit report — Helix team @ Atmos — 2026-03-27

## Repos in scope
- Helix (TypeScript + Next.js + Supabase)

> ⚠️ **No code access** — this audit is based on team-reported data only. Findings could not be verified against the codebase.

## Executive summary (3 bullets max, each under 20 words)
- CI, deployment, monitoring, and incident response are all operating at an excellent level.
- Test pyramid is healthy but integration layer is thin relative to unit coverage.
- No critical blockers; focus shifts to hardening standards and flag lifecycle discipline.

## Area scores (1 = critical · 5 = excellent)
| Area                    | Score | One-line finding                                      |
|-------------------------|-------|-------------------------------------------------------|
| 🟢 CI/CD                |  5/5  | Fast, enforced, no bypass, automatic rollback in place |
| 🟢 Testing              |  4/5  | Strong pyramid, integration layer slightly underweight |
| 🟢 Code review          |  4/5  | Substantive reviews; single approval may not scale     |
| 🟢 Monitoring           |  5/5  | Datadog SLOs, on-call, runbooks, 12-min MTTR           |
| 🟢 Developer Experience |  5/5  | Feature flags, 4+ deploys/day, fast CI feedback loop   |
| 🟢 Ownership & culture  |  4/5  | Quality-as-everyone's-job; no explicit standards noted |

> 🔴 1–2 critical/gap · 🟡 3 functional · 🟢 4–5 good/excellent

## Top 3 blockers right now
1. ⚠️ **Integration test coverage** — 380 integration tests vs 2,100 unit tests may leave service boundaries undertested.
2. ⚠️ **Single approval on PRs** — at 7 engineers and 4+ deploys/day, one reviewer may miss context on critical paths.
3. ⚠️ **No mention of technical standards** — Conventional Commits, OpenAPI, and TypeScript strict mode not confirmed in use.

## Improvement plan
### ⚡ Short term (this sprint)
- Audit integration test coverage against service boundaries in the Supabase + Next.js stack; identify gaps on critical data paths.
- Confirm TypeScript strict mode is enabled; enable it if not, starting with `warn`-level additions via the DFER loop.
- Define a feature flag lifecycle policy: owner, removal condition, and monthly review cadence.

### ◆ Medium term (this quarter)
- Adopt Conventional Commits and enforce them in CI (e.g., commitlint); this unlocks automated changelog generation.
- Introduce a second required reviewer on PRs touching auth, billing, or data persistence paths.
- Document OpenAPI specs for any external-facing APIs; validate them against implementation in CI.

### ◎ Long term (this half)
- Grow integration test count toward a 1:4 ratio with unit tests (target ~525); prioritise Supabase RLS and API boundary tests.
- Evaluate gradual rollout (5% → 20% → 100%) for high-risk features; requires confirming flag state sync across environments.
- Run a structured DX survey with the team to surface hidden friction before the team grows beyond Series B hiring.

## Action items
| ID | Description | Horizon | Owner | Status |
|----|-------------|---------|-------|--------|
| A1 | Audit integration test gaps against service boundaries | ⚡ short | | ○ open |
| A2 | Verify and enable TypeScript strict mode via DFER | ⚡ short | | ○ open |
| A3 | Define feature flag lifecycle policy with owner + removal condition | ⚡ short | | ○ open |
| A4 | Adopt Conventional Commits + enforce via commitlint in CI | ◆ medium | | ○ open |
| A5 | Require second reviewer on auth/billing/data PRs | ◆ medium | | ○ open |
| A6 | Add OpenAPI specs for external APIs and validate in CI | ◆ medium | | ○ open |
| A7 | Grow integration test count to ~525 (target 1:4 ratio with unit) | ◎ long | | ○ open |
| A8 | Implement gradual rollout with observability gates for high-risk features | ◎ long | | ○ open |
| A9 | Run team DX survey ahead of post-Series-B hiring growth | ◎ long | | ○ open |
