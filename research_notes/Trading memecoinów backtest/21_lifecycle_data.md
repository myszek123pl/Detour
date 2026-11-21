# 21. Memecoin lifecycle from real price paths (empirical)

Scripts: `backtest/lifecycle_build.py`, `lifecycle_a.py` ... `lifecycle_f.py` (run with `python3 -I`). Data treated as untrusted; only parquet/csv were read.

## 0. Data and method (read first)
- **Path data**: `solana-memecoin-dataset` (GMGN, 10-29 Jun 2026). `ohlcv.parquet` = 15m candles for 11,170 tokens, starting at the first 15m boundary AFTER detection (median 8 min after the snapshot; the token is already a median ~9 min old and mostly freshly graduated from pump.fun). So this is the lifecycle **from detection**, not from launch.
- Candles exist only when trades occurred. I forward-filled gaps (price flat, volume 0). After the last candle the token is treated as dead/flat. Median last traded bar = 3h after the first candle; 97% are silent after 24h.
- Sample: 10,130 tokens with a full 72h window inside the dataset (right-censoring removed), 3 tokens with peak>300x dropped as glitches. Glitch clip: 1,606 highs (>10x close) set to max(open,close); 62 lows. Collapses to ~1e-10 with real volume (rugs) were KEPT (real -100%).
- Entry conventions: **A** = open of first candle (~detection + 8 min, optimistic); **B** = close of first candle (what you get after seeing one candle; path from bar 1). Intrabar highs are not capturable; high-based peaks are upper bounds.
- Means are winsorised at 50x. Costs where stated = 10% round trip (fees+slippage+tip), flat assumption.
- `tokens.parquet` labels `max_return_1h/24h` are broken (zero for 99.9%), ignored. Survivorship bias (README): tokens must survive to detection.
- Second dataset: `solana-pumpfun-launches` (28,327 launches Jul-Sep 2026, gated: >=25 trades and >=$15k mcap at 15 min; only `price_15` -> best 1m high within 5h, no path). Used for the peak-multiple distribution only.

## 1. Peak multiple and time to peak
Peak = max high / entry, 72h window.

| | p50 | p75 | p90 | p95 | p99 |
|---|---|---|---|---|---|
| A (entry = bar0 open) | 1.17x | 1.75x | 3.26x | 5.12x | 16.7x |
| B (entry = bar0 close) | 1.04x | 1.46x | 2.55x | 4.08x | 13.5x |
| Launch CSV, 15m price -> 5h best (gated tokens) | 1.42x | 2.08x | 3.42x | 5.07x | 12.5x |

Exceedance P(peak >= x):

| x | 1.5 | 2 | 3 | 5 | 10 | 20 | 50 |
|---|---|---|---|---|---|---|---|
| A, detection set | 32% | 20.5% | 11.2% | 5.3% | 1.9% | 0.8% | 0.25% |
| B | 23.8% | 14.6% | 8.0% | 3.6% | 1.5% | 0.6% | - |
| Launch CSV (post-15m, gated) | 45.6% | 27.1% | 12.8% | 5.1% | 1.55% | 0.46% | 0.12% |

Practically all the upside is decided in the first hours: P(peak>=2x at 24h)=20.3% vs 20.5% at 72h. 86% of peaks occur within 1h of the first candle, 95% within 6h, 99.4% within 24h; 67% of tokens have their peak in the very first candle (i.e. at or right after detection).

Time to peak (B, hours after bar 0), by peak size:

| peak class | share | median t_peak | p75 | p90 |
|---|---|---|---|---|
| <1.25x | 67% | 0.25h | 0.25 | 1.0 |
| 1.25-2x | 18% | 0.5 | 1.0 | 3.25 |
| 2-3x | 6.5% | 1.0 | 2.5 | 7.5 |
| 3-5x | 4.4% | 1.75 | 5.25 | 14.3 |
| 5-10x | 2.2% | 2.25 | 7.25 | 16.6 |
| 10x+ | 1.5% | 7.5 | 16.4 | 27 |

