#!/usr/bin/env python3
"""
api-mocker: Define mock API endpoints in a browser UI, get a running server instantly.

Usage: python3 api_mocker.py [--port 8800]
"""

import argparse
import json
import re
import time
import webbrowser
from collections import deque
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# In-memory endpoint store
endpoints = []
request_log = deque(maxlen=200)


class MockHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def handle_request(self, method):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        # Read body (handle binary payloads gracefully)
        content_len = int(self.headers.get('Content-Length', 0))
        if content_len > 0:
            raw = self.rfile.read(content_len)
            try:
                body = raw.decode('utf-8')
            except UnicodeDecodeError:
                body = '<binary data>'
        else:
            body = ''

        # Admin UI
        if path == '/' and method == 'GET':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode())
            return

        # Admin API
        if path == '/_admin/endpoints':
            if method == 'GET':
                self.json_response(endpoints)
                return
            elif method == 'POST':
                try:
                    ep = json.loads(body)
                    ep.setdefault('id', int(time.time() * 1000))
                    ep.setdefault('method', 'GET')
                    ep.setdefault('path', '/example')
                    ep.setdefault('status', 200)
                    ep.setdefault('headers', {'Content-Type': 'application/json'})
                    ep.setdefault('body', '{"message": "hello"}')
                    ep.setdefault('delay', 0)
                    # Validate types
                    if not isinstance(ep.get('headers', {}), dict):
                        ep['headers'] = {'Content-Type': 'application/json'}
                    if not isinstance(ep.get('body', ''), str):
                        ep['body'] = json.dumps(ep['body'])
                    endpoints.append(ep)
                    self.json_response(ep, 201)
                except Exception as e:
                    self.json_response({'error': str(e)}, 400)
                return
            elif method == 'DELETE':
                try:
                    data = json.loads(body)
                    eid = data.get('id')
                    for i, ep in enumerate(endpoints):
                        if ep['id'] == eid:
                            endpoints.pop(i)
                            break
                    self.json_response({'ok': True})
                except Exception as e:
                    self.json_response({'error': str(e)}, 400)
                return

        if path == '/_admin/log':
            self.json_response(list(request_log)[-50:])
            return

        if path == '/_admin/log/clear':
            request_log.clear()
            self.json_response({'ok': True})
            return

        # Match against defined endpoints
        matched = None
        for ep in endpoints:
            if ep['method'].upper() == method.upper():
                # Escape path then replace :param with capture groups
                escaped = re.escape(ep['path'])
                pattern = re.sub(r'\\:(\w+)', r'(?P<\1>[^/]+)', escaped)
                m = re.fullmatch(pattern, path)
                if m:
                    matched = ep
                    break

        # Log request
        log_entry = {
            'time': time.strftime('%H:%M:%S'),
            'method': method,
            'path': self.path,
            'matched': matched['path'] if matched else None,
            'status': matched['status'] if matched else 404,
            'body': body[:500] if body else None,
        }
        request_log.append(log_entry)

        if matched:
            if matched.get('delay', 0) > 0:
                time.sleep(matched['delay'] / 1000)
            self.send_response(matched['status'])
            for k, v in matched.get('headers', {}).items():
                self.send_header(k, v)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(matched['body'].encode())
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'no matching endpoint', 'path': path, 'method': method}).encode())

    def json_response(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self): self.handle_request('GET')
    def do_POST(self): self.handle_request('POST')
    def do_PUT(self): self.handle_request('PUT')
    def do_DELETE(self): self.handle_request('DELETE')
    def do_PATCH(self): self.handle_request('PATCH')
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', '*')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.end_headers()


