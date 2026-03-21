#!/usr/bin/env python3
"""
system-dash: Live system resource monitor in your browser.
Usage: python3 system_dash.py [--port 8900]
"""
import argparse, json, os, subprocess, time, threading, webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler

history = []
MAX_HISTORY = 360  # 30 min at 5s intervals

def get_cpu():
    try:
        with open('/proc/stat') as f:
            line = f.readline()
        vals = [int(x) for x in line.split()[1:]]
        return vals
    except: return [0]*10

prev_cpu = get_cpu()

def cpu_percent():
    global prev_cpu
    cur = get_cpu()
    d = [c - p for c, p in zip(cur, prev_cpu)]
    prev_cpu = cur
    total = sum(d)
    if total == 0: return 0
    idle = d[3] + d[4]
    return round(100 * (1 - idle / total), 1)

def mem_info():
    info = {}
    try:
        with open('/proc/meminfo') as f:
            for line in f:
                parts = line.split()
                if parts[0].rstrip(':') in ('MemTotal','MemAvailable','SwapTotal','SwapFree','Buffers','Cached'):
                    info[parts[0].rstrip(':')] = int(parts[1])
    except: pass
    total = info.get('MemTotal', 0)
    avail = info.get('MemAvailable', 0)
    used = total - avail
    return {'total_mb': total//1024, 'used_mb': used//1024, 'avail_mb': avail//1024,
            'percent': round(100*used/total,1) if total else 0,
            'swap_total_mb': info.get('SwapTotal',0)//1024,
            'swap_used_mb': (info.get('SwapTotal',0)-info.get('SwapFree',0))//1024}

def disk_info():
    try:
        result = subprocess.run(['df','-h','--output=target,size,used,avail,pcent','/'],
            capture_output=True, text=True, timeout=5)
        lines = result.stdout.strip().split('\n')
        if len(lines) >= 2:
            parts = lines[1].split()
            return {'mount':parts[0],'size':parts[1],'used':parts[2],'avail':parts[3],'percent':parts[4]}
    except: pass
    return {}

def load_avg():
    try:
        with open('/proc/loadavg') as f:
            parts = f.read().split()
        return [float(parts[0]), float(parts[1]), float(parts[2])]
    except: return [0,0,0]

def uptime():
    try:
        with open('/proc/uptime') as f:
            secs = float(f.read().split()[0])
        days = int(secs // 86400)
        hrs = int((secs % 86400) // 3600)
        mins = int((secs % 3600) // 60)
        return f"{days}d {hrs}h {mins}m"
    except: return "?"

def net_stats():
    try:
        with open('/proc/net/dev') as f:
            lines = f.readlines()[2:]
        total_rx, total_tx = 0, 0
        for line in lines:
            parts = line.split()
            iface = parts[0].rstrip(':')
            if iface == 'lo': continue
            total_rx += int(parts[1])
            total_tx += int(parts[9])
        return {'rx_bytes': total_rx, 'tx_bytes': total_tx}
    except: return {'rx_bytes':0, 'tx_bytes':0}

prev_net = net_stats()
prev_net_time = time.time()

def net_speed():
    global prev_net, prev_net_time
    cur = net_stats()
    now = time.time()
    dt = now - prev_net_time
    if dt < 0.1: dt = 1
    rx_speed = (cur['rx_bytes'] - prev_net['rx_bytes']) / dt
    tx_speed = (cur['tx_bytes'] - prev_net['tx_bytes']) / dt
    prev_net = cur
    prev_net_time = now
    return {'rx_mbps': round(rx_speed/1048576, 2), 'tx_mbps': round(tx_speed/1048576, 2),
            'rx_total_gb': round(cur['rx_bytes']/1073741824, 2), 'tx_total_gb': round(cur['tx_bytes']/1073741824, 2)}

def top_processes():
    try:
        result = subprocess.run(['ps','aux','--sort=-%cpu'], capture_output=True, text=True, timeout=5)
        procs = []
        for line in result.stdout.strip().split('\n')[1:11]:
            parts = line.split(None, 10)
            if len(parts) >= 11:
                procs.append({'user':parts[0],'pid':parts[1],'cpu':parts[2],'mem':parts[3],'cmd':parts[10][:60]})
        return procs
    except: return []

def snapshot():
    return {
        'time': time.strftime('%H:%M:%S'),
        'epoch': time.time(),
        'cpu': cpu_percent(),
        'mem': mem_info(),
        'disk': disk_info(),
        'load': load_avg(),
        'uptime': uptime(),
        'net': net_speed(),
        'procs': top_processes(),
    }

def collector(interval=5):
    while True:
        snap = snapshot()
        history.append(snap)
        if len(history) > MAX_HISTORY: history.pop(0)
        time.sleep(interval)

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        if self.path == '/':
            self.send_response(200); self.send_header('Content-Type','text/html'); self.end_headers()
            self.wfile.write(HTML.encode())
        elif self.path == '/api/snapshot':
            self.send_response(200); self.send_header('Content-Type','application/json'); self.end_headers()
            self.wfile.write(json.dumps(history[-1] if history else {}).encode())
        elif self.path == '/api/history':
            self.send_response(200); self.send_header('Content-Type','application/json'); self.end_headers()
            self.wfile.write(json.dumps(history).encode())
        else:
            self.send_response(404); self.end_headers()

HTML = r'''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>System Dashboard</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'SF Mono','Fira Code',monospace;background:#0a0a0a;color:#ccc;padding:1.5rem}
h1{font-size:1.2rem;color:#fff;margin-bottom:0.2rem}
.sub{color:#555;font-size:0.65rem;margin-bottom:1.5rem}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1rem;margin-bottom:1.5rem}
.card{background:#111;border:1px solid #1a1a1a;border-radius:8px;padding:1rem}
.card-title{font-size:0.6rem;color:#555;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.5rem}
.card-big{font-size:2rem;font-weight:bold;color:#fff}
.card-sub{font-size:0.7rem;color:#666;margin-top:0.2rem}
.bar-bg{height:8px;background:#1a1a1a;border-radius:4px;overflow:hidden;margin-top:0.5rem}
.bar-fill{height:100%;border-radius:4px;transition:width 0.5s}
.chart-container{background:#111;border:1px solid #1a1a1a;border-radius:8px;padding:1rem;margin-bottom:1.5rem}
canvas{width:100%;height:120px}
.proc-table{width:100%;border-collapse:collapse;font-size:0.7rem}
.proc-table th{text-align:left;padding:0.3rem 0.5rem;color:#555;border-bottom:1px solid #1a1a1a;font-size:0.6rem;text-transform:uppercase}
.proc-table td{padding:0.3rem 0.5rem;border-bottom:1px solid #111}
.proc-table tr:hover td{background:#111}
</style></head><body>
<h1>System Dashboard</h1>
<p class="sub" id="uptime"></p>
<div class="grid" id="cards"></div>
<div class="chart-container"><div class="card-title">CPU & Memory History</div><canvas id="chart"></canvas></div>
<div class="card-title" style="margin-bottom:0.5rem">Top Processes</div>
<table class="proc-table"><thead><tr><th>User</th><th>PID</th><th>CPU%</th><th>MEM%</th><th>Command</th></tr></thead>
<tbody id="procs"></tbody></table>
<script>
let historyData = [];
async function poll() {
  try {
    const r = await fetch('/api/history');
    historyData = await r.json();
    if (historyData.length > 0) renderSnapshot(historyData[historyData.length-1]);
    renderChart();
  } catch(e) {}
}

function barColor(pct) {
  if (pct < 50) return '#4ade80';
  if (pct < 80) return '#fbbf24';
  return '#f87171';
}

function renderSnapshot(s) {
  document.getElementById('uptime').textContent = 'Uptime: ' + s.uptime + ' | Load: ' + s.load.join(', ');
  document.getElementById('cards').innerHTML = `
    <div class="card"><div class="card-title">CPU</div><div class="card-big" style="color:${barColor(s.cpu)}">${s.cpu}%</div>
      <div class="bar-bg"><div class="bar-fill" style="width:${s.cpu}%;background:${barColor(s.cpu)}"></div></div></div>
    <div class="card"><div class="card-title">Memory</div><div class="card-big" style="color:${barColor(s.mem.percent)}">${s.mem.percent}%</div>
      <div class="card-sub">${s.mem.used_mb} / ${s.mem.total_mb} MB</div>
      <div class="bar-bg"><div class="bar-fill" style="width:${s.mem.percent}%;background:${barColor(s.mem.percent)}"></div></div></div>
    <div class="card"><div class="card-title">Disk (/)</div><div class="card-big">${s.disk.percent||'?'}</div>
      <div class="card-sub">${s.disk.used||'?'} / ${s.disk.size||'?'}</div></div>
    <div class="card"><div class="card-title">Network</div><div class="card-big" style="font-size:1.2rem">${s.net.rx_mbps} / ${s.net.tx_mbps}</div>
      <div class="card-sub">MB/s (rx/tx) | Total: ${s.net.rx_total_gb}/${s.net.tx_total_gb} GB</div></div>
  `;
  document.getElementById('procs').innerHTML = s.procs.map(p =>
    `<tr><td>${p.user}</td><td>${p.pid}</td><td>${p.cpu}</td><td>${p.mem}</td><td style="color:#888;max-width:300px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${p.cmd}</td></tr>`
  ).join('');
}

function renderChart() {
  const canvas = document.getElementById('chart');
  const ctx = canvas.getContext('2d');
  const rect = canvas.parentElement.getBoundingClientRect();
  canvas.width = (rect.width - 32) * 2; canvas.height = 240;
  ctx.scale(2,2); const W = (rect.width-32), H = 120;
  ctx.clearRect(0,0,W,H);
  if (historyData.length < 2) return;
  const n = historyData.length;
  // CPU line
  ctx.beginPath(); ctx.strokeStyle = '#4ade80'; ctx.lineWidth = 1.5;
  historyData.forEach((s,i) => { const x = i/(n-1)*W, y = H - s.cpu/100*H; i===0?ctx.moveTo(x,y):ctx.lineTo(x,y); });
  ctx.stroke();
  // Memory line
  ctx.beginPath(); ctx.strokeStyle = '#60a5fa'; ctx.lineWidth = 1.5;
  historyData.forEach((s,i) => { const x = i/(n-1)*W, y = H - s.mem.percent/100*H; i===0?ctx.moveTo(x,y):ctx.lineTo(x,y); });
  ctx.stroke();
  // Legend
  ctx.fillStyle='#4ade80'; ctx.fillRect(W-100,5,10,3); ctx.fillStyle='#4ade80'; ctx.font='8px monospace'; ctx.fillText('CPU',W-86,9);
  ctx.fillStyle='#60a5fa'; ctx.fillRect(W-55,5,10,3); ctx.fillStyle='#60a5fa'; ctx.fillText('MEM',W-41,9);
}

poll(); setInterval(poll, 5000);
</script></body></html>'''

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8900)
    parser.add_argument('--no-browser', action='store_true')
    args = parser.parse_args()
    # Initial snapshot
    cpu_percent(); time.sleep(0.2)
    history.append(snapshot())
    t = threading.Thread(target=collector, daemon=True); t.start()
    print(f"System Dashboard: http://localhost:{args.port}")
    if not args.no_browser: webbrowser.open(f'http://localhost:{args.port}')
    server = HTTPServer(('0.0.0.0', args.port), Handler)
    try: server.serve_forever()
    except KeyboardInterrupt: print('\nStopped.')

if __name__ == '__main__': main()
