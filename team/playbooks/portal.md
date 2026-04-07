# Playbook: Portal and Mobile

Covers sub-products #5 (Portal frontend), #6 (Portal backend), #9 (Mobile frontend), #10 (Mobile backend).

Mobile shares the portal stack — mobile-specific constraints are noted where they differ.

## Recipe

### Sub-product #5 — Portal frontend

| Task | Competency | Builder | Evaluator | Standard |
|------|-----------|---------|-----------|----------|
| Design (IA, navigation, layout system) | UX / UI Design | `dashboard-dev` | `visual-screenshot-reviewer` | visualisation.md → visualization-image.md |
| Build (Dash routing, page composition, PWA shell) | Dashboard Development | `dashboard-dev` | `visualization-reviewer` | visualisation.md → visualization-diff.md |

### Sub-product #6 — Portal backend

| Task | Competency | Builder | Evaluator | Standard |
|------|-----------|---------|-----------|----------|
| Design (query layer architecture, data access patterns) | Data Architecture | `data-architect` *(gap — main Claude)* | `architecture-critic` | storage.md → architecture-review.md |
| Build (Python/DuckDB queries, lib/db.py, filter logic) | Data Engineering | `data-engineer` | `data-engineer-reviewer` | storage.md → data-engineering-review.md |

### Sub-product #9 — Mobile frontend

| Task | Competency | Builder | Evaluator | Standard |
|------|-----------|---------|-----------|----------|
| Design (mobile-first layout, touch targets, PWA manifest) | UX / UI Design | `dashboard-dev` | `visual-screenshot-reviewer` | visualisation.md → visualization-image.md |
| Build (responsive CSS, PWA manifest, service worker) | Dashboard Development | `dashboard-dev` | `visualization-reviewer` | visualisation.md → visualization-diff.md |

*Sub-product #10 (Mobile backend) — same recipe as #6. Shared stack.*

---

## Portal Architecture

### Directory layout

```
products/
  dashboards/{domain}/
    app.py          — Dash app (dynamic, served by systemd)
    static.py       — Static HTML generator
  visuals/
    lib/
      db.py         — DuckDB query layer (all data access goes here)
      theme.py      — Nordic Plotly template (import to activate)
    components/     — Reusable chart/KPI components
    {domain}/       — Domain-specific components
```

### Data access rule

**All data access goes through `products/visuals/lib/db.py`.** Dashboard code never imports DuckDB directly. This is the backend layer — query functions here, called from dashboard code.

### Design system

The Nordic design system is defined in `products/visuals/lib/theme.py`. Import it in any script to activate the template. Never hardcode colours — always import from `theme.py`.

---

## Portal Frontend

### Information architecture

A portal page follows this structure (see `team/standards/build/visualisation.md`):

```
Header (logo, navigation)
Filter pane (left sidebar, 220px)
Main canvas (topic groups → chart cards)
Footer (source attribution, last updated)
```

**Navigation** — top-level nav links to each domain dashboard. Current: Labour, Explorer, Finance.

**Topic groups** — within a dashboard, related charts are grouped under a section heading with a grey background. Max 2 charts side by side per row.

**Chart cards** — white background, `border-radius: 6px`, subtle shadow. Every chart has a title.

### Building a new portal page

1. Create `products/dashboards/{domain}/app.py` using an existing domain as template
2. Register systemd unit: `infra/systemd/or-{domain}.service`
3. Add nginx location block: `infra/nginx/conf.d/or-portal.conf`
4. Use `products/visuals/lib/db.py` for all data queries
5. Import `products/visuals.lib.theme` to activate Nordic template
6. All user-facing text in Polish

### Development command

```bash
PYTHONPATH=/opt/open-reporting python3 products/dashboards/{domain}/app.py
# serves on port 8050–8053 (pick next available)
```

---

## Portal Backend (query layer)

### Query layer rules

- All queries live in `products/visuals/lib/db.py`
- Use parameterised queries — never string concatenation in SQL
- Query the gold mart (`curated.mart_{domain}`) — never raw or silver
- DuckDB connection via `data/warehouse.duckdb` — read via `DUCKDB_PATH` env var

### Adding a new query function

```python
def get_{domain}_{metric}(
    year: int | None = None,
    geo: str = "PL"
) -> pd.DataFrame:
    sql = """
        SELECT period_date, value, detail_name
        FROM curated.mart_{domain}
        WHERE geo = ?
          AND (? IS NULL OR YEAR(period_date) = ?)
        ORDER BY period_date
    """
    return query(sql, [geo, year, year])
```

---

## Mobile Frontend

Mobile is a PWA adaptation of the portal — same Dash stack, same data layer, mobile-first constraints:

- **Touch targets** — min 44×44px for interactive elements
- **Viewport** — `<meta name="viewport" content="width=device-width, initial-scale=1">`
- **PWA manifest** — `infra/nginx/html/manifest.json`
- **Offline** — service worker caches static assets; data queries require connectivity
- **Layout** — single column below 768px breakpoint; no side-by-side charts on mobile

Mobile-specific pages live in `products/mobile/`.

---

## Checklist

### Portal frontend
- [ ] Page structure matches Header / Filter / Canvas / Footer layout
- [ ] All charts have titles
- [ ] All charts belong to a topic group
- [ ] Nordic design system applied (theme.py imported)
- [ ] Polish language for all user-facing text
- [ ] Source attribution in footer
- [ ] Systemd unit registered and enabled
- [ ] Nginx location block added

### Portal backend
- [ ] All data access via `products/visuals/lib/db.py`
- [ ] Parameterised queries only (no string SQL)
- [ ] Queries gold mart, not silver or raw
- [ ] Query functions have explicit return types

### Mobile frontend
- [ ] Touch targets ≥ 44×44px
- [ ] Single-column layout on mobile viewport
- [ ] PWA manifest present
- [ ] No side-by-side charts below 768px
