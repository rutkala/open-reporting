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

/* ──────────────────────────────────────────────────────────────────────────
   MOBILE (≤768px) — break out of the desktop fixed-canvas model.

   The desktop layout is a Power BI–style fixed canvas: the outer shell is
   height:100vh + overflow:hidden, each section is exactly one viewport tall,
   and rows are horizontal flex tracks whose chart heights come from a definite
   -height cascade (grow row → item height:100% → card height:100% → graph
   flex:1). On a phone that model crushes every chart to an unreadable sliver
   and clips the footer. These rules (CSS !important beats Dash inline styles)
   convert the page to a single natural-flow document that the BODY scrolls:
     - the sidebar becomes a FIXED, always-visible narrow rail (48px) pinned to
       the left edge — it stays on screen while the content scrolls. Nav labels
       collapse to numbered badges (a pure-CSS counter), so navigation is always
       reachable yet costs almost no horizontal space — the content gets the rest
       of the width for comfortable reading (the PO's priority).
     - the content column clears the rail with a left margin and flows as plain
       blocks; each section grows to its content instead of being one viewport
     - rows stack to one-visual-per-line, full width
     - fill-charts (which lose their definite-height chain once rows stack) get
       an explicit mobile height via .dbr-fill-graph; companion-table charts
       keep their baked figure height and simply reflow to full width
   Because the BODY scrolls (not the #dbr-main-scroll container), the scrollspy
   and nav-click handlers are rect-based and listen on BOTH the container and the
   window — see _SCROLLSPY_JS. The collapse-toggle logic is disabled on mobile
   (the rail IS the collapsed form) — see _SIDEBAR_TOGGLE_JS.
   See packages/dbr/src/dbr/layout/page_shell.py for the className hooks.
   ────────────────────────────────────────────────────────────────────────── */
