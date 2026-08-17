import os

import httpx
from deepeval.models.base_model import DeepEvalBaseLLM

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2")
OLLAMA_JUDGE_MODEL = os.environ.get("OLLAMA_JUDGE_MODEL", "mistral")
# Running evals concurrently (pytest -n) puts multiple requests on the same
# local GPU, which increases per-request latency under contention — give
# each request enough headroom to finish rather than fail with a timeout.
OLLAMA_REQUEST_TIMEOUT = float(os.environ.get("OLLAMA_REQUEST_TIMEOUT", "900"))


class OllamaModel(DeepEvalBaseLLM):
    def __init__(self, model_name: str, base_url: str = OLLAMA_URL):
        self.base_url = base_url
        super().__init__(model_name)

    def load_model(self):
        return self.name

    def _payload(self, prompt: str, schema, system: str | None) -> dict:
        payload = {"model": self.name, "prompt": prompt, "stream": False}
        if schema is not None:
            payload["format"] = "json"
        if system is not None:
            payload["system"] = system
        return payload

    def generate(self, prompt: str, schema=None, system: str | None = None) -> str:
        response = httpx.post(
            f"{self.base_url}/api/generate",
            json=self._payload(prompt, schema, system),
            timeout=OLLAMA_REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        return response.json().get("response", "")

    async def a_generate(
        self, prompt: str, schema=None, system: str | None = None
    ) -> str:
        async with httpx.AsyncClient(timeout=OLLAMA_REQUEST_TIMEOUT) as client:
            response = await client.post(
                f"{self.base_url}/api/generate",
                json=self._payload(prompt, schema, system),
            )
            response.raise_for_status()
            return response.json().get("response", "")

    def get_model_name(self) -> str:
        return self.name


def under_test_model() -> OllamaModel:
    return OllamaModel(OLLAMA_MODEL)


def judge_model() -> OllamaModel:
    return OllamaModel(OLLAMA_JUDGE_MODEL)
