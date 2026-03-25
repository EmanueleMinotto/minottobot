<!--
  Eval: startup-chaos
  Team: Swiftly Inc
  Input prompt: see evals.json id=1
  Generated: 2026-03-25
  Re-run: load minottobot/ skill, paste the prompt from evals.json id=1, capture output here
-->

# Minottobot audit report — Swiftly Inc — 2026-03-25

## Repos in scope
- swiftly-api (Node.js + PostgreSQL)
- swiftly-web (React)

## Executive summary (3 bullets max, each under 20 words)
- Zero tests and no staging mean every deploy is a live experiment with real users.
- Incidents detected by users (~1/day) indicate no internal visibility before damage is done.
- The CI pipeline lints code but offers no safety net for regressions.

## Area scores (1 = critical · 5 = excellent)
| Area                | Score | One-line finding                                      |
|---------------------|-------|-------------------------------------------------------|
| CI/CD               |  2/5  | Linting only; no tests run; manual Heroku push        |
| Testing             |  1/5  | Zero tests; no coverage at any layer                  |
| Code review         |  2/5  | Ad hoc; no policy; inconsistent participation         |
| Monitoring          |  1/5  | Users report incidents before the team notices        |
| Developer Experience|  2/5  | No staging; manual deploys; no deploy confidence      |
| Ownership & culture |  2/5  | No formal ownership; quality relies on individual care|

## Top 3 blockers right now
1. **No tests + daily production deploys = daily user-facing incidents.** The team is shipping directly to production 2-3 times a day with zero automated safety net. At ~1 incident/day, the cost of no testing is already visible in user trust and developer stress.
2. **No staging environment.** Every untested change hits production directly. Even a minimal Heroku staging app (same config, seeded DB) would catch a class of environment-specific failures before they reach users.
3. **Incidents invisible until users report them.** With no error tracking, the team has no way to know something is broken until a user complains. Mean time to *detect* is undefined — it depends entirely on user patience.

## Improvement plan
### Short term (this sprint)
- Add integration tests for the 3 most critical user flows (sign-up, core action, payment/checkout if applicable). These catch the bugs most likely causing today's daily incidents without requiring a testing culture overhaul.
- Set up a staging environment on Heroku (a second app, same environment variables, seeded database). Cost: a few hours of setup, minimal ongoing cost.
- Add Sentry (free tier) to the API. Takes ~15 minutes; immediately surfaces errors the team currently learns about from users.

### Medium term (this quarter)
- Introduce a lightweight code review policy: any PR touching data access or auth requires at least one review before merge. Start there — don't boil the ocean.
- Expand test coverage to unit tests on the most complex business logic modules, guided by the paths that have caused incidents.
- Add CI step to run integration tests on every push; block merge if tests fail.

### Long term (this half)
- Build a proper test pyramid: unit tests for business logic, integration tests for API contracts, a handful of E2E tests for the most critical happy paths.
- Move deployments from manual `git push heroku main` to a CI-triggered deploy pipeline with a mandatory staging pass before production.
- Establish a weekly incident review (15 minutes): what broke, why, what test would have caught it. This habit compounds — it is how testing culture forms in small teams.

## Action items
| ID | Description | Horizon | Owner | Status |
|----|-------------|---------|-------|--------|
| A1 | Write integration tests for top 3 user flows | short | | open |
| A2 | Create staging environment on Heroku | short | | open |
| A3 | Add Sentry to the API | short | | open |
| A4 | Define lightweight code review policy | medium | | open |
| A5 | Add CI step to run integration tests, block merge on failure | medium | | open |
| A6 | Expand unit tests to high-complexity business logic modules | medium | | open |
| A7 | Migrate to CI-triggered deploy pipeline with staging gate | long | | open |
| A8 | Establish weekly incident review ritual | long | | open |

---

## Assertions

| # | Assertion | Pass? |
|---|-----------|-------|
| 1 | Output must give at least one short-term action item related to testing | PASS — A1: "Write integration tests for top 3 user flows" is a short-horizon testing item |
| 2 | Output must mention the absence of a staging environment | PASS — Blocker #2 and A2 both explicitly address the missing staging environment |
| 3 | Output must score CI/CD at 2/5 or lower | PASS — CI/CD scored 2/5 |
| 4 | Output must recommend a specific test type to adopt first, not just "add tests" | PASS — recommends integration tests targeting the 3 most critical user flows specifically |
| 5 | Output must not recommend a full test suite rewrite as the first step | PASS — first step is targeted integration tests for 3 flows, not a rewrite |
