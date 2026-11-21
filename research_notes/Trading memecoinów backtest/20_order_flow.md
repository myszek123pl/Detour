# 20. Order-flow microstructure of Solana memecoins (ian05012/solana-memecoin-dataset, June 2026)

Scripts (all in /home/user/Detour/backtest/, run with `python3 -I`, duckdb for the big tables; no dataset scripts executed):
`of20_build.py` (local duckdb), `of20_sizes.py`, `of20_wallets.py`, `of20_timing.py`, `of20_roundtrip.py`, `of20_bars.py`, `of20_impact.py`, `of20_predict2.py`
(`of20_predict.py` = failed attempt, see 8.4). Numbers below are copied from their output.

## 0. What the data really is (read this first, it limits every claim)

- trades: 9,500,565 rows, 734,407 wallets, 66,990 tokens, $6.70B volume. 99.8% of rows are in June 2026 (a single 20-day regime).
  Only 31,004 of those tokens appear in tokens.parquet; the other ~36k tokens (median 100 trades) are wallet-history pulls.
- Per token the log is a **sample, not the full tape**: median 158 trades (p5 96, p95 338), median time span 977 s. It is the ~200 most recent trades before each snapshot (the README says this for the features). Tokens are detected very early (time_since_launch median 296 s).
- Trade timestamps are integer seconds, so same-second ties are frequent (35% of inter-arrivals are 0 s).
- ohlcv.parquet has 62k duplicated (token, 15m ts) rows (several snapshots re-fetch the same candles); I de-duplicated by taking the max-volume row -> 183,651 unique bars, 11,170 tokens. Candles start median ~8 min AFTER capture, so trade flow and candles overlap only for 31.8k bars / 4.7k tokens.
- On overlapping bars the trade log covers only a fraction of the candle volume (median trades$/candle volume = 0.28; p25 0.12, p75 0.56). Bar-level flow is therefore a noisy partial measurement (attenuation bias in all impact estimates below).
- The tokens.parquet return labels are unusable for this: max_return_1h/6h/24h is 0.0 for 99.9% of rows (median, p99 all 0), although reaches_2x is True for 11%. I did not use them. close_return_1h exists for 47 rows only.
- Survivorship: tokens/bars exist only while they were tracked; mean 15m bar return is -3.0% (log, close/open), 38% of bars are up.

## 1. Trade-size distribution

| side | n | volume $ | mean | p10 | p25 | p50 | p75 | p90 | p99 | p99.9 | p99.99 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| buy | 6.72M | 2.47B | 367 | 0.02 | 0.33 | 14.8 | 71.6 | 247 | 7,617 | 39,103 | 151,442 |
| sell | 2.78M | 4.23B | 1,524 | 0.55 | 9.3 | 58.1 | 289 | 2,527 | 26,963 | 109,343 | 234,202 |

- Buys are 70.8% of trades but only **36.8% of dollar volume**; sells are 29.2% of trades and 63.2% of volume. Sells are ~4x larger on average, 4x at the median, 15.2% of sells are >= $1k vs 3.8% of buys; >= $10k: 3.6% vs 0.8%.
- Dust: 29.9% of buys are < $1 (12.5% of sells); 44% of buys < $10. These are bot/sniper/probe trades; they carry no volume weight.
- Volume is concentrated in few trades: top 0.1% of trades = 17.5% of volume, top 1% = 52.4%, top 5% = 85.7%, top 10% = 93.0%. Trades >= $1k = 94% of sell volume, 83% of buy volume.
- Tail: Pareto MLE with KS-chosen xmin: buys alpha(pdf exponent)=1.71 (xmin $141, KS 0.017), sells alpha=2.53 (xmin $16.8k, KS 0.021). Hill estimators drift up with the threshold (buys 1.71 -> 1.73 -> 2.23 -> 2.55 at q90/95/99/99.9; sells 1.85 -> 2.17 -> 2.61 -> 3.80). Truncated-lognormal beats pure power law in loglik on the same tail for all three fits (LLR negative, e.g. buys -1,624). Conclusion: **heavy-tailed, power-law-like over ~2 decades, but not a clean power law**; the far tail is thinner (alpha 2.5-3.8, finite variance), the body is closer to lognormal. Do not extrapolate a pure Pareto.
- Size depends on token age (age = capture time - time_since_launch): 0-1 min: 88% buys by count, 96.7% by dollars (launch buys); 1-5 min 76% / 70%; 5-15 min 60% / 55%; 15-60 min 50% / 28%; >1h 58% / 30%. Median sell grows from $21 (0-1 min) to $199-247 (>15 min); i.e. exits get larger and buyers smaller as the token ages.

