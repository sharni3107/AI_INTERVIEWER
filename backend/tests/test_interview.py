```python
"""
Tests for the interview data/session/API side.

Covers:
- candidate normalization
- curriculum loading
- in-memory session state
- full POST /api/interview lifecycle
- completion and feedback
- completed-session protection

Note:
The current MVP architecture does NOT require RAG. Curriculum selection is
handled deterministically by candidate_service + curriculum_service, so
there are intentionally no RAG/Chroma tests here.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.schemas.interview import QuestionRecord
from app.services.curriculum_service import CurriculumService
from app.state.interview_state import InterviewState
from app.state.state_manager import InterviewSessionManager
from app.utils.candidate_normalizer import (
    InvalidCandidateDataError,
    normalize_candidate,
)
from tests.conftest import SAMPLE_CANDIDATE


client = TestClient(app)


# ---------------------------------------------------------------------------
# Candidate normalization
# ---------------------------------------------------------------------------


def test_normalize_candidate_extracts_member_fields():
    normalized = normalize_candidate(SAMPLE_CANDIDATE)

    assert normalized["candidate_id"] == "CAND-001"
    assert normalized["name"] == "Sarah Johnson"
    assert normalized["job_role"] == "Senior Data Engineer"


def test_normalize_candidate_passed_and_skipped_days():
    normalized = normalize_candidate(SAMPLE_CANDIDATE)

    assert normalized["passed_days"] == [
        7,
        8,
        10,
        12,
        16,
        22,
        23,
        28,
        31,
    ]
    assert normalized["skipped_days"] == [29]


def test_normalize_candidate_struggled_days_from_attempts():
    normalized = normalize_candidate(SAMPLE_CANDIDATE)

    # Day 12 = 4 attempts
    # Day 28 = 3 attempts
    assert 12 in normalized["struggled_days"]
    assert 28 in normalized["struggled_days"]

    # Day 7 was passed cleanly with one attempt.
    assert 7 not in normalized["struggled_days"]


def test_normalize_candidate_rejects_empty_payload():
    with pytest.raises(InvalidCandidateDataError):
        normalize_candidate({})


def test_normalize_candidate_tolerates_missing_missions():
    normalized = normalize_candidate(
        {
            "member": {
                "id": "x",
                "name": "Y",
            }
        }
    )

    assert normalized["passed_days"] == []
    assert normalized["skipped_days"] == []


# ---------------------------------------------------------------------------
# Curriculum service
# ---------------------------------------------------------------------------


def test_curriculum_has_31_days():
    service = CurriculumService()

    days = service.get_days()

    assert len(days) == 31
    assert sorted(day["day"] for day in days) == list(range(1, 32))


def test_day_fields_match_real_schema():
    service = CurriculumService()

    day = service.get_day(1)

    assert day is not None
    assert set(day.keys()) == {
        "day",
        "title",
        "type",
        "tools",
        "objectives",
    }


def test_get_module_for_day_uses_range():
    service = CurriculumService()

    module = service.get_module_for_day(7)

    assert module is not None
    assert module["days"] == [7, 10]


def test_get_day_returns_none_for_invalid_day():
    service = CurriculumService()

    assert service.get_day(999) is None


# ---------------------------------------------------------------------------
# In-memory session state
# ---------------------------------------------------------------------------


def test_start_session_creates_state():
    manager = InterviewSessionManager()

    state = manager.create_session(
        "s1",
        {"name": "Alice"},
    )

    assert state.session_id == "s1"
    assert state.interview_status.value == "in_progress"
    assert state.question_count == 0


def test_duplicate_session_raises():
    manager = InterviewSessionManager()

    manager.create_session(
        "s1",
        {"name": "Alice"},
    )

    with pytest.raises(Exception):
        manager.create_session(
            "s1",
            {"name": "Alice"},
        )


def test_get_session_returns_created_state():
    manager = InterviewSessionManager()

    created = manager.create_session(
        "s1",
        {"name": "Alice"},
    )

    retrieved = manager.get_session("s1")

    assert retrieved is created


def test_get_session_or_none_returns_none_for_missing_session():
    manager = InterviewSessionManager()

    assert manager.get_session_or_none("does-not-exist") is None


def test_delete_session_removes_state():
    manager = InterviewSessionManager()

    manager.create_session(
        "s1",
        {"name": "Alice"},
    )

    manager.delete_session("s1")

    assert manager.get_session_or_none("s1") is None


def test_record_question_updates_coverage_and_count():
    manager = InterviewSessionManager()

    state = manager.create_session(
        "s2",
        {"name": "Alice"},
    )

    question = QuestionRecord(
        index=1,
        question="What is RAG?",
        topic="RAG",
        curriculum_day=5,
        difficulty="medium",
        question_type="conceptual",
        is_follow_up=False,
    )

    state.record_question(question)

    assert state.question_count == 1
    assert len(state.questions) == 1
    assert 5 in state.covered_curriculum_days
    assert "RAG" in state.covered_topics
    assert state.current_question is question


def test_meets_minimum_requirements():
    manager = InterviewSessionManager()

    state = manager.create_session(
        "s3",
        {"name": "Alice"},
    )

    assert (
        state.meets_minimum_requirements(
            min_questions=8,
            min_days=4,
        )
        is False
    )

    for index, day in enumerate(
        [1, 2, 3, 4, 5, 6, 7, 8],
        start=1,
    ):
        state.record_question(
            QuestionRecord(
                index=index,
                question=f"Q{index}",
                topic="topic",
                curriculum_day=day,
                difficulty="medium",
                question_type="conceptual",
                is_follow_up=False,
            )
        )

    assert (
        state.meets_minimum_requirements(
            min_questions=8,
            min_days=4,
        )
        is True
    )


def test_no_integrity_flags_field_exists():
    """
    The integrity agent/state field was intentionally removed from the
    current MVP architecture.
    """

    state = InterviewState(
        session_id="x",
        candidate={},
    )

    assert not hasattr(state, "integrity_flags")


# ---------------------------------------------------------------------------
# Interview state lifecycle
# ---------------------------------------------------------------------------


def test_record_answer_adds_candidate_message_to_history():
    manager = InterviewSessionManager()

    state = manager.create_session(
        "history-test",
        {"name": "Alice"},
    )

    question = QuestionRecord(
        index=1,
        question="Explain RAG.",
        topic="RAG",
        curriculum_day=5,
        difficulty="medium",
        question_type="conceptual",
        is_follow_up=False,
    )

    state.record_question(question)

    # Import here so this test remains focused on state behavior.
    from app.schemas.evaluation import EvaluationRecord

    evaluation = EvaluationRecord(
        question_index=1,
        answer="RAG combines retrieval with generation.",
        score=7.0,
        correctness=0.7,
        technical_depth=0.6,
        completeness=0.7,
        reasoning=0.7,
        communication=0.8,
    )

    state.record_answer_and_evaluation(
        "RAG combines retrieval with generation.",
        evaluation,
    )

    assert state.evaluations[0] is evaluation
    assert state.interview_history[-1] == {
        "role": "candidate",
        "content": "RAG combines retrieval with generation.",
    }


# ---------------------------------------------------------------------------
# Full API flow
# ---------------------------------------------------------------------------


def test_start_interview_via_api():
    session_id = "api-start-test"

    response = client.post(
        "/api/interview",
        json={
            "sessionId": session_id,
            "candidate": SAMPLE_CANDIDATE,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["done"] is False
    assert "reply" in body
    assert body["reply"]


def test_continue_interview_via_api():
    session_id = "api-continue-test"

    start_response = client.post(
        "/api/interview",
        json={
            "sessionId": session_id,
            "candidate": SAMPLE_CANDIDATE,
        },
    )

    assert start_response.status_code == 200

    response = client.post(
        "/api/interview",
        json={
            "sessionId": session_id,
            "message": "A detailed technical answer.",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["done"] is False
    assert "reply" in body
    assert body["reply"]


def test_invalid_session_returns_404():
    response = client.post(
        "/api/interview",
        json={
            "sessionId": "does-not-exist",
            "message": "hi",
        },
    )

    assert response.status_code == 404


def test_starting_unknown_session_without_candidate_is_not_found():
    """
    No candidate means the API interprets the request as continue mode.
    Since the session does not exist, 404 is correct.
    """

    response = client.post(
        "/api/interview",
        json={
            "sessionId": "api-missing-candidate",
        },
    )

    assert response.status_code == 404


def test_empty_candidate_object_on_start_is_rejected():
    response = client.post(
        "/api/interview",
        json={
            "sessionId": "api-empty-candidate",
            "candidate": {},
        },
    )

    assert response.status_code == 400


def test_missing_message_for_existing_session_is_rejected():
    session_id = "api-missing-message"

    start_response = client.post(
        "/api/interview",
        json={
            "sessionId": session_id,
            "candidate": SAMPLE_CANDIDATE,
        },
    )

    assert start_response.status_code == 200

    response = client.post(
        "/api/interview",
        json={
            "sessionId": session_id,
        },
    )

    # The request is interpreted as continue mode and the service should
    # reject the missing message.
    assert response.status_code == 400


def test_duplicate_start_is_handled():
    session_id = "api-duplicate-start"

    first_response = client.post(
        "/api/interview",
        json={
            "sessionId": session_id,
            "candidate": SAMPLE_CANDIDATE,
        },
    )

    assert first_response.status_code == 200

    second_response = client.post(
        "/api/interview",
        json={
            "sessionId": session_id,
            "candidate": SAMPLE_CANDIDATE,
        },
    )

    # Your InterviewService intentionally allows an idempotent duplicate
    # start when no answer has been submitted yet.
    assert second_response.status_code == 200
    assert second_response.json()["done"] is False


# ---------------------------------------------------------------------------
# Full interview lifecycle
# ---------------------------------------------------------------------------


def test_full_interview_reaches_minimums_and_returns_structured_feedback():
    session_id = "api-full-test"

    start_response = client.post(
        "/api/interview",
        json={
            "sessionId": session_id,
            "candidate": SAMPLE_CANDIDATE,
        },
    )

    assert start_response.status_code == 200

    body = {}

    for _ in range(20):
        response = client.post(
            "/api/interview",
            json={
                "sessionId": session_id,
                "message": (
                    "A detailed technical answer with implementation "
                    "specifics and architectural reasoning."
                ),
            },
        )

        assert response.status_code == 200

        body = response.json()

        if body["done"]:
            break

    assert body["done"] is True
    assert "feedback" in body

    feedback = body["feedback"]

    assert set(feedback.keys()) == {
        "summary",
        "strengths",
        "gaps",
        "next",
    }

    assert isinstance(feedback["summary"], str)
    assert isinstance(feedback["strengths"], list)
    assert isinstance(feedback["gaps"], list)
    assert isinstance(feedback["next"], list)

    from app.services.interview_service import get_interview_service

    state = get_interview_service()._sessions.get_session(session_id)

    assert len(state.questions) >= 8
    assert len(state.covered_curriculum_days) >= 4
    assert state.interview_status.value == "completed"


def test_message_after_completion_is_rejected():
    session_id = "api-complete-then-continue"

    start_response = client.post(
        "/api/interview",
        json={
            "sessionId": session_id,
            "candidate": SAMPLE_CANDIDATE,
        },
    )

    assert start_response.status_code == 200

    body = {}

    for _ in range(20):
        response = client.post(
            "/api/interview",
            json={
                "sessionId": session_id,
                "message": "Detailed technical answer.",
            },
        )

        assert response.status_code == 200

        body = response.json()

        if body["done"]:
            break

    assert body["done"] is True

    response_after_completion = client.post(
        "/api/interview",
        json={
            "sessionId": session_id,
            "message": "one more?",
        },
    )

    assert response_after_completion.status_code == 400
```
