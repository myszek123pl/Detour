# 26 - Price formation and exit liquidity: pump.fun bonding curve vs PumpSwap AMM

Script: `/home/user/Detour/backtest/curve_vs_amm_sim.py` (run `python3 -I curve_vs_amm_sim.py [base|a|b|c|d|e]`, ~3 s, deterministic seeds). Full raw output is appended at the bottom of this file. Inputs: notes 01 (curve math), 02 (fees), 13 (position vs liquidity) in `analizy dogłębne/`; no new web data.

## 0. Model and assumptions (read first)
- Curve: constant product on VIRTUAL reserves, k = 30 SOL x 1,073M tokens = 32,190. Real tokens sellable 793.1M, 1B supply. Completes when vt = 279.9M, i.e. vs = 115.005 SOL, real SOL raised = 85.005, mcap 410.9 SOL (14.70x the 27.96 SOL start mcap).
- Price P = vs/vt = vs^2/k. This one identity drives everything: price depends only on the SOL reserve, not on path or timing. Mcap(SOL) = 1000 x P(SOL per Mtok).
- Fee 1.25% per side (note 02: curve 0.95% protocol + 0.30% creator; PumpSwap tier 0 = 0.93/0.30/0.02 LP). Convention from note 01: buy pays curve_cost x 1.0125; sell receives gross x 0.9875. Fees leave the reserves (only the 0.02% LP slice stays in the pool).
- Graduation: pool = 206.9M tokens (1B - 793.1M) + (85.005 - 0.015 migration fee) = 84.990 SOL. **[UNVERIFIED] seed split as in note 01 (derived, not read on-chain).** LP is burned/locked, so pool SOL is never withdrawable by anyone.
- The buy that completes the curve is capped at the curve limit; any remainder fills on the pool (synthetic migration, note 01). SOL=1 unit, no priority fees/tips/MEV, no latency, no rug via LP. Tokens held by everyone are "bags" unless they sell.
- Organic flow in (a) is synthetic (lognormal buy size, median 0.8 SOL, 15% of events are partial sells on the curve, 55% after graduation). It is a stand-in, not data: use the tables for mechanism, not as frequencies.

## 1. Mechanics: how price is formed
### Curve
| Quantity | Formula |
|---|---|
| Price | P = vs^2 / k |
| Buy S SOL (gross) | net = S/(1.0125); vs' = vs + net; tokens = vt - k/vs' |
| Sell n tokens | gross = vs - k/(vt+n) = vs*n/(vt+n); you get gross x 0.9875 |
| Price impact (no fee), buy of net s | (1 + s/vs)^2 - 1  (approx 2s/vs) |
| Price multiple left to graduation | (115.005/(30+r))^2 where r = real SOL raised |
| Net SOL to double the price | (sqrt2 - 1) x vs = 0.414 vs (12.4 at the start, 33 at r=50, 47.6 at the end) |
| Sell-all-back identity | reserve is path-independent: if every token returns, real SOL returns to 0 and sum of PnL = - fees |

Key consequence: **the curve has no path dependence and no "impact cost" if the price persists.** A round trip costs exactly 2.47% (1 - 0.9875/1.0125) at any size, any point on the curve, as long as the curve state is the same on exit (table D5). Impact only matters because after you buy, *others* buy or sell, and your exit price is set by the net SOL reserve at that time.

### Who provides exit liquidity
- Every SOL a seller receives is SOL previously deposited by buyers and not yet withdrawn. The curve contains no market makers. Reserve(t) = sum over current positions of (SOL in - SOL out, net of fees). Selling at reserve r means the people who are still net-long in SOL terms (later buyers) pay for your exit.
- Zero-sum check (table B-1): after forcing every holder to sell, sum of all traders' PnL = -(fees + 0.015 migration fee + SOL left in the AMM), residual 1e-14 SOL in 8 random paths. On a curve that never graduates (B-2), sum PnL = -fees exactly.
- So trader-vs-trader PnL is a zero-sum redistribution (ordered by timing: low-price entrants are paid by higher-price entrants), plus 3 leaks: fees (~2.3-3.3 SOL on ~85 SOL graduating, 4-5% of the pool), migration fee, and **the structural lock-up (below)**.

### The graduation discontinuity (the main structural finding)
| | Curve at completion | Pool right after migration |
|---|---|---|
| Price | 0.41088 SOL/Mtok | 0.41078 (-0.024%, continuous) |
| SOL reserve R | 115.0 virtual / 85.0 real | 84.99 real |
| k | 32,190 | 17,584 (**-45.4%**) |
| Impact of +1 SOL net | 1.75% | 2.37% |
| Net SOL to double price | 47.6 | 35.2 |
| Sell all 793.1M tokens back | returns 85.0 SOL (100%) | returns 67.4 SOL (79.3%) |

Price is continuous but depth is not: the virtual 30 SOL / 73M token cushion that supported the curve disappears. The pool holds 206.9M tokens + 85 SOL; the 793.1M tokens in traders' hands "see" a 45% thinner book. 17.6 SOL (20.7% of the raise) is permanently locked in the pool even if all holders exit. Fee tier is unchanged (1.25%) at the boundary, so the cost step is in impact only, not fees.

