# Cron jobs

User-level crontab entries for routine maintenance. These run as user `radek` on the VPS. Not tracked by git (crontab itself is system state), so this file is the source of truth — re-install from here if the host is rebuilt.

## Active jobs

| When (UTC) | Script | Purpose | Linear |
|-----------|--------|---------|--------|
| `0 22 * * *` daily | `/opt/open-reporting/products/ingestion/run_daily.sh` | NBP exchange rates + Eurostat observations refresh. Stops `or-public_finance.service` before, restarts after (DuckDB exclusive-lock workaround). Logs to `data/logs/ingest-daily-YYYY-MM-DD.log`. | OR-85 |

## Install / re-install

```bash
( crontab -l 2>/dev/null | grep -v "ingestion/run_daily.sh"; \
  echo "0 22 * * * /opt/open-reporting/products/ingestion/run_daily.sh" ) | crontab -
```

Verify:

```bash
crontab -l
```

## Why user crontab (not systemd timer)

The sudoers policy allows `cp /opt/open-reporting/infra/systemd/*.service /etc/systemd/system/` but NOT `*.timer` files — so systemd timers would require widening sudoers. User crontab needs no sudo and is sufficient for daily idempotent jobs.

The wrapper script DOES use `sudo systemctl stop|start or-public_finance.service` (allowed by sudoers `NOPASSWD: /usr/bin/systemctl {start,stop} or-*`) to release the DuckDB exclusive lock during ingestion.

## Known limitation: dashboard downtime during ingestion

DuckDB's embedded engine takes an exclusive lock on `data/warehouse.duckdb` when opened for writes. `dbr serve` (the live dashboard) holds the lock as long as it's running, blocking the daily ingestion. The wrapper currently stops the dashboard for the ingestion run (~9 minutes for the 56-dataset Eurostat pass) and restarts it after.

**Future improvement:** open the dashboard's DuckDB connection in read-only mode (DuckDB supports many concurrent readers + one writer in WAL mode). This would eliminate the daily downtime. Tracked as a follow-up dbr engine task — open as a Linear issue when next touching dbr internals.
