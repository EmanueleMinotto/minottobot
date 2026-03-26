# Platform Engineering Audit Report
## Momentum Fintech — Platform Team
**Audit Date:** 2026-03-26
**Classification:** Internal Assessment

---

## Executive Summary

The Momentum Fintech Platform team is operating in a state of significant organisational and technical risk. Across every dimension assessed — team stability, testing confidence, deployment safety, incident management, code quality, and governance — the team shows compounding weaknesses that individually would each warrant remediation, but together represent a systemic threat to platform reliability and business continuity.

**Overall Risk Rating: HIGH**

The most urgent concerns are: an unresolved major outage now six months old, dual CI systems with no authoritative deployment pipeline, a test suite of unknown validity, and a lack of stable engineering leadership or product ownership. These issues are not independent; they reinforce each other and make safe delivery increasingly difficult.

---

## Assessment Dimensions

### 1. Team Capacity and Stability

**Risk: HIGH**

| Metric | Status |
|---|---|
| Nominal headcount | 11 engineers |
| Effective headcount | 7 engineers |
| Leadership stability (18 months) | 3 VPs of Engineering |
| Product ownership | None currently assigned |

**Findings:**

- **36% capacity reduction** is not a temporary strain — at this level, it fundamentally changes what the team can safely take on. With 4 engineers on loan, the remaining 7 are almost certainly covering their responsibilities in addition to their own.
- **Three VPs of Engineering in 18 months** is a severe indicator of organisational instability. This level of churn at the leadership level means that priorities, standards, and architectural direction have changed repeatedly. Engineers are unlikely to have consistent guidance or a stable vision to work toward, which corrodes morale and decision-making quality.
- **No product owner** means the team has no clear external advocate for prioritisation. In practice, this often results in reactive work (responding to incidents and urgent requests) dominating over planned improvements — which is consistent with the "urgent" bypass pattern described in the code review findings.
- The combination of leadership churn and reduced capacity creates a **knowledge concentration risk**: institutional knowledge is held by fewer people, and those people are at elevated risk of burnout and attrition.

**Recommendations:**

1. Conduct an explicit capacity audit: map current commitments against the 7 active engineers and identify what is being deferred or dropped.
2. Establish a temporary product owner or tech lead as a single point of accountability until a permanent product owner is assigned.
3. Negotiate a return timeline for the 4 loaned engineers, or formally reduce the team's committed scope.

---

### 2. Test Suite Health

**Risk: HIGH**

| Metric | Status |
|---|---|
| Total tests | ~800 |
| Last known run | ~2 months ago |
| Current pass rate | Unknown |

**Findings:**

- A test suite that has not been run in two months provides **zero confidence** in the state of the codebase. It is functionally equivalent to having no tests, because no one knows whether it validates anything currently.
- The lack of regular test execution suggests CI is not enforcing test runs on every commit or PR, or that CI results are being ignored. Either scenario is dangerous.
- With a mixed PHP/Laravel and Node.js codebase and no confirmed passing tests, any deployment carries unknown risk. The team cannot safely assess the blast radius of any given change.
- 800 tests is a meaningful investment of engineering time. The fact that they are not being run is a waste of that investment and will become a liability if the suite is found to be substantially broken — fixing 2 months of divergence is expensive.

**Recommendations:**

1. Immediately run the full test suite and document current pass/fail state. Treat this as a discovery exercise, not a failure.
2. Triage failures: categorise as (a) tests broken due to code changes, (b) tests that were already failing before the gap, (c) flaky tests.
3. Establish a policy that CI blocks merges on test failure, with no exceptions. The "urgent" bypass culture must not extend to test gates.
4. Assign one engineer for one sprint to restore the suite to a known-passing state.

---

### 3. CI/CD Pipeline

**Risk: HIGH**

| Metric | Status |
|---|---|
| CI systems | 2 (CircleCI + GitHub Actions) |
| Authoritative deployment pipeline | Unknown |
| Last deployment | ~3 weeks ago |
| Deployment frequency | Irregular |

**Findings:**

