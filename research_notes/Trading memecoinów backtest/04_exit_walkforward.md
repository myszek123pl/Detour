# 04 - Walk-forward optimisation of exit rules (15m price paths)

Code: `backtest/exit_wf.py` (grid, vectorised; reproduces `backtest.py` simulate() to 0.0 difference on 4 named strategies), `backtest/exit_wf_report.py` (selection + bootstrap). Raw: scratchpad `wf/`.

## Setup
- Entry/data identical to `backtest.py`: first detection per token, entry at open of first 15m candle within 15 min of snapshot, high-glitch clipping, one decision per token. Horizon 24h.
- Extra data fix: tokens with a candle-to-candle close jump >1000x are dropped (2 tokens). One of them (close 30,895x entry, day 6) alone turned every "hold" rule into +300-500% gross and fooled the optimiser (train EV +5.45 for "no stop, 1h hold", val -0.07, test -0.13). Results below are after that exclusion. Remaining extreme paths (e.g. 435x then 0) were kept, so the surviving upside tail may still contain glitches (this only favours the strategy, and it is still negative).
- Days counted from first snapshot day (10 Jun = day 1): train days 1-10 (n=5,588), validation 11-15 (n=2,425), test 16-20 (n=1,671). Total 9,684 tokens.
- Costs: fee 1.25%/side, impact 2*pos/L per side (clipped 90%), L = min(liquidity_usd, 0.4*market_cap_usd), $0.30 tip per tx (1 buy + number of sells). Median L = $3.7k, so impact exceeds 10% per side for 0% / 53% / 95% of tokens at $50 / $200 / $1000.
- Grid (10,962 configs): stop-loss {none,20,30,40,50,60,70%}; TP ladder: none, 1 TP (1.3/1.5/2/3x, sell 100%), 1 TP (sell 33%/50%, rest rides), 2-level (1.5/2/3x sell 50% + 3/5/10x sell 25%/50%) = 29 ladders; trailing {none, 30/40/50/60% after 1.5x or 2x}; time stop {1,2,4,6,12,24h}.
- Selection protocol per cost level: top-20 on train, pick best on validation, report once on test. Bootstrap = 4,000 resamples of test tokens (token-level, ignores cross-token correlation within a day, so CIs are somewhat optimistic).
- Intra-candle: "worst" = stop checked before TPs in a candle (as in backtest.py); "best" = TPs first, then stop on remainder. Grid and selection were run under both.

## Walk-forward result (grid selected under worst-case; test = days 16-20)
Net EV per $1 staked per trade.

| Position | Chosen rule (train -> val pick) | Train EV | Val EV | Test EV (worst) | CI95 | Test EV (best case) | Win rate |
|---|---|---|---|---|---|---|---|
| zero cost | SL30%, no TP, trail 30% after 1.5x, 24h | +0.052 | +0.127 | -0.053 | [-0.083, -0.020] | -0.053 [-0.081,-0.020] | 24% |
| $50 | same | -0.055 | +0.013 | -0.141 | [-0.168, -0.111] | -0.141 [-0.169,-0.112] | 20% |
| $200 | SL20%, no TP, trail 40% after 1.5x, 24h | -0.222 | -0.226 | -0.276 | [-0.296, -0.256] | -0.276 [-0.296,-0.255] | 10% |
| $1000 | SL20%, no TP, trail 40% after 1.5x, 24h | -0.717 | -0.694 | -0.679 | [-0.697, -0.660] | -0.679 [-0.697,-0.660] | 4% |

(The $50 rule has one positive validation EV, +0.013, which does not survive test.)

## Does ANY exit rule make the unfiltered universe positive?
| Cost level | Configs with EV>0 train | val | test | Best single config, test EV (look-ahead / oracle) | Best-case-intra-candle grid, test max |
|---|---|---|---|---|---|
| zero cost | 8.9% | 15.6% | **0.0%** | -0.031 | -0.0002 |
| $50 | 0.0% | 0.2% (1 cfg) | 0.0% | -0.121 | -0.092 |
| $200 | 0.0% | 0.0% | 0.0% | -0.259 | -0.234 |
| $1000 | 0.0% | 0.0% | 0.0% | -0.669 | -0.657 |

