#!/usr/bin/env python3
"""
file-treemap: Scan any directory and visualize disk usage as an interactive treemap.

Usage:
  python3 file_treemap.py [path]           # Scan and generate HTML
  python3 file_treemap.py ~/projects -o out.html
"""

import argparse
import json
import os
import sys
from pathlib import Path


def scan_directory(root, max_depth=6):
    """Scan directory and return nested structure."""
    root = Path(root).resolve()
    if not root.is_dir():
        print(f"Error: {root} is not a directory")
        sys.exit(1)

    print(f"Scanning {root}...")

    def scan(path, depth=0):
        name = path.name or str(path)
        if path.is_file():
            try:
                size = path.stat().st_size
            except (OSError, PermissionError):
                size = 0
            ext = path.suffix.lstrip('.') or 'none'
            return {'name': name, 'size': size, 'ext': ext, 'type': 'file'}

        if depth > max_depth:
            # Summarize deep directories
            total = 0
            count = 0
            try:
                for p in path.rglob('*'):
                    if p.is_file():
                        try:
                            total += p.stat().st_size
                            count += 1
                        except (OSError, PermissionError):
                            pass
            except (OSError, PermissionError):
                pass
            return {'name': name + '/', 'size': total, 'type': 'dir', 'children': [], 'file_count': count}

        children = []
        try:
            entries = sorted(path.iterdir(), key=lambda p: p.name)
        except (OSError, PermissionError):
            return {'name': name + '/', 'size': 0, 'type': 'dir', 'children': []}

        for entry in entries:
            # Skip hidden and common junk
            if entry.name.startswith('.') or entry.name in ('node_modules', '__pycache__', '.git', 'venv', '.venv'):
                # Still count size
                total = 0
                try:
                    if entry.is_file():
                        total = entry.stat().st_size
                    else:
                        for p in entry.rglob('*'):
                            if p.is_file():
                                try:
                                    total += p.stat().st_size
                                except (OSError, PermissionError):
                                    pass
                except (OSError, PermissionError):
                    pass
                if total > 0:
                    children.append({'name': entry.name + ('/' if entry.is_dir() else ''), 'size': total, 'type': 'dir' if entry.is_dir() else 'file', 'ext': 'hidden', 'children': []})
                continue

            child = scan(entry, depth + 1)
            if child and child['size'] > 0:
                children.append(child)

        total = sum(c['size'] for c in children)
        return {'name': name + '/', 'size': total, 'type': 'dir', 'children': children}

    tree = scan(root)
    return tree


def format_bytes(b):
    if b < 1024: return f"{b} B"
    if b < 1048576: return f"{b/1024:.1f} KB"
    if b < 1073741824: return f"{b/1048576:.1f} MB"
    return f"{b/1073741824:.1f} GB"