HTML_PAGE = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>API Mocker</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'SF Mono', 'Fira Code', monospace; background: #0a0a0a; color: #ccc; }
.layout { display: grid; grid-template-columns: 1fr 350px; height: 100vh; }
.main { overflow-y: auto; padding: 1.5rem; }
.sidebar { border-left: 1px solid #1a1a1a; display: flex; flex-direction: column; }
h1 { font-size: 1.3rem; color: #fff; margin-bottom: 0.3rem; }
.sub { color: #555; font-size: 0.75rem; margin-bottom: 1.5rem; }
.section-title { font-size: 0.85rem; color: #fff; margin-bottom: 0.8rem; display: flex; justify-content: space-between; align-items: center; }
button { background: #1a1a1a; border: 1px solid #333; color: #999; padding: 0.35rem 0.7rem; border-radius: 4px; cursor: pointer; font-family: inherit; font-size: 0.7rem; }
button:hover { color: #fff; border-color: #555; }
button.primary { background: #0a2a0a; color: #4ade80; border-color: #166534; }
.ep-card { background: #111; border: 1px solid #1a1a1a; border-radius: 8px; padding: 1rem; margin-bottom: 0.75rem; }
.ep-card:hover { border-color: #333; }
.ep-header { display: flex; gap: 0.5rem; align-items: center; margin-bottom: 0.6rem; }
.method-badge { font-size: 0.65rem; padding: 0.15rem 0.4rem; border-radius: 3px; font-weight: bold; }
.method-GET { background: #0a2a0a; color: #4ade80; }
.method-POST { background: #0a1a2a; color: #60a5fa; }
.method-PUT { background: #2a2000; color: #fbbf24; }
.method-DELETE { background: #2a0a0a; color: #f87171; }
.method-PATCH { background: #1a0a2a; color: #a78bfa; }
.ep-path { color: #fff; font-size: 0.85rem; }
.ep-status { color: #666; font-size: 0.75rem; margin-left: auto; }
.ep-body { background: #0d0d0d; padding: 0.5rem; border-radius: 4px; font-size: 0.7rem; color: #888; margin-top: 0.5rem; max-height: 80px; overflow: hidden; white-space: pre-wrap; }
.ep-actions { display: flex; gap: 0.3rem; margin-top: 0.5rem; }
.form { background: #111; border: 1px solid #1a1a1a; border-radius: 8px; padding: 1rem; margin-bottom: 1.5rem; }
.form-row { display: flex; gap: 0.5rem; margin-bottom: 0.5rem; align-items: center; }
.form-row label { font-size: 0.65rem; color: #555; width: 55px; text-align: right; }
.form-row input, .form-row select, .form-row textarea { background: #0a0a0a; border: 1px solid #222; color: #ccc; padding: 0.35rem 0.5rem; border-radius: 4px; font-family: inherit; font-size: 0.75rem; flex: 1; }
.form-row input:focus, .form-row textarea:focus { outline: none; border-color: #4ade80; }
.form-row textarea { min-height: 60px; resize: vertical; }
.sidebar-header { padding: 0.8rem 1rem; border-bottom: 1px solid #1a1a1a; display: flex; justify-content: space-between; align-items: center; }
.sidebar-header h2 { font-size: 0.8rem; color: #fff; }
.log-list { flex: 1; overflow-y: auto; }
.log-entry { padding: 0.4rem 1rem; border-bottom: 1px solid #111; font-size: 0.7rem; display: flex; gap: 0.5rem; }
.log-entry:hover { background: #111; }
.log-time { color: #444; width: 55px; }
.log-method { width: 45px; font-weight: bold; }
.log-path { flex: 1; color: #ccc; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.log-status { width: 30px; text-align: right; }
.log-status.s2xx { color: #4ade80; }
.log-status.s4xx { color: #f87171; }
.log-status.s5xx { color: #f87171; }
.empty { color: #444; font-size: 0.8rem; text-align: center; padding: 2rem; }
.base-url { font-size: 0.75rem; color: #4ade80; background: #0a1a0a; padding: 0.3rem 0.6rem; border-radius: 4px; border: 1px solid #1a3a1a; margin-bottom: 1.5rem; display: inline-block; cursor: pointer; }
</style>
</head>
<body>
<div class="layout">
<div class="main">
  <h1>API Mocker</h1>
  <p class="sub">Define endpoints, get a running mock API</p>
  <div class="base-url" id="base-url" onclick="navigator.clipboard.writeText(this.textContent)"></div>

  <div class="section-title">New Endpoint</div>
  <div class="form">
    <div class="form-row">
      <label>Method</label>
      <select id="f-method"><option>GET</option><option>POST</option><option>PUT</option><option>DELETE</option><option>PATCH</option></select>
      <label>Path</label>
      <input id="f-path" value="/api/users" placeholder="/api/resource">
    </div>
    <div class="form-row">
      <label>Status</label>
      <input id="f-status" type="number" value="200" style="width:60px;flex:none">
      <label>Delay</label>
      <input id="f-delay" type="number" value="0" placeholder="ms" style="width:60px;flex:none">
    </div>
    <div class="form-row">
      <label>Body</label>
      <textarea id="f-body">[{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]</textarea>
    </div>
    <div class="form-row"><label></label><button class="primary" onclick="addEndpoint()">Add Endpoint</button></div>
  </div>

  <div class="section-title"><span>Endpoints</span><span id="ep-count" style="color:#555;font-size:0.7rem"></span></div>
  <div id="endpoints"><div class="empty">No endpoints yet. Add one above.</div></div>
</div>

<div class="sidebar">
  <div class="sidebar-header"><h2>Request Log</h2><button onclick="clearLog()">Clear</button></div>
  <div class="log-list" id="log-list"></div>
</div>
</div>

<script>
const baseUrl = window.location.origin;
document.getElementById('base-url').textContent = baseUrl;

async function loadEndpoints() {
  const resp = await fetch('/_admin/endpoints');
  const eps = await resp.json();
  const el = document.getElementById('endpoints');
  document.getElementById('ep-count').textContent = eps.length + ' defined';
  if (eps.length === 0) { el.innerHTML = '<div class="empty">No endpoints yet.</div>'; return; }
  el.innerHTML = eps.map(ep => `
    <div class="ep-card">
      <div class="ep-header">
        <span class="method-badge method-${escHtml(ep.method)}">${escHtml(ep.method)}</span>
        <span class="ep-path">${escHtml(ep.path)}</span>
        <span class="ep-status">${ep.status}</span>
      </div>
      <div class="ep-body">${escHtml(ep.body)}</div>
      <div class="ep-actions">
        <button data-test-method="${escHtml(ep.method)}" data-test-path="${escHtml(ep.path)}">Test</button>
        <button data-delete-id="${ep.id}">Delete</button>
        ${ep.delay ? `<span style="font-size:0.65rem;color:#555">${ep.delay}ms delay</span>` : ''}
      </div>
    </div>
  `).join('');
}

function escHtml(s) { return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;'); }

async function addEndpoint() {
  const ep = {
    method: document.getElementById('f-method').value,
    path: document.getElementById('f-path').value,
    status: parseInt(document.getElementById('f-status').value) || 200,
    delay: parseInt(document.getElementById('f-delay').value) || 0,
    body: document.getElementById('f-body').value,
    headers: {'Content-Type': 'application/json'},
  };
  await fetch('/_admin/endpoints', { method: 'POST', body: JSON.stringify(ep) });
  loadEndpoints();
}

async function deleteEndpoint(id) {
  await fetch('/_admin/endpoints', { method: 'DELETE', body: JSON.stringify({id}) });
  loadEndpoints();
}

async function testEndpoint(method, path) {
  try {
    const resp = await fetch(path, { method });
    const text = await resp.text();
    alert(`${resp.status}\n\n${text.slice(0, 500)}`);
  } catch(e) { alert('Error: ' + e.message); }
  loadLog();
}

async function loadLog() {
  const resp = await fetch('/_admin/log');
  const log = await resp.json();
  const el = document.getElementById('log-list');
  el.innerHTML = log.reverse().map(l => {
    const sc = l.status < 300 ? 's2xx' : l.status < 500 ? 's4xx' : 's5xx';
    const mc = `method-${l.method}`;
    return `<div class="log-entry">
      <span class="log-time">${l.time}</span>
      <span class="log-method" style="color:${{'GET':'#4ade80','POST':'#60a5fa','PUT':'#fbbf24','DELETE':'#f87171','PATCH':'#a78bfa'}[l.method]||'#ccc'}">${l.method}</span>
      <span class="log-path">${escHtml(l.path)}</span>
      <span class="log-status ${sc}">${l.status}</span>
    </div>`;
  }).join('');
}

async function clearLog() {
  await fetch('/_admin/log/clear');
  loadLog();
}

// Event delegation for test/delete buttons
document.getElementById('endpoints').addEventListener('click', function(e) {
  var btn = e.target;
  if (btn.dataset.testMethod) {
    testEndpoint(btn.dataset.testMethod, btn.dataset.testPath);
  } else if (btn.dataset.deleteId) {
    deleteEndpoint(parseInt(btn.dataset.deleteId));
  }
});

loadEndpoints();
setInterval(loadLog, 2000);
loadLog();
</script>
</body>
</html>'''


def main():
    parser = argparse.ArgumentParser(description='API Mocker')
    parser.add_argument('--port', type=int, default=8800)
    parser.add_argument('--no-browser', action='store_true')
    args = parser.parse_args()

    # Add some default endpoints
    endpoints.extend([
        {'id': 1, 'method': 'GET', 'path': '/api/users', 'status': 200,
         'headers': {'Content-Type': 'application/json'},
         'body': '[{"id":1,"name":"Alice","email":"alice@example.com"},{"id":2,"name":"Bob","email":"bob@example.com"}]', 'delay': 0},
        {'id': 2, 'method': 'GET', 'path': '/api/users/:id', 'status': 200,
         'headers': {'Content-Type': 'application/json'},
         'body': '{"id":1,"name":"Alice","email":"alice@example.com"}', 'delay': 0},
        {'id': 3, 'method': 'POST', 'path': '/api/users', 'status': 201,
         'headers': {'Content-Type': 'application/json'},
         'body': '{"id":3,"name":"Created","message":"User created"}', 'delay': 100},
    ])

    print(f"API Mocker running on http://localhost:{args.port}")
    print(f"  Admin UI: http://localhost:{args.port}/")
    print(f"  {len(endpoints)} default endpoints loaded")
    print(f"  Press Ctrl+C to stop\n")

    if not args.no_browser:
        webbrowser.open(f'http://localhost:{args.port}')

    server = HTTPServer(('127.0.0.1', args.port), MockHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nStopped.')


if __name__ == '__main__':
    main()
