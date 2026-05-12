"""Pydantic schema for the per-angle council Verdict.

Field set lifted from .harness/scripts/council_rules.md (the canonical
spec each persona's prompt emits). Validation rules encode the same
invariants the runner currently enforces via ad-hoc string checks.
"""
from __future__ import annotations

from typing import Literal, Optional

try:
    from pydantic import BaseModel, Field, field_validator
except ImportError as e:
    raise SystemExit(
        "pydantic not installed. Run: pip install pydantic\n"
        f"(import error: {e})"
    )


VerdictKind = Literal["APPROVE", "OBJECT"]
Severity = Literal["low", "medium", "high"]


class Verdict(BaseModel):
    """A single angle's council Verdict, as emitted by the LLM."""

    verdict: VerdictKind = Field(
        description="APPROVE if the diff passes this angle's rubric, "
                    "OBJECT if it fails."
    )
    severity: Severity = Field(
        description="Severity of the OBJECT; 'low' is advisory, 'high' is "
                    "blocking. APPROVE verdicts conventionally use 'low'."
    )
    reason: str = Field(
        min_length=1,
        description="One-sentence summary of why this verdict was issued."
    )
    required_fix: Optional[str] = Field(
        default=None,
        description="What the author must change to flip an OBJECT to "
                    "APPROVE. Required for OBJECT verdicts."
    )
    evidence: Optional[str] = Field(
        default=None,
        description="file.ext:NN citation grounding the verdict. "
                    "Mandatory for LESSONS OBJECTs (precondition_evidence "
                    "enforcement); strongly recommended for all OBJECTs."
    )

    @field_validator("reason")
    @classmethod
    def reason_not_whitespace(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("reason must not be empty or whitespace-only")
        return v


class ParseError(BaseModel):
    """Structured failure result from parse_verdict()."""

    kind: Literal["json_decode", "schema_violation", "empty_output"]
    detail: str
    raw_snippet: str = Field(
        description="First and last 200 chars of the offending raw output, "
                    "joined by ' ... ' for log readability."
    )
