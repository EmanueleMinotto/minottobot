# Minottobot audit report — Helix (Atmos) — 2026-03-26

## Repos in scope
- Helix (TypeScript · Next.js · Supabase)

> ⚠️ **No code access** — this audit is based on team-reported data only. Findings could not be verified against the codebase.

## Executive summary (3 bullets max, each under 20 words)
- Helix is a high-functioning team with strong CI, monitoring, and deployment practices.
- Three Phase 0 gaps — coverage %, skipped tests, CI success rate — remain unmeasured.
- No structural blockers; focus is on measurement discipline to sustain current excellence.

## Area scores (1 = critical · 5 = excellent)
| Area                    | Score | One-line finding                                         |
|-------------------------|-------|----------------------------------------------------------|
| 🟢 CI/CD                |  5/5  | GitHub Actions, 8 min, no bypass, auto rollback          |
| 🟢 Testing              |  4/5  | Healthy pyramid; coverage % and skipped count unknown    |
| 🟢 Code review          |  4/5  | 1 approval, substantive discussion consistently          |
| 🟢 Monitoring           |  5/5  | Datadog, custom SLOs, on-call rotation, runbooks         |
| 🟢 Developer Experience |  5/5  | Feature flags, fast CI, TypeScript strict, modern stack  |
| 🟢 Ownership & culture  |  4/5  | No dedicated QA; quality owned collectively by engineers |

> 🔴 1–2 critical/gap · 🟡 3 functional · 🟢 4–5 good/excellent

## Phase 0 gaps (numbers the team could not answer)

The following Phase 0 questions were not answered. Each unanswered number is a finding.

| # | Question | Status |
|---|----------|--------|
| 5 | Last month's CI success rate % | ❓ not provided |
| 7 | Test coverage % | ❓ not provided |
| 8 | How many tests are currently skipped or disabled? | ❓ not provided |
| 10 | Open bugs older than 30 days | ❓ not provided |

These are not necessarily problems — they may be fine on closer inspection. But the fact that they are unknown is itself a signal: a high-functioning team should be able to answer these in 60 seconds.

## Top 3 blockers right now
1. ⚠️ **CI success rate unknown** — flakiness could be eroding pipeline trust invisibly without a tracked baseline.
2. ⚠️ **Coverage % not surfaced** — no automated guard on untested surface area; growth may be adding blind spots.
3. ⚠️ **Skipped/disabled test count unknown** — disabled tests accumulate silently and create false confidence in suite completeness.

## Improvement plan

### ⚡ Short term (this sprint)
- Run a one-time audit of currently skipped/disabled tests across the suite; triage each as fix, delete, or track-as-debt.
- Query GitHub Actions run history (last 30 days) and calculate CI success rate; establish this as a tracked metric.
- Add a coverage report step to GitHub Actions (e.g., `--coverage` in Jest/Vitest) and surface the current baseline — do not enforce a gate yet, just make the number visible.
- Audit open bugs and tag those older than 30 days; produce a single-number count to track going forward.

### ◆ Medium term (this quarter)
- Enforce a pragmatic coverage threshold in CI — start at current baseline minus a small buffer, then raise it incrementally. Do not chase 100%; choose a threshold the team actually maintains.
- Implement Conventional Commits across the team (type + scope + description + optional ticket ref). Pairs well with the existing GitHub Actions setup and enables automated changelogs.
- Introduce a feature flag lifecycle review: monthly async scan of active flags — add owner + expiry to each. Flags are controlled tech debt; make them visible.
- Evaluate contract testing (e.g., Pact) for B2B SaaS integrations. At Series B with external customers, API contracts are a real integration risk worth guarding against.

### ◎ Long term (this half)
- Introduce the DFER loop for linting standards: add new ESLint/TypeScript rules as `warn` with a frozen `--max-warnings` CI threshold, then gradually reduce violations with "clean as you touch." This makes code standards monotonically improving without heroic refactors.
- Consider mutation testing (e.g., Stryker for TypeScript) on critical modules to validate that the 2,100 unit tests are actually catching real bugs — not just executing code paths.
- Formalize a post-mortem lightweight template for P1/P2 incidents. MTTR of 12 minutes is excellent; capturing the "why" on even low-frequency incidents compounds learning at the team level.

## Action items
| ID | Description | Horizon | Owner | Status |
|----|-------------|---------|-------|--------|
| A1 | Audit and triage all skipped/disabled tests | ⚡ short | | ○ open |
| A2 | Calculate CI success rate from GitHub Actions history (last 30 days) | ⚡ short | | ○ open |
| A3 | Add coverage report to CI pipeline (baseline visibility, no gate yet) | ⚡ short | | ○ open |
| A4 | Count and tag open bugs older than 30 days | ⚡ short | | ○ open |
| A5 | Enforce incremental coverage gate in GitHub Actions | ◆ medium | | ○ open |
| A6 | Adopt Conventional Commits with type + scope + ticket reference | ◆ medium | | ○ open |
| A7 | Introduce monthly feature flag lifecycle review | ◆ medium | | ○ open |
| A8 | Evaluate contract testing (Pact) for B2B API boundaries | ◆ medium | | ○ open |
| A9 | Implement DFER lint loop with frozen --max-warnings threshold in CI | ◎ long | | ○ open |
| A10 | Pilot mutation testing (Stryker) on highest-risk modules | ◎ long | | ○ open |
| A11 | Formalize lightweight P1/P2 post-mortem template | ◎ long | | ○ open |

---

## Snapshot

```
---
format_version: 1
date: 2026-03-26
team: "Helix (Atmos)"
repos:
  - name: "Helix"
    tech: "TypeScript · Next.js · Supabase"
---

# minottobot audit snapshot — Helix (Atmos) — 2026-03-26

## Repos in scope
- Helix (TypeScript · Next.js · Supabase)

## Area scores
| Area | Score |
|------|-------|
| CI/CD | 5 |
| Testing | 4 |
| Code review | 4 |
| Monitoring | 5 |
| Developer Experience | 5 |
| Ownership & culture | 4 |

## Top 3 blockers
1. CI success rate unknown — flakiness risk unmeasured
2. Coverage % not surfaced — no automated guard on untested surface area
3. Skipped/disabled test count unknown — false confidence in suite completeness

## Action items
| ID | Description | Horizon | Owner | Status |
|----|-------------|---------|-------|--------|
| A1 | Audit and triage all skipped/disabled tests | short | | open |
| A2 | Calculate CI success rate from GitHub Actions history (last 30 days) | short | | open |
| A3 | Add coverage report to CI pipeline (baseline visibility, no gate yet) | short | | open |
| A4 | Count and tag open bugs older than 30 days | short | | open |
| A5 | Enforce incremental coverage gate in GitHub Actions | medium | | open |
| A6 | Adopt Conventional Commits with type + scope + ticket reference | medium | | open |
| A7 | Introduce monthly feature flag lifecycle review | medium | | open |
| A8 | Evaluate contract testing (Pact) for B2B API boundaries | medium | | open |
| A9 | Implement DFER lint loop with frozen --max-warnings threshold in CI | long | | open |
| A10 | Pilot mutation testing (Stryker) on highest-risk modules | long | | open |
| A11 | Formalize lightweight P1/P2 post-mortem template | long | | open |
```
