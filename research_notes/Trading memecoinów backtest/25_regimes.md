# 25 - Market regimes in memecoins: persistence and regime filters

Date: 2026-11-21. Scripts: /home/user/Detour/backtest/regimes.py, regimes_lib.py (run with `python3 -I`). Raw outputs: backtest/out/regimes_{persist,cross,hmm,oos}.txt/json. No web searches. Datasets are untrusted third-party data.

## Bottom line

1. Regimes exist as slow drifts in the hit-rate, but they are not tradable for the memecoin sniper strategies. Daily share reaching 2x is over-dispersed versus pure binomial noise in all three datasets (variance ratio 1.7x tokens, 4.6x launches, 1.7x calls, all p<0.03) and is autocorrelated: lag-1 r = 0.56 (tokens, 18 days), 0.66 (launches, 60 d), 0.15 (calls, 143 d; permutation p=0.057). A 2-state binomial HMM beats a 1-state model and an i.i.d. 2-component mixture (so the persistence is real) in every dataset (parametric bootstrap, 30 sims, p<=0.03 on p2).
2. The June 2026 token sim (the only dataset with a real exit simulation) has NO profitable regime: strategy net EV per day is negative on every one of 18 full days (ladder_B between -0.29 and -0.13 per trade, best day still -13%). Regime filters can only reduce losses, not create profit. OOS (12 test days) no rule beat random day-skipping robustly (best p=0.013 for pnl_prev3d, still -16% per trade, and 12 days with 6 rules tried: not significant after multiple-testing correction).
3. Launches (Jul-Sep): a "trade only if yesterday's 2x-rate was above its expanding median" filter improves a proxy EV from -12.3% to -7.4% per trade OOS (52 test days, bootstrap CI -9.4..-5.7%, p vs random <0.001), but it stays negative. Calls (Jun-Nov): the same family lifts a proxy EV from +2.4% to +8.0% (3 consecutive good days, 28 of 136 days, CI +3.6..+12.3%, p<0.001), at the cost of 40% fewer dollars per calendar day if capital is not binding.
4. Trade count alone (launch count / call count) is highly persistent (r1 0.45-0.85) but has zero predictive value for quality (count_prev1d rule: lift +0.1pp launches, +0.3pp calls, p 0.33-0.36).
5. Practical: use regime as a throttle (size / cap on number of entries), not an on/off edge generator. See "Bot throttling".

## Data and construction

| Dataset | Period used | Unit | Days | Trades/day | Outcome |
|---|---|---|---|---|---|
| tokens + sim_results.parquet (GMGN snapshots, 15m path sim) | 11-28 Jun 2026 (edge days dropped: 10 Jun starts 08:36, 29 Jun ends 20:01) | token at first detection | 18 | ~510 | peak_mult, real simulated net return of ladder_B/tight_D/runner_F (200 USD stake, fees+impact+tips as in backtest.py) |
| pump.fun launches (28k rows) | 28 Jul - 25 Sep 2026 (27 Jul partial dropped) | launch surviving to 15 min | 60 | ~470 | `multiple` = best price in 5h / price at 15 min (>=1 by construction) |
| calls (13k) | 1 Jul - 20 Nov 2026 (30 Jun had 14 calls, all hits: dropped; 20 Nov partial, n=11, kept in count) | Telegram call | 143 | ~91 | `peak` multiple after call |

- "Qualifying launch" = a row in the dataset (already survived 15 min / has trade data). Counts are what the collector saw, NOT the chain total: the daily count mixes true launch activity with scraper coverage. Treat as an activity proxy only.
- Net EV for launches/calls has no path data, so a proxy is used: payoff per trade = 0.975*(2 if peak>=2x else 1-L) - 1 with L=50% (also 70%); break-even 2x-rate = 35.0% (L=50%) or 42.7% (L=70%). Because the payoff is a deterministic function of the 2x-rate, "EV" and p2 series are the same information. The proxy is optimistic (assumes a fill at the reference price and a 2x limit sell that always fills).
- The three datasets barely overlap in time: tokens (June) share only 14 calls with calls (30 Jun). Launches and calls overlap 28 Jul - 25 Sep (60 days) and are compared there; tokens cannot be joined to either. Net: three separate regime tests plus one cross-check, not one unified series.
- Mean level reference (daily): tokens p2 21.8% (sd 2.7pp), p5 5.4%, median peak 1.21x; launches p2 27.4% (sd 4.4pp), p5 5.2%, median 1.44x; calls p2 37.5% (sd 9.5pp incl. 30 Jun outlier; ~6pp without), p5 11.4%, median 1.60x.