## 2. Findings per question
### (a) Replayed order sequences (tables A1-A3)
Setup: dev 2 SOL + 6 snipers x 1.5 SOL at creation (dev 6.6%, snipers 21.9% of supply for 11 SOL), ~130-170 organic buyers to graduation.
| Scenario (seed 7) | Dev PnL | Snipers (6) | Organic (all) | Where the SOL ends |
|---|---|---|---|---|
| S1 snipers dump at r=15, dev holds | marked +16.4 (holds 6.6%) | +1.5 | realised -71.9; liquidation -34.7 | pool 69.8 SOL, mcap 277 |
| S2 snipers+dev dump in first pool block | +3.7 | **+36.9** | realised -95.2; liquidation -61.3 | pool 51.9 SOL, mcap 153 |
| S3 snipers dump at r=70 on curve | marked +17.8 | **+31.6** | realised -105.5; liquidation -66.6 | pool 72.5, mcap 299 |
| S4 nobody sells | marked +20.8 | marked +66.2 | marked +98.6 | pool 77.7, mcap 343 |
- Early dump (S1) earns snipers only +1.5 SOL because r=15 is early: they sell 22% of supply into a curve with only 15 SOL of real reserve, so the dump itself caps what they can take out (their tokens are worth only the reserve at that point). The **later** the dump on the curve, the more reserve exists to extract: S3 (+31.6) and S2 (+36.9 on 11 SOL cost = 3.4x). The sniper cluster is worst for organic holders when it dumps into reserves that organic buyers built.
- S2 vs S3: dumping on the pool (S2) hits the pool depth cliff: sniper+dev tokens = 28.5% of supply, pool drops ~60% in one block (mcap 411 -> ~165). Net SOL extracted by the cluster 51.6, nearly the same as S3 but the remaining bag price is 2x lower.
- Sum of marked PnL is positive (+135..+186) only because the unsold tokens are marked at spot: it is paper. The honest zero-sum line is "liquidation": about -20.7 SOL in every scenario (fees ~3 + 17.6 locked in the AMM), with sniper/dev gains matched by organic losses dollar for dollar.
- Who holds at graduation (B-3, S2 base path): organic 51.6%, snipers 21.9%, dev 6.6%, LP pool 19.8%. If the pool were hit by snipers+dev (28.5%) organic holders can liquidate only 0.80x of cost basis even before the dump.

**Bot (1 SOL) entry x exit matrix, mean over 40 seeds** (r counts real SOL on the curve; snipers already put ~11 SOL in, so the earliest feasible entry is r=12). Full tables incl. p10/p90 in A2.
| Entry | exit = first pool state, S2 (bot before dump) | exit after S2 dump block | exit +60 pool orders (S2) | exit at graduation, S1 |
|---|---|---|---|---|
| r=12 | +5.47 | +0.18 | +1.51 | +5.57 |
| r=20 | +3.62 | -0.17 | +0.75 | +3.75 |
| r=30 | +2.37 | -0.40 | +0.27 | +2.40 |
| r=45 | +1.18 | -0.61 | -0.18 | +1.21 |
| r=65 | +0.38 | -0.76 | -0.48 | +0.41 |
| r=80 | +0.04 | -0.74 | -0.52 | +0.05 |
Reading: if the exit is *at* graduation, PnL is the closed-form (115/(30+r))^2 curve minus 2.5%: +5.5x at r=12 down to ~0 at r=80. If the token still carries a sniper/dev overhang at graduation, entries after r~15 lose after the dump; only the earliest entry survives, so the sniper-overhang token is a pure "exit before graduation block" trade.

### (b) Zero-sum and who ends up holding
- Identity (verified): sum PnL over all traders = -(fees + migration fee + SOL stranded in AMM) when all holders liquidate; stranded SOL is 17.59 +- 0.01 in 8 random paths, fees 2.5-3.1 SOL.
- Pre-graduation (curve-only, 30 buyers to r=34.9, then all sell): sum PnL = -0.872 = -fees exactly (B-2).
- Final bagholders: at graduation 52-68% of supply sits with organic buyers in the base paths, who are also the net losers in every scenario; snipers/dev are the winners whenever they can exit before the organic crowd. The pool's 206.9M tokens belong to nobody (burned LP): SOL in it is not redeemable.
- Exit liquidity is therefore not a stock of "market makers": it is later buyers' SOL (curve) or later buyers' SOL plus the locked, depth-limited pool (after graduation).

### (c) Buy volume needed to absorb a dump (tables C1-C5)
Closed form (curve and pool, vs/vt or ps/pt): dump of n tokens, price drop = 1 - (vt/(vt+n))^2; SOL taken out gross = vs*n/(vt+n); **volume needed to restore the pre-dump price = gross x 1.0125** (buyers must re-deposit what was withdrawn; the reserve is path-independent). Dump size X is % of 1B supply.
| X dumped | Curve r=40: drop / net proceeds / restore volume | Curve r=80 | Pool after graduation |
|---|---|---|---|
| 2% | -8% / 2.9 / 3.0 | -12% / 6.9 / 7.1 | -17% / 7.4 / 7.6 |
| 5% | -19% / 6.8 / 7.0 | -27% / 15.9 / 16.3 | -35% / 16.3 / 16.8 |
| 10% | -33% / 12.3 / 12.7 | -44% / 27.7 / 28.4 | **-55% / 27.4 / 28.0** |
| 20% | -51% / 21.0 / 21.5 | -65% / 44.1 / 45.2 | **-74% / 41.3 / 42.3** |
- Same % dump costs holders more the later it happens (more SOL inside, bigger drop in absolute SOL) but also pays the dumper more; the dumper's take is bounded by the reserve (X=20% at r=80 extracts 44 of the 80 SOL).
- The pool is shallower: 10% on the pool drops the price 55% vs 46% on the curve end, while extracting 27.4 vs 29.8 SOL.
- If organic buyers supply only 25/50/100% of the restore volume, the price stays -11/-7/0% (X=5%, r=20) ... -52/-36/0% (X=20%, r=80) below pre-dump (C5).
- Sniper economics (C4): 10% of supply costs ~3.1 SOL at launch and extracts 12.3 SOL at r=40 (4x) or 19.4 SOL at r=60 (6x); matching it needs 13 / 20 SOL of fresh organic buying, i.e. 15-24% of the whole 85 SOL raise.

