"""Command-line interface for dbr.

Subcommands:

    dbr init <name>      scaffold a new dashboard project in ./<name>/
    dbr run <path>       start the Dash server for the dashboard at <path>
    dbr validate <path>  schema-check the YAMLs without starting the server
    dbr compile <path>   print the resolved layout tree (debug)

Registered as a console-script entry point in pyproject.toml:

    [project.scripts]
    dbr = "dbr.cli:main"
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="dbr",
        description="Declarative YAML dashboard framework.",
    )
    sub = parser.add_subparsers(dest="cmd", required=True, metavar="command")

    p_init = sub.add_parser("init", help="Scaffold a new dashboard project")
    p_init.add_argument("name", help="Project name (also used as URL prefix / domain)")

    p_run = sub.add_parser("run", help="Deploy (systemd + nginx) and (re)start the dashboard service")
    p_run.add_argument("path", nargs="?", default=".",
                       help="Path to the dashboard project (default: .)")

    p_serve = sub.add_parser("serve", help="Run the Dash server in the foreground (used by systemd; rarely called directly)")
    p_serve.add_argument("path", nargs="?", default=".",
                         help="Path to the dashboard project (default: .)")

    p_validate = sub.add_parser("validate", help="Schema-check YAMLs without starting the server")
    p_validate.add_argument("path", nargs="?", default=".",
                            help="Path to the dashboard project (default: .)")

    p_compile = sub.add_parser("compile", help="Print the resolved layout tree (debug)")
    p_compile.add_argument("path", nargs="?", default=".",
                           help="Path to the dashboard project (default: .)")

    p_build = sub.add_parser("build", help="Render the dashboard to static HTML (no server)")
    p_build.add_argument("path", nargs="?", default=".",
                         help="Path to the dashboard project (default: .)")
    p_build.add_argument("--out", required=True,
                         help="Output directory; writes <out>/<domain>/index.html (+ plotly.min.js)")
    p_build.add_argument("--plotly-src", default="plotly.min.js",
                         help="<script src> for plotly.js (default per-page 'plotly.min.js'; "
                              "pass an absolute URL like /assets/plotly.min.js to share one copy)")
    p_build.add_argument("--no-vendor-plotly", action="store_true",
                         help="Don't write plotly.min.js next to the page (use with a shared --plotly-src)")

    args = parser.parse_args(argv)

    dispatch = {
        "init":     cmd_init,
        "run":      cmd_run,
        "serve":    cmd_serve,
        "validate": cmd_validate,
        "compile":  cmd_compile,
        "build":    cmd_build,
    }
    return dispatch[args.cmd](args)


# ── init ───────────────────────────────────────────────────────────────────────

def cmd_init(args: argparse.Namespace) -> int:
    name = args.name
    root = Path(name).resolve()
    if root.exists():
        print(f"Error: {root} already exists", file=sys.stderr)
        return 1

    (root / "pages").mkdir(parents=True)

    (root / "app.py").write_text(
        "import os\n"
        "from pathlib import Path\n"
        "\n"
        "# Tell theme + layout loaders where this project lives so they pick\n"
        "# up any local theme.yaml / layout.yaml overrides. Must be set\n"
        "# BEFORE `dbr` is imported.\n"
        "os.environ.setdefault(\"DBR_PROJECT_ROOT\", str(Path(__file__).resolve().parent))\n"
        "\n"
        "from dbr.compiler import run_dashboard\n"
        "\n"
        "run_dashboard(__file__)\n"
    )

    (root / "dashboard.yml").write_text(
        "# yaml-language-server: $schema=https://open-reporting.dev/dbr/schemas/dashboard.schema.json\n"
        "# Open Reporting dashboard root config.\n"
        "# Only `domain` and `port` are required; other keys inherit kit defaults.\n"
        "\n"
        f"domain: {name}\n"
        "port:   8055\n"
        f"title:  {name.title()}\n"
    )

    (root / "pages" / "pages.yml").write_text(
        "# yaml-language-server: $schema=https://open-reporting.dev/dbr/schemas/pages.schema.json\n"
        "# Page order — list pages in the order they appear in the sidebar.\n"
        "# Each entry must match a sibling folder containing `page.yml`.\n"
        "\n"
        "order: []\n"
    )

    (root / "README.md").write_text(
        f"# {name.title()} dashboard\n"
        "\n"
        "Authored with [dbr](https://github.com/your-org/dbr).\n"
        "\n"
        "## Run locally\n"
        "\n"
        "```bash\n"
        "dbr run .\n"
        "```\n"
        "\n"
        "## Add a page\n"
        "\n"
        "1. `mkdir pages/<name>`\n"
        "2. Add `pages/<name>/page.yml` with `title` and `anchor`.\n"
        "3. Add `pages/<name>/visuals/visuals.yml` listing the visual order.\n"
        "4. Add one `pages/<name>/visuals/<visual>.yml` per visual.\n"
        "5. Add the page name to `pages/pages.yml` under `order:`.\n"
    )

    print(f"Created {root}")
    print(f"Next: cd {name} && dbr run .")
    return 0


# ── run ────────────────────────────────────────────────────────────────────────

def cmd_run(args: argparse.Namespace) -> int:
    """Deploy a dashboard end-to-end: write infra files, sudo cp, restart service, reload nginx."""
    import subprocess
    import time
    import yaml

    project_root = Path(args.path).resolve()
    _assert_project(project_root)

    config = yaml.safe_load((project_root / "dashboard.yml").read_text()) or {}
    domain = config.get("domain")
    port = config.get("port")
    if not domain or not port:
        print("Error: dashboard.yml must define `domain` and `port`", file=sys.stderr)
        return 1

    print(f"→ Deploying {domain} on port {port}")

    # 1. Write the systemd unit at infra/systemd/or-<domain>.service
    repo_root = _find_repo_root(project_root)
    unit_path = repo_root / "infra" / "systemd" / f"or-{domain}.service"
    unit_path.parent.mkdir(parents=True, exist_ok=True)
    unit_path.write_text(_render_systemd_unit(domain, project_root))
    print(f"  ✓ wrote {unit_path.relative_to(repo_root)}")

    # 2. Install + (re)start the systemd unit
    _run(["sudo", "-n", "/usr/bin/cp", str(unit_path), "/etc/systemd/system/"])
    _run(["sudo", "-n", "/usr/bin/systemctl", "daemon-reload"])
    _run(["sudo", "-n", "/usr/bin/systemctl", "enable", f"or-{domain}.service"], allow_fail=True)
    _run(["sudo", "-n", "/usr/bin/systemctl", "restart", f"or-{domain}.service"])
    print(f"  ✓ systemd: or-{domain}.service restarted — waiting for health check")

    # 2b. Health check: dashboards take ~5-10s to start. MetricFlow runs
    #     in-process now (one ~6s engine setup amortised across all
    #     visuals, then ~50ms per query). Poll for the port to be
    #     listening; if not after the budget, dump status and fail.
    health_budget_s = 60
    import socket
    deadline = time.time() + health_budget_s
    while time.time() < deadline:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            try:
                if s.connect_ex(("127.0.0.1", int(port))) == 0:
                    break
            except OSError:
                pass
        time.sleep(1)
    else:
        # Port never opened — dump systemctl status (no journal access without sudo)
        status = subprocess.run(
            ["/usr/bin/systemctl", "status", f"or-{domain}.service", "--no-pager", "-n", "30"],
            capture_output=True, text=True,
        )
        print(
            f"Error: port {port} did not open within {health_budget_s}s — service may be in a crash loop",
            file=sys.stderr,
        )
        print("─" * 60, file=sys.stderr)
        print(status.stdout, file=sys.stderr)
        print("─" * 60, file=sys.stderr)
        print(f"Inspect logs:  sudo journalctl -u or-{domain}.service -n 50", file=sys.stderr)
        return 1
    print(f"  ✓ health check: port {port} is listening")

    # 3. Write the nginx route block at infra/nginx/conf.d/dbr-routes/<domain>.conf
    nginx_path = repo_root / "infra" / "nginx" / "conf.d" / "dbr-routes" / f"{domain}.conf"
    nginx_path.parent.mkdir(parents=True, exist_ok=True)
    nginx_path.write_text(_render_nginx_block(domain, port))
    print(f"  ✓ wrote {nginx_path.relative_to(repo_root)}")

    # 4. Validate + reload nginx
    test = subprocess.run(
        ["docker", "compose", "-f", str(repo_root / "docker-compose.yml"), "exec", "-T", "nginx", "nginx", "-t"],
        capture_output=True, text=True,
    )
    if test.returncode != 0:
        print(f"Error: nginx config invalid after writing route:\n{test.stderr}", file=sys.stderr)
        return 1
    _run(["docker", "compose", "-f", str(repo_root / "docker-compose.yml"), "exec", "-T", "nginx", "nginx", "-s", "reload"])
    print(f"  ✓ nginx reloaded")

    print()
    print(f"  → https://portal.open-reporting.dev/{domain}/")
    print(f"  → http://localhost:{port}/{domain}/")
    print(f"  → Logs: sudo journalctl -u or-{domain}.service -f")
    return 0


def cmd_serve(args: argparse.Namespace) -> int:
    """Run the Dash server in the foreground. Used by systemd's ExecStart."""
    import os

    project_root = Path(args.path).resolve()
    _assert_project(project_root)
    # Tell the theme + layout loaders where this project lives, so they
    # can pick up optional theme.yaml / layout.yaml overrides. Must be
    # set BEFORE the dbr.compiler import below.
    os.environ["DBR_PROJECT_ROOT"] = str(project_root)

    from dbr.compiler import run_dashboard
    run_dashboard(project_root)
    return 0  # never reached — app.run blocks


