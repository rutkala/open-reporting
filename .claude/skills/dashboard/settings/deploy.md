# Deploy Settings

## What it is
The deployment configuration for a dashboard: systemd service unit, nginx route, and
portal registration. Each dashboard gets one of each.

---

## 1. systemd service unit

File path: `infra/systemd/or-TODO_DOMAIN.service`

```ini
[Unit]
Description=Open Reporting — TODO_DOMAIN dashboard
After=network.target

[Service]
Type=simple
User=radek
WorkingDirectory=/opt/open-reporting
Environment=PYTHONPATH=/opt/open-reporting
Environment=DUCKDB_PATH=/opt/open-reporting/data/warehouse.duckdb
ExecStart=/usr/bin/python3 products/dashboards/TODO_DOMAIN/app.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

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

## Rules
- Service name: `or-TODO_DOMAIN` — must match the `or-*` pattern (NOPASSWD sudo applies to it)
- Port in systemd and nginx must match `PORT` in `app.py`
- `requests_pathname_prefix` in `app.py` must match the nginx `location` and `proxy_pass` path
- After adding nginx route, always reload nginx — config changes are not picked up automatically
- Register in portal after the service is confirmed running (`systemctl status`)
