# 13. New public evidence: bot logs, paper-trading records, backtests (GitHub, Solana/EVM memecoins)

Date of search: 2026-11-21. Only GitHub was reachable. All repos were cloned with `--depth 1` into
`/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/datasets/<name>/repo`
and READ ONLY (no code executed). Already-held datasets were skipped.
Numbers marked "(recomputed)" were computed by me from the repo's own CSV; the rest are as reported by the repo author.

## Executive summary

Almost every honest, self-reported, cost-modeled result is NEGATIVE. The only positive numbers come from
(a) paper simulators that ignore liquidity removal or use survivorship-biased samples, (b) a competition replay
where the winning bot's edge is one rare event class (pump.fun curve completions), or (c) a signal-less
"price-path" analysis of a latency-dependent professional bot (+$29k if same-slot, -$334 if one slot late).
Recurring mechanisms: stops gap through (Sentinel: -18% stop filled at median -84%), paper fills ignore rug/LP-pull
(pumpswap-sniper: paper +1,180 SOL vs live -0.55 SOL), fees/tips eat 5-15% per round trip (pump-sniper),
and "positive" backtests collapse under drop-top-N / realistic-fill checks (signal-backtest-harness).

## Ranked catalog (most useful first)

| # | Repo | Type | n | Win rate | EV / PnL | Fees modeled? | Credibility |
|---|---|---|---|---|---|---|---|
| 1 | MuLIAICHI/sentinel | paper bot on live pump.fun, per-trade CSVs | 93 | 31% (26.3% / 34.5% cohorts) | -0.0027 / -0.0038 SOL per trade; -0.31 SOL total | paper fill engine, stops fill at observed price | High (raw CSV, self-kill, negative) |
| 2 | charllysb/pumpfun-momentum-bot | sim + live, no data files | ~370 per sim, ~90 live round trips | n/a | sim positive, live negative | 2%/side + slippage in sim | Medium (claims only) |
| 3 | pump-sniper (smile-sk/pump-sniper) | paper 12h, bootstrap CI | 1,431 | 10.5% | -8.74% of stake per trade, CI [-10.14, -7.32] | yes (1% platform, tips, 2% exit discount) | High (pre-registered, CIs; raw jsonl not committed) |
| 4 | erikjohnson181-code/solana-pumpswap-sniper | paper + live | ~3,000 paper tokens; 4 live; 21 graduation | 79% paper; 10W/11L grad | paper +1,180 SOL; live -0.55 SOL; grad +0.35 SOL/15 SOL | 1.3-2% round trip estimated for grad subset | Medium-High (honest about paper-live gap; no data files) |
| 5 | Somu2may/dexblocker-trading-bot | paper memecoin + futures | 5 Solana paper, 4 live-paper, 14 replay | 80% / 25% / 14% (IS) 43% (OOS) | +0.33% acct; mixed; negative | partial | Medium (explicit "red flags" proof pack, tiny n) |
| 6 | cudam321/signal-backtest-harness | research harness + lessons.md | many studies | n/a (judged by net PF, CI) | breakeven at best; every "GO" turned out artifact | yes (slippage, MEV, gas, dead tokens=total loss) | High (written post-mortems of own artifacts) |
| 7 | leex0x0/memecoin-paper-trader | daily-candle backtest, 9 tokens, 365d | 15-62 per strategy | 0-41% | all negative: -13% .. -72% | 30bps fee + 50-400 bps slippage + rug haircut | High but low frequency (daily bars) |
| 8 | maxmckittrick1-oss/memecoin-paper-bot | 30d backtest of 15 strategies + live equity sample | 5-1253 trades | 7-30% | all negative, best dip_buyer -3.8% vs hodl -6.7% | yes (Jupiter quotes) | Medium (established coins only) |
| 9 | diegosalinasrivera-lab/hl-memecoin-backtest | 15m perps backtest, 23 memecoins, HL 52d + OKX 12m, trade CSVs | 4,207 / 537 / 4,723 | 31-36% | -36% .. -100% | 0.035% taker + 0.03% slip per side | High (CSV outputs, robustness, 42-combo sweep, 0 profitable) |
| 10 | kokikkkk44/meme-scanner | paper trades CSV (live) | 447 closed | 35.5% (recomputed) | mean -13.9%/trade excl. 2 glitch rows | 1% fee per trade, no real slippage | Medium (raw CSV; contains 2 impossible rows) |
| 11 | andreolf/memecoin-paper-tracker | paper alerts (Telegram-style), pre-registered V2 | 20 pre-V2 + 6 V2 (560 filtered-out calls logged) | 25% (best) / 0% V2 | Strategy A -$4.92 / 20; D hold-24h -$185.89 | 0.45% fee + 2% slippage per leg | Medium-High (alerts.csv public, pre-registered exits) |
| 12 | sachinbatra1971-byte/memecoin-research | data collector + backtest scorecard, Pump graduation | 128 coins (scorecard), 797-999 coins with 26h minute prices | 59% (A, hindsight) / 55% (as-seen) / 49% (no filter) | positive in INR 1,000 units | 2% charges, 1-min close fills | Low-Medium: author flags hindsight/survivorship; only 8-17 days |
| 13 | solana-sniper-reverse-engineering (Foreist) | reverse-engineering of real bot 5brv79e... | 853 replica entries | 78.8% gross / 59.3% net (the real bot) | real bot net $937,925 (gross $1.49M, fees 37%); replica +$29,142 at 0 slots, -$334 at 1 slot | yes (measured) | High (Kaggle submission, leakage audit); latency-bound |
| 14 | make.fun `memecoin-backtest-48h-01` entries (4 repos) | replay of real pump.fun chain data, official/engine-matching grader | 176 fills etc. | 67% (one) | see below | engine fees, 2% failed-order draw | Medium (dev window only, fragile per own stress tests) |
| 15 | Positano777 / ghostfill / hillwire / yksanjo pumpsniper / Memcoin-Sniper-Bot / BetterCallTrader / grok-memecoin-desk / pump-sentry / thetopham memecoin-alpha-bot / PersonalJarvis | bot code | - | - | no performance data committed | - | Not evidence (README screenshots say "none of the numbers are real") |
| 16 | OutBlade/memecoin-freqtrade-bot | Binance CEX memecoins freqtrade | none committed | - | no results | 0.1%/side | no evidence |
| 17 | oxg43/letsgo | actually sports betting, irrelevant | - | - | - | - | irrelevant |

