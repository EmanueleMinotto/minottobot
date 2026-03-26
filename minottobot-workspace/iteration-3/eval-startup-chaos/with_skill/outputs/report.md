# Minottobot audit report — Swiftly Inc — 2026-03-26

## Repos in scope
- Node.js API (Node.js / Express — assumed)
- React frontend (React)
- PostgreSQL database (data layer, not directly audited)

> ⚠️ **No code access** — this audit is based on team-reported data only. Findings could not be verified against the codebase.

## Phase 0 — Quantitative baseline

| # | Question | Answer | Finding |
|---|----------|--------|---------|
| 1 | Team size | 4 engineers (3 backend, 1 frontend), no dedicated QA | — |
| 2 | Total test count | 0 | 🚨 No tests at all |
| 3 | Average CI run time | ~2 minutes (ESLint only) | — |
| 4 | Deployment frequency | 2–3x per day via `git push heroku main` | Manual deploy, no automation |
| 5 | Last month's CI success rate | Not provided | 🔍 Unknown — itself a finding |
| 6 | MTTR | ~1 hour once the team is notified | Detection lag is the real problem |
| 7 | Test coverage % | N/A (0 tests) | 🚨 0% |
| 8 | Skipped / disabled tests | N/A (0 tests) | — |
| 9 | Days since last production incident | ~0 — roughly 1 per day | 🚨 Daily incidents |
| 10 | Open bugs older than 30 days | Not provided | 🔍 Unknown — itself a finding |

**Unanswered numbers (findings in themselves):** CI success rate and open-bug backlog age are unknown. A team that doesn't track these has no feedback loop on its own quality posture.

---

## Executive summary
- Zero tests, no staging environment, and manual deploys create daily production incidents.
- Users detect problems before the team does — monitoring is completely absent.
- Code review is informal with no policy, allowing unreviewed code into production daily.

## Area scores (1 = critical · 5 = excellent)

| Area                    | Score | One-line finding                                        |
|-------------------------|-------|---------------------------------------------------------|
| 🔴 CI/CD                |  2/5  | Pipeline runs ESLint only; deploy is fully manual       |
| 🔴 Testing              |  1/5  | Zero tests across all repos                             |
| 🔴 Code review          |  2/5  | No policy; ad-hoc, whoever is around                   |
| 🔴 Monitoring           |  1/5  | Users report incidents before the team notices          |
| 🔴 Developer Experience |  2/5  | No staging, no safety nets, daily firefighting          |
| 🔴 Ownership & culture  |  2/5  | Quality deferred; "we'll write tests" unresolved        |

> 🔴 1–2 critical/gap · 🟡 3 functional · 🟢 4–5 good/excellent

---

## Top 3 blockers right now

1. 🚨 **No monitoring** — the team learns about production incidents from users, not systems. With 1 incident/day and ~1 hour MTTR, every outage window is unnecessarily long because detection is outsourced to paying customers. This is the highest-impact fix: an error tracker like Sentry can be up in under an hour.

2. 🚨 **Zero tests + manual deploy to production** — `git push heroku main` with 0 tests and 2–3 deploys per day means every push is a live gamble. There is no automated gate between a developer's laptop and production users. Each deploy is a trust exercise with no verification layer.