- With zero costs, 473 configs are positive in both train and validation (mostly tight stops 20% + moonshot TPs or 1.5x/30% trail); 0 of them are positive in test. Rank correlation of config EV: train-val 0.81, val-test 0.45, train-test 0.85 (the ordering is stable, but the whole level shifts down in the test period; the test window is simply a worse regime).
- With realistic costs no config is positive in ANY of the three periods at $200/$1000, and essentially none at $50. Answer: no exit rule makes the unfiltered universe positive; best oracle config (SL20%, 50%@3x + 50%@5x, 24h) still loses 3% gross, 12% at $50, 26% at $200.

## Intra-candle ambiguity bound
Per config, best-case minus worst-case EV (test, zero cost): mean +0.0125, 99th pct +0.051, max +0.066 (similar with costs; mean +0.010 at $200). Best-case grid maximum test EV is still negative at every cost level (zero-cost -0.0002, i.e. break-even at best). The selected rules are almost insensitive (no-TP rules: identical to 3 decimals). Ambiguity cannot flip the sign of the conclusion. Caveat: ambiguity is bounded only within a candle; real fills (slippage in a falling market, latency, failed sells on rugs where low=0 but nobody can exit) are worse than either bound, since the model fills stops at the stop price even when liquidity is gone.

## Costs vs price paths (all 20 days, worst-case; EV per trade)
| Strategy | Pos | Gross (zero-cost) | Fee | Impact | Tips | Net |
|---|---|---|---|---|---|---|
| hold 24h | $50 | -0.199 | -0.020 | -0.048 | -0.012 | -0.279 |
| hold 24h | $200 | -0.199 | -0.020 | -0.178 | -0.003 | -0.400 |
| hold 24h | $1000 | -0.199 | -0.020 | -0.541 | -0.001 | -0.760 |
| ladder_B (SL50, 50%@2x, 25%@5x, trail50) | $50 | -0.057 | -0.023 | -0.057 | -0.013 | -0.151 |
| ladder_B | $200 | -0.057 | -0.023 | -0.212 | -0.003 | -0.296 |
| ladder_B | $1000 | -0.057 | -0.023 | -0.638 | -0.001 | -0.720 |
| tight_D | $200 | -0.049 | -0.024 | -0.213 | -0.003 | -0.288 |
| scalp_E | $200 | -0.061 | -0.023 | -0.214 | -0.003 | -0.301 |
| WF-chosen @ $200 | $50 / $200 / $1000 | +0.034 | -0.026 | -0.064 / -0.238 / -0.713 | -0.012 / -0.003 / -0.001 | -0.068 / -0.233 / -0.705 |

(Contributions are sequential differences; the order fee -> impact -> tips is used.)

Takeaways: price paths alone are mildly negative to flat (gross -5% to +3% for stop/TP rules, -20% for buy-and-hold, i.e. entering at first detection has no edge); costs then add -9% at $50, -24% at $200, -71% at $1000, dominated by price impact in thin pools (median L $3.7k). Even at $50, fees+impact+tips (~-9.5%) exceed any gross edge found. Costs are the larger part of the loss for position >= $200; at $50 they are roughly 60-65% of the loss for stop/TP rules, the rest being the drift of the paths.

## Honest conclusions
1. No exit rule makes the unfiltered universe profitable, net or even gross, out of sample. Best zero-cost walk-forward rule: -5.3% (CI -8.3% to -2.0%) in test despite +5%/+13% in train/val.
2. Optimisation on exits finds regimes (tight stops with moonshot ladders) that look about break-even gross in-sample; this is selection on a heavy-tailed payoff and it does not carry forward.
3. The $1000 loss (-68%) is almost entirely the liquidity cap: with L=min(liq, 0.4*mcap) and 2*pos/L impact, trades of this size are not feasible in this universe. $200 is already impact-dominated.
4. Intra-candle ambiguity is a second-order effect (about +1pp mean, <= +6.6pp max).
5. Data hygiene matters: a single 30,000x close glitch fabricated a "+450% EV" strategy; any later entry-filter work should clean closes, not only highs (the existing clip in backtest.py only handles highs).
6. Caveats: only 20 days, one regime (June 2026); 9.7k tokens; token-level bootstrap; entry up to 15 min after detection; the impact formula applies the full-position impact to partial sells (slightly conservative for ladders); only exit rules were optimised here, entry filtering is covered in stages 1-3.
