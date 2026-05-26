# Session Memory
<!-- auto-sync: true -->
<!-- last-updated: 2026-05-26 -->

## Current Focus

Quality-driven dashboard framework is **shipped + live**. Phase B/C/D loop closed with measurement: the `public_finance` dashboard at https://portal.open-reporting.dev/public_finance/ rebuilt against a 21-dimension rubric grounded in 8 multimodal reference sources. Rubric pass rate jumped from **~50% baseline → ~71% post-build**.

Next session: pick a real Linear issue and run `/composite_kickoff OR-XXX` to test the new orchestration loop end-to-end. That's the unproven thing.

## Major work since 2026-05-25 (commits on main)

- `26b6bfa4` — PR 1: team/ → docs/ topic-first reorg
- `60e1ed95` — Model-tiering policy + agent frontmatter
- `65fe21a0` — Multimodal capture recipe
- `fe762bdb` / `8c601a39` — Reference library (8 sources, 33+ images)
- `6bfc1954` — `docs/visualization/quality.md` 21-dimension rubric
- `d138011d` — Baseline gap analysis
- `e95649fc` / `99348e7f` / `960fcfbe` — Phase C primitives: `table:`, `annotations:`, `delta:`
- `d3db6da6` / `5ca4836e` / `5aacc4c8` — Phase C: `label_endpoints`, grey-accent `highlight`, row `title:`
- `dfaf739f` — Theme polarity tokens red/green → orange/blue
- `fab92fc2` — Row `prose:` Markdown narrative
- `a0f7e776` — Phase C primitives wired across all 5 pages
- `75fe817b` — Post-Phase-C gap analysis (+15 PASS)
- `0dab4f13` — Codex P1 fixes (scatter, SQL paths)
- `c79c3e1d` — **Merge PR #61** to main
- `9608e806` — Delete archived public_finance_phase_b
- `57de7ba1` — YAML closures (Poland labels, COVID/breach/inflection annotations)
- `cc4c34c3` — Codex P2 fix (line.py post-fetch slice)
- `e5afdd09` — Table column labels resolver
- `ee1a1e77` + `519110d5` — Phase D orchestration reshape: 10 agents + 8 skills
- `463863b7` — C.8 `dual_year` grouped bar primitive

## Architecture (current)

**Opus orchestrates, agents execute.** Per `docs/process/model-delegation.md`:
- Opus (me) = analyse, plan, orchestrate, integrate
- Sonnet builders = `dashboard-dev`, `data-engineer`, `content-writer`, `researcher`
- Mixed evaluators = `code-reviewer` (Sonnet), `architecture-critic`, `analytical-validator`, `domain-specialist` (Opus), `visual-screenshot-reviewer` (Sonnet)
- Utility = `debug` (Sonnet)

**Skills (8):** `composite_kickoff`, `composite_plan`, `composite_develop`, `composite_review`, `composite_review_ideas` (lifecycle); `composite_knowledge`, `composite_experience`, `_template` (framework).

## Key Technical Facts (unchanged)

- DuckDB: `data/warehouse.duckdb`
- PostgreSQL: `localhost:5432 db=reporting`
- Production deploy: `dbr run products/dashboards/<name>` → systemd `or-<name>.service` + nginx route + reload
- Visual reviewer is now **multimodal** — compares rendered screenshots against `docs/visualization/references/` using `docs/visualization/quality.md` as checklist

## Deferred (low-priority, not blocking)

- Grey-history primitive (needs design decision)
- Colorblind palette enforcement (preventive; C.7 already remapped actual red/green)
- Wave 3 reference captures (Tableau / IMF PDF / GUS detail)
- complex_dashboard skill recreation (retired in feat branch; recreate when starting a 2nd dashboard)
- Bar annotation y-axis can't take categorical string (schema relaxation when next needed)

## Linear — Active (per prior memory; verify before acting)

- OR-78 (Ghost admin), OR-85 (daily cron), OR-90 (Instagram token)
- OR-108 (Mobile-optimized dashboards), OR-120 (Public Finance domain KB), OR-129 (Domain Specialist agents)
- Product backlog: OR-74 to OR-113
