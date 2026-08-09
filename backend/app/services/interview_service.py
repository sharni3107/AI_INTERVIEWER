"""
Interview Service (PART 17).

The only entry point the API layer should call.

Wraps:

- session lifecycle through the session manager
- turn processing through the orchestrator

Public methods:

    start_interview(session_id, candidate)
    process_message(session_id, message)

Both return plain dictionaries matching the API contract.
"""

from __future__ import annotations

from typing import Any, Optional

from app.agents.orchestrator import InterviewOrchestrator
from app.services.candidate_service import (
    InvalidCandidateDataError,
    normalize_candidate,
)
from app.state.interview_state import InterviewStatus
from app.state.state_manager import (
    InterviewSessionManager,
    SessionAlreadyExistsError,
    SessionNotFoundError,
    get_session_manager,
)
from app.utils.logger import get_logger


logger = get_logger(__name__)


class InterviewAlreadyCompletedError(Exception):
    """
    Raised when a message is sent to a session that already finished.
    """


class MissingCandidateError(Exception):
    """
    Raised when starting a session without a candidate payload.
    """


class MissingMessageError(Exception):
    """
    Raised when continuing a session without a message payload.
    """


class InterviewService:
    def __init__(
        self,
        session_manager: Optional[
            InterviewSessionManager
        ] = None,
        orchestrator: Optional[
            InterviewOrchestrator
        ] = None,
    ):
        self._sessions = (
            session_manager
            or get_session_manager()
        )

        self._orchestrator = (
            orchestrator
            or InterviewOrchestrator()
        )

    # ------------------------------------------------------------------
    # Start interview
    # ------------------------------------------------------------------

    def start_interview(
        self,
        session_id: str,
        candidate_raw: dict[str, Any],
    ) -> dict:
        """
        Create a new interview session and generate
        the opening interview question.
        """

        if not candidate_raw:
            raise MissingCandidateError(
                "'candidate' is required to start "
                "a new interview session."
            )

        existing = (
            self._sessions.get_session_or_none(
                session_id
            )
        )

        if existing is not None:
            # Idempotency-friendly behavior:
            #
            # If the session exists but only the opening
            # question has been generated, return that
            # question instead of creating another session.

            if (
                existing.question_count <= 1
                and existing.interview_status
                == InterviewStatus.IN_PROGRESS
            ):
                current_question = (
                    existing.current_question
                )

                if current_question is not None:
                    return {
                        "reply": current_question.question,
                        "done": False,
                    }

            raise SessionAlreadyExistsError(
                f"Session '{session_id}' already exists "
                "and is already in progress."
            )

        # Normalize the official candidate.json payload
        # into the internal candidate representation.
        try:
            candidate = normalize_candidate(
                candidate_raw
            )
        except InvalidCandidateDataError:
            raise

        # Create in-memory interview state.
        state = self._sessions.create_session(
            session_id,
            candidate,
        )

        # Generate the first question.
        result = self._orchestrator.start_interview(
            state
        )

        return {
            "reply": result.reply,
            "done": result.done,
        }

    # ------------------------------------------------------------------
    # Continue interview
    # ------------------------------------------------------------------

    def process_message(
        self,
        session_id: str,
        message: Optional[str],
    ) -> dict:
        """
        Process one candidate message.

        The session manager retrieves the state and the
        orchestrator handles evaluation, decision-making,
        question generation, and completion.
        """

        state = self._sessions.get_session(
            session_id
        )

        if (
            state.interview_status
            == InterviewStatus.COMPLETED
        ):
            raise InterviewAlreadyCompletedError(
                f"Session '{session_id}' has already "
                "completed. No further messages accepted."
            )

        if (
            not message
            or not str(message).strip()
        ):
            raise MissingMessageError(
                "'message' is required to continue "
                "an interview session."
            )

        clean_message = str(message).strip()

        result = (
            self._orchestrator.continue_interview(
                state,
                clean_message,
            )
        )

        response: dict[str, Any] = {
            "reply": result.reply,
            "done": result.done,
        }

        if result.done:
            response["feedback"] = result.feedback

        return response


# ----------------------------------------------------------------------
# Singleton
# ----------------------------------------------------------------------

_service_singleton: Optional[
    InterviewService
] = None


def get_interview_service() -> InterviewService:
    """
    Return the process-wide InterviewService singleton.
    """

    global _service_singleton

    if _service_singleton is None:
        _service_singleton = InterviewService()

    return _service_singleton


def reset_interview_service() -> None:
    """
    Test helper - reset the service singleton.
    """

    global _service_singleton

    _service_singleton = None