# Council Escalation — markdown-deck

**Gate:** implementation
**Reason:** Unresolved objections after 2 attempts
**Timestamp:** 2026-04-25T00:34:54.292351+00:00

## Angle positions

### BUGS — APPROVE (low)
- **Reason:** The chart implementation is robust, handles various edge cases and malformed input gracefully with visible warnings, and correctly applies theme-aware styling.

### SECURITY — OBJECT (high)
- **Reason:** User-controlled input in math blocks and table cells is not escaped before being inserted into the DOM, allowing for cross-site scripting (XSS).
- **Required fix:** Apply HTML escaping (e.g., `esc()`) to the content of `\text{}` and `\mathbf{}` in the `renderMath` function, and to table cell content (`c`) before insertion into `<th>` or `<td>` tags.
- **Evidence:** `renderMath: `s = s.replace(/__TEXT__\{([^}]*)\}/g, '$1');`, `s = s.replace(/__BOLD__\{([^}]*)\}/g, '<b>$1</b>');`
md (table parsing): `return '<' + tag + ' style="' + style + '">' + c + '</' + tag + '>';``

### UI — APPROVE (low)
- **Reason:** The chart implementation provides clear visual feedback, handles edge cases gracefully with warnings, and integrates well with the existing theme system and accessibility features.

### GUIDE — OBJECT (medium)
- **Reason:** The critical instructions for AI agents do not explicitly mention the syntax and rules for chart blocks, which could lead to common generation failures.
- **Required fix:** Add a point to the 'CRITICAL: Rules for AI-Generated Slides' section detailing how AI should generate `chart` blocks, similar to the existing instruction for `diagram` blocks.
- **Evidence:** `script type="text/plain" id="ai-prompt-content" (specifically the 'CRITICAL: Rules for AI-Generated Slides' section)`

### USEFULNESS — APPROVE (low)
- **Reason:** Inline chart blocks provide a highly useful, friction-reducing way to visualize data directly within the markdown presentation workflow, addressing a common need for quick, theme-aware data visualization without external tools.
- **Evidence:** `This feature solves the problem of needing to generate charts externally (e.g., in Excel, dedicated charting tools) and then embed them as static images, which is cumbersome for iterative changes and theme consistency. The ability to define charts with CSV-like data directly in markdown, with theme `

### COOL — APPROVE (low)
- **Reason:** The inline, zero-dependency, theme-aware SVG charts are a signature move that differentiates this tool from generic markdown editors and presentation tools, offering a delightful 'oh, nice' moment when themes are switched.

### LESSONS — APPROVE (low)
- **Reason:** No documented lessons or prior anti-patterns were violated. Escalation fixes are correctly implemented.

## Resolution

**RESOLVED 2026-05-28 by John (interactive session, via Claude).**

### SECURITY OBJECT — ACCEPTED (fix applied)
Legitimate XSS. `renderMath()` inserted captured `\text{}`/`\mathbf{}` (and `^{}`/`_{}`) content into innerHTML unescaped, and the table parser inserted cell content unescaped — both reachable sinks (math content reaches `<div class="math-block">`/`<span class="math-inline">`, table cells reach `<td>`/`<th>`). Fixed by:
- Escaping math input at the top of `renderMath`: `var s = esc(tex.trim());`. `esc()` only touches `& < > "`, none of which are math syntax (`\ { } ^ _`), so every transformation still works while `\text{}`, `\mathbf{}`, `^{}`, `_{}` can no longer inject markup. (Also hardens sup/sub, which had the identical hole.)
- Wrapping table cell content in `esc(c)` in the table-row builder.

Note: escaping table cells renders any raw HTML / inline links inside a cell as literal text (the secure behavior for tabular data); inline code in cells is unaffected (placeholder-protected).

### GUIDE OBJECT — ALREADY SATISFIED (no action)
Chart-block rules were added to the `ai-prompt-content` CRITICAL section in commit d28e0c1 (rule 10 "Charts use ```chart bar / line / pie", a chart example, and the "## Chart Blocks" section). The objection no longer applies.

All other angles approved. Build may resume.