## Details

### 1. MuLIAICHI/sentinel (strongest negative pump.fun paper log)
- Data: `docs/data/positions.csv` (93 rows, mode/status/entrySol/entryPrice/exitPrice/exitReason/realizedPnlSol), `excursion.csv` (55 rows, MFE/MAE price path of scalp cohort), `decisions.csv` (148 rows). `docs/POSTMORTEM.md` is the write-up.
- Funnel: 138,922 tokens seen -> 808 pass free filter (0.6%) -> 740 enriched -> 38 bought (cohort A).
- Rules: PumpPortal ws; nursery (A: ripen 20 min; B: 4 min); filter: age, bonding-curve window, top-10 holder %, dev-sold %, dev repeat-rugger, dead volume; LLM (Claude) BUY/SKIP; exits precedence kill > hard_stop > time_stop > trailing > TP.
  - Cohort A "Survivor": TP +80% (sell 50%), 25% trail, -35% hard stop, 45 min time stop. n=38, win 26.3%, net -0.101 SOL, EV -0.0027 SOL/trade, avg hold 7.1 min.
  - Cohort B "Scalp": TP +40% (sell 60%), 15% trail, -18% stop, 8 min time stop. n=55, win 34.5%, net -0.209 SOL, EV -0.0038 SOL/trade.
  - Combined 93 trades, 31% win, -0.31 SOL (~$23). Position size ~0.024 SOL (entrySol 0.02376).
- Key finding: hard stops (-18%) filled at median -84% (17/17 gapped); 0/38 reached 5x, only 2/55 reached 3x; ~84% of entries faded to ~1.0x; entries at 20 min were after the price peak 72% of the time. Winner/loser features statistically indistinguishable (curve %, top10, dev-sold). Three "fixes" (tighter filter, tighter stop, TP ladder) all negative.
- Fees: paper fill engine; stops filled at observed price (not optimistic). 9 days, one regime. Credibility: high for direction, small n.

### 2. charllysb/pumpfun-momentum-bot
- No data files. README: two sim runs of ~370 trades each; positive without friction, still positive in v2 at 2%/side friction; LIVE negative (~90 round trips, account turned over 7x; +24% in first 4 min then given back). Cause: 1-3 s confirmation latency; tokens that rose +827% on chart still closed at a loss. Useful as qualitative evidence that sim edge dies at execution.

