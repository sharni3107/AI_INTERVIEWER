"""
Central configuration for the AI Interview Agent backend.

All environment-driven settings live here.
No other module should read os.environ directly.
"""

import os
from dataclasses import dataclass, field


try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


def _get_bool(name: str, default: bool) -> bool:
    value = os.environ.get(name)

    if value is None:
        return default

    return value.strip().lower() in ("1", "true", "yes", "on")


def _get_int(name: str, default: int) -> int:
    value = os.environ.get(name)

    if value is None:
        return default

    try:
        return int(value)
    except ValueError:
        return default


@dataclass(frozen=True)
class Settings:
    # ------------------------------------------------------------------
    # LLM configuration
    # ------------------------------------------------------------------

    # "openrouter" is the production provider.
    # "mock" can be used for offline tests.
    llm_provider: str = field(
        default_factory=lambda: os.environ.get(
            "LLM_PROVIDER",
            "openrouter",
        )
    )

    openrouter_api_key: str = field(
        default_factory=lambda: os.environ.get(
            "OPENROUTER_API_KEY",
            "",
        )
    )

    openrouter_base_url: str = field(
        default_factory=lambda: os.environ.get(
            "OPENROUTER_BASE_URL",
            "https://openrouter.ai/api/v1",
        )
    )

    # GPT-4o Mini through OpenRouter.
    llm_model: str = field(
        default_factory=lambda: os.environ.get(
            "LLM_MODEL",
            "openai/gpt-4o-mini",
        )
    )

    llm_max_tokens: int = field(
        default_factory=lambda: _get_int(
            "LLM_MAX_TOKENS",
            1024,
        )
    )

    llm_temperature: float = field(
        default_factory=lambda: float(
            os.environ.get(
                "LLM_TEMPERATURE",
                "0.4",
            )
        )
    )

    # ------------------------------------------------------------------
    # Interview requirements
    # ------------------------------------------------------------------

    min_questions: int = field(
        default_factory=lambda: _get_int(
            "INTERVIEW_MIN_QUESTIONS",
            8,
        )
    )

    min_curriculum_days: int = field(
        default_factory=lambda: _get_int(
            "INTERVIEW_MIN_DAYS",
            4,
        )
    )

    # Safety limit to prevent an interview from continuing indefinitely.
    max_questions: int = field(
        default_factory=lambda: _get_int(
            "INTERVIEW_MAX_QUESTIONS",
            16,
        )
    )

    # ------------------------------------------------------------------
    # Data
    # ------------------------------------------------------------------

    curriculum_path: str = field(
        default_factory=lambda: os.environ.get(
            "CURRICULUM_PATH",
            os.path.join("data", "curriculum.json"),
        )
    )

    techspec_path: str = field(
        default_factory=lambda: os.environ.get(
            "TECHSPEC_PATH",
            os.path.join("data", "techspec.md"),
        )
    )

    # ------------------------------------------------------------------
    # Miscellaneous
    # ------------------------------------------------------------------

    debug: bool = field(
        default_factory=lambda: _get_bool(
            "DEBUG",
            False,
        )
    )


settings = Settings()
