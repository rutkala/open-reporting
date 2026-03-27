# Social Media Publishing Playbook

Covers: Instagram (`@otwarteraporty`) — other platforms TBD.

---

## Platform Setup

| Platform | Account | App | User ID |
|----------|---------|-----|---------|
| Instagram | @otwarteraporty | Otwarte Raporty (ID: 1334119365407244) | 26290813287238381 |

**Credentials** (in `.env`):
- `INSTAGRAM_APP_ID` — Meta Developer app ID
- `INSTAGRAM_APP_SECRET` — Meta Developer app secret
- `INSTAGRAM_ACCESS_TOKEN` — Instagram user token (valid ~60 days, must be refreshed)

**Token refresh**: Meta Developer portal → app → Use cases → Step 2 → Generate token for @otwarteraporty.

---

## Publishing Flow

Instagram requires two API calls:

```bash
# Step 1 — Create media container
curl -X POST "https://graph.instagram.com/v22.0/26290813287238381/media" \
  --data-urlencode "image_url=https://portal.open-reporting.dev/<filename>.png" \
  --data-urlencode "caption=<Polish caption>" \
  -d "access_token=${INSTAGRAM_ACCESS_TOKEN}"
# → returns {"id": "<creation_id>"}

# Step 2 — Publish (wait ~10s for Instagram to process image first)
sleep 10
curl -X POST "https://graph.instagram.com/v22.0/26290813287238381/media_publish" \
  -d "creation_id=<creation_id>" \
  -d "access_token=${INSTAGRAM_ACCESS_TOKEN}"
```

The image **must be publicly accessible** — serve from `infra/nginx/html/` → `https://portal.open-reporting.dev/<file>`.

Use a **unique filename per post** — Instagram caches by URL, reusing the same filename will serve the old image.

---

## Post Types

### 1. Economy Snapshot (weekly)
A 2×2 KPI card with key macro indicators.

**Indicators to feature**:
- `mac.gdp_real_growth` — Wzrost PKB
- `prc.cpi_total` — Inflacja CPI
- `lab.wage_growth` — Wzrost płac nominalnych
- `lab.real_wage_growth` — Wzrost płac realnych
- `fin.eur_pln` — EUR/PLN

**Trend color logic**:
- ▲ `POSITIVE` — up and good (PKB, płace)
- ▼ `POSITIVE` — down and good (inflacja)
- ▲ `NEGATIVE` — up and bad (inflacja rising)
- ▼ `NEGATIVE` — down and bad (płace realne falling)

### 2. Single Indicator Deep-Dive (ad hoc)
One indicator, larger visual, more context in caption.

---

## Card Design Rules

- **Format**: 1080×1080px PNG
- **Theme**: always import from `products/visuals/lib/theme.py` — never hardcode colors
- **Background**: `BG_PAGE` (`#F7F8FA`)
- **Card surface**: `BG_SURFACE` (`#FFFFFF`), border `BORDER` (`#DDE2E8`)
- **Values**: `AZURE_1` (`#4A7FB5`), 50–52px font
- **Font**: `FONT_FAMILY` from theme.py
- **Footer**: always `Otwarte Raporty • open-reporting.dev` in `MUTED`
- **Filename**: descriptive + date, e.g. `social_snapshot_2025_q1.png`

---

## Caption Format

```
🇵🇱 [Headline in Polish — one sentence]

[Emoji] [Indicator]: [value] ([trend note])
...

Więcej danych na open-reporting.dev

#gospodarka #Polska #[topic] #dane #OtwarteRaporty
```

**Standard hashtags**: `#gospodarka #Polska #dane #OtwarteRaporty`
**Topic hashtags**: `#PKB #inflacja #płace #rynekpracy #euro #finanse`

---

## Step-by-Step: Economy Snapshot Post

1. **Query warehouse** for latest + previous period values:
   ```sql
   WITH ranked AS (
       SELECT ai.detail_id, ddd.detail_name, ddd.detail_unit,
              ai.period_date, ai.value,
              ROW_NUMBER() OVER (PARTITION BY ai.detail_id ORDER BY ai.period_date DESC) as rn
       FROM curated.all_indicators ai
       JOIN curated.dim_domain_detail ddd USING (detail_id)
       WHERE ai.geo = 'PL' AND ai.detail_id IN (...)
   )
   SELECT * FROM ranked WHERE rn <= 2
   ```

2. **Generate card** with Plotly — import all colors from `products/visuals/lib/theme.py`

3. **Save image** to `infra/nginx/html/<unique_filename>.png`

4. **Preview** at `https://portal.open-reporting.dev/<unique_filename>.png`

5. **Write caption** in Polish — factual, no editorialising

6. **Get user approval** before publishing

7. **Create container** → wait 10s → **publish**

---

## Quality Gates

- [ ] Image previewed in browser before publishing
- [ ] Caption reviewed — correct Polish, accurate numbers
- [ ] Trend arrows match data direction and correct color
- [ ] Footer present on card
- [ ] Unique filename used (not reusing previous post's filename)
- [ ] User approved before publishing