Bigger winners peak later; but even for 2x tokens the median 2x is hit within 15-30 min (first 2x: median 0.25h, p90 3.25h).

Launch CSV conditional (what predicts the post-15m multiple): P(>=2x) rises with volume growth 5->15 min (lowest quintile 17.5% -> top 34%; P(>=5x) 1.2% -> 7.6%); falls with buy share (buy_vol/(buy+sell)): quintiles 30.6/34.5/28.6/23.2/18.4% for P(>=2x) - near-100% buy share (one-sided, wash/bundled) is worst (P(>=5x) 1.1%). Mcap at 15m of $15k-$200k is best (P(5x) 7-9%), >$200k price_15 (mostly mis-scaled/old tokens) is worst (1.8%). Launch hour (UTC 4h bucket) makes no difference (P(2x) 25.7-28.5%).

## 2. Drawdown from peak and its speed
- Max drawdown (close vs running high), 72h: median **-61%**, p75 -86%, p90 -96%. P(maxDD>=30%)=68%, >=50%=57%, >=70%=43%, >=90%=19%.
- Final(72h)/peak: median 0.44, p25 0.16, p10 0.04.
- Speed after the global peak (hours from the peak bar to first close <= level):

| level | P(reached) | median | p75 | p90 | within 1h | within 15m |
|---|---|---|---|---|---|---|
| -30% | 67% | 0 h (same/next bar) | 0.25 | 0.5 | 95% | 83% |
| -50% | 56% | 0.25 | 0.5 | 1.25 | 89% | 68% |
| -70% | 42% | 0.25 | 1.0 | 2.75 | 76% | 51% |
| -90% | 19% | 0.5 | 2.0 | 6.0 | 64% | 44% |

Conditional on a real pump (peak>=2x): P(-50%)=79%, median 0.25h after the peak, p90 1.75h; P(-70%)=66%, median 0.5h; P(-90%)=34%. Pumps are sold into within one-two 15m candles; there is almost no time to exit manually after the top is visible.

## 3. Terminal value vs entry (all detected tokens)
Entry A (bar0 open): median 0.89 at +15m, 0.79 at 1h, 0.675 at 6h, **0.647 at 24h**; P(>entry) 30% -> 19%; P(<0.5x) 23% -> 42%; P(<0.1x) 6% -> 12%; 24h p10 0.07, p90 1.29. Winsorised mean 0.82 at 24h.
Entry B (bar0 close): median 0.97 at +1h, 0.90 at +24h; P(>entry) 18%; P(<0.5x) 26%; P(<0.1x) 7.5%; p10 0.15; wmean 0.89. Nothing changes after ~6h: the value path is frozen by hour 6 (24h and 72h figures identical).
Note the first candle itself: close0/open0 median 0.95, p25 0.67, p10 0.31, p5 0.11 - a quarter of tokens already lost >1/3 inside the first 15m after detection (a late-entry penalty).

## 4. Shapes (first 24h)
### 4a. K-means (k=7, log10 price/entry sampled at 20 points; silhouette k=4..9: .49/.49/.46/.46/.47/.41; dominated by level, so flat tokens split by loss depth)

| cluster | share | peak med / p90 | 1h | 6h | 24h (median x entry) | P(2x) | P(end24>1) | active (median h) |
|---|---|---|---|---|---|---|---|---|
| flat/slow fade (-5%) | 46.9% | 1.06 / 2.6 | 0.97 | 0.95 | 0.95 | 15% | 27% | 1.8 |
| bleed to -60% | 24.1% | 1.23 / 2.6 | 0.50 | 0.41 | 0.39 | 17% | 0.2% | 4.8 |
| fast dump to -85% | 13.3% | 1.23 / 2.2 | 0.21 | 0.16 | 0.15 | 13% | 0.1% | 6 |
| runner / holds gains | 6.9% | 3.9 / 17.9 | 2.2 | 2.5 | 2.4 | 87% | 97% | 2 |
| collapse to ~0 within 1-2h (rug) | 4.1% | 1.3 / 2.9 | 0.06 | 0.02 | 0.02 | 23% | 0 | 7.5 |
| dead at first candle (price ~0) | 3.6% | 1.0 | 0 | 0 | 0 | 0 | 0 | 1.5 |
| spike then zero in 15 min | 1.1% | 2.0 / 8.4 | 0 | 0 | 0 | 50% | 0 | 1.5 |

