# Cron Studio

A cron expression debugger, explainer, and visualizer that runs entirely in the browser.

## What it does

- **Real-time validation** — VALID/INVALID badge as you type, red border on errors
- **Natural language explanation** — translates any cron expression to plain English instantly
- **Next N runs** — shows the next 5, 10, or 25 scheduled execution times (with date, day, time)
- **35-day calendar heatmap** — see which days the job fires and how many times, color-coded by intensity
- **8 presets** — click to load common schedules (every minute, hourly, weekdays 9am, quarterly, etc.)
- **Full cron syntax support**: `*`, `*/N`, ranges `a-b`, lists `a,b`, steps `a-b/N`, named months/days, `@daily`/`@weekly`/`@hourly` shortcuts
- **DOM+DOW OR behavior** — correct Unix crontab semantics when both fields are non-wildcard

## How to run

Open `index.html` in any browser. No server needed.

## Supported syntax

| Field   | Range | Supports               |
|---------|-------|------------------------|
| Minute  | 0–59  | `*`, `*/5`, `0,30`     |
| Hour    | 0–23  | `*`, `*/2`, `9-17`     |
| Day     | 1–31  | `*`, `1,15`, `1-7`     |
| Month   | 1–12  | `*`, `jan-mar`, `1,7`  |
| Weekday | 0–7   | `*`, `mon-fri`, `1-5`  |

Weekday 0 and 7 both mean Sunday. Month and weekday names are case-insensitive.

## What I'd change next

- Add a "test against specific date" input (will this run on Christmas?)
- Show field-by-field highlight when cursor is inside a field
- Add `@reboot` label (not schedulable in browser but explain what it means)
