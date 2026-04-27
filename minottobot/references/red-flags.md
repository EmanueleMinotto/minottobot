# minottobot — Red Flags & Anti-Patterns

A collection of recurring negative patterns minottobot has encountered across teams and organizations. These are the signals that something is wrong — sometimes obvious, sometimes hiding behind polite language and green dashboards.

---

## Cultural red flags

### "That's not my problem"

The single most common issue. Quality is treated as someone else's responsibility. Developers blame QA, QA blames developers, everyone blames ops. When nobody owns quality, nobody has quality.

**What it looks like:** bugs bounce between teams, nobody volunteers to investigate production issues, post-mortems turn into finger-pointing sessions.

### Blame culture during outages

When something breaks in production, the first question is "who did this?" instead of "what happened and how do we fix it?"

**What it looks like:** team members ready to blame each other during an outage. People hide mistakes. Incident reviews become trials. The result: silence replaces transparency, and hidden problems can't be improved.

### Fake collaboration

The team says they're ready to collaborate when management asks, but they never communicate voluntarily. Collaboration is performed, not practiced.

**What it looks like:** people attend meetings but don't speak up. Cross-team communication only happens through managers. Knowledge stays siloed. When asked "do you collaborate?" the answer is yes, but the Slack channels are silent.

### Pleasing the boss instead of the user

Work is oriented around making the manager happy rather than delivering value to the end user. Priorities are driven by internal politics, not user impact.

**What it looks like:** features ship because someone important asked for them, not because users need them. Quality shortcuts are taken because "the boss wants it by Friday." Nobody asks "but does the user actually need this?"

### QA tests exist but devs ignore them

QA writes automated tests, but developers don't look at them. Test failures are only noticed when QA manually reports them. The test suite is QA's problem, not the team's.

**What it looks like:** automated E2E tests fail regularly but nobody acts on it until the QA person sends a message. Developers see test failures as "QA noise" rather than "our product is broken." The test suite becomes a parallel universe that doesn't influence development decisions.

**Why it matters:** this is ownership failure in disguise. If tests exist but only one person cares about their results, they're not really part of the development process — they're a report that nobody reads.

---

## Process red flags

### No CI at all

If there's no CI pipeline, nothing else matters. You can't enforce quality without automation. Every other improvement depends on this.

**What it looks like:** developers run tests locally (maybe), code gets merged without any automated check, "it works on my machine" is a frequent phrase.

### CI that can be bypassed

Almost as bad as no CI. If the pipeline exists but people can merge without it passing, it's decoration.

**What it looks like:** "force merge" is used regularly, broken builds stay broken because "we'll fix it later," the pipeline is seen as a suggestion rather than a gate.

### Deploy by FTP

The deployment system consists of manually uploading source code via FTP (or equivalent manual process). No automation, no rollback strategy, no audit trail.

**What it looks like:** someone connects to a server, uploads files, and hopes for the best. Deployments are stressful events. Rollback means "upload the old files again." Nobody is sure what's actually running in production.

### Broken deploys left unfixed for hours or days

A deploy fails and nobody fixes it. The broken state becomes the new normal. The longer it stays broken, the harder it is to fix, and the more people accept it as "just how things are."

**What it looks like:** the deployment pipeline is red for days. People work around it. "Yeah, it's been broken since last week" is said casually. The urgency is gone.

**Why it matters:** this is a cultural signal. If a broken deploy doesn't create urgency, the team has normalized failure. And normalized failure is the enemy of improvement.

### No environment separation

No distinction between dev, staging/UAT, and production. Everything happens in one place, or changes go straight to production.

**What it looks like:** "don't deploy right now, I'm testing something." Developers test directly in production. There's no safe place to experiment.

### No code review

Code goes directly from a developer's machine to the main branch without any peer review.

**What it looks like:** PRs are merged by the author, or there's no PR process at all. Nobody reads anyone else's code. Knowledge stays in silos.

### Rubber-stamp reviews

Code review exists but it's a formality. Reviewers approve without reading. The review is a checkbox, not a conversation.

**What it looks like:** PRs are approved in under 2 minutes regardless of size. Review comments are rare. "LGTM" is the standard response to a 500-line change.

---

## Technical red flags

### Inverted or broken test pyramid

The test pyramid is completely unbalanced. Typically: heavy E2E tests that take 30+ minutes, zero integration tests, and sparse or no unit tests.

**What it looks like:** the E2E suite takes half an hour or more to run. Developers don't run tests locally because they're too slow. Integration tests are nonexistent — there's a gap between "test one function" and "test the whole application." Feedback is slow and expensive.

**Why it matters:** slow tests mean slow feedback. Slow feedback means developers stop running tests. When developers stop running tests, tests stop being trustworthy. It's a vicious cycle.

### Flaky tests that everyone ignores

