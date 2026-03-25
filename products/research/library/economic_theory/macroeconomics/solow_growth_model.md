# Solow Growth Model
**Area:** Macroeconomics — Growth Theory
**Source:** Solow (1956); Mankiw [MANKIW-MACRO] Ch. 8; Romer [ROMER-ADVANCED] Ch. 1
**Tags:** growth, capital accumulation, steady state, convergence, TFP

## Core Idea
Explains long-run economic growth through capital accumulation, labour growth, and exogenous
technological progress. The economy converges to a steady state where output per worker grows
at the rate of technological progress. Differences in income levels across countries are
explained by differences in savings rates, population growth, and technology.

## Key Equations

**Production function (Cobb-Douglas form):**
$$Y = K^\alpha (AL)^{1-\alpha}, \quad 0 < \alpha < 1$$

**Output per effective worker** (intensive form, $y = Y/AL$, $k = K/AL$):
$$y = k^\alpha$$

**Capital accumulation:**
$$\dot{k} = s \cdot k^\alpha - (n + g + \delta) \cdot k$$

**Steady state** ($\dot{k} = 0$):
$$k^* = \left(\frac{s}{n + g + \delta}\right)^{1/(1-\alpha)}$$

**Steady-state output per worker:**
$$\ln(y^*/A) = \frac{\alpha}{1-\alpha}\ln(s) - \frac{\alpha}{1-\alpha}\ln(n + g + \delta)$$

**Variables:**
- $Y$ = output, $K$ = capital, $L$ = labour, $A$ = technology level
- $s$ = savings rate, $n$ = population growth rate
- $g$ = technological progress rate, $\delta$ = depreciation rate
- $\alpha$ = capital share in output (~0.33 empirically)

## Assumptions
1. Constant returns to scale in K and L
2. Diminishing marginal returns to each factor individually
3. Inada conditions: $F_K, F_L \to \infty$ as inputs $\to 0$; $\to 0$ as inputs $\to \infty$
4. Technology ($A$) grows exogenously at rate $g$
5. Labour grows exogenously at rate $n$
6. Closed economy; savings = investment ($sY = I$)
7. One sector; one good

## Data Requirements
| Variable | Frequency | Catalogue Sources |
|----------|-----------|-------------------|
| GDP (Y) | Annual/Quarterly | `sdp`, `bdm`, `eurostat`, `worldbank` |
| Gross fixed capital formation (I) | Annual | `sdp`, `eurostat` |
| Employment / Population (L) | Annual | `bdl`, `ilostat`, `eurostat` |
| Capital stock (K) | Annual | `eurostat` (EU KLEMS), `worldbank` |
| Savings rate (s = I/Y) | Annual | derived from above |

## Empirical Application for Poland
- Estimate $\alpha$ via labour share: $\alpha = 1 - \text{(compensation of employees / GDP)}$
- Test conditional convergence: regress growth on $\ln(y_0)$, $\ln(s)$, $\ln(n+g+\delta)$
- Decompose GDP growth into factor accumulation vs TFP (growth accounting)

## Limitations
- Exogenous technology: does not explain *why* countries differ in $g$
- No role for human capital (addressed by Mankiw-Romer-Weil 1992 extension)
- Assumes perfect competition and full employment
- Closed economy assumption problematic for small open economies like Poland

## Extensions
- **Mankiw-Romer-Weil (1992):** adds human capital $H$, improves cross-country fit
- **Ramsey-Cass-Koopmans:** endogenous savings rate via intertemporal optimisation
- **Romer (1990) / Endogenous growth:** technology determined within model

## Related Models
- [`endogenous_growth.md`](endogenous_growth.md) — AK model, Romer's R&D model
- [`growth_accounting.md`](growth_accounting.md) — empirical decomposition method
