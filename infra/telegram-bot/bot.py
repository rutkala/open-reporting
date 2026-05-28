#!/usr/bin/env python3
"""
Open Reporting Telegram bot.

Routes between two brains:
  - Gemini API (real-time conversational): default for any message
  - Claude autonomous-lead (queued for next run): /queue <task>

Plus:
  - /status   → last entry from docs/decisions.md
  - /reset    → reset Gemini conversation context
  - /help     → command reference

Bidirectional: the bot also polls data/telegram-outbox/ every OUTBOX_POLL_SEC
and posts any new files to the chat (this is how Claude reports back from
autonomous runs).

Security: only TELEGRAM_ALLOWED_USER_ID can interact. Everyone else gets
silently ignored.

Linear: project lead infra.
"""
from __future__ import annotations

import asyncio
import logging
import os
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# ─── Config ──────────────────────────────────────────────────────────────────

REPO = Path("/opt/open-reporting")
load_dotenv(REPO / ".env", override=True)

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
ALLOWED_USER_ID = int(os.environ["TELEGRAM_ALLOWED_USER_ID"])
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
CLAUDE_CHAT_MODEL = os.environ.get("CLAUDE_CHAT_MODEL", "sonnet")
CLAUDE_BIN = shutil.which("claude") or "/home/radek/.local/bin/claude"
CLAUDE_TIMEOUT_SEC = 180

INBOX_DIR = REPO / "data" / "telegram-inbox"
OUTBOX_DIR = REPO / "data" / "telegram-outbox"
ARCHIVE_DIR = REPO / "data" / "telegram-outbox" / "archive"
STATE_FILE = REPO / "data" / "telegram-bot.state"
DECISIONS_FILE = REPO / "docs" / "decisions.md"

OUTBOX_POLL_SEC = 30

GEMINI_SYSTEM_PROMPT = """You are Gemini, in a 3-way Telegram chat with Radek (Product Owner of Open Reporting) and Claude (autonomous Project Lead running on the production VPS).

Open Reporting turns Polish public data into accessible, beautiful, useful products: dashboards at portal.open-reporting.dev, articles at www.open-reporting.dev.

Your role: brainstorming partner. You help Radek think, draft, refine — language and ideation focus. You do NOT have access to the codebase, DuckDB, Ghost CMS, or live infra — Claude does. When Radek asks anything that needs project state (what's deployed, what's in the database, what the code looks like), defer to Claude's reply in the same thread.

Claude will reply alongside you on every message. Don't duplicate what Claude can do better (state checks, code knowledge). Focus on what YOU do better: free-form brainstorm, language polish, drafting, framing ideas from scratch.

Default language: Polish for content questions (articles, KPIs, UI strings). English for technical discussion. Match Radek's language in the moment.

Be concise. ADHD-friendly: short, punchy, scannable. Long-form only when explicitly asked."""

CLAUDE_SYSTEM_PROMPT = """You are Claude, the autonomous Project Lead for Open Reporting, in a 3-way Telegram chat with Radek (PO) and Gemini.

You're running as a chat process spawned by the Telegram bot — not the 4×/day autonomous-lead run. You have full access to the codebase at /opt/open-reporting, the DuckDB warehouse, the Ghost CMS, and live infrastructure. Use your tools freely to answer with real state, not guesses.

Your role in chat:
- Answer state/code/data/infra questions with actual lookups (read files, run git log, curl URLs, query DuckDB)
- Make project decisions when asked
- Take action when Radek asks you to — you have bypass permissions and ownership of the project
- For long-running work (>5 min), prefer `/queue` (Radek can re-message with that command); for quick fixes, just do it

Gemini will reply in parallel on every message. Don't duplicate Gemini's strengths (free-form brainstorm, language polish). Focus on what YOU do: real project knowledge, real actions.

KEEP REPLIES SHORT. This is Telegram — 1-5 sentences usually. Code blocks only when essential. Polish or English to match Radek."""

# ─── Logging ─────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
log = logging.getLogger("or-bot")
logging.getLogger("httpx").setLevel(logging.WARNING)

# ─── Gemini client ───────────────────────────────────────────────────────────

gemini_client = genai.Client(api_key=GEMINI_API_KEY)
chat_sessions: dict[int, object] = {}  # user_id → chat session