# ── deploy helpers ─────────────────────────────────────────────────────────────

def _render_systemd_unit(domain: str, project_root: Path) -> str:
    """Generate the systemd unit file content for a dashboard."""
    return f"""[Unit]
Description=Open Reporting — {domain} dashboard (/{domain}/)
After=network.target

[Service]
User=radek
Group=radek
WorkingDirectory=/opt/open-reporting
Environment=DUCKDB_PATH=/opt/open-reporting/data/warehouse.duckdb
Environment=PATH=/home/radek/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
EnvironmentFile=/opt/open-reporting/.env
ExecStart=/home/radek/.local/bin/dbr serve {project_root}
Restart=on-failure
RestartSec=5
# Memory guardrails (OR-168): each dbr serve peaks ~160 MB RSS. MemoryHigh is a
# soft throttle/reclaim point; MemoryMax is a hard ceiling so a runaway process is
# cgroup-OOM-killed + auto-restarted in isolation, instead of the kernel firing the
# global OOM killer and rebooting the whole VPS (3.7 GiB box, 16 always-on services).
MemoryAccounting=yes
MemoryHigh=256M
MemoryMax=384M

[Install]
WantedBy=multi-user.target
"""


def _render_nginx_block(domain: str, port: int) -> str:
    """Generate the nginx `location` block for a dashboard route."""
    return f"""# dbr-managed — re-written by `dbr run`. Manual edits will be lost.
location /{domain}/ {{
    proxy_pass http://172.18.0.1:{port};
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    add_header Cache-Control "no-store, no-cache, must-revalidate" always;
    add_header Pragma "no-cache" always;
}}
"""


