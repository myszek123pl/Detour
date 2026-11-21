# 03 - Smart-money / wallet-following backtest (no look-ahead)

Code: `backtest/smart_money.py` (run: `python3 -I smart_money.py <data_dir> out`). Raw outputs: `backtest/out/smart_money_grid.csv`, `smart_money_latency.csv`, `smart_money_persistence.csv`, `smart_money_meta.json`, `smart_money_log.txt`.
Data: ian05012/solana-memecoin-dataset, GMGN, June 2026 (9.5M trades, 734k wallets; trades concentrated 2026-06-10..06-30). Only trades on tokens with OHLCV were used (2.38M trades).

## Verdict (short)
- Skill is estimated honestly from train (< 2026-06-24 UTC) and it does persist inside train (see 1b). But following those wallets in the test period does **not** make money: every combination (wallet set x k x exit) has a mean net return per trade of **-9% to -42%**, and the CI95 is below 0 in nearly all of them.
- Top-skill wallets are not distinguishable from a placebo (1000 random wallets with >= 5 closed tokens) or from "any >= k buyers" baseline. Differences are a few points, inside the CIs.
- The GMGN (leaky) tags look a few points better (best case +3 to +9 pp vs. our honest version, see section 4), but also remain negative, so the leakage is real yet not large enough to flip the sign.
- Delaying entry by 1-4 candles makes results *less* negative - for the baseline too. That is not a latency "decay", it is a survivorship/entry-after-dump artefact (section 3). No evidence of a copy-latency edge to lose.
- Conclusion consistent with stage 1 (README): in this dataset, with 1.25%/side fee + impact + tips, no entry signal tested so far produces positive expectancy.

