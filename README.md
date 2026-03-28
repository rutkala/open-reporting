# Otwarte Raporty

Polskie dane publiczne w jednym miejscu — wskaźniki gospodarcze, społeczne i demograficzne.

**Live products:**
- [open-reporting.dev](https://open-reporting.dev) — Blog
- [portal.open-reporting.dev](https://portal.open-reporting.dev) — Data portal (Labour dashboard, Explorer)
- [portal.open-reporting.dev/app](https://portal.open-reporting.dev/app/) — Mobile PWA
- [@otwarteraporty](https://instagram.com/otwarteraporty) — Instagram

---

## Quick Start

```bash
git clone https://github.com/rutkala/open-reporting.git
cd open-reporting
cp .env.example .env  # fill in secrets
docker compose up -d  # start nginx, postgres, ghost
```

Run portal apps (each in its own terminal or systemd service):
```bash
PYTHONPATH=/opt/open-reporting python3 products/dashboards/labour/app.py   # port 8050
PYTHONPATH=/opt/open-reporting python3 products/dashboards/explorer/app.py # port 8051
PYTHONPATH=/opt/open-reporting python3 products/mobile/app.py              # port 8052
```

---

## Documentation

| Doc | Purpose |
|-----|---------|
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Infrastructure, databases, data pipeline |
| [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) | How to contribute — issue lifecycle, Git workflow, PR process |
| [docs/ROADMAP.md](docs/ROADMAP.md) | What's planned post-MVP |
| [docs/RELEASE_NOTES.md](docs/RELEASE_NOTES.md) | What's shipped |
| [docs/MVP.md](docs/MVP.md) | MVP v0.1 declaration and scope |
| [docs/PROJECT.md](docs/PROJECT.md) | Vision, product lines, principles |
| [docs/DOMAINS.md](docs/DOMAINS.md) | Data domain taxonomy |
| [docs/DATA_SOURCES.md](docs/DATA_SOURCES.md) | Data sources, APIs, naming conventions |

Agent instructions, standards, playbooks, and lessons learned are in [.claude/](.claude/).

---

## Project Management

All work is tracked in **Linear** (`ORE` project). No idea goes directly to code — every task starts as a Linear issue. See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) for the full workflow.

---

*Owner: Radek Utkala · Poland · 2026*
