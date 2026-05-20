"""Command-line interface for or-dashboards.

Subcommands:

    or-dashboard init <name>      scaffold a new dashboard project in ./<name>/
    or-dashboard run <path>       start the Dash server for the dashboard at <path>
    or-dashboard validate <path>  schema-check the YAMLs without starting the server
    or-dashboard compile <path>   print the resolved layout tree (debug)

Registered as a console-script entry point in pyproject.toml:

    [project.scripts]
    or-dashboard = "or_dashboards.cli:main"
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="or-dashboard",
        description="Declarative YAML dashboard framework.",
    )
    sub = parser.add_subparsers(dest="cmd", required=True, metavar="command")

    p_init = sub.add_parser("init", help="Scaffold a new dashboard project")
    p_init.add_argument("name", help="Project name (also used as URL prefix / domain)")

    p_run = sub.add_parser("run", help="Start the Dash server")
    p_run.add_argument("path", nargs="?", default=".",
                       help="Path to the dashboard project (default: .)")

    p_validate = sub.add_parser("validate", help="Schema-check YAMLs without starting the server")
    p_validate.add_argument("path", nargs="?", default=".",
                            help="Path to the dashboard project (default: .)")

    p_compile = sub.add_parser("compile", help="Print the resolved layout tree (debug)")
    p_compile.add_argument("path", nargs="?", default=".",
                           help="Path to the dashboard project (default: .)")

    args = parser.parse_args(argv)

    dispatch = {
        "init":     cmd_init,
        "run":      cmd_run,
        "validate": cmd_validate,
        "compile":  cmd_compile,
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
        "# BEFORE `or_dashboards` is imported.\n"
        "os.environ.setdefault(\"OR_DASHBOARDS_PROJECT_ROOT\", str(Path(__file__).resolve().parent))\n"
        "\n"
        "from or_dashboards.compiler import run_dashboard\n"
        "\n"
        "run_dashboard(__file__)\n"
    )

    (root / "dashboard.yml").write_text(
        "# Open Reporting dashboard root config.\n"
        "# Only `domain` and `port` are required; other keys inherit kit defaults.\n"
        "\n"
        f"domain: {name}\n"
        "port:   8055\n"
        f"title:  {name.title()}\n"
    )

    (root / "pages" / "pages.yml").write_text(
        "# Page order — list pages in the order they appear in the sidebar.\n"
        "# Each entry must match a sibling folder containing `page.yml`.\n"
        "\n"
        "order: []\n"
    )

    (root / "README.md").write_text(
        f"# {name.title()} dashboard\n"
        "\n"
        "Authored with [or-dashboards](https://github.com/your-org/or-dashboards).\n"
        "\n"
        "## Run locally\n"
        "\n"
        "```bash\n"
        "or-dashboard run .\n"
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
    print(f"Next: cd {name} && or-dashboard run .")
    return 0


# ── run ────────────────────────────────────────────────────────────────────────

def cmd_run(args: argparse.Namespace) -> int:
    import os

    project_root = Path(args.path).resolve()
    _assert_project(project_root)
    # Tell the theme + layout loaders where this project lives, so they
    # can pick up optional theme.yaml / layout.yaml overrides. Must be
    # set BEFORE the or_dashboards.compiler import below.
    os.environ["OR_DASHBOARDS_PROJECT_ROOT"] = str(project_root)

    from or_dashboards.compiler import run_dashboard
    run_dashboard(project_root)
    return 0  # never reached — app.run blocks


# ── validate ───────────────────────────────────────────────────────────────────

def cmd_validate(args: argparse.Namespace) -> int:
    """Light-touch schema checks. Real jsonschema validation lands later."""
    import yaml

    from or_dashboards.visuals import VISUAL_REGISTRY

    project_root = Path(args.path).resolve()
    _assert_project(project_root)
    errors: list[str] = []

    config = yaml.safe_load((project_root / "dashboard.yml").read_text()) or {}
    for required in ("domain", "port"):
        if required not in config:
            errors.append(f"dashboard.yml missing required key: {required}")

    pages_dir = project_root / "pages"
    pages_meta_path = pages_dir / "pages.yml"
    if not pages_meta_path.exists():
        errors.append("pages/pages.yml missing")
    else:
        pages_meta = yaml.safe_load(pages_meta_path.read_text()) or {}
        for page_name in pages_meta.get("order", []) or []:
            page_dir = pages_dir / page_name
            if not (page_dir / "page.yml").exists():
                errors.append(f"pages/{page_name}/page.yml missing (referenced in pages.yml order)")
                continue
            visuals_dir = page_dir / "visuals"
            visuals_meta_path = visuals_dir / "visuals.yml"
            if not visuals_meta_path.exists():
                continue  # empty page is valid
            visuals_meta = yaml.safe_load(visuals_meta_path.read_text()) or {}
            visual_names = _extract_visual_names(visuals_meta)
            for visual_name in visual_names:
                visual_path = visuals_dir / f"{visual_name}.yml"
                if not visual_path.exists():
                    errors.append(f"pages/{page_name}/visuals/{visual_name}.yml missing")
                    continue
                spec = yaml.safe_load(visual_path.read_text()) or {}
                vtype = spec.get("type")
                if vtype is None:
                    errors.append(f"pages/{page_name}/visuals/{visual_name}.yml missing 'type'")
                elif vtype not in VISUAL_REGISTRY:
                    available = ", ".join(sorted(VISUAL_REGISTRY)) or "<none registered>"
                    errors.append(
                        f"pages/{page_name}/visuals/{visual_name}.yml: unknown visual type "
                        f"{vtype!r}. Available: {available}"
                    )

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
    from or_dashboards.compiler.compiler import _load_pages, _load_yaml

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
        print(f"Error: {project_root}/dashboard.yml not found — is this an or-dashboards project?",
              file=sys.stderr)
        sys.exit(1)
