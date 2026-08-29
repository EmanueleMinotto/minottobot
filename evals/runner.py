"""Shared eval harness factory, reused by every evals/<skill>/test_evals.py.

Each per-skill test module loads its own evals.json and the SKILL.md file(s)
that make up its system prompt, then calls one of the two runners from a
`@pytest.mark.parametrize`d test:

- `run_eval_case` — one skill, one call. The default for a skill tested on
  its own.
- `run_chained_eval_case` — a multi-skill engagement, one call per skill,
  each handed the previous skill's output. Used by evals/default/, which
  tests audit followed by strategy.

Chained engagements get their own runner because concatenating both SKILL.md
files into a single system prompt does not reproduce them. The "minottobot"
orchestrator runs the audit to completion first, then feeds that output to
strategy; collapsing the two into one call puts two output contracts in front
of the model at once, and the smaller models these evals run against answer
the last contract they read and drop the audit's score table entirely. Running
the stages separately keeps the harness faithful to the orchestrator without
duplicating either skill's content into a third, drift-prone copy.
"""

import json
import os
import re
from collections.abc import Sequence
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


def _grade(eval_case: dict, actual_output: str) -> None:
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


def run_eval_case(eval_case: dict, system_prompt: str) -> None:
    actual_output = under_test_model().generate(eval_case["prompt"], system=system_prompt)
    _grade(eval_case, actual_output)


def run_chained_eval_case(
    eval_case: dict, stages: Sequence[tuple[str, str | None]]
) -> None:
    """Run a multi-skill engagement one skill per call, then grade the whole.

    `stages` is a sequence of `(system_prompt, handoff_template)` pairs in the
    order the skills run. The first stage is given the eval's own prompt and
    its handoff template is unused; every later stage is given its template
    formatted with `previous=` the preceding stage's output and `prompt=` the
    eval's original prompt, which is how the orchestrator skill hands one
    skill's report to the next. Later stages get the original prompt as well
    as the report because in a real engagement they are continuing the same
    conversation — the user's own description is still in context, which is
    why the orchestrator tells them not to ask for it again.

    The assertions are graded against every stage's output joined together:
    the user of a chained engagement sees one continuous report, so a claim
    the audit half made counts even when the plan half never repeats it.
    """
    model = under_test_model()
    outputs: list[str] = []
    for system_prompt, handoff in stages:
        prompt = (
            eval_case["prompt"]
            if not outputs
            else handoff.format(prompt=eval_case["prompt"], previous=outputs[-1])
        )
        outputs.append(model.generate(prompt, system=system_prompt))
    _grade(eval_case, "\n\n".join(outputs))
