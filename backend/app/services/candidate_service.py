"""
Candidate service: normalizes candidate payloads and decides, from the
candidate's actual progress + the curriculum, which curriculum day to probe
next.

This replaces what would otherwise be a separate LLM-backed "planner agent".
Day selection is a deterministic decision: pick the next day the candidate
actually engaged with, with weak spots first.

The LLM is reserved for the things that actually benefit from it:
- phrasing the question (interviewer)
- scoring the answer (evaluator)
- writing the final report (feedback)
"""

from __future__ import annotations

from typing import Any, Optional

from app.rag.retriever import (
    CurriculumRetriever,
    get_curriculum_retriever,
)
from app.services.curriculum_service import (
    CurriculumService,
    get_curriculum_service,
)
from app.utils.candidate_normalizer import (
    InvalidCandidateDataError,
    normalize_candidate,
)

__all__ = [
    "InvalidCandidateDataError",
    "normalize_candidate",
    "get_prioritized_days",
]


def get_prioritized_days(
    candidate: dict[str, Any],
    covered_days: set[int],
    curriculum_service: Optional[CurriculumService] = None,
    curriculum_retriever: Optional[CurriculumRetriever] = None,
) -> list[int]:
    """
    Returns curriculum days worth asking about next, in priority order.

    Priority logic:

    1. Eligible pool:
       - days the candidate actually attempted
       - excluding explicitly skipped days
       - excluding days already covered in this session

       If the candidate has no mission data, falls back to all curriculum
       days except skipped days.

    2. Struggled days are prioritized:
       - 3+ attempts
       - or attempted but not passed

       These days represent the candidate's genuine weak areas.

    3. If fewer than two struggled days are available, RAG is used to find
       curriculum days semantically related to the candidate's struggled
       mission titles.

    4. If every eligible day has already been covered, previously covered
       days may be revisited for deeper probing.
    """

    curriculum_service = curriculum_service or get_curriculum_service()
    curriculum_retriever = (
        curriculum_retriever or get_curriculum_retriever()
    )

    passed = set(candidate.get("passed_days", []))
    failed = set(candidate.get("failed_days", []))
    skipped = set(candidate.get("skipped_days", []))

    all_days = {
        day["day"]
        for day in curriculum_service.get_days()
    }

    # Candidate-engaged curriculum days.
    pool = (passed | failed) - skipped

    # If candidate progress is unavailable, use all non-skipped days.
    if not pool:
        pool = all_days - skipped

    # Last resort: use every curriculum day.
    if not pool:
        pool = all_days

    # Avoid repeating days already covered in the current session.
    remaining = sorted(pool - covered_days)

    # If everything eligible has already been covered, allow revisiting
    # days for deeper probing.
    if not remaining:
        remaining = sorted(pool) or sorted(all_days)

    # Candidate's known weak areas.
    struggled = set(candidate.get("struggled_days", []))

    struggled_days = [
        day
        for day in remaining
        if day in struggled
    ]

    other_days = [
        day
        for day in remaining
        if day not in struggled
    ]

    # If there are not enough exact struggled days, use RAG to discover
    # semantically related curriculum days.
    if len(struggled_days) < 2:
        day_titles = candidate.get("day_titles", {})

        queries = [
            day_titles[day]
            for day in candidate.get("struggled_days", [])
            if day_titles.get(day)
        ]

        if queries:
            rag_days = (
                curriculum_retriever
                .retrieve_days_for_topics(queries)
            )

            rag_days = [
                day
                for day in rag_days
                if day in remaining
            ]

            for day in rag_days:
                if day not in struggled_days:
                    struggled_days.append(day)

            other_days = [
                day
                for day in other_days
                if day not in struggled_days
            ]

    return struggled_days + other_days