Tests that sometimes pass and sometimes fail, with no one investigating why. The team has learned to "just rerun" the pipeline.

**What it looks like:** "oh, that test is flaky, just rerun it" is common. CI results are unreliable. Nobody trusts the test suite because it cries wolf constantly.

### Skipped or disabled tests with no expiry date

Tests are commented out, marked `.skip`, or excluded by config — and stay that way indefinitely. There's no ticket, no owner, no deadline to re-enable them.

**What it looks like:** `it.skip(...)` scattered across the suite, dating back months. No one remembers why a given test was disabled. The skip set grows monotonically.

**Why it matters:** an ignored test is worse than a missing test, because it creates the illusion of coverage. A boolean enabled/disabled flag with no expiry is technical debt with no due date — the equivalent of a TODO that nobody owns. A `disabledUntil` date (or equivalent ticket with deadline) forces the conversation back open.

### Quarantine without follow-up

Flaky tests are moved to a "quarantine" suite or tagged as non-blocking, then forgotten. The quarantine becomes a graveyard.

**What it looks like:** the quarantine job has been red for weeks. Nobody triages it. The tests still exist on paper but contribute zero signal.

### No framework or code organization

The repository has no architectural framework, no folder structure conventions, no patterns. Code is organized by accident.

**What it looks like:** files are scattered randomly, there's no separation of concerns, similar logic is duplicated in multiple places, a new developer wouldn't know where to put new code.

**Why it matters:** without structure, the codebase grows in entropy. Every new feature makes it harder to understand. The perceived complexity goes up, the DX goes down, and quality follows.

### No monitoring in production

The team has no visibility into what happens after deploy. Bugs are reported by users, not detected by systems.

**What it looks like:** "we find out about bugs from users" or "we didn't know it was down until a customer called." No Sentry, no Datadog, no structured logging, no alerts.

### No local development

You can't develop or test the application locally. Development requires connecting to shared environments.

**What it looks like:** "you need access to the staging database to develop." Setting up a new developer takes days. Running a feature locally is impossible or extremely painful.

### Feature flags without owner or removal condition

Feature flags accumulate in the codebase with no expiry, no owner, no documented condition for removal. What started as a release tool becomes permanent dead weight.

**What it looks like:** flags from rollouts completed a year ago still wrap branching logic. Nobody is sure if they can be deleted. The flag platform has 200+ entries and no one has reviewed them this quarter.

**Why it matters:** every flag doubles the number of code paths to test. Two flags = four states; three = eight. Without disciplined cleanup, flags become invisible combinatorial complexity. Each flag should ship with a ticket, an owner, and a removal condition — and a monthly review pass should prune the dead ones.

### Noisy Git history

The history is dominated by automated formatting commits, vague messages ("fix", "wip", "update"), or huge unrelated changes squashed together. The story of how the system evolved is unreadable.

**What it looks like:** `git log --oneline` shows dozens of "lint fix" or "format" commits per week. Commit messages don't reference tickets or intent. Bisecting a regression is hopeless.

**Why it matters:** Git history is the evolutionary memory of the system. Garbage history → garbage insight (for humans, tooling, and increasingly AI assistants). Auto-formatting belongs in pre-commit hooks or CI checks, not in commits. Conventional Commits aren't bureaucracy — they make changelogs, releases, and incident archaeology cheap.

### No technical standards followed

Relevant technical standards exist but are ignored. REST APIs without OpenAPI documentation, no commit conventions, no versioning strategy.

**What it looks like:** the API has no documentation (or documentation that's always outdated). Commit messages are random. Versions are arbitrary. Every developer has their own style.

---

## The lies teams tell themselves

These are phrases that sound reasonable but are almost always a signal of a deeper problem.

| What they say | What it usually means |
|---------------|----------------------|
| "We don't have time for tests" | Testing is seen as extra work, not as part of the work |
| "Our tests exist, we just don't run them" | The test suite is broken or untrusted and nobody wants to fix it |
| "It's tested" (but no one opened a browser) | Automated checks describe a model of the system; manual verification compares the model to reality. Both are needed |
| "We'll remove that flag eventually" | The flag has no owner, no removal ticket, and no deadline — it's now permanent |
| "It works on my machine" | There's no CI, no environment parity, or no local dev setup |
| "We'll fix the pipeline later" | The pipeline has been broken for a while and it's now normalized |
| "We do code reviews" (but PRs are approved in 2 minutes) | Code review is a ritual, not a practice |
| "We're agile" (but there's no feedback loop) | Agile is used as a label, not a method |
| "QA will catch it" | Quality is someone else's problem |
| "We collaborate well" (but only when management is watching) | Collaboration is performed, not practiced |
| "We can't slow down to improve" | The team is stuck in a reactive loop and doesn't see that the "slowdown" would make them faster |
| "That's just tech debt, we'll get to it" | Nobody has a plan to address it, and it keeps growing |
