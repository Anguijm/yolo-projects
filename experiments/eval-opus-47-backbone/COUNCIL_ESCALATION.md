# Council Escalation — experiments/eval-opus-47-backbone

**Gate:** plan
**Reason:** Unresolved objections after 2 attempts
**Timestamp:** 2026-04-23T20:56:36.935317+00:00

## Angle positions

### BUGS — OBJECT (medium)
- **Reason:** The hardcoded cost model values for Haiku and Opus can become stale if API prices change, leading to incorrect cost calculations and potentially flawed recommendations.
- **Required fix:** The cost model should be configurable (e.g., via environment variables or a configuration file) or dynamically fetched, and a mechanism for updating these values should be documented.
- **Evidence:** `Cost model: Haiku $0.80/$4.00 per MTok in/out; Opus $15.00/$75.00 per MTok in/out`

### SECURITY — APPROVE (low)
- **Reason:** The plan explicitly addresses key security concerns such as API key handling, output path validation, and module state restoration, leaving no apparent exploitable surfaces.

### UI — APPROVE (low)
- **Reason:** The plan for the command-line interface provides excellent real-time feedback, clear error messages, and a comprehensive guide for first-time users, ensuring a frictionless experience.

### GUIDE — OBJECT (medium)
- **Reason:** The CLI tool does not explicitly plan for a `--help` flag or equivalent in-app documentation for discovering its arguments and usage.
- **Required fix:** Add a `--help` flag to `benchmark.py` that lists all CLI arguments and their descriptions.
- **Evidence:** `Missing mention of `--help` in 'UI' or 'Guide' sections of plan.md`

### USEFULNESS — APPROVE (low)
- **Reason:** This project provides a critical, repeatable tool for making data-driven decisions on core infrastructure (LLM backbone), directly impacting the quality and efficiency of the council.py system.
- **Evidence:** `The benchmark addresses a recurring need to evaluate new LLM models or model updates against existing ones, ensuring the 'council.py' tool remains performant and cost-effective; it's a tool for ongoing maintenance and improvement, not a one-off experiment.`

### COOL — APPROVE (low)
- **Reason:** This internal benchmark script demonstrates elegant, non-invasive engineering for state isolation and token tracking, which are signature moves for a robust internal tool.

### LESSONS — APPROVE (low)
- **Reason:** No documented lessons from _hot.md or learnings.md are violated by the plan.

## Resolution

**RESOLVED 2026-04-24. Both accepted — plan.md updated.**

### BUGS (medium) — ACCEPTED
Hardcoded cost model can go stale. Plan now specifies:
- Defaults documented with a pricing snapshot date (2026-04-24)
- Env-var overrides: `HAIKU_COST_IN`, `HAIKU_COST_OUT`, `OPUS_COST_IN`, `OPUS_COST_OUT`
- Runtime log line when overrides are applied
- `results.md` captures effective cost values per run for reproducibility
- `README.md` will document the single-line edit path for default updates

### GUIDE (medium) — ACCEPTED
`--help` flag added via `argparse` (auto-generated). Guide section updated with explicit `--help` usage example as the discovery path. Also added a cost-override example showcasing the new env-var knobs.

### Other 5 angles — APPROVE
SECURITY, UI, USEFULNESS, COOL, LESSONS all clean.

Cron may rerun PLAN; expected clean pass.
