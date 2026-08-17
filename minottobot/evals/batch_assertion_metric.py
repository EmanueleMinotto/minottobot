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

Assertions come in two kinds, and they are judged by opposite rules:

- **Requirements** ("Output must ...") demand the presence of something. Be strict:
  pass only if the audit output explicitly and completely contains it. When in
  doubt, fail. Evidence is a direct quote of the part that satisfies it.
- **Prohibitions** ("Output must not ...") demand the absence of something. They
  are satisfied by default. Fail one ONLY if you can quote the specific sentence
  in the audit output that commits the prohibited act. If you cannot produce that
  quote, the assertion passes. Never fail a prohibition because the output is
  silent on the topic — silence is exactly what a prohibition requires.

Assertions:
{numbered_assertions}

Return ONLY a JSON object of this exact shape, with one verdict per assertion, in the
same order as listed above:
{{"verdicts": [{{"pass": true, "evidence": "direct quote or brief justification"}}, ...]}}

For a failed prohibition, "evidence" MUST be the verbatim offending quote from the
audit output. An empty or paraphrased evidence string means you have no violation to
report, so the verdict must be true.
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

    @staticmethod
    def _is_prohibition(assertion: str) -> bool:
        return "must not" in assertion.lower()

    def _acquit_unevidenced_prohibitions(
        self, verdicts: List[dict], actual_output: str
    ) -> List[dict]:
        """Overturn prohibition failures the judge cannot back with a quote.

        Judges are heavily biased against "must not ..." assertions: they are
        satisfied by absence, so nothing in the output ever looks like positive
        proof and the verdict defaults to fail. Measured on this suite, "must
        not recommend psychological safety" failed 10/10 gradings on outputs
        where neither word appeared at all.

        A prohibition is only genuinely violated if the offending text exists,
        so we require the judge's evidence to be a quote actually found in the
        output. No quote, no violation.
        """
        haystack = " ".join(actual_output.lower().split())
        for verdict, assertion in zip(verdicts, self.assertions):
            if verdict.get("pass") or not self._is_prohibition(assertion):
                continue
            quote = " ".join(str(verdict.get("evidence", "")).lower().split())
            if len(quote) < 15 or quote not in haystack:
                verdict["pass"] = True
                verdict["evidence"] = (
                    "acquitted: judge cited no verbatim quote from the output"
                )
        return verdicts

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
        verdicts = self._acquit_unevidenced_prohibitions(
            verdicts, test_case.actual_output
        )
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
        verdicts = self._acquit_unevidenced_prohibitions(
            verdicts, test_case.actual_output
        )
        self._score_from_verdicts(verdicts)
        return self.score
