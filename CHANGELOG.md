# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Migrated the eval regression suite from `scripts/run-evals.sh` (bash + Ollama curl calls) to [DeepEval](https://deepeval.com/) (`minottobot/evals/test_evals.py`, `ollama_model.py`, `batch_assertion_metric.py`), reusing the same 5 team scenarios and 25 assertions in `evals.json`. Grading batches all assertions for a scenario into a single judge call, and the 5 scenarios run in parallel via `pytest-xdist`.
- Rewrote `.github/workflows/evals.yml` to run `uv run pytest` instead of the bash script; it now also pulls a separate judge model (default `mistral`, distinct from the model under test) and no longer commits results to a workspace directory.
- Rewrote the `## Evals` section of `CONTRIBUTING.md` for the new `uv run pytest` workflow.

### Removed

- `scripts/run-evals.sh` and the multi-iteration `minottobot-workspace/` directory (iterations 1–6).
- The manually captured `minottobot/evals/*.md` scenario outputs — superseded by the automated DeepEval suite.

## [1.0.0] - 2026-08-03

First stable release of the minottobot skill.

### Added

- `minottobot/SKILL.md` — QA consultant persona with a two-phase workflow: Phase 0 quantitative baseline, Phase 1 audit, Phase 2 improvement plan.
- Lazy-loading protocol with a context budget and a context saturation warning for long sessions.
- Structured audit report schema with visual indicators.
- Code reconnaissance step, with a fallback when file-reading tools are unavailable.
- Multi-session tracking through `.minottobot/` snapshots (`references/persistence.md`, loaded on demand).
- Reference library: `checklist.md`, `frameworks.md`, `persistence.md`, `philosophy.md`, `red-flags.md`, `strategy.md`, `test-selection.md`.
- Tool evaluation framework and a scenario-based test selection matrix.
- Audit criteria aligned with the blog corpus — DORA metrics, trust, manual verification.
- Playwright operations guidance, expiry-based skip policy, and schema-driven mocks.
- Eval regression suite in `minottobot/evals/` (5 team scenarios, 25 assertions) plus `scripts/run-evals.sh`.
- `.github/workflows/evals.yml` — `workflow_dispatch` eval pipeline running through Ollama (default model: `mistral`).
- Multi-iteration eval workspace in `minottobot-workspace/` (iterations 1–6).
- `README.md`, `CONTRIBUTING.md`, `LICENSE`, and `.gitattributes` rules that keep the GitHub zip download limited to the skill itself.

[Unreleased]: https://github.com/EmanueleMinotto/minottobot/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/EmanueleMinotto/minottobot/releases/tag/v1.0.0
