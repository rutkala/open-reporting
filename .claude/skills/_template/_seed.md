# Seed input for `<new-skill-name>`

> Fill this file in immediately after `cp -r _template/ complex_<new-skill>/`,
> before invoking `/composite_knowledge complex_<new-skill>`. The builder
> reads this file as its first input. Sections marked *optional* may be
> left empty — the builder will work without them, just less efficiently.

## What this skill should do

One paragraph: the problem this skill solves, the output it produces,
who uses it, what the outcome looks like.

## Out of scope

What this skill is explicitly NOT — adjacent topics it should not drift
into, decisions it should not make, parts of the workflow it does not
own.

## Pre-existing experience *(optional)*

Free text — what the user already knows about this area. Hard-won rules,
patterns that worked, patterns that failed, war stories. Treated as a
priority input by the `composite_knowledge` builder; rules that recur
during synthesis can be lifted into `experience/` later.

## Seed sources *(optional)*

Specific URLs, books, projects, or documents the builder should treat as
starting points for the collect phase of `/composite_knowledge` (in addition
to whatever it discovers itself). Tier them — primary first, secondary below.

- *(primary)* https://...
- *(primary)* https://...
- *(secondary)* https://...
- *(local)* file:///path/to/relevant/document
