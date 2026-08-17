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

Versioning rules for this plugin:

- **MAJOR** — a skill's workflow or output contract changes in a way that breaks existing `.minottobot/` snapshots or expectations, or a skill is added/removed/renamed.
- **MINOR** — new phases, new reference files, or new capabilities within an existing skill.
- **PATCH** — wording fixes, prompt tuning, and reference corrections that do not change the workflow.

The version lives in [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json) — bump it in the same commit as the changelog entry.

### Releasing

1. Move the `[Unreleased]` entries under a new `## [X.Y.Z] - YYYY-MM-DD` heading and add the comparison links at the bottom of the file.
2. Commit with `chore(release): vX.Y.Z`.
3. Tag the commit: `git tag -a vX.Y.Z -m "vX.Y.Z"` and push with `git push --follow-tags`.

## Skills

This repository is a [Claude Code plugin](https://docs.claude.com/en/docs/claude-code/plugins) (root = plugin, see [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json) and [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json)) containing four skills under `skills/`, each following the [Agent Skills](https://agentskills.io/) format:

- Every skill lives in its own directory under `skills/<name>/`
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

`audit` and `strategy` split what was previously a single two-phase skill: `audit` produces a scored, evidence-based report and stops; `strategy` consumes that report and builds the improvement plan. Keep that boundary when editing either — don't let scoring logic drift into `strategy` or plan-building logic drift into `audit`. `test-selection` is fully standalone. `minottobot` is a thin orchestrator that points at `audit` then `strategy` in sequence — it should never grow its own copy of their instructions; if you need to change what the default engagement does, change `audit` or `strategy`, not `minottobot`.

## Evals

The `evals/` directory contains a regression suite, built on [DeepEval](https://deepeval.com/) and run against a local Ollama instance, with one sub-suite per skill.

### Structure

```
evals/
  runner.py            — shared factory: loads evals.json, generates via the model under test, grades with BatchAssertionMetric
  _shared/
    ollama_model.py     — DeepEvalBaseLLM wrapper calling the Ollama HTTP API
    batch_assertion_metric.py — batches all of a scenario's assertions into one judge call
  default/              — audit + strategy chained (skills/audit/SKILL.md + skills/strategy/SKILL.md as system prompt)
    evals.json
    test_evals.py
  audit/                — audit skill alone (skills/audit/SKILL.md as system prompt)
    evals.json
    test_evals.py
  strategy/              — strategy skill alone; prompts are synthetic audit outputs, not raw Phase 0 data
    evals.json
    test_evals.py
  test_selection/        — test-selection skill alone (note: underscore — a valid Python package name; the skill directory itself is skills/test-selection/, with a hyphen)
    evals.json
    test_evals.py
```

Each `evals.json` is the single source of truth for its sub-suite's scenarios and assertions — nothing else needs to change when adding or editing a scenario. Each `test_evals.py` is a few lines calling `evals.runner.load_evals`, `load_skill_prompt`, and `run_eval_case` — do not duplicate the harness logic per sub-suite.

Because the eval harness calls Ollama directly over HTTP with no tool access, each `SKILL.md` must be self-sufficient as a system prompt for its own sub-suite — the "load reference X" instructions inside it are never actually executed during eval, only the literal `SKILL.md` text is evaluated. Keep whatever a sub-suite's assertions depend on (scoring rules, output contracts, mandatory rules) written directly in the relevant `SKILL.md`, not only in a `references/*.md` file.

### Running the evals

Requires [uv](https://docs.astral.sh/uv/) and a local [Ollama](https://ollama.com/) instance:

```bash
ollama serve &
ollama pull llama3.2   # model under test (OLLAMA_MODEL, default llama3.2)
ollama pull mistral    # judge model (OLLAMA_JUDGE_MODEL, default mistral — kept different
                        # from the model under test so it doesn't grade its own output)

uv sync
uv run pytest evals/ -v -n 5          # runs every sub-suite's scenarios concurrently
uv run pytest evals/audit -v          # runs only the audit sub-suite
```

Ollama serves concurrent requests against an already-loaded model, so running scenarios in parallel (`-n 5`, via `pytest-xdist`) is faster than running them sequentially — but on a single local GPU, concurrent requests contend with each other and tail latency is unpredictable. Expect the full suite to take longer than a single sub-suite: local GPU-bound inference for both report generation and grading is the structural cost, not the harness. `OLLAMA_REQUEST_TIMEOUT` (default `900`s) gives individual requests enough headroom under that contention; lower `-n` (e.g. `-n 2`) trades parallelism for more consistent per-request latency if the default flakes.

Useful env vars: `OLLAMA_MODEL`, `OLLAMA_JUDGE_MODEL`, `OLLAMA_URL`, `MIN_PASS_RATE` (per-assertion GEval threshold, default `0.80`). Run a single scenario with `-k <name>` (e.g. `-k startup-chaos`).

### Grading rules

- Each scenario's assertions are graded together in a single judge call (`BatchAssertionMetric`), using the assertion text verbatim as the evaluation criteria.
- A regression is any assertion whose score drops below `MIN_PASS_RATE` after a `SKILL.md`/reference file change that previously passed.
- Evaluations run against small local models, so scores can be noisier than a frontier-model judge — treat a single borderline failure as a signal to re-run before treating it as a hard regression.

### Adding a new eval

1. Add an entry to the relevant sub-suite's `evals.json`, following the existing schema (`id`, `name`, `prompt`, `expected_output`, `assertions`).
2. Run `uv run pytest evals/<sub-suite> -v -k <name>` to generate and grade it.
