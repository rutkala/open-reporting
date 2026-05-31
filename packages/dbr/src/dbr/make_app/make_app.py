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

/* Sidebar toggle button */
#dbr-sidebar-toggle {
  transition: background-color 0.15s ease, color 0.15s ease;
}
#dbr-sidebar-toggle:hover {
  background-color: rgba(74, 127, 181, 0.08) !important;
  color: #4A7FB5 !important;
}

/* Collapsed sidebar: !important overrides React inline style */
#dbr-sidebar.dbr-sidebar-collapsed {
  width: 52px !important;
  min-width: 52px !important;
}
/* When collapsed the logo row contains only the toggle; center it */
#dbr-sidebar.dbr-sidebar-collapsed #dbr-logo-row {
  justify-content: center;
}
#dbr-sidebar.dbr-sidebar-collapsed #dbr-sidebar-toggle {
  margin-left: 0 !important;
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

_SIDEBAR_TOGGLE_JS = """
(function () {
  var KEY = 'dbr-sidebar-collapsed';

  function applyState(sidebar, btn, collapsed) {
    if (collapsed) {
      sidebar.classList.add('dbr-sidebar-collapsed');
      btn.textContent = '›';
      btn.title = 'Rozwiń panel';
      /* Brand header stays visible (it holds the toggle button).
         Hide only the OR badge, wordmark, and dashboard title so the
         toggle button remains alone in the logo row. */
      var badge = document.getElementById('dbr-logo-badge');
      var name  = document.getElementById('dbr-logo-name');
      var title = document.getElementById('dbr-dash-title');
      var nav    = document.getElementById('dbr-sidebar-nav');
      var footer = document.getElementById('dbr-sidebar-footer');
      if (badge)  badge.style.display  = 'none';
      if (name)   name.style.display   = 'none';
      if (title)  title.style.display  = 'none';
      if (nav)    nav.style.display    = 'none';
      if (footer) footer.style.display = 'none';
      /* Tighten brand padding so the lone toggle isn't floating in dead space */
      var brand = document.getElementById('dbr-sidebar-brand');
      if (brand) brand.style.padding = '12px 8px';
    } else {
      sidebar.classList.remove('dbr-sidebar-collapsed');
      btn.textContent = '‹';
      btn.title = 'Zwiń panel';
      var badge = document.getElementById('dbr-logo-badge');
      var name  = document.getElementById('dbr-logo-name');
      var title = document.getElementById('dbr-dash-title');
      var nav    = document.getElementById('dbr-sidebar-nav');
      var footer = document.getElementById('dbr-sidebar-footer');
      if (badge)  badge.style.display  = '';
      if (name)   name.style.display   = '';
      if (title)  title.style.display  = '';
      if (nav)    nav.style.display    = '';
      if (footer) footer.style.display = '';
      var brand = document.getElementById('dbr-sidebar-brand');
      if (brand) brand.style.padding = '';
    }
  }

  function initSidebarToggle() {
    var sidebar = document.getElementById('dbr-sidebar');
    var btn     = document.getElementById('dbr-sidebar-toggle');
    if (!sidebar || !btn) { setTimeout(initSidebarToggle, 400); return; }

    var collapsed = localStorage.getItem(KEY) === 'true';
    applyState(sidebar, btn, collapsed);

    btn.addEventListener('click', function () {
      collapsed = !collapsed;
      localStorage.setItem(KEY, String(collapsed));
      applyState(sidebar, btn, collapsed);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { setTimeout(initSidebarToggle, 600); });
  } else {
    setTimeout(initSidebarToggle, 600);
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
    "    <script>" + _SIDEBAR_TOGGLE_JS + "</script>\n"
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
