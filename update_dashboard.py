#!/usr/bin/env python3
"""Regenerate dashboard.html from yolo_log.json.

Usage: python3 update_dashboard.py
Called by the overnight builder after each project.
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent
LOG_FILE = ROOT / "yolo_log.json"
DASHBOARD = ROOT / "dashboard.html"

TEMPLATE = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>YOLO Dashboard</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace; background: #0a0a0a; color: #e0e0e0; padding: 1.5rem; max-width: 1200px; margin: 0 auto; }
  h1 { font-size: 1.8rem; margin-bottom: 0.3rem; color: #fff; }
  .subtitle { color: #666; margin-bottom: 1.5rem; font-size: 0.85rem; }

  .stats { display: flex; gap: 1.5rem; margin-bottom: 1.5rem; padding: 0.8rem 1.2rem; background: #111; border-radius: 8px; border: 1px solid #222; flex-wrap: wrap; }
  .stat { text-align: center; min-width: 60px; }
  .stat-num { font-size: 1.4rem; font-weight: bold; }
  .stat-label { font-size: 0.65rem; color: #666; text-transform: uppercase; letter-spacing: 0.1em; }

  .controls { display: flex; gap: 0.75rem; margin-bottom: 1.2rem; flex-wrap: wrap; align-items: center; }
  .search-box { flex: 1; min-width: 180px; padding: 0.45rem 0.8rem; background: #111; border: 1px solid #333; border-radius: 6px; color: #e0e0e0; font-family: inherit; font-size: 0.8rem; outline: none; }
  .search-box:focus { border-color: #58a6ff; }
  .search-box::placeholder { color: #444; }
  .pill-group { display: flex; gap: 0.35rem; flex-wrap: wrap; }
  .pill { background: #1a1a1a; border: 1px solid #333; color: #888; padding: 0.3rem 0.65rem; border-radius: 20px; cursor: pointer; font-family: inherit; font-size: 0.7rem; transition: all 0.15s; white-space: nowrap; }
  .pill:hover { border-color: #555; color: #ccc; }
  .pill.active { border-color: #58a6ff; color: #58a6ff; background: #0d1b2e; }
  .pill .count { font-size: 0.6rem; color: #555; margin-left: 3px; }
  .pill.active .count { color: #58a6ff88; }

  .view-toggle { display: flex; gap: 2px; background: #111; border-radius: 4px; border: 1px solid #333; overflow: hidden; }
  .view-toggle button { background: transparent; border: none; color: #666; padding: 0.35rem 0.55rem; cursor: pointer; font-size: 0.8rem; font-family: inherit; }
  .view-toggle button.active { background: #222; color: #fff; }

  .sort-select { background: #111; border: 1px solid #333; color: #888; padding: 0.3rem 0.5rem; border-radius: 4px; font-family: inherit; font-size: 0.7rem; }

  .category { margin-bottom: 1.8rem; }
  .category-header { font-size: 0.8rem; color: #58a6ff; text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 0.6rem; padding-bottom: 0.35rem; border-bottom: 1px solid #1a1a2e; display: flex; align-items: center; gap: 0.5rem; }
  .category-icon { font-size: 1rem; }
  .category-count { font-size: 0.65rem; color: #444; margin-left: auto; }

  .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 0.65rem; }
  .list .entry { display: flex; gap: 1rem; align-items: flex-start; }
  .list .entry-body { flex: 1; }

  .entry { padding: 1rem; background: #111; border-radius: 8px; border: 1px solid #1a1a1a; transition: border-color 0.2s; position: relative; }
  .entry:hover { border-color: #333; }
  .entry.thumbs-up { border-left: 3px solid #4ade80; }
  .entry.thumbs-down { border-left: 3px solid #f87171; opacity: 0.6; }
  .entry.refined { border-top: 2px solid #58a6ff; }
  .refined-badge { font-size: 0.55rem; padding: 0.1rem 0.4rem; border-radius: 3px; background: #0d1b2e; color: #58a6ff; border: 1px solid #1a3a5e; margin-left: 6px; vertical-align: middle; }
  .section-divider { font-size: 0.9rem; color: #58a6ff; padding: 0.8rem 0 0.4rem; margin-top: 1rem; border-bottom: 1px solid #1a1a2e; margin-bottom: 0.8rem; display: flex; align-items: center; gap: 0.5rem; }
  .section-divider .count { font-size: 0.7rem; color: #444; margin-left: auto; }
  .unrefined-section { opacity: 0.75; }
  .unrefined-section .entry { border-left: 2px solid #333; }
  .entry-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem; gap: 0.5rem; }
  .entry-name { font-weight: bold; font-size: 0.95rem; color: #fff; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .entry-date { color: #444; font-size: 0.65rem; white-space: nowrap; }
  .entry-idea { color: #aaa; font-size: 0.8rem; margin-bottom: 0.4rem; line-height: 1.4; }
  .entry-takeaway { color: #666; font-size: 0.72rem; font-style: italic; line-height: 1.3; }
  .entry-footer { display: flex; justify-content: space-between; align-items: center; margin-top: 0.5rem; }
  .entry-folder { color: #333; font-size: 0.65rem; }
  .launch-link { font-size: 0.68rem; padding: 0.2rem 0.55rem; border-radius: 4px; text-decoration: none; border: 1px solid #166534; color: #4ade80; background: #0a1a0a; transition: all 0.2s; cursor: pointer; }
  .launch-link:hover { background: #0a2a0a; border-color: #4ade80; }
  .launch-link.script { border-color: #854d0e; color: #fbbf24; background: #1a1500; }
  .launch-link.script:hover { background: #2a2000; border-color: #fbbf24; }

  /* Metrics row */
  .entry-metrics { display: flex; align-items: center; gap: 8px; margin-top: 6px; font-size: 0.65rem; color: #444; }
  .metric { display: flex; align-items: center; gap: 2px; }
  .metric-icon { font-size: 0.75rem; }

  /* Thumbs */
  .thumb-btn { background: none; border: 1px solid transparent; cursor: pointer; font-size: 1rem; padding: 2px 4px; border-radius: 4px; opacity: 0.3; transition: all 0.15s; }
  .thumb-btn:hover { opacity: 0.7; }
  .thumb-btn.voted { opacity: 1; border-color: #333; }
  .thumb-up.voted { color: #4ade80; border-color: #166534; background: #0a1a0a; }
  .thumb-down.voted { color: #f87171; border-color: #991b1b; background: #1a0a0a; }

  .empty { text-align: center; padding: 3rem; color: #444; }

  /* Leaderboard */
  .leaderboard { margin-bottom: 1.5rem; padding: 1rem; background: #111; border: 1px solid #222; border-radius: 8px; }
  .leaderboard h3 { font-size: 0.75rem; color: #58a6ff; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px; }
  .lb-row { display: flex; align-items: center; gap: 8px; padding: 4px 0; font-size: 0.75rem; border-bottom: 1px solid #1a1a1a; }
  .lb-row:last-child { border-bottom: none; }
  .lb-rank { color: #555; width: 20px; text-align: right; }
  .lb-name { color: #fff; flex: 1; }
  .lb-stat { color: #888; font-size: 0.65rem; min-width: 50px; text-align: right; }
  .lb-bar { height: 4px; background: #58a6ff33; border-radius: 2px; flex: 1; max-width: 80px; overflow: hidden; }
  .lb-bar-fill { height: 100%; background: #58a6ff; border-radius: 2px; }
</style>
</head>
<body>

<h1>YOLO Dashboard</h1>
<p class="subtitle">overnight builds &mdash; shipped and ugly over planned and pretty</p>

<div class="stats" id="stats"></div>

<div id="leaderboard" class="leaderboard" style="display:none">
  <h3>Most Used</h3>
  <div id="lb-body"></div>
</div>

<div class="controls">
  <input class="search-box" id="search" type="text" placeholder="Search projects...">
  <div class="pill-group" id="cat-pills"></div>
  <div class="pill-group" id="status-pills"></div>
  <div class="pill-group" id="vote-pills"></div>
  <div class="pill-group" id="range-pills"></div>
  <select class="sort-select" id="sort-select">
    <option value="newest">Sort: Newest</option>
    <option value="date">Sort: By Category</option>
    <option value="opens">Sort: Most Opened</option>
    <option value="liked">Sort: Liked First</option>
    <option value="name">Sort: A-Z</option>
  </select>
  <div class="view-toggle">
    <button id="view-grid" class="active" title="Grid view">&#9638;</button>
    <button id="view-list" title="List view">&#9776;</button>
  </div>
</div>

<div id="feed"></div>

<script>
const LOG_DATA = __LOG_DATA__;

// ---- Usage tracking (localStorage) ----
const STORAGE_KEY = 'yolo_dash_metrics';

function loadMetrics() {
  try { return JSON.parse(localStorage.getItem(STORAGE_KEY)) || {}; } catch { return {}; }
}
function saveMetrics(m) { localStorage.setItem(STORAGE_KEY, JSON.stringify(m)); }

function getMetric(project) {
  const m = loadMetrics();
  return m[project] || { opens: 0, lastOpened: null, vote: null };
}
function setMetric(project, key, value) {
  const m = loadMetrics();
  if (!m[project]) m[project] = { opens: 0, lastOpened: null, vote: null };
  m[project][key] = value;
  saveMetrics(m);
}
function trackOpen(project) {
  const m = loadMetrics();
  if (!m[project]) m[project] = { opens: 0, lastOpened: null, vote: null };
  m[project].opens++;
  m[project].lastOpened = new Date().toISOString();
  saveMetrics(m);
}

// ---- Category assignment ----
const CATEGORIES = {
  'Simulations & Games': {
    icon: '\uD83C\uDFAE',
    match: ['ray-caster','gravity-sim','circuit-sim','mandelbrot-explorer','sound-synth','music-viz','synth-defense','weather-terrarium']
  },
  'Dev Tools': {
    icon: '\uD83D\uDEE0\uFE0F',
    match: ['git-xray','regex-playground','json-explorer','diff-painter','api-mocker','cron-decoder']
  },
  'Creative & Art': {
    icon: '\uD83C\uDFA8',
    match: ['pixel-paint','whiteboard','color-lab','markdown-deck','markov-composer']
  },
  'Productivity': {
    icon: '\u2705',
    match: ['kanban-board','pomodoro-flow','habit-grid','countdown-wall','bookmark-dash']
  },
  'System & Monitoring': {
    icon: '\uD83D\uDCBB',
    match: ['proc-map','system-dash','wifi-time-machine','file-treemap','speedtype']
  },
  'Utilities': {
    icon: '\uD83E\uDDF0',
    match: ['qr-forge','unit-convert','emoji-search','math-plot']
  },
  'Education & AI': {
    icon: '\uD83E\uDDE0',
    match: ['regex-quest','neural-playground']
  }
};

function getCategory(project) {
  for (const [cat, def] of Object.entries(CATEGORIES)) {
    if (def.match.includes(project)) return cat;
  }
  return 'Other';
}

LOG_DATA.forEach(e => { e.category = getCategory(e.project); });

let activeCategory = 'all';
let activeStatus = 'all';
let activeVote = 'all';
let activeRange = 10; // show last N (0 = all)
let searchQuery = '';
let viewMode = 'grid';
let sortMode = 'newest';

function render() {
  const metrics = loadMetrics();
  const data = LOG_DATA.slice().reverse();

  // Enrich with metrics
  data.forEach(e => {
    const m = metrics[e.project] || { opens: 0, lastOpened: null, vote: null };
    e._opens = m.opens;
    e._lastOpened = m.lastOpened;
    e._vote = m.vote;
  });

  // Filter
  let filtered = data;
  if (activeRange > 0) filtered = filtered.slice(0, activeRange);
  if (activeCategory !== 'all') filtered = filtered.filter(e => e.category === activeCategory);
  if (activeStatus === 'refined') filtered = filtered.filter(e => e.refined);
  else if (activeStatus === 'unrefined') filtered = filtered.filter(e => e.status === 'working' && !e.refined);
  else if (activeStatus !== 'all') filtered = filtered.filter(e => e.status === activeStatus);
  if (activeVote === 'up') filtered = filtered.filter(e => e._vote === 'up');
  if (activeVote === 'down') filtered = filtered.filter(e => e._vote === 'down');
  if (activeVote === 'unrated') filtered = filtered.filter(e => !e._vote);
  if (searchQuery) {
    const q = searchQuery.toLowerCase();
    filtered = filtered.filter(e =>
      e.project.toLowerCase().includes(q) ||
      e.idea.toLowerCase().includes(q) ||
      e.takeaway.toLowerCase().includes(q)
    );
  }

  // Sort
  if (sortMode === 'opens') filtered.sort((a, b) => b._opens - a._opens);
  else if (sortMode === 'liked') filtered.sort((a, b) => (b._vote === 'up' ? 1 : 0) - (a._vote === 'up' ? 1 : 0));
  else if (sortMode === 'name') filtered.sort((a, b) => a.project.localeCompare(b.project));
  // 'newest' and 'date' are already reverse-chronological

  // Stats
  const total = data.length;
  const working = data.filter(e => e.status === 'working').length;
  const failed = data.filter(e => e.status === 'failed').length;
  const refinedCount = data.filter(e => e.refined).length;
  const liked = data.filter(e => e._vote === 'up').length;
  const disliked = data.filter(e => e._vote === 'down').length;
  const totalOpens = data.reduce((s, e) => s + e._opens, 0);

  document.getElementById('stats').innerHTML = `
    <div class="stat"><div class="stat-num">${total}</div><div class="stat-label">Total</div></div>
    <div class="stat"><div class="stat-num" style="color:#4ade80">${working}</div><div class="stat-label">Working</div></div>
    <div class="stat"><div class="stat-num" style="color:#58a6ff">${refinedCount}</div><div class="stat-label">Refined</div></div>
    <div class="stat"><div class="stat-num" style="color:#f87171">${failed}</div><div class="stat-label">Culled</div></div>
    <div class="stat"><div class="stat-num">${totalOpens}</div><div class="stat-label">Opens</div></div>
  `;

  // Leaderboard — top 5 most opened
  const ranked = data.filter(e => e._opens > 0).sort((a, b) => b._opens - a._opens).slice(0, 5);
  const lbEl = document.getElementById('leaderboard');
  if (ranked.length > 0) {
    lbEl.style.display = 'block';
    const maxOpens = ranked[0]._opens;
    document.getElementById('lb-body').innerHTML = ranked.map((e, i) => `
      <div class="lb-row">
        <span class="lb-rank">${i + 1}.</span>
        <span class="lb-name">${e.project}</span>
        <div class="lb-bar"><div class="lb-bar-fill" style="width:${e._opens / maxOpens * 100}%"></div></div>
        <span class="lb-stat">${e._opens} opens</span>
        <span class="lb-stat">${e._vote === 'up' ? '\uD83D\uDC4D' : e._vote === 'down' ? '\uD83D\uDC4E' : '\u2014'}</span>
      </div>
    `).join('');
  } else {
    lbEl.style.display = 'none';
  }

  // Category pills
  const cats = {};
  data.forEach(e => { cats[e.category] = (cats[e.category] || 0) + 1; });
  const catEntries = [['all', 'All', total], ...Object.entries(cats).sort((a,b) => b[1] - a[1]).map(([c, n]) => [c, c, n])];
  document.getElementById('cat-pills').innerHTML = catEntries.map(([val, label, count]) =>
    `<button class="pill ${val === activeCategory ? 'active' : ''}" onclick="setCat('${val.replace(/'/g, "\\'")}')">${label}<span class="count">${count}</span></button>`
  ).join('');

  // Status pills (include refined filter)
  document.getElementById('status-pills').innerHTML = [
    ['all', 'All'],['working','\u2705 Working'],['refined','\u2728 Refined'],['unrefined','Unrefined'],['failed','\u274c Culled']
  ].map(([val, label]) =>
    `<button class="pill ${val === activeStatus ? 'active' : ''}" onclick="setStatus('${val}')">${label}</button>`
  ).join('');

  // Vote filter pills
  document.getElementById('vote-pills').innerHTML = [
    ['all', 'All Votes'],['up','\uD83D\uDC4D Liked'],['down','\uD83D\uDC4E Disliked'],['unrated','Unrated']
  ].map(([val, label]) =>
    `<button class="pill ${val === activeVote ? 'active' : ''}" onclick="setVote('${val}')">${label}</button>`
  ).join('');

  // Range pills
  document.getElementById('range-pills').innerHTML = [
    [10, 'Last 10'],[25, 'Last 25'],[50, 'Last 50'],[0, 'All']
  ].map(([val, label]) =>
    `<button class="pill ${val === activeRange ? 'active' : ''}" onclick="setRange(${val})">${label}</button>`
  ).join('');

  if (filtered.length === 0) {
    document.getElementById('feed').innerHTML = `<div class="empty">${total === 0 ? 'No builds yet.' : 'No projects match your filters.'}</div>`;
    return;
  }

  // Group by category only in category sort mode
  const useGroups = sortMode === 'date';

  if (useGroups) {
    const grouped = {};
    const catOrder = Object.keys(CATEGORIES).concat(['Other']);
    filtered.forEach(e => { (grouped[e.category] = grouped[e.category] || []).push(e); });

    let html = '';
    for (const cat of catOrder) {
      if (!grouped[cat] || grouped[cat].length === 0) continue;
      const def = CATEGORIES[cat] || { icon: '\uD83D\uDCC2' };
      html += `<div class="category">
        <div class="category-header">
          <span class="category-icon">${def.icon || ''}</span> ${cat}
          <span class="category-count">${grouped[cat].length} project${grouped[cat].length > 1 ? 's' : ''}</span>
        </div>
        <div class="${viewMode === 'grid' ? 'grid' : 'list'}">`;
      for (const e of grouped[cat]) html += renderEntry(e);
      html += `</div></div>`;
    }
    document.getElementById('feed').innerHTML = html;
  } else {
    // Separate refined from unrefined with section headers
    const refinedItems = filtered.filter(e => e.refined);
    const unrefinedItems = filtered.filter(e => !e.refined);
    let html = '';
    if (refinedItems.length > 0) {
      html += `<div class="section-divider">\u2728 Refined <span class="count">${refinedItems.length}</span></div>`;
      html += `<div class="${viewMode === 'grid' ? 'grid' : 'list'}">${refinedItems.map(renderEntry).join('')}</div>`;
    }
    if (unrefinedItems.length > 0) {
      html += `<div class="section-divider unrefined-section">\uD83D\uDD27 Awaiting Refinement <span class="count">${unrefinedItems.length}</span></div>`;
      html += `<div class="${viewMode === 'grid' ? 'grid' : 'list'} unrefined-section">${unrefinedItems.map(renderEntry).join('')}</div>`;
    }
    document.getElementById('feed').innerHTML = html;
  }

  // Wire up thumb buttons
  document.querySelectorAll('.thumb-btn').forEach(btn => {
    btn.addEventListener('click', function(ev) {
      ev.stopPropagation();
      const proj = this.dataset.project;
      const dir = this.dataset.dir;
      const current = getMetric(proj).vote;
      setMetric(proj, 'vote', current === dir ? null : dir);
      render();
    });
  });

  // Wire up launch links to track opens
  document.querySelectorAll('.launch-link[data-project]').forEach(link => {
    link.addEventListener('click', function() {
      trackOpen(this.dataset.project);
      // Re-render after a tick so the count updates
      setTimeout(render, 100);
    });
  });
}

function renderEntry(e) {
  const voteUp = e._vote === 'up';
  const voteDown = e._vote === 'down';
  const voteClass = voteUp ? 'thumbs-up' : voteDown ? 'thumbs-down' : '';
  const entryClass = (e.refined ? 'refined ' : '') + voteClass;

  const launchHtml = e.ui
    ? (e.ui.endsWith('.html')
      ? `<a class="launch-link" href="${e.ui}" target="_blank" data-project="${e.project}">\u25b6 Open</a>`
      : `<span class="launch-link script" title="Run: python3 ${e.ui}">\u26a1 Run</span>`)
    : '';

  const lastOpen = e._lastOpened ? timeAgo(e._lastOpened) : 'never';

  return `
    <div class="entry ${entryClass}">
      <div class="entry-header">
        <span class="entry-name">${e.project}${e.refined ? '<span class="refined-badge">refined</span>' : ''}</span>
        <span class="entry-date">${e.date}</span>
      </div>
      <div class="entry-idea">${e.idea}</div>
      <div class="entry-takeaway">${e.takeaway}</div>
      <div class="entry-metrics">
        <span class="metric"><span class="metric-icon">\uD83D\uDC41</span> ${e._opens}</span>
        <span class="metric">last: ${lastOpen}</span>
        <span style="margin-left:auto">
          <button class="thumb-btn thumb-up ${voteUp ? 'voted' : ''}" data-project="${e.project}" data-dir="up">\uD83D\uDC4D</button>
          <button class="thumb-btn thumb-down ${voteDown ? 'voted' : ''}" data-project="${e.project}" data-dir="down">\uD83D\uDC4E</button>
        </span>
      </div>
      <div class="entry-footer">
        <span class="entry-folder">${e.folder}/</span>
        <span>${launchHtml}</span>
      </div>
    </div>`;
}

function timeAgo(isoStr) {
  const diff = Date.now() - new Date(isoStr).getTime();
  const mins = Math.floor(diff / 60000);
  if (mins < 1) return 'just now';
  if (mins < 60) return mins + 'm ago';
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return hrs + 'h ago';
  const days = Math.floor(hrs / 24);
  return days + 'd ago';
}

window.setCat = function(c) { activeCategory = c; render(); };
window.setStatus = function(s) { activeStatus = s; render(); };
window.setVote = function(v) { activeVote = v; render(); };
window.setRange = function(n) { activeRange = n; render(); };

document.getElementById('search').addEventListener('input', function() {
  searchQuery = this.value; render();
});
document.getElementById('sort-select').addEventListener('change', function() {
  sortMode = this.value; render();
});
document.getElementById('view-grid').addEventListener('click', function() {
  viewMode = 'grid';
  this.classList.add('active');
  document.getElementById('view-list').classList.remove('active');
  render();
});
document.getElementById('view-list').addEventListener('click', function() {
  viewMode = 'list';
  this.classList.add('active');
  document.getElementById('view-grid').classList.remove('active');
  render();
});

render();
</script>
</body>
</html>'''


def get_refined_projects():
    """Scan learnings.md for refined project names."""
    learnings = ROOT / "learnings.md"
    refined = set()
    if learnings.exists():
        import re
        for line in learnings.read_text().split('\n'):
            m = re.match(r'^### (\S+) refinement \(', line)
            if m:
                refined.add(m.group(1))
    return refined

def update():
    log = json.loads(LOG_FILE.read_text()) if LOG_FILE.exists() else []
    refined = get_refined_projects()
    for entry in log:
        entry['refined'] = entry['project'] in refined
    html = TEMPLATE.replace('__LOG_DATA__', json.dumps(log))
    DASHBOARD.write_text(html)
    refined_count = sum(1 for e in log if e.get('refined'))
    print(f"Dashboard updated with {len(log)} entries ({refined_count} refined).")


if __name__ == "__main__":
    update()
