This is a genuinely difficult situation, and it's worth being direct about what you're actually dealing with before jumping to solutions.

## What you're actually describing

This isn't just "messy" — this is a platform in organizational distress. The technical problems are secondary symptoms. The root causes are:

**Organizational instability** — 3 VPs in 18 months means strategy has reset multiple times. No product owner means no one is making prioritization calls. The "borrowed" engineers signal the platform isn't being protected. These aren't things you can fix with a better sprint process.

**Loss of trust in the system** — CI drift (two systems, nobody knows which is authoritative), tests nobody runs, code review being skipped "often" — these are all the same pattern. People stopped trusting the guardrails, so they stopped using them. The guardrails then atrophied further.

**An unresolved major incident** — six months old and still not fully resolved is a significant fact. That's not a backlog item; that's an open wound. It likely explains some of the workarounds and "urgent" bypasses.

---

## Practical Phase 0 priorities (given the reality)

### 1. Establish ground truth before doing anything else

Don't plan around assumptions. Before week 2:

- Run the test suite. Find out the actual pass rate. 800 tests with 40% passing is a very different situation than 80% passing.
- Determine which CI system actually deploys. Read the configs, trace the last deployment, talk to whoever set up GHA. Pick one and document it. The other one should be disabled or clearly marked as non-authoritative — two CI systems is worse than one bad one.
- Map the unresolved incident properly. What is still broken? What workarounds exist? Who knows about them?

### 2. Don't try to fix everything at once

With 7 effective engineers, no product owner, and leadership instability, you have limited organizational energy. Spreading it across "fix CI + fix tests + fix code review + resolve incident" simultaneously will get you nowhere.

Pick one constraint to close first. The CI ambiguity is probably the most dangerous — you don't actually know what you're deploying or when. That's a fintech compliance and reliability risk, not just a process annoyance.

### 3. Code review enforcement needs a structural fix, not a culture nudge

"Officially required but skipped when urgent" is not a discipline problem — it's a design problem. If urgent work can bypass review, review isn't actually required. Options:

- Branch protection rules that physically prevent merges without approval (GitHub makes this easy)
- Define what "urgent" actually means and create a documented exception process with a post-merge review obligation
- Without a product owner, decide who has authority to call something urgent

### 4. Be honest about the team's capacity

7 engineers on a PHP/Laravel + Node.js + MySQL platform with dual CI, ~800 untested tests, and an open major incident is under-resourced for improvement work while maintaining the platform. Any improvement plan needs to account for actual bandwidth, not theoretical bandwidth.

---

## What I'd want to know before going further

- What does "not fully resolved" mean for the 6-month incident? Is the platform currently degraded in some way users experience?
- Is there any executive awareness of the CI ambiguity and the untested test suite, or is this only visible at the team level?
- What's driving the deployment irregularity — is it fear, process, or just lack of demand?
- Who on the team has the institutional memory? (Often one or two people; they're your real risk and your real asset.)

The goal of Phase 0 should be to produce an honest picture of where you actually are — not a reassuring one. That picture is what makes a credible Phase 1 possible.