### (d) Slippage at the graduation discontinuity (tables D1-D4)
Buy slippage (effective price vs spot including 1.25% fee; fee-free in brackets):
| buy SOL | curve r=80 | curve r=84 | pool after graduation |
|---|---|---|---|
| 1 | 2.16% [0.91] | 2.13% [0.88] | 2.43% [1.18] |
| 5 | 5.80% [4.55] | crosses | 7.13% [5.88] |
| 10 | crosses | crosses | 13.0% [11.8] |
| 50 | crosses | crosses | 60.1% [58.8] |
Sell slippage (net proceeds vs spot, size = SOL value at spot):
| sell SOL-eq | curve r=84.9 | pool after graduation | pool/curve (no-fee) |
|---|---|---|---|
| 1 | 2.10% | 2.40% | 1.35x |
| 10 | 9.16% | 11.64% | 1.32x |
| 50 | 31.2% | 37.8% | 1.22x |
| 100 | 47.2% | 54.6% | 1.16x |
| 200 | 64.0% | 70.6% | 1.11x |
- Discontinuity = +0.3 pp (1 SOL) to +7 pp (100 SOL) extra sell slippage; relative 1.1-1.35x worse (fee-free). The cliff matters for *aggregate* exits (793M tokens) not for one 1-SOL bot.
- A buy that straddles graduation (D4) is filled in two regimes: e.g. 100 SOL at r=80 gets 121M tokens at avg 0.82 SOL/Mtok and leaves the pool price at 4.4x the curve-end price (pool 178.8 SOL). Synthetic migration pushes the price through the boundary in one transaction, so there is no stable "graduation price" to trade at.
- Round-trip (D5) is a flat 2.47% on the curve and in the pool at any size if the state is restored; deviating only where a buy crosses graduation (10 SOL at r=80: 3.23%).

### (e) When on the curve is it mathematically worst/best to enter (table E1)
| entry r | entry mcap (SOL) | upside to graduation price | SOL back from 1 SOL if sold at graduation (2 fees) | net SOL demand needed for next 2x |
|---|---|---|---|---|
| 0 | 28 | 14.70x | 11.9 | 12.4 |
| 10 | 50 | 8.27x | 7.2 | 16.6 |
| 20 | 78 | 5.29x | 4.8 | 20.7 |
| 40 | 152 | 2.70x | 2.5 | 29.0 |
| 50 | 199 | 2.07x | 1.9 | 33.1 |
| 60 | 252 | 1.63x | 1.5 | 2x not reachable on curve |
| 80 | 376 | 1.09x | 1.04 | - |
| 84 | 404 | 1.02x | 0.97 | - |
- **Best (mathematically):** earliest, because upside to the graduation price is (115/(30+r))^2 and the SOL demand needed per doubling is only 0.414 x (30+r). At r<=20 doubling needs <=21 SOL of net buying, 25% of the raise, and it can happen four times before graduation.
- **Worst:** the last ~30 SOL of the curve (r>55): less than a 2x remains before graduation, then the pool starts 45% thinner and unlocks a doubling cost of 35 SOL net (E2: 2x above graduation = 35 SOL, 5x = 105, 10x = 184, 14.7x = 241 SOL, i.e. 2.8x the whole curve raise). At r=84, expected PnL on a graduation exit is -2.8% before any dumping.
- Reflexive rule: the *time-weighted* upside decays quadratically; entry cost (fees 2.47%) is constant, so the net edge needed is a fixed 2.5% -- the profit-per-trade is dominated by entry point, not by the 1.25% fee.
- Overhang rule: graduation exit is safe only if sniper+dev supply is small; with ~28% overhang on the pool, a first-block dump knocks 60% off the price (S2) and any entry after r~15 loses on a post-dump exit.

## 3. Caveats
- Organic flow is synthetic; scenario PnL distributions depend on it. The closed forms (price, impact, restore volume, locked 17.6 SOL, haircut 79%) do not.
- Seed split (206.9M / 84.99 SOL) and 1.25% fee at both stages come from notes 01/02 (partly unverified there). If the pool seeds differently, rerun with `POOL_TOK` and `MIG`.
- Bot fee model ignores Jito tips, priority fees and sandwiching, and assumes the bot is never front-run by snipers.
- Mark-to-market PnL treats tokens at spot; use the "liquidation" column for honest results.

## 4. Raw output of the simulator (`python3 -I curve_vs_amm_sim.py`)
### B0 Derived constants
- k_curve = 32,190.0 SOL*Mtok; VT_end = 279.9 Mtok; VS_end = 115.0054 SOL; real SOL raised = 85.0054
- curve end price = 4.108802e-01 SOL/Mtok; mcap = 410.88 SOL; start mcap 27.96 SOL; mult = 14.696x
- pool seed: 84.9904 SOL + 206.9 Mtok; pool price = 4.107799e-01 (vs curve end 4.108802e-01, gap -0.0244%)
- k_pool = 17584.5 vs k_curve = 32190.0  -> pool k is 54.6% of curve k (45.4% thinner)
- sell ALL 793.1M tokens back: curve returns 85.01 SOL gross (=100% of raised); pool returns 67.41 SOL gross (79.3%); structural haircut 17.60 SOL locked in pool + 0.015 migration fee

