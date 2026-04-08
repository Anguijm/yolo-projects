#!/usr/bin/env python3
"""
council.py — 7-angle advocate council with veto and escalation.

Usage:
  python3 council.py --gate plan --project cron-explain --context plan.md --goal "cron expression explainer"
  python3 council.py --gate implementation --project cron-explain --context cron-explain/index.html --goal "..."
  python3 council.py --gate tests --project cron-explain --context test_output.txt --goal "..."
  python3 council.py --gate outcome --project cron-explain --context cron-explain/index.html --goal "..."

Each gate runs all 7 angles in parallel via Gemini. Each angle is an advocate for its lens.
Lessons angle has veto power — any objection from lessons halts the build immediately.
Other angles objecting triggers a fix attempt; if the second run still has objections from
the same angle with conflicting required_fixes, the build escalates.

Escalations write COUNCIL_ESCALATION.md and halt. Status surfaces them.

Reads GEMINI_API_KEY from environment.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import google.generativeai as genai
except ImportError:
    genai = None  # type: ignore[assignment]

try:
    import anthropic as anthropic_sdk
except ImportError:
    anthropic_sdk = None  # type: ignore[assignment]

REPO_ROOT = Path(__file__).resolve().parent
ANGLES_DIR = REPO_ROOT / "council" / "angles"
ANGLES = ["bugs", "security", "ui", "guide", "usefulness", "cool", "lessons"]
GATES = ["plan", "implementation", "tests", "outcome"]
MODEL_NAME = "gemini-2.5-flash"  # fast, cheap enough to run 7 per gate × 4 gates
CLAUDE_MODEL = "claude-haiku-4-5-20251001"  # fast fallback when Gemini unavailable
DEFAULT_MAX_CONTEXT = 150000  # default deliverable byte budget per call (overridable via --max-context)
MIN_ELISION = 1000  # files within this margin of the budget pass through unchanged rather than triggering head+tail+marker for trivial overage

# Backend selected at startup
_BACKEND: str = "gemini"  # or "claude"
_ANTHROPIC_CLIENT: Any = None


@dataclass
class Verdict:
    angle: str
    verdict: str  # APPROVE | OBJECT
    severity: str
    reason: str
    required_fix: str
    evidence: str
    veto: bool = False

    @classmethod
    def from_raw(cls, angle: str, raw: str) -> "Verdict":
        """Parse a model response into a Verdict. Tolerates fenced JSON."""
        text = raw.strip()
        if text.startswith("```"):
            # strip code fence
            lines = text.split("\n")
            text = "\n".join(lines[1:-1] if lines[-1].startswith("```") else lines[1:])
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            # Fallback: construct an OBJECT verdict flagging the parse failure
            return cls(
                angle=angle,
                verdict="OBJECT",
                severity="high",
                reason=f"Council member returned unparseable output",
                required_fix="Re-run this angle with stricter JSON instructions",
                evidence=raw[:500],
                veto=False,
            )
        return cls(
            angle=data.get("angle", angle),
            verdict=data.get("verdict", "OBJECT"),
            severity=data.get("severity", "medium"),
            reason=data.get("reason", ""),
            required_fix=data.get("required_fix", ""),
            evidence=data.get("evidence", ""),
            veto=bool(data.get("veto", False)),
        )


def load_angle_prompt(angle: str) -> str:
    path = ANGLES_DIR / f"{angle}.md"
    if not path.exists():
        raise FileNotFoundError(f"Angle prompt missing: {path}")
    return path.read_text()


def load_context_for_lessons() -> str:
    """Lessons angle gets _hot.md + recent learnings.md entries."""
    parts = []
    hot = REPO_ROOT / "_hot.md"
    if hot.exists():
        parts.append("## _hot.md (active patterns)\n\n" + hot.read_text())
    learnings = REPO_ROOT / "learnings.md"
    if learnings.exists():
        content = learnings.read_text()
        # last ~8000 chars to keep prompt size reasonable
        parts.append("## learnings.md (recent entries)\n\n" + content[-8000:])
    return "\n\n".join(parts) if parts else "(no lessons files found)"


def build_user_message(gate: str, project: str, goal: str, context_path: str | None, inline_context: str | None, lessons_context: str = "", max_context: int = DEFAULT_MAX_CONTEXT) -> str:
    parts = [
        f"# Gate: {gate.upper()}",
        f"# Project: {project}",
        f"# Stated goal: {goal}",
        "",
    ]
    if lessons_context:
        parts.append("## Documented lessons you must enforce\n\n" + lessons_context)
        parts.append("")

    if context_path:
        p = Path(context_path)
        if p.exists():
            try:
                content = p.read_text()
                # Files within the limit (or only marginally over by < MIN_ELISION)
                # pass through unchanged. Larger files use a head+tail split with
                # middle elision so code appended at the END of the file (the common
                # case for tock features) is always visible to the council reviewer.
                if len(content) <= max_context + MIN_ELISION:
                    shown = content
                else:
                    head_size = int(max_context * 0.6)
                    tail_size = max_context - head_size
                    elided = len(content) - head_size - tail_size
                    shown = (
                        content[:head_size]
                        + f"\n\n[... {elided} bytes elided from middle of {len(content)}-byte file — head {head_size}B + tail {tail_size}B shown ...]\n\n"
                        + content[-tail_size:]
                    )
                parts.append(f"## Deliverable ({context_path})\n\n```\n{shown}\n```")
            except Exception as e:
                parts.append(f"## Deliverable ({context_path})\n\n[READ ERROR: {e}]")
        else:
            parts.append(f"## Deliverable ({context_path})\n\n[FILE NOT FOUND]")
    if inline_context:
        parts.append(f"## Additional context\n\n{inline_context}")

    parts.append("")
    parts.append("Return ONLY the JSON verdict per your instructions. No prose, no markdown fence.")
    return "\n".join(parts)


def call_angle(angle: str, user_message: str) -> Verdict:
    system_prompt = load_angle_prompt(angle)
    try:
        if _BACKEND == "claude":
            response = _ANTHROPIC_CLIENT.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=1024,
                temperature=0.4,
                system=system_prompt + "\n\nReturn ONLY valid JSON. No prose, no markdown fences.",
                messages=[{"role": "user", "content": user_message}],
            )
            raw = response.content[0].text
        else:
            model = genai.GenerativeModel(
                model_name=MODEL_NAME,
                system_instruction=system_prompt,
                generation_config={"temperature": 0.4, "response_mime_type": "application/json"},
            )
            response = model.generate_content(user_message)
            raw = response.text if hasattr(response, "text") else str(response)
    except Exception as e:
        return Verdict(
            angle=angle,
            verdict="OBJECT",
            severity="high",
            reason=f"API error: {type(e).__name__}",
            required_fix="Retry the call — infrastructure issue, not a real objection",
            evidence=str(e)[:500],
            veto=False,
        )
    return Verdict.from_raw(angle, raw)


def run_gate(gate: str, project: str, goal: str, context_path: str | None, inline_context: str | None, max_context: int = DEFAULT_MAX_CONTEXT) -> list[Verdict]:
    """Run all 7 angles in parallel for a single gate."""
    lessons_ctx = load_context_for_lessons()
    user_msg_base = build_user_message(gate, project, goal, context_path, inline_context, lessons_context="", max_context=max_context)
    user_msg_lessons = build_user_message(gate, project, goal, context_path, inline_context, lessons_context=lessons_ctx, max_context=max_context)

    verdicts: list[Verdict] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(ANGLES)) as pool:
        futures = {}
        for angle in ANGLES:
            msg = user_msg_lessons if angle == "lessons" else user_msg_base
            futures[pool.submit(call_angle, angle, msg)] = angle
        for fut in concurrent.futures.as_completed(futures):
            verdicts.append(fut.result())
    verdicts.sort(key=lambda v: ANGLES.index(v.angle))
    return verdicts


def write_escalation(project: str, gate: str, verdicts: list[Verdict], reason: str) -> Path:
    """Write COUNCIL_ESCALATION.md in project dir and update session_state."""
    proj_dir = REPO_ROOT / project
    proj_dir.mkdir(parents=True, exist_ok=True)
    esc_path = proj_dir / "COUNCIL_ESCALATION.md"

    lines = [
        f"# Council Escalation — {project}",
        "",
        f"**Gate:** {gate}",
        f"**Reason:** {reason}",
        f"**Timestamp:** {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Angle positions",
        "",
    ]
    for v in verdicts:
        veto_tag = " 🚫 VETO" if v.veto else ""
        lines.append(f"### {v.angle.upper()} — {v.verdict} ({v.severity}){veto_tag}")
        lines.append(f"- **Reason:** {v.reason}")
        if v.required_fix:
            lines.append(f"- **Required fix:** {v.required_fix}")
        if v.evidence:
            lines.append(f"- **Evidence:** `{v.evidence[:300]}`")
        lines.append("")
    lines.append("## Resolution")
    lines.append("")
    lines.append("Human decision required. Resume the build after updating session_state.json.")
    lines.append("")
    esc_path.write_text("\n".join(lines))

    # Update session_state.json
    state_path = REPO_ROOT / "session_state.json"
    if state_path.exists():
        try:
            state = json.loads(state_path.read_text())
            escalations = state.setdefault("council_escalations", [])
            escalations.append({
                "project": project,
                "gate": gate,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "reason": reason,
                "path": str(esc_path.relative_to(REPO_ROOT)),
            })
            state_path.write_text(json.dumps(state, indent=2))
        except Exception as e:
            print(f"WARN: could not update session_state.json: {e}", file=sys.stderr)

    return esc_path


def write_gate_result(project: str, gate: str, verdicts: list[Verdict]) -> Path:
    """Write per-gate result JSON alongside the project."""
    proj_dir = REPO_ROOT / project
    proj_dir.mkdir(parents=True, exist_ok=True)
    out_path = proj_dir / f"council_{gate}.json"
    payload = {
        "gate": gate,
        "project": project,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "verdicts": [asdict(v) for v in verdicts],
        "all_approved": all(v.verdict == "APPROVE" for v in verdicts),
        "objections": [asdict(v) for v in verdicts if v.verdict == "OBJECT"],
        "vetoed": any(v.veto and v.verdict == "OBJECT" for v in verdicts),
    }
    out_path.write_text(json.dumps(payload, indent=2))
    return out_path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate", required=True, choices=GATES)
    ap.add_argument("--project", required=True, help="Project name / directory")
    ap.add_argument("--goal", required=True, help="What this build is trying to achieve")
    ap.add_argument("--context", default=None, help="Path to the deliverable to review")
    ap.add_argument("--inline", default=None, help="Inline context text (instead of --context)")
    ap.add_argument("--attempt", type=int, default=1, help="Attempt number (escalate after 2 failed tries)")
    ap.add_argument("--max-context", type=int, default=DEFAULT_MAX_CONTEXT, help=f"Max context bytes from the deliverable file. Files larger than this are split head+tail with middle elision so end-of-file code remains visible. Default {DEFAULT_MAX_CONTEXT}.")
    args = ap.parse_args()

    global _BACKEND, _ANTHROPIC_CLIENT
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        if genai is None:
            print("ERROR: google-generativeai not installed. Run: pip install google-generativeai", file=sys.stderr)
            return 2
        genai.configure(api_key=api_key)
        _BACKEND = "gemini"
        print("[council] Backend: Gemini")
    else:
        anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
        if not anthropic_key:
            print("ERROR: Neither GEMINI_API_KEY nor ANTHROPIC_API_KEY is set", file=sys.stderr)
            return 2
        if anthropic_sdk is None:
            print("ERROR: anthropic package not installed. Run: pip install anthropic", file=sys.stderr)
            return 2
        _ANTHROPIC_CLIENT = anthropic_sdk.Anthropic(api_key=anthropic_key)
        _BACKEND = "claude"
        print(f"[council] Backend: Claude ({CLAUDE_MODEL}) — GEMINI_API_KEY not set, using fallback")

    print(f"[council] Gate: {args.gate} | Project: {args.project} | Attempt: {args.attempt} | max_context: {args.max_context}")
    verdicts = run_gate(args.gate, args.project, args.goal, args.context, args.inline, max_context=args.max_context)
    out_path = write_gate_result(args.project, args.gate, verdicts)

    objections = [v for v in verdicts if v.verdict == "OBJECT"]
    vetoes = [v for v in verdicts if v.veto and v.verdict == "OBJECT"]

    # Print summary for the agent to read
    print(f"\n[council] Results written to {out_path}")
    for v in verdicts:
        icon = "✓" if v.verdict == "APPROVE" else "✗"
        veto_tag = " 🚫VETO" if v.veto and v.verdict == "OBJECT" else ""
        print(f"  {icon} {v.angle:12s} {v.verdict:8s} {v.severity:8s}{veto_tag} — {v.reason[:80]}")

    if vetoes:
        esc_path = write_escalation(
            args.project, args.gate, verdicts,
            reason=f"LESSONS VETO — {vetoes[0].reason}",
        )
        print(f"\n[council] 🚫 LESSONS VETO — escalation written to {esc_path}")
        print("[council] Build MUST halt. Human decision required.")
        return 10  # veto exit code

    if objections:
        if args.attempt >= 2:
            esc_path = write_escalation(
                args.project, args.gate, verdicts,
                reason=f"Unresolved objections after {args.attempt} attempts",
            )
            print(f"\n[council] ⚠ Escalation written to {esc_path}")
            print("[council] Build MUST halt. Human decision required.")
            return 11  # escalation exit code
        else:
            print(f"\n[council] {len(objections)} objection(s). Agent should fix and re-run this gate.")
            return 1  # fix-and-retry exit code

    print(f"\n[council] ✓ All 7 angles APPROVE. Gate {args.gate} passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
