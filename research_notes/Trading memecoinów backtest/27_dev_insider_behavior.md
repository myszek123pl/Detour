# 27. Developer and insider behaviour: empirical analysis

Methods only. Addresses are never shown (devs referenced by sha256[:6] where needed). Scripts: /home/user/Detour/backtest/dev27_*.py (serial, serial2, build, tokfeat, panel, A, A2, A3, B). Intermediate tables are in the session scratchpad (w27/).

## 0. Data and the caveats that matter

| Dataset | What it is | Limits |
|---|---|---|
| solana_launches_public.csv (28,327 launches, 2026-07-27..09-25) | pump.fun launches **gated** at >=25 trades and >=~$15k mcap in first 15 min; 56 rows have no dev_wallet (dropped) | Survivor sample. "Serial dev" = repeat inside this gated sample only, so true serial-deployer share is understated. Outcome `multiple` = peak(15min..5h)/price_15, always >=1. |
| solana-memecoin-dataset (June 2026, 44,460 snapshots, 31,004 tokens) | GMGN snapshots (median 519 s after launch) + wallet-level trade log (~170 trades/token, window about -7..+6 min around capture, no price) + 15-min OHLCV (11,170 tokens) | Only first snapshot per token used. Wallet labels (insider/smart/normal) are GMGN tags. |

Data defects found:
- `max_return_1h/6h/24h/3d` are 0 for 99.9% of rows (unusable). Used `reaches_2x` (peak >=2x capture price; base 12.6% in days <06-20 vs 5.7% after) and `runner_peak_x` (71% equal 1.0, i.e. never traded above capture price) instead.
- Strong regime drift inside June: from 06-24 median liquidity went from ~$8k to ~$47k, bundler share of holders fell 0.30 -> 0.07, 2x rate fell 14% -> 4%. Pooled train/test AUCs are therefore inflated by Simpson mixing (test pooled AUC 0.85 vs train 0.62 for the same feature). All reported OOS AUCs are **within-day**, and rule lifts are computed against the base rate of the same period.
- Trade log covers ~47% of OHLCV volume in bars that have trades. wallet_funding covers only 2,105 funded wallets (4,921 funders; 4,597 funders feed a single wallet), and funding timestamps are mostly after the trades (median ~39 h later), so it is a static graph, not "funded just before buying" evidence.
- `cluster_max_pct`/`cluster_top3_pct` (median 0.83/0.97) are clearly shares of the clustered set, not of supply; `*_pct_holders` are shares of holder count, not supply. Supply-share is only known for dev_remaining_pct, top10_holder_pct, rat_position_pct.
- OHLCV downside labels exist only for tokens with >=2 bars (32% of tokens) = tokens that kept trading; "dump4" below is conditional on that.

## 1. Serial deployers (launch CSV)

- 22,950 distinct devs / 28,271 launches. 1,517 devs (6.6%) have >=2 launches and produce 24.1% of tokens; >=5 launches: 329 devs, 14.2% of tokens; >=10: 149 devs, 10.1%; >=20: 42 devs, 4.9%; top-20 devs 3.2%, top-100 8.2%. Max 174 launches by one dev. Ex-ante (time-consistent) share of launches by a dev with >=1 earlier launch: 14-22% per week.
- Re-launch gap (repeat launches): p5 47 min, median 30 h, p95 17 days. 349 repeat launches within 1 h.
- Raw outcomes look better for serial devs (one-off P(>=2x)=26.4%, P(>=5x)=4.3%, P(>=10x)=1.2%; 10+ launches: 29.6%, 8.2%, 3.0%). **This is a composition effect**: one-offs are 65% non-low-price tokens (price_15>=1e-4, many apparently other launchpads/odd creators) vs 17% for 5+ devs. Restricting to pump-suffix tokens with price_15<1e-4:

| group | n | P(>=2x) | P(>=5x) | P(>=10x) | median mult | P(mult<1.1) |
|---|---|---|---|---|---|---|
| one-off | 6,144 | 31.3%±1.2 | 7.8% | 2.6% | 1.455 | 21.1% |
| 2-4 launches | 1,368 | 32.0%±2.5 | 9.7% | 3.4% | 1.463 | 24.8% |
| 5+ launches | 2,669 | 31.1%±1.8 | 8.5% | 3.1% | 1.434 | 23.7% |

  Ex-ante by prior launch count (same band): 0 prior 31.9%, 1-2 32.4%, 3-9 28.1%, 10+ 29.4% for 2x. Tail (5x) is slightly higher for serial (7.8% -> 9.0% at 3-9 priors, CI overlap). Verdict: **no edge from "serial dev" per se**; a slight fatter right tail and ~3pp more flat launches.
