# screenshot

Headless-browser screenshot utility for Open Reporting dashboards. Starts a dashboard on a temporary port, waits for it to render, takes a full-page PNG, then stops it.

## Install

```bash
pip install -e packages/screenshot
```

Installs the `screenshot` CLI command.

## Use

```bash
screenshot <dashboard> [--port PORT] [--output PATH]
```

Where `<dashboard>` is one of the keys in `DASHBOARDS` (see `cli.py`). Currently supported: `labour`, `explorer`, `finance`.

Used by `.claude/agents/visual-screenshot-reviewer.md` to capture rendered output for evaluation.
