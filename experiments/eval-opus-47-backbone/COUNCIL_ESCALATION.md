# Council Escalation — experiments/eval-opus-47-backbone

**Gate:** implementation
**Reason:** Unresolved objections after 2 attempts
**Timestamp:** 2026-04-24T00:33:35.028038+00:00

## Angle positions

### BUGS — OBJECT (high)
- **Reason:** The cost model allows environment variables to set negative costs, which would produce incorrect and misleading benchmark results.
- **Required fix:** Modify `_env_float` or `_load_cost_model` to validate that all cost values (HAIKU_COST_IN/OUT, OPUS_COST_IN/OUT) are non-negative, exiting with an error if a negative value is provided.
- **Evidence:** `def _env_float(name: str, default: float) -> float:
    """Read a float from an env var; exit 1 with clear message on bad value."""
    raw = os.environ.get(name)
    if raw is None:
        return default
    try:
        return float(raw)
    except ValueError:
        print(f"[benchmark] ERROR: {`

### SECURITY — APPROVE (low)
- **Reason:** The script demonstrates robust handling of environment variables, path containment for output files, and proper state isolation for monkey-patching, mitigating common security risks.

### UI — APPROVE (low)
- **Reason:** The command-line interface provides clear usage instructions, helpful dry-run functionality, excellent progress feedback during execution, and actionable error messages.

### GUIDE — APPROVE (low)
- **Reason:** The tool provides comprehensive self-documentation through its docstring, argparse help, clear error messages, and a detailed README, making it highly discoverable for both human users and AI agents.

### USEFULNESS — APPROVE (low)
- **Reason:** This tool provides essential data for making informed, recurring decisions about the core LLM backbone of the council.py system.
- **Evidence:** `It addresses the need for data-driven model selection, cost optimization, and performance monitoring, which are critical for maintaining and evolving the council.py system. This is a clear internal tool with a recurring use case for system maintainers.`

### COOL — APPROVE (low)
- **Reason:** Internal infrastructure tool, exempt from COOL requirements per standing precedent.

### LESSONS — APPROVE (low)
- **Reason:** No documented lessons or anti-patterns were violated. The code correctly handles state restoration and path containment.

## Resolution

**RESOLVED 2026-04-24. BUGS fixed at source.**

### BUGS (high) — FIXED
Legitimate defensive programming. Negative cost values would produce garbage benchmark output.

Fix in `benchmark.py:_env_float`:
```python
if value < 0:
    print(f"[benchmark] ERROR: {name}={raw!r} must be >= 0 (cost per MTok)", file=sys.stderr)
    sys.exit(1)
return value
```

Verified: `HAIKU_COST_IN=-1 python3 -c "from benchmark import _env_float; _env_float('HAIKU_COST_IN', 0.80)"` → exits with `ERROR: HAIKU_COST_IN='-1' must be >= 0 (cost per MTok)`. Non-negative values unchanged.

### Other 6 angles — APPROVE
SECURITY, UI, GUIDE, USEFULNESS, LESSONS all clean. COOL continues to approve under the standing override (explicitly cited: "Internal infrastructure tool, exempt from COOL requirements per standing precedent") — the resume_instructions context injection from the prior round carried correctly.

Cron may rerun IMPLEMENTATION; expected clean pass → TESTS → OUTCOME → ship.
