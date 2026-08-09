"""
Interviewer Agent.

Generates exactly one interview question at a time, grounded in:

- the target curriculum day + difficulty + objective
- the candidate's profile
- the prior question/answer/evaluation
- what's already been asked

No predefined question bank - every question is produced by the LLM.
The LLM never reveals answers or gives hints.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from app.core.llm_client import (
    BaseLLMClient,
    LLMError,
    LLMMalformedResponseError,
    get_llm_client,
)
from app.schemas.interview import QuestionRecord
from app.services.curriculum_service import (
    CurriculumService,
    get_curriculum_service,
)
from app.state.interview_state import InterviewState
from app.utils.logger import get_logger


logger = get_logger(__name__)


@dataclass
class GeneratedQuestion:
    question: str
    topic: str
    curriculum_day: Optional[int]
    difficulty: str
    question_type: str
    is_follow_up: bool
    reason: str = ""


class InterviewerAgent:
    def __init__(
        self,
        llm_client: Optional[BaseLLMClient] = None,
        curriculum_service: Optional[CurriculumService] = None,
    ):
        self._llm = llm_client or get_llm_client()
        self._curriculum = (
            curriculum_service or get_curriculum_service()
        )

    def generate_question(
        self,
        state: InterviewState,
        curriculum_day: Optional[int],
        difficulty: str,
        is_follow_up: bool,
        objective: str,
    ) -> GeneratedQuestion:
        """
        Generate exactly one interview question.
        """

        if curriculum_day is not None:
            day_info = self._curriculum.get_day(
                curriculum_day
            ) or {}
        else:
            day_info = {}

        topic_fallback = day_info.get(
            "title",
            "General AI Engineering",
        )

        user_prompt = self._build_prompt(
            state=state,
            day_info=day_info,
            difficulty=difficulty,
            is_follow_up=is_follow_up,
            objective=objective,
        )

        try:
            raw = self._llm.generate_json(
                system=_INTERVIEWER_SYSTEM_PROMPT,
                user=user_prompt,
            )

            if not isinstance(raw, dict):
                raise LLMMalformedResponseError(
                    "LLM returned a non-object response"
                )

            question_text = str(
                raw.get("question", "")
            ).strip()

            if not question_text:
                raise LLMMalformedResponseError(
                    "LLM returned an empty question"
                )

            if self._is_repeat(
                question_text,
                state,
            ):
                logger.warning(
                    "Interviewer produced a duplicate question. "
                    "Using deterministic fallback."
                )

                question_text = self._deterministic_question(
                    day_info=day_info,
                    is_follow_up=is_follow_up,
                    state=state,
                    topic_fallback=topic_fallback,
                )

            return GeneratedQuestion(
                question=question_text,
                topic=str(
                    raw.get("topic")
                    or topic_fallback
                ),
                curriculum_day=self._safe_curriculum_day(
                    raw.get("curriculum_day"),
                    curriculum_day,
                ),
                difficulty=self._safe_difficulty(
                    raw.get("difficulty"),
                    difficulty,
                ),
                question_type=self._safe_question_type(
                    raw.get("question_type")
                ),
                is_follow_up=bool(
                    raw.get(
                        "is_follow_up",
                        is_follow_up,
                    )
                ),
                reason=str(
                    raw.get("reason")
                    or objective
                ),
            )

        except (
            LLMError,
            LLMMalformedResponseError,
        ) as exc:
            logger.warning(
                "Interviewer LLM call failed (%s). "
                "Using deterministic fallback question.",
                exc,
            )

            question_text = self._deterministic_question(
                day_info=day_info,
                is_follow_up=is_follow_up,
                state=state,
                topic_fallback=topic_fallback,
            )

            return GeneratedQuestion(
                question=question_text,
                topic=topic_fallback,
                curriculum_day=curriculum_day,
                difficulty=difficulty,
                question_type="conceptual",
                is_follow_up=is_follow_up,
                reason=objective,
            )

    def to_question_record(
        self,
        generated: GeneratedQuestion,
        index: int,
    ) -> QuestionRecord:
        """
        Convert GeneratedQuestion into QuestionRecord.
        """

        return QuestionRecord(
            index=index,
            question=generated.question,
            topic=generated.topic,
            curriculum_day=generated.curriculum_day,
            difficulty=generated.difficulty,
            question_type=generated.question_type,
            is_follow_up=generated.is_follow_up,
            reason=generated.reason,
        )

    def _build_prompt(
        self,
        state: InterviewState,
        day_info: dict,
        difficulty: str,
        is_follow_up: bool,
        objective: str,
    ) -> str:
        """
        Build the prompt sent to the interviewer LLM.
        """

        last_question = (
            state.questions[-1]
            if state.questions
            else None
        )

        last_evaluation = (
            state.evaluations[-1]
            if state.evaluations
            else None
        )

        last_answer = None

        if state.interview_history:
            last_message = state.interview_history[-1]

            if last_message.get("role") == "candidate":
                last_answer = last_message.get(
                    "content"
                )

        if state.questions:
            asked_so_far = "\n".join(
                f"- {question.question}"
                for question in state.questions
            )
        else:
            asked_so_far = "None yet."

        candidate = state.candidate

        objectives = "; ".join(
            day_info.get("objectives", [])
        )

        tools = ", ".join(
            day_info.get("tools", [])
        )

        previous_question = (
            last_question.question
            if last_question
            else "None (this is the opening question)."
        )

        evaluation_summary = self._eval_summary(
            last_evaluation
        )

        prompt = (
            "CANDIDATE BACKGROUND:\n"
            f"name={candidate.get('name')}\n"
            f"job_role={candidate.get('job_role')}\n"
            f"years_experience="
            f"{candidate.get('years_experience')}\n"
            f"education={candidate.get('education')}\n\n"

            "CURRICULUM DAY CONTEXT:\n"
            f"Day {day_info.get('day')} - "
            f"{day_info.get('title')}\n"
            f"Objectives: {objectives}\n"
            f"Tools: {tools}\n\n"

            "PLAN FOR THIS TURN:\n"
            f"objective={objective}\n"
            f"target_difficulty={difficulty}\n"
            f"is_follow_up={is_follow_up}\n\n"

            f"PREVIOUS QUESTION: {previous_question}\n\n"

            f"CANDIDATE'S ANSWER: "
            f"{last_answer or 'N/A'}\n\n"

            f"EVALUATION OF THAT ANSWER: "
            f"{evaluation_summary}\n\n"

            "QUESTIONS ALREADY ASKED "
            "(do not repeat these or ask something "
            "near-identical):\n"
            f"{asked_so_far}\n\n"

            "Generate the single next interview question "
            "now, as JSON."
        )

        return prompt

    @staticmethod
    def _eval_summary(
        evaluation,
    ) -> str:
        """
        Convert the latest evaluation into compact prompt context.
        """

        if not evaluation:
            return "N/A"

        return (
            f"score={evaluation.score}, "
            f"gaps={evaluation.gaps}, "
            f"missing_concepts="
            f"{evaluation.missing_concepts}, "
            f"suggested_follow_up_area="
            f"'{evaluation.suggested_follow_up_area}'"
        )

    @staticmethod
    def _is_repeat(
        question_text: str,
        state: InterviewState,
    ) -> bool:
        """
        Check whether the generated question is an exact duplicate.
        """

        normalized = question_text.strip().lower()

        for question in state.questions:
            existing = (
                question.question.strip().lower()
            )

            if existing == normalized:
                return True

        return False

    @staticmethod
    def _deterministic_question(
        day_info: dict,
        is_follow_up: bool,
        state: InterviewState,
        topic_fallback: str,
    ) -> str:
        """
        Fallback question used if the LLM is unavailable.
        """

        if is_follow_up and state.evaluations:
            area = (
                state.evaluations[-1]
                .suggested_follow_up_area
            )

            if not area:
                area = "that point"

            return (
                f"Can you go deeper into {area} "
                "and explain how you would handle "
                "it in production?"
            )

        objectives = day_info.get(
            "objectives",
            [],
        )

        if objectives:
            objective_hint = objectives[0]
        else:
            objective_hint = topic_fallback

        return (
            f"Can you explain {objective_hint.lower()} "
            "and walk me through how you applied "
            "it in your work?"
        )

    @staticmethod
    def _safe_difficulty(
        value,
        fallback: str,
    ) -> str:
        """
        Validate the difficulty returned by the LLM.
        """

        allowed = {
            "easy",
            "medium",
            "hard",
        }

        value = str(value or "").lower()

        if value in allowed:
            return value

        return fallback

    @staticmethod
    def _safe_question_type(
        value,
    ) -> str:
        """
        Validate the question type returned by the LLM.
        """

        allowed = {
            "conceptual",
            "implementation",
            "architecture",
            "why",
            "how",
            "trade-off",
            "scenario",
            "project",
        }

        value = str(value or "").lower()

        if value in allowed:
            return value

        return "conceptual"

    @staticmethod
    def _safe_curriculum_day(
        value,
        fallback: Optional[int],
    ) -> Optional[int]:
        """
        Validate curriculum_day returned by the LLM.
        """

        if value is None:
            return fallback

        try:
            return int(value)
        except (
            TypeError,
            ValueError,
        ):
            return fallback


_INTERVIEWER_SYSTEM_PROMPT = """
You are a senior technical interviewer conducting a live,
adaptive technical interview for an AI engineering cohort graduate.

You ask exactly ONE question at a time.

Behave like a real senior interviewer:

- Ask conceptual, implementation, architecture, why, how,
  trade-off, and scenario-based questions.
- Reference the candidate's own project/background where it
  supports a good question.
- Probe weak answers by asking for more specifics.
- Challenge strong answers with a harder follow-up.
- Never reveal answers.
- Never give hints.
- Never explain the concept for the candidate.
- Never repeat a question that was already asked.
- Do not behave like a tutor.
- Do not pad the question with encouragement or exposition.

Return ONLY a JSON object.

Do not return prose.
Do not return markdown fences.

Use exactly this shape:

{
    "question": "",
    "topic": "",
    "curriculum_day": null,
    "difficulty": "medium",
    "question_type": "conceptual",
    "is_follow_up": false,
    "reason": ""
}

Allowed difficulty values:

- easy
- medium
- hard

Allowed question_type values:

- conceptual
- implementation
- architecture
- why
- how
- trade-off
- scenario
- project

"is_follow_up" must be a JSON boolean.

"reason" must be one short sentence explaining
why the question is being asked now.
"""