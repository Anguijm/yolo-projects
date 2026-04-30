# Lessons — cloud-sandbox-adapter

## Cycle 1 (baseline + perturbations)
**Tried:** demo (local + dry-run), multi-step build sequence (write 2
files, exec twice), bad-command exec (exit 127), read of nonexistent
file.

**Learned:**
- The basic interface holds up under a multi-step sequence.
- **Behavior diverges between Local and DryRun on the read-error path.**
  LocalSandbox raises FileNotFoundError; DryRunSandbox silently returns
  `""`. A loop relying on the dry run to surface "this would fail
  remotely" misses missing-file errors entirely.
- The DryRun trace correctly captures order and op names but doesn't
  capture *content* of writes (only byte counts). For a real migration
  audit you'd want to know what was written, especially for short text
  writes.
- exec(bad cmd) returns exit=127 with informative stderr — good. No
  exception escapes — good.

**Change for cycle 2:**
- DryRunSandbox.read should raise FileNotFoundError if the path wasn't
  written in the same session (track written paths in a set).
- DryRunSandbox should optionally store write contents (capped at e.g.
  4KB per write) so the trace is forensic-quality, not just structural.
- Add a "replay" mode: feed a DryRun trace into a LocalSandbox and
  verify the same exit codes / outputs. That's the actual migration
  validation harness.

## Cycle 2 (DryRun read raises + write capture)
**Tried:** read() of unwritten path; read() after write(); inspect trace for `preview` field.
**Learned:** DryRun now raises FileNotFoundError matching LocalSandbox; writes capture content (up to 4KB) into trace.preview. Forensic-quality trace.
**Change for cycle 3:** Add a `replay_trace(trace, target_adapter)` helper that takes a DryRun trace and re-runs it on a real adapter, asserting the same exit codes. That's the actual migration validation harness — what the README promised.

## Cycle 3 (replay_trace integration)
**Tried:** Build a DryRun trace; replay against a fresh LocalSandbox in a tempdir.
**Learned:** **Replay matches dry-run cleanly: 5 ops, 0 discrepancies.** This is the migration validation harness the README originally promised. A future E2BSandbox can be validated by running the same trace through it and asserting 0 discrepancies vs LocalSandbox.
**Change for cycle 4:** Operational space exhausted for the local-only test. Next real exercise needs a remote adapter to validate end-to-end.

## Cycle 4 (smoke)
**Tried:** Standard demo.
**Learned:** No regressions. Operational space exhausted.

## Cycle 5 (final smoke)
**Result:** replay_trace returns 0 discrepancies between DryRun and Local. Verdict: **adopt** for Local + DryRun + replay; **defer** remote adapters until E2B/Modal integration is scoped.
