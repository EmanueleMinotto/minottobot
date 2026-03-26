# Minottobot audit report — Momentum Fintech, Platform team — 2026-03-26

## Repos in scope
- Platform (PHP + Laravel, Node.js microservices, MySQL)

> ⚠️ **No code access** — this audit is based on team-reported data only. Findings could not be verified against the codebase.

---

## Phase 0 — Quantitative baseline

| # | Question | Answer | Finding? |
|---|----------|--------|----------|
| 1 | Team size | 11 on paper, 7 actively on platform (4 on loan) | Effective capacity is fragmented — 36% of the team is unavailable |
| 2 | Total tests | ~800, not run in ~2 months | Pass rate unknown — test suite is in an unverified state |
| 3 | CI run time | Unknown | 🚨 Finding: nobody is monitoring CI performance |
| 4 | Deployment frequency | Irregular — last deploy 3 weeks ago | Effectively stalled |
| 5 | CI success rate | Unknown — two systems (CircleCI + GitHub Actions), authority unclear | 🚨 Finding: no single source of truth for CI |
| 6 | MTTR | Not tracked — major outage 6 months ago still unresolved | 🚨 Critical: active production incident with no resolution |
| 7 | Test coverage | Not tracked | Finding: no coverage baseline |
| 8 | Skipped/disabled tests | Unknown | Finding: no visibility into test suite health |
| 9 | Days since last incident | N/A — ongoing unresolved outage | 🚨 Critical: production is not fully healthy |
| 10 | Open bugs >30 days | Not tracked | Finding: no bug visibility |

**Gap count: 7 of 10 data points are unknown or untracked.** This alone is one of the most significant findings — a team that cannot measure itself cannot improve.

---

## Executive summary (3 bullets max, each under 20 words)

- Unresolved 6-month outage, unknown CI authority, and untested suite signal systemic process collapse.
- Effective team capacity is fragmented; leadership instability (3 VPs in 18 months) has eroded ownership culture.
- No measurement baseline exists — the team cannot currently distinguish improvement from deterioration.

---

## Area scores (1 = critical · 5 = excellent)

| Area                    | Score | One-line finding                                      |
|-------------------------|-------|-------------------------------------------------------|
| 🔴 CI/CD                |  1/5  | Two CI systems, no authority, status unknown          |
| 🔴 Testing              |  1/5  | 800 tests unrun for 2 months, health unknown          |
| 🔴 Code review          |  2/5  | Required in policy, routinely skipped under urgency   |
| 🔴 Monitoring           |  1/5  | No incident tracking; active outage unresolved        |
| 🔴 Developer Experience |  2/5  | No product owner, fractured team, stalled deploys     |
| 🔴 Ownership & culture  |  1/5  | 3 VPs in 18 months, no PO, urgency bypasses process   |

> 🔴 1–2 critical/gap · 🟡 3 functional · 🟢 4–5 good/excellent

---

## Top 3 blockers right now

1. 🚨 **Unresolved production outage** — a major incident from 6 months ago is still not fully resolved; this is the most urgent threat to users and team credibility.
2. 🚨 **Dual CI with no authority** — CircleCI and GitHub Actions coexist with no agreed deployment source of truth; every deploy carries undefined risk and nobody knows what is actually enforced.
3. ⚠️ **Untested test suite** — ~800 tests haven't been run in ~2 months; the pass rate is unknown, meaning CI (whichever system) cannot be trusted to gate quality even if it were unified.

---

## Phase 1 — Audit findings

### CI/CD

- **CircleCI** was the original system; **GitHub Actions** was added 6 months ago. Neither has been formally designated as the deployment authority. Both likely run, neither is reliably enforced.
- Deployment frequency is effectively stalled — 3 weeks since last deploy is a symptom of CI distrust and/or coordination failure, not a calendar choice.
- There is no evidence of automated deployment gates (CI success required to deploy).
- Code review bypasses under "urgency" compound the risk: code may be merged without CI validation or peer review.

