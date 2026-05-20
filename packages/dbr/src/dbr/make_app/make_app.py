"""Build and run a Dash app for an Open Reporting domain.

`make_app(domain)` builds a Dash instance with the canonical URL prefix —
`"finance"` produces `/finance/`, matching the nginx `location` block
and systemd unit name. Setting `url_base_pathname` configures BOTH the
server-side route prefix and the client-side request prefix in one step.

`run_app(app, port)` starts the server on the host every Open Reporting
dashboard uses (`0.0.0.0`, so nginx can reach the upstream from the
Docker network).
"""
from dash import Dash


def make_app(domain: str) -> Dash:
    return Dash(url_base_pathname=f"/{domain}/")


def run_app(app: Dash, port: int) -> None:
    app.run(host="0.0.0.0", port=port)