HTML_TEMPLATE = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>File Treemap: __ROOT_NAME__</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'SF Mono', 'Fira Code', monospace; background: #0a0a0a; color: #ccc; }
.header { padding: 1rem 1.5rem; border-bottom: 1px solid #1a1a1a; display: flex; align-items: center; gap: 1rem; }
.header h1 { font-size: 1.2rem; color: #fff; }
.header .size { color: #4ade80; font-size: 0.85rem; }
.breadcrumb { padding: 0.5rem 1.5rem; font-size: 0.75rem; color: #555; border-bottom: 1px solid #1a1a1a; background: #0d0d0d; min-height: 2rem; }
.breadcrumb span { cursor: pointer; color: #60a5fa; }
.breadcrumb span:hover { text-decoration: underline; }
.treemap { width: 100%; height: calc(100vh - 100px); position: relative; overflow: hidden; }
.cell { position: absolute; overflow: hidden; border: 1px solid #0a0a0a; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: opacity 0.1s; }
.cell:hover { opacity: 0.8; }
.cell-label { font-size: 0.6rem; color: rgba(255,255,255,0.85); text-align: center; padding: 3px; word-break: break-all; text-shadow: 0 1px 3px rgba(0,0,0,0.9); pointer-events: none; overflow: hidden; max-height: 100%; }
.tooltip { position: fixed; background: #1a1a1a; border: 1px solid #333; border-radius: 6px; padding: 0.6rem 0.8rem; font-size: 0.75rem; pointer-events: none; z-index: 100; display: none; max-width: 300px; }
.tt-name { color: #fff; font-weight: bold; margin-bottom: 0.2rem; word-break: break-all; }
.tt-row { display: flex; justify-content: space-between; gap: 1rem; }
.tt-key { color: #666; }
.tt-val { color: #ccc; }
</style>
</head>
<body>

<div class="header">
  <h1>File Treemap</h1>
  <span class="size" id="total-size"></span>
</div>
<div class="breadcrumb" id="breadcrumb"></div>
<div class="treemap" id="treemap"></div>
<div class="tooltip" id="tooltip"></div>

<script>
const DATA = __DATA__;

const EXT_COLORS = {
  py:'#3572A5', js:'#f1e05a', ts:'#3178c6', tsx:'#3178c6', jsx:'#f1e05a',
  rs:'#dea584', go:'#00ADD8', java:'#b07219', c:'#555', cpp:'#f34b7d',
  h:'#555', rb:'#701516', php:'#4F5D95', css:'#563d7c', html:'#e34c26',
  md:'#083fa1', json:'#666', yaml:'#cb171e', yml:'#cb171e', toml:'#9c4221',
  sh:'#89e051', sql:'#e38c00', svg:'#ff9900', png:'#a66', jpg:'#a66',
  txt:'#888', log:'#555', lock:'#444', hidden:'#333',
  none:'#4a4a4a'
};

function extColor(ext) { return EXT_COLORS[ext] || '#3a3a3a'; }

function formatBytes(b) {
  if (b < 1024) return b + ' B';
  if (b < 1048576) return (b/1024).toFixed(1) + ' KB';
  if (b < 1073741824) return (b/1048576).toFixed(1) + ' MB';
  return (b/1073741824).toFixed(1) + ' GB';
}

const tooltip = document.getElementById('tooltip');
let pathStack = [DATA];

function layout(items, x, y, w, h) {
  const rects = [];
  if (items.length === 0 || w < 1 || h < 1) return rects;

  const totalSize = items.reduce((s, i) => s + i.size, 0);
  if (totalSize === 0) return rects;

  function recurse(list, rx, ry, rw, rh) {
    if (list.length === 0 || rw < 1 || rh < 1) return;
    if (list.length === 1) {
      rects.push({ item: list[0], x: rx, y: ry, w: rw, h: rh });
      return;
    }
    const total = list.reduce((s, i) => s + i.size, 0);
    const half = total / 2;
    let acc = 0, split = 1;
    for (let i = 0; i < list.length; i++) {
      acc += list[i].size;
      if (acc >= half) { split = i + 1; break; }
    }
    split = Math.max(1, Math.min(split, list.length - 1));
    const leftSize = list.slice(0, split).reduce((s, i) => s + i.size, 0);
    const ratio = leftSize / total;
    if (rw >= rh) {
      recurse(list.slice(0, split), rx, ry, rw * ratio, rh);
      recurse(list.slice(split), rx + rw * ratio, ry, rw * (1 - ratio), rh);
    } else {
      recurse(list.slice(0, split), rx, ry, rw, rh * ratio);
      recurse(list.slice(split), rx, ry + rh * ratio, rw, rh * (1 - ratio));
    }
  }

  const sorted = [...items].sort((a, b) => b.size - a.size);
  recurse(sorted, x, y, w, h);
  return rects;
}

function render() {
  const current = pathStack[pathStack.length - 1];
  const container = document.getElementById('treemap');
  const W = container.clientWidth;
  const H = container.clientHeight;

  document.getElementById('total-size').textContent = formatBytes(current.size);

  // Breadcrumb
  const bc = document.getElementById('breadcrumb');
  bc.innerHTML = pathStack.map((p, i) =>
    i < pathStack.length - 1
      ? `<span onclick="navigateTo(${i})">${p.name}</span> / `
      : p.name
  ).join('');

  const items = current.children || [current];
  const rects = layout(items, 0, 0, W, H);

  container.innerHTML = rects.map((r, i) => {
    const ext = r.item.ext || (r.item.type === 'dir' ? 'none' : 'none');
    const bg = r.item.type === 'dir'
      ? `hsl(${(i * 37) % 360}, 25%, 18%)`
      : extColor(ext);
    const showLabel = r.w > 40 && r.h > 16;
    const label = r.item.name.length > 20 ? r.item.name.slice(0, 18) + '..' : r.item.name;
    return `<div class="cell" data-idx="${i}"
      style="left:${r.x}px;top:${r.y}px;width:${r.w}px;height:${r.h}px;background:${bg}"
    >${showLabel ? `<span class="cell-label">${label}<br><span style="font-size:0.5rem;opacity:0.7">${formatBytes(r.item.size)}</span></span>` : ''}</div>`;
  }).join('');

  // Events
  container.querySelectorAll('.cell').forEach(cell => {
    const r = rects[parseInt(cell.dataset.idx)];
    cell.addEventListener('click', () => {
      if (r.item.type === 'dir' && r.item.children && r.item.children.length > 0) {
        pathStack.push(r.item);
        render();
      }
    });
    cell.addEventListener('mousemove', e => {
      const item = r.item;
      tooltip.innerHTML = `
        <div class="tt-name">${item.name}</div>
        <div class="tt-row"><span class="tt-key">Size</span><span class="tt-val">${formatBytes(item.size)}</span></div>
        <div class="tt-row"><span class="tt-key">Type</span><span class="tt-val">${item.type}${item.ext ? ' .' + item.ext : ''}</span></div>
        ${item.children ? `<div class="tt-row"><span class="tt-key">Items</span><span class="tt-val">${item.children.length}</span></div>` : ''}
        ${item.file_count ? `<div class="tt-row"><span class="tt-key">Files</span><span class="tt-val">${item.file_count}</span></div>` : ''}
      `;
      tooltip.style.display = 'block';
      tooltip.style.left = Math.min(e.clientX + 12, window.innerWidth - 310) + 'px';
      tooltip.style.top = Math.min(e.clientY + 12, window.innerHeight - 150) + 'px';
    });
    cell.addEventListener('mouseleave', () => { tooltip.style.display = 'none'; });
  });
}

window.navigateTo = function(idx) {
  pathStack = pathStack.slice(0, idx + 1);
  render();
};

// Back button with backspace
document.addEventListener('keydown', e => {
  if (e.key === 'Backspace' && pathStack.length > 1) {
    pathStack.pop();
    render();
  }
});

window.addEventListener('resize', render);
render();
</script>
</body>
</html>'''


def main():
    parser = argparse.ArgumentParser(description='File Treemap')
    parser.add_argument('path', nargs='?', default='.', help='Directory to scan')
    parser.add_argument('-o', '--output', default=None, help='Output HTML file')
    parser.add_argument('--max-depth', type=int, default=6, help='Max directory depth')
    args = parser.parse_args()

    root = Path(args.path).resolve()
    output = args.output or str(Path.cwd() / f'treemap-{root.name}.html')

    tree = scan_directory(root, args.max_depth)

    html = HTML_TEMPLATE.replace('__DATA__', json.dumps(tree))
    html = html.replace('__ROOT_NAME__', tree['name'])
    Path(output).write_text(html)

    print(f"Total size: {format_bytes(tree['size'])}")
    print(f"Output: {output}")
    print(f"Open in a browser to explore.")


if __name__ == '__main__':
    main()
