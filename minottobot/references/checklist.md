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

## Step 3: Identify patterns

Look for clusters, not isolated issues. A single problem is a problem to fix. Multiple problems in the same area reveal a systemic pattern.

- Cultural flags cluster → ownership and trust problem → address team dynamics before touching tools
- Process flags cluster → workflow maturity problem → start with CI and environment setup
- Technical flags cluster → DX problem → start with the highest-friction pain point

Always prioritize the highest-impact problem. If there's no CI, don't talk about test strategy. Fix the foundation first.

---

## Step 4: Hand off to strategy

Once the audit findings are clear, move to the strategy phase to build the improvement plan. The strategy phase is always the next step — not optional.
