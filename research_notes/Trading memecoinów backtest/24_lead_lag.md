# 24. Lead-lag: does volume or buy pressure lead price? Momentum vs mean reversion at 15m-4h

Scripts: `backtest/ll_build.py`, `ll_grid.py`, `ll_lib.py`, `ll_run1..7.py` (outputs in `backtest/out/ll_part*.txt`). Data: ian05012/solana-memecoin-dataset (GMGN, 2026-06-10..06-30), 15m candles + trade log. No web searches.

## 1. Data and method (caveats first)
- ohlcv.parquet: 272k rows, but **~35% are duplicated rows (some with conflicting values)**. Dedup'd exact duplicates, dropped keys with conflicting values, dropped glitch candles (high>10x close) -> 178,676 candles, 11,022 tokens. Forward-filled gaps inside each token's span (flat bar, vol 0) -> 284k grid bars, 63% "active" (real trades).
- **Candles only cover a window after detection by the collector** (README: "within each label window"). Median span 14 bars (3.5h), p90 66 bars. So "series ends" is mostly window truncation, not death, and everything is conditioned on the token having been detected as trending/graduated. Not a random sample of memecoins. Only 26% of bars are >=24 bars old.
- Trades (9.5M) join to 30.5k candle-buckets (17% of candles); trade-log value is ~28-45% of candle volume (median) -> the buy share is a **partial, wallet-sample-based** measure, not full-market flow.
- Returns: signal on bar t, entry at close_t (open_{t+1} differs by median 0.0%, mean 0.03%), exit close of t+k (k=1,4,16 = 15m, 1h, 4h). `l` horizon = exit at last observed close if the series ends early (primary); `f` = strict (next bars must exist) - results nearly identical. Forward returns winsorised at +1000%. Cost: flat 2.5% round-trip subtracted. Stats: token-cluster bootstrap (1,500 reps), 95% CI and t = mean/bootstrap-SE. OOS: PRE < 2026-06-24 <= TEST (26% of bars, ~6 days).
- Signal bars require volume >= $1k (and age >= 2 bars) unless said otherwise. Rule count examined ~70 x 3 horizons -> need |t|>~3.3 to survive Bonferroni.

## 2. Baseline: memecoins drift down, hard
Mean return of any active bar (vol>=1k): 15m -0.27%, 1h -2.6% (median -7.0%), 4h -7.3% (median -18%). Net of 2.5%: -2.8% / -5.1% / -9.8%, all CIs < 0. Any long rule must beat this drift; for "buy X" rules the right comparison is net > 0 absolute.

## 3. Autocorrelation by lag (winsorised 1/99 c2c returns, age>=2, token-cluster CI)
| lag (x15m) | rho active-only | 95% CI | PRE | TEST |
|---|---|---|---|---|
| 1 | -0.0333 | [-0.044,-0.024] | -0.0350 | -0.0296 |
| 2 | -0.0040 | [-0.012,0.004] | | |
| 3 | -0.0114 | [-0.020,-0.004] | | |
| 4 | -0.0146 | [-0.022,-0.007] | -0.0129 | -0.0121 |
| 6 | -0.0083 | [-0.016,-0.001] | | |
| 8 / 12 / 16 | +0.001 / +0.001 / +0.001 | all CIs include 0 | | |

Spearman lag1 -0.022 [-0.029,-0.015]. Slight negative first-order autocorrelation (bid-ask-bounce / small mean reversion), stable in both periods, zero beyond 2h. By age: lag-1 rho is -0.02 (age 2-4, n.s.), -0.01 (4-8, n.s.), -0.044 / -0.053 / -0.058 for age 8-16 / 16-48 / 48+ (all significant). Economically tiny (rho^2 ~0.1% of variance). Next-bar mean after a >+5% bar: +0.8% (median -3.4%, P(up) 43.6%); after <-5%: +2.8% (median -1.0%, P(up) 48%).

