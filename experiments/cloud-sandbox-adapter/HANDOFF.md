# Handoff — cloud-sandbox-adapter

**Verdict (after 5 cycles):** adopt (Local + DryRun); defer (remote)

**One-line:** Sandbox interface + Local + DryRun + replay validator for migrating loop execution off-laptop.

## What this is
A minimal `SandboxAdapter` interface (`create / exec / write / read /
teardown`) plus three reference implementations: LocalSandbox (current
behavior), DryRunSandbox (records every op without executing), and a
`replay_trace(trace, target)` helper that runs a recorded trace against a
real adapter and reports any discrepancies.

## Why an agent might want to adopt this
- You're considering moving execution to E2B / Modal / Daytona / GitHub
  Actions ephemeral runners.
- You want to know what your code is *actually doing* at the shell layer
  without running it (DryRun mode).
- You want a validator that says "yes, this trace would behave the same
  on the real backend" before flipping the switch.

## Production-ready bits
- DryRun trace captures op order, file paths, write previews (up to 4KB).
- DryRun.read raises FileNotFoundError on unwritten paths (matches
  LocalSandbox semantics).
- replay_trace returns a structured discrepancy list; verified to return 0
  discrepancies on a 5-op trace round-trip.

## What still needs work
- E2BSandbox / ModalSandbox / DaytonaSandbox adapters not built. The
  interface is ready for them; integration with each provider's SDK is a
  separate, scoped piece of work.
- `MIGRATION.md` lists the four call-site clusters in the YOLO loop that
  need rewriting before a remote adapter can be flipped on.

## How to run
```
python3 sandbox_adapter.py demo            # LocalSandbox
python3 sandbox_adapter.py demo --dry-run  # DryRunSandbox + trace
```

## Files
- `sandbox_adapter.py` — interface + adapters + replay (~180 LOC)
- `MIGRATION.md` — call-site audit

## Verdict: adopt for Local + DryRun. Defer remote until a provider is chosen.
