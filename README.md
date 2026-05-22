# Otwarte Raporty

Polskie dane publiczne w jednym miejscu — wskaźniki gospodarcze, społeczne i demograficzne.

**Live products:**
- [open-reporting.dev](https://open-reporting.dev) — Blog
- [portal.open-reporting.dev/public_finance/](https://portal.open-reporting.dev/public_finance/) — Public Finance dashboard (first dbr dashboard)
- [@otwarteraporty](https://instagram.com/otwarteraporty) — Instagram

---

## Quick Start

```bash
git clone https://github.com/rutkala/open-reporting.git
cd open-reporting
cp .env.example .env                            # fill in secrets
docker compose up -d                            # nginx, postgres, ghost
pip install --break-system-packages -e packages/dbr packages/screenshot
```

Deploy a dashboard:
```bash
dbr validate products/dashboards/public_finance
dbr run      products/dashboards/public_finance   # systemd + nginx + health check
```

---

## Documentation

Start with [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — the source of truth for repo layout and AI delegation.

| Doc | Purpose |
|-----|---------|
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | **Authoritative**: two-plane architecture, folder ownership, AI delegation contract |
| [docs/refactor-plan.md](docs/refactor-plan.md) | Mechanical playbook for the structural refactor (mostly executed) |
| [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) | How to contribute — issue lifecycle, Git workflow, PR process |
| [docs/ROADMAP.md](docs/ROADMAP.md) | Pointer to Linear (where roadmap lives) |
| [docs/RELEASE_NOTES.md](docs/RELEASE_NOTES.md) | What's shipped |
| [docs/PROJECT.md](docs/PROJECT.md) | Vision, product lines, principles |
| [docs/DOMAINS.md](docs/DOMAINS.md) | Data domain taxonomy |
| [docs/DATA_SOURCES.md](docs/DATA_SOURCES.md) | Data sources, APIs, naming conventions |
| [docs/DATA_MODEL.md](docs/DATA_MODEL.md) | Schema overview |

**Team knowledge base** (standards, KB, agent memory):

| Doc | Purpose |
|-----|---------|
| [team/knowledge-base/INDEX.md](team/knowledge-base/INDEX.md) | Research KB index — what's built, what's planned, loading guide |
| [team/standards/INDEX.md](team/standards/INDEX.md) | Standards index — build rules + evaluation rules, derivation chain |
| [team/lessons-learned.md](team/lessons-learned.md) | Post-issue retrospectives |
| [CLAUDE.md](CLAUDE.md) | Lead Analyst & Architect instructions — collaboration model, repo structure, skills |

---

## Project Management

All work is tracked in **Linear** (`OR` project). No idea goes directly to code — every task starts as a Linear issue. See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) for the full workflow.

---

*Owner: Radek Utkala · Poland · 2026*