## 2. Who trades: concentration

Wallet level (734k wallets; Gini of volume 0.99):

| | top 1 | top 10 | top 100 | top 1000 | top 0.1% | top 1% | top 10% |
|---|---|---|---|---|---|---|---|
| all volume | 0.47% | 4.6% | 25.3% | 68.0% | 60.7% | 90.7% | 98.8% |
| buy volume | 0.52% | 3.4% | 23.0% | 62.1% | 55.9% | 82.8% | 97.6% |
| sell volume | 0.61% | 6.0% | 27.6% | 73.3% | 48.7% | 93.2% | 99.2% |
| trade count | 0.35% | 2.4% | 4.9% | 13.8% | 11.7% | 38.4% | 77.2% |

- 34% of wallets trade once; median 2 trades; p99 213; 406 wallets with >= 1000 trades make 8.7% of trades and 23.8% of volume. 11,566 wallets that touched >= 100 tokens = 67.5% of volume (bots/pros).
- The 10 biggest wallets: 82% of their volume is sells, median 1,298 trades on 264 tokens. Top 1000 wallets: 67% sells. Whole market: 63% sells. The big wallets are net distributors of tokens that the crowd buys.
- wallets.parquet labels (only 11.8k wallets labelled, but they matter): `insider` wallets (6,126) = **69.2% of volume** with 9.1% of trades, 64.7% of their volume is sells; `smart_money` (1,600) = 8.3% of volume, 73.5% sells; unlabeled (722k) = 21.9% of volume, 87.7% of trades, 54.9% sells.
- Per token (>= 50 trades, n=56,646): top wallet = median 22.5% of token volume (p25 8%, p75 78%, p90 91%); top 5 = 54%; top 10 = 70%. Distribution is bimodal: ~38% of tokens have one trade > 50% of all volume in the log. That trade is a **launch buy**: 98.7% buys, median age -6 s (at/just before launch), median $17k; made by serial wallets that repeat it on 300-730 tokens each with near-constant size (e.g. ~$7.7k, ~$18k, ~$21k median) = launcher/bundler bots. These tokens have mostly liquidity >= $18k (liquidity deciles 6-10: median dominance 0.5-0.73; deciles 1-5: 0.05-0.07), so the dominant buy is in effect the creator's seeding of the pool. For deciles <= 5 volume is spread across ~100 wallets.
- Implication for any "flow" indicator: on ~40% of tokens the raw $ buy flow in the log is mostly one insider/dev trade; use count-based imbalance or exclude trades with age < ~10 s.

## 3. Clustering in time

All numbers per token, intervals <= 1 h (9.41M intervals):
- Inter-arrival: P(0 s)=33.5%, P(<=1 s)=53.6%, P(<=5 s)=79.7%, P(<=30 s)=95.4%; quantiles p25/50/75/90/99 = 0/1/4/13/184 s; mean 11.6 s. 49.4% of trades share their exact second with another trade of the same token (max 161 trades in one second).
- By age: 0-10 s after launch 57% of gaps are 0 s; 1-5 min 28%; 5-15 min 24%; >1 h 19% (median gap 13 s).
- Burstiness: per-token CV of inter-arrivals median 2.72 (Poisson = 1), p10 1.39, p90 6.65; burstiness B=(sd-mean)/(sd+mean) median 0.46. Part of this is non-stationarity (activity decays within the window), so I also detrended: Fano factor of counts median 3.2 (5 s bins), 8.8 (30 s), 13.8 (60 s) (Poisson = 1). Lag-1 autocorrelation of bin counts 0.40 / 0.61 / 0.62 raw, but after subtracting a +-5-bin moving average: -0.02 (5 s), 0.18 (30 s), 0.26 (60 s). So bursts last tens of seconds to minutes; at 5 s resolution the clustering is almost entirely the slow intensity profile plus same-second ties.
- Side clustering: P(next is buy | previous buy)=86.4% vs P(buy | previous sell)=31.7% (unconditional 70.5%). Sign autocorrelation (token-demeaned, +-1 coding): lag1 0.44, lag2 0.43, lag3 0.40, lag5 0.37, lag10 0.32, lag20 0.24, lag50 0.075. Mean run length: buy runs 7.2 trades (iid expectation 3.4), sell runs 3.1 (iid 1.4); P(buy run >= 10)=13.1% (iid 4.4%); P(sell run >= 5)=10.6% (iid 0.7%); longest sell run 2,343 trades (a dump), longest buy run 324. Caveat: the sign has a slow trend (buys early, sells late), which inflates the long-lag ACF; the lag 1-3 value (~0.4) is robust to it because bursts are short. I did not recompute with an age-controlled mean.
- Size clustering: ACF of log trade size lag1 0.42, lag2 0.40, lag5 0.35 (large trades arrive with large trades; also partially bot repeat-size).
- Same-wallet adjacency: 2.2% of consecutive trades are by the same wallet, and only 0.25% of those are the same side, i.e. a wallet that trades twice in a row almost always does buy->sell (or sell->buy): split fills are rare here, alternation is the norm.

