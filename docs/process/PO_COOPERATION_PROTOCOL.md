# Product Owner ↔ AI Team Cooperation Protocol

**Status:** Active | **Last Updated:** 2026-06-08

This document defines exactly how the human Product Owner (PO) and the autonomous AI team communicate, track progress, and trigger work without confusion.

## 1. Single Source of Truth: Linear
We will use Linear as the definitive source of truth for all tasks, roadmaps, and blockers. The chat interface is for high-level strategy; Linear is for execution.

### The Workflow States
We will establish specific workflow states in Linear:
- **Backlog / To Do:** Ideas and future phases.
- **In Progress:** The AI team is actively writing code for this.
- **Blocked on PO:** The AI team cannot proceed (e.g., we need an Instagram API key, or we need you to click "Publish" in Ghost).
- **Done:** The AI team has shipped the code and verified it works.

## 2. Tracking the Project
Currently, tracking is difficult because the AI moves very fast in the background. We will solve this by building the **PO Command Center** (`po_dashboard.html`). 
This will be a private page on your website that queries the Linear API in real-time and displays:
1. What the AI is currently doing.
2. What specifically is waiting for your input (Blocked on PO).
3. The overall progress of the current Roadmap Phase.

## 3. How You Trigger Automatic Work
You should not have to come into this chat window and type long prompts just to start a task. 

**The Webhook Solution:**
We will build a webhook integration between Linear and the AI environment. 
- If you move a ticket from `Blocked on PO` ➡️ `To Do`, the webhook will detect it and automatically wake up the AI team to resume work.
- If you create a new ticket in Linear and assign it to the `AI Lead`, the webhook will catch it and dispatch an agent to build it immediately.

## 4. How We Handle "Actions For You"
Whenever an agent hits a wall (e.g. "I cannot log into the Meta Developer portal because it requires 2FA"), the agent will:
1. Stop execution on that specific task.
2. Create a Linear ticket outlining exactly what needs to be done.
3. Move the ticket to `Blocked on PO`.
4. It will immediately appear in your PO Command Center highlighted in Red.
