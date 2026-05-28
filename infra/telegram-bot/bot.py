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
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-pro")

INBOX_DIR = REPO / "data" / "telegram-inbox"
OUTBOX_DIR = REPO / "data" / "telegram-outbox"
ARCHIVE_DIR = REPO / "data" / "telegram-outbox" / "archive"
STATE_FILE = REPO / "data" / "telegram-bot.state"
DECISIONS_FILE = REPO / "docs" / "decisions.md"

OUTBOX_POLL_SEC = 30

GEMINI_SYSTEM_PROMPT = """You are Gemini, working in a Telegram chat with Radek, the Product Owner of Open Reporting — a one-person data media company turning Polish public data into accessible, beautiful, useful products.

Your role: brainstorming partner for ideas, feedback, content drafts. You also have access (via Radek) to the live products at portal.open-reporting.dev (dashboards) and www.open-reporting.dev (blog).

The other half of this project is Claude, who runs as the autonomous Project Lead on the production VPS. Claude builds everything: dashboards (Dash + dbt + DuckDB), articles in Polish (Ghost CMS), data ingestion (Eurostat, NBP, BDL/GUS), infra. Claude fires 4×/day on a cron and reads its inbox at data/telegram-inbox/ each run.

When Radek wants Claude to actually DO something (build, deploy, ship), he will use `/queue <task>` — that message goes straight to Claude's next autonomous run, bypassing you. You don't execute project work. You help Radek think, draft, refine.

Default language: Polish for content (articles, KPIs, UI strings). English for technical discussion. Match Radek's language in the moment.

Be concise. Treat ADHD-friendly responses as the default — short, punchy, scannable. Long-form only when explicitly asked."""

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
    return update.effective_user is not None and update.effective_user.id == ALLOWED_USER_ID


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
        "  /queue <task>  — send to Claude's next autonomous run (4×/day at 02/07/12/17 UTC)\n"
        "  /status        — last decisions.md entry (most recent autonomous run)\n"
        "  /reset         — reset Gemini conversation context\n"
        "  /help          — this message\n"
        "\n"
        "Anything else = Gemini conversation. Claude responses arrive automatically when an autonomous run finishes.",
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


async def gemini_chat(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    if not _allowed(update):
        return
    _save_chat_id(update.effective_chat.id)
    user_id = update.effective_user.id
    text = update.message.text or ""

    chat = chat_sessions.get(user_id)
    if chat is None:
        chat = _new_chat()
        chat_sessions[user_id] = chat

    await update.message.chat.send_action(ChatAction.TYPING)
    try:
        resp = await asyncio.to_thread(chat.send_message, text)
        reply = (resp.text or "").strip() or "(empty response)"
    except Exception as e:
        log.exception("gemini error")
        reply = f"Gemini error: {type(e).__name__}: {e}"
        # Drop the broken session so the next message starts fresh.
        chat_sessions.pop(user_id, None)

    # Telegram caps at 4096 chars; split if needed.
    for chunk_start in range(0, len(reply), 4000):
        await update.message.reply_text(reply[chunk_start : chunk_start + 4000])


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
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, gemini_chat))
    log.info("starting bot (long polling)")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