## 4. 15-minute price response to flow (impact)

Panel: de-duplicated bars with high <= 10x close (README glitch filter), open/close > 0, trade-log flow B,S summed in the bar, imbalance imb=(B-S)/(B+S), x=(B-S)/liquidity_usd at first capture. Returns are log(close/open) of the same bar (contemporaneous), winsorized 1%; SE clustered by token. n = 31.6k bars with flow and volume > $10 (4,621 tokens). Liquidity bucket = liquidity_usd at first capture (a static, stale proxy: pool depth moves with price).

A. Contemporaneous: ret = a + beta*imb

| liquidity | bars | tokens | beta (per 1.0 of imb) | se | R2 | lambda small flows: ret per 1.0 of net/liq, |x|<5% | se | n |
|---|---|---|---|---|---|---|---|---|
| all | 31,612 | 4,621 | 0.069 | 0.003 | 1.7% | 1.64 | 0.12 | 13,982 |
| < $5k | 601 | 177 | 0.014 | 0.033 | 0.0% | 2.40 | 0.62 | 219 |
| $5-15k | 23,868 | 3,165 | 0.109 | 0.004 | 3.5% | 1.98 | 0.15 | 11,149 |
| $15-40k | 6,232 | 1,057 | 0.000 | 0.006 | 0.0% | 0.58 | 0.21 | 2,308 |
| $40-100k | 830 | 205 | -0.006 | 0.011 | 0.0% | 1.06 | 0.27 | 283 |
| > $100k | 25 | 1 | n/a | | | | | |

- Reading: in $5-15k pools a fully one-sided bar (imb +1 vs -1) differs by ~22 pp of return (2 x 0.109); in >= $15k pools the logged imbalance explains nothing contemporaneously (beta ~0). Honest reasons: (i) the log covers only ~28% of the candle volume, (ii) imbalance in USD of a few hundred dollars in a deep pool is just noise, (iii) liquidity is stale. R2 stays tiny even in the best bucket (3.5%).
- Kyle/AMM form: for small flows (|net|/liq < 5%), +1% of liquidity net buying -> about +1.6% price overall (+2.0% in $5-15k, 95% CI ~1.7-2.3 there; +0.6% in $15-40k). That is the right order of magnitude for a constant-product pool (price impact ~ 2-4 x trade/liquidity depending on whether liquidity_usd counts one or both sides), but measurement error (partial flow capture attenuates, stale liquidity adds noise), so I do not claim a precise lambda. The full-sample linear lambda in $5-15k (0.31) and "all" (-0.008) are garbage because x has outliers up to 86x liquidity; use the small-flow or binned numbers.
- Non-linearity (deciles of x, all buckets, mean bar return): x<-0.19: +1.3% (mostly rebounds after capitulation / artifacts); -0.19..-0.04: -13.1%; -0.04..-0.002: -12.5%; ~0: -6.0%; 0.006-0.02: -5.1%; 0.02-0.04: -3.0%; 0.04-0.08: -1.5%; 0.08-0.16: +2.4%; 0.16-0.35: +8.4%; > 0.35 (mean x 1.37): +25.8%. Monotone and concave in the middle, roughly +8 pp per +0.1 of liquidity for 0.1-0.4. Note the baseline (zero-flow) bar drifts about -6% (the decay of newly launched coins); impact must be read relative to that.

B. Predictive (strictly t -> t+1, consecutive bars only, 30,260 bars, 4,343 tokens): next-bar close-to-close return on imb_t
- all: beta 0.011 (se 0.0023), R2 0.06%; $5-15k: 0.023 (se 0.0028), R2 0.2%; $15-40k: -0.009 (se 0.0046); controlling for r_t the coefficient is unchanged (0.0125). The effect is slight continuation (+2.3% next bar per +1 imbalance in $5-15k pools), statistically significant but an order of magnitude below any realistic round-trip cost for these coins (see sec. 8). Contemporaneous impact is largely mechanical (the trade IS the price move), not information that persists.

