#!/usr/bin/env python3
"""
Open Reporting Telegram bot — generic agent-powered bot.

Each bot instance is configured via env vars:

  BOT_ROLE=claude          →  Uses `claude -p` subprocess
                              Needs: TELEGRAM_BOT_TOKEN, CLAUDE_CHAT_MODEL

  BOT_ROLE=agent           →  Uses `opencode run` with an agent system prompt
                              Needs: TELEGRAM_BOT_TOKEN, AGENT_FILE, OPENCODE_MODEL

  AGENT_FILE               →  Path to .claude/agents/*.md file
                              Bot parses YAML frontmatter, uses the markdown body
                              as the system prompt.

  OTHER_BOT_TOKENS         →  Comma-separated list of other bot tokens for
                              @mention detection (so this bot stays silent when
                              another bot is addressed).

  TELEGRAM_ALLOWED_USER_ID →  Only this user can interact with the bot.

Mention behaviour in a group:
  - No @mention  → this bot replies
  - @other_bot   → this bot stays silent
  - @this_bot    → this bot replies

Security: only TELEGRAM_ALLOWED_USER_ID can interact.
"""
from __future__ import annotations

import asyncio
import logging
import os
import re
import shutil
import yaml
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
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

OPENCODE_BIN = shutil.which("opencode") or "/home/radek/.opencode/bin/opencode"
OPENCODE_TIMEOUT_SEC = 180

VALID_ROLES = ("claude", "gemini", "agent", "opencode")

BOT_ROLE = os.environ["BOT_ROLE"].lower()
if BOT_ROLE not in VALID_ROLES:
    raise SystemExit(f"BOT_ROLE must be one of {VALID_ROLES}, got {BOT_ROLE!r}")

BOT_NAME = os.environ.get("BOT_NAME", BOT_ROLE)


def _token_for(name: str) -> str:
    """Resolve TELEGRAM_<NAME>_BOT_TOKEN (uppercased, dashes→underscores)."""
    var = f"TELEGRAM_{name.upper().replace('-', '_')}_BOT_TOKEN"
    return os.environ.get(var, "").strip()


ALLOWED_USER_ID = int(os.environ["TELEGRAM_ALLOWED_USER_ID"])
BOT_TOKEN = (os.environ.get("TELEGRAM_BOT_TOKEN", "").strip() or _token_for(BOT_NAME))
if not BOT_TOKEN:
    raise SystemExit(
        f"no Telegram token for bot {BOT_NAME!r}: set TELEGRAM_BOT_TOKEN or "
        f"TELEGRAM_{BOT_NAME.upper().replace('-', '_')}_BOT_TOKEN"
    )

# ─── Agent file parser ──────────────────────────────────────────────────────


def _load_agent_prompt(path: Path) -> str:
    """Parse a .claude/agents/*.md file: extract YAML frontmatter + body."""
    raw = path.read_text()
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)", raw, re.DOTALL)
    if not match:
        return raw.strip()
    meta = yaml.safe_load(match.group(1))
    body = match.group(2).strip()
    name = meta.get("name", path.stem)
    desc = meta.get("description", "")
    return f"You are {name}. {desc}\n\n{body}"


# ─── Role-specific config ────────────────────────────────────────────────────

GEMINI_CLIENT = None
GEMINI_MODEL = None

CLAUDE_BIN = shutil.which("claude") or "/home/radek/.local/bin/claude"
CLAUDE_TIMEOUT_SEC = 180

