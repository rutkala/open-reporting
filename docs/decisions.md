# Decisions Log

Append-only record of every non-trivial strategic call by the AI Lead. Latest at the bottom; PO can override by editing the relevant entry with `// PO:` prefix or by editing `docs/roadmap.md`.

Format per entry:
- **Date** + **#N**
- **Decision** — what I'm doing (one sentence)
- **Why** — the reasoning (2-3 sentences)
- **Status** — Shipped / Queued / Blocked
- **Revisit** — when to reconsider

---

## 2026-05-26 — #1 — Took over leadership

**Decision:** AI Lead operating model activated. Strategic direction, editorial picks, prioritisation, and execution are autonomous within the cost ceiling. PO override channels documented in `docs/process/lead-protocol.md`.

**Why:** PO asked for it ("you will not ask me any question, you will always follow your recommendations"). Cost is the only hard boundary. The infrastructure (Phase B/C/D loop, rubric, orchestration) is sufficient for autonomous operation.

**Status:** Active.

**Revisit:** PO can revoke at any time by editing this entry or `lead-protocol.md`.

---

## 2026-05-26 — #2 — Strategic roadmap for next 4-6 weeks

**Decision:** Five themes prioritised in `docs/roadmap.md`:
1. Stabilise basics (OR-90 token, OR-78 Ghost admin, OR-85 daily cron)
2. Activate content channel (OR-74 blog, OR-80 first article, OR-79 portal link)
3. Replicate to 3 more domains (OR-56 Labour, OR-52 Macro, OR-55 Demographics)
4. Automate social drumbeat (OR-77, OR-89)
5. Data pipeline depth (OR-76, OR-86)

**Why:** Factory is over-engineered for one product. Next phase is using the factory at its capable rate. The 3 new domains chosen are the most-asked Polish public topics where Polish-language framing is differentiating. Polishing public_finance from 71% to 85% rubric is lower-leverage than 3 new dashboards at 70%.

**Deferred and why:** Other 14 enumerated dashboards (lack of usage signal); finance polish improvements (diminishing returns); mobile (no desktop signal yet); meta-architecture items (premature).

**Status:** Roadmap published. Theme 1 starts immediately.

**Revisit:** End of week 2 (after Themes 1-2 land) — adjust based on actual capacity + any reader signal.

---

## 2026-05-26 — #3 — OR-90 Instagram token: blocked on PO

**Decision:** Flag OR-90 as `[BLOCKED: needs PO action]`. The Instagram access token expired 2026-05-20 (six days ago); publishing has been silently stopped. Refresh requires Meta Developer portal access to the @otwarteraporty profile — that's a personal account I cannot access.

**Why:** Can't refresh a token in someone else's Meta account. This is the single critical blocker for Theme 4 (social automation).

**Status:** Blocked. PO action required.

**Required PO action (one-time):**
1. Log into Meta Developer portal as @otwarteraporty admin
2. Generate a new long-lived Instagram Graph API access token
3. Replace the value in `.env` (or wherever secrets live) — variable `INSTAGRAM_ACCESS_TOKEN` (verify exact name in the codebase)
4. Add a Linear comment on OR-90 confirming done
5. I'll pick up + verify + close OR-90 in the next autonomous session

**Revisit:** When OR-90 comment confirms token refresh.

---

## 2026-05-26 — #4 — Cost discipline: deferred per-issue execution

**Decision:** This session writes the operating contract + roadmap + decisions log + sets up `/schedule` cadence. It does NOT execute Theme 1 issues (OR-78, OR-85). Those go to the first autonomous Monday session.

**Why:** This session has already consumed ~30K Opus tokens on the protocol + roadmap. Adding `/kickoff` runs now would exceed the 15% weekly soft cap. Better to ship the contract clean and let the autonomous cadence pick up execution Monday.

**Status:** Active queue.

**Revisit:** Monday 2026-06-01 09:00 Europe/Warsaw via scheduled agent.

---

## 2026-05-26 — #5 — Scheduled autonomous lead loop (Mondays 09:07 Warsaw)

**Decision:** Created remote routine `trig_01TqBcSxS3SzQn7BtSTiDmif` ("Open Reporting — Autonomous Lead Loop") running Mondays at 07:07 UTC (= 09:07 Europe/Warsaw, CEST). Model: `claude-sonnet-4-6`. MCP: Linear (attached), Gmail (attached). First run: 2026-06-01.

**Why:** PO delegated leadership; weekly cadence is the agreed rhythm. Sonnet (not Opus) because the strategic thinking is already encoded in `docs/roadmap.md` (which Opus wrote this session) — the autonomous loop just executes the order. Keeps Opus budget free for conversational sessions with the PO.

**Behaviour per run:** read protocol + roadmap + decisions + session-memory → pick highest-priority unblocked item from Themes 1-5 → execute via builder agents → ship → update Linear status to Done → append decisions.md entry → rewrite session-memory.md → commit + push.

**Hard limits per run:** stop after 2 hours, 20 commits, 10 subagents, or any rate limit. No money spent. No CLAUDE.md / AGENTS.md / PROJECT.md changes without `[STRATEGIC SHIFT]` flag for PO review.

**Status:** Active. View at https://claude.ai/code/routines/trig_01TqBcSxS3SzQn7BtSTiDmif

**Revisit:** After 2-3 weekly runs — assess Sonnet's strategic execution quality, upgrade to Opus if needed.

---

<!-- Append new decisions below -->
