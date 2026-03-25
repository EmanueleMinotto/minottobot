# minottobot

Your friendly neighborhood QA developer.

minottobot is a QA software consultant persona built as an [agentskills.io](https://agentskills.io) skill. It audits software teams across CI/CD, testing, monitoring, Developer Experience, and culture — then builds a prioritized improvement plan.

## How to use

Include the `minottobot/` folder in your skill setup and load `minottobot/SKILL.md`.

**Claude Code:**
```
/skills add minottobot/
```

**agentskills.io:**
```yaml
skills:
  - path: minottobot/
```

Once loaded, describe your team or project and minottobot will take it from there.

## What minottobot does

minottobot runs a two-phase process every time:

### Phase 1 — Audit

Assesses the team across ten areas: CI/CD, environments, local development, code review, testing, automation, monitoring, technical standards, and ownership culture.

It looks for red flags and anti-patterns, identifies clusters, and determines the highest-impact problems.

### Phase 2 — Strategy

Once the audit is complete, minottobot builds an improvement plan on three horizons:

- **Short term** — immediate pain relief, quick wins
- **Medium term** — foundations and frameworks
- **Long term** — structural improvement based on feedback

It reasons about trade-offs case by case, calibrates advice to team size and product context, and always evaluates options against a single golden rule: does this serve the user?

## Code inspection

When running inside a repository (Claude Code or any environment with file-system access), minottobot reads the codebase before asking questions.

It starts by mapping which repositories are in scope — a single repo, multiple separate repos, or a monorepo with distinct sub-projects. It detects the primary technology of each from manifest files (`package.json`, `go.mod`, `pyproject.toml`, etc.) and adapts its scanning patterns accordingly.

For each repo it scans: CI/CD configs, test files and test config, build scripts, lint/format configs, monitoring integrations, git history (last 20 commits), and onboarding documentation.

After scanning all repos it produces an evidence map and flags cross-repo gaps — discrepancies between repositories (e.g., one has CI and the other doesn't) are often the most significant findings. If a Phase 0 answer contradicts what the code shows, minottobot flags it explicitly. The contradiction is itself a finding.

Code inspection does not replace the Phase 0 questionnaire. Operational metrics (MTTR, incident count, deployment frequency) can't be read from code — those still require the team's input.

## Multi-session tracking

minottobot can track progress across sessions using a snapshot file stored in the repository.

At the end of every audit, minottobot produces a snapshot and asks you to save it as `.minottobot/audit-YYYY-MM-DD.md` in your workspace root. The snapshot uses a fixed schema (area scores, top blockers, action items with stable IDs) so audits can be compared over time.

When you start a new session and a previous snapshot exists, minottobot enters **returning engagement mode**: it shows a summary of the last audit (date, repos, scores, blockers) and asks what has changed. At the end of the new audit it appends a **delta view** to the report:

- Score changes per area (`CI/CD: 2/5 → 3/5 ↑`)
- Blockers resolved, still open, or new
- Action item status changes (open → done)
- Repo scope changes (repos added or removed between sessions)

Action items have stable IDs (`A1`, `A2`, ...) that persist across sessions, so progress is traceable without manual cross-referencing.

## What minottobot doesn't do

- Product features and roadmap — only *how* to build, never *what* to build
- Infrastructure — cloud, scaling, networking
- ISO or regulatory certifications

## When minottobot activates

The skill description is intentionally explicit and slightly over-broad so skill routers don't miss it. Here is the full trigger text from `SKILL.md`:

> Use this skill whenever the user asks about QA, testing strategy,
> CI/CD health, team processes, developer experience, code review
> practices, test coverage, flaky tests, monitoring, or any audit
> of an engineering team's quality practices. Also trigger when the
> user says "review our process", "how do we improve our testing",
> "our CI is broken", or "we need a QA strategy".

### Prompts that SHOULD trigger minottobot

1. "Our CI pipeline is broken and builds are failing randomly."
2. "How do we improve our testing strategy?"
3. "We need a QA strategy for our new microservices project."
4. "Can you review our code review process?"
5. "Our test coverage has dropped to 40% — what do we do?"
6. "We have a bunch of flaky tests that keep failing in CI."
7. "How healthy is our CI/CD setup?"
8. "Our deployments take forever and we want better developer experience."
9. "We're not sure what kind of test to write for this feature."
10. "Audit our engineering team's quality practices."

### Prompts that should NOT trigger minottobot

1. "Can you help me implement this new feature?" — product/feature work, out of scope
2. "How do I configure our Kubernetes cluster?" — infrastructure, out of scope
3. "Write a regex that validates email addresses." — general programming task
4. "What cloud provider should we use?" — infrastructure decision, out of scope
5. "Explain how React hooks work." — general technical education, not a team/process question

---

## Repository structure

```
minottobot/               ← the folder to include
  SKILL.md                ← entry point
  references/
    checklist.md          ← step-by-step audit guide
    red-flags.md          ← anti-patterns and warning signs
    philosophy.md         ← core beliefs and communication style
    frameworks.md         ← DFER loop, test pyramid, feature flags, git history
    strategy.md           ← post-audit planning and trade-off reasoning
```
