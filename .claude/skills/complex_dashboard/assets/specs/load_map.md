# Load map — which spec to read for which task

When you (or Claude) start work on a dashboard, load only the specs
relevant to the task — not the whole `specs/` tree. This map lists
the trigger and the minimum spec set per task type.

## Starting a new dashboard from scratch

Read in order:

1. [`../README.md`](../README.md) — tri-modal map, quickstart copy commands
2. [`page_layout.md`](page_layout.md) — section block shape
3. [`layout/header.md`](layout/header.md) and [`layout/footer.md`](layout/footer.md) — both required
4. [`layout/styles.md`](layout/styles.md) — `S` dict tokens
5. [`controls/navigation/sidebar_nav.md`](controls/navigation/sidebar_nav.md) — single-page or multi-page nav
6. [`data/data_loaders.md`](data/data_loaders.md) — loader contract
7. [`deploy/app_init.md`](deploy/app_init.md) — `make_app(...)` kwargs

## Adding a new chart

1. [`chart_types.md`](chart_types.md) — pick the family
2. The relevant `visuals/<family>/*.md`
3. [`theme/colours.md`](theme/colours.md) if the chart uses semantic colour
4. [`page_layout.md`](page_layout.md) — fitting the chart into a section's grid

## Adding a slicer

1. [`controls/slicers/`](controls/slicers/) — pick the slicer type
2. [`page_layout.md`](page_layout.md) — placement above the affected charts
3. [`data/data_loaders.md`](data/data_loaders.md) — slicer triggers callbacks that read pre-loaded frames; never re-queries

## Switching to multi-page

1. [`controls/navigation/sidebar_nav.md`](controls/navigation/sidebar_nav.md) — `from_page_registry=True` mode
2. [`deploy/app_init.md`](deploy/app_init.md) — `use_pages=True` and `pages_folder` kwargs
3. [`../scaffolds/pages/_README.md`](../scaffolds/pages/_README.md) — workflow for `pages/*.py`

## Wiring deployment

1. [`deploy/deploy.md`](deploy/deploy.md) — systemd + nginx
2. [`deploy/observability.md`](deploy/observability.md) — logging + healthcheck
3. [`config.md`](config.md) — env-var contract

## Writing tests

1. [`testing.md`](testing.md) — what each scaffold covers, fixture model
2. [`../scaffolds/tests/`](../scaffolds/tests/) — copy the templates

## Reviewing a dashboard PR

1. [`page_layout.md`](page_layout.md) — section structure correctness
2. The relevant `visuals/<family>/*.md` for each chart in the diff
3. [`layout/footer.md`](layout/footer.md) — confirms `source` / `updated` are real, not TODO
4. Project standards, separately: `team/standards/build/visualisation.md`,
   `team/standards/evaluation/visualization-diff.md`,
   `team/standards/evaluation/visualization-image.md`
