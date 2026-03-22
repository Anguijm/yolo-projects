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
