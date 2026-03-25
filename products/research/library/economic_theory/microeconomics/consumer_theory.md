# Consumer Theory
**Area:** Microeconomics — Consumer Behaviour
**Source:** Mas-Colell et al. [MAS-COLELL] Ch. 2–3; Varian [VARIAN-MICRO] Ch. 4–8
**Tags:** utility, demand, budget constraint, optimisation, Slutsky, revealed preference

## Core Idea
Models how a rational consumer allocates income across goods to maximise utility subject
to a budget constraint. The solution yields Marshallian demand functions (ordinary demand).
Decomposing price effects into substitution and income effects (Slutsky equation) is central
to empirical demand analysis and welfare measurement.

## Key Equations

**Utility maximisation problem (UMP):**
$$\max_{x \geq 0} \; u(x) \quad \text{s.t.} \quad p \cdot x \leq m$$

**First-order conditions (interior solution):**
$$\frac{\partial u / \partial x_i}{\partial u / \partial x_j} = \frac{p_i}{p_j}, \quad \forall i,j$$

i.e. MRS = price ratio at optimum.

**Marshallian demand functions:**
$$x^*_i = x_i(p, m), \quad i = 1, \ldots, n$$

**Indirect utility function:**
$$V(p, m) = u(x^*(p,m))$$

**Expenditure minimisation problem (EMP) — dual:**
$$\min_x \; p \cdot x \quad \text{s.t.} \quad u(x) \geq \bar{u}$$

**Hicksian (compensated) demand:**
$$h_i(p, \bar{u}) = \frac{\partial e(p, \bar{u})}{\partial p_i} \quad \text{(Shephard's lemma)}$$

**Slutsky equation** (decomposes price effect):
$$\underbrace{\frac{\partial x_i}{\partial p_j}}_{\text{total effect}} = \underbrace{\frac{\partial h_i}{\partial p_j}}_{\text{substitution effect}} - \underbrace{x_j \frac{\partial x_i}{\partial m}}_{\text{income effect}}$$

**Own-price elasticity:**
$$\varepsilon_{ii} = \frac{\partial x_i}{\partial p_i} \cdot \frac{p_i}{x_i}$$

**Income elasticity:**
$$\varepsilon_{im} = \frac{\partial x_i}{\partial m} \cdot \frac{m}{x_i}$$

**Engel aggregation:** $\sum_i s_i \varepsilon_{im} = 1$ (budget shares $s_i = p_i x_i / m$)

**Slutsky symmetry:** $\frac{\partial h_i}{\partial p_j} = \frac{\partial h_j}{\partial p_i}$

## Assumptions
1. **Completeness:** consumer can rank all bundles
2. **Transitivity:** preferences are consistent
3. **Monotonicity (non-satiation):** more is preferred to less
4. **Convexity:** preference for diversity (diminishing MRS)
5. **Continuity:** small changes in prices/income lead to small changes in demand

## Data Requirements
| Variable | Frequency | Catalogue Sources |
|----------|-----------|-------------------|
| Household expenditure by category | Annual | `bdl`, `sdp`, `eurostat` |
| Consumer prices by category (CPI) | Monthly | `bdl`, `sdp`, `eurostat` |
| Household income / disposable income | Annual | `bdl`, `sdp`, `eurostat` |
| Budget shares by decile | Annual | `sdp` (GUS household survey) |

## Empirical Application
- Estimate price and income elasticities from household survey data (GUS)
- Test Slutsky symmetry using system of demand equations (AIDS model)
- Estimate Engel curves by income decile for Poland
- Welfare analysis: cost of living index, consumer surplus changes from price shocks

## Limitations
- Representative agent ignores heterogeneity across households
- Assumes perfect information and rational behaviour
- Static model — no savings, intertemporal choice, or uncertainty
- Aggregate demand ≠ sum of individual demands unless restrictive conditions hold (Gorman aggregation)

## Key Demand Systems
- **Linear Expenditure System (LES):** $p_i x_i = \gamma_i + \beta_i(m - \sum_j p_j \gamma_j)$
- **Almost Ideal Demand System (AIDS):** flexible, satisfies Slutsky conditions
- **QUAIDS:** quadratic extension of AIDS for non-linear Engel curves

## Related Models
- [`production_theory.md`](production_theory.md) — dual theory, cost minimisation
- [`market_equilibrium.md`](market_equilibrium.md) — demand + supply
