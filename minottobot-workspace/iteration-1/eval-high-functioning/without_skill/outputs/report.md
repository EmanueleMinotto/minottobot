## Assessment: Helix Team Engineering Quality Practices

---

### Overall Summary

Helix is operating at a high level of engineering maturity for a 7-person team at Series B. The core indicators — incident rate, MTTR, deploy frequency, and CI discipline — are elite-tier. The main gaps are in structural safeguards that become critical as the team and codebase grow.

---

### Area Scores

| Area | Score | Rationale |
|---|---|---|
| Test Coverage & Strategy | 4/5 | Strong volume and pyramid shape; missing contract and performance testing |
| CI/CD Pipeline | 4/5 | Fast, enforced, and no-exception policy is excellent; mutation testing absent |
| Deployment Safety | 5/5 | Feature flags + automatic rollback is best practice, executed well |
| Incident Management | 5/5 | 0.1 P1/month and 12-min MTTR at this scale is outstanding |
| Observability | 5/5 | Custom SLOs per service, full on-call, runbooks — nothing missing here |
| Code Review | 3/5 | 1 approval is the weak link; no architectural review process described |
| Testing Culture | 4/5 | No dedicated QA is workable with this discipline; risk grows with headcount |
| Overall | **4.3 / 5** | Top quartile for stage and size |

---

### Priority 1 — Address Before the Team Grows

**1.1 Increase required approvals to 2 for high-risk paths**

One approval is fine for low-risk changes but is a single point of failure for schema migrations, auth flows, billing logic, and public API surface. The fix is not to require 2 approvals everywhere — that creates friction — but to use GitHub CODEOWNERS to enforce 2 approvals on specific directories or file patterns. This costs the team almost nothing and closes a real blast-radius risk.

**1.2 Formalize an architectural decision record (ADR) process**

At Series B with a 4-year-old codebase, undocumented architectural decisions accumulate fast. There is no mention of how large decisions are made or recorded. A lightweight ADR process (a `/docs/decisions/` directory with a simple template) prevents the team from relitigating the same debates and gives new hires context that is otherwise locked in individual heads.

**1.3 Add contract testing for Supabase schema changes**

The TypeScript + Supabase stack has a specific failure mode: database schema changes that break application code are often caught late because unit and integration tests mock the database. Tools like `supabase test db` combined with generated types from `supabase gen types typescript` should be enforced in CI so that schema drift fails the pipeline before merge, not after deploy.

---

### Priority 2 — Improve Test Robustness

**2.1 Introduce mutation testing**

2,100 unit tests is a healthy number, but test count is a poor proxy for test quality. Mutation testing (Stryker is the standard for TypeScript) measures whether tests actually detect faults. A common finding at this test volume is a 30–40% mutation score gap, meaning a large portion of tests pass even when logic is broken. Running Stryker on a single critical module first (e.g., billing or access control) will reveal whether the test suite is trustworthy or just large.

**2.2 Add performance regression testing to CI**

There is no mention of performance benchmarks. Next.js applications have well-known bundle size and Web Vitals regression risks, especially as feature development accelerates. Lighthouse CI or a bundle size tracking tool (bundlesize, size-limit) added to the CI pipeline creates an automatic signal before customers notice. This takes roughly half a day to implement and pays for itself the first time it catches a regression.

**2.3 Define and enforce coverage thresholds per module**

Aggregate coverage numbers are not mentioned. Even with 2,500+ tests, coverage can be heavily skewed toward simple utilities and away from complex business logic. Setting per-directory coverage thresholds in Jest or Vitest config (higher for `src/billing`, `src/auth` than for `src/components`) targets the protection where it matters most.

---

### Priority 3 — Sustain as the Team Scales

**3.1 Introduce a chaos / failure injection practice**

The incident metrics are excellent, but 0.1 P1/month may reflect a codebase that has not yet been stressed by scale. At Series B, proactive failure injection (even lightweight: disabling a Supabase connection in staging, simulating third-party API timeouts) validates that automatic rollback and runbooks work before a real incident tests them. This does not require a formal chaos engineering program — a quarterly game day with the existing on-call rotation is sufficient.

**3.2 Create an explicit onboarding quality checklist**

With 7 engineers and no dedicated QA, the quality culture is currently person-dependent. As the team grows, new engineers need an explicit, written standard for what "done" means: test requirements, observability requirements (does this feature have a Datadog SLO?), rollback requirements. The current practices are strong but informal; formalizing them as a short checklist in the PR template preserves the culture through growth.

**3.3 Evaluate a second approval requirement for E2E test skips**

E2E tests at 85 is a reasonable number, but there is no mention of a policy for skipping or marking tests as flaky. A single flaky E2E test that gets marked `skip` without review is a recurring source of silent coverage loss. A lightweight policy — any E2E skip requires a comment with a linked issue and a second reviewer — keeps the E2E suite honest.

---

### What Is Already Working and Should Not Be Changed

- The no-exceptions CI policy is rare and valuable. Do not introduce escape hatches.
- Feature flags for all deploys combined with automatic rollback is the correct model. Preserve this as a hard requirement, not a soft convention.
- MTTR of 12 minutes suggests runbooks are accurate and on-call handoffs work. Invest in keeping runbooks current as the team grows rather than replacing the process.
- The culture of substantive PR discussion at consistent 1-approval throughput is a sign of a healthy, non-bureaucratic review process. Adding CODEOWNERS for high-risk paths preserves this while closing the coverage gap.

---

### Summary Table of Recommendations

| Recommendation | Effort | Impact | Priority |
|---|---|---|---|
| CODEOWNERS with 2-approval on critical paths | Low | High | P1 |
| ADR process | Low | High | P1 |
| Supabase contract testing in CI | Medium | High | P1 |
| Mutation testing on critical modules | Medium | High | P2 |
| Lighthouse CI / bundle size tracking | Low | Medium | P2 |
| Per-module coverage thresholds | Low | Medium | P2 |
| Quarterly chaos / failure injection game day | Medium | Medium | P3 |
| Quality checklist in PR template | Low | Medium | P3 |
| E2E skip policy | Low | Low | P3 |
