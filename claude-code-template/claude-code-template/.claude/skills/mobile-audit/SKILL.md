---
name: mobile-audit
description: "Audit components for mobile/PWA responsiveness. Scans for touch target issues, viewport problems, non-responsive layouts, hover-only interactions, and iOS/Android compatibility. Works on any frontend project using CSS/Tailwind/etc."
disable-model-invocation: true
user-invocable: true
argument-hint: "[component-path | page-name | 'all']"
---

# Mobile / PWA Responsiveness Audit

Scan frontend components for mobile responsiveness issues.

## Mode

- **No argument or `all`**: Scan all page-level components in priority order
- **File path or page name**: Scan that specific component

## Target
$ARGUMENTS

## Checklist (per component)

### Layout
- [ ] No fixed heights that break on mobile (use `min-h-` instead of `h-`)
- [ ] No horizontal overflow causing side-scroll (check wide containers, tables, code blocks)
- [ ] Flex/grid layouts stack vertically on mobile (mobile-first: `flex-col md:flex-row`)
- [ ] Content doesn't overflow screen width at 320px viewport

### Touch Targets
- [ ] All buttons, links, and interactive elements >= 44x44px tap area
- [ ] Adequate spacing between clickable elements (min 8px gap)
- [ ] No tiny icon-only buttons without padding

### Tables
- [ ] Wide tables wrapped in `overflow-x-auto` for horizontal scroll
- [ ] Consider card layout on mobile as alternative to tables

### Modals / Dialogs
- [ ] Full-screen on mobile (e.g., `fixed inset-0`)
- [ ] Centered card on desktop (e.g., `md:inset-auto md:max-w-lg`)
- [ ] Scrollable content inside modal body
- [ ] Close button easily reachable (top-right or bottom)

### Forms / Inputs
- [ ] Input font-size >= 16px to prevent iOS auto-zoom
- [ ] Labels visible (not just placeholder text)
- [ ] Keyboard doesn't obscure input fields
- [ ] Submit buttons visible without scrolling

### Text
- [ ] Readable without zooming (min 14px on mobile)
- [ ] Long text has proper truncation (`truncate`, `line-clamp-*`)
- [ ] No text overflow causing horizontal scroll

### Viewport Height
- [ ] Uses `dvh` (dynamic viewport height) instead of `vh` where possible
- [ ] Accounts for mobile address bar height changes
- [ ] Full-height layouts use `min-h-[100dvh]` not `h-screen`

### Safe Areas (PWA)
- [ ] Header accounts for status bar / notch (`padding-top: env(safe-area-inset-top)`)
- [ ] Footer accounts for home bar (`padding-bottom: env(safe-area-inset-bottom)`)
- [ ] Content not hidden behind system UI

### Hover States
- [ ] Every `:hover` interaction has a click/tap equivalent
- [ ] No content that only appears on hover (tooltips need tap alternative)
- [ ] Dropdown menus work with tap, not just hover

### Images / Media
- [ ] Images are responsive (`max-w-full h-auto`)
- [ ] SVGs have `viewBox` attribute
- [ ] No fixed-size images overflowing containers

### Performance
- [ ] No heavy animations that cause jank on mobile
- [ ] Large lists use virtualisation or pagination
- [ ] Images are appropriately sized (not 4K images on mobile)

## Process

1. Read the target component(s)
2. Check each item in the checklist above
3. For each issue found, note:
   - File path and line number
   - What the problem is
   - Suggested fix (specific CSS/class change)
4. Group findings by severity:
   - **BROKEN** — Unusable on mobile (layout overflow, unreachable buttons)
   - **POOR UX** — Usable but frustrating (tiny targets, hard to read)
   - **MINOR** — Could be better (hover-only, suboptimal spacing)

## Output Format

```
## Mobile Audit: [component name]

### BROKEN (must fix)
- **[file:line]** — [issue]
  Fix: [specific change]

### POOR UX (should fix)
- **[file:line]** — [issue]
  Fix: [specific change]

### MINOR (nice to have)
- **[file:line]** — [issue]
  Fix: [specific change]

### Summary
X issues found: Y broken, Z poor UX, W minor
```

## Common Fixes Reference

```css
/* Mobile-first flex layout */
flex flex-col md:flex-row

/* Touch-friendly button */
min-h-[44px] min-w-[44px] px-4 py-3

/* Scrollable table */
<div class="overflow-x-auto"><table class="min-w-[600px]">...</table></div>

/* Full-screen mobile modal */
fixed inset-0 md:inset-auto md:top-1/2 md:left-1/2 md:-translate-x-1/2 md:-translate-y-1/2

/* Safe viewport height */
min-h-[100dvh]

/* Prevent iOS input zoom */
text-base  /* 16px minimum */

/* Safe area padding */
padding-top: env(safe-area-inset-top);
padding-bottom: env(safe-area-inset-bottom);
```
