 Based on the provided data, here's a sample response following the requested structure:

# Minottobot audit report — Norsk Mobility AS — {today's date}

## Repos in scope
- Backend (Python + Django)
- Mobile App (React Native)

## Executive summary (3 bullets max, each under 20 words)
- Inefficient testing strategy
- Lack of monitoring until recently
- Room for improvement in Developer Experience

## Area scores (1 = critical · 5 = excellent)
| Area                 | Score | One-line finding                     |
|----------------------|-------|--------------------------------------|
| CI/CD                |  2/5  | GitHub Actions, but manual approval |
| Testing              |  1/5  | Limited tests (340 unit, 45 integration, 12 E2E) |
| Code review          |  3/5  | No mention of code review practices  |
| Monitoring           |  3/5  | Added Sentry recently               |
| Developer Experience |  2/5  | Frequent incidents and no tests    |
| Ownership & culture  |  2/5  | 4 days ago incident, ongoing investigation  |

## Top 3 blockers right now
1. **Inefficient testing strategy** — Limited test coverage, especially E2E tests
2. **Lack of monitoring until recently** — Inability to detect and address issues proactively before the recent incident
3. **Room for improvement in Developer Experience** — Manual approval gates and frequent incidents impacting user experience

## Improvement plan
### Short term (this sprint)
- Expand E2E test suite
- Enhance monitoring capabilities

### Medium term (this quarter)
- Implement continuous integration with automatic deployments
- Establish a formal code review process

### Long term (this half)
- Evaluate Jenkins → GitHub Actions — migration requires 4-8 weeks parallel-run, CI team capacity

## Action items
| ID | Description | Horizon | Owner | Status |
|----|-------------|---------|-------|--------|
| A1 | Expand E2E test suite | short | QA team | open |
| A2 | Enhance monitoring capabilities | short | DevOps team | open |
| A3 | Implement continuous integration with automatic deployments | medium | DevOps team | open |
| A4 | Establish a formal code review process | medium | Development team | open |
| A5 | Evaluate Jenkins → GitHub Actions — migration requires 4-8 weeks parallel-run, CI team capacity | long | DevOps team | planning |