@media (max-width: 768px) {
  /* Let the VIEWPORT be the scroller — NOT html/body. Setting overflow-y:auto on
     body makes it a scroll container, but with height:auto it never actually
     scrolls (the document does), so position:sticky inside it has no scrollport to
     stick to and the sticky section bar just scrolls away. overflow:visible keeps
     body out of the scroll-container role so the bar sticks to the viewport. (The
     desktop base rule `body{overflow:hidden}` is overridden here.) Horizontal
     overflow is prevented by the content sizing rules below, not by clipping. */
  html, body {
    overflow: visible !important;
    height: auto      !important;
  }

  html { scroll-behavior: smooth; }

  /* Outer shell: the sidebar is taken out of flow (position:fixed), so the outer
     becomes a plain block whose only in-flow child is the content column. No
     padding/gap — the rail sits flush to the viewport edge and the content
     column owns its own insets. */
  .dbr-page-outer {
    display: block    !important;
    height: auto      !important;
    min-height: 100vh !important;
    overflow: visible !important;
    padding: 0        !important;
    gap: 0            !important;
  }

  /* Sidebar → FIXED narrow rail, pinned to the left edge, always visible while
     the content scrolls past it. 48px wide: just enough for the OR badge + the
     numbered nav dots. */
  #dbr-sidebar {
    position: fixed   !important;
    top: 0            !important;
    left: 0           !important;
    bottom: 0         !important;
    width: 48px       !important;
    min-width: 48px   !important;
    height: 100vh     !important;
    z-index: 100      !important;
    overflow-y: auto  !important;
    overflow-x: hidden!important;
    border-right: 1px solid #D8E0E6 !important;
    border-radius: 0  !important;
  }
  /* Brand: centre the OR badge, drop the wordmark + toggle */
  #dbr-sidebar-brand { padding: 10px 0 !important; min-height: 48px !important;
                       justify-content: center !important; }
  #dbr-logo-row      { justify-content: center !important; gap: 0 !important; }
  #dbr-logo-name     { display: none !important; }
  #dbr-sidebar-toggle{ display: none !important; }

  /* Nav: a centred vertical stack of numbered badges (pure-CSS counter). The
     section labels are hidden — the badge number + the active highlight (driven
     by the scrollspy) carry the navigation. */
  .dbr-nav-label      { display: none !important; }
  #dbr-sidebar-nav    { padding: 10px 0 !important; flex: 1 1 auto !important; }
  #dbr-sidebar-nav nav {
    flex-direction: column !important;
    align-items: center    !important;
    gap: 8px               !important;
    counter-reset: dbrnav;
  }
  .dbr-nav-link {
    display: flex          !important;
    align-items: center    !important;
    justify-content: center!important;
    width: 30px            !important;
    height: 30px           !important;
    padding: 0             !important;
    border-left: none      !important;
    border-radius: 50%     !important;
    background-color: rgba(85, 161, 170, 0.10) !important;
    font-size: 0           !important;   /* hide the label text … */
    color: transparent     !important;
  }
  .dbr-nav-link::before {
    counter-increment: dbrnav;
    content: counter(dbrnav);            /* … and show the section number instead */
    font-size: 13px;
    font-weight: 600;
    color: #6B7A85;
  }
  /* id prefix raises specificity above the desktop `.dbr-nav-link.active` rule
     later in the sheet (equal-specificity + !important would otherwise let the
     later desktop rule win on source order, leaking its pale bg / border-left /
     padding-left and turning the dot into a pale oval). */
  #dbr-sidebar-nav .dbr-nav-link.active {
    background-color: #55A1AA !important;
    border-left: none        !important;
    padding-left: 0          !important;
    font-weight: 600         !important;
  }
  #dbr-sidebar-nav .dbr-nav-link.active::before { color: #FFFFFF; }
  /* The section name is surfaced by the sticky #dbr-mobile-section-bar at the top
     of the content (see below + the scrollspy JS) — the numbered dots stay a clean
     jump-strip, with the active one highlighted. */

  /* Footer: portal back-link collapses to a single ← glyph, centred */
  #dbr-sidebar-footer { padding: 0 !important; min-height: 44px !important;
                        justify-content: center !important; }
  #dbr-sidebar-footer a       { font-size: 0 !important; gap: 0 !important; }
  #dbr-sidebar-footer a::before { content: "←"; font-size: 16px; color: #6B7A85; }

  /* Content column: clear the fixed rail, then flow as plain blocks (drop the
     header/scroll/footer grid) so the BODY scrolls the whole document. */
  .dbr-right-col {
    margin-left: 48px !important;
    display: block    !important;
    overflow: visible !important;
    border-radius: 0  !important;
  }
  #dbr-main-scroll {
    overflow: visible       !important;
    scroll-snap-type: none  !important;
  }

  /* Sticky section-name bar: pinned to the top of the content as you scroll, it
     always names the current section (the scrollspy JS rewrites its text). Opaque
     white so content scrolls cleanly underneath; sits right of the 48px rail. */
  .dbr-mobile-section-bar {
    display: block   !important;
    position: sticky !important;
    top: 0           !important;
    z-index: 90      !important;
    background: #FFFFFF !important;
    color: #2D3339   !important;
    font-size: 14px  !important;
    font-weight: 600 !important;
    padding: 12px 16px !important;
    margin: 0 0 4px 0  !important;
    border-bottom: 1px solid #D8E0E6 !important;
    box-shadow: 0 2px 6px rgba(45, 51, 57, 0.06) !important;
  }

  /* Each section: grow to its content instead of one fixed viewport.
     display:block (not flex-column) is essential — as a flex column the page
     body keeps its flex:1 1 0 (basis 0) and collapses to ~0 once the section is
     content-sized, leaving every chart to overflow and overlap. Block flow lets
     heading + body + rows stack at their natural heights. */
  .dbr-page-section {
    display: block           !important;
    height: auto             !important;
    min-height: 0            !important;
    overflow: visible        !important;
    scroll-snap-align: none  !important;
    padding: 16px            !important;
  }
  .dbr-page-body {
    display: block    !important;
    flex: none        !important;
    overflow: visible !important;
  }

  /* Rows stack vertically; each visual takes the full width */
  .dbr-row {
    flex-direction: column !important;
    flex: 0 0 auto         !important;
    min-height: 0          !important;
    margin-bottom: 16px    !important;
  }
  .dbr-visual-item {
    width: 100%      !important;
    flex: 0 0 auto   !important;
    height: auto     !important;
    min-height: 0    !important;
    min-width: 0     !important;
  }

  /* KPI rows (fixed, non-grow) reflow to a 2-up grid instead of stacking 1-per-
     line — halves the scroll before the first chart. auto-fit + minmax means the
     card count drives the columns: 4 cards → 2×2, 2 → side-by-side, 1 → full
     width. align-items:stretch (grid default) keeps cards in a row equal height. */
  .dbr-row-fixed {
    display: grid !important;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)) !important;
    gap: 10px !important;
  }
  .dbr-row-fixed .dbr-visual-item { width: auto !important; }
  /* The KPI value is baked at 32px for the full-width desktop card; at ~150px
     grid width it would wrap. Scale it down (and tighten padding) for the grid. */
  .dbr-row-fixed .dbr-kpi-value { font-size: 23px !important; }
  .dbr-row-fixed .dbr-kpi-card  { padding: 14px !important; }

  /* Fill-charts lose their definite-height parent once rows stack — pin an
     explicit, readable mobile height. Companion-table charts are NOT tagged
     .dbr-fill-graph (they keep their baked figure height) so they are untouched
     and simply reflow to full width. KPI cards are plain divs and size to text. */
  .dbr-fill-graph {
    height: 320px     !important;
    min-height: 320px !important;
    flex: none        !important;
  }

  /* Wide tables shrink their type rather than forcing horizontal overflow */
  .dbr-visual-item table { font-size: 12px; }
}

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

    /* The sticky mobile section bar (visible only ≤768px). When shown it overlaps
       the top of the content, so click-scroll targets are offset by its height to
       keep a tapped section's heading clear of it. */
    var bar = document.getElementById('dbr-mobile-section-bar');
    function barOffset() {
      return (bar && bar.offsetParent !== null) ? bar.offsetHeight : 0;
    }

    /* The desktop layout scrolls the #dbr-main-scroll container; the mobile
       layout (≤768px) lets the BODY scroll instead (the container is
       overflow:visible). Detect which is live so the click + spy logic works in
       both modes. */
    function containerScrolls() {
      return container.scrollHeight > container.clientHeight + 2;
    }

    /* Intercept nav-link clicks: snap the WHOLE page (not just the heading) flush
       to the top so it shows fully, like opening a Power BI page. Prefer the page
       wrapper (dbr-section-<anchor>); fall back to the heading. getBoundingClientRect
       math is robust regardless of offsetParent chain — and scrolls the container
       (desktop) or the window (mobile) depending on which one actually scrolls. */
    links.forEach(function (a) {
      a.addEventListener('click', function (e) {
        e.preventDefault();
        var anchor = a.getAttribute('data-anchor');
        var target = document.getElementById('dbr-section-' + anchor) ||
                     document.getElementById(anchor);
        if (!target) { return; }
        if (containerScrolls()) {
          var top = container.scrollTop +
                    (target.getBoundingClientRect().top - container.getBoundingClientRect().top);
          container.scrollTo({ top: top, behavior: 'smooth' });
        } else {
          var wtop = window.pageYOffset + target.getBoundingClientRect().top - barOffset() - 8;
          window.scrollTo({ top: wtop, behavior: 'smooth' });
        }
      });
    });

    var ticking = false;
    /* Rect-based active detection: a heading's getBoundingClientRect().top is
       viewport-relative, so the same test works whether the container or the
       window is the scroller. The section nearest the top (within 140px) wins. */
    function update() {
      var current = sections[0] ? sections[0].id : '';
      var currentEl = sections[0] || null;
      for (var i = 0; i < sections.length; i++) {
        if (sections[i].getBoundingClientRect().top <= 140) {
          current = sections[i].id;
          currentEl = sections[i];
        }
      }
      links.forEach(function (a) {
        if (a.dataset.anchor === current) { a.classList.add('active'); }
        else                             { a.classList.remove('active'); }
      });
      // Keep the sticky mobile bar naming the current section.
      if (bar && currentEl) {
        var name = currentEl.textContent;
        if (bar.textContent !== name) { bar.textContent = name; }
      }
      ticking = false;
    }

    function onScroll() {
      if (!ticking) { requestAnimationFrame(update); ticking = true; }
    }
    container.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('scroll', onScroll, { passive: true });
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

    /* On mobile (≤768px) the sidebar is already the always-visible narrow rail —
       the CSS handles it. Skip the collapse logic entirely: a stored desktop
       `collapsed=true` would otherwise inline display:none onto the nav/footer
       and beat the rail's CSS, leaving an empty strip. */
    if (window.matchMedia('(max-width: 768px)').matches) { return; }

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
        # Without an explicit device-width viewport, mobile browsers render the
        # page at a 980px desktop canvas and zoom out — text and charts become
        # unreadably small. This makes the @media (max-width:768px) rules in
        # _CSS actually engage on real phones.
        meta_tags=[
            {"name": "viewport", "content": "width=device-width, initial-scale=1"},
        ],
    )
    app.title = title or domain
    # Stamp the running framework's git SHA into the page head so a deploy
    # can be verified end-to-end (live page advertises which commit it booted).
    build_meta = f'<meta name="dbr-build" content="{build_sha()}">'
    app.index_string = _INDEX_STRING.replace("<!--DBR_BUILD-->", build_meta)
    return app


def run_app(app: Dash, port: int) -> None:
    app.run(host="0.0.0.0", port=port)
