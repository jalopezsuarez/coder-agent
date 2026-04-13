#!/usr/bin/env python3
"""Kanban board — zero dependencies, pure Python 3"""
import http.server, json, os, re, threading, time, urllib.parse
from datetime import datetime

PORT = 8089
BASE = os.path.dirname(os.path.abspath(__file__))
BOARD = os.path.join(BASE, "coder-board", "coder-board.md")
NOTES = os.path.join(BASE, "coder-notes")

_change = threading.Event()
_last_mtime = {"board": 0.0, "notes": 0.0}


def _snapshot():
    b = os.path.getmtime(BOARD) if os.path.exists(BOARD) else 0.0
    n = 0.0
    if os.path.isdir(NOTES):
        for f in os.listdir(NOTES):
            if f.endswith(".md"):
                try:
                    t = os.path.getmtime(os.path.join(NOTES, f))
                    if t > n:
                        n = t
                except OSError:
                    pass
    return b, n


def _watcher():
    _last_mtime["board"], _last_mtime["notes"] = _snapshot()
    while True:
        time.sleep(1)
        b, n = _snapshot()
        if b != _last_mtime["board"] or n != _last_mtime["notes"]:
            _last_mtime["board"], _last_mtime["notes"] = b, n
            _change.set()


def extract_preview(txt):
    lines = txt.split("\n")
    last, best_date = -1, ""
    for i, l in enumerate(lines):
        m = re.match(r"###\s+(?:INSTRUCTIONS|PLANNING|EXECUTION|BUG FIX)\s+#\d+\s*—\s*(.+)", l)
        if m:
            date = m.group(1).strip()
            if date >= best_date:
                best_date, last = date, i
    if last < 0 or not best_date:
        return ""
    out = []
    for l in lines[last + 1:]:
        if re.match(r"###\s+", l):
            break
        if re.match(r"^---|^<!--", l.strip()):
            continue
        if re.match(r"^#{1,4}\s+", l):
            continue
        if not l.strip():
            continue
        out.append(re.sub(r"[#*_`\[\]]", "", l.strip()))
        if len(out) >= 3:
            break
    return " ".join(out)[:180]


def parse_board():
    if not os.path.exists(BOARD):
        return []
    with open(BOARD, encoding="utf-8") as f:
        text = f.read()
    cols, col = [], None
    for line in text.split("\n"):
        m = re.match(r"^## (.+)", line)
        if m:
            col = {"name": m.group(1).strip(), "tasks": []}
            cols.append(col)
            continue
        if col is None:
            continue
        m = re.match(r"^- \[([ x])\] \[\[(.+?)\]\](.*)", line)
        if m:
            full = m.group(2)
            tags = re.findall(r"#(\w+)", m.group(3))
            parts = full.split(" ", 1)
            code, title = (parts[0], parts[1]) if len(parts) > 1 else ("", full)
            task = {"code": code, "title": title, "full_name": full,
                    "done": m.group(1) == "x", "tags": tags,
                    "date": "", "updated": "", "preview": ""}
            nf = os.path.join(NOTES, full + ".md")
            if os.path.exists(nf):
                with open(nf, encoding="utf-8") as f2:
                    ntxt = f2.read()
                dm = re.search(r">\s*Created:\s*(.+)", ntxt)
                if dm:
                    task["date"] = dm.group(1).strip()
                um = re.search(r">\s*Last updated:\s*(.+)", ntxt)
                if um:
                    task["updated"] = um.group(1).strip()
                task["preview"] = extract_preview(ntxt)
            col["tasks"].append(task)
    return cols


def save_board(cols):
    lines = ["---", "kanban-plugin: board", "---", ""]
    for c in cols:
        lines.append("## " + c["name"])
        lines.append("")
        for t in c.get("tasks", []):
            ck = "x" if t.get("done") else " "
            tg = " ".join("#" + x for x in t.get("tags", []))
            entry = "- [" + ck + "] [[" + t["full_name"] + "]]"
            if tg:
                entry += " " + tg
            lines.append(entry)
        lines.append("")
    lines.append("%% kanban:settings")
    lines.append('{"kanban-plugin":"board","new-note-folder":"coder-notes"}')
    lines.append("%%")
    with open(BOARD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def safe(name):
    return name and ".." not in name and not name.startswith("/")


def get_note(name):
    if not safe(name):
        return ""
    p = os.path.join(NOTES, name + ".md")
    return open(p, encoding="utf-8").read() if os.path.exists(p) else ""


def save_note(name, content):
    if not safe(name):
        return
    with open(os.path.join(NOTES, name + ".md"), "w", encoding="utf-8") as f:
        f.write(content)


def update_status(name, col):
    if not safe(name):
        return
    p = os.path.join(NOTES, name + ".md")
    if not os.path.exists(p):
        return
    with open(p, encoding="utf-8") as f:
        text = f.read()
    text = re.sub(r"(>\s*Status:\s*).+", r"\g<1>" + col, text)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    text = re.sub(r"(>\s*Last updated:\s*).+", r"\g<1>" + now, text)
    with open(p, "w", encoding="utf-8") as f:
        f.write(text)


PAGE = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">
<title>Coder Agent</title>
<style>
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#0d1117;
  --surface:#161b22;
  --border:#30363d;
  --border-subtle:#21262d;
  --text:#e6edf3;
  --text2:#8b949e;
  --text3:#484f58;
  --accent:#58a6ff;
  --btn:#21262d;
  --btn-hover:#30363d;
  --card:#161b22;
  --card-hover:#1c2129;
  --red:#f85149;
  --green:#3fb950;
  --yellow:#d29922;
  --purple:#bc8cff;
  --orange:#f0883e;
  --overlay:rgba(1,4,9,0.5);
  --font:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans",Helvetica,Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji";
  --mono:ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,"Liberation Mono",monospace;
  --radius:6px;
  --radius-sm:3px;
}
html,body{height:100%;overflow:hidden}
body{font-family:var(--font);font-size:14px;color:var(--text);background:var(--bg);line-height:1.5}

