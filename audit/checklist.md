# minottobot — Audit Checklist

A structured guide for assessing a team or project. minottobot uses this as a starting framework — not a rigid script.

---

## Step 1: Gather context

Before looking at code or pipelines, collect three inputs:

### Tech stack assessment
- What languages, frameworks, and tools are in use?
- Is the stack modern, legacy, or a mix?
- Are there known constraints (e.g., locked versions, vendor dependencies)?

### User situation
- Is the product stable or experiencing frequent issues?
- How full is the bug backlog?
- Are users reporting problems regularly?
- What's the current incident frequency?

### Developer feedback
- How do developers feel about the codebase? (theirs vs alien)
- Where do they experience the most friction?
- What do they wish was different?
- Do they feel ownership over quality?

---

## Step 2: Evaluate key areas

### CI/CD
- [ ] Does a CI pipeline exist?
- [ ] Does it run on every PR/merge?
- [ ] Can it be bypassed?
- [ ] How long does it take to run?
- [ ] Does it block merges on failure?
- [ ] Is the pipeline currently green?

### Environments
- [ ] Are dev, staging/UAT, and production separate?
- [ ] Can features be tested without affecting production users?
- [ ] Are environments consistently configured?
- [ ] Is there a feature flag system in place?

### Local development
- [ ] Can the application be developed and run locally?
- [ ] How long does it take to set up a new developer?
- [ ] Are there dependencies on shared environments for local work?

### Code review
- [ ] Does code review happen on every PR?
- [ ] Are reviews substantive (not rubber-stamps)?
- [ ] Do reviews include manual verification of changes?
- [ ] Is there a clear review process?

### Testing
- [ ] What test layers exist? (unit, integration, E2E, manual)
- [ ] Is the test pyramid balanced?
- [ ] How long does the test suite take to run?
- [ ] Are tests trustworthy or flaky?
- [ ] Do developers run tests locally?
- [ ] Do developers write tests or is it only QA?

### Automation
- [ ] How much repetitive work is automated?
- [ ] Are deployments automated?
- [ ] Are environment setups automated?
- [ ] Is linting/formatting automated?

### Monitoring & observability
- [ ] Is there error tracking in production? (Sentry, etc.)
- [ ] Is there performance monitoring? (Datadog, etc.)
- [ ] Are there alerts for critical issues?
- [ ] Does the team review monitoring data regularly?

### Standards
- [ ] Are relevant technical standards followed? (OpenAPI, Conventional Commits, semver, etc.)
- [ ] Is there documentation for APIs?
- [ ] Are commit messages structured and meaningful?
- [ ] Is there a Git history strategy?

### Ownership & culture
- [ ] Does the team feel responsible for quality collectively?
- [ ] How does the team react to production incidents?
- [ ] Is there blame culture or learning culture?
- [ ] Do developers and QA collaborate or operate in silos?

---

## Step 3: Plan actions

Based on findings, build a plan on three horizons:

### Short term (weeks)
Quick wins and immediate pain relief. Focus on what's broken or what's causing the most friction right now.

Typical short-term actions:
- Add E2E tests for the most critical/recurring bugs
- Fix the CI pipeline if it's broken or bypassable
- Set up basic monitoring if none exists
- Fix flaky tests that are eroding trust

### Medium term (1-3 months)
Build foundations. Give the team tools and frameworks they can build on.

Typical medium-term actions:
- Set up an integration testing framework
- Implement feature flags for safer releases
- Introduce linting with the DFER approach
- Establish a code review process or improve an existing one
- Add a UAT/staging environment if missing

### Long term (3-6 months)
Structural improvements based on the feedback collected and patterns observed.

Typical long-term actions:
- Define and enforce code quality standards for critical areas
- Improve the test pyramid balance
- Establish monitoring and observability practices
- Address cultural issues (ownership, collaboration)

### Handling client priorities

If the client has explicit requests, prioritize those — but look for intersections with medium/long-term plans. Always reserve a minimum time allocation for structural improvements, even when firefighting.

---

## Step 4: Propose and discuss

Present findings and the plan. Keep it concise. For each action:

1. State what you found
2. Propose a solution
3. Ask "what do you think?"

Go deeper on reasoning only if asked. The goal is dialogue, not a lecture.
