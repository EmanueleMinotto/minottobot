 # Minottobot audit report — FinanceCore Ltd Product Teams — 01/03/2023

## Repos in scope
- Microservices: Java Spring Boot, Database: Oracle DB, Frontend: React

## Executive summary (3 bullets max, each under 20 words)
- Outdated CI setup and long build times affecting DX
- High flaky tests percentage leading to reduced trust in test suite
- Inefficient deployment process with manual approvals

## Area scores (1 = critical · 5 = excellent)
| Area                 | Score | One-line finding               |
|----------------------|-------|-------------------------------|
| CI/CD                |  1/5  | Outdated Jenkins setup         |
| Testing              |  2/5  | High flaky tests percentage    |
| Code review          |  3/5  | Informal code review policy   |
| Monitoring           |  3/5  | Adequate monitoring in place  |
| Developer Experience |  2/5  | Inefficient deployment process |
| Ownership & culture  |  2/5  | Lack of dedicated QA per team  |

## Top 3 blockers right now
1. **Inefficient CI setup** — High build times and lack of reliability
2. **Flaky tests** — Reduced trust in the test suite due to high flaky rate
3. **Manual approvals in deployment process** — Increases time-to-market and potential errors

## Improvement plan
### Short term (this sprint)
- Implement strategies for reducing flaky tests, such as isolation, retry strategies, and test stabilization techniques
- Investigate options for speeding up the CI build process
- Evaluate code review process and enforce formal policies

### Medium term (this quarter)
- Migrate to a modern CI/CD solution with faster build times, better scalability, and improved reliability — migration requires 4–8 weeks parallel-run, dedicated CI team capacity
- Implement continuous integration practices and automation for the testing pipeline

### Long term (this half)
- Implement a more efficient deployment process with less manual approvals and faster deployments
- Evaluate test coverage gaps and implement unit tests where needed

## Action items
| ID | Description | Horizon | Owner | Status |
|----|-------------|---------|-------|--------|
| A1 | Implement strategies for reducing flaky tests | short | QA Guild | open   |
| A2 | Investigate options for speeding up CI build process | short | CI Team | open   |
| A3 | Evaluate code review process and enforce formal policies | short | Teams & QA Guild | open   |
| A4 | Migrate to modern CI/CD solution | medium  | CI Team | planned  |
| A5 | Implement continuous integration practices and automation for testing pipeline | medium | Teams & QA Guild | planned  |
| A6 | Implement more efficient deployment process | long   | Teams & Operations | planned  |
| A7 | Evaluate test coverage gaps and implement unit tests where needed | long   | Teams & QA Guild | planned  |
