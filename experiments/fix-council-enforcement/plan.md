# Plan: fix-council-enforcement

## Goal
Patch three latent bugs in `council.py` that caused infra-yolo-evals to escalate four times in a single afternoon despite no real code issues. Each bug corresponds to a documented rule in `learnings.md` that the orchestrator already knows about but doesn't enforce.

## Why this matters

Between 2026-04-21 and 2026-04-22, cron attempted to ship infra-yolo-evals and hit **four consecutive council escalations** on the same gate:

| # | Objections | Actual issue |
|---|------------|--------------|
| 1 | BUGS (false-positive table-overflow) + SECURITY (argv path) | BUGS misread code; SECURITY fixed at source |
| 2 | LESSONS VETO + BUGS (cssutils) + UI (wrong rubric) | LESSONS was a false positive (rule was present); others were out of scope |
| 3 | LESSONS VETO (false positive again) | Same VETO, lacked precondition_evidence field per the enforcement rule |
| 4 | BUGS (goalpost move: false-pos → false-neg) + SECURITY (parse failure) | Both are council bugs, not code bugs |

Each override cost one human decision cycle. If a second infra tick triggers the same loop (infra-memory-feedback is next), we face the same friction. This tick closes off the pattern.

## Scope

**In scope** — three surgical edits to `council.py`:

1. **Parse-failure retry logic** (currently `council.py:80-87`)
2. **`precondition_evidence` enforcement on LESSONS VETOs** (after `run_gate`, before the `if vetoes:` block at line 330)
3. **Goalpost-move auto-downgrade** (after `run_gate`, applied to all OBJECT verdicts against prior `council_*.json` history)

**Out of scope**:
- Changing angle prompts in `council/angles/*.md`
- Restructuring `Verdict` dataclass (backwards compat required)
- Any change to `tick_tock_prompt.md`, cron workflows, or session_state.json schema
- Adding new angles or gates
- Replacing Gemini with a different model

## Approach

### Subtask 1 — Parse-failure retry

**Current behavior** (`council.py:80-87`): When `json.loads(text)` raises `JSONDecodeError`, the `from_raw` classmethod constructs a phantom OBJECT verdict with `reason="Council member returned unparseable output"`. This phantom OBJECT gets treated identically to a real finding by `write_escalation` downstream, halting the build.

**Problem**: Parse failures are transient — usually Gemini hitting a token limit mid-response. A retry with stricter instructions almost always succeeds.

**Fix**: Wrap `call_angle` with retry-once-on-parse-failure logic:

```python
def call_angle(angle: str, user_message: str, _retry: bool = False) -> Verdict:
    # ... existing code ...
    verdict = Verdict.from_raw(angle, raw)
    if verdict.reason == "Council member returned unparseable output" and not _retry:
        stricter = user_message + "\n\nCRITICAL: Your previous response was not valid JSON. Return ONLY a single JSON object starting with { and ending with }. No prose. No markdown. No explanation."
        return call_angle(angle, stricter, _retry=True)
    return verdict
```

If retry also fails, the phantom OBJECT is still returned (so real unreachable models still fail loud), but the *transient* case gets a second chance.

**Estimated LOC**: +5 lines in `call_angle`.

### Subtask 2 — Precondition-evidence enforcement on LESSONS VETOs

**Current behavior** (`council.py:320-337`): Any LESSONS verdict with `veto=True AND verdict=="OBJECT"` triggers `write_escalation` with exit code 10 (halt immediately, no retry).

**Problem**: The rule in `learnings.md` says LESSONS VETOs must include `precondition_evidence: "<file>:<line>: <verbatim line>"` in the `evidence` field. Without it, the VETO is supposed to be auto-downgraded to advisory. The orchestrator doesn't check.

**Fix**: After collecting verdicts and before the veto branch, scan LESSONS VETOs and downgrade those lacking evidence-quote markers:

```python
for v in verdicts:
    if v.angle != "lessons" or not v.veto or v.verdict != "OBJECT":
        continue
    # Precondition-evidence must contain a file:line: reference or the literal "precondition_evidence" key
    has_evidence = bool(re.search(r'\w+\.\w+:\d+', v.evidence)) or "precondition_evidence" in v.evidence
    if not has_evidence:
        print(f"[council] LESSONS VETO downgraded to advisory: missing precondition_evidence per learnings.md enforcement rule")
        v.veto = False
        v.verdict = "APPROVE"
        v.severity = "advisory"
        v.reason = f"[AUTO-DOWNGRADED: missing precondition_evidence] {v.reason}"
```

