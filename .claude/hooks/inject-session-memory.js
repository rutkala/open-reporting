#!/usr/bin/env node
/**
 * SessionStart + PostCompact hook: Injects session-memory.md as additionalContext
 * so every conversation automatically starts with recent work context.
 *
 * UNIVERSAL — works on any project. No project-specific references.
 *
 * Hook spec output:
 *   { "hookSpecificOutput": { "hookEventName": "SessionStart", "additionalContext": "..." } }
 */
const fs   = require('fs');
const path = require('path');

let input = '';
process.stdin.on('data', chunk => (input += chunk));
process.stdin.on('end', () => {
  try {
    const data    = JSON.parse(input || '{}');
    const cwd     = data.cwd || process.cwd();
    const memFile = path.join(cwd, 'docs', 'session-memory.md');

    if (!fs.existsSync(memFile)) {
      process.exit(0); // No memory file yet — start fresh
    }

    const content = fs.readFileSync(memFile, 'utf8').trim();

    console.log(JSON.stringify({
      hookSpecificOutput: {
        hookEventName: 'SessionStart',
        additionalContext: `## Session Memory (auto-loaded)\n\n${content}`
      }
    }));
  } catch (e) {
    process.exit(0); // Silent fail — never block session start
  }
});
