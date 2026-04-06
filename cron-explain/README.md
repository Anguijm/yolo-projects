# cron-explain

Cron expression explainer — paste any 5-field or 6-field cron expression and get an instant plain-English breakdown.

## Features

- **Field breakdown** — color-coded chips for each field (SEC/MIN/HOUR/DOM/MON/DOW) with per-field plain-English description
- **Plain-English description** — full combined sentence describing the schedule
- **Next 10 runs** — computed with smart iteration (skips non-matching days/months for efficiency); relative time shown alongside absolute datetime
- **Interactive builder** — click any field chip to open the type editor (Any / Exact / Range / List / Step), with quick-pick chips for common values
- **Presets bar** — 12 common patterns including @daily, @weekly, weekdays-9am, business hours, etc.
- **@-macros** — @daily, @weekly, @monthly, @yearly, @hourly, @midnight, @reboot all supported
- **6-field format** — leading seconds field (e.g. `30 0 9 * * 1-5`) fully supported

## How to run

Open `index.html` directly in any browser. No server required.

## Tech

Single HTML file, zero dependencies. Pure JS date math for schedule computation.
