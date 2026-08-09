"""
Orchestrator.

Coordinates a single interview turn end-to-end.

This module has NO knowledge of HTTP. It exposes plain Python methods
that the service layer calls.

Deciding what to do next is deterministic Python:

- FOLLOW_UP
- NEW_TOPIC
- COMPLETE

Only the parts that genuinely benefit from an LLM use one:

1. InterviewerAgent -> generate question
2. EvaluationService -> evaluate answer
3. ReportService -> generate final report

There is no separate LLM-backed planner agent.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from app.agents.interviewer import InterviewerAgent
from app.core.llm_client import BaseLLMClient
from app.schemas.evaluation import EvaluationRecord
from app.services.candidate_service import get_prioritized_days
from app.services.curriculum_service import (
    CurriculumService,
    get_curriculum_service,
)
from app.services.evaluation_service import EvaluationService
from app.services.report_service import ReportService
from app.state.interview_state import InterviewState
from app.state.state_machine import (
    TurnDecision,
    can_force_complete,
    clamp_difficulty,
    difficulty_shift_for_score,
    meets_completion_floor,
)
from app.utils.logger import get_logger


logger = get_logger(__name__)


@dataclass
class TurnResult:
    reply: str
    done: bool
    feedback: Optional[dict] = None


class InterviewOrchestrator:
    def __init__(
        self,
        llm_client: Optional[BaseLLMClient] = None,
        interviewer: Optional[InterviewerAgent] = None,
        evaluation_service: Optional[EvaluationService] = None,
        report_service: Optional[ReportService] = None,
        curriculum_service: Optional[CurriculumService] = None,
    ):
        self._interviewer = (
            interviewer
            or InterviewerAgent(
                llm_client=llm_client
            )
        )

        self._evaluation_service = (
            evaluation_service
            or EvaluationService(
                llm_client=llm_client
            )
        )

        self._report_service = (
            report_service
            or ReportService(
                llm_client=llm_client
            )
        )

        self._curriculum = (
            curriculum_service
            or get_curriculum_service()
        )

    # ------------------------------------------------------------------
    # Start interview
    # ------------------------------------------------------------------

    def start_interview(
        self,
        state: InterviewState,
    ) -> TurnResult:
        """
        Start a new interview session and generate the opening question.
        """

        day = self._next_day(
            state,
            exclude_current=False,
        )

        day_info = (
            self._curriculum.get_day(day)
            or {}
        )

        generated = self._interviewer.generate_question(
            state,
            curriculum_day=day,
            difficulty="medium",
            is_follow_up=False,
            objective=(
                "Assess foundational understanding of "
                f"{day_info.get('title', 'the topic')}."
            ),
        )

        record = self._interviewer.to_question_record(
            generated,
            index=1,
        )

        state.record_question(record)

        candidate_name = state.candidate.get(
            "name",
            "there",
        )

        opening = (
            f"Welcome, {candidate_name}. "
            "Let's begin your technical interview "
            "based on your work in the AI Cohort.\n\n"
            f"{record.question}"
        )

        return TurnResult(
            reply=opening,
            done=False,
        )

    # ------------------------------------------------------------------
    # Continue interview
    # ------------------------------------------------------------------

    def continue_interview(
        self,
        state: InterviewState,
        message: str,
    ) -> TurnResult:
        """
        Process a candidate answer and determine the next interview step.
        """

        if state.current_question is None:
            raise ValueError(
                "No active question on this session - "
                "cannot process an answer."
            )

        current_question = (
            state.current_question
        )

        evaluation = (
            self._evaluation_service.evaluate_and_record(
                state,
                current_question,
                message,
            )
        )

        decision = self._decide_next_step(
            state,
            evaluation,
        )

        logger.info(
            "Interview decision: %s | score=%.2f | "
            "question_count=%d | covered_days=%d",
            decision.value,
            evaluation.score,
            state.question_count,
            len(state.covered_curriculum_days),
        )

        # --------------------------------------------------------------
        # COMPLETE
        # --------------------------------------------------------------

        if decision == TurnDecision.COMPLETE:
            report = self._report_service.finalize(
                state
            )

            return TurnResult(
                reply="Interview completed.",
                done=True,
                feedback=report,
            )

        # --------------------------------------------------------------
        # Difficulty adjustment
        # --------------------------------------------------------------

        difficulty_shift = (
            difficulty_shift_for_score(
                evaluation.score
            )
        )

        next_difficulty = clamp_difficulty(
            state.current_difficulty,
            difficulty_shift,
        )

        # --------------------------------------------------------------
        # FOLLOW-UP
        # --------------------------------------------------------------

        if decision == TurnDecision.FOLLOW_UP:
            next_day = (
                current_question.curriculum_day
                or state.current_curriculum_day
                or 1
            )

            objective = (
                "Follow up on: "
                f"{evaluation.suggested_follow_up_area "
                "or 'the previous gap'}."
            )

            is_follow_up = True

        # --------------------------------------------------------------
        # NEW TOPIC
        # --------------------------------------------------------------

        else:
            next_day = self._next_day(
                state,
                exclude_current=True,
            )

            day_info = (
                self._curriculum.get_day(next_day)
                or {}
            )

            objective = (
                "Assess understanding of "
                f"{day_info.get('title', 'the next topic')}."
            )

            is_follow_up = False

        # --------------------------------------------------------------
        # Generate next question
        # --------------------------------------------------------------

        generated = self._interviewer.generate_question(
            state,
            curriculum_day=next_day,
            difficulty=next_difficulty,
            is_follow_up=is_follow_up,
            objective=objective,
        )

        record = self._interviewer.to_question_record(
            generated,
            index=state.question_count + 1,
        )

        state.record_question(record)

        return TurnResult(
            reply=record.question,
            done=False,
        )

    # ------------------------------------------------------------------
    # Decision logic
    # ------------------------------------------------------------------

    def _decide_next_step(
        self,
        state: InterviewState,
        evaluation: EvaluationRecord,
    ) -> TurnDecision:
        """
        Determine whether to follow up, move to another topic,
        or finish the interview.
        """

        # Hard maximum always wins.
        if can_force_complete(state):
            return TurnDecision.COMPLETE

        current_is_follow_up = (
            state.current_question.is_follow_up
            if state.current_question
            else False
        )

        needs_follow_up = (
            evaluation.follow_up_needed
            and evaluation.score < 7
            and not current_is_follow_up
        )

        if needs_follow_up:
            return TurnDecision.FOLLOW_UP

        # Do not finish before minimum requirements are satisfied.
        if meets_completion_floor(state):
            return TurnDecision.COMPLETE

        return TurnDecision.NEW_TOPIC

    # ------------------------------------------------------------------
    # Curriculum selection
    # ------------------------------------------------------------------

    def _next_day(
        self,
        state: InterviewState,
        exclude_current: bool,
    ) -> int:
        """
        Select the next curriculum day using candidate progress,
        weak areas, skipped days, and curriculum retrieval.
        """

        covered = set(
            state.covered_curriculum_days
        )

        if (
            exclude_current
            and state.current_curriculum_day is not None
        ):
            covered.add(
                state.current_curriculum_day
            )

        days = get_prioritized_days(
            state.candidate,
            covered,
            curriculum_service=self._curriculum,
        )

        if days:
            return days[0]

        # Safe fallback if no eligible curriculum day exists.
        return (
            state.current_curriculum_day
            or 1
        )