#!/usr/bin/env python3
"""
Open Reporting Discord bot — minimal test build.

Single-bot scaffold to verify Discord connectivity, message handling, and the
brain pattern (claude -p) before scaling up to the full agent fleet.

Env vars:
  BOT_NAME              — short name, e.g. "claude" / "scrum-master"
                          (token resolved as DISCORD_<NAME>_BOT_TOKEN)
  BOT_ROLE              — claude | gemini | agent (default: claude)
  AGENT_FILE            — for BOT_ROLE=agent, path to .claude/agents/*.md
  CLAUDE_CHAT_MODEL     — opus | sonnet (default: opus)
  DISCORD_ALLOWED_USER  — optional Discord user ID; if set, only that user is replied to

Behaviour:
  - In a server, replies only when @-mentioned or in a DM
  - Sends a typing indicator while thinking
  - Brain = claude -p subprocess (subscription, free, no metered cost)
  - Replies chunked at 2000 chars (Discord limit)
"""
from __future__ import annotations

import asyncio
import logging
import os
import re
import shutil
from pathlib import Path

import yaml
from dotenv import load_dotenv

import discord
from discord import Intents

# ─── Config ──────────────────────────────────────────────────────────────────

REPO = Path("/opt/open-reporting")
load_dotenv(REPO / ".env", override=True)

BOT_ROLE = os.environ.get("BOT_ROLE", "claude").lower()
BOT_NAME = os.environ.get("BOT_NAME", BOT_ROLE)


def _token_for(name: str) -> str:
    var = f"DISCORD_BOT_{name.upper().replace('-', '_')}_TOKEN"
    return os.environ.get(var, "").strip()


BOT_TOKEN = (os.environ.get("DISCORD_BOT_TOKEN", "").strip() or _token_for(BOT_NAME))
if not BOT_TOKEN:
    raise SystemExit(
        f"no Discord token for bot {BOT_NAME!r}: set DISCORD_BOT_TOKEN or "
        f"DISCORD_{BOT_NAME.upper().replace('-', '_')}_BOT_TOKEN"
    )

ALLOWED_USER_ID = int(os.environ["DISCORD_ALLOWED_USER"]) if os.environ.get("DISCORD_ALLOWED_USER") else None

CLAUDE_BIN = shutil.which("claude") or "/home/radek/.local/bin/claude"
CLAUDE_TIMEOUT_SEC = 180

# ─── Agent file parser ──────────────────────────────────────────────────────


def _load_agent_prompt(path: Path) -> str:
    raw = path.read_text()
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)", raw, re.DOTALL)
    if not match:
        return raw.strip()
    meta = yaml.safe_load(match.group(1))
    body = match.group(2).strip()
    name = meta.get("name", path.stem)
    desc = meta.get("description", "")
    return f"You are {name}. {desc}\n\n{body}"


# ─── Role config ────────────────────────────────────────────────────────────

if BOT_ROLE == "claude":
    CLAUDE_CHAT_MODEL = os.environ.get("CLAUDE_CHAT_MODEL", "opus")
    SYSTEM_PROMPT = """You are Claude, the autonomous Project Lead for Open Reporting, in the project's Discord server with Radek (PO) and your agent team.

You have full access to the codebase at /opt/open-reporting, the DuckDB warehouse, the Ghost CMS, and live infrastructure. Use your tools freely.

KEEP REPLIES SHORT (Discord 2000-char limit per message). Polish or English to match Radek. Use Discord-flavored markdown when helpful."""
elif BOT_ROLE == "agent":
    AGENT_FILE_PATH = Path(os.environ["AGENT_FILE"])
    CLAUDE_CHAT_MODEL = os.environ.get("CLAUDE_CHAT_MODEL", "opus")
    SYSTEM_PROMPT = _load_agent_prompt(AGENT_FILE_PATH)
else:
    raise SystemExit(f"unsupported BOT_ROLE {BOT_ROLE!r} (claude|agent)")

# ─── Logging ────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
log = logging.getLogger(f"or-discord-{BOT_NAME}")
logging.getLogger("discord").setLevel(logging.WARNING)
logging.getLogger("discord.http").setLevel(logging.WARNING)

# ─── Brain ──────────────────────────────────────────────────────────────────


async def _claude_reply(text: str) -> str:
    full_prompt = f"{SYSTEM_PROMPT}\n\n---\nRadek (Discord): {text}\n"
    env = {
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
            env=env,
        )
        stdout, stderr = await asyncio.wait_for(
            proc.communicate(full_prompt.encode()),
            timeout=CLAUDE_TIMEOUT_SEC,
        )
        if proc.returncode != 0:
            err = stderr.decode("utf-8", errors="replace")[:500]
            return f":warning: Claude exited {proc.returncode}: {err}"
        return stdout.decode("utf-8", errors="replace").strip() or "(empty response)"
    except asyncio.TimeoutError:
        if proc:
            try:
                proc.kill()
            except Exception:
                pass
        return f":warning: Claude timed out after {CLAUDE_TIMEOUT_SEC}s"
    except Exception as e:
        log.exception("claude subprocess error")
        return f":warning: Claude error: {type(e).__name__}: {str(e)[:300]}"


# ─── Discord client ─────────────────────────────────────────────────────────


intents = Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


def _is_addressed(message: discord.Message) -> bool:
    """Reply only when @-mentioned, replied-to, or in a DM."""
    if message.guild is None:
        return True  # DM
    if client.user in message.mentions:
        return True
    if message.reference and message.reference.resolved:
        ref = message.reference.resolved
        if isinstance(ref, discord.Message) and ref.author.id == client.user.id:
            return True
    return False


def _strip_mention(text: str) -> str:
    if client.user:
        return re.sub(rf"<@!?{client.user.id}>", "", text).strip()
    return text


@client.event
async def on_ready():
    log.info("logged in as %s (id=%s)", client.user, client.user.id if client.user else "?")
    log.info("guilds: %s", [g.name for g in client.guilds])
    log.info("model=%s role=%s", CLAUDE_CHAT_MODEL, BOT_ROLE)


@client.event
async def on_message(message: discord.Message):
    if message.author.id == client.user.id:
        return
    if message.author.bot:
        return  # ignore other bots for now (loop prevention; expand later)
    if ALLOWED_USER_ID and message.author.id != ALLOWED_USER_ID and message.guild is not None:
        return
    if not _is_addressed(message):
        return

    prompt = _strip_mention(message.content or "")
    if not prompt:
        return

    log.info("processing message from %s in %s: %r", message.author, message.channel, prompt[:80])

    async with message.channel.typing():
        reply = await _claude_reply(prompt)

    log.info("reply length=%d", len(reply))
    for i in range(0, len(reply), 2000):
        chunk = reply[i:i + 2000]
        await message.channel.send(chunk, reference=message if i == 0 else None, mention_author=False)
    log.info("reply sent (%d chunks)", (len(reply) + 1999) // 2000)


# ─── Main ───────────────────────────────────────────────────────────────────


def main() -> None:
    log.info("starting Discord bot name=%s role=%s", BOT_NAME, BOT_ROLE)
    client.run(BOT_TOKEN, log_handler=None)


if __name__ == "__main__":
    main()
