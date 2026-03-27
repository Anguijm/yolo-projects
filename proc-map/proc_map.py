#!/usr/bin/env python3
"""
proc_map.py - Process visualization tool.
Snapshots all running processes and generates an interactive HTML force-directed
graph showing parent-child relationships, CPU/memory usage, and more.

Zero external dependencies - stdlib only. Works on Linux.
"""

import subprocess
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path


def get_processes():
    """Collect process data using ps and /proc filesystem."""
    # Use ps to get process info
    cmd = ["ps", "-eo", "pid,ppid,user,%cpu,%mem,rss,vsz,stat,start_time,comm,args", "--no-headers"]
    result = subprocess.run(cmd, capture_output=True, text=True)

    processes = {}
    for line in result.stdout.strip().split("\n"):
        if not line.strip():
            continue
        parts = line.split(None, 10)
        if len(parts) < 10:
            continue
        try:
            pid = int(parts[0])
            ppid = int(parts[1])
        except ValueError:
            continue

        user = parts[2]
        try:
            cpu = float(parts[3])
        except ValueError:
            cpu = 0.0
        try:
            mem = float(parts[4])
        except ValueError:
            mem = 0.0
        try:
            rss = int(parts[5])
        except ValueError:
            rss = 0
        try:
            vsz = int(parts[6])
        except ValueError:
            vsz = 0
        stat = parts[7]
        start_time = parts[8]
        comm = parts[9]
        args = parts[10] if len(parts) > 10 else comm

        # Try to get uptime from /proc
        uptime_str = ""
        try:
            proc_stat = Path(f"/proc/{pid}/stat").read_text()
            boot_time = float(Path("/proc/uptime").read_text().split()[0])
            clk_tck = os.sysconf("SC_CLK_TCK")
            # Parse after last ')' to handle spaces in process names
            close_paren = proc_stat.rfind(')')
            if close_paren == -1:
                raise ValueError("malformed /proc/pid/stat")
            tokens = proc_stat[close_paren + 1:].split()
            # starttime is field 22 overall; after stripping pid and (comm), it's index 19
            start_ticks = int(tokens[19])
            proc_uptime_sec = boot_time - (start_ticks / clk_tck)
            if proc_uptime_sec < 0:
                proc_uptime_sec = 0
            hours = int(proc_uptime_sec // 3600)
            minutes = int((proc_uptime_sec % 3600) // 60)
            seconds = int(proc_uptime_sec % 60)
            uptime_str = f"{hours}h {minutes}m {seconds}s"
        except Exception:
            uptime_str = start_time

        processes[pid] = {
            "pid": pid,
            "ppid": ppid,
            "user": user,
            "cpu": cpu,
            "mem": mem,
            "rss_kb": rss,
            "vsz_kb": vsz,
            "stat": stat,
            "start_time": start_time,
            "comm": comm,
            "args": args[:120],  # truncate long args
            "uptime": uptime_str,
        }

    return processes


def build_graph(processes):
    """Build nodes and links for the force-directed graph."""
    nodes = []
    links = []
    pid_set = set(processes.keys())

    for pid, p in processes.items():
        nodes.append({
            "id": pid,
            "comm": p["comm"],
            "user": p["user"],
            "cpu": p["cpu"],
            "mem": p["mem"],
            "rss_kb": p["rss_kb"],
            "args": p["args"],
            "uptime": p["uptime"],
            "ppid": p["ppid"],
        })
        if p["ppid"] in pid_set and p["ppid"] != pid:
            links.append({"source": p["ppid"], "target": pid})

    return nodes, links


def format_kb(kb):
    """Format KB value for display."""
    if kb > 1048576:
        return f"{kb / 1048576:.1f} GB"
    if kb > 1024:
        return f"{kb / 1024:.1f} MB"
    return f"{kb} KB"


def generate_html(nodes, links, processes):
    """Generate self-contained HTML with embedded JS force simulation."""

    # Build the table rows data
    table_data = []
    for p in sorted(processes.values(), key=lambda x: x["cpu"], reverse=True):
        table_data.append({
            "pid": p["pid"],
            "ppid": p["ppid"],
            "comm": p["comm"],
            "user": p["user"],
            "cpu": p["cpu"],
            "mem": p["mem"],
            "rss": format_kb(p["rss_kb"]),
            "rss_kb": p["rss_kb"],
            "args": p["args"],
            "uptime": p["uptime"],
        })

    nodes_json = json.dumps(nodes).replace('<', '\\u003c').replace('>', '\\u003e')
    links_json = json.dumps(links).replace('<', '\\u003c').replace('>', '\\u003e')
    table_json = json.dumps(table_data).replace('<', '\\u003c').replace('>', '\\u003e')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    num_procs = len(nodes)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>proc-map | Process Visualization</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0a0a0f; color: #e0e0e0; display: flex; height: 100vh; overflow: hidden; }}
#graph-container {{ flex: 1; position: relative; }}
canvas {{ display: block; }}
#sidebar {{ width: 420px; background: #12121a; border-left: 1px solid #2a2a3a; display: flex; flex-direction: column; overflow: hidden; }}
#sidebar-header {{ padding: 12px 16px; background: #1a1a2a; border-bottom: 1px solid #2a2a3a; }}
#sidebar-header h2 {{ font-size: 14px; color: #8888aa; margin-bottom: 8px; }}
#search {{ width: 100%; padding: 8px 12px; background: #0a0a14; border: 1px solid #2a2a3a; border-radius: 4px; color: #e0e0e0; font-size: 13px; outline: none; }}
#search:focus {{ border-color: #4488ff; }}
#sort-controls {{ display: flex; gap: 4px; margin-top: 8px; flex-wrap: wrap; }}
.sort-btn {{ padding: 4px 8px; font-size: 11px; background: #1a1a2e; border: 1px solid #2a2a3a; color: #8888aa; border-radius: 3px; cursor: pointer; }}
.sort-btn:hover, .sort-btn.active {{ background: #2a2a4a; color: #aaaacc; border-color: #4488ff; }}
#table-container {{ flex: 1; overflow-y: auto; }}
#table-container::-webkit-scrollbar {{ width: 6px; }}
#table-container::-webkit-scrollbar-track {{ background: #12121a; }}
#table-container::-webkit-scrollbar-thumb {{ background: #2a2a3a; border-radius: 3px; }}
table {{ width: 100%; border-collapse: collapse; font-size: 12px; }}
thead {{ position: sticky; top: 0; background: #1a1a2a; z-index: 1; }}
th {{ padding: 8px 6px; text-align: left; color: #6666aa; font-weight: 600; cursor: pointer; user-select: none; white-space: nowrap; }}
th:hover {{ color: #8888cc; }}
td {{ padding: 5px 6px; border-bottom: 1px solid #1a1a22; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 120px; }}
tr:hover {{ background: #1a1a2e; }}
tr.highlighted {{ background: #1a2a3a; }}
.cpu-bar {{ display: inline-block; height: 10px; border-radius: 2px; min-width: 2px; }}
#tooltip {{ position: absolute; background: #1a1a2aee; border: 1px solid #3a3a5a; border-radius: 6px; padding: 10px 14px; font-size: 12px; pointer-events: none; display: none; z-index: 100; max-width: 350px; line-height: 1.6; }}
#tooltip .tt-comm {{ font-size: 14px; font-weight: bold; color: #ffffff; }}
#tooltip .tt-row {{ color: #aaaacc; }}
#tooltip .tt-label {{ color: #6666aa; }}
#info-bar {{ position: absolute; top: 12px; left: 12px; background: #12121aee; border: 1px solid #2a2a3a; border-radius: 6px; padding: 10px 16px; font-size: 12px; color: #8888aa; z-index: 10; }}
#info-bar h1 {{ font-size: 16px; color: #ccccee; margin-bottom: 4px; }}
#legend {{ position: absolute; bottom: 12px; left: 12px; background: #12121aee; border: 1px solid #2a2a3a; border-radius: 6px; padding: 10px 16px; font-size: 11px; color: #8888aa; z-index: 10; }}
.legend-gradient {{ width: 150px; height: 12px; border-radius: 3px; margin: 4px 0; }}
</style>
</head>
<body>
<div id="graph-container">
  <canvas id="canvas"></canvas>
  <div id="tooltip"></div>
  <div id="info-bar">
    <h1>proc-map</h1>
    <div>{num_procs} processes | {timestamp}</div>
  </div>
  <div id="legend">
    <div><strong>Node size</strong> = memory usage</div>
    <div><strong>Node color</strong> = CPU usage</div>
    <div style="display:flex;align-items:center;gap:6px;margin-top:4px;">
      <span>0%</span>
      <div class="legend-gradient" style="background: linear-gradient(to right, #2244aa, #44aaff, #ffaa00, #ff4444);"></div>
      <span>100%</span>
    </div>
    <div style="margin-top:4px;">Click node to highlight tree branch</div>
  </div>
</div>
<div id="sidebar">
  <div id="sidebar-header">
    <h2>PROCESS LIST</h2>
    <input type="text" id="search" placeholder="Filter by process name, user, or PID...">
    <div id="sort-controls">
      <button class="sort-btn active" data-sort="cpu">CPU %</button>
      <button class="sort-btn" data-sort="mem">MEM %</button>
      <button class="sort-btn" data-sort="rss_kb">RSS</button>
      <button class="sort-btn" data-sort="pid">PID</button>
      <button class="sort-btn" data-sort="comm">Name</button>
    </div>
  </div>
  <div id="table-container">
    <table>
      <thead>
        <tr>
          <th data-col="pid">PID</th>
          <th data-col="user">User</th>
          <th data-col="comm">Name</th>
          <th data-col="cpu">CPU%</th>
          <th data-col="mem">MEM%</th>
          <th data-col="rss">RSS</th>
        </tr>
      </thead>
      <tbody id="proc-tbody"></tbody>
    </table>
  </div>
</div>

<script>
// Data
const rawNodes = {nodes_json};
const rawLinks = {links_json};
const tableData = {table_json};

// --- Force-directed graph on Canvas ---
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const container = document.getElementById('graph-container');
const tooltip = document.getElementById('tooltip');

let W, H;
function resize() {{
  W = container.clientWidth;
  H = container.clientHeight;
  canvas.width = W * devicePixelRatio;
  canvas.height = H * devicePixelRatio;
  canvas.style.width = W + 'px';
  canvas.style.height = H + 'px';
  ctx.setTransform(devicePixelRatio, 0, 0, devicePixelRatio, 0, 0);
}}
resize();
window.addEventListener('resize', resize);

// Build node map
const nodeMap = {{}};
const nodes = rawNodes.map(n => {{
  const obj = {{
    ...n,
    x: W/2 + (Math.random() - 0.5) * W * 0.6,
    y: H/2 + (Math.random() - 0.5) * H * 0.6,
    vx: 0, vy: 0,
    radius: Math.max(3, Math.min(20, Math.sqrt(n.rss_kb / 1024) * 2.5)),
  }};
  nodeMap[n.id] = obj;
  return obj;
}});

const links = rawLinks.filter(l => nodeMap[l.source] && nodeMap[l.target]).map(l => ({{
  source: nodeMap[l.source],
  target: nodeMap[l.target],
}}));

// Build children map for tree highlighting
const childrenMap = {{}};
links.forEach(l => {{
  if (!childrenMap[l.source.id]) childrenMap[l.source.id] = [];
  childrenMap[l.source.id].push(l.target.id);
}});

function getDescendants(pid) {{
  const result = new Set([pid]);
  const stack = [pid];
  while (stack.length) {{
    const p = stack.pop();
    (childrenMap[p] || []).forEach(c => {{
      if (!result.has(c)) {{ result.add(c); stack.push(c); }}
    }});
  }}
  return result;
}}

function getAncestors(pid) {{
  const result = new Set();
  let cur = nodeMap[pid];
  while (cur && cur.ppid !== cur.id) {{
    result.add(cur.id);
    cur = nodeMap[cur.ppid];
    if (cur && result.has(cur.id)) break;
  }}
  if (cur) result.add(cur.id);
  return result;
}}

// Color mapping: CPU% -> color
function cpuColor(cpu) {{
  const t = Math.min(cpu / 50, 1); // 0-50% maps to full range
  let r, g, b;
  if (t < 0.33) {{
    const s = t / 0.33;
    r = Math.round(34 + s * 34);
    g = Math.round(68 + s * 102);
    b = Math.round(170 + s * 85);
  }} else if (t < 0.66) {{
    const s = (t - 0.33) / 0.33;
    r = Math.round(68 + s * 187);
    g = Math.round(170 + s * 0);
    b = Math.round(255 - s * 255);
  }} else {{
    const s = (t - 0.66) / 0.34;
    r = Math.round(255);
    g = Math.round(170 - s * 102);
    b = Math.round(0);
  }}
  return `rgb(${{r}},${{g}},${{b}})`;
}}

// Force simulation
const ALPHA_DECAY = 0.002;
const VELOCITY_DECAY = 0.4;
let alpha = 1;
let selectedPid = null;
let highlightSet = null;

function simulate() {{
  alpha = Math.max(alpha - ALPHA_DECAY, 0.001);

  // Center gravity
  nodes.forEach(n => {{
    n.vx += (W/2 - n.x) * 0.0005 * alpha;
    n.vy += (H/2 - n.y) * 0.0005 * alpha;
  }});

  // Repulsion (approximate with grid)
  for (let i = 0; i < nodes.length; i++) {{
    for (let j = i + 1; j < nodes.length; j++) {{
      let dx = nodes[j].x - nodes[i].x;
      let dy = nodes[j].y - nodes[i].y;
      let d2 = dx*dx + dy*dy;
      if (d2 < 1) d2 = 1;
      if (d2 > 40000) continue; // skip far nodes
      const f = alpha * 80 / d2;
      const fx = dx * f;
      const fy = dy * f;
      nodes[i].vx -= fx;
      nodes[i].vy -= fy;
      nodes[j].vx += fx;
      nodes[j].vy += fy;
    }}
  }}

  // Link spring force
  links.forEach(l => {{
    let dx = l.target.x - l.source.x;
    let dy = l.target.y - l.source.y;
    let d = Math.sqrt(dx*dx + dy*dy) || 1;
    const desired = 40;
    const f = (d - desired) * 0.02 * alpha;
    const fx = (dx / d) * f;
    const fy = (dy / d) * f;
    l.source.vx += fx;
    l.source.vy += fy;
    l.target.vx -= fx;
    l.target.vy -= fy;
  }});

  // Apply velocity
  nodes.forEach(n => {{
    if (n.dragging) return;
    n.vx *= VELOCITY_DECAY;
    n.vy *= VELOCITY_DECAY;
    n.x += n.vx;
    n.y += n.vy;
    // Keep in bounds
    n.x = Math.max(n.radius, Math.min(W - n.radius, n.x));
    n.y = Math.max(n.radius, Math.min(H - n.radius, n.y));
  }});
}}

function draw() {{
  ctx.clearRect(0, 0, W, H);

  // Draw links
  ctx.lineWidth = 0.5;
  links.forEach(l => {{
    const inHighlight = highlightSet && highlightSet.has(l.source.id) && highlightSet.has(l.target.id);
    ctx.strokeStyle = highlightSet ? (inHighlight ? '#4488ff55' : '#ffffff08') : '#ffffff12';
    ctx.beginPath();
    ctx.moveTo(l.source.x, l.source.y);
    ctx.lineTo(l.target.x, l.target.y);
    ctx.stroke();
  }});

  // Draw nodes
  nodes.forEach(n => {{
    const inHighlight = !highlightSet || highlightSet.has(n.id);
    const a = inHighlight ? 1.0 : 0.1;
    ctx.globalAlpha = a;
    ctx.fillStyle = cpuColor(n.cpu);
    ctx.beginPath();
    ctx.arc(n.x, n.y, n.radius, 0, Math.PI * 2);
    ctx.fill();

    // Label for bigger nodes
    if (n.radius > 6 && inHighlight) {{
      ctx.fillStyle = '#ffffffcc';
      ctx.font = '10px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(n.comm, n.x, n.y - n.radius - 3);
    }}
    ctx.globalAlpha = 1.0;
  }});
}}

function tick() {{
  simulate();
  draw();
  requestAnimationFrame(tick);
}}
tick();

// --- Mouse interaction ---
let hovered = null;
let dragNode = null;

function findNode(mx, my) {{
  for (let i = nodes.length - 1; i >= 0; i--) {{
    const n = nodes[i];
    const dx = mx - n.x;
    const dy = my - n.y;
    if (dx*dx + dy*dy < (n.radius + 4) * (n.radius + 4)) return n;
  }}
  return null;
}}

canvas.addEventListener('mousemove', e => {{
  const rect = canvas.getBoundingClientRect();
  const mx = e.clientX - rect.left;
  const my = e.clientY - rect.top;

  if (dragNode) {{
    dragNode.x = mx;
    dragNode.y = my;
    dragNode.vx = 0;
    dragNode.vy = 0;
    alpha = Math.max(alpha, 0.1);
    return;
  }}

  const n = findNode(mx, my);
  if (n) {{
    hovered = n;
    canvas.style.cursor = 'pointer';
    tooltip.style.display = 'block';
    tooltip.innerHTML = `
      <div class="tt-comm">${{n.comm}} <span style="color:#6666aa">(PID ${{n.id}})</span></div>
      <div class="tt-row"><span class="tt-label">User:</span> ${{n.user}}</div>
      <div class="tt-row"><span class="tt-label">CPU:</span> ${{n.cpu}}%</div>
      <div class="tt-row"><span class="tt-label">MEM:</span> ${{n.mem}}%</div>
      <div class="tt-row"><span class="tt-label">RSS:</span> ${{(n.rss_kb/1024).toFixed(1)}} MB</div>
      <div class="tt-row"><span class="tt-label">Uptime:</span> ${{n.uptime}}</div>
      <div class="tt-row" style="color:#666;font-size:11px;margin-top:2px">${{n.args}}</div>
    `;
    let tx = e.clientX + 12;
    let ty = e.clientY + 12;
    if (tx + 300 > window.innerWidth) tx = e.clientX - 310;
    if (ty + 150 > window.innerHeight) ty = e.clientY - 160;
    tooltip.style.left = tx + 'px';
    tooltip.style.top = ty + 'px';
  }} else {{
    hovered = null;
    canvas.style.cursor = 'default';
    tooltip.style.display = 'none';
  }}
}});

canvas.addEventListener('mousedown', e => {{
  const rect = canvas.getBoundingClientRect();
  const mx = e.clientX - rect.left;
  const my = e.clientY - rect.top;
  const n = findNode(mx, my);
  if (n) {{
    dragNode = n;
    n.dragging = true;
  }}
}});

canvas.addEventListener('mouseup', e => {{
  if (dragNode) {{
    const rect = canvas.getBoundingClientRect();
    const mx = e.clientX - rect.left;
    const my = e.clientY - rect.top;
    // Check if it was a click (not a drag)
    const dx = mx - dragNode.x;
    const dy = my - dragNode.y;
    dragNode.dragging = false;

    // Toggle highlight on click
    if (selectedPid === dragNode.id) {{
      selectedPid = null;
      highlightSet = null;
      highlightTableRows(null);
    }} else {{
      selectedPid = dragNode.id;
      const desc = getDescendants(dragNode.id);
      const anc = getAncestors(dragNode.id);
      highlightSet = new Set([...desc, ...anc]);
      highlightTableRows(highlightSet);
    }}
    dragNode = null;
  }}
}});

canvas.addEventListener('mouseleave', () => {{
  tooltip.style.display = 'none';
  if (dragNode) {{
    dragNode.dragging = false;
    dragNode = null;
  }}
}});

// --- Sidebar table ---
let currentSort = 'cpu';
let sortDir = -1; // -1 = descending
let filterText = '';

const tbody = document.getElementById('proc-tbody');
const searchInput = document.getElementById('search');

function renderTable() {{
  let data = tableData.filter(p => {{
    if (!filterText) return true;
    const q = filterText.toLowerCase();
    return p.comm.toLowerCase().includes(q) || p.user.toLowerCase().includes(q) || String(p.pid).includes(q) || p.args.toLowerCase().includes(q);
  }});

  data.sort((a, b) => {{
    let va = a[currentSort], vb = b[currentSort];
    if (typeof va === 'string') {{ va = va.toLowerCase(); vb = vb.toLowerCase(); }}
    if (va < vb) return -sortDir;
    if (va > vb) return sortDir;
    return 0;
  }});

  let html = '';
  data.forEach(p => {{
    const hl = highlightSet && highlightSet.has(p.pid) ? ' highlighted' : '';
    const cpuW = Math.min(p.cpu * 2, 100);
    html += `<tr class="${{hl}}" data-pid="${{p.pid}}">
      <td>${{p.pid}}</td>
      <td>${{p.user}}</td>
      <td title="${{p.args}}">${{p.comm}}</td>
      <td><span class="cpu-bar" style="width:${{cpuW}}px;background:${{cpuColor(p.cpu)}}"></span> ${{p.cpu}}</td>
      <td>${{p.mem}}</td>
      <td>${{p.rss}}</td>
    </tr>`;
  }});
  tbody.innerHTML = html;
}}

// Event delegation for table row clicks (avoids listener leak on re-render)
tbody.addEventListener('click', function(e) {{
  const tr = e.target.closest('tr[data-pid]');
  if (!tr) return;
  const pid = parseInt(tr.dataset.pid);
  if (selectedPid === pid) {{
    selectedPid = null;
    highlightSet = null;
    highlightTableRows(null);
  }} else {{
    selectedPid = pid;
    const desc = getDescendants(pid);
    const anc = getAncestors(pid);
    highlightSet = new Set([...desc, ...anc]);
    highlightTableRows(highlightSet);
  }}
}});

function highlightTableRows(pidSet) {{
  tbody.querySelectorAll('tr').forEach(tr => {{
    const pid = parseInt(tr.dataset.pid);
    if (!pidSet) {{
      tr.classList.remove('highlighted');
    }} else {{
      tr.classList.toggle('highlighted', pidSet.has(pid));
    }}
  }});
}}

searchInput.addEventListener('input', e => {{
  filterText = e.target.value;
  renderTable();
}});

document.querySelectorAll('.sort-btn').forEach(btn => {{
  btn.addEventListener('click', () => {{
    const s = btn.dataset.sort;
    if (currentSort === s) {{ sortDir *= -1; }}
    else {{ currentSort = s; sortDir = -1; }}
    document.querySelectorAll('.sort-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    renderTable();
  }});
}});

document.querySelectorAll('th[data-col]').forEach(th => {{
  th.addEventListener('click', () => {{
    const col = th.dataset.col;
    if (currentSort === col) {{ sortDir *= -1; }}
    else {{ currentSort = col; sortDir = -1; }}
    renderTable();
  }});
}});

renderTable();
</script>
</body>
</html>"""
    return html


def main():
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "proc_map.html")
    if len(sys.argv) > 1:
        output_path = sys.argv[1]

    print(f"Collecting process data...")
    processes = get_processes()
    print(f"Found {len(processes)} processes")

    print(f"Building graph...")
    nodes, links = build_graph(processes)
    print(f"Graph: {len(nodes)} nodes, {len(links)} edges")

    print(f"Generating HTML...")
    html = generate_html(nodes, links, processes)

    with open(output_path, "w") as f:
        f.write(html)

    print(f"Output written to: {output_path}")
    print(f"File size: {os.path.getsize(output_path) / 1024:.1f} KB")
    return output_path


if __name__ == "__main__":
    main()
