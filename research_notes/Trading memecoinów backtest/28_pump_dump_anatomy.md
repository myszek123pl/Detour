# 28. Anatomy of pumps and dumps in memecoins (June 2026, GMGN dataset)

Scripts: `/home/user/Detour/backtest/pd_events.py`, `pd_trades.py`, `pd_outcomes.py`, `pd_a3.py`, `pd_a4.py`, `pd_a5.py`, `pd_det.py`, `pd_sens.py` (helper `pd_md.py`). All gross of fees/slippage/tips. No web sources.

## 0. TL;DR

1. Under the definition +50% within <=1h (15m candles, close/open), 8,753 pump events (2,966 tokens) and 15,351 dump events (-30% within <=1h; 5,580 tokens) exist in 20 days. **Buying at the close of the trigger candle loses on average**: median -7% after 15 min, -20% after 1h, -29% after 2h, -38% after 4h (mean -12% / -15% at 1h / 2h; n=7,534). 42% of pumps fully retrace to the pre-pump price within 2h, 33% plateau/bleed, only 26% continue (+25% or more above entry within 2h without a full retrace).
2. The top is usually the trigger itself: in 55% of events the peak candle is the trigger candle; 60% of pumps are followed by a -30% close from the peak within 1h (78% within 3h); median time peak to -30% is 30 min. 25% of dumps happen inside one 15-min candle (median close 0.48x of open), 63% within 3 candles.
3. Sellers into pumps are overwhelmingly wallets that bought before the pump started (87% of sell USD in event window plus 1h; they supplied only 36% of pump-phase buy USD). First-10 buyers of the token are only 5.7% of sell USD but sell 17.5x what they buy in the window. Continuation pumps have markedly more fresh (pump-phase and later) sellers (23% vs 12%) i.e. broader distribution, retraces are sold by the early crowd (88%).
4. What separates continuation from retrace is weak. Best candle-only signals: older token (AUC 0.62), last-candle volume above base (0.61), less crowded pre-pump trade flow (n trades/15m in pre-hour AUC 0.40 i.e. crowded pre-pump retraces) and top-5 wallet concentration in pre-hour (0.59). GMGN snapshot features (stale at trigger) are nearly useless (|AUC-0.5| <= 0.05).
5. A causal detector (LightGBM, daily walk-forward, 2h purge, 5,633 OOS events 15-29 Jun) reaches **AUC 0.60 for "buyer at the top"** (AUC 0.63 vs the full-retrace label). Skipping the riskiest ~11% (p>=0.55) gives precision 59% vs 41.5% base but recall only 16%; skipping 36% (p>=0.45) gives recall 44%, precision 51%, and loses 33% of the good continuations. Mean 2h return of kept buys improves from -15.8% to -10.4% (CI of the improvement [+3.5,+7.6] pp, token-bootstrap) - **still negative**. The detector reduces damage, it does not create a positive edge; it does not reliably let you avoid being the buyer at the top.

## 1. Data and definitions

- `ohlcv.parquet`: 272k candles, 11,170 tokens. Cleaning: duplicates by (token, ts) (62k keys; 3.9k with conflicting values, 6%) -> keep highest volume; wicks > 10x the body replaced by the body edge (1,606 candles had high > 10x close); open/close used for events (continuity open_t = close_t-1 verified), so wick glitches do not trigger events. Gaps (no trades) are forward-filled flat. 183,651 real candles -> 272k grid candles. Tokens with a >400-candle span (very few) skipped.
- **Pump**: close of candle i / min open of candles i-3..i >= 1.5 (the window spans <= 1h from candle open to candle close), window volume >= $2,000, >=1 real candle. Event start S = open of the trough candle j, trigger T = close of candle i (the price a real-time observer sees), peak = max close in candles i..i+3. After an event the scan resumes after the peak (no overlapping events).
- **Dump**: mirror, close/max open <= 0.7.
- Entry for outcome analysis = close of trigger candle (== next candle open). Forward outcomes require >=2h (8 candles) of later observed series (86% of pumps); "censoring" caveat: tokens that go quiet after a pump (no candles) drop out, which biases toward survivors, so true losses are larger than reported.
- **Outcome classes** (2h after trigger; p0 = pre-pump start price): *full_retrace* = some close <= 1.05 x p0; *continue* = no full retrace and max close >= +25% above entry; *plateau* = rest.
- **Trade log**: 9.5M trades, 67k tokens; for a token the log runs launch -> last snapshot capture (verified: first trade = launch, last trade = capture - ~5 s, no duplicates). So wallet-level analysis only exists for events before the last snapshot of the token: 4,504 pump events (3,147 with a full hour after) - tokens that were re-snapshotted (trending) - a selected sample. Trade phases: pre = 1h before S, pump = [S,T), post1 = [T,T+1h], post2 = next hour. Trade log covers only ~26% of candle volume per candle in overlapping candles (median ratio), so trade-log USD levels are not comparable with candle volume; ratios are fine. Concentration metrics (top-5 share, HHI) rise mechanically when the phase has fewer trades - read with n.
- Time range: 10-29 Jun 2026, a single regime; 20 days; events are per token clustered (3 events per token on average) - CIs bootstrap by token where given.

### Sensitivity of event counts (kind, threshold as multiple, window in candles, volume floor)

