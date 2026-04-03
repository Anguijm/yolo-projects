#!/usr/bin/env python3
"""Structured build logging for YOLO projects.

Usage (from cron or manual builds):
  from build_log import BuildLog
  log = BuildLog('project-name')
  log.event('idea_selected', {'idea': 'JSON to TS converter', 'filter_score': 'pass'})
  log.event('plan_created', {'outline': '...', 'types': 3, 'functions': 5})
  log.event('gemini_plan_critique', {'issues': 2, 'fixed': True})
  log.event('build_complete', {'lines': 450, 'time_sec': 38})
  log.event('test_result', {'passed': True, 'checks': 7})
  log.event('eval_bugs_result', {'matches': 0})
  log.event('council_review', {'bugs': 8, 'security': 9, 'ui': 7, 'guide': 6, 'usefulness': 8, 'cool': 7})
  log.event('fixes_applied', {'bug_fixes': 2, 'security_fixes': 1})
  log.event('retest_result', {'passed': True})
  log.event('shipped', {'log_entry': True, 'dashboard': True, 'pushed': True})
  log.save()

Also usable from CLI:
  python3 build_log.py <project> <event_name> [key=value ...]
  python3 build_log.py <project> --show
  python3 build_log.py --recent [N]
"""

import json
import sys
import os
from datetime import datetime, timezone
from pathlib import Path

LOG_DIR = Path(__file__).parent / 'build-logs'


class BuildLog:
    def __init__(self, project_name):
        self.project = project_name
        self.started = datetime.now(timezone.utc).isoformat()
        self.events = []
        self._file = LOG_DIR / f'{project_name}.json'

        # Load existing if resuming
        if self._file.exists():
            try:
                data = json.loads(self._file.read_text())
                self.started = data.get('started', self.started)
                self.events = data.get('events', [])
            except (json.JSONDecodeError, KeyError):
                pass

    def event(self, name, data=None):
        entry = {
            'event': name,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'data': data or {}
        }
        self.events.append(entry)
        return self

    def save(self):
        LOG_DIR.mkdir(exist_ok=True)
        doc = {
            'project': self.project,
            'started': self.started,
            'updated': datetime.now(timezone.utc).isoformat(),
            'event_count': len(self.events),
            'events': self.events
        }
        self._file.write_text(json.dumps(doc, indent=2))
        return self._file

    def summary(self):
        """One-line summary of the build."""
        council = next((e for e in reversed(self.events) if e['event'] == 'council_review'), None)
        shipped = any(e['event'] == 'shipped' for e in self.events)
        scores = ''
        if council:
            d = council['data']
            scores = f" council=[B:{d.get('bugs','?')} S:{d.get('security','?')} U:{d.get('ui','?')} G:{d.get('guide','?')} USE:{d.get('usefulness','?')} C:{d.get('cool','?')}]"
        status = 'SHIPPED' if shipped else 'IN PROGRESS'
        return f"{self.project}: {status} | {len(self.events)} events{scores}"


def show_log(project):
    f = LOG_DIR / f'{project}.json'
    if not f.exists():
        print(f'No build log for {project}')
        return
    data = json.loads(f.read_text())
    print(f"Build log: {data['project']}")
    print(f"Started:   {data['started']}")
    print(f"Updated:   {data['updated']}")
    print(f"Events:    {data['event_count']}")
    print()
    for ev in data['events']:
        ts = ev['timestamp'][11:19]
        d = ev['data']
        detail = ', '.join(f'{k}={v}' for k, v in d.items()) if d else ''
        print(f"  [{ts}] {ev['event']}: {detail}")


def show_recent(n=5):
    if not LOG_DIR.exists():
        print('No build logs yet.')
        return
    logs = sorted(LOG_DIR.glob('*.json'), key=lambda f: f.stat().st_mtime, reverse=True)[:n]
    for f in logs:
        try:
            bl = BuildLog(f.stem)
            print(bl.summary())
        except Exception:
            pass


if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(0)

    if args[0] == '--recent':
        n = int(args[1]) if len(args) > 1 else 5
        show_recent(n)
    elif len(args) >= 2 and args[1] == '--show':
        show_log(args[0])
    elif len(args) >= 2:
        project = args[0]
        event_name = args[1]
        data = {}
        for arg in args[2:]:
            if '=' in arg:
                k, v = arg.split('=', 1)
                # Try to parse as number or bool
                if v.lower() == 'true': v = True
                elif v.lower() == 'false': v = False
                else:
                    try: v = int(v)
                    except ValueError:
                        try: v = float(v)
                        except ValueError: pass
                data[k] = v
        bl = BuildLog(project)
        bl.event(event_name, data)
        bl.save()
        print(f'Logged: {project} -> {event_name}')
    else:
        show_log(args[0])
