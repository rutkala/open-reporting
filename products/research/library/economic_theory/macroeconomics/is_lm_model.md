# IS-LM Model
**Area:** Macroeconomics — Business Cycle / Short-Run
**Source:** Hicks (1937); Mankiw [MANKIW-MACRO] Ch. 11–12; Blanchard [BLANCHARD] Ch. 5–6
**Tags:** short-run, goods market, money market, interest rate, fiscal policy, monetary policy

## Core Idea
Two-equation model of short-run macroeconomic equilibrium. The IS curve represents
goods market equilibrium (investment = saving); the LM curve represents money market
equilibrium (money supply = money demand). Together they determine output (Y) and the
interest rate (r) simultaneously. Used to analyse fiscal and monetary policy multipliers.

## Key Equations

**IS curve** (goods market equilibrium):
$$Y = C(Y - T) + I(r) + G + NX$$

Linearised form:
$$Y = \frac{1}{1 - c_1}(\bar{C} + I(r) + G - c_1 T)$$

where $c_1$ is the marginal propensity to consume (MPC), $0 < c_1 < 1$.

**LM curve** (money market equilibrium):
$$\frac{M}{P} = L(r, Y) = kY - hr$$

Solved for r:
$$r = \frac{k}{h}Y - \frac{1}{h}\frac{M}{P}$$

**IS-LM equilibrium** (solve simultaneously):
$$Y^* = \frac{h}{h(1-c_1) + kb}(\bar{A} + \frac{b}{h}\frac{M}{P})$$

where $b$ = sensitivity of investment to interest rate, $\bar{A}$ = autonomous spending.

**Fiscal multiplier** (with crowding out):
$$\frac{dY}{dG} = \frac{h}{h(1-c_1) + kb} < \frac{1}{1-c_1}$$

**Monetary multiplier:**
$$\frac{dY}{d(M/P)} = \frac{b}{h(1-c_1) + kb}$$

**Variables:**
- $Y$ = output/income, $r$ = real interest rate
- $C$ = consumption, $I$ = investment, $G$ = government spending
- $T$ = taxes, $NX$ = net exports, $M$ = money supply, $P$ = price level
- $k, h$ = income and interest sensitivity of money demand

## Assumptions
1. Short run: prices are fixed ($P = \bar{P}$), so real = nominal interest rate
2. Closed economy (basic form); open economy requires Mundell-Fleming extension
3. Investment is decreasing in the interest rate: $I'(r) < 0$
4. Consumption is increasing in disposable income: $C'(Y-T) > 0$
5. Money demand is increasing in Y and decreasing in r
6. Central bank controls money supply exogenously

## Data Requirements
| Variable | Frequency | Catalogue Sources |
|----------|-----------|-------------------|
| GDP components (C, I, G, NX) | Quarterly | `sdp`, `bdm`, `eurostat` |
| Interest rates (NBP reference rate) | Monthly | `nbp` |
| Money supply (M1, M2, M3) | Monthly | `nbp`, `ecb` |
| Government expenditure and taxes | Monthly | `mf`, `eurostat` |
| Price level / CPI | Monthly | `bdl`, `sdp`, `eurostat` |

## Limitations
- Static model — no dynamics or expectations
- Fixed prices assumption valid only in very short run
- LM curve assumes money supply targeting (most central banks now use interest rate targeting → IS-MP model more appropriate)
- Ignores financial sector and credit channels
- Aggregate consumption function too simplified

## Extensions
- **IS-MP model** (Romer 2000): replaces LM with a monetary policy (MP) rule — better fits modern central banking (e.g. NBP with inflation targeting)
- **Mundell-Fleming:** open economy version with exchange rate
- **AS-AD:** combines IS-LM with a supply side to endogenise prices

## Related Models
- [`as_ad_model.md`](as_ad_model.md) — adds price adjustment
- [`mundell_fleming.md`](mundell_fleming.md) — open economy extension
- [`taylor_rule.md`](taylor_rule.md) — modern monetary policy rule replacing LM
