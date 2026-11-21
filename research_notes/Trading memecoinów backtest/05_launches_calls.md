# 05 - Two public datasets: pump.fun launches and Telegram-style calls

Code: `backtest/other_datasets.py` (first pass), `backtest/launches_calls_deep.py` (this deep dive; raw stdout was not saved to out/, numbers below were copied from the run). Fees assumed 1.25% per side, so FEE factor = 0.9752 round trip. All EVs are per 1 unit staked, net of fees, **before slippage, latency and failed fills**.

## Bottom line

* Neither dataset shows a demonstrated tradeable edge. Both only give the **peak**, so any EV needs an assumption about what happens when the take-profit (TP) is missed - and that assumption decides the sign.
* Launches: the label is mildly predictable out-of-sample (walk-forward AUC about 0.62; best 5% of picks hit 2x about 45% vs 26% base), and the lift is real but the EV is only positive if a missed trade loses less than about 76% (top 5%) and the entry fill at the 15-min close is achievable. It decays over time (base rate 33.9% Jul, 28.7% Aug, 24.6% Sep).
* Serial-deployer history adds nothing to the model. Hour-of-day: not significant. Day-of-week: weak.
* Calls: hit rates are stable by month (2x about 35-37%, Jul-Oct), nearly flat across entry-mcap buckets, and the headline EV is about 0 at a -50% miss assumption (break-even miss loss about 54%). Entry latency kills it: a 20% worse fill turns +2% into -9%.
* Verdict: no edge shown. The calls dataset in particular is about 1.0x +/- noise after realistic costs; the launches model is the only candidate worth a follow-up, and it needs path data (per-minute prices) to settle.

## 1. Launches (28,327 rows, 2026-07-27 to 2026-09-25)

Gate: trades_15 >= 25 and price_15 >= 1.5e-5 USD (about $15k mc). Entry = 15-min close price; label = best 1-min-bar high in next 5h / entry. Note multiple >= 1 by construction (entry inclusive), only 2.6% equal 1.0.

### 1.1 Base rates and drift

| month | n | share >=2x | median multiple |
|---|---|---|---|
| 2026-07 (from 27th) | 1,423 | 33.9% | 1.58 |
| 2026-08 | 13,692 | 28.7% | 1.46 |
| 2026-09 | 13,212 | 24.6% | 1.38 |

Multiple quantiles: p10 1.03, p25 1.13, p50 1.42, p75 2.08, p90 3.42, p99 12.5. Share >=2x/3x/5x/10x = 27.1/12.8/5.1/1.5%. The base rate falls monotonically, so any static threshold learned early is stale later.

### 1.2 EV bounds for "TP at k, miss = loss L" (all launches, no model)

Trade: buy at 15-min close, sell at k if peak >= k, else lose L (unknown path; could be worse than L if a stop is hit before, or better).

| TP | hit | L=30% | L=50% | L=70% | L=90% | break-even L |
|---|---|---|---|---|---|---|
| 1.5x | 45.6% | +3.8% | -6.8% | -17.4% | -28.0% | 37% |
| 2x | 27.1% | +2.6% | -11.7% | -25.9% | -40.1% | 34% |
| 3x | 12.8% | -3.0% | -20.0% | -37.0% | -54.0% | 27% |
| 5x | 5.1% | -10.3% | -28.8% | -47.3% | -65.8% | 19% |

Unselected, the break-even loss is a low 34% at 2x; memecoins that fail to run usually lose more than that in 5h, so the unfiltered strategy is negative. Upper bound is optimistic: it also assumes TP fills exactly at k although the peak was a 1-min high.

### 1.3 Walk-forward LightGBM (target multiple >= 2)

Biweekly folds, expanding train, first 21 days as minimum train (only 3 test folds fit in 60 days; monthly walk-forward shown too). 200 trees, 15 leaves, features: all 15-min windows + derived (buy share, buy/sell volume imbalance, late-volume ratio). Top-q cut chosen per fold by within-fold quantile (no look-ahead). Test n = 20,474, base 25.9%.

| feature set | pooled AUC | fold AUC (min/med/max) |
|---|---|---|
| base features | 0.616 | 0.570 / 0.628 / 0.642 |
| + hour, dow, dev history | 0.617 | 0.569 / 0.629 / 0.643 |
| monthly WF, Aug (train Jul only, 1.4k rows) | 0.575 | |
| monthly WF, Sep (train Jul-Aug) | 0.588 | |

Selected-top-q results (base feature set), EV with TP=2x:

