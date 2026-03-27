## FinanceCore Ltd — Phase 0 Assessment Summary

Here's my read of where you stand and what the data is telling you.

---

### What's Working

- You have tests. 12,000 tests is a real asset — most organizations this age have far fewer.
- You have a code review policy. Enforcement is inconsistent, but the norm exists.
- A central QA guild provides some institutional knowledge and a place to anchor quality initiatives.
- Microservices architecture suggests *some* modernization has already happened.

---

### The Real Problems (Ranked by Impact)

**1. Flaky tests are your most urgent technical debt**

30% flakiness (roughly 3,600 tests) means your test suite is actively harmful. Engineers learn to ignore red builds, which destroys the value of every test — including the reliable ones. This is a cultural and technical spiral: flaky tests → ignored tests → uncaught regressions → incidents.

**2. Your CI/CD pipeline is a bottleneck and a risk**

A 47-minute build on a 2011 Jenkins setup is a compounding problem. It slows feedback loops, discourages small commits, and encourages batching — which directly causes your 6-hour biweekly deployments. The "CI team" as a separate entity also means product teams don't own their pipelines, creating a dependency that slows improvement.

**3. Biweekly deploys + 6-hour manual process = systemic fragility**

Infrequent large deployments are a root cause of both P1/P2 incidents and long MTTR. When you deploy rarely, each deployment carries enormous change volume and risk. The manual sign-off process suggests a lack of confidence in automated gates — which circles back to the flaky tests.

**4. Hotfix culture is quietly eroding your code review policy**

"Some teams skip it for hotfixes" is how policies die. Hotfixes are also when the code is most risky and review is most valuable. This is a governance issue, not just a process one.

**5. Oracle DB is likely a long-term constraint**

Not an immediate crisis, but in a microservices architecture, a shared Oracle instance creates tight coupling, schema migration risk, and a scaling ceiling. Worth flagging for a longer horizon.

---

### Key Metrics Baseline (for tracking improvement)

| Metric | Current |
|---|---|
| Deployment frequency | ~2x/month |
| Lead time for changes | Estimated 2–3 weeks |
| Change failure rate | Unknown — recommend instrumenting |
| MTTR | ~4 hours |
| Build duration | 47 minutes |
| Test flakiness rate | ~30% |

---

### Recommended Phase 1 Focus Areas

Given your context (financial services, regulated environment, 85 engineers), I'd prioritize in this order:

1. **Quarantine flaky tests immediately.** Tag them, move them to a separate non-blocking suite, and assign ownership. Don't delete them — fix or replace them. Goal: get your main suite to near-zero flakiness within 90 days.

2. **Instrument change failure rate and deployment frequency properly.** You can't improve what you don't measure. These two DORA metrics will tell you more than almost anything else.

3. **Run a blameless post-mortem on your last 3 P1s.** Look for whether any were caused by a large batch deploy. The answer is almost certainly yes, and that data will build the case for more frequent, smaller deployments.

4. **Define what a "hotfix" actually is.** Write it down. Make the exception process explicit (e.g., 1 reviewer instead of 3, but never zero) rather than leaving it as an informal norm.

5. **Start the Jenkins conversation.** You don't have to replace it immediately, but the CI team should be building a migration case. GitHub Actions or a modern alternative will pay back quickly in build time and team autonomy.

---

### One Honest Observation

FinanceCore's profile — 20-year-old financial services company, central CI team, manual deployment sign-offs, quarterly release mindset baked into a biweekly window — suggests the *organizational* structure will be the harder problem than the *technical* one. The engineering work is well-understood. Getting leadership to accept that faster, smaller deployments are *safer* (not riskier) in financial services will require evidence and trust-building, not just tooling changes.

What would you like to dig into first?
