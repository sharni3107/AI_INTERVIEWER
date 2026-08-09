"""
Report service.

Calls the FeedbackAgent to produce the final structured interview
report and marks the interview session as completed.

Kept separate from the orchestrator so that final report generation
and session completion have one clear owner.
"""

from __future__ import annotations

from typing import Optional

from app.agents.feedback import FeedbackAgent
from app.core.llm_client import BaseLLMClient
from app.state.interview_state import InterviewState


class ReportService:
    def __init__(
        self,
        llm_client: Optional[BaseLLMClient] = None,
        feedback_agent: Optional[FeedbackAgent] = None,
    ):
        self._feedback_agent = (
            feedback_agent
            or FeedbackAgent(
                llm_client=llm_client
            )
        )

    def finalize(
        self,
        state: InterviewState,
    ) -> dict:
        """
        Generate the final structured interview report
        and mark the session as completed.

        Expected report shape:

        {
            "summary": "...",
            "strengths": [...],
            "gaps": [...],
            "next": [...]
        }

        The orchestrator is responsible for ensuring that the
        minimum interview requirements have been satisfied before
        calling this method.
        """

        report = (
            self._feedback_agent.generate_feedback(
                state
            )
        )

        state.mark_completed(report)

        return report