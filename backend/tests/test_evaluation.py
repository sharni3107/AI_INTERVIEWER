
"""
Tests for the evaluation/feedback side:

- Evaluator agent scoring
- EvaluationService recording onto state
- Adaptive follow-up decision (orchestrator's deterministic logic)
- Feedback agent + ReportService final report shape
- candidate_service.get_prioritized_days personalization
"""
from app.agents.evaluator import EvaluatorAgent
from app.agents.feedback import FeedbackAgent
from app.core.llm_client import MockLLMClient
from app.state.interview_state import InterviewState, QuestionRecord
from app.services.candidate_service import get_prioritized_days
from app.services.curriculum_service import get_curriculum_service
from app.services.evaluation_service import EvaluationService
from app.services.report_service import ReportService
from app.utils.candidate_normalizer import normalize_candidate
from tests.confest import SAMPLE_CANDIDATE


def _state() -> InterviewState:
    """Create a fresh interview state for each test."""
    candidate = normalize_candidate(SAMPLE_CANDIDATE)

    return InterviewState(
        session_id="eval-test",
        candidate=candidate,
    )


def _question(day: int = 7) -> QuestionRecord:
    """Create a sample interview question."""
    return QuestionRecord(
        index=1,
        question="Explain embeddings.",
        topic="Embeddings",
        curriculum_day=day,
        difficulty="medium",
        question_type="conceptual",
        is_follow_up=False,
        reason="Test question",
    )


# ---------------------------------------------------------------------------
# Evaluator Agent
# ---------------------------------------------------------------------------


def test_evaluator_returns_score_in_range():
    agent = EvaluatorAgent(llm_client=MockLLMClient())
    state = _state()

    evaluation = agent.evaluate(
        state,
        _question(),
        "A reasonably detailed answer about embeddings.",
    )

    assert 0 <= evaluation.score <= 10


def test_evaluator_records_strengths_and_gaps():
    agent = EvaluatorAgent(llm_client=MockLLMClient())
    state = _state()

    evaluation = agent.evaluate(
        state,
        _question(),
        "Some answer.",
    )

    assert isinstance(evaluation.strengths, list)
    assert isinstance(evaluation.gaps, list)
    assert isinstance(evaluation.missing_concepts, list)


def test_evaluator_returns_dimension_scores_in_range():
    agent = EvaluatorAgent(llm_client=MockLLMClient())
    state = _state()

    evaluation = agent.evaluate(
        state,
        _question(),
        "A detailed answer explaining embeddings and their use in retrieval.",
    )

    assert 0 <= evaluation.correctness <= 1
    assert 0 <= evaluation.technical_depth <= 1
    assert 0 <= evaluation.completeness <= 1
    assert 0 <= evaluation.reasoning <= 1
    assert 0 <= evaluation.communication <= 1


# ---------------------------------------------------------------------------
# Evaluation Service
# ---------------------------------------------------------------------------


def test_evaluation_service_records_answer_and_evaluation():
    service = EvaluationService(llm_client=MockLLMClient())
    state = _state()
    question = _question()

    state.record_question(question)

    evaluation = service.evaluate_and_record(
        state,
        question,
        "My answer.",
    )

    assert len(state.evaluations) == 1
    assert state.evaluations[0] is evaluation

    assert state.interview_history[-1] == {
        "role": "candidate",
        "content": "My answer.",
    }


def test_evaluation_service_updates_state_strengths_and_gaps():
    service = EvaluationService(llm_client=MockLLMClient())
    state = _state()
    question = _question()

    state.record_question(question)

    evaluation = service.evaluate_and_record(
        state,
        question,
        "My answer about embeddings.",
    )

    assert state.evaluations
    assert evaluation in state.evaluations

    # State should receive the evaluator's signals.
    assert isinstance(state.strengths, list)
    assert isinstance(state.gaps, list)


