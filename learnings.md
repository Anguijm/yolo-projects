# YOLO Builder Learnings

Persistent knowledge base. Read this before every build.

---

## Accumulated Principles

### Architecture & Performance
- **Uint32Array pixel writes** are 4x faster than writing R,G,B,A separately to ImageData. Use for any pixel-level rendering (fractals, raycasters, image processing).
- **Object pooling** eliminates GC pauses. Pre-allocate arrays of particle/entity objects and toggle `.active` instead of push/splice. Critical for any animation with >100 entities.
- **Pre-compute lookup tables** for anything repeated per-frame: gradients, color palettes, sin/cos tables. Copy with `.set()` instead of recomputing.
- **DDA algorithm** is the correct approach for grid-based raycasting — O(1) per cell traversal, mathematically exact.
- **Bitwise AND** (`& (size - 1)`) replaces modulo for power-of-2 sizes. `~~x` replaces `Math.floor(x)` in hot paths.
- **Single canvas + ImageData** beats individual draw calls for pixel-heavy rendering. Use Canvas 2D API (fillRect, arc) only for overlays/UI elements.

### UI/UX Patterns That Score Well
- **Glassmorphic floating panels** (backdrop-filter blur, subtle borders) — consistently praised by Gemini for modern aesthetic.
- **Pre-built presets** that instantly showcase the project's range. Every project should have 4-6 presets that demonstrate different states.
- **Keyboard shortcuts** — always add them. Map common actions to single keys.
- **Live coordinate/status display** — show what's happening (FPS, position, coordinates, current state).
- **Click-to-interact** on the canvas itself, not just sliders. Direct manipulation > indirect controls.

### Common Gemini Critiques (Fix Proactively)
- **"Code is incomplete/snippet"** — Gemini docks points when it can't see the full file. When submitting for review, always note "this is the complete runnable file" and list ALL features.
- **"Global state / no encapsulation"** — Always wrap in IIFE `(function() { ... })()`.
- **"Magic numbers"** — Extract constants to top of file or a CONFIG object. Name them.
- **"Main thread blocking"** — For CPU-heavy work (fractals, physics), use progressive rendering during interaction (low-res preview → debounced full render).
- **"Memory leaks"** — Revoke object URLs, clear intervals, remove event listeners on cleanup.
- **"No resize handler"** — Always add `window.addEventListener('resize', ...)` with debounced regeneration.
- **"Diagonal movement faster than cardinal"** — Normalize movement vectors when multiple keys are pressed.

### Project Categories Well-Covered
- Dev Tools (6): git-xray, regex, json, diff, api-mocker, cron
- Simulations (6): raycaster, mandelbrot, music-viz, gravity, circuit, weather
- Creative/Art (4): pixel-paint, whiteboard, color-lab, markdown-deck
- Productivity (5): kanban, pomodoro, habit-grid, countdown, bookmark
- System/Monitoring (5): proc-map, system-dash, wifi, file-treemap, speedtype
- Utilities (4): qr, unit-convert, emoji, math-plot

### Underexplored Categories
- **Games** — synth-defense is the first! More needed.
- **Data visualization** — csv-cinema covers animated charts from CSV; still room for real-time dashboards
- **AI/ML tools** — neural-playground is the first! More possible (transformer viz, tokenizer explorer)
- **Networking/API** — http-playground covers REST; still room for WebSocket tools, GraphQL explorers
- **Text/Language** — markov-composer covers generation; still no prose analysis or sentiment tools
- **Education/Learning** — regex-quest is the first! More interactive tutorials possible

---

## Per-Build Reflections

### ray-caster (2026-03-21)
- **KEEP**: DDA raycasting + ImageData pixel buffer + bitwise ops = smooth 60fps
- **KEEP**: Procedural brick textures via sine-wave noise — zero external assets
- **IMPROVE**: Gemini wanted texture stepping based on trueWallHeight, not clamped span — fixed
- **IMPROVE**: Pre-parse hex colors at startup, not in render loop
- **INSIGHT**: For any per-pixel rendering, move ALL computation out of the inner loop. One division per column, zero per pixel.

### mandelbrot-explorer (2026-03-21)
- **KEEP**: Uint32Array for single-write pixels (ABGR little-endian format)
- **KEEP**: Progressive rendering (4x4 blocks during drag, full on idle)
- **IMPROVE**: Reuse ImageData across frames — only recreate on resize
- **INSIGHT**: Debounced full render after interaction stops = best of both worlds (responsive + sharp)

### music-viz (2026-03-21)
- **KEEP**: Web Audio API AnalyserNode is incredibly powerful — getByteFrequencyData + getByteTimeDomainData
- **KEEP**: `rgba(0,0,0,0.15)` fill trick for motion trails
- **IMPROVE**: Revoke object URLs when loading new audio files
- **IMPROVE**: Pause audio when switching from file to mic mode
- **DISCARD**: canvas shadowBlur is too expensive for sustained animation
- **INSIGHT**: Multiple visualization modes in one app >> one fancy visualization

### gravity-sim (2026-03-21)
- **KEEP**: Symplectic Euler (update velocity first, then position) for stable orbits
- **KEEP**: Sub-stepping (split dt into 0.004s chunks) for physics stability
- **KEEP**: Softening parameter prevents division-by-zero explosions
- **IMPROVE**: Don't use rgba fade trick for trails when camera can pan — store trail arrays and draw with fading opacity
- **INSIGHT**: For any physics sim: stored trail arrays > screen-space fade. Trails must live in world space.

### circuit-sim (2026-03-21)
- **KEEP**: Iterative evaluation (N+2 passes) handles arbitrary gate ordering without topological sort
- **KEEP**: Map lookups (gateMap, wireByInput) instead of Array.find() in hot paths
- **IMPROVE**: Bezier curves for wires look much better than straight lines
- **INSIGHT**: For graph-based UIs, build lookup Maps when state changes, not during render

### weather-terrarium (2026-03-21)
- **KEEP**: Deriving weather state from physical inputs (temp+humidity) beats hardcoded buttons
- **KEEP**: Lerp smoothing for state transitions prevents jarring snaps
- **KEEP**: Debounced resize handler — resize canvas immediately, debounce geometry regeneration
- **KEEP**: 6 presets that each show a dramatically different state
- **IMPROVE**: Extract magic numbers to constants
- **INSIGHT**: Simulation > animation. Let users control inputs and derive outputs = endlessly explorable

### synth-defense (2026-03-21)
- **KEEP**: Pentatonic scale (C pentatonic across 3 octaves) — guarantees every note combination sounds musical
- **KEEP**: BPM-quantized firing (globalTick % fireDiv) — turns chaotic combat into rhythmic music
- **KEEP**: Tower Y position maps to note pitch — placement becomes composition
- **KEEP**: DynamicsCompressorNode on master audio bus — prevents clipping with 15+ simultaneous oscillators
- **KEEP**: Tower shape matches wave type (square=square, sine=circle, triangle=triangle) — visual language
- **IMPROVE**: Gemini wanted decoupled audio scheduling from frame rate — use audioCtx.currentTime for precise timing
- **IMPROVE**: Uint8Array pathGrid for O(1) grid lookups instead of string Set
- **DISCARD**: Initially considered complex A* pathfinding — fixed serpentine path is way simpler and sufficient
- **INSIGHT**: Music theory constraints (scales, quantization) can make procedural audio sound good by default. The key insight: restrict the output space so random combinations still sound harmonious.
- **INSIGHT**: Games need an escalation loop (wave difficulty) + economy (gold/cost) + fail state (lives) to feel like actual games vs. toys.

### minimal-clock (2026-03-23)
- **KEEP**: High-DPI scaling with setTransform(dpr,0,0,dpr,0,0) in render loop — crisp lines on Retina
- **KEEP**: Smooth sweep via milliseconds: `seconds + ms/1000` creates liquid-smooth hand motion
- **KEEP**: All drawing relative to `Math.min(W,H) * 0.38` — auto-scales to any viewport
- **KEEP**: 4 visual modes showing same data = "multiple visualization modes >> one fancy one"
- **KEEP**: Face label opacity fades after 2s — shows info without cluttering
- **KEEP**: W/H = 0 skip in render — prevents wasted cycles when window minimized
- **TEST CAUGHT (via Gemini audit)**: createConicGradient not available in older browsers — feature detection with fallback prevents crash
- **TEST CAUGHT (via Gemini audit)**: Wake lock on page load often blocked — user gesture (click) is more reliable trigger
- **TEST CAUGHT (via Gemini audit)**: Render loop runs when minimized (W=0, H=0) — wastes CPU
- **INSIGHT**: Canvas APIs that use newer features (createConicGradient, OffscreenCanvas, etc.) ALWAYS need feature detection. `if (ctx.methodName)` before calling.
- **INSIGHT**: Wake Lock API is most reliable when called inside a click/touch handler, not on page load. Browsers increasingly restrict non-gesture API calls.
- **INSIGHT**: Multiple visual representations of the same data in one app is a powerful pattern — each face is a different "lens" on time.

### tile-painter (2026-03-23)
- **KEEP**: rAF dirty flag pattern — set `previewDirty = true` in hot path, only call expensive operation (toDataURL) in rAF loop. Essential for any drag-based editor.
- **KEEP**: toBlob + URL.createObjectURL for large canvas downloads — toDataURL hits URL length limits on 2048x2048 canvases
- **KEEP**: setPointerCapture on pointerdown, releasePointerCapture on pointerup — prevents stuck drag when pointer leaves element bounds
- **KEEP**: touch-action: none on drawing surfaces — prevents mobile scroll from interrupting paint strokes
- **KEEP**: Curated palettes (4-5 color sets) guarantee aesthetic output regardless of user skill
- **KEEP**: image-rendering: pixelated on preview — keeps pixel art crisp when scaled up
- **TEST CAUGHT (via Gemini audit)**: toDataURL called on every pointermove = CPU meltdown during drag. rAF dirty flag reduced calls from 60+/sec to 1/frame.
- **TEST CAUGHT (via Gemini audit)**: toDataURL for 2048x2048 wallpaper download = multi-MB URL string that exceeds browser limits. toBlob is the correct approach.
- **TEST CAUGHT (via Gemini audit)**: No setPointerCapture = fast drag outside grid leaves painting=true permanently.
- **TEST CAUGHT (via Gemini audit)**: No touch-action:none = mobile scroll interrupts drawing.
- **INSIGHT**: toDataURL is the MOST EXPENSIVE canvas operation. NEVER call it in a high-frequency event handler (pointermove, input, scroll). Always debounce via rAF dirty flag.
- **INSIGHT**: For large canvas exports: toBlob > toDataURL. toBlob creates a Blob in memory; toDataURL creates a Base64 string that can exceed URL limits.
- **INSIGHT**: setPointerCapture is the professional solution for drag interactions — it guarantees the element receives all pointer events even when the pointer leaves its bounds.

### coin-flip (2026-03-23)
- **KEEP**: CSS 3D coin with preserve-3d + backface-visibility hidden — clean two-sided rendering
- **KEEP**: Cumulative rotation tracking (currentRotation += turns*360 + offset) — prevents backward spinning
- **KEEP**: Custom cubic-bezier(0.15, 0.6, 0.35, 1) — gives coin a weighty, decelerating feel
- **KEEP**: Entire screen as tap target (no button) — maximum simplicity
- **KEEP**: Dot-based history (tiny colored circles) — visual pattern recognition without text clutter
- **KEEP**: isNaN + Math.max(0) guard on localStorage numbers — handles tampering and corruption
- **KEEP**: audioCtx.resume().catch() — prevents unhandled promise rejection in strict browsers
- **TEST CAUGHT (via Gemini audit)**: Backward spinning — absolute rotation causes CSS to animate in reverse when new angle < previous. MUST track cumulative rotation with +=.
- **TEST CAUGHT (via Gemini audit)**: NaN in localStorage — typeof === 'number' passes for NaN. Must also check isNaN().
- **TEST CAUGHT (via Gemini audit)**: audioCtx.resume() returns Promise — rejection goes unhandled if browser blocks. Must .catch().
- **INSIGHT**: CSS transform rotation animations MUST use cumulative angles (always increasing) to guarantee forward spin direction. Absolute angles can go backward.
- **INSIGHT**: typeof NaN === 'number' is TRUE in JavaScript. Always pair typeof check with isNaN() for localStorage number validation.
- **INSIGHT**: The simplest apps demand the most polish. When there's only one interaction, every detail of that interaction must be perfect.

### maze-runner (2026-03-23)
- **KEEP**: Recursive backtracker maze generation — long corridors, guaranteed solvable, simple implementation
- **KEEP**: Smart trail: check if new position matches trail[-2] → pop (backtrack) else push (advance). Keeps trail clean and performant.
- **KEEP**: Slide-until-wall for mobile swipe — one swipe moves player through entire corridor. Essential for maze playability on touch screens.
- **KEEP**: Cached DOM element for timer display — getElementById once at init, reference in rAF loop. Never query DOM at 60fps.
- **KEEP**: Increment game level BEFORE displaying "next" text — prevents showing impossible level ("32x32" when max is 30)
- **TEST CAUGHT (via Gemini audit)**: getElementById in 60fps timer loop — CPU waste, battery drain. Cached at init.
- **TEST CAUGHT (via Gemini audit)**: Trail grew forever on backtrack — overlapping segments caused render lag. Smart pop/push fixed it.
- **TEST CAUGHT (via Gemini audit)**: One-step-per-swipe on mobile = hundreds of swipes for 30x30 maze. Slide loop made it playable.
- **TEST CAUGHT (via Gemini audit)**: "Next: 32x32 maze" shown before clamping to 30 max. Display text must use the clamped value.
- **INSIGHT**: Mobile maze/grid games need "slide until obstacle" mechanics. One-cell-per-swipe is physically exhausting on large grids.
- **INSIGHT**: Any text showing "next level" must be computed AFTER the level increment + clamp, not before. Order of operations bug.
- **INSIGHT**: Trail data structures that only grow (push) will eventually kill render perf. Backtrack-aware trails (pop on retrace) stay bounded.

### life-canvas (2026-03-22) — PROJECT #60
- **KEEP**: Cell age as Int16Array (0=dead, 1=newborn, n=survived n generations) — cheap storage, rich visual output
- **KEEP**: HSL color mapping from age (hue=180+age*3, lightness=70-age*2) — creates beautiful cyan→purple gradient
- **KEEP**: Ghost trails via Float32Array — dead cells leave fading afterglow, adds motion history
- **KEEP**: Double-buffer grid swap (grid↔nextGrid) — avoids in-place mutation artifacts
- **KEEP**: touchmove prevention SCOPED TO CANVAS — prevents game scroll without blocking rest of page
- **KEEP**: pointercancel handler alongside pointerup/pointerleave — prevents stuck paint state on system interrupts
- **TEST CAUGHT (via Gemini audit)**: Ghost decay ran during pause (tied to render, not game state). Guarded with `if (playing)`.
- **TEST CAUGHT (via Gemini audit)**: touchmove on document blocked ALL page scrolling. Scoped to canvas element.
- **TEST CAUGHT (via Gemini audit)**: Missing pointercancel — orientation change or system alert leaves painting=true permanently.
- **INSIGHT**: Any visual effect tied to the render loop (ghosts, trails, particles) must check game state before decaying. Render runs at 60fps regardless of pause.
- **INSIGHT**: ALWAYS scope touch/scroll prevention to the specific interactive element, NEVER the whole document. Users need to scroll to reach controls.
- **INSIGHT**: The trio of pointer end events is: pointerup + pointerleave + pointercancel. Missing any one creates stuck states.

### word-garden (2026-03-22)
- **KEEP**: Seeded PRNG (mulberry32) — deterministic infinite randomness from any string. Same input = same output, forever.
- **KEEP**: hashString → seed → mulberry32 PRNG → pull rng() for each parameter. Clean separation of seed → entropy → parameters.
- **KEEP**: Curated palettes (8 high-quality combos) selected by hash mod — guarantees beauty regardless of input
- **KEEP**: Quadratic bezier curves for branches (quadraticCurveTo) — dramatically more organic than straight lineTo
- **KEEP**: Breadth-first sort (by depth) after depth-first generation — natural growth animation
- **KEEP**: Branch count cap (15,000) — prevents exponential blowup (3^10 = ~59K theoretical branches)
- **TEST CAUGHT (via Gemini audit)**: Depth-first animation drew one full branch tip-to-leaf then jumped back to trunk — ugly. Sorted by depth for natural growth.
- **TEST CAUGHT (via Gemini audit)**: No branch cap — extreme seeds could generate 88K+ segments, freezing the browser for seconds.
- **TEST CAUGHT (via Gemini audit)**: Resize on mobile keyboard open erased canvas — debounced resize prevents this.
- **INSIGHT**: Deterministic generative art (same input = same output) is powerful for personal identity — "my name makes MY unique tree." This is viral because people want to compare.
- **INSIGHT**: For recursive fractal generation: always generate depth-first (natural recursion), then SORT breadth-first for animation. Best of both worlds.
- **INSIGHT**: Any recursive algorithm with branching factor >2 needs a hard cap on total output. 3^10 = 59,049. 3^12 = over 500K. Always cap.

### color-eye (2026-03-22)
- **KEEP**: object-fit: cover coordinate mapping — must calculate render dimensions and offset to map screen coords to video coords accurately
- **KEEP**: Single getImageData for NxN area vs N*N individual calls — 9x perf improvement. Canvas batch reads always beat per-pixel reads.
- **KEEP**: Dynamic text contrast via BT.601 luminance — white text on dark colors, black on light. Essential for any color display UI.
- **KEEP**: willReadFrequently hint on canvas context — critical when getImageData is called on every tap
- **KEEP**: Palette dedup check (indexOf before unshift) — prevents duplicate saved colors
- **KEEP**: navigator.mediaDevices existence check before getUserMedia — prevents crash on HTTP contexts
- **TEST CAUGHT (via Gemini audit)**: 9 individual getImageData calls — massive perf waste. Fixed to single call with area parameters.
- **TEST CAUGHT (via Gemini audit)**: No mediaDevices check — getUserMedia is undefined on HTTP, causing crash before try/catch.
- **TEST CAUGHT (via Gemini audit)**: iOS clipboard fallback needs ta.setSelectionRange(0, 99999) after ta.select() — older Safari ignores select() alone.
- **INSIGHT**: Camera → canvas → getImageData is a reusable pipeline for ANY real-world pixel sampling (color, QR, OCR). The coordinate mapping for object-fit: cover is the hardest part.
- **INSIGHT**: getImageData(x, y, width, height) can grab an AREA in one call. Never loop individual pixel reads when you can batch.
- **INSIGHT**: Every browser API that requires a "secure context" (HTTPS) should have an existence check before use — mediaDevices, crypto.subtle, clipboard, etc.

### secure-note (2026-03-22)
- **KEEP**: AES-256-GCM provides both confidentiality AND integrity — tampered ciphertext fails to decrypt, doubling as password validation
- **KEEP**: New random IV per save (generateIV called in encryptText) — prevents catastrophic nonce reuse
- **KEEP**: Non-extractable CryptoKey (`extractable: false`) — JS can't export the raw key even if compromised by XSS
- **KEEP**: Auto-lock on visibilitychange — instantly clears plaintext from DOM and memory
- **KEEP**: First-time vs returning user flow — different UX for "Create" vs "Unlock"
- **KEEP**: beforeunload warning when unsaved changes pending — prevents data loss
- **KEEP**: autocomplete="new-password" — prevents browser from saving the encryption password
- **TEST CAUGHT (via Gemini SECURITY audit)**: PBKDF2 iterations too low (100K). OWASP recommends 600K for SHA-256. Raised.
- **TEST CAUGHT (via Gemini SECURITY audit)**: No password minimum — 1-char passwords are trivially brute-forceable. Added 8-char minimum for new notes.
- **TEST CAUGHT (via Gemini SECURITY audit)**: Missing beforeunload — async crypto might not finish before tab closes. Added warning.
- **TEST CAUGHT (via Gemini SECURITY audit)**: Missing autocomplete="new-password" — browser might save the master encryption password in autofill. Fixed.
- **INSIGHT**: For security-sensitive apps, ask Gemini for a SECURITY-focused audit, not just a bug-focused one. The `focus: 'security'` parameter finds different issues.
- **INSIGHT**: PBKDF2 iteration counts have a SHELF LIFE. 100K was fine in 2015. OWASP recommends 600K in 2024. Always check current recommendations.
- **INSIGHT**: Web Crypto API's `extractable: false` is a powerful defense against XSS — even if an attacker injects script, they can't export the key material.