| top q | n | hit 2x | hit 3x | EV L=30% | EV L=50% | EV L=70% | break-even L |
|---|---|---|---|---|---|---|---|
| 2% | 411 | 50.9% | 32.4% | +32.7% | +23.1% | +13.6% | 98% |
| 5% | 1,025 | 44.7% | 26.5% | +24.9% | +14.1% | +3.3% | 76% |
| 10% | 2,049 | 39.9% | 23.2% | +18.8% | +7.1% | -4.6% | 62% |
| 20% | 4,096 | 36.1% | 19.7% | +14.1% | +1.6% | -10.8% | 53% |

Stability: monthly AUC Aug 0.643 -> Sep 0.593; the top-5% hit rate fell 49.2% (Aug, n=362) -> 42.2% (Sep, n=663) with the base falling 28.3% -> 24.6%. The lift ratio (about 1.7x) is roughly preserved, the absolute hit rate is not. Top-2% is small-sample (n=411, 95% CI roughly +/-5pp on hit rate).

Feature importance (gain, share of total, base model): price_15 0.157, sells_15 0.092, sell_vol_15 0.078, growth_15 0.053, avg_5 0.046, vol_late 0.041, avg_10 0.038, sells_5 0.037, sell_vol_10 0.036, buy_share15 0.033. So the model leans on entry mcap and sell activity, i.e. "how many sells happened" (liquidity/real interest), not on simple buy pressure.

### 1.4 Simple univariate rules (2x hit rate; H1/H2 = first/second half of the period, base 29.5% / 24.6%)

| rule | n | all | H1 | H2 |
|---|---|---|---|---|
| growth_15 > q75 | 7,082 | 33.7% | 35.2% | 31.7% |
| mc15 20-30k | 3,113 | 31.4% | 32.9% | 29.2% |
| mc15 < 20k | 3,195 | 30.0% | 33.4% | 25.3% |
| trades_15 > q75 | 7,082 | 28.5% | 31.8% | 27.0% |
| buy_share15 > 0.55 | 23,025 | 26.0% | 28.7% | 23.3% |
| avg_15 > q75 (big tickets) | 7,082 | 19.7% | 21.5% | 18.2% |
| trades_15 < q25 | 7,082 | 23.1% | 24.7% | 21.7% |

Quintiles: buy_share15 (buys/trades) is monotonically negative - lowest quintile 31.4% 2x vs highest 18.6% (heavily one-sided buying with few sells = bot-inflated/low-sell-liquidity). trades_15 low quintile 22.0%, upper three 29-30%. mc15 buckets: 15-17k 28.4%, 17-20k 31.3%, 20-25k 32.2%, 25-35k 30.0%, 35-50k 29.8%, 50-100k 33.9%, >100k 24.0% (and p(>=3x) drops from 18% to 9%). Rules shift hit rate by only 3-8pp and every one decays from H1 to H2 along with the base rate; none is alone enough to reach a positive EV unless misses are mild.

### 1.5 Time effects

| test | result |
|---|---|
| hour-of-day (UTC) 2x rate | range 24.3% (14h) - 29.9% (7h); chi2 p = 0.18 (not significant); half-to-half correlation of hourly rates 0.08 |
| day-of-week | Mon 27.2, Tue 28.4, Wed 27.9, Thu 28.1, Fri 25.8, Sat 26.9, Sun 24.8%; chi2 p = 0.0026; half-to-half correlation 0.44. Sunday and Friday weakest, effect about 3pp and could be partly the downward drift |

Launch volume itself peaks 13-21h UTC (about 1,300-1,430/h vs about 920/h at 9-11h). Hour/dow added nothing to walk-forward AUC (0.6163 vs 0.6165).

### 1.6 Serial deployers (dev_wallet)

22,950 distinct devs; 93.4% have a single launch in the sample (note: the sample is gated, so this undercounts their true launches), but devs with >=2 launches account for 24.1% of rows. Top dev has 174 launches; top-20 devs: 893 launches, 2x rate 28.1%.

| dev's previous launches in sample | n | 2x rate | median multiple |
|---|---|---|---|
| 0 (first seen) | 22,950 | 26.8% | 1.43 |
| 1 | 1,517 | 28.9% | 1.43 |
| 2 | 674 | 27.2% | 1.44 |
| 3-4 | 764 | 27.5% | 1.40 |
| 5-9 | 991 | 28.1% | 1.40 |
| 10+ | 1,375 | 28.1% | 1.36 |

