#!/usr/bin/env node
/**
 * PostToolUse hook: detects git push commands and sets a flag.
 *
 * UNIVERSAL — works on any project. No project-specific references.
 *
 * When a Bash tool call contains "git push", writes .claude/.session-pushed
 * so the Stop hook knows real work was pushed and memory should be updated.
 */
const fs = require('fs');
const path = require('path');

let input = '';
process.stdin.on('data', chunk => input += chunk);
process.stdin.on('end', () => {
  try {
    const data = JSON.parse(input);
    const command = (data.tool_input && data.tool_input.command) || '';

    if (data.tool_name === 'Bash' && command.includes('git push')) {
      const flagFile = path.join(data.cwd || process.cwd(), '.claude', '.session-pushed');
      fs.writeFileSync(flagFile, new Date().toISOString());
    }
  } catch (e) {
    // Silent — never block on errors
  }
  process.exit(0);
});
