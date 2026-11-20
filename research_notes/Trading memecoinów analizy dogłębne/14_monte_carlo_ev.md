# Monte Carlo of memecoin bot strategies: EV, ruin and break-even edge (pump.fun entries, filtered entries, post-graduation entries)

Method and honesty note. No new web searches were run (0 of ~3 budget): the base rates come from the existing notes in `/home/user/Detour/research_notes/` (18_risk_management.md, 24_trader_outcomes.md, 02_solana_launchpads.md, pogłębienie 18_graduation_plays.md, 33_tx_reliability.md, 41_holder_retention.md, 46_lifecycle.md), which themselves rely on search-snippet-level secondary sources. Everything tagged [ASSUMPTION] is my own parameter choice; every number labelled [SIM] is output of that assumed model, not an empirical measurement. The model is a stylized stress-test: its job is to show which parameters EV is sensitive to and how large a "hit-rate uplift" is needed, not to predict profits. All absolute EV levels are only as good as the assumed outcome distributions, which are NOT calibrated to a real trade log.

Code (reproducible, numpy, seeds fixed): `/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/mc.py` (engine), `run.py` (first pass, N=200k tokens/scenario, output `out.txt`, `res.json`), `run2.py` (second pass with recalibrated post-grad class, graduation-only uplift, position cap, output `out2.txt`, `res2.json`).

## 1. What base rates and cost inputs go into the simulation?

### Takeaway
Empirical anchors are thin but consistent: graduation is ~0.2-2% of launches (0.26% in mid-2026, 2.01% peak week Mar 2026, 6.7% briefly after BOOST), ~69% of tokens make their last trade on day 0, and roughly half or more of pump.fun traders are net losers in most windows. Cost inputs are anecdotal. There is no empirical return distribution for post-graduation entries, so scenario (c) is the weakest-grounded part.

