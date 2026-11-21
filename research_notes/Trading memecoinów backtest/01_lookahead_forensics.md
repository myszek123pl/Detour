# 01 - Look-ahead / definition forensics: liquidity_usd and snapshot features

Dataset: ian05012/solana-memecoin-dataset (GMGN, 2026-06-10..06-30). 44,460 snapshots, 31,013 tokens, 9.50M trades, 272k 15m candles.
Backtest under review: `backtest/backtest.py` -> `out/sim_results.parquet` (9,684 tradeable first-snapshots), rules in `backtest/rules.py`.
Notation: `lm` = liquidity_usd / market_cap_usd. Net = after fee 1.25%/side, impact 2*200/liquidity, $0.30 tip, $200 position (same as rules.py).
Scripts: `backtest/forensics1..12.py`, `backtest/forensics_final.py` (the last one is the only one that reads only `out/`; 1-12 write intermediates to /tmp/x).

## TL;DR

1. **No timestamp look-ahead was found in liquidity_usd, price_at_capture, price_change_1h/6h or the 1h flow features.** They match trades/candles *before* capture and are uncorrelated with the future.
2. **But market_cap_usd / price_at_capture are inconsistent with liquidity_usd in ~36% of snapshots (lm>1) and impossible in 14% (lm>2).** In the lm>2 group the market cap is *frozen* (identical in 94.7% of consecutive snapshots at ~$3.5-4.0k, the pump.fun curve start value) while liquidity keeps updating. So `lm` is mostly a **stale-market-cap detector**, not a "healthy pool" signal. That is the real source of the 0.6x threshold artefact.
3. The "+24-33%/trade" result exists only in the lm>0.6 bucket (n=91, 85 of them before 06-24; 6 after) and survives dropping the liquidity filter - so it is carried by `lm`, not by liq>=10k. It is **not usable**: n is tiny, the bucket is defined by a corrupted field, the candle paths there are truncated (median 3 candles / 0.5 h), and there is no out-of-sample evidence.
4. With only safe features (five safety flags, no liquidity/mcap-derived input): **ladder_B -27.5% / trade** (95% CI -33% .. -21%), n=541. Baseline (no filter) -18.6%. No edge.

## 1. Internal consistency of price / market cap / liquidity

| Check | Result |
|---|---|
| price_at_capture * 1e9 vs market_cap_usd | within +-1% in 92.4% rows; <0.99 in 5.9% (mostly large-mcap tokens with non-1e9 supply, implied supply up to 8.4e10); >1.01 in 1.7% |
| price_at_capture vs 15m candle price at the same time (|log err| median) | 0.12 at offset 0; 0.24 at -15 min; 0.26 at +15 min; grows monotonically both ways -> **snapshot price is contemporaneous, no time shift** |
| lm = liquidity/mcap, all snapshots | lm>0.6: 52.8%; lm>1: 36.0%; lm>2: 13.9% (median lm 0.52 fresh tokens, 0.93 for 5-15 min old) |
| Same on the 9,684 tradeable first snapshots | lm>0.6: 69.7% |

Physics: for a constant-product pool with supply S = 1e9 and token reserve T, `liquidity = 2Q`, `mcap = Q/T * S` -> **lm = 2T/S**. A freshly graduated pump.fun pool holds ~20.7% of supply -> lm ~ 0.41 (the expectation in the task). lm>1 means >50% of supply sits in the pool, lm>2 is impossible.

| lm bucket (all snapshots) | n | median mcap | median liquidity | median time since launch |
|---|---|---|---|---|
| (0,0.1] | 7,179 | $110.8k | - | 0.07 h |
| (0.4,0.5] | 2,602 | $27.4k | - | 0.20 h |
| (0.6,0.8] | 4,108 | $19.7k | - | 0.22 h |
| (1,2] | 9,790 | $8.0k | - | 0.15 h |
| >2 | 6,194 | $4.0k | $46k (p5-p95 18k-78k) | 0.12 h |

lm vs mcap decile: bottom mcap decile ($1.0-3.9k) has median liquidity $33.5k, median lm 9.0.

### Liquidity is consistent with trade flow, mcap is not

Reconstructed from trades parquet (fresh tokens, time_since_launch<300 s, >=20 pre-capture trades, n=15,620). ratio = liquidity / (2 * net USD buys before capture):

