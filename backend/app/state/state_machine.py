"""
Deterministic decision vocabulary + guardrails for the adaptive interview
flow.

The actual decision of "follow up, move on, or finish" is made in plain
Python (app/agents/orchestrator.py) using these helpers.

There is no separate LLM-backed "planner agent".

Picking a curriculum day and deciding whether to follow up does not need
a model call. Only the content of the next question requires the
Interviewer agent.
"""

from __future__ import annotations

from enum import Enum

from app.core.config import settings
from app.state.interview_state import InterviewState


DIFFICULTY_LEVELS = [
    "easy",
    "medium",
    "hard",
]


class TurnDecision(str, Enum):
    FOLLOW_UP = "FOLLOW_UP"
    NEW_TOPIC = "NEW_TOPIC"
    COMPLETE = "COMPLETE"


def clamp_difficulty(
    current: str,
    direction: int,
) -> str:
    """
    Adjust difficulty by one level.

    direction:
        +1 -> increase difficulty
        -1 -> decrease difficulty
         0 -> keep difficulty unchanged

    The result is always one of:
        easy, medium, hard
    """

    if current not in DIFFICULTY_LEVELS:
        current = "medium"

    index = DIFFICULTY_LEVELS.index(current)

    index = max(
        0,
        min(
            len(DIFFICULTY_LEVELS) - 1,
            index + direction,
        ),
    )

    return DIFFICULTY_LEVELS[index]


def difficulty_shift_for_score(
    score: float,
) -> int:
    """
    Determine how difficulty should change based on an evaluation score.

    Score >= 8:
        Increase difficulty.

    Score <= 4:
        Decrease difficulty.

    Otherwise:
        Keep difficulty unchanged.
    """

    if score >= 8:
        return 1

    if score <= 4:
        return -1

    return 0


def can_force_complete(
    state: InterviewState,
) -> bool:
    """
    Hard safety ceiling.

    Prevents an interview from exceeding max_questions even if
    repeated follow-ups would otherwise continue indefinitely.
    """

    return len(state.questions) >= settings.max_questions


def meets_completion_floor(
    state: InterviewState,
) -> bool:
    """
    Determine whether the minimum requirements for completing the
    interview have been satisfied.

    Requirements:
        - minimum number of questions
        - minimum number of unique curriculum days covered
    """

    return state.meets_minimum_requirements(
        min_questions=settings.min_questions,
        min_days=settings.min_curriculum_days,
    )