Dev history computed strictly from earlier launches (expanding, current row excluded), for rows with >=1 prior launch (n=5,321):

| dev's prior hit rate (>=2x) | n | next-launch 2x rate |
|---|---|---|
| 0% | 1,750 | 23.6% |
| 0-25% | 912 | 27.2% |
| 25-50% | 1,739 | 30.0% |
| 50-99% | 304 | 30.3% |
| 100% | 616 | 36.2% |

Univariate AUC of prior hit rate on those rows 0.553 (mean prior log multiple 0.549), correlation 0.086 - a real but small signal, and most of the 100% bucket are devs with only 1 prior launch (noisy). Adding dev_prev_n, prior hit rate and prior mean-log to the LightGBM changed pooled AUC from 0.6163 to 0.6165, i.e. nothing beyond what the 15-min features already carry (devs whose tokens run also have good 15-min features). Serial devs are not systematically better than first-timers (26.8% vs 28%). Whether the heavy deployers are bundlers/rug farms cannot be seen here.

### 1.7 Caveats (launches)

* Entry price = 15-min **last bar close**, not an executable fill; slippage on a $15k+ mc curve with thousands of trades in 15 min is material, and the sample is gated on survivors of the first 15 min.
* The label peak is a 1-min high: the first minute after entry's high-low may be unobtainable; TP-fill at exactly 2x is optimistic.
* Only 60 days, one regime, and monotone decay in hit rate; 3 walk-forward folds is a weak test of stability.
* Misses: the data cannot say whether a non-2x token went to 0.3x or 1.9x. The EV rows above are the bound set, not a measurement.

## 2. Calls (12,988 calls, 2026-06-30 to 2026-11-20)

Entry = market cap at call; `peak` = best multiple after the call (ratchet, unknown horizon; the README says the peak is not revised down). No duplicate mints; about 91 calls/day, median gap 574 s.

### 2.1 Monthly stability (hit rates from call mcap)

| month | n | >=1.5x | >=2x | >=3x | >=5x | median peak | median mc | peak<=1.0 |
|---|---|---|---|---|---|---|---|---|
| 2026-07 | 2,672 | 57.1% | 36.7% | 22.4% | 11.6% | 1.64 | 10.7k | 4.9% |
| 2026-08 | 3,378 | 53.0% | 35.3% | 22.4% | 11.9% | 1.57 | 12.9k | 6.6% |
| 2026-09 | 2,707 | 51.3% | 34.5% | 20.9% | 11.0% | 1.53 | 14.9k | 10.0% |
| 2026-10 | 2,495 | 52.4% | 35.2% | 19.6% | 9.5% | 1.54 | 14.5k | 9.5% |
| 2026-11 (to 20th) | 1,722 | 65.1% | 44.4% | 25.0% | 12.1% | 1.81 | 10.6k | 1.2% |

(2026-06: 14 calls, ignore.) Overall 2x = 36.7% with a bootstrap 95% CI of 35.9-37.5%. Jul-Oct are very stable; Nov jumps (also the lowest "never went up" share, 1.2% vs 5-10%) with a lower median call mc (10.6k vs 14.5k); a ratchet peak would be biased low, not high, for young calls, so this is an unexplained regime or calling-policy change, not a censoring artifact. Peak quantiles: p5 1.00, p25 1.20, p50 1.61, p75 2.71, p90 5.4, p99 34; 25% of calls never exceeded 1.2x.

### 2.2 By entry mcap bucket

| call mc | n | >=1.5x | >=2x | >=3x | >=5x | median peak |
|---|---|---|---|---|---|---|
| <5k | 270 | 30.7% | 19.6% | 13.7% | 5.9% | 1.12 |
| 5-8k | 1,025 | 57.5% | 37.9% | 22.1% | 13.1% | 1.64 |
| 8-12k | 4,428 | 53.9% | 35.1% | 21.2% | 11.0% | 1.58 |
| 12-20k | 5,145 | 55.7% | 37.8% | 22.5% | 11.4% | 1.64 |
| 20-35k | 1,913 | 58.9% | 39.8% | 23.4% | 11.4% | 1.68 |
| 35-60k | 175 | 52.6% | 33.7% | 22.9% | 12.6% | 1.60 |

Almost flat (Spearman mc vs peak 0.05). Only the <5k tail is worse (likely calls on tokens already collapsing). Month x bucket 2x rates for 8-30k are within 33-46% every month; the <8k bucket is unstable (20% to 54%).

### 2.3 Time of day (UTC) and weekday

