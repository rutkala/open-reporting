#!/usr/bin/env node
/**
 * Lead agent activity logger
 *
 * UNIVERSAL — works on any project. No project-specific references.
 *
 * Logs what the lead (orchestrator) is doing when working solo.
 * Fires on PreToolUse for key tools (Read, Edit, Write, Bash, Grep, Glob).
 * Writes a "lead" entry to agent-activity.jsonl so the dashboard can show it.
 *
 * Throttled: only writes if last entry was >2s ago to avoid flooding.
 */
const fs   = require('fs');
const path = require('path');

// Only log meaningful tools
const TRACKED_TOOLS = new Set(['Read', 'Edit', 'Write', 'Bash', 'Grep', 'Glob', 'Agent', 'WebFetch', 'WebSearch']);

// Friendly labels for tools
const TOOL_LABELS = {
  Read:      'Reading',
  Edit:      'Editing',
  Write:     'Writing',
  Bash:      'Running command',
  Grep:      'Searching content',
  Glob:      'Searching files',
  Agent:     'Delegating',
  WebFetch:  'Fetching web page',
  WebSearch: 'Web search',
};

let input = '';
process.stdin.on('data', chunk => (input += chunk));
process.stdin.on('end', () => {
  try {
    const data = JSON.parse(input || '{}');
    const toolName = data.tool_name || '';

    // Skip untracked tools
    if (!TRACKED_TOOLS.has(toolName)) process.exit(0);

    // Skip Agent calls — those are handled by log-subagent.js
    if (toolName === 'Agent') process.exit(0);

    const cwd       = data.cwd || process.cwd();
    const jsonlFile = path.join(cwd, '.claude', 'agent-activity.jsonl');
    const throttle  = path.join(cwd, '.claude', '.lead-last-log');

    // Throttle: skip if last log was < 2s ago
    try {
      const last = parseInt(fs.readFileSync(throttle, 'utf8').trim());
      if (Date.now() - last < 2000) process.exit(0);
    } catch (_) {}

    // Build description from tool input
    let detail = '';
    if (toolName === 'Read') {
      const fp = data.tool_input?.file_path || '';
      detail = require('path').basename(fp);
    } else if (toolName === 'Edit') {
      const fp = data.tool_input?.file_path || '';
      detail = require('path').basename(fp);
    } else if (toolName === 'Write') {
      const fp = data.tool_input?.file_path || '';
      detail = require('path').basename(fp);
    } else if (toolName === 'Bash') {
      detail = (data.tool_input?.description || data.tool_input?.command || '').substring(0, 100);
    } else if (toolName === 'Grep') {
      detail = data.tool_input?.pattern || '';
    } else if (toolName === 'Glob') {
      detail = data.tool_input?.pattern || '';
    } else {
      detail = (data.tool_input?.description || '').substring(0, 100);
    }

    const label = TOOL_LABELS[toolName] || toolName;
    const task = detail ? `${label}: ${detail}` : label;
    const time = new Date().toISOString();
    const timeShort = new Date().toLocaleTimeString('en-GB', { hour12: false });

    const entry = {
      type: 'lead',
      time,
      timeShort,
      agent: 'lead',
      model: 'opus',
      color: '#f59e0b',
      tool: toolName,
      task
    };

    fs.appendFileSync(jsonlFile, JSON.stringify(entry) + '\n');
    fs.writeFileSync(throttle, String(Date.now()));

  } catch (e) {
    // Silent fail
  }
});
