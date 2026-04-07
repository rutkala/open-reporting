# Knowledge Base: Platform Operations & Infrastructure

**Module:** `team/knowledge-base/platform-ops/ops.md`
**Version:** 1.0 — April 2026
**Status:** Ready for use

Agent reference for infrastructure operations — Docker Compose, nginx, systemd, TLS certificates, security hardening, observability — for Open Reporting's platform. Read before making any infrastructure change, and during ops review.

**Does not duplicate:** `data-engineering/engineering.md` (ELT, DuckDB, dbt patterns). This file covers the infrastructure layer: containers, reverse proxy, host services, certificates, and deployment.

**Sources:** Docker Compose production documentation (2025); Docker Security Best Practices (2026); CIS Docker Benchmark; Nginx CIS Benchmarks (SOCFortress, 2026); Mozilla SSL Configuration Generator (2026); systemd.service man page; Let's Encrypt / Certbot documentation; Hetzner Cloud documentation; OWASP Deployment Security Cheat Sheet; NIST SP 800-190 (Container Security Guide).

---

## 1. Docker Compose in Production

### 1.1 Service Definition Principles

| Principle | Rule | Rationale |
|-----------|------|-----------|
| **Explicit image tags** | Never use `latest`; pin to specific version (e.g., `nginx:1.27-alpine`) | Reproducibility; `latest` changes silently |
| **Restart policy** | Use `restart: unless-stopped` for production services | Services recover from crashes and host reboots |
| **Resource limits** | Set `deploy.resources.limits` (memory, CPU) for every service | Prevents runaway containers from starving the host |
| **Read-only filesystems** | Use `read_only: true` where possible; mount tmpfs for writable dirs | Reduces attack surface; containers should be immutable |
| **No privileged mode** | Never use `privileged: true` in production | Grants full host access; equivalent to root on the host |
| **Network isolation** | Use custom networks; only expose ports that must be public | Internal services (postgres, ghost) should not be reachable from outside |

### 1.2 Compose Lifecycle

| Operation | Command | When to use |
|-----------|---------|-------------|
| **Start** | `docker compose up -d` | Initial deployment or after config change |
| **Recreate single service** | `docker compose up -d --force-recreate <service>` | After changing only that service's config |
| **Stop all** | `docker compose stop` | Maintenance window; preserves containers |
| **Stop and remove** | `docker compose down` | Full teardown; removes containers and networks |
| **View logs** | `docker compose logs -f --tail=100 <service>` | Debugging; `--tail` prevents flooding |
| **Update image** | `docker compose pull <service> && docker compose up -d <service>` | Rolling update of a single service |

### 1.3 Secrets Management

- **Never** put secrets in `docker-compose.yml` — use environment variables or Docker secrets
- **`.env` files** are for local development only; production uses systemd environment files or a secrets manager
- **Database passwords, API tokens, TLS private keys** must never appear in version control
- **Rotate secrets** on a schedule: database passwords quarterly, API tokens per provider policy, TLS certificates per Let's Encrypt cycle (90 days)

### 1.4 Volume Management

| Volume type | Use for | Backup strategy |
|------------|---------|----------------|
| **Named volumes** | Database data (`postgres_data`), persistent state | `docker compose exec postgres pg_dump` → object storage |
| **Bind mounts** | Config files (`nginx.conf`), certificates | Version-controlled in repo; redeploy on change |
| **Tmpfs** | Temporary writable dirs in read-only containers | No backup needed; recreated on restart |

**Rule:** Database volumes must be backed up before any schema migration or Docker image update that touches the database container.

---

## 2. Nginx Reverse Proxy

### 2.1 Configuration Structure

```
infra/nginx/
├── nginx.conf              → Main config (worker_processes, events, http block)
├── conf.d/
│   ├── open-reporting.conf → Main site (portal, blog, API routes)
│   └── redirects.conf      → HTTP→HTTPS, www→non-www
├── certs/
│   ├── fullchain.pem       → Let's Encrypt certificate chain
│   └── privkey.pem         → Private key (600 permissions)
└── html/
    └── index.html          → Fallback / static pages
```

### 2.2 Security Headers (Required)

Every server block must include:

```nginx
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-Frame-Options "DENY" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Content-Security-Policy "default-src 'self'" always;
```

### 2.3 TLS Configuration

- **Minimum TLS version:** 1.2 (TLS 1.3 preferred)
- **Cipher suites:** Use Mozilla "Intermediate" profile as baseline
- **Certificate source:** Let's Encrypt via Certbot (90-day validity, auto-renew)
- **OCSP stapling:** Enabled for performance and privacy
- **HSTS:** Always enabled; preload list submission recommended

### 2.4 Health Checks

```nginx
location /health {
    access_log off;
    return 200 "ok\n";
    add_header Content-Type text/plain;
}
```