### Cited Findings
- Graduation rate: ~0.26% 7-day average mid-June 2026 (Dune via DEXTools); 2.01% in the week of Mar 9-15 2026; 6.7% in late July 2026 after BOOST; peaked ~2.1% in June 2024; arXiv 2607.02823 pooled 24h graduation 0.198% (May-Jun 2026) vs 0.63% (Sep-Oct 2025) — [DEXTools](https://www.dextools.io/news/pump-fun-graduation-collapse-solana-fees-2026), [KuCoin/Odaily](https://www.kucoin.com/news/flash/pump-fun-meme-coin-graduation-rate-hits-2-01-highest-since-july-2025), [The Block](https://theblock.co/news/defi/2026-07-29-pump-fun-token-graduation-rate-jumps-boost-changes-launch-incentives-409815), [arXiv](https://arxiv.org/abs/2607.02823) (via existing notes; definitions differ and are not comparable)
- Survival: CoinGecko, ~18.67M pump.fun tokens: 68.67% made their last bonding-curve trade on launch day, ~4.55% traded beyond 90 days — [CryptoPotato](https://cryptopotato.com/nearly-70-of-pump-fun-tokens-die-on-launch-day-coingecko/), [Crypto Briefing](https://cryptobriefing.com/pump-fun-token-survival-rate-study/)
- Solidus Labs: ~98.6% of pump.fun tokens (Jan 2024-Mar 2025) became pump-and-dump/worthless (single-vendor classification) — [Solidus](https://www.soliduslabs.com/reports/solana-rug-pulls-pump-dumps-crypto-compliance)
- Trader outcomes: ~0.4% of ~13.55M wallets realized >$10k; monthly profitable-wallet share rarely above 50% (low 30.1% June 2025); 50.6% lost money in a March 2026 snapshot — [Decrypt](https://decrypt.co/300403/pump-fun-traders-millionaires), [CoinGecko](https://www.coingecko.com/research/publications/pump-fun-traders-are-making-a-comeback), [Our Crypto Talk](https://ourcryptotalk.com/news/pump-fun-96-percent-traders-losing-money)
- Bots hold ~1 in 4 new pump.fun tokens at launch and almost none graduate (June 2026 sample); up to 1.75% of launches manipulated by dev-funded snipers — [DEXTools](https://www.dextools.io/news/pumpfun-new-token-bot-activity-data-june-2026-es), [Pine Analytics](https://pineanalytics.substack.com/p/exit-liquidity-machines)
- Costs: bot platforms 0.5-1% per tx (Trojan 0.9%, BonkBot 1%); PumpSwap fee 0.25% total (0.2% LP + 0.05% protocol); failed Solana txs up to 75% of non-vote txs in mania periods; a failed pump.fun buy still pays the network fee — [RPC Fast](https://rpcfast.com/blog/top-solana-sniper-bot), [MadeOnSol](https://madeonsol.com/blog/bonkbot-vs-trojan), [The Block](https://www.theblock.co/news/business/2025-03-20-pump-fun-launches-dex-called-pumpswap-to-instantly-migrate-graduated-tokens-347360), [arXiv 2504.18055](https://arxiv.org/html/2504.18055v1), [BloFin](https://blofin.com/academy/education/pumpfun/why-pump-fun-trades-fail)
- Pump-and-dump study (arXiv 2507.01963): median dump erases ~56% of value — [arXiv](https://arxiv.org/pdf/2507.01963)

### Model specification [ASSUMPTION unless stated]
- Time grid: 120 steps per trade (1 step ~15 s, max hold ~30 min), log-price path = piecewise-linear rise to a class-specific peak, decay to a class-specific final value, plus 5%/step bridge noise; "rug" tokens get a one-step collapse to 3-10% of price after the peak.
- Scenario (a) random pump.fun entries (entry right after launch, ~$4-5k mcap), class mix: rug/dead = remainder (~55%), bleed 28%, mid-pump (peak 2-6x then decays) 12%, near-miss (peak 6-12x, dies) 3%, graduate g (peak 10-25x), moonshot 0.05% (peak 40-300x). g in {0.3%, 0.8%, 2%} spans the cited graduation range. Sanity check [SIM]: mean hold-to-end price = 0.13x of entry, mean peak = 2.1x.
- Scenario (b) filtered entries: edge u = multiplier on the probability of every class with peak >= 2x (mid-pump, near-miss, graduate, moon); mass is removed proportionally from rug and bleed classes. A second definition ("graduation-only uplift") multiplies only near-miss/graduate/moon (peak >= 6x). Filter cost (skipped trades) ignored, so b is the favourable case.
- Scenario (c) post-graduation entries (PumpSwap, entry ~20 s after migration, extra adverse entry drift ~5% + 2% slippage, fee 0.25%/side). Two class mixes with NO empirical grounding (existing note 18_graduation_plays.md found no post-graduation return dataset): "central" = 45% instant dump / 35% fade / 12% reaches 2-3x / 6% 4-8x / 1.8% 12-60x / 0.2% 60-300x (mean hold-to-end 0.71x, mean peak 2.7x); "optimistic" = 40/33/15/8/3.4/0.6% (mean hold 0.95x, mean peak 3.9x).
- Costs per leg: pump.fun curve fee 1.25%/side [ASSUMPTION; actual platform fee schedule not verified], bot markup 0% in base (self-built bot; +1% each way tested), buy slippage 1.5%, take-profit slippage 1.5%, stop slippage 4%, adverse delay drift ~2% (log-normal), tip+priority 0.0015 SOL per landed tx (3x tested), failed-buy probability 12% (costs 0.0005 SOL, no position), sell failure 8% per attempt (retried next step, so stops fill at worse prices), 25% when price <0.5x entry. Stops are checked on step closes and fill at the observed (gapped) price, so rugs gap through stops.
- Position: 0.25 SOL per trade in the library (fixed costs ~1.2-2% of position); bankroll paths: start 10 SOL, position = f x current equity (f = 1%, 2.5%, 5%) capped at 1 SOL (liquidity cap [ASSUMPTION]); 10,000 paths x 300 or 1,000 trades by bootstrapping from 150-200k simulated trades per scenario. Ruin = equity falls to <=25% of start at any time. Max drawdown = peak-to-trough on equity.
- Exit policies: A = hold to time-out with -35% stop (no take-profit); B = ladder sell 50% at 2x and 25% at 5x, remaining 25% on 40% trailing stop (armed after 2x), hard stop -35%; C = ladder 40% at 2x, 20% at 4x, 20% at 10x, 50% trail, stop -35%; D = tight: 50% at 1.5x, 25% trail, stop -20%.

### Inferences
- Costs are not the main driver of -EV for random entries: the frictionless version of B (no fees, slippage, tips or failures) still has EV -17.2% per trade vs -21.9% with base costs [SIM]. The assumed outcome distribution (rugs, bleeds, gapped stops) dominates; costs add 5 pp (more once the edge is positive; see section 3).
- Failed txs barely matter to EV in this model: removing them entirely moves B/u=1 EV from -21.9% to -24.7% (worse, not better), because a failed buy simply skips a -EV trade for ~0.0005 SOL. Do not read this as "failures are good"; it is an artifact of the base trade being -EV. Failed or delayed sells are the costly case (stops fill later at gapped prices), but that effect is small next to the distribution itself.

### Gaps
- No empirical distribution of per-trade returns for a real bot; no sourced post-graduation return statistics (share continuing vs dumping at 5m/1h/24h); no verified current pump.fun curve fee; no sourced landing rates or tip floors. All of those are assumptions above.

## 2. What are the outcome distributions, EV, median, P(ruin) and max drawdown for (a), (b), (c)?

### Takeaway
[SIM, assumption-driven] Random pump.fun entries are deeply -EV (about -22% per trade with a ladder, -50% with no take-profit) and a 300-trade run at 1% of equity per trade ends at a median of 0.46x the starting bankroll with a median max drawdown of 55%. A filtered strategy is only profitable if the filter roughly doubles the share of tokens reaching >= 2x; even then the median trade loses ~41% and the profit sits in a thin right tail. Post-graduation entries look roughly breakeven-to-slightly-negative under a pessimistic ("central") assumption and strongly +EV under the optimistic one, so the conclusion for (c) is entirely a function of an unmeasured parameter.

### Per-trade results (net return on stake, after all costs; N = 150-200k simulated trades; "win" = net > 0) [SIM]
| Scenario / policy | EV per trade | Median trade | Win rate |
|---|---|---|---|
| (a) random, g=0.3%, A no-TP | -50.1% | -42.7% | 0.2% |
| (a) random, g=0.3%, B ladder | -23.7% | -42.0% | 15.6% |
| (a) random, g=0.8%, A | -49.8% | -42.7% | 0.3% |
| (a) random, g=0.8%, B | -21.9% to -22.0% | -41.9% | 16.1% |
| (a) random, g=0.8%, C | -24.0% | -41.9% | 15.4% |
| (a) random, g=0.8%, D tight TP | +0.6% to +1.2% (see caveat) | -26.9% | 28.5% |
| (a) random, g=2%, B | -17.6% | -41.8% | 17.0% |
| (b) filtered u=1.5, B | -8.4% | n/a | n/a |
| (b) filtered u=1.8, B | -0.5% | -41.2% | 26.1% |
| (b) filtered u=2, B | +4.9% | -41.0% | 28.5% |
| (b) filtered u=3, B | +32.0% | -0.2% | 41.1% |
| (b) filtered u=2, A (no TP) | -47.5% | -42.6% | 0.7% |
| (c) post-grad central, A | -20.3% | -40.0% | 8.1% |
| (c) post-grad central, B | -3.1% to -3.3% | -39.9% | 16.6% |
| (c) post-grad central, D | +22.6% | -25.4% | 25.5% |
| (c) post-grad optimistic, B | +20.5% to +22.0% | -39.6% | 22.8% |
| (c) post-grad central, tail x1.5, B | +14.8% | -39.5% | 24.4% |

Caveats on this table: (1) The D rows are positive mostly because the model gives every class a peak >= ~1.0-1.5x after a delayed entry and D's 1.5x/trail rule harvests that built-in "pump then dump" shape; real entries at a slipped price may not see that spike. Treat D as a model artifact, not evidence that tight take-profits have edge. (2) The ladder-vs-no-ladder gap (B beats A by ~28 pp) mostly reflects that the assumed paths peak and then decay, which is built into every class. (3) Win rate under B is 15-17% for random entries; median trade is a -40% stop-out loss.

Trade-level tail shape (B, g=0.8%) [SIM]: P(>2x multiple) = 7.7%, P(<0.5x) = 23.7%, 99th percentile net +276%, 99.9th +464%, stdev 88% of stake; EV excluding the top 0.1% of trades is -22.9%, excluding the top 1% is -26.1%. For filtered u=2: EV +4.9%, but EV excluding the top 1% of trades is -0.2%, so the whole edge sits in the top percentile (consistent with the venture-style point in 18_risk_management.md).

### Bankroll paths (10k paths, start 10 SOL, position f x equity capped 1 SOL, B policy unless noted) [SIM]
| Scenario | f | Trades | Median final / start | Mean final / start | P(>start) | P(ruin: equity <=25%) | Median max DD | P(max DD>50%) |
|---|---|---|---|---|---|---|---|---|
| (a) random g=0.8% | 1% | 300 | 0.46 | 0.47 | 0% | 0% | 55% | 76% |
| (a) random g=0.8% | 1% | 1000 | 0.00 | 0.01 | 0% | 100% | 100% | 100% |
| (a) random g=0.8% | 2.5% | 300 | 0.15 | 0.16 | 0% | 90% | 86% | 100% |
| (a) random g=0.8% | 5% | 300 | 0.01 | 0.02 | 0% | 99.9% | 99% | 100% |
| (b) u=1.8 (near breakeven) | 1% | 300 | 0.90 | 0.93 | 30% | 0% | 21% | 0% |
| (b) u=1.8 | 1% | 1000 | 0.69 | 0.75 | 18% | 1% | 44% | 35% |
| (b) u=1.8 | 2.5% | 1000 | 0.52 | 0.85 | 27% | 30.5% | 70% | 86% |
| (b) u=2 | 1% | 300 | 1.06 | 1.10 | 62% | 0% | 15% | 0% |
| (b) u=2 | 1% | 1000 | 1.28 | 1.40 | 73% | 0% | 25% | 3% |
| (b) u=2 | 2.5% | 1000 | 2.51 | 3.42 | 83% | 2.2% | 46% | 39% |
| (b) u=2 | 5% | 300 | 1.53 | 2.08 | 67% | 4.8% | 52% | 55% |
| (b) u=2 | 5% | 1000 | 4.79 | 5.09 | 79% | 17.2% | 64% | 72% |
| (b) u=3 | 1% | 1000 | 18.5 | 18.6 | 100% | 0% | 7% | 0% |
| (b) u=3 | 5% | 1000 | 33.3 | 33.5 | 100% | 0% | 18% | 0% |
| (c) post-grad central | 1% | 300 | 0.81 | 0.85 | 19% | 0% | 27% | 0% |
| (c) post-grad central | 1% | 1000 | 0.48 | 0.54 | 7% | 11.4% | 59% | 70% |
| (c) post-grad central | 2.5% | 1000 | 0.17 | 0.36 | 8% | 67.9% | 88% | 98% |
| (c) post-grad central, tail x1.5 | 2.5% | 1000 | 12.5 | 12.7 | 100% | 0% | 28% | 3% |
| (c) post-grad optimistic | 2.5% | 1000 | 18.1 | 18.4 | 100% | 0% | 26% | 2% |
| (a) random, D tight TP | 2.5% | 1000 | 0.75 | 1.17 | 38% | 15.6% | 59% | 69% |

Reading: the paths are extremely sensitive to the edge parameter. Between u=1.8 (EV about 0) and u=3 (EV +32%) the 1000-trade median bankroll goes from 0.69x to ~18x; that sensitivity (a +/-1 pp shift in a ~1% event) is the real finding, not any single row. With bankroll compounding capped at 1 SOL per trade, the large-multiple rows (u=3, optimistic) are mostly linear accumulation; read them as "profitable" or "not", not as forecasts. Near-breakeven strategies still show median max drawdowns of 40-70% over 1000 trades at 1-2.5% sizing, matching the earlier finding in 18_risk_management.md that 1%+ sizing on a ~70%-loser strategy gives >50% drawdowns more often than not.

### Inferences
- With P(ruin) near zero only at f=1% and positive edge, 0.25-1% per-trade sizing (as 18_risk_management.md recommends) remains the only range that survives a thin or overestimated edge. At f=2.5% with edge u=1.8 (EV ~0), P(ruin) is 30% over 1000 trades; at f=5% with true edge u=2, 17%.
- Median outcome is negative in most plausible regimes even when mean EV is positive (the median trade is a stop-out around -40%); a 300-trade live test can easily look like -30% drawdown on a positive-EV strategy, so a short live sample cannot validate it.
- For post-graduation entries the sign of EV flips between "central" and "optimistic" class mixes, so the strategy cannot be assessed without measuring the actual 5m/1h return distribution after migration (listed as a gap in 18_graduation_plays.md).

### Gaps
- Position-size/liquidity impact is represented only by the 1 SOL cap; real exit-liquidity limits and sandwich losses were not modelled. Correlated crashes (all positions dumping at once) are not modelled: trades are drawn i.i.d., which understates drawdown clustering; the 18_risk_management.md note treats cross-position correlation as ~1 in stress.
- Regime shifts (graduation rate 0.2% to 6.7% within months) are not simulated as a time-varying process.

## 3. What minimum edge (hit-rate uplift) is needed to break even?

### Takeaway
[SIM] For random-launch entries with ladder policy B, break-even needs the share of tokens reaching >= 2x to rise by ~1.57-1.94x (u = 1.57 at g=2%, 1.82 at g=0.8%, 1.94 at g=0.3%), i.e. from ~15.9% to ~29% at g=0.8%. If only the high-peak tail (>= 6x, including graduates) can be improved, the required uplift is ~3.0x at g=0.8% (2.15x at g=2%, 3.55x at g=0.3%): about 11-12% of entries must reach >= 6x, versus 3.4-5.1% for random entries. Without any take-profit ladder (policy A) break-even needs u ~5-6.5x, so exit rules matter as much as the filter. For post-graduation entries break-even is u ~1.09x under the central class mix (needs ~9% more hits), but that number is only meaningful if the central mix is realistic.

### Break-even uplift table [SIM]
| Scenario | Policy | Break-even multiplier on hit probabilities |
|---|---|---|
| (a)->(b) random g=0.3%, all >=2x classes scaled | B | 1.94x |
| (a)->(b) random g=0.8%, all >=2x classes scaled | B | 1.82x |
| (a)->(b) random g=2%, all >=2x classes scaled | B | 1.57x |
| random g=0.3% / 0.8% / 2% | A (no TP) | 6.5x / 6.3x / 5.0x (bisection capped at 5.0 for g=2%) |
| graduation-only uplift (near-miss, graduate, moon scaled), g=0.3% | B | 3.55x (graduation 0.3% -> ~1.1%; share reaching >=6x ~3.4% -> ~11.9%) |
| graduation-only uplift, g=0.8% | B | 2.98x (graduation 0.8% -> ~2.4%; >=6x share 3.9% -> ~11.5%) |
| graduation-only uplift, g=2% | B | 2.15x (graduation 2% -> ~4.3%; >=6x share 5.1% -> ~10.9%) |
| (c) post-grad central, tail scaled | B | 1.09x (central EV at u=1 is -3.1%) |
| (c) post-grad central, tail scaled | D | 0.49x (EV already positive; artifact caveat above) |

Cost sensitivity at B, g=0.8% [SIM, EV per trade at u=1 / u=2]: base -21.9% / +5.1%; +1% bot fee each way -23.2% / +3.2%; tips x3 (0.0045 SOL) -24.2% / +2.5%; frictionless -17.2% / +16.0%; no failed txs -24.7% / +5.7%. So at u=2, total friction (fees 2.5% round trip, slippage, tips, failures) consumes about 11 pp of EV, and an off-the-shelf bot's extra 1% per side costs ~1.9 pp. Moving u from 1.8 to 2.0 swings EV by ~5 pp, so friction uncertainty of +/-2 pp corresponds to roughly +/-0.08 in the break-even uplift.

### Inferences
- In rough terms, a filter must "double the number of >=2x tokens" (or triple the number of >=6x/graduating tokens) while costing nothing in skipped winners, to merely break even under the assumed ladder and ~2.5%+ round-trip frictions. Precision at that level (picking ~11% of entries that reach 6x, vs ~4% base) is an ambitious claim given that bots already occupy 1 in 4 launches and almost none graduate (DEXTools June 2026) and that existing notes found no evidence of profitable predictive signals beyond graduation-prediction models whose metrics were not retrieved.
- Because break-even u shrinks as base graduation rate rises (g=2% needs 1.57x vs 1.94x at 0.3%), the same filter is more likely to be profitable in a high-graduation regime than in the mid-2026 regime of ~0.2-0.3%; a regime-aware on/off switch (see 18_risk_management.md rule 7) is consistent with this.
- Statistical verification burden: with a win rate near 26-29% and a heavy tail (stdev ~1.1x stake per trade vs EV ~0.05x), the standard error of mean EV after n trades is ~1.1/sqrt(n); n=1,000 gives +/-3.5 pp (1 sigma), so an EV of +5% cannot be distinguished from 0 with fewer than several thousand trades. This matches the "thousands of trades" statement in 18_risk_management.md.
- Exit policy is as important as entry filtering: moving from no-TP to a 2x/5x ladder improved EV by ~28 pp in this model, comparable to an ~2x filter uplift. Whether that gain is real depends on the unvalidated assumption that tokens peak after a delayed, slipped entry.

### Gaps
- Break-even numbers are for specific assumed class mixes and exit rules; different assumptions (e.g. fewer tokens that spike after entry, heavier sniper/insider extraction) would move the required uplift higher, possibly beyond what any plausible filter can deliver. A real estimate requires logging ~1,000+ live or shadow trades with actual fills, then re-fitting the class mix.
- Hit-rate uplift achievable by any real filter (holder concentration, dev reputation, bundling checks, narrative scoring) was not measured here; no sourced precision/recall numbers were available.
- Not modelled: MEV/sandwich losses beyond the slippage assumption, tax, hot-wallet/security losses, API/latency competition with snipers on the same tokens (which would erode u), and filter-induced trade skipping costs.
