# Weather Terrarium

Procedural micro-climate simulator. Control temperature, humidity, wind, and time of day to generate 10 different weather states in real-time. Single HTML file, zero dependencies.

## Features

- 10 weather states: Clear, Cloudy, Rain, Thunderstorm, Snow, Blizzard, Fog, Dust Storm, Haze, Aurora
- Weather derived from physical inputs (temp + humidity), not hardcoded buttons
- 4-layer parallax procedural landscape (changes color with weather)
- 3000 object-pooled particles (rain streaks, drifting snow, dust) — zero GC
- Procedural clouds that drift with wind
- Recursive branching lightning with screen flash
- Aurora borealis sine-wave bands
- Fog layers with vertical drift
- Stars with twinkle (night only)
- Smooth weather transitions via lerp interpolation
- Time-of-day slider (dawn, day, dusk, night sky colors)
- 6 presets: Storm, Blizzard, Desert, Aurora, Spring, Fog
- Click canvas to burst particles
- Glassmorphic floating control panel

## How to Run

Open `index.html` in any modern browser.

## What You'd Change

- WebGL for GPU-accelerated particles at 4K
- Sound effects (thunder rumble, rain ambience, wind howl)
- Animated day/night cycle (auto-advance time slider)
