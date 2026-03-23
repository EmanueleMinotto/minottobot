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