## Series (daily, abbreviated; full table in out/ and regimes.py series)

Tokens (net per trade at 200 USD, winsorised 99%): p2 rises from 0.16-0.20 (11-14 Jun) to 0.23-0.26 (22-28 Jun); net ladder_B in [-0.29,-0.13], tight_D in [-0.23,-0.13], runner_F in [-0.29,-0.13]; weekly chunks: p2 19.3% / 22.9% / 24.1%, ladder_B net -20.1% / -18.4% / -22.9% (higher hit-rate did NOT give better net EV: 2x-rate and strategy EV are only loosely tied, costs and liquidity dominate).

Launches weekly (start, n, p2, p5, median multiple, proxy EV L=50%):

| Week | n | p2 | p5 | med | EV |
|---|---|---|---|---|---|
| 28 Jul | 2054 | 31.9% | 6.2% | 1.57 | -4.9% |
| 3 Aug | 2550 | 28.9% | 5.6% | 1.44 | -8.8% |
| 10 Aug | 2846 | 29.2% | 5.8% | 1.50 | -8.5% |
| 17 Aug | 3348 | 29.2% | 5.5% | 1.49 | -8.6% |
| 24 Aug | 3795 | 28.8% | 5.7% | 1.50 | -9.1% |
| 31 Aug | 3496 | 20.2% | 2.4% | 1.35 | -21.9% |
| 7 Sep | 4039 | 25.0% | 4.4% | 1.38 | -14.8% |
| 14 Sep | 3621 | 23.6% | 4.3% | 1.36 | -16.7% |
| 21 Sep | 2578 | 31.1% | 7.3% | 1.43 | -5.7% |

Clear cold phase 31 Aug - 20 Sep (trough 4 Sep: p2 13.8%, 5 Sep 16.8%, 6 Sep 18.8%) and recovery 21 Sep; no week reaches break-even (35%) even in the best weeks (daily max 37.3%, 31 Jul).

Calls weekly: p2 between 31% and 45%, stable ~35-37% from July to mid-Oct, cold dip 20-26 Oct (30.9%), then a clear hot phase 3 Nov onward: p2 41% / 43% / 45% / 45%, median peak 1.87-1.93x, proxy EV +7% to +18%/trade (daily p2 up to 52% on 12 Nov). Note this is an end-of-sample phase of only ~18 days; it may be genuine or a change in the caller population / data scraping.

## Persistence tests

Dispersion = Pearson chi2 of daily hit counts vs binomial with pooled p (H0: no day effect). Lag-1 r computed on Pearson residuals (removes the changing n). Permutation p (4000 shuffles). Bartlett 95% bound in last column.

| Series | T | var ratio p2 (p) | r1 p2 | perm p | r1 p5 | r1 log n (detrended) | r1 log median peak (detr.) | Bartlett |
|---|---|---|---|---|---|---|---|---|
| tokens daily | 18 | 1.78 (0.025) | 0.56 | 0.003 | -0.33 | -0.29 | 0.25 | 0.46 |
| launches daily | 60 | 4.62 (<0.001) | 0.66 | <0.001 | 0.47 | 0.63 | 0.42 | 0.25 |
| calls daily | 143 | 1.68 (<0.001) | 0.15 | 0.057 | 0.13 | 0.45 | 0.15 | 0.16 |
| tokens 4h blocks | 107 | 1.35 (0.010) | 0.24 | 0.011 | 0.18 | 0.37 | 0.04 | 0.19 |
| launches 4h blocks | 360 | 1.93 (<0.001) | 0.31 | <0.001 | 0.29 | 0.36 | 0.27 | 0.10 |
| calls 4h blocks | 849 | 1.09 (0.038) | 0.18 | <0.001 | 0.10 | 0.47 | 0.23 | 0.07 |

(4h-block residuals have the 4h-of-day mean removed. Low power for tokens: 18 days can only detect |r1| > ~0.47.)

