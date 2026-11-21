# 29. The execution gap: how much worse real trading is than the ideal chart

Scripts (all `python3 -I`): `backtest/exec_gap_lib.py` (engine, validated: reproduces `backtest.py` ladder_B gross values exactly, max abs diff 0.0), `exec_gap_a.py` (one component at a time), `exec_gap_b.py` (2^8 factorial of components x 3 trader profiles x 2 strategies), `exec_gap_c.py` (waterfall, Shapley, slices). Raw output: `backtest/out/exec_gap_{a,c}.{json,txt}`.
Data: ian05012/solana-memecoin-dataset (tokens.parquet, ohlcv.parquet; 15m candles; June 2026). No web searches. Primary strategy: **ladder_B** (SL -50%, TP 2x sell 50%, TP 5x sell 25%, remainder trailing -50% after 2x, 24h horizon); ladder_C (SL -40%, 1.5x/3x/10x thirds) as a check. EV = mean net return per $1 staked per signal.

## 0. Headline

| | ladder_B EV per trade (pos $200) | 95% CI |
|---|---|---|
| Ideal chart (open entry, exact fills, no costs) | **-7.2%** | -9.6 .. -4.8 |
| Bot, realistic (fee 1.25%, tip $0.60, slippage, 5% fail with fast retry, impact) | **-26.7%** | -28.3 .. -25.3 |
| Semi-automatic terminal user | -28.8% | -29.8 .. -27.8 |
| Manual trader with behaviour errors | **-29.2%** | -30.2 .. -28.1 |

- The unfiltered ideal is already negative (consistent with README stage 1). So the execution gap is not "profit eaten": it is 20-22 pp of additional loss per trade, i.e. the realistic result is ~4x worse than the chart.
- **Price impact (position vs L) is the single largest component** at $200 (-12.6 pp) and explodes with size ($1000: -36 pp). Fees are second among the "certain" ones (-2.2 pp). Everything else is small in the mean but matters in the winner tail (section 3).
- A bot removes delay, chasing, behaviour and failed-tx damage, but NOT fees, stop gaps or impact. Its gap vs a manual trader is only ~2.5 pp in the mean at $200 (but ~20 pp in the right tail, see sec. 3).

## 1. Setup, assumptions and what the data cannot say

- Universe U = 5,115 tokens that have a tradable candle at all delays k=0..4 (of 9,686 tradeable at k=0). Needed so every scenario uses the same tokens; it is a survivor set (ideal EV on full k=0 set: -4.7%; on U: -7.2%). One scale-break token (price 0.48 -> 1e-11, gross multiple 1e5 at k=1) lies outside U; I did not use any k>0 full-set means because of it.
- "0 candles" is NOT zero latency: entry is the open of the first candle starting after the snapshot, median 8 min (5-95%: 0.7-49 min) after capture. A bot with ~1 s latency is therefore modelled as k=0; the data cannot resolve sub-candle latency, so second-scale latency, MEV/sandwiching and landing probability are parameters, not measurements.
- Fills: SL-first inside ambiguous candles (as in backtest.py). Ideal = exact stop fill; TP-first ordering would add +0.9 pp (bracket -7.2% .. -6.2%).
- Impact: CPMM, per side x = 2V/L, proceeds = V/(1+x), L = min(liquidity_usd, 0.4*market_cap_usd) fixed at entry value (conservative for winners). Median L is only $4.8k (5%: $1.5k, 95%: $23k); 78% of tokens have liquidity_usd > 0.4 mcap, so the 0.4 cap binds almost always.
- Fees 1.25%/side (pump low-mcap tier; 89% of U has mcap < ~$63k ~ 420 SOL, 99.7% < $15M, so the 0.3% floor tier is practically never reachable on these tokens). Tip $0.30/tx (2.27 tx per round trip incl. buy).
- Behaviour parameters (mix of trade "types") are my assumptions, not measured from data.
- Paths: 95% of OHLCV paths end before the 24h horizon; leftover positions are marked at the last close (as in backtest.py). A haircut of that mark to 50% costs -9.6 pp (to 0: -19 pp). This affects ideal and real alike but is a real optimism source. 21% of trades end via this forced mark (mean final mult 0.83).

