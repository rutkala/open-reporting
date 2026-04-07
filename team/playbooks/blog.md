# Playbook: Blog

Covers sub-products #7 (Blog frontend) and #8 (Blog backend).

## Recipe

### Sub-product #7 — Blog frontend

| Task | Competency | Builder | Evaluator | Standard |
|------|-----------|---------|-----------|----------|
| Design (Ghost theme, article layout, chart embeds) | UX / UI Design | `dashboard-dev` *(partial — no Ghost specialist)* | `visual-screenshot-reviewer` | visualisation.md → visualization-image.md |
| Build (Ghost Handlebars, CSS, chart integration) | *(gap — Ghost-specific, no dedicated agent)* | *(gap)* | *(gap)* | — |

### Sub-product #8 — Blog backend

| Task | Competency | Builder | Evaluator | Standard |
|------|-----------|---------|-----------|----------|
| Configure (Ghost CMS config, content API, webhooks) | Platform / Ops | `ops-engineer` | `ops-reviewer` | ops-review.md |
| Operate (Docker lifecycle, database backup, token refresh) | Platform / Ops | `ops-engineer` | `ops-reviewer` | ops-review.md |

**Note:** `ops-engineer` and `ops-reviewer` are live (OR-137). Ghost frontend (Handlebars templating, Ghost theme API) remains a gap — no dedicated agent. Blog frontend work is done by `dashboard-dev` with `visual-screenshot-reviewer` review.

---

## Blog Architecture

### Stack

- **CMS:** Ghost (running in Docker, accessible at `localhost:2368`)
- **Public URL:** `open-reporting.dev` (served via nginx reverse proxy)
- **Admin:** `open-reporting.dev/ghost` (Ghost admin panel)
- **Content API:** Ghost Content API (for reading published posts)
- **Database:** PostgreSQL via Docker (separate from analytics DuckDB)
- **Theme:** Custom Ghost theme (Handlebars templates)

### Directory layout

```
products/blog/          — Blog product code (theme, integrations)
infra/nginx/conf.d/     — nginx config includes Ghost proxy rules
docker-compose.yml      — Ghost service definition
```

### Services in Docker Compose

```yaml
ghost:
  image: ghost:5
  ports: ["2368:2368"]   # internal only — nginx proxies
  environment:
    url: https://open-reporting.dev
    database__client: mysql   # or sqlite for simple setup
```

---

## Blog Frontend

### Ghost theme development

A Ghost theme consists of:
- `index.hbs` — post list
- `post.hbs` — single article
- `page.hbs` — static pages
- `assets/` — CSS, JS, images
- `package.json` — theme metadata

**Chart embeds** — to embed a Plotly chart in an article:
1. Generate the chart as a standalone HTML div (no outer HTML, no inline JS)
2. Host the static HTML file at `infra/nginx/html/charts/{slug}.html`
3. Embed in Ghost via an HTML card: `<iframe src="https://portal.open-reporting.dev/charts/{slug}.html">`

### Design rules

Blog design follows the same Nordic minimal style as the portal:
- Typography: Inter font stack
- Colours: import from `products/visuals/lib/theme.py` palette where applicable
- Line length: max 680px for article body
- Responsive: mobile-first

---

## Blog Backend

### Ghost configuration

Key configuration in `docker-compose.yml` environment:

```yaml
url: https://open-reporting.dev          # public URL
database__client: sqlite3                # or mysql
mail__transport: Direct                  # or SMTP
```

### Content API

The Ghost Content API provides read access to published content. Use for:
- Generating article lists for embedding in portal
- Fetching article metadata for social card generation

```python
import requests
API_KEY = os.getenv("GHOST_CONTENT_API_KEY")
r = requests.get(
    "https://open-reporting.dev/ghost/api/content/posts/",
    params={"key": API_KEY, "limit": 5}
)
```

### Token / credential management

| Credential | Storage | Purpose |
|-----------|---------|---------|
| `GHOST_CONTENT_API_KEY` | `.env` | Read-only public API access |
| `GHOST_ADMIN_API_KEY` | `.env` | Admin operations (create posts, upload media) |
| Ghost admin password | Password manager | Human login to admin panel |

### Backup

Ghost content is stored in the PostgreSQL container. Backup via:
```bash
docker compose exec postgres pg_dump ghost > backups/ghost_$(date +%Y%m%d).sql
```

---

## Checklist

### Blog frontend
- [ ] Ghost theme validated in Ghost admin (Themes → Upload)
- [ ] Mobile responsive (check at 375px, 768px, 1280px)
- [ ] Article typography readable (line length, spacing)
- [ ] Chart embeds load correctly (iframes from portal.open-reporting.dev)
- [ ] Polish language throughout (no stray English in templates)

### Blog backend
- [ ] Ghost service running: `docker compose ps ghost`
- [ ] Public URL resolves: `curl -I https://open-reporting.dev`
- [ ] Admin accessible: `open-reporting.dev/ghost`
- [ ] Content API responds with published posts
- [ ] Database backup scheduled (or manual backup taken before upgrades)