### 3. smile-sk/pump-sniper (RESULTS.md, STRATEGY.md in Russian)
- 12 h VPS (Frankfurt) paper run 03-04 Nov 2026, 1,504 tokens heard, 1,431 with trajectory. Data files (`data/paper.jsonl` 47.6 MB) are NOT in the repo, only the summary.
- Rules: buy at pump.fun create event with 1.5 s delay model, flat ~0.055 SOL stake; ladder exit 50% at 1.5x, 25% at 2x, 25% to 3x or 30-min timeout; stop on remainder 0.7x.
- Result: wins 150 (10.5%), stops 340, timeouts 1,046; PnL -6.879 SOL = -8.74% of stake per trade, bootstrap 95% CI [-10.14%, -7.32%]; both halves -8.85% / -8.63%.
- Outcome stats of price peak after entry: median x1.00; >=1.5x 13%; >=2x 8%; >=3x 4.7%; >=5x 2.6%; >=10x 0.8%; only 5/1431 (0.3%) graduated.
- Fees: 1% platform each way, 0.0001-0.001 SOL tip per tx (3.2 tx/trade) -> -8.7% to -13.9%; entry premium 1-2% -> -9.7/-10.6%. Cohort by dev initial buy: dev-bought 0.05-0.3 SOL gives median peak x1.23 and 32% reaching 1.5x (selection signal real, p<0.001) but still -7.9%/trade net.
- Credibility: high (pre-frozen rules, CIs, sensitivity), "no edge, pump.fun closed".

### 4. erikjohnson181-code/solana-pumpswap-sniper
- ~5 days Sept 2026. Paper: direct PumpSwap pools ~3,000 tokens, +1,180 SOL (+2.1% per SOL cycled, 79% winners); GeckoTerminal-polling control +520 SOL (+1.2%). Live real SOL: -0.55 SOL on 4 tokens (3 had LP pulled within a minute). Direct launches ~95% rug. Restricting to operator-run Pump.fun graduations (LP burned): 21 tokens, 10W/11L, +0.35 SOL on 15 SOL cycled (+2.3%), "statistically thin".
- Rules (v3): dip entry >=1% below the 20 s high, TP 3% verified against executable quote, crash abort at -35% from peak, max hold; round trip cost 1.3-2% at 0.2 SOL clip; pricing from vault balances at `confirmed`.
- Lesson: paper simulator blind to liquidity removal inflates results. No trade CSVs in repo.

### 5. Somu2may/dexblocker-trading-bot (`results/` proof pack)
- `solana_local_positions.csv` (5 closed paper positions, 80% wins, account +0.33%), `solana_local_fills.csv`, `solana_replay_grid.md` (687 tokens / 67,014 feed trades, 26-27 Oct 2026; current config in-sample 7 trades, 14% win, -38.9%/trade; OOS 7 trades, 43% win, -9.7%/trade), `gmgn_meme_reported.md` (4 live-paper trades, 25% win: GIGAHUG +0.22%, BTC-clone -22.8%, SLINGOOR -13.5% twice), `bsc_paper_summary.md` (BSC, 3,753 pairs seen, 0 trades). Also futures backtests (all negative, e.g. hf_maker PF 0.76, -91.8%; donchian_15m PF 0.74).
- Rules gmgn_meme: gates on liquidity/holders/RugCheck/GMGN, 1h momentum entry, stops ~-20%, time stop; 0.15 SOL replay size. Credibility: author lists what is missing; n tiny; the "red_flags.png" checklist is notable.

### 6. cudam321/signal-backtest-harness (`tasks/lessons.md`, `scripts/stage*.py`)
- Measurement-first harness for Telegram signal channels and on-chain wallet copy-trading. No raw dataset in repo, but lessons.md documents multiple retracted "+EV" results:
  - copy-discovered wallets: OOS EV -22% (hold/moonbag) to -30..-38% across full pool; power-law tail (OOS max 99.6x, train 6316x) real but not per-wallet persistent (OOS >=10x rate 1.6% = baseline).
  - "buy_and_die" policy +23.1% EV was a single-token tail artifact (CI low -24%; +0.6% without top trade).
  - Bankroll sim by resampling with replacement showed $500 -> $5,000; honest single-pass: $500 -> $320 (5% size), $98 without the one lucky token.
  - Graduated-token-only regime: grad+24h entry OOS mean multiple 1.04 (~breakeven); pullback-buy "edge" (mean 2.6-4.4) was a bottom-wick artifact, realistic next-candle-high+5% fill -> 0.53.
  - Lookahead error in a channel+feature model initially showed OOS top-10% mean 1.63x.
