# 23. Does WHEN you enter matter? Entry-timing analysis

Scripts: `/home/user/Detour/backtest/entry_timing.py` (run `python3 -I entry_timing.py x`; full output kept in scratchpad).
Data: `backtest/out/sim_results.parquet` (9,686 tokens, snapshots 2026-06-10..06-29; 2 glitch tokens with peak_mult>=1000 dropped -> N=9,684; train <2026-06-24 n=7,589, test >=06-24 n=2,095). Secondary dataset: `solana_launches_public.csv` (28,327 launches, 2026-07-27..09-25), used only for sanity checks on hour/day (see section 8).

## 0. Method and definitions

- Net EV per $1 staked, same cost model as `backtest.py`/`filters.py`: `gross*(1-fee-impact)^2 - 0.30*(1+n_sells)/pos - 1`, fee 1.25%/side, impact = 2*pos/L, position $200 (also $50 shown as `EV_B50`).
- **Conservative liquidity** `L = min(liquidity_usd, 0.4*market_cap_usd)` (floor 1; impact capped at 90%). Median L = $3.7k (vs $8.6k raw liquidity). This makes cost strongly dependent on market cap, which matters for every conclusion below.
- Deciles by qcut on the full sample; train/test columns use the *same* bucket edges. P(2x) = share with `peak_mult>=2` (price touched 2x within 24h, gross, not net). "mdd" = median `mdd_from_peak` (max peak-to-trough drawdown of the token path after entry, as stored in the parquet). "med" = median net return of ladder_B.
- Stability tools: bootstrap 95% CI of decile EV, train-vs-test Spearman of bucket EVs (10 buckets, so rho>0.7 is the bar), token-level Spearman by period, placebo permutation of spread (max-min decile EV) and rank-OLS with all timing variables jointly.
- Baseline (all tokens, $200): EV ladder_B -0.298, tight_D -0.288, hold_24h -0.402, scalp_E -0.301, runner_F -0.286. P(2x)=21.6%. Median net ladder_B -0.54. Train -0.292 / test -0.320. **Everything is deeply negative before any timing split.**

## 1. Time since launch (minutes at snapshot; 90% of tokens < 25 min, median 5.7 min)

| decile | age min | n | P(2x) | EV ladder_B | EV tight_D | EV hold_24h | mdd med | med B | train B | test B |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.2-1.8 | 963 | .212 | -.283 | -.314 | -.534 | .74 | -.54 | -.278 | -.325 (n=85) |
| 2 | 1.8-2.6 | 964 | .193 | -.348 | -.312 | -.435 | .71 | -.54 | -.346 | -.378 (52) |
| 3 | 2.6-3.4 | 964 | .187 | -.315 | -.308 | -.479 | .70 | -.53 | -.316 | -.289 (43) |
| 4 | 3.4-4.4 | 950 | .206 | -.273 | -.276 | -.400 | .71 | -.53 | -.277 | -.187 (43) |
| 5 | 4.4-5.7 | 960 | .206 | -.284 | -.271 | -.377 | .70 | -.54 | -.285 | -.273 (72) |
| 6 | 5.7-7.7 | 958 | .207 | -.291 | -.266 | -.372 | .69 | -.54 | -.293 | -.277 (113) |
| 7 | 7.7-10.9 | 957 | .233 | -.262 | -.249 | -.343 | .68 | -.53 | -.262 | -.260 (163) |
| 8 | 10.9-15.7 | 959 | .227 | -.303 | -.285 | -.341 | .67 | -.54 | -.273 | -.357 (342) |
| 9 | 15.7-25.2 | 960 | .245 | -.302 | -.282 | -.417 | .64 | -.55 | -.270 | -.326 (552) |
| 10 | 25.2-1429 | 957 | .243 | -.306 | -.303 | -.314 | .59 | -.57 | -.268 | -.327 (609) |