- Dev history as predictor: prior hit rate over >=3 prior launches (all gated data) gives P(2x) 21% (zero hits) / 28-31% (hit rate 0.15-0.5); the OOS test (dev stats from first half of window, tested on second half) gives: unseen dev 24.3%, seen >=5 launches 26.5%, seen >=5 with zero prior 2x 9.4% (n=32, tiny). Logistic regression on [log prior count, prior hit rate] gives OOS AUC **0.516** (time split 60/40); early-trading features (trades_5, buy/sell vol ratio, avg size) give 0.552; combining adds nothing (0.555). Previous launch flat (<1.2x): next launch P(2x) 25.8%; previous 5x+: 34.9% (n=430, P(5x) 10.7%), weak momentum, not tradable alone.
- Serial devs' launches carry 4x lower buy/sell volume ratio at 5 min (1.2 vs 5.8 median) and 2-3x more trades, i.e. more bot/wash-like flow, consistent with prior notes on wash trading.

## 2. Dev and insider holdings (June snapshots, N=31k)

- dev_remaining_pct (share of supply): median 0; >0: 25.6%, >1%: 21.4%, >5%: 11.9%, >20%: 4.4% (a mass near 0.99, 4.1%: dev holds ~all).
- top10_holder_pct: median 16%, p75 23%, p90 41%.
- Share of holders flagged: insider median 0.2%, p75 22%, p90 45%; >40% insiders 12%; bundler p75 37%, p90 63%; >40% bundlers 24%. sniper_count median 2 (p90 22).
- Trade-flow share before capture (first-10 buyers in log): 47% of window buy$ (median), first-25: 66%; insider-labeled wallets: median 12%, mean 37%, p90 97% of buy$; smart-money 2% mean; funder-cluster wallets (>=2 funded buyers sharing a funder, found in 6,510 tokens = 21%, 39.8k token-funder groups): mean 9.2% of buy$, p90 14%.
- Cohort sell behaviour before capture: median sell$/buy$ = 0 for insider and cluster cohorts, 0.02 for first-10 buyers, 0.10 for first-25, 0.30 for smart money. Most insiders had not sold by capture (insider_holding_ratio median 1.0).

## 3. Do holdings/cohorts predict outcomes? (time split: train <06-20, test >=06-20; within-day AUC)

Outcome "dump4" = min low over first 4 post-capture 15-min bars <= -50% of first-bar open (base 38%, requires >=2 bars). Upside = reaches_2x.

| feature | AUC 2x train/test | AUC dump4 train/test |
|---|---|---|
| bundler_pct_holders | 0.70 / 0.86 | 0.51 / 0.51 |
| top10_holder_pct | 0.62 / 0.85 | 0.55 / 0.54 |
| insider_pct_holders | 0.57 / 0.84 | 0.45 / 0.49 |
| dev_remaining_pct | 0.50 / 0.47 | 0.53 / 0.51 |
| sniper_count | 0.46 / 0.55 | 0.59 / 0.59 |
| first-10 buyer sell/buy | 0.59 / 0.81 | 0.41 / 0.45 |
| window sell/buy (all) | 0.58 / 0.83 | 0.31 / 0.35 |

Interpretation caution: the 2x AUCs for bundler/insider/top10 are mostly "token is alive and bot-traded" detection. Tokens with 0 bundlers/insiders/low top10 almost never trade again (2x 0.5-2%; runner_peak=1.0 for 96-99%), and tokens with 10-70% bundlers show 20-22% 2x rates (3.4-3.9x lift in test). These are survival/activity filters, not evidence that insiders help price. Above ~70% insiders (or top10>60%) the 2x rate falls back and dumps rise.

Holder-structure bins (test period, base 2x 5.7%, dump4 38.4%):
- dev_remaining >20%: dump4 **69% train / 62% test** (n_labeled 188/128) vs 36-38% base; the most stable downside flag. 2x rate inconsistent (6% train, 10% test): dev holding is a volatility marker, not a direction marker. 5-20%: 2x lift 1.8 train / 0.24 test (unstable).
- sniper_count >15: dump4 51-55% in both periods, 2x lift 2.1-5.6 (alive tokens with many snipers: high variance both ways). sniper_count 2-6: 2x lift 0.3, dump4 45-63%.
- top10 >60%: dump4 51% train, 45% test; 2x lift 0.7 / 2.1.
- insider_pct_holders >50%: dump4 17-30% (lower; insiders already hold, little sell pressure) but 2x lift near 1.
- Early-buyer (first 10) sell/buy before capture >0.5: 2x lift 1.5 train / 3.0-3.3 test, dump4 30-38% (they have taken profit into strength and the token kept going). Nothing says early selling predicts dump.

Multivariate (HistGradientBoosting, train first 11 days, test last 9, 21 features): dump4 within-day AUC 0.71; top 9% by score precision 62% (n=407) and top 5% 60% vs base 38%. Dominant feature: window sell/buy ratio (perm imp 0.08), others <0.015. 2x within-day AUC 0.87 (driven by bundler share and smart_money share = activity); top 9% precision 27% vs 5.7% base (n=1,848). Treat as regime-fragile.

## 4. Rule hit rates (rules chosen by quantile on train, measured on test)

