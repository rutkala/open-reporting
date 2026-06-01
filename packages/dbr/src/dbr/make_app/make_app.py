"""Build and run a Dash app for an Open Reporting domain.

`make_app(domain)` builds a Dash instance with the canonical URL prefix —
`"finance"` produces `/finance/`, matching the nginx `location` block
and systemd unit name. Setting `url_base_pathname` configures BOTH the
server-side route prefix and the client-side request prefix in one step.

`run_app(app, port)` starts the server on the host every Open Reporting
dashboard uses (`0.0.0.0`, so nginx can reach the upstream from the
Docker network).
"""
import subprocess
from functools import lru_cache
from pathlib import Path

from dash import Dash


@lru_cache(maxsize=1)
def build_sha() -> str:
    """Return the short git SHA of the repo this dbr install was loaded from.

    dbr is editable-installed from the repo working tree, so the SHA of
    HEAD at process-start time is exactly the framework code this running
    service is executing. Embedded as a ``<meta name="dbr-build">`` tag in
    every page (see ``_INDEX_STRING``) so a deploy can be *verified*: fetch
    the live page, read the stamp, compare to repo HEAD. If they differ the
    service is running stale code and the restart did not take effect.

    Cached: computed once per process. Returns ``"unknown"`` if git is
    unavailable (e.g. running outside a checkout).
    """
    # Walk up from this file to the repo root (dir containing .git).
    cur = Path(__file__).resolve()
    for parent in [cur, *cur.parents]:
        if (parent / ".git").exists():
            try:
                out = subprocess.run(
                    ["git", "rev-parse", "--short", "HEAD"],
                    cwd=parent, capture_output=True, text=True, timeout=5,
                )
                if out.returncode == 0:
                    return out.stdout.strip() or "unknown"
            except (OSError, subprocess.SubprocessError):
                return "unknown"
            break
    return "unknown"


_CSS = """
body { margin: 0; padding: 0; overflow: hidden; }

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

# Scrollspy that listens on the inner scrollable container (dbr-main-scroll),
# not on window — because the page itself does not scroll in the new layout.
# Nav link clicks are also intercepted to scroll the container smoothly.
_SCROLLSPY_JS = """
(function () {
  var SCROLL_ID = 'dbr-main-scroll';

  function initScrollspy() {
    var container = document.getElementById(SCROLL_ID);
    if (!container) { setTimeout(initScrollspy, 400); return; }

    var sections = container.querySelectorAll('h2[id]');
    var links    = document.querySelectorAll('.dbr-nav-link');
    if (!sections.length || !links.length) {
      setTimeout(initScrollspy, 400);
      return;
    }

    /* Intercept nav-link clicks: snap the WHOLE page (not just the heading) flush
       to the top of the scroll container so it shows fully, like opening a Power BI
       page. Prefer the page wrapper (dbr-section-<anchor>); fall back to the heading.
       getBoundingClientRect math is robust regardless of offsetParent chain. */
    links.forEach(function (a) {
      a.addEventListener('click', function (e) {
        e.preventDefault();
        var anchor = a.getAttribute('data-anchor');
        var target = document.getElementById('dbr-section-' + anchor) ||
                     document.getElementById(anchor);
        if (target && container) {
          var top = container.scrollTop +
                    (target.getBoundingClientRect().top - container.getBoundingClientRect().top);
          container.scrollTo({ top: top, behavior: 'smooth' });
        }
      });
    });

    var ticking = false;
    function update() {
      var scrollTop = container.scrollTop;
      var current   = sections[0] ? sections[0].id : '';
      for (var i = 0; i < sections.length; i++) {
        if (scrollTop >= sections[i].offsetTop - 130) { current = sections[i].id; }
      }
      links.forEach(function (a) {
        if (a.dataset.anchor === current) { a.classList.add('active'); }
        else                             { a.classList.remove('active'); }
      });
      ticking = false;
    }

    container.addEventListener('scroll', function () {
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

# Sidebar collapse toggle. Explicitly restores display values to their
# React-set originals (flex/block) rather than '' — resetting to '' would
# make the browser use the CSS default (block) for elements whose inline
# style is display:flex, breaking their internal centering.
_SIDEBAR_TOGGLE_JS = """
(function () {
  var KEY = 'dbr-sidebar-collapsed';

  function applyState(sidebar, btn, collapsed) {
    if (collapsed) {
      sidebar.classList.add('dbr-sidebar-collapsed');
      btn.textContent = '›';
      btn.title = 'Rozwiń panel';
      var badge  = document.getElementById('dbr-logo-badge');
      var name   = document.getElementById('dbr-logo-name');
      var nav    = document.getElementById('dbr-sidebar-nav');
      var footer = document.getElementById('dbr-sidebar-footer');
      if (badge)  badge.style.display  = 'none';
      if (name)   name.style.display   = 'none';
      if (nav)    nav.style.display    = 'none';
      if (footer) footer.style.display = 'none';
      var brand = document.getElementById('dbr-sidebar-brand');
      if (brand) brand.style.justifyContent = 'center';
    } else {
      sidebar.classList.remove('dbr-sidebar-collapsed');
      btn.textContent = '‹';
      btn.title = 'Zwiń panel';
      var badge  = document.getElementById('dbr-logo-badge');
      var name   = document.getElementById('dbr-logo-name');
      var nav    = document.getElementById('dbr-sidebar-nav');
      var footer = document.getElementById('dbr-sidebar-footer');
      /* Restore to their React-set inline display values, not '' (CSS default). */
      if (badge)  badge.style.display  = 'flex';
      if (name)   name.style.display   = 'block';
      if (nav)    nav.style.display    = 'flex';
      if (footer) footer.style.display = 'block';
      var brand = document.getElementById('dbr-sidebar-brand');
      if (brand) brand.style.justifyContent = '';
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
    "    <!--DBR_BUILD-->\n"
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
    # Stamp the running framework's git SHA into the page head so a deploy
    # can be verified end-to-end (live page advertises which commit it booted).
    build_meta = f'<meta name="dbr-build" content="{build_sha()}">'
    app.index_string = _INDEX_STRING.replace("<!--DBR_BUILD-->", build_meta)
    return app


def run_app(app: Dash, port: int) -> None:
    app.run(host="0.0.0.0", port=port)
