# Production Theory
**Area:** Microeconomics — Producer Behaviour
**Source:** Mas-Colell et al. [MAS-COLELL] Ch. 5; Varian [VARIAN-MICRO] Ch. 18–21
**Tags:** production function, cost, profit maximisation, returns to scale, Cobb-Douglas

## Core Idea
Models how a firm transforms inputs (labour, capital) into output to maximise profit.
The production function describes technological possibilities; cost minimisation yields
the cost function; together they determine supply behaviour. Empirically central to
productivity analysis, growth accounting, and industrial economics.

## Key Equations

**Production function:**
$$Q = F(K, L)$$

**Cobb-Douglas (most common empirical form):**
$$Q = A \cdot K^\alpha L^\beta$$

- $\alpha + \beta = 1$: constant returns to scale (CRS)
- $\alpha + \beta > 1$: increasing returns to scale (IRS)
- $\alpha + \beta < 1$: decreasing returns to scale (DRS)

**Marginal products:**
$$MP_K = \frac{\partial Q}{\partial K} = \alpha \frac{Q}{K}, \quad MP_L = \frac{\partial Q}{\partial L} = \beta \frac{Q}{L}$$

**Marginal rate of technical substitution:**
$$MRTS_{LK} = \frac{MP_L}{MP_K} = \frac{\beta K}{\alpha L}$$

**Profit maximisation** (price-taking firm):
$$\max_{K,L} \; pQ - wL - rK \quad \Rightarrow \quad p \cdot MP_L = w, \quad p \cdot MP_K = r$$

**Cost minimisation** (given output $\bar{Q}$):
$$\min_{K,L} \; wL + rK \quad \text{s.t.} \quad F(K,L) \geq \bar{Q}$$

**Conditional factor demands (Cobb-Douglas):**
$$L^* = \bar{Q}^{1/(\alpha+\beta)} \left(\frac{\alpha w}{\beta r}\right)^{-\beta/(\alpha+\beta)} \cdot \text{const}$$

**Total cost function (Cobb-Douglas, CRS):**
$$TC(w, r, Q) = Q \cdot A^{-1} \left(\frac{w}{\beta}\right)^\beta \left(\frac{r}{\alpha}\right)^\alpha$$

**Shephard's lemma:**
$$\frac{\partial TC}{\partial w} = L^*(w, r, Q), \quad \frac{\partial TC}{\partial r} = K^*(w, r, Q)$$

**TFP (Total Factor Productivity):**
$$\ln A = \ln Q - \alpha \ln K - \beta \ln L$$

## Assumptions
1. Profit maximisation (or cost minimisation)
2. Price-taking in input and output markets (competitive firm)
3. Free disposal of inputs
4. Differentiable, strictly quasi-concave production function

## Data Requirements
| Variable | Frequency | Catalogue Sources |
|----------|-----------|-------------------|
| Gross output or value added (Q) | Annual | `sdp`, `bdl`, `eurostat` |
| Capital stock (K) | Annual | `eurostat` (EU KLEMS), `worldbank` |
| Employment / hours worked (L) | Annual | `bdl`, `sdp`, `ilostat` |
| Wages (w) | Annual | `bdl`, `sdp`, `eurostat` |
| Capital cost / interest rate (r) | Annual | `nbp`, `ecb` |

## Empirical Application for Poland
- Estimate Cobb-Douglas parameters by sector using GUS/Eurostat industry data
- Decompose labour productivity growth into capital deepening vs TFP
- Compare TFP levels across Polish manufacturing sectors
- Estimate firm-level production functions using enterprise survey data (GUS)

## Limitations
- Cobb-Douglas imposes unit elasticity of substitution — may be restrictive
- Aggregate production function aggregation problems (Cambridge controversy)
- TFP is a residual — captures measurement error, not just technology
- Static model; dynamic investment decisions require separate framework (Tobin's q)

## Alternative Functional Forms
- **CES (Constant Elasticity of Substitution):** $Q = A[\delta K^{-\rho} + (1-\delta)L^{-\rho}]^{-1/\rho}$
  - Nests Cobb-Douglas ($\rho \to 0$), Leontief ($\rho \to \infty$), linear ($\rho = -1$)
- **Translog:** flexible second-order approximation; used in productivity studies

## Related Models
- [`consumer_theory.md`](consumer_theory.md) — dual optimisation structure
- [`solow_growth_model.md`](../macroeconomics/solow_growth_model.md) — aggregate production function