if BOT_ROLE == "claude":
    CLAUDE_CHAT_MODEL = os.environ.get("CLAUDE_CHAT_MODEL", "opus")
    SYSTEM_PROMPT = """You are Claude, the autonomous Project Lead for Open Reporting, in a Telegram group chat with Radek (PO).

You're running as a chat process spawned by the Telegram bot — not the 4×/day autonomous-lead cron run. You have full access to the codebase at /opt/open-reporting, the DuckDB warehouse, the Ghost CMS, and live infrastructure. Use your tools freely to answer with real state, not guesses.

Your role in chat:
- Answer state/code/data/infra questions with actual lookups (read files, run git log, curl URLs, query DuckDB).
- Make project decisions when asked.
- Take action when Radek asks you to — you have bypass permissions and ownership of the project.
- For long-running work (>5 min), suggest `/queue` so it runs in the next scheduled autonomous slot; for quick fixes, just do it.

KEEP REPLIES SHORT. This is Telegram — 1–5 sentences usually. Code blocks only when essential. Polish or English to match Radek."""
elif BOT_ROLE == "gemini":
    from google import genai  # noqa: WPS433

    GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
    GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
    GEMINI_CLIENT = genai.Client(api_key=GEMINI_API_KEY)
    SYSTEM_PROMPT = """You are Gemini, brainstorming partner in the Open Reporting Telegram group with Radek (PO) and Claude (Project Lead).

You don't have VPS access or tools — you're a conversational thinking partner. Use your strengths: ideation, alternative framings, Polish-language nuance, quick research from memory, sanity-checking Claude's reasoning.

KEEP REPLIES SHORT. 1–5 sentences usually. Polish or English to match Radek. If a question needs real codebase / data / infra lookups, suggest tagging @open_reporting_claude_bot."""
elif BOT_ROLE == "agent":
    AGENT_FILE_PATH = Path(os.environ["AGENT_FILE"])
    CLAUDE_CHAT_MODEL = os.environ.get("CLAUDE_CHAT_MODEL", "opus")
    SYSTEM_PROMPT = _load_agent_prompt(AGENT_FILE_PATH)
else:  # opencode — generic coding assistant
    OPENCODE_MODEL = os.environ.get("OPENCODE_MODEL", "opencode/mimo-v2.5-free")
    SYSTEM_PROMPT = """You are an opencode coding assistant in the Open Reporting Telegram group.

Help Radek with quick code questions, snippets, and explanations. You have read access to /opt/open-reporting via opencode tools. Defer big project decisions to @open_reporting_claude_bot.

KEEP REPLIES SHORT. Polish or English to match Radek."""

INBOX_DIR = REPO / "data" / "telegram-inbox"
OUTBOX_DIR = REPO / "data" / "telegram-outbox"
ARCHIVE_DIR = OUTBOX_DIR / "archive"
STATE_FILE = REPO / "data" / f"telegram-bot-{BOT_NAME}.state"
DECISIONS_FILE = REPO / "docs" / "decisions.md"

OUTBOX_POLL_SEC = 30

# ─── Logging ─────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
log = logging.getLogger(f"or-bot-{BOT_NAME}")
logging.getLogger("httpx").setLevel(logging.WARNING)

# ─── Bot identity (used for mention detection) ───────────────────────────────

OWN_USERNAME: str | None = None  # populated in post_init via getMe
OTHER_USERNAMES: list[str] = []  # populated below from other bots' tokens via getMe at boot

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


# ─── Allowlist + mention detection ──────────────────────────────────────────


def _from_allowed_user(update: Update) -> bool:
    user = update.effective_user
    if user is None:
        return False
    if user.id == ALLOWED_USER_ID:
        return True
    if user.is_bot:
        return False
    log.warning(
        "ignoring non-allowlisted user id=%s username=%s",
        user.id,
        user.username,
    )
    return False


def _addressed_to_other_bot(update: Update) -> bool:
    """Return True if the message @-mentions any other bot specifically."""
    if not OTHER_USERNAMES:
        return False
    text = (update.message.text or "") if update.message else ""
    for other in OTHER_USERNAMES:
        if not other:
            continue
        pattern = re.compile(rf"@{re.escape(other)}\b", re.IGNORECASE)
        if pattern.search(text):
            if OWN_USERNAME and re.search(rf"@{re.escape(OWN_USERNAME)}\b", text, re.IGNORECASE):
                return False
            return True
    return False


# ─── Handlers ────────────────────────────────────────────────────────────────


async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    if not _from_allowed_user(update):
        return
    _save_chat_id(update.effective_chat.id)
    await update.message.reply_text(f"{BOT_NAME} connected. Ready to help.")


