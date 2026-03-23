#!/usr/bin/env node
/**
 * Stop hook: Reminds the agent to update session-memory.md before ending.
 *
 * UNIVERSAL — works on any project. No project-specific references.
 *
 * Logic:
 * 1. If stop_hook_active (already reminded once) → allow stop (prevents infinite loop)
 * 2. If .claude/.session-pushed flag does not exist → allow stop (no push this session)
 * 3. If session-memory.md was modified in last 5 minutes → clear flag and allow stop
 * 4. Otherwise → block and remind agent to update
 */
const fs = require('fs');
const path = require('path');

let input = '';
process.stdin.on('data', chunk => input += chunk);
process.stdin.on('end', () => {
  try {
    const data = JSON.parse(input);

    // Prevent infinite loops — if hook already fired once, let agent stop
    if (data.stop_hook_active) {
      process.exit(0);
    }

    const cwd = data.cwd || process.cwd();
    const flagFile = path.join(cwd, '.claude', '.session-pushed');

    // No push happened this session — nothing to document
    if (!fs.existsSync(flagFile)) {
      process.exit(0);
    }

    // Push happened — check if session-memory.md was recently updated
    const memFile = path.join(cwd, '.claude', 'session-memory.md');
    if (fs.existsSync(memFile)) {
      const stat = fs.statSync(memFile);
      const minutesSinceModified = (Date.now() - stat.mtimeMs) / 60000;

      if (minutesSinceModified < 5) {
        // Memory updated — clear flag and allow stop
        fs.unlinkSync(flagFile);
        process.exit(0);
      }
    }

    // Push happened but memory not updated — block and remind
    console.log(JSON.stringify({
      decision: 'block',
      reason: 'Before ending, update .claude/session-memory.md with this session\'s work. Update sections: Current Focus, Last Session Summary, Recent Changes. Keep under 100 lines, roll off oldest entries.'
    }));
  } catch (e) {
    // On any error, allow stop gracefully
    process.exit(0);
  }
});
