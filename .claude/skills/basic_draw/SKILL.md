---
name: basic_draw
description: "Create visual diagrams — architecture diagrams, ERDs, wireframes, flowcharts — using Excalidraw. Atomic action invoked by design and plan when a diagram is needed."
user-invocable: true
argument-hint: "<what to diagram>"
---

# Draw

Create a visual diagram using the Excalidraw MCP tool. Invoked when a process skill
needs a diagram to communicate structure, flow, or layout.

## Task
`$ARGUMENTS`

**Called by:** design and plan, when a visual diagram is needed to communicate structure, flow, or layout. Returns the diagram reference (Excalidraw checkpoint path) to the calling skill.

## Steps

1. Identify the diagram type: architecture / ERD / wireframe / flowchart / sequence
2. Identify all elements: nodes, connections, groupings, labels
3. Create the diagram using `mcp__claude_ai_Excalidraw__create_view`
4. Save a checkpoint using `mcp__claude_ai_Excalidraw__save_checkpoint`
5. Return the diagram reference to the calling skill

## Diagram types by use case

| Use case | Diagram type |
|----------|-------------|
| Data layer (tables, flows) | ERD or flowchart |
| System components | Architecture diagram |
| Page layout, UI | Wireframe |
| Process steps | Flowchart |
| Data pipeline | Sequence diagram |

## Rules

- Labels in English (internal diagrams); Polish labels for user-facing wireframes
- Every node must have a label — no unlabelled boxes
- Group related elements visually
- Keep diagrams focused — one diagram per concept, not one per project