## 2. One component at a time, from the ideal (ladder_B, U, gross unless stated)

**Entry delay (extra candles, cost basis re-anchored at the later open).**

| k (extra min) | EV | d vs k=0 | 95% CI of d |
|---|---|---|---|
| 0 | -7.2% | - | - |
| 1 (15) | -9.6% | -2.4 pp | -4.6 .. -0.1 |
| 2 (30) | -5.7% | +1.5 | -1.4 .. +4.2 |
| 4 (60) | -2.8% | +4.3 | +1.4 .. +7.8 |

Entry price drifts down after the snapshot (median open vs k=0: 0.90, 0.80, 0.73, 0.69x for k=1..4; P(>=2x) only 5-6.5%): snapshots are taken near local highs and the cohort mean-reverts. So with no edge, waiting looks harmless or even good in the mean. This is survivorship-contaminated (U needs trading 1h later) and edge-free. See the winners lens (sec. 3): for winners, k=1 alone cuts ladder EV from +102% to +57%.

**Fill inside the entry candle (chasing).** Entry-candle high/open-1 quantiles: 25% 4%, median 20%, 75% 50%, 90% 101%.

| fill | mean premium | EV | d |
|---|---|---|---|
| open | 0 | -7.2% | - |
| OHLC4 (random intrabar time) | +3.7% | -12.5% | -5.3 pp |
| open + 25% of range | +11.6% | -18.7% | -11.5 pp |
| open + 50% | +23% | -25.2% | -18.1 pp |
| candle high | +47% | -33.8% | -26.6 pp |

The loss is far larger than the mean premium (3.7% -> 5.3 pp) because the candles with the largest in-candle pump are exactly those whose payoff is high: chasing taxes winners. (Candle close fill is look-ahead, ignored.)

**Stop-loss execution.** 55% of trades end at the stop; gap-through (open below stop) is 10.6% of those, mean loss 21 pp on such a trade, -1.25 pp on average (ladder_C: -0.2 pp). Extra slippage on stop fills: 3% -1.4 pp, 5% -2.3, 10% -4.5, 20% -9.0 (linear: ~0.45 x slippage). Stop evaluated on candle closes only: -5.5 pp. **Surprise: selling at the next candle open after a trigger (a slow/manual reaction) is +4.2 pp better than the exact stop**, because 33% of stop-trigger candles close back above the stop (wick-outs) and 15m wicks mean-revert. This is a property of the no-edge, noisy-wick cohort, not an argument for slow stops. TP slippage: 2% -0.6 pp, 5% -1.4, 10% -2.8.

**Failed transactions.** Sell fails w.p. p and is only retried on the next triggering candle (worst case "no retry in seconds"): p=5/10/15/25% -> **+0.2 / +0.3 / +0.6 / +1.6 pp** (CI mostly above 0); buy fails retried one candle later: -0.1 / -0.2 / -0.3 / -0.3 pp. In the mean, failure is ~0 (same wick-reversion effect), so the failure cost is variance/tail and the wasted tip, not mean EV, in this dataset. Mean failed sells at p=10%: 0.11 per trade (9.7% of trades hit >=1 failure). A fast-retry bot pays only 1/(1-p) more tips.

**Fees (round trip both sides, ladder_B).**

| fee per side | EV | d |
|---|---|---|
| 0.3% | -7.7% | -0.56 pp |
| 0.5% | -8.1% | -0.93 |
| 1.0% | -9.0% | -1.85 |
| 1.25% | -9.5% | **-2.31** |
| 2.0% | -10.8% | -3.68 |

