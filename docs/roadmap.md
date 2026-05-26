# Roadmap — Strategic Priorities

**Linear** is the canonical backlog at https://linear.app/open-reporting/. This file is the strategic prioritisation overlay on top of it — what I'm focusing on and why.

**Owned by:** AI Lead (autonomous; see `docs/process/lead-protocol.md`).
**PO override:** edit this file directly — I read on next session and adapt.

---

## Current state (2026-05-26)

**Factory built:**
- `dbr` engine has the primitives needed for high-quality dashboards (8 of 10 from Phase C shipped; dim 13 closed with `dual_year`)
- 21-dimension `docs/visualization/quality.md` rubric with 8 multimodal reference sources
- Orchestration: 10 agents (4 Sonnet builders + 5 evaluators + 1 utility), 7 lifecycle skills
- `public_finance` dashboard live + passes ~71% of the rubric

**Factory under-used:**
- One live dashboard (public_finance); 17 enumerated domain dashboards in backlog
- Ghost blog operational but **no articles published**
- Instagram token **OVERDUE since 2026-05-20** — publishing has stopped
- Data pipeline partial (some sources manual)

**The strategic gap:** I've built a factory that can produce many products and shipped one. The next 4-6 weeks are about USING the factory at the rate it's capable of.

---

## Four themes, next 4-6 weeks

### Theme 1 — Stabilise the basics (Week 1)

Blockers + overdue items. Cannot defer.

| # | Linear | Why |
|---|--------|-----|
| 1 | **OR-90** Instagram token refresh | OVERDUE — Instagram publishing stopped. **Requires PO action** in Meta Developer portal; I cannot refresh tokens for someone else's Meta account. Flagged in decisions.md. |
| 2 | OR-78 Ghost admin setup | Blocks all content publishing (Theme 2) |
| 3 | OR-85 Automate daily ingestion cron | Data freshness foundation; enables Theme 3 |

### Theme 2 — Activate content channel (Weeks 1-2)

Ghost is up but the blog is empty. The dashboard at `portal.open-reporting.dev/public_finance/` is genuinely interesting and a public-finance article almost writes itself from the same data.

| # | Linear | Why |
|---|--------|-----|
| 4 | OR-74 Blog setup + theme + voice | Foundation; no point on next without this |
| 5 | OR-80 First data-driven article | Topic: "Polska wobec progów SGP/Maastricht — co mówią dane 1995-2024." Built directly from the public_finance data + rubric annotations. Linked back to the dashboard. |
| 6 | OR-79 "Portal" link in Ghost navigation | Connects content to dashboards (cross-traffic) |

### Theme 3 — Replicate to 2-3 more domains (Weeks 2-4)

The factory pattern works. Three more domains pick up the most differentiating signal in the Polish public-data market.

| # | Linear | Why |
|---|--------|-----|
| 7 | **OR-56** Labour Market dashboard | Most-asked Polish public topic; data ready in Eurostat + GUS; differentiating because Polish-language framing is rare |
| 8 | **OR-52** National Accounts & Macroeconomics | Pair with public_finance for full macro picture (GDP, investment, trade) |
| 9 | **OR-55** Population & Demographics | Long-arc public-interest topic; data deep + stable |

These three give: people work (labour), economy works (macro), and society works (demographics). Together with public_finance, that's a coherent "Polska w liczbach" core.

Deferred: the other 14 enumerated dashboards (OR-51, OR-53, OR-54, OR-57 through OR-68). Re-prioritise after the first 3 ship and we see usage signal.

### Theme 4 — Automate the social drumbeat (Weeks 3-5)

Distribution. Right now there's no automated rhythm. `/schedule` (cron) can run weekly autonomous loops that produce social posts from dashboard data.

| # | Linear | Why |
|---|--------|-----|
| 10 | OR-77 Social media automation Phase 1 | Foundation: post drafting, image generation, scheduled publish |
| 11 | OR-89 Weekly Economy Snapshot | First recurring autonomous loop; uses Theme 3 dashboards as data sources |

### Theme 5 — Data pipeline depth (parallel; week 3-6)

| # | Linear | Why |
|---|--------|-----|
| 12 | OR-76 Data pipeline Phase 1 | Robustness for the daily cron + retries + alerting |
| 13 | OR-86 BDL (GUS) ingestion | Unlocks regional / NUTS2 dashboards (future themes) |

---

## What I'm intentionally NOT doing

- **OR-110/111/112/113 Finance dashboard improvements** — `public_finance` already passes 71% of the rubric. Polishing it from 71% to 85% is lower-leverage than adding 3 new dashboards at 70%. Revisit in 6 weeks if usage signal says polish matters more than coverage.
- **The remaining 14 domain dashboards** (OR-51, 53, 54, 57-68) — defer. Three new domains first; expand if pattern holds.
- **OR-141 Product hierarchy clarification** — meta-work. Defer until there's friction. Currently the two-plane + topic-first docs structure works.
- **OR-129 Domain Specialist per-domain agents** — premature. Generic `domain-specialist` agent is fine; specialise only when a domain reveals it needs distinct judgment.
- **OR-108 Mobile-optimized dashboards** — defer until desktop usage signal is real. Mobile is a future bet, not a current need.
- **OR-69 Multi-Model AI Agent Team architecture work** — already resolved by Phase D reshape.
- **All OR-51 to OR-72 "OPE-*" issues** — legacy IDs from a prior architecture iteration. Will close as part of Linear hygiene.

---

## Cadence

- **Weekly autonomous** (Monday 09:00 Europe/Warsaw via `/schedule`): roadmap review → pick highest-priority unblocked item → kickoff → ship → decisions.md entry
- **Per-session**: I read this file + `docs/decisions.md` + `docs/session-memory.md` at start, integrate any PO edits, then work
- **Monthly**: re-evaluate themes, retire completed ones, raise new ones

---

## Themes I'd raise after Themes 1-5 land

(Not committed; written so the next strategic re-think has a starting point.)

- **A-1: Reader feedback loop** — instrument basic dashboard analytics, surface what readers actually look at
- **A-2: English version** — second-language audience expands reach (already noted in OR-91 dictionary)
- **A-3: Newsletter** — Ghost has subscription primitives; convert dashboard updates into a weekly email
- **A-4: Data-as-API** — surface curated datasets via a simple REST endpoint; researchers + journalists are the natural audience
- **A-5: Mobile** — only when desktop demand is proven