# ---------------------------------------------------------------------------
# Feedback Agent
# ---------------------------------------------------------------------------


def test_feedback_agent_returns_required_keys():
    agent = FeedbackAgent(llm_client=MockLLMClient())
    state = _state()

    question = _question()
    state.record_question(question)

    report = agent.generate_feedback(state)

    assert set(report.keys()) == {
        "summary",
        "strengths",
        "gaps",
        "next",
    }


def test_feedback_agent_returns_correct_value_types():
    agent = FeedbackAgent(llm_client=MockLLMClient())
    state = _state()

    state.record_question(_question())

    report = agent.generate_feedback(state)

    assert isinstance(report["summary"], str)
    assert isinstance(report["strengths"], list)
    assert isinstance(report["gaps"], list)
    assert isinstance(report["next"], list)


def test_feedback_agent_uses_interview_data():
    agent = FeedbackAgent(llm_client=MockLLMClient())
    state = _state()

    state.record_question(_question(day=7))

    report = agent.generate_feedback(state)

    assert report["summary"]
    assert report["strengths"]
    assert report["gaps"]
    assert report["next"]


# ---------------------------------------------------------------------------
# Report Service
# ---------------------------------------------------------------------------


def test_report_service_marks_session_completed():
    service = ReportService(llm_client=MockLLMClient())
    state = _state()

    state.record_question(_question())

    report = service.finalize(state)

    assert state.interview_status.value == "completed"
    assert state.feedback == report


def test_report_service_returns_required_report_shape():
    service = ReportService(llm_client=MockLLMClient())
    state = _state()

    state.record_question(_question())

    report = service.finalize(state)

    assert set(report.keys()) == {
        "summary",
        "strengths",
        "gaps",
        "next",
    }


# ---------------------------------------------------------------------------
# Candidate Service - Prioritized Curriculum Days
# ---------------------------------------------------------------------------


def test_prioritized_days_only_includes_attempted_days():
    candidate = normalize_candidate(SAMPLE_CANDIDATE)
    curriculum_service = get_curriculum_service()

    days = get_prioritized_days(
        candidate,
        covered_days=set(),
        curriculum_service=curriculum_service,
    )

    attempted_days = (
        set(candidate["passed_days"])
        | set(candidate["failed_days"])
    )

    assert set(days) <= attempted_days


def test_prioritized_days_excludes_skipped_days():
    candidate = normalize_candidate(SAMPLE_CANDIDATE)
    curriculum_service = get_curriculum_service()

    days = get_prioritized_days(
        candidate,
        covered_days=set(),
        curriculum_service=curriculum_service,
    )

    skipped_days = set(candidate["skipped_days"])

    assert set(days).isdisjoint(skipped_days)


def test_prioritized_days_puts_struggled_days_first():
    candidate = normalize_candidate(SAMPLE_CANDIDATE)
    curriculum_service = get_curriculum_service()

    days = get_prioritized_days(
        candidate,
        covered_days=set(),
        curriculum_service=curriculum_service,
    )

    struggled_days = set(candidate["struggled_days"])

    # Only make this assertion when the fixture actually contains
    # struggled days that are eligible for prioritization.
    eligible_struggled_days = (
        struggled_days
        & (
            set(candidate["passed_days"])
            | set(candidate["failed_days"])
        )
    )

    if eligible_struggled_days:
        assert days
        assert days[0] in eligible_struggled_days


def test_prioritized_days_shrinks_as_days_are_covered():
    candidate = normalize_candidate(SAMPLE_CANDIDATE)
    curriculum_service = get_curriculum_service()

    first_pass = get_prioritized_days(
        candidate,
        covered_days=set(),
        curriculum_service=curriculum_service,
    )

    if not first_pass:
        return

    first_day = first_pass[0]

    second_pass = get_prioritized_days(
        candidate,
        covered_days={first_day},
        curriculum_service=curriculum_service,
    )

    assert first_day not in second_pass

