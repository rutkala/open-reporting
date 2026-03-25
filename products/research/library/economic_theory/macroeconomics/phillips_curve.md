# Phillips Curve
**Area:** Macroeconomics — Inflation & Labour Market
**Source:** Phillips (1958); Mankiw [MANKIW-MACRO] Ch. 14; Blanchard [BLANCHARD] Ch. 8–9
**Tags:** inflation, unemployment, expectations, NAIRU, monetary policy, short-run

## Core Idea
Describes the empirical relationship between inflation and unemployment. The original
Phillips curve showed a stable negative trade-off; the expectations-augmented version
(Friedman-Phelps) shows no long-run trade-off — only a short-run relationship around
the natural rate of unemployment (NAIRU). Central to understanding monetary policy
transmission and inflation dynamics in Poland.

## Key Equations

**Original Phillips curve:**
$$\pi = -\epsilon(u - u^*), \quad \epsilon > 0$$

**Expectations-augmented (Friedman-Phelps):**
$$\pi = \pi^e - \epsilon(u - u^*) + \nu$$

**New Keynesian Phillips Curve (NKPC):**
$$\pi_t = \beta E_t[\pi_{t+1}] + \kappa \tilde{y}_t$$

where $\tilde{y}_t = y_t - y_t^*$ is the output gap.

**Adaptive expectations version:**
$$\pi^e_t = \pi_{t-1}$$
$$\Rightarrow \pi_t = \pi_{t-1} - \epsilon(u_t - u^*) + \nu_t$$

**Sacrifice ratio** (cost of disinflation):
$$SR = \frac{\text{cumulative output loss}}{\text{reduction in inflation}}$$

**Variables:**
- $\pi$ = inflation rate, $\pi^e$ = expected inflation
- $u$ = unemployment rate, $u^*$ = natural rate of unemployment (NAIRU)
- $\epsilon$ = slope of Phillips curve (sensitivity)
- $\nu$ = supply shock term, $\kappa$ = slope in NKPC
- $\tilde{y}$ = output gap, $\beta$ = discount factor (~0.99)

## Assumptions
1. Expectations-augmented: workers and firms form inflation expectations
2. NAIRU is stable (controversial — may shift with structural changes)
3. Supply shocks enter additively
4. Short-run trade-off exists; long-run Phillips curve is vertical at $u^*$

## Data Requirements
| Variable | Frequency | Catalogue Sources |
|----------|-----------|-------------------|
| Inflation (CPI, HICP) | Monthly | `bdl`, `sdp`, `nbp`, `eurostat` |
| Unemployment rate | Monthly | `bdl`, `mrpips`, `eurostat` |
| Inflation expectations | Monthly | `nbp` (surveys), `ec_bcs` |
| Output gap estimate | Quarterly | `eurostat`, `imf`, `oecd` |
| Wage growth | Quarterly | `bdl`, `sdp`, `eurostat` |

## Empirical Application for Poland
- Estimate NAIRU using Kalman filter or HP-filter decomposition
- Test stability of Phillips curve pre/post-2008 and pre/post-2020
- Estimate sacrifice ratio from disinflation episodes (e.g. 2022–2024 tightening cycle)
- Compare expectations anchoring: adaptive vs rational expectations

## Limitations
- NAIRU is unobservable and must be estimated — high uncertainty
- Relationship has flattened significantly in many countries post-1990s
- Global factors (import prices, global slack) may dominate domestic factors
- Energy/food supply shocks dominate in small open economies like Poland

## Related Models
- [`as_ad_model.md`](as_ad_model.md) — AS curve is derived from Phillips curve
- [`taylor_rule.md`](taylor_rule.md) — central bank response to inflation/output gap
- [`okun_law.md`](okun_law.md) — links output gap to unemployment gap