- **Dual CI systems with no clear authority** is one of the most operationally dangerous configurations a team can be in. It creates ambiguity about which pipeline's results matter, which one gates deployments, and which one is monitoring production. During an incident, this ambiguity becomes critical.
- The fact that no one knows which system is authoritative suggests that both may be partially configured and that deployments may be happening through ad hoc means — or that the team has quietly defaulted to one system without formalising it.
- Irregular deployment frequency (last deploy 3 weeks ago) indicates the team is not practicing continuous delivery. Infrequent deployments mean larger change sets per deploy, which means higher risk per deployment and longer blast radius when something goes wrong.
- The combination of infrequent deploys and unknown test validity means each deployment is a high-stakes event with limited safety mechanisms.

**Recommendations:**

1. Immediately designate one CI system as authoritative. Audit what each system currently does, then migrate everything to the chosen system. Decommission the other.
2. Document the deployment process end-to-end, including who has production access, how deployments are triggered, and what automated checks run.
3. Aim to increase deployment frequency — small, frequent deploys reduce per-deploy risk. Start with a goal of at least weekly deploys once the test suite is restored.
4. Add a deployment checklist (automated where possible) that includes: test pass confirmation, change log, rollback plan, monitoring alert review.

---

### 4. Incident Management

**Risk: CRITICAL**

| Metric | Status |
|---|---|
| Formal incident tracking | None |
| Major outages (last 6 months) | 1 (unresolved) |
| Post-incident reviews | Unknown/unlikely |

**Findings:**

- An unresolved major outage from **six months ago** is the single most alarming finding in this audit. An outage that remains unresolved after six months is not an incident — it is a chronic system failure. It means customers or internal users are operating on a degraded platform indefinitely, with no committed resolution.
- The absence of formal incident tracking means there is no record of what has failed, how often, how long resolution took, or what remediation was attempted. This makes trend analysis impossible and creates a false impression of system stability.
- Without post-incident reviews, the team cannot learn from failures, which means the same failures will recur. This is consistent with having a 6-month-old unresolved outage.
- The combination of no incident tracking and unstable engineering leadership means that institutional knowledge about what has gone wrong lives only in individual engineers' memory — and when those engineers leave, the context leaves with them.

**Recommendations:**

1. **Escalate the unresolved outage immediately.** Assign an owner, define the full scope of what remains broken, and set a concrete remediation deadline. This is non-negotiable.
2. Adopt a minimal incident tracking process today — even a shared spreadsheet or simple Jira board is better than nothing. Track: date, description, severity, resolution status, owner.
3. Conduct a retrospective on the 6-month-old outage, even now. The goal is to understand why it was not resolved and what systemic conditions allowed that to persist.
4. Establish a lightweight post-incident review template. All P1/P2 incidents should produce a written summary within 5 business days of resolution.

---

### 5. Code Review and Quality Gates

**Risk: HIGH**

| Metric | Status |
|---|---|
| Code review policy | Required (officially) |
| Code review in practice | Frequently skipped ("urgent") |
| Merge gates (test, lint, etc.) | Unclear |

**Findings:**

- A code review policy that is "frequently skipped" is worse than no policy in some respects — it creates an illusion of a safety gate while providing none of the protection. Engineers who believe code is reviewed may be less vigilant about their own changes.
- The "urgent" justification is a classic anti-pattern. In dysfunctional teams, the definition of "urgent" expands over time until almost everything qualifies. With no product owner enforcing prioritisation and 3 VPs in 18 months creating repeated context switches, urgency signals are likely distorted and unreliable.
- Skipping code review in a fintech platform is particularly high-risk. Financial logic bugs, security vulnerabilities, and compliance issues are all more likely to reach production without review.
- The absence of review also compounds the knowledge concentration problem: if code isn't reviewed, fewer engineers understand each area of the codebase.

**Recommendations:**

1. Enforce code review via branch protection rules at the GitHub level — make it technically impossible to merge without at least one approval. Remove the human discretion to skip.
2. Define "urgent" formally: what criteria must be met, who can invoke it, and what compensating controls apply (e.g., immediate post-merge review within 24 hours).
3. Treat bypass events as incidents: log them, review them in retrospectives, and track the trend.

---

### 6. Technology Stack

**Risk: MEDIUM**

| Component | Status |
|---|---|
| Original backend | PHP + Laravel |
| Newer services | Node.js microservices |
| Database | MySQL |