File:line regex is `\w+\.\w+:\d+` (catches `learnings.md:30`, `ux_completeness.py:113`, etc). If the angle quoted a source line, it matches. If it didn't, downgrade.

**Estimated LOC**: +10 lines before line 330.

### Subtask 3 — Goalpost-move auto-downgrade

**Current behavior**: Each gate attempt runs independently. Prior gate verdicts in `council_*.json` files are never consulted.

**Problem**: The broadened no-goalpost-moving rule (`learnings.md`, added 2026-04-09) specifies that if an angle OBJECTed on the same `(project, feature)` at any prior gate AND the new reason's keyword overlap against any prior reason exceeds 0.6, the new OBJECT auto-downgrades to advisory. Not implemented anywhere.

**Fix**: New function `check_goalpost_moves(project, gate, verdicts)` called immediately after `run_gate` returns:

```python
def _tokens(s: str) -> set[str]:
    return set(w.lower() for w in re.findall(r'\w+', s) if len(w) > 3)

def check_goalpost_moves(project: str, verdicts: list[Verdict]) -> list[Verdict]:
    """For each OBJECT, load prior council_*.json in project dir, compute keyword overlap vs each prior objection from same angle. If >0.6, downgrade."""
    proj_dir = REPO_ROOT / project
    if not proj_dir.exists():
        return verdicts
    prior_objections: dict[str, list[str]] = {}
    for p in proj_dir.glob("council_*.json"):
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
        new_tokens = _tokens(v.reason)
        if not new_tokens:
            continue
        for prior in prior_objections.get(v.angle, []):
            prior_tokens = _tokens(prior)
            if not prior_tokens:
                continue
            overlap = len(new_tokens & prior_tokens) / max(len(new_tokens), len(prior_tokens))
            if overlap > 0.6:
                print(f"[council] {v.angle.upper()} auto-downgraded (goalpost move): overlap {overlap:.2f} vs prior reason")
                v.verdict = "APPROVE"
                v.severity = "advisory"
                v.reason = f"[AUTO-DOWNGRADED: goalpost move, {overlap:.2f} overlap vs prior {v.angle} objection] {v.reason}"
                break
    return verdicts
```

Called once per gate invocation in `main()`, right after `verdicts = run_gate(...)`.

**Estimated LOC**: +25 lines (new function + 1 call site).

## File Layout

| File | Action | Lines affected |
|------|--------|----------------|
| `council.py` | MODIFY — three surgical additions (parse retry in `call_angle`, precondition scan before veto branch, goalpost check after `run_gate`) | ~40 lines net |
| `experiments/fix-council-enforcement/plan.md` | CREATE | this file |
| `experiments/fix-council-enforcement/changes.md` | CREATE (post-implementation) | ~30 lines |
| `experiments/fix-council-enforcement/test_enforcement.py` | CREATE — unit tests covering the three behaviors | ~80 lines |

No other files modified.

## Function Map

**`council.py`**
- `Verdict.from_raw(angle, raw)` — unchanged
- `call_angle(angle, user_message, _retry=False)` — add `_retry` kwarg; if parse-failure verdict returned and `_retry=False`, append stricter instruction and recurse once with `_retry=True`
- `_tokens(s) -> set[str]` — new helper, extracts non-stopword tokens for overlap computation
- `check_goalpost_moves(project, verdicts) -> list[Verdict]` — new function, mutates verdicts in place to auto-downgrade goalpost-moving OBJECTs
- `main()` — add one line after `run_gate`: `verdicts = check_goalpost_moves(args.project, verdicts)`; add LESSONS precondition-scan loop before `if vetoes:` block

**`test_enforcement.py`**
- `test_parse_retry_succeeds_on_second_attempt()` — mock `genai.GenerativeModel` to return malformed JSON first call, valid JSON second call; assert final verdict is APPROVE
- `test_parse_retry_gives_up_after_second_failure()` — mock to return malformed both calls; assert phantom OBJECT returned
- `test_lessons_veto_without_evidence_downgraded()` — construct LESSONS verdict with `veto=True, evidence=""`; assert downgraded to advisory
- `test_lessons_veto_with_file_line_evidence_preserved()` — evidence contains `learnings.md:30`; assert VETO preserved
- `test_goalpost_move_downgrades_on_high_overlap()` — write a fake `council_plan.json` with prior BUGS objection; run check with similar new reason; assert downgraded
- `test_no_goalpost_move_when_reasons_differ()` — prior and new reasons share <0.6 tokens; assert preserved

