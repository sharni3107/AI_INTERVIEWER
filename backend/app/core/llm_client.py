"""
LLM abstraction layer.

Every agent (interviewer, evaluator, feedback) talks to this module only.
No agent imports an HTTP/SDK client directly and no agent reads environment
variables.

Provider:
    OpenRouter, using its OpenAI-compatible /chat/completions endpoint.

Default model:
    openai/gpt-4o-mini

A mock provider is also available for local development and tests.
"""

from __future__ import annotations

import json
import re
from abc import ABC, abstractmethod
from typing import Any, Optional

from app.core.config import settings
from app.utils.logger import get_logger


logger = get_logger(__name__)


class LLMError(Exception):
    """Raised when the LLM cannot produce a usable response."""


class LLMMalformedResponseError(LLMError):
    """Raised when the LLM response cannot be parsed correctly."""


class BaseLLMClient(ABC):
    """Common interface every LLM provider implementation must satisfy."""

    @abstractmethod
    def generate_text(
        self,
        system: str,
        user: str,
    ) -> str:
        """Return a raw text completion."""
        raise NotImplementedError

    def generate_json(
        self,
        system: str,
        user: str,
    ) -> dict:
        """
        Generate a completion expected to contain a single JSON object.

        Markdown code fences are stripped defensively.
        """

        raw = self.generate_text(
            system=system,
            user=user,
        )

        return _parse_json_response(raw)


def _parse_json_response(raw: str) -> dict:
    """Parse a JSON object from an LLM response."""

    if raw is None:
        raise LLMMalformedResponseError(
            "LLM returned an empty response."
        )

    text = raw.strip()

    # Remove ```json ... ``` or ``` ... ``` fences.
    fence_match = re.search(
        r"```(?:json)?\s*(.*?)\s*```",
        text,
        re.DOTALL,
    )

    if fence_match:
        text = fence_match.group(1).strip()

    # If there is leading/trailing prose, isolate the outer JSON object.
    if not text.startswith("{"):
        brace_start = text.find("{")
        brace_end = text.rfind("}")

        if (
            brace_start != -1
            and brace_end != -1
            and brace_end > brace_start
        ):
            text = text[
                brace_start : brace_end + 1
            ]

    try:
        result = json.loads(text)
    except json.JSONDecodeError as exc:
        logger.error(
            "Failed to parse LLM JSON response: %s | raw=%r",
            exc,
            raw,
        )

        raise LLMMalformedResponseError(
            f"Could not parse LLM response as JSON: {exc}"
        ) from exc

    if not isinstance(result, dict):
        raise LLMMalformedResponseError(
            "LLM response JSON must be an object."
        )

    return result


class OpenRouterLLMClient(BaseLLMClient):
    """
    Thin wrapper around OpenRouter's OpenAI-compatible
    /chat/completions endpoint.

    Uses httpx directly instead of the OpenAI or Anthropic SDK.
    """

    def __init__(
        self,
        api_key: str,
        model: str,
        base_url: str,
        max_tokens: int,
        temperature: float,
    ):
        if not api_key:
            raise LLMError(
                "OPENROUTER_API_KEY is not set. "
                "Set it in the environment or .env file, "
                "or use LLM_PROVIDER=mock."
            )

        self._api_key = api_key
        self._model = model
        self._base_url = base_url.rstrip("/")
        self._max_tokens = max_tokens
        self._temperature = temperature

    def generate_text(
        self,
        system: str,
        user: str,
    ) -> str:
        import httpx

        try:
            response = httpx.post(
                f"{self._base_url}/chat/completions",
                headers={
                    "Authorization": (
                        f"Bearer {self._api_key}"
                    ),
                    "Content-Type": "application/json",
                },
                json={
                    "model": self._model,
                    "max_tokens": self._max_tokens,
                    "temperature": self._temperature,
                    "messages": [
                        {
                            "role": "system",
                            "content": system,
                        },
                        {
                            "role": "user",
                            "content": user,
                        },
                    ],
                },
                timeout=60.0,
            )

            response.raise_for_status()
            data = response.json()

        except httpx.HTTPStatusError as exc:
            logger.error(
                "OpenRouter API call failed: %s | body=%s",
                exc,
                exc.response.text[:500],
            )

            raise LLMError(
                f"LLM provider call failed: {exc}"
            ) from exc

        except Exception as exc:
            logger.error(
                "OpenRouter API call failed: %s",
                exc,
            )

            raise LLMError(
                f"LLM provider call failed: {exc}"
            ) from exc

        try:
            content = data[
                "choices"
            ][0][
                "message"
            ]["content"]

        except (
            KeyError,
            IndexError,
            TypeError,
        ) as exc:
            raise LLMMalformedResponseError(
                "Unexpected OpenRouter response shape: "
                f"{data}"
            ) from exc

        if not content or not str(content).strip():
            raise LLMMalformedResponseError(
                "LLM response contained no text content."
            )

        return str(content)