| kind | thr | win_candles | minvol | events | tokens |
|---|---|---|---|---|---|
| pump | 1.300 | 4 | 2000 | 13460 | 3586 |
| pump | 1.300 | 4 | 0 | 15647 | 4021 |
| pump | 1.300 | 4 | 10000 | 8311 | 2633 |
| pump | 1.300 | 2 | 2000 | 8908 | 3413 |
| pump | 1.300 | 8 | 2000 | 19335 | 3662 |
| pump | 1.500 | 4 | 2000 | 8753 | 2966 |
| pump | 1.500 | 4 | 0 | 9429 | 3172 |
| pump | 1.500 | 4 | 10000 | 6057 | 2297 |
| pump | 1.500 | 2 | 2000 | 5503 | 2745 |
| pump | 1.500 | 8 | 2000 | 13164 | 3074 |
| pump | 2.000 | 4 | 2000 | 3993 | 1959 |
| pump | 2.000 | 4 | 0 | 4135 | 2013 |
| pump | 2.000 | 4 | 10000 | 3242 | 1630 |
| pump | 2.000 | 2 | 2000 | 2333 | 1662 |
| pump | 2.000 | 8 | 2000 | 6547 | 2133 |
| pump | 3.000 | 4 | 2000 | 1533 | 955 |
| pump | 3.000 | 4 | 0 | 1590 | 983 |
| pump | 3.000 | 4 | 10000 | 1388 | 874 |
| pump | 3.000 | 2 | 2000 | 786 | 676 |
| pump | 3.000 | 8 | 2000 | 2725 | 1118 |
| dump | 0.800 | 4 | 2000 | 20116 | 5822 |
| dump | 0.800 | 4 | 0 | 27790 | 7000 |
| dump | 0.800 | 4 | 10000 | 10561 | 3816 |
| dump | 0.800 | 2 | 2000 | 12636 | 5614 |
| dump | 0.800 | 8 | 2000 | 32789 | 5945 |
| dump | 0.700 | 4 | 2000 | 15351 | 5580 |
| dump | 0.700 | 4 | 0 | 18788 | 6355 |
| dump | 0.700 | 4 | 10000 | 8457 | 3662 |
| dump | 0.700 | 2 | 2000 | 9206 | 5273 |
| dump | 0.700 | 8 | 2000 | 26943 | 5748 |
| dump | 0.500 | 4 | 2000 | 8371 | 4575 |
| dump | 0.500 | 4 | 0 | 9108 | 4868 |
| dump | 0.500 | 4 | 10000 | 5259 | 3137 |
| dump | 0.500 | 2 | 2000 | 4868 | 3972 |
| dump | 0.500 | 8 | 2000 | 16567 | 4914 |
| dump | 0.300 | 4 | 2000 | 4073 | 2693 |
| dump | 0.300 | 4 | 0 | 4400 | 2823 |
| dump | 0.300 | 4 | 10000 | 2946 | 2044 |
| dump | 0.300 | 2 | 2000 | 2289 | 2024 |
| dump | 0.300 | 8 | 2000 | 8656 | 3169 |

(base case: pump 1.5x / 4 candles / $2k; dump 0.7x / 4 candles / $2k). Counts scale roughly 3x per tightening of the threshold; $0 floor adds 7-48% mostly micro-volume noise.

## 2. Anatomy: hour before / during / after

Candle-level (all events):

### Candle volume around pumps (events with >=2 pre candles)

| index | median $/15m | mean $/15m | median ratio vs pre | n |
|---|---|---|---|---|
| pre15 | 3,148 | 15,392 | 1.000 | 6062 |
| ev15 | 4,734 | 17,190 | 1.544 | 6062 |
| post1_15 | 3,181 | 12,325 | 1.003 | 5709 |
| post2_15 | 1,724 | 8,632 | 0.610 | 5283 |

### Candle volume around dumps (events with >=2 pre candles)

| index | median $/15m | mean $/15m | median ratio vs pre | n |
|---|---|---|---|---|
| pre15 | 6,534 | 24,038 | 1.000 | 9205 |
| ev15 | 3,663 | 16,678 | 0.686 | 9205 |
| post1_15 | 1,451 | 6,846 | 0.294 | 8499 |
| post2_15 | 828.063 | 4,575 | 0.162 | 7788 |

### Pump classes (2h forward, entry = trigger close): share and volume

| cls | n | share | pre $/15m | event $/15m | post1 $/15m | post2 $/15m |
|---|---|---|---|---|---|---|
| continue | 1,925 | 0.256 | 2,511 | 7,913 | 8,422 | 6,535 |
| full_retrace | 3,154 | 0.419 | 2,776 | 9,423 | 4,407 | 1,259 |
| plateau | 2,455 | 0.326 | 1,589 | 4,833 | 2,128 | 1,037 |

### Forward return after buying at trigger close

| cls | n | med r15m | med r30m | med r60m | med r120m | med r240m | mean r15m | mean r60m | mean r120m | med_fmax2h | med_fmin2h | med_trig_mult | med_peak_mult |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ALL | 7534 | -0.073 | -0.125 | -0.197 | -0.294 | -0.378 | -0.058 | -0.115 | -0.154 | 0.047 | -0.387 | 1.809 | 2.036 |
| continue | 1925 | 0.060 | 0.153 | 0.258 | 0.273 | 0.085 | 0.180 | 0.491 | 0.616 | 0.701 | -0.108 | 1.852 | 2.689 |
| full_retrace | 3154 | -0.166 | -0.298 | -0.464 | -0.618 | -0.682 | -0.177 | -0.446 | -0.584 | -0.092 | -0.663 | 1.756 | 1.859 |
| plateau | 2455 | -0.079 | -0.120 | -0.158 | -0.199 | -0.269 | -0.092 | -0.166 | -0.205 | 0.008 | -0.286 | 1.858 | 1.942 |

### Fraction of pumps ending below pre-pump start price (close vs p0) by horizon

| h | share_below_start | share_below_entry | n |
|---|---|---|---|
| +30m | 0.121 | 0.670 | 6540 |
| +1h | 0.208 | 0.698 | 6540 |
| +2h | 0.301 | 0.732 | 6540 |
| +4h | 0.400 | 0.762 | 6540 |

### Time (15m steps after trigger) until close first <= 1.05x pre-pump price (4h window, n=6540)

| retr_step | share | cum |
|---|---|---|
| 1.000 | 0.071 | 0.071 |
| 2.000 | 0.078 | 0.149 |
| 3.000 | 0.062 | 0.211 |
| 4.000 | 0.056 | 0.267 |
| 5.000 | 0.048 | 0.315 |
| 6.000 | 0.037 | 0.352 |
| 7.000 | 0.030 | 0.382 |
| 8.000 | 0.025 | 0.407 |
| 9.000 | 0.022 | 0.429 |
| 10.000 | 0.024 | 0.453 |
| 11.000 | 0.017 | 0.470 |
| 12.000 | 0.017 | 0.487 |
| 13.000 | 0.014 | 0.501 |
| 14.000 | 0.014 | 0.515 |
| 15.000 | 0.011 | 0.527 |
| 16.000 | 0.010 | 0.537 |
|  | 0.463 | 1.000 |

