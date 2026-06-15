# Open Reporting — Shared Agent Contract

The single source of truth for **both** AI collaborators on this repo:
**Claude Code** (reads `CLAUDE.md`) and **Gemini / Antigravity** (reads `AGENTS.md`).
Both tool-specific files point here for the shared rules. When they conflict, **this file wins.**

PO (owner) = **Radek**. Two AIs work this repo together; neither acts alone on a non-trivial
task without discussing it first (see Collaboration Protocol below).

## Hard Floors — never, by either AI

- Force-push to `main`.
- Delete `data/warehouse.duckdb`, `data/telegram-inbox/`, `data/telegram-outbox/`, or any DB content.
- Disable the daily ingestion cron, the autonomous-lead cron, or the Telegram/Discord bots.
- Spend money or add recurring cost without PO approval — flag it instead.
- Provision credentials in 3rd-party portals (Meta, BDL API, Ghost admin, OAuth) — PO action only.
- Rewrite this file, `CLAUDE.md`, `AGENTS.md`, or the project charter without flagging the change to the PO.

## Git Discipline (prevents the two AIs clobbering each other)

- Each AI commits **only its own files, with explicit paths**. **Never `git add -A`** — the working
  tree routinely holds the *other* AI's uncommitted work. Treat unknown untracked files as not yours.
- Do non-trivial work on a branch; never overwrite the other's uncommitted changes.
- One logical change per commit. Convention: `feat:`/`fix:`/`refactor:`/`docs:`/`chore:`.

## Collaboration Protocol — discuss each task before acting

The PO wants the two AIs to **talk through every non-trivial task** before doing it. The channel is
a shared thread file — not live chat, not message relaying.

1. **One thread per task/decision:** `docs/collab/<YYYY-MM-DD>-<slug>.md`.
2. **Before acting** on anything beyond a trivial edit, open or continue the thread.
3. **Turn format** — append a signed, timestamped entry; never edit the other AI's entries:
   ```
   ### [Claude] 2026-06-15T17:20Z
   <your message — concise>
   ```
   (Gemini signs `### [Gemini] …`.)
4. **Read the whole thread first.** Add exactly one entry per turn. End every entry with one of:
   a **question**, a **proposal**, or `AGREED: <one-line decision>`.
5. **Settle:** when both AIs have written `AGREED:` matching the same decision, the thread is closed.
   Whoever owns the work records the outcome in `docs/decisions.md` and proceeds.
6. **Turn-taking is PO-driven:** the PO nudges each side (*"your turn on docs/collab/X.md"*). No AI
   waits/polls; you respond when nudged, having re-read the thread.
7. Keep entries short. Disagreement is fine — surface it; don't rubber-stamp.

## Language Rules

- **Code, config, DB, filenames, logs, commits, reviews:** English, always, no exceptions.
- **User-facing content** (chart/axis labels, portal copy, tooltips): formal Polish, proper diacritics.

## Where the detail lives

This file is the lean shared contract. The full domain/architecture/process detail is in `docs/`
(`ARCHITECTURE.md`, the topic folders, `process/`). Both AIs read the same `docs/` — no tool-specific
knowledge base.
