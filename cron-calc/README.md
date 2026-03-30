# cron-calc

Multi-cron visual timeline. Paste a list of cron jobs and see when everything fires across a 24-hour day or 7-day week. Find collisions, gaps, and peak load times at a glance.

## Features

- **Multi-job input** — one `cron-expression  label` pair per line
- **24-Hour day view** — per-job horizontal tracks with minute-resolution ticks
- **7-Day week view** — each job as a row of 7 day cells
- **Collision detection** — same-minute fires highlighted in red, listed in collision report
- **Statistics panel** — total fires/day, collision count, peak hour, per-job fire count
- **Hover tooltips** — shows time and all jobs firing at that minute
- **4 presets** — WEB SERVER, DATABASE, CI/CD, MIXED
- **Text aliases** — `MON-FRI`, `JAN-DEC`, etc. fully supported
- **Sunday=7** normalization — both `0` and `7` accepted for Sunday

## Usage

Format: `MIN HR DOM MON DOW  label`

```
# one job per line
*/5 * * * *    cache-warm
0 2 * * *      nightly-backup
0 9 * * MON-FRI  standup-reminder
0 0 1 * *      monthly-billing
```

Lines starting with `#` are ignored.

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `d` | Switch to 24H day view |
| `w` | Switch to 7-day week view |

## Zero Dependencies

Single HTML file, no CDN, no frameworks.