async def cmd_help(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    if not _from_allowed_user(update):
        return
    if BOT_ROLE == "claude":
        await update.message.reply_text(
            f"{BOT_NAME} — Project Lead. Full VPS access.\n"
            "Commands:\n"
            "  /queue <task>  — defer to next autonomous run (02/07/12/17 UTC)\n"
            "  /status        — last decisions.md entry\n"
            "  /help          — this message\n"
            "\n"
            "Direct mention: `@{OWN_USERNAME} <text>` — only I reply.",
        )
    else:
        await update.message.reply_text(
            f"{BOT_NAME} — Agent. Full VPS access.\n"
            "Commands:\n"
            "  /help  — this message\n"
            "\n"
            "Send me any task and I'll execute it.",
        )


async def cmd_status(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    if not _from_allowed_user(update):
        return
    if not DECISIONS_FILE.exists():
        await update.message.reply_text("No decisions.md found.")
        return
    text = DECISIONS_FILE.read_text()
    entries = re.split(r"^## ", text, flags=re.MULTILINE)
    if len(entries) < 2:
        await update.message.reply_text("decisions.md is empty.")
        return
    latest = "## " + entries[1].strip()
    if len(latest) > 3800:
        latest = latest[:3800] + "\n…(truncated)"
    await update.message.reply_text(latest)


async def cmd_queue(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    if not _from_allowed_user(update):
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
        f"Next slot: 02/07/12/17 UTC. /status when done.",
    )


# ─── Text message handler ───────────────────────────────────────────────────


async def text_handler(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    eu = update.effective_user
    log.info(
        "received text chat_id=%s user_id=%s username=%s is_bot=%s text=%r",
        update.effective_chat.id if update.effective_chat else None,
        (eu.id if eu else None),
        (eu.username if eu else None),
        (eu.is_bot if eu else None),
        ((update.message.text or "") if update.message else "")[:80],
    )
    if not _from_allowed_user(update):
        log.info("dropped — not from allowed user (allowed=%s got=%s)", ALLOWED_USER_ID, eu.id if eu else None)
        return
    if _addressed_to_other_bot(update):
        log.info("skipping — addressed to other bot")
        return

    log.info("processing message (bot=%s role=%s)", BOT_NAME, BOT_ROLE)
    _save_chat_id(update.effective_chat.id)
    text = update.message.text or ""

    # Strip my own @mention so the model doesn't see it.
    if OWN_USERNAME:
        text = re.sub(rf"@{re.escape(OWN_USERNAME)}\b", "", text, flags=re.IGNORECASE).strip()

    try:
        await update.message.chat.send_action(ChatAction.TYPING)
    except Exception:
        log.exception("send_action failed (continuing)")

    try:
        if BOT_ROLE in ("claude", "agent"):
            log.info("invoking claude -p (model=%s)", CLAUDE_CHAT_MODEL)
            reply = await _claude_reply(text)
        elif BOT_ROLE == "gemini":
            log.info("invoking gemini")
            reply = await _gemini_reply(text)
        else:
            log.info("invoking opencode run (agent=%s)", BOT_NAME)
            reply = await _opencode_reply(text)
        log.info("reply length=%d", len(reply))
    except Exception as e:
        log.exception("reply error")
        reply = f"⚠️ {BOT_NAME} crashed: {type(e).__name__}: {str(e)[:300]}"

    try:
        for chunk_start in range(0, len(reply), 4000):
            await update.message.reply_text(reply[chunk_start : chunk_start + 4000])
        log.info("reply sent to chat")
    except Exception:
        log.exception("reply_text failed")


async def _claude_reply(text: str) -> str:
    full_prompt = f"{SYSTEM_PROMPT}\n\n---\nRadek (Telegram): {text}\n"
    claude_env = {
        "HOME": "/home/radek",
        "PATH": "/home/radek/.local/bin:/usr/local/bin:/usr/bin:/bin",
        "USER": "radek",
        "LANG": os.environ.get("LANG", "C.UTF-8"),
    }
    proc = None
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
            env=claude_env,
        )
        stdout, stderr = await asyncio.wait_for(
            proc.communicate(full_prompt.encode()),
            timeout=CLAUDE_TIMEOUT_SEC,
        )
        if proc.returncode != 0:
            err = stderr.decode("utf-8", errors="replace")[:500]
            return f"⚠️ Claude exited {proc.returncode}: {err}"
        return stdout.decode("utf-8", errors="replace").strip() or "(empty response)"
    except asyncio.TimeoutError:
        if proc:
            try:
                proc.kill()
            except Exception:
                pass
        return f"⚠️ Claude timed out after {CLAUDE_TIMEOUT_SEC}s"
    except Exception as e:
        log.exception("claude subprocess error")
        return f"⚠️ Claude error: {type(e).__name__}: {str(e)[:300]}"


async def _gemini_reply(text: str) -> str:
    if GEMINI_CLIENT is None:
        return "⚠️ Gemini client not initialized"
    try:
        response = await asyncio.to_thread(
            GEMINI_CLIENT.models.generate_content,
            model=GEMINI_MODEL,
            contents=text,
            config={"system_instruction": SYSTEM_PROMPT},
        )
        return (response.text or "").strip() or "(empty response)"
    except Exception as e:
        log.exception("gemini error")
        return f"⚠️ Gemini error: {type(e).__name__}: {str(e)[:300]}"


async def _opencode_reply(text: str) -> str:
    full_prompt = f"{SYSTEM_PROMPT}\n\n---\nRadek (Telegram): {text}\n"
    opencode_env = {
        "HOME": "/home/radek",
        "PATH": "/home/radek/.opencode/bin:/home/radek/.local/bin:/usr/local/bin:/usr/bin:/bin",
        "USER": "radek",
        "LANG": os.environ.get("LANG", "C.UTF-8"),
    }
    proc = None
    try:
        proc = await asyncio.create_subprocess_exec(
            OPENCODE_BIN,
            "run",
            "--model", OPENCODE_MODEL,
            full_prompt,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(REPO),
            env=opencode_env,
        )
        stdout, stderr = await asyncio.wait_for(
            proc.communicate(),
            timeout=OPENCODE_TIMEOUT_SEC,
        )
        if proc.returncode != 0:
            err = stderr.decode("utf-8", errors="replace")[:500]
            return f"⚠️ OpenCode exited {proc.returncode}: {err}"
        return stdout.decode("utf-8", errors="replace").strip() or "(empty response)"
    except asyncio.TimeoutError:
        if proc:
            try:
                proc.kill()
            except Exception:
                pass
        return f"⚠️ OpenCode timed out after {OPENCODE_TIMEOUT_SEC}s"
    except Exception as e:
        log.exception("opencode subprocess error")
        return f"⚠️ OpenCode error: {type(e).__name__}: {str(e)[:300]}"


# ─── Outbox poller (Claude bot only) ────────────────────────────────────────


async def outbox_poller(app: Application) -> None:
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


# ─── post_init: discover own + other bot usernames, start outbox if claude ──


async def post_init(app: Application) -> None:
    global OWN_USERNAME, OTHER_USERNAMES
    me = await app.bot.get_me()
    OWN_USERNAME = me.username
    log.info("own identity: @%s (id=%d)", OWN_USERNAME, me.id)

    # Discover other bot usernames from OTHER_BOT_TOKENS env var (comma-separated).
    import httpx

    other_tokens_str = os.environ.get("OTHER_BOT_TOKENS", "")
    other_tokens = [t.strip() for t in other_tokens_str.split(",") if t.strip()]

    other_names_str = os.environ.get("OTHER_BOT_NAMES", "")
    for n in (x.strip() for x in other_names_str.split(",") if x.strip()):
        t = _token_for(n)
        if t:
            other_tokens.append(t)
        else:
            log.warning("OTHER_BOT_NAMES: no token for %r — skipping", n)

    # De-dup and drop our own token (paranoia)
    other_tokens = list({t for t in other_tokens if t and t != BOT_TOKEN})

    other_usernames = []
    for token in other_tokens:
        try:
            async with httpx.AsyncClient(timeout=10) as cl:
                r = await cl.get(f"https://api.telegram.org/bot{token}/getMe")
                other_usernames.append(r.json()["result"]["username"])
        except Exception:
            log.exception("could not fetch bot identity for token")

    if other_usernames:
        OTHER_USERNAMES.extend(other_usernames)
        log.info("other bots: %s", other_usernames)

    if BOT_ROLE == "claude":
        app.create_task(outbox_poller(app))


# ─── Main ────────────────────────────────────────────────────────────────────


def main() -> None:
    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .post_init(post_init)
        .build()
    )
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))

    if BOT_ROLE == "claude":
        app.add_handler(CommandHandler("status", cmd_status))
        app.add_handler(CommandHandler("queue", cmd_queue))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    log.info("starting bot name=%s role=%s (long polling)", BOT_NAME, BOT_ROLE)
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
