# 02 - Leak-free features from raw trades, out-of-sample test

Scripts (backtest/): `cov.py` (coverage), `tf_extract.py` (pre-capture trades), `tf_features.py` (features), `tf_model.py` (LightGBM + net returns). Run with `python3 -I`.
Split as in filters.py: train = first snapshot before 2026-06-24 UTC (n=7589), test = on/after (n=2095). Universe = tokens in sim_results.parquet (peak_mult<1000), one decision per token (first snapshot).

## 1. Coverage (do trades exist before capture?)
| Item | Result |
|---|---|
| Trades file | 9.50M rows (6.72M buys / 2.78M sells), 66,990 tokens, 734k wallets |
| Tokens with first snapshot | 31,013; 31,004 have >=1 trade with ts < capture |
| Trades pre / post capture (these tokens) | 3.99M / 1.53M |
| Sim-results tokens with pre-capture trade features | 9,683 of 9,684 (99.99%); 99.6% have >=10 buys |
| Median pre-capture buys per token | 98 (median last trade 8 s before capture; median first trade ~400 s before) |
| wallet_funding | only 15,493 rows; a funder is known (ts < capture) for ~7% of buyers (median) - weak signal by construction |

Caveats: per-token trade count is capped around ~300 (max buys 307), i.e. the log is truncated/sampled, so unique-buyer and USD totals saturate; the README says it is a "wallet x token" log "for graph construction", sampling rule unknown. Some tokens have trades up to 2 years before the snapshot (f_age_s mean is dominated by these).

## 2. Features (all strictly ts < capture)
buy/sell USD, counts, unique buyers/sellers, net USD, buy share, sellers per buyer; top-1/top-5 buyer share (USD); share of buyers with a funder, share sharing a funder with another buyer, top-funder share (funding ts < capture, first known funder); crew features (share of buyers who bought >=1 / >=3 earlier tokens, mean/max prior-token count; history only from tokens with cap_j < cap_i, tie-groups handled, outcomes never used); buy-size uniformity (log-size CV, modal-size share, median/mean size); acceleration (buy USD last 60 s/300 s, log ratio vs earlier rate, buys last 60 s, rate/min). 31 features total.
Observed: crew_rep1_frac median 0.93 (almost every buyer bought earlier tokens - bots/dominant wallet set), same_funder_frac median 0 (funding data too sparse).

## 3. Univariate AUC vs peak>=2x (top by |AUC-0.5| on train)
| Feature | AUC train | AUC test |
|---|---|---|
| f_buy_size_mean | 0.638 | 0.620 |
| f_buy_usd | 0.637 | 0.625 |
| f_net_usd | 0.632 | 0.620 |
| f_buy_usd_last300 | 0.590 | 0.594 |
| f_sellers_per_buyer | 0.415 | 0.430 |
| f_n_sells | 0.427 | 0.428 |
Signs are stable train->test, but the effect is "more USD traded = bigger token", i.e. mostly size/popularity, not crew/funder structure (those features ranked low).

## 4. LightGBM, net returns on TEST ($200 position, fee 1.25%/side, tip $0.30/tx)
Target = net return > 0 under the same cost variant; 3-seed average; 200 trees, 15 leaves. Bootstrap CI95 of the mean (2000 resamples). "liq" = impact 2*pos/liquidity_usd; "fix15k" = impact from fixed $15k liquidity (2.67%/side).
Trade-feature model (the object of this task):
| Impact | Strategy | Test AUC (net>0) | Unfiltered mean [CI95] | top5% mean [CI95] | top10% mean [CI95] | top20% mean [CI95] |
|---|---|---|---|---|---|---|
| liq | ladder_B | 0.682 | -0.221 [-0.244,-0.196] | +0.153 [+0.015,+0.295] | +0.047 [-0.045,+0.148] | -0.019 [-0.086,+0.048] |
| liq | tight_D | 0.708 | -0.187 [-0.204,-0.169] | +0.062 [-0.040,+0.172] | +0.017 [-0.049,+0.090] | -0.022 [-0.068,+0.026] |
| liq | hold_24h | 0.702 | -0.342 [-0.392,-0.285] | -0.094 [-0.282,+0.112] | +0.088 [-0.184,+0.413] | -0.079 [-0.245,+0.107] |
| fix15k | ladder_B | 0.685 | -0.179 [-0.204,-0.154] | +0.109 [-0.014,+0.231] | +0.040 [-0.046,+0.130] | -0.019 [-0.085,+0.045] |
| fix15k | tight_D | 0.669 | -0.143 [-0.161,-0.126] | +0.078 [-0.017,+0.181] | -0.002 [-0.065,+0.064] | -0.053 [-0.096,-0.006] |
| fix15k | hold_24h | 0.693 | -0.306 [-0.356,-0.249] | +0.445 [-0.004,+1.047] | +0.019 [-0.213,+0.315] | -0.032 [-0.195,+0.171] |
Sanity: shuffled-train-label models give AUC 0.48-0.52 and selected means of -0.10 to -0.36 (about the unfiltered level), so the pipeline itself is not generating spurious gains.

Win rates in the selections are 24-49% (ladder_B top5%: 48%), medians are <=0 in nearly all cells.

## 5. Snapshot columns: do NOT trust (leak signature)
Same pipeline with the existing tokens.parquet snapshot features gives test AUC 0.93-0.998 and top-k means of +40% to +145% with win rates 80-100% (ladder_B top5% +1.21 / +1.00 under liq / fix15k; CI lower bound > +0.8). A 100% win rate after 1.25%/side fees plus impact on memeoin entries is not credible; this is a look-ahead signature in some snapshot columns (candidates: columns computed over windows including post-capture data, or rug/label-derived fields such as rug_probability, buy_late/sell_late, buy_total, the *_1h fields). I did not isolate the column. Adding trade features to snapshot features changes nothing (trade+snapshot ~ snapshot). This contradicts nothing in the leak-free trade result; it just means snapshot-based results from filters.py should be re-audited before anyone uses them.

## 6. Honest conclusions
- Leak-free trade-only features carry weak signal (AUC ~0.67-0.71 for net>0, mostly size/volume proxies). Unfiltered strategies lose 14-34% per trade, consistent with stage 1.
- Only ladder_B top-5% under the actual-liquidity cost shows a CI95 above 0 (+15%, CI +1.5% to +29.5%, n=105). With fixed $15k impact it is +11% with CI crossing 0 (-1.4%). Across 6 strategy/impact cells x 3 cut-offs (18 tests) one marginal hit is what chance gives; top10/20% are ~0 or negative. I would not call this a tradable edge.
- Execution realism not modelled: top-5% tokens tend to be larger, so entry delay (up to 15 min to the next candle) and slippage under volatility are likely worse than assumed; n=105 in a single 6-day regime; 5 days of test.
- Not tested: tuning of hyperparameters, other position sizes, rolling-window retraining.
- Crew and same-funder features add little: funding coverage ~7%, crew features saturated (most buyers are repeat wallets). Their importance in the model is low (top gain features: buy_size_mean, sell_usd, funded_buyers_frac, net_usd).