### B1 Price / depth vs progress (closed form: P = vs^2/k, mcap = P*1000)
| real SOL r | % of 85 | % tokens sold | price | x start | mcap SOL | price impact of 1 SOL buy (excl. fee) | price mult left to graduation (115/(30+r))^2 | net SOL needed for next 2x (0.414*vs) |
|---|---|---|---|---|---|---|---|---|
| 0 | 0% | 0.0% | 2.796e-02 | 1.00x | 28.0 | 6.69% | 14.70x | 12.4 |
| 5 | 6% | 19.3% | 3.806e-02 | 1.36x | 38.1 | 5.72% | 10.80x | 14.5 |
| 10 | 12% | 33.8% | 4.970e-02 | 1.78x | 49.7 | 5.00% | 8.27x | 16.6 |
| 20 | 24% | 54.1% | 7.766e-02 | 2.78x | 77.7 | 3.99% | 5.29x | 20.7 |
| 30 | 35% | 67.6% | 1.118e-01 | 4.00x | 111.8 | 3.32% | 3.67x | 24.9 |
| 40 | 47% | 77.3% | 1.522e-01 | 5.44x | 152.2 | 2.84% | 2.70x | 29.0 |
| 50 | 59% | 84.6% | 1.988e-01 | 7.11x | 198.8 | 2.48% | 2.07x | 33.1 |
| 60 | 71% | 90.2% | 2.516e-01 | 9.00x | 251.6 | 2.21% | 1.63x | n/a (<2x left) |
| 70 | 82% | 94.7% | 3.107e-01 | 11.11x | 310.7 | 1.99% | 1.32x | n/a (<2x left) |
| 80 | 94% | 98.4% | 3.759e-01 | 13.44x | 375.9 | 1.80% | 1.09x | n/a (<2x left) |
| 85 | 100% | 100.0% | 4.108e-01 | 14.69x | 410.8 | 1.73% | 1.00x | n/a (<2x left) |

### B2 Marginal depth: price impact per SOL of net buy = 2/R_eff
| venue/state | R_eff (SOL) | impact of +1 SOL net | SOL net to double price | SOL net to 10x |
|---|---|---|---|---|
| curve r=0 | 30 | 6.78% | 12.4 | 65 |
| curve r=50 | 80 | 2.52% | 33.1 | 173 |
| curve end (vs=115) | 115 | 1.75% | 47.6 | 249 |
| pool just after migration | 84.99 | 2.37% | 35.2 | 184 |

### A1 Scenario base: dev 2 SOL + 6 snipers x 1.5 SOL at creation, ~organic flow (lognormal median 0.8 SOL, 15% sells) to graduation, then 60 pool orders (55% sell bias)

#### S1 snipers dump at r=15 SOL (curve), dev holds
final state: phase=pool, pool/curve SOL reserve=69.83, price=2.772e-01, mcap=277 SOL, fees paid=2.582 SOL, mig fee=0.015
| class | # | SOL in | SOL out (realised) | tokens held (M) | % supply | realised PnL | PnL marked @spot | PnL if all liquidate (sequential) |
|---|---|---|---|---|---|---|---|---|
| dev | 1 | 2.00 | 0.00 | 66.3 | 6.63% | -2.00 | +16.38 | +12.37 |
| sniper | 6 | 9.00 | 10.49 | 0.0 | 0.00% | +1.49 | +1.49 | +1.49 |
| organic | 135 | 129.43 | 57.51 | 681.8 | 68.18% | -71.92 | +117.11 | -34.69 |
- sum realised PnL = -72.424 ; sum marked@spot = +134.979 ; sum liquidation = -20.832
- identity check: -(fees 3.225 + migfee 0.015 + SOL left in market 17.593) = -20.832  vs sum liquidation -20.832

#### S2 snipers+dev hold to graduation and dump in first pool block
final state: phase=pool, pool/curve SOL reserve=51.91, price=1.532e-01, mcap=153 SOL, fees paid=2.653 SOL, mig fee=0.015
| class | # | SOL in | SOL out (realised) | tokens held (M) | % supply | realised PnL | PnL marked @spot | PnL if all liquidate (sequential) |
|---|---|---|---|---|---|---|---|---|
| dev | 1 | 2.00 | 5.70 | 0.0 | 0.00% | +3.70 | +3.70 | +3.70 |
| sniper | 6 | 9.00 | 45.94 | 0.0 | 0.00% | +36.94 | +36.94 | +36.94 |
| organic | 128 | 123.47 | 28.26 | 661.1 | 66.11% | -95.21 | +6.04 | -61.32 |
- sum realised PnL = -54.575 ; sum marked@spot = +46.683 ; sum liquidation = -20.685
- identity check: -(fees 3.075 + migfee 0.015 + SOL left in market 17.595) = -20.685  vs sum liquidation -20.685

#### S3 snipers dump on the curve at r=70, dev holds
final state: phase=pool, pool/curve SOL reserve=72.46, price=2.986e-01, mcap=299 SOL, fees paid=3.341 SOL, mig fee=0.015
| class | # | SOL in | SOL out (realised) | tokens held (M) | % supply | realised PnL | PnL marked @spot | PnL if all liquidate (sequential) |
|---|---|---|---|---|---|---|---|---|
| dev | 1 | 2.00 | 0.00 | 66.3 | 6.63% | -2.00 | +17.79 | +13.35 |
| sniper | 6 | 9.00 | 40.63 | 0.0 | 0.00% | +31.63 | +31.63 | +31.63 |
| organic | 172 | 161.48 | 56.03 | 691.0 | 69.10% | -105.45 | +100.86 | -66.61 |
- sum realised PnL = -75.820 ; sum marked@spot = +150.288 ; sum liquidation = -21.623
- identity check: -(fees 4.016 + migfee 0.015 + SOL left in market 17.592) = -21.623  vs sum liquidation -21.623

