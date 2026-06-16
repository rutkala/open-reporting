#!/usr/bin/env python3
"""Agora daemon — two-layer presence for ONE agent (Claude or Gemini).

ORCHESTRATOR (this daemon): watches the shared chat log and replies FAST in
read-only / plan mode. It talks with Radek, thinks, plans, coordinates with the
other orchestrator, and DELEGATES. It never edits the repo itself, so it always
stays responsive to chat — you can check in and steer mid-flight.

WORKER: when the orchestrator decides real work is needed, it emits one or more
lines of the form `DISPATCH: <self-contained task spec>`. The daemon spawns each
as a BACKGROUND worker — a full-tools CLI run that makes the changes and posts
its result back to the chat — without blocking the orchestrator's chat loop.

So: Radek always talks to orchestrators; orchestrators delegate to workers.

Loop-guards (in code, not just prompt): never answer your own message; answer
Radek unless he named only the other agent; answer the other agent only when it
@mentions you; hard-stop on agent-only streaks. Survives restarts via a processed
high-water mark.

Usage:  agora_daemon.py <Claude|Gemini>
"""
import json
import logging
import os
import re
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone

REPO = "/opt/open-reporting"
LOG_FILE = f"{REPO}/data/agora/chat.jsonl"
POLL_SECONDS = 4
ORCH_TIMEOUT = 150         # orchestrator reply (read-only) — must stay snappy
WORKER_TIMEOUT = 900       # background worker — real multi-step changes get time
TRANSCRIPT_TAIL = 24       # how many recent messages to feed the orchestrator
MAX_AGENT_STREAK = 4       # if the last N msgs have no human turn, stop replying
RETRY_BACKOFF = 120        # seconds to back off after an orchestrator CLI failure
MAX_WORKERS = 2            # cap concurrent background workers (shared rate-limit pool)

_cooldown_until = 0.0
_append_lock = threading.Lock()
_worker_slots = threading.BoundedSemaphore(MAX_WORKERS)

AGENT = (sys.argv[1] if len(sys.argv) > 1 else "").strip()
if AGENT not in ("Claude", "Gemini"):
    sys.exit("usage: agora_daemon.py <Claude|Gemini>")
OTHER = "Gemini" if AGENT == "Claude" else "Claude"
HWM_FILE = f"{REPO}/data/agora/.{AGENT.lower()}.hwm"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger(f"agora.{AGENT.lower()}")

DISPATCH_RE = re.compile(r"^\s*DISPATCH:\s*(.+)$", re.IGNORECASE)

# Short CLI notices that are NOT real replies — usage/auth limits leaking to stdout.
_LIMIT_MARKERS = (
    "session limit", "usage limit", "rate limit", "hit your", "you've hit",
    "limit reached", "overloaded", "please run /login", "/upgrade",
)


