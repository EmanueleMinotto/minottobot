"""Regression suite for the default (audit + strategy chained) engagement.

Run as two calls, not one: skills/audit/SKILL.md answers the user's Phase 0
description, then skills/strategy/SKILL.md is handed that audit output and
builds the plan from it. That is what the "minottobot" orchestrator skill
does at runtime — it runs the audit to completion, then continues into
strategy with the audit's own output as input — and neither SKILL.md is
duplicated into skills/minottobot/SKILL.md, which stays a thin pointer.

The assertions are graded against both halves joined together, because that
is what the user of a combined engagement reads: one continuous report.
"""

from pathlib import Path

import pytest

from evals.runner import load_evals, load_skill_prompt, run_chained_eval_case

EVALS_DIR = Path(__file__).parent
REPO_ROOT = EVALS_DIR.parent.parent

EVALS_JSON = load_evals(EVALS_DIR / "evals.json")

# What the orchestrator gives strategy when it continues from the audit:
# the user's original description, the finished audit output, and the
# instruction to plan from it. The description is included because strategy
# is continuing the same conversation and can still see it — without it the
# evidence it is required to cite verbatim (the incident, the named tools)
# survives only if the audit half happened to repeat it. Without the closing
# instruction the smaller models under test read the audit report as
# something to restate and never produce a plan at all.
STRATEGY_HANDOFF = (
    "The team described themselves like this:\n\n"
    "{prompt}\n\n"
    "Here is the completed audit output for this team:\n\n"
    "{previous}\n\n"
    "Build the improvement plan from this audit, following your output "
    "requirement in full."
)

STAGES = [
    (load_skill_prompt(REPO_ROOT / "skills" / "audit" / "SKILL.md"), None),
    (
        load_skill_prompt(REPO_ROOT / "skills" / "strategy" / "SKILL.md"),
        STRATEGY_HANDOFF,
    ),
]


@pytest.mark.parametrize("eval_case", EVALS_JSON, ids=[e["name"] for e in EVALS_JSON])
def test_eval(eval_case):
    run_chained_eval_case(eval_case, STAGES)
