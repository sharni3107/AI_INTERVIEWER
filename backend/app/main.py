"""
FastAPI application entrypoint.

Run locally with:
    uvicorn app.main:app --reload --port 8000

By default LLM_PROVIDER=openrouter (GPT-4o Mini via OpenRouter).
Set OPENROUTER_API_KEY in the environment or a .env file.

Use LLM_PROVIDER=mock for zero-dependency local development/tests
with no API key.
"""

from fastapi import FastAPI

from app.api.interviews import router as interview_router


app = FastAPI(
    title="AI Interview Agent",
    description=(
        "Adaptive, multi-turn technical interviewer "
        "for AI Cohort graduates."
    ),
    version="1.0.0",
)

app.include_router(interview_router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}