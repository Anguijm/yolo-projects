# Wealth Calc

Compound interest savings calculator with inflation adjustment and CSS bar chart. See your money grow year by year.

## Features

- Inputs: initial amount, monthly contribution, annual return rate, time horizon (years)
- Monthly compounding: A = P(1+r/n)^(nt) + future value of series
- Inflation toggle (3% average) showing real purchasing power
- Inflation-adjusted contributions tracked separately for accurate breakdown
- CSS bar chart showing contributions vs interest per year
- Stacked bars: blue (contributions) + green (interest)
- Chart auto-samples for large year counts (>30 years)
- Big final number display with color change on inflation mode
- Contribution + interest breakdown text
- Real-time updates on any input change
- Input clamping (years 1-60, NaN-safe parsing)
- OLED black, mobile-first, all PWA metas

## Bugs Fixed by Gemini Audit

- Inflation-adjusted breakdown subtracted nominal contributions from real total (numbers didn't add up) — tracked real contributions separately with per-year inflation discounting
- Chart used nominal contributions with inflation-adjusted total — now uses matching real contributions

## How to Run

Open `index.html`. Adjust the inputs to see projected savings. Toggle inflation to see real purchasing power. The chart shows growth by year.
