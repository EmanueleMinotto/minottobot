# Minottobot audit report — Swiftly Inc — 2026-03-26

## Repos in scope
- swiftly-api (Node.js / PostgreSQL)
- swiftly-frontend (React)

## Executive summary (3 bullets max, each under 20 words)
- Zero tests and daily user-reported incidents signal a team in permanent reactive firefighting mode.
- No staging environment means every deploy is a live experiment on real users.
- CI runs ESLint only — no safety net exists beyond a linter.

## Area scores (1 = critical · 5 = excellent)
| Area                 | Score | One-line finding                              |
|----------------------|-------|-----------------------------------------------|
| CI/CD                |  2/5  | GitHub Actions exists but enforces no quality gate |
| Testing              |  1/5  | Zero tests across all layers                  |
| Code review          |  2/5  | Informal, ad-hoc, no policy enforced          |
| Monitoring           |  1/5  | Users report bugs before team notices         |
| Developer Experience |  2/5  | Manual deploys, no staging, constant incidents |
| Ownership & culture  |  2/5  | No QA role; quality has no clear owner        |

## Top 3 blockers right now
1. **No monitoring** — the team is blind in production; users are the alert system. Every incident is a surprise.
2. **Zero tests** — there is no automated safety net; any deploy can break anything undetected.
3. **No staging environment** — untested code ships directly to production users, amplifying every other risk.

## Improvement plan

### Short term (this sprint)
- Add Sentry (free tier) to both the Node.js API and the React frontend for production error tracking — this is one day of work and immediately ends the "users report before we notice" pattern.
- Add a health-check endpoint to the API and a basic uptime monitor (Better Uptime or UptimeRobot free tier) so the team knows about outages before customers do.
- Establish a minimal code review policy: no self-merges, at least one approval required before merging to `main`. Enforce this via GitHub branch protection rules — 30 minutes of configuration.
- Add GitHub branch protection to block direct pushes to `main` and require the existing ESLint GitHub Actions check to pass before merge.

### Medium term (this quarter)
- Provision a staging environment on Heroku (a second app pointing at a separate PostgreSQL database). Mirror the production deploy process. Make "deploy to staging first" the team norm before any production push.
- Introduce a testing baseline: start with integration tests for the Node.js API using Jest + Supertest, targeting the three most incident-prone endpoints first. Don't aim for coverage percentage — aim for the paths that have burned the team.
- Automate deployments: replace `git push heroku main` with a GitHub Actions deploy workflow that requires the CI check to pass and deploys to staging automatically on merge, with a manual promotion gate to production.
- Introduce Conventional Commits and a lightweight commit message convention. This costs nothing but makes the Git history usable and sets the foundation for automated changelogs.

### Long term (this half)
- Grow the test pyramid: once integration tests exist and the team trusts them, add unit tests for business logic (Node.js services/utils) and a thin layer of E2E smoke tests using Playwright covering the two or three most critical user flows.
- Build an incident review habit: after each production incident, hold a short blameless post-mortem (15 minutes max). Document what happened, what the detection gap was, and what test or alert would have caught it. Over time this feeds the test suite organically.
- Evaluate hiring or designating a quality champion — not a dedicated QA gatekeeper, but a developer who owns the health of the test suite and CI pipeline as part of their responsibilities. At 4 engineers this doesn't require a new hire; it requires a role assignment.
- Once staging is stable and tests exist, aim for a deployment pipeline with automated promotion: PR → CI (lint + tests) → auto-deploy to staging → manual promote to production.

## Action items
| ID | Description | Horizon | Owner | Status |
|----|-------------|---------|-------|--------|
| A1 | Install Sentry on Node.js API and React frontend | short | | open |
| A2 | Add uptime monitoring (UptimeRobot or Better Uptime) | short | | open |
| A3 | Enable GitHub branch protection on `main` (no self-merge, CI required) | short | | open |
| A4 | Establish and document minimum code review policy | short | | open |
| A5 | Provision staging environment on Heroku with separate PostgreSQL | medium | | open |
| A6 | Write integration tests for top 3 incident-prone API endpoints (Jest + Supertest) | medium | | open |
| A7 | Automate deploy pipeline in GitHub Actions (staging auto, production manual gate) | medium | | open |
| A8 | Adopt Conventional Commits convention across the team | medium | | open |
| A9 | Grow test coverage to unit tests for core business logic | long | | open |
| A10 | Add Playwright E2E smoke tests for 2-3 critical user flows | long | | open |
| A11 | Establish blameless post-mortem ritual after each production incident | long | | open |
| A12 | Designate a quality champion responsible for CI and test suite health | long | | open |