(The 4.7% in last two clusters are rugs/dead pools: price 0 by the first full candle.) Only ~7% of tokens ever end the first day above entry in a meaningful way.

### 4b. Rule-based taxonomy (24h window, entry A; more useful than k-means for the named patterns)

| shape | share | peak med (p90) | t_peak | 1h | 6h | 24h | wmean24 | active h |
|---|---|---|---|---|---|---|---|---|
| flat/chop (peak<2x, end>=0.5x) | 44.9% | 1.02 (1.54) | 0 | 0.95 | 0.94 | 0.935 | 0.91 | 1.5 |
| **instant dump** (peak<1.25x, <0.5x by 1h) | 19.0% | 1.01 (1.18) | 0 | 0.21 | 0.18 | 0.18 | 0.19 | 2.75 |
| **slow bleed** (peak<2x, end<0.5x, not instant) | 14.6% | 1.43 (1.82) | 0 | 0.42 | 0.27 | 0.25 | 0.25 | 6.5 |
| pump and hold/fade (>=2x, end>=0.5x) | 8.0% | 2.85 (5.7) | 0.5h | 1.54 | 1.31 | 1.24 | 1.52 | 3.75 |
| **pump then dump** (>=2x, end<0.5x) | 6.4% | 2.85 (6.1) | 0.4h | 0.65 | 0.24 | 0.20 | 0.21 | 8.75 |
| **second leg** (-50% from >=1.3x peak, then >=2x off low and >=80% of old peak) | 4.9% | 2.87 (6.7) | 2h | 1.03 | 0.86 | 0.70 | 0.92 | 13.5 |
| **runner** (peak>=5x and >=2x at 24h) | 2.2% | 9.6 (43) | 6.75h | 2.48 | 4.73 | 5.17 | 7.44 | 20 |

Median hours from the peak to -50% in "pump then dump": 0.25 (p75 0.5, p90 0.75). Takeaways: 79% of tokens are flat-to-dead; real pumps (>=2x, 20%) split roughly 40% hold/fade, 32% dump to <50%, 24% second leg, 11% runner. Runners and second-leggers are the only ones with long active lives (13-20h median) - activity itself is a signal.

## 5. Second pumps after a -50% drop
Event = first close at or below (1-X) of the running high, running high >= minimum multiple. "Bounce" measured off the lowest close since the event (high-based, upper bound); window to 72h.

| drawdown | peak>= | n | back to old peak | new ATH (1.2x old) | +100% off low | +50% off low | close back >= ENTRY | still trading 6h after |
|---|---|---|---|---|---|---|---|---|
| -30% | 2x | 1,837 | 30.4% | 22.1% | 45.0% | 63.7% | 72.2% | 84% |
| -50% | 1.3x | 3,217 | 15.2% | 11.6% | 35.4% | 52.4% | 39.8% | 85% |
| **-50%** | **2x** | 1,686 | **17.9%** | **13.5%** | **42.5%** | 60.3% | 62.7% | 86% |
| -70% | 2x | 1,410 | 7.4% | 5.5% | 35.2% | 53.3% | 42.7% | 86% |

Timing (-50% from a >=2x peak): +100% bounce off the low within 1h: 18%; 6h: 35%; 24h: 42%; after 24h nothing new. Back to old peak: 7.8% in 1h, 14% in 6h, 17.9% in 72h. Interpretation: a dead-cat bounce (+50-100% off the low) is common (60%/42%) - but it is a bounce from an already collapsed price and mostly does not reach the old high. A genuine second pump (new ATH >1.2x old peak) after -50% is ~13% of pumpers (~2.2% of all tokens). Bounces are very fast (hours) so they are tradeable only with already resting orders, not a manual reaction. Part of the 'bounce' is bad ticks/thin-liquidity wicks.

