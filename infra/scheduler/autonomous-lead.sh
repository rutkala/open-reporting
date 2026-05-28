#!/usr/bin/env bash
# Autonomous Lead — fires Claude Code with the lead-protocol prompt.
#
# Invoked by radek's user crontab at 02/07/12/17 UTC. Replaces the
# previously-used cloud RemoteTrigger, which could not reach the VPS to
# deploy what it built (dashboards, dbt models, ingestion). This wrapper
# runs ON the VPS where dbt/dbr/systemctl/docker are all available, so the
# agent can ship complete work — code AND deploy — in a single run.
#
# Permission mode: bypass (set globally in ~/.claude/settings.json). No
# prompts will appear. The Never list inside the prompt is the only guard.
#
# Logs to data/logs/autonomous-lead-YYYY-MM-DD-HH.log with one file per
# run. Wall-clock cap 75 min matches the prompt's own hard-stop.
#
# Linear: covers all autonomous OR work.

set -uo pipefail

REPO=/opt/open-reporting
export HOME=/home/radek
export PATH=/home/radek/.local/bin:/usr/local/bin:/usr/bin:/bin
export PYTHONPATH=$REPO

cd "$REPO"

LOG_DIR=$REPO/data/logs
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/autonomous-lead-$(date -u +%Y-%m-%d-%H).log"

ts() { date -u +'%Y-%m-%dT%H:%M:%SZ'; }
log() { echo "[$(ts)] $*" | tee -a "$LOG"; }

log "=== autonomous-lead run start ==="
log "host: $(hostname)  user: $(whoami)  claude: $(claude --version 2>&1 | head -1)"

# Ensure local main matches origin before the agent reads state.
log "git pull --ff-only"
git pull --ff-only origin main >>"$LOG" 2>&1 || log "WARN: git pull failed (continuing — agent will retry)"

PROMPT_FILE="$REPO/infra/scheduler/lead-protocol-prompt.md"
if [[ ! -f "$PROMPT_FILE" ]]; then
  log "FATAL: prompt file missing: $PROMPT_FILE"
  exit 2
fi

log "invoking claude -p (timeout 4500s) ..."
# 75-minute wall-clock cap matches the prompt's hard-stop.
# --model opus = primary lead model; agent delegates to Sonnet builders internally.
timeout 4500 claude -p --model opus < "$PROMPT_FILE" >>"$LOG" 2>&1
rc=$?

log "=== autonomous-lead run end (exit=$rc) ==="
exit $rc
