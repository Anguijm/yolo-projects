# Council Escalation — experiments/infra-yolo-evals

**Gate:** implementation
**Reason:** Unresolved objections after 2 attempts
**Timestamp:** 2026-04-21T13:05:55.279266+00:00

## Angle positions

### BUGS — OBJECT (high)
- **Reason:** The 'table-overflow' check in mobile_usability.py incorrectly flags valid responsive table implementations where 'overflow-x:auto' is applied to a parent wrapper element instead of directly to the <table>, leading to false positive warnings.
- **Required fix:** The 'table-overflow' check must be refined to detect if 'overflow-x:auto' is applied to the <table> element itself or to a direct parent/ancestor wrapper, rather than merely checking for its global presence or absence.
- **Evidence:** `mobile_usability.py check 4: "flags <table> without overflow-x:auto anywhere in the file"`

### SECURITY — OBJECT (high)
- **Reason:** The scripts accept an arbitrary file path via sys.argv[1] which, despite canonicalization with os.path.abspath, allows reading any file on the system accessible to the script's user if an attacker can control the input argument, leading to arbitrary file disclosure.
- **Required fix:** Implement strict path validation to ensure the input path is a child of an explicitly allowed, sandboxed directory (e.g., the project root or a temporary build directory), or use a more robust sandboxing mechanism to prevent reading arbitrary files.
- **Evidence:** `path = os.path.abspath(sys.argv[1])
    # ...
def read_html(path):
    try:
        text = open(path, encoding="utf-8", errors="replace").read()`

### UI — APPROVE (low)
- **Reason:** All proposed evaluation lenses encourage best practices for user experience, including accessibility, responsiveness, feedback, and clear interaction patterns.

### GUIDE — APPROVE (low)
- **Reason:** All discoverability concerns from previous attempt have been addressed; comprehensive in-app help and documentation are provided.

### USEFULNESS — APPROVE (low)
- **Reason:** These advisory lenses provide practical, recurring utility for developers building YOLO projects, catching common oversights and prompting valuable polish.
- **Evidence:** `The portfolio hit rates demonstrate real-world catches like 'focus-ring' on all projects, 'table-overflow' regression, and correct 'cult_status' grading for markdown-deck. This indicates the heuristics are effective for the target single-file HTML projects. The tools address common development blind`

### COOL — APPROVE (low)
- **Reason:** Internal pipeline tools are explicitly exempt from the signature-move requirement per PLAN gate approval and the broadened goalpost rule.

### LESSONS — APPROVE (low)
- **Reason:** 

## Resolution

Human decision required. Resume the build after updating session_state.json.
