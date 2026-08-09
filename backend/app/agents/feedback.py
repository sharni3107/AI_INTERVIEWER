"""
Feedback Agent (PART 13).

Produces the final structured feedback object using the COMPLETE collection
of questions, answers, and evaluations from the session.

Output contract:

{
    "summary": str,
    "strengths": [str],
    "gaps": [str],
    "next": [str]
}
"""

from __future__ import annotations

from typing import Optional

from app.core.llm_client import (
    BaseLLMClient,
    LLMError,
    LLMMalformedResponseError,
    get_llm_client,
)
from app.state.interview_state import InterviewState
from app.utils.logger import get_logger


logger = get_logger(__name__)


class FeedbackAgent:
    def __init__(
        self,
        llm_client: Optional[BaseLLMClient] = None,
    ):
        self._llm = (
            llm_client
            or get_llm_client()
        )

    def generate_feedback(
        self,
        state: InterviewState,
    ) -> dict:
        """
        Generate the final structured feedback report.

        The complete interview transcript is provided to the LLM,
        rather than only the most recent question.
        """

        transcript = self._build_transcript(
            state
        )

        avg_score = self._average_score(
            state
        )

        user_prompt = (
            f"CANDIDATE: "
            f"{state.candidate.get('name')}\n"
            f"CURRICULUM DAYS COVERED: "
            f"{sorted(state.covered_curriculum_days)}\n"
            f"TOPICS COVERED: "
            f"{sorted(state.covered_topics)}\n"
            f"QUESTIONS ASKED: "
            f"{len(state.questions)}\n"
            f"AVERAGE SCORE: "
            f"{avg_score:.2f}/10\n\n"
            "FULL INTERVIEW TRANSCRIPT "
            "(question -> answer -> evaluation):\n"
            f"{transcript}\n\n"
            "Generate the final structured feedback now, "
            "as JSON, based on the ENTIRE transcript above, "
            "not just the most recent exchange."
        )

        try:
            raw = self._llm.generate_json(
                system=_FEEDBACK_SYSTEM_PROMPT,
                user=user_prompt,
            )

            if not isinstance(raw, dict):
                raise LLMMalformedResponseError(
                    "Feedback LLM returned a non-object response."
                )

            return self._normalize(
                raw,
                state,
            )

        except (
            LLMError,
            LLMMalformedResponseError,
        ) as exc:
            logger.warning(
                "Feedback LLM call failed (%s) - "
                "using deterministic fallback feedback.",
                exc,
            )

            return self._deterministic_fallback(
                state,
                avg_score,
            )

    # ------------------------------------------------------------------
    # Transcript
    # ------------------------------------------------------------------

    def _build_transcript(
        self,
        state: InterviewState,
    ) -> str:
        """
        Build the complete question -> answer -> evaluation transcript.
        """

        lines: list[str] = []

        for question in state.questions:
            evaluation = next(
                (
                    evaluation
                    for evaluation in state.evaluations
                    if evaluation.question_index
                    == question.index
                ),
                None,
            )

            lines.append(
                f"Q{question.index} "
                f"[{question.topic} / "
                f"Day {question.curriculum_day} / "
                f"{question.difficulty}]: "
                f"{question.question}"
            )

            if evaluation:
                lines.append(
                    f"  Answer: "
                    f"{evaluation.answer}"
                )

                lines.append(
                    f"  Eval: "
                    f"score={evaluation.score}, "
                    f"strengths={evaluation.strengths}, "
                    f"gaps={evaluation.gaps}, "
                    f"missing_concepts="
                    f"{evaluation.missing_concepts}"
                )

        if not lines:
            return "No questions were asked."

        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Score
    # ------------------------------------------------------------------

    def _average_score(
        self,
        state: InterviewState,
    ) -> float:
        """
        Calculate the average evaluation score.
        """

        if not state.evaluations:
            return 0.0

        return sum(
            evaluation.score
            for evaluation in state.evaluations
        ) / len(state.evaluations)

    # ------------------------------------------------------------------
    # Normalize LLM output
    # ------------------------------------------------------------------

    def _normalize(
        self,
        raw: dict,
        state: InterviewState,
    ) -> dict:
        """
        Normalize and validate the final LLM response.
        """

        summary = (
            str(
                raw.get(
                    "summary",
                    "",
                )
            ).strip()
            or self._fallback_summary(state)
        )

        strengths = [
            str(strength)
            for strength in (
                raw.get("strengths")
                or []
            )
        ][:8]

        gaps = [
            str(gap)
            for gap in (
                raw.get("gaps")
                or []
            )
        ][:8]

        next_steps = [
            str(next_step)
            for next_step in (
                raw.get("next")
                or []
            )
        ][:8]

        if not strengths:
            strengths = (
                self._dedupe(
                    state.strengths
                )[:5]
                or [
                    "No standout strengths "
                    "identified from this session."
                ]
            )

        if not gaps:
            gaps = (
                self._dedupe(
                    state.gaps
                )[:5]
                or [
                    "No major gaps identified "
                    "from this session."
                ]
            )

        if not next_steps:
            next_steps = [
                f"Revisit and practice explaining: "
                f"{gap}"
                for gap in gaps[:3]
            ]

        return {
            "summary": summary,
            "strengths": strengths,
            "gaps": gaps,
            "next": next_steps,
        }

    # ------------------------------------------------------------------
    # Deterministic fallback
    # ------------------------------------------------------------------

    def _deterministic_fallback(
        self,
        state: InterviewState,
        avg_score: float,
    ) -> dict:
        """
        Generate usable feedback even when the LLM is unavailable.
        """

        strengths = (
            self._dedupe(
                state.strengths
            )[:5]
            or [
                "Engaged with each question "
                "and provided answers."
            ]
        )

        gaps = (
            self._dedupe(
                state.gaps
            )[:5]
            or [
                "No major gaps captured."
            ]
        )

        next_steps = [
            f"Review and strengthen: {gap}"
            for gap in gaps[:3]
        ]

        if not next_steps:
            next_steps = [
                "Continue practicing explaining "
                "system design trade-offs out loud."
            ]

        return {
            "summary": self._fallback_summary(
                state,
                avg_score,
            ),
            "strengths": strengths,
            "gaps": gaps,
            "next": next_steps,
        }

    # ------------------------------------------------------------------
    # Fallback summary
    # ------------------------------------------------------------------

    def _fallback_summary(
        self,
        state: InterviewState,
        avg_score: Optional[float] = None,
    ) -> str:
        """
        Generate a simple summary without the LLM.
        """

        if avg_score is None:
            avg_score = self._average_score(
                state
            )

        days = len(
            state.covered_curriculum_days
        )

        candidate_name = state.candidate.get(
            "name",
            "The candidate",
        )

        return (
            f"{candidate_name} answered "
            f"{len(state.questions)} questions "
            f"across {days} curriculum days, "
            f"averaging {avg_score:.1f}/10."
        )

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    @staticmethod
    def _dedupe(
        items: list[str],
    ) -> list[str]:
        """
        Remove duplicate strings while preserving order.
        """

        seen: set[str] = set()
        output: list[str] = []

        for item in items:
            key = item.strip().lower()

            if key and key not in seen:
                seen.add(key)
                output.append(item)

        return output


_FEEDBACK_SYSTEM_PROMPT = """
You are the feedback module of a technical interview system.

You write the final performance report for a candidate based on their
COMPLETE interview transcript:

- every question
- every candidate answer
- every evaluation

Do NOT base the report only on the last exchange.

Return ONLY a JSON object.

Do not return prose.
Do not return markdown fences.

Use exactly this shape:

{
    "summary": "<2-4 sentence overall summary of performance>",
    "strengths": [
        "<concise, specific, evidence-backed strength>"
    ],
    "gaps": [
        "<concise, specific, evidence-backed gap>"
    ],
    "next": [
        "<concise, specific, actionable next step>"
    ]
}

Rules:

- Every point must be traceable to something that actually happened
  in the interview transcript.
- Do not invent strengths.
- Do not invent weaknesses.
- Do not produce generic feedback such as "good job" or
  "keep learning".
- Be specific about technical topics.
- Reference curriculum days when useful.
- Strengths must be supported by actual candidate answers.
- Gaps must be supported by actual evaluation evidence.
- Next steps must directly address identified gaps.
- Keep the feedback concise and actionable.
"""