## 4. Conditional next returns after big candles (vol>=1k)
Return profile by candle size (net of 2.5% cost; gross in brackets), CI lower bound shown for net:
| prior candle | 15m gross / net [CI] | 1h gross / net | 4h gross / net |
|---|---|---|---|
| <= -50% | +0.6 / -1.9 [-4.0,0.3] | -6.9 / -9.4 | -16.6 / -19.1 |
| -50..-30% | +0.6 / -1.9 [-3.0,-0.8] | -3.4 / -5.9 | -9.6 / -12.1 |
| -30..-15% | +0.4 / -2.1 | -1.4 / -3.9 | -4.5 / -7.0 |
| -5..+5% (ref) | -0.3 / -2.8 | -1.2 / -3.7 | -5.4 / -7.9 |
| +15..+30% | -1.8 / -4.3 | -4.4 / -6.9 | -9.6 / -12.1 |
| +30..+50% | -1.4 / -3.9 | -5.4 / -7.9 | -12.0 / -14.5 |
| +50..+100% | -1.6 / -4.1 | -7.3 / -9.8 | -14.9 / -17.4 |
| >= +100% | -1.2 / -3.7 | -7.0 / -9.5 | -12.2 / -14.7 |

Headline rules (ALL / PRE / TEST), net of cost:
| rule | 15m | 1h | 4h |
|---|---|---|---|
| UP >= +50% (n=2,761, 1,643 tokens) | -4.0 [-5.5,-2.5] / -4.2 / -3.8 | -9.8 [-12.5,-6.9] / -11.0 / -7.2 | -16.7 [-21.4,-11.5] / -17.9 / -14.1 |
| DN <= -30% (n=4,727, 2,666 tokens) | -1.9 [-2.9,-0.8] / -2.5 / -0.5 | -6.9 [-8.9,-4.7] / -8.0 / -4.3 | -14.1 [-17.5,-10.7] / -14.6 / -12.8 |

Gross after DN30 at 15m is +0.6% (t 1.1; TEST +2.0%, t 2.2) -> a small bounce, far below the 2.5% cost. Age-matched excess vs baseline: DN30 +1.24% at 15m (CI [0.24,2.30], t 2.3), ~0 at 1h/4h; UP50 -1.0% (15m, n.s.), -3.7% at 1h (CI [-6.6,-0.9]), -4.9% at 4h. Conclusion: **pumped candles are followed by continued decay (reversal) and dumped candles by only a 15m bounce; no momentum**. Same sign in every age bucket (strongest reversal for age 2-4: UP50 4h gross -10.9%, median -26.8%). Win rate after cost is 28-30% for UP50 and 31-38% for DN30.
Hypothetical short of UP50 (no borrow/funding, not generally possible on pump.fun tokens): net -1.0% (15m), **+4.8% [1.9,7.6] (1h)**, **+11.7% [6.7,16.8] (4h)**; UP30: +3.8% / +10.5%. Same-sign in PRE and TEST, but not executable on spot memecoins -> an "avoid chasing" rule, not a trade.