.app{display:flex;flex-direction:column;height:100vh}
.header{display:flex;align-items:center;justify-content:space-between;padding:12px 16px;border-bottom:1px solid var(--border);background:var(--surface);flex-shrink:0}
.header-left{display:flex;align-items:center;gap:10px}
.header-title{font-size:14px;font-weight:600;color:#7afa4f}
.header-count{font-size:12px;color:var(--text2);background:var(--btn);padding:1px 8px;border-radius:10px;border:1px solid var(--border)}
.header-right{display:flex;align-items:center;gap:8px}
.search-box{position:relative;display:flex;align-items:center}
.search-box svg{position:absolute;left:8px;width:14px;height:14px;color:var(--text3);pointer-events:none}
.search-input{width:180px;height:32px;padding:0 8px 0 28px;border:1px solid var(--border);border-radius:var(--radius);background:var(--bg);color:var(--text);font-size:13px;font-family:var(--font);outline:none;transition:border-color .15s,width .2s}
.search-input::placeholder{color:var(--text3)}
.search-input:focus{border-color:var(--accent);width:240px}
.search-clear{position:absolute;right:6px;display:none;align-items:center;justify-content:center;width:18px;height:18px;border:none;border-radius:3px;background:var(--btn);color:var(--text3);cursor:pointer;padding:0;line-height:1}
.search-clear:hover{background:var(--btn-hover);color:var(--text)}
.search-box.has-value .search-clear{display:flex}
.btn-icon{display:flex;align-items:center;justify-content:center;width:32px;height:32px;border:1px solid var(--border);border-radius:var(--radius);background:var(--btn);color:var(--text2);cursor:pointer}
.btn-icon:hover{background:var(--btn-hover);color:var(--text);border-color:var(--text2)}
.btn-icon svg{width:16px;height:16px}
.card.search-hidden{display:none}

.board{display:flex;flex:1;overflow-x:auto;gap:12px;padding:16px;min-height:0;position:relative}
.column{display:flex;flex-direction:column;min-width:240px;max-width:300px;width:100%;flex-shrink:0}
.column.drag-over .col-cards{background:rgba(56,139,253,0.06);border-radius:var(--radius)}
.col-header{display:flex;align-items:center;gap:8px;padding:0 4px 8px}
.col-dot{width:8px;height:8px;border-radius:50%}
.col-name{font-size:12px;font-weight:600}
.col-count{font-size:12px;color:var(--text3);margin-left:auto}
.col-cards{flex:1;overflow-y:auto;display:flex;flex-direction:column;gap:6px;padding:4px 2px;min-height:40px;transition:background .15s}
.col-cards::-webkit-scrollbar{width:5px}
.col-cards::-webkit-scrollbar-track{background:transparent}
.col-cards::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px}

.card{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:10px 12px;cursor:grab;transition:background .15s,border-color .15s,box-shadow .15s}
.card:hover{background:var(--card-hover);border-color:var(--text2)}
.card.dragging{opacity:0.4;border-style:dashed;cursor:grabbing}
.card.active{border-color:var(--accent);box-shadow:0 0 0 1px var(--accent)}
.card-title{font-size:13px;font-weight:500;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;line-height:1.4}
.card-preview{font-size:12px;color:var(--text2);margin-top:4px;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;line-height:1.4}
.card-footer{display:flex;align-items:center;justify-content:space-between;margin-top:8px;gap:4px;flex-wrap:wrap}
.card-date{font-size:11px;color:var(--text3)}
.card-meta{display:flex;align-items:center;gap:4px;flex-wrap:wrap;justify-content:flex-end}
.card-id{font-size:12px;font-family:var(--mono);color:#fff;background:#1f6feb;padding:2px 6px;border-radius:var(--radius-sm);margin-right:5px;vertical-align:baseline}
.tag{font-size:11px;padding:1px 6px;border-radius:var(--radius-sm);font-weight:500}
.tag-coder{background:rgba(56,139,253,0.15);color:var(--accent)}
.tag-urgent{background:rgba(248,81,73,0.15);color:var(--red)}
.tag-blocked{background:rgba(210,153,34,0.15);color:var(--yellow)}
.tag-default{background:var(--btn);color:var(--text2)}

.empty{position:absolute;inset:0;display:none;align-items:center;justify-content:center;pointer-events:none}
.empty-box{text-align:center;max-width:380px;padding:0 16px}
.empty-box p{color:var(--text2);font-size:14px;margin-bottom:4px}
.empty-box .sub{color:var(--text3);font-size:12px}

/* Help modal */
.modal-bg{position:fixed;inset:0;background:var(--overlay);z-index:100;display:none;align-items:center;justify-content:center}
.modal-bg.open{display:flex}
.modal{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);width:560px;max-width:calc(100vw - 32px);box-shadow:0 16px 32px rgba(1,4,9,0.85)}
.modal-head{display:flex;align-items:center;justify-content:space-between;padding:12px 16px;border-bottom:1px solid var(--border)}
.modal-head h2{font-size:14px;font-weight:600}
.help-body{padding:16px;max-height:70vh;overflow-y:auto}
.help-body::-webkit-scrollbar{width:5px}
.help-body::-webkit-scrollbar-track{background:transparent}
.help-body::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px}
.help-section{margin-bottom:16px}
.help-section:last-child{margin-bottom:0}
.help-section h3{font-size:11px;font-weight:600;color:var(--text3);text-transform:uppercase;letter-spacing:0.5px;margin-bottom:8px}
.help-row{display:flex;gap:12px;padding:4px 0;font-size:13px}
.help-row code{font-family:var(--mono);font-size:12px;color:var(--accent);background:var(--btn);padding:2px 6px;border-radius:var(--radius-sm);white-space:nowrap}
.help-flow{display:flex;align-items:center;gap:6px;flex-wrap:wrap;font-size:12px;margin-bottom:8px}
.help-pill{padding:2px 8px;border-radius:var(--radius-sm);font-weight:500}
.help-arrow{color:var(--text3)}