Findings: EV is flat (-0.26 to -0.35), bucket CIs overlap almost completely; placebo test p=0.13 (spread 0.087 vs 95th-pct placebo 0.097) => **indistinguishable from noise**. Train-vs-test bucket correlation rho=0.14 (ladder_B), -0.04 (tight_D). Token-level Spearman(age, net B): -0.011 all, +0.026 train, **-0.106 test** (sign flips). The test period is also composed differently (test snapshots are mostly 10+ min old, train mostly <10 min), so age is partly a period proxy.
Mild real pattern: older entry -> higher P(2x) (.21 -> .245), smaller drawdown (.74 -> .59), higher median final multiple for hold; but ladder_B net does not improve because the 50% stop/exits still lose. Hold_24h improves with age (-0.53 -> -0.31) in-sample only (bucket rho train/test 0.72 for hold, one of the few consistent ones, but all negative and driven by fewer rugs surviving to the snapshot, i.e. survivorship: older snapshot = token already survived).
After controlling for L, age adds nothing (rank-OLS coef -0.002, t=-0.1 all; train +0.005; test +0.136 t=2.7 - again period-specific). In high-L tokens the age bins are: <2 min -0.199, 2-5 -0.071, 5-10 -0.030, 10-30 -0.049, >30 -0.153 (CIs: first and last clearly worse than 5-30 min, n=480/142) - a weak "avoid the first 2 min" signal, plausibly bots/snipers at first minutes; not tested out-of-sample per bin.

## 2. Market cap at entry (USD) - the dominant "timing" variable, but mostly a cost artefact

| decile | mcap | n | median L | P(2x) | EV B | EV D | EV hold | mdd | train B | test B |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 1.3-3.9k | 969 | 1.4k | .093 | **-.565** | -.570 | -.602 | .44 | -.560 | -.585 |
| 2 | 3.9-5.1k | 968 | 1.8k | .129 | -.491 | -.475 | -.537 | .57 | -.483 | -.522 |
| 3 | 5.1-6.5k | 968 | 2.3k | .162 | -.430 | -.406 | -.449 | .66 | -.436 | -.406 |
| 4 | 6.5-8.2k | 969 | 2.9k | .202 | -.354 | -.323 | -.481 | .72 | -.361 | -.323 |
| 5 | 8.2-10.6k | 968 | 3.7k | .216 | -.332 | -.314 | -.407 | .78 | -.333 | -.328 |
| 6 | 10.6-14.3k | 968 | 4.9k | .258 | -.200 | -.222 | -.316 | .81 | -.176 | -.291 |
| 7 | 14.3-20.5k | 969 | 6.7k | .273 | -.171 | -.161 | -.173 | .78 | -.140 | -.269 |
| 8 | 20.5-31.8k | 968 | 10.3k | .278 | **-.088** | -.086 | -.214 | .72 | -.049 | -.251 |
| 9 | 31.8-66.2k | 968 | 14.1k | .267 | -.161 | -.127 | -.276 | .80 | -.169 | -.135 |
| 10 | 66k-1.2bn | 969 | 18.5k | .281 | -.186 | -.198 | -.566 | .76 | -.197 | -.156 |

