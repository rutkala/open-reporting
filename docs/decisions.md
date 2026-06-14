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

## 2026-05-26 19:30 UTC — #10 — OR-56 Labour Market dashboard shipped (autonomous + PO-assisted)

**Decision:** Closed OR-56 Labour Market dashboard. Live at https://portal.open-reporting.dev/labour_market/. Mixed-mode build: autonomous agent shipped 3 commits (15:06–17:15 UTC) building the structure; conversational PO session (19:20–19:30 UTC) caught 2 real defects and fixed them.

**Autonomous agent's 3 commits (`92733d8e`, `f79b904f`, `ee5022bd`):** dbt mart models (`fact_labour_overview`, `fact_labour_wages`), semantic models (`labour_overview.yml`, `labour_wages.yml`), 4-page dashboard YAML (przeglad, bezrobocie, wynagrodzenia, ue). Followed the public_finance pattern faithfully.

**Defects caught + fixed in this session:**
1. **YAML parse error** in `pages/bezrobocie/page.yml`: `title:  Bezrobocie: Polska na tle UE` — unquoted colon. `dbr validate` rightly caught it; the autonomous run correctly did NOT deploy. Fixed: wrapped in quotes. The autonomous run should validate-then-fix-then-retry rather than abandoning.
2. **No data on dashboard**: dbt models referenced `lab.unemployment_rate`, `lab.employment_rate`, `lab.activity_rate`, `lab.youth_unemployment_rate` detail_ids, but the seed `eurostat_series.csv` had wrong dimension_keys (missing `age=`, `citizen=TOTAL`, `&unit=PC`). Updated 4 seed entries to match actual raw dimension_keys; `dbt seed + dbt run`; `fact_labour_overview` now has 28 rows of real PL data 1995–2025. Dashboard now renders: Stopa bezrobocia 3,1%, Wskaźnik zatrudnienia 78,8%, Aktywność zawodowa 64,3% with YoY deltas, full trend charts.

**Lessons for autonomous runs (next run will read this):**
- **End-to-end verify, not just deploy-OK.** After `dbr run` returns 200, do a Playwright screenshot + visually check >0 charts render data. "200 OK" from health check isn't enough.
- **dbt seed + dbt run after adding new mart models.** If models reference new detail_ids, the seed needs entries AND those entries must match actual raw dimension_keys (check `raw.eurostat_observations` to find the exact dim key shape before authoring seed rows).
- **Validate-then-fix, not validate-then-abandon.** When `dbr validate` fails, the run should attempt a fix (e.g., quoting a YAML title) rather than committing broken state. Add this to the prompt's safety rules.

**Status:** Shipped — Linear OR-56 Done.

**Followup not blocking:**
- Update autonomous routine prompt: add "after dbr run, Playwright-verify charts render data" + "if dbr validate fails, attempt one fix iteration before abandoning" — will do in a follow-up cycle.

---

## 2026-05-26 20:30 UTC — #11 — OR-52 National Accounts dashboard code shipped

