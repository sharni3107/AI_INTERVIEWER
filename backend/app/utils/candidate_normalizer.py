"""
Pure function that normalizes an incoming candidate payload into a
consistent internal representation used by the agents/services.

The REAL candidate.json shape (one entry of the `candidates` array in
candidates.json, which is what the technical spec's POST /api/interview
`candidate` field actually contains) is:

{
    "member": {
        "id": "CAND-001",
        "name": "Sarah Johnson",
        "jobRole": "Senior Data Engineer",
        "yearsExperience": 9,
        "education": "MS Computer Science",
        "status": "COMPLETED"
    },
    "missions": [
        {
            "day": 7,
            "title": "Embeddings Explained",
            "passed": true,
            "attempts": 1
        },
        {
            "day": 29,
            "title": "Monitoring, Logging & Observability",
            "skipped": true
        }
    ],
    "signals": {
        "commitDays": 28,
        "missionsCompleted": 30,
        "missionsFirstTry": 20
    }
}

Notes on fields actually present:

- A mission is either a completed attempt (has "passed": bool and
  "attempts": int) or a skipped mission (has "skipped": true, and no
  "passed"/"attempts").
- There is no "score" field on a mission.
- There is no "topic", "project", or "strong_areas" field on the candidate.

We deliberately do NOT validate against a strict Pydantic schema here.
The official contract says the candidate payload will follow the provided
candidate.json schema without pinning an exact structure.

Instead, we defensively read the fields we know are present and tolerate
missing/partial data.

This is a plain, side-effect-free function, so it lives in utils/ rather
than services/.

app/services/candidate_service.py calls it and adds the
candidate-vs-curriculum business logic on top.
"""

from __future__ import annotations

from typing import Any


class InvalidCandidateDataError(Exception):
    """Raised when the candidate payload is missing required structure."""


def normalize_candidate(
    candidate_raw: dict[str, Any],
) -> dict[str, Any]:
    """
    Normalize the incoming candidate payload into the internal format
    used by the interview agents and services.
    """

    if not isinstance(candidate_raw, dict) or not candidate_raw:
        raise InvalidCandidateDataError(
            "candidate must be a non-empty JSON object"
        )

    member = candidate_raw.get("member", {}) or {}
    missions = candidate_raw.get("missions", []) or []
    signals = candidate_raw.get("signals", {}) or {}

    if not isinstance(member, dict):
        raise InvalidCandidateDataError(
            "candidate.member must be an object"
        )

    if not isinstance(missions, list):
        raise InvalidCandidateDataError(
            "candidate.missions must be an array"
        )

    if not isinstance(signals, dict):
        raise InvalidCandidateDataError(
            "candidate.signals must be an object"
        )

    # Completed/attempted missions.
    completed_missions = [
        mission
        for mission in missions
        if (
            isinstance(mission, dict)
            and mission.get("day") is not None
            and not mission.get("skipped")
        )
    ]

    # Explicitly skipped missions.
    skipped_missions = [
        mission
        for mission in missions
        if (
            isinstance(mission, dict)
            and mission.get("day") is not None
            and mission.get("skipped")
        )
    ]

    # Passed missions.
    passed_days = sorted(
        {
            mission["day"]
            for mission in completed_missions
            if mission.get("passed") is True
        }
    )

    # Failed missions.
    failed_days = sorted(
        {
            mission["day"]
            for mission in completed_missions
            if mission.get("passed") is False
        }
    )

    # Skipped missions.
    skipped_days = sorted(
        {
            mission["day"]
            for mission in skipped_missions
        }
    )

    # All missions the candidate attempted.
    attempted_days = sorted(
        {
            mission["day"]
            for mission in completed_missions
        }
    )

    # Missions requiring multiple attempts.
    high_attempt_missions = [
        mission
        for mission in completed_missions
        if (
            isinstance(
                mission.get("attempts"),
                (int, float),
            )
            and mission["attempts"] >= 3
        )
    ]

    # A struggled day is either:
    # - a mission requiring 3+ attempts, or
    # - a mission that was attempted but failed.
    struggled_days = sorted(
        {
            mission["day"]
            for mission in high_attempt_missions
        }
        | set(failed_days)
    )

    # Map curriculum day -> mission title.
    day_titles = {
        mission["day"]: mission.get("title", "")
        for mission in missions
        if (
            isinstance(mission, dict)
            and mission.get("day") is not None
        )
    }

    return {
        "candidate_id": member.get("id", "unknown"),
        "name": member.get("name", "Candidate"),
        "job_role": member.get("jobRole", ""),
        "years_experience": member.get("yearsExperience"),
        "education": member.get("education", ""),
        "status": member.get("status", ""),
        "missions": missions,
        "day_titles": day_titles,
        "passed_days": passed_days,
        "failed_days": failed_days,
        "skipped_days": skipped_days,
        "attempted_days": attempted_days,
        "struggled_days": struggled_days,
        "commit_days": signals.get("commitDays"),
        "missions_completed": signals.get("missionsCompleted"),
        "missions_first_try": signals.get("missionsFirstTry"),
        "raw": candidate_raw,
    }