#### S4 nobody dumps (all hold)
final state: phase=pool, pool/curve SOL reserve=77.70, price=3.433e-01, mcap=343 SOL, fees paid=2.335 SOL, mig fee=0.015
| class | # | SOL in | SOL out (realised) | tokens held (M) | % supply | realised PnL | PnL marked @spot | PnL if all liquidate (sequential) |
|---|---|---|---|---|---|---|---|---|
| dev | 1 | 2.00 | 0.00 | 66.3 | 6.63% | -2.00 | +20.76 | +15.38 |
| sniper | 6 | 9.00 | 0.00 | 219.0 | 21.90% | -9.00 | +66.18 | +16.17 |
| organic | 128 | 123.47 | 54.42 | 488.4 | 48.84% | -69.05 | +98.61 | -52.23 |
- sum realised PnL = -80.053 ; sum marked@spot = +185.540 ; sum liquidation = -20.683
- identity check: -(fees 3.075 + migfee 0.015 + SOL left in market 17.593) = -20.683  vs sum liquidation -20.683

### A2 Bot (1 SOL) entry at different points x exit at different points; Scenario = S2 (snipers+dev dump on pool right after graduation) vs S1

#### Bot PnL (SOL, realised after exit incl. all fees), S2: snipers+dev dump at pool block 0; seeds 1..40 mean [p10 .. p90]
| bot entry | first pool state (before dump) | after sniper/dev dump block | +5 pool orders | +30 pool orders | +60 pool orders |
|---|---|---|---|---|---|
| r=12 | +5.465 [+4.97 .. +5.95] | +0.177 [+0.10 .. +0.23] | +0.291 [+0.11 .. +0.72] | +0.877 [+0.36 .. +1.83] | +1.512 [+0.93 .. +2.16] |
| r=20 | +3.619 [+3.19 .. +3.98] | -0.170 [-0.24 .. -0.13] | -0.083 [-0.20 .. +0.21] | +0.322 [-0.01 .. +0.86] | +0.754 [+0.34 .. +1.33] |
| r=30 | +2.370 [+2.25 .. +2.59] | -0.399 [-0.42 .. -0.37] | -0.333 [-0.42 .. -0.11] | -0.043 [-0.33 .. +0.43] | +0.272 [-0.00 .. +0.62] |
| r=45 | +1.184 [+1.11 .. +1.30] | -0.614 [-0.62 .. -0.60] | -0.569 [-0.62 .. -0.43] | -0.384 [-0.55 .. -0.10] | -0.177 [-0.37 .. +0.08] |
| r=65 | +0.384 [+0.31 .. +0.46] | -0.757 [-0.77 .. -0.75] | -0.730 [-0.77 .. -0.65] | -0.612 [-0.72 .. -0.47] | -0.483 [-0.59 .. -0.31] |
| r=80 | +0.044 [-0.00 .. +0.08] | -0.736 [-0.82 .. -0.02] | -0.749 [-0.82 .. -0.68] | -0.648 [-0.79 .. -0.54] | -0.521 [-0.70 .. -0.41] |

#### Bot PnL (SOL, realised after exit incl. all fees), S1: snipers dumped early at r=15, dev holds; seeds 1..40 mean [p10 .. p90]
| bot entry | first pool state (before dump) | after sniper/dev dump block | +5 pool orders | +30 pool orders | +60 pool orders |
|---|---|---|---|---|---|
| r=12 | +5.571 [+5.27 .. +5.85] | +5.571 [+5.27 .. +5.85] | +5.318 [+4.47 .. +6.62] | +4.161 [+2.54 .. +5.66] | +3.773 [+2.14 .. +5.39] |
| r=20 | +3.751 [+3.54 .. +4.01] | +3.751 [+3.54 .. +4.01] | +3.508 [+2.65 .. +4.37] | +2.649 [+1.55 .. +3.89] | +2.329 [+1.41 .. +3.40] |
| r=30 | +2.398 [+2.23 .. +2.57] | +2.398 [+2.23 .. +2.57] | +2.224 [+1.64 .. +2.82] | +1.594 [+0.79 .. +2.47] | +1.367 [+0.65 .. +2.21] |
| r=45 | +1.210 [+1.11 .. +1.33] | +1.210 [+1.11 .. +1.33] | +1.081 [+0.67 .. +1.40] | +0.675 [+0.20 .. +1.23] | +0.529 [+0.09 .. +1.05] |
| r=65 | +0.407 [+0.36 .. +0.48] | +0.407 [+0.36 .. +0.48] | +0.329 [+0.01 .. +0.55] | +0.067 [-0.27 .. +0.43] | -0.029 [-0.32 .. +0.30] |
| r=80 | +0.051 [+0.00 .. +0.10] | +0.051 [+0.00 .. +0.10] | -0.011 [-0.22 .. +0.14] | -0.201 [-0.44 .. +0.04] | -0.272 [-0.48 .. -0.03] |

