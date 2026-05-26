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

## 2026-05-26 — #6 — Shipped OR-78 + OR-85; flagged OR-79 PO-blocked

**Decision:** Closed OR-78 (Ghost admin) and OR-85 (daily ingestion cron) directly in this session, deviating from Decision #4's "defer per-issue execution to autonomous loop" — PO explicitly overrode it ("you stopped from old-cost-discipline habit").

**What shipped:**

- **OR-78 (Ghost admin)** — verified via Admin API JWT auth (Integration key already in `.env`). Admin account exists, title "Otwarte Raporty" set, site responds 200. Marked Done with comment.

- **OR-85 (daily ingestion cron)** — `products/ingestion/run_daily.sh` wrapper + user crontab entry `0 22 * * * ...`. Stops dbr serve to release DuckDB exclusive lock, runs NBP + Eurostat, restarts dashboard via `trap EXIT`. Logs to `data/logs/ingest-daily-YYYY-MM-DD.log`. Test run upserted 39,814 Eurostat observations. Documented at `docs/platform-ops/cron.md`. Marked Done with full implementation comment in Linear.

- **OR-79 (Portal nav link)** — BLOCKED on PO. Ghost's Custom Integration JWT does not have permission to write site settings (returns 501 NotImplementedError on `PUT /ghost/api/admin/settings/`). Settings updates require a logged-in admin browser session. Documented in OR-78's closing comment with 5-min setup steps for the PO.

**Why ship now vs. defer:** PO directive overrides cost-discipline default. Theme 1 work is real value: data freshness foundation (OR-85) unlocks every downstream domain dashboard; OR-78 unblocks Theme 2 (content). Two of three Theme 1 items now closed (OR-90 still PO-blocked on Meta portal).

**Follow-up surfaced (not blocking):**
- DuckDB read-only mode in dbr serve would eliminate the daily 9-minute downtime — file a Linear issue when next touching dbr internals.

**Status:** Shipped. Linear OR-78 + OR-85 = Done. OR-79 + OR-90 = Backlog (PO action).

**Revisit:** Next autonomous Monday (2026-06-01) — pick up Theme 2 (OR-74 blog setup → OR-80 first article) and/or Theme 3 (start OR-56 Labour Market dashboard).

---

## 2026-05-26 — #7 — Shipped OR-80 + OR-74 (first article published); built reusable Ghost pipeline

**Decision:** Drafted, charted, and published OR-80 ("Polska wobec progów SGP i Maastricht: co mówią dane 1995-2024") on https://www.open-reporting.dev/sgp-maastricht-1995-2024/. Built and committed a reusable Markdown→Ghost publisher (`products/blog/publish_to_ghost.py`) so future articles are a one-command shipment.

**Why:** Theme 2 (Activate content channel) — the dashboard is the data, the article is the story. Pairing data-journalism articles with the live dashboard is the core value proposition of Open Reporting.

**What shipped:**
- `data/drafts/or-80-sgp-maastricht.md` — ~888 word Polish draft (via `content-writer` agent, Sonnet). Source-attributed, neutral framing, internal verification block on numbers.
- `products/blog/publish_to_ghost.py` — frontmatter-aware MD→HTML→Ghost publisher. Uploads referenced images, embeds figures at specified headings, posts via Ghost Admin API. CLI for one-command future publishes.
- Live article: 2 embedded charts (debt trend 1995-2024 + EU-27 deficit cross-section 2024 vs 2023), source citations in every section, dedicated Źródła i metodologia closing, ESA 2010 methodology footnote, CTA to portal dashboard.
- Linear OR-80 + OR-74 → Done.

**Pipeline reusable for future articles:** spec → content-writer agent → markdown draft → Playwright clip 2-3 dashboard sections → `publish_to_ghost.py --publish`. Per article: ~30-45K tokens (Sonnet draft + Opus oversight) + ~3 min Playwright capture + 5 sec API publish.

**Surprise:** Ghost blog had 2 pre-existing posts ("Budżety polskich województw", "Budżet państwa") that weren't documented anywhere in the repo. OR-80's "first article" interpretation: first AI-Lead-authored data-journalism piece tied to the dashboards. Doesn't change the ship status.