### Median price path (multiple of pre-pump start price p0)

| minutes | step_after_trigger | median_x_of_start | p25 | p75 | n |
|---|---|---|---|---|---|
| 0 | 0 | 1.804 | 1.611 | 2.231 | 8753 |
| 15 | 1 | 1.685 | 1.394 | 2.216 | 8625 |
| 30 | 2 | 1.601 | 1.263 | 2.153 | 8450 |
| 45 | 3 | 1.538 | 1.153 | 2.123 | 8270 |
| 60 | 4 | 1.482 | 1.067 | 2.090 | 8146 |
| 90 | 6 | 1.392 | 0.936 | 2.039 | 7860 |
| 120 | 8 | 1.341 | 0.847 | 1.966 | 7534 |
| 180 | 12 | 1.254 | 0.733 | 1.940 | 7007 |
| 240 | 16 | 1.203 | 0.655 | 1.905 | 6540 |

### PUMP events: trade-log phases (median over events; pre = 1h before start, pump = event window, post1 = 1h after trigger)

| ph | n15 | usd15 | buy_share | nb15 | ns | med_a | mean_buy | top1 | top5 | hhi | new_tok_share_trades | fresh_ds_usd_share | N_events |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pre | 16.000 | 3,355 | 0.688 | 9.500 | 20.000 | 135.802 | 211.519 | 0.140 | 0.424 | 0.057 | 0.808 | 0.064 | 2557 |
| pump | 12.000 | 4,964 | 0.698 | 7.500 | 11.000 | 218.841 | 356.206 | 0.183 | 0.562 | 0.091 | 0.696 | 0.063 | 2557 |
| post1 | 6.500 | 3,094 | 0.621 | 3.500 | 10.000 | 242.093 | 379.288 | 0.211 | 0.609 | 0.107 | 0.629 | 0.062 | 2557 |

### DUMP events: trade-log phases (pre = 1h before start, pump row = the dump window itself)

| ph | n15 | usd15 | buy_share | nb15 | ns | med_a | mean_buy | top1 | top5 | hhi | new_tok_share_trades | fresh_ds_usd_share | N_events |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pre | 18.125 | 5,130 | 0.684 | 11.000 | 25.000 | 169.973 | 274.887 | 0.125 | 0.385 | 0.048 | 0.775 | 0.069 | 2408 |
| pump | 7.000 | 2,589 | 0.580 | 3.750 | 7.000 | 196.349 | 287.823 | 0.276 | 0.748 | 0.155 | 0.618 | 0.041 | 2408 |
| post1 | 4.250 | 1,533 | 0.645 | 2.500 | 6.000 | 196.696 | 318.588 | 0.280 | 0.762 | 0.162 | 0.639 | 0.049 | 2408 |

### PUMP events: phase means

| ph | buy_share | top5 | new_tok_share_trades | fresh_ds_usd_share | med_a | mean_buy |
|---|---|---|---|---|---|---|
| pre | 0.678 | 0.451 | 0.780 | 0.109 | 337.528 | 523.047 |
| pump | 0.693 | 0.533 | 0.670 | 0.104 | 531.591 | 788.908 |
| post1 | 0.610 | 0.583 | 0.602 | 0.104 | 668.900 | 937.029 |


Reading the tables above:
- Pumps: median volume rises only 1.5x vs the preceding hour during the pump ($4.7k vs $3.1k per 15 min), is flat in the following hour (1.0x) and halves in the second hour (0.6x). The pump is not a volume explosion on average; it is a thin-book price move on ~1.5x volume.
- Trade log (n=2,557 pumps with full pre/pump/post coverage): buy share of USD is 0.69 pre, 0.70 in the pump, 0.62 after; trades per 15 min fall 16 -> 12 -> 6.5, unique buyers per 15 min 9.5 -> 7.5 -> 3.5, while median trade size rises 136 -> 219 -> 242 USD and the top-5 wallets' share of USD rises 0.42 -> 0.56 -> 0.61. I.e. the crowd leaves and trade becomes concentrated and larger - consistent with whales/insiders as the residual counterparties after the move. The share of wallets that are new to the token falls 0.81 -> 0.70 -> 0.63 (repeat wallets dominate). "Fresh to the dataset" wallets are flat at ~6% of USD (median) in all phases - no sign of a flood of brand-new wallets in the pump itself.
- Dumps: the hour before a dump is already the busiest (5.1k USD/15m, 25 sellers) and is followed by volume decay to 0.69x during the dump, 0.29x and 0.16x in the following 2 hours: dumps kill liquidity. Buy share drops 0.68 -> 0.58 in the dump window but never inverts (a -30% move on ~58% buy USD means thin books, not a sell stampede); top-5 share jumps to 0.75 (a few wallets do the damage; trade count drops to 7 per 15 min).

## 3. Continue vs retrace (what distinguishes them)

Fraction of pumps at the horizon below pre-pump price: 12% at 30 min, 21% at 1h, 30% at 2h, 40% at 4h; below entry: 67% / 70% / 73% / 76%. Time to full retrace (first close <= 1.05 x p0) is fast: 15% within 30 min, 27% within 1h, 41% within 2h, 54% within 4h (46% never within 4h). Median price path (x of pre-pump price): 1.80 at trigger, 1.48 at +1h, 1.34 at +2h, 1.20 at +4h (p25 at +4h = 0.66). Class shares are stable across days (retrace 35-48%, continue 20-29%; median 2h return -21% to -35%), so the result is not a single-day artifact.

### Continue vs full retrace: candle features (known at trigger)