#### A3 Example fixed-seed trade log, S2 with bot in at r=45 and out +5 pool orders (seed 7)
#### S2 + bot(r=45 -> pool+5)
final state: phase=pool, pool/curve SOL reserve=53.89, price=1.651e-01, mcap=165 SOL, fees paid=2.615 SOL, mig fee=0.015
| class | # | SOL in | SOL out (realised) | tokens held (M) | % supply | realised PnL | PnL marked @spot | PnL if all liquidate (sequential) |
|---|---|---|---|---|---|---|---|---|
| dev | 1 | 2.00 | 5.52 | 0.0 | 0.00% | +3.52 | +3.52 | +3.52 |
| sniper | 6 | 9.00 | 43.47 | 0.0 | 0.00% | +34.47 | +34.47 | +34.47 |
| organic | 127 | 121.93 | 27.83 | 673.5 | 67.35% | -94.10 | +17.08 | -58.26 |
| bot | 1 | 1.00 | 0.60 | 0.0 | 0.00% | -0.40 | -0.40 | -0.40 |
- sum realised PnL = -56.516 ; sum marked@spot = +54.665 ; sum liquidation = -20.671
- identity check: -(fees 3.061 + migfee 0.015 + SOL left in market 17.595) = -20.671  vs sum liquidation -20.671


### B-1 Zero-sum identity checks (full liquidation of every holder)
| seed | sum trader PnL (all liquidated) | fees leaked | migration fee | SOL left in AMM (locked LP) | -(fees+mig+locked) | residual |
|---|---|---|---|---|---|---|
| 1 | -20.0769 | 2.4682 | 0.015 | 17.5937 | -20.0769 | -1.07e-14 |
| 2 | -20.4150 | 2.8061 | 0.015 | 17.5938 | -20.4150 | +3.55e-14 |
| 3 | -20.5763 | 2.9662 | 0.015 | 17.5951 | -20.5763 | -1.42e-14 |
| 4 | -20.3180 | 2.7091 | 0.015 | 17.5939 | -20.3180 | -7.46e-14 |
| 5 | -20.6456 | 3.0377 | 0.015 | 17.5930 | -20.6456 | +1.78e-14 |
| 6 | -20.5125 | 2.9042 | 0.015 | 17.5933 | -20.5125 | -4.97e-14 |
| 7 | -20.3774 | 2.7690 | 0.015 | 17.5935 | -20.3774 | -2.84e-14 |
| 8 | -20.7460 | 3.1356 | 0.015 | 17.5954 | -20.7460 | -1.78e-14 |

### B-2 Same for a curve-only life (no graduation): buy a bunch, all sell back -> PnL sum = -fees
curve phase after buys: real SOL 34.88; after liquidation: real SOL 0.00e+00; sum PnL -0.8720 vs -fees -0.8720

### B-3 Who is left holding at graduation (token distribution under S2 base path)
| class | tokens (M) | % of 1B | cost basis SOL | mark @pool spot | liq value into pool | liq/cost |
|---|---|---|---|---|---|---|
| dev | 66.3 | 6.6% | 2.00 | 29.62 | 21.93 | 10.96 |
| sniper | 219.0 | 21.9% | 9.00 | 97.86 | 45.93 | 5.10 |
| organic | 516.4 | 51.6% | 79.21 | 230.77 | 63.25 | 0.80 |

pool tokens 198.4 M = 19.8% of supply (owned by locked LP); traders hold 801.6 M

### B-4 Exit-liquidity attribution (curve): a seller is paid from the SOL previously deposited and not yet withdrawn
- Reserve identity: real_sol(t) = sum_i (net SOL deposited by i, ex fee) = sum over *current holders* of their (cost basis - realised proceeds). A sell of X tokens is funded by whoever is currently net-long in SOL terms, i.e. the later buyers (and bag holders of earlier flows).
- Therefore per-token PnL transfers only along the price path: a token bought at price p_b and sold at p_s gives (p_s - p_b)*n to the seller and the same amount is lost by the buyer chain *holding at the bottom of the chain*; fees (1.25% each side) leak to protocol/creator.

### C1 Dump of X% of total supply on the CURVE at real-SOL level r (holder must exist, i.e. X*1000 <= tokens sold)
Cell: price drop % / SOL proceeds net of 1.25% / buy volume (gross SOL incl. fee) needed from new buyers to push price back to the pre-dump level
| X (supply) | r=10 | r=20 | r=40 | r=60 | r=80 | r=84.9 |
|---|---|---|---|---|---|---|
| 1% | -2% / 0.5 / 0.5 | -3% / 0.8 / 0.8 | -4% / 1.5 / 1.5 | -5% / 2.4 / 2.5 | -6% / 3.6 / 3.7 | -7% / 3.9 / 4.0 |
| 2% | -5% / 1.0 / 1.0 | -6% / 1.5 / 1.5 | -8% / 2.9 / 3.0 | -10% / 4.7 / 4.8 | -12% / 6.9 / 7.1 | -13% / 7.6 / 7.8 |
| 5% | -11% / 2.3 / 2.4 | -14% / 3.6 / 3.6 | -19% / 6.8 / 7.0 | -23% / 10.9 / 11.2 | -27% / 15.9 / 16.3 | -28% / 17.2 / 17.6 |
| 10% | -21% / 4.4 / 4.5 | -25% / 6.6 / 6.8 | -33% / 12.3 / 12.7 | -39% / 19.4 / 19.9 | -44% / 27.7 / 28.4 | -46% / 29.8 / 30.6 |
| 15% | -29% / 6.2 / 6.4 | -34% / 9.3 / 9.6 | -43% / 17.0 / 17.4 | -50% / 26.3 / 26.9 | -56% / 36.8 / 37.7 | -58% / 39.6 / 40.6 |
| 20% | -36% / 7.9 / 8.1 | -42% / 11.7 / 12.0 | -51% / 21.0 / 21.5 | -59% / 31.9 / 32.7 | -65% / 44.1 / 45.2 | -66% / 47.3 / 48.5 |

