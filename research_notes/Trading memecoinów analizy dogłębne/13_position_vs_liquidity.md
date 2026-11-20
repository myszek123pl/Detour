# Optimal position size relative to pool liquidity (memecoins): constant-product and pump.fun simulation

Scripts: `/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/sim2.py` (final; output in `out.txt` there). `sim.py` there is a discarded first attempt with a modelling bug, not used.

## Simulation assumptions (read first)
- A1. CPMM x*y=k. R = quote-side reserve in USD. TVL = 2R (liquidity at the usual "TVL" definition). A position of P USD is P/R of the quote reserve and P/TVL = P/(2R).
- A2. Fee is charged on input on each side and stays in the pool. The 0.25%/side Raydium-style fee is a modelling assumption (not verified by search); a 1.00%/side variant is also run.
- A3. Pump.fun: virtual reserves 30 SOL / 1.073B tokens, 793.1M tokens sold to graduation (sourced below), SOL = $150 (assumption). Fee 1.25%/side is a single-source claim; another source suggests 1%. Both are run. Fee leaves the curve (not retained in reserves).
- A4. Two bookends for the exit:
  - "persist": nobody trades between our entry and exit, so the pool stays where our buy left it. Cost is only the fees (about 2f). Impact is fully refunded on the way out.
  - "reset": fair price is unchanged and arbitrage or other flow restores the pool to its entry reserves before we sell. We then pay impact on both entry and exit. This is the conservative case and the one used for the max-size tables. Real memecoin outcomes lie between the two, depending on whether other traders keep the post-buy price.
- A5. "Round-trip cost" = 1 - (USD proceeds / P) at an unchanged fair price. Gas, priority fees, Jito tips and MEV/sandwich losses are excluded unless noted. Slippage tolerance, failed transactions and latency are not modelled.
- A6. Other traders' flow is modelled as a net buy/sell volume (fraction of R) hitting the pool before our exit. In the Monte Carlo it is drawn from N(0, s*R) with no skew. Real flow is autocorrelated and fat-tailed, and that is not captured.
- A7. No LP withdrawal (rug) risk and no concentrated liquidity. Pool depth is assumed constant.

## 1. How does round-trip cost scale with position/liquidity?

### Takeaway
Under "reset", round-trip cost is about 2*(P/R) + 2f = 4*(P/TVL) + 2f, so each 1% of TVL you take costs roughly 4% round trip, on top of fees. Under "persist" you pay only fees, but you still hold the risk that others restore the price. Fee-dominated below about 0.1% of TVL, impact-dominated above 0.5% of TVL.

