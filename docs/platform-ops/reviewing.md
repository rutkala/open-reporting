# Ops Review Rules

**Derived from:** `docs/platform-ops/principles.md` ✓ (KB complete — Docker Compose production, nginx security, systemd hygiene, TLS lifecycle, security posture, observability, backup & recovery)
**Used by:** `.claude/agents/ops-reviewer.md`
**Does NOT cover:** application-level code quality (see `evaluation/code-review.md`), data pipeline correctness (see `evaluation/data-engineering-review.md`), analytical soundness (see `evaluation/analytical-review.md`)

Rules applied by the `ops-reviewer` agent on infrastructure changes produced by the `ops-engineer` agent. Changes are reviewed before deployment. The goal is to catch security misconfigurations, reliability risks, and missing rollback paths before they affect the live platform.

---

## P1 — Blocks Deployment

### Security

- **Secrets in config or diff** — any API key, password, token, private key, or DSN appearing in `docker-compose.yml`, nginx config, systemd units, or any version-controlled file. Secrets must come from environment variables, Docker secrets, or a secrets manager.
- **New publicly exposed port without justification** — any port added to the `ports:` section of a Docker Compose service that is not 80, 443, or 22 (SSH). Internal services (postgres, ghost, dash apps) must not be exposed to the host.
- **`privileged: true` in Docker Compose** — grants full host access to the container. Equivalent to root on the host.
- **Docker socket mounted into application container** — `/var/run/docker.sock` mounted into any container other than a dedicated CI/CD or management container.
- **TLS version below 1.2** — `ssl_protocols` directive including SSLv3, TLSv1, or TLSv1.1.
- **Password-based SSH authentication enabled** — `PasswordAuthentication yes` in sshd_config.

### Nginx

- **HTTP without HTTPS redirect** — a server block listening on port 80 that serves content instead of redirecting to HTTPS.
- **Missing security headers on a public server block** — any of: `Strict-Transport-Security`, `X-Content-Type-Options`, `X-Frame-Options` absent from a server block serving public content.

### Rollback

- **No rollback path** — the change modifies production state (database schema, certificate, config) without a documented and tested rollback command.

---

## P2 — Should Fix Before Deployment

### Docker Compose

- **Image tag is `latest` or unpinned** — `image: postgres` without a version tag. Must be `image: postgres:16-alpine` or equivalent.
- **No restart policy** — service lacks `restart:` directive. Production services need `restart: unless-stopped` or `restart: on-failure`.
- **No resource limits** — service lacks `deploy.resources.limits` for memory or CPU. Runaway containers can starve the host.
- **Internal service on host network** — service uses `network_mode: host` when a custom Docker network would suffice.

### Nginx

- **No rate limiting on public endpoints** — `limit_req_zone` not configured for API or login endpoints.
- **`autoindex on;`** — directory listing enabled. Should be `off` (default).
- **Missing `server_name`** — server block without explicit `server_name`; catches all unmatched requests.
- **Upstream without `proxy_set_header Host`** — backend receives wrong host header.

### Systemd

- **`Restart=always`** — restarts even on clean exit (exit code 0). Should be `on-failure`.
- **No `RestartSec=`** — no delay between restart attempts; rapid crash loops consume resources.
- **Relative paths in `ExecStart=`** — systemd does not inherit `$PATH`; must use absolute paths.

### TLS

- **`privkey.pem` permissions not 600** — private key readable by group or others.
- **No post-renewal hook for nginx reload** — Certbot renewal does not trigger `systemctl reload nginx`.

### Backup

- **New data asset without backup plan** — a new volume, database, or persistent store created without specifying how it is backed up and how often.

---

## P3 — Noted

- **No health check endpoint** — new service does not expose a `/health` or equivalent endpoint for monitoring.
- **No logging configuration** — service does not specify log driver or rotation policy.
- **Base image not minimal** — using `ubuntu` or `debian` full image where `-alpine` or `-slim` would suffice.
- **No monitoring alert configured** — new service not added to alerting triggers (service down, high memory, high error rate).
- **Certificate expiry not monitored** — no automated check for Let's Encrypt certificate expiration.

---

## What this standard does NOT cover

- Whether the application code running in the container is correct — that is `code-reviewer`'s scope.
- Whether the data pipeline produces correct results — that is `data-engineer-reviewer`'s scope.
- Whether the nginx config serves the right content to the right URL — that is a functional test, not a security review.
- Subjective preferences for config formatting or ordering — matters of style are not P1/P2/P3 findings.