- Good day predicts good next day, launches: P(next above median | today above median) = 72% vs 27% after a below-median day (Fisher p=0.001; 4h blocks 59% vs 41%, p=0.001). Calls daily: 54% vs 44% (p=0.31, n.s.); calls 4h blocks 55% vs 45% (p=0.003). Tokens daily 75% vs 33% (p=0.15, n.s., 17 pairs).
- Persistence is mostly slow-moving level, not mean-reverting noise: r2 and r3 stay high for launches (0.55, 0.42) i.e. phases of 1-3 weeks. Calls decay quickly (r2 0.09) except in the late Nov phase.
- Count (activity) autocorrelation is stronger than quality autocorrelation in every dataset (raw log n r1 0.85 launches, 0.46 calls). Launches log n has a upward trend through Aug (330 -> 590/day), which is the collector, not necessarily the market.
- Tokens net return per trade: days differ more than sampling noise (one-way ANOVA across days: ladder_B p=0.005, tight_D p=0.003, runner_F p=0.005; Kruskal p<0.01; between-day sd of mean 3.5pp vs 2.6pp expected from within-day noise, so ~2.3pp of true day-to-day sd). Lag-1 r of daily mean net: 0.30 (ladder_B), 0.39 (runner_F) (n.s., p 0.09-0.19); 4h blocks 0.20-0.23 (p 0.02-0.04). A day-effect exists but is of size +-2-3pp around a mean of -18%.
- Seasonality (UTC 4h blocks and weekday) is weak or irrelevant for p2: tokens p=0.05 / 0.42; launches p=0.04 / 0.003 (Sunday worst 24.8%, Tue best 28.4%); calls p<0.001 by 4h (00-12 UTC 39% vs 12-24 UTC 34-36%) and weekday n.s.

### Cross-dataset (launches vs calls, 60 overlapping days, Spearman)

| Statistic | same day | launches(t) -> calls(t+1) | calls(t) -> launches(t+1) |
|---|---|---|---|
| p2 | +0.21 (p=0.11) | +0.23 (0.08) | +0.29 (0.03) |
| p5 | +0.12 (0.37) | +0.12 | +0.03 |
| log count (detrended) | +0.52 (<0.001) | +0.54 | +0.41 |
| log median peak (detrended) | +0.19 (0.15) | +0.30 (0.02) | +0.13 |

Activity moves together across datasets; quality co-moves only weakly (r~0.2). A composite z of both p2 series has lag-1 r 0.64 (same as launches alone 0.66): no gain from combining. No evidence of a lead-lag signal worth trading (the one p=0.03 is one of 8 looks).

## 2-state HMM (binomial emissions, daily hit counts, EM, weak Dirichlet prior on transitions)

| Series | T | low-state p | high-state p | stay (low/high) | exp. duration (days) | occupancy | LRT vs 1-state (boot p) | LRT vs i.i.d. mixture (boot p) |
|---|---|---|---|---|---|---|---|---|
| tokens p2 | 18 | 19.1% | 23.0% | 0.74 / 0.98 | 3.8 / 47.6 | 24/76% | 14.9 (<0.03) | 8.4 (0.033) |
| tokens p5 | 18 | 4.6% | 7.4% | 0.47 / 0.05 | 1.9 / 1.1 | 65/35% | 15.8 (<0.03) | 4.0 (0.10) |
| launches p2 | 60 | 22.2% | 29.4% | 0.87 / 0.94 | 7.4 / 17.1 | 29/71% | 142 (<0.03) | 30.9 (<0.03) |
| launches p5 | 60 | 3.7% | 6.0% | 0.93 / 0.96 | 13.4 / 23.7 | 35/65% | 65.8 (<0.03) | 16.6 (<0.03) |
| calls p2 | 143 | 35.3% | 45.3% | 0.99 / 0.92 | 72 / 11.8 | 85/15% | 45.6 (<0.03) | 16.7 (<0.03) |
| calls p5 | 143 | 8.8% | 12.4% | 0.78 / 0.89 | 4.5 / 9.0 | 33/67% | 8.8 (<0.03) | 5.7 (0.033) |

(Bootstrap: 30 parametric simulations, so the smallest reportable p is ~0.03; "<0.03" means 0 of 30.) Interpretation: launches have a cold state (p2 22%, ~7 days) and a normal state (29%, ~17 days); calls have a rare hot regime (45% 2x-rate, ~12 days, 15% occupancy, essentially the Nov phase) on top of a stable ~35% base. The tokens fit (T=18) is a trend, not a regime; token p5 states flip every 1-2 days (noise). Note the p-state differences are 4-10pp: regimes modulate the hit-rate modestly.

## Out-of-sample regime filters

Design: expanding window walk-forward; first 6-7 days warm-up; signal for day d uses only days <= d-lag (lag 1 = yesterday, lag 2 = strict, covers the 24h token hold); threshold = expanding median (top50) or 33rd percentile (skip_worst33) of the signal history; HMM refit daily on data up to d-lag, trade if filtered P(high state) >= 0.5. Metrics on test days: mean net per trade (trades pooled), cluster-bootstrap CI over selected days, p vs random = fraction of 10,000 random draws of the same number of days that do at least as well, pnl/day = sum of per-trade returns on 1 unit stakes per calendar test day. "p2_prev1d" and "pnl_prev1d" are identical for launches/calls (deterministic proxy).

