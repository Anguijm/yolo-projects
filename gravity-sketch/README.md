# Gravity Sketch

Physics playground. Draw ramps, drop balls and boxes, watch them bounce and roll. Grab and throw objects. Zero external dependencies — custom physics engine.

## Features

### Drawing
- Draw lines that become static ramps/platforms
- Minimum distance threshold between points for smooth lines
- Drawing preview while sketching

### Physics (Custom Engine)
- Gravity with configurable toggle
- Circle-to-line-segment collision (project onto segment, reflect velocity)
- Circle-to-circle collision (overlap resolution + velocity exchange)
- Surface friction on line collisions
- Velocity-based bounce (configurable restitution)
- Box rotation with angular velocity

### Interaction
- Draw Ramp mode: sketch platforms and ramps
- Drop Ball mode: click to spawn bouncing circles
- Drop Box mode: click to spawn tumbling rectangles
- Grab and throw: click any ball to drag, release to toss with mouse velocity
- Gravity toggle (on/off)
- Clear all button

### Visual
- Blueprint grid background
- Neon glow on dynamic bodies (shadowBlur)
- Color variety on spawned objects
- Floor and wall boundaries
- Body count display
- Demo scene on load (ramps + balls)

### Architecture
- Custom circle-line and circle-circle collision (no Matter.js, no external libs)
- MAX_BODIES cap (80) with oldest-first removal
- Out-of-bounds cleanup prevents memory leaks
- Zero external dependencies, single-file HTML
- OLED black, mobile-first, all PWA metas

## How to Run

Open `index.html`. Draw ramps with the default Draw tool. Switch to Drop Ball or Drop Box to spawn objects. Click and drag balls to throw them. Toggle gravity. Clear to reset.
