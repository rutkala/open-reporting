# Tableau Public Viz of the Day — Article Text

Source: https://public.tableau.com/app/discover/viz-of-the-day
Fetched: 2026-05-25
Status: DROPPED — access fully blocked

## Access Failure Log

- WebFetch to public.tableau.com returns HTTP 403 (Cloudflare WAF)
- Playwright (Chromium headless, Playwright 1.58.0) to public.tableau.com returns "ERROR: The request could not be satisfied" — Cloudflare bot detection blocks headless browsers
- Secondary Playwright attempts to /app/gallery and /app/profile/sheets/featured — same block
- Individual viz embed URL (COVID viz) — same block
- No user-agent spoofing resolves this without additional browser fingerprint infrastructure

## Known Context (from prior knowledge, not from capture)

Tableau Public hosts hundreds of thousands of community-authored vizzes. The "Viz of the Day" programme selects 1 featured viz per day. Common types in the gallery:
- Geographic choropleth maps
- Multi-panel analytical dashboards
- Scrollytelling with embedded Tableau views
- Custom colour schemes and non-standard chart types (Sankey, hex maps, radial charts)

The gallery is particularly known for creative use of Tableau's calculated fields to produce chart types not natively available (e.g., bump charts, slope charts, waffle charts).

## Wave 3 Recommendation

Download 3-5 featured viz thumbnails from public.tableau.com via a residential proxy or by fetching from a secondary aggregator (e.g., The Information Lab blog, Tableau Ambassador portfolios). The gallery thumbnails use the pattern: `public.tableau.com/static/images/<workbook-hash>/<viz-name>/1_rss.png` — direct URL fetch of known thumbnail hashes may succeed where the main page does not.
