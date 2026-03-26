#!/usr/bin/env python3
"""
git-xray: X-ray any git repo into an interactive HTML visualization.

Analyzes git history to reveal:
- File hotspots (most frequently changed files)
- Code age (when each file was last touched)
- Churn rate (additions + deletions over time)
- Author territories (who owns what)
- File size treemap

Usage: python3 git_xray.py [path-to-repo] [-o output.html]
"""

import argparse
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


def run_git(repo_path, *args):
    """Run a git command and return stdout. Handles timeouts and encoding."""
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_path)] + list(args),
            capture_output=True, timeout=120
        )
        if result.returncode != 0:
            return ""
        return result.stdout.decode('utf-8', errors='replace')
    except subprocess.TimeoutExpired:
        print(f"Warning: git command timed out: git {' '.join(args)}", file=sys.stderr)
        return ""


def clean_git_path(path_str):
    """Transform path/{old => new}/file to path/new/file for renames."""
    return re.sub(r'\{.* => (.*?)\}', r'\1', path_str).replace('//', '/')


def analyze_repo(repo_path):
    """Analyze a git repository and return structured data."""
    repo_path = Path(repo_path).resolve()
    check = run_git(repo_path, "rev-parse", "--is-inside-work-tree").strip()
    if check != "true":
        print(f"Error: {repo_path} is not a git repository")
        sys.exit(1)

    print(f"Analyzing {repo_path}...")

    # Get all tracked files with sizes
    print("  Collecting file list...")
    ls_output = run_git(repo_path, "ls-files")
    all_files = [f for f in ls_output.strip().split("\n") if f]

    # File sizes (current)
    file_sizes = {}
    for f in all_files:
        full_path = repo_path / f
        if full_path.exists() and full_path.is_file():
            try:
                file_sizes[f] = full_path.stat().st_size
            except OSError:
                file_sizes[f] = 0

    # Get commit count per file (hotspots)
    print("  Analyzing commit frequency...")
    commit_counts = defaultdict(int)
    log_output = run_git(repo_path, "log", "--pretty=format:", "--name-only", "--diff-filter=AMRC")
    for line in log_output.strip().split("\n"):
        line = line.strip()
        if line:
            commit_counts[line] += 1

    # Get first_seen and last_modified in a single pass (no per-file subprocess)
    print("  Analyzing code age...")
    first_seen = {}
    last_modified = {}
    age_log = run_git(repo_path, "log", "--name-only", "--pretty=format:COMMIT|%aI", "--diff-filter=AMRC")
    current_date = None
    for line in age_log.strip().split("\n"):
        line = line.strip()
        if not line:
            current_date = None
            continue
        if line.startswith("COMMIT|"):
            current_date = line[7:].strip()
        elif current_date:
            fname = line
            if fname not in last_modified:
                last_modified[fname] = current_date
            first_seen[fname] = current_date

    # Get churn (insertions + deletions) per file
    print("  Analyzing churn...")
    churn = defaultdict(lambda: {"insertions": 0, "deletions": 0})
    numstat_output = run_git(repo_path, "log", "--pretty=format:", "--numstat")
    for line in numstat_output.strip().split("\n"):
        parts = line.split("\t")
        if len(parts) == 3:
            ins, dels, fname = parts
            if ins != "-" and dels != "-":
                try:
                    fname = clean_git_path(fname)
                    churn[fname]["insertions"] += int(ins)
                    churn[fname]["deletions"] += int(dels)
                except ValueError:
                    pass

    # Get author stats per file (top author = most commits)
    print("  Analyzing author territories...")
    file_authors = defaultdict(lambda: defaultdict(int))
    author_log = run_git(repo_path, "log", "--pretty=format:%aN", "--name-only", "--diff-filter=AMRC")
    current_author = None
    for line in author_log.strip().split("\n"):
        line = line.strip()
        if not line:
            current_author = None
            continue
        if current_author is None:
            current_author = line
        else:
            file_authors[line][current_author] += 1

    # Get top authors overall
    print("  Analyzing contributors...")
    author_commits = defaultdict(int)
    shortlog = run_git(repo_path, "shortlog", "-sn", "--no-merges", "HEAD")
    for line in shortlog.strip().split("\n"):
        line = line.strip()
        if line:
            parts = line.split("\t", 1)
            if len(parts) == 2:
                try:
                    count = int(parts[0].strip())
                    name = parts[1].strip()
                    author_commits[name] = count
                except ValueError:
                    pass

    # Get recent commit activity (last 90 days, commits per day)
    print("  Analyzing activity timeline...")
    activity_log = run_git(repo_path, "log", "--since=90 days ago", "--pretty=format:%aI")
    daily_activity = defaultdict(int)
    for line in activity_log.strip().split("\n"):
        line = line.strip()
        if line:
            day = line[:10]
            daily_activity[day] += 1

    # Get total commit count
    total_commits = run_git(repo_path, "rev-list", "--count", "HEAD").strip()

    # Get repo name
    repo_name = repo_path.name

    # Build file data
    print("  Building visualization data...")
    files_data = []
    for f in all_files:
        if f not in file_sizes:
            continue
        # Determine directory structure
        parts = f.split("/")
        directory = "/".join(parts[:-1]) if len(parts) > 1 else "."
        extension = Path(f).suffix.lstrip(".") or "none"

        # Top author for this file
        top_author = ""
        if f in file_authors:
            top_author = max(file_authors[f], key=file_authors[f].get)

        files_data.append({
            "path": f,
            "directory": directory,
            "extension": extension,
            "size": file_sizes.get(f, 0),
            "commits": commit_counts.get(f, 0),
            "last_modified": last_modified.get(f, ""),
            "first_seen": first_seen.get(f, ""),
            "insertions": churn[f]["insertions"],
            "deletions": churn[f]["deletions"],
            "churn": churn[f]["insertions"] + churn[f]["deletions"],
            "top_author": top_author,
        })

    # Sort authors by commit count
    top_authors = sorted(author_commits.items(), key=lambda x: -x[1])[:20]

    return {
        "repo_name": repo_name,
        "total_files": len(all_files),
        "total_commits": int(total_commits) if total_commits.isdigit() else 0,
        "files": files_data,
        "authors": [{"name": a, "commits": c} for a, c in top_authors],
        "daily_activity": [{"date": d, "commits": c} for d, c in sorted(daily_activity.items())],
    }


