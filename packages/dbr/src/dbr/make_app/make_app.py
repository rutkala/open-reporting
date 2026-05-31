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

_CSS = """
html { scroll-behavior: smooth; }
body { margin: 0; padding: 0; }

/* Sidebar nav link hover + active states (augment Dash inline styles) */
.dbr-nav-link {
  transition: color 0.15s ease, background-color 0.15s ease;
}
.dbr-nav-link:hover {
  color: #4A7FB5 !important;
  background-color: rgba(74, 127, 181, 0.07) !important;
  border-radius: 0 6px 6px 0;
}
.dbr-nav-link.active {
  color: #4A7FB5 !important;
  font-weight: 600 !important;
  background-color: rgba(74, 127, 181, 0.09) !important;
  border-left: 3px solid #4A7FB5 !important;
  padding-left: 17px !important;
}
"""

_SCROLLSPY_JS = """
(function () {
  function initScrollspy() {
    var sections = document.querySelectorAll('h2[id]');
    var links    = document.querySelectorAll('.dbr-nav-link');
    if (!sections.length || !links.length) {
      setTimeout(initScrollspy, 400);
      return;
    }
    var ticking = false;
    function update() {
      var scrollY  = window.pageYOffset || document.documentElement.scrollTop;
      var current  = sections[0] ? sections[0].id : '';
      for (var i = 0; i < sections.length; i++) {
        if (scrollY >= sections[i].offsetTop - 130) { current = sections[i].id; }
      }
      links.forEach(function (a) {
        if (a.dataset.anchor === current) { a.classList.add('active'); }
        else { a.classList.remove('active'); }
      });
      ticking = false;
    }
    window.addEventListener('scroll', function () {
      if (!ticking) { requestAnimationFrame(update); ticking = true; }
    }, { passive: true });
    update();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { setTimeout(initScrollspy, 600); });
  } else {
    setTimeout(initScrollspy, 600);
  }
})();
"""

_INDEX_STRING = (
    "<!DOCTYPE html>\n"
    "<html>\n"
    "  <head>\n"
    "    {%metas%}\n"
    "    <title>{%title%}</title>\n"
    "    {%favicon%}\n"
    "    {%css%}\n"
    "    <style>" + _CSS + "</style>\n"
    "  </head>\n"
    "  <body>\n"
    "    {%app_entry%}\n"
    "    <footer>\n"
    "      {%config%}\n"
    "      {%scripts%}\n"
    "      {%renderer%}\n"
    "    </footer>\n"
    "    <script>" + _SCROLLSPY_JS + "</script>\n"
    "  </body>\n"
    "</html>\n"
)


def make_app(domain: str, title: str = "") -> Dash:
    app = Dash(
        url_base_pathname=f"/{domain}/",
        suppress_callback_exceptions=True,
    )
    app.title = title or domain
    app.index_string = _INDEX_STRING
    return app


def run_app(app: Dash, port: int) -> None:
    app.run(host="0.0.0.0", port=port)