class MockLLMClient(BaseLLMClient):
    """
    Deterministic, offline-friendly LLM stand-in.

    A custom responder can be injected for tests:

        responder(system, user) -> str
    """

    def __init__(
        self,
        responder: Optional[Any] = None,
    ):
        self._responder = responder
        self.call_log: list[dict] = []

    def generate_text(
        self,
        system: str,
        user: str,
    ) -> str:
        self.call_log.append(
            {
                "system": system,
                "user": user,
            }
        )

        if self._responder is not None:
            return self._responder(
                system,
                user,
            )

        return json.dumps(
            _default_mock_reply(
                system,
                user,
            )
        )


def _default_mock_reply(
    system: str,
    user: str,
) -> dict:
    """
    Very small heuristic mock so the pipeline can run end-to-end
    without an external LLM.
    """

    lowered = (
        system + user
    ).lower()

    if (
        "generate the single next interview question"
        in lowered
        or '"question"' in lowered
    ):
        return {
            "question": (
                "Can you walk me through how "
                "your system decides what to retrieve?"
            ),
            "topic": (
                "Retrieval-Augmented Generation"
            ),
            "curriculum_day": 5,
            "difficulty": "medium",
            "question_type": "conceptual",
            "is_follow_up": False,
            "reason": (
                "Mock default question - "
                "no responder configured."
            ),
        }

    if (
        "evaluate the candidate" in lowered
        or '"correctness"' in lowered
    ):
        return {
            "score": 6.0,
            "correctness": 0.6,
            "technical_depth": 0.6,
            "completeness": 0.6,
            "reasoning": 0.6,
            "communication": 0.7,
            "strengths": [
                "Communicated the general idea clearly"
            ],
            "gaps": [
                "Did not go into implementation detail"
            ],
            "missing_concepts": [],
            "follow_up_needed": True,
            "suggested_follow_up_area": (
                "implementation detail"
            ),
        }

    if (
        '"summary"' in lowered
        or "final feedback" in lowered
    ):
        return {
            "summary": "Mock feedback summary.",
            "strengths": ["Mock strength"],
            "gaps": ["Mock gap"],
            "next": ["Mock next step"],
        }

    return {
        "reply": "Mock response."
    }


_llm_singleton: Optional[
    BaseLLMClient
] = None


def get_llm_client(
    force_new: bool = False,
) -> BaseLLMClient:
    """
    Factory returning the configured LLM client.

    The client is cached as a singleton unless
    force_new=True.
    """

    global _llm_singleton

    if (
        _llm_singleton is not None
        and not force_new
    ):
        return _llm_singleton

    provider = settings.llm_provider.lower()

    if provider == "mock":
        client: BaseLLMClient = (
            MockLLMClient()
        )

    elif provider == "openrouter":
        client = OpenRouterLLMClient(
            api_key=settings.openrouter_api_key,
            model=settings.llm_model,
            base_url=settings.openrouter_base_url,
            max_tokens=settings.llm_max_tokens,
            temperature=settings.llm_temperature,
        )

    else:
        raise LLMError(
            f"Unknown LLM_PROVIDER "
            f"'{settings.llm_provider}'. "
            "Expected 'openrouter' or 'mock'."
        )

    _llm_singleton = client

    return client


def set_llm_client(
    client: BaseLLMClient,
) -> None:
    """
    Override the singleton.

    Primarily useful for tests that need to inject
    a scripted mock client.
    """

    global _llm_singleton

    _llm_singleton = client