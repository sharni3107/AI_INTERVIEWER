"""
Shape of a NORMALIZED candidate (the output of
utils/candidate_normalizer.normalize_candidate), used as a type hint
throughout the app.

This is a TypedDict, not a dataclass or Pydantic model, because
InterviewState.candidate is a plain dict end-to-end (it's stored,
copied, and read via `.get(...)` everywhere).

This file exists purely to document that shape in one place,
not to change how it's used at runtime.
"""

from __future__ import annotations

from typing import Any, Optional, TypedDict


class NormalizedCandidate(TypedDict, total=False):
    candidate_id: str
    name: str
    job_role: str
    years_experience: Optional[int]
    education: str
    status: str

    missions: list[dict]
    day_titles: dict[int, str]

    passed_days: list[int]
    failed_days: list[int]
    skipped_days: list[int]
    attempted_days: list[int]
    struggled_days: list[int]

    commit_days: Optional[int]
    missions_completed: Optional[int]
    missions_first_try: Optional[int]

    raw: dict[str, Any]