### Launches (proxy EV, L=50%; 52-53 test days, 25.9k trades), lag 1 day

| Rule | days traded | mean/trade | lift | 95% CI | p vs random | pnl/day |
|---|---|---|---|---|---|---|
| Always | 53 (100%) | -12.3% | - | -14.0..-10.7 | - | -60.1 |
| yesterday p2 >= expanding median | 14 (26%) | -7.4% | +4.9pp | -9.4..-5.7 | <0.001 | -9.1 |
| skip worst third by yesterday p2 | 24 (45%) | -9.1% | +3.2pp | -10.8..-7.4 | 0.0003 | -19.8 |
| prev-3-day p2 >= median | 13 (25%) | -9.6% | +2.7pp | -11.3..-7.9 | 0.038 | -11.5 |
| 2 consecutive good days | 6 (11%) | -8.1% | +4.2pp | -11.0..-5.7 | 0.038 | -4.5 |
| 3 consecutive good days | 2 (4%) | -6.6% | +5.7pp | -7.6..-5.4 | 0.09 | -1.2 |
| HMM P(high)>=0.5 | 8 (15%) | -10.0% | +2.3pp | -13.5..-6.7 | 0.14 | -7.9 |
| count_prev1d >= median | 50 (94%) | -12.2% | +0.1pp | - | 0.33 | -56.7 |
| INVERSE (trade after bad days) | 39 | -13.9% | -1.7pp | - | 0.9997 | -51.0 |
| Oracle: same-day p2 >= median (not tradable) | 15 | -5.4% | +6.9pp | - | <0.001 | -7.1 |

Lag 2 (strict): top50 +2.9pp (p=0.033), 3 good days +6.9pp (1 day only), HMM +0.0pp, count 0. With L=70% all lifts are of the same size (+3..+6pp). Every filtered book is still negative EV: the filter captures 40-70% of what a perfect same-day oracle would, but the oracle itself is at -5%.

### Calls (proxy EV, L=50%; 135-136 test days, 12.3k trades), lag 1 day

| Rule | days traded | mean/trade | lift | 95% CI | p vs random | pnl/day |
|---|---|---|---|---|---|---|
| Always | 136 | +2.4% | - | +1.0..+4.0 | - | +2.19 |
| yesterday p2 >= median | 73 (54%) | +3.8% | +1.4pp | +1.6..+6.2 | 0.023 | +1.80 |
| skip worst third | 94 (69%) | +3.2% | +0.7pp | +1.1..+5.1 | 0.076 | +1.93 |
| prev-3-day p2 >= median | 74 (54%) | +3.0% | +0.6pp | +0.8..+5.2 | 0.20 | +1.48 |
| 2 consecutive good days | 45 (33%) | +5.3% | +2.9pp | +2.3..+8.4 | 0.004 | +1.47 |
| 3 consecutive good days | 28 (21%) | +8.0% | +5.6pp | +3.6..+12.3 | <0.001 | +1.33 |
| HMM P(high)>=0.5 | 3 (2%) | +14.0% | +11.6pp | +8.7..+28.5 | 0.015 | +0.16 |
| count_prev1d >= median | 67 (49%) | +2.7% | +0.3pp | - | 0.36 | +1.37 |
| INVERSE | 63 | +0.9% | -1.5pp | - | 0.97 | +0.40 |
| Oracle same-day | 74 | +8.8% | +6.4pp | - | <0.001 | +4.07 |

Lag 2: 3 good days +6.3pp (CI +4.8..+12.7%), top50 +0.9pp (p=0.12), count -0.5pp. With L=70% (baseline -9.9%) the 3-good-days book is -3.6% (CI -8.7..+1.2%): the filter lifts +6pp but cannot rescue a book whose loss on misses is 70%. HMM rule trades only 2-3 days (the filtered state is on only in the Nov phase) so its +12pp lift rests on ~157 trades in one phase: anecdote, not evidence.

Key point on opportunity cost: because the unfiltered calls book is already positive at L=50%, every filter reduces total P&L per calendar day (e.g. 3 good days: +1.33 vs +2.19 per day at 1 unit per trade). A filter pays only when capital, latency or attention is the binding constraint (then it raises return on capital), or in a negative-EV book where it reduces the loss (launches: -60 -> -9 to -20 per day).