| feature | med_continue | med_plateau | med_retrace | AUC_cont_vs_retr | n_cont | n_retr |
|---|---|---|---|---|---|---|
| log_age | 5.152 | 5.697 | 4.593 | 0.618 | 1915 | 3138 |
| vlast_vs_base | 0.225 | 0.556 | -0.221 | 0.608 | 1560 | 2108 |
| trig_mult | 1.852 | 1.858 | 1.756 | 0.567 | 1925 | 3154 |
| nsteps | 3.000 | 4.000 | 3.000 | 0.554 | 1925 | 3154 |
| log_vpump15 | 8.976 | 8.483 | 9.151 | 0.460 | 1925 | 3154 |
| log_mcap | 4.476 | 4.438 | 4.441 | 0.533 | 1924 | 3152 |
| pre_run | -0.158 | -0.106 | -0.214 | 0.532 | 1560 | 2108 |
| from_first | 1.794 | 1.728 | 1.709 | 0.521 | 1925 | 3154 |
| hi_over_close | 0.131 | 0.131 | 0.122 | 0.516 | 1925 | 3154 |
| uwick | 0.181 | 0.178 | 0.173 | 0.509 | 1925 | 3154 |
| vol_ratio | 0.710 | 1.007 | 0.576 | 0.492 | 1925 | 3154 |
| cpos | 0.674 | 0.563 | 0.657 | 0.494 | 1925 | 3154 |
| prev_ret | 0.112 | 0.119 | 0.117 | 0.495 | 1760 | 2682 |
| real_frac_pump | 1.000 | 1.000 | 1.000 | 0.497 | 1925 | 3154 |
| last_ret | 0.304 | 0.120 | 0.289 | 0.501 | 1925 | 3154 |

### Continue vs full retrace: snapshot features (GMGN, captured before trigger)

| feature | med_continue | med_plateau | med_retrace | AUC_cont_vs_retr | n_cont | n_retr |
|---|---|---|---|---|---|---|
| liq_mcap | 0.430 | 0.463 | 0.485 | 0.451 | 1924 | 3152 |
| s_smart_money_count | 3.000 | 3.000 | 2.000 | 0.544 | 1924 | 3152 |
| s_crew_cohesion | 0.440 | 0.447 | 0.503 | 0.462 | 1863 | 3044 |
| s_bundler_ratio | 0.188 | 0.184 | 0.206 | 0.466 | 1924 | 3152 |
| s_seller_loss_ratio | 0.295 | 0.318 | 0.316 | 0.472 | 1924 | 3152 |
| s_unique_buyers | 96.000 | 96.000 | 97.000 | 0.476 | 1924 | 3152 |
| s_unique_sellers | 34.000 | 34.000 | 32.000 | 0.523 | 1924 | 3152 |
| s_only_buy_pct | 0.626 | 0.622 | 0.646 | 0.477 | 1924 | 3152 |
| s_trade_buy_sell_ratio | 2.848 | 2.800 | 2.970 | 0.478 | 1924 | 3152 |
| s_flipper_ratio | 0.349 | 0.351 | 0.333 | 0.522 | 1924 | 3152 |
| s_holder_count | 256.000 | 237.000 | 247.000 | 0.517 | 1923 | 3143 |
| s_profitable_pct | 0.626 | 0.602 | 0.606 | 0.516 | 1915 | 3132 |
| s_sniper_count | 13.000 | 13.000 | 13.000 | 0.515 | 1924 | 3152 |
| s_dev_remaining_pct | 0.000 | 0.000 | 0.000 | 0.514 | 1924 | 3152 |
| s_cluster_max_pct | 0.178 | 0.172 | 0.181 | 0.489 | 1924 | 3152 |
| s_price_change_1h | 47.705 | 37.760 | 46.205 | 0.509 | 1924 | 3152 |
| s_insider_pct_holders | 0.334 | 0.341 | 0.334 | 0.507 | 1924 | 3152 |
| s_top10_holder_pct | 0.229 | 0.234 | 0.230 | 0.503 | 1924 | 3152 |
| s_is_boosted | 0.000 | 0.000 | 0.000 | 0.503 | 1924 | 3152 |
| s_has_twitter | 1.000 | 1.000 | 1.000 | 0.498 | 1924 | 3152 |
| s_fresh_wallet_pct | 0.090 | 0.089 | 0.091 | 0.501 | 1924 | 3152 |
| s_lp_burned_pct | 1.000 | 1.000 | 1.000 | 0.500 | 1924 | 3152 |
| s_rug_probability | 0.000 | 0.000 | 0.000 | 0.500 | 1924 | 3152 |

### Continue vs full retrace: trade-log features pre-trigger (subset with trade coverage)

| feature | med_continue | med_plateau | med_retrace | AUC_cont_vs_retr | n_cont | n_retr |
|---|---|---|---|---|---|---|
| n15_pre | 16.000 | 6.000 | 29.750 | 0.402 | 1026 | 791 |
| nb15_pre | 8.875 | 3.500 | 19.750 | 0.403 | 1026 | 791 |
| ns_pre | 20.000 | 9.000 | 28.000 | 0.410 | 1026 | 791 |
| top5_pre | 0.438 | 0.628 | 0.332 | 0.589 | 1026 | 791 |
| new_tok_share_trades_pre | 0.803 | 0.756 | 0.877 | 0.446 | 1026 | 791 |
| buy_share_pump | 0.725 | 0.715 | 0.685 | 0.550 | 1026 | 791 |
| ns_pump | 9.500 | 7.000 | 13.000 | 0.457 | 1026 | 791 |
| fresh_ds_usd_share_pump | 0.060 | 0.074 | 0.048 | 0.543 | 1026 | 791 |
| n15_pump | 12.500 | 6.500 | 15.000 | 0.474 | 1026 | 791 |
| med_a_pump | 195.550 | 276.450 | 193.393 | 0.515 | 1026 | 791 |
| nb15_pump | 8.000 | 4.500 | 8.750 | 0.486 | 1026 | 791 |
| buy_share_pre | 0.686 | 0.692 | 0.701 | 0.491 | 1026 | 791 |
| mean_buy_pump | 316.805 | 427.013 | 314.692 | 0.509 | 1018 | 788 |
| mean_buy_pre | 187.564 | 236.088 | 199.772 | 0.492 | 1017 | 789 |
| fresh_ds_usd_share_pre | 0.063 | 0.062 | 0.064 | 0.494 | 1026 | 791 |
| new_tok_share_trades_pump | 0.700 | 0.713 | 0.706 | 0.495 | 1026 | 791 |
| med_a_pre | 122.383 | 167.905 | 117.025 | 0.502 | 1026 | 791 |
| top5_pump | 0.567 | 0.667 | 0.551 | 0.499 | 1026 | 791 |

### (Outcome side, NOT usable in real time) trade behaviour in hour after trigger