## 5. Volume spikes (vol / mean of prior 8 bars, age>=8, vol>=1k)
- Volume does not lead price direction: cross-correlation of dlog(vol)_t with return_{t+k}: k=+1 -0.007 [-0.015,0.000], k=+2..+4 ~ -0.005..-0.001 (all n.s.); contemporaneous +0.111. Weak "return leads volume" (k=-2..-4: -0.01..-0.02, negative, significant but tiny).
- Volume leads/concurs with volatility, not sign: corr(dlogvol_t, |ret|_t)=+0.26, but k=+1 is 0.006; |ret| at t+1 is *negatively* tied to volume at t only through the t-1 spike term (-0.33 at k=-1 is mechanical: the spike bar's prior bar is quiet).
- Spike (>=5x) on an up bar: net -2.8% (15m), -6.9% (1h), -7.8% (4h); on a down bar: -2.7%, -2.0%, -2.7% (CIs include 0 at 1h/4h). Down bar with vratio 3-10: gross +2.0% at 15m (t 2.7) but net -0.5% [-1.9,+0.9]. Nothing beats cost. TEST: up&spike net -2.7/-7.8/-6.9, same sign.
- Regression (all vol>=1k bars) l1 ~ rbar + dlogvol + logvol: rbar -0.032 (t -5.0) = reversal; dlogvol t 1.2, logvol t -0.3.

## 6. Buy share (the one real signal)
Sample: bars with trade-log volume >= $1k and >= 10 trades: 6,234 bars, 1,808 tokens (12% of vol>=1k bars). Mean bs 0.57. Contemporaneous corr(imbalance, return) = 0.28; imbalance_t vs return_{t+1} 0.069 [0.04,0.09]; t+2 0.021 (n.s.). Regression l1 ~ rbar + imb + dlogvol: imb +0.074 (t 6.7), rbar -0.004 (t -0.4); l4: imb +0.10 (t 4.7).

Buy-share buckets (net of 2.5%):
| bs bucket | n | 15m net [CI] | 1h net [CI] | 4h net |
|---|---|---|---|---|
| <0.3 | 726 | -3.2 [-5.3,-1.0] | -9.1 | -22.1 |
| 0.3-0.5 | 1,364 | -4.2 | -8.2 | -14.4 |
| 0.5-0.7 | 2,386 | -2.3 | -7.5 | -16.7 |
| 0.7-0.9 | 1,375 | +1.9 [-0.2,+4.2] | -2.4 | -12.0 |
| >=0.9 | 383 (304 tokens) | **+17.0 [+9.7,+25.7]**, t 4.1 | **+26.7 [+13.8,+41.1]**, t 3.9 | +12.5 [-3.5,+30.0] |
| >=0.8 | 925 | +9.5 [5.9,13.8], t 4.8 | +11.7 [4.1,19.7] | |

Out of sample (bs>=0.9): PRE 15m net +12.1% (t 4.3), TEST +25.8% [8.6,48.0] (t 2.6); 1h PRE +16.9% (t 2.1), TEST +44.7% [22.1,70.1] (t 3.5). Train-quintile top bucket (>=0.76): TEST 15m +10.0% [3.5,18.1], 1h +9.3% [-2.4,20.9]. Positive in 17 of 21 calendar days.

Robustness / weaknesses of this signal:
- Heavy right tail: median 15m gross is only +2.6% (1h median -1.75%); win rate after cost 50% (15m) / 46% (1h). Winsorising at +100%: 15m net +10.3% [6.4,14.4], 1h net +5.6% [-0.5,12.1]; at +50%: 1h net -5.1% [-9.7,-0.3]. Dropping the top 10 events: 15m +8.6% (t 4.3), 1h +11.9% (t 2.8); top 20: 15m +5.5% (t 3.0), 1h +5.0% (n.s.). So the 15m effect is robust, the 1h effect hinges on a few moonshots.
- First event per token only: 15m +18.6% (t 3.7), 1h +28.3% (t 3.7). Not clustering of repeats. Shuffling bs within token (300 placebo draws): net 15m mean +4.2% (97.5th pct +8.4%) vs actual +17.0% -> the effect is not an artifact of the sample.
- Higher trade-log coverage (tv/volume >= 0.3) is stronger (+27.6% / +40.9%) than low coverage (+7.1% / +13.6%).
- Entry-assumption sensitivity: entering at open_{t+1} changes nothing (gap ~0). **But one bar of latency kills it**: entering at close_{t+1}: 15m net +3.3% [-1.0,7.6], 1h +6.4% [-1.8,16.0] (bs>=0.8: +0.5%, -0.7%). At 5% cost the unlagged 15m net is +14.5% (t 3.6), at 7.5% +12.0% (t 2.9) - the edge is the immediate next candle, i.e. it decays within 15-30 minutes.
- Possible bias I could not rule out: (a) the signal bar itself has contemporaneous return mean +53%, so entering a token that just pumped hard needs tradeable liquidity at 2.5% cost - unrealistic for the large-move cases; (b) the trade log is a wallet sample of unknown selection (hi bars are from ~13 distinct buyers, top wallet 26% of volume, mixed insider/smart_money/normal tags) - if the log was backfilled with ex-post knowledge, buy share could embed future info. Timestamps of all candles/trades are after the detection time, and the signal uses only bar t, so there is no formal look-ahead in the construction, but the collection process is unverified; (c) n=383 events, 11 days of clustering.
- Verdict: the only rule with positive net edge; treat as hypothesis requiring a live/forward test with real fill data.

## 7. Breakout after consolidation (prior 8 closes range <=25%, vol>=1k, age>=8)
| rule | n | 15m net | 1h net | 4h net |
|---|---|---|---|---|
| consolidation, no breakout | 1,128 | -2.6 | -3.6 | -5.7 |
| breakout >=+10% over 8-bar high | 975 | -4.3 [-5.8,-2.7] | -8.0 | -12.6 |
| breakout >=+10% & vol>=3x | 482 | -4.0 | -7.0 [-11.6,-0.8] | -9.8 |
| breakout >=+25% | 580 | -4.6 | -9.7 | -16.0 |
| new 8-bar high (non-consolidated) >=10%, vol>=3x | 1,191 | -2.5 | -7.7 | -8.1 |
| breakdown (<= prior min -10%) | 525 | -1.0 [-2.4,+0.4] | +0.5 [-2.5,+3.7] | -0.9 |
Breakouts fail; TEST has the same sign (e.g. brk>=25% TEST: -4.9/-7.0/-17.3). Breakdowns bounce about enough to cover cost at best (gross +1.5% / +3.0%, CIs include 0 after cost).

## 8. Which simple rules survive costs?
| rule | survives 2.5% cost? |
|---|---|
| Momentum after +50% / +100% candle (long) | No. Reverses: net -4% / -10% / -17% (15m/1h/4h) |
| Momentum after volume spike (up bar) | No. Net -2.8 / -6.9 / -7.8 |
| Breakout after consolidation (long) | No. Net -4 / -8 / -13 |
| Buy dip after -30% (reversal long) | No. 15m bounce +0.6% gross, net -1.9% (TEST -0.5%, CI incl. 0); 1h/4h strongly negative |
| Contrarian after volume spike on down bar | No (CIs include 0 but means negative) |
| Fade the pump (short after +50%) | Gross reversal is real and stable OOS (1h +4.8%, 4h +11.7% net), but shorting is not available; mostly says "do not chase" |
| Autocorrelation (lag-1 rho -0.03) | Statistically significant but economically negligible |
| Buy share >=0.9 in the last 15m bar, buy next 15m (and optionally hold 1h) | **Yes on paper**: net +17% (15m, CI [9.7,25.7], t 4.1, TEST +26%), robust to dropping top 10 and to 7.5% cost, but only with zero execution latency, a partial wallet-sample signal, n=383, and a tail-driven 1h leg |

## 9. Answer to the question
- Volume does not lead price direction at 15m-4h (all lead cross-correlations ~0); volume is contemporaneous with and a weak proxy for volatility.
- Buy pressure (signed trade-log imbalance) shows a short-lived lead: effect only in the extreme top bucket (>=0.8-0.9), concentrated in the next 15m, gone with one bar of delay.
- Price: slight lag-1 mean reversion (rho -0.03), and after large pumps clear multi-hour reversal (consistent with a strong negative baseline drift of -7% per 4h); no momentum at any horizon. After large dumps only a 15m bounce, smaller than cost.
- No pure price/volume momentum or reversal long rule survives a 2.5% round-trip. The only surviving candidate uses trade flow and needs live validation.

## 10. Limitations
Detection-conditioned windows, partial trade log, duplicates/conflicts in raw candles (dropped), 20-day regime, OOS only 6 days (n small for tails), many comparisons, no slippage model beyond flat cost, winsorising at +1000%, forward-fill of empty bars.