## 5. Autocorrelation of flow and returns (within token, consecutive 15 m bars, bootstrap over tokens)

| series | lag1 | lag2 | lag3 | lag4 |
|---|---|---|---|---|
| bar return log(c/o) | -0.063 [-0.071,-0.055] | -0.040 | -0.048 | -0.054 |
| imbalance (bars with flow) | -0.001 | 0.000 | -0.004 | 0.000 |
| log candle volume | 0.671 | 0.558 | 0.469 | 0.394 |

- Returns have small, consistent **negative** autocorrelation at all of lags 1-4 (-4% to -6%, CIs exclude 0); lag-1 by liquidity bucket: < $5k -0.13, $5-15k -0.05, $15-40k -0.11, $40-100k -0.16. This is mean reversion / overshoot-and-fade after pumps and dumps (and partly the survivorship + decay drift being demeaned per token). Volume is strongly persistent (0.67 at lag 1, still 0.39 at 1 h): activity clusters, direction does not.
- Dollar-imbalance at the 15 m bar level has zero autocorrelation (n=22.6k), in contrast with trade-sign autocorrelation of ~0.4 at the single-trade level (sec. 3): order-splitting/herding persists for minutes, not for 15 m bars. I do not report ACF of x (net flow / liquidity): bars without logged flow are zero-filled and it comes out -0.21 spuriously.

## 6. Round-trip / self-trading

Definition: trade is "round-tripped within W" if the SAME wallet has an opposite-side trade in the SAME token within +-W seconds in the log (matched volume = 2*min(buy$,sell$) per wallet-token pair over flagged trades). Lower bounds, because the log is truncated.

| W | % of trades | % of volume | % of buy vol | % of sell vol | matched vol share |
|---|---|---|---|---|---|
| same second | 3.5% | 3.9% | 5.5% | 2.9% | 3.6% |
| 10 s | 9.3% | 7.2% | 10.2% | 5.4% | 6.7% |
| 60 s | 19.6% | 14.5% | 21.1% | 10.7% | 13.3% |
| 5 min | 34.7% | 32.5% | 47.1% | 24.1% | 28.2% |
| 15 min | 46.0% | 53.7% | 70.7% | 43.8% | 43.4% |
| 1 h | 51.5% | 84.5% | | | 52.8% |
| any time in log | 52.8% | 94.2% | | | 53.9% |

- 32.9% of wallet-token pairs trade both sides, and they hold 94% of volume. Most memecoin "volume" is therefore wallets that both buy and sell the same coin; roughly **a seventh of volume has a same-wallet opposite trade within 1 minute and a third within 5 minutes**.
- That is NOT all wash trading: legitimate snipers/flippers do buy-and-sell within minutes. To separate, I used the sell/buy $ ratio of mutually-nearest buy-sell pairs within 5 min (1.62M pairs; ratio ~1 minus fees means no net position change): |ratio-1| <= 2% for 9.8% of pairs (<= 5%: 18.4%), versus **1.0% (2.4%) for a null** (random different-wallet buy in the same token within 5 min). The spike is ~10x null. It grows with size: for buys >= $1k 31.8% of pairs are within 2% (53.6% within 5%), for buys >= $10k 61.9% (73.2%). Same-second share of pairs 10.2%, median gap 43 s. Distribution of sell/buy ratio: <0.5: ~21% (stopped-out dumps), 0.5-0.9 ~33%, 0.9-1.1 ~21%, 1.1-2 ~15%, >2 ~2.5%.
- Big trades: of 5,481 trades >= $100k, 14.9% have a same-wallet opposite trade within 60 s and 35.1% within 5 min; for >= $10k (152,862 trades) 11.9% / 26.7%. The ten largest single trades ($430-470k) are matched pairs (e.g. sell $466,681 / buy $465,841, 59 s apart, same wallet) in tokens whose liquidity is tens of thousands: round-trip/cycling inflates headline volume, rather than genuine $400k+ risk-taking.
- Who: round-trip share (within 5 min, by $): insider-labelled wallets 35.8% (60 s: 15.5%), smart_money 24.9% (7.7%), unlabeled 25.3% (14.0%). Wallets active in >= 100 tokens (67% of volume) 33.7%; wallets active in one token 19.4%.
- Per token: median token has 24% of its volume in 5-min round trips, p75 81.5%, p90 98%; 37% of tokens have > 50% of volume in same-wallet 5-min round trips; 60 s version: median 1.8%, p75 35%, p90 74%. The distribution is bimodal: a clean organic group and a group dominated by wallets cycling.
- Estimate to use: self-matched volume (same wallet, opposite side, within 60 s) ~13-15% of dollar volume overall, up to ~28-33% with a 5-min window (upper bound includes real flips). Exact wash volume is not identifiable without on-chain funding links (wallet_funding.parquet not used here).