def _new_chat():
    return gemini_client.chats.create(
        model=GEMINI_MODEL,
        config={"system_instruction": GEMINI_SYSTEM_PROMPT},
    )


# ─── State (chat_id persistence for outbox poller) ──────────────────────────


def _save_chat_id(chat_id: int) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(str(chat_id))


def _load_chat_id() -> int | None:
    if STATE_FILE.exists():
        try:
            return int(STATE_FILE.read_text().strip())
        except ValueError:
            return None
    return None


# ─── Allowlist guard ─────────────────────────────────────────────────────────


def _allowed(update: Update) -> bool:
    user = update.effective_user
    if user is None:
        return False
    if user.id == ALLOWED_USER_ID:
        return True
    log.warning(
        "ignoring message from non-allowlisted user id=%s username=%s text=%r",
        user.id,
        user.username,
        (update.message.text if update.message else "")[:80],
    )
    return False


# ─── Handlers ────────────────────────────────────────────────────────────────


async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    if not _allowed(update):
        return
    _save_chat_id(update.effective_chat.id)
    await update.message.reply_text(
        "Connected. Default chat = Gemini. `/queue <task>` sends work to Claude's next autonomous run. `/status` shows latest run. `/help` for full reference.",
    )


async def cmd_help(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    if not _allowed(update):
        return
    await update.message.reply_text(
        "Commands:\n"
        "  /queue <task>  — defer to Claude's next scheduled autonomous run (4×/day, 02/07/12/17 UTC)\n"
        "  /status        — last decisions.md entry (most recent autonomous run)\n"
        "  /reset         — reset Gemini conversation context\n"
        "  /help          — this message\n"
        "\n"
        "Anything else = both Gemini AND Claude respond in parallel.\n"
        "  • Gemini: free-form brainstorm, language, framing\n"
        "  • Claude: real project state, code lookups, immediate actions",
    )


async def cmd_status(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    if not _allowed(update):
        return
    if not DECISIONS_FILE.exists():
        await update.message.reply_text("No decisions.md found.")
        return
    text = DECISIONS_FILE.read_text()
    # Each entry starts with "## " — grab the most recent one.
    entries = re.split(r"^## ", text, flags=re.MULTILINE)
    if len(entries) < 2:
        await update.message.reply_text("decisions.md is empty.")
        return
    latest = "## " + entries[1].strip()
    # Telegram caps at 4096 chars
    if len(latest) > 3800:
        latest = latest[:3800] + "\n…(truncated)"
    await update.message.reply_text(latest)


async def cmd_reset(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    if not _allowed(update):
        return
    chat_sessions.pop(update.effective_user.id, None)
    await update.message.reply_text("Gemini context reset.")


async def cmd_queue(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    if not _allowed(update):
        return
    _save_chat_id(update.effective_chat.id)
    task = " ".join(ctx.args) if ctx.args else ""
    if not task:
        await update.message.reply_text("Usage: /queue <task>")
        return
    INBOX_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    inbox_file = INBOX_DIR / f"{ts}.md"
    inbox_file.write_text(
        f"# Queued via Telegram {ts}\n"
        f"From: Radek (user_id={update.effective_user.id})\n"
        f"Source: Telegram /queue\n"
        f"\n"
        f"{task}\n"
    )
    log.info("queued task %s (%d chars)", inbox_file.name, len(task))
    await update.message.reply_text(
        f"Queued for next autonomous run.\n"
        f"File: {inbox_file.name}\n"
        f"Next run: see /status after the next 02/07/12/17 UTC slot.",
    )


async def _gemini_reply(user_id: int, text: str) -> str:
    chat = chat_sessions.get(user_id)
    if chat is None:
        chat = _new_chat()
        chat_sessions[user_id] = chat
    try:
        resp = await asyncio.to_thread(chat.send_message, text)
        return (resp.text or "").strip() or "(empty response)"
    except Exception as e:
        log.exception("gemini error")
        chat_sessions.pop(user_id, None)
        return f"⚠️ Gemini error: {type(e).__name__}: {str(e)[:300]}"


async def _claude_reply(text: str) -> str:
    """Invoke `claude -p` as a subprocess with the chat prompt fed via stdin."""
    full_prompt = f"{CLAUDE_SYSTEM_PROMPT}\n\n---\nRadek (Telegram): {text}\n"
    try:
        proc = await asyncio.create_subprocess_exec(
            CLAUDE_BIN,
            "-p",
            "--model", CLAUDE_CHAT_MODEL,
            "--no-session-persistence",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(REPO),
            env={
                **os.environ,
                "HOME": "/home/radek",
                "PATH": "/home/radek/.local/bin:/usr/local/bin:/usr/bin:/bin",
            },
        )
        stdout, stderr = await asyncio.wait_for(
            proc.communicate(full_prompt.encode()),
            timeout=CLAUDE_TIMEOUT_SEC,
        )
        if proc.returncode != 0:
            err = stderr.decode("utf-8", errors="replace")[:500]
            return f"⚠️ Claude exited {proc.returncode}: {err}"
        reply = stdout.decode("utf-8", errors="replace").strip()
        return reply or "(empty response)"
    except asyncio.TimeoutError:
        try:
            proc.kill()
        except Exception:
            pass
        return f"⚠️ Claude timed out after {CLAUDE_TIMEOUT_SEC}s"
    except Exception as e:
        log.exception("claude error")
        return f"⚠️ Claude error: {type(e).__name__}: {str(e)[:300]}"


async def chat_handler(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    """Fire both Gemini and Claude in parallel; post each reply when ready."""
    if not _allowed(update):
        return
    _save_chat_id(update.effective_chat.id)
    user_id = update.effective_user.id
    text = update.message.text or ""

    await update.message.chat.send_action(ChatAction.TYPING)

    gemini_task = asyncio.create_task(_gemini_reply(user_id, text))
    claude_task = asyncio.create_task(_claude_reply(text))

    async def _send_when_ready(task: asyncio.Task, label: str) -> None:
        try:
            reply = await task
        except Exception as e:
            reply = f"⚠️ {label} crashed: {type(e).__name__}: {e}"
        body = f"*{label}*\n{reply}"
        for chunk_start in range(0, len(body), 4000):
            try:
                await update.message.reply_text(
                    body[chunk_start : chunk_start + 4000],
                    parse_mode="Markdown",
                )
            except Exception:
                # Fallback to plain text if Markdown parsing breaks
                await update.message.reply_text(body[chunk_start : chunk_start + 4000])

    await asyncio.gather(
        _send_when_ready(gemini_task, "Gemini"),
        _send_when_ready(claude_task, "Claude"),
    )


# ─── Outbox poller ───────────────────────────────────────────────────────────


async def outbox_poller(app: Application) -> None:
    """Watch data/telegram-outbox/ for new files and post them to the chat."""
    OUTBOX_DIR.mkdir(parents=True, exist_ok=True)
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    log.info("outbox poller started (interval=%ds)", OUTBOX_POLL_SEC)
    while True:
        try:
            chat_id = _load_chat_id()
            if chat_id is not None:
                for f in sorted(OUTBOX_DIR.glob("*.md")):
                    if f.parent != OUTBOX_DIR:
                        continue
                    text = f.read_text().strip()
                    if not text:
                        f.rename(ARCHIVE_DIR / f.name)
                        continue
                    log.info("posting outbox file %s", f.name)
                    for chunk_start in range(0, len(text), 4000):
                        await app.bot.send_message(
                            chat_id=chat_id,
                            text=text[chunk_start : chunk_start + 4000],
                        )
                    f.rename(ARCHIVE_DIR / f.name)
        except Exception:
            log.exception("outbox poller error")
        await asyncio.sleep(OUTBOX_POLL_SEC)


async def post_init(app: Application) -> None:
    """Schedule the outbox poller as a background task once the bot is up."""
    app.create_task(outbox_poller(app))
    log.info("bot ready (allowed_user=%d, gemini_model=%s)", ALLOWED_USER_ID, GEMINI_MODEL)


# ─── Main ────────────────────────────────────────────────────────────────────


def main() -> None:
    app = (
        Application.builder()
        .token(TELEGRAM_BOT_TOKEN)
        .post_init(post_init)
        .build()
    )
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("status", cmd_status))
    app.add_handler(CommandHandler("reset", cmd_reset))
    app.add_handler(CommandHandler("queue", cmd_queue))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_handler))
    log.info("starting bot (long polling)")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