**Status:** Shipped. Linear OR-80, OR-74 Done. OR-79 (Portal nav) still Backlog/PO-action.

**Revisit:** Add another article every 1-2 weeks as cadence. Topics in the pipeline (worth a Linear capture):
- "Koszty obsługi długu — dlaczego podwoiły się w 4 lata" (deep-dive into the interest-cost story)
- "COFOG — gdzie naprawdę idą wydatki państwa" (paired with wydatki page)
- "Polska na tle UE — deficyt vs dług 2024" (paired with ue page)

---

## 2026-05-26 — #8 — Switched autonomous routine from weekly to daily (week-long unattended mode)

**Decision:** PO directive: "I want you to work for the whole week independently, as I will not have access to this VPS." Changed remote routine `trig_01TqBcSxS3SzQn7BtSTiDmif` from `0 7 * * 1` (Mondays) to `0 6 * * *` (daily 06:00 UTC = 08:00 Warsaw CEST). Hardened prompt for unattended ops.

**Why:** Maximise progress over 7 days of zero PO interaction. Weekly cadence = 1 shot; daily = 7 shots. Sonnet budget should absorb 7 runs comfortably; if a run hits rate limit it exits clean and next day picks up.

**Hardening changes in the prompt:**
- **Step 0: smoke check before any work.** Curl portal + blog; tail yesterday's ingestion log. If broken, P0 fix-or-rollback ahead of new work.
- **Safe-by-default ops:** validate before deploy; preview before publish (article drafts get curl-checked first); branch + PR for big changes (let Codex auto-review); direct-to-main only for single-file YAML/markdown.
- **Auto-rollback** if a deploy makes production return 5xx.
- **Tightened stop conditions:** 90 min/run (was 2h), 10 commits/run (was 20), 6 subagents/run (was 10).
- **Deterministic priority order:** Linear MCP query for Urgent+Infra first, then Theme 3 dashboards in order (OR-56 → OR-52 → OR-55), then Theme 2 articles, then Theme 4 social, then Theme 5 pipeline depth.

**Realistic week-long forecast:**
- Best case (4-5 successful runs): 1-2 new domain dashboards + 3-5 new articles + OR-77 social automation + backlog grooming
- Median case: 1 new dashboard + 2-3 articles + smaller wins
- Worst case: rate limits or production breaks; whatever didn't ship on day N gets one more shot day N+1

**Status:** Active. First daily fire: 2026-05-27T06:00Z (~16h from now).

**Revisit:** When the PO returns — assess what shipped vs forecast, decide whether to keep daily cadence, revert to weekly, or shift model/scope.

---

## 2026-05-26 15:02 UTC — #9 — Cadence correction: every 4 hours + immediate trigger

**Decision:** PO pushback: "why daily? we are at 5pm Today, a lot of time wasted before tomorrow 8am". Two changes:
1. Cron `0 6 * * *` (daily) → `0 */4 * * *` (every 4 hours: 00, 04, 08, 12, 16, 20 UTC) → ~42 runs over the week (was 7)
2. Triggered an immediate manual run (don't wait for the 16:00 UTC cron tick — start NOW)

**Why:** Maximise chances of progress with PO away. Sonnet is the model; Pro quota should absorb 42 runs comfortably. Most runs will be small/incremental — cumulative progress is the goal, not heroic single sessions. If rate limits fire, agent exits clean + next 4h tick picks up.

**Prompt patched to match:**
- "you will fire every 4 hours...~42 runs total"
- "Most runs will be small ones — that's fine; cumulative progress is what matters. Don't try to do everything in one run."
- Added "When there's nothing to do" section — pivot to rubric re-review, backlog grooming, or Wave 3 reference captures rather than burning a run on nothing
- "IMPORTANT: previous runs may have already advanced work — check git log -20 and Linear recently-Done so you don't redo finished work"
- Multi-run dashboard builds use "In Progress" status to signal continuation across runs

**Status:** Active. Manual run triggered at 15:02 UTC; next cron tick 16:00 UTC; then every 4 hours.

**Revisit:** When PO returns — assess total progress, decide whether to keep 4h cadence or scale back.

---

<!-- Append new decisions below -->
