#!/usr/bin/env python3
"""Agora chat daemon — a persistent presence for ONE agent (Claude or Gemini).

Runs as a systemd service, independent of any interactive CLI session. Watches the
shared chat log (data/agora/chat.jsonl); when a new message arrives that this agent
should answer, it invokes the agent's own CLI headless to generate ONE reply and
appends it to the log. Reasoning is stateless per message (the log IS the memory),
so the daemon survives restarts cleanly via a processed high-water mark.

Loop-guards live in CODE, not just the prompt, so the two agents cannot ping-pong
and drain the shared rate-limit pool:
  - never answer your own message
  - answer Radek (the human) — unless he addressed ONLY the other agent by name
  - answer the other agent only when it names/@mentions you
  - hard stop if the last N messages are all agents with no human turn (anti-runaway)

Usage:  agora_daemon.py <Claude|Gemini>
"""
import json
import logging
import os
import subprocess
import sys
import time
from datetime import datetime, timezone

REPO = "/opt/open-reporting"
LOG_FILE = f"{REPO}/data/agora/chat.jsonl"
POLL_SECONDS = 4
CLI_TIMEOUT = 150          # hard cap per reply so a stuck CLI can't wedge the daemon
TRANSCRIPT_TAIL = 24       # how many recent messages to feed the model
MAX_AGENT_STREAK = 4       # if the last N msgs have no human turn, stop replying
RETRY_BACKOFF = 120        # seconds to wait before retrying after a CLI failure (e.g. rate limit)

_cooldown_until = 0.0      # module state: skip reply attempts until this time

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


def append_reply(text):
    rec = {"ts": datetime.now(timezone.utc).isoformat(), "author": AGENT, "text": text}
    with open(LOG_FILE, "a", encoding="utf-8") as fh:
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


def should_reply(msgs):
    """Decide if this agent should answer the latest turn. Returns bool."""
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
        # addressed to the other agent only -> stay out
        return not (names_other and not names_me) or names_me or not names_other
    if author == OTHER:
        # answer another agent only when it names you
        return AGENT.lower() in text
    return False


def build_prompt(msgs):
    transcript = "\n".join(
        f"{m.get('author')}: {m.get('text')}" for m in msgs[-TRANSCRIPT_TAIL:]
    )
    return (
        f"You are {AGENT}, an AI collaborator in a 3-way group chat for the Open Reporting "
        f"project. Participants: Radek (the human owner/PO), and two AI collaborators — "
        f"Claude and Gemini. You are {AGENT}; the other AI is {OTHER}. Shared rules and lanes "
        f"are in docs/AGENT_CONTRACT.md.\n\n"
        f"Reply with ONE concise message, plain text only — no name prefix, no markdown "
        f"headings. If you genuinely have nothing useful to add, reply with exactly: <SKIP>\n\n"
        f"Recent conversation:\n{transcript}\n\nYour reply as {AGENT}:"
    )


def run_cli(prompt):
    # Claude reads the prompt on stdin; Gemini needs -p for headless (bare `gemini`
    # stays interactive and hangs). --approval-mode plan = read-only, never blocks
    # on a tool-approval prompt the daemon can't answer.
    if AGENT == "Claude":
        cmd = ["claude", "-p", "--model", "sonnet", "--permission-mode", "bypassPermissions"]
        stdin = prompt
    else:
        cmd = ["gemini", "-p", prompt, "-o", "text", "--approval-mode", "yolo", "--skip-trust"]
        stdin = None
    try:
        res = subprocess.run(
            cmd, input=stdin, capture_output=True, text=True,
            timeout=CLI_TIMEOUT, cwd=REPO,
        )
    except subprocess.TimeoutExpired:
        log.warning("CLI timed out after %ss", CLI_TIMEOUT)
        return False, ""
    if res.returncode != 0:
        log.warning("CLI exit %s: %s", res.returncode, (res.stderr or "")[:300])
        return False, (res.stdout or "").strip()
    return True, (res.stdout or "").strip()


def clean_reply(text):
    # drop a stray "Claude:" / "Gemini:" prefix some models add
    for name in (AGENT, OTHER):
        if text.lower().startswith(name.lower() + ":"):
            text = text[len(name) + 1:].strip()
    return text


def tick():
    """Process new messages. Returns True if handled (advance), False to retry later."""
    global _cooldown_until
    msgs = read_log()
    hwm = read_hwm()
    if hwm is None:                      # first ever start: skip existing backlog
        write_hwm(len(msgs))
        log.info("initialised high-water mark at %d (skipping backlog)", len(msgs))
        return True
    if len(msgs) <= hwm:
        return True                      # nothing new
    if not should_reply(msgs):
        write_hwm(len(msgs))             # consume: nothing for us to say
        return True
    log.info("new turn from %s -> generating reply", msgs[-1].get("author"))
    ok, raw = run_cli(build_prompt(msgs))
    if not ok:                           # rate limit / timeout: DON'T consume — back off and retry
        _cooldown_until = time.time() + RETRY_BACKOFF
        log.warning("reply failed (rate limit/timeout?); retrying in %ss", RETRY_BACKOFF)
        return False
    write_hwm(len(msgs))                 # consume only once we got a real result
    reply = clean_reply(raw)
    if not reply or reply.strip().upper().strip("<>") == "SKIP":
        log.info("no reply (empty or SKIP)")
        return True
    append_reply(reply)
    log.info("replied (%d chars)", len(reply))
    return True


def main():
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    log.info("agora daemon up: agent=%s other=%s log=%s", AGENT, OTHER, LOG_FILE)
    last_sig = None
    while True:
        try:
            if time.time() >= _cooldown_until:
                sig = os.path.getmtime(LOG_FILE) if os.path.exists(LOG_FILE) else 0
                if sig != last_sig:
                    if tick():           # advance the seen-marker only when handled
                        last_sig = sig
                    # on retry (tick→False) keep last_sig stale so we re-enter after cooldown
        except Exception:                # never let one bad cycle kill the daemon
            log.exception("tick failed")
        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    main()
