# Plan: adopt-bare-agent

## Goal
Build the smallest possible Anthropic SDK agent loop (~60–80 lines) with 3 built-in tools and no framework dependencies, plus a comparison protocol and README.

## Scope
**In scope:**
- `experiments/adopt-bare-agent/bare_agent.py` — 60–80 line agent loop using raw `anthropic` SDK
- `experiments/adopt-bare-agent/comparison_plan.md` — human-executable protocol for comparing bare_agent.py vs harness-cli
- `experiments/adopt-bare-agent/README.md` — when to use each approach

**Out of scope:**
- Running the actual comparison study
- Modifying harness-cli, council.py, or any other pipeline file
- Adding retry logic, logging frameworks, or production hardening
- Reusing any code from harness-cli (written from scratch)

## Approach
Three sequential subtasks:

**Subtask 1 — bare_agent.py**
Write a self-contained Python file:
1. Import `anthropic`, `os`, `subprocess`, `json`, `sys` (5 lines)
2. Define 3 tool handler functions with one-line docstrings: `read_file(path)`, `write_file(path, content)`, `run_shell(command, timeout=30)` (~15 lines) — `run_shell` uses `subprocess.run(..., timeout=30)` and catches `subprocess.TimeoutExpired`
3. Inline tool registry as a Python list of dicts (name/description/input_schema) (~30 lines — this is the verbose part that pushes us toward 80)
4. `run_agent(task, model, max_turns)` with one-line docstring: while-loop calling `client.messages.create()`, checking `stop_reason`, dispatching tool_use blocks, injecting tool_result messages, breaking on `end_turn` (~18 lines)
5. `__main__` block: parse `sys.argv[1]` as task, call `run_agent`, print result (~5 lines)

Total: ~73 lines. Feasibility: 50 lines is not achievable without sacrificing readable tool schemas; 80 is achievable with tight but readable code. The `timeout` on `run_shell` prevents indefinite hangs.

**Subtask 2 — comparison_plan.md** (no dependency on subtask 1 completion)
Define the measurement protocol: shared task spec, what to record (LOC, API calls, wall time, output quality rubric), acceptance criteria, how to report.

**Subtask 3 — README.md** (depends on subtask 1 being written)
Two sections: "Use bare_agent.py when…" and "Use harness-cli when…", plus a one-liner run example.

## File Layout
| File | Action | Notes |
|------|--------|-------|
| `experiments/adopt-bare-agent/plan.md` | create | this file |
| `experiments/adopt-bare-agent/bare_agent.py` | create | ~69 lines |
| `experiments/adopt-bare-agent/comparison_plan.md` | create | ~35 lines |
| `experiments/adopt-bare-agent/README.md` | create | ~25 lines |

No existing files are modified.

## Function Map
**`experiments/adopt-bare-agent/bare_agent.py`**
- `read_file(path: str) -> str` — reads and returns file content, or error string on IOError
- `write_file(path: str, content: str) -> str` — writes content to path, returns "ok" or error string
- `run_shell(command: str, timeout: int = 30) -> str` — runs command via subprocess with 30s timeout, returns stdout+stderr truncated to 2000 chars; catches TimeoutExpired
- `run_agent(task: str, model: str = "claude-opus-4-7", max_turns: int = 20) -> str` — main agent loop; returns final assistant message text; docstring: "Run the minimal agent loop until end_turn or max_turns."
- `__main__` block (not a function) — parses argv[1], calls run_agent, prints result

## Security
- `run_shell` executes arbitrary shell commands via `subprocess.run(shell=True, ...)` with a 30-second timeout. This is intentional for a local research prototype. README will carry a prominent **WARNING** that this must never be used with untrusted task strings.
- `write_file` can overwrite any writable path reachable by the process. Path traversal is not mitigated — again intentional for a scratch prototype. README documents this.
- Trust boundary: local developer use only. Not to be deployed as a service or piped from untrusted input.
- No hardcoded credentials. API key via `ANTHROPIC_API_KEY` env var (SDK default).
- No SQL, no HTML rendering, no XSS surface.
- `subprocess.run` uses `timeout=30` to prevent indefinite blocking; `TimeoutExpired` is caught and returned as a tool error string.

## UI
CLI tool only:
- Invocation: `python3 bare_agent.py "<task>"`
- During execution: prints each tool call name + first 80 chars of input to stdout
- Final: prints the model's closing message text
- On error (API, tool exception): prints to stderr, exits 1

## Guide
- README.md: plain prose, no jargon. Two clear bullet lists. One `python3` example command. Prominent **WARNING** about run_shell and write_file security implications.
- comparison_plan.md: numbered protocol steps, table of metrics, human-readable rubric.
- bare_agent.py: one-line docstrings on all 4 functions (`read_file`, `write_file`, `run_shell`, `run_agent`). Inline comments only where the logic is non-obvious (tool_result injection format).

## Edge Cases
| Condition | Handling |
|-----------|---------|
| Model returns `end_turn` immediately (no tools) | Loop exits after first turn, returns text |
| Tool handler raises an exception | Catch, return `"error: <msg>"` as tool_result content |
| Unknown tool name in tool_use block | Return `"error: unknown tool <name>"` as tool_result |
| `max_turns` exceeded | Break loop, append warning to return string |
| Empty `sys.argv` | Print usage and exit 1 |
| `ANTHROPIC_API_KEY` not set | SDK raises `AuthenticationError`; propagate (not our job to handle) |

## Test Strategy
1. `python3 -c "import ast; ast.parse(open('experiments/adopt-bare-agent/bare_agent.py').read())"` — syntax check
2. `python3 experiments/adopt-bare-agent/bare_agent.py "read experiments/adopt-bare-agent/README.md and tell me how many lines it has"` — end-to-end smoke test; verify it completes without error and prints a sensible answer
3. Verify all 3 deliverable files exist and are non-empty
4. Count lines in bare_agent.py — must be ≤ 100 (warn if > 80)