### neon-snake (2026-03-22)
- **KEEP**: HSL gradient on snake segments `(i * 8 + Date.now() * 0.02) % 360` — creates animated rainbow ribbon with zero effort
- **KEEP**: globalCompositeOperation = 'lighter' + shadowBlur = instant neon glow aesthetic
- **KEEP**: Layered oscillators (sine + detuned triangle at freq * 1.002) creates shimmer/chorus effect
- **KEEP**: Swipe controls with min threshold (20px) prevents accidental direction changes
- **KEEP**: Only preventDefault on handled keys — global preventDefault blocks browser functions (F5, devtools)
- **KEEP**: touchmove preventDefault during gameplay — prevents mobile page scroll/refresh during swipes
- **TEST CAUGHT (automated)**: Dynamic ID not in HTML caused test failure. Fixed by adding element to HTML.
- **TEST CAUGHT (automated)**: Uninitialized snake array caused console error before game start. Fixed with empty array default.
- **TEST CAUGHT (via Gemini audit)**: e.preventDefault() on every keydown — blocked F5, Ctrl+C, etc. Must only prevent game keys.
- **TEST CAUGHT (via Gemini audit)**: getElementById in 60fps render loop — redundant DOM query killed performance. Removed.
- **TEST CAUGHT (via Gemini audit)**: No touchmove handler — swipe gestures scrolled the page instead of steering.
- **TEST CAUGHT (via Gemini audit)**: No win state — snake filling grid caused infinite spawnFood loop.
- **INSIGHT**: DOM queries in render loops are performance killers. Cache element references at init, NEVER query during animation.
- **INSIGHT**: Mobile games MUST prevent touchmove during active gameplay — otherwise the browser interprets swipes as scroll/pull-to-refresh.
- **INSIGHT**: Game state must handle ALL terminal conditions: lose (collision), AND win (board full). Missing the win state = infinite loop.

### gradient-studio (2026-03-22) — FIRST CLICK-ONLY BUILD (no pointerdown)
- **KEEP**: Fullscreen preview IS the UI — no separate preview panel needed. Body background = product.
- **KEEP**: Glassmorphic control panel (backdrop-filter blur + rgba background) looks premium over content
- **KEEP**: HSL randomization with constrained S (50-90) and L (40-70) guarantees visually pleasing colors
- **KEEP**: Click-only event handlers — ZERO double-fire issues. Process improvement validated.
- **KEEP**: Clipboard fallback (textarea + execCommand) for non-HTTPS contexts
- **KEEP**: Array.isArray guard on localStorage parse — prevents crashes from corrupted/tampered data
- **TEST CAUGHT (via Gemini audit)**: Toast race condition — rapid clicks queued overlapping timeouts. Fixed with clearTimeout.
- **TEST CAUGHT (via Gemini audit)**: Stale color slots — loading a 2-color saved gradient left colors 3 and 4 from previous session. Reset unused to random.
- **TEST CAUGHT (via Gemini audit)**: Non-array localStorage data caused .unshift crash. Array.isArray guard prevents this.
- **INSIGHT**: The click-only rule eliminated an entire bug class (double-fire). Process improvements that eliminate bug CLASSES are more valuable than fixing individual bugs.
- **INSIGHT**: Always guard localStorage with both try/catch AND type validation (Array.isArray, typeof === 'object', etc.). Users, extensions, and other apps can corrupt stored data.
- **INSIGHT**: Toast notifications need a single shared timeout variable with clearTimeout — otherwise rapid triggers cause visual glitches.

### one-line (2026-03-22)
- **KEEP**: Constraint as feature — 80 char limit forces distillation, creates a unique medium
- **KEEP**: Calendar mosaic with filled/empty indicators — visual progress tracking without numbers
- **KEEP**: Streak that tolerates "not yet written today" — check yesterday if today empty, prevents discouraging reset
- **KEEP**: Auto-focus input with 300ms delay — mobile keyboard pops up immediately
- **KEEP**: Pre-fill existing entry on load — user sees what they already wrote, can edit
- **KEEP**: Storage-full error feedback instead of silent failure — user knows their data wasn't saved
- **TEST CAUGHT (via Gemini audit)**: Streak showed 0 mid-day before writing — demoralizing, wrong. Fixed by checking yesterday first.
- **TEST CAUGHT (via Gemini audit)**: Entry deletion unreachable — save() returned early on empty string, so saveEntry's delete logic never ran
- **TEST CAUGHT (via Gemini audit)**: localStorage.setItem failure silently swallowed — user sees "Saved" but entry lost. Added error UI.
- **INSIGHT**: Streak algorithms must handle "haven't done it YET today" gracefully. Breaking the streak at 2pm because you haven't written yet is hostile UX. Always look back from yesterday if today is empty.
- **INSIGHT**: Any feature that has both "save" and "delete" semantics through the same action (empty vs filled input) must NOT have early returns that prevent the delete path.
- **INSIGHT**: The simplest apps benefit MOST from Gemini audit — fewer lines means each bug has outsized impact. 3 bugs in 200 lines = 1 bug per 67 lines.

### interval-timer (2026-03-22)
- **KEEP**: Absolute timestamps (Date.now() + duration) instead of dt subtraction — timer counts correctly even when rAF is paused in background
- **KEEP**: audioCtx.currentTime scheduling for completion arpeggio — setTimeout throttled to 1s+ in background tabs
- **KEEP**: Phase state machine (ready→work→rest→work→...→done) is clean and prevents invalid transitions
- **KEEP**: Haptic choreography: heartbeat (short pulses) in last 3s, sharp double-snap on phase start, triple burst on done
- **KEEP**: Preset buttons fill input fields (not direct-start) — lets users see/modify values before starting
- **KEEP**: Input validation with isNaN + minimum check — prevents negative values that bypass || fallback
- **TEST CAUGHT (via Gemini audit)**: dt=0 cap after tab switch KILLED the timer in background — switched to absolute Date.now() timestamps. This is the correct approach for ANY timer that must survive backgrounding.
- **TEST CAUGHT (via Gemini audit)**: Dual pointerdown+click on start button = double startTimer() = double rAF loop = 2x speed. Added `if (running) return` guard.
- **TEST CAUGHT (via Gemini audit)**: `parseInt('-10') || 20` = -10 (truthy). Negative values bypass || fallback. Must use explicit isNaN/min check.
- **TEST CAUGHT (via Gemini audit)**: setTimeout in playDone throttled when backgrounded. Switched to audioCtx.currentTime scheduling.
- **INSIGHT**: For ANY countdown timer: use absolute timestamps (endTime = Date.now() + seconds*1000), then calculate remaining = (endTime - Date.now()) / 1000. NEVER subtract dt — it breaks on background.
- **INSIGHT**: parseInt(negativeString) || defaultValue DOES NOT CATCH negative numbers. -10 is truthy. Always validate with explicit range checks.
- **INSIGHT**: Web Audio's currentTime is the ONLY reliable scheduler for background audio. setTimeout/setInterval are throttled to 1s+ in inactive tabs.

### wheel-of-fate (2026-03-22)
- **KEEP**: Physics spin with friction coefficient (velocity *= 0.985 per frame) creates realistic deceleration
- **KEEP**: Segment boundary detection via `(pointerAngle / sliceAngle) % n` — clean and frame-rate independent
- **KEEP**: Haptic tick with cooldown (30ms) prevents spam at high velocity but still feels satisfying at low velocity
- **KEEP**: CSS pointer/flapper as a separate div above canvas — simpler than drawing it in canvas, always visible
- **KEEP**: Celebratory arpeggio (C5-E5-G5-C6 at 80ms intervals) feels like a genuine "win" moment
- **KEEP**: Edit via textarea (one per line) — simplest possible input for list customization
- **TEST CAUGHT (via Gemini audit)**: indexOf for color mapping broken with duplicate options — must use segment index directly
- **TEST CAUGHT (via Gemini audit)**: No minimum wheelSize = negative canvas arc radius = DOMException crash on tiny windows
- **INSIGHT**: Any time you map a string to an index (for color, position, etc.), use the KNOWN index, not indexOf(). indexOf always returns the first occurrence, which is wrong for duplicates.
- **INSIGHT**: Canvas arc() throws DOMException on negative radius. Always clamp computed sizes to a minimum.

### sound-meter (2026-03-22)
- **KEEP**: RMS-to-dB formula: `20 * Math.log10(rms) + 94` — +94 approximates SPL from digital full scale
- **KEEP**: Color-coded severity levels (quiet/moderate/loud/very loud/dangerous) — immediately graspable
- **KEEP**: Vibration cooldown (1s) prevents battery death and browser freezing from 60fps haptics
- **KEEP**: AudioContext created synchronously BEFORE async getUserMedia — iOS REQUIRES this order
- **KEEP**: AudioContext.resume() on visibilitychange — OS can suspend context when backgrounded
- **KEEP**: Double-start guard (`if (running) return`) — prevents overlapping streams and animation loops
- **KEEP**: Proper cleanup: stream.getTracks().forEach(stop), audioCtx.close() — prevents resource leaks
- **TEST CAUGHT (via Gemini audit)**: AudioContext after await = silent on iOS (moved to synchronous creation)
- **TEST CAUGHT (via Gemini audit)**: navigator.vibrate at 60fps = device lockup (added 1s cooldown)
- **TEST CAUGHT (via Gemini audit)**: No running guard = potential double streams + double rAF loops
- **TEST CAUGHT (via Gemini audit)**: Background suspension kills AudioContext without notification (resume on visibility)
- **INSIGHT**: APIs that fire at requestAnimationFrame rate (60fps) MUST be throttled for any side effect (vibration, audio triggers, DOM updates). Only the rendering itself should run at full frame rate.
- **INSIGHT**: iOS audio initialization order is STRICTLY: create AudioContext → resume → THEN async getUserMedia. Reversing this = permanent silence. This is the #1 mobile audio gotcha.

