#!/usr/bin/env node
/**
 * Agent activity logger — visualises the Lead → Delegate → Report flow
 *
 * UNIVERSAL — works on any project. Agent names/colors auto-adapt.
 *
 * Writes TWO formats:
 *   1. agent-activity.log  — plain text for terminal (tail -f)
 *   2. agent-activity.jsonl — structured JSON for the web UI dashboard
 *
 * Called two ways (set in settings.local.json):
 *   PreToolUse:Agent → "node .claude/hooks/log-subagent.js pre"
 *   SubagentStop     → "node .claude/hooks/log-subagent.js stop"
 */
const fs   = require('fs');
const path = require('path');

const event = process.argv[2]; // "pre" or "stop"

// Default model mapping — add your custom agents here
const DEFAULT_MODELS = {
  'dashboard-dev':  'sonnet',
  'data-engineer':  'sonnet',
  'debug':          'sonnet',
  'Explore':        'sonnet',
  'Plan':           'sonnet',
  'general-purpose':'sonnet',
};

// Color mapping — add your custom agents here
const AGENT_COLORS = {
  'dashboard-dev':  '#10b981',
  'data-engineer':  '#3b82f6',
  'debug':          '#a855f7',
  'Explore':        '#6b7280',
  'Plan':           '#ec4899',
  'general-purpose':'#6b7280',
};

function timestamp() {
  return new Date().toLocaleTimeString('en-GB', { hour12: false });
}

function formatDuration(ms) {
  if (ms < 1000) return `${ms}ms`;
  const sec = Math.round(ms / 1000);
  if (sec < 60) return `${sec}s`;
  const min = Math.floor(sec / 60);
  const remSec = sec % 60;
  return remSec > 0 ? `${min}m ${remSec}s` : `${min}m`;
}

function padRight(str, width) {
  return str.length >= width ? str.substring(0, width) : str + ' '.repeat(width - str.length);
}

function truncate(str, max) {
  const clean = (str || '').replace(/\n/g, ' ').replace(/\s+/g, ' ').trim();
  return clean.length > max ? clean.substring(0, max) + '…' : clean;
}

const SEP = '  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─';

let input = '';
process.stdin.on('data', chunk => (input += chunk));
process.stdin.on('end', () => {
  try {
    const data       = JSON.parse(input || '{}');
    const cwd        = data.cwd || process.cwd();
    const logFile    = path.join(cwd, '.claude', 'agent-activity.log');
    const jsonlFile  = path.join(cwd, '.claude', 'agent-activity.jsonl');
    const timersDir  = path.join(cwd, '.claude', '.agent-timers');

    const time = timestamp();
    const now  = new Date().toISOString();

    if (event === 'pre') {
      const agentType  = data.tool_input?.subagent_type || data.tool_input?.type || 'system';
      const model      = data.tool_input?.model || DEFAULT_MODELS[agentType] || '?';
      const color      = AGENT_COLORS[agentType] || '#6b7280';
      const description = (data.tool_input?.description || '').replace(/\n/g, ' ').trim();
      const prompt      = (data.tool_input?.prompt || '').replace(/\n/g, ' ').trim();
      const task        = description || prompt.substring(0, 200) || '';

      // ── Plain text log ──
      const taskShort = truncate(task, 80);
      const agentCol  = padRight(`${agentType} · ${model}`, 22);
      fs.appendFileSync(logFile, `  ${time}  │  ▶ DELEGATE  │  ${agentCol}│  ${taskShort}\n`);

      // ── JSON log ──
      const entry = {
        type: 'delegate',
        time: now,
        timeShort: time,
        agent: agentType,
        model,
        color,
        task,
        id: `${agentType}-${Date.now()}`
      };
      fs.appendFileSync(jsonlFile, JSON.stringify(entry) + '\n');

      // ── Timer ──
      if (!fs.existsSync(timersDir)) {
        fs.mkdirSync(timersDir, { recursive: true });
      }
      fs.writeFileSync(
        path.join(timersDir, `${agentType}-${Date.now()}.json`),
        JSON.stringify({ start: Date.now(), model })
      );

    } else if (event === 'stop') {
      const agentType = data.agent_type || '';
      // Skip non-subagent stop events (session-end analysis has no agent_type)
      if (!agentType) { process.exit(0); }
      const color     = AGENT_COLORS[agentType] || '#6b7280';

      let durationStr = '';
      let durationMs  = 0;
      let model       = DEFAULT_MODELS[agentType] || '?';

      if (fs.existsSync(timersDir)) {
        const timerFiles = fs.readdirSync(timersDir)
          .filter(f => f.startsWith(agentType + '-'))
          .sort().reverse();

        if (timerFiles.length > 0) {
          const timerFile = path.join(timersDir, timerFiles[0]);
          try {
            const timerData = JSON.parse(fs.readFileSync(timerFile, 'utf8'));
            if (timerData.start) {
              durationMs  = Date.now() - timerData.start;
              durationStr = formatDuration(durationMs);
            }
            if (timerData.model) model = timerData.model;
          } catch (e) {
            const startMs = parseInt(fs.readFileSync(timerFile, 'utf8').trim());
            if (!isNaN(startMs)) {
              durationMs  = Date.now() - startMs;
              durationStr = formatDuration(durationMs);
            }
          }
          fs.unlinkSync(timerFile);
        }
      }

      const fullResult = (data.last_assistant_message || '').replace(/\n/g, ' ').replace(/\s+/g, ' ').trim();
      const summaryShort = truncate(fullResult, 120);

      // ── Plain text log ──
      const agentCol = padRight(`${agentType} · ${model}`, 22);
      let parts = [];
      if (durationStr) parts.push(`⏱ ${durationStr}`);
      if (summaryShort) parts.push(summaryShort);
      fs.appendFileSync(logFile, `  ${time}  │  ✓ REPORT    │  ${agentCol}│  ${parts.join('  ·  ')}\n`);
      fs.appendFileSync(logFile, SEP + '\n');

      // ── JSON log ──
      const entry = {
        type: 'report',
        time: now,
        timeShort: time,
        agent: agentType,
        model,
        color,
        durationMs,
        duration: durationStr,
        result: fullResult.substring(0, 500),
        id: `${agentType}-${Date.now()}`
      };
      fs.appendFileSync(jsonlFile, JSON.stringify(entry) + '\n');
    }
  } catch (e) {
    try {
      const errLog = path.join(data?.cwd || process.cwd(), '.claude', '.hook-errors.log');
      fs.appendFileSync(errLog, `[${new Date().toISOString()}] ${event}: ${e.message}\n${e.stack}\n\n`);
    } catch (_) {}
  }
});
