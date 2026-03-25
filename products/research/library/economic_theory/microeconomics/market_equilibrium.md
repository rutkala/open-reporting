# Market Equilibrium
**Area:** Microeconomics — Markets
**Source:** Varian [VARIAN-MICRO] Ch. 1, 15–16; Mankiw [MANKIW-MACRO] Ch. 4
**Tags:** supply, demand, equilibrium, elasticity, welfare, surplus, market clearing

## Core Idea
Competitive market equilibrium occurs where quantity demanded equals quantity supplied,
determining the equilibrium price and quantity. Comparative statics analyse how equilibrium
changes with shifts in supply or demand. Welfare analysis measures consumer and producer
surplus. Foundation for all applied price and market analysis.

## Key Equations

**Demand function (linear approximation):**
$$Q^D = a - b \cdot P + c \cdot M + d \cdot P_s$$

**Supply function (linear approximation):**
$$Q^S = e + f \cdot P - g \cdot W$$

**Equilibrium:** $Q^D = Q^S = Q^*$, solves for $P^*$:
$$P^* = \frac{a - e + cM + dP_s + gW}{b + f}$$

**Price elasticity of demand:**
$$\varepsilon_D = \frac{\partial Q^D}{\partial P} \cdot \frac{P}{Q^D} < 0$$

**Price elasticity of supply:**
$$\varepsilon_S = \frac{\partial Q^S}{\partial P} \cdot \frac{P}{Q^S} > 0$$

**Consumer surplus:**
$$CS = \int_0^{Q^*} P^D(Q) \, dQ - P^* Q^*$$

**Producer surplus:**
$$PS = P^* Q^* - \int_0^{Q^*} P^S(Q) \, dQ$$

**Tax incidence** (specific tax $t$ per unit):
$$\frac{dP^D/dt}{1} = \frac{\varepsilon_S}{\varepsilon_S - \varepsilon_D}, \quad \frac{dP^S/dt}{1} = \frac{\varepsilon_D}{\varepsilon_S - \varepsilon_D}$$

Burden falls more on the inelastic side of the market.

**Deadweight loss from tax:**
$$DWL = \frac{1}{2} t \cdot \Delta Q = \frac{1}{2} \frac{\varepsilon_D \varepsilon_S}{\varepsilon_S - \varepsilon_D} \frac{Q^*}{P^*} t^2$$

**Variables:**
- $P$ = price, $Q$ = quantity, $M$ = consumer income
- $P_s$ = price of substitute, $W$ = input price (wage)
- $a,b,c,d,e,f,g$ = demand/supply parameters

## Assumptions
1. Many buyers and sellers (price-taking)
2. Homogeneous good
3. Free entry and exit (long run)
4. Perfect information
5. No externalities (private good)

## Data Requirements
| Variable | Frequency | Catalogue Sources |
|----------|-----------|-------------------|
| Prices by category | Monthly | `bdl`, `sdp`, `eurostat`, `tge` (energy) |
| Quantities / volumes | Monthly/Annual | `bdl`, `sdp` |
| Wages / input costs | Monthly | `bdl`, `sdp` |
| Household income | Annual | `bdl`, `sdp` |

## Empirical Applications for Poland
- Estimate price elasticity of demand for energy using PSE/TGE + household data
- Estimate labour market supply and demand elasticities
- Analyse pass-through of energy prices to consumer prices (PRC domain)
- Tax incidence analysis for VAT changes using CPI micro-data

## Limitations
- Linear approximation valid only locally around equilibrium
- Competitive assumption may not hold (oligopoly, regulated markets)
- Static model — no inventory, expectations, or adjustment dynamics
- Partial equilibrium ignores economy-wide feedback effects

## Related Models
- [`consumer_theory.md`](consumer_theory.md) — micro-foundations of demand
- [`production_theory.md`](production_theory.md) — micro-foundations of supply
- [`is_lm_model.md`](../macroeconomics/is_lm_model.md) — goods market in macro context
