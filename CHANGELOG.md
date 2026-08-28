# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- `breaking-change-detector` now opens every answer about a concrete schema change with a fixed classification line — `Classification: {breaking | dangerous | safe} — SemVer: {MAJOR | MINOR | PATCH}` — above the tooling table, instead of leaving the SemVer consequence to a step halfway down "Deprecate before you remove". v2.4.2 required stating it in those exact terms but not *where*, so the `openapi-field-removal` eval kept failing intermittently on answers that covered deprecation and tooling first and reached the version bump late or not at all. The same section keeps the tool recommendation (oasdiff, GraphQL Inspector, Buf breaking, Pact) mandatory so the fixed opening does not crowd it out, and exempts policy, setup, and "how do I find out" questions where there is no specific change to classify.
- `audit` now caps CI/CD at 2/5 for a pipeline that runs lint, build, or type checks but no tests, and for deployment done by hand with no automated deploy pipeline — two signals the mandatory score-cap table did not cover, so a fast, modern pipeline read as a strength. Run time is now framed as evidence about the feedback loop, not about quality gating: a 2-minute lint-only GitHub Actions run and frequent manual deploys do not buy the cap back, and the one-line finding must name what the pipeline does *not* do. The `startup-chaos` eval was failing because CI/CD scored 3/5 on exactly that shape.
- `strategy` now carries every one of the six area scores forward from the audit — no blank cells, no dropped rows, and no softening `Ownership & culture` because the plan proposes to fix it — and requires at least one short-term item the engineering team can start alone, this sprint, when the audit reports ownership gaps (no product owner, leadership churn, staff on loan, two CI systems). The `org-chaos` eval was failing on both counts in the chained audit + strategy output: the ownership score got lost, and every short-term item waited on a VP, an owner, or another team.

### Added

- Snapshot parsing, delta views, and output-contract checking are now done by a script instead of by careful reading. The plugin ships `scripts/snapshot.py` (stdlib-only, Python 3.9+), which `audit` and `strategy` call for the three parts of an engagement that are arithmetic rather than judgement: reading a `.minottobot/` snapshot into structured data — including `next_action_id`, so a returning engagement never reuses an action item ID — rendering the delta between two snapshots with the score arrows, emoji, blocker classification and repo scope changes computed rather than recalled, and validating a finished audit or plan before it is handed over. The validator enforces what the format contract already required but could only ask for in prose: the six area rows present and in the fixed order, every score written as `N/5` rather than a bare number or a `[score]/5` placeholder, no unreplaced template placeholders, and — via `--cap "AREA=N"` — that a mandatory score cap the Phase 0 data triggered was actually applied, the Ownership & culture cap being the one most often missed. Scores, findings, and wording remain the model's: the script never writes a report, only reads one. It is optional everywhere it is used — with no Bash, no `python3`, or a script that fails to run, both skills fall back to the previous by-hand instructions, so a chat client with no filesystem behaves exactly as before.

