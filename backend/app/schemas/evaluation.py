"""
Shape of a single answer's evaluation, produced by the Evaluator agent and
consumed by the Interviewer, Orchestrator, and Feedback agent.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class EvaluationRecord:
    question_index: int
    answer: str

    score: float

    correctness: float
    technical_depth: float
    completeness: float
    reasoning: float
    communication: float

    strengths: list[str] = field(
        default_factory=list
    )

    gaps: list[str] = field(
        default_factory=list
    )

    missing_concepts: list[str] = field(
        default_factory=list
    )

    follow_up_needed: bool = False

    suggested_follow_up_area: str = ""