- Fill model: latency, microcap slippage, venue fee, MEV drag, fixed gas both sides, dead token = total loss. Very credible as a source of "what looks like edge but isn't".

### 7. leex0x0/memecoin-paper-trader
- Daily OHLCV, 9 tokens (WIF, BONK, POPCAT, MEW, PNUT, BRETT, TOSHI, DEGEN, PEPE), 2025-10-28 to 2026-10-27; trade CSVs per strategy in `results/` (190 lines total).
- $1,000/token. fomo_baseline -13.4% (win 13.3%, 15 trades); dip_buy -14.2% (41%, 39); momentum_breakout -40.5% (22.6%, 62); ma_crossover -58.6% (10%, 60); buy_and_hold -71.7%.
- Costs: 30 bps fee + 50-400 bps slippage by liquidity + 150-300 bps rug-exit haircut. Established coins only, daily bars, one down regime.

### 8. maxmckittrick1-oss/memecoin-paper-bot
- 30d (2026-09-19 to 10-19) 1-min backtest on 6 established Solana coins (BONK, WIF, POPCAT, FARTCOIN, PENGU, MEW), $1,000 per strategy, Jupiter quote-based costs: dip_buyer -3.8% (20 trades, 30% win), hodl -6.7%, momentum_trail -13.4%, momentum -21.0% (22 trades, 18%), ma_trend -40.3% (86), ma_crossover -99.9% (1,253 trades, 7%). Halves reported separately. Files: `results/backtest_report_30d.txt`, `equity_sample.csv`. Lesson: flat 1% fee looked better than per-trade quotes.

### 9. diegosalinasrivera-lab/hl-memecoin-backtest ("tablero / odd-one-out", 23 memecoin perps, 15m)
- Hyperliquid 52 days: v1 4,207 trades, win 33.4%, 3x -96.3%; v2 filters 537 trades, 31.5% win, 3x -36.2%. OKX 12 months (35,039 bars): 4,723 trades, 36.2% win, 3x -97.4%; momentum variant 16,565 trades -99.9998%. Costs 0.035% taker + 0.03% slippage per side times leverage. 42-combination filter sweep: 0 profitable. Files: `output*/trades_*.csv`, `robustness_*.csv`, `sweep_filters.csv`. Perps on listed memecoins, not DEX launches, but a clean negative benchmark for rule-based mean reversion/momentum.

### 10. kokikkkk44/meme-scanner (Japanese README; GitHub Actions scanner, every 15 min)
- `data/paper_trades.csv` 460 rows (447 closed) 2026-10-04..10-20, `candidates.csv` 1,389, `screening_2026-10.csv` 41,485 rows, `tracking_report.md`, wallet copy-trade data (`copy_bt/`, `wallet_hunt/`).
- Recomputed: 447 closed, win 35.8% (35.5% excl. outliers); exits: stop 209, time exit 202, +30% TP 24, +100% TP 5, +50% TP 3; median -14.6%; two rows have impossible +9.8M% and +26.8M% (price glitch on Altruists/Gunner) so the raw sum (+$1.98M) is garbage; mean excl. those = -13.9%/trade, sum of USD (|x|<500) = -$394 on 445 trades (stakes ~$2-24).
- Rules (README): scored 5-tier candidates from DexScreener/Solana Tracker/RugCheck; stop -40%, TP1 +50% half, TP2 +100%, 1% fee per trade; later variants stop -20%/-25%. Tracking report: after exit the traded coins mostly fell 24h later (many -90%); on 39 trades a -50% stop with +25% TP gave +1.3%/trade pre-fee, -20% stop gave -5.0%.

### 11. andreolf/memecoin-paper-tracker
- `data/alerts.csv` (586 alerts: time, mint, mc, liq, age, bonding %, reason), `calls.csv`, `peaks.csv`. Pre-V2 20 real alerts at $10: A (sell all at 2x, -30% stop) -$4.92 / 25% win; B -$47.74; C -$79.64; D hold 24h -$185.89 (0% win). Pre-registered Rules V2 (from 2026-10-28): 2x or -20% stop, 0.45% fee + 2% slippage per leg: 6 trades, 0 wins (max multiple 1.1-1.65x, one NNN reached 16x after stop). Breakeven win rate ~21%.

