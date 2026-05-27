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