Every upstream service should have a health check endpoint. Nginx should proxy to it and log failures.

### 2.5 Common Misconfigurations

| Misconfiguration | Risk | Fix |
|-----------------|------|-----|
| `autoindex on;` | Directory listing exposes files | `autoindex off;` (default) |
| Missing `server_name` | Catches all unmatched requests; serves wrong content | Explicit `server_name` for each virtual host |
| No rate limiting | Brute force, scraping, DoS | `limit_req_zone` + `limit_req` in location blocks |
| Upstream without `proxy_set_header Host` | Backend receives wrong host header | Always pass `Host $host` |
| HTTP without redirect to HTTPS | Plaintext traffic accepted | 301 redirect from port 80 to 443 |

---

## 3. Systemd Service Management

### 3.1 Service Unit Structure

```ini
[Unit]
Description=Open Reporting - Labour Dashboard
After=docker.service
Requires=docker.service
Wants=network-online.target

[Service]
Type=simple
ExecStart=/usr/bin/docker compose -f /opt/open-reporting/docker-compose.yml up labour
ExecStop=/usr/bin/docker compose -f /opt/open-reporting/docker-compose.yml stop labour
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

### 3.2 Service Hygiene

- **`After=` and `Requires=`** — services that depend on Docker must declare it
- **`Restart=on-failure`** — automatic recovery from crashes; not `always` (which restarts even on clean exit)
- **`RestartSec=`** — delay between restart attempts; prevents rapid crash loops
- **`StandardOutput=journal`** — logs go to journald, not to files; enables `journalctl -u <service>`
- **No hardcoded paths** — use absolute paths in `ExecStart=`; systemd does not inherit `$PATH`
- **Resource limits** — `MemoryMax=`, `CPUQuota=` in `[Service]` section for isolation

### 3.3 Service Operations

| Operation | Command | Notes |
|-----------|---------|-------|
| **Start** | `systemctl start <service>` | Starts immediately |
| **Enable** | `systemctl enable <service>` | Starts on boot |
| **Status** | `systemctl status <service>` | Shows running state, recent logs |
| **Logs** | `journalctl -u <service> -f --no-pager` | Follow logs in real time |
| **Reload config** | `systemctl daemon-reload` | After editing `.service` files |
| **Restart** | `systemctl restart <service>` | Stop + start; brief downtime |

---

## 4. TLS Certificate Management

### 4.1 Let's Encrypt / Certbot Lifecycle

| Step | Action | Frequency |
|------|--------|-----------|
| **Initial issuance** | `certbot certonly --webroot -w /path/to/webroot -d domain.com` | Once per domain |
| **Renewal** | `certbot renew --dry-run` (test), `certbot renew` (actual) | Every 60 days (auto) |
| **Post-renewal hook** | `--deploy-hook "systemctl reload nginx"` | After each successful renewal |
| **Expiry monitoring** | Check `certbot certificates`; alert at 14 days | Weekly automated check |

### 4.2 Certificate Storage

- **Location:** `/etc/letsencrypt/live/<domain>/`
- **Permissions:** `privkey.pem` must be `600` (owner read/write only)
- **Symlinks:** Certbot manages symlinks from `live/` to `archive/`; never edit archive files directly
- **Backup:** Copy the entire `/etc/letsencrypt/` directory to secure storage

### 4.3 Certificate Rotation

When rotating certificates:
1. Run `certbot renew` (or issue new certificate)
2. Verify new certificate: `openssl x509 -in /etc/letsencrypt/live/<domain>/fullchain.pem -text -noout`
3. Reload nginx: `systemctl reload nginx` (zero-downtime)
4. Verify in browser or with `curl -vI https://<domain>`
5. **Never** stop nginx during rotation — `reload` is sufficient and safe

---

## 5. Security Posture

### 5.1 Host-Level Security

| Control | Requirement |
|---------|------------|
| **SSH** | Key-only authentication; no password auth; non-standard port optional |
| **Firewall** | Default-deny inbound; allow only 80, 443, 22 (SSH) |
| **Automatic updates** | `unattended-upgrades` enabled for security patches |
| **Fail2ban** | Enabled for SSH and nginx; bans after 5 failed attempts |
| **User accounts** | No root login; sudo with specific commands only |

### 5.2 Container Security

| Control | Requirement |
|---------|------------|
| **Non-root containers** | Run containers as non-root user where possible (`user: "1000:1000"`) |
| **Minimal base images** | Use `-alpine` or `-slim` variants; no full OS in containers |
| **No Docker socket mount** | Never mount `/var/run/docker.sock` into application containers |
| **Image scanning** | Check for known CVEs before updating images (`docker scout` or `trivy`) |
| **Network segmentation** | Internal services on separate Docker network; not exposed to host |

### 5.3 Exposed Ports Audit

