## Engineering Quality Assessment — Swiftly Inc.

---

### Overall Summary

Swiftly is operating at a pre-quality baseline. The current practices are characteristic of an early-stage team that has optimized entirely for shipping speed while accumulating compounding operational risk. With 1 incident per day and zero automated safety nets, the team is one bad deployment away from a significant customer trust event. The good news: the stack is conventional, the team is small enough to move quickly, and the gaps are well-understood problems with well-understood solutions.

---

### Area Scores (1–5)

| Area | Score | Rationale |
|---|---|---|
| Test Coverage | 1/5 | Zero tests. No unit, integration, or E2E coverage. |
| CI/CD Pipeline | 1.5/5 | CI exists but provides almost no safety signal beyond syntax. No staging gate. |
| Deployment Process | 1.5/5 | Fully manual, no rollback strategy, direct push to production. |
| Observability | 1/5 | Incidents are user-reported. Team has no proactive visibility into system health. |
| Code Review | 2/5 | Ad hoc reviews happen, but inconsistency means coverage is unpredictable. |
| Environment Strategy | 1/5 | No staging. Every change is validated in production by real users. |
| Incident Management | 2/5 | 1-hour MTTR is reasonable once the team knows about it. The detection gap is the failure. |

**Composite Score: 1.4 / 5**

---

### Recommendations by Priority

---

#### Priority 1 — Stop the Bleeding (Week 1–2)

These are low-effort, high-impact changes that reduce daily incident rate immediately.

**1.1 — Add basic uptime and error monitoring**

Deploy a lightweight monitoring tool (Sentry for error tracking, Better Uptime or Checkly for endpoint monitoring). This alone will shift incident detection from "user reports it" to "you know before the user does." This is a single afternoon of work. Do it first.

**1.2 — Formalize code review as a hard gate**

Establish a branch protection rule on `main` requiring at least one approved review before merge. This is a GitHub setting, not a process negotiation. It takes five minutes to configure. The current "whoever is around" model creates coverage gaps and diffuses accountability. A written policy does not need to be long — a single paragraph defining what reviewers are expected to check is sufficient.

**1.3 — Add a staging environment**

Heroku supports environment pipelining natively. A staging dyno that mirrors production can be provisioned in under an hour. Every change should run in staging before reaching production. This single change reduces the blast radius of every deployment.

---

#### Priority 2 — Build a Safety Net (Weeks 2–6)

**2.1 — Introduce a testing baseline**

Do not attempt to retroactively test the entire codebase. Instead, establish a forward rule: all new features and all bug fixes require a test. Start with the highest-risk surface area — database migrations, authentication flows, and any billing logic. A reasonable near-term target is 40–60% coverage on critical paths, not blanket coverage.

Recommended tooling for this stack:
- Node.js API: Jest or Vitest with Supertest for HTTP-level integration tests
- React frontend: Vitest + React Testing Library for component tests
- PostgreSQL: include migration smoke tests that verify schema integrity after each migration

**2.2 — Expand CI to run tests and enforce a merge gate**

The current 2-minute ESLint-only pipeline provides false confidence. Expand the pipeline to: lint → unit tests → integration tests → build verification. The pipeline should block merges on failure. A 5–10 minute CI run with real test coverage is worth far more than a 2-minute run that only checks formatting.

**2.3 — Automate deployments through the pipeline**

Replace `git push heroku main` with a pipeline-triggered deployment. The flow should be: PR merged to main → CI passes → auto-deploy to staging → manual promotion gate to production (or auto-promote after a soak period). This removes the ability to bypass safety checks via a direct push.

---

#### Priority 3 — Build Operational Maturity (Weeks 6–12)

**3.1 — Implement structured incident response**

Even without a dedicated QA engineer, the team can adopt a lightweight incident process: a shared Slack channel for incident coordination, a simple severity classification (P1/P2/P3), and a lightweight post-mortem template for any incident that affects customers. The goal is pattern recognition — if the same component causes three incidents, you surface that before the fourth.

**3.2 — Add database migration safety**

No mention was made of migration strategy. On a PostgreSQL + Node.js stack, uncontrolled migrations run directly against production are a common source of incidents. Migrations should be versioned (e.g., via node-postgres-migrate or Knex migrations), reviewed in PRs, and run as an explicit step in the deployment pipeline — not ad hoc.

**3.3 — Define an on-call rotation**

With 1 incident per day, someone is implicitly always on-call. Making that explicit — rotating the responsibility weekly across the three backend engineers — distributes burnout and ensures clear ownership. This costs nothing but a calendar entry and a brief runbook.

---

### What Not to Do Right Now

- Do not invest in a full QA process or hire a QA engineer at this stage. The leverage is in automated tests and monitoring, not manual QA.
- Do not attempt to reach 80%+ test coverage immediately. That target applied retroactively will consume weeks with low marginal safety gain. Incremental forward coverage is the right approach.
- Do not redesign the CI/CD system from scratch. The GitHub Actions + Heroku pipeline is entirely capable of supporting the improvements above. Replace the manual push step before introducing new tooling.

---

### Suggested 30-Day Target State

| Area | Current | 30-Day Target |
|---|---|---|
| Test Coverage | 0% | ~30% on critical paths |
| CI Duration | 2 min (lint only) | 8–12 min (lint + tests + build) |
| Deployment | Manual push | Pipeline-gated, staging required |
| Monitoring | None | Sentry + uptime checks live |
| Incident detection | User-reported | Automated alerting before users notice |
| Code Review | Ad hoc | Branch protection enforced |

Achieving the above within 30 days is realistic for a 4-person team without disrupting feature delivery. The first week's changes (monitoring, branch protection, staging) require no test-writing at all and will have an immediate effect on incident rate.
