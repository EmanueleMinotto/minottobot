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

## Changelog

Every user-visible change must be recorded in [`CHANGELOG.md`](CHANGELOG.md), which follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). The project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

- Add the entry under `## [Unreleased]`, in the matching group: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.
- Write entries for users of the skill, not for the diff: describe the behaviour that changed, not the file that moved.
- Internal-only work (eval runs, workspace iterations, CI tweaks) does not need an entry.

Versioning rules for this skill:

- **MAJOR** — the audit workflow or the skill contract changes in a way that breaks existing `.minottobot/` snapshots or expectations.
- **MINOR** — new phases, new reference files, or new capabilities.
- **PATCH** — wording fixes, prompt tuning, and reference corrections that do not change the workflow.

### Releasing

1. Move the `[Unreleased]` entries under a new `## [X.Y.Z] - YYYY-MM-DD` heading and add the comparison links at the bottom of the file.
2. Commit with `chore(release): vX.Y.Z`.
3. Tag the commit: `git tag -a vX.Y.Z -m "vX.Y.Z"` and push with `git push --follow-tags`.

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

The `minottobot/evals/` directory contains a regression suite for the skill, built on [DeepEval](https://deepeval.com/) and run against a local Ollama instance.

### Structure

```
minottobot/evals/
  evals.json         — machine-readable test cases: prompt + natural-language assertions per scenario
  ollama_model.py     — DeepEvalBaseLLM wrapper calling the Ollama HTTP API
  test_evals.py        — pytest suite: generates the audit report, grades each assertion with GEval
```

`evals.json` is the single source of truth for the 5 scenarios (startup-chaos, enterprise-legacy, post-incident, high-functioning, org-chaos) and their assertions — nothing else needs to change when adding or editing a scenario.

### Running the evals

Requires [uv](https://docs.astral.sh/uv/) and a local [Ollama](https://ollama.com/) instance:

```bash
ollama serve &
ollama pull llama3.2   # model under test (OLLAMA_MODEL, default llama3.2)
ollama pull mistral    # judge model (OLLAMA_JUDGE_MODEL, default mistral — kept different
                        # from the model under test so it doesn't grade its own output)

uv sync
uv run pytest minottobot/evals/test_evals.py -v -n 5   # runs all 5 scenarios concurrently
```

Ollama serves concurrent requests against an already-loaded model, so running the 5 scenarios in parallel (`-n 5`, via `pytest-xdist`) is faster than running them sequentially — but on a single local GPU, 5 concurrent requests contend with each other and tail latency is unpredictable. Expect the full suite to take roughly **8-12 minutes** on typical consumer hardware (`llama3.2` under test, `mistral` as judge), not sub-5-minutes: local GPU-bound inference for both report generation and grading is the structural cost, not the harness. `OLLAMA_REQUEST_TIMEOUT` (default `900`s) gives individual requests enough headroom under that contention; lower `-n` (e.g. `-n 2`) trades parallelism for more consistent per-request latency if the default flakes.

Useful env vars: `OLLAMA_MODEL`, `OLLAMA_JUDGE_MODEL`, `OLLAMA_URL`, `MIN_PASS_RATE` (per-assertion GEval threshold, default `0.80`). Run a single scenario with `-k <name>` (e.g. `-k startup-chaos`).

For each scenario, `test_evals.py` loads `SKILL.md` as the system prompt (no separate hardcoded output-contract template — `SKILL.md` is the only source of truth for the expected output format), generates the audit report via the model under test, then evaluates every assertion in that scenario as its own `GEval` metric against the judge model.

### Grading rules

- Each assertion is graded independently by the judge model via `GEval`, using the assertion text verbatim as the evaluation criteria.
- A regression is any assertion whose score drops below `MIN_PASS_RATE` after a `SKILL.md`/reference file change that previously passed.
- Evaluations run against small local models, so scores can be noisier than a frontier-model judge — treat a single borderline failure as a signal to re-run before treating it as a hard regression.

### Adding a new eval

1. Add an entry to `evals.json` following the existing schema (`id`, `name`, `prompt`, `expected_output`, `assertions`).
2. Run `uv run pytest minottobot/evals/test_evals.py -v -k <name>` to generate and grade it.