### 12. sachinbatra1971-byte/memecoin-research (potential reusable data)
- Large data: `data/candles/` 17 day-folders with ~2,486 per-token 1-min `.csv.gz`, `tracked.csv`, `safety/`, `snapshots/` (51 MB), `research/analysis/*.md`, `daily_scorecard.md`. Pump graduation (PumpSwap) coins.
- Rules: buy INR 1,000 at minute 15 after graduation; filters liquidity >= $30K, Twitter link, mint/freeze revoked, LP locked >= 95%, top-10 <= 30%, holders >= 300, mcap $30K-$2M; stop -25%; Plan A sell all +60%; Plan B half at +100% and rest at +200%; 2% charges; fill at 1-min close.
- Reported: scorecard 128 coins A 59% win / B 45% (+INR 29k / 53k). Author's own reality check (14 Nov, safety as seen at entry, 98 coins, 6-13 Nov): A 55%, B 43%. Unfiltered 797 coins: A 49% win, avg INR 1,139 back per INR 1,000. Entry timing: 5-20 min equal, 30 min A 43%, 60 min A 33% (no edge). Warning in file: coins first seen by the collector 30+ min after graduation -> survivorship/hindsight. Fill-at-close assumption understates slippage. Treat as optimistic; useful as a dataset for graduation-based backtests (note: overlaps in concept with held graduation datasets, but has minute candles).

### 13. Foreist/solana-sniper-reverse-engineering
- Kaggle-style study of a real on-chain pump.fun sniper (wallet 5brv79e...). Real bot gross $1,488,270, 78.8% hit rate, fees $550,345 (37%), net $937,925 (59.3% hit, 4.7% median ROI), June 2026. Replica: +$29,142 net at 0-slot delay (56% net hit, +6.9% median ROI), -$334 net at 1-slot (400 ms) delay (28.5% hit, -15.4% median ROI). GBDT selector PR-AUC 0.0761 (15.5x baseline), ROC-AUC 0.891. Raw 83 GB corpus not in repo; the intermediate artifacts are on Kaggle (not reachable). Message: edge exists only for same-slot landing; retail latency loses. Fees: priority spend $26.66/buy, 1.1% venue fee, $0.116 exit gas.

### 14. make.fun `memecoin-backtest-48h-01` (replay/v2 of real pump.fun chain data, start 10 SOL, ranked by net PnL)
- gunrflxtion/makefun-memecoin-backtest: momentum-lite (age >= 180 slots, >= 4 buys of last 6 trades, net flow >= 0.25 SOL, reserves 19-80 SOL; TP +8%, stop -18%, trail -22%, max hold 900 slots). Official dev grade +0.5527 SOL, 176 fills / 88 coins, 67% win, max DD 3.84%. House pilots on same window: sniper -0.50, reversion -3.71, momentum -9.47, hold-cash 0, equal-weight -0.02. Stress over 20 rebuilt copies: median -0.76 SOL (fragile).
- WhoIsTyfur/makefun-memecoin-backtest-48h ("Curve trader"): enters curves with 39-60 SOL reserve, 40-120 slots old, >= 30 wallets; 45% equity/coin, hold to completion; ~+27 SOL net on the 24 h dev window (+24.7 with doubled fees, +5.0 without top 3 coins), DD 27%; hash-split halves +10.2/+16.9; an earlier version (+3.32 official) was dropped as overfit. Profit comes from curve completions ("a quiet day earns about nothing").
- Omrani7/memecoin-replay-bot: same bounty, Python; STRATEGY.md: only 7 of 1,222 coins completed on the dev window; 30-80 SOL reserve sprint entries, 1 SOL/position, max 5; dev window +8.03 SOL, DD 12.5% (5 completions at ~+2.2 SOL, 10 stopped at ~-0.33 each; break-even at ~1 completion in 8 entries); its two halves: -0.56 and +6.25 SOL; block surrogates 13 of 40 positive.
- yeziR4/memecoin-grad-bot: momentum into completion (reserve >= 55 SOL), no results.
- Credibility: engine-replay results single day (10 Nov 2026 03:30 UTC window), strongly regime/day dependent, fees modeled by engine. Not reproducible without the kit (not on GitHub).

