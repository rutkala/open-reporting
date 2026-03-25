# Taylor Rule
**Area:** Macroeconomics — Monetary Policy
**Source:** Taylor (1993); Mankiw [MANKIW-MACRO] Ch. 15; Blanchard [BLANCHARD] Ch. 25
**Tags:** monetary policy, interest rate, inflation targeting, output gap, central bank, NBP

## Core Idea
A simple rule describing how a central bank should (or does) set the nominal interest rate
in response to deviations of inflation from target and output from potential. Introduced by
John Taylor (1993) to describe Fed behaviour. Widely used to evaluate central bank policy
and as a replacement for the LM curve in modern macro models. Directly applicable to NBP
(National Bank of Poland) interest rate decisions.

## Key Equations

**Original Taylor Rule (1993):**
$$i_t = r^* + \pi_t + \phi_\pi(\pi_t - \pi^*) + \phi_y \tilde{y}_t$$

**Simplified form:**
$$i_t = \bar{r} + \phi_\pi \pi_t + \phi_y \tilde{y}_t$$

**Taylor's original coefficients:**
$$\phi_\pi = 1.5, \quad \phi_y = 0.5, \quad r^* = 2\%, \quad \pi^* = 2\%$$

**Inertial (smoothing) version:**
$$i_t = \rho i_{t-1} + (1-\rho)[\bar{r} + \phi_\pi(\pi_t - \pi^*) + \phi_y \tilde{y}_t]$$

where $\rho \in (0,1)$ is the interest rate smoothing parameter.

**Taylor principle:** requires $\phi_\pi > 1$ — the nominal rate must rise by more than
one-for-one with inflation to raise the *real* rate and stabilise inflation.

**Variables:**
- $i_t$ = nominal policy interest rate (e.g. NBP reference rate)
- $r^*$ = neutral/natural real interest rate
- $\pi_t$ = current inflation, $\pi^*$ = inflation target
- $\tilde{y}_t = y_t - y_t^*$ = output gap (% deviation from potential)
- $\phi_\pi$ = inflation response coefficient
- $\phi_y$ = output gap response coefficient
- $\rho$ = smoothing parameter

## Assumptions
1. Central bank observes inflation and output gap contemporaneously
2. Neutral rate $r^*$ is stable and known (strong assumption)
3. Linear response to both gaps
4. No zero lower bound (ZLB) considerations in basic form

## Data Requirements
| Variable | Frequency | Catalogue Sources |
|----------|-----------|-------------------|
| NBP reference rate ($i_t$) | Monthly | `nbp` |
| CPI / HICP inflation ($\pi_t$) | Monthly | `bdl`, `sdp`, `nbp` |
| GDP / output gap ($\tilde{y}_t$) | Quarterly | `eurostat`, `imf`, `oecd` |
| Potential output estimate | Quarterly | `eurostat`, `imf`, `oecd` |

## Empirical Application for Poland
- Estimate implied Taylor rule coefficients for NBP using OLS regression on historical data
- Compare actual NBP rate to Taylor-implied rate to identify deviations (policy stance)
- Test whether NBP satisfied the Taylor principle ($\hat{\phi}_\pi > 1$)
- Estimate neutral rate $r^*$ using HP filter or state-space model

## Limitations
- $r^*$ is unobservable and has likely declined since 2008
- Output gap estimates are highly revised ex-post
- Backward-looking specification; modern central banks use forward-looking rules
- Does not account for financial stability considerations
- ZLB binds when neutral rate is low (relevant post-2020)

## Related Models
- [`is_lm_model.md`](is_lm_model.md) — Taylor rule replaces LM curve in IS-MP model
- [`phillips_curve.md`](phillips_curve.md) — provides the inflation dynamics
- [`as_ad_model.md`](as_ad_model.md) — full system including Taylor rule
