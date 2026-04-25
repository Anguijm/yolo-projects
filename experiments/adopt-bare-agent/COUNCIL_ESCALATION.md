# Council Escalation — experiments/adopt-bare-agent

**Gate:** plan
**Reason:** Unresolved objections after 2 attempts
**Timestamp:** 2026-04-25T04:28:03.349679+00:00

## Angle positions

### BUGS — OBJECT (high)
- **Reason:** The agent lacks retry logic for API calls, making it susceptible to transient failures, and `run_shell` truncates output, potentially leading to incorrect agent reasoning due to incomplete information.
- **Required fix:** Implement basic retry logic for `client.messages.create()` and remove or make configurable the `run_shell` output truncation.
- **Evidence:** `Out of scope: Adding retry logic, logging frameworks, or production hardening; run_shell: returns stdout+stderr truncated to 2000 chars`

### SECURITY — OBJECT (critical)
- **Reason:** The agent's `run_shell` tool uses `subprocess.run(shell=True)` and `write_file` allows arbitrary path traversal, creating critical command injection and arbitrary file write vulnerabilities from user-influenced input.
- **Required fix:** Implement robust input validation and sanitization for all tool arguments, avoid `shell=True` for command execution, and restrict file operations to a safe, sandboxed directory.
- **Evidence:** `Security section: `run_shell` executes arbitrary shell commands via `subprocess.run(shell=True, ...)`... `write_file` can overwrite any writable path reachable by the process. Path traversal is not mitigated`

### UI — APPROVE (low)
- **Reason:** The plan for the CLI tool includes clear invocation, good feedback during execution, sensible error handling, and a well-structured README with warnings and examples, ensuring a good first-use experience.

### GUIDE — APPROVE (low)
- **Reason:** The plan includes a comprehensive README, clear CLI usage instructions, and a well-structured inline tool registry, ensuring high discoverability for both human users and AI agents.

### USEFULNESS — APPROVE (low)
- **Reason:** Provides a crucial minimal reference implementation for Anthropic tool use, aiding developer understanding and framework comparison.
- **Evidence:** `Addresses the common developer need for 'how does this work with just the SDK?' and serves as a baseline for framework evaluation, explicitly detailed in the comparison_plan.md and README.md.`

### COOL — APPROVE (low)
- **Reason:** The extreme minimalism and 'no framework' approach is a signature move, providing a clear, unencumbered reference implementation of the core agent loop.
- **Evidence:** `LangChain, LlamaIndex (as complex agent frameworks)`

### LESSONS — APPROVE (advisory)
- **Reason:** [AUTO-DOWNGRADED: LESSONS VETO missing precondition_evidence] The plan introduces intentional security risks for a prototype without documenting them in a CONSTRAINTS.md file, which is a recurring SECURITY escalation pattern.
- **Required fix:** Add a `experiments/adopt-bare-agent/CONSTRAINTS.md` file at the PLAN gate, documenting the intentional security risks of `run_shell(shell=True)` and `write_file` path traversal, and the 'local developer use only' trust boundary.
- **Evidence:** `TML tool, document the architectural decision once in `<project>/CONSTRAINTS.md` (matching the naval-scribe precedent). Per-feature reviews must cite specific new attack surfaces, not revisit the architectural choice. This ended a recurring SECURITY escalation pattern. (from learnings.md)

[INSIGHT]`

## Resolution

Human decision required. Resume the build after updating session_state.json.