## 6. Probability of recovering the ENTRY price after a drop
First close at -X% below entry (A), then close >= entry later (72h; the 24h figure is almost identical):

| drop | P(ever happens) | P(recover entry, close) | P(recover, high) | median time to recover | p90 | P(+100% off that level) |
|---|---|---|---|---|---|---|
| -30% | 57.5% | **11.7%** | 16.6% | 1.25h | 9.5h | 10% |
| -50% | 45.4% | **6.6%** | 9.0% | 1.75h | 12.9h | 9% |
| -70% | 30.8% | **2.8%** | 4.0% | 2.9h | 13.9h | 7.8% |
| -90% | 12.8% | 0.4% | 0.5% | 10h | 16h | 3.8% |

If the token had already printed >=1.5x before the drop: -30% -> 15.4% recover, -50% -> 8.0%, -70% -> 3.5% (vs 10.1%/5.9%/2.4% for never-pumped). Recovery is rare; waiting for a recovery is -EV. Contrast with section 5: after a >=2x pump, closing back above entry from -50% off the peak (still above entry) is much likelier (63%) simply because the peak was far above entry - the relevant anchor is the peak, not your entry.

## 7. Volume half-life (USD, 15m candles)
- Volume is concentrated at the start: median share of the 72h volume in the first candle 54%, in the first hour 95%, in 6h ~100%. Median time to 50% of total volume: 0 (first candle), p75 0.5h, p90 2h; 90% of volume by median 0.5h (p75 2.25h, p90 6.75h).
- Volume peak window (rolling 1h) starts at hour 0 for >90% of tokens; the price peak coincides with it (91.6% price peak at/before the end of the volume-peak hour).
- Rolling-1h volume falls to 50% of its peak within 0.25h (median), 0.5h (p75), 1h (p90); to 10% within 0.75h (median), 1.25h (p75), 2.25h (p90). By peak class (median half-life from the volume peak): <1.25x 0.25h; 1.25-2x 0.25h; 2-5x 0.5h; 5x+ 0.75h (p75 1h). 72h USD volume median: $0.9k / $30k / $94k / $380k for those classes.
- Aggregate (volume-weighted) profile vs hour 0: hour1 18.6%, h2 8.8%, h3 5.3%, h4 3.7%, h6 2.3%, h12 0.8%, h24 0.4%; fitted exponential half-life hours 1-24 = **4.8h** (driven by the few long-lived winners). The median token has zero volume after hour 1.
- At the -50% from peak event (peak>=2x, n=881): volume 1h before the drop is 65% of peak-hour volume, volume in the 2h after is 15% - the drop coincides with volume drying up, not with a panic spike. Volume is a lagging/coincident signal here, not a lead: no volume left means no bounce.

## 8. What this means for buy/sell timing (exit simulations, 10% cost, entry = close of bar 0, 24h)
All numbers are multiples of invested capital (net of 10% cost); hold/exits tested with stops at level (optimistic) and, where marked, at bar close (pessimistic).

| rule | net mean | median | P(win>10%) | exit hit |
|---|---|---|---|---|
| hold 1h | 0.84 | 0.98 | 14% | - |
| hold 6h | 0.81 | 0.91 | 11% | - |
| hold 24h | 0.79 | 0.90 | 10% | - |
| SL -30% TP +100% (optimistic fill) | 0.87 | 0.92 | 13% | 49% |
| SL -30% TP +50% | 0.86 | 0.96 | 19% | 51% |
| SL -50% TP +100% | 0.85 | 0.95 | 16% | 39% |
| SL -30% TP +100% (**pessimistic: bar-close fill**) | 0.81 | 0.92 | 13% | - |
| trailing -30% from high (optimistic) | 0.93 | 0.96 | 15% | 52% |
| trailing -30% (pessimistic) | 0.82 | 0.93 | 11% | - |
| sell half at 2x, other half trail 50%, SL -30% | 0.885 | 0.92 | 13% | - |

