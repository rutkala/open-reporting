#!/usr/bin/env python3
"""Visual-component showroom — example entry point.

Single-page Dash app demonstrating every chart family + slicer wired
through the skill's runtime helpers. Runs on port 8060 under
``/example/``.

The full layout (41 sections, sample data, sidebar nav, palette
reference) lives in ``showroom.py`` so any caller — this file or
``products/dashboards/template/app.py`` — gets the same showroom.

Run:
    PYTHONPATH=/opt/open-reporting:/opt/open-reporting/.claude/skills \\
    python3 .claude/skills/complex_dashboard/assets/example/app.py

Then open http://localhost:8060/example/.
"""
from complex_dashboard.assets.example.showroom import build_showroom_app
from complex_dashboard.assets.runtime import register_healthcheck


PORT = 8060

app = build_showroom_app(domain="example", module_name=__name__)
register_healthcheck(app)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=False)