| feature | med_continue | med_plateau | med_retrace | AUC_cont_vs_retr | n_cont | n_retr |
|---|---|---|---|---|---|---|
| top5_post1 | 0.507 | 0.837 | 0.652 | 0.380 | 1026 | 791 |
| mean_buy_post1 | 428.569 | 386.500 | 277.635 | 0.602 | 1016 | 778 |
| nb15_post1 | 5.250 | 1.750 | 3.500 | 0.589 | 1026 | 791 |
| buy_share_post1 | 0.656 | 0.626 | 0.598 | 0.582 | 1026 | 791 |
| n15_post1 | 9.125 | 3.000 | 6.750 | 0.578 | 1026 | 791 |
| fresh_ds_usd_share_post1 | 0.071 | 0.054 | 0.052 | 0.558 | 1026 | 791 |
| ns_post1 | 15.000 | 4.000 | 11.000 | 0.557 | 1026 | 791 |
| new_tok_share_trades_post1 | 0.652 | 0.600 | 0.643 | 0.520 | 1026 | 791 |

### Stability by trigger day

| ts_day | n | retrace | continue | med_r8 |
|---|---|---|---|---|
| 2026-06-10 | 159.000 | 0.409 | 0.233 | -0.308 |
| 2026-06-11 | 411.000 | 0.465 | 0.260 | -0.298 |
| 2026-06-12 | 448.000 | 0.400 | 0.288 | -0.319 |
| 2026-06-13 | 414.000 | 0.374 | 0.268 | -0.262 |
| 2026-06-14 | 469.000 | 0.426 | 0.264 | -0.306 |
| 2026-06-15 | 451.000 | 0.483 | 0.228 | -0.354 |
| 2026-06-16 | 400.000 | 0.463 | 0.275 | -0.346 |
| 2026-06-17 | 373.000 | 0.416 | 0.198 | -0.312 |
| 2026-06-18 | 319.000 | 0.442 | 0.238 | -0.304 |
| 2026-06-19 | 172.000 | 0.349 | 0.233 | -0.234 |
| 2026-06-20 | 408.000 | 0.385 | 0.235 | -0.238 |
| 2026-06-21 | 325.000 | 0.403 | 0.231 | -0.260 |
| 2026-06-22 | 383.000 | 0.358 | 0.285 | -0.206 |
| 2026-06-23 | 453.000 | 0.442 | 0.278 | -0.274 |
| 2026-06-24 | 487.000 | 0.390 | 0.279 | -0.267 |
| 2026-06-25 | 362.000 | 0.406 | 0.273 | -0.252 |
| 2026-06-26 | 346.000 | 0.379 | 0.275 | -0.282 |
| 2026-06-27 | 376.000 | 0.428 | 0.226 | -0.303 |
| 2026-06-28 | 443.000 | 0.449 | 0.251 | -0.331 |
| 2026-06-29 | 335.000 | 0.454 | 0.245 | -0.322 |

Interpretation: (a) age is the strongest candle-level discriminator - older tokens (median log-age 5.15 vs 4.59, i.e. ~3h vs ~1.6h) continue more; very young tokens (<1h) retrace (49% trap rate). (b) A fading last-candle volume (volume of trigger candle below the prior 2h average) is a warning but explains little by itself. (c) Pre-pump trade flow: crowded pre-pump books (high n trades, many buyers in the hour before) retrace; sparse, less-concentrated pre-flow (low n, top-5 share high = a few holders) continues. (d) Post-trigger behaviour discriminates much better (AUC 0.58-0.62 for mean buy size, unique buyers, buy share; top-5 share AUC 0.38): continuation = fresh demand with larger buys in the hour after - but that is not observable at the trigger. (e) GMGN snapshot features are stale and near-constant (rug_probability, lp_burned, has_twitter, dev_remaining all constant in these events) - uninformative.

## 4. Who sells into pumps

Roles use the wallet's first logged buy of that token relative to the event start. Sample: pump events with trade coverage until trigger+1h (2,862 events, 66k early wallet-event pairs).


### Share of sell USD in [event start, trigger+1h] by wallet role (role = timing of the wallet's first logged buy of that token)

| group | role | share_of_sell_usd | share_of_pumpphase_buy_usd | wallets | events |
|---|---|---|---|---|---|
| pump:ALL | early(pre-start) | 0.875 | 0.360 | 66389 | 2862 |
| pump:ALL | late(post-trigger) | 0.035 | 0.000 | 32949 | 2862 |
| pump:ALL | no_buy_logged | 0.004 | 0.000 | 662 | 2862 |
| pump:ALL | pump-phase buyer | 0.086 | 0.640 | 30100 | 2862 |
| pump:full_retrace | early(pre-start) | 0.882 | 0.446 | 39501 | 826 |
| pump:full_retrace | late(post-trigger) | 0.035 | 0.000 | 14569 | 826 |
| pump:full_retrace | no_buy_logged | 0.005 | 0.000 | 366 | 826 |
| pump:full_retrace | pump-phase buyer | 0.078 | 0.554 | 13552 | 826 |
| pump:continue | early(pre-start) | 0.768 | 0.305 | 40487 | 1070 |
| pump:continue | late(post-trigger) | 0.074 | 0.000 | 21867 | 1070 |
| pump:continue | no_buy_logged | 0.005 | 0.000 | 366 | 1070 |
| pump:continue | pump-phase buyer | 0.153 | 0.695 | 16355 | 1070 |
| pump:plateau | early(pre-start) | 0.882 | 0.211 | 31637 | 947 |
| pump:plateau | late(post-trigger) | 0.023 | 0.000 | 9088 | 947 |
| pump:plateau | no_buy_logged | 0.005 | 0.000 | 252 | 947 |
| pump:plateau | pump-phase buyer | 0.090 | 0.789 | 11937 | 947 |
| dump:ALL | early(pre-start) | 0.899 | 0.448 | 68061 | 2886 |
| dump:ALL | late(post-trigger) | 0.037 | 0.000 | 27258 | 2886 |
| dump:ALL | no_buy_logged | 0.006 | 0.000 | 647 | 2886 |
| dump:ALL | pump-phase buyer | 0.058 | 0.552 | 18812 | 2886 |

### Early buyers (first buy before event start): who exits