| block | n | 2x rate | median peak |
|---|---|---|---|
| 00-03 | 2,073 | 39.3% | 1.66 |
| 04-07 | 1,573 | 39.4% | 1.70 |
| 08-11 | 1,611 | 38.9% | 1.64 |
| 12-15 | 2,307 | 34.0% | 1.57 |
| 16-19 | 2,908 | 34.8% | 1.57 |
| 20-23 | 2,516 | 36.0% | 1.59 |

Hourly 2x range 31.1% (12h) - 43.4% (6h); chi2 p = 0.002 and half-to-half correlation of hourly rates 0.45, so a real but small effect (Asian-night calls about 4-5pp better, when fewer calls are made). Weekday: 35.7-37.9%, flat. Effect is about 5pp - worth less than any realistic entry slippage.

### 2.4 EV bounds, TP at k (all calls; miss loses L)

| TP | hit | L=30% | L=50% | L=70% | L=90% | break-even L |
|---|---|---|---|---|---|---|
| 1.5x | 55.0% | +11.2% | +2.4% | -6.3% | -15.1% | 55.5% |
| 2x | 36.7% | +14.8% | +2.4% | -9.9% | -22.3% | 53.9% |
| 3x | 21.9% | +17.5% | +2.3% | -13.0% | -28.2% | 53.0% |
| 5x | 11.3% | +15.5% | -1.8% | -19.2% | -36.5% | 47.9% |

Monthly EV at TP 2x / L=50%: Jul +2.5%, Aug +0.4%, Sep -0.7%, Oct +0.2%, Nov +13.7%. i.e. roughly zero except November.

Entry latency (price already x(1+d) when you buy; TP stays k x over your entry, so needs peak >= k(1+d)):

| delay d | TP 2x hit | EV L=50% | EV L=70% | TP 3x hit | EV L=50% |
|---|---|---|---|---|---|
| 0% | 36.7% | +2.4% | -9.9% | 21.9% | +2.3% |
| +20% | 28.8% | -9.1% | -22.9% | 17.4% | -8.8% |
| +50% | 21.9% | -19.1% | -34.4% | 13.0% | -19.7% |

Calls are posted early (the 1,033 mints that also appear in the launches file were called a median 46 s after launch, 75th pct 133 s, at median mc 16k vs 30k at the 15-min mark; their median peak 4.4x vs 1.5x for the launches' 15-min-entry label) so the entry mc is the earliest price, and anybody following the call fills later/higher - exactly the cost row above. Peak is measured from the call mc, a price few followers can achieve.

### 2.5 Caveats (calls)

* Source is a single caller's own feed (selection of what they call is unknown; self-published, hash-anchored to prevent edits, not to prevent selection or timing bias). A call-driven buy wave plausibly means d in the +20-50% range for followers (assumption, not measured here).
* Peak is a ratchet over an undefined horizon (can be hours); realizable exits at the peak are not achievable, a TP limit order would fill only if liquidity exists at that moment; a rug can take the price down at the same minute.
* Rows with peak = 1.0 (6.8%) are tokens that never traded higher after the call, so that loss path is observed but the size of the typical loss on non-hits is not.

## 3. Comparison and honest conclusions

| | launches (15-min entry) | calls (call-time entry) |
|---|---|---|
| 2x base rate | 27.1% (drifting 34% -> 25%) | 36.7% (stable 35-37%, Nov 44%) |
| selection signal | LGBM AUC 0.62, top 5% 45% hit | none (mc flat; hour +/-5pp) |
| break-even miss loss at 2x TP | 34% unfiltered; 76% top 5% | 54% |
| time stability | decaying | stable then jump |
| latency sensitivity | entry at close of 15-min bar | high (+20% = -11pp EV) |
| dev history | no incremental value | n/a |

1. Neither shows a proven edge. Both are consistent with "positive-looking only under optimistic miss losses (<= -30..-50%)", which is exactly the unobserved quantity.
2. The launches model is the only thing with real out-of-sample lift (1.7x at top 5%, AUC 0.62 survives monthly walk-forward at 0.58-0.59), but 60 days and 3 folds is thin, the lift appears to be concentrated in entry mcap/sell-count (i.e. liquidity) rather than a hidden signal, and the base rate is falling.
3. A fair experiment requires path data: per-minute OHLC after the 15-min mark to simulate real SL/TP, plus a fill-lag assumption. Without it do not size anything off these EVs.
4. Do not deploy time-of-day or dev-history filters: dev history is redundant, hour effects are +/-5pp at best in calls and insignificant in launches.
