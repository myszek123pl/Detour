# 30. Anatomy of a demonstrably profitable professional pump.fun bot (wallet 5brv79e...) and a professional operating model

Date: 2026-11-21. Primary source: `Foreist/solana-sniper-reverse-engineering` (cloned, READ ONLY, nothing executed; path
`/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/datasets/solana-sniper-reverse-engineering/repo`).
Files read in full: README.md, WRITEUP.md, RESEARCH_LOG.ko.md, part1_behavior.py, part2_model.py, part3_backtest.py, head of features.py, figure 03,
notebook (no stored outputs). Contrast: notes 01, 10, 11, 13 in this folder. Web search NOT used (note 13 found only promotional or blocked pages).

Evidence tags used below: **[R]** reported by the repo, **[D]** derived by me from repo numbers (arithmetic shown), **[I]** my inference,
**[X]** not in any evidence I hold (background knowledge / assumption, treat as unverified).

Important: the repo ships NO data (the 83 GB corpus lives on IP-address servers, the intermediate CSVs/parquets are on Kaggle and are not in the
GitHub clone). Every number below is therefore the author's printed number; I could re-derive only internal consistency, not the numbers themselves.

---

## 0. Corrections to note 13 (read first)

1. Note 13 says "~$938k net in June 2026". Wrong period. **$937,925 net is the whole window 2026-03-12 to 2026-06-30 (111 days, "3.5 months")** [R].
   **June alone: net $188,084**, gross $319,637, fees $131,553 (41.2% of gross), 4,194 trades [R, head-to-head table].
2. "59% hit rate, fees 37% of gross" are whole-window numbers; June was 57.7% net hit rate and 41.2% fee share (worse).
3. "Replica +$29k same-slot, -$334 one slot later" are **simulated, June only**, 853 candidate entries, and the slot axis is an assumed mapping
   (section 7), not a measurement. The replica is 15% of the bot's June dollars, with 148 of 853 entries overlapping the bot's actual buys.

---

## 1. What the bot actually does (facts)

