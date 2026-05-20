"""JSON Schemas for or-dashboards project YAMLs.

Schemas are JSON Schema 2020-12 files shipped with the package. The
loader function below returns a parsed schema by name; the CLI's
`validate` command applies them to YAML files at the matching paths.

Files:
  dashboard.schema.json  — root dashboard.yml
  pages.schema.json      — pages/pages.yml
  page.schema.json       — pages/<name>/page.yml
  visuals.schema.json    — pages/<name>/visuals/visuals.yml
  visual.schema.json     — pages/<name>/visuals/<visual>.yml

For editor auto-complete: configure yaml-language-server to point each
file at the matching schema (e.g. via VS Code `yaml.schemas` setting or
`# yaml-language-server: $schema=…` comments in the YAML files).
"""
from __future__ import annotations

import json
from pathlib import Path

_SCHEMAS_DIR = Path(__file__).parent


def load_schema(name: str) -> dict:
    """Load a packaged schema by short name (without `.schema.json`)."""
    path = _SCHEMAS_DIR / f"{name}.schema.json"
    return json.loads(path.read_text())


__all__ = ["load_schema"]
