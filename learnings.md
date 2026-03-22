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
