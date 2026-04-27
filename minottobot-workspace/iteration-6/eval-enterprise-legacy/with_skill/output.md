# Minottobot audit report — FinanceCore Ltd. — 2023-02-20

## Repos in scope
- Not specified ({Java Spring Boot, React})

## Executive summary (3 bullets max, each under 20 words)
- Central QA guild of 6 lacks dedicated resources for 8 product teams.
- 30% flaky tests and frequent ignores hint at inadequate testing practices.
- Jenkins, set up in 2011, contributes to lengthy deployments.

## Area scores
| Area                 | Score | One-line finding |
|----------------------|-------|-----------------|
| CI/CD                | 2/5   | Maturity issues in Jenkins (2011 setup) impact deployment times. |
| Testing              | 2/5   | Flaky tests and frequent ignores compromise test effectiveness. |
| Code review          | 3/5   | Formal policy, but some teams skip it for 'hotfixes', weakening code quality. |
| Monitoring           | 4/5   | No major concerns, but could benefit from more granular monitoring. |
| Developer Experience | 2/5   | Slow deployments and flaky tests erode developer confidence. |
| Ownership & culture  | 3/5   | Central QA guild lacks dedicated resources for product teams, creating silos. |

## Top 3 blockers right now
1. **Flaky test maintenance** — Addressing the high percentage of flaky tests to prevent frequent ignores and maintain testing integrity.
2. **Jenkins migration planning** — Evaluate Jenkins replacement due to its age and impact on deployment times; include migration cost/risk.
3. **Central QA resource allocation** — Ensure dedicated resources for each product team within the central QA guild.

## Improvement plan
### Short term (this sprint)
- Implement 'break the build' feature in CI/CD pipelines to prevent ignored test failures.
- Improve testing efficiency by addressing flaky tests and reducing test suite size.

### Medium term (this quarter)
- Evaluate Jenkins → GitHub Actions migration — migration requires 4-8 weeks parallel-run, CI team capacity; assess tool's maturity and user experience.
- Implement automated deployment with reduced manual sign-offs to decrease deployment time.

### Long term (this half)
- Replace Oracle DB with a more modern database management system, considering cloud-based solutions for scalability and performance improvements.
- Establish dedicated QA resources within each product team under the central QA guild.

## Action items
| ID | Description | Horizon | Owner | Status |
|----|-------------|---------|-------|--------|
| A1 | Implement 'break the build' feature in CI/CD pipelines. | short | Central QA Guild | open |