### C2 Same dump on the POOL right after graduation (pool: 84.985 SOL / 206.9M tok)
| X (supply) | price drop | SOL proceeds net | buy volume to restore price (gross) | effective sell price vs spot |
|---|---|---|---|---|
| 1% | -9% | 3.87 | 3.97 | -5.8% |
| 2% | -17% | 7.40 | 7.59 | -10.0% |
| 5% | -35% | 16.33 | 16.75 | -20.5% |
| 10% | -55% | 27.35 | 28.04 | -33.4% |
| 15% | -66% | 35.27 | 36.17 | -42.8% |
| 20% | -74% | 41.25 | 42.30 | -49.8% |

Closed forms: curve - drop = 1-(vt/(vt+n))^2 ; gross out = vs*n/(vt+n) ; restore volume = gross*(1+f).  pool - identical with (ps, pt).  Restore volume equals what the dumper took out, plus the 1.25% fee: buyers must re-deposit exactly the SOL withdrawn.

### C3 Required buy volume to ABSORB the dump *and* keep market cap flat when the dumper's tokens are re-bought (same quantity as restore); expressed vs organic flow
Example: 10% of supply dumped at r=40 on the curve:
  restore volume = 12.7 SOL = 15% of the whole graduation raise; price drop 33%
  same 10% dumped on pool post-graduation: restore 28.0 SOL, drop 55%; pool dump proceeds 27.3 SOL

### C4 Dump absorption by buying: time series. Sniper cluster (X% supply bought at start for tiny SOL) dumps at r; organic buyers needed to bring price back to the sniper's *entry* mcap level is trivial -> but to bring it back to the PRE-DUMP level requires restore volume above.
| sniper X% | entry cost SOL (incl fee) | dump @r=20 (proceeds, multiple, restore) | dump @r=40 | dump @r=60 |
|---|---|---|---|---|
| 5% | 1.48 | 3.6 SOL (2x) / needs 4 SOL organic | 6.8 SOL (5x) / needs 7 SOL organic | 10.9 SOL (7x) / needs 11 SOL organic |
| 10% | 3.12 | 6.6 SOL (2x) / needs 7 SOL organic | 12.3 SOL (4x) / needs 13 SOL organic | 19.4 SOL (6x) / needs 20 SOL organic |
| 15% | 4.94 | 9.3 SOL (2x) / needs 10 SOL organic | 17.0 SOL (3x) / needs 17 SOL organic | 26.3 SOL (5x) / needs 27 SOL organic |
| 20% | 6.96 | 11.7 SOL (2x) / needs 12 SOL organic | 21.0 SOL (3x) / needs 21 SOL organic | 31.9 SOL (5x) / needs 33 SOL organic |

### C5 Breakeven absorption: how much organic buy volume per sniper-dumped SOL to hold the *price* at the level it had before dump? = (1+f) SOL per 1 SOL taken out (curve) -- independent of dump size. What changes with size is how far price falls if volume is insufficient:
| state | X=5% (25%/50%/100% of restore vol) | X=10% | X=20% |
|---|---|---|---|
| r=20 | -11% / -7% / +0% | -19% / -13% / +0% | -32% / -22% / +0% |
| r=40 | -14% / -10% / +0% | -25% / -17% / +0% | -40% / -28% / +0% |
| r=60 | -18% / -12% / +0% | -30% / -21% / +0% | -47% / -33% / +0% |
| r=80 | -21% / -14% / +0% | -35% / -24% / +0% | -52% / -36% / +0% |
(price vs pre-dump after buyers supply 25%/50%/100% of the restore volume; since reserve vs is path-independent, price = vs_final^2/k)

### D1 BUY slippage (effective price vs spot, INCLUDING the 1.25% fee; fee-free impact in brackets): last curve states vs pool just after graduation
| buy SOL | curve r=60 | curve r=80 | curve r=84 | pool just after graduation |
|---|---|---|---|---|
| 0.5 | 1.81% [0.56%] | 1.70% [0.45%] | 1.69% [0.44%] | 1.84% [0.59%] |
| 1 | 2.36% [1.11%] | 2.16% [0.91%] | 2.13% [0.88%] | 2.43% [1.18%] |
| 2 | 3.47% [2.22%] | 3.07% [1.82%] | crosses grad | 3.60% [2.35%] |
| 5 | 6.81% [5.56%] | 5.80% [4.55%] | crosses grad | 7.13% [5.88%] |
| 10 | 12.36% [11.11%] | crosses grad | crosses grad | 13.02% [11.77%] |
| 25 | 29.03% [27.78%] | crosses grad | crosses grad | 30.67% [29.42%] |
| 50 | crosses grad | crosses grad | crosses grad | 60.08% [58.83%] |

### D2 SELL slippage (shortfall of net proceeds vs spot*tokens, including 1.25% fee). Size given as SOL-equivalent at spot (tokens = S/spot)
| sell SOL-eq | curve r=60 | curve r=80 | curve r=84.9 | pool just after graduation |
|---|---|---|---|---|
| 0.5 | 1.80% | 1.70% | 1.68% | 1.83% |
| 1 | 2.34% | 2.14% | 2.10% | 2.40% |
| 2 | 3.40% | 3.01% | 2.94% | 3.52% |
| 5 | 6.45% | 5.54% | 5.37% | 6.74% |
| 10 | 11.12% | 9.48% | 9.16% | 11.64% |
| 25 | 22.72% | 19.54% | 18.90% | 23.69% |
| 50 | 36.52% | 32.11% | 31.19% | 37.82% |
| 100 | 53.22% | 48.27% | 47.20% | 54.63% |
| 200 | - | 64.96% | 63.97% | 70.55% |
| 400 | - | - | - | 82.69% |

