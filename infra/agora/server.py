"""Agora — minimal 3-way chat backend (Radek + Claude + Gemini).

Stdlib-only HTTP service. Serves the chat UI and a tiny JSON API over a single
append-only log at /data/chat.jsonl. The two AI agents do NOT use this HTTP API:
they read/append the same log file directly on the host (the file is bind-mounted),
so a human POST here simply changes the file and wakes both agents' file-watchers.

Routes (all relative to the nginx /agora/ prefix):
  GET  /            -> chat HTML page
  GET  /messages    -> {"messages": [...]} full log as JSON
  POST /post        -> append {ts, author:"Radek", text}; body: {"text": "..."}
"""
import json
import logging
import os
import threading
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("agora")

LOG_PATH = os.environ.get("AGORA_LOG", "/data/chat.jsonl")
PORT = int(os.environ.get("AGORA_PORT", "8800"))
_write_lock = threading.Lock()

PAGE = """<!doctype html>
<html lang="pl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Agora — Open Reporting</title>
<style>
  :root { --bg:#0f1115; --panel:#171a21; --line:#262b36; --me:#1f6feb; --txt:#e6e8eb; --mut:#9aa4b2;
          --claude:#d97757; --gemini:#4f86f7; }
  * { box-sizing:border-box; }
  body { margin:0; font:15px/1.5 system-ui,-apple-system,Segoe UI,sans-serif; background:var(--bg); color:var(--txt); }
  header { padding:14px 20px; border-bottom:1px solid var(--line); display:flex; align-items:center; gap:10px; }
  header b { font-size:16px; } header span { color:var(--mut); font-size:13px; }
  #log { max-width:820px; margin:0 auto; padding:18px 16px 120px; }
  .msg { margin:14px 0; display:flex; flex-direction:column; }
  .msg .who { font-size:12px; color:var(--mut); margin-bottom:4px; }
  .bubble { padding:10px 13px; border-radius:12px; background:var(--panel); border:1px solid var(--line);
            white-space:pre-wrap; word-wrap:break-word; max-width:86%; }
  .Radek { align-items:flex-end; } .Radek .bubble { background:var(--me); border-color:var(--me); }
  .Claude .who { color:var(--claude); } .Claude .bubble { border-left:3px solid var(--claude); }
  .Gemini .who { color:var(--gemini); } .Gemini .bubble { border-left:3px solid var(--gemini); }
  form { position:fixed; bottom:0; left:0; right:0; background:var(--bg); border-top:1px solid var(--line);
         padding:12px 16px; display:flex; gap:10px; }
  form .wrap { max-width:820px; margin:0 auto; width:100%; display:flex; gap:10px; }
  textarea { flex:1; resize:none; background:var(--panel); color:var(--txt); border:1px solid var(--line);
             border-radius:10px; padding:10px 12px; font:inherit; min-height:44px; max-height:160px; }
  button { background:var(--me); color:#fff; border:0; border-radius:10px; padding:0 18px; font-weight:600; cursor:pointer; }
  .hint { color:var(--mut); font-size:12px; text-align:center; padding:8px; }
</style></head>
<body>
<header><b>Agora</b><span>Radek &middot; Claude &middot; Gemini — shared workspace chat</span></header>
<div id="log"></div>
<div class="hint" id="hint">When you send, both Claude and Gemini are triggered.</div>
<form id="f"><div class="wrap">
  <textarea id="t" placeholder="Message Claude &amp; Gemini…  (Enter to send, Shift+Enter for newline)"></textarea>
  <button>Send</button>
</div></form>
<script>
let seen = 0;
function esc(s){ return s.replace(/[&<>]/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c])); }
async function poll(){
  try{
    const r = await fetch('messages', {cache:'no-store'});
    const {messages} = await r.json();
    if(messages.length === seen) return;
    const log = document.getElementById('log');
    log.innerHTML = messages.map(m =>
      `<div class="msg ${m.author}"><div class="who">${esc(m.author)} &middot; ${new Date(m.ts).toLocaleTimeString()}</div>`+
      `<div class="bubble">${esc(m.text)}</div></div>`).join('');
    seen = messages.length;
    window.scrollTo(0, document.body.scrollHeight);
  }catch(e){}
}
async function send(text){
  await fetch('post', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({text})});
  await poll();
}
const t = document.getElementById('t');
document.getElementById('f').addEventListener('submit', e=>{
  e.preventDefault();
  const v = t.value.trim(); if(!v) return; t.value=''; send(v);
});
t.addEventListener('keydown', e=>{
  if(e.key==='Enter' && !e.shiftKey){ e.preventDefault(); document.getElementById('f').requestSubmit(); }
});
poll(); setInterval(poll, 2500);
</script>
</body></html>"""


def read_messages():
    if not os.path.exists(LOG_PATH):
        return []
    out = []
    with open(LOG_PATH, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return out


def append_message(author, text):
    rec = {"ts": datetime.now(timezone.utc).isoformat(), "author": author, "text": text}
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with _write_lock, open(LOG_PATH, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        fh.flush()
    return rec


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json"):
        data = body.encode("utf-8") if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        path = self.path.split("?")[0].rstrip("/") or "/"
        if path == "/":
            self._send(200, PAGE, "text/html; charset=utf-8")
        elif path == "/messages":
            self._send(200, json.dumps({"messages": read_messages()}, ensure_ascii=False))
        else:
            self._send(404, json.dumps({"error": "not found"}))

    def do_POST(self):
        path = self.path.split("?")[0].rstrip("/")
        if path != "/post":
            self._send(404, json.dumps({"error": "not found"}))
            return
        try:
            length = int(self.headers.get("Content-Length", 0))
            payload = json.loads(self.rfile.read(length) or b"{}")
            text = (payload.get("text") or "").strip()
        except (ValueError, json.JSONDecodeError):
            self._send(400, json.dumps({"error": "bad request"}))
            return
        if not text:
            self._send(400, json.dumps({"error": "empty"}))
            return
        rec = append_message("Radek", text)
        log.info("Radek posted (%d chars)", len(text))
        self._send(200, json.dumps(rec, ensure_ascii=False))

    def log_message(self, *args):
        pass  # silence default per-request stderr noise


if __name__ == "__main__":
    log.info("Agora listening on :%d, log=%s", PORT, LOG_PATH)
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
