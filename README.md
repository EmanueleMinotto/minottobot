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

## What minottobot doesn't do

- Product features and roadmap — only *how* to build, never *what* to build
- Infrastructure — cloud, scaling, networking
- ISO or regulatory certifications

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
