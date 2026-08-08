"""
Central configuration for the AI Interview Agent backend.

All environment-driven settings live here so that no other module reads
os.environ directly. Nothing in this file hardcodes secrets.
"""

import os
from dataclasses import dataclass, field


def _get_bool(name: str, default: bool) -> bool:
    val = os.environ.get(name)
    if val is None:
        return default
    return val.strip().lower() in ("1", "true", "yes", "on")


def _get_int(name: str, default: int) -> int:
    val = os.environ.get(name)
    if val is None:
        return default

    try:
        return int(val)
    except ValueError:
        return default


@dataclass(frozen=True)
class Settings:

    # --- LLM provider configuration ----------------------------------------

    llm_provider: str = field(
        default_factory=lambda: os.environ.get(
            "LLM_PROVIDER",
            "openrouter"
        )
    )

    llm_model: str = field(
        default_factory=lambda: os.environ.get(
            "LLM_MODEL",
            "openai/gpt-4o-mini"
        )
    )

    openrouter_api_key: str = field(
        default_factory=lambda: os.environ.get(
            "OPENROUTER_API_KEY",
            ""
        )
    )

    llm_max_tokens: int = field(
        default_factory=lambda: _get_int(
            "LLM_MAX_TOKENS",
            1024
        )
    )

    llm_temperature: float = field(
        default_factory=lambda: float(
            os.environ.get(
                "LLM_TEMPERATURE",
                "0.4"
            )
        )
    )

    # --- Interview rules --------------------------------------------------

    min_questions: int = field(
        default_factory=lambda: _get_int(
            "INTERVIEW_MIN_QUESTIONS",
            8
        )
    )

    min_curriculum_days: int = field(
        default_factory=lambda: _get_int(
            "INTERVIEW_MIN_DAYS",
            4
        )
    )

    # --- Data locations ---------------------------------------------------

    curriculum_path: str = field(
        default_factory=lambda: os.environ.get(
            "CURRICULUM_PATH",
            os.path.join("data", "curriculum.json")
        )
    )

    techspec_path: str = field(
        default_factory=lambda: os.environ.get(
            "TECHSPEC_PATH",
            os.path.join("data", "techspec.md")
        )
    )

    # --- Misc -------------------------------------------------------------

    debug: bool = field(
        default_factory=lambda: _get_bool(
            "DEBUG",
            False
        )
    )


settings = Settings()
