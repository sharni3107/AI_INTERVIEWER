"""
Shape of the final structured feedback report.

Exact contract required by the technical spec:

{
    "summary": str,
    "strengths": [str],
    "gaps": [str],
    "next": [str]
}
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field


@dataclass
class FeedbackReport:
    summary: str

    strengths: list[str] = field(
        default_factory=list
    )

    gaps: list[str] = field(
        default_factory=list
    )

    next: list[str] = field(
        default_factory=list
    )

    def to_dict(self) -> dict:
        return asdict(self)