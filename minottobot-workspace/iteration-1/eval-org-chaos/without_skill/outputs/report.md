## Engineering Quality Assessment — Momentum Fintech Platform Team

---

### Overall Situation Summary

This team is in a high-risk state. The combination of leadership instability (3 VPs in 18 months), an unresolved major incident, split ownership across two CI systems, and an untested test suite constitutes compounding technical and organizational debt. The risks are not hypothetical — the conditions described are a reliable precursor to a serious production failure or a key-person departure that triggers a crisis. The positive framing is that all of these are fixable with deliberate sequencing.

---

### Area Scores (1–5)

| Area | Score | Rationale |
|---|---|---|
| Test Coverage & Health | 1.5 / 5 | ~800 tests exist but have not been run in 2 months. Unknown pass rate means the suite provides no actual safety signal. |
| CI/CD Pipeline | 1.5 / 5 | Two CI systems with no clear authority for deployments is worse than one bad system. It creates false confidence and unpredictable behavior. |
| Deployment Practice | 2 / 5 | Irregular cadence and a 3-week gap indicate deployments are treated as events rather than a routine. This increases batch size and therefore risk per deploy. |
| Incident Management | 1 / 5 | No formal tracking, a 6-month-old unresolved major outage, and no post-mortem culture documented. This is the single most dangerous area. |
| Code Review Culture | 2 / 5 | A policy that is routinely bypassed under "urgency" is effectively no policy. The bypass pattern itself signals deeper prioritization problems. |
| Team Stability & Ownership | 1.5 / 5 | 4 of 11 engineers on loan, no product owner, 3 engineering VPs in 18 months. There is no stable decision-making authority. |
| Stack Coherence | 2.5 / 5 | PHP/Laravel + Node.js microservices is a common hybrid but adds cognitive overhead with a reduced team. MySQL is a stable anchor. |

**Composite Score: 1.7 / 5**

---

### Recommendations by Priority

---

#### Priority 1 — Stabilize the Foundation (Weeks 1–2)

These are not improvements. They are damage control. Nothing else in this list is trustworthy until these are addressed.

**1.1 — Designate one authoritative CI system.**
Pick either CircleCI or GitHub Actions. Do not optimize this choice — just make it and document it. Audit which system is currently triggering actual deployments (check webhook configurations in both, compare to recent deployment timestamps). The other system must be disabled or clearly labeled as non-authoritative. Running two systems in ambiguous parallel is a deployment integrity risk: you do not know with certainty what code is running in production.

**1.2 — Run the test suite immediately and record the result.**
You need a baseline. Run the full suite today and capture: total tests, pass count, fail count, error count. Do not fix failures yet — just establish the number. A test suite with an unknown pass rate is not an asset; it is a liability that creates false confidence. The output of this run becomes your starting measurement.

**1.3 — Document the unresolved major outage in writing.**
Six months without a documented resolution means institutional knowledge of what happened exists only in people's heads, and those people may leave. Assign one engineer 2–3 hours to write a plain-text incident summary: what failed, what the current state is, what is blocking full resolution. This is not a formal post-mortem yet — it is a knowledge preservation step.

---

#### Priority 2 — Restore Operational Hygiene (Weeks 2–6)

**2.1 — Establish a lightweight incident tracking process.**
You do not need a sophisticated tool. A shared document or a dedicated Slack channel with a structured template (date, severity, description, current status, owner) is sufficient to start. The goal is that every incident — past and future — has a written record with an owner. Retroactively log the 6-month-old outage as the first entry.

**2.2 — Harden the code review policy with a realistic bypass rule.**
"Urgency" bypasses will always happen in fintech. The current problem is that the bypass has no cost and no audit trail. The fix is not to eliminate bypasses but to require: (a) a second engineer explicitly approves the bypass in writing (a Slack message or PR comment), and (b) a follow-up review ticket is created within 24 hours. This converts an invisible pattern into a visible, trackable one. High bypass rates then become a measurable signal that something else is wrong with workload or prioritization.

**2.3 — Triage failing tests into three buckets.**
After running the suite (1.2), sort failures into: (a) tests that are broken due to environment/configuration issues — fix these first, they are cheap wins; (b) tests covering functionality that no longer exists — delete them; (c) tests exposing real bugs — these become a prioritized backlog. Do not attempt to fix everything at once. The goal is a green baseline suite, even if that suite is smaller than 800.

**2.4 — Set a deployment rhythm target.**
With 7 active engineers on a fintech platform, a reasonable near-term target is one deployment per week, with a defined rollback procedure. The specific frequency is less important than the fact that it is scheduled and expected rather than event-driven. Weekly deploys force smaller batch sizes and reduce the fear that accumulates around infrequent ones.

---

#### Priority 3 — Build Toward Sustainability (Weeks 6–16)

**3.1 — Formally resolve the unresolved outage.**
Using the documented summary from 1.3, schedule the work needed to fully close this incident. An unresolved major outage in fintech is a regulatory and reputational risk, not just a technical one. It also degrades team morale — engineers know it is still there. Assign a dedicated owner and a target close date.

**3.2 — Establish a minimum test coverage gate on the CI pipeline.**
Once the test suite is green (or close to it), configure the authoritative CI system to fail a build if coverage drops below the current baseline. This is a floor, not a ceiling. It prevents regression without requiring a big-bang coverage improvement effort.

**3.3 — Define team ownership while engineers are on loan.**
With 4 engineers on loan, there is a risk that they return to a codebase that has drifted significantly from what they knew. Maintain a short weekly written update (not a meeting — a document) summarizing what changed, what decisions were made, and what is blocked. This reduces re-onboarding cost when they return and forces the active 7 to articulate their decisions.

**3.4 — Advocate for a product owner assignment.**
This is outside engineering's direct control, but the absence of a product owner means the team cannot prioritize confidently. Technical debt work, incident resolution, and feature work are all competing without a clear external signal on business value. The engineering lead (whoever currently holds that role) should escalate this gap to leadership with a concrete description of the prioritization paralysis it causes.

---

### Structural Observations

**On leadership instability:** Three VPs in 18 months means engineering strategy has reset at least twice. The symptom of this in the codebase is the dual CI setup — each new leader brought a preference and no one cleaned up the previous one. Before implementing any of the above recommendations, identify who currently has the authority to make and sustain these decisions. If that person is not stable, the recommendations will not stick.

**On the PHP/Node split:** This is a genuine long-term cost but is not the priority right now. The team is too small and too unstable to take on a consolidation effort. Document the boundary between the two systems clearly so the 7 active engineers all share the same mental model of what lives where.

**On the fintech context:** Irregular deployments, no incident tracking, and bypassed code review are not just engineering quality issues in a financial services company — they are the conditions under which compliance and audit obligations become difficult to meet. If Momentum Fintech is subject to SOC 2, PCI-DSS, or similar frameworks, the current state of code review bypass and deployment ambiguity should be flagged to whoever owns compliance, not just to engineering leadership.

---

### Summary of Immediate Actions (Next 5 Business Days)

1. Run the test suite. Record the number.
2. Identify which CI system triggered the last 3 deployments. Designate that one as authoritative.
3. Write a plain-text summary of the unresolved major outage. Assign an owner.
4. Create an incident log with that outage as entry #1.
5. Identify who currently holds engineering decision authority and confirm they are aware of this assessment.

None of these require budget, new tooling, or returning the loaned engineers. They require time and will.