/* Sidebar overlay */
.side-bg{position:fixed;inset:0;background:var(--overlay);z-index:50;display:none}
.side-bg.open{display:block}
.side{position:fixed;top:0;right:0;bottom:0;width:50%;max-width:100vw;min-width:320px;background:var(--surface);border-left:1px solid var(--border);z-index:60;display:none;flex-direction:column;box-shadow:-8px 0 24px rgba(1,4,9,0.6)}
.side.open{display:flex}
@media(max-width:700px){.side{width:100%;min-width:0;border-left:none}}
.side-head{display:flex;align-items:center;gap:8px;padding:12px 16px;border-bottom:1px solid var(--border);flex-shrink:0}
.side-badge{font-size:12px;font-family:var(--mono);font-weight:600;background:#1f6feb;color:#fff;padding:2px 8px;border-radius:var(--radius-sm)}
.side-status{font-size:12px;font-weight:500;padding:2px 8px;border-radius:var(--radius-sm)}
.side-title{font-size:14px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;flex:1}
.side-close{margin-left:auto;flex-shrink:0}
.side-meta{display:flex;align-items:center;gap:8px;padding:8px 16px;border-bottom:1px solid var(--border-subtle);font-size:12px;color:var(--text3);flex-shrink:0}
.side-tags{display:flex;align-items:center;gap:4px}
.tag-toggle{font-size:11px;padding:1px 6px;border-radius:var(--radius-sm);font-weight:500;cursor:pointer;transition:background .15s,color .15s;text-decoration:none;user-select:none}
.tag-toggle.off{background:var(--btn-hover);color:var(--text2)}
.side-dates{display:flex;align-items:center;gap:12px}
.side-actions{display:flex;margin-left:auto;flex-shrink:0}
.side-btn{display:flex;align-items:center;justify-content:center;width:30px;height:26px;border:1px solid var(--border);background:var(--btn);color:var(--text3);cursor:pointer;padding:0}
.side-btn:hover{background:var(--btn-hover);color:var(--text)}
.side-btn.on{background:#1f6feb;border-color:#1f6feb;color:#fff}
.side-btn:first-child{border-radius:var(--radius-sm) 0 0 var(--radius-sm)}
.side-btn:last-child{border-radius:0 var(--radius-sm) var(--radius-sm) 0}
.side-btn:not(:first-child){border-left:0}
.side-btn svg{width:14px;height:14px}
.side-body{flex:1;overflow:hidden;display:flex;flex-direction:column;min-height:0}
.side-body .md{flex:1;overflow-y:auto;padding:32px}
.side-body .md::-webkit-scrollbar{width:5px}
.side-body .md::-webkit-scrollbar-track{background:transparent}
.side-body .md::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px}
.side-body textarea{flex:1;background:var(--bg);color:var(--text);border:none;padding:16px 32px;font-family:var(--mono);font-size:13px;resize:none;line-height:1.5;outline:none}
.side-body textarea::-webkit-scrollbar{width:5px}
.side-body textarea::-webkit-scrollbar-track{background:transparent}
.side-body textarea::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px}
.btn-save{display:flex;align-items:center;justify-content:center;width:32px;height:32px;border:1px solid var(--border);border-radius:var(--radius);background:var(--btn);color:var(--text2);cursor:pointer;flex-shrink:0;transition:background .2s,border-color .2s,color .2s}
.btn-save:hover{background:var(--btn-hover);color:var(--text);border-color:var(--text2)}
.btn-save.ok{background:#238636;border-color:#2ea043;color:#fff}
.btn-save.err{background:#da3633;border-color:#f85149;color:#fff}
.btn-save svg{width:16px;height:16px}

/* GitHub Markdown */
.md{font-family:var(--font);font-size:14px;line-height:1.5;word-wrap:break-word;color:var(--text)}
.md h1{font-size:2em;font-weight:600;padding-bottom:.3em;border-bottom:1px solid var(--border);margin:24px 0 16px}
.md h2{font-size:1.5em;font-weight:600;padding-bottom:.3em;border-bottom:1px solid var(--border);margin:24px 0 16px;color:#fff}
.md h3{font-size:1.25em;font-weight:600;margin:24px 0 16px;color:#fcfe58}
.md h4{font-size:1em;font-weight:600;margin:24px 0 16px;color:#e59746}
.md h5{font-size:.875em;font-weight:600;margin:24px 0 16px}
.md h6{font-size:.85em;font-weight:600;color:var(--text3);margin:24px 0 16px}
.md p{margin:0 0 16px}
.md blockquote{padding:0 1em;color:var(--text2);border-left:.25em solid var(--border);margin:0 0}
.md blockquote>:first-child{margin-top:0}
.md blockquote>:last-child{margin-bottom:0}
.md ul,.md ol{padding-left:2em;margin:0 0 16px}
.md li{margin-top:.25em}
.md code{font-family:var(--mono);font-size:85%;padding:.2em .4em;background:#282a31;color:#15f844;border-radius:var(--radius-sm)}
.md pre{font-family:var(--mono);font-size:85%;padding:16px;overflow:auto;line-height:1.45;background:var(--bg);border-radius:var(--radius);margin:0 0 16px;border:1px solid var(--border)}
.md pre code{font-size:100%;padding:0;background:transparent;border:0}
.md hr{height:0;padding:0;margin:16px 0;background:var(--border);border:0;border-radius:2px}
.md table{display:block;width:max-content;max-width:100%;overflow:auto;margin:0 0 16px;border-spacing:0;border-radius:var(--radius);border:1px solid var(--border)}
.md table th,.md table td{padding:6px 13px;border-top:1px solid var(--border);border-left:1px solid var(--border)}
.md table th{font-weight:600}
.md table tr:first-child th{border-top:0}
.md table th:first-child,.md table td:first-child{border-left:0}
.md table tr{background:var(--surface)}
.md table tr:nth-child(2n){background:var(--bg)}
.md a{color:#4493f8;text-decoration:none;cursor:pointer}
.md a:hover{text-decoration:underline}
.md strong{font-weight:600}
.md del{color:var(--text2)}
.md .task-item{list-style:none;margin-left:-1.5em}
.md .task-item input{margin-right:.5em;vertical-align:middle}
.md.editable{cursor:text;outline:none;min-height:200px;border-left:2px solid var(--accent);margin-left:-2px}
.md.editable:focus{background:rgba(56,139,253,0.02)}
</style>
</head>
<body>
<div class="app">
  <header class="header">
    <div class="header-left">
      <svg width="20" height="20" viewBox="0 0 16 16" fill="var(--text2)"><path fill-rule="evenodd" d="M1.75 1.5a.25.25 0 0 0-.25.25v12.5c0 .138.112.25.25.25h12.5a.25.25 0 0 0 .25-.25V1.75a.25.25 0 0 0-.25-.25H1.75ZM0 1.75C0 .784.784 0 1.75 0h12.5C15.216 0 16 .784 16 1.75v12.5A1.75 1.75 0 0 1 14.25 16H1.75A1.75 1.75 0 0 1 0 14.25V1.75Zm9.22 3.72a.75.75 0 0 0 0 1.06L10.69 8 9.22 9.47a.75.75 0 1 0 1.06 1.06l2-2a.75.75 0 0 0 0-1.06l-2-2a.75.75 0 0 0-1.06 0ZM6.78 6.53a.75.75 0 0 0-1.06-1.06l-2 2a.75.75 0 0 0 0 1.06l2 2a.75.75 0 1 0 1.06-1.06L5.31 8l1.47-1.47Z"/></svg>
      <span class="header-title">Coder Agent</span>
      <span class="header-count" id="count">0 stories</span>
    </div>
    <div class="header-right">
      <div class="search-box" id="searchBox">
        <svg viewBox="0 0 16 16" fill="currentColor"><path d="M10.68 11.74a6 6 0 0 1-7.922-8.982 6 6 0 0 1 8.982 7.922l3.04 3.04a.749.749 0 0 1-.326 1.275.749.749 0 0 1-.734-.215ZM11.5 7a4.499 4.499 0 1 0-8.997 0A4.499 4.499 0 0 0 11.5 7Z"/></svg>
        <input class="search-input" id="searchInput" type="text" placeholder="Filter stories…" autocomplete="off" spellcheck="false">
        <button class="search-clear" id="searchClear" title="Clear">&times;</button>
      </div>
      <button class="btn-icon" id="helpBtn" title="Help">
        <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round"><circle cx="8" cy="8" r="6.25"/><line x1="8" y1="7" x2="8" y2="11"/><circle cx="8" cy="4.75" r=".5" fill="currentColor" stroke="none"/></svg>
      </button>
    </div>
  </header>
  <main class="board" id="board"></main>
</div>

<div class="empty" id="empty">
  <div class="empty-box">
    <p>No stories loaded</p>
    <p class="sub">Board file is empty</p>
  </div>
</div>

<!-- Help -->
<div class="modal-bg" id="helpModal">
  <div class="modal">
    <div class="modal-head">
      <h2>Quick Reference</h2>
      <button class="btn-icon" id="helpClose" style="border:0;background:transparent">
        <svg viewBox="0 0 16 16" fill="currentColor"><path d="M3.72 3.72a.75.75 0 0 1 1.06 0L8 6.94l3.22-3.22a.749.749 0 0 1 1.275.326.749.749 0 0 1-.215.734L9.06 8l3.22 3.22a.749.749 0 0 1-.326 1.275.749.749 0 0 1-.734-.215L8 9.06l-3.22 3.22a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042L6.94 8 3.72 4.78a.75.75 0 0 1 0-1.06Z"/></svg>
      </button>
    </div>
    <div class="help-body">
      <div class="help-section">
        <h3>Commands</h3>
        <div class="help-row"><code>Coder create task &lt;desc&gt;</code><span>Create story in BACKLOG</span></div>
        <div class="help-row"><code>Coder plan</code><span>Plan stories in PLAN column</span></div>
        <div class="help-row"><code>Coder execute</code><span>Implement stories in EXECUTION</span></div>
        <div class="help-row"><code>Coder move S001 to PLAN</code><span>Move story between columns</span></div>
        <div class="help-row"><code>Coder add to S001 &lt;text&gt;</code><span>Append to USER PROMPT</span></div>
        <div class="help-row"><code>Coder for S001 &lt;instr&gt;</code><span>Add instruction directly</span></div>
        <div class="help-row"><code>Coder status</code><span>Board summary</span></div>
        <div class="help-row"><code>Coder update memory</code><span>Re-index knowledge base</span></div>
        <div class="help-row"><code>Coder &lt;bug desc&gt;</code><span>Smart bug detection</span></div>
      </div>
      <div class="help-section">
        <h3>Workflow</h3>
        <div class="help-flow">
          <span class="help-pill" style="background:var(--btn);color:var(--text2)">BACKLOG</span>
          <span class="help-arrow">&rarr;</span>
          <span class="help-pill" style="background:rgba(210,153,34,0.15);color:var(--yellow)">PLAN</span>
          <span class="help-arrow">&rarr;</span>
          <span class="help-pill" style="background:rgba(188,140,255,0.15);color:var(--purple)">REVIEW</span>
          <span class="help-arrow">&rarr;</span>
          <span class="help-pill" style="background:rgba(56,139,253,0.15);color:var(--accent)">EXECUTION</span>
          <span class="help-arrow">&rarr;</span>
          <span class="help-pill" style="background:rgba(240,136,62,0.15);color:var(--orange)">TESTING</span>
          <span class="help-arrow">&rarr;</span>
          <span class="help-pill" style="background:rgba(63,185,80,0.15);color:var(--green)">DONE</span>
        </div>
        <div style="font-size:12px;color:var(--text3);line-height:1.6">
          Drag cards between columns. Click a card to view/edit its detail. Ctrl+S to save edits.
        </div>
      </div>
      <div class="help-section">
        <h3>Tags</h3>
        <div class="help-row"><span class="tag tag-coder">#coder</span><span>Assigned to agent</span></div>
        <div class="help-row"><span class="tag tag-urgent">#urgent</span><span>Processed first</span></div>
        <div class="help-row"><span class="tag tag-blocked">#blocked</span><span>Agent skips it</span></div>
      </div>
    </div>
  </div>
</div>

<!-- Sidebar -->
<div class="side-bg" id="sideBg"></div>
<div class="side" id="side">
  <div class="side-head">
    <span class="side-badge" id="sBadge"></span>
    <span class="side-status" id="sStatus"></span>
    <span class="side-title" id="sTitle"></span>
    <button class="btn-save" id="btn-save" title="Save">
      <svg viewBox="0 0 16 16" fill="currentColor"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg>
    </button>
    <button class="btn-icon side-close" id="btn-close">
      <svg viewBox="0 0 16 16" fill="currentColor"><path d="M3.72 3.72a.75.75 0 0 1 1.06 0L8 6.94l3.22-3.22a.749.749 0 0 1 1.275.326.749.749 0 0 1-.215.734L9.06 8l3.22 3.22a.749.749 0 0 1-.326 1.275.749.749 0 0 1-.734-.215L8 9.06l-3.22 3.22a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042L6.94 8 3.72 4.78a.75.75 0 0 1 0-1.06Z"/></svg>
    </button>
  </div>
  <div class="side-meta">
    <div class="side-tags">
      <a class="tag-toggle off" id="tagCoder" data-tag="coder">#coder</a>
      <a class="tag-toggle off" id="tagUrgent" data-tag="urgent">#urgent</a>
      <a class="tag-toggle off" id="tagBlocked" data-tag="blocked">#blocked</a>
    </div>
    <div class="side-dates">
      <span id="sCreated"></span>
      <span id="sUpdated"></span>
    </div>
    <div class="side-actions">
      <button class="side-btn on" id="btn-edit" title="Edit"><svg viewBox="0 0 16 16" fill="currentColor"><path d="M11.013 1.427a1.75 1.75 0 0 1 2.474 0l1.086 1.086a1.75 1.75 0 0 1 0 2.474l-8.61 8.61c-.21.21-.47.364-.756.445l-3.251.93a.75.75 0 0 1-.927-.928l.929-3.25c.081-.286.235-.547.445-.758l8.61-8.61Zm.176 4.823L9.75 4.81l-6.286 6.287a.253.253 0 0 0-.064.108l-.558 1.953 1.953-.558a.253.253 0 0 0 .108-.064Zm1.238-3.763a.25.25 0 0 0-.354 0L10.811 3.75l1.439 1.44 1.263-1.263a.25.25 0 0 0 0-.354Z"/></svg></button>
      <button class="side-btn" id="btn-source" title="Source"><svg viewBox="0 0 16 16" fill="currentColor"><path d="m11.28 3.22 4.25 4.25a.75.75 0 0 1 0 1.06l-4.25 4.25a.749.749 0 0 1-1.275-.326.749.749 0 0 1 .215-.734L13.94 8l-3.72-3.72a.749.749 0 0 1 .326-1.275.749.749 0 0 1 .734.215Zm-6.56 0a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042L2.06 8l3.72 3.72a.749.749 0 0 1-.326 1.275.749.749 0 0 1-.734-.215L.47 8.53a.75.75 0 0 1 0-1.06Z"/></svg></button>
      <button class="side-btn" id="btn-view" title="View"><svg viewBox="0 0 16 16" fill="currentColor"><path d="M8 2c1.981 0 3.671.992 4.933 2.078 1.27 1.091 2.187 2.345 2.637 3.023a1.62 1.62 0 0 1 0 1.798c-.45.678-1.367 1.932-2.637 3.023C11.67 13.008 9.981 14 8 14c-1.981 0-3.671-.992-4.933-2.078C1.797 10.831.88 9.577.43 8.899a1.62 1.62 0 0 1 0-1.798c.45-.678 1.367-1.932 2.637-3.023C4.33 2.992 6.019 2 8 2ZM1.679 7.932a.12.12 0 0 0 0 .136c.411.622 1.241 1.75 2.366 2.717C5.176 11.758 6.527 12.5 8 12.5c1.473 0 2.825-.742 3.955-1.715 1.124-.967 1.954-2.096 2.366-2.717a.12.12 0 0 0 0-.136c-.412-.621-1.242-1.75-2.366-2.717C10.824 4.242 9.473 3.5 8 3.5c-1.473 0-2.824.742-3.955 1.715-1.124.967-1.954 2.096-2.366 2.717ZM8 10a2 2 0 1 1-.001-3.999A2 2 0 0 1 8 10Z"/></svg></button>
    </div>
  </div>
  <div class="side-body" id="sBody"></div>
</div>

<script>
(function(){
var DOT={BACKLOG:'var(--text3)',PLAN:'var(--yellow)',REVIEW:'var(--purple)',EXECUTION:'var(--accent)',TESTING:'var(--orange)',DONE:'var(--green)'};
var SSTYLE={
  BACKLOG:'background:var(--btn);color:var(--text2)',
  PLAN:'background:rgba(210,153,34,0.15);color:var(--yellow)',
  REVIEW:'background:rgba(188,140,255,0.15);color:var(--purple)',
  EXECUTION:'background:rgba(56,139,253,0.15);color:var(--accent)',
  TESTING:'background:rgba(240,136,62,0.15);color:var(--orange)',
  DONE:'background:rgba(63,185,80,0.15);color:var(--green)'
};
var TSTYLE={
  coder:'background:rgba(56,139,253,0.15);color:var(--accent)',
  urgent:'background:rgba(248,81,73,0.15);color:var(--red)',
  blocked:'background:rgba(210,153,34,0.15);color:var(--yellow)'
};
var board=[],active=null,activeCI=-1,note='',mode='edit';

async function load(){
  board=await(await fetch('/api/board')).json();
  render();
}

function shortDate(s){
  var m=s.match(/^(\d{4})-(\d{2})-(\d{2})\s+(\d{2}:\d{2})/);
  if(!m)return s;
  return parseInt(m[3],10)+'/'+parseInt(m[2],10)+'/'+m[1].slice(2)+' '+m[4];
}

function render(){
  var el=document.getElementById('board'),total=0;
  el.innerHTML='';
  board.forEach(function(col,ci){
    total+=col.tasks.length;
    var d=document.createElement('div');d.className='column';d.dataset.ci=ci;
    var h=document.createElement('div');h.className='col-header';
    h.innerHTML='<span class="col-dot" style="background:'+(DOT[col.name]||'var(--text3)')+'"></span><span class="col-name">'+esc(col.name)+'</span><span class="col-count">'+col.tasks.length+'</span>';
    d.appendChild(h);
    var cards=document.createElement('div');cards.className='col-cards';cards.dataset.ci=ci;
    col.tasks.forEach(function(t,ti){
      var c=document.createElement('div');c.className='card'+(active&&active.full_name===t.full_name?' active':'');
      c.draggable=true;c.dataset.ci=ci;c.dataset.ti=ti;
      var htm='<div class="card-title">';
      if(t.code)htm+='<span class="card-id">'+esc(t.code)+'</span>';
      htm+=esc(t.title)+'</div>';
      if(t.preview)htm+='<div class="card-preview">'+esc(t.preview)+'</div>';
      htm+='<div class="card-footer"><span class="card-date">';
      var dt=t.updated||t.date;
      if(dt)htm+=esc(shortDate(dt));
      htm+='</span><div class="card-meta">';
      t.tags.forEach(function(tag){
        var tc='tag-default';
        if(tag==='coder')tc='tag-coder';else if(tag==='urgent')tc='tag-urgent';else if(tag==='blocked')tc='tag-blocked';
        htm+='<span class="tag '+tc+'">#'+esc(tag)+'</span>';
      });
      htm+='</div></div>';
      c.innerHTML=htm;
      cards.appendChild(c);
    });
    d.appendChild(cards);
    el.appendChild(d);
  });
  document.getElementById('count').textContent=total+' stor'+(total===1?'y':'ies');
  document.getElementById('empty').style.display=total?'none':'flex';
  if(typeof applyFilter==='function')applyFilter();
}

/* --- Drag & Drop --- */
var dragData=null;
var brd=document.getElementById('board');
brd.addEventListener('dragstart',function(e){
  var c=e.target.closest('.card');
  if(!c)return;
  c.classList.add('dragging');
  dragData={ci:+c.dataset.ci,ti:+c.dataset.ti};
  e.dataTransfer.effectAllowed='move';
});
brd.addEventListener('dragend',function(){
  dragData=null;
  document.querySelectorAll('.dragging').forEach(function(x){x.classList.remove('dragging')});
  document.querySelectorAll('.drag-over').forEach(function(x){x.classList.remove('drag-over')});
});
brd.addEventListener('dragover',function(e){
  e.preventDefault();
  var col=e.target.closest('.column');
  if(!col)return;
  document.querySelectorAll('.drag-over').forEach(function(x){x.classList.remove('drag-over')});
  col.classList.add('drag-over');
});
brd.addEventListener('drop',function(e){
  e.preventDefault();
  document.querySelectorAll('.drag-over').forEach(function(x){x.classList.remove('drag-over')});
  if(!dragData)return;
  var colEl=e.target.closest('.column');
  if(!colEl)return;
  var toCol=+colEl.dataset.ci;
  var cardsEl=colEl.querySelector('.col-cards');
  var children=cardsEl.querySelectorAll('.card:not(.dragging)');
  var insertAt=children.length;
  for(var i=0;i<children.length;i++){
    var rect=children[i].getBoundingClientRect();
    if(e.clientY<rect.top+rect.height/2){insertAt=i;break;}
  }
  var task=board[dragData.ci].tasks.splice(dragData.ti,1)[0];
  board[toCol].tasks.splice(insertAt,0,task);
  render();
  fetch('/api/board',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({columns:board,move:{name:task.full_name,column:board[toCol].name}})}).then(function(){return load();});
});

/* --- Card click -> sidebar --- */
brd.addEventListener('click',function(e){
  var c=e.target.closest('.card');
  if(!c)return;
  openSide(board[+c.dataset.ci].tasks[+c.dataset.ti],+c.dataset.ci);
});

async function openSide(t,ci){
  active=t;activeCI=ci;
  var r=await fetch('/api/note?name='+encodeURIComponent(t.full_name));
  note=(await r.json()).content;
  document.getElementById('sBadge').textContent=t.code;
  var st=document.getElementById('sStatus');
  var colName=board[ci].name;
  st.textContent=colName;st.style.cssText=SSTYLE[colName]||SSTYLE.BACKLOG;
  document.getElementById('sTitle').textContent=t.title;
  document.getElementById('sCreated').textContent=t.date?'Created: '+t.date:'';
  document.getElementById('sUpdated').textContent=t.updated?'Updated: '+t.updated:'';
  syncTags();
  showEdit();
  sRatio=0;
  document.getElementById('side').classList.add('open');
  document.getElementById('sideBg').classList.add('open');
  render();
}

function closeSide(){
  active=null;activeCI=-1;mode='edit';sRatio=0;
  document.getElementById('side').classList.remove('open');
  document.getElementById('sideBg').classList.remove('open');
  render();
}

function setBtn(m){
  mode=m;
  document.getElementById('btn-view').classList.toggle('on',m==='view');
  document.getElementById('btn-edit').classList.toggle('on',m==='edit');
  document.getElementById('btn-source').classList.toggle('on',m==='source');
}

var sRatio=0;
function scrollEl(){return document.querySelector('#sBody .md')||document.getElementById('editor');}
function saveScroll(){var el=scrollEl();if(!el)return;var mx=el.scrollHeight-el.clientHeight;sRatio=mx>0?el.scrollTop/mx:0;}
function restoreScroll(){var el=scrollEl();if(!el)return;var mx=el.scrollHeight-el.clientHeight;el.scrollTop=Math.round(sRatio*mx);}

function showView(){
  saveScroll();
  setBtn('view');
  document.getElementById('sBody').innerHTML='<div class="md">'+renderMd(note)+'</div>';

  requestAnimationFrame(restoreScroll);
}

function showEdit(){
  saveScroll();
  setBtn('edit');
  document.getElementById('sBody').innerHTML='<div class="md editable" contenteditable="true">'+renderMd(note)+'</div>';

  requestAnimationFrame(restoreScroll);
}

function showSource(){
  saveScroll();
  setBtn('source');
  var body=document.getElementById('sBody');
  body.innerHTML='';
  var ta=document.createElement('textarea');
  ta.id='editor';ta.value=note;ta.spellcheck=false;
  body.appendChild(ta);

  requestAnimationFrame(restoreScroll);
}

async function saveNote(){
  if(!active)return;
  if(mode==='source')note=document.getElementById('editor').value;
  else if(mode==='edit')note=htmlToMd(document.querySelector('#sBody .md'));
  else return;
  var btn=document.getElementById('btn-save');
  try{
    var r1=await fetch('/api/note',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({name:active.full_name,content:note})});
    var r2=await fetch('/api/board',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({columns:board})});
    btn.classList.add(r1.ok&&r2.ok?'ok':'err');
  }catch(e){btn.classList.add('err');}
  setTimeout(function(){btn.classList.remove('ok','err');},1500);
}

function htmlToMd(el){
  function walk(node){
    if(node.nodeType===3)return node.textContent;
    if(node.nodeType!==1)return '';
    var tag=node.tagName.toLowerCase(),kids='';
    if(tag!=='li')for(var i=0;i<node.childNodes.length;i++)kids+=walk(node.childNodes[i]);
    switch(tag){
      case 'h1':return '# '+kids.trim()+'\n\n';
      case 'h2':return '## '+kids.trim()+'\n\n';
      case 'h3':return '### '+kids.trim()+'\n\n';
      case 'h4':return '#### '+kids.trim()+'\n\n';
      case 'h5':return '##### '+kids.trim()+'\n\n';
      case 'h6':return '###### '+kids.trim()+'\n\n';
      case 'p':return kids+'\n\n';
      case 'br':return '\n';
      case 'strong':case 'b':return '**'+kids+'**';
      case 'em':case 'i':return '*'+kids+'*';
      case 'del':case 's':return '~~'+kids+'~~';
      case 'code':
        if(node.parentElement&&node.parentElement.tagName==='PRE')return kids;
        return '`'+kids+'`';
      case 'pre':return '```\n'+kids.trim()+'\n```\n\n';
      case 'blockquote':
        var bq=kids.trim().split('\n').map(function(l){return '> '+l;}).join('\n');
        return bq+'\n\n';
      case 'ul':case 'ol':return kids;
      case 'li':
        var cb=node.querySelector('input[type=checkbox]');
        var pf;
        if(cb)pf=cb.checked?'- [x] ':'- [ ] ';
        else if(node.parentElement&&node.parentElement.tagName==='OL')pf='1. ';
        else pf='- ';
        var litxt='',lisub='';
        for(var ci=0;ci<node.childNodes.length;ci++){
          var cn=node.childNodes[ci];
          if(cn.nodeType===1&&/^(UL|OL)$/.test(cn.tagName))lisub+=walk(cn);
          else litxt+=walk(cn);
        }
        var r=pf+litxt.trim()+'\n';
        if(lisub)lisub.split('\n').forEach(function(sl){if(sl)r+='  '+sl+'\n';});
        return r;
      case 'hr':return '\n---\n\n';
      case 'a':return '['+kids+']('+( node.getAttribute('href')||'')+')';
      case 'table':return tblToMd(node)+'\n';
      case 'thead':case 'tbody':case 'tfoot':case 'tr':return kids;
      case 'th':case 'td':return kids;
      case 'input':return '';
      case 'span':case 'div':return kids;
      default:return kids;
    }
  }
  var out='';
  for(var i=0;i<el.childNodes.length;i++)out+=walk(el.childNodes[i]);
  return out.replace(/\n{3,}/g,'\n\n').trim()+'\n';
}

function tblToMd(table){
  var rows=table.querySelectorAll('tr');
  if(!rows.length)return '';
  var out='',first=true;
  rows.forEach(function(tr){
    var cells=tr.querySelectorAll('th,td');
    var line='|';
    cells.forEach(function(c){line+=' '+c.textContent.trim()+' |';});
    out+=line+'\n';
    if(first){var sep='|';cells.forEach(function(){sep+='---|';});out+=sep+'\n';first=false;}
  });
  return out;
}

/* --- Events --- */
document.getElementById('btn-view').addEventListener('click',showView);
document.getElementById('btn-edit').addEventListener('click',showEdit);
document.getElementById('btn-source').addEventListener('click',showSource);
document.getElementById('btn-close').addEventListener('click',closeSide);
document.getElementById('btn-save').addEventListener('click',saveNote);
document.getElementById('sideBg').addEventListener('click',closeSide);
document.getElementById('helpBtn').addEventListener('click',function(){document.getElementById('helpModal').classList.toggle('open');});
document.getElementById('helpClose').addEventListener('click',function(){document.getElementById('helpModal').classList.remove('open');});
document.getElementById('helpModal').addEventListener('click',function(e){if(e.target===this)this.classList.remove('open');});
document.addEventListener('keydown',function(e){
  if(e.key==='Escape'){
    if(document.getElementById('helpModal').classList.contains('open'))document.getElementById('helpModal').classList.remove('open');
    else if(document.getElementById('side').classList.contains('open'))closeSide();
  }
  if((e.ctrlKey||e.metaKey)&&e.key==='s'&&mode!=='view'){e.preventDefault();saveNote();}
});

/* --- Tag toggles --- */
function syncTags(){
  ['coder','urgent','blocked'].forEach(function(tag){
    var btn=document.getElementById('tag'+tag.charAt(0).toUpperCase()+tag.slice(1));
    var on=active&&active.tags.indexOf(tag)!==-1;
    btn.classList.toggle('off',!on);
    btn.style.cssText=on?(TSTYLE[tag]||''):'';
  });
}
function toggleTag(tag){
  if(!active)return;
  var idx=active.tags.indexOf(tag);
  if(idx===-1)active.tags.push(tag);else active.tags.splice(idx,1);
  syncTags();
}
document.querySelectorAll('.tag-toggle').forEach(function(btn){
  btn.addEventListener('click',function(){toggleTag(this.dataset.tag);});
});

/* --- Search / filter --- */
var searchInput=document.getElementById('searchInput');
var searchBox=document.getElementById('searchBox');
var searchClear=document.getElementById('searchClear');
function norm(s){return s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();}
function applyFilter(){
  var q=norm(searchInput.value.trim());
  searchBox.classList.toggle('has-value',q.length>0);
  var shown=0;
  document.querySelectorAll('.card').forEach(function(c){
    var ci=+c.dataset.ci,ti=+c.dataset.ti;
    var t=board[ci]&&board[ci].tasks[ti];
    if(!t){c.classList.remove('search-hidden');shown++;return;}
    var hay=norm(t.code+' '+t.title+' '+t.tags.join(' ')+' '+(t.preview||''));
    var match=!q||hay.indexOf(q)!==-1;
    c.classList.toggle('search-hidden',!match);
    if(match)shown++;
  });
  document.querySelectorAll('.col-count').forEach(function(el){
    var col=el.closest('.column');
    var vis=col.querySelectorAll('.card:not(.search-hidden)').length;
    el.textContent=vis;
  });
}
searchInput.addEventListener('input',applyFilter);
searchClear.addEventListener('click',function(){searchInput.value='';applyFilter();searchInput.focus();});
document.addEventListener('keydown',function(e){if(e.key==='/'&&!e.ctrlKey&&!e.metaKey&&document.activeElement.tagName!=='INPUT'&&document.activeElement.tagName!=='TEXTAREA'&&!document.activeElement.isContentEditable){e.preventDefault();searchInput.focus();searchInput.select();}});

/* --- Markdown renderer --- */
function renderMd(txt){
  var html='',lines=txt.split('\n'),inCode=false,code=[],inList=false,lt='ul',tbl=[],inTbl=false,ulDepth=0,ulOpen=false;
  function fl(){if(inList){while(ulDepth>0){html+='</li></ul>';ulDepth--;}if(ulOpen){html+='</li>';ulOpen=false;}html+='</'+lt+'>';inList=false;}}
  function ft(){if(!inTbl)return;inTbl=false;if(!tbl.length)return;
    html+='<table>';
    for(var i=0;i<tbl.length;i++){var cells=tbl[i].split('|').slice(1,-1);var tg=i===0?'th':'td';
    html+='<tr>';for(var j=0;j<cells.length;j++)html+='<'+tg+'>'+il(cells[j].trim())+'</'+tg+'>';html+='</tr>';}
    html+='</table>';tbl=[];
  }
  for(var i=0;i<lines.length;i++){
    var l=lines[i];
    if(/^```/.test(l)){if(inCode){html+='<pre><code>'+esc(code.join('\n'))+'</code></pre>';code=[];inCode=false;}else{fl();ft();inCode=true;}continue;}
    if(inCode){code.push(l);continue;}
    if(/^\s*<!--/.test(l)){var j=i;while(j<lines.length&&lines[j].indexOf('-->')===-1)j++;i=j;continue;}
    if(/^\|/.test(l)){if(/^\|[\s\-:|]+\|$/.test(l.trim()))continue;fl();if(!inTbl){inTbl=true;tbl=[];}tbl.push(l);continue;}else ft();
    if(l.trim()===''){fl();continue;}
    if(/^(\s*[-*_]\s*){3,}$/.test(l.trim())){fl();html+='<hr>';continue;}
    var hm=l.match(/^(#{1,6})\s+(.+)/);
    if(hm){fl();var raw=hm[2],aid;
      var im=raw.match(/^(INSTRUCTIONS|PLANNING|EXECUTION|BUG FIX)\s+#(\d+)/);
      if(im) aid=im[1].toLowerCase().replace(/\s+/g,'-')+'-'+im[2];
      else aid=raw.replace(/[\u2014\u2013]/g,'').replace(/[^\w\s-]/g,'').trim().toLowerCase().replace(/\s+/g,'-');
      html+='<h'+hm[1].length+' id="'+esc(aid)+'">'+il(raw)+'</h'+hm[1].length+'>';continue;}
    if(/^>\s?/.test(l)){fl();html+='<blockquote><p>'+il(l.replace(/^>\s?/,''))+'</p></blockquote>';continue;}
    if(/^\s*[-*+]\s+\[[ xX]\]/.test(l)){if(!inList){html+='<ul>';inList=true;lt='ul';}var ck=/\[[xX]\]/.test(l);
      html+='<li class="task-item"><input type="checkbox" disabled'+(ck?' checked':'')+'> '+il(l.replace(/^\s*[-*+]\s+\[[ xX]\]\s*/,''))+'</li>';continue;}
    if(/^(\s*)[-*+]\s/.test(l)){var nd=RegExp.$1.length>=2?1:0,ct=il(l.replace(/^\s*[-*+]\s/,''));if(!inList){html+='<ul>';inList=true;lt='ul';ulDepth=0;ulOpen=false;}if(nd>ulDepth){html+='<ul><li>'+ct;ulDepth=nd;ulOpen=true;}else if(nd<ulDepth){while(ulDepth>nd){html+='</li></ul>';ulDepth--;}html+='</li><li>'+ct;ulOpen=true;}else{html+=(ulOpen?'</li>':'')+'<li>'+ct;ulOpen=true;}continue;}
    if(/^\s*\d+\.\s/.test(l)){if(!inList||lt!=='ol'){fl();html+='<ol>';inList=true;lt='ol';}html+='<li>'+il(l.replace(/^\s*\d+\.\s/,''))+'</li>';continue;}
    if(/^\s+[a-z]\.\s/.test(l)){if(!inList){html+='<ol style="list-style-type:lower-alpha">';inList=true;lt='ol';}html+='<li>'+il(l.replace(/^\s+[a-z]\.\s/,''))+'</li>';continue;}
    fl();html+='<p>'+il(l)+'</p>';
  }
  fl();ft();if(inCode)html+='<pre><code>'+esc(code.join('\n'))+'</code></pre>';
  return html;
}
function il(t){
  t=esc(t);
  t=t.replace(/\*\*(.+?)\*\*/g,'<strong>$1</strong>');
  t=t.replace(/\*(.+?)\*/g,'<em>$1</em>');
  t=t.replace(/_(.+?)_/g,'<em>$1</em>');
  t=t.replace(/`(.+?)`/g,'<code>$1</code>');
  t=t.replace(/~~(.+?)~~/g,'<del>$1</del>');
  t=t.replace(/\[([^\]]+)\]\((#[^)]+)\)/g,'<a href="$2" onclick="var el=document.getElementById(this.getAttribute(\'href\').slice(1));if(el){el.scrollIntoView({behavior:\'smooth\'});return false;}">$1</a>');
  t=t.replace(/\[([^\]]+)\]\(([^#][^)]*)\)/g,'<a href="$2" target="_blank" rel="noopener">$1</a>');
  t=t.replace(/\[\[([^\]]+)\]\]/g,'<span style="color:var(--accent)">$1</span>');
  return t;
}
function esc(s){var d=document.createElement('div');d.textContent=s;return d.innerHTML;}

load();
var es=new EventSource('/api/events');
es.onmessage=function(e){if(e.data==='reload')load();};
})();
</script>
</body>
</html>'''


class H(http.server.BaseHTTPRequestHandler):
    def nocache(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")

    def j(self, data, code=200):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.nocache()
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        if u.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html;charset=utf-8")
            self.nocache()
            self.end_headers()
            self.wfile.write(PAGE.encode())
        elif u.path == "/api/board":
            self.j(parse_board())
        elif u.path == "/api/note":
            q = urllib.parse.parse_qs(u.query)
            self.j({"content": get_note(q.get("name", [""])[0])})
        elif u.path == "/api/events":
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "keep-alive")
            self.send_header("X-Accel-Buffering", "no")
            self.end_headers()
            try:
                while True:
                    if _change.wait(timeout=30):
                        _change.clear()
                        self.wfile.write(b"data: reload\n\n")
                    else:
                        self.wfile.write(b": heartbeat\n\n")
                    self.wfile.flush()
            except (BrokenPipeError, ConnectionResetError, OSError):
                pass
        else:
            self.send_error(404)

    def do_POST(self):
        try:
            body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
        except (json.JSONDecodeError, ValueError):
            self.send_error(400)
            return
        if self.path == "/api/board":
            save_board(body.get("columns", []))
            mv = body.get("move")
            if mv:
                update_status(mv.get("name", ""), mv.get("column", ""))
            self.j({"ok": True})
        elif self.path == "/api/note":
            save_note(body.get("name", ""), body.get("content", ""))
            self.j({"ok": True})
        else:
            self.send_error(404)

    def handle(self):
        try:
            super().handle()
        except (ConnectionResetError, BrokenPipeError, OSError):
            pass

    def log_message(self, *a):
        pass


threading.Thread(target=_watcher, daemon=True).start()
print(f"Kanban -> http://localhost:{PORT}")
http.server.ThreadingHTTPServer.allow_reuse_address = True
http.server.ThreadingHTTPServer(("", PORT), H).serve_forever()
