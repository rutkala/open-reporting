#!/usr/bin/env node
/**
 * Agent Activity Monitor — Web Dashboard
 *
 * UNIVERSAL — works on any project. Zero dependencies, Node.js built-ins only.
 * Serves a single-page dashboard with real-time SSE updates.
 *
 * Features:
 *   - Real-time agent spawn/complete tracking via SSE
 *   - Lead agent (orchestrator) activity bar
 *   - Currently-working agents panel with live timers
 *   - Timeline with date filtering (Today / Yesterday / All)
 *   - Stat filtering (All / Active / Completed)
 *   - Auto-expire stale agents after 10 minutes
 *   - Click-to-expand result text
 *
 * Usage:
 *   node .claude/watch-agents-ui.js          → http://localhost:5555
 *   double-click .claude/watch-agents-ui.bat → opens browser automatically
 */
const http = require('http');
const fs   = require('fs');
const path = require('path');
const { exec } = require('child_process');

const PORT     = 5555;
const BASE_DIR = path.resolve(__dirname);
const JSONL    = path.join(BASE_DIR, 'agent-activity.jsonl');

// ── SSE clients ──
const clients = new Set();

// ── Watch JSONL for changes ──
let lastSize = 0;
try { lastSize = fs.statSync(JSONL).size; } catch (_) {}

function checkForNewEntries() {
  try {
    const stat = fs.statSync(JSONL);
    if (stat.size > lastSize) {
      const stream = fs.createReadStream(JSONL, { start: lastSize, encoding: 'utf8' });
      let buffer = '';
      stream.on('data', chunk => buffer += chunk);
      stream.on('end', () => {
        lastSize = stat.size;
        const lines = buffer.split('\n').filter(l => l.trim());
        for (const line of lines) {
          for (const client of clients) {
            client.write(`data: ${line}\n\n`);
          }
        }
      });
    }
  } catch (_) {}
}

setInterval(checkForNewEntries, 500);

function loadAllEntries() {
  try {
    const content = fs.readFileSync(JSONL, 'utf8');
    return content.split('\n').filter(l => l.trim());
  } catch (_) {
    return [];
  }
}

// ── HTTP Server ──
const server = http.createServer((req, res) => {
  if (req.url === '/events') {
    res.writeHead(200, {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
      'Access-Control-Allow-Origin': '*',
    });
    res.write(':ok\n\n');
    clients.add(res);
    req.on('close', () => clients.delete(res));
    return;
  }

  if (req.url === '/api/entries') {
    const entries = loadAllEntries();
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(entries.map(e => { try { return JSON.parse(e); } catch(_) { return null; } }).filter(Boolean)));
    return;
  }

  res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
  res.end(DASHBOARD_HTML);
});

server.listen(PORT, () => {
  console.log(`\n  ⚡ Agent Activity Monitor → http://localhost:${PORT}\n`);
  // Auto-open browser (Windows: start, macOS: open, Linux: xdg-open)
  const platform = process.platform;
  const cmd = platform === 'win32' ? 'start' : platform === 'darwin' ? 'open' : 'xdg-open';
  exec(`${cmd} http://localhost:${PORT}`);
});