No rule is profitable on the unfiltered detection set; the best (trailing -20/-30%, optimistic fill) gets 0.93-0.94 and collapses to 0.81 when rug-gap fills are accounted for. Consistent with the earlier backtests (stage 1: -17% to -34% per trade).

Event studies, entry at event close, 24h forward (median / P(fwd>entry) / P(fwd max >=2x)):
| event | n | med fwd24 | P>entry | P(max>=2x) |
|---|---|---|---|---|
| baseline: first-candle close | 10,127 | 0.90 | 18% | 14% |
| +1h, any token | 10,127 | 0.99 | 18% | 9% |
| +1h, only if price 0.8-1.5x entry and still trading | 1,387 | 0.90 | 28.5% | 17% |
| +6h if still trading | 1,602 | 0.89 | 29% | 17.5% |
| momentum: first CLOSE >=2x | 1,510 | **0.375** | 19.5% | 26% |
| momentum >=3x | 845 | 0.32 | 19.5% | 27% |
| dip -30% from peak (>=2x) | 1,831 | 0.55 | 19% | 26% |
| dip -50% from peak (>=2x) | 1,680 | 0.62 | 20% | 26% |
| dip -70% from peak (>=2x) | 1,406 | 0.73 | 21% | 22% |
| falling knife: first close <=0.5x entry | 4,594 | 0.84 | 17% | 13% |

Conclusions:
1. **The edge window is the first 15-60 minutes after detection; after that the path is frozen.** 86% of peaks in 1h, value path identical at 24h and 72h. Holding for "the second leg" is a lottery: P(second leg)=4.9%, P(runner)=2.2%.
2. **Never buy a confirmed breakout late**: buying the first close >=2x (or 3x) gives median 0.32-0.38 after 24h; the 2x close is usually the local top (P(drop >50%) 56-60%).
3. **Dip-buying a pumped coin is not free money**: median -38% after a -50% dip, only 20% above entry; however P(+100% bounce) is 42% and P(old peak reclaim) 18% - convexity exists but it is paid for by a 41% chance of losing >50% more. Only with a tight stop / small size.
4. **Sell fast into strength**: after a >=2x peak the -50% level comes within a median 15 min; 79% reach -50% and 66% reach -70%. A 2x take-profit hits for ~20% of tokens and a resting limit is the only realistic way to capture it; a trailing -30% beats a fixed hold, but only with fills at the stop level (rug candles gap through).
5. **Stop-loss is mostly a rug filter, not a risk management tool**: 12% of tokens go to <10% of entry and 4% are essentially zero by the first candle; 77% of drawdowns to -30% happen within a bar or two so market stops fill far below the level.
6. **Waiting to "average down/recover" is -EV**: P(recover entry) 11.7%/6.6%/2.8% after -30/-50/-70%.
7. **Filter beats timing**: launch data say growth in volume 5->15 min (top quintile) doubles P(>=2x) vs the bottom, and one-sided (>=80% buy) or already-large mcap launches are worst. Waiting 1h and requiring the token to still trade near entry lifts P(win) to ~28% from 18% but does not make the average positive (survivors still fade; wmean ~0.98 gross).
8. Caveat on conclusions 4-5: first candle starts ~8 min after detection and a quarter of tokens already lost >1/3 by its close; the real bot latency and detection-time price (not in the path data) matter more than any exit rule.

## 9. Limitations
- 20 days, one regime (June 2026), survivorship-biased detection set (GMGN); pump.fun launches CSV is a different regime (Jul-Sep) and gated.
- 15m candles, gaps forward-filled, high-based quantities are upper bounds, no slippage/impact model other than the flat 10% cost; the exit simulations assume fills at the stop/TP level (optimistic) or bar close (pessimistic) as marked.
- The pumper-only k-means (n=2,057 tokens with >=2x) was started but not completed; the rule-based taxonomy replaces it. Silhouette for k=3..7: .42/.35/.30/.25/.26.
