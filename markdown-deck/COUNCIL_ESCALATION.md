# Council Escalation — markdown-deck

**Gate:** plan
**Reason:** LESSONS VETO — The plan for `renderSnapshotsList` violates a documented KEEP lesson by using `innerHTML` for a full re-render of a list (up to 20 items) instead of `document.createDocumentFragment()` for batch rendering.
**Timestamp:** 2026-04-12T08:00:26.011170+00:00

## Angle positions

### BUGS — APPROVE (low)
- **Reason:** The plan demonstrates robust error handling for localStorage (quota, corruption) and ensures state consistency between in-memory and persisted data, with no new critical correctness risks identified.

### SECURITY — OBJECT (high)
- **Reason:** The plan describes rendering user-controlled markdown content (via the `md()` function) directly into `innerHTML` for snapshot previews without explicit mention of robust HTML sanitization, which, combined with an `unsafe-inline` CSP, creates a Cross-Site Scripting (XSS) vulnerability.
- **Required fix:** Implement robust HTML sanitization (e.g., using DOMPurify) on the output of the `md()` function before it is assigned to `innerHTML` for any user-controlled content, including snapshot thumbnails and main slide rendering.
- **Evidence:** `Thumbnail: extract text before first \n---\n from snapshot.content, pass through `md()`, inject as innerHTML of `.sn-thumb`. This is the identical pattern to the existing thumb strip (which also sets `innerHTML = md(slideText)`).
CSP: `unsafe-inline` is the existing architectural baseline.`

### UI — OBJECT (high)
- **Reason:** Placing a 'Take Snapshot' button inside the modal for viewing/managing snapshots creates a confusing flow, as the button affects the main editor content rather than the modal's context.
- **Required fix:** Remove the 'Take Snapshot' button from the modal header. The primary method (Ctrl+Shift+S) and the toolbar button to open the modal are sufficient for saving.
- **Evidence:** `UI section: 'Header: ... + "Take Snapshot" button + close ×.' and Scope: 'takeSnapshot() triggered by Ctrl+Shift+S (and modal button)'`

### GUIDE — OBJECT (medium)
- **Reason:** The inline editable snapshot label lacks a clear visual cue for discoverability, requiring users to guess or be told they can click to edit.
- **Required fix:** Add a visual hint (e.g., a subtle pencil icon on hover, or a tooltip on the label itself) to indicate the snapshot label is editable.
- **Evidence:** `Scope: 'Inline editable label per snapshot (click label text → contenteditable)'; Guide: 'Edit label: click label to edit inline, blur to save'`

### USEFULNESS — APPROVE (low)
- **Reason:** This feature provides a critical safety net and enables confident experimentation, solving a common problem of accidental data loss or regret during content creation.
- **Evidence:** `Similar version history/snapshot features are standard in most serious content creation tools (e.g., Google Docs, Figma, IDEs) because users frequently need to revert changes or track milestones. This directly enhances the utility of markdown-deck as a reliable tool.`

### COOL — APPROVE (low)
- **Reason:** The visual thumbnail preview of the first slide for each snapshot, combined with quick Ctrl+Shift+S saving and inline editable labels, provides a signature 'oh, nice' moment for a markdown presentation tool, differentiating it from generic text-based version histories.

### LESSONS — OBJECT (critical) 🚫 VETO
- **Reason:** The plan for `renderSnapshotsList` violates a documented KEEP lesson by using `innerHTML` for a full re-render of a list (up to 20 items) instead of `document.createDocumentFragment()` for batch rendering.
- **Required fix:** Modify `renderSnapshotsList()` to use `document.createDocumentFragment()` to build the list items, and then append the fragment to `#sn-list` to avoid unnecessary DOM reflows during full re-renders.
- **Evidence:** `KEEP: `document.createDocumentFragment()` for addr-list batch render — even though typical address book is 0-50 entries (below the >50 threshold), the pattern was used because the full re-render on every add/delete rebuilds the entire list. (from learnings.md under [naval-scribe: Command Address Boo`

## Resolution

Human decision required. Resume the build after updating session_state.json.