3. ⚠️ **No staging environment** — without a staging environment, there is no safe place to test anything. Features go straight from local to production. This makes every code review moot (you can't verify the change), every deploy risky, and every experiment user-visible. This is also the source of the high coordination overhead ("don't deploy, I'm testing something").

---

## Improvement plan

### ⚡ Short term (this sprint)

- **Add Sentry to both the Node.js API and the React frontend.** Sentry's free tier covers seed-stage needs. This single action converts user-reported incidents into team-detected incidents and reduces MTTR from "when a user complains" to "within minutes." Target: deployed by end of week.

- **Add a `test` script placeholder in `package.json` and write the first 3 unit tests for the highest-risk API endpoint.** The goal is not coverage — it is establishing the habit and the scaffold. Pick the endpoint that, if broken, would generate a support ticket in under 5 minutes.

- **Freeze the ESLint warning count.** GitHub Actions already runs ESLint. Add `--max-warnings=N` (where N is the current count) so the build fails if warnings increase. Quality becomes monotonically improving from day one, at zero cost.

- **Document the deployment process in a README or runbook.** `git push heroku main` is undocumented tribal knowledge. If the person who knows the process is unavailable during an incident, MTTR doubles.

### ◆ Medium term (this quarter)

- **Add a staging environment on Heroku.** Heroku makes this a single `heroku create` command with a git remote. The payoff: safe testing, no more coordination overhead, and a place to run automated checks before production. This directly addresses Case Study 2 in the operational frameworks.

- **Adopt Jest (backend) and Vitest (frontend) and reach 20% coverage on critical paths.** Do not target 100% — target the paths that, if broken, hurt users immediately: authentication, payment flows, core CRUD. Use test-after for now; move toward test-first incrementally.

- **Formalize code review with a lightweight policy.** Two rules are enough to start: (1) no self-merge, (2) at least one approval required. Enforce via GitHub branch protection rules on `main`. This is a 5-minute configuration change with significant quality impact.

- **Add integration tests for the PostgreSQL layer.** Node.js API + PostgreSQL is the most likely source of silent data bugs. Integration tests against a test database (using testcontainers or a Docker Compose setup) catch the class of bugs that unit tests miss.

- **Set up Conventional Commits and a commit message lint hook.** With 2–3 deploys/day, git history is a high-velocity asset. A hook (commitlint + husky) costs 30 minutes to set up and pays off every time you need to trace a regression.

### ◎ Long term (this half)

- **Add Playwright E2E tests for the 3 most critical user journeys.** These are the tests that verify what no unit or integration test can: the full user experience from browser to database. Start with the journeys that, if broken, would generate a support ticket within 5 minutes (login, core workflow, billing if applicable).

- **Implement a feature flag system (LaunchDarkly free tier or Unleash self-hosted).** This separates deploy from release — you can push code any time and control who sees it. It also enables gradual rollouts (5% → 20% → 100%) once observability is in place. This is the foundation for safe experimentation at a faster pace.

- **Build a lightweight incident review process.** 1 incident/day is a signal, not just a fact. Run a 15-minute blameless post-mortem after each notable incident: what happened, why it wasn't caught earlier, what one thing we change to prevent recurrence. The goal is to feed learnings back into the test suite and monitoring, not to assign blame.

- **Establish a quality ownership model.** Right now, quality belongs to no one ("we keep saying we'll write tests"). Rotate a "quality champion" role weekly — one engineer owns the test suite health, incident follow-ups, and flag for new coverage gaps. Rotate every sprint so no one owns it permanently and everyone understands it.

---

## Action items

| ID  | Description                                                          | Horizon   | Owner | Status  |
|-----|----------------------------------------------------------------------|-----------|-------|---------|
| A1  | Add Sentry to Node.js API and React frontend                         | ⚡ short  |       | ○ open  |
| A2  | Write first 3 unit tests for highest-risk API endpoint               | ⚡ short  |       | ○ open  |
| A3  | Freeze ESLint warning count with `--max-warnings=N` in GitHub Actions | ⚡ short |       | ○ open  |
| A4  | Document deployment process (runbook in README)                      | ⚡ short  |       | ○ open  |
| A5  | Add staging environment on Heroku                                    | ◆ medium  |       | ○ open  |
| A6  | Adopt Jest (API) and Vitest (frontend); reach 20% coverage on critical paths | ◆ medium | | ○ open |
| A7  | Configure GitHub branch protection: no self-merge, 1 approval required | ◆ medium |      | ○ open  |
| A8  | Add integration tests for PostgreSQL layer                           | ◆ medium  |       | ○ open  |
| A9  | Set up Conventional Commits + commitlint + husky                     | ◆ medium  |       | ○ open  |
| A10 | Add Playwright E2E tests for top 3 user journeys                     | ◎ long    |       | ○ open  |
| A11 | Implement feature flag system (LaunchDarkly or Unleash)              | ◎ long    |       | ○ open  |
| A12 | Establish lightweight blameless incident review process              | ◎ long    |       | ○ open  |
| A13 | Rotate weekly quality champion role across the team                  | ◎ long    |       | ○ open  |

---

*Snapshot saved to `.minottobot/audit-2026-03-26.md` — future sessions will compare against this baseline.*