**Red flags triggered:** CI that can be bypassed (de facto, because authority is unclear) · Broken deploys left unfixed (implicit, given 2-month test silence) · Process red flag: dual CI is "two competing CI systems" — the team has normalized operational ambiguity.

### Testing

- ~800 tests exist but have not been run in approximately 2 months. The team does not know how many pass.
- The statement "our tests exist, we just don't run them" maps directly to the anti-pattern: *the test suite is broken or untrusted and nobody wants to fix it.*
- No coverage tracking means there is no baseline from which to measure regression.
- No information on test type breakdown (unit/integration/E2E) — the pyramid shape is unknown, but the trust level is effectively zero.

**Red flags triggered:** "Our tests exist, we just don't run them" · Inverted/broken test pyramid (potential — cannot verify) · Flaky tests that everyone ignores (possible — no evidence of active maintenance).

### Code review

- Code review is officially required — a policy exists.
- In practice it is skipped "whenever something is urgent" — and urgent is the default state.
- This is rubber-stamp review at best, and no review at worst, depending on the PR.
- Without a product owner to triage priority, "urgent" becomes the justification for every shortcut.

**Red flags triggered:** Rubber-stamp reviews · "We do code reviews" (but with a known bypass).

### Monitoring & observability

- Incidents are not formally tracked. The team does not know how many bugs are older than 30 days.
- A major production outage occurred 6 months ago and remains partially unresolved. Six months without resolution suggests either: no observability to diagnose the root cause, or organizational inability to act on findings.
- Without monitoring, the team finds out about bugs from users — Shift Right is absent.

**Red flags triggered:** No monitoring in production · No incident tracking · Bugs reported by users rather than detected by systems.

### Developer Experience

- Effective team size is 7 out of 11, with 4 on loan. There is no product owner. Three VPs of Engineering in 18 months means no sustained leadership direction.
- The stack is a hybrid: PHP + Laravel (original) and Node.js microservices (newer). This bifurcation may mean different CI configurations, test frameworks, and standards for each layer.
- No deployment in 3 weeks, an active outage, and untested tests all compound developer friction.
- The team cannot easily tell whether things are better or worse than 3 months ago — no measurement baseline exists.

### Ownership & culture

- 3 VPs of Engineering in 18 months is a leadership churn rate that actively prevents culture formation. Each VP likely reset direction; accumulated context was lost each time.
- No product owner means no one is accountable for prioritization — "urgent" becomes whatever is loudest.
- Formal processes (code review, CI) exist on paper but are bypassed under pressure — a classic sign that the team does not feel ownership of quality as a shared value.
- Incident response is informal and untracked — there is no post-mortem culture, no MTTR baseline.

**Red flags triggered:** "That's not my problem" (implicit — process bypasses) · Pleasing the boss instead of the user (likely, given leadership instability) · Blame vs learning culture (unknown, but untracked incidents suggest no structured retrospection).

### Pattern identification (checklist Step 3)

All three flag clusters are active simultaneously:

- **Cultural flags** (leadership instability, no PO, process bypasses under urgency) → ownership and trust problem
- **Process flags** (dual CI, unrun tests, no incident tracking, stalled deploys) → workflow maturity problem
- **Technical flags** (unknown test health, no coverage, no monitoring) → DX problem

This is not a "pick one" situation. However, the skill's guidance is clear: **always prioritize the highest-impact problem.** The active production outage is the immediate threat. The CI authority problem is the structural root of deploy stall. The cultural problem is the reason neither has been resolved in months.

---

## Improvement plan

### ⚡ Short term (this sprint)

- **Resolve or formally triage the active production outage.** Assign a named owner, define "fully resolved" criteria, and set a deadline. Six months without resolution is no longer a technical problem — it is a coordination and ownership failure.
- **Designate GitHub Actions as the single CI authority for deployments** and disable or archive CircleCI build triggers. Two CI systems with no authority is a liability in every deploy. Pick one (GitHub Actions is the current-generation tool), document the decision, inform the team.
- **Run the full test suite once** (against a non-production environment if possible) and record how many tests pass. This gives you a baseline. Even if the number is low, you now have a measurement point.
- **Freeze code review bypasses for non-hotfix work.** Define a narrow hotfix process with a post-merge review obligation. "Urgent" is not a review exemption.

