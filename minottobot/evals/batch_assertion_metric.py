from typing import List

from deepeval.metrics.base_metric import BaseMetric
from deepeval.metrics.utils import trimAndLoadJson
from deepeval.test_case import LLMTestCase, SingleTurnParams

from minottobot.evals.ollama_model import OllamaModel

GRADE_PROMPT_TEMPLATE = """You are a strict pass/fail evaluator for an audit report.

Audit output:
---
{actual_output}
---

For each of the following assertions, decide whether the audit output satisfies it.
Only answer "yes" if the assertion is explicitly and completely satisfied. Be strict.

Assertions:
{numbered_assertions}

Return ONLY a JSON object of this exact shape, with one verdict per assertion, in the
same order as listed above:
{{"verdicts": [{{"pass": true, "evidence": "direct quote or brief justification"}}, ...]}}
"""


class BatchAssertionMetric(BaseMetric):
    """Grades every assertion for a test case in a single LLM call.

    GEval issues one (or two) LLM calls per assertion, which is accurate but
    slow against a local CPU/GPU-bound Ollama judge. This metric mirrors the
    single-call batch grading the legacy bash script used, so an eval with
    N assertions costs one judge call instead of N.
    """

    _required_params: List[SingleTurnParams] = [
        SingleTurnParams.INPUT,
        SingleTurnParams.ACTUAL_OUTPUT,
    ]

    def __init__(
        self,
        assertions: List[str],
        model: OllamaModel,
        threshold: float = 0.8,
        include_reason: bool = True,
    ):
        self.assertions = assertions
        self.model = model
        self.threshold = threshold
        self.include_reason = include_reason
        self.evaluation_model = model.get_model_name()
        self.async_mode = False

    @property
    def __name__(self) -> str:
        return "Batch Assertion Grading"

    def _build_prompt(self, actual_output: str) -> str:
        numbered = "\n".join(
            f"{i}. {assertion}" for i, assertion in enumerate(self.assertions, start=1)
        )
        return GRADE_PROMPT_TEMPLATE.format(
            actual_output=actual_output, numbered_assertions=numbered
        )

    def _score_from_verdicts(self, verdicts: List[dict]) -> None:
        self.verdicts = verdicts
        passed = sum(1 for v in verdicts if v.get("pass"))
        self.score = passed / len(self.assertions)
        if self.include_reason:
            failed = [
                f"- {self.assertions[i]}: {v.get('evidence', '')}"
                for i, v in enumerate(verdicts)
                if not v.get("pass")
            ]
            self.reason = (
                f"{passed}/{len(self.assertions)} assertions passed."
                + ("\nFailed:\n" + "\n".join(failed) if failed else "")
            )
        self.success = self.is_successful()

    def measure(self, test_case: LLMTestCase, *args, **kwargs) -> float:
        prompt = self._build_prompt(test_case.actual_output)
        raw = self.model.generate(prompt, schema=True)
        data = trimAndLoadJson(raw, self)
        verdicts = data.get("verdicts", [])
        if len(verdicts) != len(self.assertions):
            verdicts = (verdicts + [{"pass": False, "evidence": "missing verdict"}] * len(
                self.assertions
            ))[: len(self.assertions)]
        self._score_from_verdicts(verdicts)
        return self.score

    async def a_measure(self, test_case: LLMTestCase, *args, **kwargs) -> float:
        prompt = self._build_prompt(test_case.actual_output)
        raw = await self.model.a_generate(prompt, schema=True)
        data = trimAndLoadJson(raw, self)
        verdicts = data.get("verdicts", [])
        if len(verdicts) != len(self.assertions):
            verdicts = (verdicts + [{"pass": False, "evidence": "missing verdict"}] * len(
                self.assertions
            ))[: len(self.assertions)]
        self._score_from_verdicts(verdicts)
        return self.score
