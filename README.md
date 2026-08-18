# minottobot

Your friendly neighborhood QA developer.

minottobot is a QA software consultant persona, distributed as a [Claude Code plugin](https://docs.claude.com/en/docs/claude-code/plugins) with four skills. It audits software teams across CI/CD, testing, monitoring, Developer Experience, and culture — then builds a prioritized improvement plan.

## How to use

**Claude Code:**
```
/plugin marketplace add EmanueleMinotto/minottobot
/plugin install minottobot
```

Once installed, describe your team or project and the relevant skill activates automatically. Most users want the default engagement — just describe your team and stop there.

## The four skills

### `minottobot` — the default engagement

Runs [`audit`](skills/audit/SKILL.md) then automatically continues into [`strategy`](skills/strategy/SKILL.md), using the audit's output as the strategy's input. This is what activates on general requests like "audit our team" or "how do we improve our testing" — describe your team once, get the full audit + plan back in one pass.

<details>
<summary>Example output</summary>

```markdown
# Minottobot audit report — Acme Checkout squad — 2026-08-18

## Repos in scope
- checkout-web (React)
- checkout-api (Node)

## Executive summary
- CI is split across Jenkins and GitHub Actions with no authoritative pipeline — deploys can bypass review.
- Zero integration tests despite a 47-minute Jenkins build; regressions surface in production instead.
- No named owner for checkout-api since the last reorg — three months of unresolved P1s.

## Area scores (1 = critical · 5 = excellent)
| Area                    | Score | One-line finding                              |
|--------------------------|-------|-----------------------------------------------|
| CI/CD                    | 2/5   | Jenkins + GitHub Actions, no authoritative one |
| Testing                  | 2/5   | Unit only, 0 integration, 47-min build         |
| Code review               | 3/5   | Required on main, skipped on hotfix branch     |
| Monitoring                | 3/5   | Sentry present, no alerting on P1s             |
| Developer Experience      | 3/5   | Local setup documented, no staging parity      |
| Ownership & culture       | 2/5   | No named owner since reorg — 3mo unresolved P1s|

## Top 3 blockers right now
1. **No authoritative CI** — teams don't trust either pipeline enough to gate deploys on it.
2. **Ownership gap on checkout-api** — nobody has authority to prioritize the fix backlog.
3. **Zero integration coverage** — unit tests pass while checkout breaks in production.

## Improvement plan
### Short term (this sprint)
- Designate GitHub Actions as the single source of truth; make Jenkins advisory-only.
- Assign a named owner for checkout-api.

### Medium term (this quarter)
- Add integration tests around the checkout API's payment and cart endpoints.

### Long term (this half)
- Retire Jenkins once GitHub Actions has run in parallel for 4–8 weeks with no gaps.

## Action items
| ID | Description                          | Horizon | Owner | Status |
|----|---------------------------------------|---------|-------|--------|
| A1 | Make GitHub Actions authoritative      | short   |       | open   |
| A2 | Assign checkout-api owner               | short   |       | open   |
| A3 | Integration tests on payment/cart       | medium  |       | open   |
```

*(Full reports also include the Phase 0 baseline and evidence/red-flags sections, trimmed here for length.)*

</details>

### `audit`

Assesses the team across ten areas — CI/CD, environments, local development, code review, testing, automation, monitoring, technical standards, and ownership culture — and produces a scored audit report (repos in scope, Phase 0 baseline, six-area score table with evidence-based caps). It looks for red flags and anti-patterns, and stops there: no improvement plan, no action items. Use it directly when you only want the diagnosis, or want to feed the same audit output into `strategy` more than once.

<details>
<summary>Example output</summary>

```markdown
# Minottobot audit — Acme Checkout squad — 2026-08-18

## Repos in scope
- checkout-web (React)
- checkout-api (Node)

## Phase 0 baseline
- Team size: 6 engineers
- Total test count: 340 unit / 0 integration / 0 e2e
- Average CI run time: 47 minutes
- Deployment frequency: ~2/week
- Change failure rate: not tracked
- Days since last production incident: 4

## Area scores (1 = critical · 5 = excellent)
| Area                    | Score | One-line finding                              |
|--------------------------|-------|-----------------------------------------------|
| CI/CD                    | 2/5   | Jenkins + GitHub Actions, no authoritative one |
| Testing                  | 2/5   | Unit only, 0 integration, 47-min build         |
| Code review               | 3/5   | Required on main, skipped on hotfix branch     |
| Monitoring                | 3/5   | Sentry present, no alerting on P1s             |
| Developer Experience      | 3/5   | Local setup documented, no staging parity      |
| Ownership & culture       | 2/5   | No named owner since reorg — 3mo unresolved P1s|

## Evidence & red flags
- checkout-web has CI on every PR; checkout-api's Jenkins pipeline can be skipped with `[skip ci]`.
- 0 integration tests found despite payment logic spanning both repos.
- Last 20 commits on checkout-api: no conventional format, 6 direct pushes to main.

## Systems flagged for replacement evaluation
- Jenkins — 47-minute build, maintained by no one specific, duplicated by GitHub Actions on checkout-web.
```

</details>

### `strategy`

Takes an audit output — from a fresh `audit` run, pasted by the user, or loaded from a saved `.minottobot/` snapshot — and builds an improvement plan on three horizons:

- **Short term** — immediate pain relief, quick wins
- **Medium term** — foundations and frameworks
- **Long term** — structural improvement based on feedback

It reasons about trade-offs case by case, calibrates advice to team size and product context, and always evaluates options against a single golden rule: does this serve the user? Use it directly when you already have an audit output and only want the plan built from it.

<details>
<summary>Example output</summary>

```markdown
## Executive summary
- CI is split across Jenkins and GitHub Actions with no authoritative pipeline — deploys can bypass review.
- Zero integration tests despite a 47-minute Jenkins build; regressions surface in production instead.
- No named owner for checkout-api since the last reorg — three months of unresolved P1s.

## Top 3 blockers right now
1. **No authoritative CI** — teams don't trust either pipeline enough to gate deploys on it.
2. **Ownership gap on checkout-api** — nobody has authority to prioritize the fix backlog.
3. **Zero integration coverage** — unit tests pass while checkout breaks in production.

## Improvement plan
### Short term (this sprint)
- Designate GitHub Actions as the single source of truth; make Jenkins advisory-only.
- Assign a named owner for checkout-api.

### Medium term (this quarter)
- Add integration tests around the checkout API's payment and cart endpoints.

### Long term (this half)
- Evaluate retiring Jenkins — migration requires porting pipelines, a 4–8 week parallel-run
  period, and dedicated CI team capacity; do not start without explicit resourcing.

## Action items
| ID | Description                          | Horizon | Owner | Status |
|----|---------------------------------------|---------|-------|--------|
| A1 | Make GitHub Actions authoritative      | short   |       | open   |
| A2 | Assign checkout-api owner               | short   |       | open   |
| A3 | Integration tests on payment/cart       | medium  |       | open   |
```

*(Prepended with the "Repos in scope" and "Area scores" sections carried forward verbatim from the audit — trimmed here since they're shown in the `audit` example above.)*

</details>

### `test-selection`

Standalone — no audit required. Given a specific scenario ("what test should I write for this checkout flow?", "our E2E suite takes 45 minutes"), recommends the right test type (unit, integration, E2E, contract, visual regression, performance, mutation) using a decision matrix and heuristics. Both `audit` and `strategy` hand off to it on-demand when a testing gap surfaces mid-engagement.

<details>
<summary>Example output</summary>

```markdown
> **"What test should I write for our checkout's payment confirmation step?"**

This spans two internal services (cart → payment) plus a third-party payment gateway — start from the test pyramid, not the scenario alone.

- **Unit** — the discount/total calculation logic. Pure function, no external dependencies, fast feedback.
- **Integration** — cart-to-payment-service call, and the payment gateway call if a sandbox is available. This is where the interesting failure modes live (timeouts, partial charges).
- **E2E** — one test covering the full happy-path checkout journey. Don't add more than one or two here; it's a critical journey, not a place to re-test edge cases already covered below.

Skip contract tests unless the payment gateway's API changes without notice — not the case here since it's third-party with a stable, versioned API.

**Watch out:** if the gateway has no sandbox, fall back to a contract test against a mocked schema instead of hitting the real API from CI.
```
</details>


## Code inspection

When running inside a repository (Claude Code or any environment with file-system access), the `audit` skill reads the codebase before asking questions.

It starts by mapping which repositories are in scope — a single repo, multiple separate repos, or a monorepo with distinct sub-projects. It detects the primary technology of each from manifest files (`package.json`, `go.mod`, `pyproject.toml`, etc.) and adapts its scanning patterns accordingly.

For each repo it scans: CI/CD configs, test files and test config, build scripts, lint/format configs, monitoring integrations, git history (last 20 commits), and onboarding documentation.

After scanning all repos it produces an evidence map and flags cross-repo gaps — discrepancies between repositories (e.g., one has CI and the other doesn't) are often the most significant findings. If a Phase 0 answer contradicts what the code shows, the audit flags it explicitly. The contradiction is itself a finding.

Code inspection does not replace the Phase 0 questionnaire. Operational metrics (MTTR, incident count, deployment frequency) can't be read from code — those still require the team's input.

## Multi-session tracking

Progress can be tracked across sessions using a snapshot file stored in the repository.

At the end of every engagement, `strategy` produces a snapshot and asks you to save it as `.minottobot/audit-YYYY-MM-DD.md` in your workspace root. The snapshot uses a fixed schema (area scores, top blockers, action items with stable IDs) so audits can be compared over time.

When you start a new session and a previous snapshot exists, `audit` enters **returning engagement mode**: it shows a summary of the last audit (date, repos, scores, blockers) and asks what has changed. At the end of the new plan, `strategy` appends a **delta view** to the report:

- Score changes per area (`CI/CD: 2/5 → 3/5 ↑`)
- Blockers resolved, still open, or new
- Action item status changes (open → done)
- Repo scope changes (repos added or removed between sessions)

Action items have stable IDs (`A1`, `A2`, ...) that persist across sessions, so progress is traceable without manual cross-referencing.

## What minottobot doesn't do

- Product features and roadmap — only *how* to build, never *what* to build
- Infrastructure — cloud, scaling, networking
- ISO or regulatory certifications

## When each skill activates

The skill descriptions are intentionally explicit and slightly over-broad so skill routers don't miss them.

### Prompts that SHOULD trigger the default `minottobot` engagement

1. "Our CI pipeline is broken and builds are failing randomly."
2. "How do we improve our testing strategy?"
3. "We need a QA strategy for our new microservices project."
4. "Can you review our code review process?"
5. "Our test coverage has dropped to 40% — what do we do?"
6. "We have a bunch of flaky tests that keep failing in CI."
7. "How healthy is our CI/CD setup?"
8. "Our deployments take forever and we want better developer experience."
9. "Audit our engineering team's quality practices."

### Prompts that trigger `test-selection` directly

1. "We're not sure what kind of test to write for this feature."
2. "Unit or integration test for this ORM query?"

### Prompts that should NOT trigger minottobot

1. "Can you help me implement this new feature?" — product/feature work, out of scope
2. "How do I configure our Kubernetes cluster?" — infrastructure, out of scope
3. "Write a regex that validates email addresses." — general programming task
4. "What cloud provider should we use?" — infrastructure decision, out of scope
5. "Explain how React hooks work." — general technical education, not a team/process question

---

## Repository structure

```
.claude-plugin/
  plugin.json              ← plugin manifest (this repo root is the plugin)
  marketplace.json         ← self-hosted catalog, so this repo can be added directly
skills/
  minottobot/SKILL.md      ← default: orchestrates audit → strategy
  audit/
    SKILL.md
    references/
      checklist.md          ← step-by-step audit guide
      red-flags.md          ← anti-patterns and warning signs
      session-resume.md     ← returning-engagement greeting
  strategy/
    SKILL.md
    references/
      strategy.md           ← post-audit planning and trade-off reasoning
      philosophy.md         ← core beliefs and communication style
      frameworks.md         ← DFER loop, test pyramid, feature flags, git history
      snapshot-delta.md     ← snapshot format and delta view
  test-selection/
    SKILL.md                ← standalone test-type decision guide
```
