# Playbook: Platform Infrastructure

Covers sub-product #14 (Platform infra).

## Recipe

### Sub-product #14 — Platform infra

| Task | Competency | Builder | Evaluator | Standard |
|------|-----------|---------|-----------|----------|
| Design (service topology, security, backup strategy) | Platform / Ops | `ops-engineer` | `ops-reviewer` | ops-review.md |
| Build (Docker Compose, nginx, systemd, TLS, DNS, monitoring) | Platform / Ops | `ops-engineer` | `ops-reviewer` | ops-review.md |

**Note:** `ops-engineer` and `ops-reviewer` are live (OR-137).

---

## Infrastructure Overview

### Hosting

| Component | Details |
|-----------|---------|
| Provider | Hetzner Cloud |
| Server type | VPS (single server) |
| OS | Ubuntu 24.04 LTS |
| Public IP | Static (configured in DNS) |

### Running services

| Service | How it runs | Port | Purpose |
|---------|------------|------|---------|
| nginx | Docker Compose | 80, 443 | Reverse proxy, static file serving |
| PostgreSQL 16 | Docker Compose | 5432 (internal) | Ghost CMS database, operational store |
| Ghost | Docker Compose | 2368 (internal) | Blog CMS |
| Labour dashboard | systemd (`or-labour`) | 8050 | Dash app |
| Explorer dashboard | systemd (`or-explorer`) | 8051 | Dash app |
| Finance dashboard | systemd (`or-finance`) | 8053 | Dash app |
| Mobile app | systemd (`or-mobile`) | 8052 | Dash app |

### Directory layout

```
/opt/open-reporting/
  docker-compose.yml        — All Docker services (root, always)
  infra/
    nginx/
      conf.d/               — nginx server blocks
      html/                 — Static files served at portal.open-reporting.dev
      certs/                — TLS certificates (Let's Encrypt)
    systemd/                — Systemd service unit files
  .env                      — Secrets (never committed)
```

---

## Docker Compose

### Starting / stopping services

```bash
docker compose up -d                        # Start all services
docker compose ps                           # Check status
docker compose logs -f {service}            # Tail logs
docker compose down                         # Stop all (data persists in volumes)
docker compose up -d --force-recreate nginx # Reload nginx after config change
```

### Updating a service

```bash
docker compose pull {service}    # Pull latest image
docker compose up -d {service}   # Recreate container
```

---

## nginx

### Configuration structure

```
infra/nginx/conf.d/
  or-portal.conf      — Portal dashboards (proxy to systemd apps on 8050-8053)
  or-blog.conf        — Blog (proxy to Ghost on 2368)
  or-static.conf      — Static files (charts, social images)
```

### Applying config changes

```bash
# Validate config
docker compose exec nginx nginx -t

# Reload (no downtime)
docker compose exec nginx nginx -s reload

# Or force recreate
docker compose up -d --force-recreate nginx
```

### TLS / SSL

Certificates are managed by Let's Encrypt (Certbot). Renewal is automatic via cron.

```bash
# Manual renewal check
docker compose exec nginx certbot renew --dry-run
```

---

## systemd (Dash apps)

Each Dash app runs as a systemd service:

```bash
# Start / stop / status
sudo systemctl start or-labour
sudo systemctl stop or-labour
sudo systemctl status or-labour

# Restart after code change
sudo systemctl restart or-labour

# View logs
journalctl -u or-labour -f
```

### Deploying a new service unit

```bash
sudo cp infra/systemd/or-{domain}.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable or-{domain}
sudo systemctl start or-{domain}
```

### Service unit template

```ini
[Unit]
Description=Open Reporting — {Domain} dashboard
After=network.target

[Service]
Type=simple
User=radek
WorkingDirectory=/opt/open-reporting
Environment=PYTHONPATH=/opt/open-reporting
EnvironmentFile=/opt/open-reporting/.env
ExecStart=/usr/bin/python3 products/dashboards/{domain}/app.py
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

---

## DNS

DNS is managed externally (domain registrar). Key records:

| Record | Type | Points to |
|--------|------|-----------|
| `portal.open-reporting.dev` | A | VPS IP |
| `open-reporting.dev` | A | VPS IP |
| `www.open-reporting.dev` | CNAME | `open-reporting.dev` |

---

## Monitoring and observability

Currently manual. Planned improvements (tracked in Linear):
- Health check endpoint per Dash app
- Uptime monitoring (UptimeRobot or similar)
- Log aggregation
- Disk usage alerts

For now: check service status with `docker compose ps` and `sudo systemctl status or-*`.

---

## Backup

| What | How | Frequency |
|------|-----|-----------|
| DuckDB warehouse | `cp data/warehouse.duckdb backups/warehouse_$(date +%Y%m%d).duckdb` | Before major data changes |
| PostgreSQL (Ghost) | `docker compose exec postgres pg_dump ghost > backups/ghost_$(date +%Y%m%d).sql` | Before Ghost upgrades |
| nginx config | Git (already in repo) | On every change |
| .env | Manual copy to secure location | On every change |

---

## Checklist for infrastructure changes

- [ ] Config validated (`nginx -t`) before applying
- [ ] Change tested in dev before prod (where possible)
- [ ] Rollback path identified and documented
- [ ] No secrets in committed files (`.env` stays out of git)
- [ ] Exposed ports verified — only 80 and 443 publicly exposed
- [ ] Dash app ports (8050–8053) internal only (not in nginx exposed externally)
- [ ] Service restarts gracefully (no hard kills without reason)
- [ ] After applying: verify all services healthy (`docker compose ps` + `systemctl status or-*`)
