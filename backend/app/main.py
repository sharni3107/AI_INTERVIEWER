from fastapi import FastAPI

from app.api.interviews import router as interview_router


app = FastAPI(
    title="AI Interview Agent",
    description="Adaptive, multi-turn technical interviewer for AI Cohort graduates.",
    version="1.0.0",
)

app.include_router(interview_router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}