## Cross-cutting facts useful for the main analysis
- Breakeven win rate at TP +100%/-20% stop with ~5% round-trip cost: ~21%. Observed live-like win rates: 10.5% (pump-sniper), 31% (Sentinel), 36% (meme-scanner), 25% (paper-tracker pre-V2) -> negative.
- Stop-loss realism: Sentinel -18% stop filled median -84%; do not model stops at trigger price on pump.fun tokens.
- Paper-vs-live gap: +1,180 SOL paper vs -0.55 SOL live (pumpswap-sniper) because LP pulls are not simulated.
- Per-trade friction on pump.fun: 1% platform fee each way + tips 0.0001-0.001 SOL/tx (3.2 tx per laddered trade) + 1-2% price impact: -5% to -14% per round trip (pump-sniper sensitivity).
- Positive results appear only with: survivor conditioning (graduated coins observed after the fact), same-slot landing, or single-day replay windows with a few completions.
- Graduated-only entry at +24h: OOS mean multiple 1.04 (signal-backtest-harness) -> breakeven, consistent with the 49-55% win/INR-1,139-1,190 per 1,000 as-seen results of memecoin-research before real slippage.

## Searched but no performance evidence (code only; READMEs state numbers are demo/not real)
alexvxonchain/ghostfill, alexvxonchain/hillwire, Positano777/pump-launch-sniper, yksanjo/pumpsniper, vineetdev02/Memcoin-Sniper-Bot, BetterCallDzuks/BetterCallTrader, golddexzy-create/grok-memecoin-desk, sembraniteam/pump-sentry (journal/replay tool but no journal committed), thetopham/memecoin-alpha-bot (wallet-vetting JSONs only: 115 Dune wallets vetted, 24 keep/16 probation/75 reject; no PnL), HawkeyNL/PersonalJarvis, MyWestLord/petri and hexcat, ReDV101/pump-fun-copy-trader, Marketcap-cder/AI-Backtest-Strategy-G-1, Somu2may extra futures. Not cloned (unchecked): OnlyTerp/papertrench (cloned, 97 MB, tool not a results repo), dexterm-xyz/dexterm, farfary/ScreenerBot, B3an-boi/Kraken, BasketDotRich/basket, kingvavasav/memecoin-paper, Hollylummen/solana-paper-desk.

## Limits
GitHub search is keyword-limited; code search returned few hits (paper_trades.csv in kokikkkk44/meme-scanner; paper_trades_log_OLD.csv in oxg43/letsgo was sports betting). Further targets could be found by searching `filename:paper_trades.csv`, `filename:journal.jsonl`, `filename:positions.csv` with pump/solana terms.

## Addendum: web search (WebSearch) and blocked hosts

WebSearch works (returns titles/URLs and snippets). WebFetch does NOT: every host tried failed DNS resolution
(not in the session's allowed network domains): dev.to, www.arxiv.org, web3.arxiv.org. Per the tool guidance I stopped
trying further hosts (not tried, presumably blocked too: forklog.com, finbold.com, kitemetric.com, ketchupjl.github.io,
gitbook, sbfc.sydney.edu.au, coingecko.com). Content below is from search snippets only (unverified, not fetched).

Leads found, none with a verifiable trade log:
- dev.to "My pump.fun bot makes $4000 a day, here are the 4 numbers" (dev.to/gengengen/...): claims backtest sweep of 270 combos; settings dev buy >= 1 SOL, TP +30%, SL -30%, 120 s hold. No sample size, period, or fees visible. Promotional, low credibility.
- Lookonchain/press (forklog, finbold, blockchainreporter, captainaltcoin, Oct 2024): "AI bot 100% win rate, +780.8 SOL ($129.5k) on 10 memecoins in 5 hours" - on-chain observation, tiny n, one position open, suspected insider trading. Not evidence of replicable edge.
- arXiv 2601.08641 (2026 preprint, multi-agent LLM memecoin copy trading, claims profits): methodology not checked; fetch blocked. Worth reading if arxiv becomes allowed.
- arXiv 2602.14860 (Pump.fun related study; contents not seen): snippet says activity spikes occur without improvement in average trader profitability. Fetch blocked.
- Pine Analytics (via beincrypto): up to 1.75% of Pump.fun launches manipulated by dev-funded sniper wallets; 85% sell within 5 min, 90% within 1-2 swaps - adverse selection for any sniper backtest assuming a fair first-block entry.
- kitemetric.com "Mastering Solana Sniper Bot Backtesting" / ketchupjl.github.io/backtesting: methodology posts; claim tight exits (TP 20/SL 10) give >70% win rate but low profit, loose exits (TP 200/SL 70) poor expectancy; buy/sell ratio filter 1.2 -> 1.6 helped more than TP/SL tuning (unverified).
- sol-bangers-only.gitbook.io backtest report docs: vendor docs; no data seen.
Conclusion: web search added no independent trade-log dataset beyond the GitHub finds; the GitHub results remain the primary evidence.
