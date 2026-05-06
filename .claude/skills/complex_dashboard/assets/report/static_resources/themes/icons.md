# Icons

## What it is
SVG icon assets bundled with every dashboard. The skill ships its own
canonical icon set under `assets/report/static_resources/images/` — products copy from
the skill, not from another product.

## Directory structure (in the skill)
```
.claude/skills/complex_dashboard/assets/report/static_resources/
└── images/
    ├── logo.svg        ← Open Reporting wordmark (sidebar, collapsed: icon only)
    ├── sidebar.svg     ← Sidebar toggle button icon
    ├── settings.svg    ← Header settings button icon
    └── user.svg        ← Header user button icon
```

## Directory structure (in the dashboard product, after copy)
```
products/dashboards/TODO_DOMAIN/
└── assets/
    └── images/
        ├── logo.svg
        ├── sidebar.svg
        ├── settings.svg
        └── user.svg
```

Dash auto-serves from `products/dashboards/TODO_DOMAIN/assets/`, so the
SVGs must live there at runtime — they cannot be served from the skill
directory directly.

## Where each icon is used
| File | Component | `src` attribute |
|------|-----------|-----------------|
| `logo.svg` | Sidebar `html.A > html.Img` | `/TODO_DOMAIN/assets/images/logo.svg` |
| `sidebar.svg` | `btn-toggle` button | `/TODO_DOMAIN/assets/images/sidebar.svg` |
| `settings.svg` | `btn-settings` in header | `/TODO_DOMAIN/assets/images/settings.svg` |
| `user.svg` | `btn-user` in header | `/TODO_DOMAIN/assets/images/user.svg` |

## Setup
Copy the canonical icon set from the skill:
```bash
mkdir -p products/dashboards/TODO_DOMAIN/assets/images
cp .claude/skills/complex_dashboard/assets/report/static_resources/images/*.svg \
   products/dashboards/TODO_DOMAIN/assets/images/
```

## src path convention
All `src` paths use the dashboard's URL prefix: `/TODO_DOMAIN/assets/images/FILENAME.svg`

This must match the `requests_pathname_prefix` in `app.py` (`/TODO_DOMAIN/`).

## Rules
- Never reference icons with relative paths or absolute filesystem paths
- `logo.svg`: shown full-width when sidebar is expanded; hidden when collapsed (via toggle callback)
- `sidebar.svg`: always visible — it is the only element visible in the collapsed sidebar strip
- `settings.svg` and `user.svg`: always present in the header — no callbacks required by default