| lm bucket | n | median liquidity | median net buys | liq/(2*net buys) | median mcap |
|---|---|---|---|---|---|
| (0,0.4] | 6,821 | $12.3k | $7.6k | 0.98 | $93k |
| (0.4,0.6] | 1,574 | $12.0k | $10.9k | 0.89 | $28k |
| (0.6,1] | 1,723 | $10.5k | $5.3k | 1.00 | $12.7k |
| (1,2] | 3,252 | $8.4k | $2.3k | 2.52 | $7.1k |
| >2 | 2,250 | $41.5k | $20.8k | 1.00 | $4.0k |

- liquidity ~ 2 x net USD buys (ratio ~1.0, Spearman liq vs pre-net 0.76, liq vs pre-buy 0.70) -> **liquidity_usd tracks past flow as an AMM reserve should**.
- In the lm>1 fresh group 99.3% have net buying > 0 and median net buys = 0.5 x mcap; net buyers cannot leave >50% of supply in the pool. Flow-implied lm (2*(0.207 - net/mcap)) has Spearman **-0.75** vs actual lm (the actual lm *rises* with net buying, i.e. mcap is the stale one).
- Multi-snapshot persistence (7,874 tokens with >=2 snapshots, median gap ~18 min):

| lm bucket (1st snap) | n | P(mcap identical in next snap) | P(liquidity identical) | median mcap ratio next/first | P(lm>1 in next snap) |
|---|---|---|---|---|---|
| (0,0.4] | 2,864 | 20% | 2% | 1.00 | 1% |
| (0.6,1] | 1,586 | 13% | 0.2% | 1.00 | 25% |
| (1,2] | 2,171 | 9% | 0.1% | 1.44 | 61% |
| >2 | 253 | **94.7%** | 0% | 1.00 | 96% |

  Liquidity (and holder_count: 2-4% unchanged) refresh each snapshot; mcap/price for lm>2 tokens do not. Top repeated mcap among lm>2: 3,827.78 / 3,990 / 3,829.44 (curve-start level), versus 64,845.97 overall (graduation level).
- Corr(log d-liquidity, log d-mcap) between snapshots of one token is only 0.54.

Conclusion: **liquidity_usd is the better-behaved field; market_cap_usd/price_at_capture are stale or from a different source for a large share of rows**. lm>0.6 therefore selects mostly stale-mcap rows. (Not time-shift look-ahead, but a definitional/data-freshness inconsistency that a filter can exploit by accident.)

## 2. Look-ahead tests (future information inside snapshot features)

| Feature | Test | Result | Verdict |
|---|---|---|---|
| buy_usd_1h / sell_usd_1h | vs trades in last 1 h before capture; vs next 1 h | Spearman 0.964 / 0.979 vs past (median ratio 1.000); vs future 0.235 / 0.733 (sell persistence) | safe |
| buy_total, net_flow_usd | vs pre-capture trade sums | Spearman 0.999 / 0.936, ratio 1.000 | safe |
| price_change_1h | vs candle return before capture / after capture | **0.83 past (n=2,949)**, -0.06 future (n=14,780) | safe |
| price_change_6h | same | 0.79 past, -0.01 future | safe |
| price_at_capture | vs candles at offsets -2h..+4h | minimum error at offset 0 | safe |
| liquidity_usd | regression log(liq) ~ log(pre buys)+log(mcap)+log(last-1h buys)+log(1+future 1h return)+log(future 1h buys), n=14,780, R2 0.67 | future return coef -0.016 (t=-5.5), future buys +0.019 (t=26) vs past buys +0.210 (t=60). Spearman liq vs future 1h return 0.098; lm vs future return -0.064 | no meaningful leak (small activity-persistence effect only) |
| holder_count | Spearman with distinct wallets pre-capture vs all trades (incl. future) | 0.465 vs 0.299 (trade log only holds ~140-170 trades per snapshot, so weak overall) | no leak evidence; low information |
| volume_h24 | vs candle volume before / next 1 h / next 24 h | 0.645 / 0.554 / 0.559; ratio to either ~1.3 | **inconclusive** (candles cover mostly the future; cannot separate persistence from leak) -> treat as suspect |
| lm, time_since_launch | Spearman 0.04; time buckets 0-2 min lm med 0.36, 5-15 min 0.94, >6 h 0.38 | not a time-since-launch effect | - |
| Post-capture trades in trades parquet | 23% of rows are after captured_at | features cut cleanly at capture; exposed future trades are a trap for anyone reconstructing features | note |

