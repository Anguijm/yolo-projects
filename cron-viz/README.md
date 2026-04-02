# cron-viz

Visual cron expression builder. Click, slide, and pick to compose cron schedules -- see plain-English descriptions and the next 10 fire times update in real time.

## Features

- **Visual builder** -- toggle between Every / Step / Pick modes for each of the 5 cron fields (minute, hour, day-of-month, month, day-of-week)
- **Step sliders** -- drag a range slider to set `*/N` intervals for minute, hour, and day-of-month
- **Multi-select picks** -- click individual values to build comma-separated lists
- **Paste to visualize** -- paste any standard 5-field cron expression and the UI updates to match
- **Alias support** -- recognizes `@yearly`, `@monthly`, `@weekly`, `@daily`, `@hourly`
- **Plain-English description** -- auto-generated human-readable summary of the expression
- **Next 10 fire times** -- computed client-side, scans up to one year ahead
- **Presets** -- one-click common schedules (every min, hourly, daily, weekly, monthly, weekdays 9am, every 5/15 min)
- **Mobile-friendly** -- works at 375px minimum width, touch targets sized for fingers

## Usage

Open `index.html` in any browser. No server required, no dependencies.

- Use the mode buttons (Every / Step / Pick) under each field to switch input method
- Drag step sliders to set interval values
- Click number/name buttons to toggle specific values on/off (cyan border = selected)
- Paste an existing expression into the text input and press PARSE or Enter
- Click any preset button to load a common schedule

## Tech

Single HTML file. Zero dependencies. All CSS and JS inline. Dark industrial aesthetic per the YOLO design system.
