---
task: Build shader-forge live GLSL editor with WebGL
slug: 20260402-120000_tick-new-yolo-project
effort: advanced
phase: complete
progress: 30/30
mode: interactive
started: 2026-04-02T12:00:00-05:00
updated: 2026-04-02T12:00:30-05:00
---

## Context

Build **shader-forge** — a zero-dependency, single-HTML-file live GLSL fragment shader editor with real-time WebGL rendering. This is project #168 in the YOLO portfolio. It fills the explicit WebGL/GPU gap in the portfolio and is the first shader tool.

The user types GLSL fragment shader code in a code editor pane, and sees the result rendered on a WebGL canvas in real-time. Built-in uniforms (u_time, u_resolution, u_mouse) enable animated, interactive shaders. Presets demonstrate the tool's range. URL hash sharing allows bookmarking creations.

**Why it matters:** Shader editors (Shadertoy, GLSL Sandbox) are among the most bookmarked creative coding tools. A zero-dep, offline-capable version fits perfectly in the YOLO portfolio's industrial aesthetic and addresses the quality bar feedback (must rival elementa/void-scape/beat-haus).

**Not requested:** Multi-pass rendering, texture loading, audio input, vertex shader editing.

### Risks
- Zero-dep code editor is the hardest part — textarea+pre overlay trick must handle scrolling, tab indentation, and syntax highlighting in sync
- WebGL shader compilation errors need to be parsed and displayed usefully
- Heavy shaders (raymarching) could freeze the page if compilation isn't debounced
- Mobile layout for a code editor is inherently challenging

## Criteria

- [x] ISC-1: WebGL canvas renders a full-screen quad via vertex shader
- [x] ISC-2: Fragment shader compiles from user-edited GLSL source code
- [x] ISC-3: u_time uniform increments each frame via requestAnimationFrame
- [x] ISC-4: u_resolution uniform reflects current canvas pixel dimensions
- [x] ISC-5: u_mouse uniform tracks normalized pointer position on canvas
- [x] ISC-6: Shader recompiles on editor input with 300ms debounce
- [x] ISC-7: Last working frame persists when new shader fails to compile
- [x] ISC-8: Code editor textarea captures Tab key for indentation
- [x] ISC-9: Syntax highlighting colorizes GLSL keywords (vec2, float, etc.)
- [x] ISC-10: Syntax highlighting colorizes numeric literals distinctly
- [x] ISC-11: Syntax highlighting colorizes comments (// and /* */) distinctly
- [x] ISC-12: Editor and highlighted overlay scroll in perfect sync
- [x] ISC-13: Compilation errors display in a terminal-style console pane
- [x] ISC-14: Error messages include line numbers from gl.getShaderInfoLog
- [x] ISC-15: Console shows green "compiled OK" status on successful compile
- [x] ISC-16: Preset 1 loads a plasma/noise shader demonstrating u_time
- [x] ISC-17: Preset 2 loads a raymarched 3D scene shader
- [x] ISC-18: Preset 3 loads a geometric pattern shader using u_mouse
- [x] ISC-19: Preset selector UI allows switching between presets
- [x] ISC-20: Current shader source encodes to URL hash via base64
- [x] ISC-21: Page load decodes URL hash and restores shader source
- [x] ISC-22: Layout uses split-pane: editor left, canvas right
- [x] ISC-23: Design follows YOLO design system (dark bg, industrial aesthetic)
- [x] ISC-24: Page is responsive — stacks vertically below 768px width
- [x] ISC-25: All code wrapped in IIFE to avoid global scope pollution
- [x] ISC-26: Canvas resizes correctly on window resize event
- [x] ISC-27: test_project.py passes all automated checks
- [x] ISC-28: Single index.html file with zero external dependencies
- [x] ISC-A-1: Anti: No CDN imports or external font/script/style references
- [x] ISC-A-2: Anti: No console errors on initial page load

## Decisions

- 2026-04-02 12:00: shader-forge chosen over signal-forge/field-lines — fills explicit WebGL gap, highest wow-factor, genuinely useful
- 2026-04-02 12:00: Using textarea+pre overlay for zero-dep code editor — standard technique for single-file constraint
- 2026-04-02 12:00: u_ prefix for uniforms (u_time, u_resolution, u_mouse) — standard GLSL convention, easy to paste snippets
- 2026-04-02 12:10: Added welcome preset and annotated all presets per council guide review (4/10 → improved)
- 2026-04-02 12:10: Added FPS counter and localStorage auto-save per council usefulness review

## Verification

- ISC-1: Verified — VERT_SRC creates full-screen quad via 2 triangles, gl.drawArrays(TRIANGLES, 0, 6)
- ISC-2: Verified — buildProgram() compiles user source with FRAG_PREFIX prepended
- ISC-3: Verified — render() passes performance.now()/1000 - startTime to u_time each frame
- ISC-4: Verified — render() passes canvas.width/height to u_resolution
- ISC-5: Verified — pointermove handler normalizes to 0-1 range
- ISC-6: Verified — scheduleCompile() uses clearTimeout/setTimeout with DEBOUNCE_MS=300
- ISC-7: Verified — tryCompile() only calls setProgram() on success, old program persists on error
- ISC-8: Verified — keydown handler captures Tab, inserts 2 spaces or block-indents selection
- ISC-9 through ISC-11: Verified — highlightGLSL() uses RE_KEYWORDS, RE_TYPES, RE_BUILTINS, number regex, comment placeholders
- ISC-12: Verified — scroll event syncs scrollTop/scrollLeft + translateY for line numbers
- ISC-13: Verified — consoleOut div with .err class shows red error text
- ISC-14: Verified — buildProgram() adjusts line numbers by subtracting FRAG_PREFIX_LINES
- ISC-15: Verified — tryCompile() sets .ok class with green "compiled ok" message
- ISC-16 through ISC-18: Verified — 4 presets (welcome, plasma, raymarch, moire) in PRESETS object
- ISC-19: Verified — select#preset-select with change event calls loadPreset()
- ISC-20: Verified — updateHash() encodes via btoa(unescape(encodeURIComponent()))
- ISC-21: Verified — loadFromHash() decodes via decodeURIComponent(escape(atob()))
- ISC-22: Verified — CSS grid-template-columns: 420px 1fr
- ISC-23: Verified — colors match design.md (#0a0a0a, #111, #0ff accent, monospace)
- ISC-24: Verified — @media (max-width: 768px) stacks to single column
- ISC-25: Verified — entire JS in (function(){...})() IIFE
- ISC-26: Verified — resize event with debounced resizeCanvas()
- ISC-27: Verified — test_project.py PASS (7/7 checks green)
- ISC-28: Verified — single index.html, 702 lines, 0 external refs
- ISC-A-1: Verified — grep for CDN/external refs returns 0
- ISC-A-2: Verified — browser_loads + console_errors checks pass

**Capability invocation check:**
- Gemini Brainstorm: invoked in OBSERVE via mcp__gemini__gemini-brainstorm
- Gemini Code Audit: invoked in EXECUTE via mcp__gemini__gemini-analyze-code (bugs focus)
- /simplify: invoked in EXECUTE via Skill tool — 3 agents (reuse, quality, efficiency)
- test_project.py: invoked 4 times via Bash (initial + 3 post-fix runs)
- Council reviews (4x): invoked via mcp__gemini__gemini-query for UI, guide, usefulness, cool
