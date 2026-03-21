# ASCII Cam

Live webcam feed converted to real-time ASCII art. Multiple character sets, color themes, snapshot export. The "show people at a party" app. Single HTML file, zero dependencies.

## Features

- 5 character sets: Detailed (70-char), Simple (10-char), Blocks (Unicode), Braille (2x4 dot matrix), Emoji
- 5 color themes: Green Terminal, Amber CRT, Blue Neon, White, Hot Pink
- Resolution slider (40-200 columns)
- Contrast/gamma adjustment slider
- Mirror toggle (selfie mode)
- Invert toggle (light/dark swap)
- SNAP: renders to canvas, downloads as themed PNG
- Copy Text: copies raw ASCII to clipboard
- Auto-sizing font fits viewport
- FPS counter
- Keyboard: S=snap, I=invert, M=mirror
- Array-join rendering (no string concatenation GC pressure)
- ITU-R BT.601 luminance calculation
- Aspect ratio correction (rows halved for character height)
- willReadFrequently canvas optimization

## How to Run

Open `index.html` in a browser (HTTPS or localhost required for camera). Click "Enable Camera."

## What You'd Change

- Rear camera toggle for mobile
- FPS throttle option (15fps for retro feel)
- Floyd-Steinberg dithering for better gradients
- Color ASCII mode (colored characters matching source pixels)