### Cited Findings
- The effective execution price in a constant-product pool exceeds the spot price by a term of order dx/x, so large trades get progressively more expensive — [Raydium constant-product docs](https://docs.raydium.io/algorithms/constant-product.md) via search summary
- Paradigm heuristic: price impact is roughly twice the size of your order relative to the pool; Raydium notes this is an upper bound, with a 10%-of-reserves example giving about 10.3% impact rather than 20% — [Paradigm: Understanding AMMs Part 1](https://paradigm.xyz/2021/04/understanding-automated-market-makers-part-1-price-impact), [Raydium docs](https://docs.raydium.io/algorithms/constant-product.md)
- Worked example with a 100 ETH / 10,000 USDC pool: paying about 1,111.11 USDC for 10 ETH gives 11.11% slippage — [arXiv 2509.16157](https://arxiv.org/pdf/2509.16157)
- Slippage (execution price vs spot) and price impact (change in spot over the trade) are distinct; first-order price impact is about twice slippage — [arXiv 2601.03799](https://arxiv.org/pdf/2601.03799)
- arXiv 2110.09872 separates "linear slippage" (cost of your own trade) from "angular slippage" (effect on later prices) — [arXiv 2110.09872](https://www.arxiv.org/pdf/2110.09872)
- Foundational CFMM framework (the term "constant function market maker") — [Angeris & Chitra 2020, arXiv 2003.10001](https://arxiv.org/abs/2003.10001v4)

### Simulation results (f = 0.25%/side, my model; see A1-A5)
| P/R | P/TVL | persist (fees only) | reset total | reset no-fee | approx 2P/R+2f |
|---|---|---|---|---|---|
| 0.001 | 0.05% | 0.50% | 0.70% | 0.20% | 0.70% |
| 0.005 | 0.25% | 0.50% | 1.48% | 0.99% | 1.50% |
| 0.01 | 0.5% | 0.49% | 2.44% | 1.96% | 2.50% |
| 0.02 | 1% | 0.49% | 4.31% | 3.85% | 4.50% |
| 0.05 | 2.5% | 0.48% | 9.51% | 9.09% | 10.50% |
| 0.10 | 5% | 0.45% | 17.03% | 16.67% | 20.50% |
| 0.20 | 10% | 0.42% | 28.85% | 28.57% | 40.50% |
| 0.50 | 25% | 0.33% | 50.16% | 50.00% | 100.50% |

### Inferences
- The linear approximation 2P/R + 2f is accurate (within about 0.1 pp) up to about P/R = 2%, and overstates cost beyond that. The exact no-fee reset cost is 2r/(1+r) (consistent with Raydium's note that the "2x" rule is an upper bound).
- Cost does not depend on absolute TVL, only on P/TVL, so the same ratio applies at $10k and $1M.

### Gaps
- Fee tier of any specific venue (Raydium AMM, PumpSwap, Meteora) was not verified here.

## 2. Pump.fun bonding curve

### Takeaway
The curve starts with a thin virtual quote reserve (30 SOL, about $4.5k at SOL=$150), so a $500 round trip with 1.25% fees costs about 20% early and about 8% near graduation. The 2x1.25% fee floor alone (2.5%) is higher than the CPMM's 0.5%.

### Cited Findings
- Initial virtual reserves about 1.073B tokens and 30 SOL; about 793M tokens available to the curve; graduation at about 85 real SOL (115 SOL total), leaving roughly 280M tokens — [DeepWiki pump bonding curve](https://deepwiki.com/pump-fun/pump-public-docs/3.1-pump-bonding-curve-mechanism), consistent with [OnChainDivers](https://onchaindivers.substack.com/p/the-176-sol-ghost-reverse-engineering) and other search hits
- Fee: one source says 1.25% total per trade split between creator and protocol; a different page refers to 1% — the figure is not confirmed across sources — see [Mobula bonding curve docs](https://docs.mobula.io/almanac/bonding-curves) and [skillselion pumpfun mechanics](https://skillselion.com/skills/agiprolabs/claude-trading-skills/pumpfun-mechanics) (low-quality aggregators; treat as unverified)
- One source reports pump.fun moving to a dynamic fee model — [Blockworks](https://blockworks.co/news/pumpdotfun-fee-model) (title seen only; not fetched, so current fee schedule is unverified)

### Simulation results (reset mode, SOL=$150, my model)
Max position for round-trip cost under the threshold, fee 1.25%/side:
| Real SOL raised | virtual quote | approx mcap | <3% | <5% | <10% | cost of $100 / $500 / $2000 |
|---|---|---|---|---|---|---|
| 0 | $4.5k | $4.2k | $12 | $60 | $190 | 6.6 / 20.0 / 48.1% |
| 10 | $6.0k | $7.5k | $16 | $80 | $254 | 5.6 / 16.3 / 41.2% |
| 30 | $9.0k | $16.8k | $24 | $121 | $381 | 4.6 / 12.1 / 32.2% |
| 60 | $13.5k | $37.7k | $36 | $181 | $571 | 3.9 / 9.1 / 24.6% |
| 85 | $17.3k | $61.6k | $46 | $231 | $729 | 3.6 / 7.8 / 20.7% |

With a 1.00% fee: at 85 SOL raised the limits are $91 / $276 / $775; at 0 SOL raised $24 / $72 / $202.

### Inferences
- Pump.fun has no outside arbitrage that "resets" the curve, so "persist" (cost = fees about 2.0-2.5%) applies if nobody else trades; in practice the exit depends on later buyers. The reset numbers are the cost if you need price to be at the same level when you leave.
- Bonding-curve depth in USD is only $4.5k-$17k, so positions above a few hundred dollars are already a meaningful share of the curve.

### Gaps
- Current pump.fun and PumpSwap fee values and any creator-fee changes were not confirmed from a primary source.
- SOL price assumed; scaling to a different SOL price shifts all USD limits proportionally.

## 3. Effect of other traders' flow

### Takeaway
Other traders' net flow of only 2-5% of R moves your outcome by 4-14 percentage points, far more than the round-trip cost of a small position. A small position is mostly a bet on flow, not a fee problem; a large position (above 2.5% of TVL) has a cost that flow rarely offsets.

### Cited Findings
- No sources found directly quantifying flow versus position size for memecoin pools; this section is my simulation only (see A6).

### Simulation results (R=$50k, TVL=$100k, f=0.25%, reset mode)
Deterministic other net flow, P=$1,000 (1% of TVL): pnl at flow = -10%R: -22.3%; -5%: -13.6%; -2%: -8.1%; 0: -4.3%; +2%: -0.5%; +5%: +5.4%; +10%: +15.6% (persist mode: -19.2 / -10.1 / -4.4 / -0.5 / +3.5 / +9.6 / +20.2%).

Monte Carlo, flow ~ N(0, s*R), 20,000 draws, 5th/95th percentile pnl:
| P (% TVL) | s=0 | s=2%R | s=5%R | s=10%R |
|---|---|---|---|---|
| $500 (0.5%) | -2.4% | -8.8% / +4.0% | -17.8% / +14.1% | -32.1% / +32.6% |
| $2,500 (2.5%) | -9.5% | -15.2% / -3.6% | -23.5% / +6.0% | -36.5% / +21.7% |
| $5,000 (5%) | -17.0% | -22.2% / -11.7% | -29.6% / -3.5% | -41.3% / +11.1% |

### Inferences
- Mean cost barely changes with symmetric flow (variance rises, mean slightly falls from convexity), so flow adds risk, not expected cost, in this symmetric model. With skewed (net selling after launch hype) flow it is a pure loss.
- Take-away for sizing: size so that the impact cost (4x P/TVL) is no more than the fee floor, i.e. P below about 0.1-0.25% of TVL, unless you have an edge on the flow direction.

### Gaps
- Empirical distribution of memecoin pool flow (autocorrelation, skew) was not found; the normal distribution here is a placeholder.

## 4. Required gross move to profit

### Takeaway
At unchanged pool depth, you need the fair price to rise by roughly the round-trip cost, slightly more for big positions: +1.3% at 0.2% TVL, +4.6% at 1% TVL, +21.6% at 5% TVL, +44.6% at 10% TVL.

### Cited Findings
- None external; simulation only (reset mode, f=0.25%, drift applied at constant k).

### Simulation results
| P/TVL | cost at flat price | required gross rise in fair price |
|---|---|---|
| 0.2% | 1.29% | +1.31% |
| 1.0% | 4.31% | +4.55% |
| 5.0% | 17.03% | +21.55% |
| 10.0% | 28.85% | +44.60% |

Identical for TVL of $10k, $50k and $250k (depends only on P/TVL).

### Inferences
- The required move is worse than the cost because impact also reduces tokens bought (price rise applies to a smaller position's value).
- With a $2 fixed cost (gas + tip) per round trip, a $2 cost is 1% of a $200 position; so tiny positions are fixed-cost-limited. For a 3% budget at 0.25% fee, the minimum viable size is roughly $100-150 (rough hand estimate, not simulated; the tool's fixed-cost run returned 0 because the tiny-size probe already exceeded budget).

### Gaps
- Gas/tip/MEV figures for Solana were not researched.

## 5. Table: max position for given liquidity and round-trip cost budget

### Takeaway
At 0.25%/side fees, with cost including fees and reset-mode impact: max position is about 0.65% of TVL for a 3% budget, 1.19% for 5%, 2.65% for 10%. With 1% fees: 0.26% / 0.80% / 2.26%.

### Cited Findings
- None external; simulation (A1-A5), TVL = 2R.

### Simulation results
Fee 0.25%/side, no fixed costs:
| TVL | <3% | <5% | <10% |
|---|---|---|---|
| $5k | $32 | $59 | $132 |
| $10k | $65 | $119 | $265 |
| $25k | $162 | $297 | $662 |
| $50k | $323 | $594 | $1,324 |
| $100k | $647 | $1,189 | $2,649 |
| $250k | $1,617 | $2,972 | $6,622 |
| $500k | $3,235 | $5,944 | $13,245 |
| $1M | $6,469 | $11,888 | $26,490 |

Fee 1.00%/side (e.g. launchpad-like fee): $5k: $13 / $40 / $113; $10k: $26 / $80 / $226; $25k: $66 / $201 / $565; $50k: $132 / $402 / $1,129; $100k: $264 / $804 / $2,259; $250k: $661 / $2,010 / $5,647; $500k: $1,321 / $4,021 / $11,294; $1M: $2,643 / $8,041 / $22,588.

Impact-only budget (fees excluded, f=0): $5k: $39 / $66 / $139; $100k: $773 / $1,316 / $2,778; $1M: $7,732 / $13,158 / $27,778.

### Inferences
- Rule of thumb: position <= TVL * (budget - 2f) / 4. Check: 0.25% fee, 5% budget gives (0.05 - 0.005)/4 = 1.1% of TVL (sim 1.19%, linear approximation slightly conservative).
- For $5k-$25k TVL pools, positions of $30-$300 are all that stay under a 3-5% round-trip budget, before gas and MEV.
- These limits assume you need the fair price unchanged at exit; if you expect other buyers to keep price up ("persist" regime), cost reduces to about 2f, but that is a bet on others' flow (section 3).

### Gaps
- Table ignores gas, tips, MEV/sandwich costs and slippage settings.
- TVL in the table is quote+base value; venues that report "liquidity" as quote-side only would shift limits by a factor of 2 (use R instead of TVL: limits roughly halve relative to reported liquidity).
