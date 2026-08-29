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

- **MAJOR** — a skill's workflow or output contract changes in a way that breaks existing `.minottobot/` snapshots or expectations, or an existing skill is removed or renamed.
- **MINOR** — new phases, new reference files, or new capabilities within an existing skill, or an entirely new skill added without changing any existing skill's contract.
- **PATCH** — wording fixes, prompt tuning, and reference corrections that do not change the workflow.

The version lives in three manifests — [`plugin.json`](plugin.json), [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json) and [`.codex-plugin/plugin.json`](.codex-plugin/plugin.json) — bump all three in the same commit as the changelog entry. The `manifest-consistency` job in CI fails the pull request if the `name` or `version` fields drift apart.

### Releasing

1. Move the `[Unreleased]` entries under a new `## [X.Y.Z] - YYYY-MM-DD` heading and add the comparison links at the bottom of the file.
2. Commit with `chore(release): vX.Y.Z`.
3. Tag the commit: `git tag -a vX.Y.Z -m "vX.Y.Z"` and push with `git push --follow-tags`.

## Plugin manifests

The repository root is the plugin, and it carries one manifest per ecosystem so every client can install it straight from the repo:

- [`plugin.json`](plugin.json) — [Agent Plugins 1.0.0](https://agent-plugins.org/), read by Cursor and any other conforming client. Its schema is `additionalProperties: false`: only the fields the spec defines are allowed, and anything client-specific belongs under `extensions`, keyed by reverse-domain namespace. Do not add `skills` or `interface` here.
- [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json) + [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json) — [Claude Code](https://docs.claude.com/en/docs/claude-code/plugins), the self-hosted catalog behind `/plugin marketplace add EmanueleMinotto/minottobot`.
- [`.codex-plugin/plugin.json`](.codex-plugin/plugin.json) + [`.agents/plugins/marketplace.json`](.agents/plugins/marketplace.json) — [Codex](https://developers.openai.com/plugins/build/plugins), behind `codex plugin marketplace add EmanueleMinotto/minottobot`. Only `plugin.json` goes inside `.codex-plugin/`.

All three point at the same `skills/` directory at the repository root — keep it there. Moving or nesting it breaks discovery in every client at once.

## Skills

The repository contains eight skills under `skills/`, each following the [Agent Skills](https://agentskills.io/) format:

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

## The snapshot helper script

`scripts/snapshot.py` handles the parts of an engagement that are mechanical rather than judgement calls: parsing a `.minottobot/` snapshot, computing the delta between two of them, and checking a finished report against the fixed output contract. `audit` and `strategy` both call it; it ships inside the plugin, so every client that installs the repo gets it.

```bash
python3 scripts/snapshot.py parse    .minottobot/audit-2026-04-27.md
python3 scripts/snapshot.py delta    .minottobot/audit-2026-01-15.md .minottobot/audit-2026-04-27.md
python3 scripts/snapshot.py validate report.md --cap "Ownership & culture=2"
```

Three constraints keep it viable, and none of them are negotiable:

- **Stdlib only, Python 3.9+.** It has to run wherever the plugin is installed, which is not a machine you control — no PyYAML (the snapshot frontmatter is parsed by hand), no dependency on `uv sync` having been run. `requires-python = ">=3.11"` in `pyproject.toml` governs the eval dependencies, not this script; CI runs the unit suite on 3.9 to catch a stray f-string or match statement.
- **It never writes a report.** Scores, findings, blockers, and wording stay with the model. The script reads what the model wrote, does the arithmetic, and reports violations. If it ever starts generating prose, the determinism argument for having it has been lost.
- **It is optional at every call site.** Every skill instruction that invokes it also says what to do when it is unavailable. The skills must keep working in a chat client with no filesystem, which is the case `audit/SKILL.md` already handles for code reconnaissance.

When the output contract in `skills/audit/SKILL.md` or `skills/strategy/references/snapshot-delta.md` changes, update the script and its tests in the same commit — a validator that enforces last month's format is worse than no validator. If the snapshot format itself changes shape, bump `format_version` and add it to `SUPPORTED_FORMAT_VERSIONS`; the script warns instead of guessing when it meets a version it does not know.

### Unit tests

`tests/` covers the script with ordinary pytest — no Ollama, no LLM, no variance. It runs in well under a second and is the right place for anything deterministic:

```bash
python -m pytest tests -v      # no dependencies beyond pytest
uv run pytest tests -v
```

`tests/conftest.py` puts `scripts/` on the path, since it ships as a plain directory inside the plugin rather than as an importable package. The `unit-tests` job in CI runs this suite on Python 3.9 and 3.13, installing only pytest so an accidental third-party import fails the build.

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
  daily_prevention/       — daily-prevention skill alone (same hyphen/underscore convention as test_selection)
    evals.json
    test_evals.py
  reality_check/          — reality-check skill alone
    evals.json
    test_evals.py
  breaking_change_detector/ — breaking-change-detector skill alone
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
uv run pytest evals/ -v -n 2 --reruns 2 --reruns-delay 10   # runs every sub-suite's scenarios concurrently
uv run pytest evals/audit -v                                # runs only the audit sub-suite
```

Ollama serves concurrent requests against an already-loaded model, so running scenarios in parallel (`-n`, via `pytest-xdist`) is faster than running them sequentially — but on a single local GPU (or, in CI, a shared CPU-only runner), concurrent requests contend with each other and tail latency is unpredictable. Expect the full suite to take longer than a single sub-suite: local GPU/CPU-bound inference for both report generation and grading is the structural cost, not the harness. `OLLAMA_REQUEST_TIMEOUT` (default `900`s) gives individual requests enough headroom under that contention; keep `-n` low (`2`, the CI default) if a higher value flakes with timeouts. `--reruns` (via `pytest-rerunfailures`) retries a scenario that fails once before failing the build, which absorbs the single-run noise described below.

Useful env vars: `OLLAMA_MODEL`, `OLLAMA_JUDGE_MODEL`, `OLLAMA_URL`, `MIN_PASS_RATE` (per-assertion GEval threshold, default `0.80`). Run a single scenario with `-k <name>` (e.g. `-k startup-chaos`).

### Grading rules

- Each scenario's assertions are graded together in a single judge call (`BatchAssertionMetric`), using the assertion text verbatim as the evaluation criteria.
- A regression is any assertion that still fails after a rerun, following a `SKILL.md`/reference file change that previously passed.
- Evaluations run against small local models, so scores can be noisier than a frontier-model judge — treat a single borderline failure (one that only fails without a rerun) as noise, not a hard regression. CI reruns each failure up to twice before failing the build for exactly this reason.

### Adding a new eval

1. Add an entry to the relevant sub-suite's `evals.json`, following the existing schema (`id`, `name`, `prompt`, `expected_output`, `assertions`).
2. Run `uv run pytest evals/<sub-suite> -v -k <name>` to generate and grade it.

### CI

[`.github/workflows/evals.yml`](.github/workflows/evals.yml) runs the full suite on every pull request and on every push to `main`, using the default models (`llama3.2` under test, `mistral` as judge). The full suite runs as a matrix job — one job per sub-suite under `evals/`, each on its own runner with its own ephemeral `ubuntu-latest` Ollama instance (`-n 2 --reruns 2 --reruns-delay 10` inside each job) — so sub-suites run in true parallel instead of contending for a single shared CPU-only runner. Pulled models are cached across runs (`~/.ollama/models`, keyed on the model pair) to avoid re-downloading them on every job. It can also be triggered manually via `workflow_dispatch`, which additionally lets you pick a specific model pair, a custom `MIN_PASS_RATE`, or a single scenario by name — a named scenario runs as one non-matrix job against the whole `evals/` tree instead, since a single scenario doesn't benefit from the sub-suite split.
