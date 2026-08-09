"""
Defines the shape of a single interview session's state.

This is plain, serializable data - no business logic lives here. The
orchestrator reads/writes this object; state_manager owns its lifecycle
(creation, lookup, persistence-for-the-process-lifetime - in-memory only,
per the hackathon scope: no database, no persistent accounts).
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional

from app.schemas.evaluation import EvaluationRecord
from app.schemas.interview import QuestionRecord


__all__ = [
    "InterviewStatus",
    "QuestionRecord",
    "EvaluationRecord",
    "InterviewState",
]


class InterviewStatus(str, Enum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


@dataclass
class InterviewState:
    session_id: str
    candidate: dict[str, Any]

    interview_status: InterviewStatus = (
        InterviewStatus.IN_PROGRESS
    )

    question_count: int = 0

    current_question: Optional[QuestionRecord] = None
    current_topic: Optional[str] = None
    current_curriculum_day: Optional[int] = None
    current_difficulty: str = "medium"

    questions: list[QuestionRecord] = field(
        default_factory=list
    )

    evaluations: list[EvaluationRecord] = field(
        default_factory=list
    )

    covered_curriculum_days: set[int] = field(
        default_factory=set
    )

    covered_topics: set[str] = field(
        default_factory=set
    )

    strengths: list[str] = field(
        default_factory=list
    )

    gaps: list[str] = field(
        default_factory=list
    )

    # Chronological log of:
    # {"role": "interviewer"|"candidate", "content": str}
    #
    # This provides multi-turn conversation context for the lifetime
    # of this in-memory interview session.
    interview_history: list[dict[str, str]] = field(
        default_factory=list
    )

    feedback: Optional[dict[str, Any]] = None

    created_at: float = field(
        default_factory=time.time
    )

    updated_at: float = field(
        default_factory=time.time
    )

    def touch(self) -> None:
        """Update the session's last-modified timestamp."""

        self.updated_at = time.time()

    def record_question(
        self,
        q: QuestionRecord,
    ) -> None:
        """Record a newly generated interview question."""

        self.current_question = q
        self.current_topic = q.topic
        self.current_curriculum_day = q.curriculum_day
        self.current_difficulty = q.difficulty

        self.questions.append(q)
        self.question_count = len(self.questions)

        if q.curriculum_day is not None:
            self.covered_curriculum_days.add(
                q.curriculum_day
            )

        if q.topic:
            self.covered_topics.add(q.topic)

        self.interview_history.append(
            {
                "role": "interviewer",
                "content": q.question,
            }
        )

        self.touch()

    def record_answer_and_evaluation(
        self,
        answer: str,
        evaluation: EvaluationRecord,
    ) -> None:
        """
        Record the candidate's answer and the evaluation generated
        for that answer.
        """

        self.evaluations.append(evaluation)

        self.strengths.extend(
            evaluation.strengths
        )

        self.gaps.extend(
            evaluation.gaps
        )

        self.interview_history.append(
            {
                "role": "candidate",
                "content": answer,
            }
        )

        self.touch()

    def mark_completed(
        self,
        feedback: dict[str, Any],
    ) -> None:
        """Mark the interview as completed and store final feedback."""

        self.interview_status = InterviewStatus.COMPLETED
        self.feedback = feedback
        self.touch()

    def meets_minimum_requirements(
        self,
        min_questions: int,
        min_days: int,
    ) -> bool:
        """
        Return True when the interview has satisfied both minimum
        question and curriculum-day requirements.
        """

        return (
            len(self.questions) >= min_questions
            and len(self.covered_curriculum_days) >= min_days
        )