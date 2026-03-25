# Contributing

## Commit messages

All commits must follow the [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>(<scope>): <description>
```

Common types: `feat`, `fix`, `docs`, `refactor`, `chore`.

Examples:
```
feat(audit): add security review checklist
fix(shared): correct DFER loop description
docs(strategy): expand trade-off reasoning examples
```

## Skills

Each skill must follow the [Agent Skills](https://agentskills.io/) format:

- Every skill lives in its own directory
- The directory must contain a `SKILL.md` file with YAML frontmatter
- The `name` field must match the directory name (lowercase letters and hyphens only)
- The `description` field must explain what the skill does and when to use it
- Additional documentation goes in a `references/` subdirectory

Minimal `SKILL.md`:

```markdown
---
name: skill-name
description: What this skill does and when to use it.
---

Instructions for the agent...
```

## Evals

The `minottobot/evals/` directory contains a regression suite for the skill. It follows the [agentskills.io eval pattern](https://agentskills.io/skill-creation/evaluating-skills).

### Structure

```
minottobot/evals/
  evals.json            — machine-readable test cases with prompts and assertions
  startup-chaos.md      — captured output for Swiftly Inc (startup, 0 tests)
  enterprise-legacy.md  — captured output for FinanceCore Ltd (enterprise, legacy CI)
  post-incident.md      — captured output for Norsk Mobility AS (post-incident team)
  high-functioning.md   — captured output for Helix Team @ Atmos (high-functioning)
  org-chaos.md          — captured output for Momentum Fintech Platform (org chaos)
```

Each `*.md` file has three sections: the input team profile, the minottobot audit output, and an assertions table with PASS/FAIL grades.

### Re-running an eval

1. Load the skill in a fresh Claude Code session: `/skills add minottobot/`
2. Find the prompt for the eval in `evals.json` (match by `name`)
3. Paste the prompt into the session and let minottobot complete the audit
4. Replace the "Minottobot output" section in the `*.md` file with the new output
5. Re-evaluate each assertion in the assertions table — mark PASS or FAIL with a brief evidence quote from the output

### Grading rules

- **PASS** requires concrete evidence: quote or reference the specific part of the output that satisfies the assertion.
- **FAIL** if you have to give the benefit of the doubt. If an assertion says "must mention X" and X is implied but not stated, that is a FAIL.
- A regression is any assertion that flips from PASS to FAIL after a reference file change.

### Adding a new eval

1. Add an entry to `evals.json` following the existing schema (`id`, `name`, `prompt`, `expected_output`, `assertions`).
2. Run the eval using the steps above and save the output as `evals/<name>.md`.
3. Fill in the assertions table with initial PASS/FAIL grades.

### Workspace model

For multi-iteration tracking (comparing skill versions, measuring improvement over time), use the workspace structure described at [agentskills.io/skill-creation/evaluating-skills](https://agentskills.io/skill-creation/evaluating-skills). The workspace lives outside the skill directory: `minottobot-workspace/iteration-N/eval-<name>/with_skill/` and `without_skill/`.