| group | early_wallet_event_pairs | sold_in_event_window | sold_in_window_or_post1 | sold_ge50pct_by_trig_plus1h | sold_ge90pct_by_trig_plus1h | usd_sold_to_usd_bought_pre |
|---|---|---|---|---|---|---|
| pump:ALL | 269936 | 0.078 | 0.123 | 0.307 | 0.202 | 0.888 |
| pump:full_retrace | 98693 | 0.078 | 0.122 | 0.302 | 0.194 | 0.833 |
| pump:continue | 102824 | 0.072 | 0.125 | 0.316 | 0.209 | 0.540 |
| pump:plateau | 66861 | 0.082 | 0.112 | 0.294 | 0.194 | 0.815 |
| dump:ALL | 300448 | 0.053 | 0.086 | 0.274 | 0.168 | 0.524 |

### Seller identity by token buy rank (rank by first buy time within the token)

| kind | group | share_sell_usd | share_pumpphase_buy_usd | sell_over_buy |
|---|---|---|---|---|
| pump | first-10 buyers of token | 0.057 | 0.007 | 17.504 |
| pump | buyers rank 11-50 | 0.223 | 0.078 | 6.533 |
| pump | rank >50 | 0.716 | 0.915 | 1.782 |
| pump | never logged buying | 0.004 | 0.000 | 458,133 |
| dump | first-10 buyers of token | 0.054 | 0.016 | 10.572 |
| dump | buyers rank 11-50 | 0.241 | 0.086 | 8.965 |
| dump | rank >50 | 0.699 | 0.897 | 2.500 |
| dump | never logged buying | 0.006 | 0.000 | 472,228 |

### GMGN wallet tags (smart_money/insider/normal/untagged) share of sells vs pump-phase buys

| kind | tag | share_sell_usd | share_pumpphase_buy_usd | wallets |
|---|---|---|---|---|
| pump | insider | 0.395 | 0.346 | 3398 |
| pump | normal | 0.042 | 0.098 | 3017 |
| pump | smart_money | 0.112 | 0.065 | 1184 |
| pump | untagged | 0.450 | 0.491 | 72713 |
| dump | insider | 0.278 | 0.300 | 3108 |
| dump | normal | 0.042 | 0.079 | 2893 |
| dump | smart_money | 0.112 | 0.102 | 1171 |
| dump | untagged | 0.568 | 0.518 | 69952 |

### Same-funder wallet clusters inside an event (wallet_funding coverage is thin)

| kind | events_with_cluster | events | wallets_with_funding_record | clustered_wallets | sell_share_clustered | buy_share_clustered |
|---|---|---|---|---|---|---|
| pump | 815 | 2862 | 922 | 273 | 0.004 | 0.005 |
| dump | 744 | 2886 | 877 | 281 | 0.005 | 0.003 |

### Net flow by phase (USD per event)

| group | events | net_flow_event_window | buy_over_sell_event | sell_over_buy_post |
|---|---|---|---|---|
| pump:ALL | 2862 | -48.724 | 0.997 | 1.663 |
| pump:full_retrace | 826 | 1,697 | 1.095 | 1.472 |
| pump:continue | 1070 | 4,289 | 1.422 | 0.959 |
| pump:plateau | 947 | -3,561 | 0.805 | 2.262 |
| dump:ALL | 2886 | -2,503 | 0.771 | 1.646 |

### Per-event medians by outcome class (sells in event window + 1h after trigger)

| cls | early_sell_share | sniper_sell_share | sell_buy_ratio | early_sold_frac_of_pre_buys | n_events |
|---|---|---|---|---|---|
| continue | 0.710 | 0.000 | 1.219 | 0.472 | 1042 |
| full_retrace | 0.737 | 0.000 | 1.024 | 0.321 | 785 |
| plateau | 0.802 | 0.000 | 0.765 | 0.425 | 880 |

Interpretation:
- 87% of sell USD in [S, T+1h] comes from wallets that bought before the pump started, although those wallets contributed only 36% of pump-phase buy USD; wallets that bought during the pump supply 8.6% of sells (and 64% of buys) - the pump-phase buyers are net holders at the end of the window. Late buyers (after trigger) sell 3.5%.
- Retracing pumps: early buyers 88% of sells, pump-phase buyers 7.8%; continuing pumps: early buyers 77%, pump-phase buyers 15% and late buyers 7.4% - i.e. in continuing pumps newer holders also take profit and distribution is broader; in retraces the pre-pump holders do all the selling while the pump-phase buyer is the bag holder.
- Only 7.8% of early wallet-event pairs sell during the pump window and 12% by trigger+1h, but 31% have sold >=50% of their pre-start buy USD by trigger+1h (20% >=90%). USD sold in the window per USD bought pre-start by early wallets: 0.83 (retrace) vs 0.54 (continue); the per-event median of the same ratio shows the opposite order (0.32 vs 0.47), so the signal is not robust. I do not claim this as a clean predictor.
- Token buy rank: first-10 buyers are 5.7% of sell USD but only 0.7% of pump-phase buy USD (sell/buy 17.5x); ranks 11-50 are 22% of sells vs 7.8% of pump buys. Ranks > 50 (the crowd) are 72% of sells and 91% of pump buys (1.8x). Dumps look the same (first-10 = 5.4% of sells).
- GMGN tags: insider-tagged wallets are 40% of sell USD vs 35% of buy USD in pumps (28% vs 30% in dumps); smart_money 11.2% of sells vs 6.5% of buys in pumps (11.2% vs 10.2% in dumps) - smart money is net seller into pumps. Normal wallets are 4% of sells, 10% of buys. Tag coverage (11.8k wallets) is limited, so 45-57% of USD is untagged.
- Same-funder clusters (wallet_funding, 15k edges) cover only 922 of the wallets, 273 clustered, <1% of sell USD: no usable evidence either way (data too thin). The wallets table has no cluster ids.
- Net flow in the event window is ~0 for pumps overall (-49 USD/event; buy/sell 1.00), positive for retraces (buy/sell 1.10) and strongest for continues (1.42, +4.3k USD/event), negative for plateaus (0.81). After the trigger sells exceed buys 1.66x in the following two hours.

## 5. Speed of dumps


### Dump events: duration (candles from window start to the trigger close) and depth