- Train-vs-test bucket Spearman 0.85 (B), 0.85 (D), 0.83 (hold); token-level Spearman(mcap, net B) +0.27 train / +0.39 test; placebo p<0.003. **Robust and monotone up to ~$30k, then flat.**
- Gross (pre-cost) mean ladder_B multiple by decile: .92 .88 .88 .90 .87 .98 .97 1.02 .96 1.01 - the gross edge is basically 0.87-1.02 everywhere. Most of the -0.57 vs -0.09 spread is **cost**: L ~ 0.4*mcap makes impact = 2*200/L = 30% round-trip at $4k mcap. At $50 position EV_B50 is -0.245 (D1) vs -0.037 (D8): the gradient shrinks 10x, confirming it is mostly impact. The residual real effect: P(2x) rises from 9% to 28% with mcap (tokens priced under ~$5k are mostly pre-traction or dead: mdd .44, medFinal .85 meaning many are flat-dead).
- Sweet spot (best bucket): mcap $20-32k, EV_B -0.088 (CI -0.129..-0.048), still negative; test -0.251 (n=183) - the "best bucket" regresses by -0.2 out of sample (winner's curse; train->test drop in D6-D8 is large, -0.05 -> -0.25), while the worst bucket (<$4k) is stable at -0.56/-0.585. **Avoiding mcap <$6k is robust; picking $20-30k is not.**
- Simple rule check: mcap<5k n=1880 EV -0.529 (train -0.522, test -0.558); 5-20k -0.301; >20k -0.144 (train -0.135, test -0.175); >100k -0.137 (hold -0.56 because those have 0.02 median final multiple: rugs/dumps).

## 3. Momentum at entry: price_change_1h (chasing vs dip)

| decile | pc1h % | n | medL | P(2x) | EV B | EV D | EV hold | mdd | train B | test B |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | -95..-9 | 969 | 5.8k | .224 | -.338 | -.312 | -.523 | .74 | -.325 | -.359 |
| 2 | -9..21 | 968 | 9.4k | .204 | -.348 | -.305 | -.471 | .68 | -.357 | -.321 |
| 3 | 21..49 | 969 | 2.0k | .166 | -.325 | -.337 | -.413 | .48 | -.320 | -.344 |
| 4 | 49..78 | 969 | 1.8k | .198 | -.348 | -.350 | -.443 | .52 | -.329 | -.421 |
| 5 | 78..111 | 979 | 2.0k | .205 | -.305 | -.305 | -.423 | .59 | -.306 | -.301 |
| 6 | 112..154 | 961 | 2.3k | .206 | -.303 | -.287 | -.357 | .64 | -.303 | -.302 |
| 7 | 155..220 | 973 | 2.8k | .247 | -.279 | -.273 | -.373 | .69 | -.281 | -.269 |
| 8 | 221..310 | 960 | 3.4k | .227 | -.285 | -.277 | -.366 | .75 | -.280 | -.311 |
| 9 | 311..478 | 968 | 4.4k | .257 | -.233 | -.234 | -.339 | .79 | -.231 | -.239 |
| 10 | 480..972k | 968 | 6.7k | .225 | -.213 | -.200 | -.312 | .85 | -.194 | -.282 |

- Weak positive monotone trend ("chasing" is slightly *less bad*, not better): token Spearman +0.11 (train .12, test .05); bucket rho 0.79/0.76 for B/D, 0.36 for hold. Placebo p<0.003 for the spread (0.135) but it is small and shrinks in test (0.051) and in a rank-OLS with controls: coef +0.074 (t=4.2) in train, **-0.012 (t=-0.3) in test**.
- Dips (pc1h < -50%): n=387, EV_B -0.398 (train -0.372, test -0.428), hold -0.578, P(2x) .191 - the worst momentum group; falling knives do not mean-revert at this cost level. Flat (-50..+50): -0.328. Chase >100%: -0.265 (train -0.261, test -0.282); >500%: n=892, -0.210 (train -0.185, **test -0.299**); >1000%: n=113, -0.026 (train +0.021, test -0.210, CI wide -0.43..+0.08).
- High momentum has higher mdd (.85 vs .48) - bigger swings, so the 50% stop is hit more often, but the right tail (P(2x) 23-26%) pays for it.
- Interaction with L: the Q3 momentum bin x highest L tercile shows +0.151 train, +0.013 test (n small) - noise-level.
- Conclusion: "don't buy dips, mild preference for strong momentum" is directionally consistent train/test for the dip side only. No positive-EV momentum bucket.

## 4. Buy/sell pressure

Ratio A = buy_usd_1h / sell_usd_1h (computed); ratio B = `trade_buy_sell_ratio` (count based, capped at 99).

A (USD ratio):
| decile | range | n | medL | P(2x) | EV B | EV D | mdd | train B | test B |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 0-1.09 | 969 | 7.3k | .256 | **-.037** | -.089 | .51 | -.013 | -.182 (n=139) |
| 2 | 1.09-1.25 | 968 | 1.7k | .164 | -.346 | -.361 | .51 | -.319 | -.484 |
| 3 | 1.25-1.44 | 968 | 2.0k | .167 | -.398 | -.390 | .60 | -.394 | -.412 |
| 4 | 1.44-1.68 | 969 | 2.4k | .186 | -.401 | -.387 | .66 | -.404 | -.387 |
| 5 | 1.68-2.06 | 968 | 2.9k | .199 | -.356 | -.323 | .70 | -.360 | -.342 |
| 6 | 2.06-2.58 | 968 | 4.0k | .259 | -.256 | -.260 | .74 | -.241 | -.294 |
| 7 | 2.58-3.29 | 969 | 5.5k | .253 | -.300 | -.260 | .77 | -.302 | -.295 |
| 8 | 3.29-4.40 | 968 | 5.4k | .233 | -.322 | -.276 | .77 | -.327 | -.307 |
| 9 | 4.4-7.1 | 968 | 5.4k | .226 | -.327 | -.283 | .78 | -.338 | -.285 |
| 10 | 7.1-59k | 969 | 4.8k | .215 | -.235 | -.253 | .78 | -.241 | -.208 |

B (count ratio): D1-D2 (<1.5) are the worst: EV -0.425/-0.443 (P(2x) 12-13%, stable train/test: -0.425/-0.425 and -0.434/-0.471); EV rises to ~-0.28 at 1.8-4 and best -0.173 at 4.1-5.05 and -0.19 at >8; train-vs-test bucket rho 0.89 (B and D). Token Spearman +0.155 (train .156, test .159) - **the only variable besides mcap/L with a consistent, same-size token-level effect in both periods**. Low buy-dominance (ratio <1.5) = low demand = worst; but ratio is correlated with L (rho 0.29).
Net flow (USD) is essentially a size proxy: EV -0.465 (D1) -> -0.159/-0.166 (D8-D10), rho 0.88/0.98 train-vs-test, token Spearman 0.29/0.30 - same story as mcap/L.

Odd decile A-D1 (sell >= buy over the last hour, high liquidity, medFinal 0.99): EV -0.037 all (train -0.013, **test -0.182**, CI test -0.28..-0.08). It is a distinct population (median mcap $19.7k, L $7.3k, liq/mcap 1.17 vs .93) - "old, consolidating" tokens that hold price; gross multiple 1.22. Intersected with L>7k: n=499 EV **+0.198** (train +0.226 n=426; test +0.031 n=73, CI -0.09..+0.17) - the only positive-EV cell in this whole study, but it was found post hoc (one of ~100 cells), the test estimate is statistically zero, and test sell>buy tokens (n=62) have -0.170. Treat as a hypothesis, not an edge.
Rank-OLS: bsr coefficient -0.293 (t=-16) in train, -0.126 (t=-2.7) test: sign opposite to the count-ratio, driven entirely by that D1 population -> non-monotone, unreliable as a linear signal.

## 5. Liquidity/cost control (the confounder)

L deciles (conservative): EV_B -.570 (L<1.5k), -.481, -.463, -.392, -.337, -.270, -.205, -.106, -.093, **-.060** (L>14.3k, P(2x) .336). Train-vs-test rho 0.98; token Spearman 0.44 in both periods. Test for the top bucket: -0.050 (n=309) vs train -0.065 - stable. This is the strongest and most robust predictor in the data, and it is mechanical (cost model: impact=2*pos/L; the real uncertainty is whether real liquidity is as low as 0.4*mcap suggests; the raw liquidity column gives much better numbers, so these tables are a *lower bound*).
Within-L-tercile checks (EV ladder_B): mcap quartile effect vanishes or becomes non-monotone (L_low: -.511, -.395, -.294, -.469); age effect has no pattern (L_high: -.159, -.058, -.069, -.100); pc1h pattern is non-monotone (L_high: -.200, +.001, +.151, -.164; test -.232, -.073, +.013, -.230). Even at the highest-L tercile no timing variable gives a positive, train/test-stable EV.

## 6. Hour of day and day of week (UTC; entry time = snapshot time)

Hour (n 288-503 per hour, test n 44-125 per hour):
- EV_B by hour ranges -0.217 (22h) ... -0.392 (11h); best: 22h -0.217, 21h -0.228, 4-5h -0.235/-0.245, 20h -0.255; worst: 11h -0.392, 6h -0.370, 8h -0.349. P(2x) range .166 (11h) - .261 (16h).
- Per-hour train->test: 22h -0.204 -> -0.284; 21h -0.246 -> -0.160; 4h -0.243 -> -0.216; 11h -0.385 -> -0.419; 6h -0.357 -> -0.445. Train-vs-test hour rho 0.35 (B), 0.22 (D), -0.14 (hold). Token Spearman 0.011/0.035. Bootstrap CIs per hour are about +/-0.06, the best-vs-worst spread (0.175) is the size expected from the maximum of 24 noisy means; the 22h CI (-0.327..-0.045) overlaps almost every other hour.
- 8h blocks: 00-07 -0.291 (train -0.282, test -0.322), 08-15 -0.324 (-0.314/-0.359), 16-23 -0.279 (-0.279/-0.278). Differences 0.04, within noise. Hours 21-22 combined: -0.223 (n=937; test -0.211 n=179, CI test -0.31..-0.11) is ~7pp better than average and holds in both periods, but it is small, post hoc and still negative. Hour 11 combined -0.392, test -0.419 (n=98): consistently worst, again post hoc.
Day of week: EV_B Mon -.311, Tue -.288, Wed -.297, Thu -.282, Fri -.347, Sat -.291, Sun -.276; weekend -0.283 vs weekday -0.304; P(2x) .197-.226. Train/test rho 0.31/-0.37/-0.89 (hold) => no stable signal. Calendar date: EV_B day by day -0.395 (Jun 10) ... -0.225 (Jun 20), token Spearman ~0 - day-to-day regime noise is larger (+/-0.08) than any hour effect.

## 7. Multivariate and multiple-testing summary

Rank-OLS on net ladder_B (clipped at 99th pct), t-values: train: age +0.3, mcap +1.6, pc1h +4.1, bsr -16, L (strong, positive); test: age +2.7, mcap +1.0, pc1h -0.3, bsr -2.7. Placebo permutation (spread of 10 decile means): age p=0.13 (n.s.), mcap p<0.003, pc1h p<0.003, bsr p<0.003, but only mcap/L (and count buy-sell ratio) keep the same sign and size in test.

Robustness scorecard (token-level effect on net EV; same sign & magnitude train vs test?):
| factor | in-sample effect | out-of-sample | verdict |
|---|---|---|---|
| L / market cap (size, cost) | EV -0.57 -> -0.06 | rho 0.85-0.98, Spearman .27/.39 | ROBUST, but mostly mechanical cost |
| count buy/sell ratio | -0.44 (low) -> -0.17 | rho 0.89, Spearman .156/.159 | Robust, modest (about 0.1-0.2) |
| price_change_1h | dips -0.40, chase -0.21 | .12 -> .05, OLS t 4.1 -> -0.3 | Weak; dip-avoid holds, chase-prefer does not |
| time since launch | flat | sign flips (+.03 / -.11) | None |
| hour of day | +/-0.08 | rho 0.35 | None (noise-sized); 21-22h/11h tentative |
| day of week | +/-0.03 | rho 0.3, -0.37 | None |
| sell>buy & high L | +0.198 | +0.031 (n=73) | Post hoc hypothesis |

## 8. Cross-check on the launches CSV (entry fixed at minute 15 after launch)

28,327 launches; `multiple = best_price_5h/price_15` (peak after minute 15, i.e. a gross *ceiling*, not tradeable; P(multiple>=2) 27.4%, median 1.42). No costs, so only relative comparisons:
- Hour of day (launch hour UTC): P(2x) by hour .243-.299, n 920-1429 per hour (SE ~1.3pp); the spread of 5.6pp is what 24 noisy proportions give; mean multiple 2.02-2.76 driven by outliers (19h 2.76 due to a few 100x+). Slight low at 14-15 and 23-00 and high at 3-8 UTC (same direction as snapshot data that 4-5h hours looked good, 11h/14h bad - weak agreement, not significant). Day of week: P(2x) .248 (Sun) - .284 (Tue); n 3.6-4.3k, SE .7pp -> Sun/Fri lower is borderline, trivial in size.
- Calendar drift is larger than hour effect: P(2x) .30-.37 in late July/Aug vs ~.14-.25 in early Sep (e.g. Sep 3-5 .14-.19) and back to .30-.32 on Sep 21-24. Regime/time-period dominates hour-of-day, which also explains why train and test differ.
- Entry-state variables at minute 15: price level quintiles (P(2x) .31/.32/.33 for low, .19/.21 for the highest prices - price level is token-supply specific, not meaningful), 5-to-15 min growth quintiles .175 -> .342 (strong momentum -> higher P(2x), median 1.29 -> 1.57), buy/sell count ratio quintiles .314 -> .186 (opposite sign to the snapshot data: high buy ratio = *lower* P(2x), consistent with "buy dominance late = chasing").
- Caveat: no costs, no drawdown, peak window known ex post. Do not read as net-EV evidence. It does say momentum 5->15 min is positively related to reaching 2x and extreme buy dominance is not.

## 9. Conclusions

1. **Entry timing does not rescue the strategies.** Across every one of 5 variables x 10 buckets (about 50 deciles) plus hour/day, no bucket has a robust positive net EV: best bucket EV (-0.037 for sell>buy, -0.060 for L>14k, -0.088 for mcap $20-32k) is still negative, and median net return is -0.52..-0.57 in almost every bucket (the stop-loss dominates; -0.23 to -0.17 in the sell>buy population).
2. **Worst conditions (robust, same in train and test):** (a) market cap under ~$5k / L under ~$2k: EV -0.50..-0.57, P(2x) 9-13% - a mechanical cost (impact 30%+ at $200) plus weak tokens; avoid or shrink size. (b) Count buy/sell ratio < 1.5: EV -0.43..-0.44, P(2x) 12%, both periods. (c) Dip entries (pc1h < -50%): -0.40, test -0.43; and hold_24h on them -0.58. (d) Hour 11 UTC (-0.39, test -0.42) and first 2 min of life (high-L: -0.20) are tentative.
3. **Best conditions:** higher L (> $10-14k), mcap $20k-$70k, count buy/sell > 4, strong +300-500% 1h momentum: EV -0.06..-0.2. The improvement of the top of the L/mcap range vs the bottom (about +0.5) is real but mostly the cost model; beware that in true-liquidity terms (raw liquidity column) the cost penalty is smaller and the ranking could change.
4. **Time since launch** (5 s - 24 h; 90% under 25 min), **hour** and **day** show no robust effect. The apparent best hours (21-22 UTC, 4-5 UTC) and best-case age buckets fall within the max-of-many-noisy-means range and flip in test.
5. Winner's-curse check: all "best buckets" regress by 0.1-0.2 into test (mcap D8 -0.049 -> -0.251, D7 -0.140 -> -0.269, sell>buy&high-L +0.226 -> +0.031), while worst buckets stay worst. That asymmetry means timing/size is useful as an *avoidance filter* (cheap, robust) not as a *selection edge*.
6. Practical implication: apply minimum L/market-cap and a buy-pressure floor (count ratio >= ~1.8) as exclusion filters, treat entry hour/day/age as irrelevant, and look elsewhere (exit logic, holder/insider safety filters, notes 1-22) for edge. Given the sign of the only positive cell, a follow-up could test "sell>=buy but liquid and stable" tokens on fresh out-of-sample data before any belief.

Caveats: single regime (3 weeks, June 2026); test is 2,095 tokens with mixed ages (test is older at snapshot); P(2x) uses gross peaks; position-size impact inflated by L=min(liquidity, 0.4*mcap); drawdown metric is per-token path max drawdown, not per-strategy; ~100 cells examined without multiple-testing correction beyond the placebo checks above.