- minottobot is now installable as a plugin outside Claude Code, without copying skill files by hand. The repository root carries an [Agent Plugins 1.0.0](https://agent-plugins.org/) manifest (`plugin.json`), so Cursor and any other conforming client install it straight from the repo — for Cursor, either as a team marketplace imported from the repo, or as a symlinked local plugin that updates with a `git pull`. Codex gets its own manifest (`.codex-plugin/plugin.json`) and a self-hosted catalog (`.agents/plugins/marketplace.json`), so `codex plugin marketplace add EmanueleMinotto/minottobot` is enough to install and `codex plugin marketplace upgrade` to update. The Claude Code manifests are unchanged and `/plugin install minottobot` keeps working exactly as before. Copying `skills/*` into an agent's skills directory is still documented, but only as the fallback for agents with no plugin installer.

## [2.4.2] - 2026-08-25

### Fixed

- `breaking-change-detector` now requires stating the SemVer/MAJOR consequence of a breaking change in those exact terms, not just implying it through a deprecation recommendation — the `openapi-field-removal` eval was intermittently failing because the model's answer covered deprecation and tooling but left the version-bump conclusion unstated.

## [2.4.1] - 2026-08-25

### Fixed

- `test-review` now proposes the deterministic check behind a finding whenever there is one: when it can name the exact rule (`jest/expect-expect`, `jest/no-conditional-in-test`, `no-magic-numbers`, `playwright/no-wait-for-timeout`, the `RSpec/*` and Ruff `PT` equivalents) and the pattern recurs, it says so alongside the fix, so that class of finding is caught for free on every future change instead of costing another AI review round. Findings carry an optional `Prevention` field for it. Guarded on three sides: never invent a rule ID (falling back to a quick web search for a plugin that would add it before giving up), don't propose a custom rule or codemod for a one-off, and propose a baseline-and-ratchet rollout — handed off to `daily-prevention` — rather than a flat "enable this" when the rule would light up hundreds of existing violations. Explicitly does not apply to the semantic checks (requirement matching, pyramid placement), where no rule expresses the judgment and an approximate one would give false confidence.

## [2.4.0] - 2026-08-20

### Added

- New standalone skill `test-review`: reviews test code already written — weak or tautological assertions, over-broad tests that should be split, magic numbers in place of named constants, whether a test actually verifies the requirement it claims to (when that information is available), alignment with repo/team conventions, and whether a test sits at the right pyramid level (e.g. an E2E test that should be an integration or unit test). Complements the built-in code-review skill by owning the test-specific half of that judgment; `audit` and `daily-prevention` hand off to it on-demand, and `test-selection` cross-references it as the "is it any good" counterpart to "what should I write."

## [2.3.1] - 2026-08-18

### Changed

- `.github/workflows/evals.yml` now runs the full suite as a matrix job — one job per `evals/` sub-suite, each on its own runner with its own Ollama instance — instead of one job running every sub-suite sequentially with `pytest-xdist` contending for a single shared CPU-only runner. Pulled models are cached (`~/.ollama/models`, keyed on the model pair) across runs to avoid re-downloading them in every matrix job. A single named scenario via `workflow_dispatch` still runs as one non-matrix job against the whole `evals/` tree, since it doesn't benefit from the sub-suite split.

## [2.3.0] - 2026-08-18

### Added

- New standalone skill `daily-prevention`: recommends linters, type checkers, and specific rule presets for day-to-day maintainability, adapting first to whatever is already configured in the repo before proposing anything new, with guidance on wiring checks into the editor, pre-commit, and CI, and pointing to AI-assisted review as a complement where static analysis structurally can't reach. `audit` and `strategy` hand off to it on-demand when a linting/static-analysis gap surfaces mid-engagement.
- New standalone skill `reality-check`: a lightweight, current-state pulse check for team leads and engineering managers — pulls live data from issue-tracker, VCS, and monitoring MCP servers when connected, falling back to asking directly when not. Deliberately lighter-weight than `audit` and not a substitute for it.
- New standalone skill `breaking-change-detector`: recommends the right tool (oasdiff, Buf breaking, GraphQL Inspector, or Pact) for catching API breaking changes across OpenAPI/REST, Protobuf/gRPC, GraphQL, and consumer-driven contracts, plus SemVer and deprecation-workflow guidance. `audit` and `strategy` hand off to it on-demand when unmanaged API compatibility risk surfaces mid-engagement.
- Collapsible "Example output" sections under each of the four skills in the README, showing a realistic sample report for `minottobot`, `audit`, and `strategy`, and a sample recommendation for `test-selection` — hidden by default via `<details>` so the README stays scannable.

### Changed

- `daily-prevention` and `reality-check` now cross-reference each other as the shift-left/shift-right halves of the same picture (per `strategy/references/philosophy.md`), and `daily-prevention` points to the existing DFER loop in `strategy/references/frameworks.md` for warn-first rollout, baseline-freeze, and "clean as you touch" mechanics instead of giving weaker ad-hoc advice — by reference only, no content duplicated.

### Fixed

- `.github/workflows/evals.yml` was flaking on borderline judge scores and contention-driven Ollama timeouts under `-n 5`. Lowered CI concurrency to `-n 2` and added `--reruns 2 --reruns-delay 10` (via a new direct `pytest-rerunfailures` dependency) so a scenario that fails once is regenerated and re-graded before it fails the build, per `CONTRIBUTING.md`'s documented eval philosophy.

## [2.0.0] - 2026-08-17

**Breaking:** restructured the single `minottobot` skill into a four-skill [Claude Code plugin](https://docs.claude.com/en/docs/claude-code/plugins). Existing `.minottobot/` snapshots remain compatible (same schema), but anything that assumed a single skill handled the whole engagement needs to switch to the new install/invocation path.

### Added

- Converted the repository into a self-hosted Claude Code plugin: `.claude-plugin/plugin.json` (root = plugin) and `.claude-plugin/marketplace.json` (`source: "."`), installable via `/plugin marketplace add` + `/plugin install minottobot`.
- Split the monolithic skill into four: `audit` (session init, code reconnaissance, Phase 0, checklist/red-flags assessment, evidence-anchored scoring — stops at a scored audit output), `strategy` (consumes an audit output and builds the improvement plan, action items, snapshot, and delta view), `test-selection` (fully standalone decision guide for what test to write), and `minottobot` (the default engagement — a thin orchestrator that runs `audit` then `strategy` in sequence).
- New `skills/audit/references/session-resume.md` and `skills/strategy/references/snapshot-delta.md`, split from the former `persistence.md` along the audit/strategy boundary.
- Per-skill eval sub-suites under `evals/<skill>/` (`audit`, `strategy`, `test_selection`), plus `evals/default/` retaining the original 5-scenario/25-assertion suite against the audit+strategy skills chained together. New `evals/runner.py` centralizes the harness previously duplicated in a single `test_evals.py`.
- Migrated the eval regression suite from `scripts/run-evals.sh` (bash + Ollama curl calls) to [DeepEval](https://deepeval.com/) (`ollama_model.py`, `batch_assertion_metric.py`), reusing the same 5 team scenarios and 25 assertions. Grading batches all assertions for a scenario into a single judge call, and scenarios run in parallel via `pytest-xdist`.

### Changed

- Moved `minottobot/references/*.md` into `skills/audit/references/` and `skills/strategy/references/` depending on which skill now owns them (see README's "Repository structure").
- Moved the eval suite from `minottobot/evals/` to a top-level `evals/` package; `pyproject.toml` `testpaths` updated accordingly.
- Area scores and their evidence-based caps moved from the former "Phase 2 — Strategy" section into `audit`, since scoring is a judgment made from Phase 0/checklist evidence, not part of the improvement plan.
- Rewrote `.github/workflows/evals.yml` to run `uv run pytest` instead of the bash script; it now also pulls a separate judge model (default `mistral`, distinct from the model under test) and no longer commits results to a workspace directory.
- `.github/workflows/evals.yml` now runs automatically on every pull request and on every push to `main` (in addition to manual `workflow_dispatch`), running the full `evals/` suite across all sub-suites.
- `strategy` now explicitly requires citing the audit's verbatim metrics and evidence in the executive summary, including positive signals and not just problems.

### Removed

- `scripts/run-evals.sh` and the multi-iteration `minottobot-workspace/` directory (iterations 1–6).
- The manually captured scenario outputs — superseded by the automated DeepEval suite.

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

[2.4.2]: https://github.com/EmanueleMinotto/minottobot/compare/v2.4.1...v2.4.2
[2.4.1]: https://github.com/EmanueleMinotto/minottobot/compare/v2.4.0...v2.4.1
[2.4.0]: https://github.com/EmanueleMinotto/minottobot/compare/v2.3.1...v2.4.0
[2.3.1]: https://github.com/EmanueleMinotto/minottobot/compare/v2.3.0...v2.3.1
[2.3.0]: https://github.com/EmanueleMinotto/minottobot/compare/v2.0.0...v2.3.0
[2.0.0]: https://github.com/EmanueleMinotto/minottobot/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/EmanueleMinotto/minottobot/releases/tag/v1.0.0