### Tokens (real sim EV; 11-12 test days, 5.2k trades), lag 1 / lag 2

Baseline net per trade ladder_B -17.8%, tight_D -16.9%, runner_F -16.3% (CIs ~[-0.20,-0.15]). The p2-based rules trade all or all-but-one days (p2 trends upward in June so yesterday is always above the expanding median): no information, lift 0.0 to -1.1pp. The only differentiating signals: lagged trailing 3-day mean net return (lift +1.8pp ladder_B p=0.013, +1.9pp runner_F p=0.039 for skip_worst33) and count_prev1d (1 day, noise). None survives a multiple-testing correction (36 rule x strategy combinations, 12 test days). Verdict: no evidence a regime filter helps the sniper strategies in June; and even a perfect filter would leave EV at about -13% on the best day.

## Interpretation

- Regime = slow variation of the 2x/5x hit rate by about +-4-10pp around a base that is below break-even for tokens/launches and about break-even for calls. Launch counts and call counts behave like activity regimes (very persistent) but do not carry quality information.
- Hit rate 2x is more persistent than 5x (r1 0.66 vs 0.47 launches); the HMM on p5 is less persistent (tokens) or has short phases (calls 4.5 days). 5x runner hunting is not regime-predictable at these sample sizes.
- Persistence is best explained by multi-week phases (launches: cold 31 Aug - 20 Sep; calls: hot Nov). For a bot the exploitable signal is the trailing multi-day hit rate (3 consecutive good days), not same-day activity.
- Selection effects: filtering on yesterday's p2 picks days where the preceding phase was hot; the lift equals roughly 40-70% of the oracle lift, consistent with r1 ~0.6 for launches and much weaker (r1 0.15, lift only +1.4pp for a single day, +5.6pp only for 3 days) for calls.

## How a bot should throttle by regime

Compute from the bot's own closed trades or from a broad feed (not just taken trades) with outcomes older than the maximum hold (lag at least 24h for 24h-hold exits):
1. Regime signal R = trailing 3-day share of candidate tokens reaching >= 2x (from all candidates seen, not only entered ones), compared with its own trailing 14-30 day median (relative, not absolute, because level drifts: June tokens 16%->26%, launches 14%..37%).
2. State machine: HOT if R above median for 3 consecutive days; NORMAL otherwise; COLD if below the 33rd percentile of the trailing window (launches Sep 4-6 type troughs).
3. Throttle size/entry cap, not a binary switch: HOT 100% of normal size and normal max entries/day; NORMAL 50%; COLD 0-25% (probe size only, to keep measuring). Expected effect from the tests: +3 to +6pp per trade on the book, at 25-45% of days in the active state; improvement in drawdown is much larger than in mean.
4. Break-even guard overrides the regime: only the proxy break-even hit rate (35% for 2x at -50% misses) justifies running at all; in the June token sim no day was profitable, so a regime filter on that strategy must not be read as a reason to trade.
5. Do not throttle on raw launch/call count; it is persistent but uninformative (lift ~0, p 0.33-0.73). Use it only for capacity (rate limits, RPC budget).
6. Optional time-of-day tilt for calls (00-12 UTC hit-rate 39% vs 34-36%), weak and from one dataset.
7. Re-estimate every week; kill the filter if the walk-forward lift over random days goes below 0 for 3 weeks. Add a circuit breaker on realised net PnL (e.g. 3-day trailing mean net < -15%/trade).

## Caveats

- Short samples: 18 days (tokens), 60 days (launches, includes one 3-week cold episode that dominates the autocorrelation), 143 days (calls, one hot end-phase). Autocorrelation estimates have wide CIs; HMM bootstrap used 30 simulations only. Filter OOS tests are walk-forward but one path only; with ~10 rules per dataset the p-values should be Bonferroni-adjusted (x10): launches top50 and calls 3 good days remain below 0.01 after correction, everything else does not.
- Launches `multiple` is a best-price statistic over 5h with survivor selection (>=1 by construction); calls `peak` is selected by callers and has an unknown horizon; the 2x-limit payoff with a fixed 50% miss loss is an assumption. Both inflate absolute EV; the regime lifts are relative.
- Counts depend on scraper coverage; trend in launch counts (+80% in August) is probably partly collection.
- The earlier README finding (look-ahead in a liquidity>0.6*mcap rule) is unrelated here; the regime signals use only lagged aggregate outcomes.
- Tokens dataset ends 29 Jun, calls start 30 Jun, launches 27 Jul: regime state cannot be carried across datasets; the three series are separate evidence of the same phenomenon, not one long time series.