Other data defects found (all matter for backtests):
- `max_return_1h/6h/24h/3d` are **0.0 in 99.9%** of rows and `close_return_1h` is NaN in 99.9% -> unusable labels (README says they are labels anyway). Usable independent labels: `staged_exit_return` (5% NaN), `runner_peak_x`, `reaches_2x`.
- trades parquet contains 16,678 rows dated 2024-06..2026-05 (before the collection window) and sells total $4.23B vs buys $2.47B (median sell $58 vs buy $15) - treat trade log as a sample, not a full ledger.
- Candle series for the lm>0.6 filtered bucket are short: median 3 candles, span 0.49 h (vs 14-21 candles, 3.5-5.3 h elsewhere). backtest.py marks any open remainder at the last available close ("time exit at last close") -> optimistic when a series ends early, and `hold_24h` becomes "last close of a 30-minute series".

## 3. Why the filter looked profitable (reproduced)

Original six conditions (mint+freeze off, top10<30%, dev<5%, bundler<15%, insider<15%, liq>=10k), net per trade, $200 position, bootstrap 95% CI in brackets (rules.py convention):

| Set | n | peak>=2x | ladder_B | tight_D | runner_F | hold_24h |
|---|---|---|---|---|---|---|
| All tradeable | 9,684 | 21.6% | -18.6% | -17.5% | -17.4% | -30.0% |
| Six conditions, lm>0.6 | 91 | 25.3% | **+43.0%** [31,55] | +34.0% | +46.6% | +61.3% |
| Six conditions, lm<=0.6 | 42 | 23.8% | -2.1% [-21,19] | +2.0% | +3.0% | -37.3% |
| Six conditions, all | 133 | - | ~ +28% | | | |

- Permutation test inside the 133 rows (shuffle the lm>0.6 flag): ladder_B diff +45.1 pp, p<0.0001 (it is a real difference in this sample - the question is why, see below).
- Dropping top-3 winners: ladder_B +36.9% (median +25.6%); top-5 gross winners = 38% of gross gain.
- Time split at 06-24 (rules.py): train 85 rows +42.5% / test **6 rows** +50% -> no usable out-of-sample.
- Independent GMGN labels agree directionally (so not only a candle-truncation artefact): in the filtered lm>0.6 rows reaches_2x = 39.6% vs 21.4% (lm<=0.6), staged_exit_return mean 1.63 vs 0.97.
- Cost model leak is minor: removing price impact altogether gives +46.5% vs +43.0%; flat 4% impact gives +34.8% for ladder_B.
- But the lm effect does **not** exist on the unfiltered sample: label reaches_2x is 26.5% (lm<=0.6) vs 21.1% (lm>0.6); all ladder_B means by lm bucket are -11% to -31%. It appears only in the intersection with the safety flags, where lm<=0.6 rows are terrible (-42.5%): a conjunction of a corrupted field with filters that select "low holder concentration" -> classic fishing in a small, 20-day, one-regime sample. Forking paths (6 conditions, thresholds tuned on the same data) are not corrected for.

Interpretation (hypothesis, not proven): lm>0.6 + safety flags selects very young tokens still carrying a frozen curve-start market cap (price column stale) while the live pool already has real liquidity; those tokens are in an early pump phase, and their short candle paths end mid-pump. The effect is therefore driven by a data-freshness artefact (and path truncation), not by tradable information. I could not prove a smoking-gun time shift; I could show the field is internally inconsistent and the signal is not robust.

## 4. Feature verdicts

