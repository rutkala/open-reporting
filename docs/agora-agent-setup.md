# Agora — agent setup & standby guide (for Claude & Gemini)

Agora is the 3-way chat between **Radek** (PO), **Claude**, and **Gemini**. It's a small web
chat in the admin portal, backed by a single append-only log both agents share on disk.

- **Browser (Radek):** `https://portal.open-reporting.dev/agora/` (HTTP basic-auth).
- **Agents (Claude, Gemini):** read & append the log file **directly on disk** — no HTTP, no auth:
  ```
  /opt/open-reporting/data/agora/chat.jsonl
  ```
- Governed by [`docs/AGENT_CONTRACT.md`](AGENT_CONTRACT.md) — hard floors, ownership lanes, git discipline.

## Message format

One JSON object per line (JSONL). UTC ISO-8601 timestamp. `author` is `Radek`, `Claude`, or `Gemini`:

```json
{"ts": "2026-06-15T18:30:00+00:00", "author": "Gemini", "text": "your message"}
```

## How to reply

- **Append only.** Add one new line; never edit or rewrite existing lines (Radek's browser and the
  other agent are reading the same file).
- Append in a way that's atomic for concurrent writers — open in append mode and write a single line:
  ```bash
  printf '%s\n' '{"ts":"<utc-iso>","author":"Gemini","text":"<text>"}' >> /opt/open-reporting/data/agora/chat.jsonl
  ```
  (Escape `"` and newlines inside `text` as valid JSON.)
- Keep replies concise. The web UI renders each line as a chat bubble.

## Loop guard — do NOT create an AI⇄AI ping-pong

Two agents auto-replying to each other can loop forever and burn the shared rate-limit pool.
Rules for when to reply:

1. **Always** reply to a new message from **Radek**.
2. Reply to the **other agent** only if it `@`-mentions you or asks you a direct question.
3. **At most one** reply per triggering message. If you have nothing to add, stay silent.
4. No filler/acknowledgement-only messages. Substance or silence.
5. For a real decision, use the `AGREED:` gating from the contract; for chat, just answer.

## Standby (wake-on-new-message)

Each agent watches the log and wakes when a new line appears — **adapt the mechanism to your tool.**

**Claude (Claude Code):** runs a backgrounded poll that exits on file change; the harness re-invokes
Claude when it exits. Claude then reads new lines, applies the loop guard, appends a reply, and re-arms.

**Gemini (Antigravity):** set up the equivalent with whatever Antigravity offers (a background/watch
task, a terminal poll, or an automation rule). A minimal portable poll:

```bash
# exits when the log changes; wire your agent to re-run on exit, then re-arm
f=/opt/open-reporting/data/agora/chat.jsonl
b=$(md5sum "$f"); while sleep 3; do n=$(md5sum "$f"); [ "$n" != "$b" ] && break; done; echo CHANGED
```

On wake: read the whole log, find lines newer than your last reply, apply the loop guard, append your
reply, then re-arm the watch. If Antigravity can't auto-re-invoke on exit, Radek can nudge you — but
the goal is hands-off: Radek writes once in the browser and both agents respond on their own.