| nsteps | share of events | cum |
|---|---|---|
| 1 | 0.248 | 0.248 |
| 2 | 0.177 | 0.424 |
| 3 | 0.202 | 0.626 |
| 4 | 0.374 | 1.000 |

### Dump depth (min close within 3 candles after trigger / start price)

| index | count | mean | std | min | 10% | 25% | 50% | 75% | 90% | max |
|---|---|---|---|---|---|---|---|---|---|---|
| depth | 15,351 | 0.394 | 0.197 | 0.000 | 0.096 | 0.247 | 0.420 | 0.560 | 0.640 | 0.700 |

### Single-candle (<=15 min) dumps

| n | share | median close/open | share closing <=0.5x |
|---|---|---|---|
| 3801 | 0.248 | 0.480 | 0.533 |

### After a dump (2h): recovery

| share regaining >=80% of pre-dump price within 2h | share regaining >=50% | median return from trigger close to +2h | share further -30% from trigger close within 2h (close) | share ending +2h <=10% of pre-dump price | n |
|---|---|---|---|---|---|
| 0.244 | 0.619 | -0.129 | 0.389 | 0.113 | 12481 |

### Pumps: first candle (15m steps after peak candle) whose CLOSE is <=-30% from the peak close (n=7007, 3h window)

| dump_step | share | cum |
|---|---|---|
| 1.000 | 0.229 | 0.229 |
| 2.000 | 0.192 | 0.421 |
| 3.000 | 0.111 | 0.532 |
| 4.000 | 0.067 | 0.599 |
| 5.000 | 0.050 | 0.648 |
| 6.000 | 0.034 | 0.682 |
| 7.000 | 0.028 | 0.710 |
| 8.000 | 0.023 | 0.732 |
| 9.000 | 0.018 | 0.750 |
| 10.000 | 0.013 | 0.763 |
| 11.000 | 0.011 | 0.774 |
| 12.000 | 0.010 | 0.784 |
|  | 0.216 | 1.000 |

### Pump->dump linkage

| share of pumps followed by -30% from peak (close) within 1h | within 3h | median minutes peak->-30% (among those) | n |
|---|---|---|---|
| 0.599 | 0.784 | 30.000 | 7007 |

### Dumps: share that start within 2h after a pump peak (same token)

| share | n |
|---|---|
| 0.434 | 15351 |

Interpretation: a quarter of dump events are complete within one 15-min candle (median close at 0.48x open; 53% of those close <= 0.5x); 42% within two candles. Median depth of the move is -58% (first 3 candles after trigger, min close/start). A dump is rarely a clean one-way event: 24% of dumped tokens regain >= 80% of the pre-dump price within 2h, 62% regain >= 50% (dead-cat/rebound or a wick-heavy market; partly glitch candles) while 39% fall a further 30% from the trigger close. Pump -> dump: 60% of pumps give back 30% from the peak close within 1h, 78% within 3h; 43% of dump events start within 2h after a pump peak of the same token. At 15-min resolution a manual or even API-polling buyer cannot see intra-candle dynamics; the trade log carries no price, so second-level speed of the drop cannot be measured here.

## 6. Real-time detector (past data only)

Setup: at each pump trigger (close of the candle where +50% in <=1h is first reached), features known at that time: trigger multiple, candles in the move, last/previous candle return, upper wick, close position, volume in the move per 15m vs previous hour, last candle volume vs base and vs previous candle, token age, market cap at trigger (snapshot market cap x price ratio), pre-run, history length; plus 12 stale GMGN snapshot features (second model). Label TRAP = never closes >+10% above entry in the next 2h and ends 2h later <= -25% (41.8% of events; = "I bought the top"). Model: LightGBM (8 leaves, 150 rounds, strong regularisation); expanding-window daily refit on events with trigger+2h <= test-day start; test days 15-29 Jun (5,633 events). Trade-log features exist only for events inside the trade coverage (n=2,689 with trade features after filters) and are tested separately.


### Walk-forward (daily refit, expanding train, 2h purge) AUC for label TRAP = (no close >+10% above entry within 2h) & (-25% after 2h)

| model | n_oos | AUC_trap | AUC_vs_retrace_label | AUC_good_inverse |
|---|---|---|---|---|
| candle | 5633 | 0.601 | 0.634 | 0.521 |
| candle+snapshot | 5633 | 0.607 | 0.632 | 0.528 |

### Single-feature rules (no fitting; whole sample)

| rule | flag_rate | precision_trap | base_trap | recall_trap | good_lost | mean_r8_flagged | mean_r8_unflagged |
|---|---|---|---|---|---|---|---|
| vol_fading(vlast_vs_base<0) | 0.357 | 0.416 | 0.418 | 0.355 | 0.346 | -0.133 | -0.165 |
| young(age<60min) | 0.190 | 0.492 | 0.418 | 0.224 | 0.180 | -0.254 | -0.130 |
| blowoff(trig_mult>=2.5) | 0.181 | 0.493 | 0.418 | 0.214 | 0.204 | -0.208 | -0.142 |
| upper_wick>0.3 | 0.336 | 0.422 | 0.418 | 0.339 | 0.327 | -0.158 | -0.152 |
| vol_fading & young | 0.130 | 0.475 | 0.418 | 0.147 | 0.125 | -0.218 | -0.144 |

### Out-of-sample filter performance (pooled test days 2026-06-15..29), gross of fees/slippage

| model | thr | skip_rate | precision_trap | base_trap | recall_trap | good_continue_lost | mean_r8_all | mean_r8_kept | med_r8_all | med_r8_kept | gain_kept_minus_all_CI95 | mean_r4_kept | mean_r4_all |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| candle | 0.450 | 0.355 | 0.509 | 0.415 | 0.436 | 0.327 | -0.158 | -0.104 | -0.290 | -0.221 | [+0.035,+0.076] | -0.074 | -0.116 |
| candle | 0.550 | 0.114 | 0.594 | 0.415 | 0.163 | 0.083 | -0.158 | -0.133 | -0.290 | -0.261 | [+0.017,+0.035] | -0.096 | -0.116 |
| candle | 0.650 | 0.026 | 0.764 | 0.415 | 0.047 | 0.013 | -0.158 | -0.146 | -0.290 | -0.279 | [+0.009,+0.015] | -0.107 | -0.116 |
| candle+snapshot | 0.450 | 0.337 | 0.519 | 0.415 | 0.421 | 0.294 | -0.158 | -0.102 | -0.290 | -0.217 | [+0.038,+0.076] | -0.076 | -0.116 |
| candle+snapshot | 0.550 | 0.115 | 0.590 | 0.415 | 0.163 | 0.088 | -0.158 | -0.137 | -0.290 | -0.259 | [+0.009,+0.032] | -0.102 | -0.116 |
| candle+snapshot | 0.650 | 0.024 | 0.732 | 0.415 | 0.043 | 0.011 | -0.158 | -0.148 | -0.290 | -0.280 | [+0.008,+0.013] | -0.108 | -0.116 |

