"""Regression suite for the audit skill in isolation.

System prompt = skills/audit/SKILL.md only. Assertions are restricted to
what the audit contract owns (scores, evidence, verbatim citations) and
explicitly guard against scope creep into the improvement plan, which is
strategy's job.
"""

from pathlib import Path

import pytest

from evals.runner import load_evals, load_skill_prompt, run_eval_case

EVALS_DIR = Path(__file__).parent
REPO_ROOT = EVALS_DIR.parent.parent

EVALS_JSON = load_evals(EVALS_DIR / "evals.json")
SYSTEM_PROMPT = load_skill_prompt(REPO_ROOT / "skills" / "audit" / "SKILL.md")


@pytest.mark.parametrize("eval_case", EVALS_JSON, ids=[e["name"] for e in EVALS_JSON])
def test_eval(eval_case):
    run_eval_case(eval_case, SYSTEM_PROMPT)
