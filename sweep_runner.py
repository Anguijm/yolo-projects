#!/usr/bin/env python3
"""sweep_runner.py — parameterized experiment sweeps for the YOLO tick queue.

Reads a sweep spec, enumerates a parameter grid (cartesian product), and
enqueues N parameterized tick specs into ``tick_tock.tick_queue_approved`` in
``.harness/session_state.json``. The existing YOLO loop then drains them
one-per-tick through the normal 4 council gates.

Design: sweep_runner is a PURE PRODUCER. It does NOT invoke council.py, run
builds, call any LLM, or shell out. It only enumerates and enqueues; the loop
runs each generated tick with the full, unmodified council treatment. See
experiments/infra-sweep-mode/README.md for rationale.

Dependency-free: prefers PyYAML when importable, else falls back to an embedded
minimal YAML-subset parser (PyYAML is not installed in CI).

Usage:
  python3 sweep_runner.py --spec <spec.yaml> --dry-run        # inspect, write nothing
  python3 sweep_runner.py --spec <spec.yaml>                  # enqueue (atomic, idempotent)
  python3 sweep_runner.py --selftest                          # parse+enumerate+build the bundled example
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from itertools import product
from pathlib import Path

DEFAULT_STATE = ".harness/session_state.json"
EXAMPLE_SPEC = "experiments/infra-sweep-mode/sweep_spec_example.yaml"
MAX_RUNS_CEILING = 50  # hard upper bound; max_runs is clamped to this
VALID_TYPES = {"infrastructure", "yolo", "experiment"}
# param values must be benign scalars — no shell/path/markup metacharacters.
SAFE_VALUE_RE = re.compile(r"^[A-Za-z0-9._/+\- ]+$")
# deliverable paths: repo-relative, no traversal, no absolute, no NUL.
SAFE_PATH_RE = re.compile(r"^[A-Za-z0-9._/\-]+$")
# defense-in-depth: reject the most common prompt-injection phrasings in
# owner-authored static text fields before they reach a downstream LLM tick.
INJECTION_RE = re.compile(
    r"(?i)(ignore\s+((all|previous|prior|the|these|those|any)\s+)*(instructions|context|rules)"
    r"|disregard\s+((the|all|any|previous|prior)\s+)*(above|previous|prior|instructions)"
    r"|you\s+are\s+now\b|new\s+system\s+prompt|</?\s*(system|assistant)\b)"
)


# --------------------------------------------------------------------------- #
# Spec loading                                                                #
# --------------------------------------------------------------------------- #
def _mini_yaml_load(text: str) -> dict:
    """Parse the documented YAML subset: top-level scalars, one level of nested
    mapping, block sequences (``- item``), and inline flow lists (``[a, b]``).
    Not a general YAML parser — closed subset, covered by --selftest."""
    root: dict = {}
    stack = [(-1, root)]  # (indent, container)
    pending_list_key = None  # (indent, key, parent) awaiting block-seq items

    def scalar(tok: str):
        tok = tok.strip()
        if not tok:
            return None
        if (tok[0] == tok[-1]) and tok[0] in "\"'" and len(tok) >= 2:
            return tok[1:-1]
        low = tok.lower()
        if low == "true":
            return True
        if low == "false":
            return False
        if low in ("null", "~"):
            return None
        try:
            return int(tok)
        except ValueError:
            pass
        try:
            return float(tok)
        except ValueError:
            pass
        return tok

    def flow_list(tok: str):
        inner = tok.strip()[1:-1].strip()
        if not inner:
            return []
        return [scalar(p) for p in _split_flow(inner)]

    for raw in text.splitlines():
        # strip comments — quote-aware: '#' opens a comment only at line start
        # or after whitespace, and never inside a quoted string.
        line = _strip_comment(raw).rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        body = line.strip()

        # pop containers shallower-or-equal
        while stack and indent <= stack[-1][0] and len(stack) > 1:
            stack.pop()
        parent = stack[-1][1]

        if body.startswith("- "):
            item = body[2:].strip()
            if pending_list_key is not None:
                _, lk, lparent = pending_list_key
                lparent.setdefault(lk, [])
                if not isinstance(lparent[lk], list):
                    lparent[lk] = []
                lparent[lk].append(scalar(item))
            continue

        if ":" not in body:
            continue
        key, _, val = body.partition(":")
        key = key.strip()
        val = val.strip()
        if val == "":
            # could open a nested mapping or a block sequence; defer decision
            new_map: dict = {}
            parent[key] = new_map
            stack.append((indent, new_map))
            pending_list_key = (indent, key, parent)
        elif val.startswith("[") and val.endswith("]"):
            parent[key] = flow_list(val)
            pending_list_key = None
        else:
            parent[key] = scalar(val)
            pending_list_key = None
    return root


def _strip_comment(line: str) -> str:
    """Remove a trailing YAML comment, respecting quotes. '#' starts a comment
    only at line start or when preceded by whitespace, and never inside a
    quoted string (fixes corruption of values containing '#')."""
    q = None
    for i, ch in enumerate(line):
        if q:
            if ch == q:
                q = None
        elif ch in "\"'":
            q = ch
        elif ch == "#" and (i == 0 or line[i - 1] in " \t"):
            return line[:i]
    return line


def _split_flow(inner: str) -> list[str]:
    """Split a flow-list body on commas, respecting quotes."""
    parts, buf, q = [], [], None
    for ch in inner:
        if q:
            buf.append(ch)
            if ch == q:
                q = None
        elif ch in "\"'":
            q = ch
            buf.append(ch)
        elif ch == ",":
            parts.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
    if buf:
        parts.append("".join(buf))
    return [p.strip() for p in parts if p.strip()]


def load_spec(path: str) -> dict:
    text = Path(path).read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore
        return yaml.safe_load(text) or {}
    except ImportError:
        return _mini_yaml_load(text)


# --------------------------------------------------------------------------- #
# Validation                                                                  #
# --------------------------------------------------------------------------- #
def validate_spec(spec: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(spec, dict):
        return ["spec is not a mapping"]
    if not spec.get("sweep_id"):
        errs.append("missing required key: sweep_id")
    bt = spec.get("base_tick")
    if not isinstance(bt, dict):
        errs.append("missing/invalid base_tick (must be a mapping)")
        bt = {}
    else:
        if not bt.get("name"):
            errs.append("base_tick.name is required")
        t = bt.get("type", "infrastructure")
        if t not in VALID_TYPES:
            errs.append(f"base_tick.type {t!r} not in {sorted(VALID_TYPES)}")
        # defense-in-depth: scan static (whole) text fields for prompt-injection
        # phrasings before they reach a downstream LLM tick.
        for tf in ("name", "idea", "rationale", "council_focus", "plan_summary"):
            tv = bt.get(tf)
            if isinstance(tv, str) and INJECTION_RE.search(tv):
                errs.append(f"base_tick.{tf} contains a prompt-injection phrase (rejected as defense-in-depth)")
        dps = bt.get("deliverable_paths", [])
        if not isinstance(dps, list) or not dps:
            errs.append("base_tick.deliverable_paths must be a non-empty list")
        else:
            for p in dps:
                # placeholders are allowed here; the *substituted* path is
                # re-checked in build_entries. Static part must be path-safe.
                static = re.sub(r"\{[^}]+\}", "", str(p))
                if ".." in str(p) or str(p).startswith("/") or (static and not SAFE_PATH_RE.match(static)):
                    errs.append(f"unsafe deliverable_path: {p!r} (no traversal/absolute/metachars)")

    grid = spec.get("param_grid")
    if not isinstance(grid, dict) or not grid:
        errs.append("param_grid must be a non-empty mapping (use the queue directly for a 0-param tick)")
        grid = {}
    grid_keys = set()
    for k, vals in grid.items():
        grid_keys.add(k)
        if not isinstance(vals, list) or not vals:
            errs.append(f"param_grid.{k} must be a non-empty list")
            continue
        for v in vals:
            if not SAFE_VALUE_RE.match(str(v)):
                errs.append(f"param_grid.{k} value {v!r} has unsafe characters (allowed: alnum . _ / + - space)")

    # every {placeholder} used must reference a known grid key
    used = set()
    for field in ("plan_summary", "deliverable_paths", "name", "council_focus"):
        val = bt.get(field)
        for s in (val if isinstance(val, list) else [val]):
            if isinstance(s, str):
                used.update(re.findall(r"\{([^}]+)\}", s))
    unknown = used - grid_keys
    if unknown:
        errs.append(f"placeholder(s) reference unknown param(s): {sorted(unknown)}")

    mr = spec.get("max_runs", 10)
    if not isinstance(mr, int) or mr < 1:
        errs.append("max_runs must be a positive integer")
    bc = spec.get("budget_cap", 5.0)
    if not isinstance(bc, (int, float)) or bc <= 0:
        errs.append("budget_cap must be a positive number")
    ec = spec.get("est_cost_per_run", 0.5)
    if not isinstance(ec, (int, float)) or ec <= 0:
        errs.append("est_cost_per_run must be a positive number")
    return errs


# --------------------------------------------------------------------------- #
# Enumeration + entry building                                                #
# --------------------------------------------------------------------------- #
def effective_cap(spec: dict) -> tuple[int, str]:
    """Resolve the binding cap on generated entries from BOTH max_runs and the
    budget. Returns (cap, binding_reason). budget_cap is a total-sweep USD
    budget; est_cost_per_run (default $0.50) converts it to a run count, so the
    budget actually constrains the sweep rather than being a decorative field."""
    max_runs = min(int(spec.get("max_runs", 10)), MAX_RUNS_CEILING)
    est = float(spec.get("est_cost_per_run", 0.5))
    budget_cap = float(spec.get("budget_cap", 5.0))
    budget_runs = int(budget_cap // est) if est > 0 else max_runs
    if budget_runs < max_runs:
        return budget_runs, f"budget_cap ${budget_cap}/${est} per run = {budget_runs} runs"
    if int(spec.get("max_runs", 10)) > MAX_RUNS_CEILING:
        return max_runs, f"max_runs clamped to ceiling {MAX_RUNS_CEILING}"
    return max_runs, f"max_runs {max_runs}"


def enumerate_grid(param_grid: dict) -> list[dict]:
    keys = sorted(param_grid)  # deterministic order
    combos = []
    for values in product(*(param_grid[k] for k in keys)):
        combos.append({k: v for k, v in zip(keys, values)})
    return combos


def _slug(s: str) -> str:
    s = re.sub(r"[^A-Za-z0-9]+", "-", str(s)).strip("-").lower()
    return s or "x"


def _subst(value, combo: dict):
    def one(s: str) -> str:
        out = s
        for k, v in combo.items():
            out = out.replace("{" + k + "}", str(v))
        return out
    if isinstance(value, list):
        return [one(str(x)) for x in value]
    if isinstance(value, str):
        return one(value)
    return value


def build_entries(spec: dict, date: str) -> tuple[list[dict], list[str]]:
    """Return (entries, warnings). Caller must have validated the spec."""
    warnings: list[str] = []
    bt = spec["base_tick"]
    sweep_id = spec["sweep_id"]
    combos = enumerate_grid(spec["param_grid"])
    grid_total = len(combos)

    cap, binding = effective_cap(spec)
    if grid_total > cap:
        warnings.append(f"grid size {grid_total} exceeds cap {cap} ({binding}); dropping {grid_total - cap} combo(s)")
        combos = combos[:cap]

    budget_cap = float(spec.get("budget_cap", 5.0))
    entries = []
    for i, combo in enumerate(combos, start=1):
        suffix = "__".join(f"{_slug(k)}_{_slug(v)}" for k, v in sorted(combo.items()))
        name = f"{_slug(bt['name'])}--{suffix}"
        plan_summary = _subst(bt.get("plan_summary", ""), combo)
        param_tail = " | ".join(f"param_{k}={v}" for k, v in sorted(combo.items()))
        plan_summary = (plan_summary + (" " if plan_summary else "") + f"[sweep {sweep_id} {i}/{len(combos)}: {param_tail}]").strip()

        dps = _subst(bt.get("deliverable_paths", []), combo)
        # re-check the *substituted* paths (defends against hostile param values)
        for p in dps:
            if ".." in p or p.startswith("/") or not SAFE_PATH_RE.match(p):
                raise ValueError(f"substituted deliverable_path unsafe: {p!r} (combo {combo})")

        entries.append({
            "name": name,
            "type": bt.get("type", "infrastructure"),
            "idea": _subst(bt.get("idea", ""), combo),
            "rationale": _subst(bt.get("rationale", ""), combo),
            "deliverable_paths": dps,
            "plan_summary": plan_summary,
            "council_focus": _subst(bt.get("council_focus", ""), combo),
            "sweep_id": sweep_id,
            "sweep_run": i,
            "sweep_total": len(combos),
            "sweep_params": combo,
            "budget_cap": budget_cap,
            "queued_date": date,
        })
    return entries, warnings


# --------------------------------------------------------------------------- #
# Enqueue (atomic, idempotent)                                                #
# --------------------------------------------------------------------------- #
def enqueue(entries: list[dict], state_path: str, sweep_id: str) -> dict:
    p = Path(state_path)
    if not p.exists():
        raise FileNotFoundError(f"state file not found: {state_path} (refusing to create a fresh one)")

    # Hold an exclusive advisory lock across the whole read-modify-write so a
    # concurrent writer (e.g. the cron) cannot interleave and cause a lost
    # update. fcntl is POSIX-only; degrade gracefully where it is unavailable
    # (atomic os.replace below still prevents a *corrupt* file regardless).
    lock_handle = None
    try:
        import fcntl
        lock_path = p.with_suffix(p.suffix + ".lock")
        lock_handle = open(lock_path, "w")
        fcntl.flock(lock_handle, fcntl.LOCK_EX)
    except (ImportError, OSError):
        lock_handle = None

    try:
        return _enqueue_locked(entries, p, sweep_id)
    finally:
        if lock_handle is not None:
            lock_handle.close()


def _enqueue_locked(entries: list[dict], p: Path, sweep_id: str) -> dict:
    state = json.loads(p.read_text(encoding="utf-8"))
    tt = state.get("tick_tock")
    if not isinstance(tt, dict) or not isinstance(tt.get("tick_queue_approved"), list):
        raise KeyError("session_state.json missing tick_tock.tick_queue_approved list")

    queue = tt["tick_queue_approved"]
    existing_names = {e.get("name") for e in queue if isinstance(e, dict)}
    added, skipped = [], 0
    for e in entries:
        if e["name"] in existing_names:
            skipped += 1
            continue
        queue.append(e)
        existing_names.add(e["name"])
        added.append(e["name"])

    # atomic write: temp + os.replace (crash-safe; no partial state)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(state, indent=2), encoding="utf-8")
    os.replace(tmp, p)
    return {"added": added, "skipped": skipped, "queue_len": len(queue)}


# --------------------------------------------------------------------------- #
# CLI + selftest                                                              #
# --------------------------------------------------------------------------- #
def _print_entries(entries: list[dict]) -> None:
    for e in entries:
        print(f"  [{e['sweep_run']}/{e['sweep_total']}] {e['name']}")
        print(f"      deliverables: {e['deliverable_paths']}")
        print(f"      params: {e['sweep_params']}")


def selftest() -> int:
    spec_path = EXAMPLE_SPEC
    if not Path(spec_path).exists():
        print(f"FAIL: example spec not found at {spec_path}", file=sys.stderr)
        return 1
    spec = load_spec(spec_path)
    errs = validate_spec(spec)
    ok = True

    def check(cond: bool, msg: str):
        nonlocal ok
        print(("PASS" if cond else "FAIL") + ": " + msg)
        ok = ok and cond

    check(not errs, f"example spec validates ({errs})")
    if errs:
        return 1
    grid = enumerate_grid(spec["param_grid"])
    expected = 1
    for v in spec["param_grid"].values():
        expected *= len(v)
    check(len(grid) == expected, f"grid size {len(grid)} == product {expected}")

    entries, warns = build_entries(spec, date="2026-01-01")
    cap, _ = effective_cap(spec)
    check(len(entries) == min(expected, cap), f"entry count {len(entries)} == min(grid,cap)={min(expected, cap)}")
    names = [e["name"] for e in entries]
    check(len(names) == len(set(names)), "entry names unique")
    no_residual = all("{" not in e["plan_summary"] and all("{" not in p for p in e["deliverable_paths"]) for e in entries)
    check(no_residual, "no residual {placeholders} after substitution")
    required = {"name", "type", "idea", "deliverable_paths", "plan_summary", "council_focus"}
    check(all(required <= set(e) for e in entries), "all entries have required queue fields")
    check(all(e["budget_cap"] == float(spec.get("budget_cap", 5.0)) for e in entries), "budget_cap stamped on every entry")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Enumerate a sweep grid and enqueue N parameterized ticks. "
                                             "Pure producer: does not run builds or call council.py.")
    ap.add_argument("--spec", help="Path to the sweep spec (YAML; subset documented in README).")
    ap.add_argument("--state", default=DEFAULT_STATE, help=f"Path to session_state.json (default {DEFAULT_STATE}).")
    ap.add_argument("--dry-run", action="store_true", help="Enumerate + show entries; write nothing (safe default for inspection).")
    ap.add_argument("--date", default=None, help="queued_date stamp (default: today, UTC).")
    ap.add_argument("--selftest", action="store_true", help="Run built-in tests against the bundled example spec.")
    args = ap.parse_args()

    if args.selftest:
        return selftest()
    if not args.spec:
        ap.error("--spec is required (or use --selftest)")

    spec = load_spec(args.spec)
    errs = validate_spec(spec)
    if errs:
        print("spec validation failed:", file=sys.stderr)
        for e in errs:
            print(f"  - {e}", file=sys.stderr)
        return 2

    date = args.date or datetime.now(timezone.utc).date().isoformat()
    entries, warnings = build_entries(spec, date=date)
    for w in warnings:
        print(f"WARNING: {w}", file=sys.stderr)

    print(f"sweep_id={spec['sweep_id']}  grid->entries={len(entries)}")
    _print_entries(entries)

    if args.dry_run:
        print("\n[dry-run] nothing written.")
        return 0

    result = enqueue(entries, args.state, spec["sweep_id"])
    print(f"\nenqueued {len(result['added'])} (skipped {result['skipped']} already-present); "
          f"tick_queue_approved now {result['queue_len']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
