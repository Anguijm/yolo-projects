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

Auto-downgrade enforcement (each rule converts an OBJECT verdict to APPROVE-advisory
and prefixes `reason` with `[AUTO-DOWNGRADED: …]` so the trigger is self-evident):

  1. Parse-failure retry — unparseable JSON triggers one stricter retry inside
     `call_angle` before falling back to a phantom OBJECT.
  2. LESSONS VETO precondition_evidence — `enforce_lessons_precondition` downgrades
     LESSONS vetoes whose `evidence` lacks a `file.ext:NN` citation OR the literal
     string `precondition_evidence`.
  3. Goalpost-move — `check_goalpost_moves` downgrades OBJECTs whose keyword
     overlap vs any prior reason for the same `(project, angle)` exceeds
     `GOALPOST_OVERLAP_THRESHOLD` (0.35).
  4. BUGS hallucination — `detect_bugs_hallucination` downgrades BUGS OBJECTs that
     claim "undefined/missing/not defined" symbols when those symbols are actually
     defined in cited files (language-aware definition-pattern check, JS/TS/HTML/Py).

Cron logs every fired downgrade with the `[council]` prefix. See learnings.md
"Council enforcement rules are now LIVE in code" for the full per-rule rationale
and `experiments/fix-council-enforcement/` + `experiments/fix-council-bugs-hallucination/`
for the ticks that shipped them.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PARSE_FAILURE_MARKER = "Council member returned unparseable output"
# Goalpost threshold — learnings.md:22 originally specified 0.6 as an educated guess.
# Empirical data from 4 real infra-yolo-evals escalations 2026-04-21/22 shows actual
# same-concern / opposite-framing pairs land around 0.35-0.43 using the count/max metric,
# while genuinely distinct concerns land at 0.00. 0.35 cleanly separates the observed cases.
GOALPOST_OVERLAP_THRESHOLD = 0.35
# Pattern for a file:line: citation — e.g. "learnings.md:30", "council.py:87"
EVIDENCE_CITATION_RE = re.compile(r"\w+\.\w+:\d+")
# Words 4+ chars long, lowercased, used for keyword-overlap scoring between objections
TOKEN_RE = re.compile(r"\w{4,}")
# Patch 4 constants — BUGS hallucination detection. Every quantifier is bounded;
# none have nested or overlapping character classes so worst-case backtracking is
# linear in input length (ReDoS-safe even on adversarial 2MB-cap file content).
_HALLUCINATION_CLAIM_RE = re.compile(
    r"\b(undefined|undeclared|not\s{1,4}defined|does\s{1,4}not\s{1,4}exist|missing)\b",
    re.IGNORECASE,
)
# Identifiers cap at 80 chars — real symbol names never approach that; bound prevents pathological inputs.
_SYMBOL_FROM_FIX_RE = re.compile(r"`([a-zA-Z_][a-zA-Z0-9_]{2,80})`")
# Path segment capped at 200 chars, line number capped at 8 digits (covers files up to 100M lines).
_FILE_REF_RE = re.compile(r"([\w\-/.]{1,200}\.\w{1,12}):(\d{1,8})(?:[-,]\d{1,8})?")

try:
    import google.generativeai as genai
except ImportError:
    genai = None  # type: ignore[assignment]

try:
    import anthropic as anthropic_sdk
except ImportError:
    anthropic_sdk = None  # type: ignore[assignment]