**Findings:**

- The coexistence of PHP/Laravel and Node.js microservices is common in evolving platforms, but it introduces **operational and cognitive overhead**: two runtimes, two deployment patterns, two dependency management ecosystems, potentially two monitoring configurations, and a team that must be proficient in both.
- With a reduced effective team (7 engineers), this overhead is proportionally more costly. Context switching between PHP and Node.js increases cognitive load and slows onboarding of new engineers.
- Without a clear architectural roadmap (which would typically come from stable VP-level leadership), it is unclear whether the intent is to migrate fully to Node.js, maintain both permanently, or adopt another direction. Each option has different implications for the team.
- MySQL is a stable and appropriate choice for a fintech platform. No immediate concerns, but data migration practices, schema versioning, and backup/recovery procedures should be audited separately.

**Recommendations:**

1. Document the intended long-term architecture explicitly. Even a one-page decision record stating the intent for the PHP/Node coexistence would reduce ambiguity.
2. Ensure both stacks have equivalent CI, monitoring, and alerting coverage — it is common for the "older" stack to have less investment in these areas once migration begins.
3. Audit the boundary between PHP and Node.js services: how do they communicate, what are the failure modes, and are those failure modes tested?

---

## Risk Summary Matrix

| Dimension | Risk Level | Primary Driver |
|---|---|---|
| Team Capacity & Stability | HIGH | Leadership churn, 36% capacity reduction, no product owner |
| Test Suite Health | HIGH | 2 months without execution, unknown pass rate |
| CI/CD Pipeline | HIGH | Dual systems, no authoritative pipeline, irregular deploys |
| Incident Management | CRITICAL | 6-month unresolved outage, no formal tracking |
| Code Review & Quality Gates | HIGH | Policy routinely bypassed, no enforcement mechanism |
| Technology Stack | MEDIUM | Dual-stack complexity with reduced team capacity |

---

## Prioritised Action Plan

### Immediate (This Week)

1. **Escalate and assign an owner to the 6-month unresolved outage.** Define the remaining scope and set a deadline. This is the single highest-priority action.
2. **Run the test suite.** Document which tests pass, which fail, and which are skipped. Share results with the team.
3. **Designate one CI system as authoritative.** Communicate this to the team. Stop accepting the ambiguity.

### Short-Term (Next 2–4 Weeks)

4. Restore the test suite to a known-passing baseline. Assign ownership.
5. Implement GitHub branch protection rules to enforce code review. No exceptions path without a documented compensating control.
6. Establish minimal incident tracking. Even a simple log is a significant improvement over nothing.
7. Document the deployment process end-to-end.

### Medium-Term (Next 1–3 Months)

8. Conduct a capacity planning exercise with the 7 active engineers. Renegotiate scope if necessary.
9. Establish a post-incident review process and run a retrospective on the major outage.
10. Increase deployment frequency. Target weekly cadence within 2 months.
11. Document the architectural intent for the PHP/Node.js stack boundary.
12. Assign (even interim) product ownership to the team.

### Longer-Term (3–6 Months)

13. Evaluate and formalise the path for the loaned engineers — return, backfill, or scope reduction.
14. Stabilise engineering leadership. The recurring VP churn must be addressed at an organisational level.
15. Conduct a full security and compliance audit of the platform, given the fintech context and the gaps identified in code review and incident management.

---

## Closing Assessment

This team is not failing through lack of competence or effort. The pattern described — policy bypasses, deferred incidents, CI ambiguity, test neglect — is the signature of a team that has been asked to do too much with too little stability for too long. Three VPs in 18 months, a 36% reduction in active headcount, and an unresolved major outage are not team-level problems. They are organisational problems that must be acknowledged at the leadership level.

The recommended actions above are achievable, but they require two things that are currently absent: a stable point of accountability within the team, and organisational commitment to not adding new scope until the foundational risks are addressed. Without those two preconditions, the recommendations will remain aspirational.

**The single most important message from this audit: the 6-month unresolved outage must be resolved before any new feature work begins.** Running a fintech platform with a known, unresolved major outage is an operational and reputational liability that no amount of new delivery will offset.