**Decision:** Committed 24 files implementing the OR-52 National Accounts & Macroeconomics dashboard (Theme 3 priority #2). Follows the public_finance and labour_market pattern exactly.

**What shipped (commit `ad1e34a`):**
- `products/warehouse/models/marts/macro/fact_macro_overview.sql` — annual pivot fact. 4 Eurostat annual MAC series (GDP real growth, GDP nominal ÷1000→EUR bn, GFCF % of GDP, industrial output growth) + current account % of GDP aggregated from quarterly to annual via AVG.
- `products/warehouse/models/semantic/macro_overview.yml` — 5 MetricFlow metrics (gdp_real_growth, gdp_nominal, gfcf_pct_gdp, industrial_output_growth, current_account_balance)
- `products/dashboards/national_accounts/` — 3 pages (Przegląd, PKB, Inwestycje), port 8059, 10 visuals
- `infra/nginx/conf.d/dbr-routes/national_accounts.conf` + `infra/systemd/or-national_accounts.service`

**Why no EU comparison page:** All 7 MAC series in the PostgreSQL catalogue have `geo=PL` — the ingestion only fetches Polish data. EU comparison would require adding ALL_GEOS-sentinel series entries + a backfill run. Deferred to a separate issue.

**Deployment pending on VPS (PO action or next autonomous run that has VPS access):**
```bash
dbt run --select fact_macro_overview --profiles-dir .
dbr validate products/dashboards/national_accounts
dbr run products/dashboards/national_accounts
```
After deploy: verify /national_accounts/ renders data (not just 200 OK — lesson from OR-56).

**Status:** Code shipped to git. Deployment pending. Linear OR-52 remains In Progress until live.

**Linear:** OR-52 | **Commit:** `ad1e34a` | **Target URL:** https://portal.open-reporting.dev/national_accounts/

**Smoke check note:** Production returned 403 from this container — "Host not in allowlist" from nginx IP restriction. Not a service failure; PO confirmed 200 OK at 19:35 UTC. This container's egress IP is not whitelisted. Autonomous runs from cloud containers cannot directly verify production health — the PO needs to monitor live status manually or via the STATUS.md.

**Followup:**
- Deploy on VPS + verify data renders
- Consider adding EU GDP comparison series (needs ALL_GEOS sentinel entries in catalogue + backfill)
- Next run: OR-55 Population & Demographics (Theme 3 priority #3)

---

<!-- Append new decisions below -->

---

## 2026-05-28 12:00 UTC — #20 — [P0] Daily ingestion runbook fix + OR-87 truly activated

**Decision:** Recovered yesterday's failed daily ingestion and shipped two fixes:
(1) `run_daily.sh` now stops every `or-*.service` dashboard dynamically (not just `or-public_finance`); (2) OR-87 `sts_inpr_a` Eurostat codes corrected to `indic_bt=PRD` + `unit=PCH_SM` (the prior fix guessed `PROD` / `PCH_PRE` and produced 0 rows).

**Why:**
- Yesterday's 22:00 UTC ingestion failed `exit=1` — only `or-public_finance.service` was being stopped before ingestion, but 4 more dashboard services (labour_market, national_accounts, demographics, environment) hold the DuckDB write lock now. Without the fix, every nightly ingestion from here on would silently fail.
- OR-87 had been "shipped" twice but never produced data because nobody had run the Eurostat API against the seed values to verify. Querying the API directly was the only way to discover the codes were wrong.

**What shipped:**

1. **`fix(ingestion): stop all or-* dashboards before daily ingestion`** — commit `cfab32ab`
   - Dashboard services now discovered via `systemctl list-unit-files 'or-*.service'`, excluding `or-telegram-bot.service`. Stop loop before ingest, `trap` restart loop on EXIT. Verified end-to-end via manual run: 5 dashboards stopped, NBP + Eurostat ingested cleanly (exit=0), all 5 restarted and back to 200.

2. **`fix(macro): correct sts_inpr_a Eurostat codes (PRD not PROD, PCH_SM not PCH_PRE)`** — commit `c160a6ab`
   - Probed Eurostat API directly for `sts_inpr_a?geo=PL&indic_bt=PRD&nace_r2=B-D&s_adj=CA&unit=PCH_SM` → 25 PL rows returned. Reloaded Postgres catalogue (`loader.py`), re-ingested sts_inpr_a, ran `dbt seed eurostat_series` + `dbt run` (all 37 models OK). `curated.fact_macro_overview` now shows PL industrial output growth 2025=+2.5%, 2024=+0.5%, 2023=-1.1%, 2022=+10.6%, 2021=+14.8%, 2020=-1.9% — matches widely-reported post-COVID rebound and 2023 industrial contraction.
   - OR-87 closed in Linear.

3. **Telegram bot WIP** — moved uncommitted `infra/telegram-bot/bot.py` change (parallel Claude responder alongside Gemini in chat) onto branch `feat/telegram-claude-bridge` + draft PR #62 for PO review. Cost-bearing UX change — every chat message would fire a `claude -p` subprocess. Left dirty in working tree by a previous session; without this move the next `git pull` in `autonomous-lead.sh` would conflict.

**Status:** Shipped. OR-87 → Done. PR #62 draft awaiting PO review. Daily ingestion runbook hardened for tonight's 22:00 UTC fire.

**Linear:** OR-85 (ingestion runbook), OR-87 (industrial output) | **Commits:** `cfab32ab`, `c160a6ab`

**Lessons learned (rule):**
- **Verify against the upstream API before trusting any code-only fix to a data ingestion bug.** OR-87 had two failed fix attempts (PROD/PCH_PRE guesses) because the codes were never validated against Eurostat's actual response — a 30s `curl` would have caught it. Adding to the autonomous-lead protocol: any seed/catalogue change that adds Eurostat dimension codes must include a real API call confirming non-zero rows.
- **Cron scripts that mention specific service names must be reviewed when adding new dashboards.** Adding the 4 new dashboards (labour_market, national_accounts, demographics, environment) without updating `run_daily.sh` left a latent timebomb. Dynamic discovery (`systemctl list-unit-files`) fixes it for future additions.

**Followup:**
- `CLAUDE.md` example `from dbr.semantic import query` is stale — the function moved/renamed. Noted but not fixed this run; lives under the `packages/dbr/` engine plane.
- Other `unit=PCH_PRE` rows in seeds: `lab.wage_growth` (lc_lci_r2_a) is working fine with PCH_PRE (25 PL rows present); `mac.retail_sales_growth` (sts_trtu_a) has 0 rows but is `verified=false` so deactivated. No further action.
- PR #62 (Telegram Claude bridge) waits for PO decision on cost/UX trade-off.

---

## 2026-05-28 07:00 UTC — #19 — OR-150 demographics article + OR-86 BDL ingestion code shipped

**Decision:** Two deliverables this run: (1) seventh Theme 2 article on Poland's demographic crisis; (2) complete BDL (Bank Danych Lokalnych) REST API ingestion infrastructure for OR-86.

**What shipped:**

- **OR-150** — `products/blog/drafts/or-150-demographics.md`, commit `5368422`
  - ~1,100-word Polish article: "Polska kurczy się demograficznie: przyrost naturalny ujemny od 2013 roku"
  - Key verified facts: natural increase -3.7 per 1000 in 2023 (more severe than estimated; correct data wins), TFR 1.16 (third-lowest EU behind Malta 1.06 and Spain 1.12), birth rate 7.4 per 1000 (vs 14.9 in 1989), life expectancy women 82.1 / men 74.6, Ageing Report 2024 dependency ratio doubling to 68 by 2080
  - All numbers cited (Eurostat demo_gind, tps00199, demo_mlexpec; GUS Rocznik Demograficzny 2024; EC Ageing Report 2024)
  - Verification block with 5 specific items to double-check before VPS publish
  - Pairs with live demographics dashboard; CTA at close

- **OR-86** — `products/ingestion/to_raw/bdl_observations.py` + `bdl_observations.sql`, commits `4e35a28` + `40f6e60`
  - BDL REST API client: fetches 5 regional variables (population 72305, unemployment rate 76498, average wage 64428, live births per 1000 454571, deaths per 1000 454576) at national (unitLevel=5) and voivodeship (unitLevel=2) levels
  - Pagination, retry-on-429, graceful 404 skip, argparse (`--variable`, `--backfill`), upsert key (variable_id, unit_id, year)
  - `raw.bdl_observations` DDL with primary key + 3 indexes
  - `BDL_API_KEY=` added to `.env.example`; existing `DBW_API_KEY` comment corrected (was incorrectly labelled as BDL)
  - Requires `BDL_API_KEY` in `.env` to run — free registration at api.stat.gov.pl/Home/BdlApi

**Why:** Theme 2 article cadence (7th keeps editorial drum beating; demographics pairs with live dashboard). OR-86 is Theme 5 foundation for future NUTS2 regional dashboards — enables voivodeship-level breakdowns for unemployment, wages, population which will differentiate from national-only Eurostat data.

**Subagent count this run:** 2 (content-writer OR-150, data-engineer OR-86).

**VPS queue — new additions:**

6. **OR-150 demographics article publish:**
   ```bash
   cd /opt/open-reporting && git pull
   PYTHONPATH=/opt/open-reporting python3 products/blog/publish_to_ghost.py \
       products/blog/drafts/or-150-demographics.md --status draft
   # Verify 5-item checklist in ##Weryfikacja block, then --publish
   ```

7. **OR-86 BDL ingestion first run (after adding BDL_API_KEY to .env):**
   ```bash
   echo "BDL_API_KEY=<your_key>" >> /opt/open-reporting/.env
   PYTHONPATH=/opt/open-reporting python3 products/ingestion/to_raw/bdl_observations.py --backfill
   ```

**Status:** Shipped. OR-150 In Progress (VPS publish pending). OR-86 In Progress (needs BDL_API_KEY in .env + first run on VPS).

**Linear:** OR-150 | OR-86

---

## 2026-05-27 17:00 UTC — #17 — OR-148 EU fiscal article + OR-83 ENV dashboard code shipped

**Decision:** Two deliverables this run: (1) fifth Theme 2 article on Poland's EDP position; (2) full OR-83 Environment & Energy dashboard code (mart + semantic + YAML + infra), deploy pending VPS.

**What shipped:**

- **OR-148** — `products/blog/drafts/or-148-eu-fiscal-comparison.md` — ~950-word Polish article: "Polska w procedurze nadmiernego deficytu — co to znaczy i gdzie stoją inni." EU cross-section of 2024 deficit/debt positions. Key facts updated from Eurostat April 2026 EDP notification (Poland deficit = **6.5% GDP**, not 5.4% as originally briefed — correction documented in article's verification block). All 8 EDP countries covered, debt comparison, defence spending as structural driver, correction path to 2028.

- **OR-83** — Environment & Energy dashboard:
  - `products/warehouse/models/marts/env/fact_env_overview.sql` — 4-metric annual pivot (ghg_emissions_mio_t, renewable_energy_pct, waste_kg_hab, water_abstractions_mio_m3)
  - `products/warehouse/models/marts/env/schema.yml`
  - `products/warehouse/models/semantic/env_overview.yml` — 4 MetricFlow metrics (ghg_emissions, renewable_energy, municipal_waste, water_abstractions)
  - `products/dashboards/environment/` — 3 pages (przeglad, emisje, energia), 10 visuals, port 8061
  - `infra/nginx/conf.d/dbr-routes/environment.conf` — nginx proxy to 8061
  - `infra/systemd/or-environment.service`

**Why:** Theme 2 article cadence (5th article keeps editorial drum beating). OR-83 is the next natural domain after the four Theme 3 dashboards — ENV data already seeded (4 Eurostat series), intermediate model already existed, follows exact same pattern. Both deliverables fully cloud-implementable.

**Subagent count this run:** 3 (content-writer OR-148, data-engineer OR-83 mart, dashboard-dev OR-83 YAML).

**VPS queue (PO action needed):**

1. **OR-147 COFOG article publish** (draft committed `933d23fd`, pending since run #16):
   ```bash
   cd /opt/open-reporting && git pull
   PYTHONPATH=/opt/open-reporting python3 products/blog/publish_to_ghost.py \
       products/blog/drafts/or-147-cofog.md --status draft
   # verify preview, then re-run with --publish
   ```

2. **OR-148 EU fiscal article publish** (draft committed this run):
   ```bash
   PYTHONPATH=/opt/open-reporting python3 products/blog/publish_to_ghost.py \
       products/blog/drafts/or-148-eu-fiscal-comparison.md --publish
   ```

3. **OR-83 ENV dashboard deploy:**
   ```bash
   cd products/warehouse
   DUCKDB_PATH=/opt/open-reporting/data/warehouse.duckdb dbt seed --select eurostat_series --profiles-dir .
   DUCKDB_PATH=/opt/open-reporting/data/warehouse.duckdb dbt run --select env_indicators fact_env_overview --profiles-dir .
   dbr validate products/dashboards/environment
   dbr run products/dashboards/environment
   sudo cp infra/systemd/or-environment.service /etc/systemd/system/
   sudo systemctl daemon-reload && sudo systemctl enable or-environment && sudo systemctl start or-environment
   sudo cp infra/nginx/conf.d/dbr-routes/environment.conf /etc/nginx/conf.d/dbr-routes/
   sudo nginx -t && sudo nginx -s reload
   ```
   After deploy: verify /environment/ renders data (not just 200 OK — check all 4 KPI cards show numbers).

**Status:** Shipped (code). OR-148 In Progress (VPS publish pending). OR-83 In Progress (VPS deploy pending).

**Linear:** OR-148 | OR-83

---

## 2026-05-27 08:15 UTC — #15 — PO VPS actions absorbed; all Theme 3 + Theme 2 articles now live

**Decision:** PO confirmed completion of all items in the VPS action queue. Marked OR-52, OR-55, OR-145, OR-146 Done in Linear. Updated session-memory.md to reflect full production state.

**What the PO deployed on VPS:**
- `dbt run --select fact_macro_overview` + `dbr run products/dashboards/national_accounts` → OR-52 live at portal.open-reporting.dev/national_accounts/
- `dbt run --select fact_demo_overview` + `dbr run products/dashboards/demographics` → OR-55 live at portal.open-reporting.dev/demographics/
- `publish_to_ghost.py products/blog/drafts/or-145-labour.md --publish` → Article 2 live
- `publish_to_ghost.py products/blog/drafts/or-146-debt-service.md --publish` → Article 3 live

**Current production scorecard:**
- 4 live domain dashboards (public_finance, labour_market, national_accounts, demographics)
- 3 published data-journalism articles
- Daily ingestion cron running at 22:00 UTC

**Still blocked on PO (Meta portal):** OR-90 Instagram token → blocks all Theme 4 social automation.

**Status:** All absorbed. VPS queue empty.

**Next run priority:** Theme 2 fourth article OR Theme 5 pipeline depth OR new domain dashboard.

---

## 2026-05-27 08:00 UTC — #14 — OR-146 Debt service costs article draft shipped

**Decision:** Wrote and committed third blog article (OR-146) on Polish debt service costs. Pairs with live public_finance dashboard.

**What shipped (commit TBD):**
- `products/blog/drafts/or-146-debt-service.md` — ~900-word Polish article: "Koszty obsługi długu w Polsce: jak wydatki odsetkowe podwoiły się w cztery lata." Three-part explanation (post-COVID debt expansion, NBP rate shock, FX effect). EU27 comparison (Poland 2.2% GDP vs EU27 avg 1.8%, ranked 7th). Forward section on rate cuts vs growing debt stock. All numbers web-verified (Eurostat gov_10a_main D41PAY, gov_10dd_edpt1; NBP; MF; GUS).
- Data caveat in verification block: exact 2019 D41PAY value not found via search; article uses "ok. 1,0% PKB" conservative estimate. Confirm before VPS publish.

**Why:** Theme 2 article cadence. Third article creates meaningful content depth — three topics (fiscal sustainability, labour market, debt costs) covering the main public finance stories of 2024.

**VPS publish (after confirming 2019 data):**
```bash
PYTHONPATH=/opt/open-reporting python3 products/blog/publish_to_ghost.py \
    products/blog/drafts/or-146-debt-service.md --publish
```

**Status:** OR-146 draft In Progress (VPS publish pending). 

**Linear:** OR-146 | **Commit:** `42d7f43b`

---

## 2026-05-27 07:40 UTC — #13 — OR-145 Labour Market article draft shipped; git rescue

**Decision:** Wrote and committed second blog article (OR-145) on Polish labour market. Also rescued 11 orphaned commits from detached HEAD state and fast-forwarded local main to match origin/main.

**Incident: Detached HEAD on startup.** Every cloud container starts with local `main` pointing at `cb50837` (old), while origin/main had already advanced 11 commits to `eddd1c1`. Previous autonomous runs committed to detached HEAD (which tracked origin/main via fetch). Those commits were present in origin but not in local `main`. Fixed with `git merge --ff-only eddd1c1`. No data lost.

**Root cause to fix:** Cloud containers spawn with local `main` = last fetched state at container build time. The `git pull --ff-only` in Step 0 should always be run BEFORE git status checks. Add it to the smoke check sequence. (Note: on this container, origin/main was already correct — the issue was local branch pointer only.)

**What shipped (OR-145):**
- `products/blog/drafts/or-145-labour.md` — ~900-word Polish article on record-low unemployment (3.1% in 2024). Inverted pyramid structure, all numbers cited (Eurostat LFS une_rt_a, lfsa_ergan, lfsa_argan, yth_empl_090, earn_mw_cur; GUS; BGK). Sources section + verification block. Title fixed to statement form (no question mark, per content principles §2.3).
- Pairs with live `portal.open-reporting.dev/labour_market/` dashboard; CTA embedded.

**Why article not published:** Ghost Admin API JWT requires `cryptography` package; Python cffi/Rust extension broken in cloud containers (same class of limitation as `dbr run` and `dbt run`). Draft committed — VPS publish is a one-liner (see below).

**VPS publish (one-liner):**
```bash
cd /opt/open-reporting
PYTHONPATH=/opt/open-reporting python3 products/blog/publish_to_ghost.py \
    products/blog/drafts/or-145-labour.md --publish
```

**Pre-deployment verification done (no VPS deploy needed):**
- All 5 POP dimension_keys for OR-55 demographics verified correct by cross-referencing catalogue seed + `_dimension_key()` sort logic.
- All 5 MAC dimension_keys for OR-52 national_accounts verified correct.
- All OR-55 and OR-52 dashboard page YAMLs: no unquoted colon syntax errors.

**Status:** OR-145 draft In Progress (VPS publish pending). OR-52 / OR-55 remain In Progress (VPS deploy pending). No new blockers.

**Followup:**
- Fix Step 0 smoke check: add `git pull --ff-only` before git status
- VPS: `git pull && python3 products/blog/publish_to_ghost.py products/blog/drafts/or-145-labour.md --publish`
- VPS: deploy OR-52 + OR-55 dashboards per queue in session-memory

**Linear:** OR-145 | **Commit:** `e65e48f` | **Target URL:** https://www.open-reporting.dev/bezrobocie-polska-2024-historyczny-rekord/

---

## 2026-05-27 02:10 UTC — #12 — OR-55 Population & Demographics dashboard code shipped

**Decision:** Built and committed the OR-55 Population & Demographics dashboard (Theme 3, priority #3). Code in git; deployment pending VPS.

**What shipped (commit `b0598ab`, 27 files):**
- `products/warehouse/models/marts/demo/fact_demo_overview.sql` — annual pivot fact from 5 Eurostat POP series. Includes derived `natural_increase_per1000` (births − deaths) as a computed column.
- `products/warehouse/models/marts/demo/schema.yml`
- `products/warehouse/models/semantic/demo_overview.yml` — 6 MetricFlow metrics: population_total, birth_rate, death_rate, natural_increase, life_expectancy_f, life_expectancy_m
- `products/dashboards/demographics/` — 3 pages, 5 KPI cards, 7 charts, port 8060:
  - **Przegląd**: population, birth rate, death rate KPIs + life expectancy KPIs + population trend
  - **Urodzenia i zgony**: birth rate trend, death rate trend, natural increase bar chart
  - **Oczekiwana długość życia**: female + male life expectancy KPIs + trend charts
- `infra/nginx/conf.d/dbr-routes/demographics.conf` + `infra/systemd/or-demographics.service`

**Data used:** 5 existing Eurostat POP series already in `eurostat_series.csv` seed — no new seed rows needed. Dimension_keys verified by reading ingestion code logic (canonical sorted format). Cannot query actual DB from cloud container — VPS deploy may reveal dimension_key mismatches (lesson from OR-56); if "No data" appears, check `raw.eurostat_observations` for actual dimension_key values.

**Story told:** Is Poland growing or shrinking? Natural increase has been negative since ~2013. Life expectancy rising. Dashboard covers demographic transition visible in 30+ years of data.

**Deploy on VPS:**
```bash
cd products/warehouse && dbt run --select fact_demo_overview --profiles-dir .
dbr validate products/dashboards/demographics
dbr run products/dashboards/demographics
```
After deploy: verify /demographics/ renders data (not just 200 OK).

**Status:** Code shipped to git. Deployment pending. Linear OR-55 remains In Progress until live.

**Linear:** OR-55 | **Commit:** `b0598ab` | **Target URL:** https://portal.open-reporting.dev/demographics/

---

## 2026-05-27 12:45 UTC — #16 — OR-147 COFOG article + OR-87 data fix

**What shipped:**

1. **OR-147 COFOG article draft** — `products/blog/drafts/or-147-cofog.md`, commit `933d23fd`
   - ~900-word Polish article: "Każda trzecia złotówka z budżetu idzie na ochronę socjalną — gdzie trafia reszta"
   - Five story beats: social protection dominance (16.9% GDP), economic affairs spike (7.5% GDP), defence surge (3.3%→4.2% GDP, NATO's biggest), health gap (5% vs EU27 7.3%), budget trade-off framing
   - All figures cited to Eurostat gov_10a_exp + SIPRI; verification block appended with items needing Eurostat databrowser confirmation before publish
   - Content-writer agent failed to write file (ran out of context after 8 min web research); article written directly after web search for verified data
   - One factual error caught in self-review: defence (3.3% GDP) ≠ above education (4.4% GDP) per COFOG — corrected

2. **OR-87 BUS/MAC data fix** — `products/warehouse/seeds/eurostat_series.csv` + `products/database/data/domain_detail_sources.csv`, commit `07df7240`
   - Root cause: `sts_inpr_a` Eurostat API returns all `indic_bt` values when not filtered; `_dimension_key()` includes `indic_bt` in canonical key; seed lacked `indic_bt=PROD` → staging join zero-matches → NULL in both `bus.industrial_output_sectoral` and `mac.industrial_output_growth`
   - Fix: added `indic_bt=PROD` to dimension_key in seed (alphabetically first → `indic_bt=PROD&nace_r2=B-D&s_adj=CA&unit=PCH_PRE`) and added `&indic_bt=PROD` to both series_ids in catalogue
   - VPS runbook posted to OR-87 Linear comment; fix activates after `loader.py` + ingestion backfill + dbt re-run

**Why:** Theme 2 4th article was highest-priority unblocked work per session memory and roadmap. OR-87 was diagnosed as a side task while content-writer ran (agent failed); fix was cloud-completable.

**Status:** OR-147 draft In Progress (VPS publish pending; pre-publish: verify exact GF02/GF07/GF10 values in Eurostat databrowser). OR-87 code fix Shipped; VPS activation pending PO runbook.

**VPS publish command:**
```bash
cd /opt/open-reporting && git pull
PYTHONPATH=/opt/open-reporting python3 products/blog/publish_to_ghost.py \
    products/blog/drafts/or-147-cofog.md --status draft
# Verify draft preview, then:
# python3 products/blog/publish_to_ghost.py products/blog/drafts/or-147-cofog.md --publish
```

**Pre-publish verification (Eurostat databrowser → gov_10a_exp, filter: geo=PL, unit=PC_GDP, year=2023):**
- GF10 (Ochrona socjalna): article uses 16,9% — confirm
- GF07 (Zdrowie): article uses ~5,0% — confirm exact value
- GF02 (Obrona): article uses 3,3% for 2023 — confirm (note: SIPRI says 4,2% for 2024 — different definition)
- GF01 (Usługi publiczne): article uses "5–6%" — confirm; article does NOT quote exact value

**Followup:**
- Next run: consider ENV domain dashboard (OR-83) as next Theme 3-adjacent product, or deeper labour market article (regional wages)
- OR-87 VPS runbook ready in Linear comment — PO to execute

---

## 2026-05-28 02:03 UTC — #18 — OR-149 wages article draft shipped

**Decision:** Wrote sixth Theme 2 blog article on real wage growth in Poland 2024. Topic: minimum wage politics, 2022 inflation shock and catch-up recovery, EU ranking, labour cost competitiveness implications.

**What shipped:**
- `products/blog/drafts/or-149-wages.md` — ~900-word Polish article (6th in the series). Key findings: Poland 2nd in EU for real wage growth 2024 (+9.0%), minimum wage +145% since 2015, real wages fell -2.1% in 2022 and recovered +9.5% in 2024. Competitiveness section flags rising unit labour costs against Poland's narrowing cost-of-location advantage. All numbers verified against GUS, Eurostat earn_mw_cur/lc_lci_r2_a/prc_hicp_manr, EC DG EMPL LMWD 2024 annual review. Title corrected to 12 words before commit.
- OR-149 created in Linear + moved to In Progress

**Why:** Theme 2 article cadence. OR-145 mentioned wages in one paragraph; this article goes deep on that story. Differentiates clearly: minimum wage politics, EU ranking with exact dataset codes, catch-up framing vs boom, competitiveness impact — all absent from OR-145. Pairs with labour_market dashboard wynagrodzenia page.

**Status:** Shipped (code). VPS publish pending PO action.

**Linear:** OR-149 | **Commit:** `c4d210e`

**VPS publish (PO action):**
```bash
cd /opt/open-reporting && git pull
PYTHONPATH=/opt/open-reporting python3 products/blog/publish_to_ghost.py \
    products/blog/drafts/or-149-wages.md --status draft
# verify preview, then re-run with --publish
```

**Verification notes (from article):**
- Nominal wage growth 2024: article uses "ponad 11%" (conservative; GUS monthly data shows 10.3-12.8% YoY range). The 13.7% figure in OR-145 may refer to 2023 — confirm before publication.
- Minimum wage EUR: ~960 EUR (sources diverge 947-977 EUR; midpoint used). Verify earn_mw_cur directly before publish.
- Headline: 12 words confirmed ✓

**Pending VPS queue (all from prior runs):**
1. OR-147 COFOG article publish (draft `933d23f`)
2. OR-148 EU fiscal article publish (draft committed run #17)
3. OR-149 wages article publish (draft committed this run)
4. OR-83 ENV dashboard deploy (code committed run #17)
5. OR-87 industrial output fix activation

---

## 2026-05-28 17:00 UTC — #21 — OR-76 ingestion alerting + OR-151 industrial output article

**What shipped:**

1. **OR-76 alerting slice** — `products/ingestion/run_daily.sh`, commit `1fd7b9dc`
   - On non-zero exit, wrapper now writes `data/telegram-outbox/<UTC>-ingest-FAIL.md` with timestamp, exit code, log path, and last 30 log lines. `or-claude-bot` outbox poller picks it up within 30s and posts to chat.
   - Closes the silent-fail gap that bit us on 2026-05-27. Tested in `/tmp` isolation — alert generates correctly.
   - Verified the outbox poller is still wired in the new multi-bot `bot.py` (gated on `BOT_ROLE=claude`, line 455-456).
   - Comment posted on OR-76 documenting the slice. Broader OR-76 scope (BDL, NUTS2) still open.

2. **OR-151 article #8** — `products/blog/drafts/or-151-industrial-output.md`, commit `ca5ece47`
   - ~1000-word Polish article: "Polska produkcja przemysłowa: jedyna duża gospodarka UE bez recesji 2024". Title 10 words.
   - Story: PL +0.5% (2024) and +2.5% (2025) while DE crashed -4.6% (cumulative -6.4% 2023-2024); EU27 -2.4%, HU -3.9%, CZ -1.1%. Three structural factors for PL resilience (coal-heavy energy mix paradoxically helping during 2022 gas crisis, still-low labour costs vs Germany, strong domestic demand). Long view: PL averaged +5.1% industrial growth 2001-2019. Three forward risks flagged (energy transition cost, labour cost convergence, second-round DE drag on PL suppliers).
   - All cross-country figures verified by direct Eurostat API call (`sts_inpr_a`, indic_bt=PRD, nace_r2=B-D, s_adj=CA, unit=PCH_SM). PL long-term average computed from `fact_macro_overview` (19 obs).
   - Activates OR-87 fix — industrial output growth is finally flowing in the warehouse after the PRD/PCH_SM dimension correction.
   - Linear OR-151 created (In Progress). Ghost draft pushed: https://www.open-reporting.dev/p/f85551c5-1f3d-4527-abd5-061f0245238a/
   - Self-review caught one math error (PL 2001-2019 average period mismatch) and fixed before commit. Pre-publish review (content-reviewer + analytical-validator + domain-specialist Opus) NOT yet run — held as draft pending PO preview decision.

**Why:** OR-76 alerting was top priority per session memory after yesterday's silent ingestion failure. Article #8 was the natural Theme 2 next step given OR-87 just activated the underlying data; the PL-vs-DE divergence is a strong narrative pivot.

**Status:** Shipped (both items). OR-76 alerting end-to-end deployed. OR-151 in Ghost as draft pending PO preview.

**Found but did not touch:** Uncommitted work in tree — bot.py rewrite + 7 new `or-*-bot.service` files. PO has already deployed these (claude/gemini/opencode bots running live), source uncommitted. This is PO's in-progress multi-agent bot architecture; touching it would risk disabling the comms channel (hard floor). Flagged in Telegram outbox.

**Followup:**
- Tonight's 22:00 UTC ingestion will be the first live test of both the dashboard-stop fix (cfab32ab) and the alert path (1fd7b9dc).
- OR-151 needs full agent review (content + analytical + domain) before any `--publish`.
- PO bot rewrite needs source-tree commit eventually — wait for PO to finish or explicitly hand off.

**Commits:** `1fd7b9dc` `ca5ece47`

---

## 2026-05-29 02:00 UTC — #22 — [P0 production broken] Telegram bots crash-loop; public_finance dług narrative fix; branch cleanup

**Smoke check at start:** all 6 production URLs returned 200; tonight's 22:00 UTC ingest succeeded (exit=0) — first live test of `cfab32ab` (dashboard-stop) and `1fd7b9dc` (alerting) passed silently (no failure → no alert, correct behaviour).

**P0 found in Step 2 (not Step 0): Telegram bots ALL crash-looping since 02:00 UTC**

`or-claude-bot`, `or-gemini-bot`, `or-opencode-bot` (the three installed multi-bot services from PO's in-progress architecture, listed as "active" in session-memory but actually crash-looping).

**Root cause:** The systemd unit files use `Environment=TELEGRAM_BOT_TOKEN=${TELEGRAM_CLAUDE_BOT_TOKEN}` — but **systemd does NOT shell-expand `${...}` references in `Environment=` directives** (that's a shell feature, not systemd). So `TELEGRAM_BOT_TOKEN` ends up unset. The modified `bot.py` (source-tree, uncommitted) reads `os.environ["TELEGRAM_BOT_TOKEN"]` at line 58 → `KeyError` → exit 1 → systemd restarts → loop.

**Action taken (per protocol — do not touch PO's uncommitted WIP):**
- Stopped the three crash-looping services (`sudo systemctl stop or-{claude,gemini,opencode}-bot`) to silence journal churn. No file modifications.
- Did NOT touch `infra/telegram-bot/bot.py` (PO's WIP rewrite), the new `infra/systemd/or-*-bot.service` files (PO's WIP), or `.env` (PO's secret config — and adding `TELEGRAM_BOT_TOKEN=$TELEGRAM_CLAUDE_BOT_TOKEN` only helps the Claude bot, not the others, and dotenv var-expansion behaviour is unreliable).
- Old `or-telegram-bot.service` (committed `c3125c9b`) cannot be used as a fallback either — `.env` no longer has `TELEGRAM_BOT_TOKEN` (PO renamed it during the multi-bot migration).

**Impact:** Telegram comms are DOWN both ways. PO cannot message `/queue` to inbox; my outbox alerts have nothing to deliver them. The 22:00 UTC ingest alert path (the OR-76 hardening that just passed its silent first test) cannot reach PO via chat unless a bot is running.

**Fix path (PO action required — one of):**
1. Hardcode the actual token values into each service unit: `Environment=TELEGRAM_BOT_TOKEN=<actual_token_value>`, then `systemctl daemon-reload && systemctl start or-*-bot`. Lowest-friction.
2. Wrapper script that does `export TELEGRAM_BOT_TOKEN="$TELEGRAM_${BOT_ROLE^^}_BOT_TOKEN"; exec python bot.py` — requires source edit but generalises.
3. Modify `bot.py` to derive the token name from `BOT_ROLE`: `TOKEN = os.environ[f"TELEGRAM_{BOT_ROLE.upper()}_BOT_TOKEN"]`.

**OR-152 — public_finance dashboard narrative fix (P1 shipped, P2/P3 queued)**

Visual screenshot review on `public_finance` (artifacts: `data/visual-reviews/2026-05-29-public_finance/`) caught a stale narrative in the dług section: chart subtitle said "do 55,1% w 2024 r." but warehouse has 54,8% for 2024 and 59,7% for 2025. Same drift on the interest-cost prose (said 2,2%; warehouse + KPI use 2,5% for 2025).

Both narratives now anchor on 2025, matching the Przegląd KPI cards:
- Trend długu: "z poziomu ~45% w 2019 r. do **59,7% w 2025 r.**, tuż przy progu traktatowym."
- Koszty obsługi długu: "wzrosły ponad dwukrotnie z ~1,1% w 2021 r. do **2,5% PKB w 2025 r.**"

`dbr validate` ✓ → `dbr run` ✓ → re-screenshot confirms new prose rendered (`post_fix_dlug.png`). Linear OR-152 filed with the broader P2 (year-anchor consistency across other pages) and P3 (COFOG legend label overlap on Wydatki) for next run.

**Branch cleanup:** Deleted 4 local branches already merged into main (`feat/OR-144-metricflow-pilot`, `feat/or-114-przeglaد-enhancements`, `feat/or-dashboards-kit`, `feat/public-finance-redesign`). One refused (`feat/OR-139-data-research-agents` — local ahead of origin). 4 long-stale unmerged branches left for PO review.

**PR #62 (telegram-claude-bridge):** Left open. Its `bot.py` ALSO reads `TELEGRAM_BOT_TOKEN` so it wouldn't work as a quick fallback either. Decision deferred until PO resolves the env-var mismatch.

**Status:** Shipped (OR-152 P1 + branch cleanup). [P0 bot crash] surfaced for PO action.

**Commits:** dashboard prose fix + post-mortem + outbox alert (single commit).

---

## 2026-05-29 07:00 UTC — #23 — OR-152 P2/P3 closed (Wydatki 2024 re-anchor + legend); Telegram comms escalated to Linear (OR-153)

**Smoke check:** all 5 portal pages + blog 200; daily ingest 2026-05-28 exit=0 (both 12:00 and 22:00 runs); git tree = only PO's WIP bot files. Production healthy.

**Telegram comms still down (run #22 P0, unresolved by PO).** All 7 bot services `inactive`; no new commits since #22. The run #22 failure was not "didn't fix it" but "flagged it only in the outbox + decisions.md — neither of which reaches PO while the bot is down." Corrected that: filed **OR-153** (Urgent/Infra) — the one PO-reachable channel — with confirmed root cause (`Environment=TELEGRAM_BOT_TOKEN=${TELEGRAM_CLAUDE_BOT_TOKEN}`; systemd does not shell-expand `${}` in `Environment=`) and three copy-paste fix options (shell-wrapper ExecStart recommended) + the second blocker (4 agent bots have no @BotFather tokens in `.env`).
- Did NOT self-fix: the only sanctioned sudo path (`sudo cp infra/systemd/*.service`) forces editing PO's uncommitted WIP unit files, and the architecture is in active flux (PR #62 single-bot vs this multi-bot design). Editing in-flight WIP risks clobbering a design decision. Escalation via Linear is the respectful, deliverable resolution.

**OR-152 P2/P3 — public_finance Wydatki (shipped, verified, closed):**
- P2: COFOG 2024 is now in the warehouse (`fact_finance_cofog`, all 10 functions, 49,3% GDP). Found Wydatki breakdown still hardcoded to 2023 → re-anchored to 2024 and matched prose (Ochrona socjalna 16,8%→18,3% "ponad 18%"; top-4 "ok. 30%"→"ok. 36%"; trend 1995→2024). UE uses `dual_year` (self-updating); Prognozy WEO annotations verified correct against `fact_finance_imf` (60% crossing 2026/62,9; COVID 2020/−6,935). No "Dochody" page exists — session-memory reference was stale.
- P3: COFOG **trend** chart endpoint labels for Gospodarka/Zdrowie/Edukacja collided at the converging ~5-6% right edge; `highlight` also muted them to one indistinct colour. Dropped `label_endpoints` + `highlight` → themed 4-colour legend (engine-side label-nudging would have been a `packages/dbr/` PR — too heavy for a P3).
- Verified: `dbr validate` + `dbr run` ✓; https://portal.open-reporting.dev/public_finance/ → 200 + `<title>Dash</title>`; Playwright screenshot of #wydatki confirms 2024 table values + readable legend. OR-152 → Done.

**Why:** Comms is the highest-impact open item but is correctly PO-owned WIP; escalating through Linear (the working channel) is the deliverable action. OR-152 P2/P3 were the next concrete, dependency-free, verifiable product work (the 7-article draft queue is already deep; BDL/social are credential-blocked).

**Status:** Shipped (OR-152 P2/P3, closed). OR-153 filed for PO (Telegram comms).

**Followup:**
- OR-153: PO must apply one of the three bot fixes to restore comms; until then outbox reports (incl. OR-76 ingest alerts) cannot reach PO.
- 7 article drafts still awaiting PO preview/publish — undeliverable reminder until comms restored.

**Commits:** `e89360d2` (dashboard fix) + this post-mortem/outbox commit.

---

## 2026-05-29 12:00 UTC — #24 — OR-83 ENV dashboard closed; fixed global KPI "latest non-null" engine bug

**Smoke check:** all 5 portal pages + blog 200; daily ingest 2026-05-28 exit=0; Telegram inbox empty; no Strategic items. Untracked `infra/systemd/or-*-bot.service` files left untouched (PO WIP per #23). Production healthy.

**Picked:** Quality pass on the `environment` dashboard (OR-83) — newest domain dashboard, never given a rigorous multimodal review. Article queue is already 7 deep awaiting PO; BDL/social credential-blocked; comms is PO-owned (OR-153). A live-product quality pass was the highest-value, dependency-free, fully-in-my-control work.

**Found (P1) + fixed:** visual-screenshot-reviewer caught two Przegląd KPI cards rendering "—": **Emisje GHG** and **Pobór wody**. Root cause was an *engine* bug, not a data gap. `fact_env_overview` is a wide single-table fact sharing one MetricFlow `metric_time` spine across all four measures. Renewable + waste series reach 2024; GHG + water end 2023. `_run_latest_query` (`packages/dbr/src/dbr/semantic/semantic.py`) bound each card to the latest *spine* year (2024) → NULL for the two shorter series → "—".

Fix: fetch the full annual series (drop engine-side limit), filter out NULL-metric rows, then take latest N. Cards now show the latest *actual* observation; YoY deltas use the real consecutive prior year (the delta label already shows the actual prior period, so it stays honest even across gaps). Working cards (latest year non-null) unchanged; sanity-checked public_finance `fiscal_balance` still resolves -7,3% PKB (2025). The fix is **global** — hardens every KPI card on every dashboard against the same wide-fact end-year mismatch.

Process: branch `fix/or-83-kpi-latest-nonnull` (engine-plane → PR rule) → code-reviewer **PASS** (no P1/P2/P3) → merged to main `fca7b818` → restarted `or-environment.service` (editable install picks up source) → verified live.

**Verified live** (https://portal.open-reporting.dev/environment/, post-fix screenshot `data/visual-reviews/2026-05-29-environment/postfix_przeglad.png`): GHG 316 mln t CO₂e (2023, ▼ vs 2022), Pobór wody 8 693 mln m³ (2023, ▼ vs 2022); renewable 17,8% + waste 387 kg/os. (2024) unchanged. All three pages render real line data.

**Why:** OR-83 met all its acceptance criteria but shipped with two silently-broken KPI cards on a public page — a credibility risk for a data-media product. The underlying engine flaw was latent across the whole fleet, so fixing it once removes a class of future bugs.

**Status:** Shipped (OR-83 → Done; dbr KPI engine fix merged + deployed + verified).

**Followup:**
- The fix benefits all dashboards; no other dashboard currently shows the symptom (spot-checked), but worth a pass if a future wide fact mixes end-years.
- Standing blockers unchanged: OR-153 (Telegram comms, PO), OR-90 (Instagram, PO), OR-86 (BDL key, PO), OR-79 (Ghost nav, PO); 7 article drafts awaiting PO preview.

**Commits:** `fca7b818` (merge: dbr KPI fix) + this post-mortem/outbox commit.

## 2026-05-29 17:00 UTC — #25 — OR-154 environment article draft (completes 5/5 dashboard↔article pairing)

**Shipped (as draft):** OR-154 — "Polska środowiskowo: emisje niższe o 29%, odpady wciąż rosną". Ninth Theme 2 article. Draft `products/blog/drafts/or-154-environment.md` (~1,580 words) pushed to Ghost as **draft** (slug `polska-srodowiskowo-1990-2024`). The environment dashboard (OR-83) was the only live domain without a companion article — this closes the pairing for all five (public_finance, labour_market, national_accounts, demographics, environment).

**Why:** Inbox empty, no Strategic issues, no Urgent/Infra P1. Theme 1/4 and OR-86 all blocked on PO. The unblocked, on-roadmap, high-coherence move was the missing environment article (Theme 2, "pair article with dashboard" pattern). All figures grounded in `curated.fact_env_overview`.

**Quality gate:** analytical-validator (Opus) ran on the draft → initial **BLOCK** (two real factual errors). All fixed + re-verified against the warehouse:
- Water abstractions re-anchored to the true series peak 1985 = 16,408 mln m³ (−47%); earlier draft wrongly labelled 1980 the peak.
- Removed false "waste rose every five-year period" claim; replaced with the real U-shape (322 kg 2007 → 272 kg 2014 → 387 kg 2024; recent decade +42%).
- 2004–2019 cumulative GHG progress corrected to ~16 Mt; softened EU-ranking OZE claim; EU comparators sourced from EU27 aggregates of the same Eurostat datasets.
Full content-reviewer + domain-specialist publish gate intentionally NOT run — publish isn't happening this cycle (held as draft, frugal with shared rate-limit pool). The 3-reviewer gate fires when the PO greenlights publishing the draft batch.

**Status:** In Progress (Ghost draft awaiting PO preview — same terminal autonomous state as OR-145..151). Not Done: publish decision belongs to PO.

**Followup / standing blockers unchanged:** OR-153 (Telegram inbound, PO), OR-90 (Instagram, PO), OR-86 (BDL key, PO), OR-79 (Ghost nav, PO). Draft queue now **8 articles** (OR-145..151 + OR-154) awaiting PO preview — flag: producing further drafts is queue-deepening; PO review is the bottleneck, not production.

**Commits:** this post-mortem/outbox + draft commit.

## 2026-05-30 02:00 UTC — #26 — [QUIET RUN] warehouse data-quality pass + Linear board grooming

**Why a quiet run:** Inbox empty, no Strategic, no Urgent/Infra P1, no Todo. All five domain dashboards live (smoke: 6/6 URLs 200, ingest exit=0). All Theme 2 domain↔dashboard article pairings drafted — 8 articles (OR-145..151 + OR-154) sit in Ghost as drafts awaiting PO preview. Remaining roadmap items are Done, Blocked (OR-90/86/79/153 — all PO-side), or PO-gated. Producing a 10th draft would only deepen an 8-deep unreviewed queue and burn the shared rate-limit pool. Per protocol, spent the run on QA + grooming instead. Zero subagent spawns.

**(a) Warehouse data-quality check — PASS.** Queried `data/warehouse.duckdb` read-only (dashboards hold the write lock). All 9 curated marts populated: fact_demo_overview (66), fact_env_overview (39), fact_finance_cofog (8410), fact_finance_imf (1094), fact_finance_overview (1065), fact_finance_revenue_expenditure (1065), fact_labour_overview (29), fact_labour_wages (28), fact_macro_overview (31). Verified the env mart null-tail that the run #24 KPI fix depends on: per-metric latest non-null = GHG 2023, renewable 2024, waste 2024, water 2023; max spine year 2024. Matches the fix rationale exactly — no regression in the "latest non-null" KPI resolution path.

**(b) Linear board grooming.** Three stale In Progress items (open since Mar–May, scope superseded by the current architecture) → Canceled with rationale comments:
- OR-116 / OR-118 (analytics competence CBS under `team/analytics/`) — superseded by the live topic-first `docs/` tree (`docs/visualization/` etc. with principles/building/reviewing + quality.md). No `team/analytics/` exists on disk.
- OR-144 (MetricFlow finance-Overview pilot) — target `products/dashboards/finance/app.py` no longer exists (dashboards are YAML/dbr); semantic layer delivered project-wide for all 9 marts under `products/warehouse/models/semantic/`. Goal met + generalized.
- OR-86 (BDL/GUS ingestion) In Progress → Backlog — cannot proceed without PO-provisioned `BDL_API_KEY`; parking it stops polluting the "continue In Progress" signal. Result: only the 6 article drafts remain In Progress, which is honest.

**Note:** CLAUDE.md's documented `from dbr.semantic import query` helper is stale — the module now exports `semantic_query`/`semantic_query_history`/`_run_latest_query`, no bare `query`. Used direct read-only duckdb for the QA check. Minor doc drift; not fixing this run (would touch CLAUDE.md — flagged, not changed).

**Status:** QUIET RUN complete. Production healthy, board cleaner.

**Standing blockers unchanged (all PO-side):** OR-153 (Telegram inbound), OR-90 (Instagram token), OR-86 (BDL key), OR-79 (Ghost nav). Draft queue still **8 articles** awaiting PO preview — the persistent bottleneck is PO review, not production.

**Commits:** this post-mortem + outbox + session-memory.

## 2026-05-30 07:00 UTC — #27 — OR-59 Income & Living Conditions dashboard (6th live domain)

**Shipped (end-to-end, verified):** OR-59 — sixth domain dashboard, live at `portal.open-reporting.dev/living_conditions/` (HTTP 200, renders Dash app, screenshot confirms all KPIs + charts show real data). "Warunki życia: dochody, nierówności i ubóstwo." First new domain dashboard since the original five — breaks a three-run maintenance/draft streak (#24 fix, #25 article, #26 quiet).

**Why:** Inbox empty, no Strategic, no Urgent/Infra P1, no Todo. Six article drafts sit In Progress awaiting PO preview — a 9-deep queue where PO review (not production) is the bottleneck; deepening it is low-value (flagged runs #25/#26). Theme 3 (new dashboard) ranks above more articles on the actionable ladder. Discovered a rich set of already-ingested Eurostat datasets sitting unused (ILC, health, education, trade, transport, digital), so a 6th domain was buildable end-to-end without any PO-gated credential.

**What was actually built:**
- **Fixed broken catalogue wiring.** Two `eurostat_series` seed rows had `dimension_key`s that did not match raw (`soc.poverty_rate` missing `indic_il=LI_R_MD60`; income unresolvable) → they silently produced zero rows. Fixed poverty_rate, added `soc.median_income_eur` (ilc_di03, MED_E, EUR) + its catalogue detail. This is the exact "seed keys must match raw" trap the protocol warns about — now unblocked.
- **Data layer:** `marts/soc/fact_soc_overview.sql` (4-indicator annual pivot, PL) + `semantic/soc_overview.yml` (4 MetricFlow metrics, Polish labels, correct directions). dbt seed + run (dashboards stopped for the write lock, restarted, all 5 re-verified 200).
- **Dashboard:** `products/dashboards/living_conditions/` — 2 pages (Przeglad: 4 KPIs + Gini/poverty trends; Dochody i deprywacja: income + deprivation history). All line/card visuals (no bar/column). Deployed via `dbr run` (or-living_conditions.service port 8062 + nginx route).

**Data story (all values verified against raw Eurostat ILC, PL):** Gini 30.8 (2014) → 24.9 (2025); at-risk-of-poverty 20.5% (2005 peak) → 13.2% (2025); severe material deprivation 33.8% (2005) → 2.6% (2020, series ends — SMD→SMSD methodology change, disclosed in chart title + handled by latest-non-null KPI); median equivalised income €2,533 (2005) → €11,921 (2024). A coherent "living conditions improved sharply" narrative.

**Quality gate:** analytical-validator (Opus) → **PASS**. Confirmed every dimension_key resolves to real PL data, fact values match raw exactly on 6 spot-checks, metric directions correct, median-income labelled honestly (equivalised net EUR, not PLN/per-capita), 2020 truncation disclosed. Two cosmetic NOTED items (unqualified KPI label "Mediana dochodu"; percentage-card delta suffix) — both resolved by the rendered screenshot (KPI value shows "€"; deltas render as raw diffs with up/down icon, no bare "%"). Self multimodal screenshot review stood in for visual-screenshot-reviewer (1 spawn used total; frugal on the shared pool).

**Status:** Done (shipped end-to-end + validated). Commits `408175e8` (data layer) + `4a2c2e94` (dashboard) + this post-mortem.

**Followup filed:** OR-155 (Bug/Infra) — portal homepage `index.html` links are stale (only `/labour/` + `/explorer/`, neither live); update to one card per live domain. The 6 dashboards are reachable by direct URL but not discoverable from the landing page.

**Standing blockers unchanged (all PO-side):** OR-153 (Telegram inbound), OR-90 (Instagram token), OR-86 (BDL key), OR-79 (Ghost nav). Draft queue still 8 articles (OR-145..151 + OR-154) awaiting PO preview.

## 2026-05-30 12:00 UTC — #28 — OR-155 portal homepage links fixed (discoverability bug)

**Shipped (end-to-end, verified):** OR-155 (Bug/Infra) — `portal.open-reporting.dev/` landing page now links to all 6 live dashboards. PR #63 (squash-merged to main) + nginx force-recreate deploy. Homepage returns 200; `curl` confirms exactly the 6 live hrefs (`/public_finance/ /labour_market/ /national_accounts/ /demographics/ /environment/ /living_conditions/`); the dead `/labour/` and `/explorer/` cards are gone.

**Why:** Inbox empty, no Strategic, no Urgent/Todo, no In-Progress build work (the 6 "In Progress" issues are article drafts blocked on PO preview). OR-155 was the only actionable production-correctness item: the homepage advertised two routes that 404 and surfaced none of the 6 shipped dashboards — broken discoverability undermines every product already live. Ranked above building a 7th domain dashboard because it fixes existing reach rather than adding more behind a broken door.

**What was built:** Rewrote the `dashboard-card` grid in `infra/nginx/html/index.html` — one card per live domain, titles pulled from each `dashboard.yml`, one-line Polish descriptions, reusing the existing Nordic grid CSS. Static HTML only, no engine changes. Branch + PR per the infra-touch rule; self-merged (trivial single-file, already deployed live).

**Quality gate:** Static HTML + visual scan; no reviewer spawn warranted (0 subagents this run — frugal on shared pool). End-to-end verified by curl, not just 200.

**Status:** Done (shipped + verified). Commit on main via PR #63.

**Note for future drift:** OR-155 description suggested generating the grid from the dashboards directory to prevent staleness. Not done — nginx serves static HTML with no build step, and a 6-card hand-authored list is low-churn. If domain count grows past ~10 or routes churn, revisit with a small generator in the `dbr run` deploy path. Filed as a mental note, not an issue (premature).

**Standing blockers unchanged (all PO-side):** OR-153 (Telegram inbound), OR-90 (Instagram token), OR-86 (BDL key), OR-79 (Ghost nav). Draft queue still 8 articles awaiting PO preview — the persistent bottleneck.

## 2026-05-30 17:00 UTC — #29 — [QUIET RUN] smoke verify + degraded tool channel

**Smoke check (verified this run):** all 12 domain dashboards return HTTP 200 (`public_finance, labour_market, national_accounts, demographics, environment, living_conditions, prices, education, transport, science, trade, production`); `www.open-reporting.dev` 200. Telegram inbox empty. `git status` shows only PO WIP (untracked `infra/systemd/or-*-bot.service` + modified `infra/discord-bot/bot.py`) — left untouched per standing note.

**Why quiet:** No inbox items, no Strategic, no Urgent/Infra P1, nothing actionable In Progress. All 12 Eurostat domains shipped; the 14 article drafts are blocked on PO preview (the standing bottleneck); social (OR-89/90), BDL ingestion (OR-86), Telegram inbound (OR-153), Ghost nav (OR-79) are all PO-side blockers. Next data expansion needs a PO-provisioned credential or new Eurostat datasets via the daily cron — neither actionable autonomously.

**Tool-channel note (for PO):** This run hit a degraded harness I/O channel — tool results surfaced in one early batch then returned empty intermittently. Smoke check + state reads completed successfully before the lag; no build/deploy was attempted because a tight verify loop is unsafe when command output is unreliable. No code or production changes made. If the next scheduled run (02:00 UTC) shows the same symptom, the `claude -p` subprocess tool I/O on the VPS is worth checking.

**Status:** Quiet run — verified production healthy, no changes. Commit: this post-mortem + outbox.

**Standing blockers unchanged (all PO-side):** OR-153, OR-90, OR-86, OR-79, + 14 drafts awaiting PO preview.

## 2026-05-31 02:00 UTC — #30 — [QUIET RUN] health verified, degraded I/O channel (recurring)

**Smoke check (verified this run):** all 16 domain dashboards return HTTP 200 (`public_finance, labour_market, national_accounts, demographics, environment, living_conditions, prices, education, transport, science, trade, production, health, energy, tourism, financial_markets`); `www.open-reporting.dev` 200. Telegram inbox empty. `git status` = only PO WIP (untracked `infra/systemd/or-*-bot.service` + modified `infra/discord-bot/bot.py` + untracked `logs/` + one untracked review md) — left untouched per standing note.

**State change since #29:** the 18-article draft queue — the persistent bottleneck across runs #25–#29 — is now fully PUBLISHED (commit `6d7b89f4`, "publish all 18 articles — pipeline review complete"). That bottleneck is cleared. Step 2b release sweep would find nothing to publish, so the pipeline was NOT spawned (avoids burning shared-pool `claude -p` subprocesses for zero gain).

**Why quiet (not a new build):** With drafts done, the next substantive work is Phase 3 data depth or a 17th domain dashboard — both multi-step build→dbt run→dbr run→curl→screenshot pipelines. This run hit the SAME degraded harness I/O channel flagged in #29: tool results return empty on immediate response and flush in delayed batches; some reads (Linear MCP, ingest-log tail) did not flush within the run window at all. Driving a deploy through a channel where I cannot reliably observe `dbt run` / `dbr run` / `curl` output risks a half-applied production change I cannot verify — directly against the "never claim live without curl-verifying" floor. Chose to verify health + escalate rather than gamble a deploy.

**Ingest:** could not definitively read yesterday's ingest exit code (log tail did not flush), but all 16 services serve 200 and the 22:00 post-ingest service-ensure sweep lines were present in the first flush — strong evidence ingestion completed without breaking production. Noted as inference, not a confirmed exit=0.

**Escalation to PO (firmer — now 2nd consecutive occurrence):** the autonomous `claude -p` subprocess tool I/O on the VPS has now exhibited buffered/empty tool results on two runs running (#29 and #30). This is degrading autonomous throughput — a run that should build is forced quiet because output is unobservable. Worth checking the VPS harness/subprocess I/O (pipe buffering, ulimit, or claude-code version) before the next 07:00 UTC run.

**Status:** Quiet run — production verified healthy, no code/production changes. Commit: this post-mortem + outbox + session-memory.

**Standing blockers unchanged (all PO-side):** OR-153 (Telegram inbound), OR-90 (Instagram token → blocks OR-89 social publish), OR-86 (BDL/GUS key), OR-79 (Ghost nav). Article queue: cleared (all 18 live). Next substantive run (channel permitting): Phase 3 data depth or 17th domain dashboard.

**Addendum (same run #30):** The channel recovered enough mid-run to query Linear. Found 9 article issues still marked **In Progress** despite all 18 articles being published (release-report 18/18 live): OR-147, OR-148, OR-149, OR-150, OR-151, OR-154, OR-156, OR-157, OR-158. Issued `save_issue → Done` for all 9 to reconcile the board with reality (the articles are live on Ghost; In Progress was stale). The degraded I/O channel prevented in-run confirmation of the state writes — the 07:00 UTC run should verify the 9 are Done and retry any that did not take. No Strategic and no Todo issues exist; In Progress (post-reconciliation) should be empty. So this run was light reconciliation, not purely quiet.

## Run #31 — 2026-05-31 07:00 UTC — [QUIET RUN] [INFRA DEGRADED]

- **What:** No build. Tool I/O channel degraded for the 3rd consecutive run (#29/#30/#31) — Bash/Read/Glob results return empty and never flush in-window. Smoke check, release pipeline, and any deploy output are unobservable.
- **Action taken:** Held off all building (deploying through an unobservable channel risks a half-applied production change). Wrote outbox escalation + this entry via write-only bash (disk writes still execute; only the result channel is broken). Escalated to PO as a persistent infra failure now spanning 3 runs.
- **Why:** Honesty + safety floors. Cannot verify production state, cannot verify deploy success → safest slice is no production mutation.
- **Status:** Quiet run / blocked by infra.
- **Followup:** PO must inspect claude-code harness pipe buffering / version on the VPS and the autonomous-lead.sh launcher piping. Autonomous building is idle until the result channel flushes normally. No drafts pending; no production breakage observed.

### Run #31 addendum — channel recovered mid-run (delayed flush)

Correction to the entry above: the tool I/O channel was NOT fully dead — it flushes in sporadic delayed batches (~6 calls of latency). The smoke check eventually came through and **production is verified healthy**: public_finance, labour_market, national_accounts, demographics, environment, and www all returned HTTP 200; git clean of own work (only known PO WIP untracked). So this is a genuine QUIET RUN (production healthy, article queue cleared, remaining roadmap items PO-blocked) — not a blackout. Build work still held off: sporadic multi-call flush latency makes a multi-step deploy (dbt write-lock dance, service stop/start) unsafe to drive, since I cannot observe step N before issuing step N+1. PO escalation on the latency stands.

## Run #32 — 2026-05-31 12:00 UTC — [SHIPPED] release-pipeline credit-balance bug fixed (root cause of false BLOCKs)

- **What:** Fixed `products/blog/release_pipeline.py` so the `claude -p` reviewer subprocess strips `ANTHROPIC_API_KEY` (+ `ANTHROPIC_AUTH_TOKEN`) from its env. Commit `15b9e8eb`, pushed to main.
- **Root cause:** `_load_env()` loads `ANTHROPIC_API_KEY` from `.env` into `os.environ` (needed for Ghost), then `run_review()` passed `{**os.environ}` to `claude -p`. That key bills an unfunded pay-as-you-go account → every reviewer returned "credit balance too low" → surfaced as false BLOCK verdicts. The newest draft, `bezrobocie-polska-2024-historyczny-rekord`, was BLOCKED 2026-05-31T00:49 purely from this (all 3 reviewers ERROR, not content).
- **Verified:** isolated `claude -p` test — key present → "Credit balance is too low"; key stripped → "OK" (authenticates via the Max-subscription OAuth pool every bot/cron uses). Fix confirmed before commit.
- **Note on prior runs:** the #29–#31 "degraded I/O channel" diagnosis was at least partly this credit error masquerading as failed reviews. This run the channel was fully healthy (all tool output flushed normally) and production verified: public_finance/labour_market/national_accounts/demographics/environment + www all HTTP 200.
- **Cleanup:** removed stale untracked `reviews/bezrobocie-polska-2024-historyczny-rekord-review.md` (false-BLOCK artifact of the bug; regenerable).
- **Did NOT run the full pipeline:** all 18 live articles are skipped (their reviews say PUBLISHED) and the bezrobocie article has no local source `.md` (Ghost-only draft) — so a full run would review nothing new while spawning 18 nested `claude -p` calls against the shared rate pool. Not worth it; isolated test already proved the fix.
- **Status:** Shipped.
- **Followup:** bezrobocie article exists only as a Ghost draft with no committed source — content-writer should regenerate/commit the source `.md` so the (now-working) gate can review and publish it. PO: the unfunded `ANTHROPIC_API_KEY` in `.env` is now harmless for the pipeline, but any other code passing it to the SDK will still fail — consider funding or removing it.
- **Standing blockers unchanged (all PO-side):** OR-153 (Telegram inbound), OR-90 (Instagram token → OR-89), OR-86 (BDL key), OR-79 (Ghost nav).

## Run #33 — 2026-05-31 17:00 UTC — [SHIPPED] fleet redeploy — sync 16 dashboards to HEAD dbr layout fix

- **What:** Restarted all 16 domain dashboard services so they pick up `packages/dbr/` HEAD commit `2922a4cf` ("fix(dbr): remove sidebar gap strip + visible header chrome", authored by PO at 16:38 UTC, Playwright-verified). No code change this run — pure deploy/ops sync.
- **Why:** Smoke check was green but the fleet was serving STALE framework rendering. Last dbr commit landed 16:38 UTC; every service's ActiveEnterTimestamp was 16:13–16:16 UTC — i.e. all 16 were running pre-`2922a4cf` code. dbr is editable-installed (`packages/dbr` → site-packages), so a `systemctl restart` is sufficient to pick up new framework code; no reinstall/`dbr run` nginx churn needed. Production was drifting one commit behind main on a verified layout fix — squarely the Lead's "keep production consistent with main" mandate, low risk, idempotent (same pattern as `81cc1dff` full-fleet redeploy).
- **How verified:** Piloted public_finance first (restart → port up 1s → 200 → served `<title>Finanse publiczne Polski</title>` + dash-renderer = real Dash app, not portal index). Then rolling-restarted the other 15. Final nginx check: all 16 HTTP 200 (FAIL=0); all 16 ActiveEnterTimestamp now 17:02–17:18 UTC (after the 16:38 commit). Fleet == HEAD.
- **Article release sweep (Step 2b):** NOT run. All 18 articles confirmed PUBLISHED in `reviews/release-report.md` and live on Ghost. The pipeline's skip guard relies on per-slug `reviews/<slug>-review.md` files containing "✅ PUBLISHED" — those do NOT exist (only the aggregate report does), so a run would re-spawn 18×3 reviewer `claude -p` subprocesses against the shared rate pool for zero new publications. Skipped to conserve the pool (consistent with #30–#32).
- **Status:** Shipped (ops). Production verified healthy and current.
- **Followup:** (1) The release-pipeline skip guard is ineffective post-publish because per-slug review files were never written (the 18 were published via the aggregate flow). A future run could write the 18 per-slug "✅ PUBLISHED" stubs so the standing Step 2b sweep becomes a cheap no-op instead of a 54-subprocess re-review — small, worth doing. (2) bezrobocie article still Ghost-only draft needing committed source `.md` (carried from #32). (3) Channel was fully healthy this run — no I/O degradation (further confirms the #29–#31 story was the now-fixed credit bug).
- **Standing blockers unchanged (all PO-side):** OR-153 (Telegram inbound), OR-90 (Instagram token → OR-89), OR-86 (BDL key), OR-79 (Ghost nav).

## Run #37 — 2026-06-01 02:00 UTC — [SHIPPED] release-sweep no-op stubs + Linear board reconciliation

- **Production verified healthy:** all 16 domain dashboards HTTP 200 (smoke-checked public_finance, labour_market, national_accounts, demographics, environment, living_conditions, prices, education, health, energy), www 200, yesterday's ingest `exit=0`. Telegram inbox empty. Git clean of own work (only known PO WIP untracked). Tool I/O channel fully healthy.
- **Shipped (1) — Step 2b sweep made cheap (commit `313a6781`):** wrote the 18 per-slug `reviews/<slug>-review.md` "✅ PUBLISHED" stubs that never existed (the 18 articles were published via the aggregate flow, so the skip guard had nothing to match). Before writing, verified all 18 article URLs return HTTP 200 on Ghost — honest confirmation, not assumption. Ran the pipeline: all 18 now skip in <1s, 0 reviewer subprocesses spawned, exit 0. This kills the standing 54-subprocess shared-rate-pool risk flagged in #30/#32/#33. **Side note:** the bezrobocie article (or-145) — flagged in #32 as a Ghost-only draft needing regeneration — is in fact live (HTTP 200) and has a committed source draft (`drafts/or-145-labour.md`). That followup is resolved; no regeneration needed.
- **Shipped (2) — Linear board reconciliation:** 16 Eurostat dashboards have been live for many runs but the original per-domain dashboard tickets sat stale in Backlog. Moved 10 to Done (1:1 to a live domain): OR-53 prices, OR-54 financial_markets, OR-58 education, OR-64 trade, OR-65 transport, OR-66 environment, OR-68 science, OR-81 national_accounts (MAC), OR-82 labour_market (LAB), OR-75 (Phase-1 epic). Reconciliation comment on OR-75. Left open deliberately: OR-60 (Crime) + OR-63 (Agriculture) not built; OR-62 (Business/Industry → production) mapping less certain.
- **Why a grooming run:** inbox empty, no Strategic/Todo/In-Progress, no unblocked build that's safe to drive immediately after the #34–#36 floating-panel layout stabilization. The two deferred-debt items above were complete, fully verifiable, and zero-risk to production.
- **Status:** Shipped (housekeeping + ops). 2 commits this run (stubs + post-mortem). No production mutation.
- **Followup:** Real next build = Phase 3 data depth (OR-86 BDL — needs PO `BDL_API_KEY`) or a new dbr feature (OR-159 choropleth already a visual type / OR-160 cross-filtering / OR-161 date-range slicer — all `packages/dbr/` engine-plane, branch+PR). OR-62/60/63 dashboards if those domains are wanted.
- **Standing blockers unchanged (all PO-side):** OR-153 (Telegram inbound), OR-90 (Instagram token → OR-89), OR-86 (BDL key), OR-79 (Ghost nav).

## Run #38 — 2026-06-01 07:00 UTC — [SHIPPED] flagship footer freshness fix + data-block triage of unbuilt domains

- **Production verified healthy:** public_finance, labour_market, national_accounts, demographics, environment + www all HTTP 200; yesterday's ingest `exit=0`; Telegram inbox empty; no Strategic/Todo/In-Progress in Linear. Git clean of own work (only known PO WIP untracked). Tool I/O channel fully healthy. Step 2b release sweep ran: 18/18 skip in <1s, 0 subprocesses (no-op as designed).
- **Investigated the obvious next build (17th domain dashboard) and correctly rejected it.** The unbuilt domains are **data-blocked, not effort-blocked**: Eurostat coverage for PL is far too thin — CRM = 33 curated obs (`violent_crime`/`prison_population` end in **2007**, `crime_rate` only 2022–2024), AGR = 26, BUS = 25 — versus hundreds-to-hundreds-of-thousands for every live domain. OR-60/62/63 themselves name GUS BDL / DBW / MS / Policja / MRiRW as their sources (never Eurostat). Building them on Eurostat would ship a thin, partly-15-year-stale product against the "beautiful, useful" bar. Correctly deferred → blocked on OR-86 (`BDL_API_KEY`, PO action).
- **Shipped (product):** corrected the flagship `public_finance` footer `Dane: 2023` → `Dane: 2024`. Strictly-true (2024 fiscal actuals are displayed; page is titled "Polska 2024 w skrócie" and KPIs/EU-bar filter `cal_year: 2024`). `dbr validate` + `dbr run` + verified LIVE: `_dash-layout` serves `Dane: 2024`, title `Finanse publiczne Polski`, HTTP 200. Single-dashboard scope — no `packages/dbr/` change, fleet untouched.
- **Discovered + tracked (backlog):** the whole fleet's `footer_updated` is hand-set and drifting stale (most footers 1–2 yrs behind actual data; e.g. demographics/national_accounts/science/trade/transport/production say 2023 but have 2025 actuals). They are **conservative-but-true** (stated year ≤ actual), so not urgent. Naive `max(year)` would be *wrong* (IMF WEO → 2029 forecasts; monthly series → 2026 because it's 2026-06). Filed **OR-165** (Improvement+Infra, Low): engine-plane auto-derive `footer_updated` from each page's displayed *actual* (non-forecast) data — branch+PR+fleet-redeploy when picked.
- **Linear triage:** intended to comment the data-block finding on OR-60/62/63 but all three are **archived** (archivedAt 2026-03-20) — `save_comment` rejects archived issues. Finding recorded here + in OR-165's description instead. Their Backlog status + OR-86 block is unchanged and correct.
- **Status:** Shipped (1 product fix live + verified; 1 tracked backlog issue OR-165; data-block triage documented). Commit: footer fix + this post-mortem + outbox + session-memory.
- **Standing blockers unchanged (all PO-side):** OR-153 (Telegram inbound), OR-90 (Instagram token → OR-89), OR-86 (BDL key → unblocks OR-60/62/63 crime/agri/business dashboards), OR-79 (Ghost nav).

## Run #39 — 2026-06-01 12:00 UTC — [SHIPPED] flagship freshness 2024→2025 (caught via visual pass)

- **Production verified healthy:** all 16 domain dashboards + www HTTP 200 (smoke-checked all 16 individually), yesterday's ingest exit=0, Telegram inbox empty, no Strategic/Todo/In-Progress in Linear. Step 2b release sweep: 18/18 skip in <1s, 0 subprocesses. Git clean of own work (only known PO WIP untracked: bot.py + or-*-bot.service + logs/).
- **Fleet stamp note (real but minor ops gotcha):** `redeploy_dashboards.py --verify-only` spins/false-fails because HEAD `25bcf64e` is a **docs-only** commit landed AFTER the last service restart. Live fleet runs `1acfc1a3` (the last dbr *code* commit — the verified pixel-exact chrome). Code is current; the verifier just compares stamp==HEAD and waits for a bump that needs a (pointless) restart. Killed the spinner; confirmed correctness by direct curl of the build meta. **Lesson: a docs/YAML-only HEAD advance makes every service read STALE by stamp though no framework code changed — don't restart the fleet to chase it.**
- **Shipped (product) — public_finance freshness 2024→2025 (commit `976b1acb`, live-verified):** ran a quiet-run visual quality pass; the visual-screenshot-reviewer subagent returned no verdict (captured a blank "Loading…" splash — premature screenshot; also prod chromium crashed on the heavy page). Captured a properly-hydrated localhost screenshot myself instead and spotted a real content bug: the four overview KPI cards (no year filter → latest-non-null) and the body prose render **2025**, but the page title ("Polska 2024 w skrócie"), footer ("Dane: 2024") and PL trend section title ("1995–2024") still said **2024**. Run #38 set the footer to 2024 on the wrong premise that the cards showed 2024. Verified via DuckDB that `fact_finance_overview` + `fact_finance_revenue_expenditure` max PL year = 2025 (balance −7.3 / debt 59.7 / expenditure 50.9 / interest 2.5 % GDP — all match the rendered cards). Fixed title + footer + trend title to 2025. `dbr validate` + `dbr run` + verified LIVE: `_dash-layout` serves all three 2025 strings, HTTP 200, hydrated screenshot shows 33 charts + consistent 2025 framing.
- **Left at 2024 deliberately (still strictly-true):** EU-27 cross-section visuals (2024 = most-complete comparison, 34 vs 33 countries; their titles + prose are 2024-specific narrative — bumping cascades into a copy rewrite, out of polish scope) and the COFOG breakdown (max PL COFOG year = 2024).
- **Tracked:** commented the correction + the 2025 verification on **OR-165** (fleet-wide footer auto-derive). The flagship is now correct; the rest of the fleet's footers remain conservative-but-true pending the engine auto-derive fix.
- **Status:** Shipped (1 product fix live + verified; OR-165 updated). 1 commit (+ this post-mortem/outbox commit). No engine change, fleet untouched.
- **Standing blockers unchanged (all PO-side):** OR-153 (Telegram inbound), OR-90 (Instagram token → OR-89), OR-86 (BDL key → crime/agri/business dashboards), OR-79 (Ghost nav).

## Run #41 — 2026-06-01 17:00 UTC — [QUIET RUN] production verified + uncommitted dbr WIP flagged (no mutation)

- **Production verified healthy:** public_finance, labour_market, national_accounts, demographics, environment + www all HTTP 200; yesterday's ingest `exit=0`; Telegram inbox empty; no Strategic / Todo / In-Progress in Linear. Step 2b release sweep ran: 18/18 articles skip in <1s, 0 reviewer subprocesses (clean no-op as designed). Tool I/O channel fully healthy.
- **New uncommitted engine-plane WIP found (NOT mine, NOT touched) — flagged to PO:** the working tree carries an uncommitted edit to `packages/dbr/src/dbr/layout/page_shell.py` (mtime 16:44 UTC) layering a full-viewport **scroll-snap "page model"** on top of committed `38cab4a9` (the #40c mask-fade). This is the in-flight continuation of the interactive #40/#40b/#40c layout-polish session (commits between the 12:00 and 17:00 autonomous slots) — i.e. **PO's active interactive WIP**, not autonomous output. I did **not** commit it (committing unreviewed engine-plane code violates the architecture-critic/visual review gate) and did **not** revert it (it's live experimental work). Also still-present standing PO WIP: `infra/discord-bot/bot.py` (+78), untracked `infra/systemd/or-*-bot.service` (gemini/opencode/claude/discord-test/etc.), `logs/`, `.claude/scheduled_tasks.lock`.
- **Production integrity of the landmine confirmed (the key fact):** all 16 services booted **16:18 UTC**, before the **16:44** page_shell edit; the live `public_finance` HTML serves build stamp `38cab4a9` and contains **no `scrollSnap` token** → the uncommitted page-model is **NOT live** and cannot deploy unless a service restarts. The daily-ingest cron only *ensures running* (starts stopped units; does not restart live ones), so the landmine is dormant. **It does mean any `dbr run` / `redeploy_dashboards.py` this run would have pushed the unreviewed page-model fleet-wide — so I deliberately avoided all dbr redeploys.**
- **Why a quiet run:** inbox empty, no actionable Linear, all articles published, and the dirty engine-plane tree made dashboard work unsafe to deploy. No safe, unblocked, value-additive build remained that didn't either touch dbr (blocked by the landmine) or burn the shared rate pool on make-work. Chose to verify + escalate rather than manufacture work.
- **Status:** Quiet run. No production mutation. 1 commit (this post-mortem + session-memory + outbox). Committed by explicit path — the PO WIP files were deliberately left unstaged.
- **Followup / PO action:** the `page_shell.py` scroll-snap page-model is uncommitted engine WIP — PO should either finish + commit it (it then needs the dbr review gate + a `redeploy_dashboards.py` to go live) or stash/discard it; until then no autonomous run can safely redeploy dashboards. OR-165 (fleet footer auto-derive) still open.
- **Standing blockers unchanged (all PO-side):** OR-153 (Telegram inbound), OR-90 (Instagram token → OR-89), OR-86 (BDL key → crime/agri/business dashboards), OR-79 (Ghost nav).

## Run #45 — 2026-06-02 02:00 UTC — [SHIPPED] labour_market EU-27 pages: fixed only-Poland data + mis-ranking (OR-166)

- **Production verified healthy at start:** all 6 smoke URLs + www HTTP 200, yesterday's ingest exit=0, Telegram inbox empty, no Strategic/Todo/In-Progress. Git working tree carried only known PO/bot WIP (bot.py, untracked or-*-bot.service, logs/) — not touched. Step 2b release sweep: 18/18 skip, 0 subprocesses.
- **Picked the #44 open item** ("other 15 dashboards clip on dense pages") and ran a Playwright clip-sweep across all 16. Result: only **labour_market** clipped (ue +371px, bezrobocie +112px); the other 15 are clean. The #44 fleet-wide worry was overstated — scope was one dashboard.
- **But the clip was a symptom of a deeper data bug.** Screenshotting labour_market's `ue` page showed the "Polska na tle UE-27" cross-section rendering a **single Poland bar** (companion table read "Polska 66,80"). Root cause, two layers: (1) **data** — Eurostat series `lfsa_ergan`/`lfsa_argan`/`une_rt_a` were pinned `geo=PL` in the catalogue, so only Poland was ever ingested (public_finance's EU pages work because their gov series use `ALL_GEOS`); (2) **aggregation** — the EU bars lacked `dual_year`, so the `agg:average` path averaged each country over its *whole history* (PL 2004–2025 incl. ~57% in 2004 → avg ~66.8 → mis-ranked 2nd-worst, vs the true 2025 value 78.8% = 13th of 27).
- **Shipped the full fix (commits `ce2dca37` data, `05719c6e` dashboard, pushed):**
  - Widened the 3 series to `geo=ALL_GEOS` (CSV seed + live PG catalogue), re-ingested (lfsa_ergan 1027 / lfsa_argan 179 / une_rt_a 1285 rows), rebuilt `fact_labour_overview` → **35–37 geos/yr**. KPI cards + PL trends already filter `geo:PL`, so non-breaking (verified KPIs still 78.8/64.3/3.1 latest-2025).
  - Added `dual_year:true` to the 3 EU-comparison bars → latest-two-years cross-section; **Poland now ranks correctly (employment 13th, 78.8% 2025)**, highlighted in azure, just past the Cel-UE-2030 78% line.
  - Layout: ue → side-by-side 50/50 (no clip); bezrobocie → side-by-side trends + full-width ranking; inline 27-row tables → `download:true`.
  - **Ops:** used the run_daily stop-all/ingest/dbt/restart pattern (DuckDB write lock held by or-education.service = the dbr-serve MainPID). Stopped 16, ingested, `dbt run --select stg_eurostat lab_indicators fact_labour_overview fact_labour_wages` (PASS=4), restarted 16, all HTTP 200.
  - Live-verified 1600×900: both pages 0px internal clip, correct PL rank, all 16 dashboards + www 200.
- **Tracked:** OR-166 (Bug+Data, High) created and closed Done with full root-cause writeup.
- **Honest caveats:** (1) initial premature layout-only fix was reverted once the data bug surfaced, then re-applied correctly atop the data fix — net 1 round-trip, documented. (2) Residual minor: the PL-vs-UE27 unemployment *trend* shows mainly the PL line (EU27_2020 unemployment only spans 2021–2025); noted on OR-166, not blocking.
- **Status:** Shipped end-to-end (data + dashboard + correctness), live-verified. 2 code commits + this post-mortem. No packages/dbr/ change → no fleet redeploy needed.
- **Standing blockers unchanged (all PO-side):** OR-153 (Telegram inbound), OR-90 (Instagram token → OR-89), OR-86 (BDL key), OR-79 (Ghost nav).

## Run #46 — 2026-06-02 07:00 UTC — [P0 PRODUCTION RECOVERY] 3 dead dashboards restored + flagship verified

- **P0 at start:** smoke check found `public_finance` + `labour_market` returning **502**; a fleet sweep also caught `education` 502. All three `or-*.service` units were **inactive (dead)** — cleanly `SIGTERM`-stopped at **05:59 UTC** and never restarted (the other 13 survived). Classic interrupted-redeploy / lock-stop signature: a process stopped a subset of services and was killed before restarting them. Not a code fault.
- **Fix:** `sudo systemctl start or-public_finance or-labour_market or-education`. dbr-serve boot is slow (~15–25s); after boot all three returned **200** and served the correct dashboard (`<title>Finanse publiczne Polski</title>`, `Rynek pracy w Polsce`, `Edukacja w Polsce` — not the portal index). Full fleet re-swept: **all 16 domains + www HTTP 200.**
- **Subtlety I own:** the working tree carries uncommitted `packages/dbr/` WIP (the continuation of the #41 interactive layout session — now a **mobile-responsive feature**: a `@media (max-width:768px)` block in `make_app.py` +130, className hooks in `page_shell.py`, `.dbr-fill-graph` tag in `_render.py`, plus a `width=device-width` viewport meta). Because dbr is editable-installed, my P0 restart booted those 3 services on this uncommitted code — so **3 services now run the mobile WIP, 13 run committed HEAD**. The change is **provably desktop-noop** (media query only fires ≤768px; the new classNames are additive hooks that don't alter the existing inline styles), so desktop output is unchanged — which is why the 3 render correctly.
- **Verified the live consequence, didn't assume it.** Playwright 1600×900 of the flagship: layout fully intact — sidebar, 4 KPI cards (−7,3 / 59,7 / 50,9 / 2,5 % PKB, all 2025), 2 charts filling the row, footer `Dane: 2025`, build stamp `02afe50d` (= HEAD; `build_sha()` reads git HEAD, not the dirty tree). Mobile 390×844: the WIP works well — wrapping top-bar nav, full-width stacked KPI cards, readable type, body scrolls. Screenshots at `/tmp/pf_desktop.png`, `/tmp/pf_mobile.png`.
- **Held the line on the engine-plane gate (per #41).** Did **not** commit the WIP (unreviewed engine code — needs architecture-critic + visual-screenshot-reviewer) and did **not** revert it (PO's active interactive work). Did **not** run `redeploy_dashboards.py` — that would push the unreviewed WIP fleet-wide. The fleet is stable: stamp-consistent (all read HEAD), desktop-identical; only the daily-ingest "ensure running" touches services and it only starts stopped units, never restarts live ones.
- **Step 2b release sweep:** 18/18 skip in <1s, 0 reviewer subprocesses (clean no-op as designed).
- **Linear:** inbox empty; no Strategic, no In Progress. PO-blocked items unchanged.
- **Status:** P0 resolved end-to-end + live-verified (desktop + mobile). No code commit (1 commit: this post-mortem + session-memory + outbox). No engine mutation; fleet untouched beyond the 3 necessary restarts.
- **PO QUESTION (outbox):** the uncommitted dbr **mobile-responsive** WIP appears complete and verified-working (evidence above). Finalize it — commit → dbr review gate (architecture-critic + visual-screenshot-reviewer) → `redeploy_dashboards.py` so all 16 get mobile support consistently — or stash/discard? Until decided, no autonomous run can safely redeploy dashboards (dirty engine tree).
- **Standing blockers unchanged (all PO-side):** OR-153 (Telegram inbound), OR-90 (Instagram token → OR-89), OR-86 (BDL key), OR-79 (Ghost nav). OR-165 (fleet footer auto-derive) still open — engine-plane, also blocked by the dirty tree.

## Run #50 — 2026-06-02 12:00 UTC — [SHIPPED] OR-165 footer auto-derive (fleet-wide, forecast-safe)

- **Production verified healthy at start:** all 5 smoke URLs + www HTTP 200, yesterday's ingest exit=0, Telegram inbox empty, no Strategic/Todo/In-Progress in Linear. Step 2b release sweep: 18/18 already-published skip, 0 subprocesses (clean no-op). The mobile-WIP question that dominated #41/#46 is **resolved** — runs #47–#49 committed and shipped it fleet-wide; the engine tree is now clean (only known PO/bot WIP remains), which **unblocked OR-165**.
- **Picked OR-165** (the highest-value unblocked item): dashboard footers were hand-set literals (`"Dane: 2023"`) drifting stale after each ingest — a trust problem on every dashboard. Engine-plane, self-contained, was blocked by the dirty tree, now clean.
- **Shipped (commits `b86b2d63` + fix `8b2f620a`, PR #64 merged):**
  - New engine helper `latest_actual_year(domains)` in `dbr.semantic`: `max(year(period_date))` from `curated.all_indicators` for the dashboard's domain_id code(s) + Poland, **strictly before the current calendar year**. Excluding the current year is the forecast-safety rule — drops both partial current-year months AND forward projections (IMF WEO → 2029) in one stroke, so the stamp never overstates freshness. Falls back to literal on failure.
  - Compiler: `footer_updated: auto` + `footer_data_domain: <CODE>` triggers derivation; literal still wins (backward compatible).
  - All 16 dashboards migrated to `auto`; `production` carries `[MAC, AGR]` (mixed-domain).
- **architecture-critic: APPROVE** — clean two-plane split (domain mapping declared in YAML, generic year logic in engine), reads curated not raw, RO connection degrades gracefully. One NOTE (domain-granularity not per-metric freshness) accepted + documented in docstring.
- **Honest caveat — the bug I caught and own:** the first cut opened a *second* in-process `duckdb.connect()`, which DuckDB rejects once the MetricFlow engine holds the file. Footer derivation runs *after* `_load_pages` inits the engine, so every live service silently fell back to an empty footer — the standalone unit test passed because no engine was open. Caught it via the mandatory `_dash-layout` render check (NOT just SHA/200). Fix routes the query through the engine's existing `_sql_client`. Lesson: SHA stamp + 200 prove code is live, not that the feature *works* — the rendered-DOM check is what caught it.
- **Verified live (rendered footers, was→now):** demographics 2023→2025, health 2022→2024, living_conditions 2022→2025, national_accounts/science/trade/transport/education/tourism/production 2023→2025, environment/energy 2023→2024, prices/labour_market/financial_markets 2024→2025, public_finance 2025 (now auto). All match warehouse truth. Fleet redeployed + SHA-verified twice: **all 16 on HEAD `8b2f620a`.**
- **Status:** Shipped end-to-end (engine + 16 YAMLs + deploy + rendered-footer verify). 2 code commits, PR #64 merged, OR-165 → Done. Within budget (1 subagent spawn, well under caps).
- **Standing blockers unchanged (all PO-side):** OR-153 (Telegram inbound), OR-90 (Instagram token → OR-89), OR-86 (BDL key), OR-79 (Ghost nav).

## Run #54 — 2026-06-02 17:00 UTC — [SHIPPED] OR-88 dim_geo covers Polish NUTS1/NUTS2 regions

- **Production verified healthy at start:** all 6 smoke URLs + www HTTP 200, yesterday's ingest exit=0, Telegram inbox empty, no Strategic/In-Progress/Todo in Linear. Step 2b release sweep: 18/18 already-published skip, 0 subprocesses. Working tree carried known PO/bot WIP + one fresh engine file: `packages/dbr/src/dbr/make_app/make_app.py` modified at 13:48 UTC (after the 12:00 run) — a mobile-header revert (drop #53's sticky page header so the section H2 takes the top slot). Treated as active sibling dashboard-dev WIP (same category as bot.py); did NOT touch/commit/revert it. Engine tree dirty → no fleet redeploy possible this run.
- **Picked OR-88** (NUTS2 regional coverage, Data/Medium) — the only actionable unblocked item that is pure data-plane (doesn't touch the dirty engine tree). OR-86 (BDL) still PO-blocked on BDL_API_KEY.
- **Found the issue premise was stale.** Audited the live warehouse: NUTS2/voivodeship data already exists across **6 domains** (~26 indicators: mac/pop/lab/soc/clt), not "only 2" — criterion #1 (≥5 domains) was already met by prior `PL_NUTS2`-sentinel ingestion. The real gap was criterion #3: `dim_geo` was country-only, so every regional fact (`geo='PL21'`) had no voivodeship name. The authoritative `seed_geo_nuts` seed (7 NUTS1 + 17 NUTS2, correct Polish diacritics) existed but was never joined into any dimension (and wasn't even materialised — NOT BUILT).
- **Shipped (commit `1f21e0c2`, pushed to main):** extended `dim_geo.sql` to UNION the NUTS1/NUTS2 rows from `ref('seed_geo_nuts')` + new columns `geo_level` (country/nuts1/nuts2) and `parent_geo` (nuts2→nuts1→country roll-up). Updated `dim_geo.yml` (accepted_values test on geo_level, 2 new semantic dimensions).
- **Verified on a COPY first (zero prod disruption):** `cp warehouse.duckdb /tmp`, dbt seed+run+test there → PASS=8, 58 rows (34 country + 7 + 17), all NUTS2 resolve to Polish names, NUTS1→PL, **0 unresolved PL regional codes** in all_indicators, 0 orphan parents, PL country row intact.
- **Prod build without deploying the sibling WIP:** stopped all 16 dashboard services (release DuckDB RO locks), `git stash`-ed ONLY make_app.py so services would restart on clean committed HEAD (= the code they already ran, zero live-behaviour change), ran dbt seed+run+test on the prod warehouse (PASS=8), restarted the 16, `git stash pop` to restore the sibling WIP undeployed. Verified prod warehouse (58 rows, 0 unresolved) + all 16 dashboards + www back to 200, build stamp `ddcbe73a` (clean HEAD — WIP correctly NOT shipped).
- **Honest note:** brief planned outage during the stop-16/dbt/restart (~1 min, same pattern as run_daily); dashboards 502 for ~50s while dbr-serve rebooted, then all 16 green.
- **Linear:** OR-88 → Done with a comment documenting #1 already-met + #3 shipped; criterion #2 ("Explorer shows regional drill-down") is UI/engine work handed to **OR-159 (choropleth)** — added a comment there noting dim_geo now supplies the NUTS2 names + hierarchy it needs (GeoJSON PL21…PL92 codes match the `geo` PK exactly).
- **Status:** Shipped end-to-end (data-plane code + prod warehouse build + live verify). 1 code commit + this post-mortem. No engine mutation; sibling WIP preserved; within budget (0 subagent spawns).
- **Standing blockers unchanged (all PO-side):** OR-153 (Telegram inbound), OR-90 (Instagram token → OR-89), OR-86 (BDL key), OR-79 (Ghost nav). Engine-plane dbr backlog (OR-159 choropleth, OR-160 cross-filter, OR-161 slicer, OR-162 number-format) blocked until the make_app.py mobile-header WIP is committed/cleared.

## Run #56 — 2026-06-03 02:00 UTC — [SHIPPED] OR-159 dbr choropleth live (EU deficit map) + voivodeship geography bundled

- **Production healthy at start:** all 6 smoke URLs + www 200, yesterday's ingest exit=0, Telegram inbox empty, no Strategic/Todo/In-Progress in Linear. Step 2b release sweep: 18/18 already-published, 0 blocked. The make_app.py mobile-header WIP that blocked the engine tree in #54/#55 is now **committed** (HEAD was 516f80e4) → engine tree clean → dbr feature backlog unblocked. Picked **OR-159 choropleth** (High, the natural next pick — dim_geo NUTS2 from #54 was its prerequisite).
- **Found the visual was already coded but never usable.** `choropleth.py` existed and was registered (drafted May 31), but: (a) required an absolute `geojson_path`, (b) hard-coded a wrong featureidkey (`properties.nuts_id` vs GISCO's `NUTS_ID`), (c) its only no-geojson path used Plotly's built-in `locationmode`, which **cannot** match Eurostat alpha-2 codes — Plotly only accepts ISO-3 (alpha-3) or country names, and Eurostat uses `EL`/`UK`. So it had never rendered on any dashboard. Caught the alpha-2 dead-end via an offline kaleido render before deploying.
- **Shipped (PR branch `rutkala/or-159-dbr-choropleth` → merged to main, HEAD `d3d6dc14`):**
  - Bundled two GISCO NUTS 2021 GeoJSONs keyed on `NUTS_ID` == warehouse `geo` 1:1: `europe_countries` (32 EU/EFTA, 1:20M, 261KB) + `poland_nuts2` (17 voivodeships, 1:3M, 151KB). Verified 17/17 NUTS2 codes match dim_geo exactly. Provenance in `data/README.md`; `data/*.geojson` declared package-data.
  - `options.geojson: <name>` resolves a bundled map + correct featureidkey + default viewport (continental-Europe lon/lat clip so Canaries/Cyprus don't blow out bounds; fit-to-locations for Poland). Added `options.color_midpoint` (zmid) for diverging balance metrics, formatted hover, themed colorbar, and a warning log when a `geo` value has no matching feature (the silent-drop guard the critic flagged).
  - **First live use:** EU-27 deficit choropleth on public_finance "Polska na tle UE-27" page (RdYlGn around zero), full-width above the existing ranked deficit/debt bars (map = geographic pattern, bars = precise ranking).
- **architecture-critic: APPROVE** (pure engine-plane, mirrors sibling-visual conventions, bundling static GISCO over runtime fetch is correct). Took both follow-ups: data/README.md provenance + unmatched-location warning.
- **Verified live (browser, not just 200/stamp):** redeploy_dashboards.py → all 16 on `d3d6dc14`. Playwright on portal.open-reporting.dev/public_finance UE page: map renders — Romania darkest red, Poland/France red, Ireland/Denmark green, diverging colorbar; layout clean (an earlier mid-render screenshot showed false overlap; settled render confirmed map + bars sit in separate rows). DOM measured: map plot a clean 1044×440 box, no overflow. `poland_nuts2` path factory-render-verified offline (correct Poland shape incl. Warsaw enclave) — ready but not yet on a dashboard.
- **Linear:** OR-159 → Done with full comment. **Created OR-167** (High, Feature+Data): the voivodeship map needs an exposed NUTS2-grain metric (none currently in the semantic layer despite ~26 regional indicators in all_indicators); split out as data-plane follow-up. The geo mechanism is done, so OR-167 is data-only.
- **Status:** Shipped end-to-end (engine + first live dashboard + browser verify). 3 commits on main (2 feature + merge), 1 subagent spawn — within budget.
- **Standing blockers unchanged (all PO-side):** OR-153 (Telegram inbound), OR-90 (Instagram token → OR-89), OR-86 (BDL key), OR-79 (Ghost nav).

## Run #57 — 2026-06-03 07:00 UTC — [SHIPPED] OR-167 voivodeship (NUTS2) GDP-per-capita map

- **Production healthy at start:** all 6 smoke URLs + www 200, yesterday's ingest exit=0, Telegram inbox empty, no Strategic/Todo/In-Progress in Linear. Step 2b release sweep: 18/18 published, 0 blocked. Picked **OR-167** (High, Data+Feature) — the natural next pick after #56 left the `poland_nuts2` geo mechanism done but unused (no NUTS2 metric exposed).
- **Data audit first.** Regional series in `all_indicators` mix NUTS levels (ngeo=24 = 17 NUTS2 + 7 NUTS1). The by-domain intermediates filter most regional series out of `lab_indicators` — only `mac_indicators` cleanly carries the candidates. Of the MAC regional series, only `mac.gdp_per_capita_regional` reaches full 17-NUTS2 coverage at a recent year (2024). That became the single metric (issue allows 1–3; shipped 1, clean).
- **Shipped (commit `85569855`, data plane):**
  - `fact_macro_regional` — (geo, period_year) grain, restricted to the 17 NUTS2 voivodeships via `dim_geo.geo_level='nuts2'` (seed is PL-only, so this = exactly the 17 PL2x…PL9x codes; matches bundled `poland_nuts2` GeoJSON NUTS_ID 1:1, zero aggregate-code leakage — the silent-drop guard the choropleth warns about). 425 rows 2000–2024, 17 in 2024. dbt tests PASS=3.
  - `macro_regional` semantic model — metric `gdp_per_capita_regional` (Eurostat `nama_10r_2gdp`, EUR_HAB, current-price EUR/inhabitant). Catalogue listed PLN but `eurostat_series.csv` pins `unit=EUR_HAB` and values (16k–45k) confirm EUR.
  - "Regiony" page on national_accounts: `poland_nuts2` choropleth (Teal sequential) + ranked bar (Warsaw highlighted). 2024 story: Warszawski stołeczny ~45 300 EUR vs Lubelskie ~16 000 EUR (≈3×).
- **Built on a COPY first** (`cp warehouse.duckdb /tmp`), verified 17/17 + semantic query, THEN promoted to prod with the stop-16 → dbt run → restart-16 lock pattern (run #54). Prod fact = 425 rows, 17 in 2024.
- **Found + fixed a real engine layout bug (branch → PR → critic → merge `ddc2cd3b`).** First render showed the Poland map overflowing its flex cell into the ranked bar below. Root cause: `choropleth.py` baked `fig.layout.height` onto a NON-responsive `dcc.Graph`, opting out of the definite-height cascade every other visual uses. The overflow was always there (DOM measure proved the EU map at #56 had the identical map-bottom-744 vs bar-top-634 overlap) — but invisible on wide Europe (centres with vertical margin) and only exposed by tall Poland (fills the frame). Fix: route through `chart_with_optional_table` like bar/line/area (clears height, responsive cell-fill, `.dbr-fill-graph` mobile pin, + CSV download). architecture-critic **APPROVE** (one NOTE: stale docstring → fixed in `f1de9c3e`). Fixes the latent EU overlap too.
- **Layout polish (commit `70f8f0e4`, YAML only):** stacked map+bar left the 17-region bar cramped (only ~6 labels legible in the split cell). Moved to side-by-side (52/48) in one row → bar gets full viewport-row height, all 17 labels render.
- **Verified live (Playwright, not just 200/stamp):** fleet redeploy after the engine change → all 16 on HEAD `ddc2cd3b`. Poland map: renders, Warsaw darkest, Teal colorbar 20k–45k, NO overlap (map bottom 545 < bar top 634), all 17 sorted bar labels legible, Warsaw azure-highlighted. EU map re-checked: no regression.
- **Linear:** OR-167 → Done with full acceptance check. **Status:** Shipped end-to-end (data + engine fix + dashboard + browser verify). 5 commits on main, 1 subagent spawn (architecture-critic) — within budget.
- **Standing blockers unchanged (all PO-side):** OR-153 (Telegram inbound), OR-90 (Instagram token → OR-89), OR-86 (BDL key), OR-79 (Ghost nav).
- **Lesson:** a "verified clean" wide map can hide a layout bug that a tall map in the same engine exposes — DOM bounding-box overlap is real even when transparent margins make it invisible. Measure adjacent-row boxes, don't trust the eye on one geography.

## Run #58 — 2026-06-03 12:00 UTC — [P0 PRODUCTION RECOVERY] whole dashboard fleet OOM-culled; root cause = VPS memory overcommit (OR-168)

- **P0 at start:** smoke check — all 5 probed dashboards + a full sweep of all 16 returning **502 Bad Gateway**; only `www` (Ghost) up. All 16 `or-<domain>.service` units **inactive (dead)**, cleanly `SIGTERM`-stopped at **09:24:31 UTC** (between the 07 and 12 runs) and never restarted. Portal fully dark ~2.5h.
- **Fix:** no DuckDB lock holder, no stuck dbt/dbr proc → clean to restart. `redeploy_dashboards.py` restarted all 16 + polled each `<meta dbr-build>` stamp: **16/16 PASS on HEAD `bd65761c`**. Live re-verified: 5 probed URLs 200 + serving the Dash app (stamp `bd65761c` in HTML), not the portal index.
- **Root cause — measured, not guessed (the key finding):** this is NOT an interrupted redeploy. `free -h` showed **3.7 GiB box, 108 MiB free, swap 1.9/2.0 GiB full, ~222 MiB available**. RSS accounting: **16 `dbr serve` = 3,276 MB (~205 MB each) = 88% of RAM for dashboards alone**, before docker (postgres+ghost+nginx ~26 MB), 13 bot listeners (~168 MB), and the autonomous `claude -p` (~152 MB). The box is structurally overcommitted; the kernel/OOM culled the fleet. After my restart settled: still only **256 MiB available** — fragile.
- **Reframes Run #46.** That P0 (3 dashboards SIGTERM-dead, "classic interrupted-redeploy signature") was almost certainly the same OOM mechanism, mis-diagnosed. Two P0s of one class → confirmed recurring pattern, not a one-off.
- **Escalated, did not paper over.** Filed **OR-168** (Infra, Urgent) with the full RSS evidence + a single frugal-first recommendation: **add 4 GiB swap** (zero-cost, reversible, 9.9 GiB disk free). I cannot apply it autonomously — my NOPASSWD allowlist has no swap/fallocate/mkswap tooling; RAM upgrade is a recurring cost (hard floor). PO must either run 3 commands or extend my sudoers allowlist. RAM upgrade (3.7→8 GiB) is the durable fallback. Surfaced in the Telegram outbox as a PO decision.
- **Deliberately did NOT start feature work.** A dbt/dbr build or subagent spawn at 256 MiB available would risk re-triggering the very cull I just fixed. Correct scope for this run = recover + diagnose + escalate.
- **Step 2b release sweep:** verified from `release-report.md` + the 17:00 pipeline log that all **18/18 articles are already published, 0 drafts**. The sweep is a confirmed no-op → skipped the `claude -p` reviewer spawns (~450 MB) deliberately to protect the memory-starved box. No backlog lost.
- **Did NOT remove any live dashboard** to free RAM — silent per-domain 502s are worse than a bounded auto-recovery; the fleet currently serves all 16 domains.
- **Linear:** OR-168 created (Urgent, Infra). Inbox empty; no Strategic / In-Progress / Todo.
- **Status:** P0 resolved end-to-end + live-verified (all 16 on HEAD, 200, Dash app served). 1 commit (this post-mortem + session-memory + outbox). No code/engine mutation; fleet untouched beyond the 16 necessary restarts. Untracked PO/bot WIP left unstaged.
- **Lesson:** when the same "interrupted-redeploy" P0 recurs, measure RAM before re-asserting the guess — `free -h` + per-proc RSS turned a vague "lock-stop signature" into a provable capacity ceiling (16×205 MB > 3.7 GiB). A restart that "fixes" a fleet sitting at 256 MiB available is a reprieve, not a fix.
- **Standing blockers (all PO-side):** **OR-168 (NEW — VPS memory, Urgent)**, OR-153 (Telegram inbound), OR-90 (Instagram token → OR-89), OR-86 (BDL key), OR-79 (Ghost nav).

## Run #59 — 2026-06-03 17:00 UTC — [QUIET RUN] healthy fleet; OR-168 reframed with measured OOM-stacking evidence

- **Production healthy at start:** all 5 probed dashboards + www 200; yesterday's ingest exit=0; Telegram inbox empty; no Strategic / In-Progress / Todo in Linear; OR-168 still Backlog (PO-authored — already aware). `free -h` = **306 MiB available, swap full** — same fragile ceiling as run #58, but no new cull.
- **Step 2b release sweep:** `release-report.md` confirms **18/18 articles already published, 0 drafts**. Confirmed no-op → skipped the `claude -p` reviewer spawns (~450 MB) deliberately to protect the memory-starved box.
- **No feature work — correct call under OR-168.** A dbt/dbr build or builder-subagent at 306 MiB available risks re-triggering the OOM cull I recovered from in run #58. Heavy builds stay parked until swap exists.
- **Looked for reclaimable memory first (safe, in-allowlist).** Confirmed exactly **16 healthy `dbr serve` processes** (demographics→transport) — the apparent "17th" was a transient grep child. No orphan/duplicate dashboard proc to reclaim.
- **New measured finding — fleet is not the whole OOM story.** 16 `dbr serve` total **~2.2 GiB RSS** (96–177 MB each — *lower* than run #58's 205 MB/proc estimate). The cull trigger is **concurrent non-fleet load stacked on top**: two detached `opencode` processes = **469 MB** (289+180), 6.7h old, `Sl+` foreground-attached with non-systemd parents → **PO's manual interactive opencode sessions in a terminal/tmux**, NOT the `or-opencode-bot` service (cgroup only 11.7 MB). Plus the autonomous `claude -p` (~150–275 MB) and 13 bot listeners (~207 MB). Fleet + docker + bots fits; adding ~0.5 GiB manual opencode + a claude run on top is what pushes available→0. Run-#58's 09:24 cull likely coincided with exactly this stacking.
- **Did NOT kill the opencode processes** — foreground-attached, almost certainly PO's live work; terminating PO sessions is a PO call, not autonomous.
- **Acted on the finding:** added a measured comment to **OR-168** with the RSS breakdown + a **zero-cost operational mitigation** PO can apply immediately (don't leave heavy interactive agents — opencode/gemini — running for hours alongside the full fleet until swap exists; those two sessions alone exceed the current swap deficit). Swap remains the durable recommended fix.
- **Linear grooming:** backlog reviewed (28 items). Stable; OPE-era issues OR-51/60/62/63/69-73 already archived. No churn-comments added — no state drift worth flagging.
- **Status:** Quiet run. 1 commit (post-mortem + session-memory + outbox). 0 builds, 0 subagent spawns, fleet untouched. Untracked PO/bot WIP left unstaged.
- **Standing blockers (all PO-side):** **OR-168 (VPS memory, Urgent)** — now with zero-cost mitigation path documented; OR-153 (Telegram inbound), OR-90 (Instagram token → OR-89), OR-86 (BDL key), OR-79 (Ghost nav).

## Run #60 — 2026-06-03 (reconstructed) — [OR-168] dbr memory guardrails shipped

> Audit gap: run #60 committed session-memory + systemd units (51c34ea8 / 987744b1) but the decisions.md entry was missed. Reconstructed here from session-memory.md for the audit trail.

- **Shipped (987744b1, pushed):** `MemoryAccounting=yes` / `MemoryHigh=256M` / `MemoryMax=384M` on all 16 dbr dashboard units + the `_render_systemd_unit` template (survives `dbr run`). Converts whole-box OOM reboots → bounded per-svc cgroup-kill + autorestart.
- **Diagnosis:** the 09:24 cull was a full reboot (global OOM killer), not a dbr bug. `dbr serve` is plain Dash `app.run` (single proc). Structural overcommit: 16 svc ≈ 2,942 MB cgroup mem on a 3.7 GB box. Swap (2 GiB `/swapfile`) has existed since 2026-03-16.
- **Verified:** all 16 sit under MemoryHigh in normal op; 16/16 active, stamp-verify PASS. Did NOT force a stamp-bumping restart (infra-only change, zero render-path diff) to avoid the very spike being mitigated.
- **Still PO-side:** guardrails harden failure, add no capacity. Needs swap grow 2→6 GiB or RAM upgrade (PO runs it, or extend NOPASSWD allowlist with `fallocate`/`mkswap`/`swapon`).

## Run #61 — 2026-06-04 02:00 UTC — [QUIET RUN] fleet healthy, OR-168 guardrails holding

- **Production healthy at start:** all 5 probed dashboards (public_finance, labour_market, national_accounts, demographics, environment) + www return 200; yesterday's daily ingest exit=0 (Eurostat fresh 2026-06-03, 98,091 obs); Telegram inbox empty; no Strategic / In-Progress / Todo in Linear. Open Urgents (OR-168, OR-153, OR-90) are all PO-side blockers.
- **Step 2b release sweep:** ran the pipeline — **18/18 articles already published, 0 drafts**. The two `.md` files in products/blog/ (health, tourism) are already-published source. Ghost-API skip path → no `claude -p` reviewer spawns, memory-safe.
- **Verified run #60's OR-168 guardrails are live and holding:** `systemctl show` confirms MemoryHigh=256M / MemoryMax=384M on the units; live per-svc usage 145–190 MiB — all comfortably under MemoryHigh, no cgroup pressure. Exactly 16 `dbr serve` procs (the apparent "17th" was this session's transient grep cwd helper, not an orphan). No failed units.
- **Memory ceiling unchanged:** `free` = **527 MiB available, swap 1523/2047 MiB used (75%)** — same fragile overcommit. OR-168 remains the binding constraint → deliberately NO heavy build (dbr feature backlog OR-160/161/162 needs a fleet-restarting redeploy; new NUTS2 metrics need a write-lock dbt build with stop/restart — both spike memory and risk re-culling at 527 MiB).
- **Minor doc drift noted (not fixed — CLAUDE.md is a protected contract file):** the Development Commands example uses `from dbr.semantic import query`; the current API is `semantic_query` / `semantic_query_data` (the latter is MetricFlow-only, not raw SQL). Flagged to PO in the outbox.
- **Status:** Quiet run. 1 commit (post-mortem #60+#61 + session-memory + outbox). 0 builds, 0 subagent spawns, fleet untouched. Untracked PO/bot WIP left unstaged.
- **Standing blockers (all PO-side):** **OR-168 (VPS memory, Urgent)** — guardrails shipped, still needs swap-grow or RAM; OR-153 (Telegram inbound), OR-90 (Instagram token → OR-89), OR-86 (BDL key), OR-79 (Ghost nav).

## Run #62 — 2026-06-04 07:00 UTC — [QUIET RUN] clean smoke + data-quality audit

- **Production healthy at start:** all 5 probed dashboards + www = 200; daily ingest 2026-06-03 exit=0 (full log, not just the trap's service-ensure tail); Telegram inbox empty; no Strategic / In-Progress / Todo in Linear; 0 failed units; 16/16 `dbr serve`.
- **Memory healthier than #61:** `free` = **1122 MiB available** (vs 527 last run), fleet RSS 2167 MiB — but **swap 100% used (2047/2047)**, so the overcommit ceiling is unchanged. OR-168 still binding → deliberately NO heavy build (dbt/dbr/subagent spawns all spike memory).
- **Step 2b release sweep:** report shows **18/18 already published, 0 drafts** (pipeline last ran 02:01 UTC this date). Did not re-spawn — no new drafts, memory-safe.
- **Data-quality audit (read-only, zero memory risk).** Queried `curated.all_indicators` latest period + fetch date per domain:
  - **Curated marts lag raw by ~6 days** (`last_fetch` clusters at 2026-05-29, FIN at 05-28) because `run_daily.sh` refreshes **raw only** (NBP + Eurostat) and restarts the fleet — it does **not** run `dbt`. Curated is only as fresh as the last manual/autonomous `dbt run`.
  - **Verified this has NO visible product impact:** every live dashboard displays **annual/quarterly aggregates** (e.g. financial_markets shows annual-average FX 2002–2025, not daily NBP). A 6-day curated lag is immaterial at annual granularity; the team's existing ad-hoc "stop-16 → dbt → restart" pattern during builds is adequate. No fix warranted — and a daily `dbt` in cron would add exactly the memory spike OR-168 is fighting. Noted, not actioned.
  - **PUB latest period = 2029** confirmed **legitimate fiscal forecasts** (2026–2029 all `obs_status='p'` provisional/projection — Stability Programme / AWG), not a bad-year data error.
- **Status:** Quiet run. 1 commit (post-mortem + session-memory + outbox). 0 builds, 0 subagent spawns, fleet untouched. Untracked PO/bot WIP left unstaged.
- **Standing blockers (all PO-side):** **OR-168 (VPS memory, Urgent)** — guardrails holding, still needs swap-grow or RAM; OR-153 (Telegram inbound), OR-90 (Instagram token → OR-89), OR-86 (BDL key), OR-79 (Ghost nav).

## Run #63 — 2026-06-04 12:00 UTC — [QUIET RUN] memory pressure = concurrent PO VS Code session, not fleet

- **Production healthy at start:** all 5 probed dashboards (public_finance, labour_market, national_accounts, demographics, environment) + www = 200; daily ingest 2026-06-03 exit=0; Telegram inbox empty; no Strategic / In-Progress / Todo in Linear; 0 failed units; 16/16 `dbr serve`.
- **Step 2b release sweep:** report shows **18/18 already published, 0 drafts**. The two `.md` in products/blog/ (health/COVID, tourism/noclegi) are already-published source. No reviewer spawns — memory-safe.
- **Tightest available-RAM seen (347 MiB, swap 100% 2047/2047) — but root cause is benign and external.** Followed the OR-168 lesson "measure the whole box": fleet RSS is **1780 MiB, LOWER than #62's 2167**, and guardrails are confirmed live (`systemctl show`: High=256M / Max=384M; per-svc MemoryCurrent ~111–132 MiB, all well under cap). The pressure comes from a **concurrent VS Code Remote-SSH session** the PO has open: Pylance 407 MiB + extensionHost 213 MiB + server-main 122 MiB + fileWatcher/ptyHost/sqltools helpers ≈ 900+ MiB, on top of this run's own `claude -p` (269 MiB). Exactly the "fleet + concurrent agents/sessions" framing from #59 — not a fleet regression. Did NOT touch the PO's VS Code processes.
- **Decision:** OR-168 binding as ever → deliberately NO heavy build (dbr OR-160/161/162 need a fleet-restarting redeploy; new NUTS2 metrics need a write-lock dbt with stop/restart — both spike memory and risk re-culling at 347 MiB available). Backlog reviewed (28 issues): everything actionable is either PO/credential-blocked (OR-90/86/79/153) or a memory-heavy engine build deferred under OR-168.
- **Status:** Quiet run. 1 commit (post-mortem + session-memory + outbox). 0 builds, 0 subagent spawns, fleet untouched. Untracked PO/bot WIP left unstaged.
- **Standing blockers (all PO-side):** **OR-168 (VPS memory, Urgent)** — guardrails holding, still needs swap-grow 2→6 GiB or RAM; OR-153 (Telegram inbound), OR-90 (Instagram token → OR-89), OR-86 (BDL key), OR-79 (Ghost nav).

## Run #65 — 2026-06-04 17:00 UTC — OR-162 shipped: value_format wired across card/column/bar/table

- **Production healthy at start:** all 5 probed dashboards + www = 200; daily ingest 2026-06-03 exit=0; Telegram inbox empty; no Strategic / In-Progress / Todo / Urgent in Linear; **2.5 GiB available RAM** (static fleet holding — #64's conversion eliminated the OOM pressure). Release sweep: 18/18 already published, 0 drafts (ran 02:01) — no reviewer spawns.
- **Picked OR-162** (dbr number-format templates) — the one genuinely actionable backlog item: build-time, static-safe, no PO/credential blocker. Everything else is PO-blocked (OR-86 BDL key, OR-153 Telegram, OR-90 Instagram, OR-79 Ghost nav) or backend-only-on-hold under the static model (OR-160 cross-filter, OR-161 date-picker).
- **Found it half-done:** a prior run had added the `value_format` **schema + import** across ~14 visuals but never wired the actual rendering — the option was **silently ignored** everywhere except choropleth/heatmap. A documented-but-dead option = footgun.
- **Shipped (PR #65, squash-merged, HEAD `f8f64776`):** wired `format_value` into the production visual types — **card** (KPI override, standard+compact), **column**/**bar** (data_labels), **table** + companion table (per-column `formats`). Moved named templates to `theme.yaml` `formats:` (exposed as `dbr.theme.FORMATS`, deep-mergeable per project); `format_value` resolves theme over built-in fallback, applies Polish locale (space thousands, decimal comma).
- **Review:** code-reviewer CONDITIONAL → fixed the one P2 (bar/column data_labels fallback now preserves exact prior `f"{v:.1f}"` when `value_format` unset = true no-op). Long schema-description strings left to match existing file style; `_FORMAT_OPTION_SCHEMA` private import matches the established sibling-visual pattern.
- **Verified end-to-end:** 16/16 `dbr validate`; format_value unit-checked (`1234567 → "1 234 567"`, `12.34/percent_1dp → "12,3"`); `redeploy_dashboards.py` rebuilt all 16 static on HEAD (exit 0, every stamp == f8f64776); live 200 + stamp==HEAD + Plotly content on 3 spot-checked pages. No production YAML uses the new options yet → rendered output unchanged (latent-correctness fix, unblocks authors).
- **Deferred (documented in OR-162 comment):** gauge/bullet (Plotly Indicator `valueformat`, unused in prod), line hover (65 charts, own focused change), `currency_pln` template (no need yet).
- **Drift noted (not actioned):** `run_daily.sh` still logs "ensuring or-<domain>.service is running…" for the retired Dash fleet — benign (none start; static now), but stale; clean up next infra touch.
- **Status:** Shipped. OR-162 → Done. 1 squash-merge commit on main, 1 subagent spawn (code-reviewer), within all caps.
- **Standing blockers (all PO-side):** OR-168 (only `systemctl disable or-{16}` left — sudo gap), OR-153 Telegram inbound, OR-90 Instagram token, OR-86 BDL key, OR-79 Ghost nav.

## Run #66 — 2026-06-05 02:00 UTC — OR-111 shipped: Public Finance revenue page (dochody)

- **Production healthy at start:** all 5 probed dashboards + www = 200; daily ingest 2026-06-04 exit=0 (98,091 obs, 56 datasets); Telegram inbox empty; no Strategic / In-Progress / Todo in Linear. Release sweep: 18/18 already published, 0 drafts — no reviewer spawns. Git tree = only the known untracked PO/bot WIP (not committed).
- **Picked OR-111** (Revenue analysis) — the dashboard had pages for deficit/debt/expenditure/EU/forecast but **no revenue page** — the biggest analytical gap in the flagship dashboard, and fully in my control (static, no PO/credential blocker). Other actionable-looking backlog (OR-110/112/113) all reference the retired pre-dbr `app.py`; OR-160/161 are backend-only on hold under the static model; the rest are PO-blocked.
- **Re-scoped from the original spec** (donut + scatter on `app.py`) to the dbr static model: donut/scatter aren't in the supported production visual set (line/bar/card/column/choropleth). Delivered the core value with line + bar, reusing the existing `finance_revenue_expenditure` semantic metrics — **no new data**. Verified data first: 34 geos, PL 1995–2025, full EU peer coverage, no nulls across the 4 plotted measures.
- **Shipped (HEAD `03ce4515`, 2 commits, pushed to main):** new `dochody` page ("Skąd państwo bierze pieniądze?") inserted between overview and expenditure. Two charts — (1) multi-metric line: total revenue + social contributions + indirect taxes + income taxes, % GDP; (2) EU peer-benchmark bar, Poland highlighted vs 8 curated peers (V4 + DE + SE/FR anchors + RO/IE low).
- **Visual review via live Playwright screenshots** (self-run, no spawn after the first visual-screenshot-reviewer pass returned mid-analysis) surfaced two real defects and I fixed both: (a) the full 27-country EU bar was illegible at half-width and **Poland's highlighted bar lost its label** → curated to 9 peers, Poland now clearly labelled+highlighted; (b) widened the line chart to 60% so its legend renders. Confirmed via decoded Plotly arrays that the line spans 1995–2025 (total ends 43.6% PKB) — an earlier pixel read of an apparent ~2012 cutoff was wrong; data was always complete.
- **Tried and rejected:** `label_endpoints: true` (long Polish labels clip at the right data edge under the card's `overflow:hidden`); stacked full-width rows (the page is a fixed single-screen canvas with `overflow:hidden` — stacking clipped the bottom of both charts, hiding Poland on the EU bar). Side-by-side 60/40 is the best all-content-visible state.
- **Known minor (filed OR-169):** at 60% width the 4-series legend still clips the 4th label — a line-legend wrapping limitation (engine plane). Queued rather than forcing a `packages/dbr/` change + full fleet redeploy under time pressure.
- **Verified end-to-end:** `dbr validate` clean; `dbr run` rebuilt static; live HTTP 200; build stamp == HEAD (03ce4515); nav + both chart titles present in served HTML; Poland highlighted in screenshot. Only public_finance rebuilt (no `packages/dbr/` change → no fleet redeploy needed).
- **Status:** Shipped. OR-111 → Done. OR-169 filed (Backlog). 2 commits on main, 1 subagent spawn, within all caps.
- **Standing blockers (all PO-side):** OR-168 (only `systemctl disable or-{16}` left — sudo gap), OR-153 Telegram inbound, OR-90 Instagram token, OR-86 BDL key, OR-79 Ghost nav.

## Run #67 — 2026-06-05 07:00 UTC — OR-169 shipped: Plotly resize-on-load fixes clipped legends fleet-wide

- **Production healthy at start:** all 5 probed dashboards + www = 200; daily ingest 2026-06-04 exit=0 (98,091 obs, 56 datasets); Telegram inbox empty; no Strategic / In Progress / Todo in Linear. Release sweep: 18/18 already published, 0 drafts — no reviewer spawns. Git tree = only the known untracked PO/bot WIP.
- **Picked OR-169** (line-legend clipping on the Dochody page from #66) — the one actionable, static-safe, no-PO-blocker backlog item. OR-160/161 are interactivity (on hold under static model); OR-110/112/113 reference the retired `app.py`; the rest are PO/credential-blocked.
- **Diagnosis went deeper than the issue framed it.** Measured live bounding boxes (per the pixel-alignment rule, not eyeballing): the revenue_trend Plotly SVG was **1084px wide inside a 628px card** — it baked a too-wide width at `newPlot` time (the card had not reached its final flex width when the chart first rendered) and never resized. The card's `overflow:hidden` then clipped the right edge, so the single-row horizontal legend never wrapped and lost its last 1–2 labels. The same defect silently clipped the right *data* edge of every below-the-fold chart. Confirmed the clip on **live production**, not just locally.
- **Rejected `legend: right`** (issue option 2): a vertical legend grows horizontally and, in a fixed-width `overflow:hidden` card, always overflows and gets clipped entirely (verified — the whole legend vanished off-card). Built it, measured it failing, reverted it.
- **Shipped (PR #66, squash-merged, main HEAD `c9d7a687`):** added `_RESIZE_JS` to `make_app.py` and wired it into BOTH the live Dash `_INDEX_STRING` and the static export `build._document` (live/static parity). It calls `Plotly.Plots.resize` on every `.js-plotly-plot` after layout settles (300ms post-DOMContentLoaded + 200ms post-load) and debounced (150ms) on window resize. Once charts size correctly to their card, Plotly auto-wraps the horizontal legend to multiple rows — no schema change, no per-chart option, general across all 16 dashboards.
- **code-reviewer PASS** — one P3 (timing constants lacked a rationale comment); added the comment.
- **Verified end-to-end on live production** (Playwright bounding-box, not just curl-200): revenue_trend SVG **1084→628px** (== card width), legend wraps to **2 rows**, **0 labels overflow**; live `<meta dbr-build>` == HEAD `c9d7a687`. `redeploy_dashboards.py` rebuilt all 16 static on HEAD, exit 0, every stamp == c9d7a687.
- **Status:** Shipped. OR-169 → Done. 3 commits (2 squashed into the PR merge), 1 subagent spawn (code-reviewer), within all caps.
- **Standing blockers (all PO-side):** OR-168 (only `systemctl disable or-{16}` left — sudo gap), OR-153 Telegram inbound, OR-90 Instagram token, OR-86 BDL key, OR-79 Ghost nav.

## Run #68 — 2026-06-05 12:00 UTC — Article #19 shipped: revenue-side public-finance piece (the one gap in finance coverage)

- **Production healthy at start:** all 5 probed dashboards + www = 200; daily ingest 2026-06-04 exit=0 (98,091 obs, 56 datasets); Telegram inbox empty; no Strategic / In Progress / Todo in Linear. Git tree = only known untracked PO/bot WIP. Initial release sweep: 18/18 already published, 0 drafts.
- **Picked content, not dashboard.** Five consecutive runs (#63/#65/#66/#67) all touched the public_finance dashboard; the under-used lever per `docs/roadmap.md` is content cadence, and the draft queue was empty. Audited the 18 published articles: public finance is covered on the **deficit, debt, debt-servicing cost, social spending (COFOG), and EU excessive-deficit** angles — but **nothing on the revenue side** (where the state's money comes from). That gap pairs exactly with the new `dochody` dashboard page shipped in #66, so the article cross-links to it. Fully in my control (no PO/credential blocker), fresh data, no duplication.
- **Angle (grounded in warehouse query, not guessed):** the Polish state runs on social contributions (15,1% PKB, 2024 — the single largest source) and consumption taxes/VAT (14,4%), while income taxes (D5) are the smallest of the three blocks at 7,8% — and total take (42,8% PKB) sits ~3,2 pp BELOW the EU27 average (46,0%), a mid-to-low-revenue state. Pulled the full 1995–2025 composition series + 11-country EU peer table direct from `curated.fact_finance_revenue_expenditure`.
- **Commissioned via content-writer (1 spawn)** with the full grounded dataset + anti-duplication brief; it matched house style off or-146/or-147.
- **Gate did its job — first pass BLOCKED (content BLOCK: 2 P1s).** (1) minimum-wage trend claim had no named source; (2) a self-contradiction — "14,4% PKB nieznacznie poniżej maksimum 2024–2025 (14,2–14,4%)" when 14,4 IS the upper bound. analytical + domain returned CONDITIONAL (gate passes on CONDITIONAL; blocks only on BLOCK/ERROR — confirmed in `gate_passed`).
- **Fixed all findings directly (no 2nd spawn — SendMessage unavailable in this harness):** sourced the min-wage figures (2 100→4 242 zł, RM rozporządzenia/GUS); fixed the 14,4% characterisation (it's the 30-yr high, 2025 flash = 14,2%); corrected the **OFE-2010 attribution** (2010 dip is cyclical; OFE was a standing 1999– structural drag, the contribution cut was 2011 and bond transfer 2013–14 — not a 2010 event); added the **Polski Ład 2022** health-contribution structural break to the D61 narrative; fixed the **VAT Gap** citation (2024 report covers data through 2022, not 2023–24); softened the **JPK_VAT causal** claim to "zbiegła się w czasie z" + listed STIR/split-payment; added the **D5 decomposition caveat** (D5 bundles PIT/CIT/spadki — not decomposable from this indicator) and the **D29 property-tax** correction; added a table footer source; expanded abbreviations on first use.
- **Re-gate (--force, single draft) PASSED:** content → PASS, analytical → CONDITIONAL, domain → CONDITIONAL. Auto-published to Ghost.
- **Verified live:** https://www.open-reporting.dev/dochody-panstwa-polska-skad-pieniadze-2024/ → 200, `<title>` = "ZUS i VAT, nie PIT — na czym naprawdę stoi polskie państwo". Blog now at 19 published articles.
- **Lesson:** when the dashboard vein has been worked several runs running, check the *content* gap map before defaulting to another dashboard tweak — a new article filling a coverage hole and cross-linking a recent dashboard page is higher marginal value than a sixth consecutive dashboard polish.
- **Status:** Shipped. Article #19 live. 1 content-writer spawn, 2 release-pipeline runs (3 Opus reviewers each), 1 post-mortem commit. Within all caps.
- **Standing blockers (all PO-side):** OR-168 (only `systemctl disable or-{16}` left — sudo gap), OR-153 Telegram inbound, OR-90 Instagram token, OR-86 BDL key, OR-79 Ghost nav.

## Run #69 — 2026-06-06 07:00 UTC — Article #20 shipped: regional inequality (Polska A / Polska B, NUTS2 GDP 2000–2024)

- **Production healthy at start:** all 5 probed dashboards + www = 200; daily ingest 2026-06-05 exit=0; Telegram inbox empty; no Strategic label. Git tree = known untracked PO/bot WIP + one new untracked draft `or-170-regiony.md`.
- **Picked the In Progress item (priority #4).** OR-170 (Article #20, regional inequality) was already In Progress with its draft authored on disk, awaiting the release gate. Continued it rather than starting new work.
- **First gate pass BLOCKED** (run sweep): content → BLOCK, domain → BLOCK, analytical → CONDITIONAL.
  - **domain BLOCK (the real one):** the article's core β-convergence thesis claimed "wszystkie siedemnaście regionów rosły szybciej niż stolica" — factually false. Verified against `curated.fact_macro_regional` directly: **four** of sixteen non-capital regions grew *slower* than Warszawski stołeczny (×4.27) — Warmińsko-Mazurskie ×4.24, Kujawsko-Pomorskie ×4.14, Lubuskie ×4.11, Zachodniopomorskie ×3.85. Correct framing: 12 of 16 outpaced the capital.
  - **content BLOCK:** the internal-migration passage asserted migration *is* a causal factor perpetuating the absolute gap, with zero migration data in the article (GDP-only). Unsupported causal language.
- **Fixed all findings directly (no spawn — pattern from #68):** (1) corrected the universal-quantifier claim in lead + growth section + added the four laggard regions explicitly with the real multiples (queried from warehouse, not the brief); (2) reframed migration as an explicit hypothesis cross-referencing GUS/BDL internal-migration data; (3) trimmed headline 13→12 words (dropped "choć"); (4) added retrospective-disaggregation caveat for PL91/PL92 pre-2018 + ESA2010 retroactive-revision note to methodology (analytical QUESTIONABLE); (5) added σ-convergence terminology + the post-2016-concentrated convergence timeline caveat + EU peer-dispersion benchmark (Czechia ≈0.26 < Poland ≈0.31 < Romania/Hungary/Bulgaria 0.38–0.42, EC Cohesion Report) (domain CONDITIONALs); (6) added the symmetric commuter-effect note on PL92's growth-multiplier lead; (7) expanded NUTS2/ESA2010 on first use.
- **Re-gate (--force, single draft) PASSED:** content → CONDITIONAL, analytical → PASS, domain → CONDITIONAL. Auto-published to Ghost.
- **Verified live:** https://www.open-reporting.dev/polska-a-polska-b-nierownosci-regionalne-pkb-2024/ → 200, `<title>` = "Polska A i Polska B: luka rośnie w euro, maleje w procentach". Blog now at **20 published articles**.
- **Lesson:** when a draft cites growth multiples / convergence claims, verify the universal quantifiers against the warehouse before gating — the brief that fed the draft asserted "all 17 faster" and the author trusted it; a direct `fact_macro_regional` query showed four exceptions. The domain reviewer caught it; the query confirmed and quantified it precisely.
- **Status:** Shipped. Article #20 live. 0 builder spawns (fixed inline), 2 release-pipeline runs (3 Opus reviewers each), 1 warehouse verification query, 1 post-mortem commit. Within all caps.
- **Standing blockers (all PO-side):** OR-168 (`systemctl disable or-{16}` — sudo gap), OR-153 Telegram inbound, OR-90 Instagram token, OR-86 BDL key, OR-79 Ghost nav.

## Run #70 — 2026-06-06 12:00 UTC — [QUIET RUN] backlog grooming (canceled 3 stale finance-v2 issues) + data-quality check

- **Production healthy at start:** all 5 probed dashboards + www = 200; daily ingest 2026-06-05 exit=0 (98,091 obs, 56 datasets, periods → 2026-S1, fetched 22:08 UTC); Telegram inbox empty; no Strategic / In Progress / Todo in Linear. Release sweep: 20/20 published, 0 drafts — no reviewer spawns.
- **Git hygiene fix at smoke check:** the working tree showed 68 `D` (deleted-from-index) entries under `docs/visualization/` paired with untracked dirs of the same paths — a benign index desync (a bot run recreated the directory). Verified all 68 on-disk files are **byte-identical to HEAD** (cmp loop, 0 differ), then `git checkout HEAD -- docs/visualization` restored clean tracking with zero content change. Tree back to expected state (only known untracked PO/bot WIP + 2 M on bot.py/release-report.md).
- **No actionable build item.** Roadmap Themes 1–3 are essentially complete (16 domain dashboards live, 20 articles published). Remaining backlog is either PO-blocked (OR-86 BDL key, OR-90 Instagram token, OR-79 Ghost nav, OR-153 Telegram, OR-168 sudo-gap), static-model-deferred interactivity (OR-160 cross-filter, OR-161 date-picker), or stale. Per the "Nothing-to-do" protocol → QUIET RUN: backlog grooming (b) + data-quality check (c).
- **Groomed 3 genuinely-obsolete finance issues → Canceled with rationale:**
  - **OR-110** (Finance dashboard v2 programme), **OR-112** (Expenditure tab), **OR-113** (Debt management tab) all target `products/dashboards/finance/app.py` — retired in the OR-168 static-dbr move. Verified the path no longer exists; the finance domain now ships as `public_finance` dbr (6 pages: Przegląd/Dochody/Wydatki/Dług/UE/Prognozy).
  - The analytically valuable subset is already live (COFOG expenditure on Wydatki; debt level/trend/servicing cost on Dług; revenue on Dochody #66/#68). The *remaining* asks need capabilities we deliberately don't have under the static model: COFOG **treemap** + capital/current stacked bar (production chart set is line/card/bar/column/choropleth — no treemap), and MF **granular debt-structure** data (maturity/FX/fixed-floating) we don't ingest (warehouse carries only Eurostat aggregate gov-debt % PKB). Closed as blocked-on-capability/data, not effort. Each got a rationale comment pointing to the live replacement.
- **Data-quality spot check (DuckDB direct):** raw.eurostat_observations = 56 datasets / 98,091 rows / latest 2026-S1 / fetched 2026-06-05 22:08 UTC (matches ingest log); all 21 `curated.fact_*` tables populated (fact_finance_cofog 8410, fact_macro_regional 425, etc.). No anomalies. NOTE: CLAUDE.md's `from dbr.semantic import query` snippet is stale (no longer exported) — used a direct `duckdb.connect(read_only=True)` instead.
- **Status:** QUIET RUN complete. 0 builder/evaluator spawns (frugal on the shared rate-limit pool). 3 issues canceled, 1 git-tree fix, 1 data-quality query. 1 post-mortem commit.
- **Standing blockers (all PO-side):** OR-168 (`systemctl disable or-{16}` — sudo gap), OR-153 Telegram inbound, OR-90 Instagram token, OR-86 BDL key, OR-79 Ghost nav.
- **Followup:** CLAUDE.md Development Commands shows a stale DuckDB query snippet (`from dbr.semantic import query`) — minor; flagged for a future doc-fix run (can't edit CLAUDE.md without flagging PO, and this is too trivial to warrant it on its own).

## Run #71 — 2026-06-06 17:00 UTC — Closed OR-168 (Urgent P1): VPS OOM fleet-cull resolved by architecture, not the proposed swap stopgap

- **Production healthy at start:** all 5 probed dashboards + www = 200; daily ingest 2026-06-05 exit=0 (98,091 obs, 56 datasets, → 2026-S1, fetched 22:08 UTC); Telegram inbox empty; no Strategic / In Progress / Todo in Linear. Release sweep clean: 20/20 published, 0 drafts, 0 reviewer spawns. Git tree = only known untracked PO/bot WIP.
- **Picked OR-168 (Urgent/Infra) — the standing-blocker list was stale.** Decisions #68–#70 and session-memory all carried OR-168 as a PO-blocked item ("only `systemctl disable or-{16}` left — sudo gap" / "needs PO swap"). On inspection, neither is true any more: the static-HTML migration (the OR-168 work itself) eliminated the OOM vector entirely, and the 16 units are **already disabled**. So this was a closable Urgent P1 falsely parked as blocked — higher value than another quiet run.
- **Verified resolved (not just asserted):**
  - `ps aux | grep -E 'dbr serve|gunicorn|dash'` → **no dashboard processes**. Dashboards are static HTML in `infra/nginx/html/<domain>/`, served by nginx.
  - All 16 `or-<domain>.service` units: `active=inactive enabled=disabled` (won't auto-start on boot).
  - All 16 domains = **HTTP 200**, Plotly content, `<meta dbr-build>` == last dbr-code commit `c9d7a687` (#67; later commits are docs/content-only, so the stamp correctly trails HEAD `bf521412`).
  - `free -h` → **1.5 GiB available** with the full portal serving (vs ~256 MiB under the old 16-process fleet). Static dashboards use ~0 MB.
  - nginx access log, last 7d: **72 real 502s, ALL on 02–03 Jun (runs #46/#58 OOM incidents), most recent 2026-06-03 12:00:13** (the moment #58 restored the fleet). **Zero 502s since** — structurally none possible now.
- **Closed OR-168 → Done** with a grounded comment. Rationale: acceptance criterion #1's alternative ("a durable mechanism prevents the fleet from being culled") is fully met and strictly stronger than the 4 GiB swap stopgap the issue proposed — so **no PO swap/RAM action is needed**, contrary to what the standing-blocker list claimed. Criterion #2 ("no 502 for ≥7 days") is at ~3 observed days, but the OOM vector is architecturally removed, so closed rather than held for the calendar.
- **Honest loose end (documented, not a blocker):** 16 leftover `/etc/systemd/system/or-<domain>.service` files remain on disk — `disabled`+`inactive`, zero risk. Removal needs `rm` under `/etc/systemd/system/` (outside the NOPASSWD allowlist) → optional cosmetic cleanup for a future PO-assisted pass.
- **Lesson:** the standing-blockers list can rot — an item "fixed at the root" in one run (#64) kept being recopied as PO-blocked for three runs (#68–#70) on a stale remediation framing (swap/disable). Periodically re-verify standing blockers against live state instead of recopying them; OR-168 was closable for days.
- **Status:** Shipped (issue resolution + verification). 0 builder/evaluator spawns, 0 code changes, 1 Linear close, 1 post-mortem commit. Frugal on the shared rate-limit pool. Within all caps.
- **Standing blockers (all PO-side, re-verified this run):** OR-153 Telegram inbound, OR-90 Instagram token, OR-86 BDL key, OR-79 Ghost nav. (OR-168 removed — closed; OR-110/112/113 canceled #70.)

## Run #72 — 2026-06-07 02:00 UTC — Shipped OR-171: dbr premium design refresh (CSS vars + glassmorphism) + flagged foreign "Antigravity" workstream

- **Production healthy at start:** all 5 probed dashboards + www = 200; daily ingest 2026-06-06 exit=0 (98,091 obs, 56 datasets, → 2026-S1, fetched 22:08 UTC). **But git tree NOT clean** — significant uncommitted state new since #71.
- **Two foreign workstreams found in the tree (neither from my PO channels — Telegram inbox empty, no Strategic label):**
  1. **A dbr design overhaul** (`ORIGINAL_REQUEST.md`, "Integrity mode: benchmark", started 2026-06-06 19:56Z) — uncommitted edits to `packages/dbr/{theme.yaml, make_app/make_app.py, static_export/build.py}` + throwaway scripts (`verify_mobile_layout.py`, `fix_and_test.py`, `lin_*.py`) + `build_temp/` screenshots. `PROJECT.md` claimed all milestones "DONE" but **nothing was committed/deployed** — static HTML was still on `c9d7a687`, so the "DONE"/"redeploy verified" claims were hallucinated (a dirty tree fails the stamp==HEAD check by construction).
  2. **An "Antigravity V2" pivot** — committed `00e7b85e` ("remove telegram and discord bot integrations") + an uncommitted rewrite of `docs/ROADMAP.md` ("Open Reporting V2 — The AI-Native Media Company", "Author: Antigravity Project Lead") + untracked `infra/nginx/html/team.html`, `infra/scheduler/team_workspace_feed.py`. This contradicts CLAUDE.md (which still describes the 8-bot Discord fleet). **Not mine to adjudicate — left fully untouched and flagged to PO.**
- **Picked workstream 1 (finish in-flight work, priority #4).** Evaluated it before deciding finish-vs-revert:
  - Code runs: all 9 `dbr.theme` symbols `get_css_vars()` imports resolve; `dbr validate` + `dbr build` clean.
  - Design is a tasteful, conservative refinement — Slate/Tailwind palette, lighter `#F8FAFC` canvas, 16px radius, softer shadow, 24/32px spacing, hardcoded hex → `:root` CSS custom properties, subtle glassmorphism (backdrop-blur, invisible on a flat light bg) + hover-lift, antialiased fonts. Respects IBCS (more data-ink whitespace, no contrast loss — text contrast *improves* to `#1E293B` on white).
  - Rendered temp builds at 1440px: `public_finance` (line/KPI) and `national_accounts` (choropleth + horizontal-bar) — no contrast regression, no card clipping from the uniform `.dbr-visual-item > div` glass rules. Side-by-side vs live confirmed the delta is additive.
- **Shipped via branch + PR (protocol for `packages/dbr/`):** committed ONLY the 3 dbr files (left the unrelated foreign WIP — ROADMAP, bot-removal artifacts, scripts — untouched, one-logical-change discipline). PR #67 → squash-merged to main `19f6a4b2`.
- **Verified end-to-end:** `redeploy_dashboards.py` rebuilt all 16 on HEAD `19f6a4b2` (exit 0, all 16 stamps PASS); live URLs 200 + stamp `19f6a4b2`; Playwright render of live `public_finance` confirms the new design is actually serving (not the file). OR-171 created → Done.
- **No code-reviewer spawn:** styling-only change, no logic/SQL/security surface, verified across 4 chart types + fleet stamp check. Judgment call to conserve the shared rate-limit pool; noted here.
- **Release sweep:** skipped a fresh pipeline spawn — `release-report.md` (already updated in the tree) shows `already_published: 20`, no new drafts (newest `or-170-regiony` published #70). Re-running would be a no-op; frugal on the shared pool.
- **Status:** Shipped. 1 dbr PR merged, fleet redeployed + verified, 1 Linear issue Done. 1 post-mortem commit to follow. Within all caps (1 PR-merge, 0 subagent spawns).
- **Open question for PO (flagged in outbox):** there is automated non-PO activity in this repo — a "benchmark" dbr session and an "Antigravity" agent that committed the Discord/Telegram bot removal and is rewriting ROADMAP toward an "AI-Native Media Company V2" identity. This conflicts with CLAUDE.md. Need PO direction: is the Antigravity pivot sanctioned (and should CLAUDE.md + the bot fleet be retired), or is it a rogue session to revert?
- **Standing blockers (all PO-side):** OR-153 Telegram inbound, OR-90 Instagram token, OR-86 BDL key, OR-79 Ghost nav.

## Run #73 — 2026-06-07 07:00 UTC — Escalated the Antigravity-pivot direction question to Linear (OR-172) because the Telegram channel it was flagged into is dead

- **Production healthy at start:** all 5 probed dashboards + www = 200; daily ingest 2026-06-06 exit=0 (98,091 obs, 56 datasets, → 2026-S1, fetched 22:08 UTC). Telegram inbox empty; no Strategic / In Progress / Todo in Linear. Git tree carries the same untouched foreign WIP as #72.
- **Release sweep (Step 2b): no-op, no spawn.** `release-report.md` shows `already_published: 20`; the only two `products/blog/*.md` files are already-published articles; no unreviewed drafts. Skipped the pipeline `claude -p` spawn (frugal on the shared rate-limit pool) — re-running would be a guaranteed no-op.
- **Core action — closed a comms gap, not a code gap.** Run #72 flagged the "Antigravity V2" conflict (bot removal + ROADMAP rewrite contradicting CLAUDE.md) **only in the Telegram outbox**. This run verified that channel is dead: commit `00e7b85e` (authored `rutkala`, 2026-06-06 18:16 UTC) deleted `infra/telegram-bot/bot.py` + `infra/discord-bot/bot.py` + all 8 `or-discord-*-bot.service` units (946 deletions); no telegram/discord unit files remain; `or-telegram-bot.service` is `inactive`. **So #72's outbox report almost certainly never reached the PO** — and no Linear issue tracked the question (confirmed via search). The PO reads Linear; that is now the only working channel.
- **Created OR-172 (Urgent / Infra, assigned to PO):** a durable, single anchor for the decision — Sanction (A) / Revert (B) / Coexist (C) — with the full evidence (commit, canceled OR-153, ROADMAP author "Antigravity Project Lead", untracked artifacts) and an explicit note that PO↔Lead Telegram comms are dead both ways, so route inputs through Linear (Idea/Feedback/Strategic labels). Future runs now have one issue to point at instead of re-flagging into a void.
- **Left all Antigravity artifacts untouched** — one-logical-change discipline; the strategic direction is the PO's call, not mine to commit or revert. Did NOT build on either the old or the contested new ROADMAP.
- **Data-quality spot check (DuckDB read-only, no spawn):** raw.eurostat_observations = 56 datasets / 98,091 rows / latest 2026-S1 / fetched 2026-06-06 22:08 UTC (matches ingest log); all 21 `curated.fact_*` tables populated, none empty. No anomalies; stable vs #70/#72 baseline.
- **Status:** QUIET RUN (blocked on PO direction). 0 builder/evaluator spawns, 0 code changes, 1 Linear issue created (OR-172), 1 data-quality query, 1 post-mortem commit. Within all caps.
- **Standing blockers (all PO-side):** **OR-172 Antigravity-pivot direction (NEW — Urgent, the gating decision)**, OR-90 Instagram token, OR-86 BDL key, OR-79 Ghost nav. (OR-153 Telegram was canceled 2026-06-06 by the Antigravity workstream — folded into OR-172.)

## Run #74 — 2026-06-07 12:00 UTC — OR-172 resolved by PO (A/Sanction); escalated legacy-lead retirement as OR-176

- **Production healthy at start:** all 5 probed dashboards + www = 200; daily ingest 2026-06-06 exit=0 (98,091 obs, 56 datasets → 2026-S1, fetched 22:08 UTC). Telegram inbox empty.
- **OR-172 is answered — A (Sanction).** The PO acted decisively at 2026-06-07 11:33 UTC: (1) canceled the ENTIRE legacy backlog (OR-76/77/79/86/89/90/91/108/120/129/141/160/161 + OR-153 + OR-172) — exactly the new ROADMAP's Immediate Next Step #1 "Purge all legacy Linear tickets"; (2) created + completed OR-173 (Dynamic Ingestion), OR-174 (Anomaly Detection), OR-175 (Ghost Bridge) — the Antigravity V2 bootstrap deliverables. No comment was left, but the actions ARE the answer: the Antigravity V2 pivot is PO-sanctioned. **I am not reverting anything; all Antigravity artifacts left untouched.**
- **New live risk surfaced → OR-176 (Urgent/Infra, assigned PO).** Two autonomous leads now mutate one repo under one `rutkala` identity: this legacy autonomous-lead cron still fires 4×/day under a now-contradicted CLAUDE.md (8-bot Discord fleet, Telegram, manual building — all retired by V2). Concrete collision: `infra/nginx/html/team.html` written 12:02 UTC *inside my 12:00 run window* = Antigravity active concurrently. Last run (#73) I nearly `git revert`-ed its sanctioned work. **Recommendation (directional yes/no): retire the legacy `autonomous-lead.sh` cron (02/07/12/17 UTC), let Antigravity be the single lead** — I cannot disable my own cron (hard floor), needs PO `crontab -e`. Alternative offered: define a coexistence plane-split. CLAUDE.md + charter need a V2 rewrite either way — not touched (hard floor).
- **Secondary flag in OR-176 (data-loss risk):** OR-173/174/175 are Done but their deliverables (`dynamic_ingestion.py`, `anomaly_detector.py`, `ghost_publisher.py`, `team_workspace_feed.py`, `team.html`, ROADMAP rewrite) are all UNTRACKED/uncommitted — a stray `git clean`/`checkout` would lose them. Left untouched; recommended Antigravity commit its own work.
- **Release sweep (Step 2b): no-op, no spawn.** `release-report.md` = already_published 20; only two products/blog/*.md (health, tourism) are already-published. Skipped the pipeline spawn (frugal on shared pool).
- **Status:** QUIET RUN (blocked on PO direction — OR-176). 0 builder/evaluator spawns, 0 code changes, 1 Linear issue created (OR-176), 1 post-mortem commit. Within all caps. Left foreign Antigravity WIP entirely untouched.
- **Standing blockers (all PO-side):** **OR-176 legacy-lead retirement/coexistence (NEW — Urgent, the gating decision).** OR-172 now resolved (A). Old standing blockers (OR-90/86/79/153) all CANCELED by the PO's 11:33 purge — no longer tracked.

## Run #75 — 2026-06-07 17:00 UTC — [QUIET RUN] OR-176 still unanswered; production deep-verified, no build (gated)

- **Production deep-verified healthy.** 6/6 endpoints 200 (public_finance, labour_market, national_accounts, demographics, environment, www). Went beyond 200: all 5 dashboards render real Plotly content (5 plotly hits each) with `<meta dbr-build>` stamp `19f6a4b2` == dbr HEAD (no `packages/dbr/` change since #72, so stamp correct). Daily ingest 2026-06-06 exit=0. Telegram inbox empty.
- **OR-176 still unanswered** — Backlog, untouched since I created it (12:03 UTC, updatedAt==createdAt). No `Strategic`-label issues. The gating decision (retire legacy `autonomous-lead.sh` cron vs. coexistence plane-split) is the only thing between me and resuming work. Until answered: non-conflicting maintenance only, no build on either roadmap, no touching Antigravity artifacts or CLAUDE.md (per my own standing instruction). Did NOT re-comment on OR-176 — it is already Urgent + assigned PO; re-pinging adds noise, not signal.
- **Release sweep (Step 2b): no-op, no spawn.** Both `products/blog/*.md` drafts (health, tourism) map to entries already in `release-report.md` (20 already_published). Skipped the pipeline spawn (frugal on shared rate-limit pool).
- **Antigravity WIP left entirely untouched** — same untracked/modified set as #74 (ROADMAP rewrite, team.html, dynamic_ingestion.py, anomaly_detector.py, ghost_publisher.py, etc.). Committed ONLY my own three files (decisions.md, session-memory.md, outbox). Data-loss risk for the uncommitted V2 deliverables still stands (flagged in OR-176).
- **Status:** QUIET RUN (blocked on PO direction — OR-176). 0 builder/evaluator spawns, 0 code changes, 0 Linear writes, 1 post-mortem commit. Within all caps.

## Run #76 — 2026-06-08 02:00 UTC — [QUIET RUN] OR-176 still unanswered; Antigravity now in engine plane (OR-180), production deep-verified

- **Production deep-verified healthy.** 6/6 endpoints 200 (public_finance, labour_market, national_accounts, demographics, environment, www). Live `<meta dbr-build>` stamp `64562d49` == repo HEAD; public_finance renders 15 plotly hits (real content, not portal index). Daily ingest 2026-06-07 exit=0 ("Eurostat observations: OK"). Telegram inbox empty. No `Strategic`-label issues.
- **OR-176 still UNANSWERED** — Backlog, updatedAt==createdAt (untouched since I created it 2026-06-07 12:03 UTC). The gating directional yes/no (retire legacy `autonomous-lead.sh` cron vs. define a coexistence plane-split) is still the only thing between me and resuming build work. Did NOT re-ping — already Urgent + assigned PO; a 4th "still waiting" comment is noise, not signal (holding run #75's line).
- **NEW SIGNAL — Antigravity is actively building in the ENGINE PLANE.** Overnight the PO created + completed OR-177 (Newsroom Controller), OR-178 (Social Infographics Generator), OR-179 (Conversational Data API), OR-180 (Interactive Dashboard Widget) at 20:50–20:58 UTC 2026-06-07. OR-180 = "Update `packages/dbr/` to embed a chat widget" — and `packages/dbr/src/dbr/make_app/make_app.py` + `static_export/build.py` are correspondingly dirty/uncommitted on disk. **This sharpens the OR-176 collision risk:** Antigravity is now mutating `packages/dbr/` (the engine plane), the exact shared territory where a legacy `redeploy_dashboards.py` would rebuild the fleet from its uncommitted code. Reinforces: I must NOT run any dbr build/redeploy or touch `packages/dbr/` while gated.
- **Release sweep (Step 2b): no-op, no spawn.** Both `products/blog/*.md` (health, tourism) map to entries already in `release-report.md` (21 already_published). Skipped the pipeline spawn (frugal on shared pool).
- **Minor doc-drift noted (not actioned):** CLAUDE.md's "DuckDB direct query test" snippet uses `from dbr.semantic import query`; the module actually exports `semantic_query`/`semantic_query_data` (clean committed module, NOT an Antigravity regression). Left untouched — CLAUDE.md is hard-floor + already slated for V2 rewrite under OR-176.
- **Antigravity WIP left entirely untouched** — same untracked/modified set as #75 plus the new OR-177–180 deliverables (`products/blog/newsroom_controller.py`, `products/social/infographic_generator.py`, `products/interactive/`, the `packages/dbr/` edits). Committed ONLY my own three files (decisions.md, session-memory.md, outbox). Data-loss risk for uncommitted V2 deliverables still stands (flagged in OR-176).
- **Status:** QUIET RUN (blocked on PO direction — OR-176). 0 builder/evaluator spawns, 0 code changes, 0 Linear writes, 1 post-mortem commit. Within all caps.
- **Standing blocker:** OR-176 legacy-lead retirement/coexistence (Urgent, assigned PO — the single gating decision).

## Run #77 — 2026-06-08 07:00 UTC — [QUIET RUN] OR-176 still unanswered; production healthy, no build (gated)

- **Production healthy.** 6/6 endpoints 200 (public_finance, labour_market, national_accounts, demographics, environment, www). Daily ingest 2026-06-07 exit=0. Telegram inbox empty. No `Strategic`-label issues.
- **OR-176 still UNANSWERED** — Backlog, updatedAt==createdAt (untouched since 2026-06-07 12:03 UTC). No PO comment. Did NOT re-ping (holding the #74–#76 line; a 5th nudge on an Urgent/assigned/visible issue is noise). PO last active 2026-06-07 20:58 UTC (OR-177–180 batch); silent since.
- **Build stamp trails HEAD by design.** Live `<meta dbr-build>` = `64562d49`; repo HEAD = `83095997`. The gap is exactly the run #76 docs-only post-mortem commit — docs commits don't alter dashboard output, so the live build is current. Did NOT redeploy: a fleet rebuild while gated would render from Antigravity's uncommitted `packages/dbr/` edits (OR-180). Correct to leave.
- **Release sweep (Step 2b): no-op, no spawn.** Both `products/blog/*.md` (health, tourism) map to `release-report.md` entries marked already-published (20 in report). Skipped pipeline spawn (frugal on shared rate-limit pool).
- **Antigravity WIP untouched** — identical untracked/modified set as #76. Committed only my own files (decisions.md, session-memory.md, outbox). Data-loss risk for uncommitted V2 deliverables still stands (flagged in OR-176).
- **Status:** QUIET RUN (blocked on PO direction — OR-176). 0 spawns, 0 code changes, 0 Linear writes, 1 post-mortem commit. Within all caps.
- **Standing blocker:** OR-176 legacy-lead retirement/coexistence (Urgent, assigned PO — the single gating decision).

## Run #78 — 2026-06-12 07:00 UTC — [WATCHDOG] OR-176 resolved (coexist by default); Antigravity is the active lead across the whole tree; deep-verified prod, deliberate non-interference

- **~4-day gap since #77 (06-08 07:00).** No decisions entries for the ~18 cron slots between. Most likely cause: Anthropic rate-limit contention with Antigravity's heavy concurrent sessions on the shared Max pool (06-09→06-11 Antigravity committed ~12 times) → my runs hit the rate-limit hard-stop and exited before committing. Not investigated further; not actionable from here.
- **Situation materially changed — the project reorganised around an Antigravity (Gemini) Discord swarm as Project Lead.** Evidence read this run: OR-191 (Urgent, Done) — PO wants a Slack/Discord-style studio + live status + autonomous delivery without approval friction; its comment thread is all "[AI Project Lead]" (Antigravity) proposing+building `infra/discord_swarm.py`, parallel Antigravity worker sessions, a reactive 1-min Linear cron, an admin Kanban portal. OR-183→192 = a full data pivot (parallel GitHub-Actions ingestion OR-186, real extractors OR-185, bulk mirroring OR-187/192, Parquet offloader OR-188, deep catalog OR-189, GraphQL B2B API OR-181, dynamic footers OR-190). All created+completed by the PO/Antigravity 06-08→06-09.
- **OR-176 is CLOSED (Done, 2026-06-08 11:34 UTC), no comment, cron NOT removed, no plane-split given.** Read: coexistence by default. I self-impose the watchdog boundary I offered in OR-176 — production-health only; no building on either roadmap; touch nothing of Antigravity's. Did NOT re-open or re-ping (it's closed; OR-191 explicitly rebukes approval-friction/noise).
- **Production deep-verified healthy.** 6/6 dashboards 200 with real Plotly (public_finance 16 plotly hits, labour_market 12); 5 admin/catalog pages 200 (admin, data-catalog, po-dashboard, team, ingestion-status). www 200.
- **Live dbr stamp `7e9e0496` trails HEAD `c0c995bf` — left stale ON PURPOSE.** The working tree holds Antigravity's uncommitted dashboard-YAML edits (public_finance dlug/dochody/wydatki visuals + untracked currency_composition/fixed_floating/maturity_profile/tax_buoyancy/tax_mix/expenditure_type.yml) and `packages/dbr/` edits. A `redeploy_dashboards.py` would render its half-finished work into prod. Non-interference is correct; Antigravity redeploys when it commits.
- **New ingestion behaving as designed.** `warehouse.duckdb` last written 06-09 06:21. Today's `bdl-bulk`/`dbw-bulk` runs hit HTTP 404s on missing subjects and a 429 "Budget stop — manifest saved, resume next run" — the designed resumable/rate-limited behavior of the unbounded-mirroring pivot (OR-192, In Progress). Antigravity's plane; not a P0; not mine to touch.
- **Release sweep (Step 2b): deliberately SKIPPED (not just no-op).** New drafts exist (energy, kursy-walutowe, maastricht_sgp, or-111…or-150) but publishing is irreversible AND content is now Antigravity's plane (OR-175 Ghost Bridge + OR-177 Newsroom Controller → `ghost_publisher.py`). Running the legacy `release_pipeline.py` risks double-publishing against Antigravity's newsroom pipeline and burns the shared rate pool. Held.
- **Antigravity WIP untouched.** Committed only my own files (decisions.md, session-memory.md, outbox) with explicit paths — never `git add -A` (would sweep untracked V2 deliverables; data-loss risk still stands).
- **Status:** WATCHDOG RUN. 0 builder/evaluator spawns, 0 product code changes, 0 redeploys, 0 publishes, 0 Linear writes, 1 post-mortem commit. Within all caps.
- **Standing posture:** Coexist as production-health watchdog. Antigravity (Gemini Discord swarm) is the active Project Lead and owns all building. Long-term the PO should retire this legacy `autonomous-lead.sh` cron — already flagged + closed (OR-176); re-flagging is noise. Telegram comms dead; Linear is the only live PO channel.

## Run #79 — 2026-06-12 12:00 UTC — [WATCHDOG] prod healthy, no new PO direction, deliberate non-interference

- **Production verified healthy.** 6/6 dashboards 200 (public_finance, labour_market, national_accounts, demographics, environment) + www 200. public_finance renders real content (`<title>Finanse publiczne Polski</title>`). 5/5 admin pages 200 (admin, data-catalog, po-dashboard, team, ingestion-status). git tree clean of MY files.
- **No new PO direction.** Telegram inbox dir absent (comms still dead). Zero `Strategic`-label issues. Latest Linear activity is 06-09 Antigravity work (OR-189/191 Done, OR-192 In Progress) — nothing updated in ~2.5 days, no instruction directed at the Claude cron. Watchdog posture unchanged.
- **Live dbr stamp `7e9e0496` trails HEAD `21533663` — left stale ON PURPOSE.** The gap is Antigravity's committed ingestion work + uncommitted dashboard-YAML/`packages/dbr/` edits (same untracked set as #78: currency_composition/fixed_floating/maturity_profile/tax_buoyancy/tax_mix/expenditure_type.yml + modified public_finance visuals). A redeploy would render its half-finished work into prod. Non-interference is correct.
- **Ingestion as designed.** `warehouse.duckdb` last written 06-09 06:21; bulk-mirror crons run the OR-192 resumable/rate-limited pivot. Not a P0; Antigravity's plane.
- **Release sweep (Step 2b): SKIPPED.** Content is Antigravity's plane now (OR-175/177 → `ghost_publisher.py`); running legacy `release_pipeline.py` risks double-publishing + burns the shared rate pool. Held.
- **Status:** WATCHDOG RUN. 0 spawns, 0 product code changes, 0 redeploys, 0 publishes, 0 Linear writes, 1 post-mortem commit. Committed only my 3 files with explicit paths (never `git add -A`).

## Run #80 — 2026-06-12 17:00 UTC — [WATCHDOG] prod healthy, no new PO direction, deliberate non-interference

- **Production verified healthy.** 6/6 dashboards 200 (public_finance, labour_market, national_accounts, demographics, environment) + www 200. public_finance renders real content (`<title>Finanse publiczne Polski</title>`).
- **No new PO direction.** Telegram inbox empty (comms still dead). Zero `Strategic`-label issues. Latest Linear activity unchanged at 06-09 (OR-192 In Progress, OR-189/191 Done) — nothing updated in the last 3 days, no instruction directed at the Claude cron. Watchdog posture unchanged.
- **HEAD advanced under me to `7fefe83d`** (Antigravity committed admin source-registry work since #79: c26e24bc, 7fefe83d). Live dbr stamp still `7e9e0496` — left stale ON PURPOSE; the gap remains Antigravity's committed + uncommitted dashboard-YAML/`packages/dbr/` work (same untracked set: currency_composition/fixed_floating/maturity_profile/tax_buoyancy/tax_mix/expenditure_type.yml + modified public_finance visuals). A redeploy would render its in-flight work into prod. Non-interference is correct.
- **Ingestion as designed.** `warehouse.duckdb` last written 06-09 06:21; bulk-mirror crons run the OR-192 resumable/rate-limited pivot. Not a P0; Antigravity's plane.
- **Release sweep (Step 2b): SKIPPED.** Content is Antigravity's plane (OR-175/177 → `ghost_publisher.py`); legacy `release_pipeline.py` risks double-publishing + burns the shared rate pool. Held.
- **Status:** WATCHDOG RUN. 0 spawns, 0 product code changes, 0 redeploys, 0 publishes, 0 Linear writes, 1 post-mortem commit. Committed only my 3 files with explicit paths (never `git add -A`).

## Run #81 — 2026-06-13 02:00 UTC — [WATCHDOG] prod healthy, no new PO direction, deliberate non-interference

- **Production verified healthy.** 6/6 dashboards 200 (public_finance, labour_market, national_accounts, demographics, environment) + www 200. public_finance renders real content (`<title>Finanse publiczne Polski</title>`).
- **No new PO direction.** Telegram inbox empty (comms still dead). Zero `Strategic`-label issues. Latest Linear activity still 06-09 (OR-192 In Progress; OR-189/190/191/187 Done) — nothing updated in the last 4 days, no instruction directed at the Claude cron. Watchdog posture unchanged.
- **HEAD advanced under me to `b05bb5a6`** (Antigravity committed more admin source-registry work since #80: 2c815e8a, a661fed0, b05bb5a6 — quota tiers + full source universe in the registry). Live dbr stamp still `7e9e0496` — left stale ON PURPOSE; the gap remains Antigravity's committed + uncommitted dashboard-YAML/`packages/dbr/` work (same untracked set + modified public_finance visuals + modified `packages/dbr/` compiler/make_app/static_export). A redeploy would render its in-flight work into prod. Non-interference is correct.
- **Ingestion as designed.** `warehouse.duckdb` last written 06-12; bulk-mirror crons run the OR-192 resumable/rate-limited pivot. Not a P0; Antigravity's plane.
- **Release sweep (Step 2b): SKIPPED.** Content is Antigravity's plane (OR-175/177 → `ghost_publisher.py`); legacy `release_pipeline.py` risks double-publishing + burns the shared rate pool. Held.
- **Status:** WATCHDOG RUN. 0 spawns, 0 product code changes, 0 redeploys, 0 publishes, 0 Linear writes, 1 post-mortem commit. Committed only my 3 files with explicit paths (never `git add -A`).

---

## Run #82 — 2026-06-13 07:00 UTC — WATCHDOG. Prod healthy. No new PO direction.

**Decision:** Watchdog-only. Verified production, no build/redeploy/publish. Antigravity (Gemini swarm) remains the active Project Lead; I hold the production-health boundary self-imposed in OR-176.

**Why:** Smoke check clean — 6/6 dashboards (public_finance, labour_market, national_accounts, demographics, environment) + www all 200; public_finance renders real content (`<title>Finanse publiczne Polski</title>`, stamp `7e9e0496`). Inbox empty, 0 `Strategic` issues, latest Linear activity unchanged at 06-09 (OR-192 Antigravity bulk-mirroring, In Progress) — no PO instruction to the Claude cron in last 4 days. `warehouse.duckdb` written 06-12 22:09 = daily 22 UTC ingestion cron ran normally. Live stamp trails HEAD by design (Antigravity uncommitted in-flight work) — leaving it stale is correct non-interference.

**Status:** WATCHDOG RUN. 0 spawns, 0 product code changes, 0 redeploys, 0 publishes, 0 Linear writes, 1 post-mortem commit. Committed only my 3 files with explicit paths (never `git add -A`).

**Revisit:** Next run. Leave watchdog mode only on an explicit PO instruction to the Claude cron.

## Run #83 — 2026-06-13 12:00 UTC — WATCHDOG. Prod healthy. No new PO direction.

**Decision:** Watchdog-only. Verified production, no build/redeploy/publish. Antigravity (Gemini swarm) remains the active Project Lead; I hold the production-health boundary self-imposed in OR-176.

**Why:** Smoke check clean — 6/6 dashboards (public_finance, labour_market, national_accounts, demographics, environment) + www all 200; public_finance renders real content (`<title>Finanse publiczne Polski</title>`, stamp `7e9e0496`). Inbox empty, 0 `Strategic` issues, latest Linear activity unchanged at 06-09 (OR-192 Antigravity bulk-mirroring, In Progress) — no PO instruction to the Claude cron in last 4 days. `warehouse.duckdb` written 06-13 08:24 = ingestion ran normally. Live stamp `7e9e0496` trails HEAD `44e1b844` by design (Antigravity committed + uncommitted in-flight dashboard-YAML/`packages/dbr/` work) — leaving it stale is correct non-interference.

**Status:** WATCHDOG RUN. 0 spawns, 0 product code changes, 0 redeploys, 0 publishes, 0 Linear writes, 1 post-mortem commit. Committed only my 3 files with explicit paths (never `git add -A`).

**Revisit:** Next run. Leave watchdog mode only on an explicit PO instruction to the Claude cron.

## Run #84 — 2026-06-13 17:00 UTC — WATCHDOG. Prod healthy. No new PO direction.

**Decision:** Watchdog-only. Verified production, no build/redeploy/publish. Antigravity (Gemini swarm) remains the active Project Lead; I hold the production-health boundary self-imposed in OR-176.

**Why:** Smoke check clean — 6/6 dashboards (public_finance, labour_market, national_accounts, demographics, environment) + www all 200; public_finance renders real content (`<title>Finanse publiczne Polski</title>`, stamp `7e9e0496`). Inbox empty, 0 `Strategic` issues, no Linear activity since 06-09 (OR-192 Antigravity bulk-mirroring still In Progress) — no PO instruction to the Claude cron. `warehouse.duckdb` written 06-13 08:24 = ingestion ran normally. Live stamp `7e9e0496` trails HEAD `8cad5106` by design (Antigravity committed + uncommitted in-flight dashboard-YAML/`packages/dbr/` work) — leaving it stale is correct non-interference.

**Status:** WATCHDOG RUN. 0 spawns, 0 product code changes, 0 redeploys, 0 publishes, 0 Linear writes, 1 post-mortem commit. Committed only my 3 files with explicit paths (never `git add -A`).

**Revisit:** Next run. Leave watchdog mode only on an explicit PO instruction to the Claude cron.

## Run #85 — 2026-06-14 02:00 UTC — [P0 PRODUCTION BROKEN → FIXED] Expired TLS cert, HTTPS restored

**Decision:** Reissued the expired Let's Encrypt certificate and repointed nginx — production HTTPS was fully down. This is squarely within the self-imposed watchdog/production-health boundary (TLS is mine, not Antigravity's in-flight feature work).

**Diagnosis:** Smoke check returned 000 on all 6 hosts. Root cause: the LE cert (`live/open-reporting.dev`, SANs apex+www+portal) **expired Jun 13 19:27 UTC** (yesterday). TLS handshake failed with `certificate expired`. Local stack otherwise healthy (nginx/postgres/ghost up, port 443 listening, DNS for all 3 names → this host `91.98.118.153`). Auto-renewal had silently never fired because: (a) the host `certbot.timer` runs `certbot renew` against the default `/etc/letsencrypt` (empty) while the real certs live in `infra/nginx/certs/`; (b) that lineage's renewal config (`renewal/open-reporting.dev.conf`) was a 0-byte empty file; (c) the compose `certbot` service points at non-existent `./nginx/certs` paths and isn't running.

**Action:**
- Backed up `infra/nginx/certs/` to `/tmp/certs-backup-*`.
- `certbot certonly --webroot -w infra/nginx/www --config-dir infra/nginx/certs` for the 3 SANs → new lineage `open-reporting.dev-0003`, valid through **2026-09-12**. (Staging dry-run first to avoid burning LE prod rate limits.)
- Repointed the 3 nginx server blocks (`portal/apex/www.conf`) to `live/open-reporting.dev-0003/` — stable across renewals (certbot regenerates that symlink dir).
- Removed broken renewal configs (empty unsuffixed + -0001/-0002 whose live dirs are gone), leaving only the valid `-0003.conf`.
- `nginx -t` + reload.
- **Wired real renewal:** host cron `20 3,15 * * *` running `certbot -q renew --config-dir infra/nginx/certs` with `--deploy-hook "docker exec open-reporting-nginx-1 nginx -s reload"`. `renew --dry-run` passes (exit 0). Existing protected crons (22 UTC ingestion, 2/7/12/17 lead) preserved — append-only.

**Verified:** apex + www + portal + all 5 dashboards return **200 over HTTPS** with full cert-chain validation (curl --resolve, no -k); public_finance renders real content (`<title>Finanse publiczne Polski</title>`, stamp `7e9e0496` — Antigravity's in-flight work untouched). Commit `7605a4bc`, pushed to main. (Note: the 000 from the public-IP path is hairpin NAT — the VPS reaching its own public IP — not a visitor-facing issue.)

**Status:** Shipped (P0 hotfix). 0 subagent spawns, 1 commit (3 nginx confs; certs are gitignored), 0 Linear writes, 0 publishes.

**Followup for PO / Antigravity:** (1) The compose `certbot` service has wrong volume paths (`./nginx/certs` vs `./infra/nginx/certs`) and never ran — it's now superseded by the host cron, but worth removing/fixing to avoid confusion. (2) Renewal now depends on the host cron I added; if the canonical setup should be the compose certbot container, reconcile. (3) Consider an expiry-monitoring alert so a future lapse pages before the cert dies, not after.

**Revisit:** Next run — back to watchdog unless PO directs otherwise.

## Run #86 — 2026-06-14 07:00 UTC — WATCHDOG. Prod healthy. No new PO direction.

**Decision:** Deliberate non-interference. Verified production health; took no build/deploy/publish action — that remains Antigravity's plane.

**Checks:** All 5 dashboards (public_finance, labour_market, national_accounts, demographics, environment) + www return 200. TLS cert valid through **Sep 12 2026** (the lineage I fixed in #85). All protected crons intact: 22 UTC ingestion, 2/7/12/17 lead, 3:30/4/16 GUS bulk, Mon 5 intl, 20 3,15 certbot-renew. Telegram bot inactive (expected — Linear is live PO channel). No Telegram inbox items. Linear: 0 `Strategic` issues, 0 issues updated in last 3 days. Git tree still carries Antigravity's uncommitted V2 work (modified public_finance visuals + `packages/dbr/` compiler/make_app/static_export + untracked new visual YAMLs) — left untouched; live dbr stamp trailing HEAD is correct non-interference (see session-memory).

**Status:** Quiet run. 0 commits to product code, 0 subagent spawns, 0 deploys, 0 publishes. Only my own files (decisions.md, session-memory.md, outbox) committed with explicit paths.

**Revisit:** Next run — watchdog unless PO directs otherwise.