### ◆ Medium term (this quarter)

- **Establish incident tracking** — even a lightweight process (a shared document, a Jira label, a Slack channel) is better than nothing. Log every production event with: time detected, time resolved, root cause, action item. This creates the MTTR baseline you currently lack.
- **Triage and repair the test suite.** With a baseline pass rate in hand: fix failing tests, delete or skip tests that cannot be fixed in a sprint, and re-run CI on every PR. Do not demand 100% — demand a stable and known number.
- **Resolve the PHP + Laravel vs Node.js CI split.** Ensure both layers have unified CI coverage under GitHub Actions. Different codebases should have the same enforcement standards even if they use different test runners.
- **Introduce basic production observability.** At minimum: error tracking (Sentry is the community standard for both PHP and Node.js) and structured logging. A team with an unresolved 6-month outage needs eyes on production before attempting further improvements.
- **Apply the DFER loop to code standards.** Introduce linting rules as `warn` for the most critical violations (in PHP: PHP_CodeSniffer or PHP-CS-Fixer; in Node.js: ESLint). Freeze the warning count in CI and lower it incrementally.

### ◎ Long term (this half)

- **Rebuild team ownership culture.** This requires leadership stability above all else — no process fix survives another VP rotation. Whichever leader is in place now needs to make explicit commitments: quality is a team responsibility, urgency is not a bypass, every incident gets a blameless post-mortem.
- **Get a product owner assigned.** Without prioritization ownership, urgency defaults to "whoever is loudest." A PO creates the buffer that lets the team say no to shortcuts.
- **Balance the test pyramid.** Once the suite is running and passing, analyze the breakdown. If the team has ~800 tests and no integration layer, fill that gap. Integration tests for the PHP + Laravel application and contract tests between the Node.js microservices are the most impactful additions.
- **Introduce feature flags for deploys.** Once CI is unified and stable, separating deploy from release via feature flags will reduce deploy anxiety and restore deployment frequency. The 3-week gap between deploys is partly fear — feature flags reduce the blast radius of each release.
- **Adopt Conventional Commits across both codebases.** Git history is currently of unknown quality; standardizing it now, while the team is smaller than it should be, is the right time. It enables future automated changelogs and regression tracing.

---

## Action items

| ID | Description | Horizon | Owner | Status |
|----|-------------|---------|-------|--------|
| A1 | Assign owner and define resolution criteria for the active production outage | ⚡ short | | ○ open |
| A2 | Designate GitHub Actions as sole CI authority; disable CircleCI deployment triggers | ⚡ short | | ○ open |
| A3 | Run the full test suite and record baseline pass rate | ⚡ short | | ○ open |
| A4 | Define and communicate the hotfix-only code review bypass policy | ⚡ short | | ○ open |
| A5 | Stand up lightweight incident tracking (log: time, resolution, root cause, action item) | ◆ medium | | ○ open |
| A6 | Triage failing tests: fix, skip with ticket, or delete — restore CI gate on every PR | ◆ medium | | ○ open |
| A7 | Unify CI coverage for PHP + Laravel and Node.js layers under GitHub Actions | ◆ medium | | ○ open |
| A8 | Add error tracking (Sentry) to production for both PHP and Node.js services | ◆ medium | | ○ open |
| A9 | Introduce linting rules as `warn` and freeze warning count in CI (DFER phase 1) | ◆ medium | | ○ open |
| A10 | Secure leadership commitment to blameless post-mortems and no-bypass code review | ◎ long | | ○ open |
| A11 | Get a product owner formally assigned to the Platform team | ◎ long | | ○ open |
| A12 | Analyze test pyramid breakdown and fill integration/contract testing gap | ◎ long | | ○ open |
| A13 | Implement feature flags to decouple deploy from release | ◎ long | | ○ open |
| A14 | Adopt Conventional Commits across PHP and Node.js codebases | ◎ long | | ○ open |
