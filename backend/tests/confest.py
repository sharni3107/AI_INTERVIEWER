```python
import json
import os
import sys


# ---------------------------------------------------------------------------
# Test environment
# ---------------------------------------------------------------------------

# Add the backend project root to Python's import path.
BACKEND_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.insert(0, BACKEND_ROOT)


# Use the deterministic mock LLM during tests.
os.environ.setdefault("LLM_PROVIDER", "mock")

# Test data paths.
os.environ.setdefault(
    "CURRICULUM_PATH",
    os.path.join(BACKEND_ROOT, "data", "curriculum.json"),
)

os.environ.setdefault(
    "TECHSPEC_PATH",
    os.path.join(BACKEND_ROOT, "data", "techspec.md"),
)

# Interview guardrails.
os.environ.setdefault("INTERVIEW_MIN_QUESTIONS", "8")
os.environ.setdefault("INTERVIEW_MIN_DAYS", "4")
os.environ.setdefault("INTERVIEW_MAX_QUESTIONS", "16")


# ---------------------------------------------------------------------------
# Pytest imports
# ---------------------------------------------------------------------------

import pytest

from app.core.llm_client import MockLLMClient, set_llm_client
from app.services.interview_service import reset_interview_service
from app.state.state_manager import reset_session_manager


# ---------------------------------------------------------------------------
# Sample candidate
# ---------------------------------------------------------------------------
#
# Matches the actual candidates.json structure:
#
# {
#   "member": {...},
#   "missions": [...],
#   "signals": {...}
# }
#
# CAND-001 / Sarah Johnson
# - passed missions across multiple curriculum days
# - day 29 skipped
# - no fabricated fields such as score/project/strong_areas
# ---------------------------------------------------------------------------

SAMPLE_CANDIDATE = {
    "member": {
        "id": "CAND-001",
        "name": "Sarah Johnson",
        "jobRole": "Senior Data Engineer",
        "yearsExperience": 9,
        "education": "MS Computer Science",
        "status": "COMPLETED",
    },
    "missions": [
        {
            "day": 7,
            "title": "Embeddings Explained",
            "passed": True,
            "attempts": 1,
        },
        {
            "day": 8,
            "title": "Vector Databases Overview",
            "passed": True,
            "attempts": 1,
        },
        {
            "day": 10,
            "title": "The Retrieval & Matching Engine",
            "passed": True,
            "attempts": 2,
        },
        {
            "day": 12,
            "title": "Prompt Engineering Fundamentals",
            "passed": True,
            "attempts": 4,
        },
        {
            "day": 16,
            "title": "Chatbot Backend & API Integration",
            "passed": True,
            "attempts": 1,
        },
        {
            "day": 22,
            "title": "Multi-Agent Orchestration",
            "passed": True,
            "attempts": 2,
        },
        {
            "day": 23,
            "title": "Model Context Protocol (MCP)",
            "passed": True,
            "attempts": 2,
        },
        {
            "day": 28,
            "title": "Docker & Kubernetes Deployment",
            "passed": True,
            "attempts": 3,
        },
        {
            "day": 29,
            "title": "Monitoring, Logging & Observability",
            "skipped": True,
        },
        {
            "day": 31,
            "title": "Capstone Project & Final Demo",
            "passed": True,
            "attempts": 1,
        },
    ],
    "signals": {
        "commitDays": 28,
        "missionsCompleted": 30,
        "missionsFirstTry": 20,
    },
}


# ---------------------------------------------------------------------------
# Scripted LLM
# ---------------------------------------------------------------------------


def scripted_llm_responder():
    """
    Deterministic responder for the test suite.

    Current architecture has exactly three LLM-backed operations:

    1. Interviewer -> question generation
    2. Evaluator -> answer evaluation
    3. Feedback -> final report

    Curriculum-day selection and follow-up decisions are deterministic
    Python logic in the orchestrator. There is no planner LLM call.
    """

    counters = {
        "question": 0,
    }

    def _responder(system: str, user: str) -> str:
        system_lower = system.lower()

        # ---------------------------------------------------------------
        # Interviewer
        # ---------------------------------------------------------------

        if "senior technical interviewer" in system_lower:
            counters["question"] += 1

            return json.dumps(
                {
                    "question": (
                        f"Scripted question number "
                        f"{counters['question']}?"
                    ),
                    "topic": "Scripted Topic",
                    "difficulty": "medium",
                    "question_type": "conceptual",
                    "is_follow_up": False,
                    "reason": "scripted",
                }
            )

        # ---------------------------------------------------------------
        # Evaluator
        # ---------------------------------------------------------------

        if '"correctness"' in system_lower:
            return json.dumps(
                {
                    "score": 7.0,
                    "correctness": 0.7,
                    "technical_depth": 0.7,
                    "completeness": 0.7,
                    "reasoning": 0.7,
                    "communication": 0.8,
                    "strengths": [
                        "Explained the core mechanism correctly"
                    ],
                    "gaps": [
                        "Missing production trade-off discussion"
                    ],
                    "missing_concepts": [
                        "latency trade-offs"
                    ],
                    "follow_up_needed": False,
                    "suggested_follow_up_area": "",
                }
            )

        # ---------------------------------------------------------------
        # Feedback
        # ---------------------------------------------------------------

        if '"summary"' in system_lower:
            return json.dumps(
                {
                    "summary": (
                        "Candidate demonstrated solid understanding "
                        "across RAG and agentic topics."
                    ),
                    "strengths": [
                        "Strong grasp of embeddings",
                        "Clear communication",
                    ],
                    "gaps": [
                        "Limited depth on multi-agent orchestration"
                    ],
                    "next": [
                        "Review agent memory patterns",
                        "Practice explaining trade-offs",
                    ],
                }
            )

        # ---------------------------------------------------------------
        # Fallback
        # ---------------------------------------------------------------

        return json.dumps(
            {
                "reply": "scripted default"
            }
        )

    return _responder


# ---------------------------------------------------------------------------
# Test fixture
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def isolated_state():
    """
    Reset all process-level singletons before every test and install a
    deterministic scripted mock LLM.

    This prevents:
    - sessions leaking between tests
    - InterviewService singleton state leaking
    - LLM calls depending on an external API
    """

    reset_session_manager()
    reset_interview_service()

    set_llm_client(
        MockLLMClient(
            responder=scripted_llm_responder()
        )
    )

    yield

    reset_session_manager()
    reset_interview_service()
```
