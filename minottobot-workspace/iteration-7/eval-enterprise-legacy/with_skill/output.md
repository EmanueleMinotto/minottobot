 # Minottobot audit report — FinanceCore Ltd — March 03, 2023

## Repos in scope
- Microservices (Java Spring Boot) and React Frontend

## Executive summary (3 bullets max, each under 20 words)
- Long CI times impact productivity
- High incident rate requires improved monitoring
- Flaky tests create bottlenecks in development cycle

## Area scores (1 = critical · 5 = excellent)
| Area                 | Score | One-line finding |
|----------------------|-------|-----------------|
| CI/CD                |  1/5  | Long build times |
| Testing              |  2/5  | High flakiness    |
| Code review          |  3/5  | Formal policy, but ignored for 'hotfixes' |
| Monitoring           |  2/5  | High incident rate |
| Developer Experience |  2/5  | Inefficient dev cycle |
| Ownership & culture  |  2/5  | Low QA team capacity |

## Top 3 blockers right now
1. Inefficient development cycle due to flaky tests and long CI times
2. High incident rate requiring quicker resolution
3. Limited QA team capacity hindering quality control across teams

## Improvement plan
### Short term (this sprint)
- Reduce test flakiness by refactoring test code, improving test isolation, and adopting a testing framework with better stability
- Optimize CI builds to reduce build times
- Increase QA team capacity for immediate coverage across teams

### Medium term (this quarter)
- Evaluate CI tool migration (e.g. Jenkins → GitHub Actions, CircleCI, etc.) — migration requires 4–6 weeks parallel-run, dedicated CI team capacity
- Implement test automation to reduce manual testing and prevent regressions
- Adopt a more flexible code review process that incentivizes collaboration across teams

### Long term (this half)
- Replace Jenkins with a modern CI tool, improving overall developer experience
- Establish DevOps practices to promote a shift left culture and reduce incident rate
- Implement continuous testing strategies for quicker feedback and shorter release cycles

## Action items
| ID | Description | Horizon | Owner | Status |
|----|-------------|---------|-------|--------|
| A1 | Reduce test flakiness by refactoring test code | short | QA lead  | open  |
| A2 | Optimize CI builds to reduce build times  | short | DevOps engineer  | open  |
| A3 | Increase QA team capacity across teams   | short | HR manager  | open  |
| A4 | Evaluate CI tool migration (4–6 weeks parallel-run, dedicated CI team)  | medium | IT Manager  | open  |
| A5 | Implement test automation for faster feedback and reduced manual testing  | medium | QA engineer  | open  |
| A6 | Adopt a more flexible code review process across teams | medium | Engineering lead  | open  |
| A7 | Establish DevOps practices to reduce incident rate  | long | IT Manager, DevOps engineer  | open  |
| A8 | Implement continuous testing strategies for shorter release cycles   | long | QA engineer, Engineering lead  | open  |
