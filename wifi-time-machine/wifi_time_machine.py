#!/usr/bin/env python3
"""
wifi-time-machine: Log WiFi data over time, browse it with a timeline scrubber.

Usage:
  python3 wifi_time_machine.py              # Start collecting + serving UI
  python3 wifi_time_machine.py --port 8765  # Custom port

Opens a browser UI where you can:
- See real-time WiFi signal strength and nearby networks
- Scrub through history like a video timeline
- View signal strength charts over time
- See networks appear/disappear
"""

import argparse
import json
import os
import subprocess
import threading
import time
import webbrowser
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)
LOG_FILE = DATA_DIR / "wifi_log.jsonl"

# ---------------------------------------------------------------------------
# WiFi scanning
# ---------------------------------------------------------------------------

def scan_wifi():
    """Scan WiFi networks using nmcli. Returns list of network dicts."""
    try:
        result = subprocess.run(
            ["nmcli", "-t", "-f", "IN-USE,BSSID,SSID,MODE,CHAN,RATE,SIGNAL,SECURITY", "dev", "wifi", "list", "--rescan", "auto"],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode != 0:
            return []
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return []

    networks = []
    for line in result.stdout.strip().split("\n"):
        if not line:
            continue
        # nmcli -t uses : as separator, but BSSID contains colons escaped as \:
        # Replace escaped colons in BSSID temporarily
        parts = []
        current = ""
        i = 0
        while i < len(line):
            if line[i] == '\\' and i + 1 < len(line) and line[i + 1] == ':':
                current += ':'
                i += 2
            elif line[i] == ':':
                parts.append(current)
                current = ""
                i += 1
            else:
                current += line[i]
                i += 1
        parts.append(current)

        if len(parts) >= 8:
            networks.append({
                "in_use": parts[0] == "*",
                "bssid": parts[1],
                "ssid": parts[2] or "(hidden)",
                "mode": parts[3],
                "channel": parts[4],
                "rate": parts[5],
                "signal": int(parts[6]) if parts[6].isdigit() else 0,
                "security": parts[7],
            })
    return networks


def collect_snapshot():
    """Collect a single WiFi snapshot."""
    networks = scan_wifi()
    connected = next((n for n in networks if n["in_use"]), None)

    snapshot = {
        "timestamp": datetime.now().isoformat(),
        "epoch": time.time(),
        "networks": networks,
        "connected_ssid": connected["ssid"] if connected else None,
        "connected_signal": connected["signal"] if connected else 0,
        "connected_bssid": connected["bssid"] if connected else None,
        "network_count": len(networks),
    }
    return snapshot


# ---------------------------------------------------------------------------
# Data collection thread
# ---------------------------------------------------------------------------

snapshots_in_memory = []
collection_running = True
MAX_MEMORY_SNAPSHOTS = 10000

def collection_loop(interval=10):
    """Collect WiFi data every `interval` seconds."""
    global collection_running
    while collection_running:
        try:
            snap = collect_snapshot()
            snapshots_in_memory.append(snap)
            if len(snapshots_in_memory) > MAX_MEMORY_SNAPSHOTS:
                snapshots_in_memory.pop(0)
            # Append to log file
            with open(LOG_FILE, "a") as f:
                f.write(json.dumps(snap) + "\n")
        except Exception as e:
            print(f"Collection error: {e}")
        time.sleep(interval)


def load_history():
    """Load all historical snapshots from disk (line-by-line to avoid OOM)."""
    if not LOG_FILE.exists():
        return []
    snapshots = []
    with open(LOG_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    snapshots.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return snapshots


# ---------------------------------------------------------------------------
# HTTP server
# ---------------------------------------------------------------------------

class WifiHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Silence request logs

    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode())
        elif self.path == "/api/history":
            # Return all data from memory (no disk read per request)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(snapshots_in_memory).encode())
        elif self.path == "/api/latest":
            if snapshots_in_memory:
                data = snapshots_in_memory[-1]
            else:
                data = {"error": "no data yet"}
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
        elif self.path.startswith("/api/since/"):
            # Return snapshots since epoch timestamp
            try:
                since = float(self.path.split("/api/since/")[1])
            except (ValueError, IndexError):
                since = 0
            filtered = [s for s in snapshots_in_memory if s.get("epoch", 0) > since]
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(filtered).encode())
        else:
            self.send_response(404)
            self.end_headers()


