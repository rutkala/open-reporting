# Open Reporting — Project Vision

## What We Build

Open Reporting is a one-person data media company turning Polish public data into accessible, beautiful, and useful products. We believe public data should be understandable by everyone, not just researchers and civil servants.

## Four Product Lines

### 1. Analytical Portal (`portal.open-reporting.dev`)
Dashboards built from Polish public datasets, authored declaratively in YAML using the **dbr** framework (Plotly + MetricFlow over DuckDB). dbr compiles each dashboard and **pre-renders it to static HTML** (`dbr build`), served directly by nginx — no always-on backend (OR-168). Charts keep Plotly's client-side interactivity (hover/zoom); server-driven interactivity (cross-filter, slicers) is on hold to conserve VPS resources. One folder per domain dashboard under `products/dashboards/`.

### 2. Content Portal / Blog (`www.open-reporting.dev`)
Data-driven articles and analyses powered by Ghost CMS. Long-form content explaining what the numbers mean, not just what they are.

### 3. Mobile App (future phase)
Not in active development. Future intent is mobile-responsive dashboards built on the same dbr framework — same declarative YAML targeting both desktop and mobile.

### 4. Social Media
Short-form content derived from dashboards and articles. LinkedIn, X, Instagram. Charts adapted for vertical formats.

## Guiding Principles

- **Accessible** — Polish public data explained in plain language
- **Beautiful** — Charts that people want to share
- **Accurate** — Source attribution always visible, methodology transparent
- **Declarative** — Dashboards, metrics, and pipelines authored in YAML/SQL wherever possible; Python only where genuinely required

## Current Status (May 2026)

Infrastructure is live (Docker Compose on Hetzner VPS). First dbr dashboard published: Public Finance (`portal.open-reporting.dev/public_finance/`). Repository follows a two-plane architecture — see [`ARCHITECTURE.md`](ARCHITECTURE.md).

## Target Audience

Polish citizens who want to understand public finances, health statistics, labour market, and economic indicators without reading government reports.
