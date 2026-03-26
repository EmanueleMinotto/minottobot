# Minottobot audit report — Swiftly Inc — 2026-03-25

## Repos in scope
- swiftly-api (Node.js + PostgreSQL)
- swiftly-frontend (React)

## Executive summary
- Zero tests and no staging environment make every deploy a live gamble with real users.
- Daily user-reported incidents signal a complete monitoring blind spot — the team is always last to know.
- CI is cosmetic: linting alone provides no safety net, and manual Heroku pushes bypass any gate entirely.

## Area scores (1 = critical · 5 = excellent)

| Area                 | Score | One-line finding                                          |
|----------------------|-------|-----------------------------------------------------------|
| CI/CD                |  2/5  | Actions runs lint only; deploys are fully manual with no pipeline gate. |
| Testing              |  1/5  | Zero tests across the entire stack — critical gap.        |
| Code review          |  2/5  | Informal and inconsistent; no policy, no required approvals. |
| Monitoring           |  1/5  | No alerting; users are the de facto monitoring system.    |
| Developer Experience |  2/5  | No staging means devs can only validate in production.    |
| Ownership & culture  |  3/5  | Small team, likely high trust — but no structures to back it up yet. |

## Top 3 blockers right now
1. No monitoring or alerting — incidents are discovered by users, not the team, causing reputational damage daily.
2. Zero tests combined with direct pushes to production — there is no safety layer between a keystroke and a live outage.
3. No staging environment — every untested change lands directly on paying customers with no intermediate validation.

## Improvement plan

### Short term (this sprint)
- Wire up error tracking (Sentry free tier is immediate and zero-config for Node.js and React) and set up a Slack/email alert channel — the team must know before users do.
- Add a basic uptime monitor (Better Uptime, UptimeRobot) on the production API and frontend URL.
- Write the first 5–10 unit tests targeting the highest-risk business logic (auth, billing, data mutations) — establish the habit, not coverage targets.
- Create a lightweight code review policy: minimum 1 approval required before merge, enforced via GitHub branch protection on `main`.

### Medium term (this quarter)
- Provision a staging environment on Heroku (it can mirror production at low cost) and make it a hard rule: nothing goes to production without passing staging first.
- Replace `git push heroku main` with a GitHub Actions deployment pipeline: test → lint → deploy to staging → manual promote to production.
- Expand test coverage to integration tests on the most-used API endpoints (auth, core CRUD, critical user journeys).
- Add a structured PR template to make code review consistent and faster.

### Long term (this half)
- Build toward a meaningful test pyramid: unit tests on all business logic, integration tests on all endpoints, 2–3 E2E tests on the most critical user journeys (signup, core workflow, billing).
- Introduce structured on-call rotation and a lightweight incident post-mortem habit — even a 15-minute async write-up per incident builds a learning culture.
- Evaluate database migration tooling (e.g. node-pg-migrate or Prisma Migrate) to make schema changes safe and reproducible across environments.
- Define technical standards document: code style, API conventions, error handling patterns — reduces review friction and ramp-up time for future hires.

## Action items

| ID | Description | Horizon | Owner | Status |
|----|-------------|---------|-------|--------|
| A1 | Install Sentry on Node.js API and React frontend; configure Slack alerts | short | | open |
| A2 | Set up uptime monitoring on production API and frontend | short | | open |
| A3 | Write unit tests for top 3 highest-risk business logic modules | short | | open |
| A4 | Enable GitHub branch protection on `main`; require 1 approval to merge | short | | open |
| A5 | Provision Heroku staging environment mirroring production config | medium | | open |
| A6 | Build GitHub Actions deploy pipeline: lint → test → staging deploy → manual prod promote | medium | | open |
| A7 | Add integration tests for auth, core CRUD, and most-used API endpoints | medium | | open |
| A8 | Add PR template to both repos | medium | | open |
| A9 | Define and document minimum test pyramid targets; enforce in CI | long | | open |
| A10 | Establish incident post-mortem habit; store write-ups in a shared doc | long | | open |
| A11 | Adopt and configure a database migration tool across all environments | long | | open |
| A12 | Write a lightweight technical standards document covering style, API patterns, error handling | long | | open |
