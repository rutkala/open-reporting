# Test_Dashboard dashboard

Authored with [dbr](https://github.com/your-org/dbr).

## Run locally

```bash
dbr run .
```

## Add a page

1. `mkdir pages/<name>`
2. Add `pages/<name>/page.yml` with `title` and `anchor`.
3. Add `pages/<name>/visuals/visuals.yml` listing the visual order.
4. Add one `pages/<name>/visuals/<visual>.yml` per visual.
5. Add the page name to `pages/pages.yml` under `order:`.