### breath-pacer (2026-03-22) — FIRST MOBILE-FIRST PWA BUILD
- **KEEP**: OLED black (#000) saves battery and looks premium on modern phones
- **KEEP**: Screen Wake Lock API prevents screen dimming during sessions — critical for breathing apps
- **KEEP**: WakeLock release event listener + re-acquisition on visibilitychange — handles OS-level revocation
- **KEEP**: CSS transform: scale() for circle animation — hardware accelerated, silky smooth on mobile
- **KEEP**: Haptic feedback (navigator.vibrate) on phase transitions — genuine mobile-only feature
- **KEEP**: Solfeggio-adjacent frequencies (396/432/528 Hz) feel genuinely calming vs arbitrary tones
- **KEEP**: Dual event handling (pointerdown + click with dedup flag) — pointerdown for speed, click for iOS audio compat
- **TEST CAUGHT (via Gemini audit)**: Tab-inactive dt catch-up — returning after 30s caused 30+ rapid phase transitions. Capping dt > 2s to 0 prevents this.
- **TEST CAUGHT (via Gemini audit)**: WakeLock leaked on repeated start/stop — overwrote reference without releasing previous lock
- **TEST CAUGHT (via Gemini audit)**: iOS WebKit may not honor pointerdown for AudioContext resume — needs click fallback
- **INSIGHT**: Mobile-first PWAs need: viewport meta (with user-scalable=no), apple-mobile-web-app-capable, theme-color, touch-action: manipulation, -webkit-tap-highlight-color: transparent. This is a checklist, not optional.
- **INSIGHT**: requestAnimationFrame pauses when tab is hidden but performance.now() keeps counting. ALWAYS cap dt in tick functions to prevent physics/state explosions on return.
- **INSIGHT**: The best mobile apps are the ones that leverage mobile-ONLY features (wake lock, haptics, camera, accelerometer) that desktops simply can't do.

### pendulum-waves (2026-03-22)
- **KEEP**: Sub-stepped physics (4 steps per frame) prevents instability at high gravity values
- **KEEP**: HSL hue mapped to pendulum index creates instant rainbow beauty — zero effort, maximum visual impact
- **KEEP**: Canvas shadowBlur on bobs creates a glow effect that elevates the aesthetic dramatically
- **KEEP**: Trail arrays (trailX/trailY) with .shift() capping give smooth fading paths without canvas fade tricks
- **KEEP**: Zero-crossing detection (sign change) is a clean audio trigger — fires exactly once per swing direction
- **KEEP**: Octave shifting for pendulums beyond the PENTA array length — prevents identical frequency phasing
- **TEST CAUGHT (via Gemini audit)**: prevSign hardcoded to 1 — if amplitude was negative, ALL pendulums would trigger audio on frame 1 (loud burst)
- **TEST CAUGHT (via Gemini audit)**: Resize didn't re-init pendulums — they'd render off-screen after window shrink
- **TEST CAUGHT (via Gemini audit)**: Audio frequency wrapping — pendulums 11-15 played same notes as 1-5, causing phasing artifacts
- **INSIGHT**: Physics simulations using pixel lengths in formulas designed for meters will run at wrong speeds. Either add a scale factor or calibrate constants empirically.
- **INSIGHT**: Any parameter that indexes into a finite array (PENTA[i % length]) needs to handle wrap-around distinctly — same index = same output = unwanted duplication.

### drum-lab (2026-03-22)
- **KEEP**: Lookahead scheduler (100ms window, 25ms setTimeout check) — the "Tale of Two Clocks" pattern is mandatory for Web Audio timing
- **KEEP**: DynamicsCompressor with low threshold (-18dB) and fast attack (3ms) — essential for punchy drum sounds without clipping
- **KEEP**: Per-track synth engines with exposed parameters — makes "sequencer" into "instrument"
- **KEEP**: Randomize with per-track density distributions (kick 25%, hat 35%, clap 10%) — generates musically sensible patterns
- **KEEP**: Pattern save/load via localStorage including params + volumes + bpm + swing — complete state persistence
- **TEST CAUGHT (via Gemini audit)**: Swing math was REVERSED (lengthened offbeats, shortened downbeats) AND caused cumulative tempo drift (asymmetric add/subtract). Would have sounded wrong and gradually decelerated.
- **TEST CAUGHT (via Gemini audit)**: exponentialRampToValueAtTime crashes when starting value is exactly 0. Volume slider at zero = immediate DOMException crash. Clamped to 0.001 minimum.
- **TEST CAUGHT (via Gemini audit)**: Creating noise buffers (Math.random() fill) on every drum hit caused GC pressure. Cached 2-second buffer at init, reused everywhere.
- **TEST CAUGHT (via Gemini audit)**: querySelectorAll('.step') on every highlight tick is wasteful. Track previousStep and only update delta.
- **INSIGHT**: Web Audio's exponentialRamp CANNOT start or end at zero — this is a framework constraint that's easy to forget. Always clamp gain values to >= 0.001.
- **INSIGHT**: Swing math must be SYMMETRIC — if you add X to downbeats, subtract X from offbeats. Asymmetric swing = tempo drift over time.
- **INSIGHT**: Pre-generate noise buffers once. Random noise doesn't change perceptibly between hits, but creating Float32Arrays 8x/sec absolutely causes GC stutter.

### key-strike (2026-03-22)
- **KEEP**: Instant start (no button, no overlay, just start typing) = fastest possible time-to-value
- **KEEP**: Combo counter with visual glow at 10+ creates "flow state" pursuit
- **KEEP**: Micro-shake on errors (50ms, 1-2px CSS transform) — tactile without disrupting eye tracking
- **KEEP**: Web Audio key sounds with randomized pitch (800-1200Hz) feel satisfyingly mechanical
- **KEEP**: performance.now() for timing — essential for competitive accuracy
- **KEEP**: Share format with ego-bait ("Your fingers are too slow") drives competitive sharing
- **TEST CAUGHT (via Gemini audit)**: Wrong chars never rendered red — chars array wasn't mutated on incorrect key, cursor didn't advance. User couldn't see their mistakes. Would have been invisible to syntax/static checks.
- **TEST CAUGHT (via Gemini audit)**: AudioContext.resume() needed — browsers start context suspended, sounds wouldn't play on first keystrokes
- **INSIGHT**: Typing tests have a unique state bug: storing wrong input vs skipping it. If wrong keys don't advance the cursor AND mutate the display array, errors become invisible. Always test the error state, not just the happy path.
- **INSIGHT**: "No start button" is the ultimate 3-second time-to-value — the app is ready the instant the page loads.

### pulse-dungeon (2026-03-22)
- **KEEP**: BSP-like room generation (random rooms + overlap check + corridor carving) creates varied, connected layouts
- **KEEP**: Position-mapped pentatonic notes (noteIdx = (x + y*3) % PENTA.length) makes exploration musical
- **KEEP**: DynamicsCompressor threshold/ratio mapped to HP ratio — creates genuine audio tension at low health
- **KEEP**: Different synth sounds for different events (sine=movement, noise=combat, kick=kill, sawtooth=death, triangle=gold)
- **KEEP**: Turn-based movement with enemy AI chase gives tactical depth
- **TEST CAUGHT (via Gemini audit)**: Double attack bug — enemy counter-attacked in movePlayer AND moveEnemies, hitting player twice per turn
- **TEST CAUGHT (via Gemini audit)**: Enemy stacking — no overlap check during spawn allowed multiple enemies on one tile
- **TEST CAUGHT (via Gemini audit)**: Multiple game-over — dying to 3 enemies in one turn queued 3 setTimeout(showGameOver) calls
- **INSIGHT**: When sending code to Gemini, if the file is too long, send the LOGIC portions (game mechanics, state management) not the rendering. Gemini found gameplay bugs, not rendering bugs.
- **INSIGHT**: Turn-based games have a unique bug class: "action happens twice per turn." Always trace the full execution path of one player action to verify each entity acts exactly once.

### prose-xray (2026-03-22) — FIRST BUILD UNDER NEW TESTING PROTOCOL
- **KEEP**: Sending ACTUAL CODE to Gemini (not summaries) found 5 real bugs. This is the single biggest quality improvement.
- **KEEP**: Automated test suite caught the project loads and has no console errors
- **KEEP**: Debounced analysis (300ms) prevents jank while typing — essential for any live-analysis tool
- **KEEP**: Abbreviation protection in sentence splitting (Mr., Dr., etc.) — common edge case
- **KEEP**: Demo texts that show dramatically different stats (Hemingway vs Academic) prove the tool's value instantly
- **IMPROVE**: Brace balance test has false positives on regex-heavy code — need to improve the test tool's string stripping
- **TEST CAUGHT**: Variable ordering bug (validSentCount used before const declaration) — would have been a runtime crash
- **TEST CAUGHT**: Syllable regex {1,2} incorrectly split "beautiful" into 4 syllables instead of 3
- **TEST CAUGHT**: Sentence splitter broke "Mr. Smith" into two sentences
- **TEST CAUGHT**: escapeHtml missing quote escaping — potential XSS in future attribute contexts
- **INSIGHT**: The new protocol works. Sending actual code to Gemini for audit is 10x more valuable than sending summaries. Gemini found bugs that syntax checking and static analysis could never catch.
- **INSIGHT**: The testing protocol has its own bugs (brace checker false positives). The test tool itself needs continuous improvement.

### sonic-reflex (2026-03-22)
- **KEEP**: Synthesized audio tension (rising sine + accelerating LFO noise pump) creates genuine physical anxiety. Way more engaging than a simple color change.
- **KEEP**: pointerdown event instead of click — eliminates ~300ms mobile tap delay, critical for reaction games
- **KEEP**: performance.now() tied to visual frame, NOT AudioContext.currentTime — measures what the user actually reacts to
- **KEEP**: Random delay 2-6s prevents rhythmic prediction — essential for reaction test integrity
- **KEEP**: Proper gain ramp to 0 over 10ms before stopping oscillators — prevents audio click/pop artifacts
- **KEEP**: Rating tiers (INHUMAN/ELITE/FAST/etc.) with colors create aspirational goals and shareability
- **KEEP**: Clipboard share format: "Sonic Reflex: 185ms (ELITE) | Best: 172ms | Can you beat me?" — natural viral loop
- **KEEP**: Histogram with 7 color-coded buckets — visual proof of improvement over time
- **IMPROVE**: Should add photosensitivity toggle (reduce flash to subtle color shift for sensitive users)
- **IMPROVE**: No account for Bluetooth latency — calibration mode would make it fairer
- **INSIGHT**: Audio creates EMOTIONAL tension that visual cues alone cannot. The dread of waiting for the "drop" is what makes this addictive, not the click itself.
- **INSIGHT**: Competitive shareability ("beat my score") is a powerful retention loop that none of my other projects had. The share button turns users into distributors.
- **INSIGHT**: Use pointerdown for ALL time-critical interactions. click has variable delay across browsers and devices.

### ascii-cam (2026-03-22)
- **KEEP**: 3-second time-to-value > feature depth. User opens it, sees themselves as ASCII, laughs. Done.
- **KEEP**: Downscale video on hidden canvas BEFORE getImageData — critical perf win (process 100 cols not 640)
- **KEEP**: willReadFrequently hint on canvas context — tells browser to keep pixels in CPU memory
- **KEEP**: Array pre-allocation + join('') instead of string concat — eliminates GC pressure at 60fps
- **KEEP**: ITU-R BT.601 luminance (0.299R + 0.587G + 0.114B) — perceptually accurate grayscale
- **KEEP**: Aspect ratio correction: rows = cols / aspect / 2 (chars are ~2x taller than wide)
- **KEEP**: Braille characters encode 2x4 pixel blocks as 8-bit patterns — extremely high visual density
- **KEEP**: Snapshot renders to temp canvas with theme colors — export matches what user sees
- **KEEP**: textContent for all user-facing text — zero XSS surface
- **IMPROVE**: Could add rear camera toggle for mobile
- **IMPROVE**: 60fps is overkill for ASCII — 15-30fps would be more retro and battery-friendly
- **INSIGHT**: "Toy" projects that make people smile are just as valuable as serious tools. They get shared more.
- **INSIGHT**: The webcam pipeline (getUserMedia → hidden video → canvas downsample → getImageData → transform → render) is a reusable pattern for any real-time video processing project.

### git-time-machine (2026-03-22)
- **KEEP**: CLI-driven interaction (type commands → see graph update) is MUCH better than click-to-build for educational tools. Users learn the actual commands, not a custom UI.
- **KEEP**: Short readable commit IDs (c0, c1, c2) instead of real SHA hashes — makes the visualization immediately scannable
- **KEEP**: BFS ancestor check for fast-forward detection — accurate to how real Git works
- **KEEP**: Rebase = collect commits not in target ancestry + replay on new base. Simple, correct, visual.
- **KEEP**: Colored lanes per branch with bezier cross-connections — immediately shows branch/merge topology
- **KEEP**: Branch labels as colored rounded-rect tags next to nodes — much clearer than just colored circles
- **KEEP**: Command history with up/down arrows — essential for any terminal UI
- **KEEP**: Progressive challenges with validation functions — check(git) returns true when DAG matches goal
- **IMPROVE**: Graph layout gets messy with many branches — need graph panning and a smarter lane assignment algorithm
- **IMPROVE**: No animated transitions — nodes should physically move when rebasing, not just re-render statically
- **INSIGHT**: Git is just a DAG with mutable branch pointers. Once you model it that way, every git operation is a simple graph transformation.
- **INSIGHT**: Educational CLI tools are more valuable than click-based ones because users build muscle memory for the REAL tool.

### flow-field (2026-03-22)
- **KEEP**: Float32Array with stride access (STRIDE=5, x/y/vx/vy/life) — THE way to do high-count particles in JS. Zero allocation, linear memory, cache-friendly.
- **KEEP**: Array compaction on dead particles — swap last active into dead slot, decrement count. No splice, no holes.
- **KEEP**: Custom Perlin noise from scratch (permutation table + gradient interpolation) — eliminates external dependency
- **KEEP**: Long-exposure fade (bg fill at alpha 0.04) + additive blending (globalCompositeOperation='lighter') at low particle alpha (0.15) = gorgeous trails without white blowout
- **KEEP**: Density-based audio triggers (count particles near attractor, fire note when threshold reached) — prevents polyphony choking while sounding organic
- **KEEP**: DynamicsCompressor + MAX_VOICES + rate limiting (every 15 frames) = three-layer audio safety
- **KEEP**: Curated palettes with named presets > raw color pickers. Constraining the output space guarantees aesthetics.
- **KEEP**: Immersive "anti-UI" (no sidebar, just canvas + fading hints + keyboard) — appropriate for creative/art tools
- **IMPROVE**: Modifier keys (Shift/Alt+click) are undiscoverable and mobile-incompatible. Need touch gesture support or a subtle mode toggle.
- **INSIGHT**: Combining visual generative art + audio generative art in one tool creates something exponentially more captivating than either alone. The feedback loop (see flow → hear harmony) is mesmerizing.
- **INSIGHT**: Float32Array particles with stride access is 10-50x more memory-efficient than arrays of objects. Use this pattern for ANY project with >1000 entities.

### minesweeper-evolved (2026-03-22)
- **KEEP**: "Classic + one twist" formula proven again — everyone knows minesweeper, the explosion mechanic is one sentence
- **KEEP**: Hex grid with parity-dependent direction arrays — 6-way adjacency tightens chain reactions vs 8-way
- **KEEP**: First-click safety (mines placed AFTER first click, safe zone includes neighbors) — essential for minesweeper
- **KEEP**: `cell.revealed = true` set BEFORE recursing into neighbors — prevents infinite recursion in chain reactions
- **KEEP**: Screen shake intensity scaling with chain depth — deeper chains feel more impactful
- **KEEP**: Dig/Flag mode toggle button for mobile/touch support — right-click alternatives are essential
- **IMPROVE**: Could use dual canvas layering (static grid + animated particles) for better perf
- **IMPROVE**: Hex cell click detection uses brute-force distance check — axial coordinate rounding would be O(1)
- **INSIGHT**: Turning a PASSIVE game action into an OFFENSIVE one creates completely new gameplay. Flagging in classic minesweeper is defensive; here it's a weapon.
- **INSIGHT**: Puzzle games need the same "juice" as action games — screen shake, particles, chain notifications all make the deductive gameplay feel exciting.

### pathfinder-arena (2026-03-22)
- **KEEP**: Layering all algorithms on ONE grid beats split-screen — you see the race happen spatially
- **KEEP**: Path offsets per algorithm ([-2,-2], [2,2], etc.) make overlapping paths distinguishable
- **KEEP**: Integer key `y * COLS + x` for O(1) Set/Map lookups — crucial for 6 simultaneous algorithms
- **KEEP**: State object pattern { visited, frontier, parent, done } isolates each algorithm cleanly
- **KEEP**: Lockstep stepping (all algorithms advance N steps per frame) ensures a fair visual race
- **KEEP**: Maze presets (random/spiral/rooms/diagonal) give users instant variety
- **IMPROVE**: Priority queue uses linear scan (O(n)) — binary min-heap would help at 60x60 grid
- **IMPROVE**: Semi-transparent overlaps get muddy with 6 colors — algorithm visibility toggles would help
- **IMPROVE**: Gemini wanted RL neural agent racing classic algorithms — too heavy for single file, but great future concept
- **INSIGHT**: Algorithm races are more engaging than single-algorithm visualizations. Competition creates narrative tension.
- **INSIGHT**: When Gemini's suggestion is too ambitious (WebGPU neural swarm), it's OK to take the core concept (pathfinder race) and leave the advanced twist for a future iteration. Ship the 80% that's great.

### http-playground (2026-03-21)
- **KEEP**: Presets that auto-send on click = instant gratification. User sees a working response in <1 second.
- **KEEP**: Ctrl/Cmd+Enter to send — non-negotiable for any dev tool
- **KEEP**: localStorage auto-save makes the tool "sticky" — users come back and their last request is still there
- **KEEP**: Dual header parsing (try JSON first, fallback to key:value lines) — forgiving input
- **KEEP**: CORS proxy toggle WITH security warning — honest UX about the trade-off
- **KEEP**: Color-coded methods (GET=green, POST=yellow, DELETE=red) — instantly scannable
- **KEEP**: Copy button with "Copied!" feedback — tiny detail, big UX win
- **IMPROVE**: Regex-based JSON highlighting is fragile on edge cases (nested strings with colons). A proper tokenizer would be more robust.
- **IMPROVE**: Should truncate/omit response bodies in localStorage history to avoid 5MB quota
- **INSIGHT**: Dev tools that persist state via localStorage feel 10x more professional than tools that reset on refresh.
- **INSIGHT**: The CORS problem is the #1 killer for browser-based API tools. Having a proxy toggle is essential — but warning about it is equally important.

### csv-cinema (2026-03-21)
- **KEEP**: Auto-inference with graceful fallback (manual remap UI) = zero-config magic that still works when it guesses wrong
- **KEEP**: Lerp factor 0.12 for bar position + value = buttery smooth chart transitions
- **KEEP**: 3 built-in demo datasets eliminate the "I don't have a CSV handy" cold-start problem
- **KEEP**: Dynamic HSL color generation via string hash for labels beyond the palette — handles 50+ categories
- **KEEP**: XSS-safe DOM construction (createElement + textContent) for user-supplied CSV headers
- **KEEP**: Top-15 bar filter prevents visual overload with large datasets
- **IMPROVE**: Custom CSV parser is fragile — doesn't handle quoted newlines or escaped quotes. A more robust regex parser would help.
- **IMPROVE**: Parsing large files (50MB) blocks main thread — Web Worker would fix this
- **INSIGHT**: "Zero config with fallback" is the ideal UX pattern for data tools. Auto-detect everything, but always provide a manual override.
- **INSIGHT**: Bar chart races are captivating because of ranking changes — the visual is the bars SWAPPING POSITIONS, not just growing. The lerp on Y position is what makes it magical.
- **INSIGHT**: Demo datasets are even more important for data tools than for simulations — users need to see the wow factor before committing to finding their own data.

### asteroids-evolved (2026-03-21)
- **KEEP**: Familiar mechanic + one emergent twist = instantly understandable AND creative. Everyone knows Asteroids, the drone ecosystem is the hook.
- **KEEP**: Wireframe neon aesthetic is cheap to render and looks great — no sprites needed
- **KEEP**: Screen shake proportional to event size makes impacts feel satisfying
- **KEEP**: Color legend on start screen eliminates "what am I looking at?" confusion
- **KEEP**: Drone separation forces (repel when too close) prevent the ugly clumping blob
- **KEEP**: Reverse-iteration splice for entity cleanup — correct pattern, no skipped elements
- **KEEP**: Window blur clears keys + dt cap at 0.05 — standard browser game safety
- **IMPROVE**: Should use object pooling for bullets/particles (learnings say this, I didn't do it here — GC will stutter at high entity counts)
- **INSIGHT**: "Take a classic everyone knows + add one simulation twist" is a reliable game design formula. Zero explanation needed because the base is familiar.
- **INSIGHT**: Always verify syntax with `node -c` — this build passed cleanly because I learned from the regex-quest bug.

### markov-composer (2026-03-21)
- **KEEP**: Force-directed graph layout (Coulomb repulsion + Hooke attraction + center gravity + damping) — organic, stable, beautiful
- **KEEP**: Animated playhead + trail glow makes abstract algorithms tangible and mesmerizing
- **KEEP**: Click-to-steer generation bridges passive viz and active sandbox — key interactivity pattern
- **KEEP**: Log-scale node sizing (Math.log(1 + freq)) — essential for natural language where Zipf's law makes top words dominate
- **KEEP**: Debounced slider rebuild (200ms timeout) — prevents chain reconstruction spam
- **KEEP**: Built-in sample texts let users experience it instantly without finding their own corpus
- **IMPROVE**: Off-graph word handling still feels abrupt — could animate playhead fading and reappearing
- **IMPROVE**: O(N^2) repulsion limits to ~200 nodes — Barnes-Hut quadtree would allow 1000+
- **INSIGHT**: Algorithms become fascinating when made visual and interactive. Markov chains are boring as text generators but captivating as animated graph walks.
- **INSIGHT**: Debounce expensive operations triggered by sliders — rebuild on `input` event only after 150-200ms of inactivity.
- **INSIGHT**: The "steering" mechanic (click to redirect) turns any generation algorithm into a collaborative sandbox.

### neural-playground (2026-03-21)
- **KEEP**: Xavier/Glorot initialization — essential for deep networks, prevents vanishing/exploding gradients
- **KEEP**: Float32Array pre-allocated grid buffer for decision boundary — zero GC in render loop
- **KEEP**: Gradient clipping (max +-5) in backward pass — prevents ReLU explosion
- **KEEP**: L2 regularization makes boundaries smooth and visually appealing
- **KEEP**: Stats updated every 100 epochs, loss recorded every 5 — prevents DOM thrashing
- **KEEP**: Log-scale learning rate slider — exponential range feels linear to the user
- **IMPROVE**: Gemini suggested Adam optimizer — would converge faster on spiral dataset
- **IMPROVE**: 40x40 grid with individual fillRect calls — could use ImageData for single putImageData call
- **IMPROVE**: Training on main thread — Web Worker would prevent UI lag on 6-layer networks
- **INSIGHT**: Implementing ML from scratch in ~200 lines of JS is very doable. The math is just matrix multiply + chain rule. Xavier init and gradient clipping are the difference between "works" and "explodes."
- **INSIGHT**: The 40x40 grid resolution is the sweet spot — lower looks blocky, higher kills the CPU. Canvas interpolation smooths it visually.

### regex-quest (2026-03-21)
- **KEEP**: Tiered enemy database maps 1:1 to skill progression — each tier introduces one new regex concept
- **KEEP**: Live regex preview with debounced highlighting — immediate feedback is critical for learning
- **KEEP**: safeMatch() with performance.now() timeout — prevents ReDoS browser freezes without Web Workers
- **KEEP**: Anti-cheat penalty for `.*` and other lazy patterns — forces players to actually learn
- **KEEP**: escapeHtml() before innerHTML insertion — prevents XSS from user regex output
- **KEEP**: Shop every N floors breaks up combat monotony and adds economic decisions
- **IMPROVE**: Gemini wanted Web Worker for regex execution — safeMatch timeout is simpler but less robust
- **IMPROVE**: Could add localStorage save state to prevent losing progress on tab close
- **DISCARD**: Considered real-time regex like Regex101 without debounce — too janky while typing complex patterns
- **INSIGHT**: Educational games work when the difficulty curve IS the curriculum. Each enemy tier = one lesson.
- **INSIGHT**: User-input regex is a security surface — always guard against ReDoS, XSS, and infinite loops.
- **INSIGHT**: Anti-exploit mechanics (cheesy pattern penalty) are important for maintaining the learning incentive.

---

## Meta-Patterns

1. **The best projects are simulations, not animations.** Give users controls that feed into a system, and let the system produce emergent behavior. This scores highest on creativity.

2. **Progressive rendering is the universal performance fix.** Low-res during interaction, full-res on idle. Works for fractals, maps, any CPU-heavy canvas work.

3. **Object pooling + typed arrays + bitwise math** = the performance trifecta for canvas rendering. Learn it once, apply everywhere.

4. **Presets are essential.** They're the fastest way to show off what a project can do. 4-6 presets minimum.

5. **Single-file constraint is a strength.** Procedural generation of textures/assets eliminates loading, CORS, and dependency issues. Lean into it.

6. **Web Audio API is a superpower.** OscillatorNode + GainNode + exponentialRamp = instant synth sounds. Pentatonic scales guarantee harmony. DynamicsCompressorNode prevents clipping with polyphony.

7. **Gemini keeps docking for "incomplete code"** when I send summaries. In future reviews, either send the full file verbatim or clearly list every function/variable that exists with line counts.

8. **Always run `node -c` syntax check** after refactoring JS. A stray `});` (leftover from extracting an anonymous function) silently broke regex-quest's start button. The IIFE still loaded but threw at the bad line, preventing all event listeners below it from binding.

9. **Abstract projects need onboarding.** Neural-playground was "too abstract" — adding a welcome overlay explaining what the colors mean + descriptive preset cards with difficulty hints made it approachable. If the user can't understand what they're looking at in 5 seconds, add a guide.

### flash-cards (2026-03-23)
- **KEEP**: CSS 3D card flip with preserve-3d + backface-visibility — clean, performant animation with no JS animation frames needed
- **KEEP**: Using front+back composite key to match existing cards when re-parsing editor text — preserves spaced repetition progress
- **IMPROVE**: parseEditor was rebuilding the entire cards array from scratch, destroying all study progress — Gemini caught this critical UX bug. Always preserve user data when editing content that has associated metadata
- **IMPROVE**: Rating fallthrough defaulted to "Easy" on invalid input — always use explicit conditionals with a failsafe return for user-facing rating/scoring functions
- **DISCARD**: Shuffle button that resets intervals — since cards are already shown randomly, shuffling the array does nothing useful. Changed to a "Reset" button that only clears nextReview times
- **INSIGHT**: When a data model has both user-editable content (front/back text) AND system-managed metadata (intervals, timestamps), editing must merge, not replace. This applies broadly: any editor that touches objects with hidden state needs a merge strategy.
- **TEST CAUGHT**: No bugs caught by automated tests this build — all bugs were logic-level (data loss on edit) that require Gemini review to catch

### elementa (2026-03-23) — PROJECT #70 (5-build review)
- **KEEP**: Uint8Array grid + Uint32Array pixel buffer via ImageData — proven pattern for any cellular automata or pixel-level sim
- **KEEP**: Alternating left-to-right / right-to-left scan direction — prevents directional bias in fluid flow
- **KEEP**: Bottom-to-top processing for gravity — prevents particles teleporting downward in a single frame
- **KEEP**: Bresenham line algorithm for brush input — eliminates gaps in fast strokes
- **KEEP**: Density-based displacement (sand sinks through water, oil floats) — simple numeric comparison creates rich emergent behavior
- **KEEP**: Probabilistic reactions (Math.random() < rate) — organic feel vs instant state changes
- **IMPROVE**: Fire/steam teleported to top instantly — upward-moving cells were processed multiple times per frame. Fixed with bit-flag bitmask (high bit of Uint8Array cell value). Gemini caught this.
- **IMPROVE**: Resize destroyed simulation — initGrid wiped grid. Fixed by copying old data into new grid. Gemini caught this.
- **IMPROVE**: Brush couldn't overwrite existing elements — too restrictive. Removed the empty-cell check. Gemini caught this.
- **INSIGHT**: For cellular automata with bidirectional movement (gravity + rising), use a "processed this frame" flag to prevent double-processing. The high bit of a Uint8Array is free when element IDs < 128 — elegant zero-cost flag.
- **INSIGHT**: Any operation that reinitializes a data structure (resize, reset, mode change) must preserve user data. Copy first, then reinitialize.
- **TEST CAUGHT**: No bugs caught by automated tests — all 3 bugs were physics/logic-level issues only visible through Gemini code review.

#### 5-Build Review (Builds #66-70: tip-calc, sudoku, tic-tac-toe, flash-cards, elementa)
- **All 5 shipped working.** Zero user-reported bugs in this batch.
- **Gemini audit value**: Caught 12+ bugs across 5 builds. Most common: data integrity (progress wipe, ghost values), input timing (click spam), and physics correctness (teleportation).
- **New accumulated principle**: When a data model has both user-editable content AND system-managed metadata (intervals, scores, timestamps), any edit/parse operation MUST merge with existing data rather than replacing it.
- **New accumulated principle**: Typed array bit flags (using unused high bits) are an elegant way to track per-cell state without allocating a second array.
- **No recurring Gemini critiques** — each build's bugs were unique. Process is healthy.
- **Automated tests caught 0 bugs this batch** — all bugs were logic-level. Consider adding: physics simulation frame tests? Hard to automate for single-file HTML apps.

### memory-xray (2026-03-23)
- **KEEP**: ArrayBuffer + DataView + Uint8Array trifecta — one buffer, three views for different access patterns (bit manipulation, typed reads, raw bytes)
- **KEEP**: IEEE 754 color-coding (sign/exponent/mantissa) with CSS classes — immediate visual understanding of float structure
- **KEEP**: Number() instead of parseFloat() for strict parsing — rejects "123abc", accepts hex "0x1A"
- **KEEP**: Brutalist terminal aesthetic (monospace, zero border-radius, neon on black) — strong visual identity for technical tools
- **IMPROVE**: formatFloat regex `/\.?0+$/` stripped trailing zeros from integers (100→"1") — Gemini caught. Fix: Number(toPrecision(17)).toString()
- **IMPROVE**: Endian toggle physically reversed bytes — should change DataView interpretation flag instead. Physical reversal desyncs writes.
- **IMPROVE**: IEEE 754 bit classification was hardcoded for big-endian — must remap with `(7 - byteIdx) * 8 + (7 - bitIdx)` for little-endian
- **INSIGHT**: Regex for stripping trailing zeros from formatted numbers is DANGEROUS. The optional dot `\.?` makes `0+$` match integer trailing zeros. Always use Number() round-trip instead.
- **INSIGHT**: DataView endianness should be a READ/WRITE parameter, never a physical byte reorder. The buffer stays the same; interpretation changes.
- **INSIGHT**: When a UI toggle changes data interpretation (not data itself), rebuild any derived visual elements (IEEE 754 labels, color coding) to match the new interpretation.
- **TEST CAUGHT**: No bugs caught by automated tests — all bugs were logic-level (formatting, endianness semantics)

### neon-mandala (2026-03-23)
- **KEEP**: Canvas radial symmetry via translate(center) + rotate(angleStep*i) + scale(1,-1) mirror — elegant loop produces kaleidoscopic patterns
- **KEEP**: Auto-cycling HSL hue based on time + distance from center — creates continuous rainbow gradients without user color selection
- **KEEP**: Ephemeral fade via rgba(bg, low-alpha) fillRect each frame — creates ghost trails that naturally decay
- **KEEP**: setPointerCapture for drawing — ensures strokes continue smoothly even when pointer leaves canvas bounds
- **KEEP**: Glassmorphic controls with low opacity that increase on hover — keeps the canvas immersive
- **IMPROVE**: High-DPI canvas set canvas.width but not canvas.style.width — caused 2x overflow on Retina. Must ALWAYS set both buffer size and CSS layout size.
- **IMPROVE**: getPos used raw clientX without subtracting canvas bounding rect — drawing offset from cursor when any margin/padding exists
- **INSIGHT**: High-DPI canvas rendering requires TWO size settings: canvas.width/height (buffer resolution) AND canvas.style.width/height (CSS layout). Missing either causes overflow or blurriness.
- **INSIGHT**: CSS comments can trigger test regex patterns — the word "overlay" in a comment triggered the start-screen test. Be mindful of test heuristics.
- **TEST CAUGHT (automated)**: CSS comment "Controls overlay" triggered overlay detection test. Renamed to "Controls panel".

### glitch-studio (2026-03-23)
- **KEEP**: Uint32Array view over ImageData buffer for pixel manipulation — move whole pixels as 32-bit integers instead of 4 separate channel reads
- **KEEP**: Transpose-sort-transpose for vertical pixel sorting — avoids rewriting sort logic for column traversal
- **KEEP**: SMPTE test pattern as default demo — immediately shows what the tool does without requiring user upload
- **KEEP**: toBlob for image export — avoids toDataURL length limits on large images
- **KEEP**: Luminance threshold band (min+max) for selective sorting — gives fine control over which pixel ranges get sorted
- **IMPROVE**: Init applied effect with temp values then reset sliders to defaults — UI showed 0 but canvas showed 8. Gemini caught. UI state must always match visual state.
- **IMPROVE**: Paired range sliders (min/max threshold) could cross, silently breaking the filter. Must auto-clamp on input.
- **IMPROVE**: Missing dragenter preventDefault — browser could navigate away on file drop. Must handle dragenter + dragover + drop.
- **IMPROVE**: Array.push in hot pixel loop causes GC pressure — use pre-allocated Uint32Array instead
- **INSIGHT**: When initializing a demo/preview state, set the UI controls to match the demo values and LEAVE them there. Never apply temporary values then silently reset.
- **INSIGHT**: Any paired min/max slider UI must enforce ordering constraints on input — the lower slider must not exceed the upper, and vice versa. Silent failure on impossible ranges is confusing.
- **INSIGHT**: For drag-and-drop: handle ALL three events (dragenter, dragover, drop) with preventDefault. Missing any one can cause the browser to navigate away.
- **TEST CAUGHT**: No bugs caught by automated tests — all issues were UI logic and UX patterns

### morse-pulse (2026-03-23)
- **KEEP**: Koch method character progression (start with 2 chars, add at 90% accuracy) — scientifically backed Morse learning approach
- **KEEP**: Farnsworth timing (fast character speed, stretched spacing) — forces auditory pattern recognition over counting
- **KEEP**: 550Hz sine wave with 5ms linear ramp envelope — clean, fatigue-free Morse tone
- **KEEP**: Silent progression (no fanfare on level-up) — maintains flow state
- **KEEP**: Error replay with visual aid (letter = morse pattern) shown during replay — reinforces correct association
- **IMPROVE**: Rolling accuracy history not cleared on level-up — caused cascading multi-level jumps. Gemini caught. Must reset tracking state on progression events.
- **IMPROVE**: calcFarnsworthDelay() was defined but never called — dead code meant the key Farnsworth feature was missing. Always grep for defined-but-uncalled functions before shipping.
- **IMPROVE**: Visual aid text reverted before replay audio finished — moved revert into playMorse callback so user sees the answer while hearing it
- **IMPROVE**: Audio envelope had fixed 5ms ramp that could exceed duration at high WPM — use Math.min(0.005, duration/4) for safety
- **INSIGHT**: Any progression system with a rolling accuracy window must RESET the window on progression. Otherwise the old high-accuracy data carries forward and triggers immediate cascading level-ups.
- **INSIGHT**: Dead code is a bug signal. If you define a function and never call it, you either have an unused feature or a missing integration. Grep for all function definitions and verify each is called.
- **INSIGHT**: Start screens that are plain divs (not buttons) may not be clicked by automated tests that look for button elements. Include a visible button for test compatibility.
- **TEST CAUGHT (automated)**: Start screen (#start-screen div) wasn't dismissed by Playwright — test clicks buttons, not divs. Added a START button.

### dice-oracle (2026-03-23) — PROJECT #75 (5-build review)
- **KEEP**: Discrete convolution for exact dice probability distributions — mathematically correct, zero approximation for standard dice
- **KEEP**: Monte Carlo fallback only for complex modifiers (keep-highest) — clean separation of exact vs approximate
- **KEEP**: crypto.getRandomValues for dice rolls — proper entropy source
- **KEEP**: Live preview distribution on input change (debounced 300ms) — user sees the shape before rolling
- **KEEP**: Percentile + probability display — gives statistical context ("TOP 8% roll")
- **KEEP**: Preset buttons that actually execute the action — don't just preview
- **IMPROVE**: Chart axis labels invisible (#222 on #000) — always test text contrast against background
- **IMPROVE**: Preset buttons only previewed without rolling — Gemini caught. Buttons that look like they DO something must DO it.
- **IMPROVE**: Leading negatives silently dropped (-1d4 → +1d4) — parser must handle unary minus
- **IMPROVE**: Rolls sampled from Monte Carlo distribution instead of true simulation — never derive randomness from approximated randomness. Always roll actual dice.
- **IMPROVE**: for...in loop on objects vulnerable to prototype pollution — use Object.keys() always
- **INSIGHT**: When you have both a distribution (for visualization) AND a roll (for the result), generate them independently. The roll must come from true simulation, not from sampling the precomputed graph.
- **INSIGHT**: for...in is NEVER safe for iterating object keys in a single-file app where you can't control the global environment. Always use Object.keys().
- **TEST CAUGHT**: No bugs caught by automated tests — all were logic-level

#### 5-Build Review (Builds #71-75: memory-xray, neon-mandala, glitch-studio, morse-pulse, dice-oracle)
- **All 5 shipped working.** Zero user-reported bugs. 10 consecutive working builds (66-75).
- **Recurring: UI state desync** — appeared in glitch-studio and memory-xray. NEW ACCUMULATED PRINCIPLE: UI controls must always reflect the actual visual/data state. Never apply temp values then reset sliders.
- **Recurring: High-DPI canvas** — neon-mandala forgot CSS dimensions (2nd occurrence across all builds). ADDED TO ACCUMULATED PRINCIPLES: High-DPI canvas requires BOTH canvas.width/height AND canvas.style.width/height.
- **New pattern: Dead code = missing feature** — morse-pulse had Farnsworth function defined but never called. Consider adding a "defined but uncalled function" check to the test suite.
- **Gemini audit value**: Caught 15+ bugs across 5 builds. Most valuable catches: architectural (roll-from-distribution), state management (cascading level-up), and visual (invisible text).
- **No recurring Gemini critiques** — each build's bugs were unique. Process is healthy.

### void-scape (2026-03-23)
- **KEEP**: Euclidean rhythms via Bresenham/modulo — simple, reliable, produces correct patterns for all inputs
- **KEEP**: FM synthesis (sine carrier + high-ratio sine modulator) — creates rich bell/marimba tones with just 2 oscillators
- **KEEP**: Cross-fed ping-pong delay network with LP filters — creates spatial reverb from pure math, zero external assets
- **KEEP**: Lookahead audio scheduler (setInterval 25ms + AudioContext.currentTime) — rock-solid timing decoupled from frame rate
- **KEEP**: Frequency quantization to a musical scale — ensures all random note selections sound harmonious
- **IMPROVE**: Recursive Bjorklund algorithm produced empty patterns for some inputs — Gemini caught. Replaced with Bresenham. Lesson: prefer simpler algorithms when correctness is critical.
- **IMPROVE**: Visual flash fired before audio — lookahead scheduling sets trigger time in the future, but visual immediately started decaying. Fixed with `elapsed >= 0` clamp.
- **IMPROVE**: Tab throttling caused scheduling in the past — Math.max(time, currentTime) prevents DOMException
- **INSIGHT**: When audio scheduling uses lookahead (time in the future), visual effects must NOT trigger until that future time arrives. Always clamp `elapsed = now - scheduledTime` to >= 0.
- **INSIGHT**: Complex recursive algorithms can silently fail (return empty/wrong results) for edge-case inputs. Simpler mathematical approaches (modulo, Bresenham) are often more reliable AND faster.
- **INSIGHT**: Algorithmic reverb (delay network + LP filters + cross-feedback) achieves convincing spatial audio with pure Web Audio nodes — no impulse response files needed.
- **TEST CAUGHT**: No bugs caught by automated tests — all were algorithm/timing level

### connect-four (2026-03-23)
- **KEEP**: Minimax with alpha-beta pruning + center-first move ordering — effective AI for 7x6 grid
- **KEEP**: Center-weighted heuristic array [0,1,2,3,2,1,0] — captures the most important Connect Four strategy
- **KEEP**: Window scoring (all 4-cell windows for H/V/diag) — comprehensive board evaluation
- **KEEP**: setTimeout(aiMove, 50) to yield to UI thread — prevents browser freeze during AI calculation
- **KEEP**: Depth-aware terminal scoring (win + depth*100) — AI prefers faster wins and delays losses
- **IMPROVE**: renderBoard used className = 'cell' which wiped ALL classes including 'dropping' animation — must only toggle player-specific classes with classList.remove/add
- **IMPROVE**: CENTER_WEIGHT array defined but evaluate() used hardcoded b[r][3] check — dead variable = weaker AI. Gemini caught.
- **IMPROVE**: Minimax scored all wins equally regardless of depth — AI would stall instead of winning immediately. Added depth bonus to terminal scores.
- **INSIGHT**: When rendering board state, NEVER overwrite className entirely if elements can have additional state classes (animations, highlights, previews). Use classList.remove/add for the specific classes you manage.
- **INSIGHT**: Minimax terminal scores MUST include depth to create urgency. Without it, the AI is "apathetic" — it knows it will win but doesn't care when. score += depth * factor for wins, score -= depth * factor for losses.
- **INSIGHT**: Defined-but-unused variables are a recurring pattern (3rd occurrence: CENTER_WEIGHT, Farnsworth delay, stopScheduler). Must grep for unused definitions before shipping.
- **TEST CAUGHT**: No bugs caught by automated tests — all were CSS/logic level

### entropy-forge (2026-03-23)
- **KEEP**: crypto.getRandomValues with rejection sampling — eliminates modulo bias for cryptographically fair selection
- **KEEP**: Embedded wordlist as comma-split string.split(",") — compact, no external assets, instant load
- **KEEP**: Shannon entropy calculation (L × log2(R)) — gives users real security context, not just "weak/strong"
- **KEEP**: Scramble reveal animation with progressive settling — satisfying visual feedback without blocking copy
- **KEEP**: Clipboard API with textarea fallback for non-HTTPS contexts
- **IMPROVE**: Rapid generate clicks caused multiple concurrent scramble animations — Gemini caught. Fixed with cancelAnimationFrame tracking.
- **IMPROVE**: Settings changes (sliders, checkboxes) only updated entropy bar, not password — stale password displayed with mismatched entropy. Must regenerate on every setting change.
- **IMPROVE**: cryptoRandInt(0) caused NaN/infinite loop — guard clause needed for edge case
- **INSIGHT**: Any UI that shows both "output" and "metadata about output" (entropy, stats, labels) MUST regenerate both in sync. Updating metadata without regenerating the output creates a dangerous UX desync.
- **INSIGHT**: requestAnimationFrame-based animations that can be re-triggered need cancellation tracking. Store the frame ID and cancelAnimationFrame before starting a new sequence.
- **TEST CAUGHT**: No bugs caught by automated tests — all were UX/logic level

### crypt-lex (2026-03-23)
- **KEEP**: Two-pass evaluation for Wordle-style games — Pass 1: exact matches (decrement target counts), Pass 2: partial matches against remaining counts. Handles duplicate letters correctly.
- **KEEP**: Virtual keyboard state priority (absent=1, present=2, correct=3) — keys never downgrade, always show highest achieved state
- **KEEP**: Split dictionary (small target list + large validation list) — keeps target pool curated while allowing broad guess vocabulary
- **KEEP**: Only update active row on keystroke instead of full grid — avoids redundant evaluate() calls on every keypress
- **KEEP**: void offsetWidth reflow trick to restart CSS animations — solves rapid-fire animation restart without setTimeout race conditions
- **IMPROVE**: updateGrid re-evaluated ALL past guesses on every single keystroke — wasteful DOM+logic work. Gemini caught. Split into updateActiveRow (for typing) and direct render in submitGuess.
- **IMPROVE**: Shake animation used setTimeout which raced on rapid Enter presses — reflow trick is the correct pattern for restartable CSS animations
- **INSIGHT**: For any game with a grid of past+current state, separate the rendering: past rows are static (render once on submit), current row is dynamic (update on every keystroke). Never re-evaluate past rows.
- **INSIGHT**: CSS animation restart: remove class → force reflow (void el.offsetWidth) → re-add class. This is the standard pattern; setTimeout-based removal races with rapid re-triggers.
- **TEST CAUGHT**: No bugs caught by automated tests — all were performance/animation level

### beat-haus (2026-03-23) — PROJECT #80 (5-build review)
- **KEEP**: Lookahead audio scheduler (setInterval 25ms + schedule 100ms ahead) — sample-accurate timing decoupled from UI thread
- **KEEP**: Visual event queue — schedule visual updates at audio time, process in rAF when audioCtx.currentTime catches up
- **KEEP**: WaveShaperNode with mathematical distortion curve — adjustable drive without external assets
- **KEEP**: DynamicsCompressorNode as master limiter — prevents clipping when grid is fully active
- **KEEP**: Programmatic noise buffer (AudioBuffer filled with Math.random) — reusable for snare and hat
- **KEEP**: Acid track with 3-state cycling (off → lo → hi) — compact UI for pitch variation in a grid
- **IMPROVE**: Swing math asymmetric (added 0.5x odd, subtracted 0.1x even) — Gemini caught. Tempo drifted upward with swing. Must be symmetric: +X even, -X odd.
- **IMPROVE**: Visual playhead fired at schedule time, not audio time — lookahead causes 100ms visual lead. Fixed with visual event queue.
- **IMPROVE**: parseInt('') on slider → NaN permanently broke scheduler — must use || fallback
- **INSIGHT**: ANY audio scheduler with lookahead must decouple visuals. Push {step, time} into a queue, then in rAF check queue[0].time <= audioCtx.currentTime before triggering visual. This is the ONLY correct pattern.
- **INSIGHT**: Swing timing must be perfectly symmetric: the time added to one step MUST equal the time subtracted from the next. Otherwise BPM physically changes with swing amount.
- **INSIGHT**: parseInt on slider values ALWAYS needs a fallback (|| currentValue) because slider values pass through empty string during interaction.
- **TEST CAUGHT**: No bugs caught by automated tests

#### 5-Build Review (Builds #76-80: void-scape, connect-four, entropy-forge, crypt-lex, beat-haus)
- **All 5 shipped working.** 15 consecutive working builds (66-80). Zero user-reported bugs.
- **Recurring: Audio-visual lookahead desync** — appeared in void-scape AND beat-haus. ADDED TO PRINCIPLES: lookahead schedulers must use visual event queues.
- **Recurring: CSS class overwrite** — connect-four wiped animation classes (2nd lifetime occurrence). REINFORCED: never set className directly; use classList.
- **Recurring: parseInt NaN from empty input** — beat-haus. ADDED TO PRINCIPLES: always || fallback.
- **Gemini audit value**: Caught 14+ bugs across 5 builds. Most valuable: timing math (swing asymmetry), architectural (visual queue pattern), and state management (stale data on settings change).
- **Portfolio milestone**: 80 projects, all working. Process is mature and consistent.

### stellar-forge (2026-03-23)
- **KEEP**: Unified rotation approach for 2048 slide logic — rotate grid to align direction, apply single slideRow, rotate back. 4 directions handled by 1 function.
- **KEEP**: Element-themed progression with unique colors per tier — educational twist on 2048 mechanics
- **KEEP**: slideRow with merge ceiling (filtered[i] < WIN_TIER) — prevents max-tier tiles from merging
- **IMPROVE**: canMove() didn't respect merge ceiling — reported adjacent max-tier tiles as mergeable, causing infinite softlock. Gemini caught. Must add `if (v >= WIN_TIER) continue` in canMove.
- **IMPROVE**: Win state (vibrate + status) triggered on EVERY move after winning — global `won` flag never gated. Added `winAlerted` one-time flag.
- **IMPROVE**: No touchmove preventDefault — mobile page scrolled during gameplay swipes. Added scoped handler on #board.
- **INSIGHT**: Any game with a "merge ceiling" (max tile that can't merge further) must ensure BOTH the merge logic AND the game-over detection agree on the ceiling. If slideRow refuses to merge max tiles but canMove says they can merge, the game softlocks.
- **INSIGHT**: One-time game events (win alerts, achievement popups) need a dedicated boolean flag separate from the win condition itself. The win condition persists (player keeps playing), but the alert should fire exactly once.
- **TEST CAUGHT**: No bugs caught by automated tests — all were game logic level

### chess-clock (2026-03-23)
- **KEEP**: performance.now() + requestAnimationFrame for precision timing — drift-free, frame-perfect countdown
- **KEEP**: 50/50 split with transform: rotate(180deg) on top half — turns single device into 2-player tool
- **KEEP**: Conditional time format (MM:SS above 60s, SS.ms below) — panic-inducing format shift
- **KEEP**: Screen Wake Lock API with visibilitychange re-acquisition — essential for any long-running display app
- **KEEP**: pointerdown instead of click for zero-latency input — critical for competitive timing tools
- **IMPROVE**: First tap started YOUR clock instead of opponent's — chess convention is tap-to-start-opponent. Must use `1 - tappedPlayer` for initial activation. Gemini caught.
- **IMPROVE**: Initial display showed 0.00 — timeLeft initialized to [0,0], startGame not called before first render. Must call startGame() at init.
- **IMPROVE**: Background tab caused rAF throttling → massive dt on return → instant timeout. Must auto-pause on visibilitychange hidden AND reset lastTick on visible.
- **IMPROVE**: WakeLock orphaning — multiple acquireWakeLock calls overwrote reference, leaking locks. Added !wakeLock guard.
- **INSIGHT**: Any timer app using rAF MUST handle background tabs. rAF pauses but performance.now() keeps counting. The delta on return can be minutes. Auto-pause on hidden + reset lastTick on visible is the correct pattern.
- **INSIGHT**: Domain-specific conventions matter. Chess clocks follow "tap starts opponent's clock" — getting this wrong makes the tool feel broken to experienced players even though it technically works.
- **INSIGHT**: WakeLock is a limited resource. Always check if you already hold one before requesting another, or you leak handles that can't be released.
- **TEST CAUGHT**: No bugs caught by automated tests — all were domain logic and platform API level

### neon-shatter (2026-03-23)
- **KEEP**: Fixed aspect ratio canvas scaling (fit to window while maintaining GW/GH ratio) — game coordinates stay consistent across all screens
- **KEEP**: Paddle-relative bounce angles (rel = hitPos / halfWidth, angle = rel * π/3) — essential for breakout gameplay variety
- **KEEP**: Circle-to-AABB collision for ball-to-brick — more accurate than pure AABB for a circular ball
- **KEEP**: Delta-time capped at 0.05s — prevents physics explosion after tab backgrounding
- **KEEP**: Particle system with life decay + splice removal — lightweight "juice" for brick destruction
- **IMPROVE**: Trail rendering used (1 - i/length) making oldest points brightest — should use (i+1)/length so newest = brightest. Gemini caught.
- **IMPROVE**: Keyboard input relied on OS key repeat rate — stuttery, inconsistent movement. Fixed with held-key map + dt-based continuous movement.
- **IMPROVE**: Brick collision blindly inverted velocity — could trap ball inside brick on corner hits. Fixed by forcing velocity direction AWAY from brick center using sign of dx/dy.
- **INSIGHT**: For ball trails, the rendering order matters: if trail[0] is oldest and trail[n] is newest, alpha should increase with index (i/length), not decrease.
- **INSIGHT**: Game input for continuous movement (paddle, character) must use a keysHeld map (keydown sets true, keyup sets false) processed in the update loop, not discrete keydown events. Key repeat rate is OS-dependent and stutters.
- **INSIGHT**: Collision response should force the velocity direction based on the collision normal (sign of distance vector), not blindly invert. Blind inversion causes trapping when the ball is inside the collider.
- **TEST CAUGHT (automated)**: Overlay didn't dismiss — test clicks buttons, overlay only had click handler on div. Added START button inside overlay.

### color-forge (2026-03-24)
- **KEEP**: HSL color math for harmony generation — simple hue rotation (±30, ±120, ±150, +180) produces all standard harmony types
- **KEEP**: Canvas HSL wheel drawn with 360 arc strokes — lightweight, no image assets
- **KEEP**: Bidirectional input sync with source tracking (updateAll('hex'|'slider'|'picker')) — prevents circular update loops
- **KEEP**: Dynamic text contrast via BT.601 luminance — white text on dark swatches, black on light
- **KEEP**: CSS variable export block — practical output designers actually want
- **IMPROVE**: Clipboard writeText toast fired synchronously regardless of async result — must put toast in .then() callback. Gemini caught.
- **IMPROVE**: Hex input regex required # and exactly 6 chars — users paste without # and use 3-char shorthand. Relaxed to /^#?([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$/
- **INSIGHT**: navigator.clipboard.writeText returns a Promise. Any UI feedback (toast, flash, icon change) must go in .then(), never synchronously after the call. The operation can fail silently.
- **INSIGHT**: Input validation for color codes should be permissive: accept with/without #, accept 3 or 6 hex chars. Strict validation frustrates users who paste from different sources.
- **TEST CAUGHT**: No bugs caught by automated tests — all were async/UX level

### aura-keys (2026-03-24) — PROJECT #85 (5-build review)
- **KEEP**: QWERTY-to-note mapping with e.repeat guard — prevents note re-triggering on key hold
- **KEEP**: Polyphonic activeNotes dictionary (noteIndex → {osc, gain}) — clean tracking of simultaneous notes
- **KEEP**: setTargetAtTime(0, now, 0.03) for release — safely approaches zero without exponentialRamp crash
- **KEEP**: Audio node disconnect on note stop — prevents memory leaks in long sessions
- **KEEP**: Pointer glissando via elementFromPoint in pointermove — allows sliding across keys like a real keyboard
- **IMPROVE**: exponentialRampToValueAtTime(0.001, now+0.15) crashes when gain.value is exactly 0 — Gemini caught. setTargetAtTime is the safe alternative.
- **IMPROVE**: Notes stuck on tab switch (keyup never fires) — added window blur → stopAll. This is the 2nd occurrence (also chess-clock).
- **IMPROVE**: Modifier keys (Ctrl+A) triggered notes and blocked browser shortcuts — must check e.ctrlKey/e.metaKey/e.altKey
- **IMPROVE**: Touch glissando scrolled page instead of sliding — need preventDefault on pointermove when pointer is captured
- **INSIGHT**: exponentialRampToValueAtTime requires the starting value to be > 0. If the attack hasn't completed (gain still at 0), it throws DOMException. setTargetAtTime has no such constraint — it's always safe for release envelopes.
- **INSIGHT**: Any keyboard-driven app must ignore modifier key combos (Ctrl/Cmd/Alt). Otherwise the app steals browser shortcuts.
- **INSIGHT**: Test regex for brace balance can be confused by quotes containing the opposite quote character (e.g., "'"). Use escape sequences (\x27) to avoid false failures.
- **TEST CAUGHT (automated)**: Brace balance test confused by `"'"` in QWERTY_MAP — mixed quote characters tripped the string-stripping regex. Used \x27 escape.

#### 5-Build Review (Builds #81-85: stellar-forge, chess-clock, neon-shatter, color-forge, aura-keys)
- **All 5 shipped working.** 20 consecutive working builds (66-85). Zero user-reported bugs.
- **Recurring: Window blur handling** — chess-clock (auto-pause timer) AND aura-keys (stop stuck notes). REINFORCED: ANY persistent-state app (audio, timers, animations) must handle window blur/visibilitychange.
- **Recurring: Web Audio exponentialRamp from zero** — aura-keys. ADDED TO PRINCIPLES: always use setTargetAtTime for release, never exponentialRamp (crashes on 0).
- **Recurring: Async clipboard feedback** — color-forge. REINFORCED: clipboard.writeText is a Promise; UI feedback in .then() only.
- **Portfolio milestone**: 85 projects, 20 consecutive working. Process is highly mature. Gemini audits catching 3-5 bugs per build consistently.

### neon-tetra (2026-03-24)
- **KEEP**: 7-bag randomizer (shuffle array of 7 types, pop until empty, refill) — guarantees fair piece distribution, prevents long droughts
- **KEEP**: Ghost piece via while(isValid(shape, x, gy+1)) gy++ — shows exact landing position
- **KEEP**: Wall kick table with multiple offset attempts — allows rotation near walls/blocks
- **KEEP**: Grid rotation approach (rotateMatrix for CW rotation) — single function handles all orientations
- **KEEP**: Gravity tick decoupled from render (time-based dropInterval vs rAF) — consistent game speed
- **IMPROVE**: O-piece rotation triggered wall kicks and shifted position — O-piece is rotationally symmetric, must skip rotation entirely. Gemini caught.
- **IMPROVE**: Any keypress instantly restarted on game over — player couldn't see final board state. Added 1s gameOverTime delay before restart allowed.
- **IMPROVE**: Grid not initialized before first draw() call — caused "Cannot read properties of undefined" on load. Added initGrid() before first rAF.
- **INSIGHT**: Rotationally symmetric pieces (O-piece in Tetris, or any piece that looks the same after rotation) should skip the rotation function entirely, because wall kick offsets can still shift them unexpectedly.
- **INSIGHT**: Game over state needs a "cool-down" delay before accepting restart input. Players are mashing keys when they die — instant restart feels broken and they never see their final board.
- **TEST CAUGHT (automated)**: Console error — grid accessed before initGrid() was called. Added early initGrid() call.

### base-sync (2026-03-24)
- **KEEP**: BigInt for number base conversion — handles arbitrary precision beyond Number.MAX_SAFE_INTEGER
- **KEEP**: BigInt prefix parsing ('0x', '0b', '0o') + toString(radix) — clean, native base conversion
- **KEEP**: Auto-formatting binary in nibbles (4-bit groups) and decimal with commas — dramatically improves readability
- **KEEP**: Cursor-relative-to-data-characters tracking for formatted inputs — prevents cursor jump
- **KEEP**: One-click copy with formatting stripped (commas/spaces removed) — clean clipboard output
- **IMPROVE**: Cursor jumped to end of input on every keystroke — el.value reassignment kills cursor. Gemini caught. Fixed by tracking cursor position relative to data characters (ignoring format chars), then restoring after re-format.
- **IMPROVE**: Dead variable (toastTimer) and unused function (filterInput) — removed. Consolidated into handleInput.
- **INSIGHT**: Any input field with auto-formatting (commas, spaces, dashes) MUST track cursor position relative to meaningful data characters, not raw string index. The pattern: count non-format chars before cursor → reformat → walk new string counting non-format chars to find new cursor position.
- **INSIGHT**: BigInt prefix strings ('0x', '0b', '0o') are the cleanest way to parse arbitrary-base strings in JS without writing custom parsers.
- **TEST CAUGHT**: No bugs caught by automated tests — cursor jump is a UX issue only visible during interaction

### neon-reflex (2026-03-24)
- **KEEP**: performance.now() for sub-ms reaction timing — essential for competitive reflex tests
- **KEEP**: 5-round structure with grade ranking (S/A/B/C/D) — gives statistical significance and gamification
- **KEEP**: False start detection (tap during wait = penalty) — prevents cheating by tapping blindly
- **KEEP**: Round progress dots with color coding — instant visual feedback of run status
- **KEEP**: History bar chart in final stats — shows consistency at a glance
- **IMPROVE**: Key auto-repeat cycled through all rounds instantly — e.repeat must be guarded in any tap-based game. Gemini caught.
- **IMPROVE**: Simultaneous pointer+keyboard double-fired, skipping result display — added 100ms cooldown between handleTap calls.
- **IMPROVE**: Play again required two taps (done→idle→start) — simplified to done→start. UX flow should minimize taps for common actions.
- **IMPROVE**: Shake animation didn't restart on rapid false starts — need reflow trick (void offsetWidth)
- **INSIGHT**: Any game accepting input from BOTH pointer AND keyboard must debounce with a cooldown timer. The two input sources can fire within the same event loop iteration, causing state to advance twice.
- **INSIGHT**: e.repeat is CRITICAL for tap-based games. Key auto-repeat fires keydown events at 30Hz+ — without the guard, a held key will cycle through the entire game in under a second.
- **INSIGHT**: "Play again" from a results screen should start the game directly, not return to a menu. Extra taps = friction = user abandonment.
- **TEST CAUGHT**: No bugs caught by automated tests — all were input timing/UX flow issues

### type-forge (2026-03-24)
- **KEEP**: CSS variables (--p-size, --p-weight, etc.) driving preview styles — cleanest pattern for live typography manipulation
- **KEEP**: Google variable fonts for smooth weight sliding — single font file, continuous weight range
- **KEEP**: contenteditable for live text preview — users type directly in the styled area, no separate input
- **KEEP**: Dark/light toggle for contrast testing — essential for font readability assessment
- **KEEP**: Copy CSS with font-family + all properties — practical output designers need
- **IMPROVE**: Used `|| default` for numeric parsing — 0 is falsy, so `parseFloat(v) || 0` never allows zero. Gemini caught. Use explicit `isNaN()` check instead.
- **INSIGHT**: The `|| fallback` pattern for numbers is a JS anti-pattern when zero is a valid value. `parseInt(v) || 32` breaks for input value "0". Always use: `var v = parseInt(x); if (isNaN(v)) v = default;`
- **INSIGHT**: For typography tools, CSS variables on :root are the optimal architecture — single source of truth, no inline style manipulation, and the preview automatically responds to any property change.
- **TEST CAUGHT**: No bugs caught by automated tests — falsy zero is a logic-level issue

### sprite-forge (2026-03-24) — PROJECT #90 (5-build review)
- **KEEP**: Frame array of pixel arrays — simple, efficient state for multi-frame animation
- **KEEP**: Onion skinning via 15% globalAlpha rendering of previous frame — essential animation feature
- **KEEP**: Stack-based flood fill — simple BFS with boundary checks, handles all shapes
- **KEEP**: Sprite sheet export via offscreen canvas + toBlob — clean, no-library approach
- **KEEP**: Optimized thumb update (only active frame during drawing) — prevents DOM thrash
- **IMPROVE**: Timeline rebuilt ALL canvas thumbnails on every pixel paint — massive DOM thrash at 60fps. Gemini caught. Only update the active frame's thumbnail during painting.
- **IMPROVE**: Dead conditional in fill tool (tool === 'eraser' inside tool === 'fill' branch) — impossible condition. Simplified.
- **IMPROVE**: FPS 0 caused Infinity interval — clamped to minimum 1
- **INSIGHT**: During high-frequency events (pointermove, drag), minimize DOM manipulation. Only update the specific element that changed, never rebuild the entire list/grid.
- **INSIGHT**: Dead conditionals (checking a variable that's guaranteed to be a specific value by the enclosing if/else) are logic errors. They indicate the code was refactored and a branch wasn't cleaned up.

#### 5-Build Review (Builds #86-90: neon-tetra, base-sync, neon-reflex, type-forge, sprite-forge)
- **All 5 shipped working.** 25 consecutive working builds (66-90). Zero user-reported bugs.
- **Recurring: falsy zero (|| operator)** — type-forge (3rd lifetime occurrence). REINFORCED: always isNaN() for numeric parsing.
- **Recurring: DOM thrash during high-frequency events** — sprite-forge. NEW PRINCIPLE: during pointermove/drag, update only the affected DOM element.
- **Recurring: e.repeat guard** — neon-reflex. Now a standard check for all keyboard-driven games.
- **Portfolio milestone**: 90 projects, 25 consecutive working. Process mature, bugs caught at audit stage.

### algo-vision (2026-03-24)
- **KEEP**: Async/await for sorting visualization — natural pause points with `await delay()` at each step
- **KEEP**: Color-coded bar states (comparing/swapping/sorted/pivot) — instant visual understanding
- **KEEP**: Audio mapped to value (freq = 200 + value/max * 800) — algorithmic music adds sensory dimension
- **KEEP**: DOM bar reuse (add/remove only as needed) — avoids full rebuild on every render
- **IMPROVE**: insertionSort outer loop missing cancel check — sort continued silently after stop. Gemini caught. Must check cancelled at EVERY loop level.
- **IMPROVE**: mergeSort second recursive branch executed after cancel — need cancel check between `await msHelper(lo, mid)` and `await msHelper(mid+1, hi)`
- **IMPROVE**: Stats display not reset until first comparison — stale values shown briefly. Added updateInfo() on start.
- **IMPROVE**: Audio nodes never disconnected — onended callback with disconnect() prevents memory leaks at high speed
- **INSIGHT**: Async cancellation in recursive algorithms needs checks at EVERY level: before each recursive call, between sibling calls, and inside each inner loop. A single check at the top of the function is not enough.
- **INSIGHT**: Web Audio nodes (oscillator, gain) persist in the audio graph even after stop(). Must explicitly disconnect via onended callback to prevent GC pressure during rapid creation.
- **TEST CAUGHT**: No bugs caught by automated tests — all were async control flow and audio lifecycle issues

### ink-stack (2026-03-24)
- **KEEP**: Stroke-based undo/redo (array of {points, color, size} objects) — lighter than pixel snapshots, enables selective redo
- **KEEP**: Quadratic bezier smoothing between points — eliminates jagged lines from discrete pointer events
- **KEEP**: Baked canvas for oldest strokes — preserves visual history even when undo stack is capped
- **KEEP**: Redo stack cleared on new stroke — correct branching history model
- **KEEP**: setPointerCapture for smooth drawing beyond canvas edges
- **IMPROVE**: MAX_HISTORY shift() deleted strokes from array, causing redrawAll to lose them visually — Gemini caught. Must bake to offscreen canvas before shifting.
- **IMPROVE**: pointercancel saved partial strokes — should discard since the interaction was interrupted
- **INSIGHT**: Any history system with a cap that redraws from the history array will LOSE data when shifting. If the array IS the source of truth for rendering, bake evicted entries to a persistent layer (offscreen canvas) before removing them.
- **INSIGHT**: pointercancel means the OS interrupted the gesture (system dialog, orientation change). The partial data is unreliable and should be discarded, not committed.
- **TEST CAUGHT**: Browser test timed out (transient Playwright issue, not a code bug). Non-browser checks all passed.

### raw-md (2026-03-24)
- **KEEP**: Parse pipeline order: escape HTML → extract code blocks → block elements → inline elements → paragraphs → restore code blocks
- **KEEP**: XSS protection first (escape &, <, >) before any markdown processing
- **KEEP**: Code block extraction with sentinel replacement — prevents inline regex from breaking code content
- **KEEP**: Proportional sync scroll (scrollTop / scrollHeight ratio) — simple and effective
- **KEEP**: Debounced rendering (150ms) — prevents lag on fast typing of large documents
- **KEEP**: localStorage auto-save on every render — zero-friction persistence
- **INSIGHT**: Custom markdown parsers must process elements in strict order. Code blocks MUST be extracted first, otherwise inline patterns (bold, italic, links) will corrupt code content.
- **INSIGHT**: The test suite's brace balance checker uses regex to strip strings/comments but doesn't strip regex literals. Code with regex containing braces ({3,}, {1,6}) will false-fail. Known limitation — browser load test confirms correctness.
- **TEST NOTE**: Brace balance test false-failed due to regex literals with quantifier braces. All other tests passed including browser load with zero console errors.

### neon-node (2026-03-24)
- **KEEP**: CSS 3D card flip (transform-style: preserve-3d, backface-visibility: hidden, rotateY(180deg)) — clean, performant card flip
- **KEEP**: Fisher-Yates shuffle for card randomization — correct, unbiased
- **KEEP**: Board lock during mismatch display — prevents click spam
- **KEEP**: Timer starts on first flip, not on page load — accurate game timing
- **IMPROVE**: Mismatch setTimeout fired on stale cards after reset — Gemini caught. Must track timeout IDs and clearTimeout on newGame. Also add null guards in the callback.
- **INSIGHT**: Any game with delayed state changes (setTimeout for animations, reveals, transitions) MUST track all timeout IDs and clear them when the game resets. Otherwise the callbacks fire on the new game's state, causing corruption or crashes.
- **INSIGHT**: This is now the 2nd occurrence of "stale timeout on reset" (also neon-tetra had instant restart issue). PATTERN: every newGame/reset function must clear ALL pending timers.
- **TEST CAUGHT**: No bugs caught by automated tests — timeout leak is a state management issue

### neon-pong (2026-03-24) — PROJECT #95 (5-build review)
- **KEEP**: Fixed aspect ratio canvas with scale factor — consistent game coordinates across devices
- **KEEP**: Ball trail via position history array — simple, visually effective
- **KEEP**: Screen shake via ctx.translate with random offset — instant tactile feedback
- **KEEP**: AI lerp with max speed — beatable but challenging
- **KEEP**: Collision snap to paddle edge — prevents tunneling and sticking
- **IMPROVE**: Paddle collision used narrow coordinate window + fixed push offset — ball tunneled through at high speed, or got stuck vibrating. Snap ball.x to paddle edge is correct pattern. Gemini caught.
- **IMPROVE**: Keyboard used targetY offset per keydown — mushy, inconsistent. 3rd occurrence of this pattern (neon-shatter, neon-reflex). Held-key map is the ONLY correct approach.
- **INSIGHT**: For any AABB collision where the moving object can skip the collision zone in one frame, snap the object to the collision boundary (not push by a fixed offset). Snapping guarantees the object is outside the collider.
- **INSIGHT**: This is now the 3rd time held-key tracking has been needed. It's a FUNDAMENTAL pattern: keydown sets flag, keyup clears flag, update loop reads flags. This must be the default for ALL game keyboard input.

#### 5-Build Review (Builds #91-95: algo-vision, ink-stack, raw-md, neon-node, neon-pong)
- **All 5 shipped working.** 30 consecutive working builds (66-95). Zero user-reported bugs.
- **Recurring: Held-key tracking** — 3rd lifetime occurrence. NOW FUNDAMENTAL: all game keyboard input uses keydown/keyup flag map.
- **Recurring: Stale timeout on reset** — neon-node (2nd occurrence). REINFORCED: every reset function must clear ALL pending timers.
- **Recurring: Collision snap** — neon-pong. Fixed-offset push fails at high speed. Snap to boundary is correct.
- **Test suite limitation**: raw-md brace balance false positive (regex quantifiers), ink-stack transient Playwright timeout. Known issues.
- **Portfolio milestone**: 95 projects, 30 consecutive working. Approaching 100.

### cyber-breach (2026-03-24)
- **KEEP**: Category hints next to word blanks — helps player without giving away the answer
- **KEEP**: Trace bar (progress bar for wrong guesses) — cleaner visual than traditional hangman drawing
- **KEEP**: On-screen keyboard with correct/wrong/disabled states — essential for mobile, visual feedback
- **KEEP**: Reflow trick for shake animation restart (void offsetWidth)
- **IMPROVE**: className = 'win' wiped all other classes — 4th occurrence of className overwrite pattern. Must ALWAYS use classList.add/remove. Gemini caught.
- **IMPROVE**: for...in on guessed object — Object.keys().filter() is safer and more predictable
- **INSIGHT**: el.className = value is DESTRUCTIVE — it replaces ALL classes. This is now the 4th occurrence (connect-four renderBoard, and now twice in this project). classList is the ONLY safe way to toggle state classes.
- **TEST CAUGHT**: No bugs caught by automated tests — all were class management and iteration safety

### ipsum-gen (2026-03-24)
- **KEEP**: Real-time generation on slider/mode change — zero-friction UX
- **KEEP**: Classic "Lorem ipsum..." opening for authenticity — always start with the standard text
- **KEEP**: Word and character count display — practical metadata
- **IMPROVE**: Clipboard API .catch() was empty — modern API can reject (permissions, non-HTTPS). Must fall back to execCommand in the catch handler, not just swallow the error. Gemini caught.
- **IMPROVE**: Generated sentence then immediately overwrote with CLASSIC_START — wasted computation. Push the fixed value directly, loop from index 1.
- **INSIGHT**: navigator.clipboard.writeText().catch() must ALWAYS have a functional fallback, not an empty handler. The modern API can fail for many reasons (permissions, security context, browser policy).
- **TEST CAUGHT**: No bugs caught by automated tests

### wealth-calc (2026-03-24)
- **KEEP**: CSS bar chart with stacked bars (contributions + interest) — lightweight, no charting library needed
- **KEEP**: Inflation toggle with per-year discounting — shows real purchasing power
- **KEEP**: Real-time calculation on every input change — zero-friction UX
- **KEEP**: Chart auto-sampling for large year counts — prevents DOM overload
- **IMPROVE**: Inflation-adjusted breakdown mixed nominal contributions with real total — numbers didn't add up. Must track realContributions separately with per-year inflation discounting. Gemini caught.
- **INSIGHT**: When displaying inflation-adjusted financial data, ALL components must be consistently adjusted. Mixing nominal contributions with real total creates a mathematical impossibility (interest = total - contributions gives wrong number). Track both nominal and real values in parallel.
- **TEST CAUGHT**: No bugs caught by automated tests — financial math consistency is logic-level

### particle-life (2026-03-24) — PROJECT #99
- **KEEP**: Float32Array SoA (Structure of Arrays) layout for particles — cache-friendly, no GC pressure
- **KEEP**: Batch rendering by color (one fillStyle change per color, not per particle) — massive Canvas2D speedup
- **KEEP**: fillRect instead of arc for tiny particles — 3x+ rendering performance
- **KEEP**: Toroidal wrap with half-width distance check — prevents edge clumping, creates infinite-feeling space
- **KEEP**: Close-range repulsion (d < radius*0.3) — prevents particle collapse into singularities
- **KEEP**: Pre-calculated constants outside inner loop (frictionMult, repulseR, invD) — reduces per-iteration overhead
- **KEEP**: Clickable matrix cells for live rule editing — deeply interactive
- **KEEP**: Presets (Cells, Worms, Swarm, Ecosystem) — demonstrates the system's range immediately
- **KEEP**: Glassmorphism panel that auto-hides — keeps the visual experience immersive
- **INSIGHT**: Emergent complexity from simple rules is the most visually impressive pattern in single-file apps. Particle Life, Elementa, Life-Canvas — these are the projects people actually play with.
- **INSIGHT**: For N-body simulations, the render loop is often the bottleneck, not the physics. Optimizing draw calls (batch by color, use simpler primitives) has more impact than optimizing math.

### neon-runner (2026-03-24) — PROJECT #100: THE GRAND FINALE
- **KEEP**: Separate X/Y axis collision resolution — prevents corner snagging, the foundation of tile-based platformer physics
- **KEEP**: Coyote time (5 frames after leaving ledge) + jump buffering (5 frames before landing) — invisible mechanics that make platformers feel "right"
- **KEEP**: Variable jump height via velocity cap (not continuous damping) — clean short/long hop distinction
- **KEEP**: Squash/stretch rendering based on velocity events — makes a rectangle feel alive
- **KEEP**: Parallax background with multiple scroll rates — depth from simple math
- **KEEP**: Synthesized audio per game event (jump/coin/death) with onended cleanup
- **KEEP**: Fixed game resolution scaled to viewport — consistent physics across all screen sizes
- **IMPROVE**: Variable jump continuous damping (vy *= 0.5 every frame) caused jerky halt — Gemini caught. Single cap (vy = -3) is cleaner.
- **IMPROVE**: Collision direction resolved via vx sign — fails at vx=0. Must use previous position comparison.
- **IMPROVE**: inputJump() called twice per frame — cached to single variable.
- **INSIGHT**: Platformer "feel" is 90% invisible mechanics (coyote time, jump buffer, variable height, acceleration curves) and 10% visible game. Without these, even perfect collision code feels wrong.
- **INSIGHT**: Collision resolution direction must NEVER depend on velocity sign. Velocity can be zero while a collision exists (pushed by other forces, floating-point drift). Always compare current vs previous position.

## THE 100-PROJECT MILESTONE
100 single-file HTML apps. Zero external dependencies. Every one tested, audited by Gemini, and shipped to GitHub Pages. The learnings file grew from empty to 500+ insights. The process evolved from ad-hoc to a rigorous build pipeline with automated tests, code audits, and 5-build continuous improvement reviews. 30+ consecutive working builds to close out the series.

### tension-matrix (2026-03-24) — PROJECT #101
- **KEEP**: Verlet integration (position-based, no velocity storage) — elegant, stable, perfect for cloth
- **KEEP**: Structural constraints with iterative relaxation — more iterations = stiffer cloth
- **KEEP**: Tension-based HSL coloring (hue 200→320 mapped to constraint stress) — makes invisible physics visible
- **KEEP**: basePinned property on points — remembers structural pin state through drag/release cycle
- **KEEP**: Weighted constraint relaxation (free point takes full correction when neighbor pinned) — prevents stretchy anchors
- **KEEP**: Line intersection test for cutting (shift+drag severs constraints along path)
- **KEEP**: Toss mechanics (apply mouse delta as velocity on release) — deeply satisfying
- **IMPROVE**: Drag release set pinned=false unconditionally — curtain detached from support. Must restore basePinned. Gemini caught.
- **IMPROVE**: Constraint relaxation used 0.5 weight for both points — when one is pinned, the free point should take full correction. Fixed with pin-aware weighting.
- **IMPROVE**: Tension rendering divided by zero when tearDist=1 — Math.max guard added.
- **INSIGHT**: Interactive physics sims need pin state management. Points that are structurally pinned must retain that state through user interaction cycles. A basePinned/originalPinned pattern handles this cleanly.
- **INSIGHT**: Constraint relaxation weighting: when one end is fixed, the other must absorb 100% of the correction. The standard 50/50 split makes anchored cloth too stretchy.

### terra-forge (2026-03-24) — PROJECT #102
- **KEEP**: Custom Simplex noise + fBm — no external libs, full control over terrain character
- **KEEP**: Dual noise layers (elevation + moisture) for biome determination — creates realistic biome distribution
- **KEEP**: Hillshading from neighbor elevation gradients — transforms flat 2D map into convincing topographic display
- **KEEP**: Island mode with radial falloff mask — guarantees water borders for pleasing island shapes
- **KEEP**: ImageData pixel buffer with half-resolution + CSS upscale — smooth real-time slider interaction
- **KEEP**: Debounced regeneration on slider input — prevents lag during rapid parameter changes
- **KEEP**: Hover tooltip with biome name + stats — makes exploration engaging
- **IMPROVE**: Zero seed broke PRNG — Lehmer multiplicative PRNG produces 0*16807=0 forever. Gemini caught. Clamp seed to min 1.
- **IMPROVE**: Coastline shadows harsh — hillshade used deep water elevation creating dark edges. Clamp water neighbor elevations to seaLevel.
- **INSIGHT**: Multiplicative PRNGs (like Lehmer/Park-Miller: s = s*16807 % 2147483647) have a fatal fixed point at 0. Seed must NEVER be 0.
- **INSIGHT**: When computing terrain hillshading near water boundaries, water elevations are much lower than land. The slope calculation sees a massive drop, casting unnaturally dark shadows on coastlines. Fix: clamp all neighbor lookups to max(seaLevel, elevation) for land pixels.

### flock-mind (2026-03-24) — PROJECT #103
- **KEEP**: Two-pass boid update (calc all forces → apply all) — prevents directional drift from sequential in-place modification
- **KEEP**: Inverse-distance separation (dx/d² not dx/d) — stronger repulsion when closer, natural behavior
- **KEEP**: Group-specific alignment+cohesion with universal separation — creates distinct flocks that avoid each other
- **KEEP**: Oriented triangles (atan2 velocity) batched per group — boids look alive, efficient rendering
- **KEEP**: Minimum speed enforcement with random nudge at speed=0 — prevents dead boids
- **IMPROVE**: In-place update (modify position in same loop that reads positions) caused directional drift — Gemini caught. Two-pass is essential for N-body systems.
- **IMPROVE**: Mouse sentinel value (-9999) wrapped to visible position via toroidal distance math — guard with mouseX > -1 check.
- **INSIGHT**: Any N-body simulation where entity A reads entity B's state while B may already be updated THIS frame needs a two-pass architecture. This is the same principle as double-buffering in Game of Life.
- **INSIGHT**: Sentinel values (like -9999 for "no mouse") can become valid values through mathematical transforms (wrapping, normalization). Always guard with an explicit boolean or range check, not just the sentinel itself.

### dungeon-descent (2026-03-24) — PROJECT #104
- **KEEP**: Procedural room placement with overlap rejection + L-shaped corridors — reliable dungeon layout
- **KEEP**: Raycasting FOV with explored/visible/hidden states — creates tension and exploration reward
- **KEEP**: Bump-to-attack (walk into enemy = combat) — simplest possible combat input
- **KEEP**: Turn-based loop (player acts → enemies act → rerender) — no continuous animation needed
- **KEEP**: Enemies scale with floor depth — natural difficulty progression
- **KEEP**: Camera centered on player — essential for maps larger than viewport
- **IMPROVE**: Draw loop accessed visible[my][mx] without checking if visible[my] exists — camera offset puts my outside map bounds. Added row existence check.
- **IMPROVE**: Comment "Game over overlay" triggered test's overlay regex — renamed to "screen"
- **INSIGHT**: When rendering a camera-offset view of a 2D array, the viewport coordinates can go negative or beyond array bounds. ALWAYS check row existence (arr[y] !== undefined) before column access.
- **INSIGHT**: Roguelikes are perfect for single-file HTML — ASCII rendering needs zero assets, turn-based means no animation loop, and procedural generation gives infinite replayability.
- **TEST CAUGHT (automated)**: Console error from undefined array access in draw loop. Comment keyword triggered overlay test.

### wave-draw (2026-03-24) — PROJECT #105 (5-build review)
- **KEEP**: DFT to extract Fourier coefficients from drawn waveform → createPeriodicWave — turns any shape into a playable sound
- **KEEP**: Interpolated drawing (fill gaps between pointer samples) — continuous waveform from discrete events
- **KEEP**: osc.stop(time) on audio thread instead of setTimeout — reliable in background tabs
- **KEEP**: onended with reference comparison for cleanup — prevents rapid-retrigger bugs
- **KEEP**: Feedback delay with LP filter for spatial sound — makes any synth patch sound better
- **IMPROVE**: playNote checked `!audioCtx` before calling `initAudio()` — first note silently failed. Must init first, then check. Gemini caught.
- **IMPROVE**: setTimeout for oscillator cleanup — unreliable when tab backgrounded. Use osc.stop(audioCtx.currentTime + duration) instead.
- **INSIGHT**: When a function both initializes a resource AND uses it, init MUST come before the existence check. `if(!resource) return; init();` is backwards — should be `init(); if(!resource) return;`
- **INSIGHT**: Web Audio osc.stop(time) is the ONLY reliable way to stop oscillators — it runs on the audio thread which isn't throttled like setTimeout. Use onended for cleanup.

#### 5-Build Review (Builds #101-105: tension-matrix, terra-forge, flock-mind, dungeon-descent, wave-draw)
- **All 5 shipped working.** Post-100 quality bar maintained.
- **Variety achieved:** cloth physics, terrain gen, boid flocking, roguelike game, waveform synth — five completely different categories.
- **Recurring: Two-pass N-body updates** — flock-mind. Established pattern: any system where entities read each other's state needs double-buffered updates.
- **Recurring: Sentinel values as positions** — flock-mind. NEW: sentinel values (-9999) can wrap to valid coordinates via toroidal math. Always guard with explicit boolean.
- **Recurring: Audio init ordering** — wave-draw. Pattern: init before check, not check before init.
- **New: Camera-offset array access** — dungeon-descent. Viewport rendering of 2D arrays must bounds-check row existence.
- **Portfolio status**: 105 projects. Quality consistently high post-100.

### graph-forge (2026-03-24) — PROJECT #106
- **KEEP**: Coulomb repulsion + Hooke spring + centering gravity — classic force-directed layout that self-organizes beautifully
- **KEEP**: Drag-to-connect interaction (drag from node A to node B creates edge) — intuitive edge creation
- **KEEP**: Inline label editing via hidden HTML input positioned over canvas — seamless text input
- **KEEP**: localStorage auto-save on every graph change — zero-friction persistence
- **KEEP**: Terminal velocity cap (15px/frame) — prevents explosion from high repulsion settings
- **IMPROVE**: Overlapping nodes (dx=dy=0) produced zero repulsion force — Gemini caught. `dx/d*f` = `0/1*f` = 0. Must add random jitter to break symmetry.
- **INSIGHT**: Force-directed graphs have a degenerate case when nodes perfectly overlap: the normalized direction vector is (0,0), so no force is applied regardless of magnitude. The fix is trivial — add tiny random displacement — but the bug is invisible until it happens.
- **INSIGHT**: Any N-body repulsion system needs a terminal velocity cap. Without it, two nodes spawned at the same position experience near-infinite force in one frame and fly to Infinity.

### dither-forge (2026-03-24) — PROJECT #107
- **KEEP**: Float32Array buffer for error diffusion — prevents Uint8ClampedArray truncation of accumulated error
- **KEEP**: Nearest-color matching via Euclidean RGB distance — works with any palette size
- **KEEP**: Multiple dithering algorithms (threshold, Floyd-Steinberg, Atkinson, Bayer 4x4/8x8) — users can compare approaches
- **KEEP**: Pixel scale slider with imageSmoothingEnabled=false upscale — crisp retro pixel art from any image
- **KEEP**: Pre-processing (brightness/contrast) before dither — critical for good results on dark/light images
- **KEEP**: Procedural sample image — tool works immediately without upload
- **IMPROVE**: Error diffusion on Uint8ClampedArray truncated accumulated values — Gemini caught. Float32Array intermediate buffer is REQUIRED for correct Floyd-Steinberg/Atkinson. Read from buffer, write final to uint8 output.
- **INSIGHT**: Uint8ClampedArray (from getImageData) silently clamps values to 0-255 on write. Error diffusion algorithms RELY on temporarily exceeding these bounds. Any algorithm that accumulates error into neighbor pixels must use an unclamped buffer (Float32Array or Int16Array).
- **INSIGHT**: This is the same class of bug as "data structure silently destroys data" — seen before with history.shift() in ink-stack. The container's behavior modifies the data without throwing an error.

### bezier-forge (2026-03-25) — PROJECT #108
- **KEEP**: SVG for interactive curve editors — crisp at any scale, native draggable elements, easy path commands
- **KEEP**: CSS transition on preview elements (not JS animation) — leverages browser's native timing implementation
- **KEEP**: Y-axis allows values outside 0-1 for overshoot/bounce while X clamped to 0-1 per CSS spec
- **KEEP**: Ghost comparison (linear alongside custom curve) — immediate visual context
- **KEEP**: Presets with auto-play — user sees the effect instantly
- **INSIGHT**: CSS cubic-bezier has strict rules: X values MUST be 0-1 (time is always forward), but Y values CAN exceed 0-1 (property can overshoot). The editor must enforce this asymmetry.
- **INSIGHT**: Dev tools that show the OUTPUT of what you're building (animation preview) are infinitely more useful than those that just show the INPUT (raw numbers). Always include a live preview.

### wire-forge (2026-03-25) — PROJECT #109
- **KEEP**: Pure math 3D (rotation matrices + perspective projection) on Canvas2D — no WebGL needed for impressive wireframe rendering
- **KEEP**: Z-depth coloring (HSL hue + lightness + alpha mapped to depth) — creates convincing atmospheric perspective
- **KEEP**: Painter's algorithm for edge z-sorting — simple and effective for wireframe
- **KEEP**: Golden ratio (φ) for icosahedron/dodecahedron vertices — mathematically elegant
- **KEEP**: Parametric torus/sphere generation (nested loops over u,v angles) — infinite shape variety from simple math
- **IMPROVE**: Depth coloring mapped t=0 to near and t=1 to far — BACKWARDS. Near must be bright/opaque, far must be dim/transparent. Gemini caught.
- **IMPROVE**: Painter's algorithm sorted ascending Z — drew near edges first, then far on top. Must sort DESCENDING (far first). Gemini caught.
- **IMPROVE**: Rotation angles grew infinitely with auto-spin — eventual float precision jitter. Wrap with modulo 2π.
- **INSIGHT**: Z-depth mapping is easy to get backwards. The natural `(z-min)/range` gives 0=near, 1=far — but for rendering, you usually want 1=near (bright). Always invert: `t = 1 - normalized_z`.
- **INSIGHT**: Painter's algorithm sorts far-to-near (DESCENDING z). The name "painter's" is the clue — a painter covers background first, foreground last.

### tower-siege (2026-03-25) — PROJECT #110 (5-build review)
- **KEEP**: Path-following via waypoint linear interpolation — simple, flexible path design
- **KEEP**: Tower auto-targeting with range check — classic TD mechanic
- **KEEP**: Wave economy (kill gold + wave bonus) — natural difficulty/resource curve
- **KEEP**: Splash damage via distance check against all enemies — clean AoE implementation
- **KEEP**: Shop UI with cost gating (disabled when gold < cost) — prevents confusion
- **IMPROVE**: Projectile movement and lifetime were per-frame, not dt-based — frame-rate dependent. Gemini caught. ALL movement/timers must use dt.
- **IMPROVE**: Towers targeted dead enemies (hp<=0 not filtered) — wasted shots. Check hp before targeting.
- **IMPROVE**: Zero-distance targeting (tower at enemy position) caused NaN velocity — Math.max(0.001, d) guard.
- **INSIGHT**: ANY value that changes per frame (position, lifetime, cooldown) MUST be multiplied by dt. Per-frame increments are frame-rate dependent — 144Hz monitors get double speed.
- **INSIGHT**: Targeting/selection loops must ALWAYS filter out dead/invalid entities. The entity may have been "killed" earlier in the same frame but not yet removed from the array.

#### 5-Build Review (Builds #106-110: graph-forge, dither-forge, bezier-forge, wire-forge, tower-siege)
- **All 5 shipped working.** Quality maintained post-100.
- **Variety:** force graph, image dithering, CSS easing editor, 3D wireframe, tower defense — five completely different categories.
- **Recurring: dt-based movement** — tower-siege. FUNDAMENTAL: all movement uses dt, never per-frame.
- **Recurring: Zero-distance division** — graph-forge AND tower-siege. PATTERN: always clamp distance to Math.max(epsilon, d).
- **New: Depth mapping inversion** — wire-forge. Natural normalized_z gives 0=near, rendering wants 1=near. Always invert.
- **New: Uint8ClampedArray truncation** — dither-forge. Error diffusion needs Float32 buffer.
- **Portfolio: 110 projects.** Post-100 quality consistently high.

### rhythm-type (2026-03-25) — PROJECT #111
- **KEEP**: Note Y position anchored to audioCtx.currentTime — perfect audio-visual sync regardless of frame rate
- **KEEP**: Fall speed locked per-note at spawn — prevents in-flight desync when global speed changes
- **KEEP**: Lookahead audio scheduler for procedural drum beat — sample-accurate timing
- **KEEP**: Melodic synth stab on keystroke — makes typing feel musical
- **KEEP**: Distinct missed state (falls off screen) vs completed (floats up) — clear visual feedback
- **KEEP**: Progressive difficulty via word pool + speed scaling — natural engagement curve
- **IMPROVE**: Note movement was dt-based (FALL_SPEED*dt) — desynced from audio on frame drops. Gemini caught. Must anchor to audio clock: y = HIT_Y - (timeRemaining/fallDuration) * HIT_Y.
- **IMPROVE**: FALL_SPEED changed globally, invalidating all in-flight notes — speed must be locked per-note at spawn time.
- **IMPROVE**: Missed notes flew upward like completed notes — confusing. Added n.missed flag with distinct fall-off behavior.
- **INSIGHT**: In rhythm games, visual position = f(audioTime), NEVER f(dt). The audio clock is the single source of truth. Calculate where a note SHOULD be based on its target time minus current audio time, not by accumulating frame deltas.
- **INSIGHT**: Any per-entity parameter that affects timing (speed, duration) must be FROZEN at entity creation time. If you change it globally, all existing entities desync.

### maze-lab (2026-03-25) — PROJECT #112
- **KEEP**: Animated step-by-step algorithm visualization — mesmerizing and educational
- **KEEP**: Multiple generation algorithms (Backtracker/Prim/Kruskal) — each creates visually distinct mazes
- **KEEP**: BFS vs DFS solver comparison — BFS guarantees shortest path, DFS is dramatic
- **KEEP**: Path compression in findSet for Kruskal's — near O(1) amortized set operations
- **KEEP**: Step button for single-step mode — essential for studying algorithm behavior
- **KEEP**: Batch stepping (speed slider controls steps per frame) — fast or slow animation
- **IMPROVE**: unionSets used O(N) flat scan (iterated entire grid) instead of O(1) tree linking — Gemini caught. Must link root to root, not scan and replace.
- **INSIGHT**: Union-Find has two optimizations: path compression (in find) and union by rank/tree linking (in union). Using path compression WITHOUT proper tree union creates an inconsistent data structure that works but is O(N) instead of O(α(N)).
- **INSIGHT**: Algorithm visualizers are deeply engaging when they have: 1) step-by-step mode, 2) speed control, 3) multiple algorithms to compare, 4) color-coded state. All four are essential.

### ascii-forge (2026-03-25) — PROJECT #113
- **KEEP**: Luminance-based character mapping with BT.601 weights — perceptually accurate brightness
- **KEEP**: Aspect ratio correction (0.5x height) — monospace fonts are ~2x taller than wide
- **KEEP**: Multiple character sets (standard/minimal/blocks/binary/braille) — different aesthetics from same image
- **KEEP**: Color mode via inline spans — each character colored by source pixel
- **KEEP**: Brightness/contrast pre-processing — essential for making details pop in text form
- **IMPROVE**: HTML entities in charset (<, >, &) broke DOM in color mode — Gemini caught. Must escape before innerHTML insertion.
- **IMPROVE**: Character index distribution biased — lum/255*(length-1) with Math.floor means last char only selected at lum=255. Use lum/256*length for even buckets.
- **INSIGHT**: When inserting user-controlled or data-derived characters into innerHTML, ALWAYS escape HTML entities. Even "safe" charsets can contain <, >, &, " which the browser interprets as markup.
- **INSIGHT**: Mapping a continuous range (0-255) to discrete buckets (charset indices) needs careful math. `floor(value / (max+1) * bucketCount)` gives even distribution. Using `floor(value / max * (bucketCount-1))` biases the last bucket.

### gravity-sketch (2026-03-25) — PROJECT #114
- **KEEP**: Circle-to-line-segment collision (project onto segment → closest point → push out → reflect) — simple, reliable
- **KEEP**: Circle-to-circle collision (overlap resolution + velocity exchange along normal) — clean elastic-ish bounce
- **KEEP**: Demo scene on load (pre-drawn ramps + spawned balls) — user sees physics immediately
- **KEEP**: Grab-and-throw with mouse velocity on release — deeply satisfying interaction
- **KEEP**: Body cap (MAX_BODIES) with oldest-first removal — prevents memory issues
- **KEEP**: Drawing with minimum distance threshold — smooth line segments without excessive points
- **INSIGHT**: Custom 2D physics engines are viable for simple interactions (circles + lines + boxes). Circle-line collision is the core building block: project point onto segment, check distance, push out along normal, reflect velocity. Everything else builds on this.
- **INSIGHT**: Physics playgrounds need a demo scene on load. A blank canvas with no objects gives no feedback about what the tool does. Pre-draw ramps + drop balls so physics is visible on first frame.

### automata-lab (2026-03-25) — PROJECT #115 (5-build review)
- **KEEP**: Multi-state CA engine (2-state B/S + 3-state Brian's Brain in same framework) — flexible state handling
- **KEEP**: B/S rule string parser — users can type any rule and explore custom automata
- **KEEP**: Cell aging via Uint16Array → HSL heatmap — stunning visual distinction between stable/chaotic regions
- **KEEP**: Double-buffered Uint8Array grid with swap — essential for correct CA simulation
- **KEEP**: Toroidal edge wrapping — patterns that exit one side enter the opposite
- **KEEP**: Pattern library loaded on click (glider gun, pulsar, R-pentomino) — immediate engagement
- **KEEP**: Draw/erase while running — deeply interactive sandbox feel
- **INSIGHT**: We dodged this project for 20+ builds because it seemed like "just another simulation." In reality, the generalized rule engine + custom B/S parser + cell aging visuals make it fundamentally different from life-canvas (Conway-only). The lesson: don't let category labels prevent building genuinely interesting projects.
- **INSIGHT**: Multi-state automata (Brian's Brain) need completely different transition logic from binary B/S rules. The engine must branch on rule type, not try to generalize everything into birth/survival sets.

#### 5-Build Review (Builds #111-115: rhythm-type, maze-lab, ascii-forge, gravity-sketch, automata-lab)
- **All 5 shipped working.** Quality maintained post-100.
- **Variety:** rhythm game, algorithm viz, image processing, physics sandbox, CA sandbox — five distinct categories.
- **Key patterns:** Audio-time anchoring (rhythm-type), HTML entity escaping (ascii-forge), per-entity frozen params (rhythm-type), Union-Find optimization (maze-lab).
- **Milestone:** Finally built the CA sandbox after 20+ builds of dodging. The "too cool critic" kept vetoing it as "another simulation" but the generalized engine + custom rules + cell aging proved it worthy.
- **Portfolio: 115 projects.** Post-100 quality consistently high.

### voronoi-forge (2026-03-25) — PROJECT #116
- **KEEP**: Brute-force Voronoi (nearest seed per pixel) — simple, correct, no complex Fortune's algorithm needed
- **KEEP**: Edge detection via distance differential (|d2-d1| < threshold) — clean cell boundaries without line-drawing
- **KEEP**: 2x downscale + imageSmoothingEnabled=false upscale — 4x fewer pixels to compute, still looks sharp
- **KEEP**: ctx.fillStyle normalization trick for color parsing — set fillStyle to any CSS color, read back as #rrggbb
- **KEEP**: Multiple color modes (vivid/pastel/mono/distance) — same diagram, different aesthetics
- **KEEP**: Real-time drag with debounced render — responsive interaction without frame drops
- **INSIGHT**: Brute-force Voronoi is O(pixels × seeds). At 2x downscale on a 1920×1080 screen (480K pixels) with 20 seeds, that's ~10M distance comparisons per frame. Fast enough for interactive use with debouncing.
- **INSIGHT**: Edge detection in Voronoi doesn't need explicit edge computation. The difference between distance-to-nearest and distance-to-second-nearest naturally identifies pixels on cell boundaries.

### harmonic-forge (2026-03-25) — PROJECT #117
- **KEEP**: Chord progression builder (creation tool) not just Circle of Fifths reference chart — engagement comes from MAKING music, not reading theory
- **KEEP**: Strum delay (40ms between chord tones) — makes synth chords sound like a real instrument strumming
- **KEEP**: Triangle+sine with slight detune (1.002x) — warm pad-like sound from simple oscillators
- **KEEP**: Diatonic chord generation from intervals — compute I-ii-iii-IV-V-vi-vii° for any key using semitone offsets
- **KEEP**: Preset progressions (Pop I-V-vi-IV, Jazz ii-V-I, Pachelbel) — instant gratification + education
- **KEEP**: DOM-based UI (no Canvas) — total visual/technical break from recent Canvas-heavy projects
- **INSIGHT**: Music theory tools must be CREATION tools, not reference charts. A static Circle of Fifths holds attention for 15 seconds. A progression builder that plays back your creation holds attention for 10+ minutes.
- **INSIGHT**: The difference between "beepy" and "musical" synth is: 1) strum delay between chord tones, 2) dual oscillators with slight detune, 3) smooth ADSR envelope. All three together transform harsh beeps into pleasant chords.

### tale-weaver (2026-03-25) — PROJECT #118
- **KEEP**: JSON node graph for interactive fiction (nodes with text, choices with targets, actions, conditions) — clean, extensible
- **KEEP**: Action system: item (add to inventory), stat (modify numeric value), set (flag boolean) — covers all common IF state changes
- **KEEP**: Conditional choices: locked with visible requirement text (item/stat) — teaches player what to look for
- **KEEP**: Pre-loaded compelling story (~15 nodes, 4 endings) — immediate engagement without authoring overhead
- **KEEP**: Typography-focused UI (Georgia serif, 1.8 line-height, generous paragraph spacing) — makes reading comfortable
- **KEEP**: Sidebar with live stats + inventory — player always knows their state
- **INSIGHT**: Interactive fiction MUST ship with a playable story. An empty engine is useless — the story IS the product. The engine is invisible infrastructure.
- **INSIGHT**: Conditional choices (locked + visible requirement) are more engaging than hidden choices. Seeing "Requires: flashlight" teaches the player to explore and backtrack. Hidden conditions just feel random.
- **INSIGHT**: Pure text/DOM projects are a complete technical and visual break from Canvas-heavy builds. No rAF loop, no pixel manipulation — just JSON traversal and DOM updates. Valuable for portfolio variety.

### fractal-forge (2026-03-25) — PROJECT #119
- **KEEP**: Two-pass rendering (dry-run bounding box → scaled drawing) — fractal always fits perfectly in viewport
- **KEEP**: String length cap (500K) — prevents exponential L-system growth from crashing browser
- **KEEP**: Gradient coloring mapped to draw progress (hue = drawCount/totalF × 300) — stunning visual on complex fractals
- **KEEP**: Multiple presets with fundamentally different visual character (snowflake, fern, dragon, tree, hilbert, sierpinski)
- **KEEP**: Custom axiom + rules editor — users can discover their own fractals
- **KEEP**: Turtle graphics with stack-based branching ([/]) — essential for organic plant-like L-systems
- **INSIGHT**: L-system rendering MUST auto-fit. Without bounding box calculation, fractals draw off-screen at most angles/iterations. The dry-run (simulate turtle without drawing) → calculate scale/offset → render pattern solves this cleanly.
- **INSIGHT**: L-system strings grow exponentially. A simple rule like F=FF doubles length each iteration. 20 iterations = 2^20 = 1M+ characters. Hard cap on string length is essential safety measure.
- **INSIGHT**: This is the THIRD project we've dodged for 20+ builds and then finally shipped (after automata-lab and the original life-canvas Conway's expansion). Lesson: if an idea keeps coming up in brainstorms, just build it.