| Feature group | Verdict | Reason |
|---|---|---|
| price_at_capture | safe as timestamp, **suspect level** for lm>1 rows | contemporaneous with candles; stale (frozen) in lm>2 rows |
| market_cap_usd | **suspect** | frozen at ~$3.5-4k in 94.7% repeat snapshots of lm>2 tokens; = price*1e9 only by construction |
| liquidity_usd | safe w.r.t. look-ahead; **do not combine with mcap** (no lm / liq-to-mcap ratios); OK as a cost/size input | ~2x net buys, no future info; but it is the (only) fresh half of an inconsistent pair |
| price_change_1h, price_change_6h | safe | past-only (rho 0.83 / 0.79 vs past, ~0 vs future) |
| buy_usd_1h, sell_usd_1h, net_flow_usd, buy_total, unique_buyers/sellers, trade-flow group | safe (pre-capture) | match trade log exactly before capture |
| holder_count | probably safe, low quality | no leak evidence; weak link to trade log |
| volume_h24 | suspect | cannot rule out forward-looking window; ratio ~1.3 to both past and future volume |
| mint/freeze_disabled, top10_holder_pct, dev_remaining_pct, bundler/insider_pct_holders | unverified but plausible snapshot-time | cannot be checked against trades; only used as safety screens |
| max_return_*, close_return_1h | broken (0 / NaN) | never use |
| staged_exit_return, runner_peak_x, reaches_2x, time_to_peak_sec, mdd_from_peak, scalp_exit_return | labels (future) | never as features |
| number_markets | constant (1 in 99.8%) | useless |

## 5. Re-computed backtest with safe features only

"Safe" = five safety flags (mint+freeze, top10<30%, dev<5%, bundler<15%, insider<15%); **no liq>=10k, no lm, no mcap-derived input**. Entry/exit logic unchanged. Net per trade, $200, 95% bootstrap CI.

| Set | n | peak>=2x | ladder_B | tight_D | runner_F | hold_24h |
|---|---|---|---|---|---|---|
| All tradeable (no filter) | 9,684 | 21.6% | -18.6% [-19.9,-17.2] | -17.5% | -17.4% | -30.0% |
| **Five safety flags (safe set)** | 541 | 16.5% | **-27.5% [-33.2,-21.3]** | -26.4% [-30.2,-22.5] | -22.4% [-30.7,-11.7] | -49.7% |
| Five safety, flat 4% impact (liquidity-free costs) | 541 | 16.5% | -14.8% [-21.5,-6.5] | -12.6% | -7.6% [-18.6,+8.9] | -46.6% |
| Five safety, lm<=1 (physically possible) | 444 | 15.1% | -41.8% [-47.4,-35.1] | -38.5% | -36.3% | -72.5% |
| Five safety, lm>0.6 (diagnostic only) | 109 | 21.1% | +31.7% [20.6,42.9] | +24.4% | +34.7% | +46.9% |
| Five safety, lm>1 (impossible region, diagnostic) | 97 | 22.7% | +37.7% | +29.1% | +41.6% | +55.1% |

Result: **no edge from safe features.** Safety flags alone make results *worse* than no filter at -27.5% (they remove lottery tickets). Only after conditioning on the corrupted lm does a positive number appear; it persists without liq>=10k (+31.7%, n=109), confirming `lm` rather than liquidity drives it. The best-case liquidity-free cost model still gives -7.6% (runner_F) with CI spanning 0.

## 6. Recommendations

1. Remove `lm`, liq>=10k-based selection and any mcap/price-level feature from rules; keep liquidity only in the cost model (it behaves like pool reserve), preferably capped by flow-implied reserve (2 x net buys).
2. Drop snapshots with market cap frozen across snapshots or lm>1 from all evaluations, or re-derive mcap from candles at capture time.
3. Fix exits for truncated candle paths: if the series ends before the horizon, mark the remainder at 0 or haircut it (current code uses the last close).
4. Do not use `max_return_*`; evaluate against `staged_exit_return`/`runner_peak_x` as cross-check only.
5. Any new rule needs a pre-registered threshold, a time split with enough OOS rows (>=100), and correction for the number of tried combos.

## Open items / limits

- Smoking-gun mechanism for *why* lm>0.6 + safety flags profits was not proven; stale mcap + young age + truncated paths is the best-supported explanation.
- The trade log holds only ~140-170 trades per snapshot (about the last 200), so flow reconstructions for older tokens are lower bounds; the liquidity/flow check was therefore restricted to tokens <300 s old.
- No safe-feature ML/flow rules were fitted here (only the filter reproduction); that is the next step if wanted.