| Port | Service | Exposure | Justification |
|------|---------|----------|---------------|
| 80 | nginx | Public | HTTP → HTTPS redirect |
| 443 | nginx | Public | HTTPS traffic |
| 22 | sshd | Public (restricted) | Remote administration |
| 5432 | postgres | Internal only | Database; must NOT be public |
| 2368 | ghost | Internal only | CMS; accessed via nginx proxy |
| 8050–8053 | Dash apps | Internal only | Accessed via nginx proxy |

**Rule:** Any port not in this table must not be exposed. Run `ss -tlnp` periodically to audit.

---

## 6. Observability & Monitoring

### 6.1 Logging Strategy

| Layer | Tool | Retention |
|-------|------|-----------|
| **Systemd services** | journald (`journalctl -u <service>`) | Per `SystemMaxUse=` in `journald.conf` |
| **Docker containers** | `docker compose logs` (stdout/stderr) | Per Docker daemon json-file config |
| **Nginx access logs** | `/var/log/nginx/access.log` | Rotated by logrotate; 30-day retention |
| **Nginx error logs** | `/var/log/nginx/error.log` | Rotated by logrotate; 90-day retention |
| **Application logs** | Python `logging` module → stdout | Captured by Docker; per container config |

### 6.2 Health Check Endpoints

Every service should respond to a health check:

| Service | Endpoint | Expected response |
|---------|----------|-------------------|
| **Nginx** | `/health` | `200 OK` with body "ok" |
| **Dash apps** | `/_health` | `200 OK` with JSON `{"status": "healthy"}` |
| **PostgreSQL** | `pg_isready` (CLI) | Exit code 0 |
| **Ghost** | `/ghost/api/v4/admin/site/` | `200 OK` (authenticated) |

### 6.3 Alerting Triggers

| Condition | Severity | Action |
|-----------|----------|--------|
| Service down (systemd exit) | Critical | Immediate notification; auto-restart via `Restart=on-failure` |
| TLS certificate expires in < 14 days | High | Notification; run `certbot renew` |
| Disk usage > 80% | High | Clean logs, prune Docker images |
| Memory usage > 90% | High | Identify process; consider scaling |
| Nginx 5xx rate > 1/min | Medium | Check upstream logs; restart affected service |

---

## 7. Deployment & Rollback

### 7.1 Deployment Checklist

Before deploying any infrastructure change:

- [ ] Change reviewed by `ops-reviewer` (or peer if reviewer unavailable)
- [ ] Backup of affected data (database dumps, config files)
- [ ] Rollback plan documented (what command reverses this change)
- [ ] Health check endpoints verified after deployment
- [ ] TLS certificates valid (if nginx config changed)
- [ ] No secrets in diff (`.env`, private keys, passwords)

### 7.2 Rollback Strategy

| Change type | Rollback method |
|------------|----------------|
| **Nginx config** | `git checkout HEAD -- infra/nginx/ && systemctl reload nginx` |
| **Docker Compose** | `git checkout HEAD -- docker-compose.yml && docker compose up -d` |
| **Systemd unit** | `git checkout HEAD -- infra/systemd/ && systemctl daemon-reload && systemctl restart <service>` |
| **TLS certificate** | Previous cert is in `/etc/letsencrypt/archive/`; restore symlink and reload nginx |
| **Database schema** | Restore from last backup dump; `psql < reporting < backup.sql` |

**Rule:** Every deployment must have a documented rollback command. If a change cannot be rolled back, it must not be deployed without a maintenance window.

### 7.3 Zero-Downtime Deployments

- **Nginx config changes:** `systemctl reload nginx` — graceful reload, no dropped connections
- **Docker service updates:** `docker compose up -d <service>` — replaces container; brief gap acceptable for internal services
- **Database migrations:** Run during low-traffic window; backward-compatible changes only (add columns, not drop)

---

## 8. Backup & Disaster Recovery

### 8.1 Backup Schedule

| Asset | Method | Frequency | Retention |
|-------|--------|-----------|-----------|
| **PostgreSQL** | `pg_dump` → compressed SQL | Daily | 30 days |
| **DuckDB warehouse** | File copy of `warehouse.duckdb` | Daily | 7 days |
| **Nginx config** | Git repo (version controlled) | On every change | Full history |
| **TLS certificates** | `/etc/letsencrypt/` directory copy | Weekly | 90 days |
| **Ghost content** | Ghost export (JSON) | Weekly | 30 days |
| **`.env` file** | Encrypted backup to separate location | On every change | Full history |

### 8.2 Recovery Procedure

1. **Identify the failure** — which service, which data, what is the impact
2. **Stop affected services** — prevent further corruption
3. **Restore from backup** — use the most recent valid backup
4. **Verify integrity** — run health checks, spot-check data
5. **Restart services** — in dependency order: postgres → DuckDB → nginx → apps
6. **Notify** — document the incident and resolution
