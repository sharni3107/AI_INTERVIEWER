"""
In-memory session manager.

PART 16 of the spec is explicit: use an in-memory session manager for the
MVP, no Redis/Kafka/Celery.

A process-level dict keyed by session_id is sufficient for a hackathon
demo.

Thread-safety is handled with a simple lock since FastAPI can serve
requests concurrently via threadpool/async.
"""

from __future__ import annotations

import threading
from typing import Optional

from app.state.interview_state import InterviewState


class SessionNotFoundError(Exception):
    """Raised when a sessionId is referenced but no session exists."""


class SessionAlreadyExistsError(Exception):
    """Raised when trying to start a session that already exists."""


class InterviewSessionManager:
    def __init__(self):
        self._sessions: dict[str, InterviewState] = {}
        self._lock = threading.Lock()

    def create_session(
        self,
        session_id: str,
        candidate: dict,
    ) -> InterviewState:
        """
        Create and store a new interview session.

        Raises:
            SessionAlreadyExistsError:
                If the session_id already exists.
        """

        with self._lock:
            if session_id in self._sessions:
                raise SessionAlreadyExistsError(
                    f"Session '{session_id}' already exists. "
                    "Send a 'message' to continue it."
                )

            state = InterviewState(
                session_id=session_id,
                candidate=candidate,
            )

            self._sessions[session_id] = state

            return state

    def get_session(
        self,
        session_id: str,
    ) -> InterviewState:
        """
        Retrieve an existing interview session.

        Raises:
            SessionNotFoundError:
                If no session exists with the given ID.
        """

        with self._lock:
            state = self._sessions.get(session_id)

        if state is None:
            raise SessionNotFoundError(
                f"No interview session found for "
                f"sessionId '{session_id}'"
            )

        return state

    def get_session_or_none(
        self,
        session_id: str,
    ) -> Optional[InterviewState]:
        """Return a session if it exists, otherwise None."""

        with self._lock:
            return self._sessions.get(session_id)

    def delete_session(
        self,
        session_id: str,
    ) -> None:
        """Delete an interview session if it exists."""

        with self._lock:
            self._sessions.pop(
                session_id,
                None,
            )

    def all_session_ids(self) -> list[str]:
        """Return all currently active session IDs."""

        with self._lock:
            return list(self._sessions.keys())


_manager_singleton: Optional[InterviewSessionManager] = None


def get_session_manager() -> InterviewSessionManager:
    """
    Return the process-wide session manager singleton.
    """

    global _manager_singleton

    if _manager_singleton is None:
        _manager_singleton = InterviewSessionManager()

    return _manager_singleton


def reset_session_manager() -> None:
    """
    Test helper - clears all in-memory sessions.
    """

    global _manager_singleton

    _manager_singleton = InterviewSessionManager()