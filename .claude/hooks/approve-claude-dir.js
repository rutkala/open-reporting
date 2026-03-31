#!/usr/bin/env node
/**
 * Auto-approve Write and Edit calls targeting the .claude/ directory.
 *
 * Claude Code's bypassPermissions mode still prompts for .claude/ root-level
 * files (session-memory.md, etc.) by design. This hook explicitly approves
 * those calls so they run without user interaction.
 */

let input = '';
process.stdin.on('data', chunk => (input += chunk));
process.stdin.on('end', () => {
  try {
    const data = JSON.parse(input || '{}');
    const tool = data.tool_name || '';
    const path = data.tool_input?.file_path || '';

    if ((tool === 'Write' || tool === 'Edit') && path.includes('/.claude/')) {
      process.stdout.write(JSON.stringify({ decision: 'approve' }));
    }
  } catch (_) {}
  process.exit(0);
});