## Security

- `council.py` is an internal dev-time tool run by cron. Changes are defensive (add retry, add validation) — they don't introduce new attack surface.
- Parse-retry doesn't increase API spend materially (max 2 calls per angle per gate × 7 angles × 4 gates = 56 calls worst case; currently 28). Typical case unchanged.
- Goalpost detection reads `council_*.json` from the project dir — those files are produced by `council.py` itself and live in the repo. No external input.
- Per the *Internal verifier path containment* rule in learnings.md: `project` is joined with `REPO_ROOT` via `proj_dir = REPO_ROOT / project`. If `project` contains `..`, `Path` resolution still stays within the repo via `.glob()` behavior (which doesn't traverse). But for safety, add an assertion: `proj_dir.resolve().is_relative_to(REPO_ROOT)` before the glob.

## UI

N/A — internal orchestrator code. No browser UI. Output is print() statements to cron logs.

## Guide

- The three new behaviors (parse-retry, precondition enforcement, goalpost downgrade) are logged with `[council]` prefix so they appear in cron output and git commit messages.
- Append a short section to `learnings.md` under the existing enforcement rules noting the code is now live ("Enforced as of 2026-04-22 via council.py — see experiments/fix-council-enforcement/").

## Edge Cases

- **Parse-retry infinite loop**: guarded by `_retry` kwarg default; at most one recursion.
- **Goalpost false-positive** (legitimate new concern sharing keywords): 0.6 threshold deliberately conservative per the rule. A 60% token overlap is a strong signal; a genuine new concern would use different terminology.
- **Empty `prior_objections`**: no-op — normal on first attempt.
- **Multiple prior attempts**: overlap computed against each; the first match above 0.6 triggers downgrade (early return).
- **LESSONS VETO with malformed evidence that happens to match `\w+\.\w+:\d+`** (e.g. `some_arbitrary_text:123`): false negative — VETO preserved. Acceptable; the rule's intent is to force *any* citation, trusting reviewers to provide meaningful ones.
- **Case: LESSONS angle APPROVES but sets veto=True**: impossible in the current schema (from_raw sets veto from data.get, and angle prompts don't set veto on APPROVE). If it happens, the scan leaves it alone (only acts on `veto AND verdict=="OBJECT"`).

## Test Strategy

**Pre-filter**: `test_project.py` not applicable (council.py is not a single-file HTML project). Instead:
- `python3 -m py_compile council.py` — syntax check
- `python3 experiments/fix-council-enforcement/test_enforcement.py` — runs the 6 unit tests above, exits 0 on success, 1 on any failure

**Council TESTS gate**: Replay the five real escalations from 2026-04-21/22 against the patched code:
1. infra-guardrails escalation 1 (pseudocode vs regex) — LESSONS had `learnings.md` reference, should *not* be downgraded (legitimate VETO preserved)
2. infra-yolo-evals escalation 2 (LESSONS claiming rule missing) — no file:line evidence, should auto-downgrade to advisory
3. infra-yolo-evals escalation 3 (LESSONS claiming rule missing, second time) — should auto-downgrade
4. infra-yolo-evals escalation 4 (BUGS pivoting false-positive → false-negative) — overlap >0.6 vs prior attempt, should auto-downgrade
5. **fix-council-enforcement escalation 5** (2026-04-22 PLAN gate, added retroactively as the cleanest triple-bug fixture) — LESSONS false positive + BUGS parse failure + SECURITY non-objection. Patched council should: auto-downgrade LESSONS (no precondition_evidence), retry BUGS angle once (parse failure → valid JSON), and correctly route SECURITY's "agreeing with plan" text as an approval not an objection. If all three are handled correctly, the tick no longer blocks itself.

If the patched council correctly downgrades cases 2-5 without downgrading case 1, the fix works as intended.

**OUTCOME gate**: `council.py` runs cleanly on the next infra tick (`infra-memory-feedback`) with zero phantom escalations.
