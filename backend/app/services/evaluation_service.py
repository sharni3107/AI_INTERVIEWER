"""
Evaluation service.

Calls the EvaluatorAgent for a single candidate answer and records
the resulting evaluation onto the interview session state.

Kept separate from the orchestrator so that answer evaluation and
storage have one clear owner and can also be tested independently.
"""

from __future__ import annotations

from typing import Optional

from app.agents.evaluator import EvaluatorAgent
from app.core.llm_client import BaseLLMClient
from app.schemas.evaluation import EvaluationRecord
from app.schemas.interview import QuestionRecord
from app.state.interview_state import InterviewState


class EvaluationService:
    def __init__(
        self,
        llm_client: Optional[BaseLLMClient] = None,
        evaluator: Optional[EvaluatorAgent] = None,
    ):
        self._evaluator = (
            evaluator
            or EvaluatorAgent(
                llm_client=llm_client
            )
        )

    def evaluate_and_record(
        self,
        state: InterviewState,
        question: QuestionRecord,
        answer: str,
    ) -> EvaluationRecord:
        """
        Evaluate a candidate answer and record the evaluation
        on the interview state.
        """

        evaluation = self._evaluator.evaluate(
            state,
            question,
            answer,
        )

        state.record_answer_and_evaluation(
            answer,
            evaluation,
        )

        return evaluation