def _find_repo_root(start: Path) -> Path:
    """Walk up from `start` until a directory containing `.git` is found."""
    cur = start.resolve()
    while cur != cur.parent:
        if (cur / ".git").exists():
            return cur
        cur = cur.parent
    raise RuntimeError(f"No .git found above {start}")


def _run(cmd: list[str], *, allow_fail: bool = False) -> None:
    """Run a subprocess; raise on non-zero unless allow_fail is set."""
    import subprocess
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0 and not allow_fail:
        print(f"Error running: {' '.join(cmd)}", file=sys.stderr)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        sys.exit(result.returncode)


# ── validate ───────────────────────────────────────────────────────────────────

def cmd_validate(args: argparse.Namespace) -> int:
    """Schema-check every YAML in the project tree against the packaged JSON Schemas."""
    import yaml
    from jsonschema import Draft202012Validator

    from dbr.schemas import load_schema
    from dbr.visuals import VISUAL_REGISTRY, VISUAL_SCHEMAS

    project_root = Path(args.path).resolve()
    _assert_project(project_root)
    errors: list[str] = []

    def _check(path: Path, schema: dict, rel: str) -> dict | None:
        """Load + schema-validate one YAML file. Returns parsed dict on success."""
        if not path.exists():
            errors.append(f"{rel}: file missing")
            return None
        try:
            data = yaml.safe_load(path.read_text()) or {}
        except yaml.YAMLError as e:
            errors.append(f"{rel}: invalid YAML — {e}")
            return None
        validator = Draft202012Validator(schema)
        for err in sorted(validator.iter_errors(data), key=lambda e: list(e.absolute_path)):
            loc = ".".join(str(p) for p in err.absolute_path) or "<root>"
            errors.append(f"{rel}: at `{loc}` — {err.message}")
        return data

    # 1. dashboard.yml
    _check(project_root / "dashboard.yml", load_schema("dashboard"), "dashboard.yml")

    # 2. pages/pages.yml
    pages_dir = project_root / "pages"
    pages_meta = _check(pages_dir / "pages.yml", load_schema("pages"), "pages/pages.yml")

    if pages_meta is not None:
        page_schema    = load_schema("page")
        visuals_schema = load_schema("visuals")
        visual_schema  = load_schema("visual")

        for page_name in pages_meta.get("order", []) or []:
            page_dir = pages_dir / page_name
            rel = f"pages/{page_name}"

            # 3. pages/<name>/page.yml
            _check(page_dir / "page.yml", page_schema, f"{rel}/page.yml")

            visuals_dir = page_dir / "visuals"
            if not (visuals_dir / "visuals.yml").exists():
                continue  # empty page = no visuals.yml = valid

            # 4. pages/<name>/visuals/visuals.yml
            visuals_meta = _check(visuals_dir / "visuals.yml", visuals_schema, f"{rel}/visuals/visuals.yml")
            if visuals_meta is None:
                continue

            # 5. each pages/<name>/visuals/<visual>.yml
            for visual_name in _extract_visual_names(visuals_meta):
                vpath = visuals_dir / f"{visual_name}.yml"
                vrel  = f"{rel}/visuals/{visual_name}.yml"
                if not vpath.exists():
                    errors.append(f"{vrel}: file missing (referenced in visuals.yml)")
                    continue
                spec = _check(vpath, visual_schema, vrel)
                # Enum check against the live VISUAL_REGISTRY (not encoded in schema
                # so newly registered visuals work without schema edits).
                if spec is not None:
                    vtype = spec.get("type")
                    if vtype is not None and vtype not in VISUAL_REGISTRY:
                        available = ", ".join(sorted(VISUAL_REGISTRY)) or "<none>"
                        errors.append(
                            f"{vrel}: at `type` — unknown visual {vtype!r}. Available: {available}"
                        )
                    elif vtype in VISUAL_SCHEMAS:
                        # Per-visual schema check — catches typos in visual-specific
                        # options (e.g. `show_perido` instead of `show_period`).
                        per_visual = Draft202012Validator(VISUAL_SCHEMAS[vtype])
                        for err in sorted(per_visual.iter_errors(spec), key=lambda e: list(e.absolute_path)):
                            loc = ".".join(str(p) for p in err.absolute_path) or "<root>"
                            errors.append(f"{vrel}: at `{loc}` — {err.message}")

    # 6. Optional project-level theme.yaml override (every key is optional, no schema yet)
    # 7. Optional project-level layout.yaml override (every key is optional, no schema yet)
    # Both files are deep-merged onto the package defaults, so a stray key just gets ignored.
    # Tightening to a real schema is a follow-up.

    if errors:
        print(f"{len(errors)} validation error(s):", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print(f"OK — {project_root} validates cleanly.")
    return 0


# ── compile ────────────────────────────────────────────────────────────────────

def cmd_compile(args: argparse.Namespace) -> int:
    """Build the layout tree without starting the server. Useful for debug."""
    from dbr.compiler.compiler import _load_pages, _load_yaml

    project_root = Path(args.path).resolve()
    _assert_project(project_root)

    config = _load_yaml(project_root / "dashboard.yml")
    sections = _load_pages(project_root / "pages")

    summary = {
        "project_root": str(project_root),
        "domain":       config.get("domain"),
        "port":         config.get("port"),
        "title":        config.get("title"),
        "page_count":   len(sections),
        "pages":        [{"title": s[0], "anchor": s[1], "visual_count": len(s[2])} for s in sections],
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


# ── build ──────────────────────────────────────────────────────────────────────

def cmd_build(args: argparse.Namespace) -> int:
    """Render the dashboard to static HTML under ``--out``."""
    import os

    project_root = Path(args.path).resolve()
    _assert_project(project_root)

    # Match app.py: set DBR_PROJECT_ROOT BEFORE importing dbr's theme/layout
    # loaders so any per-project theme.yaml / layout.yaml overrides are picked up.
    os.environ.setdefault("DBR_PROJECT_ROOT", str(project_root))

    from dbr.static_export import UnsupportedComponentError, build_static_dashboard

    try:
        index = build_static_dashboard(
            project_root, args.out,
            plotly_src=args.plotly_src,
            vendor_plotly=not args.no_vendor_plotly,
        )
    except UnsupportedComponentError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    size_kb = index.stat().st_size / 1024
    print(f"  ✓ built {project_root.name} → {index} ({size_kb:.0f} KB)")
    return 0


# ── helpers ────────────────────────────────────────────────────────────────────

def _extract_visual_names(visuals_meta: dict) -> list[str]:
    """Pull every referenced visual name from either the short or explicit shape."""
    names: list[str] = []
    if "rows" in visuals_meta:
        for row_spec in visuals_meta.get("rows", []) or []:
            for item in row_spec.get("items", []) or []:
                if isinstance(item, str):
                    names.append(item)
                else:
                    names.append(item["visual"])
    elif "order" in visuals_meta:
        names.extend(visuals_meta.get("order", []) or [])
    return names


def _assert_project(project_root: Path) -> None:
    if not project_root.is_dir():
        print(f"Error: {project_root} is not a directory", file=sys.stderr)
        sys.exit(1)
    if not (project_root / "dashboard.yml").exists():
        print(f"Error: {project_root}/dashboard.yml not found — is this an dbr project?",
              file=sys.stderr)
        sys.exit(1)
