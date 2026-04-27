# Minottobot audit report — Atmos (Helix team) — 2026-04-27

## Repos in scope
- Helix product repos (TypeScript + Next.js + Supabase)

> ⚠️ Helix repositories were not accessible in the current workspace; findings use team-reported data.

## Executive summary (3 bullets max, each under 20 words)
- GitHub Actions 8-minute mandatory gate supports 4.2 deploys/day safely.
- Reliability is strong: 0.1 P1/month, 0.5 P2/month, MTTR 12 minutes.
- Biggest gap: missing lead time, change failure rate, CI success, coverage, skip, and flag-age metrics.

## Area scores (1 = critical · 5 = excellent)
| Area                    | Score | One-line finding                     |
|-------------------------|-------|--------------------------------------|
| 🟢 CI/CD                |  5/5  | GitHub Actions gate, 8-minute feedback, no bypass. |
| 🟢 Testing              |  4/5  | 2,100/380/85 tests; trust metrics missing. |
| 🟢 Code review          |  4/5  | One approval required; discussion is consistently substantive. |
| 🟢 Monitoring           |  5/5  | Datadog SLOs, runbooks, full on-call, 12-minute MTTR. |
| 🟢 Developer Experience |  4/5  | 4.2 deploys/day, feature flags, automatic rollback. |
| 🟢 Ownership & culture  |  4/5  | Seven engineers share quality ownership; no QA silo. |

> 🔴 1–2 critical/gap · 🟡 3 functional · 🟢 4–5 good/excellent

## Top 3 blockers right now
1. 🚨 **Quality telemetry gaps** — lead time, change failure rate, CI success %, coverage %, skipped-test count, flag count/age, and >30-day bugs are unreported.
2. ⚠️ **Test trust not yet measurable** — high test volume (2,100 unit, 380 integration, 85 E2E) but no flaky/disabled test signal.
3. ⚠️ **Evidence mismatch risk** — reported TypeScript + Next.js + Supabase stack could not be verified from available repository paths.

## Improvement plan
### ⚡ Short term (this sprint)
- Build one GitHub Actions + Datadog quality dashboard with lead time, change failure rate, CI success %, MTTR, skipped tests, and flag age.
- Enforce skipped/quarantined test metadata (`owner`, `ticket`, `disabledUntil`) and fail CI when expiry is reached.
- Add PR checklist evidence for manual golden-path verification on user-facing changes.

### ◆ Medium term (this quarter)
- Add contract checks between TypeScript service boundaries and Supabase schema/migrations in CI.
- Run a monthly feature-flag lifecycle review with explicit owner and removal condition per flag.
- Track flaky-test rate in GitHub Actions and enforce quarantine SLA by failure cluster.

### ◎ Long term (this half)
- Run quarterly reliability game days to validate rollback/runbook quality against Datadog SLO behavior.
- Establish a rotating quality-champion model across the 7 engineers to avoid concentrated process knowledge.

## Action items
| ID | Description | Horizon | Owner | Status |
|----|-------------|---------|-------|--------|
| A21 | Publish GitHub Actions + Datadog quality dashboard for missing DORA/quality metrics | ⚡ short | Tech lead + on-call lead | ○ open |
| A22 | Add expiry-based skipped-test policy with CI enforcement | ⚡ short | Test owners | ○ open |
| A23 | Add manual verification checklist evidence to PR template | ⚡ short | Engineering manager | ○ open |
| A24 | Introduce Supabase schema contract checks in CI | ◆ medium | Backend lead | ○ open |
| A25 | Create monthly feature-flag pruning ritual with owner/removal fields | ◆ medium | Feature owners | ○ open |
| A26 | Instrument flaky-test metric and quarantine SLA in GitHub Actions | ◆ medium | CI owner | ○ open |
| A27 | Run quarterly game days using existing runbooks and rollback paths | ◎ long | On-call rotation lead | ○ open |
| A28 | Rotate quality champion role across all engineers quarterly | ◎ long | Engineering manager | ○ open |
| A29 | Capture and report open bugs older than 30 days weekly | ⚡ short | Team lead | ○ open |

## Delta since 2026-04-27

### Score changes
| Area | Previous | Current | Change |
|------|----------|---------|--------|
| 🟢 CI/CD | 1/5 | 5/5 | ↑ +4 |
| 🟢 Testing | 1/5 | 4/5 | ↑ +3 |
| 🟢 Code review | 3/5 | 4/5 | ↑ +1 |
| 🟢 Monitoring | 3/5 | 5/5 | ↑ +2 |
| 🟢 Developer Experience | 1/5 | 4/5 | ↑ +3 |
| 🟢 Ownership & culture | 2/5 | 4/5 | ↑ +2 |

> Emoji reflects the **current** score: 🔴 1–2 · 🟡 3 · 🟢 4–5

### Blockers
- **Resolved:** none verifiable; previous blockers were tied to dropped repo scope.
- **Still open:** none; previous blockers are not in current scope.
- **New:** missing quality telemetry baseline; unmeasured test trust; repository-evidence mismatch risk.

### Action items
| ID | Description | Status change |
|----|-------------|---------------|
| A12 | Flaky-test reduction program (previous engagement) | dropped from scope |
| A13 | Jenkins pipeline split (previous engagement) | dropped from scope |
| A14 | Hotfix review enforcement (previous engagement) | dropped from scope |
| A15 | DORA instrumentation (previous engagement) | dropped from scope |
| A16 | Manual deployment sign-off replacement (previous engagement) | dropped from scope |
| A17 | Test pyramid rebalance (previous engagement) | dropped from scope |
| A18 | SLO + runbook response standardization (previous engagement) | dropped from scope |
| A19 | Team quality ownership rollout (previous engagement) | dropped from scope |
| A20 | Jenkins replacement pilot (previous engagement) | dropped from scope |
| A21 | GitHub Actions + Datadog quality dashboard | new |
| A22 | Expiry-based skipped-test policy | new |
| A23 | PR manual verification evidence checklist | new |
| A24 | Supabase contract checks in CI | new |
| A25 | Monthly feature-flag lifecycle review | new |
| A26 | Flaky-test rate + quarantine SLA | new |
| A27 | Quarterly reliability game days | new |
| A28 | Rotating quality champion model | new |
| A29 | Weekly >30-day bug reporting | new |

### Repo scope
- Added: Helix product repos (TypeScript + Next.js + Supabase) — no previous data to compare
- Removed: Spring Boot microservices (Java Spring Boot) — dropped from scope
- Removed: React frontend (React) — dropped from scope