1.25% vs 0.3% is a 1.75 pp difference per trade. Payoff-weighted (gross ~0.93x), cost is ~0.93 x 2 x fee.

**Tips (EV delta, $ per tx; 2.27 tx/trade).**

| tip | pos $50 | pos $200 | pos $1000 |
|---|---|---|---|
| $0.30 | -1.4 pp | -0.34 | -0.07 |
| $1.00 | -4.6 | -1.1 | -0.2 |
| $3.00 | -13.6 | -3.4 | -0.7 |

Tips are a small-size problem: at $50 a $1 tip is 4.6 pp, bigger than the fee difference.

**Price impact vs position size (no fee/tip).**

| pos | EV | d | median pos/L | P(pos/L>5%) | P(pos/L>25%) |
|---|---|---|---|---|---|
| $25 | -9.6% | -2.5 pp | 0.5% | 0% | 0% |
| $50 | -11.7% | -4.6 | 1.0% | 0.1% | 0% |
| $100 | -15.4% | -8.2 | 2.1% | 12.6% | 0% |
| $200 | -21.4% | -14.3 | 4.2% | 41.9% | 0% |
| $500 | -33.9% | -26.8 | 10.4% | 72% | 12.6% |
| $1000 | -46.3% | -39.2 | 20.7% | 92% | 41.9% |
| $5000 | -75.7% | -68.6 | 104% | 100% | 92% |

Sizing rule (position = min(pos, cap x L), impact only): cap 0.5% of L -> EV -9.0% (avg position $39), 1% -> -10.7%, 2% -> -13.3%, 5% -> -17.9%. Dollar-weighted EV is slightly better than unweighted (-6.9% at 0.5%) because small-L tokens get small bets.

**Human behaviour (each applied to 100% of trades; gross, d vs disciplined ladder).**

| behaviour | EV | d | 95% CI of d |
|---|---|---|---|
| move stop -50% -> -80% when hit | -10.4% | -3.2 pp | -4.3 .. -2.1 |
| no stop at all | -11.1% | -4.0 | -5.0 .. -2.7 |
| hold loser, exit only at break-even recovery | -23.0% | **-15.8** | -16.5 .. -15.3 |
| greed: no TP, no trail | -18.7% | **-11.5** | -14.9 .. -7.6 |
| all out at 1.3x | -9.0% | -1.9 | -4.1 .. 0.1 |
| all out at 2x | -7.5% | -0.3 | n.s. |
| panic sell at close <= -25% | -7.1% | +0.1 | n.s. |
| panic sell after -20% from peak (post TP1) | -6.4% | +0.8 | +0.2 .. +1.4 |

The expensive errors are the ones that turn a bounded loss into an unbounded or capped-upside one: hoping/holding losers and not taking profit. Panic selling is not costly in the mean here (mean reversion again), and sells winners only mildly early.

## 3. Waterfall: ideal -> realistic (ladder_B, pos $200, sequential order, U)

Order: delay, chase, stop/exit execution, failed tx, fees, tips, impact, behaviour. "Winners EV" = mean over the 15.8% of tokens with peak >= 3x (look-ahead subset, used only to show what each friction does to the right tail).

Manual trader (k=1, fill open+25% of range, stops reacted to at next candle open with 3% slippage, TP slip 3%, 10% fail (sell not retried, buy retried next candle), 1.25% fee, $0.30 tip, behaviour mix: 30% disciplined, 15% move stop, 10% no stop, 10% hope, 10% panic loss, 5% panic win, 10% all-out at 1.3x, 10% greed):