### Candle model, thr 0.55, by test block

| block | n | AUC | base_trap | skip | precision | recall | mean_r8_all | mean_r8_kept |
|---|---|---|---|---|---|---|---|---|
| 15-19 Jun | 1715 | 0.594 | 0.423 | 0.164 | 0.571 | 0.222 | -0.220 | -0.192 |
| 20-24 Jun | 2056 | 0.629 | 0.396 | 0.118 | 0.588 | 0.176 | -0.117 | -0.088 |
| 25-29 Jun | 1862 | 0.583 | 0.429 | 0.062 | 0.661 | 0.095 | -0.147 | -0.130 |

### Candle model OOS by risk quintile

| dec | n | mean_p | trap_rate | retrace | good | mean_r1h | mean_r2h | med_r2h |
|---|---|---|---|---|---|---|---|---|
| 0 | 1127 | 0.276 | 0.311 | 0.294 | 0.240 | -0.060 | -0.082 | -0.163 |
| 1 | 1126 | 0.340 | 0.355 | 0.337 | 0.282 | -0.064 | -0.079 | -0.202 |
| 2 | 1127 | 0.402 | 0.410 | 0.370 | 0.275 | -0.073 | -0.113 | -0.284 |
| 3 | 1126 | 0.470 | 0.449 | 0.496 | 0.257 | -0.138 | -0.195 | -0.387 |
| 4 | 1127 | 0.577 | 0.550 | 0.602 | 0.204 | -0.247 | -0.323 | -0.533 |

### LightGBM gain importance (all data, descriptive)

| index | gain share |
|---|---|
| log_kstart | 0.105 |
| log_mcap | 0.083 |
| log_vpump15 | 0.068 |
| trig_mult | 0.052 |
| liq_mcap | 0.051 |
| last_ret | 0.046 |
| vlast_vs_prev | 0.046 |
| s_seller_loss_ratio | 0.045 |
| cpos | 0.044 |
| s_bundler_ratio | 0.040 |
| log_age | 0.039 |
| s_crew_cohesion | 0.039 |

### Trade-log subset: train 10-19 Jun, test 20-29 Jun (events with full trade coverage)

| features | n_train | n_test | AUC_test | trap_rate_test |
|---|---|---|---|---|
| candle | 1005 | 1684 | 0.538 | 0.286 |
| trade-log only | 1005 | 1684 | 0.561 | 0.286 |
| candle+trade-log | 1005 | 1684 | 0.580 | 0.286 |

Interpretation:
- Discrimination is weak but stable: AUC 0.59/0.63/0.58 across three test blocks; adding GMGN snapshot adds nothing (0.607 vs 0.601). Risk quintiles are monotone: the riskiest 20% have a trap rate 55%, retrace rate 60%, mean 2h return -32% (median -53%); the safest 20% have trap 31%, mean 2h -8% (median -16%) - the safest quintile still loses.
- Filter trade-off at threshold 0.55: flags 11% of events, precision 59% (base 41.5%), catches only 16% of tops, loses 8% of good continuations; at 0.45: flags 36%, precision 51%, recall 44%, loses 33% of continuations. Mean 2h return of the kept buys improves by +3.5 to +7.6 pp (token-bootstrap CI), but from -15.8% to about -10%, which is still negative before fees and slippage (hundreds of bp round trip on thin pools). Single-feature rules are even weaker (young token <60 min: precision 49% vs 42%, recall 22%; blowoff >= 2.5x: precision 49%, recall 21%; upper-wick and fading volume ~ no skill).
- Descriptive importance: history length (how many candles before the move), market cap, volume in the move, trigger multiple, last-candle return and volume trend.
- Trade-log subset (static split 10-19 Jun / 20-29 Jun; n_train 1,005, n_test 1,684, test trap rate 28.6% vs 42% in the full sample - a different, more mature, selected population): candle-only AUC 0.54, trade-log-only 0.56, combined 0.58. Trade-flow features add a few AUC points but the sample is small and the improvement is within noise; treat as a hint.
- Conclusion: from past data alone one cannot reliably avoid the top. The structural reason is that (i) pump size is selected ex-post (a +50% trigger has 73% chance of being below the entry 2h later regardless of features), (ii) the information that separates continuation (new bigger buyers in the next hour) arrives after the decision.

## 7. Caveats

- 15-min candles: pumps/dumps entirely inside a candle are only seen when open/close span +50%/-30%; entry at trigger close is optimistic (no latency, no slippage, no tip, no fee). Real fills on thin pools at a +50% price would be much worse.
- Survivorship/selection: tokens enter the dataset when detected (graduated pump.fun tokens / GMGN trending) and candles exist only for a window after detection; forward outcomes require >=2h of later candles (86%); dead tokens drop out, making the retrace outcomes optimistic. Trade-log events are a further selected subset (tokens re-snapshotted later).
- The event definition favours micro-liquidity moves (median pump window volume above the $2k floor; 25th percentile pre-hour volume per 15 min a few $100). Sensitivity: floor $10k cuts events by 30-35% but not the qualitative conclusions (not re-run for all tables).
- Concentration/new-wallet metrics depend on the number of trades in the phase; 'new to token' is within the logged sample; 'fresh to dataset' means first appearance in this dataset (all 9.5M trades), not wallet age.
- A single 20-day regime, correlated events (one token can produce many events; 5,633 OOS events over ~2,000 tokens); CIs resampled by token only for the detector gains.
- The 'continue' class is defined with a look-ahead (it is an outcome), only used to describe, never as a feature.
