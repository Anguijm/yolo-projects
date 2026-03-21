# WiFi Time Machine

A local web app that continuously logs WiFi signal strength and nearby networks, then lets you scrub through time like a video player.

## What it does

- Real-time monitoring of your WiFi connection (signal, channel, rate, security)
- Logs all visible networks every 10 seconds to a local JSONL file
- Signal strength chart over time with current-position marker
- Network visibility heatmap — see which networks appear/disappear
- Timeline scrubber to browse any historical moment
- LIVE mode with auto-updating, or pause and scrub manually

## How to run

```bash
python3 wifi_time_machine.py
```

Opens `http://localhost:8765` in your browser automatically. Leave it running — it collects data as long as it's alive. Come back hours later and scrub through the full history.

```bash
# Custom port
python3 wifi_time_machine.py --port 9000

# Faster scanning (every 5 seconds)
python3 wifi_time_machine.py --interval 5

# Don't auto-open browser
python3 wifi_time_machine.py --no-browser
```

Data persists in `data/wifi_log.jsonl` — restart the app and your full history is still there.

## Requirements

- Linux with `nmcli` (most distros have this)
- Python 3 (stdlib only, zero dependencies)

## What you'd want to change

- Scan interval (default 10s) — lower for more granularity, higher for less resource use
- The WiFi interface is currently hardcoded to `wlo1` in the connection info helper — change if yours differs
- Heatmap caps at 15 networks and 80 time columns — adjustable in the JS