# ---------- log i/o ----------
def read_log():
    if not os.path.exists(LOG_FILE):
        return []
    out = []
    with open(LOG_FILE, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return out


def append_msg(author, text):
    rec = {"ts": datetime.now(timezone.utc).isoformat(), "author": author, "text": text}
    with _append_lock, open(LOG_FILE, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        fh.flush()


def read_hwm():
    try:
        with open(HWM_FILE) as fh:
            return int(fh.read().strip())
    except (OSError, ValueError):
        return None


def write_hwm(n):
    with open(HWM_FILE, "w") as fh:
        fh.write(str(n))


# ---------- decision ----------
def should_reply(msgs):
    """Decide if this orchestrator should answer the latest turn. Returns bool."""
    if not msgs:
        return False
    last = msgs[-1]
    author, text = last.get("author", ""), (last.get("text") or "").lower()

    # anti-runaway: never extend an agent-only streak
    tail = msgs[-MAX_AGENT_STREAK:]
    if len(tail) >= MAX_AGENT_STREAK and all(m.get("author") != "Radek" for m in tail):
        return False

    if author == AGENT:
        return False
    if author == "Radek":
        names_me = AGENT.lower() in text
        names_other = OTHER.lower() in text
        return not (names_other and not names_me) or names_me or not names_other
    if author == OTHER:
        return AGENT.lower() in text
    return False


# ---------- prompts ----------
def build_orchestrator_prompt(msgs):
    transcript = "\n".join(
        f"{m.get('author')}: {m.get('text')}" for m in msgs[-TRANSCRIPT_TAIL:]
    )
    return (
        f"You are the {AGENT} ORCHESTRATOR in a 3-way chat for the Open Reporting project. "
        f"Participants: Radek (human owner/PO), and two AI orchestrators — Claude and Gemini. "
        f"You are {AGENT}; the other is {OTHER}.\n\n"
        f"YOUR ROLE: talk with Radek, think, plan, and COORDINATE. You are READ-ONLY — you may "
        f"read/search files to inform your answer, but you do NOT edit the repo yourself. Stay "
        f"responsive: reply quickly and concisely.\n\n"
        f"TO MAKE CHANGES, DELEGATE. When real work (edits, builds, commits) is needed in your "
        f"lane, add ONE line per task starting with `DISPATCH:` followed by a precise, "
        f"self-contained spec a worker can execute alone — name the files, the exact change, and "
        f"that it must commit only its own files. A background worker does it and posts the result "
        f"here. Anything you write that is NOT a DISPATCH line is your chat reply to Radek.\n\n"
        f"Lanes: Gemini=data+content (products/ingestion, products/warehouse, products/blog); "
        f"Claude=engine/infra (packages/dbr, infra, .claude) + prod health. To avoid overlap, "
        f"coordinate with {OTHER} here BEFORE dispatching work that touches shared files "
        f"(e.g. products/warehouse/source_registry.yaml).\n\n"
        f"Hard floors (also bind your workers): never force-push main; never delete "
        f"data/warehouse.duckdb or the telegram/discord dirs; never disable crons or bots.\n\n"
        f"Plain text only — no name prefix, no markdown headings. If nothing here is for you, "
        f"reply with exactly: <SKIP>\n\n"
        f"Recent conversation:\n{transcript}\n\n"
        f"Your reply as {AGENT} (chat text and/or DISPATCH lines):"
    )


def build_worker_prompt(task):
    return (
        f"You are a {AGENT} WORKER agent for the Open Reporting project (repo at {REPO}). An "
        f"orchestrator has delegated ONE task to you. Execute it fully and autonomously with all "
        f"tools (read, edit, run, commit), then report concisely (3-6 lines): what you changed, "
        f"which files, and any commit hash.\n\n"
        f"Follow docs/AGENT_CONTRACT.md: never force-push main; never delete data/warehouse.duckdb "
        f"or the telegram/discord dirs; never disable crons or bots. Commit ONLY the files you "
        f"created or changed, with explicit paths — NEVER `git add -A` (the tree holds other "
        f"uncommitted work).\n\n"
        f"TASK:\n{task}\n\nDo the work now, then give your concise report."
    )


# ---------- cli ----------
def _run(cmd, stdin, timeout):
    try:
        res = subprocess.run(
            cmd, input=stdin, capture_output=True, text=True, timeout=timeout, cwd=REPO,
        )
    except subprocess.TimeoutExpired:
        return False, "", "timeout"
    out = (res.stdout or "").strip()
    if res.returncode != 0:
        return False, out, (res.stderr or "")[:300]
    return True, out, ""


def _looks_like_limit_notice(text):
    low = text.lower()
    return len(text) < 200 and any(marker in low for marker in _LIMIT_MARKERS)


def run_orchestrator(prompt):
    # Read-only: Claude gets only Read/Grep/Glob; Gemini runs in plan (read-only) mode.
    if AGENT == "Claude":
        cmd = ["claude", "-p", "--model", "sonnet", "--permission-mode", "bypassPermissions",
               "--allowedTools", "Read,Grep,Glob"]
        stdin = prompt
    else:
        cmd = ["gemini", "-p", prompt, "-o", "text", "--approval-mode", "plan", "--skip-trust"]
        stdin = None
    ok, out, err = _run(cmd, stdin, ORCH_TIMEOUT)
    if not ok:
        log.warning("orchestrator CLI failed: %s", err)
        return False, ""
    if _looks_like_limit_notice(out):
        log.warning("orchestrator returned a limit notice, not a reply")
        return False, ""
    return True, out


def run_worker(task):
    # Full tools: Claude bypassPermissions (all), Gemini --approval-mode yolo (all).
    prompt = build_worker_prompt(task)
    if AGENT == "Claude":
        cmd = ["claude", "-p", "--model", "sonnet", "--permission-mode", "bypassPermissions"]
        stdin = prompt
    else:
        cmd = ["gemini", "-p", prompt, "-o", "text", "--approval-mode", "yolo", "--skip-trust"]
        stdin = None
    ok, out, err = _run(cmd, stdin, WORKER_TIMEOUT)
    if not ok:
        return f"(worker failed: {err or 'timeout'})"
    if _looks_like_limit_notice(out):
        return "(worker hit a usage limit — needs a retry later)"
    return out or "(worker finished with no output)"


# ---------- dispatch ----------
def clean_reply(text):
    for name in (AGENT, OTHER):
        if text.lower().startswith(name.lower() + ":"):
            text = text[len(name) + 1:].strip()
    return text


def parse_reply(reply):
    """Split an orchestrator reply into (chat_text, [task_specs])."""
    chat_lines, tasks = [], []
    for line in reply.splitlines():
        m = DISPATCH_RE.match(line)
        if m:
            spec = m.group(1).strip()
            if spec:
                tasks.append(spec)
        else:
            chat_lines.append(line)
    return "\n".join(chat_lines).strip(), tasks


def spawn_worker(task):
    def _job():
        with _worker_slots:                       # cap concurrency on the shared pool
            log.info("worker START: %s", task[:120])
            result = run_worker(task)
            append_msg(AGENT, f"\U0001f527 [worker] {result}")
            log.info("worker DONE (%d chars)", len(result))
    threading.Thread(target=_job, daemon=True).start()


# ---------- tick / main ----------
def tick():
    """Process the latest turn. Returns True if handled, False to retry later."""
    global _cooldown_until
    msgs = read_log()
    hwm = read_hwm()
    if hwm is None:                      # first ever start: skip existing backlog
        write_hwm(len(msgs))
        log.info("initialised high-water mark at %d (skipping backlog)", len(msgs))
        return True
    if len(msgs) <= hwm:
        return True
    if not should_reply(msgs):
        write_hwm(len(msgs))
        return True
    log.info("new turn from %s -> orchestrator", msgs[-1].get("author"))
    ok, raw = run_orchestrator(build_orchestrator_prompt(msgs))
    if not ok:                           # rate limit / timeout: don't consume — back off
        _cooldown_until = time.time() + RETRY_BACKOFF
        log.warning("orchestrator failed; retrying in %ss", RETRY_BACKOFF)
        return False
    write_hwm(len(msgs))                 # consume only once we got a real result
    reply = clean_reply(raw)
    if not reply or reply.strip().upper().strip("<>") == "SKIP":
        log.info("no reply (empty or SKIP)")
        return True
    chat, tasks = parse_reply(reply)
    if tasks and not chat:               # always acknowledge a dispatch in chat
        chat = f"On it — dispatching {len(tasks)} worker task(s); I'll post results here."
    if chat:
        append_msg(AGENT, chat)
        log.info("orchestrator replied (%d chars), %d dispatch(es)", len(chat), len(tasks))
    for task in tasks:
        spawn_worker(task)
    return True


def main():
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    log.info("agora orchestrator up: agent=%s other=%s log=%s", AGENT, OTHER, LOG_FILE)
    last_sig = None
    while True:
        try:
            if time.time() >= _cooldown_until:
                sig = os.path.getmtime(LOG_FILE) if os.path.exists(LOG_FILE) else 0
                if sig != last_sig:
                    if tick():
                        last_sig = sig
        except Exception:
            log.exception("tick failed")
        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    main()
