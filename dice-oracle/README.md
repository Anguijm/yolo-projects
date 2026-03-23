# Dice Oracle

Dice notation parser with discrete probability visualization. Type dice expressions, see the exact probability distribution, roll with crypto-quality RNG, and see where your roll lands on the histogram.

## Features

- Dice notation parser: NdX, NdXkH (keep highest), +/- modifiers, leading negatives
- Exact discrete convolution for standard dice distributions
- Monte Carlo simulation (20K iterations) for keep-highest distributions
- Canvas histogram with discrete bars (not continuous curves)
- Roll marker: magenta highlight + dashed line showing where your roll landed
- Percentile display (TOP X% | PERCENTILE Y)
- Range, mean, and P(roll) statistics
- Crypto.getRandomValues for high-quality entropy
- True roll simulation (not sampled from distribution)
- Live preview: distribution updates as you type (debounced)
- Preset buttons that actually roll (d20, 2d6, 4d6k3, d100, 3d8+5, 8d6)
- Synthesized click audio (white noise bandpass burst)
- Roll history log
- Cybernetic terminal aesthetic, OLED black, mobile-first

## Bugs Fixed by Gemini Audit

- Chart axis labels invisible (#222 on black background — changed to #555)
- Preset buttons only previewed, didn't roll (now call doRoll())
- Leading negatives ignored (-1d4 treated as +1d4 — now convolves from zero)
- Roll sampled from Monte Carlo distribution instead of true simulation (now uses independent crypto RNG roll)
- for...in loop vulnerable to prototype pollution (switched to Object.keys)

## How to Run

Open `index.html`. Type dice notation (e.g. `4d6k3+2`) and press Enter to roll. Use presets for common rolls. The histogram shows probability distribution with your roll highlighted.