# ---------------------------------------------------------------------------
# HTML UI
# ---------------------------------------------------------------------------

HTML_PAGE = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>WiFi Time Machine</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'SF Mono', 'Fira Code', monospace; background: #0a0a0a; color: #ccc; overflow-x: hidden; }
.header { padding: 1.2rem 2rem; border-bottom: 1px solid #1a1a1a; display: flex; justify-content: space-between; align-items: center; }
.header h1 { font-size: 1.3rem; color: #fff; }
.header .live-badge { font-size: 0.7rem; padding: 0.2rem 0.6rem; border-radius: 10px; background: #0a2a0a; color: #4ade80; border: 1px solid #166534; animation: pulse 2s infinite; }
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
.connected-bar { padding: 0.8rem 2rem; background: #0d0d0d; border-bottom: 1px solid #1a1a1a; display: flex; gap: 2rem; align-items: center; flex-wrap: wrap; }
.conn-item { display: flex; flex-direction: column; }
.conn-label { font-size: 0.6rem; color: #555; text-transform: uppercase; letter-spacing: 0.1em; }
.conn-value { font-size: 0.9rem; color: #fff; margin-top: 0.1rem; }
.signal-big { font-size: 2rem; font-weight: bold; }

.timeline-section { padding: 1rem 2rem; border-bottom: 1px solid #1a1a1a; }
.timeline-controls { display: flex; align-items: center; gap: 1rem; margin-bottom: 0.5rem; }
.timeline-controls button { background: #1a1a1a; border: 1px solid #333; color: #ccc; padding: 0.3rem 0.7rem; border-radius: 4px; cursor: pointer; font-family: inherit; font-size: 0.75rem; }
.timeline-controls button:hover { background: #222; color: #fff; }
.timeline-controls button.active { background: #166534; border-color: #4ade80; color: #4ade80; }
.timeline-label { font-size: 0.75rem; color: #666; }
#timeline-slider { flex: 1; accent-color: #4ade80; }
.timeline-time { font-size: 0.8rem; color: #fff; min-width: 160px; text-align: right; }

.main { display: grid; grid-template-columns: 1fr 1fr; gap: 0; min-height: calc(100vh - 220px); }
.panel { padding: 1.5rem 2rem; }
.panel-left { border-right: 1px solid #1a1a1a; }
.section-title { font-size: 0.85rem; color: #fff; margin-bottom: 0.8rem; }

/* Signal chart */
.chart-area { width: 100%; height: 200px; position: relative; background: #111; border-radius: 8px; border: 1px solid #1a1a1a; overflow: hidden; }
canvas { width: 100%; height: 100%; }

/* Network list */
.network-list { margin-top: 1rem; }
.net-row { display: flex; align-items: center; gap: 0.8rem; padding: 0.5rem 0.6rem; border-radius: 4px; margin-bottom: 2px; transition: background 0.15s; }
.net-row:hover { background: #151515; }
.net-row.connected { background: #0a1a0a; border: 1px solid #1a3a1a; }
.net-ssid { flex: 1; font-size: 0.8rem; color: #fff; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.net-signal-bar { width: 60px; height: 12px; background: #1a1a1a; border-radius: 2px; overflow: hidden; }
.net-signal-fill { height: 100%; border-radius: 2px; transition: width 0.3s; }
.net-signal-num { font-size: 0.7rem; color: #666; width: 35px; text-align: right; }
.net-security { font-size: 0.6rem; color: #555; width: 50px; }
.net-channel { font-size: 0.65rem; color: #444; width: 30px; text-align: center; }

/* Heatmap */
.heatmap { margin-top: 1rem; }
.heatmap-row { display: flex; align-items: center; margin-bottom: 2px; }
.heatmap-label { width: 120px; font-size: 0.65rem; color: #888; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.heatmap-cells { display: flex; gap: 1px; flex: 1; }
.heatmap-cell { height: 14px; min-width: 3px; flex: 1; border-radius: 1px; cursor: pointer; transition: opacity 0.1s; }
.heatmap-cell:hover { opacity: 0.7; }

.empty-state { text-align: center; padding: 3rem; color: #444; }
.empty-state .icon { font-size: 2.5rem; margin-bottom: 0.5rem; }
</style>
</head>
<body>

<div class="header">
  <h1>WiFi Time Machine</h1>
  <div>
    <span class="live-badge" id="live-badge">LIVE</span>
    <span style="font-size:0.7rem;color:#555;margin-left:0.5rem" id="snapshot-count">0 snapshots</span>
  </div>
</div>

<div class="connected-bar" id="connected-bar">
  <div class="conn-item"><span class="conn-label">Connected To</span><span class="conn-value" id="conn-ssid">--</span></div>
  <div class="conn-item"><span class="conn-label">Signal</span><span class="conn-value signal-big" id="conn-signal">--</span></div>
  <div class="conn-item"><span class="conn-label">Channel</span><span class="conn-value" id="conn-channel">--</span></div>
  <div class="conn-item"><span class="conn-label">Rate</span><span class="conn-value" id="conn-rate">--</span></div>
  <div class="conn-item"><span class="conn-label">Security</span><span class="conn-value" id="conn-security">--</span></div>
  <div class="conn-item"><span class="conn-label">Networks Visible</span><span class="conn-value" id="conn-count">--</span></div>
</div>

<div class="timeline-section">
  <div class="timeline-controls">
    <button id="btn-live" class="active" onclick="goLive()">LIVE</button>
    <input type="range" id="timeline-slider" min="0" max="0" value="0">
    <span class="timeline-time" id="timeline-time">--</span>
  </div>
</div>

<div class="main">
  <div class="panel panel-left">
    <div class="section-title">Signal Strength Over Time</div>
    <div class="chart-area"><canvas id="signal-chart"></canvas></div>

    <div class="section-title" style="margin-top:1.5rem">Network Visibility Heatmap</div>
    <div class="heatmap" id="heatmap"></div>
  </div>
  <div class="panel">
    <div class="section-title">Nearby Networks</div>
    <div class="network-list" id="network-list">
      <div class="empty-state"><div class="icon">📡</div><div>Collecting data...</div></div>
    </div>
  </div>
</div>

<script>
function escapeHtml(s) {
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');
}

let allSnapshots = [];
let isLive = true;
let currentIdx = 0;
const slider = document.getElementById('timeline-slider');

// Fetch all history on load, then poll for new
async function init() {
  try {
    const resp = await fetch('/api/history');
    allSnapshots = await resp.json();
  } catch(e) { allSnapshots = []; }
  if (allSnapshots.length > 0) {
    slider.max = allSnapshots.length - 1;
    slider.value = slider.max;
    currentIdx = allSnapshots.length - 1;
    renderSnapshot(allSnapshots[currentIdx]);
    renderChart();
    renderHeatmap();
  }
  document.getElementById('snapshot-count').textContent = allSnapshots.length + ' snapshots';
  // Poll every 10s
  setInterval(poll, 10000);
}

async function poll() {
  const lastEpoch = allSnapshots.length > 0 ? allSnapshots[allSnapshots.length - 1].epoch : 0;
  try {
    const resp = await fetch('/api/since/' + lastEpoch);
    const newData = await resp.json();
    if (newData.length > 0) {
      allSnapshots.push(...newData);
      slider.max = allSnapshots.length - 1;
      document.getElementById('snapshot-count').textContent = allSnapshots.length + ' snapshots';
      if (isLive) {
        currentIdx = allSnapshots.length - 1;
        slider.value = currentIdx;
        renderSnapshot(allSnapshots[currentIdx]);
      }
      renderChart();
      renderHeatmap();
    }
  } catch(e) {}
}

slider.addEventListener('input', () => {
  isLive = false;
  document.getElementById('btn-live').classList.remove('active');
  document.getElementById('live-badge').style.display = 'none';
  currentIdx = parseInt(slider.value);
  if (allSnapshots[currentIdx]) {
    renderSnapshot(allSnapshots[currentIdx]);
    renderChart();
  }
});

function goLive() {
  isLive = true;
  document.getElementById('btn-live').classList.add('active');
  document.getElementById('live-badge').style.display = '';
  if (allSnapshots.length > 0) {
    currentIdx = allSnapshots.length - 1;
    slider.value = currentIdx;
    renderSnapshot(allSnapshots[currentIdx]);
    renderChart();
  }
}

function signalColor(signal) {
  if (signal >= 75) return '#4ade80';
  if (signal >= 50) return '#fbbf24';
  if (signal >= 25) return '#fb923c';
  return '#f87171';
}

function formatTime(iso) {
  const d = new Date(iso);
  return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
}

function formatDateTime(iso) {
  const d = new Date(iso);
  return d.toLocaleDateString([], { month: 'short', day: 'numeric' }) + ' ' + formatTime(iso);
}

function renderSnapshot(snap) {
  document.getElementById('timeline-time').textContent = formatDateTime(snap.timestamp);

  // Connected info
  document.getElementById('conn-ssid').textContent = snap.connected_ssid || 'Disconnected';
  const sig = snap.connected_signal || 0;
  document.getElementById('conn-signal').textContent = sig + '%';
  document.getElementById('conn-signal').style.color = signalColor(sig);
  document.getElementById('conn-count').textContent = snap.network_count;

  const connected = snap.networks.find(n => n.in_use);
  document.getElementById('conn-channel').textContent = connected ? connected.channel : '--';
  document.getElementById('conn-rate').textContent = connected ? connected.rate : '--';
  document.getElementById('conn-security').textContent = connected ? connected.security : '--';

  // Network list
  const sorted = [...snap.networks].sort((a, b) => b.signal - a.signal);
  const listEl = document.getElementById('network-list');
  listEl.innerHTML = sorted.map(n => `
    <div class="net-row ${n.in_use ? 'connected' : ''}">
      <span class="net-ssid">${n.in_use ? '● ' : ''}${escapeHtml(n.ssid)}</span>
      <span class="net-channel">ch${n.channel}</span>
      <div class="net-signal-bar"><div class="net-signal-fill" style="width:${n.signal}%;background:${signalColor(n.signal)}"></div></div>
      <span class="net-signal-num">${n.signal}%</span>
      <span class="net-security">${n.security}</span>
    </div>
  `).join('');
}

// Signal chart (canvas)
function renderChart() {
  const canvas = document.getElementById('signal-chart');
  const ctx = canvas.getContext('2d');
  const rect = canvas.parentElement.getBoundingClientRect();
  canvas.width = rect.width * 2;
  canvas.height = rect.height * 2;
  ctx.scale(2, 2);
  const W = rect.width;
  const H = rect.height;

  ctx.clearRect(0, 0, W, H);

  if (allSnapshots.length < 2) return;

  const pad = { top: 10, right: 10, bottom: 25, left: 35 };
  const chartW = W - pad.left - pad.right;
  const chartH = H - pad.top - pad.bottom;

  // Y axis (0-100%)
  ctx.strokeStyle = '#222';
  ctx.lineWidth = 0.5;
  ctx.fillStyle = '#444';
  ctx.font = '9px monospace';
  ctx.textAlign = 'right';
  for (let pct of [0, 25, 50, 75, 100]) {
    const y = pad.top + chartH - (pct / 100) * chartH;
    ctx.beginPath();
    ctx.moveTo(pad.left, y);
    ctx.lineTo(pad.left + chartW, y);
    ctx.stroke();
    ctx.fillText(pct + '%', pad.left - 4, y + 3);
  }

  // Draw connected signal line
  ctx.beginPath();
  ctx.strokeStyle = '#4ade80';
  ctx.lineWidth = 1.5;
  const n = allSnapshots.length;
  for (let i = 0; i < n; i++) {
    const x = pad.left + (i / (n - 1)) * chartW;
    const sig = allSnapshots[i].connected_signal || 0;
    const y = pad.top + chartH - (sig / 100) * chartH;
    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  }
  ctx.stroke();

  // Fill area under
  ctx.lineTo(pad.left + chartW, pad.top + chartH);
  ctx.lineTo(pad.left, pad.top + chartH);
  ctx.closePath();
  ctx.fillStyle = 'rgba(74, 222, 128, 0.08)';
  ctx.fill();

  // Current position marker
  if (allSnapshots.length > 1) {
    const cx = pad.left + (currentIdx / (n - 1)) * chartW;
    ctx.beginPath();
    ctx.strokeStyle = '#fff';
    ctx.lineWidth = 1;
    ctx.setLineDash([3, 3]);
    ctx.moveTo(cx, pad.top);
    ctx.lineTo(cx, pad.top + chartH);
    ctx.stroke();
    ctx.setLineDash([]);

    // Dot
    const sig = allSnapshots[currentIdx].connected_signal || 0;
    const cy = pad.top + chartH - (sig / 100) * chartH;
    ctx.beginPath();
    ctx.fillStyle = '#fff';
    ctx.arc(cx, cy, 4, 0, Math.PI * 2);
    ctx.fill();
  }

  // Time labels
  ctx.fillStyle = '#444';
  ctx.font = '8px monospace';
  ctx.textAlign = 'center';
  const labelCount = Math.min(6, n);
  for (let i = 0; i < labelCount; i++) {
    const idx = Math.floor(i * (n - 1) / (labelCount - 1));
    const x = pad.left + (idx / (n - 1)) * chartW;
    ctx.fillText(formatTime(allSnapshots[idx].timestamp), x, pad.top + chartH + 15);
  }
}

// Heatmap: rows = SSIDs, columns = time snapshots, cell color = signal
function renderHeatmap() {
  const el = document.getElementById('heatmap');
  if (allSnapshots.length < 2) {
    el.innerHTML = '<div style="color:#444;font-size:0.75rem;padding:0.5rem">Need more data...</div>';
    return;
  }

  // Collect all SSIDs seen
  const ssidSignals = {};
  allSnapshots.forEach((snap, i) => {
    snap.networks.forEach(n => {
      if (!ssidSignals[n.ssid]) ssidSignals[n.ssid] = new Array(allSnapshots.length).fill(0);
      ssidSignals[n.ssid][i] = n.signal;
    });
  });

  // Sort by average signal (most visible first), cap at 15
  const sorted = Object.entries(ssidSignals)
    .map(([ssid, signals]) => ({ ssid, signals, avg: signals.reduce((a, b) => a + b, 0) / signals.length }))
    .sort((a, b) => b.avg - a.avg)
    .slice(0, 15);

  // Downsample if too many snapshots
  const maxCells = 80;
  const step = Math.max(1, Math.floor(allSnapshots.length / maxCells));
  const indices = [];
  for (let i = 0; i < allSnapshots.length; i += step) indices.push(i);

  el.innerHTML = sorted.map(row => `
    <div class="heatmap-row">
      <span class="heatmap-label" title="${escapeHtml(row.ssid)}">${escapeHtml(row.ssid)}</span>
      <div class="heatmap-cells">
        ${indices.map(i => {
          const sig = row.signals[i] || 0;
          const bg = sig === 0 ? '#111' : signalColor(sig);
          const opacity = sig === 0 ? 0.3 : 0.3 + (sig / 100) * 0.7;
          return `<div class="heatmap-cell" style="background:${bg};opacity:${opacity}" title="${row.ssid} @ ${formatTime(allSnapshots[i].timestamp)}: ${sig}%"></div>`;
        }).join('')}
      </div>
    </div>
  `).join('');
}

// Resize handler
window.addEventListener('resize', () => { renderChart(); });

init();
</script>
</body>
</html>'''


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="WiFi Time Machine")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--interval", type=int, default=10, help="Scan interval in seconds")
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args()

    print(f"WiFi Time Machine")
    print(f"  Data: {LOG_FILE}")
    print(f"  Scan interval: {args.interval}s")
    print(f"  UI: http://localhost:{args.port}")
    print()

    # Load existing data count
    existing = load_history()
    if existing:
        print(f"  Loaded {len(existing)} historical snapshots")
        for snap in existing:
            snapshots_in_memory.append(snap)

    # Start collection thread
    collector = threading.Thread(target=collection_loop, args=(args.interval,), daemon=True)
    collector.start()
    print("  Collection started...")

    # Collect first snapshot immediately
    time.sleep(1)

    # Open browser
    if not args.no_browser:
        webbrowser.open(f"http://localhost:{args.port}")

    # Start HTTP server
    server = HTTPServer(("127.0.0.1", args.port), WifiHandler)
    print(f"  Server running on http://localhost:{args.port}")
    print(f"  Press Ctrl+C to stop\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        global collection_running
        collection_running = False
        print("\nStopped.")


if __name__ == "__main__":
    main()