| Step | EV all | step delta (95% CI) | EV winners | median | win rate | P(loss >= 70%) |
|---|---|---|---|---|---|---|
| Ideal | -7.2% | | +101.9% | -50% | 27.7% | 0 |
| + entry delay (1 candle) | -9.6% | -2.4 (-4.6..-0.1) | +56.7% | -38% | 26.0% | 0 |
| + chasing | -16.1% | **-6.5** (-6.9..-6.1) | +38.3% | -40% | 25.2% | 0 |
| + stop/exit execution | -10.2% | **+5.8** (+5.2..+6.5) | +50.1% | -23% | 26.4% | 4.9% |
| + failed tx | -10.5% | -0.2 (-0.4..0) | +50.5% | -22% | 26.2% | 3.8% |
| + fees 1.25% | -12.7% | -2.2 | +46.7% | -24% | 24.3% | 4.1% |
| + tips $0.30 | -13.0% | -0.3 | +46.3% | -24% | 24.2% | 4.2% |
| + price impact | -25.7% | **-12.7** (-13.0..-12.3) | +24.3% | -37% | 19.1% | 6.0% |
| + human behaviour | **-29.2%** | **-3.5** (-3.8..-3.2) | +18.8% | -41% | 17.4% | 6.2% |

The +5.8 pp "stop execution" step is the next-open/wick-reversion artefact (sec. 2) and lowers the cumulative gap; it comes with a tail cost (P(loss>=70%) from 0 to 4.9%). Gap ideal -> manual: **-22.0 pp** (CI of total EV -30.2 .. -28.1%).

Bot (k=0, 2% fill premium, gap-fills + 2% stop slip + 1% TP slip, 5% failure with fast retry, 1.25% fee, $0.60 tip, no behaviour errors):

| Step | EV all | delta | EV winners |
|---|---|---|---|
| Ideal | -7.2% | | +101.9% |
| + delay (0) | -7.2% | 0 | |
| + chasing (2% of range) | -8.9% | -1.8 | +93.4% |
| + stop/exit (gap-through, slippage) | -11.3% | -2.3 | +85.9% |
| + failed tx (fast retry: tips only) | -11.3% | 0 | |
| + fees | -13.5% | -2.2 | +81.3% |
| + tips | -14.2% | -0.7 | +80.4% |
| + price impact ($200) | **-26.7%** | **-12.5** | +52.2% |
| + behaviour (none) | -26.7% | 0 | |