## 7. Launch-buy / insider footprint (side result)
38% of tokens (21,647 of 56,646) have one buy > 50% of logged volume at launch (+-seconds), and 7,125 distinct wallets do it; the top serial wallets appear on 320-734 tokens each at stable sizes. Volume-weighted, the market is dominated by these wallets (insider label 69% of $ volume, 65% of it sells).

## 8. Practical implications for a trader (no look-ahead claims)

1. Volume and "trade count" are poor proxies for demand. 15-50% of dollar volume is the same wallets going in and out within minutes; the biggest prints are cycles. A volume filter (e.g. 24h volume, volume spikes) should use net, wallet-deduplicated flow or at least exclude wallets with both sides within 5 min.
2. Price impact in the $5-15k pools is large and roughly mechanical: ~1.6-2.0% price per 1% of liquidity net bought (order-of-magnitude, noisy). A $200 buy in a $10k pool (2% of liquidity) moves the price ~4%, and you pay it again on exit. Sizing should be a fraction of liquidity (<0.5-1%), consistent with notes 13/14 on position vs liquidity.
3. Impact is not alpha: next-15m return on bar imbalance has beta 0.01-0.02 (R2 < 0.2%) and returns mean-revert (ACF -0.04 to -0.06, up to -0.16 in some buckets). Chasing a bar with strong buying is not supported; if anything, fading extremes after the move is closer to what the data says, but I have not backtested a fade net of costs, and these are in-sample unconditional statistics on survivors.
4. A pre-entry check that is look-ahead-free (features from trades with ts <= first capture, entry at the OPEN of the first candle at/after capture, median 513 s later, exit at the last close within 1 h; 10,985 tokens, `of20_predict2.py`): the mean 1 h log return is -37% (median -17.7%, 26.7% positive). USD buy imbalance in the log before capture is **negatively** rank-correlated with that forward return: Spearman -0.20 (p ~ 1e-98); imb in the last 5 min -0.18; count-based imbalance -0.07; launch-buy dominance -0.03. Quintiles of USD imbalance (lowest -> highest): mean return -1.9%, -32%, -43%, -53%, -54%; share positive 39%, 20%, 22%, 24%, 26%. Reading: heavily one-sided buying at detection is the hype/pump leg that is already priced in, and the exits (sell side, large) come right after; the least one-sided tokens lost almost nothing. Caveats: survivors with candles only; the 513 s entry delay is the dataset's, not something I optimised; the sample is one 20-day regime; no fees/slippage applied (they only make it worse). This is an association for risk screening (avoid chasing max-imbalance tokens), not a proven edge.
5. Expect clusters: after one trade, the next is the same side with 86% (buys) probability and large trades follow large trades. A 1-3 s reaction window sees most of a burst; copy-trading a wallet's buy lands inside the burst, in a pool you move yourself.
6. Whale/insider concentration: ~38% of tokens carry one dominant launch buy and insider-labelled wallets are 69% of volume with ~65% of it sells. The dominant buyer is effectively the main exit counterparty; any holder-concentration or "dev/bundle" filter (note 07) should be checked on this flow, because logged flow is mostly theirs.
7. Fat tails: top 1% of trades = 52% of volume; Pareto alpha 1.7-2.5 body, thinner far tail. Use medians/quantiles or log-sizes, never means, and expect single prints to dominate token-level indicators.

## 9. Limits and what I did not do
- Log is a truncated sample (~200 trades) of the first minutes of life; ages > 1 h are a minority (3.5% of trades). Everything about "mid-life" order flow rests on 15 m candles with 28% flow coverage.
- Impact regressions use a stale static liquidity and partial flow: coefficients are attenuated and the bucket results for >= $40k pools are low power (830 bars).
- No fee/MEV/Jito modelling; no on-chain linkage to confirm wash; wallet labels cover 1.6% of wallets. 20 days of a single regime.
- I did not run an age-controlled sign ACF or any strategy net of costs; items 3-4 in section 8 are hypotheses to test with note-style walk-forward before use.