### D3 Ratio: sell slippage excluding fee, pool / curve(r=84.9) at the same SOL-eq size (depth cliff)
| sell SOL-eq | curve slip (no fee) | pool slip (no fee) | pool/curve |
|---|---|---|---|
| 1 | 0.86% | 1.16% | 1.35x |
| 5 | 4.16% | 5.55% | 1.33x |
| 10 | 7.99% | 10.53% | 1.32x |
| 25 | 17.84% | 22.72% | 1.27x |
| 50 | 30.28% | 37.03% | 1.22x |
| 100 | 46.49% | 54.05% | 1.16x |
| 200 | 63.47% | 70.17% | 1.11x |

### D4 Sequence across the boundary: a single big BUY that straddles graduation (synthetic migration) vs the same two buys split
- start r=80 (5 SOL left on curve): buy 100 SOL -> 121.3M tokens, avg price 8.247e-01, post-grad pool price 1.817e+00 (x4.42 of curve-end price), pool SOL 178.8
- start r=80 (5 SOL left on curve): buy 120 SOL -> 131.1M tokens, avg price 9.157e-01, post-grad pool price 2.241e+00 (x5.45 of curve-end price), pool SOL 198.5
- start r=80 (5 SOL left on curve): buy 150 SOL -> 142.6M tokens, avg price 1.052e+00, post-grad pool price 2.960e+00 (x7.20 of curve-end price), pool SOL 228.2

### D5 Round-trip cost for 1/5/10 SOL: enter at r then exit immediately at same-state (reset) vs enter at curve end and exit into the pool (price flat)
| SOL | curve r=0 | r=30 | r=60 | r=80 | pool (post-grad) |
|---|---|---|---|---|---|
| 1 | 2.47% | 2.47% | 2.47% | 2.47% | 2.47% |
| 5 | 2.47% | 2.47% | 2.47% | 2.47% | 2.47% |
| 10 | 2.47% | 2.47% | 2.47% | 3.23% | 2.47% |

### E1 Entry-point scorecard (1 SOL buy at real-SOL level r; all numbers computed)
| entry r | entry mcap SOL | tokens bought | breakeven price mult (1 SOL, exit same state) | price mult left to grad | SOL back if graduates & sold on first pool state (net of 2 fees) | = PnL | net SOL demand needed for 2x |
|---|---|---|---|---|---|---|---|
| 0 | 28 | 34.2M (3.42%) | 1.025x | 14.70x | 11.905 | +1090.5% | 12.4 |
| 5 | 38 | 25.2M (2.52%) | 1.025x | 10.80x | 9.126 | +812.6% | 14.5 |
| 10 | 50 | 19.4M (1.94%) | 1.025x | 8.27x | 7.192 | +619.2% | 16.6 |
| 20 | 78 | 12.5M (1.25%) | 1.025x | 5.29x | 4.771 | +377.1% | 20.7 |
| 30 | 112 | 8.7M (0.87%) | 1.025x | 3.67x | 3.382 | +238.2% | 24.9 |
| 40 | 152 | 6.4M (0.64%) | 1.025x | 2.70x | 2.517 | +151.7% | 29.0 |
| 50 | 199 | 4.9M (0.49%) | 1.025x | 2.07x | 1.944 | +94.4% | 33.1 |
| 60 | 252 | 3.9M (0.39%) | 1.025x | 1.63x | 1.546 | +54.6% | - |
| 70 | 311 | 3.1M (0.31%) | 1.025x | 1.32x | 1.258 | +25.8% | - |
| 80 | 376 | 2.6M (0.26%) | 1.025x | 1.09x | 1.043 | +4.3% | - |
| 84 | 404 | 2.4M (0.24%) | 1.025x | 1.02x | 0.972 | -2.8% | - |

### E2 Post-graduation: demand needed for multiples above graduation price
| price multiple above graduation price | net SOL into pool | gross incl 1.25% fee | vs 85 SOL curve raise |
|---|---|---|---|
| 1.5x | 19.1 | 19.3 | 0.22x of whole curve raise |
| 2x | 35.2 | 35.6 | 0.41x of whole curve raise |
| 3x | 62.2 | 63.0 | 0.73x of whole curve raise |
| 5x | 105.1 | 106.4 | 1.24x of whole curve raise |
| 10x | 183.8 | 186.1 | 2.16x of whole curve raise |
| 14.7x | 240.9 | 243.9 | 2.83x of whole curve raise |

### E3 Where is the aggregate-exit haircut: SOL obtainable if every holder sells everything, as function of progress (curve) vs after graduation
| state | reserve SOL | recoverable if all exit | left stuck |
|---|---|---|---|
| curve r=20 | 20.0 | 100% of net deposits (before fees) | n/a |
| curve r=40 | 40.0 | 100% of net deposits (before fees) | n/a |
| curve r=60 | 60.0 | 100% of net deposits (before fees) | n/a |
| curve r=80 | 80.0 | 100% of net deposits (before fees) | n/a |
| curve r=84.9 | 84.9 | 100% of net deposits (before fees) | n/a |
| after graduation (all 793.1M back into pool) | 84.985 | 67.4 gross = 79.3% | locked: 17.6 SOL |

