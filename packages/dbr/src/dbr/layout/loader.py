"""Layout loader — reads layout.yaml and exposes chrome-behaviour flags.

On import:
  1. Loads the package's default ``layout.yaml`` (immutable, ships with the kit).
  2. If env var ``DBR_PROJECT_ROOT`` is set and the project has its
     own ``layout.yaml``, deep-merges it on top of the defaults.
  3. Exposes each behaviour flag as a module-level constant.

Visual tokens (colours, fonts, paddings) come from ``theme`` — NOT from
this loader. Layout YAML only controls structural behaviour (enabled/
disabled, position).

Other layout files (``sidebar.py``, ``page_shell.py``) read these
constants and adjust their output accordingly.

The env var must be set BEFORE any ``dbr`` import.
"""
import os
from pathlib import Path

import yaml


def _deep_merge(base: dict, override: dict) -> dict:
    """Recursive dict merge — override wins on leaf-key collisions."""
    result = dict(base)
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


_PACKAGE_DEFAULTS = yaml.safe_load((Path(__file__).parent / "layout.yaml").read_text())
_DATA = _PACKAGE_DEFAULTS

_project_root = os.environ.get("DBR_PROJECT_ROOT")
if _project_root:
    _override_path = Path(_project_root) / "layout.yaml"
    if _override_path.exists():
        _override = yaml.safe_load(_override_path.read_text()) or {}
        _DATA = _deep_merge(_PACKAGE_DEFAULTS, _override)

_SIDEBAR = _DATA["sidebar"]
_HEADER  = _DATA.get("header", {})
_FOOTER  = _DATA.get("footer", {})

# ── Sidebar behaviour ──────────────────────────────────────────────────
SIDEBAR_ENABLED      = _SIDEBAR["enabled"]
SIDEBAR_POSITION     = _SIDEBAR["position"]      # "left" | "right"
SIDEBAR_SHOW_TOGGLE  = _SIDEBAR.get("show_toggle", True)
SIDEBAR_SHOW_TITLE   = _SIDEBAR.get("show_title", True)

# ── Header behaviour ───────────────────────────────────────────────────
HEADER_ENABLED    = _HEADER.get("enabled", False)
HEADER_SHOW_TITLE = _HEADER.get("show_title", True)

# ── Footer behaviour ───────────────────────────────────────────────────
FOOTER_ENABLED      = _FOOTER.get("enabled", False)
FOOTER_SHOW_SOURCE  = _FOOTER.get("show_source", True)
FOOTER_SHOW_UPDATED = _FOOTER.get("show_updated", True)
