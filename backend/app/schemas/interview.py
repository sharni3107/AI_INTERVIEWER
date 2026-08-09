
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from pydantic import BaseModel, Field


@dataclass
class QuestionRecord:
    index: int
    question: str
    topic: str
    curriculum_day: Optional[int]
    difficulty: str
    question_type: str
    is_follow_up: bool
    reason: str = ""


class InterviewRequest(BaseModel):
    sessionId: str = Field(..., min_length=1)
    candidate: Optional[dict[str, Any]] = None
    message: Optional[str] = None


class FeedbackSchema(BaseModel):
    summary: str
    strengths: list[str]
    gaps: list[str]
    next: list[str]


class InterviewResponse(BaseModel):
    reply: str
    done: bool
    feedback: Optional[FeedbackSchema] = None


class ErrorResponse(BaseModel):
    error: str
    detail: str