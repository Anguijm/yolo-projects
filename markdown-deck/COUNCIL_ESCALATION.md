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

Human decision required. Resume the build after updating session_state.json.
