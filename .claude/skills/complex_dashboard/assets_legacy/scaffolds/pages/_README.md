# `pages/` scaffolds

These templates only matter for **multi-page** dashboards
(`make_app(..., use_pages=True)` and `app_multipage.py.template`).
Single-page dashboards inline their layout in `app.py` and never
touch this folder.

## Workflow

1. Copy the relevant `.py.template` files into your dashboard:
   ```bash
   cp .claude/skills/complex_dashboard/assets/scaffolds/pages/overview.py.template \
      products/dashboards/<domain>/pages/overview.py
   cp .claude/skills/complex_dashboard/assets/scaffolds/pages/_section.py.template \
      products/dashboards/<domain>/pages/regional.py
   ```
2. Strip the `.template` suffix and replace every `TODO_*` placeholder.
3. Each page module must call `dash.register_page(__name__, path="/...")`
   and export a `layout` (either an `html.Div` or a callable returning one).
4. Delete this `_README.md` from your dashboard's copy — it is a
   skill-side note, not part of the dashboard.

## Conventions

- One file per page. Filename matches the URL slug
  (`pages/regional.py` → `/regional`).
- `path="/"` is reserved for the overview / landing page.
- Page layouts are wrapped automatically by Dash's Pages framework
  inside the shared `app.layout` defined in `app.py`. Do not include
  the sidebar / header / footer in a page module.
- Each page imports `MEASURES` and `DIMS` from the dashboard's own
  `measures.py`, and any `load_*` it needs from `data_loaders.py`.