REPO_ROOT = Path(__file__).resolve().parent.parent.parent  # .harness/scripts/council.py → repo root
ANGLES_DIR = REPO_ROOT / ".harness" / "council"
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
    parse_failed: bool = False  # set True by from_raw on JSONDecodeError; drives retry in call_angle

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
            # Fallback: construct an OBJECT verdict and mark it with parse_failed=True so
            # call_angle can reliably detect the transient failure regardless of the
            # human-readable reason text (critique from fix-council-enforcement PLAN
            # gate escalation 6, 2026-04-21: string-based detection is brittle).
            return cls(
                angle=angle,
                verdict="OBJECT",
                severity="high",
                reason=PARSE_FAILURE_MARKER,
                required_fix="Re-run this angle with stricter JSON instructions",
                evidence=raw[:500],
                veto=False,
                parse_failed=True,
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
    learnings = REPO_ROOT / ".harness" / "learnings.md"
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


def call_angle(angle: str, user_message: str, _retry: bool = False) -> Verdict:
    system_prompt = load_angle_prompt(angle)
    try:
        if _BACKEND == "claude":
            # Opus 4.7 and later use extended thinking and reject `temperature` as a
            # deprecated parameter (per eval-opus-47-backbone benchmark 2026-04-24
            # which surfaced the BadRequestError: 'temperature is deprecated for
            # this model'). Keep the 0.4 temperature for Haiku/Sonnet classes where
            # it still works as a determinism knob; omit it for Opus-4.x.
            claude_params = {
                "model": CLAUDE_MODEL,
                "max_tokens": 1024,
                "system": system_prompt + "\n\nReturn ONLY valid JSON. No prose, no markdown fences.",
                "messages": [{"role": "user", "content": user_message}],
            }
            if "opus-4" not in CLAUDE_MODEL:
                claude_params["temperature"] = 0.4
            response = _ANTHROPIC_CLIENT.messages.create(**claude_params)
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
    verdict = Verdict.from_raw(angle, raw)
    # Patch 1: parse-failure retry — if JSON didn't parse, from_raw sets
    # parse_failed=True. Retry once with stricter instructions before giving up —
    # most parse failures are the model truncating mid-JSON, not a genuine refusal.
    # Using the flag (not string comparison against reason) per BUGS critique on
    # fix-council-enforcement PLAN gate 2026-04-21.
    if verdict.parse_failed and not _retry:
        stricter = user_message + (
            "\n\nCRITICAL: Your previous response was not valid JSON. "
            "Return ONLY a single JSON object starting with { and ending with }. "
            "No prose. No markdown. No explanation. Complete every field before the closing brace."
        )
        print(f"[council] {angle}: parse-failure retry", file=sys.stderr)
        return call_angle(angle, stricter, _retry=True)
    return verdict


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


def enforce_lessons_precondition(verdicts: list[Verdict]) -> list[Verdict]:
    """Patch 2: downgrade LESSONS VETOs whose evidence lacks a file:line: citation.

    Per learnings.md:20 "Enforcement (added 2026-04-08 after 3rd false positive)":
    every LESSONS VETO must include precondition_evidence quoting a verbatim source
    line. VETOs without such a citation are auto-downgraded to low-severity advisory
    and cannot block the build. Mutates verdicts in place.
    """
    for v in verdicts:
        if v.angle != "lessons" or not v.veto or v.verdict != "OBJECT":
            continue
        has_citation = bool(EVIDENCE_CITATION_RE.search(v.evidence or ""))
        has_marker = "precondition_evidence" in (v.evidence or "")
        if has_citation or has_marker:
            continue
        print(
            "[council] LESSONS VETO auto-downgraded to advisory — missing precondition_evidence "
            "(no file:line citation or 'precondition_evidence' marker in evidence field). "
            "Per learnings.md:20 enforcement rule.",
            file=sys.stderr,
        )
        v.veto = False
        v.verdict = "APPROVE"
        v.severity = "advisory"
        v.reason = f"[AUTO-DOWNGRADED: LESSONS VETO missing precondition_evidence] {v.reason}"
    return verdicts


def _tokens(s: str) -> set[str]:
    """Extract non-short lowercase tokens from a string for keyword-overlap scoring."""
    return {w.lower() for w in TOKEN_RE.findall(s or "")}


def _keyword_overlap(a: str, b: str) -> float:
    """Shared tokens divided by max token count — the metric learnings.md:22 specifies."""
    ta, tb = _tokens(a), _tokens(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / max(len(ta), len(tb))


def check_goalpost_moves(project: str, verdicts: list[Verdict]) -> list[Verdict]:
    """Patch 3: auto-downgrade OBJECTs that repeat a prior same-angle objection.

    Per learnings.md:22 "No goalpost-moving (broadened 2026-04-09 to cross-gate)":
    when an angle has previously OBJECTed on the same (project, feature), a new
    OBJECT from that angle whose keyword overlap vs any prior reason exceeds
    GOALPOST_OVERLAP_THRESHOLD auto-downgrades to advisory.

    Loads prior council_*.json files in the project directory; mutates verdicts
    in place. Safe no-op if the project directory doesn't exist yet.
    """
    proj_dir = REPO_ROOT / project
    try:
        resolved = proj_dir.resolve()
        resolved.relative_to(REPO_ROOT)  # raises ValueError if outside
    except ValueError:
        print(f"[council] refusing to read council_*.json outside REPO_ROOT for '{project}'", file=sys.stderr)
        return verdicts
    if not proj_dir.exists():
        return verdicts
    prior_objections: dict[str, list[str]] = {}
    for p in sorted(proj_dir.glob("council_*.json")):
        try:
            data = json.loads(p.read_text())
            for v in data.get("verdicts", []):
                if v.get("verdict") == "OBJECT":
                    prior_objections.setdefault(v["angle"], []).append(v.get("reason", ""))
        except Exception:
            continue
    for v in verdicts:
        if v.verdict != "OBJECT":
            continue
        for prior in prior_objections.get(v.angle, []):
            overlap = _keyword_overlap(v.reason, prior)
            if overlap > GOALPOST_OVERLAP_THRESHOLD:
                print(
                    f"[council] {v.angle.upper()} auto-downgraded (goalpost move): "
                    f"overlap {overlap:.2f} vs prior reason. Per learnings.md:22.",
                    file=sys.stderr,
                )
                v.veto = False
                v.verdict = "APPROVE"
                v.severity = "advisory"
                v.reason = (
                    f"[AUTO-DOWNGRADED: goalpost move, {overlap:.2f} overlap vs prior {v.angle} "
                    f"objection] {v.reason}"
                )
                break
    return verdicts


def _symbol_defined_in_content(symbol: str, content: str, ext: str) -> bool:
    """Return True if symbol appears to be *defined* in content via language-specific patterns.

    Uses definition-syntax patterns rather than bare identifier search to avoid matching
    comments, string literals, and call sites. Falls back False for unknown file types.
    """
    esc = re.escape(symbol)
    # Quantifier bounds below cap worst-case backtracking on adversarial inputs (ReDoS guard
    # — file-size already capped at 2MB by caller). Real source code never has 80 leading
    # spaces or 500 chars between `(` and `)` on a method signature.
    if ext in (".html", ".js", ".ts"):
        patterns = [
            rf"function\s{{1,8}}{esc}\b",
            rf"(?:const|let|var)\s{{1,8}}{esc}\b\s{{0,8}}=",
            # Method shorthand — line-anchored, requires `{` after `)` to exclude call sites.
            rf"(?m)^[ \t]{{0,80}}(?:async\s{{1,4}})?(?:static\s{{1,4}})?{esc}\b\s{{0,8}}\([^)]{{0,500}}\)\s{{0,8}}\{{",
            # TypeScript/JS class, interface, type alias, enum declarations
            rf"(?:class|interface|type|enum)\s{{1,8}}{esc}\b",
        ]
    elif ext == ".py":
        patterns = [
            rf"(?:def|class)\s{{1,8}}{esc}\b\s{{0,8}}[:(]",
            rf"(?m)^[ \t]{{0,80}}{esc}\b\s{{0,8}}=",
        ]
    else:
        return False
    return any(re.search(p, content, re.MULTILINE) for p in patterns)


def detect_bugs_hallucination(verdict: "Verdict", project: str) -> bool:
    """Return True if a BUGS OBJECT verdict appears to cite nonexistent symbols.

    Scans each cited file with language-aware definition patterns — not bare text search —
    so comments and call sites never trigger false auto-downgrades.
    Returns True only when any cited file disproves the "undefined symbol" claim.
    """
    if verdict.angle != "bugs" or verdict.verdict != "OBJECT":
        return False
    reason_text = verdict.reason or ""
    if not _HALLUCINATION_CLAIM_RE.search(reason_text):
        return False
    # Extract only symbols that appear BEFORE each claim keyword — not after — to avoid
    # matching scope/container identifiers like "not defined IN `getFullState`" or
    # alternative fix suggestions like "replace with `setDraftStatus`" from required_fix.
    claimed_symbols: set[str] = set()
    for m in _HALLUCINATION_CLAIM_RE.finditer(reason_text):
        window_start = max(0, m.start() - 100)
        claimed_symbols.update(_SYMBOL_FROM_FIX_RE.findall(reason_text[window_start:m.start()]))
    if not claimed_symbols:
        return False
    evidence = verdict.evidence or ""
    file_refs = list(_FILE_REF_RE.finditer(evidence))
    files = [m.group(1) for m in file_refs]
    if not files:
        proj_dir = REPO_ROOT / project
        for candidate in ("index.html", "benchmark.py", "build_memory.py"):
            for base in (proj_dir, REPO_ROOT):
                if (base / candidate).exists():
                    files.append(str(base / candidate))
                    break
    if not files:
        return False
    for raw_path in files:
        path_obj = Path(raw_path) if os.path.isabs(raw_path) else (REPO_ROOT / raw_path)
        try:
            resolved = path_obj.resolve()
            resolved.relative_to(REPO_ROOT)  # path-traversal guard — raises ValueError if outside repo
            if resolved.stat().st_size > 2_000_000:  # skip files >2 MB
                continue
            content = resolved.read_text(encoding="utf-8", errors="replace")
        except (FileNotFoundError, ValueError, OSError):
            continue
        ext = resolved.suffix.lower()
        # Definition-pattern check — requires actual definition syntax, not comments or call sites
        for s in claimed_symbols:
            if _symbol_defined_in_content(s, content, ext):
                return True
    return False


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
    state_path = REPO_ROOT / ".harness" / "session_state.json"
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
    # Enforcement passes (learnings.md:20 and :22 — previously documented but not implemented)
    verdicts = enforce_lessons_precondition(verdicts)
    verdicts = check_goalpost_moves(args.project, verdicts)
    # Patch 4: detect BUGS hallucinations — auto-downgrade "undefined symbol" claims
    # contradicted by the actual file contents (cited-line check + definition-pattern check).
    for v in verdicts:
        if detect_bugs_hallucination(v, args.project):
            print(
                "[council] BUGS auto-downgraded (hallucinated symbol) — "
                "verified definition exists in cited files",
                file=sys.stderr,
            )
            v.verdict = "APPROVE"
            v.severity = "advisory"
            v.reason = f"[AUTO-DOWNGRADED: hallucinated symbol claim, symbols present in cited files] {v.reason}"
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
