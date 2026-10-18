#!/usr/bin/env python3
"""Local search over everything in yolo-projects, built and unbuilt.

Rebuilds .index/yolo.db from the files every time (nothing is hand-maintained).

  python3 yolo_index.py build              # (re)build the index
  python3 yolo_index.py stats              # counts per kind
  python3 yolo_index.py search "word2 word2" [--kind K] [--status S] [-n 15]
  python3 yolo_index.py cards [--status S] [--verdict V] [--channel C] [-q TEXT] [-n 25]
  python3 yolo_index.py projects [-q TEXT] [-n 25]
  python3 yolo_index.py show <id-or-slug>  # full text of one entry

Kinds: project, card, learning, buildlog, video, doc, expdoc.
Card statuses: backlog discarded adopted deferred done in_progress skipped.
"""
import argparse, json, os, re, sqlite3, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(ROOT, ".index", "yolo.db")
SKIP_DIRS = {"experiments", "MEMORY", "scripts", "__pycache__", "node_modules"}


def rd(path):
    try:
        with open(os.path.join(ROOT, path), encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return ""


def jload(path):
    try:
        return json.loads(rd(path))
    except ValueError:
        return None


def title_of(md, default):
    m = re.search(r"^#\s+(.+)$", md, re.M)
    return m.group(1).strip() if m else default


def build():
    os.makedirs(os.path.dirname(DB), exist_ok=True)
    if os.path.exists(DB):
        os.remove(DB)
    c = sqlite3.connect(DB)
    c.execute("CREATE TABLE docs(id INTEGER PRIMARY KEY, kind, slug, title, status, verdict, "
              "channel, date, path, body)")
    c.execute("CREATE VIRTUAL TABLE fts USING fts5(title, body, content='docs', content_rowid='id', "
              "tokenize='porter unicode61')")

    def add(kind, slug, title, body, status="", verdict="", channel="", date="", path=""):
        c.execute("INSERT INTO docs(kind,slug,title,status,verdict,channel,date,path,body) "
                  "VALUES(?,?,?,?,?,?,?,?,?)",
                  (kind, slug, title or slug, status or "", verdict or "", channel or "",
                   date or "", path, body or ""))

    # build log lookup: project -> idea/takeaway
    log = jload(".harness/yolo_log.json") or []
    byproj = {}
    for e in log:
        byproj.setdefault(e.get("project"), []).append(e)
        add("buildlog", e.get("project", "?"), f'{e.get("project")}: {e.get("idea","")[:80]}',
            "\n".join(f"{k}: {v}" for k, v in e.items() if isinstance(v, (str, int, float))),
            status=e.get("status"), date=e.get("date"), path=".harness/yolo_log.json")

    # built projects: top-level dirs with a README or index.html
    for d in sorted(os.listdir(ROOT)):
        p = os.path.join(ROOT, d)
        if not os.path.isdir(p) or d.startswith(".") or d in SKIP_DIRS:
            continue
        readme = rd(f"{d}/README.md")
        index = rd(f"{d}/index.html")
        if not (readme or index):
            continue
        t = re.search(r"<title>(.*?)</title>", index, re.S)
        files = sorted(os.listdir(p))
        extra = "\n".join(f'{e.get("idea","")} {e.get("takeaway","")}' for e in byproj.get(d, []))
        body = f"{readme}\n{extra}\nfiles: {' '.join(files)}"
        add("project", d, title_of(readme, t.group(1).strip() if t else d), body,
            status="built", date=(byproj.get(d) or [{}])[0].get("date", ""),
            path=f"{d}/README.md" if readme else f"{d}/index.html")

    # cards
    for x in jload("experiments.json") or []:
        ex, src = x.get("experiment") or {}, x.get("source") or {}
        hist = "\n".join(f'{h.get("date","")} {h.get("status","")}: {h.get("note","")}'
                         for h in x.get("status_history") or [])
        steps = "\n".join(ex.get("actionable_steps") or [])
        body = "\n".join(str(v) for v in [
            ex.get("hypothesis"), ex.get("what_they_did"), steps, ex.get("success_metric"),
            ex.get("relevance_to_yolo_loop"), ", ".join(ex.get("target_project_ids") or []),
            "OUTCOME: " + str(x.get("outcome", "")), "NOTES: " + str(x.get("notes", "")),
            hist, "source video: " + str(src.get("video_title", ""))] if v)
        add("card", x.get("id", "?"), ex.get("title"), body, status=x.get("status"),
            verdict=x.get("verdict"), channel=src.get("channel"),
            date=src.get("ingested_date"), path="experiments.json")

    # build-memory learnings
    try:
        m = sqlite3.connect(os.path.join(ROOT, "build_memory.db"))
        for i, proj, date, typ, text in m.execute("SELECT id,project,date,type,text FROM learnings"):
            add("learning", f"L{i}", f"[{typ}] {proj}", text, status=typ, date=date,
                path="build_memory.db")
        m.close()
    except sqlite3.Error as e:
        print("build_memory.db skipped:", e, file=sys.stderr)

    # phase4 queue (videos seen)
    for v in jload("phase4_queue.json") or []:
        add("video", v.get("video_id", "?"), v.get("title"), v.get("notes", ""),
            status="processed" if v.get("processed") else "unprocessed",
            channel=v.get("channel"), date=v.get("fetched_date"), path="phase4_queue.json")

    # prose docs: root + .harness + experiments/*
    docs = [f for f in os.listdir(ROOT) if f.endswith(".md")]
    docs += [f".harness/{f}" for f in os.listdir(os.path.join(ROOT, ".harness")) if f.endswith(".md")]
    for rel in sorted(docs):
        t = rd(rel)
        add("doc", rel, title_of(t, rel), t, path=rel)
    for d in sorted(os.listdir(os.path.join(ROOT, "experiments"))):
        ed = os.path.join(ROOT, "experiments", d)
        if not os.path.isdir(ed):
            continue
        for f in sorted(os.listdir(ed)):
            if f.endswith((".md", ".json")):
                t = rd(f"experiments/{d}/{f}")
                add("expdoc", f"{d}/{f}", f"{d}: {f}", t, path=f"experiments/{d}/{f}")
    # session state
    add("doc", ".harness/session_state.json", "session state", rd(".harness/session_state.json"),
        path=".harness/session_state.json")

    c.execute("INSERT INTO fts(rowid,title,body) SELECT id,title,body FROM docs")
    c.commit()
    stats(c)
    c.close()


def conn():
    if not os.path.exists(DB):
        build()
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c


def stats(c=None):
    c = c or conn()
    print("indexed:")
    for k, n in c.execute("SELECT kind,count(*) FROM docs GROUP BY kind"):
        print(f"  {k:9} {n}")
    print("cards by status:", dict(c.execute(
        "SELECT status,count(*) FROM docs WHERE kind='card' GROUP BY status").fetchall()))
    print("cards by verdict:", dict(c.execute(
        "SELECT CASE verdict WHEN '' THEN '(none)' ELSE verdict END,count(*) FROM docs "
        "WHERE kind='card' GROUP BY 1").fetchall()))


def fts_query(q):
    words = re.findall(r"[\w-]+", q)
    return " ".join('"%s"' % w for w in words)


def snippet(c, rowid, q):
    r = c.execute("SELECT snippet(fts,1,'[',']','...',18) FROM fts WHERE fts MATCH ? AND rowid=?",
                  (fts_query(q), rowid)).fetchone()
    return r[0].replace("\n", " ") if r else ""


def listing(c, where, args, q, n):
    sql = "SELECT d.* FROM docs d "
    if q:
        sql += "JOIN fts ON fts.rowid=d.id AND fts MATCH ? "
        args = [fts_query(q)] + args
    sql += ("WHERE " + " AND ".join(where) if where else "") + (" ORDER BY rank" if q else " ORDER BY date DESC")
    rows = c.execute(sql + " LIMIT ?", args + [n]).fetchall()
    for r in rows:
        tag = "/".join(x for x in (r["kind"], r["status"], r["verdict"]) if x)
        print(f'- {r["slug"]}  [{tag}] {r["date"]}\n    {r["title"]}')
        if q:
            print("    " + snippet(c, r["id"], q))
    print(f"({len(rows)} shown)")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("build"); sp.add_parser("stats")
    s = sp.add_parser("search"); s.add_argument("q"); s.add_argument("--kind"); s.add_argument("--status")
    s.add_argument("--verdict"); s.add_argument("-n", type=int, default=15)
    k = sp.add_parser("cards"); k.add_argument("--status"); k.add_argument("--verdict")
    k.add_argument("--channel"); k.add_argument("-q"); k.add_argument("-n", type=int, default=25)
    p = sp.add_parser("projects"); p.add_argument("-q"); p.add_argument("-n", type=int, default=25)
    sh = sp.add_parser("show"); sh.add_argument("slug")
    a = ap.parse_args()

    if a.cmd == "build":
        return build()
    c = conn()
    if a.cmd == "stats":
        return stats(c)
    if a.cmd == "search":
        w, args = [], []
        for col in ("kind", "status", "verdict"):
            if getattr(a, col):
                w.append(f"d.{col}=?"); args.append(getattr(a, col))
        return listing(c, w, args, a.q, a.n)
    if a.cmd == "cards":
        w, args = ["d.kind='card'"], []
        for col in ("status", "verdict"):
            if getattr(a, col):
                w.append(f"d.{col}=?"); args.append(getattr(a, col))
        if a.channel:
            w.append("d.channel LIKE ?"); args.append(f"%{a.channel}%")
        return listing(c, w, args, a.q, a.n)
    if a.cmd == "projects":
        return listing(c, ["d.kind='project'"], [], a.q, a.n)
    if a.cmd == "show":
        for r in c.execute("SELECT * FROM docs WHERE slug=? OR slug LIKE ? ORDER BY kind", (a.slug, a.slug + "%")).fetchall()[:5]:
            print(f'=== {r["kind"]} {r["slug"]} [{r["status"]} {r["verdict"]}] {r["path"]}\n{r["title"]}\n\n{r["body"]}\n')


if __name__ == "__main__":
    main()