## Method
1. **Skill (train only, trades with ts < 2026-06-24 00:00 UTC).** Per (wallet, token): buys USD B, sells USD S. A position is *closed* if S > 0; win = S > B; PnL = S - B. Wallet table: n = closed tokens, wins, total PnL, mean log(S/B) (clipped 0.01..100). Open positions (no sell in train) are **not** counted (counted separately as n_open; unknown outcome, so a winner-biased measure - accepted, train-only so no leak). Bayesian shrinkage: skill = (wins + 10*p0)/(n + 10), p0 = pooled win rate = 0.383. Eligible = n >= 5 closed tokens (21,051 wallets; 10,248 with n >= 10; 121,603 scored in total). Top-N by skill: N = 200 / 1000 / 3000.
2. **Signal (test, signal time >= 2026-06-24).** For each token, first buy time of each wallet in the set (any history); the k-th distinct wallet's first-buy time = signal time t (k = 1, 2, 3). Signals before the split are discarded. No future information used: k-th wallet is known at t.
3. **Entry.** Open of the first 15m candle strictly after t (`(t//900+1)*900`), + delay d candles. Skip if no candle within 15 min of the target (token has no candle / dead) or open <= 0.
4. **Exits/path rules** copied from `backtest.py`: SL checked before TP in the same candle, gap-through fills at open, glitch-high clipping, 24h horizon; strategies hold_24h, ladder_B, ladder_C, tight_D, scalp_E, runner_F.
5. **Costs** as in `filters.py`: eff = gross * (1 - 1.25% - impact)^2 - $0.30 * (1 + #sells)/pos - 1, pos = $200, impact = 2*pos/liquidity (cap 0.9). Two liquidity variants: **15k** (assumed, $15,000 -> impact 2.67% per side) and **col** (tokens.parquet `liquidity_usd`, NaN -> 15k). Note: the column is measured at token capture, possibly after the signal (mild look-ahead on cost only; it makes `col` slightly less reliable than `15k`).
6. **CI95:** percentile bootstrap, 2000 resamples of per-trade returns (trades iid - trades on the same day/market regime are correlated, so true CIs are somewhat wider).
Placebo: 1000 random eligible wallets. Baseline: signal = k-th distinct buyer of any kind (k = 3, 10).

## 1. Skill estimation sanity
### 1b. Persistence inside train (skill on days < 06-17, outcomes on 06-17..06-24, wallets with n >= 10 then n2 >= 3)
| group (by train skill) | wallets | next-week pooled win rate | share of wallets with PnL > 0 |
|---|---|---|---|
| top 1% | 58 | 0.707 | 0.948 |
| top 5% | 258 | 0.646 | 0.946 |
| top 20% | 1062 | 0.606 | 0.897 |
| bottom 80% | 3665 | 0.368 | 0.482 |

So wallet-level skill (measured as realised win rate on closed trades) persists out of sample. Caveat: wallets are conditioned on having sells, so win rate is biased upward for everyone; the useful part is the gap vs. the bottom 80%. It does not say that *copying* them works (they enter earlier/cheaper than a follower can, and exit via sells that the follower cannot see).

### Wallet sets
| set | size | notes |
|---|---|---|
| ours_top200 / 1000 / 3000 | 200 / 1000 / 3000 | shrunk win rate, train only |
| gmgn_smart_money (LEAKY) | 1600 | `wallet_type == smart_money` |
| gmgn_winrate_top1600 / top200 (LEAKY) | 1600 / 200 | top by GMGN `win_rate` (whole-period) |
| placebo_random1000 | 1000 | random eligible |

Overlap with GMGN smart_money: ours_top1000 has 95 wallets in common, ours_top3000 has 302. Our selection is largely different from GMGN's.

## 2. Test-period results ($200, 15k liquidity, mean net return per trade with CI95)
n = tradable signals (signals: tokens with signal >= 2026-06-24 / having an entry candle).

### ladder_B (SL 50%, TP 2x 50% + 5x 25%, trail 50% after 2x, 24h)
| set | k | n | mean | CI95 | median | win % |
|---|---|---|---|---|---|---|
| ours_top200 | 1 | 411 | -0.219 | [-0.268, -0.160] | -0.400 | 13.6 |
| ours_top200 | 2 | 148 | -0.279 | [-0.342, -0.197] | -0.391 | 8.8 |
| ours_top200 | 3 | 58 | -0.315 | [-0.391, -0.233] | -0.408 | 8.6 |
| ours_top1000 | 1 | 748 | -0.218 | [-0.255, -0.178] | -0.446 | 17.1 |
| ours_top1000 | 2 | 508 | -0.183 | [-0.229, -0.135] | -0.387 | 17.3 |
| ours_top1000 | 3 | 344 | -0.195 | [-0.248, -0.136] | -0.360 | 14.5 |
| ours_top3000 | 1 | 1079 | -0.205 | [-0.237, -0.171] | -0.541 | 20.2 |
| ours_top3000 | 2 | 1076 | -0.213 | [-0.243, -0.181] | -0.508 | 20.0 |
| ours_top3000 | 3 | 973 | -0.221 | [-0.253, -0.185] | -0.500 | 18.9 |
| placebo_random1000 | 2 | 992 | -0.202 | [-0.237, -0.166] | -0.541 | 22.1 |
| baseline any buyers | 3 | 1138 | -0.192 | [-0.225, -0.160] | -0.490 | 20.9 |
| baseline any buyers | 10 | 1210 | -0.193 | [-0.224, -0.162] | -0.508 | 21.1 |

### tight_D (SL 30%, TP 1.5x 50% + 3x 50%, 6h)
| set | k | n | mean | CI95 | median | win % |
|---|---|---|---|---|---|---|
| ours_top200 | 1 | 411 | -0.192 | [-0.219, -0.158] | -0.357 | 16.5 |
| ours_top200 | 2 | 148 | -0.208 | [-0.251, -0.156] | -0.357 | 13.5 |
| ours_top1000 | 1 | 748 | -0.184 | [-0.208, -0.158] | -0.357 | 18.9 |
| ours_top1000 | 2 | 508 | -0.163 | [-0.193, -0.131] | -0.357 | 19.9 |
| ours_top1000 | 3 | 344 | -0.157 | [-0.195, -0.117] | -0.343 | 19.8 |
| ours_top3000 | 2 | 1076 | -0.168 | [-0.190, -0.146] | -0.357 | 21.4 |
| placebo_random1000 | 3 | 672 | -0.127 | [-0.159, -0.093] | -0.357 | 27.1 |
| baseline any buyers | 3 | 1138 | -0.156 | [-0.178, -0.134] | -0.357 | 22.1 |

### hold_24h (no stop) - best and worst cases
| set | k | n | mean | CI95 |
|---|---|---|---|---|
| ours_top1000 | 3 | 344 | -0.180 | [-0.330, +0.056] |
| ours_top1000 | 2 | 508 | -0.224 | [-0.336, -0.071] |
| ours_top200 | 3 | 58 | -0.420 | [-0.488, -0.356] |
| baseline any buyers | 3 | 1138 | -0.380 | [-0.449, -0.300] |

Other exits (15k, selected rows, mean [CI95]): ladder_C ours_top1000 k=3: -0.144 [-0.208, -0.077]; scalp_E (SL 20%, TP 1.3x, 2h) all sets -0.14 to -0.17 (CI upper bound always < -0.12); runner_F ours_top1000 k=2: -0.181 [-0.235, -0.123]. Full grid (7 sets x 3 k + baselines x 6 exits x 2 liquidity modes) is in `smart_money_grid.csv`.

`col` liquidity variant is ~3-6 pp worse on average (e.g. ours_top1000 k=2: ladder_B -0.236 [-0.279, -0.189], tight_D -0.215 [-0.243, -0.186]). Ranking of sets is unchanged.

Observations
- Only 4 of 276 cells (set x k x exit x liquidity mode) have a CI95 upper bound above 0: honest hold_24h ours_top1000 k=3 ([-0.33, +0.06], n=344, point -18%), and three LEAKY GMGN-winrate-top200 cells (hold_24h k=2, ladder_C k=2 and k=3; n = 92-177). That is what chance gives at this multiplicity; none has a positive point estimate.
- Higher k does not help (k=3 for top200 gets worse: n=58 is tiny and the signal arrives late).
- The ordering ours vs. placebo vs. baseline is within noise. Honest smart-money selection gives no improvement in the expected return of the follower.
- Median trade is a loss of 36-54%: the stop is hit in most trades; wins are 9-30%.
- Fraction of signals tradable: ~60% (e.g. ours_top1000 k=2: 508 of 789). The remainder lack a candle within 15 min after the signal - mostly dead/illiquid tokens. This is a limitation (it excludes some losses that a real follower might still take) but also cannot be fixed with this data.

## 3. Copy-latency decay (entry delayed 0 / 1 / 2 / 4 candles = 0 / 15 / 30 / 60 min extra)
Mean net return, $200, 15k liquidity. "Per-d sample" = all signals tradable at that delay (n varies). Note the expected direction (edge decays with delay) is **not** observed.

| set (k) | exit | d=0 | d=1 | d=2 | d=4 | n (d=0 -> d=4) |
|---|---|---|---|---|---|---|
| ours_top1000 (2) | ladder_B | -0.183 | -0.145 | -0.159 | -0.108 | 508 -> 609 |
| ours_top1000 (2) | tight_D | -0.163 | -0.136 | -0.140 | -0.100 | 508 -> 609 |
| ours_top1000 (1) | ladder_B | -0.218 | -0.198 | -0.167 | -0.122 | 748 -> 994 |
| ours_top1000 (1) | tight_D | -0.184 | -0.159 | -0.149 | -0.104 | 748 -> 994 |
| gmgn_smart_money LEAKY (2) | ladder_B | -0.210 | -0.201 | -0.191 | -0.139 | 918 -> 1072 |
| gmgn_smart_money LEAKY (2) | tight_D | -0.164 | -0.151 | -0.146 | -0.115 | 918 -> 1072 |
| baseline any buyers (3) | ladder_B | -0.192 | -0.189 | -0.168 | -0.142 | 1138 -> 1743 |
| baseline any buyers (3) | tight_D | -0.156 | -0.148 | -0.134 | -0.111 | 1138 -> 1743 |

Same-token sample (only tokens tradable at all four delays; ours_top1000 k=2 n=405, tight_D): -0.171, -0.137, -0.126, -0.093; ladder_B: -0.198, -0.152, -0.143, -0.111. CIs ~ +-0.04-0.06, so d=0 vs d=4 is borderline significant, but the baseline shows the same pattern.

Interpretation (hypotheses, not tested):
1. The first candle after a signal is the worst entry in this universe: freshly launched tokens tend to dump; waiting reduces the fraction hitting stops and reduces the entry slippage in time. This is pure "buy later in the token's life" and does not depend on smart money.
2. The surviving-token effect: requiring a candle at +4 candles removes tokens that went to ~0 within the first hour (and the same-token sample conditions on the future existence of candles, which is itself a mild look-ahead). A real follower who enters at d=4 only enters tokens still alive, so for the "per-d sample" it is feasible, but one cannot compare d=0 and d=4 as the same bet.
3. Signal strength decay (the classic latency story) cannot be seen because there is no signal edge to start with.

## 4. Leakage: GMGN tags vs. train-only skill (same size, same exits, 15k, mean [CI95])
| exit | ours_top1000 k=2 (honest) | gmgn_smart_money k=2 (leaky) | ours_top200 k=2 (honest) | gmgn_winrate_top200 k=2 (leaky) | placebo k=2 |
|---|---|---|---|---|---|
| ladder_B | -0.183 [-0.229, -0.135] | -0.210 [-0.247, -0.170] | -0.279 [-0.342, -0.197] | -0.173 [-0.253, -0.086] | -0.202 |
| tight_D | -0.163 [-0.193, -0.131] | -0.164 [-0.190, -0.136] | -0.208 [-0.251, -0.156] | -0.117 [-0.175, -0.050] | -0.160 |
| hold_24h | -0.224 [-0.336, -0.071] | -0.349 [-0.423, -0.270] | -0.295 [-0.408, -0.130] | -0.307 [-0.534, +0.024] | -0.314 |
| ladder_C | -0.161 | -0.182 | -0.204 | -0.089 [-0.211, +0.040] | -0.169 |

Size of leakage
- `wallet_type == smart_money` (1600 wallets) shows **no** visible advantage over honest or random wallets (-0.164 vs -0.163 vs placebo -0.160 on tight_D). The tag is built on whole-period stats, yet it did not translate into better entries.
- Selection by the leaky continuous `win_rate` (top 200 of 5,943 with data) is the one that leaks visibly: tight_D k=2 -0.117 vs honest top200 -0.208 (leakage ~ +9 pp); ladder_B -0.173 vs -0.279 (~ +11 pp); k=1: -0.151 vs -0.192 (+4 pp), ladder_B -0.198 vs -0.219 (+2 pp). At the 1600-wallet size: -0.128 (k=2, tight_D) vs ours_top1000/3000 -0.163/-0.168 (+3 to +4 pp). The leaky winner is ~1 stdev stronger, but still below zero (only 3 cells touch 0 at the upper CI bound, n = 92-177).
- So the order of magnitude of the leakage in this dataset is ~3-10 pp per trade and it is not statistically solid (CIs overlap); it is smaller than the fees+impact burden (~7-8 pp round trip at 15k) and doesn't flip the sign. Do not take the GMGN tags as evidence of smart-money alpha; the tagged `win_rate` is computed over the whole period including the test trades.

## 5. Caveats
- One month of data, one regime (June 2026); test = 6 days. Trades are time-clustered; bootstrap CIs assume iid, so they are too narrow.
- ~40% of signals untradable (no candle), 75% of trades in the dataset are on tokens without OHLCV and were dropped (the signal set is the 25% subset).
- Win rate is estimated over closed positions only; positions never sold (rugged or held) are ignored, flattering all wallets. A harsher definition (open = loss) was not tried.
- Skill is static (computed once at the split, not rolling) - a rolling update would use fresher info but the persistence test suggests the skill itself is not what is missing.
- Wallet first-buy time may be from before the token's first candle; entry still follows the "next candle after t" rule.
- Multiple-comparison note: 276 cells examined, no cell was selected; none should be read as a discovery.
- Not tested: following sells (exit when smart wallets sell), sizing by wallet PnL, combining with the stage-1 safety filters, requiring wallet's buy size > $X, other timing of k-th buyer (e.g. within N minutes of launch).
