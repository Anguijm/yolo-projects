# eval-opus-47-backbone — Benchmark Results

**Run date:** 2026-04-24 UTC  
**Benchmark file:** `benchmark_results_20260424T004229.json`  
**Cost model:** Haiku $0.80/$4.00 per MTok in/out · Opus $15.00/$75.00 per MTok in/out

---

## Verdict

**Recommendation: KEEP Haiku. DO NOT swap to Opus 4.7 without fixing `call_angle`.**

Opus 4.7 is fully blocked — `temperature` is a deprecated parameter for this model and council.py hardcodes `temperature=0.4`. Until that is fixed, Opus 4.7 cannot serve as the council backbone. A follow-on infrastructure tick to remove `temperature` from `call_angle` (or make it model-conditional) is required before Opus can be re-evaluated.

---

## Haiku Results (3 fixtures)

| Fixture | Approve | Object | Latency | Tokens in | Tokens out | Cost |
|---|---|---|---|---|---|---|
| url-dissect | 2/7 | 5/7 | 6.22s | 85,773 | 1,985 | $0.0766 |
| cron-explain | 2/7 | 5/7 | 7.02s | 93,102 | 1,769 | $0.0816 |
| uuid-inspector | 2/7 | 5/7 | 5.51s | 86,844 | 1,897 | $0.0771 |
| **Total** | **6/21** | **15/21** | — | **265,719** | **5,651** | **$0.2353** |

### Per-angle APPROVE/OBJECT across 3 fixtures (Haiku)

| Angle | url-dissect | cron-explain | uuid-inspector | Pattern |
|---|---|---|---|---|
| bugs | OBJECT | OBJECT | OBJECT | 3/3 OBJECT — different reason each time |
| security | OBJECT | OBJECT | OBJECT | 3/3 OBJECT — always cites `unsafe-inline` CSP |
| ui | OBJECT | OBJECT | OBJECT | 3/3 OBJECT — **see hallucination note below** |
| guide | OBJECT | OBJECT | OBJECT | 3/3 OBJECT — no README.md (real, consistent) |
| usefulness | APPROVE | APPROVE | APPROVE | 3/3 APPROVE |
| cool | APPROVE | OBJECT | OBJECT | 1/3 — cron-explain/uuid-inspector "no signature move" |
| lessons | OBJECT | APPROVE | APPROVE | 1/3 OBJECT — url-dissect split/join lesson |

### Notable findings in Haiku verdicts

**SECURITY over-indexing on portfolio-wide CSP:** All 3 fixtures get OBJECT for `unsafe-inline` and `connect-src *`. This is the YOLO portfolio's known architectural choice — single-file HTML with no build step. The security angle is applying a per-project standard to a portfolio-wide decision that council.py itself approved when naval-scribe established this pattern (naval-scribe/CONSTRAINTS.md). Action: consider adding a portfolio-level `SECURITY_BASELINE.md` similar to CONSTRAINTS.md.

**UI hallucination — "injected accessibility override with !important":** All 3 fixtures received nearly identical UI OBJECT verdicts claiming an accessibility override forces illegible font sizes. None of these projects contain such an override — this is fabricated evidence consistent across all 3. This is a Haiku-specific pattern where the UI angle invents a specific technical detail and applies it uniformly. Severity: the benchmark detects a systematic Haiku hallucination type that was previously invisible (no cross-fixture comparison existed).

**BUGS substantive and fixture-specific:** Each fixture's bugs objection cited a different technical concern (URL regex, DOW normalization in cron, UUID v1 bit manipulation). These are plausible but unverified — Haiku may be finding real latent bugs or fabricating credible-sounding ones. Requires code audit to distinguish signal from noise.

**GUIDE consistently correct:** No README.md files exist for these utility tools. This is real and consistent.

---

## Opus 4.7 Results

| Fixture | Approve | Object | Latency | Tokens | Cost | Error |
|---|---|---|---|---|---|---|
| url-dissect | 0/7 | 7/7 | 0.26s | 0 | $0.00 | BadRequestError |
| cron-explain | 0/7 | 7/7 | 0.24s | 0 | $0.00 | BadRequestError |
| uuid-inspector | 0/7 | 7/7 | 0.13s | 0 | $0.00 | BadRequestError |

**Root cause:** `temperature` parameter is deprecated for `claude-opus-4-7`. The Anthropic API returns HTTP 400 with message: `"temperature" is deprecated for this model`. council.py's `call_angle` hardcodes `temperature=0.4` (line 188) — this is incompatible with Opus 4.7.

**Diagnosis path:** Direct `client.messages.create(model="claude-opus-4-7", ...)` without `temperature` returns OK. The benchmark's monkey-patch correctly forced the Claude backend; the failure is in `council.py:188`, not in the benchmark.

**Fix required (not in scope for this tick):** Remove `temperature=0.4` from `call_angle`, or make it conditional: `params = {...}; if "opus-4-7" not in CLAUDE_MODEL: params["temperature"] = 0.4`. The Anthropic SDK's Opus 4.7 extended-thinking mode does not accept temperature.

---

## Cost summary

| Model | Runs | Total cost |
|---|---|---|
| haiku (claude-haiku-4-5-20251001) | 3 | $0.2353 |
| opus (claude-opus-4-7) | 3 | $0.0000 (all failed) |
| **Grand total** | 6 | **$0.2353** |

Cost estimate from plan (~$0.30 total) was close for the Haiku portion. Opus portion was $0 due to the API blocker.

---

## Follow-on actions

1. **Fix `call_angle` temperature handling** (infrastructure tick) — remove or conditionalize `temperature=0.4` for Opus 4.7 compatibility. One-line fix in `council.py:188`.
2. **Re-run benchmark after fix** — use `--fixtures 3` once Opus runs successfully to get quality comparison.
3. **Investigate UI hallucination pattern** — the "accessibility override !important" fabrication is a systematic Haiku failure mode worth documenting in `learnings.md`.
4. **Portfolio-level CSP baseline** — add a `SECURITY_BASELINE.md` (similar to naval-scribe/CONSTRAINTS.md) documenting that `unsafe-inline` is the YOLO portfolio's intended CSP so SECURITY can stop objecting to it on every individual project.