| rule (flag => dump4) | train p (n) | test p (n) | base tr/te | lift test |
|---|---|---|---|---|
| dev_remaining_pct > 8.7% | 60.8% (273) | 49.2% (189) | 37.8/38.4 | 1.28 |
| top10 > 76% | 54.9% (273) | 50.6% (172) | | 1.32 |
| sniper_count > 20 | 54.3% (536) | 54.6% (511) | | 1.42 |
| cluster_max_pct > 0.975 | 53.7% (546) | 55.7% (183) | | 1.45 |
| window sell/buy < 0.046 (nobody sold) | 61.2% (273) | 47.0% (164) | | 1.22 |
| window sell/buy > 0.66 (flow balanced, sells happening) | 16.4% (1,636) | 18.3% (1,219) | | 0.48 (safer) |
| insider_pct_holders > 52% | 22.3% (546) | 26.0% (489) | | 0.68 (safer) |

Recall is low (each flag covers 1-7% of labeled tokens); these are exclusion filters or a minor sizing input, with 1.2-1.5x lift decaying train->test. Simple conjunctions did not hold up in the scan.

## 5. Event study: does insider/cluster selling precede dumps?

Design: 15-min bar panel (60.7k bars with trades, 5,070 tokens). Event = cohort net-sells >=$300 in bar j (sell>buy); control = bars of same token set with cohort sells <$300; effect stratified by bar index since first bar; log returns winsorized at +-1.5; bootstrap by token. Next-bar return "fwd1" = close(j+1)/close(j).

| cohort | events (tokens) | prev bar | same bar | fwd1 | fwd2 | P(next bar <= -30%) diff |
|---|---|---|---|---|---|---|
| insider-labeled | 5,908 (1,667) | -0.060 | -0.040 | -0.020 [-0.030,-0.008] | -0.001 | +3.4pp (train +2.9, test +3.9) |
| smart-money | 8,213 (1,200) | +0.002 | +0.004 | -0.032 [-0.045,-0.020] | -0.094 | +4.5pp (4.5 / 4.1) |
| funder cluster (>=2 shared-funder buyers) | 649 (265) | +0.005 | +0.016 | -0.051 [-0.087,-0.017] | -0.222 | +10.7pp (12.7 / 5.5) |
| first-10 buyers | 4,058 (1,677) | +0.039 | +0.026 | -0.013 [-0.029,-0.002] | -0.051 | +2.6pp (3.2 / 1.8) |
| all wallets (reference) | 16,613 (3,020) | -0.092 | -0.089 | -0.049 | -0.039 | +4.2pp |

Findings: (a) funder-cluster selling is the clearest lead: price still rising or flat while they sell, then -5% next bar and -22% two bars later, 10.7pp more likely to drop >=30% in the next 15 min (train 12.7pp, test 5.5pp: same sign, smaller OOS; only 237 test events). (b) Insider/smart-money selling is a weak negative lead (-2 to -3% next bar, +3-4pp drop probability, stable sign OOS). (c) All-wallet selling carries the same size effect, so most of insider selling is not information beyond general selling; insider-labeled selling is mostly reactive (prior bar -6%). (d) Large events ($>=2000) by insiders/first-10 buyers show **positive** next-bar returns (+3 to +6% fwd1, drop diff -2 to -4pp): big insider sells happen into rising demand and did not precede dumps within 30 min. Funder-cluster large events are too few (161/62).
Peak-aligned (tokens with >=6 bars, peak bar by OHLCV high; median peak is only 0.9 bars after capture): insider sell share of its own flow rises from 0.63-0.68 (bars -3,-2) to 0.79 (-1) and 0.82 at peak bar, and 0.69-0.70 after; smart-money 0.60 -> 0.87 at peak; cluster 0.75 -> 0.92 at peak; first-10 buyers sell 84-95% of their flow in all bars (they are already net sellers). So cohort selling peaks with the price peak, with one-bar lead for the cluster/smart groups; not an earlier, separable signal. Resolution limit: 15-min bars, so anything faster than ~15 min is invisible.

## 6. Practical detection rules (summary)

1. Hard exclude / size down: dev_remaining >20% (dump4 62-69%, 1.6-1.8x base, stable both periods); top10 >60-75%; sniper_count >20 with falling flow.
2. In-trade exit trigger: >=2 shared-funder wallets net-selling in a 15-min bar: expect -5% next bar, ~+11pp odds of a >=30% drop (OOS +5.5pp, small n); insider/smart-money net selling alone only +3-4pp.
3. Do not use serial-dev status or dev's prior hit rate as a signal (AUC 0.52). Fast re-launch (<1 h) is also neutral.
4. Do not treat high insider/bundler share as bullish or bearish by itself: it proxies for activity; 2x lift disappears once the token's activity is controlled for and flips for >70% insider share.
5. Everything is regime-dependent (June: bundler share and liquidity shifted mid-month); re-estimate thresholds on rolling windows and compare against same-period base rates.

Open items: no full launch-time trade data (cannot compute dev sells at t0), no dev wallet in the June set (dev_remaining only a snapshot), launch CSV has no holder fields, so serial-dev x insider interaction cannot be tested; the funder graph is too sparse (2,105 wallets) for a general cluster detector.
