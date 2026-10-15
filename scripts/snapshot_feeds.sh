#!/usr/bin/env bash
# Fetch the YouTube feed snapshot from this machine (the MS-S1, on the home
# network) and push it to the branch feeds/snapshot, which the Daily YouTube
# Research workflow reads. Installed in the MS-S1 crontab at 06:00 and 10:00
# JST (the research runs are at 06:37 and 10:37 JST).
#
# Layout on the MS-S1:
#   ~/projects/yolo-projects         this clone, on main (the code)
#   ~/projects/yolo-projects-feeds   git worktree of the same clone, on the
#                                    orphan branch feeds/snapshot (data only)
# Log: ~/projects/yolo-projects/snapshot.log
# Off switch: comment out the two snapshot_feeds.sh lines in `crontab -e`.
set -u
REPO="$(cd "$(dirname "$0")/.." && pwd)"
FEEDS="${FEEDS_WORKTREE:-$(dirname "$REPO")/yolo-projects-feeds}"
LOG="$REPO/snapshot.log"
export GIT_TERMINAL_PROMPT=0
rc=1

{
  echo "=== $(date '+%Y-%m-%d %H:%M:%S %Z') snapshot start ==="
  cd "$REPO" || { echo "ERROR: no repo at $REPO"; exit 1; }
  timeout 120 git pull -q --ff-only origin main \
    || echo "WARN: git pull of main failed; using the script as checked out"
  if [ ! -e "$FEEDS/.git" ]; then
    echo "ERROR: feeds worktree missing at $FEEDS (create with: git worktree add --orphan -b feeds/snapshot $FEEDS)"
    exit 1
  fi
  cd "$FEEDS" || exit 1
  timeout 120 git pull -q --rebase origin feeds/snapshot \
    || echo "WARN: git pull of feeds/snapshot failed; committing on top of the local branch"
  timeout 600 python3 "$REPO/scripts/fetch_feeds_snapshot.py" --out "$FEEDS/data/feeds/snapshot.json"
  rc=$?
  echo "fetch exit code $rc"
  if git ls-files --error-unmatch data/feeds/snapshot.json >/dev/null 2>&1 \
     && git diff --quiet -- data/feeds/snapshot.json; then
    echo "snapshot unchanged; nothing to commit"
  else
    git add data/feeds/snapshot.json
    if git commit -q -m "feeds: snapshot from ms-s1 $(date '+%Y-%m-%d %H:%M %Z')" \
       && timeout 120 git push -q origin HEAD:feeds/snapshot; then
      echo "pushed $(git rev-parse --short HEAD) to feeds/snapshot"
    else
      echo "ERROR: commit or push failed (the next run retries)"
    fi
  fi
  echo "=== end rc=$rc ==="
} >> "$LOG" 2>&1
exit "$rc"