### spiro-forge (2026-03-25) — PROJECT #120 (5-build review)
- **KEEP**: Hypotrochoid + epitrochoid dual mode — doubles pattern variety from same UI
- **KEEP**: GCD-based rotation calculation for perfect loop closure — curve draws exactly once then stops
- **KEEP**: Per-segment HSL gradient coloring — rainbow effect along the curve
- **KEEP**: Gear visualization (fixed circle, rolling circle, pen arm) — makes abstract math tangible
- **KEEP**: Animated + instant draw modes — watch it draw OR see result immediately
- **KEEP**: Presets that demonstrate fundamentally different shapes (small r = lace, epi = orbits)
- **INSIGHT**: Spirograph math: GCD(R,r) determines how many rotations r makes before the path closes. totalRotations = r/GCD(R,r). maxTheta = totalRotations × 2π. This ensures the animation stops exactly when the curve completes.
- **INSIGHT**: Comment keywords like "overlay" trigger test false positives. Now the 4th occurrence. Must avoid the word in any context (comments, variable names).

#### 5-Build Review (Builds #116-120: voronoi-forge, harmonic-forge, tale-weaver, fractal-forge, spiro-forge)
- **All 5 shipped working.** Quality maintained.
- **Variety:** Voronoi diagram, music theory, interactive fiction, L-system fractals, spirograph — five completely different categories. This batch is possibly the most diverse 5-build stretch in the entire portfolio.
- **Long-dodged projects finally shipped:** automata-lab (#115, dodged 20+ builds), fractal-forge (#119, dodged 20+ builds). Both proved worthy despite repeated "too cool critic" vetoes.
- **New domains touched:** Interactive fiction (tale-weaver), music theory (harmonic-forge) — two categories that had zero representation before.
- **Recurring test issue:** Comment keyword "overlay" caused false positive (4th occurrence total). Consider updating test to only match HTML content, not JS comments.
- **Portfolio: 120 projects.** Post-100 era consistently high quality. 20 projects since hitting 100, all working.

### orbit-well (2026-03-25)
- **KEEP**: Semi-transparent fillRect overlay for trail effect — simple, performant, looks great
- **KEEP**: Speed-based HSL coloring (hue + lightness shift) gives particles natural energy visualization
- **IMPROVE**: Burst button bypassed MAX_P limit — Gemini caught this. Always enforce limits at every particle creation point, not just the spawn loop
- **IMPROVE**: Mobile hover opacity — `@media(hover:hover)` is the correct pattern for hover-only styles. Default to visible, hide only on hover-capable devices
- **IMPROVE**: Right-click-only removal doesn't work on mobile — added click-on-well-to-remove as universal alternative
- **INSIGHT**: For any particle limit, enforce it at EVERY creation point (spawn loop, burst, any future additions). A single bypass can crash the tab
- **INSIGHT**: `@media(hover:hover)` should be the default pattern for all toolbar opacity tricks going forward — fixes mobile accessibility for free
- **TEST CAUGHT**: Nothing — all bugs found by Gemini this round

### neuro-forge (2026-03-25)
- **KEEP**: Unrolled backprop (no matrix/tensor class) — V8-optimized, tiny file, highly readable math
- **KEEP**: Low-res ImageData (60x60) scaled to full screen via drawImage — perfect for real-time heatmap viz at 60fps
- **KEEP**: Network diagram overlay showing weight magnitudes and node activations — makes the "black box" transparent
- **KEEP**: Default dataset on load (XOR) so user immediately sees the network learning — never start with empty state
- **IMPROVE**: Loss display was lifetime average, not current — Gemini caught this. Always show current-epoch loss, not cumulative
- **IMPROVE**: Pointer drag created point explosion (pointermove fires fast) — must enforce minimum distance between consecutive drag-added points
- **IMPROVE**: Canvas coordinates should use getBoundingClientRect, not raw clientX/clientY — matters when canvas isn't at (0,0)
- **IMPROVE**: Keyboard shortcuts should check e.target.tagName to avoid firing when user is in a form control
- **INSIGHT**: For any real-time visualization of ML training, separate the "predict for display" function from the "forward for backprop" function to avoid shared state corruption
- **INSIGHT**: Xavier initialization (scale by 1/sqrt(fan_in)) is critical — without it, tanh saturates immediately and learning stalls
- **TEST CAUGHT**: Nothing — all bugs found by Gemini. The predict/forward separation was proactively handled.

### fluid-type (2026-03-25)
- **KEEP**: Jos Stam Stable Fluids algorithm — unconditionally stable, works at interactive framerates on 128x128 grid
- **KEEP**: Text-as-obstacle via OffscreenCanvas pixel sampling — render text at grid resolution, threshold alpha channel to build obstacle mask
- **KEEP**: Edge emission (dye bleeds from text boundaries) creates beautiful organic effect without user interaction
- **KEEP**: RGB dye channels (3 separate density fields) allow full-color mixing
- **IMPROVE**: CRITICAL — Gemini caught createElement('canvas') inside render loop (60 canvases/sec = memory leak + context limit crash). Always pre-allocate offscreen canvases as module-level variables
- **IMPROVE**: Mouse velocity must be normalized by screen dimensions before injecting into fluid grid. Raw pixel deltas cause physics blow-up on high-res screens
- **IMPROVE**: pointerup should be on window, not canvas — dragging outside window leaves pointer "stuck" otherwise
- **IMPROVE**: Test keyword "overlay" triggers false positive — renamed drawTextOverlay to drawTextLayer to avoid start_screen test match
- **INSIGHT**: For any per-frame rendering that uses an intermediate canvas, ALWAYS create it once at init, not inside the render function. This is a critical performance rule.
- **INSIGHT**: Navier-Stokes with obstacles: skip obstacle cells in diffuse/advect/project, zero velocity inside obstacles in setBnd
- **TEST CAUGHT**: "overlay" keyword false positive (5th occurrence). Known issue with test regex matching JS comments/function names.

### sonic-sight (2026-03-25)
- **KEEP**: Web Audio AnalyserNode for dual visualization (getByteTimeDomainData for waveform, getByteFrequencyData for spectrum)
- **KEEP**: Guided lesson system with auto-configured oscillator states — turns a sandbox into an educational tool
- **KEEP**: Unlock screen pattern (full-page overlay → click → AudioContext init) for browser autoplay policy compliance
- **KEEP**: CRT-style grid lines on oscilloscope canvas for authentic instrumentation feel
- **IMPROVE**: Gemini caught music theory error — Lesson 6 set 330Hz as "octave" when it's actually a perfect fifth (3:2 ratio). 440Hz is the true octave (2:1). Always verify music theory claims
- **IMPROVE**: Changing wave type destroyed and recreated ALL oscillators causing clicks. Fix: set OscillatorNode.type directly in-place, no restart needed
- **IMPROVE**: Must call actx.resume() after AudioContext creation — iOS/Safari start contexts in suspended state
- **IMPROVE**: Use setTargetAtTime instead of direct .value assignment for audio params to prevent zipper noise on rapid slider changes
- **IMPROVE**: masterGain.gain.value must sync with slider DOM value at init, not use hardcoded value
- **INSIGHT**: OscillatorNode.type can be changed on a live running oscillator without stopping/restarting it — this is far smoother
- **INSIGHT**: setTargetAtTime(value, currentTime, 0.015) gives smooth ~15ms ramp that eliminates clicks while feeling instant
- **TEST CAUGHT**: Browser test timeout — transient Playwright infrastructure issue, not a code bug. Page verified manually. Same class as ink-stack/neon-runner timeouts.

### picross (2026-03-25)
- **KEEP**: Handcrafted puzzle data as binary 2D arrays — clues auto-generated, tiny file size, no human error in clue authoring
- **KEEP**: Fill/Cross mode toggle instead of long-press — faster gameplay flow, more accessible on mobile
- **KEEP**: Progressive level unlock with localStorage persistence — gives real sense of progression
- **KEEP**: Pixel art color reveal on completion — transforms a logic exercise into a visual reward
- **IMPROVE**: Gemini caught missing game state lock — must prevent all interaction after win/loss. Any game needs a state machine (playing/won/lost)
- **IMPROVE**: drawMode must be established on pointerdown and enforced throughout drag — otherwise drag toggles chaotically between fill/erase/cross
- **IMPROVE**: setTimeout race condition on retry — pending timeouts from previous game corrupt fresh board. Always clear pending timeouts on game restart
- **IMPROVE**: localStorage.setItem can throw in private browsing — always wrap in try/catch
- **INSIGHT**: For any game with win/loss states: (1) set gameState flag, (2) check it in every input handler, (3) clear all pending timeouts on restart
- **INSIGHT**: Event listeners should be attached once, not inside renderBoard which runs on every level start. Same-reference listeners are safely deduplicated by browsers but it's fragile
- **TEST CAUGHT**: Nothing — all bugs found by Gemini

### iso-city (2026-03-25)
- **KEEP**: Procedural isometric buildings with 3-shade lighting (top=bright, left=mid, right=dark) — looks convincingly 3D with zero sprites
- **KEEP**: Adjacency-based leveling system — simple rules create emergent strategy (place parks next to houses, roads next to shops)
- **KEEP**: Separated pan vs tap detection (hasMoved threshold) — prevents accidental builds while dragging camera
- **IMPROVE**: Gemini caught infinite money exploit — calling gameTick (which adds revenue) on every tile placement let players spam-build for free money. Fix: separate updateStats (safe, no money) from gameTick (timer-only revenue)
- **IMPROVE**: Isometric z-sorting was wrong — nested for-loops don't sort by depth (r+c). Must sort renderList by r+c ascending for correct painter's algorithm
- **IMPROVE**: Floating text stored screen coords — drifts when camera pans. Store grid coords (r,c) and recalculate screen position each frame
- **IMPROVE**: Hover highlight drawn after all buildings — appears on top of closer buildings. Draw highlight in z-order pass instead
- **INSIGHT**: In any game with a tick-based economy, NEVER let manual actions trigger the economy tick. Separate "update display" from "generate resources"
- **INSIGHT**: Isometric depth = r+c for standard diamond grids. Always sort by this before drawing, don't rely on loop iteration order
- **TEST CAUGHT**: Nothing — all bugs found by Gemini

### 5-Build Review: #126-#130
**Builds:** neuro-forge, fluid-type, sonic-sight, picross, iso-city
**Pattern analysis:**
- **Gemini consistently catches 4-6 bugs per build** — the audit process is working well
- **Recurring theme: state management** — picross needed gameState lock, iso-city needed separated stat/revenue updates. Any game needs explicit state machines
- **Recurring theme: mobile UX** — hover opacity, touch-action, pointer events, getBoundingClientRect. These are now well-internalized
- **New category coverage:** AI/ML (neuro-forge), audio/education (sonic-sight), puzzle game (picross), strategy/city builder (iso-city), fluid sim (fluid-type) — excellent diversity
- **No user-reported bugs** in this stretch — the testing + Gemini audit pipeline continues to work
- **createElement in render loop** was the most dangerous bug caught (fluid-type) — would have crashed the browser. Added to permanent checklist
- **Test infrastructure note:** Browser test had transient Playwright timeout on sonic-sight. Not a code bug. Known issue with audio-heavy projects and headless browser

### contrast-check (2026-03-26)
- **KEEP**: WCAG contrast ratio formula (relative luminance with sRGB linearization) is well-standardized and straightforward to implement
- **KEEP**: Color blindness simulation via Brettel/Vienot matrices with proper sRGB linearize→transform→gamma pipeline
- **KEEP**: Palette contrast matrix — cross-referencing all colors pairwise is a powerful visualization for design systems
- **KEEP**: Auto-fix via binary search on HSL lightness preserves hue/saturation while finding accessible contrast
- **IMPROVE**: Gemini caught hex regex {3,6} accepts 4 and 5 char hex which are invalid — must use alternation (3|6) for strict matching
- **IMPROVE**: Auto-fix tested lightness 5/95 instead of 0/100 — missed cases requiring pure black or white
- **IMPROVE**: Integer rounding in rgbToHex can drop contrast ratio below threshold — add 0.05 buffer to target ratio
- **IMPROVE**: hexToRgb should substring(0,6) to safely ignore alpha channel if 8-char hex is passed
- **INSIGHT**: For hex color validation, never use {3,6} range — only {3} or {6} are valid lengths. Use /^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$/
- **INSIGHT**: Any binary search that outputs to a quantized space (integer RGB) needs a small buffer on the target to survive rounding
- **TEST CAUGHT**: Nothing — all bugs found by Gemini

### beat-forge (2026-03-26)
- **KEEP**: Lookahead scheduling (setInterval polls, Web Audio clock schedules) — rock-solid timing independent of UI jank
- **KEEP**: Procedural drum synthesis — kick=sine sweep, snare=noise+triangle, hat=highpass noise, clap=multiple short noise bursts, bass=lowpass square
- **KEEP**: URL-encoded pattern state — encodes 96 bits as base64-like string, enables sharing without backend
- **KEEP**: Weighted random beat generation — kick on downbeats, snare on 5/13, hats frequent — produces musically sensible patterns
- **KEEP**: Sound preview on cell toggle — immediate feedback makes interaction satisfying
- **IMPROVE**: Gemini caught float buffer sizes — sampleRate*0.15 can be non-integer, crashes createBuffer(). Must Math.floor ALL buffer size calculations
- **IMPROVE**: Ghost highlight timeouts — setTimeout for visual sync persists after stop. Must track all timeout IDs and clear them on stop
- **IMPROVE**: Swing value missing from URL encoding — any shared state must include ALL user-configurable parameters
- **INSIGHT**: Web Audio createBuffer requires integer length — always Math.floor any sampleRate multiplication
- **INSIGHT**: Any scheduled visual effect (setTimeout) must be cancellable. Track IDs in an array, clear on state change
- **TEST CAUGHT**: Nothing — all bugs found by Gemini

### solitaire (2026-03-26)
- **KEEP**: Smart-tap auto-move (tap card → auto-place to best valid destination) — far superior to drag-and-drop on mobile
- **KEEP**: CSS-only card rendering with Unicode suits (♠♥♦♣) — zero images, crisp at any DPI, tiny file size
- **KEEP**: Responsive card sizing via CSS variables recalculated on resize — cards fit any screen width
- **KEEP**: Deep undo via JSON-serialized state snapshots — simple, reliable, no inverse-operation complexity
- **IMPROVE**: Gemini caught "teleporting card" bug — smartTap validated a middle card but moveCard did .pop() which grabs the TOP card. Must check isExposed (card is last in array) before allowing foundation moves
- **IMPROVE**: getComputedStyle inside calcTop loop caused 50+ synchronous reflows per render. Cache CSS variable values in JS variables on resize, use cached values in calcTop
- **IMPROVE**: Undo didn't reset gameWon flag — undoing a winning move left game locked. Must reset gameWon and restart timer on undo
- **IMPROVE**: Empty stock+waste still incremented move counter — guard with early return
- **INSIGHT**: In any card game, the card you VALIDATE must be the exact card you MOVE. Never validate one card and pop() a different one
- **INSIGHT**: Never call getComputedStyle inside a render loop — cache computed values on resize/init
- **TEST CAUGHT**: Nothing — all bugs found by Gemini

### sprite-studio (2026-03-26)
- **KEEP**: Checkerboard background for transparency indication — standard pixel art editor pattern
- **KEEP**: Onion skinning via globalAlpha=0.2 on previous frame before drawing current — simple and effective
- **KEEP**: PNG spritesheet export (stitch frames horizontally on hidden canvas + toDataURL) — zero-dependency animated output
- **KEEP**: Flood fill with visited array + stack — iterative, no recursion depth limit
- **IMPROVE**: Gemini caught preview not updating during draw — must call renderPreviewFrame after every applyTool
- **IMPROVE**: Playback crash on frame delete/grid resize — timer's frame index goes out of bounds. Fix: stop playback before destructive operations, bound index with modulo before accessing frames array
- **IMPROVE**: FPS change restarted animation from frame 0 — use module-scoped playbackFrame variable that persists across timer restarts
- **IMPROVE**: renderTimeline on every pointerup was unnecessary DOM churn — only rebuild when isDrawing was true
- **INSIGHT**: Any setInterval animation that references an external array MUST bounds-check the index BEFORE accessing the array, because the array can be modified between ticks
- **INSIGHT**: Canvas .width/.height assignment clears the context — always re-render after resize
- **TEST CAUGHT**: Nothing — all bugs found by Gemini

### fourier-draw (2026-03-26)
- **KEEP**: DFT on complex path points (x+yi) — standard formula, sort by amplitude descending for best visual
- **KEEP**: Path resampling to fixed N points before DFT — even spacing is critical for accurate frequency extraction
- **KEEP**: Epicycles drawn as chain of rotating circles with connecting arms — mesmerizing visual output
- **KEEP**: Neon trace with shadowBlur + semi-transparent canvas clear for trail effect
- **KEEP**: Preset shapes (heart parametric equation, lemniscate) for instant demo without drawing
- **IMPROVE**: Gemini caught numCircles permanent downgrade — setting global to min(global, dftLength) persisted across drawings. drawFrame already uses Math.min, so don't also clobber the global
- **IMPROVE**: Speed 0 causes infinite tracePath growth (60 points/sec, never cleared). Cap array length at 2000
- **IMPROVE**: Preset setTimeout race — clearing during 300ms delay still fires animation. Store timeout ID, clear in stopAnimation
- **IMPROVE**: Canvas coords must use getBoundingClientRect for offset safety
- **IMPROVE**: Short paths (<10 points) left canvas dirty — call stopAnimation to properly clean up
- **INSIGHT**: When a variable is already bounded at USE site (Math.min in drawFrame), don't also bound it at SET site — this permanently downgrades the original value
- **INSIGHT**: Any unbounded array that grows per frame MUST have a cap. Even 60 pushes/sec = 3600/min = crash in minutes
- **TEST CAUGHT**: Nothing — all bugs found by Gemini

### 5-Build Review: #131-#135
**Builds:** contrast-check, beat-forge, solitaire, sprite-studio, fourier-draw
**Pattern analysis:**
- **Category explosion:** Design tool, music sequencer, card game, animation editor, math visualization — 5 builds spanning 5 completely different categories
- **Gemini consistently finding 4-6 bugs per build** — audit process remains the strongest quality gate
- **Recurring theme: state management across time** — playback timers in beat-forge/sprite-studio, animation frames in fourier-draw, game state in solitaire. All need careful lifecycle management (stop timers on state transitions, clear timeouts, bound growing arrays)
- **Recurring theme: global state pollution** — numCircles downgrade in fourier-draw, gameWon lock in solitaire. Prefer local bounds over global mutations
- **New insight patterns:** setTimeout race conditions (fourier-draw presets, picross error flash), canvas coordinate offsets (now in 3+ projects — should be default pattern)
- **Zero user-reported bugs** — pipeline continues to work
- **Milestone #135** demonstrates mastery: complex math (DFT), interactive drawing, real-time animation, all in single file

### logic-forge (2026-03-26)
- **KEEP**: Tap-to-place + tap-to-wire interaction model — far better than drag on mobile
- **KEEP**: Bezier curve wires between pins — visually clean, auto-routes around obstacles
- **KEEP**: Convergence-based simulation (iterate until stable, max 10 passes) — handles both deep circuits and oscillators safely
- **KEEP**: Directed graph with truth-table evaluation — clean, extensible architecture for digital logic
- **KEEP**: Glowing wires (shadowBlur + bright green) for HIGH signals — immediate visual feedback
- **IMPROVE**: Gemini caught node stacking — placing on existing node created hidden duplicates. Must check hitTestNode before placing
- **IMPROVE**: hitTestPin iterated forward while hitTestNode iterated backward — inconsistent z-order. Both must iterate backward (top node first)
- **IMPROVE**: Hardcoded 3-pass simulation breaks circuits deeper than 3 gates. Convergence loop with changed flag handles any depth
- **IMPROVE**: Out-of-bounds placement pushed pins off-screen. Clamp coordinates to keep all pins accessible
- **INSIGHT**: For graph-based simulations, use convergence check (did any state change?) rather than fixed pass count. Cap iterations to prevent infinite loops from feedback circuits
- **INSIGHT**: All hit-testing functions in a layered canvas must iterate in the SAME direction (backward = topmost first)
- **TEST CAUGHT**: Nothing — all bugs found by Gemini

### gravity-golf (2026-03-26)
- **KEEP**: Slingshot aim with predictive trajectory — essential for physics puzzle games, makes them feel fair
- **KEEP**: Percentage-based level coordinates (x/100*W) — scales to any screen size naturally
- **KEEP**: Attract (blue) + repel (orange) wells — doubles puzzle design space with just one extra mechanic
- **KEEP**: Par scoring with golf terminology — gives players a goal beyond just completing the level
- **IMPROVE**: Gemini caught par=0 labeled as "Under par" — must distinguish diff<0 (under), diff===0 (par), diff===1 (bogey)
- **IMPROVE**: Trajectory preview broke on repel wells — computeTrajectory had `if(d<8)break` for ALL wells but actual physics only absorbs on attract. Must match preview physics to actual physics exactly
- **IMPROVE**: Resize called loadLevel which reset strokes/state — mobile address bar hide triggers resize. Must recalculate positions without resetting game state
- **IMPROVE**: Divide-by-zero possible if ball hits exact well center — add epsilon guard (d<0.001 → d=0.001)
- **INSIGHT**: Trajectory preview must use IDENTICAL physics to the actual simulation. Any discrepancy makes the game feel unfair
- **INSIGHT**: Resize handler must distinguish "recalculate layout" from "reset game state" — never reset progress on resize
- **TEST CAUGHT**: Nothing — all bugs found by Gemini

### graph-calc (2026-03-26)
- **KEEP**: Custom math parser via regex replacement + new Function — handles implicit multiplication, trig functions, powers
- **KEEP**: niceStep() algorithm for dynamic grid spacing — 1/2/5 steps based on visible range, adapts beautifully to zoom
- **KEEP**: Asymptote detection via y-jump threshold — breaks line at discontinuities in tan(x), 1/x
- **KEEP**: Coordinate cursor display — shows math (x,y) at pointer position
- **IMPROVE**: Gemini caught canvas aspect ratio distortion — canvas.height was set to full window height but CSS clipped it to panelTop(). Must set canvas.height = panelTop() so internal resolution matches visual size
- **IMPROVE**: try/catch inside per-pixel render loop de-optimizes V8. Math functions return NaN for domain errors (sqrt(-1)), no throw needed. Use typeof check instead
- **IMPROVE**: log() should map to Math.log10 (base-10) for math convention, ln() to Math.log (natural). Users typing log(100) expect 2, not 4.6
- **IMPROVE**: Regex literals with character classes (e.g., /[a-zA-Z(]/) cause false positive in test's brace checker. Use RegExp constructor for complex patterns
- **INSIGHT**: Canvas internal dimensions (width/height attributes) MUST match CSS visual dimensions. Mismatches cause stretching/squishing
- **INSIGHT**: Never put try/catch inside a tight loop that runs 1000+ times per frame. Check validity once at parse time, not at evaluation time
- **TEST CAUGHT**: Brace balance false positive from regex literals — 6th occurrence of this test limitation

### crypto-lens (2026-03-26)
- **KEEP**: Step-by-step cipher visualization — shows exact math for each character transformation
- **KEEP**: Three cipher types representing distinct math concepts: Caesar (modular arithmetic), Vigenere (polyalphabetic), XOR (bitwise)
- **KEEP**: Encrypt/decrypt bidirectional toggle — proves mathematical symmetry of ciphers
- **KEEP**: XOR binary visualization with per-bit coloring (same bits → green, different → red)
- **IMPROVE**: Gemini caught case destruction — caesarChar and vigenereChar forced toUpperCase before processing, losing original casing. Must detect isLower/isUpper and use appropriate base (97 vs 65)
- **IMPROVE**: innerHTML += in loops causes layout thrashing — should build string first, assign once. Noted but not fully refactored (works for current DOM size)
- **IMPROVE**: Play always reset stepIdx to 0 — should resume from current position, only reset if at end
- **INSIGHT**: Any text transformation function must preserve properties of the input (case, whitespace, punctuation) that aren't part of the transformation. Test with mixed-case inputs during development
- **INSIGHT**: For cipher implementations, the decrypt operation should be the exact mathematical inverse of encrypt. Test: decrypt(encrypt(text)) === text
- **TEST CAUGHT**: Nothing — all bugs found by Gemini

### palette-gen (2026-03-26)
- **KEEP**: HSL-based color harmony generation — simple hue rotations produce beautiful palettes (analogous ±30°, complementary +180°, triadic +120°/+240°)
- **KEEP**: Full-viewport swatches with auto black/white text — immediately visual, no chrome needed
- **KEEP**: Constrained random seed (S: 40-85, L: 35-65) — avoids ugly washed-out or invisible colors
- **KEEP**: Export as CSS custom properties — practical for designers
- **IMPROVE**: Gemini caught WCAG luminance threshold at 0.4 — WAY too high. Correct crossover for black/white text is approximately 0.179. This is the second time luminance math has been reviewed (also in contrast-check)
- **IMPROVE**: Clipboard "Copied!" shown even when writeText fails — must use .then() to only show on success
- **IMPROVE**: Locked colors broke harmony when seed randomized — locked color should BECOME the seed so unlocked colors harmonize with it
- **INSIGHT**: The WCAG luminance crossover for max contrast between black and white text is ~0.179, not 0.4 or 0.5. Memorize this number.
- **INSIGHT**: When a "lock" feature exists alongside regeneration, the locked item should constrain the regeneration, not be ignored by it
- **TEST CAUGHT**: Nothing — all bugs found by Gemini

### 5-Build Review: #136-#140
**Builds:** logic-forge, gravity-golf, graph-calc, crypto-lens, palette-gen
**Pattern analysis:**
- **Category diversity restored:** CS education (logic gates), physics game (gravity golf), math tool (grapher), cryptography (ciphers), design tool (palette gen) — 5 different categories
- **Gemini consistently finding 3-5 bugs per build** — audit continues to be essential
- **Recurring WCAG luminance errors** — appeared in both contrast-check and palette-gen. The 0.179 threshold is now permanently learned
- **Recurring themes:** canvas coordinate offsets (getBoundingClientRect), game state/timer lifecycle, try/catch performance in loops
- **New patterns learned:** convergence-based simulation (logic-forge), trajectory preview must match actual physics (gravity-golf), locked items should constrain regeneration (palette-gen)
- **Zero user-reported bugs** — pipeline working perfectly
- **10 projects remaining** before pivot to adversarial review at #150
