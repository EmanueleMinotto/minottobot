"""Regression suite for the default (audit + strategy chained) engagement.

System prompt = skills/audit/SKILL.md + skills/strategy/SKILL.md concatenated,
simulating what the "minottobot" orchestrator skill does at runtime — it
points the agent at both files in sequence — without duplicating their
content into skills/minottobot/SKILL.md, which stays a thin pointer.
"""

from pathlib import Path

import pytest

from evals.runner import load_evals, load_skill_prompt, run_eval_case

EVALS_DIR = Path(__file__).parent
REPO_ROOT = EVALS_DIR.parent.parent

EVALS_JSON = load_evals(EVALS_DIR / "evals.json")
SYSTEM_PROMPT = load_skill_prompt(
    REPO_ROOT / "skills" / "audit" / "SKILL.md",
    REPO_ROOT / "skills" / "strategy" / "SKILL.md",
)


@pytest.mark.parametrize("eval_case", EVALS_JSON, ids=[e["name"] for e in EVALS_JSON])
def test_eval(eval_case):
    run_eval_case(eval_case, SYSTEM_PROMPT)
