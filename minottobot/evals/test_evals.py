import json
import os
import re
from pathlib import Path

# Local Ollama inference on CPU is slow; raise DeepEval's internal timeouts
# well above its ~180s default before any deepeval module reads them.
os.environ.setdefault("DEEPEVAL_PER_ATTEMPT_TIMEOUT_SECONDS_OVERRIDE", "600")
os.environ.setdefault("DEEPEVAL_PER_TASK_TIMEOUT_SECONDS_OVERRIDE", "900")

import pytest
from deepeval import assert_test
from deepeval.test_case import LLMTestCase

from minottobot.evals.batch_assertion_metric import BatchAssertionMetric
from minottobot.evals.ollama_model import judge_model, under_test_model

EVALS_DIR = Path(__file__).parent
EVALS_JSON = json.loads((EVALS_DIR / "evals.json").read_text())
SKILL_MD = re.sub(
    r"^---\n.*?\n---\n", "", (EVALS_DIR.parent / "SKILL.md").read_text(), flags=re.DOTALL
)
MIN_PASS_RATE = float(os.environ.get("MIN_PASS_RATE", "0.80"))


@pytest.mark.parametrize(
    "eval_case",
    EVALS_JSON["evals"],
    ids=[e["name"] for e in EVALS_JSON["evals"]],
)
def test_eval(eval_case):
    actual_output = under_test_model().generate(
        eval_case["prompt"], system=SKILL_MD
    )

    test_case = LLMTestCase(
        input=eval_case["prompt"],
        actual_output=actual_output,
    )
    # Grades all assertions for this eval in a single judge call instead of
    # one GEval call per assertion — the accuracy tradeoff is worth it to
    # keep the full suite runnable in a few minutes on local Ollama.
    metric = BatchAssertionMetric(
        assertions=eval_case["assertions"],
        model=judge_model(),
        threshold=MIN_PASS_RATE,
    )

    assert_test(test_case, [metric], run_async=False)
