"""
Evaluator Agent (PART 12).

Scores a single candidate answer against the question that was asked,
across several dimensions:

- correctness
- technical depth
- completeness
- reasoning
- communication

It also surfaces:

- strengths
- gaps
- missing concepts
- whether a follow-up is warranted
- suggested follow-up area

These are AI evaluation signals, not ground truth.
"""

from __future__ import annotations

from typing import Optional

from app.core.llm_client import (
    BaseLLMClient,
    LLMError,
    LLMMalformedResponseError,
    get_llm_client,
)
from app.schemas.evaluation import EvaluationRecord
from app.schemas.interview import QuestionRecord
from app.services.curriculum_service import (
    CurriculumService,
    get_curriculum_service,
)
from app.state.interview_state import InterviewState
from app.utils.logger import get_logger


logger = get_logger(__name__)


class EvaluatorAgent:
    def __init__(
        self,
        llm_client: Optional[BaseLLMClient] = None,
        curriculum_service: Optional[CurriculumService] = None,
    ):
        self._llm = (
            llm_client
            or get_llm_client()
        )

        self._curriculum = (
            curriculum_service
            or get_curriculum_service()
        )

    def evaluate(
        self,
        state: InterviewState,
        question: QuestionRecord,
        answer: str,
    ) -> EvaluationRecord:
        """
        Evaluate one candidate answer against the corresponding question.
        """

        day_info = (
            self._curriculum.get_day(
                question.curriculum_day
            )
            if question.curriculum_day is not None
            else {}
        )

        day_info = day_info or {}

        candidate = state.candidate

        objectives = "; ".join(
            day_info.get("objectives", [])
        )

        tools = ", ".join(
            day_info.get("tools", [])
        )

        user_prompt = (
            f"QUESTION ASKED: {question.question}\n"
            f"QUESTION TYPE: {question.question_type} | "
            f"DIFFICULTY: {question.difficulty} | "
            f"TOPIC: {question.topic} "
            f"(Day {question.curriculum_day})\n\n"

            "CURRICULUM CONTEXT:\n"
            f"Objectives: {objectives}\n"
            f"Tools: {tools}\n\n"

            "CANDIDATE BACKGROUND:\n"
            f"{candidate.get('job_role')}, "
            f"{candidate.get('years_experience')} "
            "years experience, "
            f"{candidate.get('education')}\n\n"

            "CANDIDATE'S ANSWER:\n"
            f"{answer}\n\n"

            "Evaluate the candidate's answer now, as JSON."
        )

        try:
            raw = self._llm.generate_json(
                system=_EVALUATOR_SYSTEM_PROMPT,
                user=user_prompt,
            )

            if not isinstance(raw, dict):
                raise LLMMalformedResponseError(
                    "LLM returned a non-object evaluation"
                )

            return self._record_from_llm_output(
                raw,
                question.index,
                answer,
            )

        except (
            LLMError,
            LLMMalformedResponseError,
        ) as exc:
            logger.warning(
                "Evaluator LLM call failed (%s) - "
                "using deterministic fallback evaluation.",
                exc,
            )

            return self._deterministic_fallback(
                question.index,
                answer,
            )

    # ------------------------------------------------------------------
    # LLM output processing
    # ------------------------------------------------------------------

    def _record_from_llm_output(
        self,
        raw: dict,
        question_index: int,
        answer: str,
    ) -> EvaluationRecord:
        """Convert validated LLM output into EvaluationRecord."""

        def _float_value(
            key: str,
            default: float = 0.5,
        ) -> float:
            try:
                return float(
                    raw.get(
                        key,
                        default,
                    )
                )
            except (
                TypeError,
                ValueError,
            ):
                return default

        correctness = _clamp01(
            _float_value("correctness")
        )

        technical_depth = _clamp01(
            _float_value("technical_depth")
        )

        completeness = _clamp01(
            _float_value("completeness")
        )

        reasoning = _clamp01(
            _float_value("reasoning")
        )

        communication = _clamp01(
            _float_value("communication")
        )

        # Prefer the LLM-provided score when valid.
        score = raw.get("score")

        try:
            score = float(score)
        except (
            TypeError,
            ValueError,
        ):
            score = round(
                10
                * (
                    correctness * 0.35
                    + technical_depth * 0.25
                    + completeness * 0.20
                    + reasoning * 0.10
                    + communication * 0.10
                ),
                2,
            )

        score = max(
            0.0,
            min(10.0, score),
        )

        return EvaluationRecord(
            question_index=question_index,
            answer=answer,
            score=score,
            correctness=correctness,
            technical_depth=technical_depth,
            completeness=completeness,
            reasoning=reasoning,
            communication=communication,
            strengths=self._safe_string_list(
                raw.get("strengths")
            ),
            gaps=self._safe_string_list(
                raw.get("gaps")
            ),
            missing_concepts=self._safe_string_list(
                raw.get("missing_concepts")
            ),
            follow_up_needed=bool(
                raw.get(
                    "follow_up_needed",
                    False,
                )
            ),
            suggested_follow_up_area=str(
                raw.get(
                    "suggested_follow_up_area",
                    "",
                )
                or ""
            ),
        )

    # ------------------------------------------------------------------
    # Deterministic fallback
    # ------------------------------------------------------------------

    def _deterministic_fallback(
        self,
        question_index: int,
        answer: str,
    ) -> EvaluationRecord:
        """
        Length-based heuristic used only if the LLM call fails.

        This allows a transient LLM/provider failure to degrade gracefully
        instead of terminating the interview.
        """

        word_count = len(
            answer.split()
        )

        depth_score = _clamp01(
            word_count / 80
        )

        base = 4.0 + 3.0 * depth_score

        gaps = (
            []
            if word_count > 40
            else [
                "Answer was brief; more technical "
                "detail would strengthen it."
            ]
        )

        return EvaluationRecord(
            question_index=question_index,
            answer=answer,
            score=round(base, 2),
            correctness=0.6,
            technical_depth=depth_score,
            completeness=depth_score,
            reasoning=0.6,
            communication=0.6,
            strengths=(
                [
                    "Provided a response addressing "
                    "the question."
                ]
                if word_count > 10
                else []
            ),
            gaps=gaps,
            missing_concepts=[],
            follow_up_needed=word_count < 40,
            suggested_follow_up_area=(
                "more implementation detail"
                if word_count < 40
                else ""
            ),
        )

    @staticmethod
    def _safe_string_list(
        value,
    ) -> list[str]:
        """
        Convert an arbitrary LLM field into a safe list of strings.
        """

        if not isinstance(value, list):
            return []

        return [
            str(item).strip()
            for item in value
            if str(item).strip()
        ]


