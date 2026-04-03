# Cron Builder

Visual cron expression builder with live human-readable descriptions and next-run preview.

## What it does

- Type a cron expression or edit the 5 individual fields (minute, hour, day, month, weekday)
- See an instant human-readable description: "At 9am on Monday–Friday"
- Preview the next 10 scheduled run times with relative times ("in 2h")
- 12 preset schedules (@daily, @hourly, every 5m, etc.)
- Timezone selector with auto-detection of your local zone
- Copy button to grab the expression
- 100% offline — nothing leaves your browser

## How to run

Open `index.html` directly in any browser. No server needed.

## Syntax supported

| Pattern | Meaning |
|---------|---------|
| `*` | Every value |
| `*/n` | Every n units |
| `a-b` | Range |
| `a,b,c` | List |
| `a-b/n` | Range with step |

Weekday: 0=Sunday, 1=Monday, ..., 6=Saturday (7 also accepted as Sunday alias).

## What to change

- Add named months (JAN-DEC) and weekday aliases (MON-SUN) in `expandField`
- Add `@reboot` / `@annually` as preset aliases
- Extend timezone list