// ── Dashboard HTML ──
// CUSTOMIZATION POINTS marked with {PROJECT_NAME} — search and replace
const DASHBOARD_HTML = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Agent Activity Monitor</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    background: #0f172a;
    color: #e2e8f0;
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    min-height: 100vh;
  }

  /* ── Header ── */
  .header {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    border-bottom: 1px solid #334155;
    padding: 16px 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 10;
  }

  .header-left { display: flex; align-items: center; gap: 16px; }

  .header h1 { font-size: 20px; font-weight: 600; color: #f8fafc; }
  .header h1 span { color: #f59e0b; }
  .header-sub { font-size: 13px; color: #94a3b8; margin-top: 2px; }

  .live-badge {
    display: flex; align-items: center; gap: 8px;
    background: #1e293b; border: 1px solid #334155;
    border-radius: 20px; padding: 6px 14px;
    font-size: 13px; color: #94a3b8;
  }

  .live-dot {
    width: 8px; height: 8px; background: #22c55e;
    border-radius: 50%; animation: pulse 2s ease-in-out infinite;
  }

  @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }

  /* ── Toolbar ── */
  .toolbar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 12px 32px; border-bottom: 1px solid #1e293b;
    background: #0f172a; position: sticky; top: 60px; z-index: 9;
  }

  .stats { display: flex; gap: 20px; }

  .stat {
    display: flex; align-items: center; gap: 6px; font-size: 13px; color: #94a3b8;
    cursor: pointer; padding: 6px 14px; border-radius: 8px;
    border: 1px solid transparent; transition: all 0.15s; user-select: none;
  }

  .stat:hover { background: #1e293b; border-color: #334155; }

  .stat.stat-active { background: #1e293b; border-color: #475569; }

  .stat-value { font-weight: 600; color: #e2e8f0; font-size: 18px; }

  .filters { display: flex; gap: 6px; }

  .filter-btn {
    background: #1e293b; border: 1px solid #334155; color: #94a3b8;
    padding: 6px 16px; border-radius: 8px; cursor: pointer;
    font-size: 13px; font-family: inherit; transition: all 0.15s;
  }

  .filter-btn:hover { border-color: #475569; color: #e2e8f0; }

  .filter-btn.active {
    background: #f59e0b; border-color: #f59e0b;
    color: #0f172a; font-weight: 600;
  }

  /* ── Currently Active section ── */
  .active-section {
    padding: 16px 32px;
    background: linear-gradient(180deg, #1a1a2e 0%, #0f172a 100%);
    border-bottom: 1px solid #1e293b;
    display: none;
  }

  .active-section.visible { display: block; }

  .active-section-title {
    font-size: 11px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 1.5px; color: #f59e0b; margin-bottom: 12px;
    display: flex; align-items: center; gap: 8px;
  }

  .active-grid {
    display: flex; flex-wrap: wrap; gap: 10px;
    max-width: 1200px; margin: 0 auto;
  }

  .active-card {
    background: #1e293b; border: 1px solid #f59e0b;
    border-radius: 10px; padding: 12px 16px;
    min-width: 280px; flex: 1; max-width: 400px;
    box-shadow: 0 0 16px rgba(245, 158, 11, 0.08);
    animation: fadeIn 0.3s ease;
  }

  @keyframes fadeIn { from { opacity: 0; transform: translateY(-8px); } to { opacity: 1; transform: translateY(0); } }

  .active-card-top {
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 6px;
  }

  .active-card-agent {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 3px 10px; border-radius: 5px;
    font-size: 12px; font-weight: 600; color: white;
  }

  .active-card-timer {
    font-family: 'Cascadia Code', 'Fira Code', monospace;
    font-size: 13px; color: #f59e0b; font-weight: 600;
  }

  .active-card-task {
    font-size: 13px; color: #cbd5e1; line-height: 1.4;
  }

  .active-card-spinner {
    display: inline-block; width: 12px; height: 12px;
    border: 2px solid rgba(245,158,11,0.3); border-top-color: #f59e0b;
    border-radius: 50%; animation: spin 0.8s linear infinite;
    margin-right: 4px; vertical-align: middle;
  }

  @keyframes spin { to { transform: rotate(360deg); } }

  /* ── Timeline ── */
  .timeline {
    padding: 20px 32px; display: flex; flex-direction: column;
    gap: 10px; max-width: 1200px; margin: 0 auto; width: 100%;
  }

  .empty-state {
    text-align: center; color: #64748b; padding: 80px 20px; font-size: 15px;
  }
  .empty-state .icon { font-size: 48px; margin-bottom: 16px; }

  .date-divider {
    display: flex; align-items: center; gap: 12px;
    margin: 16px 0 8px; color: #64748b; font-size: 12px;
    font-weight: 600; text-transform: uppercase; letter-spacing: 1px;
  }

  .date-divider::after {
    content: ''; flex: 1; height: 1px; background: #1e293b;
  }

  /* ── Agent card ── */
  .card {
    background: #1e293b; border: 1px solid #334155;
    border-radius: 10px; overflow: hidden;
    transition: all 0.2s; animation: fadeIn 0.3s ease;
  }

  .card:hover { border-color: #475569; }

  .card.active-card-timeline {
    border-color: #f59e0b;
    box-shadow: 0 0 16px rgba(245, 158, 11, 0.08);
  }

  .card.hidden { display: none; }

  .card-header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 12px 16px; gap: 12px;
  }

  .card-left { display: flex; align-items: center; gap: 10px; }

  .agent-badge {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 3px 10px; border-radius: 5px;
    font-size: 12px; font-weight: 600; color: white;
  }

  .model-tag {
    font-size: 10px; font-weight: 400; padding: 1px 6px;
    background: rgba(0,0,0,0.3); border-radius: 3px;
    color: rgba(255,255,255,0.8);
  }

  .card-time {
    font-size: 11px; color: #64748b;
    font-family: 'Cascadia Code', 'Fira Code', monospace;
  }

  .card-meta { display: flex; align-items: center; gap: 10px; }

  .duration-badge {
    display: inline-flex; align-items: center; gap: 4px;
    font-size: 11px; color: #94a3b8; background: #0f172a;
    padding: 2px 8px; border-radius: 4px;
  }

  .status-working {
    display: inline-flex; align-items: center; gap: 5px;
    font-size: 12px; color: #f59e0b; font-weight: 500;
  }

  .spinner {
    width: 12px; height: 12px;
    border: 2px solid rgba(245,158,11,0.3); border-top-color: #f59e0b;
    border-radius: 50%; animation: spin 0.8s linear infinite;
  }

  .status-done { font-size: 12px; color: #22c55e; font-weight: 500; }

  .card-body { padding: 0 16px 12px; }

  .task-text { font-size: 13px; color: #cbd5e1; margin-bottom: 6px; }

  .result-text {
    font-size: 12px; color: #94a3b8; background: #0f172a;
    border-radius: 6px; padding: 10px 12px; line-height: 1.5;
    max-height: 80px; overflow-y: auto; cursor: pointer;
    transition: max-height 0.3s ease;
  }

  .result-text.expanded { max-height: 600px; }

  .result-text::-webkit-scrollbar { width: 5px; }
  .result-text::-webkit-scrollbar-track { background: transparent; }
  .result-text::-webkit-scrollbar-thumb { background: #334155; border-radius: 3px; }

  .working-timer {
    font-family: 'Cascadia Code', 'Fira Code', monospace;
    font-size: 12px; color: #f59e0b;
  }

  /* -- Lead activity bar -- */
  .lead-bar {
    background: #1a2332;
    border-bottom: 1px solid #1e293b;
    padding: 8px 32px;
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 13px;
    color: #94a3b8;
    transition: opacity 0.5s ease;
    min-height: 38px;
  }

  .lead-bar.faded { opacity: 0.4; }

  .lead-action-icon {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    color: #f59e0b;
    font-weight: 600;
    font-size: 12px;
    white-space: nowrap;
  }

  .lead-action-icon .lead-dot {
    width: 6px; height: 6px;
    background: #f59e0b;
    border-radius: 50%;
    animation: pulse 1.5s ease-in-out infinite;
  }

  .lead-task {
    color: #cbd5e1;
    font-family: 'Cascadia Code', 'Fira Code', monospace;
    font-size: 12px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .lead-time {
    margin-left: auto;
    color: #475569;
    font-size: 11px;
    white-space: nowrap;
  }
</style>
</head>
<body>

<div class="header">
  <div class="header-left">
    <div>
      <h1><span>⚡</span> Agent Activity Monitor</h1>
      <div class="header-sub" id="lead-status">Lead Agent — <span style="color:#22c55e">working solo</span></div>
    </div>
  </div>
  <div class="live-badge">
    <div class="live-dot"></div>
    LIVE
  </div>
</div>

<div class="toolbar">
  <div class="stats">
    <div class="stat" data-stat="all" title="Show all delegations">
      <span>Delegations</span>
      <span class="stat-value" id="stat-total">0</span>
    </div>
    <div class="stat" data-stat="active" title="Show active only">
      <span>Active</span>
      <span class="stat-value" id="stat-active" style="color:#f59e0b">0</span>
    </div>
    <div class="stat" data-stat="completed" title="Show completed only">
      <span>Completed</span>
      <span class="stat-value" id="stat-done" style="color:#22c55e">0</span>
    </div>
  </div>
  <div class="filters">
    <button class="filter-btn active" data-filter="today">Today</button>
    <button class="filter-btn" data-filter="yesterday">Yesterday</button>
    <button class="filter-btn" data-filter="all">All</button>
  </div>
</div>

<div class="lead-bar faded" id="lead-bar">
  <span class="lead-action-icon"><span class="lead-dot"></span> LEAD</span>
  <span class="lead-task" id="lead-task">Waiting for activity...</span>
  <span class="lead-time" id="lead-time"></span>
</div>

<!-- Currently Active Agents -->
<div class="active-section" id="active-section">
  <div class="active-section-title">
    <span class="active-card-spinner"></span>
    Currently Working
  </div>
  <div class="active-grid" id="active-grid"></div>
</div>

<div class="timeline" id="timeline">
  <div class="empty-state" id="empty">
    <div class="icon">⚡</div>
    <div>Waiting for agent activity...</div>
    <div style="margin-top:8px;font-size:13px">Agents will appear here in real time when delegated</div>
  </div>
</div>

<script>
const timeline     = document.getElementById('timeline');
const empty        = document.getElementById('empty');
const activeSection = document.getElementById('active-section');
const activeGrid   = document.getElementById('active-grid');

const allEntries = [];
const activeAgents = new Map();
let currentFilter = 'today';
let currentStatFilter = 'all';
let agentCounter = 0;

// ── Date helpers ──
function toDateStr(isoStr) {
  return new Date(isoStr).toLocaleDateString('en-CA');
}

function todayStr() { return new Date().toLocaleDateString('en-CA'); }

function yesterdayStr() {
  const d = new Date(); d.setDate(d.getDate() - 1);
  return d.toLocaleDateString('en-CA');
}

function friendlyDate(dateStr) {
  const t = todayStr(), y = yesterdayStr();
  if (dateStr === t) return 'Today';
  if (dateStr === y) return 'Yesterday';
  return new Date(dateStr).toLocaleDateString('en-GB', { weekday: 'short', day: 'numeric', month: 'short' });
}

function matchesFilter(isoStr) {
  const d = toDateStr(isoStr);
  if (currentFilter === 'today') return d === todayStr();
  if (currentFilter === 'yesterday') return d === yesterdayStr();
  return true;
}

// ── Filter buttons ──
document.querySelectorAll('.filter-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    currentFilter = btn.dataset.filter;
    rebuildTimeline();
  });
});

// ── Stat filter clicks ──
document.querySelectorAll('.stat[data-stat]').forEach(stat => {
  stat.addEventListener('click', () => {
    const clicked = stat.dataset.stat;
    if (currentStatFilter === clicked) {
      currentStatFilter = 'all';
    } else {
      currentStatFilter = clicked;
    }
    document.querySelectorAll('.stat[data-stat]').forEach(s => s.classList.remove('stat-active'));
    if (currentStatFilter !== 'all') {
      stat.classList.add('stat-active');
    }
    rebuildTimeline();
  });
});

// ── Stats ──
function updateStats() {
  const allCards = timeline.querySelectorAll('.card');
  let totalCount = 0, activeCount = 0, doneCount = 0;
  allCards.forEach(c => {
    const t = c.dataset.time;
    if (t && matchesFilter(t)) {
      totalCount++;
      if (c.classList.contains('active-card-timeline')) activeCount++;
      else doneCount++;
    }
  });
  activeCount = Math.max(activeCount, activeAgents.size);
  totalCount = Math.max(totalCount, activeCount + doneCount);

  document.getElementById('stat-total').textContent  = totalCount;
  document.getElementById('stat-active').textContent = activeCount;
  document.getElementById('stat-done').textContent   = doneCount;
}

function formatMs(ms) {
  if (ms < 1000) return ms + 'ms';
  const sec = Math.round(ms / 1000);
  if (sec < 60) return sec + 's';
  const min = Math.floor(sec / 60);
  const rem = sec % 60;
  return rem > 0 ? min + 'm ' + rem + 's' : min + 'm';
}

function escapeHtml(str) {
  const d = document.createElement('div');
  d.textContent = str || '';
  return d.innerHTML;
}

// ── Active section ──
function updateActiveSection() {
  const leadStatus = document.getElementById('lead-status');
  if (activeAgents.size > 0) {
    activeSection.classList.add('visible');
    const names = [...activeAgents.values()].map(a => a.entry.agent).join(', ');
    leadStatus.innerHTML = 'Lead Agent — <span style="color:#f59e0b">delegating to ' + names + '</span>';
  } else {
    activeSection.classList.remove('visible');
    leadStatus.innerHTML = 'Lead Agent — <span style="color:#22c55e">working solo</span>';
  }
}

function createActiveCard(entry, key) {
  const card = document.createElement('div');
  card.className = 'active-card';
  card.dataset.key = key;
  card.innerHTML = \`
    <div class="active-card-top">
      <div class="active-card-agent" style="background:\${entry.color}">
        \${entry.agent}
        <span class="model-tag">\${entry.model}</span>
      </div>
      <div class="active-card-timer">
        <span class="active-card-spinner"></span>
        <span class="timer-value">0s</span>
      </div>
    </div>
    <div class="active-card-task">\${escapeHtml(entry.task)}</div>
  \`;
  activeGrid.appendChild(card);
  return card;
}

// ── Timeline card ──
function createTimelineCard(entry, key) {
  empty.style.display = 'none';
  const card = document.createElement('div');
  card.className = 'card active-card-timeline';
  card.dataset.key = key;
  card.dataset.time = entry.time;

  const dateMatch = matchesFilter(entry.time);
  const statMatch = currentStatFilter === 'all' || currentStatFilter === 'active';
  if (!dateMatch || !statMatch) card.classList.add('hidden');

  card.innerHTML = \`
    <div class="card-header">
      <div class="card-left">
        <div class="agent-badge" style="background:\${entry.color}">
          \${entry.agent}
          <span class="model-tag">\${entry.model}</span>
        </div>
        <span class="status-working">
          <div class="spinner"></div>
          working...
          <span class="working-timer">0s</span>
        </span>
      </div>
      <div class="card-meta">
        <span class="card-time">\${entry.timeShort}</span>
      </div>
    </div>
    <div class="card-body">
      <div class="task-text">\${escapeHtml(entry.task)}</div>
    </div>
  \`;

  timeline.prepend(card);
  if (dateMatch && statMatch) card.scrollIntoView({ behavior: 'smooth', block: 'start' });
  return card;
}

// ── Handle entries ──
function handleDelegate(entry) {
  agentCounter++;
  const key = entry.agent + '-' + agentCounter;

  const activeCard   = createActiveCard(entry, key);
  const timelineCard = createTimelineCard(entry, key);
  const startTime    = Date.now();

  const STALE_MS = 10 * 60 * 1000;
  const intervalId = setInterval(() => {
    const elapsedMs = Date.now() - startTime;
    const elapsed = formatMs(elapsedMs);
    const timerEl = activeCard.querySelector('.timer-value');
    const tlTimer = timelineCard.querySelector('.working-timer');
    if (timerEl) timerEl.textContent = elapsed;
    if (tlTimer) tlTimer.textContent = elapsed;

    if (elapsedMs > STALE_MS) {
      clearInterval(intervalId);
      activeCard.remove();
      activeAgents.delete(entry.id || entry.agent);
      updateActiveSection();
      timelineCard.className = 'card';
      const statusEl = timelineCard.querySelector('.status-working');
      if (statusEl) {
        statusEl.outerHTML = '<span class="status-done" style="color:#f59e0b">⚠ timed out</span> <span class="duration-badge">⏱ ' + elapsed + '</span>';
      }
      updateStats();
    }
  }, 1000);

  const agentKey = entry.id || entry.agent;
  activeAgents.set(agentKey, { entry, activeCard, timelineCard, intervalId, startTime, key });
  allEntries.push({ ...entry, _key: key });
  updateActiveSection();
  updateStats();
}

function handleReport(entry) {
  const agentKey = entry.id && activeAgents.has(entry.id) ? entry.id : entry.agent;
  const active = activeAgents.get(agentKey);
  if (!active) {
    agentCounter++;
    const key = entry.agent + '-' + agentCounter;
    empty.style.display = 'none';
    const card = document.createElement('div');
    card.className = 'card';
    card.dataset.key = key;
    card.dataset.time = entry.time;
    if (!matchesFilter(entry.time)) card.classList.add('hidden');
    card.innerHTML = \`
      <div class="card-header">
        <div class="card-left">
          <div class="agent-badge" style="background:\${entry.color}">\${entry.agent}<span class="model-tag">\${entry.model}</span></div>
          <span class="status-done">✓ done</span>
          \${entry.duration ? '<span class="duration-badge">⏱ ' + entry.duration + '</span>' : ''}
        </div>
        <div class="card-meta"><span class="card-time">\${entry.timeShort}</span></div>
      </div>
      <div class="card-body">
        \${entry.result ? '<div class="result-text">' + escapeHtml(entry.result) + '</div>' : ''}
      </div>
    \`;
    timeline.prepend(card);
    allEntries.push({ ...entry, _key: key });
    updateStats();
    return;
  }

  const { activeCard, timelineCard, intervalId } = active;
  clearInterval(intervalId);

  activeCard.remove();
  activeAgents.delete(agentKey);
  updateActiveSection();

  timelineCard.className = 'card';
  timelineCard.dataset.time = entry.time;

  const statusEl = timelineCard.querySelector('.status-working');
  if (statusEl) {
    statusEl.outerHTML = \`
      <span class="status-done">✓ done</span>
      \${entry.duration ? '<span class="duration-badge">⏱ ' + entry.duration + '</span>' : ''}
    \`;
  }

  if (entry.result) {
    const body = timelineCard.querySelector('.card-body');
    const rd = document.createElement('div');
    rd.className = 'result-text';
    rd.textContent = entry.result;
    rd.title = 'Click to expand';
    rd.addEventListener('click', () => rd.classList.toggle('expanded'));
    body.appendChild(rd);
  }

  const metaEl = timelineCard.querySelector('.card-meta');
  if (metaEl) {
    metaEl.innerHTML = '<span class="card-time">' + entry.timeShort + '</span>';
  }

  if (!timelineCard.classList.contains('hidden')) {
    timelineCard.scrollIntoView({ behavior: 'smooth', block: 'end' });
  }

  allEntries.push({ ...entry, _key: active.key });
  updateStats();
}

let leadFadeTimer = null;

function handleLead(entry) {
  const bar = document.getElementById('lead-bar');
  const task = document.getElementById('lead-task');
  const time = document.getElementById('lead-time');
  const leadStatus = document.getElementById('lead-status');

  bar.classList.remove('faded');
  task.textContent = entry.task || 'Working...';
  time.textContent = entry.timeShort;

  if (activeAgents.size === 0) {
    leadStatus.innerHTML = 'Lead Agent — <span style="color:#22c55e">working solo</span>';
  }

  if (leadFadeTimer) clearTimeout(leadFadeTimer);
  leadFadeTimer = setTimeout(function() {
    bar.classList.add('faded');
  }, 10000);
}

function handleEntry(entry) {
  if (entry.type === 'delegate') handleDelegate(entry);
  else if (entry.type === 'report') handleReport(entry);
  else if (entry.type === 'lead') handleLead(entry);
}

// ── Rebuild timeline with filter ──
function rebuildTimeline() {
  timeline.querySelectorAll('.card').forEach(card => {
    const t = card.dataset.time;
    if (!t) return;

    const dateMatch = matchesFilter(t);
    const isActive  = card.classList.contains('active-card-timeline');
    let statMatch = true;
    if (currentStatFilter === 'active')    statMatch = isActive;
    if (currentStatFilter === 'completed') statMatch = !isActive;

    if (dateMatch && statMatch) {
      card.classList.remove('hidden');
    } else {
      card.classList.add('hidden');
    }
  });

  const visible = timeline.querySelectorAll('.card:not(.hidden)');
  empty.style.display = visible.length === 0 ? 'block' : 'none';
  updateStats();
}

// ── Load existing ──
fetch('/api/entries')
  .then(r => r.json())
  .then(entries => {
    let lastLead = null;
    entries.forEach(function(e) {
      if (e.type === 'lead') { lastLead = e; }
      else { handleEntry(e); }
    });
    if (lastLead) handleLead(lastLead);
    const STALE_LOAD_MS = 10 * 60 * 1000;
    for (const [key, a] of activeAgents) {
      const ageMs = Date.now() - new Date(a.entry.time).getTime();
      if (ageMs > STALE_LOAD_MS) {
        clearInterval(a.intervalId);
        a.activeCard.remove();
        activeAgents.delete(key);
        a.timelineCard.className = 'card';
        const statusEl = a.timelineCard.querySelector('.status-working');
        if (statusEl) {
          statusEl.outerHTML = '<span class="status-done" style="color:#f59e0b">⚠ timed out</span> <span class="duration-badge">⏱ ' + formatMs(ageMs) + '</span>';
        }
      }
    }
    updateActiveSection();
    rebuildTimeline();
    window.scrollTo(0, 0);
  });

// ── SSE ──
const evtSource = new EventSource('/events');
evtSource.onmessage = (e) => {
  try { handleEntry(JSON.parse(e.data)); } catch (_) {}
};
</script>
</body>
</html>`;