HTML_TEMPLATE = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>git-xray: __REPO_NAME__</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'SF Mono', 'Fira Code', monospace; background: #0a0a0a; color: #ccc; }
.header { padding: 1.5rem 2rem; border-bottom: 1px solid #1a1a1a; }
.header h1 { font-size: 1.4rem; color: #fff; }
.header .meta { color: #555; font-size: 0.75rem; margin-top: 0.3rem; }
.tabs { display: flex; gap: 0; border-bottom: 1px solid #1a1a1a; padding: 0 2rem; background: #0d0d0d; }
.tab { padding: 0.7rem 1.2rem; cursor: pointer; color: #666; font-size: 0.8rem; border-bottom: 2px solid transparent; transition: all 0.2s; }
.tab:hover { color: #aaa; }
.tab.active { color: #fff; border-bottom-color: #4ade80; }
.panel { display: none; padding: 1.5rem 2rem; }
.panel.active { display: block; }
.controls { display: flex; gap: 1rem; margin-bottom: 1.5rem; align-items: center; flex-wrap: wrap; }
.controls select, .controls input { background: #111; border: 1px solid #333; color: #ccc; padding: 0.4rem 0.7rem; border-radius: 4px; font-family: inherit; font-size: 0.75rem; }
.controls label { font-size: 0.7rem; color: #666; }
table { width: 100%; border-collapse: collapse; font-size: 0.8rem; }
th { text-align: left; padding: 0.5rem 0.8rem; border-bottom: 1px solid #222; color: #666; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.05em; cursor: pointer; user-select: none; }
th:hover { color: #aaa; }
td { padding: 0.45rem 0.8rem; border-bottom: 1px solid #111; }
tr:hover td { background: #111; }
.bar-cell { position: relative; }
.bar { position: absolute; left: 0; top: 0; bottom: 0; opacity: 0.15; border-radius: 2px; }
.bar-hot { background: #f87171; }
.bar-churn { background: #fbbf24; }
.bar-age { background: #60a5fa; }
.bar-size { background: #a78bfa; }
.badge { display: inline-block; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.65rem; }
.treemap-container { width: 100%; height: 500px; position: relative; border-radius: 8px; overflow: hidden; border: 1px solid #222; }
.treemap-cell { position: absolute; overflow: hidden; border: 1px solid #0a0a0a; cursor: pointer; transition: opacity 0.15s; display: flex; align-items: center; justify-content: center; }
.treemap-cell:hover { opacity: 0.8; }
.treemap-label { font-size: 0.6rem; color: rgba(255,255,255,0.9); text-align: center; padding: 2px; word-break: break-all; text-shadow: 0 1px 2px rgba(0,0,0,0.8); pointer-events: none; }
.tooltip { position: fixed; background: #1a1a1a; border: 1px solid #333; border-radius: 6px; padding: 0.7rem; font-size: 0.75rem; pointer-events: none; z-index: 100; max-width: 350px; }
.tooltip-row { display: flex; justify-content: space-between; gap: 1.5rem; margin: 0.15rem 0; }
.tooltip-key { color: #666; }
.tooltip-val { color: #fff; text-align: right; }
.chart-container { width: 100%; height: 200px; position: relative; background: #111; border-radius: 8px; border: 1px solid #1a1a1a; overflow: hidden; padding: 1rem 1rem 2rem 3rem; }
.chart-bar { position: absolute; bottom: 2rem; background: #4ade80; border-radius: 2px 2px 0 0; min-width: 3px; opacity: 0.7; }
.chart-label { position: absolute; bottom: 0.3rem; font-size: 0.55rem; color: #444; transform: rotate(-45deg); transform-origin: top left; white-space: nowrap; }
.author-row { display: flex; align-items: center; gap: 1rem; padding: 0.5rem 0; border-bottom: 1px solid #111; }
.author-name { width: 200px; font-size: 0.8rem; color: #fff; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.author-bar-bg { flex: 1; height: 20px; background: #111; border-radius: 3px; overflow: hidden; position: relative; }
.author-bar-fill { height: 100%; border-radius: 3px; transition: width 0.3s; }
.author-count { width: 60px; text-align: right; font-size: 0.75rem; color: #666; }
.section-title { font-size: 1rem; color: #fff; margin-bottom: 1rem; }
.section-sub { font-size: 0.75rem; color: #555; margin-bottom: 1.5rem; }
.stat-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin-bottom: 2rem; }
.stat-card { background: #111; padding: 1rem; border-radius: 8px; border: 1px solid #1a1a1a; }
.stat-num { font-size: 1.5rem; font-weight: bold; color: #fff; }
.stat-label { font-size: 0.65rem; color: #555; text-transform: uppercase; letter-spacing: 0.1em; margin-top: 0.2rem; }
</style>
</head>
<body>

<div class="header">
  <h1>git-xray: <span id="repo-name"></span></h1>
  <div class="meta" id="repo-meta"></div>
</div>

<div class="tabs" id="tabs">
  <div class="tab active" data-tab="overview">Overview</div>
  <div class="tab" data-tab="hotspots">Hotspots</div>
  <div class="tab" data-tab="treemap">Treemap</div>
  <div class="tab" data-tab="authors">Authors</div>
  <div class="tab" data-tab="activity">Activity</div>
</div>

<div class="panel active" id="panel-overview"></div>
<div class="panel" id="panel-hotspots"></div>
<div class="panel" id="panel-treemap"></div>
<div class="panel" id="panel-authors"></div>
<div class="panel" id="panel-activity"></div>

<div class="tooltip" id="tooltip" style="display:none"></div>

<script>
const DATA = __DATA__;

// --- Tabs ---
document.querySelectorAll('.tab').forEach(tab => {
  tab.addEventListener('click', () => {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
    tab.classList.add('active');
    document.getElementById('panel-' + tab.dataset.tab).classList.add('active');
  });
});

// --- Tooltip ---
const tooltip = document.getElementById('tooltip');
function showTooltip(e, html) {
  tooltip.innerHTML = html;
  tooltip.style.display = 'block';
  const x = Math.min(e.clientX + 12, window.innerWidth - 360);
  const y = Math.min(e.clientY + 12, window.innerHeight - 200);
  tooltip.style.left = x + 'px';
  tooltip.style.top = y + 'px';
}
function hideTooltip() { tooltip.style.display = 'none'; }

// --- Helpers ---
function formatBytes(b) {
  if (b < 1024) return b + ' B';
  if (b < 1048576) return (b/1024).toFixed(1) + ' KB';
  return (b/1048576).toFixed(1) + ' MB';
}
function daysAgo(dateStr) {
  if (!dateStr) return Infinity;
  const d = new Date(dateStr);
  return Math.floor((Date.now() - d.getTime()) / 86400000);
}
function ageLabel(dateStr) {
  const d = daysAgo(dateStr);
  if (d === Infinity) return 'unknown';
  if (d === 0) return 'today';
  if (d === 1) return 'yesterday';
  if (d < 30) return d + 'd ago';
  if (d < 365) return Math.floor(d/30) + 'mo ago';
  return (d/365).toFixed(1) + 'y ago';
}
function extColor(ext) {
  const colors = {
    py: '#3572A5', js: '#f1e05a', ts: '#3178c6', tsx: '#3178c6', jsx: '#f1e05a',
    rs: '#dea584', go: '#00ADD8', java: '#b07219', c: '#555555', cpp: '#f34b7d',
    h: '#555555', rb: '#701516', php: '#4F5D95', css: '#563d7c', html: '#e34c26',
    md: '#083fa1', json: '#666', yaml: '#cb171e', yml: '#cb171e', toml: '#9c4221',
    sh: '#89e051', bash: '#89e051', sql: '#e38c00', svg: '#ff9900',
  };
  return colors[ext] || '#4a4a4a';
}

// --- Overview ---
function renderOverview() {
  const files = DATA.files;
  const totalSize = files.reduce((s, f) => s + f.size, 0);
  const totalChurn = files.reduce((s, f) => s + f.churn, 0);
  const hottest = [...files].sort((a, b) => b.commits - a.commits).slice(0, 5);
  const extensions = {};
  files.forEach(f => { extensions[f.extension] = (extensions[f.extension] || 0) + 1; });
  const topExts = Object.entries(extensions).sort((a, b) => b[1] - a[1]).slice(0, 10);

  document.getElementById('repo-name').textContent = DATA.repo_name;
  document.getElementById('repo-meta').textContent = `${DATA.total_files} files \u00b7 ${DATA.total_commits} commits \u00b7 ${DATA.authors.length} contributors`;

  const panel = document.getElementById('panel-overview');
  panel.innerHTML = `
    <div class="stat-grid">
      <div class="stat-card"><div class="stat-num">${DATA.total_files}</div><div class="stat-label">Files</div></div>
      <div class="stat-card"><div class="stat-num">${DATA.total_commits.toLocaleString()}</div><div class="stat-label">Commits</div></div>
      <div class="stat-card"><div class="stat-num">${formatBytes(totalSize)}</div><div class="stat-label">Total Size</div></div>
      <div class="stat-card"><div class="stat-num">${totalChurn.toLocaleString()}</div><div class="stat-label">Total Churn</div></div>
      <div class="stat-card"><div class="stat-num">${DATA.authors.length}</div><div class="stat-label">Contributors</div></div>
      <div class="stat-card"><div class="stat-num">${topExts.length > 0 ? topExts[0][0] : '-'}</div><div class="stat-label">Top Language</div></div>
    </div>
    <div class="section-title">Hottest Files</div>
    <div class="section-sub">Files with the most commits</div>
    <table>
      <tr><th>File</th><th>Commits</th><th>Churn</th><th>Last Modified</th></tr>
      ${hottest.map(f => `<tr>
        <td style="color:#fff">${f.path}</td>
        <td>${f.commits}</td>
        <td>${f.churn.toLocaleString()}</td>
        <td style="color:#666">${ageLabel(f.last_modified)}</td>
      </tr>`).join('')}
    </table>
    <br>
    <div class="section-title">File Types</div>
    <div class="section-sub">Distribution by extension</div>
    ${topExts.map(([ext, count]) => `
      <div class="author-row">
        <div class="author-name" style="width:100px">.${ext}</div>
        <div class="author-bar-bg">
          <div class="author-bar-fill" style="width:${100*count/files.length}%; background:${extColor(ext)}"></div>
        </div>
        <div class="author-count">${count}</div>
      </div>
    `).join('')}
  `;
}

// --- Hotspots Table ---
let sortKey = 'commits';
let sortAsc = false;

function renderHotspots() {
  const panel = document.getElementById('panel-hotspots');
  const files = [...DATA.files].sort((a, b) => {
    let va = a[sortKey], vb = b[sortKey];
    if (sortKey === 'last_modified') { va = daysAgo(va); vb = daysAgo(vb); }
    if (typeof va === 'string') return sortAsc ? va.localeCompare(vb) : vb.localeCompare(va);
    return sortAsc ? va - vb : vb - va;
  });

  const maxCommits = Math.max(...files.map(f => f.commits), 1);
  const maxChurn = Math.max(...files.map(f => f.churn), 1);
  const maxSize = Math.max(...files.map(f => f.size), 1);

  panel.innerHTML = `
    <div class="controls">
      <label>Sort by:</label>
      <select id="sort-select">
        <option value="commits" ${sortKey==='commits'?'selected':''}>Commits</option>
        <option value="churn" ${sortKey==='churn'?'selected':''}>Churn</option>
        <option value="size" ${sortKey==='size'?'selected':''}>Size</option>
        <option value="last_modified" ${sortKey==='last_modified'?'selected':''}>Last Modified</option>
        <option value="path" ${sortKey==='path'?'selected':''}>Name</option>
      </select>
      <label><input type="checkbox" id="sort-asc" ${sortAsc?'checked':''}> Ascending</label>
    </div>
    <table>
      <tr>
        <th>File</th><th>Ext</th><th>Commits</th><th>Churn</th><th>Size</th><th>Age</th><th>Author</th>
      </tr>
      ${files.slice(0, 200).map(f => `
        <tr>
          <td style="color:#fff; max-width:350px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap" title="${f.path}">${f.path}</td>
          <td><span class="badge" style="background:${extColor(f.extension)}30; color:${extColor(f.extension)}">${f.extension}</span></td>
          <td class="bar-cell"><div class="bar bar-hot" style="width:${100*f.commits/maxCommits}%"></div>${f.commits}</td>
          <td class="bar-cell"><div class="bar bar-churn" style="width:${100*f.churn/maxChurn}%"></div>${f.churn.toLocaleString()}</td>
          <td class="bar-cell"><div class="bar bar-size" style="width:${100*f.size/maxSize}%"></div>${formatBytes(f.size)}</td>
          <td style="color:#666">${ageLabel(f.last_modified)}</td>
          <td style="color:#888; max-width:120px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap">${f.top_author}</td>
        </tr>
      `).join('')}
    </table>
    ${files.length > 200 ? `<div style="color:#444;padding:1rem;font-size:0.75rem">Showing 200 of ${files.length} files</div>` : ''}
  `;

  document.getElementById('sort-select').addEventListener('change', e => { sortKey = e.target.value; renderHotspots(); });
  document.getElementById('sort-asc').addEventListener('change', e => { sortAsc = e.target.checked; renderHotspots(); });
}

// --- Treemap ---
function renderTreemap() {
  const panel = document.getElementById('panel-treemap');
  const container = document.createElement('div');

  const colorModes = { extension: 'By Language', commits: 'By Hotspot', age: 'By Code Age' };
  let colorMode = 'extension';

  function draw() {
    const files = DATA.files.filter(f => f.size > 0);
    const totalSize = files.reduce((s, f) => s + f.size, 0);
    if (totalSize === 0) { panel.innerHTML = '<div style="padding:2rem;color:#666">No files with size data.</div>'; return; }

    const maxCommits = Math.max(...files.map(f => f.commits), 1);

    // Simple squarified-ish treemap: sort by size desc, lay out in rows
    const sorted = [...files].sort((a, b) => b.size - a.size).slice(0, 300);
    const width = 900;
    const height = 500;

    // Slice-and-dice layout
    const rects = [];
    function layout(items, x, y, w, h, depth) {
      if (items.length === 0) return;
      if (items.length === 1 || w < 4 || h < 4) {
        const totalS = items.reduce((s, f) => s + f.size, 0);
        let cy = y;
        items.forEach(f => {
          const fh = totalS > 0 ? (f.size / totalS) * h : h / items.length;
          rects.push({ file: f, x, y: cy, w, h: fh });
          cy += fh;
        });
        return;
      }
      const totalS = items.reduce((s, f) => s + f.size, 0);
      const half = totalS / 2;
      let acc = 0;
      let split = 1;
      for (let i = 0; i < items.length; i++) {
        acc += items[i].size;
        if (acc >= half) { split = i + 1; break; }
      }
      split = Math.max(1, Math.min(split, items.length - 1));
      const leftSize = items.slice(0, split).reduce((s, f) => s + f.size, 0);
      const ratio = leftSize / totalS;

      if (w >= h) {
        const lw = w * ratio;
        layout(items.slice(0, split), x, y, lw, h, depth + 1);
        layout(items.slice(split), x + lw, y, w - lw, h, depth + 1);
      } else {
        const lh = h * ratio;
        layout(items.slice(0, split), x, y, w, lh, depth + 1);
        layout(items.slice(split), x, y + lh, w, h - lh, depth + 1);
      }
    }

    layout(sorted, 0, 0, width, height, 0);

    let html = `
      <div class="controls">
        <label>Color by:</label>
        <select id="treemap-color">
          ${Object.entries(colorModes).map(([k,v]) => `<option value="${k}" ${k===colorMode?'selected':''}>${v}</option>`).join('')}
        </select>
      </div>
      <div class="treemap-container" style="width:100%;max-width:${width}px;height:${height}px;">
    `;

    rects.forEach((r, i) => {
      let bg;
      if (colorMode === 'extension') {
        bg = extColor(r.file.extension);
      } else if (colorMode === 'commits') {
        const intensity = Math.min(r.file.commits / maxCommits, 1);
        const red = Math.round(40 + intensity * 200);
        bg = `rgb(${red}, ${Math.round(40 - intensity*20)}, ${Math.round(40 - intensity*20)})`;
      } else {
        const d = daysAgo(r.file.last_modified);
        const freshness = Math.max(0, 1 - d / 365);
        const green = Math.round(60 + freshness * 150);
        bg = `rgb(${Math.round(40 - freshness*20)}, ${green}, ${Math.round(60 + freshness*100)})`;
      }
      const pctW = (r.w / width * 100);
      const pctH = (r.h / height * 100);
      const pctX = (r.x / width * 100);
      const pctY = (r.y / height * 100);
      const showLabel = r.w > 40 && r.h > 20;
      const name = r.file.path.split('/').pop();
      html += `<div class="treemap-cell" data-idx="${i}"
        style="left:${pctX}%;top:${pctY}%;width:${pctW}%;height:${pctH}%;background:${bg}"
        >${showLabel ? `<span class="treemap-label">${name}</span>` : ''}</div>`;
    });
    html += '</div>';
    panel.innerHTML = html;

    // Events
    document.getElementById('treemap-color').addEventListener('change', e => { colorMode = e.target.value; draw(); });
    panel.querySelectorAll('.treemap-cell').forEach(cell => {
      cell.addEventListener('mousemove', e => {
        const f = rects[parseInt(cell.dataset.idx)].file;
        showTooltip(e, `
          <div style="color:#fff;font-weight:bold;margin-bottom:0.3rem">${f.path}</div>
          <div class="tooltip-row"><span class="tooltip-key">Size</span><span class="tooltip-val">${formatBytes(f.size)}</span></div>
          <div class="tooltip-row"><span class="tooltip-key">Commits</span><span class="tooltip-val">${f.commits}</span></div>
          <div class="tooltip-row"><span class="tooltip-key">Churn</span><span class="tooltip-val">${f.churn.toLocaleString()}</span></div>
          <div class="tooltip-row"><span class="tooltip-key">Last Modified</span><span class="tooltip-val">${ageLabel(f.last_modified)}</span></div>
          <div class="tooltip-row"><span class="tooltip-key">Top Author</span><span class="tooltip-val">${f.top_author}</span></div>
        `);
      });
      cell.addEventListener('mouseleave', hideTooltip);
    });
  }
  draw();
}

// --- Authors ---
function renderAuthors() {
  const panel = document.getElementById('panel-authors');
  const authors = DATA.authors;
  const maxC = authors.length > 0 ? authors[0].commits : 1;
  const colors = ['#4ade80','#60a5fa','#f87171','#fbbf24','#a78bfa','#fb923c','#34d399','#f472b6','#38bdf8','#e879f9'];

  panel.innerHTML = `
    <div class="section-title">Contributors</div>
    <div class="section-sub">Ranked by commit count</div>
    ${authors.map((a, i) => `
      <div class="author-row">
        <div class="author-name">${a.name}</div>
        <div class="author-bar-bg">
          <div class="author-bar-fill" style="width:${100*a.commits/maxC}%; background:${colors[i%colors.length]}"></div>
        </div>
        <div class="author-count">${a.commits}</div>
      </div>
    `).join('')}
  `;
}

// --- Activity ---
function renderActivity() {
  const panel = document.getElementById('panel-activity');
  const activity = DATA.daily_activity;
  if (activity.length === 0) {
    panel.innerHTML = '<div style="padding:2rem;color:#666">No recent activity data (last 90 days).</div>';
    return;
  }
  const maxC = Math.max(...activity.map(a => a.commits), 1);
  const barWidth = Math.max(3, Math.min(12, Math.floor(800 / activity.length) - 1));

  panel.innerHTML = `
    <div class="section-title">Activity (Last 90 Days)</div>
    <div class="section-sub">Commits per day</div>
    <div class="chart-container" style="height:250px">
      ${activity.map((a, i) => {
        const h = (a.commits / maxC) * 180;
        const x = 40 + i * (barWidth + 1);
        return `<div class="chart-bar" style="left:${x}px;height:${h}px;width:${barWidth}px"
          onmousemove="showTooltip(event, '${a.date}: ${a.commits} commits')"
          onmouseleave="hideTooltip()"></div>
          ${i % Math.ceil(activity.length / 10) === 0 ? `<div class="chart-label" style="left:${x}px">${a.date.slice(5)}</div>` : ''}`;
      }).join('')}
    </div>
  `;
}

// Make tooltip functions global for inline handlers
window.showTooltip = showTooltip;
window.hideTooltip = hideTooltip;

// Render all
renderOverview();
renderHotspots();
renderTreemap();
renderAuthors();
renderActivity();
</script>
</body>
</html>'''


def generate_html(data, output_path):
    """Generate the HTML visualization."""
    import html as html_lib
    # Escape </script> sequences to prevent XSS via malicious filenames
    json_data = json.dumps(data).replace('<', '\\u003c').replace('>', '\\u003e')
    html = HTML_TEMPLATE.replace('__DATA__', json_data)
    html = html.replace('__REPO_NAME__', html_lib.escape(data['repo_name']))
    Path(output_path).write_text(html, encoding='utf-8')
    print(f"Output written to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="git-xray: X-ray a git repository")
    parser.add_argument("repo", nargs="?", default=".", help="Path to git repository")
    parser.add_argument("-o", "--output", default=None, help="Output HTML file path")
    args = parser.parse_args()

    repo_path = Path(args.repo).resolve()
    output = args.output or str(Path.cwd() / f"xray-{repo_path.name}.html")

    data = analyze_repo(repo_path)
    generate_html(data, output)
    print(f"\nDone! Open {output} in a browser.")


if __name__ == "__main__":
    main()
