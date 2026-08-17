"""Shared eval harness factory, reused by every evals/<skill>/test_evals.py.

Each per-skill test module loads its own evals.json and the SKILL.md file(s)
that make up its system prompt, then calls `run_eval_case` from a
`@pytest.mark.parametrize`d test. Concatenating multiple SKILL.md files (used
by evals/default/, which tests the audit + strategy skills chained together)
mirrors what the "minottobot" orchestrator skill does at runtime — it points
the agent at both files in sequence — without duplicating their content into
a third, drift-prone copy.
"""

import json
import os
import re
from pathlib import Path

# Local Ollama inference on CPU is slow; raise DeepEval's internal timeouts
# well above its ~180s default before any deepeval module reads them.
os.environ.setdefault("DEEPEVAL_PER_ATTEMPT_TIMEOUT_SECONDS_OVERRIDE", "600")
os.environ.setdefault("DEEPEVAL_PER_TASK_TIMEOUT_SECONDS_OVERRIDE", "900")

from deepeval import assert_test
from deepeval.test_case import LLMTestCase

from evals._shared.batch_assertion_metric import BatchAssertionMetric
from evals._shared.ollama_model import judge_model, under_test_model

MIN_PASS_RATE = float(os.environ.get("MIN_PASS_RATE", "0.80"))

_FRONTMATTER_RE = re.compile(r"^---\n.*?\n---\n", re.DOTALL)


def load_skill_prompt(*skill_md_paths: Path) -> str:
    """Strip frontmatter from one or more SKILL.md files and join them.

    Order matters when passing multiple paths — it should match the order
    the skills run in during a real engagement (e.g. audit before strategy).
    """
    parts = [
        _FRONTMATTER_RE.sub("", path.read_text(), count=1) for path in skill_md_paths
    ]
    return "\n\n".join(parts)


def load_evals(evals_json_path: Path) -> list[dict]:
    return json.loads(evals_json_path.read_text())["evals"]


def run_eval_case(eval_case: dict, system_prompt: str) -> None:
    actual_output = under_test_model().generate(eval_case["prompt"], system=system_prompt)

    test_case = LLMTestCase(input=eval_case["prompt"], actual_output=actual_output)
    # Grades all assertions for this eval in a single judge call instead of
    # one GEval call per assertion — the accuracy tradeoff is worth it to
    # keep the full suite runnable in a few minutes on local Ollama.
    metric = BatchAssertionMetric(
        assertions=eval_case["assertions"],
        model=judge_model(),
        threshold=MIN_PASS_RATE,
    )
    assert_test(test_case, [metric], run_async=False)
