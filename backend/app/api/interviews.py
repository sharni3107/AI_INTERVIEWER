"""
The ONLY required endpoint (PART 22): POST /api/interview

This module is a thin HTTP adapter. All actual logic lives in
InterviewService / InterviewOrchestrator.

No agent or state code imports FastAPI - only this file does.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.core.llm_client import (
    LLMError,
    LLMMalformedResponseError,
)
from app.schemas.interview import (
    ErrorResponse,
    InterviewRequest,
    InterviewResponse,
)
from app.services.candidate_service import (
    InvalidCandidateDataError,
)
from app.services.curriculum_service import (
    CurriculumLoadError,
)
from app.services.interview_service import (
    InterviewAlreadyCompletedError,
    MissingCandidateError,
    MissingMessageError,
    get_interview_service,
)
from app.state.state_manager import (
    SessionAlreadyExistsError,
    SessionNotFoundError,
)
from app.utils.logger import get_logger


logger = get_logger(__name__)

router = APIRouter(
    prefix="/api",
    tags=["interview"],
)


@router.post(
    "/interview",
    response_model=InterviewResponse,
    responses={
        400: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        502: {"model": ErrorResponse},
    },
)
def interview_turn(
    payload: InterviewRequest,
) -> InterviewResponse:
    """
    Handle one interview turn.

    If `candidate` is provided, a new interview session is started.

    Otherwise, the supplied `message` is treated as the candidate's
    answer to the current interview question.
    """

    service = get_interview_service()

    try:
        if payload.candidate is not None:
            # Start mode.
            result = service.start_interview(
                payload.sessionId,
                payload.candidate,
            )
        else:
            # Continue mode.
            result = service.process_message(
                payload.sessionId,
                payload.message,
            )

        return InterviewResponse(**result)

    except MissingCandidateError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except InvalidCandidateDataError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except MissingMessageError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except SessionAlreadyExistsError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except SessionNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    except InterviewAlreadyCompletedError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except CurriculumLoadError as exc:
        logger.error(
            "Curriculum/techspec load failure: %s",
            exc,
        )

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc

    except (
        LLMError,
        LLMMalformedResponseError,
    ) as exc:
        logger.error(
            "LLM failure while processing interview turn: %s",
            exc,
        )

        raise HTTPException(
            status_code=502,
            detail=f"LLM provider error: {exc}",
        ) from exc