| Item | Value | Tag |
|---|---|---|
| Venue | pump.fun launches (activity schema also lists pump_agent, pump_mayhem, letsbonk, bags for the *deployers' history*; the bot's own venue is described as pump.fun) | R |
| Window | 2026-03-12 08:54 to 2026-06-30 23:29 UTC (111 days; nominal corpus start 01-01 but bot first buys 03-12) | R |
| Volume | 16,163 tokens, 16,192 buy events, 70,812 sell events, 2 burns; about 146 tokens/day (June 140/day) | R, D |
| Tokens by month | Mar(12-31) 3,361 / Apr 3,466 / May 5,110 / Jun ~4,190-4,226 (figures differ by definition: 4,189, 4,194, 4,195, 4,226 appear) | R |
| Universe it picks from | about 28k deployments/day (5.06M "not bought" over 6 months, 3.01M inside the bot's active window); it buys ~0.5% | R, D |
| Signal (what is observable at t0) | Only deployer-history style information is recoverable: top features `mean_buy_usd`, `total_volume_usd`, `secs_since_last`, `launch_rate_per_day`, `hist_events`, `sell_to_buy_ratio`, `launches_last_24h`, `hist_launches`, `hist_sells`, `wallet_age_s`. Time-of-day features rank low. "The bot reads WHO is deploying" | R |
| Entry timing | Deploy-to-first-buy latency median 0 s; 90.7% at <=0 s (same wall-clock second as deployment tx), 98.5% <=1 s; mean 36.4 s from a thin late tail. A second = ~2.5 slots, so "<=0 s" is a 2-3 slot window, NOT proven same-slot (activity data has no slot numbers; authors say so) | R, I |
| Sizing | Median $183, mean $263, sd $233 (CV 0.89), p05 $100, p95 $727. June median $160, mean $231 | R, D |
| Exit | Median 4 sells/token (mean 4.38), 96.6% of tokens exited in >1 sell (ladder), hold median 6 s (p25 4 s, p75 9 s, i.e. ~10-20 slots), 3 tokens never sold. Exit gas only $0.116/sell, so exits are not raced; they are time/ladder driven | R, D |
| Entry cost | $26.66 mean per buy (priority fee + Jito tip, `gas_native == priority_fee + tip_fee`, corr 1.000); = 10.1% of mean position, 14.5% of median position | R, D |
| Landing infra visible in data | Jito tips (2,302 SOL) are paid alongside compute-unit priority fees (3,067 SOL). Total 5,369 SOL = ~$451k at median SOL $84.1, vs $439.8k reported gas: roughly consistent. Split: **57% priority fee, 43% Jito tip**; ~0.33 SOL (~$27) per buy, ~0.19 SOL priority + ~0.14 SOL tip | R, D |
| Venue fee | `dex_usd` $110,506 total, mean $2.90 per buy = ~1.1% of position. Back-solving: buys ~$4.26M x 1.1% = $47k, so sells carry ~$64k = ~1.1% of ~$5.75M proceeds. **~1.1% per side** | R, D |

What is NOT known from the repo: slot of landing, in-block position, whether the bot spams multiple txs/bundles per launch (failed attempts do not appear in an
activity feed of executed swaps), RPC/shred provider, geographic location, whether the wallet is related to the deployers it buys, whether other wallets
belong to the same operator, what the exit ladder levels are (only that there are ~4 sells in ~6 s).

### Fee-spend composition (whole window) [D]
- Entry gas+tips ~$431.7k (16,192 x $26.66) = **78% of all fees**; exit gas ~$8.2k (1.5%); venue $110.5k (20%).
- Fees per round trip = $550,345 / $4.26M buy notional = **12.9% of notional**; gross 34.9% of notional; net 22.0% of notional.
- Turnover ~$10.0M (buys $4.26M + sells ~$5.75M). Net = ~9.4% of turnover.
- Fee spend per day: ~$4.96k (about 59 SOL/day at $84). The bot pays ~$27 *before* it knows whether the spike will hold, on ~146 attempts/day.

---

## 2. PnL distribution

Whole window, per token with >=1 sell [R unless noted]:

| | Gross | Net |
|---|---|---|
| Total | $1,488,270 | $937,925 |
| Hit rate | 78.8% | 59.3% |
| Median ROI per position | 13.3% | 4.7% |
| Mean net per position | | $58.03 [D] (check: 0.593 x 117.25 - 0.407 x 28.16 = $58.07, internally consistent) |
| Avg win / avg loss | | $117.25 / -$28.16 (payoff 4.2:1) |
| Net ROI deciles | | p10 -17.7%, p25 -5.9%, p50 +4.7%, p75 +26.8%, p90 +56.4% |

Shape (figure 03): a unimodal hump centred slightly above 0, thin left tail (p10 only -17.7%), long right shoulder to +100%; the plot has stacked
edge bars at -100% and +200% (~50 positions each, clipped/winsorised bins). **This is not a lottery-ticket, moonshot distribution.** Mean net ROI on notional
(22%) is ~4.7x the median (4.7%): the profit is carried by a right shoulder of +30% to +100% round trips in 6 seconds, not by 100x outliers. That is the
opposite of what retail memecoin strategies look like (compare note 13: sentinel 0/38 reached 5x, 26-31% win rates, loss tails of -84% gap-through).

Caveats on the distribution [I]:
- Positions with a leftover unsold bag are valued at cash received only (no mark-to-market, only 3 tokens never sold, so small), biasing net slightly DOWN.
- Failed or dropped transactions that still burned priority fees are invisible in an executed-swap feed, biasing fees DOWN (section 8).
- The -100% and +200% edge bars are not explained by the authors (could be rugs/partial data, or just clipping). ~0.6% of positions.

### Per-day / per-month stability (what exists and what does not)
**The repo reports NO per-day or per-week PnL series.** No bootstrap CI, no worst-day, no rolling Sharpe. What can be derived [D]:

| | Mar12-May31 (81 d) | June (30 d) |
|---|---|---|
| Net | $749,841 -> **$9.26k/day** | $188,084 -> **$6.27k/day** |
| Trades | 11,969 (148/day) | 4,194 (140/day) |
| Gross per trade | $97.6 | **$76.2 (-22%)** |
| Fees per trade | $35.0 | $31.4 |
| Net per trade | **$62.6** | **$44.8 (-28%)** |
| Fees / gross | 35.8% | **41.2%** |

Reading [I]: June looks like either a decay (competition, or pump.fun regime change) or normal variance; with no daily series the two cannot be separated.
Gross edge per attempt fell 22% while the bot did not reduce its fee spend proportionally, so the cost/gross ratio rose from 36% to 41%. A rising fee share
is the classic signature of a latency race getting more crowded (you must bid more per slot for the same fill). One month of decline is not proof, but it is
exactly the kind of series a professional would monitor with a kill rule (section 9).
June max drawdown: bot $1,131 = 0.6% of June net, replica $445 = 1.5% of its net [R]. The equity curve is nearly monotone, but this is a *realised-PnL cumulative
curve ordered by first-buy time*, with positions of ~$200, so it understates risk (no failed-tx costs, no balance volatility, no downtime days).

---

## 3. Capital needed and capacity

- Positions are tiny and held ~6 s. Capital at risk at any instant is a few positions: 140 trades/day x 6 s = ~14 minutes of position-time per day, so
  average concurrent notional is well under $1k.
- Capital *cycled* in June: $971,151 (turnover, not balance). Return on cycled capital: gross 32.9%, fees 13.5%, net 19.4% [R/D].
- Required working balance [I]: p95 position $727, max June drawdown $1,131, daily fee burn ~$5k. A **bankroll of low-single-digit $k to ~$10k covers the
  strategy mechanically**; the binding constraints are not capital but (a) fee burn if the edge disappears ($5k/day), (b) capacity.
- Capacity is the real limiter [I]: ~$183 median size is set by how much a fresh bonding curve can absorb in the first seconds before your own impact eats the spike;
  $58/trade x 146/day. Doubling size does not double profit. This is why the profit pool ($8.4k/day average, $6.3k in June) is small in absolute terms: it is
  a 3.5-month, $0.94M pool for the best-equipped operator, shared by an unknown number of competitors. A newcomer should expect a fraction of one operator's pool.
- Infrastructure cost is NOT in the net figure [X]: colocated or low-latency servers, a private RPC/gRPC/shred feed, dev time. The repo gives no figures; any
  guess ($ thousands/month) is outside the evidence. Even at $10-20k/month that is <=7% of the bot's June net, so the economics only work for a landed-in-slot
  operator, and only break even-or-negative for anyone landing 1+ slots later.

---

## 4. What is the real edge? Speed vs selection vs both

Evidence pieces:

1. **Fill position dominates (authors' own test, [R]).** Applying the *same* 6 s hold to the bot's own June tokens: entry at the deploy-second open -> 1.5043x median;
   entry at the deploy-second close -> 0.9221x. 30 s hold: 1.32x vs 0.865x; 60 s hold (close entry): 0.808x. The token spikes in the first second then decays
   monotonically. So the *same selected token* is a +50% or -8% trade depending purely on where in the second you got filled.
2. **Cost asymmetry makes it binary [D].** Round-trip cost at $183 is ~16.8% of position ($26.66 flat + 2.2% venue); at $100 it is 28.9%; at $727 it is 5.9%.
   Gross 6 s median multiple is ~1.11 at the bot's observed fill. So after ~1 slot of delay the gross move is gone while the bid for priority is still paid.
3. **Selection is real but weak and unproven in dollars.** GBDT: PR-AUC 0.0761 (15.5x the 0.49% prevalence), ROC-AUC 0.891, precision 17.6% at 5% recall,
   17.4% at the top-0.1% operating point (853 picks, 148 overlap with the bot). So (i) deployer history does separate bot-bought launches from the rest,
   (ii) the bot's rule is **not recovered**: 83% of the replica's top picks are tokens the bot did not buy, and only 0.92% of the bot's buys are captured.
   The bot clearly uses information not in the feature set (dev-buy size/dev-wallet funding, in-block position, metadata, real-time order flow, maybe whitelists of known
   serial launchers). Logistic baseline PR-AUC 0.0157; so nonlinear interactions matter.
4. **No selection-vs-random control exists in the repo.** The needed baseline (enter ALL, or a random 0.1% sample of, June deployments with the same alpha=0.5 fill and
   6 s exit and the same fees) is never reported. Without it, "selection adds X dollars" is unmeasured; the replica's profit could be mostly "any
   launch bought mid-first-second beats the cost" or mostly "deployer-quality tokens". The authors' own wording concedes: "we do not assert that our
   selection model beats the bot".
5. **Independent corroboration from other notes (note 13) [R in those repos]:**
   - smile-sk/pump-sniper: buy at create with a 1.5 s delay model, 1,431 tokens, win 10.5%, -8.74%/trade, CI [-10.1, -7.3]. A token selection signal on dev-buy size
     is real (p<0.001, 32% reach 1.5x for 0.05-0.3 SOL dev buys) but still -7.9%/trade net. = selection without speed loses.
   - repwarrior copybot: 2 s copy delay -103.8 SOL on 449.5 SOL deployed, 13% win; wallets' entries overpaid 16-23% at 2 s / 20 s.
   - charllysb live: 1-3 s confirmation latency turned a positive simulator into a negative live account.
   - Pine Analytics via note 13: up to 1.75% of launches are dev-funded sniper manipulation, 85% of those wallets sell within 5 minutes (adverse selection for first-block buyers).
   These all point the same direction: the information content of "which launch" is not enough to pay ~15% round-trip friction unless you are first.

**Verdict [I]: the edge is primarily positional (speed), conditional on a cheap pre-filter.** Speed supplies the fill at the start of the spike; the
deployer-history filter chooses which of ~28k daily launches to spend $27 racing on. Both are necessary: speed without the filter pays $27 x 28k; the filter
without speed buys at the top of the spike. If forced to apportion: speed is the necessary condition (the authors' 1.50 vs 0.92 fill-spread is 60% of a
multiple, while the best selection lift they could show is a classifier precision), selection is a cost-control layer (cuts the number of paid attempts by >99%).
The honest summary of the paper title: "a latency edge with a thin selection wrapper", and whether the wrapper is skill or just a whitelist of
deployers the operator has an arrangement with is untested (hypotheses below).

Mechanism hypotheses the repo does NOT test [I]:
- H1 pure infrastructure: shred-level or leader-near visibility of the create tx, same-slot landing after the create inside the block, sells into follow-on buyers
  (other snipers, copy bots) within ~6 s. Selection only by deployer signer (readable from the tx instantly, which also explains why deployer-history features are the
  only recoverable ones: anything else is too slow to compute at t0).
- H2 relationship/insider: bundle partner or affiliated wallet of serial deployers (dev knows when it will launch; first-slot allocation). Would explain the 0 s median, 78.8%
  gross win rate and why the best features are deployer history and repeat behaviour (4,095 deployers for 16,163 tokens = ~3.9 buys per deployer). A funding-graph check
  of the bot wallet against the deployers (note 11 holds funding-graph material) would discriminate. If H2, the strategy is not replicable by a third party at any price.

---

## 5. What the "replica" proves and does not prove

Mechanics [R, read in part3_backtest.py]:
- Entry: top 0.1% of GBDT test scores (threshold = 99.9th percentile of the TEST scores themselves, a mild in-sample choice) -> 853 candidates, 852 resolvable from candles.
- Fill: `entry = open + alpha x (close - open)` of the deploy second's 1 s candle (market cap), alpha = 0.50 calibrated so a passive 6 s hold on the bot's own June tokens
  reproduces the bot's observed median realised multiple 1.1153 (simulated 1.1099; neighbours 0.45/0.55 give 1.1357/1.0846).
- Exit: close of the candle at entry + 6 s. No ladder, no stop.
- Fees: flat $26.66 entry + 1.1% each side (+ $0.116) on the $183.42 median position.
- Fill probability: `0.85 x {1.0, 0.45, 0.20}` for delay 0/1/2 (reproduces 718/302/129 fills from 852). **Invented numbers, no measurement behind them.**
- Delay: converted to alpha with `alpha = 0.5 + (delay x 0.4 s) x 0.5 x 2` -> 0.90 at 1 slot, capped at 1.0 at >=2 slots.

Results: 0 slots +$29,142 (718 trades, net hit 56.0%, median ROI +6.9%, total ROI on deployed 22.1%, max DD $445); 1 slot -$334 (302 trades, hit 28.5%, median ROI -15.4%, DD $2,026);
2 slots -$883 (129 trades).

### Methodology critique (ordered by how much it moves the conclusion)

1. **The slot axis is not measured.** The mapping "0.4 s late = alpha 0.5 -> 0.9" is an invented linear map within a 1-second candle; it says a 400 ms delay traverses 80% of the remaining
   open->close path. The 1-slot and 2-slot median ROIs are identical (-15.4%) simply because alpha is capped at 1.0 (both fill at the close). The sensitivity *direction* (later
   = worse) is trivially true and corroborated elsewhere; the *magnitude* ("one slot kills it") is an artifact of the mapping. Real evidence would need slot-level trade data
   (note 10's windowopner sample has slot + intra-slot ordering, 32 minutes) or the 429 GB raw-block tier the authors skipped.
2. **"0 slot" in the simulation is the bot's own latency distribution, not "landing in the deploy block".** alpha = 0.5 is calibrated on the bot's actual entries (90.7% within the
   same second, i.e. a spread of 2-3 slots). Calling it "same slot" in the headline (and in note 13) overstates what is modelled.
3. **One free parameter absorbs fill, exit and selection (calibration circularity, authors partly admit).** alpha is solved so passive hold = realised result, so the bot's laddered exit
   and the bot's selection are credited to the fill. If the ladder contributes, the true fill is later (alpha > 0.5). Slope from the authors' table: ~-0.05 in multiple per +0.1 alpha. The
   replica's median ROI +6.9% (multiple 1.243) is therefore wiped out around alpha ~0.6-0.65 [D, approximate]. The mean (22% total) is more robust than the median, but the whole
   result sits inside the calibration's own error band, and **no CI or bootstrap is given for any replica statistic** (single month, 718 trades, no drop-top-N check; compare the
   standard in note 13 item 6 signal-backtest-harness).
4. **The replica shows a better gross edge than the incumbent from the same fill assumption.** Replica gross 39.7% of capital vs bot June 32.9%; median multiple 1.243 vs 1.115;
   at 85% fill. A 17%-precision model beating the bot per dollar is a red flag for the *fill transfer assumption*: alpha=0.5 learned on the bot's tokens is applied to tokens the bot
   mostly did NOT take (705 of 853). Tokens the bot skipped might be ones it could not get a good fill on, or whose first-second candle looks great precisely because of a late/ugly
   print. Fill quality is assumed independent of token; it is not.
5. **Candle resolution / candle construction.** 1 s market-cap candles omit seconds with no trade, "open" of the deploy second may be the dev's own first buy or the creation
   state; picking mid-path of such a candle is a modelling convention. The authors' own 1.50 vs 0.92 spread shows the answer is mostly the convention.
6. **Fee model inconsistency.** Writeup says costs are "~11% of position" (that is $26.66 / mean $263 + 1.1%); the replica charges the same flat $26.66 to a $183 median position
   (actual replica fees $32.3/trade = 17.6% of position). Not fatal (conservative for the replica) but shows the flat-tip assumption: a real bot likely scales tip with expected edge, and
   the bot's small $100 positions at $26.66 would cost 29%.
7. **Selection model data hygiene.** Positives' deployer history comes from `bought_deployers_activity` (709 MB, 4,095 deployers, 16k tokens) while negatives come from a separate
   `not_bought_*` extract (5.06M deployments, 177M events). Different extraction pipelines per class with a per-deployer 10,000-event cap that hits 5.7% of deployers holding 47.4% of
   activity: the sort of artifact that makes class-dependent feature distributions (hence `history_truncated` as a feature, a patch rather than a cure). The 4,095 deployers repeat across
   train and test, so the model can memorise "deployers the bot likes" - legitimate for copying a bot's whitelist, but then AUC 0.89 measures whitelist recovery, not skill.
   The shift test flags `secs_since_last` (2.02x); the authors keep it. Internal inconsistency: strongest single-feature AUC reported as 0.785 in WRITEUP/README and 0.769 in the log.
8. **Leakage handling is good on paper.** The frozen `TruncatedHistory` + `audit_truncation()` design, dropping `deploy_slot/deploy_time/neg_sample_scale`, the self-caught AUC=0.5000 bug,
   and the dropped-out-of-window negatives (1:318 -> 1:189) are all sound practice and worth copying. But an audit that checks timestamps cannot catch label-conditional sampling frames (item 7).
9. **Incentive and verifiability.** It is a $1,000 Kaggle contest with a 100-point rubric; the narrative is optimised for the rubric (honesty is explicitly scored, "byte for byte reproducible" claims,
   a self-found bug showcased). None of that is a reason to disbelieve the Part 1 numbers, which are straight aggregations of an on-chain-derived feed. But the Part 2/3 story is the part where the
   marketing and the evidence diverge, and the raw corpus is not independently obtainable here (IP-address servers, not touched).
10. **Part 1 itself:** (a) net excludes infrastructure, failed-tx fees and possible sibling wallets; (b) 111 days, one regime; (c) no per-day series, no CI; (d) the data provider's `cost_usd` is
    trusted as-is; (e) SOL price converts gas to USD at a median rate, fine for aggregates.
11. **Staleness.** Data ends 06-30; today is 11-21. Note 10 documents a changed 2026 pump.fun fee regime (creator fees, cashback, mayhem mode, Token-2022). The bot's edge may have decayed
    or the venue economics changed; June's -28% net per trade is a hint, not a finding.

Net assessment of the repo [I]: Part 1 is high credibility and the single most valuable thing in it (an observed, fee-complete P&L of a real, profitable bot). Part 2 shows deployer history carries
selection information but does not recover the rule. Part 3 is a sensitivity illustration whose conclusion (latency dominates) is plausible and externally corroborated, but whose numbers (+$29,142,
-$334, "400 ms") should be quoted as "model-dependent, June only, assumed slot mapping, no CI", not as measurements.

---

## 6. What a newcomer can realistically replicate

| Layer | Replicable? | Why |
|---|---|---|
| The bot's PnL (same-slot sniping of selected launches) | **No, not as a newcomer on retail/public infra.** | Requires landing within ~1 slot of deployment, paying ~$27/attempt, against operators who already do. All evidence on 1.5-3 s latency (pump-sniper, copybot, charllysb, sentinel) is negative |
| The replica's +$29k | **Not credible as a target** | It is a model-dependent June simulation with an assumed fill; even taken at face value it is ~$1k/day at zero slot, and -$334 at the delayed fill |
| Deployer-history features as a filter | Yes (data: launches + deployer activity are derivable from chain; note 11's fingerprinter dump has creator reputation) | Value is as a *pre-filter* to cut paid attempts or reduce rug exposure; gives only a modest lift (precision 17% at top 0.1%) and no standalone edge at slower speed (pump-sniper: -7.9% even on the good dev-buy cohort) |
| The measurement stack (leak-proof features, fee accounting from own txs, alpha/fill calibration, slot sweep, overlap-with-incumbent) | **Yes, and this is the main transferable asset** | Cheap, and it would have caught most of the false positives catalogued in notes 01 and 13 |
| Landing-latency measurement of your own stack | Yes, first experiment | Decides everything: measure your own slot-delta distribution vs deploy slot at ~$20 positions before any strategy work |
| A different, slower, lower-friction strategy | Possible but unproven | Notes 10/13 show positive results only from survivor conditioning, same-slot landing, or single-window curve-completion replays; nothing there is a clean positive for a retail-speed operator |

Realistic newcomer outcome [I]: first replicate infrastructure parity (can you land in the same second as the deploy 90% of the time?), and only if yes, a micro-size live test. If the
answer is "median landing 1-3 slots later", the repo's own numbers say the same strategy yields ~zero gross and -15% net per attempt.

Simple break-even arithmetic for any fast-snipe design [D]:
`net per attempt = size x (gross_move - 2 x 1.1%) - tip`. At $183, tip $26.66: need gross_move > ~14.7% to break even. The bot's mean gross is 34.9% of notional, the replica's 39.7%.
Cutting the tip to $5 lowers break-even to ~5%, but the fill then slides later along the spike and gross falls faster than costs. The tip-vs-fill-vs-gross curve is the one thing nobody
in the folder measured; it must be measured on your own stack (checklist 1 and 2).

---

## 7. Cross-reference: how the pro bot differs from everything that loses in note 13

| Dimension | Pro bot 5brv79e | Typical public repo (notes 10/13) |
|---|---|---|
| Entry latency | ~0 s, same-second as deploy (90.7%) | 1.5 s model (pump-sniper), 2-20 s (copybot), 1-3 s live (charllysb), 20 min nursery (sentinel) |
| Hold | 6 s | minutes to 30 min to 24 h |
| Win rate | net 59.3% (gross 78.8%) | 10-36% |
| Payoff | avg win $117 / loss -$28 (4.2:1), bounded left tail | stops gap to -84% (sentinel), -100% rugs, paper ignoring LP pulls |
| Fee burden | 12.9% of notional, 37-41% of gross - and still profitable | 5-14% per round trip with no gross edge to pay for it |
| Selection | pre-trade deployer-history rule (weak alone) | LLM/filters on post-hoc features, hindsight survivorship |
| Evidence quality | fee-complete realised PnL from the chain-derived feed | paper fills ignoring impact, LP removal, failed landings |

The pro bot is the exception that proves the rule in note 13's executive summary: the only real positive is a latency-bound one, and its own authors show it vanishes when the fill is
slightly later.

---

## 8. Hidden costs and risks the repo cannot see [X / I]

- Failed transactions: priority fees on non-bundled transactions that landed-and-failed are paid but are not "buy" events. A spam-style lander pays this on top of the visible $26.66. Illustration (assumption, not evidence): +20% on gas = +$88k, net $938k -> ~$850k; +50% = -$220k. Direction certain, size unknown.
- Infrastructure and operator cost not in net (servers, feeds, dev time, key custody).
- Counterparty/tail risk: tokens with transfer hooks, Token-2022 extensions, mayhem mode or sell-restrictions at 6 s are bounded by size ($100-$727) but a stuck bag cannot be exited; 3 never-sold tokens suggest rare.
- Competition decay: rising fee share (36% -> 41%), falling gross/trade (-22%) from Mar-May to June.
- Venue/regime risk: a fee-schedule or curve-parameter change can erase a 12-13% friction budget overnight; pump.fun changed fee regime during 2026 (note 10).
- Operational: wallet draining, MEV on your own landing, relayer outages, SOL price (fee in SOL, PnL partly in tokens swapped to USD).
- Legal/ethics [I]: if H2 (insider/affiliated-deployer) is true, replication is both impossible and potentially problematic; a newcomer should not interpret deployer-based filters as a licence to front-run affiliated launches.

---

## 9. Professional operating model: checklist

Grounded in: the repo's good practices (leak-proof architecture, fee accounting measured from own txs, calibration against an observable, slot sweep, overlap reporting);
its failures (invented slot map, no CI, no control, no per-day series, class-dependent sampling); and the pattern across notes 01/10/11/13 (paper fills ignore LP pulls and stop gaps;
"edges" collapse under drop-top-N; selection on trailing leaderboards leaks; stop fills at -84%; flat 1% fee models flatter results).

### A. Infrastructure (gate: no strategy work until these are measured)
- [ ] **Landing-latency census**: log for every own transaction `{send_ts, send_slot, landed_slot, landed_index_in_block, lander (RPC/Jito/other), tip, priority, status}` and for every target event `{observed_ts, observed_slot, source}`. Compute own slot-delta distribution vs the target event's slot. Target before any capital: >=90% of fills within +0/+1 slots of the trigger *by your own measurement*, not by assumption.
- [ ] Data feed with known gap accounting (gRPC/shred or own full-node websocket with coverage table, like note 10's `connections` table); record `received_at` vs block time for every event.
- [ ] Dual submission path (bundle and plain) with per-path landing stats; tip policy tested as a function of expected edge, logged per trade.
- [ ] Immutable raw log of every attempt including FAILED/dropped (this is the data the pro bot's public feed lacks and the repo cannot see; it is the denominator of true cost).
- [ ] Wallet hygiene: hot wallet with a hard balance cap (<= few days of fee burn + max position x concurrency), separate treasury, automatic sweep of proceeds, key isolation, no shared RPC keys with research code.
- [ ] Environment parity: the live engine and the backtest engine call the same decision function (one code path), versioned and hash-logged per trade.

### B. Measurement (every claim carries these, or it is not a claim)
- [ ] Fees charged from the *measured* fee model of your own stack (priority + tip + venue + exit + failed attempts), per attempt, never a flat percentage. Report fee share of gross every day.
- [ ] Fill model calibrated against an observable of your own live trades (the repo's alpha trick is the right idea, but calibrate on **>1 observable** - fill price, hold-time multiple, and exit ladder separately - so fill and exit are not confounded as in section 5.3).
- [ ] Slot/latency sensitivity from **slot-resolution** data (not an assumed mapping inside a 1 s candle). If sub-second data is missing, label the output "ordinal only".
- [ ] A **null/control strategy** for every backtest: random same-count entries at the same fill, fee model and exit; report selection value = strategy minus control, per trade, with a CI.
- [ ] Uncertainty: bootstrap by day (block) for net/trade, hit rate, payoff; report drop-top-1%/top-10-trades PnL; report per-day PnL series and worst day/week; never a single-month point estimate.
- [ ] Leakage audit as code (frozen truncated-history object + audit assertion, as in the repo) PLUS a **sampling-frame audit**: identical extraction pipeline and caps for positives and negatives; train/test split by *entity* (deployer) as well as by time; negatives only from the active window.
- [ ] Threshold selection from train/validation only, never from test-score quantiles.
- [ ] Paper-to-live reconciliation: for the same trigger set, paper PnL vs live PnL, per-component (price, fees, missed fills). Divergence budget in the kill rules below. (Note 13: +1,180 SOL paper vs -0.55 SOL live.)
- [ ] Stop/exit realism: never model stops at trigger price on thin curves (sentinel: -18% stop filled at median -84%); exits priced from the post-exit book or the next trade, with partial-sell impact.
- [ ] Reporting hygiene: whole-window vs sub-window numbers always labelled (cf. the $938k vs $188k mix-up in note 13).

### C. Risk
- [ ] Position size cap set by curve depth / measured impact (the bot: $100-$727, median $183), not by bankroll; size-up only after measured slippage stays flat.
- [ ] Fee-aware sizing: do not take positions where fixed tip / size exceeds expected gross move (at $100 the bot's tip is 29% of position).
- [ ] Daily fee-burn budget and a daily net-loss limit tied to the strategy's measured daily volatility, not to the bankroll.
- [ ] Concentration: max concurrent positions, max per deployer, max per source; cap on exposure to tokens with extensions/freeze authority/transfer hooks (hard filters at t0).
- [ ] Never size on a distribution tail you cannot reproduce without the top N trades (cf. signal-backtest-harness: +23% EV vanished without one token).
- [ ] Regime/venue-change watch: fee schedule, curve parameters, program upgrades; auto-pause on schema or fee-field change.

### D. Research loop
1. Hypothesis written before data (pre-registration: universe, entry rule, exit rule, fee model, success threshold, the control, n required).
2. Frozen backtest with the control and CIs (section B); a single replay-day or single month never decides anything.
3. Shadow mode on live data with full landing simulation (no capital), compare paper vs shadow-live vs real fills.
4. Micro-live: smallest size that still pays real fees; target n >= 300-500 attempts before any statement about edge; compare to the model with the paper-to-live reconciliation.
5. Scale in steps only if the lower CI bound of net/trade is positive and the fee share is stable.
6. Weekly review: gross/trade, fee/trade, fee share, landing-slot distribution, hit rate, payoff, top-decile dependence; monthly: re-estimate fill model on the last 30 days.
7. Written post-mortem for every retraction (the repo's self-found AUC=0.5 bug and random-dropout bug, and signal-backtest-harness's lessons.md are good templates).
8. Keep an "artifact catalogue" (what looked like edge but was: stale market cap, bottom-wick fills, survivors, top-1 trade).

### E. Kill criteria (set BEFORE going live; numbers are suggested starting points, derived from the bot's observed ratios)
- **Edge decay**: rolling 300-attempt net/trade < 0 for two consecutive windows, or lower 95% CI bound < -10% of position. (The pro bot's own net/trade fell 28% between Mar-May and June, so a monitor should fire at much smaller moves, e.g. -25% vs its own trailing 60 days = investigate, -50% = halve size.)
- **Fee-share**: fees/gross > 50% for 3 consecutive days (the bot was 36% then 41%) -> reduce tips/attempts or stop; > 60% -> stop.
- **Landing**: share landing within +1 slot of trigger falls below the level at which the backtest still shows positive net (measured, per section B) - e.g. below 70% -> pause.
- **Paper-vs-live gap**: live net/trade more than 5 percentage points of position below shadow/paper for 200 attempts -> stop, find the missing cost.
- **Failed-tx cost**: failed attempts' fees > 15% of total gas -> redesign submission path.
- **Tail dependence**: net PnL turns <= 0 after dropping the top 1% of trades in any rolling 30-day window -> the edge is a lottery; stop scaling.
- **Capital**: cumulative drawdown from peak > 3 x average monthly net, or > 30 days of fee burn with no net profit -> stop and post-mortem.
- **Structural**: any venue fee/curve/program change, or a data-feed gap > X minutes, auto-pauses; resume only after re-calibration.
- **Time-box**: if after N weeks / n attempts the landing census (A) does not reach the required slot distribution, the strategy is closed, not "tuned".

---

## 10. Bottom line

- The bot is real and profitable by the repo's own fee-complete accounting: $937,925 net over 111 days, **not** in June alone; June net $188,084 at 57.7% net hit rate and 41.2% fee share.
- What it does: ~146 launches/day bought in the first second, $100-$727 (median $183), flat ~$27 entry spend (57% priority fee / 43% Jito tip), ~1.1% fee per side, exit in ~4 ladder sells over ~6 s, near-zero exit gas.
- The profit distribution is a bounded-loss, ~4:1 payoff hump (median +4.7%, mean ~22% of notional), not a tail lottery; the profit per attempt is ~$58 and capacity-limited.
- Per-day stability is NOT documented; the derived June vs Mar-May split shows -28% net/trade and a rising fee share, consistent with decay but not conclusive.
- Edge = speed first (fill position inside the first second decides +50% vs -8% on the same token), selection second (deployer-history pre-filter; weak, rule not recovered, no random-control in the repo).
- Capital is small; the scarce resources are latency, a pre-filter that is cheap enough to run at t0, and the right to compete (possibly relationships, untested).
- The replica's headline is model-dependent (assumed fill-probability, assumed slot-to-alpha map, calibration confounding fill and exit, no CI, no control). Use it as direction, not as a number.
- For a newcomer, the replicable asset is the measurement stack and the operating discipline in section 9, not the trade.