def _clamp01(
    value: float,
) -> float:
    """Clamp a numeric value to the [0, 1] range."""

    return max(
        0.0,
        min(1.0, value),
    )


_EVALUATOR_SYSTEM_PROMPT = """
You are the evaluation module of a technical interview system.

You assess a single candidate answer against the question that was asked.

You are strict but fair, like a senior engineer grading a real interview,
not a lenient tutor.

Evaluate ONLY what the candidate actually said.

Return ONLY a JSON object.
Do not return prose.
Do not return markdown fences.

The JSON must have exactly this shape:

{
    "score": 0.0,
    "correctness": 0.0,
    "technical_depth": 0.0,
    "completeness": 0.0,
    "reasoning": 0.0,
    "communication": 0.0,
    "strengths": [],
    "gaps": [],
    "missing_concepts": [],
    "follow_up_needed": false,
    "suggested_follow_up_area": ""
}

Scoring:

- score: overall score from 0 to 10
- correctness: 0 to 1
- technical_depth: 0 to 1
- completeness: 0 to 1
- reasoning: 0 to 1
- communication: 0 to 1

Base every field on the actual content of the answer.

Do not invent strengths.
Do not invent gaps.
Do not assume concepts that the candidate did not demonstrate.

A follow-up should be needed when the answer has a meaningful gap,
lacks sufficient depth, contains an unclear technical claim, or would
benefit from deeper probing.

"suggested_follow_up_area" should be a short phrase describing what
should be probed next. Use an empty string when no follow-up is needed.
"""