# Deploy Settings

## What it is
The deployment configuration for a dashboard: systemd service unit, nginx route, and
portal registration. Each dashboard gets one of each.

---

## 1. systemd service unit

File path: `infra/systemd/or-TODO_DOMAIN.service`

```ini
[Unit]
Description=Open Reporting — TODO_DOMAIN dashboard (/TODO_DOMAIN/)
After=network.target

[Service]
WorkingDirectory=/opt/open-reporting
Environment=PYTHONPATH=/opt/open-reporting:/opt/open-reporting/.claude/skills
Environment=DUCKDB_PATH=/opt/open-reporting/data/warehouse.duckdb
EnvironmentFile=/opt/open-reporting/.env
ExecStart=/usr/bin/python3 products/dashboards/TODO_DOMAIN/app.py
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Matches the shape of the running units — `infra/systemd/or-template.service`,
`or-labour.service`, `or-explorer.service`, `or-finance.service`. Notes:

- No `Type=` — `simple` is the systemd default
- No `User=` — units run as root (matches the existing fleet)
- `Restart=on-failure`, not `always` — manual `systemctl stop` should not be reverted
- `EnvironmentFile=/opt/open-reporting/.env` — picks up DB credentials and Ghost tokens
- `PYTHONPATH` includes `/opt/open-reporting/.claude/skills` so the dashboard can
  import `complex_dashboard.assets.*` helpers (the existing fleet predates the skill
  and omits this entry; new dashboards built on the skill require it)

Deploy:
```bash
sudo cp infra/systemd/or-TODO_DOMAIN.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable or-TODO_DOMAIN
sudo systemctl start or-TODO_DOMAIN
sudo systemctl status or-TODO_DOMAIN
```

---

## 2. nginx route

Add to `infra/nginx/conf.d/dashboards.conf` (inside the `server` block):

```nginx
location /TODO_DOMAIN/ {
    proxy_pass         http://127.0.0.1:TODO_PORT/TODO_DOMAIN/;
    proxy_http_version 1.1;
    proxy_set_header   Upgrade $http_upgrade;
    proxy_set_header   Connection "upgrade";
    proxy_set_header   Host $host;
    proxy_cache_bypass $http_upgrade;
}
```

Reload nginx after editing:
```bash
sudo docker compose up -d --force-recreate nginx
```

---

## 3. Portal registration

Add to `products/portal/index.html` (or via Ghost CMS admin) so the dashboard appears
on the portal landing page.

```html
<a href="/TODO_DOMAIN/" class="portal-card">
    <h3>TODO: Dashboard title (Polish)</h3>
    <p>TODO: One-line description of what the dashboard shows (Polish)</p>
</a>
```

---

## 4. Local dev launcher (optional)

For iteration during development, drop a `start.sh` next to the dashboard:

```bash
#!/bin/bash
cd /opt/open-reporting
pkill -f "TODO_DOMAIN/app.py" 2>/dev/null
sleep 1
PYTHONPATH=/opt/open-reporting:/opt/open-reporting/.claude/skills \
DUCKDB_PATH=/opt/open-reporting/data/warehouse.duckdb \
python3 products/dashboards/TODO_DOMAIN/app.py > /tmp/TODO_DOMAIN-dashboard.log 2>&1 &
disown
echo "Dashboard started, PID: $!"
```

```bash
chmod +x products/dashboards/TODO_DOMAIN/start.sh
products/dashboards/TODO_DOMAIN/start.sh
tail -f /tmp/TODO_DOMAIN-dashboard.log
```

Mirrors `products/dashboards/template/start.sh`. Use only for local
iteration — production runs through systemd.

---

## Rules
- Service name: `or-TODO_DOMAIN` — must match the `or-*` pattern (NOPASSWD sudo applies to it)
- Port in systemd and nginx must match `PORT` in `app.py`
- `PYTHONPATH` must include **both** `/opt/open-reporting` and `/opt/open-reporting/.claude/skills` — the second entry lets the dashboard import `complex_dashboard.assets.layout.styles`, `complex_dashboard.assets.settings.app_init`, etc.
- `domain=` argument to `make_app(...)` must match the nginx `location` and `proxy_pass` path
- After adding nginx route, always reload nginx — config changes are not picked up automatically
- Register in portal after the service is confirmed running (`systemctl status`)
- `EnvironmentFile=/opt/open-reporting/.env` — required for any unit that touches PostgreSQL or Ghost