Same bot at other sizes: $50 -> -20.1% (tips -2.9, impact -3.8); $1000 -> **-49.2%** (impact -35.6, winners' EV falls to +3.9%). Manual at $50 -> -21.3%, at $1000 -> -51.6% (winners EV -19%).

Terminal user with auto-orders (k=1, OHLC4 fill, gap stops, 10% fast-retry fails, milder behaviour mix): -28.8% at $200 (delay -2.4, chase -1.1, stop -2.4, fail +0.4, fees -2.2, tips -0.4, impact -12.4, behaviour -1.2). ladder_C gives the same picture: ideal -7.3%, bot -25.4%, terminal -26.7%, manual -29.6%; impact -12.3..-12.6 pp in all three.

## 4. Order-independent attribution (Shapley over the 8 components, pp of EV, pos $200)

| Component | Bot | Manual | Manual, winners lens |
|---|---|---|---|
| price impact | **-13.4** | **-13.2** | -28.4 |
| chase | -1.4 | **-8.0** | -27.5 |
| fees | -2.0 | -2.0 | -3.8 |
| human behaviour | 0 | -3.4 | -4.8 |
| tips | -0.7 | -0.3 | -0.4 |
| stop/exit execution | -2.1 | +2.8 | +9.7 |
| entry delay | 0 | +2.1 | **-27.1** |
| failed tx | 0.0 | 0.0 | -0.9 |
| Total | -19.5 | -21.9 | |

Standalone / leave-one-out agree on ranking for the manual profile. Key reading: in the mean (all tokens) the ranking is impact >> chase > behaviour > fees > tips; in the winners lens (what an actual edge would be trying to capture) **delay and chase are each ~27-28 pp, as large as impact**, and the winners' ladder EV falls from +102% (ideal) to +19% (manual) or +52% (bot).

**Break-even signal precision** (stylised: a fraction pi of trades are perfectly picked winners, the rest random; pi* = -EV_all/(EV_win-EV_all)): ideal 6.6% -> bot realistic 33.9% -> manual 60.8% at $200 (bot at $1000: >100%, i.e. no signal of this kind pays at that size). Components along the way: 6.6% -> delay 14.5% -> chase 29.6% -> fees 21% -> impact 51% -> behaviour 61% (manual). The execution gap means a signal must identify the top tail ~5-9x better than the ideal chart suggests.

## 5. Slices (ladder_B, pos $200)

By liquidity quartile (L median): Q1 $2.0k: ideal -1.2% / manual -40.3% (gap -39 pp); Q2 $3.6k: -10.0% / -32.9%; Q3 $6.9k: -14.3% / -27.3%; Q4 $15.6k: -3.2% / -16.2% (gap -13 pp). Bot: Q1 -35.0%, Q4 -13.4%. The same $200 costs 3x more in the thin quartile; the gap is almost entirely impact.
By token age at snapshot: gap -25 pp (<2 min), -24 (2-5), -20 (5-15), -23 (15-60), -18 (>1 h) for manual; flat-ish, so age is not the driver.

## 6. Which components matter most, and how a bot removes them

Ranking by mean-EV damage at $200: (1) price impact 12.5-13.4 pp (rises ~linearly in pos/L; $1000: 36 pp); (2) chasing 1-8 pp mean but ~27 pp on winners; (3) entry delay ~0 in mean, ~27-45 pp on winners; (4) human behaviour 3.4 pp (hope-holding -15.8 pp and no-profit-taking -11.5 pp as pure types); (5) fees 2.2 pp (round trip, 1.25%); (6) stop gaps+slippage 1.3-2.3 pp; (7) tips 0.3 pp at $200 but 1.4-2.9 pp at $50; (8) failed tx ~0 in mean, tail + tips only.

What a bot can and cannot remove:
- Delay / chase (largest on the winner tail): remove with pre-armed triggers, direct pool-state reading, Jito/priority landing at the first slot; resolution here stops at 15 min, so the real gain is under-measured by this dataset.
- Behaviour: hard-coded stop/TP, no stop widening, kill switch; removes the -3.4 pp and the tail of the "hope" type.
- Failed tx: blockhash refresh, fast resend, simulate-before-send; turns a variable missed-exit risk into ~1/(1-p) more tips.
- Tips: adaptive tips scaled to position; irrelevant above ~$200, binding below ~$100.
- Impact: the bot cannot change L. It can only cap size: position <= 0.5-1% of L cuts the impact drag to ~2-3.5 pp (from 14 pp at $200) at the price of average positions of $40-70. Equivalent to refusing the bottom liquidity quartile.
- Fees: only by venue/tier/cashback; with mcap < $63k the 1.25% tier applies, so a 0.3% fee is not available on 89%+ of these tokens.
- Stop gaps: not removable; mitigate with smaller sizes (gaps hurt 21 pp on 10.6% of stopped trades) and avoiding tokens with very low L.

## 7. Limitations

- No edge exists in the unfiltered ideal, so "loss vs ideal" can be negative for slow/lazy behaviours (next-open stops, failed sells, delay k>=2): that is mean reversion of wicks/prices in a losing cohort, not a free lunch. The winners lens is look-ahead and only shows exposure.
- 15m candles: no second-level latency, no sandwich/MEV, no partial fills, impact computed at snapshot L (no pool dynamics, fixed L for exits, no impact from own earlier tranches).
- Behaviour mix, failure rates, slippage values, tips are assumptions; not calibrated on real wallet data (see notes 24, 27 for qualitative anchors).
- Survivor universe (53% of tradeable tokens), 95% truncated paths, one glitch family in OHLCV (scale breaks), which I excluded by universe construction rather than cleaned.
