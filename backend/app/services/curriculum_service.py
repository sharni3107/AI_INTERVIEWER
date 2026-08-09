"""
Loads and caches curriculum + techspec data from disk.

This is the ONLY place that reads curriculum.json / techspec.md from disk.
Agents (planner, interviewer, evaluator) must go through this service instead
of opening files themselves.

curriculum.json is the real, authoritative shape:

{
    "cohort": "AI Cohort · 31 days · 8 modules",
    "modules": [
        {"n": 1, "title": "...", "days": [1, 3]},
        ...
    ],
    "days": [
        {
            "day": 1,
            "title": "...",
            "type": "SETUP",
            "tools": [...],
            "objectives": [...]
        },
        ...
    ]
}

There is NO "topic" field and NO per-day "module" field in the real data.
The module a day belongs to is derived from modules[i].days, which represents
an inclusive [start, end] day range.

The human-readable label for a day is "title", not "topic".
"""

from __future__ import annotations

import json
import os
from functools import lru_cache
from typing import Optional

from app.core.config import settings
from app.utils.logger import get_logger


logger = get_logger(__name__)


class CurriculumLoadError(Exception):
    """Raised when curriculum or techspec data cannot be loaded."""


class CurriculumService:
    def __init__(
        self,
        curriculum_path: Optional[str] = None,
        techspec_path: Optional[str] = None,
    ):
        self._curriculum_path = (
            curriculum_path or settings.curriculum_path
        )
        self._techspec_path = (
            techspec_path or settings.techspec_path
        )

        self._curriculum: Optional[dict] = None
        self._techspec_text: Optional[str] = None

    # ------------------------------------------------------------------
    # Curriculum
    # ------------------------------------------------------------------

    def get_curriculum(self) -> dict:
        """Load and cache curriculum.json."""

        if self._curriculum is None:
            if not os.path.exists(self._curriculum_path):
                raise CurriculumLoadError(
                    f"Curriculum file not found at "
                    f"'{self._curriculum_path}'. "
                    "Set CURRICULUM_PATH or place curriculum.json "
                    "under backend/data/."
                )

            try:
                with open(
                    self._curriculum_path,
                    "r",
                    encoding="utf-8-sig",
                ) as f:
                    self._curriculum = json.load(f)

            except (OSError, json.JSONDecodeError) as exc:
                raise CurriculumLoadError(
                    f"Failed to load curriculum: {exc}"
                ) from exc

        return self._curriculum

    def get_cohort(self) -> str:
        """Return the cohort description."""

        return self.get_curriculum().get("cohort", "")

    def get_modules(self) -> list[dict]:
        """Return all curriculum modules."""

        return self.get_curriculum().get("modules", [])

    def get_days(self) -> list[dict]:
        """Return all curriculum days."""

        return self.get_curriculum().get("days", [])

    def get_day(self, day_number: int) -> Optional[dict]:
        """Return a specific curriculum day."""

        for day in self.get_days():
            if day.get("day") == day_number:
                return day

        return None

    def get_module_for_day(
        self,
        day_number: int,
    ) -> Optional[dict]:
        """
        Return the module containing the specified day.

        Modules store an inclusive [start, end] day range in `days`.
        """

        for module in self.get_modules():
            day_range = module.get("days") or []

            if (
                len(day_range) == 2
                and day_range[0] <= day_number <= day_range[1]
            ):
                return module

        return None

    def get_days_by_type(
        self,
        type_: str,
    ) -> list[dict]:
        """Return curriculum days matching a day type."""

        type_upper = type_.upper()

        return [
            day
            for day in self.get_days()
            if day.get("type", "").upper() == type_upper
        ]

    def get_days_by_keyword(
        self,
        keyword: str,
    ) -> list[dict]:
        """
        Naive keyword match over title/objectives/tools.

        This is a cheap fallback for exact keyword matching.
        Prefer CurriculumRetriever.retrieve() for fuzzy/semantic matching.
        """

        keyword_lower = keyword.lower()
        matches = []

        for day in self.get_days():
            haystack = " ".join(
                [
                    day.get("title", ""),
                    " ".join(day.get("objectives", [])),
                    " ".join(day.get("tools", [])),
                ]
            ).lower()

            if keyword_lower in haystack:
                matches.append(day)

        return matches

    def day_display_title(
        self,
        day_number: int,
    ) -> str:
        """
        Return a human-readable curriculum day label.

        Example:
        [Embeddings & Vector Search] Embeddings Explained
        """

        day = self.get_day(day_number) or {}
        module = self.get_module_for_day(day_number) or {}

        module_title = module.get("title", "")
        title = day.get(
            "title",
            f"Day {day_number}",
        )

        if module_title:
            return f"[{module_title}] {title}"

        return title

    def summarize_for_prompt(
        self,
        day_numbers: Optional[list[int]] = None,
    ) -> str:
        """
        Create a compact, LLM-friendly curriculum summary.

        Uses the real curriculum fields:
        - title
        - type
        - tools
        - objectives

        Module information is derived from modules[].days.
        """

        days = self.get_days()

        if day_numbers:
            days = [
                day
                for day in days
                if day.get("day") in day_numbers
            ]

        lines = []

        for day in days:
            day_number = day.get("day")

            module = (
                self.get_module_for_day(day_number)
                or {}
            )

            objectives = "; ".join(
                day.get("objectives", [])
            )

            tools = ", ".join(
                day.get("tools", [])
            )

            lines.append(
                f"Day {day_number} "
                f"[{module.get('title', 'Unknown Module')}] "
                f"{day.get('title')} "
                f"({day.get('type')}) - "
                f"Tools: {tools} - "
                f"Objectives: {objectives}"
            )

        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Techspec
    # ------------------------------------------------------------------

    def get_techspec_text(self) -> str:
        """Load and cache techspec.md."""

        if self._techspec_text is None:
            if not os.path.exists(self._techspec_path):
                raise CurriculumLoadError(
                    f"Techspec file not found at "
                    f"'{self._techspec_path}'. "
                    "Set TECHSPEC_PATH or place techspec.md "
                    "under backend/data/."
                )

            try:
                with open(
                    self._techspec_path,
                    "r",
                    encoding="utf-8",
                ) as f:
                    self._techspec_text = f.read()

            except OSError as exc:
                raise CurriculumLoadError(
                    f"Failed to load techspec: {exc}"
                ) from exc

        return self._techspec_text


@lru_cache(maxsize=1)
def get_curriculum_service() -> CurriculumService:
    """
    Return the process-wide CurriculumService singleton.

    The curriculum and techspec files are therefore loaded once
    and cached for subsequent requests.
    """

    return CurriculumService()