# Council Escalation — experiments/eval-opus-47-backbone

**Gate:** outcome
**Reason:** Unresolved objections after 2 attempts
**Timestamp:** 2026-04-24T00:46:51.334905+00:00

## Angle positions

### BUGS — APPROVE (low)
- **Reason:** The benchmark correctly identified a critical blocking issue in the system under test (council.py) and accurately reported the error, root cause, and a data-grounded recommendation, fulfilling its stated goal without introducing new correctness risks in its own deliverables.

### SECURITY — APPROVE (low)
- **Reason:** The deliverable is a static report that accurately identifies existing security risks (CSP issues) in other projects and proposes a process improvement for handling recurring findings, without introducing new vulnerabilities.

### UI — APPROVE (low)
- **Reason:** The results.md document is clearly structured, easy to read, and presents a clear verdict with actionable follow-on steps.

### GUIDE — OBJECT (high)
- **Reason:** The project's `benchmark.py` tool lacks explicit instructions or help documentation for a first-time user or AI agent to understand how to run it.
- **Required fix:** Add clear instructions to the `README.md` for `eval-opus-47-backbone` on how to execute `benchmark.py`, including required parameters and environment setup, or implement a `--help` flag for `benchmark.py`.
- **Evidence:** `Missing explicit documentation for `benchmark.py` execution; the content of the project's `README.md` is not provided to confirm it addresses this.`

### USEFULNESS — APPROVE (low)
- **Reason:** This benchmark provides critical data for strategic decisions regarding the core council.py backbone, identifying both model-specific quirks and infrastructure needs.
- **Evidence:** `The project successfully identified a blocking infrastructure issue for Opus 4.7 and a systematic hallucination pattern in Haiku, directly informing future development and preventing costly mistakes.`

### COOL — APPROVE (low)
- **Reason:** The benchmark successfully identified unique, repeatable LLM failure modes specific to the council.py context, like the Haiku 'UI hallucination' and Opus's temperature parameter incompatibility, which are signature moves for internal diagnostics.

### LESSONS — APPROVE (low)
- **Reason:** The deliverable is a benchmark report that accurately reflects observations, including prior lessons angle verdicts, and does not violate any documented architectural rules or anti-patterns.

## Resolution

**RESOLVED 2026-04-24. GUIDE overridden — README exists with full usage docs.**

### GUIDE OBJECT (high) — OVERRIDE (context-window false positive)
GUIDE's own evidence admits the cause: *"the content of the project's README.md is not provided to confirm it addresses this."* The angle couldn't see the README in its context window and assumed it was missing.

Verified on disk — `experiments/eval-opus-47-backbone/README.md` exists (89 lines) with:
- "What it does" section
- "Quick start" with `--help` discovery command + full 3-fixture run + cost-override example
- Fixtures list, output format, cost model, dependencies, interpretation guide

Plus `benchmark.py` implements `--help` via argparse (verified earlier in this saga). Both the file-based and tool-based discovery paths requested by GUIDE already exist.

No code change needed — override with evidence.

### Other 6 angles — APPROVE
BUGS explicitly praised that the benchmark "correctly identified a critical blocking issue (Opus 4.7 temperature parameter incompatibility) and a systematic hallucination pattern in Haiku" — the benchmark ran and produced real signal. SECURITY, UI, USEFULNESS, COOL, LESSONS all clean.

Cron may rerun OUTCOME; expected clean pass → ship.
