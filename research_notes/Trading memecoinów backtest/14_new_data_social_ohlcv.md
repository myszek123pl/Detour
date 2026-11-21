# 14. New public datasets: social/attention data and long memecoin OHLCV

Date of survey: 2026-11-21. Method: GitHub repo search (`gh api search/repositories`), `git clone --depth 1` into
`/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/datasets/<name>/repo`, inspection with `python3 -I` only (no repo scripts executed).
Row counts below were measured by me unless marked "(README)".

## Access notes
- Reachable: github.com (git clone), GitHub search API (hit the 30/min search rate limit once; recovered).
- Blocked (DNS `ENOTFOUND` from WebFetch): **huggingface.co, www.kaggle.com**. Not tried after the first failures (per policy): zenodo.org, arxiv.org, dune.com, coingecko, geckoterminal, dexscreener, X/Twitter.
- WebSearch worked (snippets only, unverified). Leads found that I could NOT download or verify (hosts blocked):
  - HF `ethers/twitter_ads_dataset` - tweets labeled as ads, many promoting paid Telegram memecoin call groups (contract addresses, call market cap, ATH). Highly relevant for an X-shill dataset; unverified size/license.
  - HF `Pumpdotstudio/pump-fun-sentiment-100k`, HF `jackendoe/Pumpfun` - titles only, contents unknown.
  - arXiv 2602.13480 MemeTrans (= the MELT dataset below, same 41k launches), arXiv 2601.22185 MemeChain (multimodal cross-chain meme coin dataset), arXiv 2412.04913 (34,988 memecoins across ETH/BSC/SOL), arXiv 2607.02823 (RED-PUMP-2026-v1, 860k pump.fun launches, Zenodo doi 10.5281/zenodo.20633486; CC-BY per smurf repo README).
- Not found on GitHub: any public dump of KOL tweets linked to memecoin prices, GeckoTerminal/DexScreener full OHLCV dumps, or a CoinGecko meme-category price history. Closest: MEXC daily set (below).

## Summary table

| # | Name | Social/attention | OHLCV | Size | License | Period | Verdict |
|---|---|---|---|---|---|---|---|
| 1 | Smurfetc/solana-memecoin-calls-dataset | Telegram call channel (SmugCalls) | peak multiple only | 3 MB | CC0 | 2026-06-30 to 2026-11-20 | Best clean call-event set |
| 2 | KrazySnipeOof/MEXC-data | none | 3y daily + 30d 1m, 322 memes incl. BONK/WIF/PEPE/FARTCOIN | 955 MB | none stated | 2023-06 to 2026-06-20 | Best large-cap meme OHLCV |
| 3 | hwlongCUHK/Coin-Meme | token descriptions (narratives), 223k pump.fun comments, logos | final mcap only | 456 MB | MIT | tokens created 2024-01 to 2024-11 | Narrative/attention cross-section |
| 4 | git-disl/MELT (MemeTrans) | twitter/telegram link flags + descriptions | SOL hourly only; tx on Google Drive | 43 MB | CC BY-NC 4.0 | launches 2024-12-09 to 2025-02-28 | Labels + metadata |
| 5 | ian05012/solana-memecoin-dataset | has_twitter/telegram, kol_buy_1h, tg_mention_count (~5%) | 272k 15m candles, 9.5M trades | 579 MB | MIT | 2026-06-10 to 2026-06-30 | Rich features, short window |
| 6 | sachinbatra1971-byte/memecoin-research | has_twitter, socials, GMGN top traders | 1m candles ~1,400 tokens, snapshots | 171 MB | none stated | 2026-11-03 to 2026-11-21 | Live-collected, growing |
| 7 | nikolan17/pumpfun-call-analyzer | 280 Telegram calls (channel, msg_id, time) | entry/peak/now mcap | 0.6 MB | none stated | 2026-04 onward | Small, daily-refreshed |
| 8 | Erin-Blockchain/solana-pumpfun-launches | none | first-15m features + 5h peak | 15 MB | CC BY 4.0 | 2026-07-27 to 2026-09-25 | Launch microstructure |
| 9 | Solid-Sea/pump-gold-dataset | none | per-token pmin/pmax | 73 MB | unclear (NOASSERTION) | unknown | Labels only |
| 10 | SystemsLab-Sapienza/pump-and-dump-dataset | Telegram P&D events (1,110 rows) | script to fetch Binance data | 35 MB | MIT | 2018-2020 | Analogue event study (not memes) |
| 11 | Bayi-Hu/Pump-and-Dump-Detection | 516 Telegram channel raw pickles, 1,335 P&D logs | Binance kline collector (no data) | 1.3 GB | none stated | 2019-01 to 2022-01 | Telegram call-to-price template |
| 12 | SystemsLab-Sapienza/gme-pump-xrp-telegram | full Telegram group HTML export | none | 153 MB | none stated | 2021 | Language/timing study of a pump group |
| 13 | rippere/Memecoin-Sentiment-Analyzer | Reddit/TikTok pipeline | CoinGecko snapshots | 1.7 MB | none stated | 2025-11 | Pipeline only; data is trivial (25 rows) |

## Detailed entries

### 1. Smurfetc/solana-memecoin-calls-dataset (clone: `sol_calls`)
- 12,988 rows in `calls.jsonl`, 12,988 distinct mints, period 2026-06-30 13:24 to 2026-11-20 01:26 UTC. Hash anchored via OpenTimestamps (`attest.json`, `.ots`) - tamper-evident, the author claims losers are kept.
- Fields: `mint, sym, t` (unix s), `utc, mc` (USD mcap at call), `peak` (max multiple after call, ratchet), `tg` (message no. in t.me/SmugCalls).
- README stats: median call mcap $12.8k; 36.7% reach 2x, 21.9% 3x, 11.3% 5x, 4.7% 10x. Single channel (the dataset publisher's own), so selection and promotion effects are likely; `peak` has no time-to-peak and no path.
- Enables: event study of "call -> return" if joined with own OHLCV (GeckoTerminal) keyed by mint+`t`; base rate for peak-multiple distribution; test of whether a call's market cap at call predicts peak. Quality: high format quality, poor generality (one channel, bonding-curve-stage calls).

### 2. KrazySnipeOof/MEXC-data (clone: `mexc_data`)
- 548 daily files / 322 one-minute files across 326 symbol folders (`<SYM>USDT data/`), 139,437 daily rows total, 13,871,750 1m rows total. Semicolon-delimited, no header: `YYYYMMDD HHMMSS;open;high;low;close;volume`.
- Daily: up to 3 years to 2026-06-20. Verified: BONK 1,095 days from 2023-06-22; PEPE 1,095 from 2023-06-22; WIF 915 from 2023-12-19; FARTCOIN 608 from 2024-10-21. Also DOGE, SHIB, BOME, MOG, POPCAT, PNUT, TRUMP present. 1m: last ~30 days only (e.g. WIF 42,961 bars in 2026).
- Universe: CoinGecko meme-category union (~20 categories) intersected with MEXC USDT spot; ticker heuristic, some false positives possible; manifests list failures (several symbols have "0 candles").
- No license file; derived from MEXC public API (check MEXC terms before redistribution). Quality: good for large-cap/CEX memes; no on-chain DEX tokens, no social data.
- Enables: cross-sectional meme-basket momentum/reversal, BTC/SOL beta, lead-lag among BONK/WIF/PEPE/FARTCOIN, volatility regimes, as the price leg for any attention series. Daily only for events older than 30 days.

### 3. hwlongCUHK/Coin-Meme (clone: `coin_meme`)
- `destription+finance.csv`: 3,751 tokens (3,752 lines with header) created 2024-01 to 2024-11 that migrated to Raydium. Fields: `token_name, token_ticker, token_address, description, mCap, createdAt, bonding_completeTime`.
- `comments.csv.zip`: ~223k lines (some multi-line comments) with `user_name, comment, time_posted (date resolution), likes, comment_id, token_address, token_name, token_ticker`. Ten image zips (~230 MB logos).
- License MIT (WWW'25 paper). Caveat: survivor bias (only migrated tokens); mCap is a single snapshot; comment time is date-only.
- Enables: narrative clustering (text -> theme -> later cohort performance), comment-count/likes as attention proxy vs mcap and time-to-bond; no OHLCV, so no intraday lead-lag.

### 4. git-disl/MELT / MemeTrans (clone: `melt`)
- `data/memecoin/memecoin_list.jsonl`: 46,139 launches (token_address, signature, timestamp, creator), 2024-12-09 to 2025-02-28. `metadata.jsonl`: 29,557 rows incl. name, description, imageUrl, twitter (18,856 non-null), website, telegram (6,512 non-null). `data/label/label.csv`: 41,471 rows (`mint_address, min_ratio, manipulated, return_ratio, label`). `data/feat/sol_hourly.txt`: SOL hourly price. Prediction CSVs in `results/`.
- Raw/parsed transactions (>1 TB raw; pre/post migration zips) are on Google Drive - not reachable here.
- License: CC BY-NC 4.0 (non-commercial; keep research-only). Enables: labelled high-risk launches, social-link presence as a feature (Twitter handle presence: 64%), join with own price data via mint; no post tweets.

### 5. ian05012/solana-memecoin-dataset (clone: `ian`)
- Parquet: `tokens` 44,460 snapshots x ~80 features (checked columns include holder structure, `smart_buy_1h`, `kol_buy_1h`, `has_twitter/website/telegram`, forward max return labels 1h/6h/24h/3d), `ohlcv` 272,426 rows (token_address, ts, open, high, low, close, volume; 15-minute candles inside label windows), `trades` 9,500,565 wallet-level rows, `sequences` 506,628, `wallets` 11,817, `wallet_funding` 15,493.
- Window only 2026-06-10 to 2026-06-30 (~20 days), detection at graduation or on GMGN trending (selection effect: only trending/graduated tokens). `tg_mention_count` has ~5% coverage. License MIT.
- Enables: KOL/smart-money buy flow as attention proxy -> forward-return lead-lag (1h-3d); wallet-graph studies. Limits: short regime, GMGN-labelled "KOL", candles not continuous history.

### 6. sachinbatra1971-byte/memecoin-research (clone: `sachin`)
- `data/tracked.csv` 13,318 tokens (first seen 2026-11-05+); `data/snapshots/<date>/<HHMM>.csv.gz` 405 files, 432,516 DexScreener rows (fields: price, liq, mcap, vol m5/h1/h6/h24, buys/sells, chg, boosts_active, has_profile, n_socials, socials, ...); `data/candles/<date>/<mint>.csv.gz` 1-minute OHLCV for ~1,400 graduated tokens (2026-11-03 onward); `backfill/` 48,007 graduation timestamps plus ~7.6k result rows (price ratios at +5/10/15/20/30/60 min, RugCheck fields); `research/gmgn/top_traders_*.csv`; daily scorecard markdown.
- No license; research-only intent. Author warns of hindsight bias (coins first seen after minute 15). Growing dataset - re-clone later for more days.
- Enables: DexScreener boosts and social-link presence vs. post-graduation returns; entry-timing studies at minute 15-60. Short (about 3 weeks).

### 7. nikolan17/pumpfun-call-analyzer (clone: `call_analyzer`)
- `calls_detected.csv` 280 rows (channel, msg_id, mint, symbol, call_time_utc, msg_text; e.g. channel `devcabal`, 2026-04-30), `calls_analysis.csv` 280 rows (entry_mc, peak_mc, now_mc, peak_gain_pct, drawdown_pct, minutes_to_peak, pool addresses). Daily GitHub Action refreshes; raw OHLCV cached by script (not in repo clone).
- No license. Small but includes time-to-peak and drawdown, useful as a sanity check on #1. Tooling pattern worth copying: scrape public `t.me/s/<channel>` previews with no API key.

### 8. Erin-Blockchain/solana-pumpfun-launches (clone: `erin`)
- 28,327 launches, 2026-07-27 to 2026-09-25, CSV with `token, dev_wallet, launch_unix, price_15, best_price_5h, multiple, vol_5/10/15, trades_5/10/15, growth_*` etc. Gate: >=25 trades and >= ~$15k mcap at minute 15 (survivorship toward active launches). License CC BY 4.0. No social fields.

### 9. Solid-Sea/pump-gold-dataset (clone: `pumpgold`)
- `pump_gold_dataset_core.csv.gz` (80 MB): 1,306,082 tokens (per README), columns mint, buy/sell counts, unique wallets, total quote lamports, pmin, pmax, is_golden (>=10x, 0.25%), is_dead (<2x, 93.4%). Derived from a public Kaggle pump.fun trades set. License field ambiguous; labels only, no time axis in the file. Use only for base rates.

### 10-12. Telegram pump-and-dump corpora (non-meme but the only public Telegram-call-to-price corpora found)
- 10. Sapienza `pump_telegram.csv`: 1,110 events (symbol, group, date, hour, exchange), 2018-01-01 to 2020-12-31, MIT; groups listed in `groups.csv`; includes feature and labelled-feature directories; downloader script for Binance trades (not run).
- 11. Bayi-Hu: 516 raw Telegram session pickles (845 MB), `PD_logs_cleaned.txt` 1,335 samples / ~709 P&Ds across 108 channels (495 in 2019, 363 in 2020, 450 in 2021, 27 in 2022), columns channel_id, session_id, coin, exchange, pair, timestamp. No license file. 1.3 GB, under the cap.
- 12. gme-pump-xrp-telegram: HTML export of the "OFFICIAL BUY & HOLD XRP" group (2021), anonymised users. Needs HTML parsing; NLP of pump hype language.
- Use: event-study design (t0 = announced pump time; abnormal returns, run-up before announcement, insider front-running) to port to memecoin Telegram calls. Prices must be fetched separately (Binance klines).

### 13. rippere/Memecoin-Sentiment-Analyzer (clone: `rippere`)
- Reddit/TikTok VADER + hype-keyword pipeline correlating with next-day returns of DOGE, PEPE, SHIB, BONK, FLOKI, WIF. Only data file `meme_coin_data.csv` has 25 rows (CoinGecko snapshot, 2025-11). Code reference only; no usable dataset.

## Checked and rejected / not usable
- backtest-kit/signal-dataset: Telegram channel WallstreetQueenOfficial, 9,189 posts 2021-05 to 2026-09 and 921 LLM signals, but `messages.jsonl`/`signals.jsonl` are Git LFS pointers (about 420 MB, not fetched), and targets are Binance large caps (82 USDT pairs), not memes.
- agboolaOluwaseun/solana-tracker: Telegram caller backtest tool (cloned, 37 MB); contains code, eval/simulation CSVs of channel win rates (e.g. `eval_666.csv`), no raw call corpus checked in. Possible only as a result reference.
- diegosalinasrivera-lab/hl-memecoin-backtest: Hyperliquid 15m candles for 23 memes (DOGE, kPEPE, WIF, kBONK, FARTCOIN, ...) but only 52 days (2026-09-24 to 2026-11-15, API limit) and repo ships only outputs/code.
- willho/fingerprinter-dataset (428 MB clone): pg_dump (3 parts, ~224 MB compressed, ~2.1 GB restored) of ~39,000 pump.fun launches, snapshot taken 2026-06-11; event-triggered snapshots (price_2x/5x/10x, drawdown, discovery), not fixed-interval OHLCV; no license file; needs Postgres to restore (not done). Useful for trajectory/drawdown studies, no social fields confirmed.
- virusLuke3/MemeCoinDatasets: only API-call scripts and CoinMarket ID lists; no price/social data.
- whogotpump (duolaAmengweb3): tool for counting Twitter handles referenced by pump.fun tokens; no data in repo (MIT).
- Many tweet-sniper bots (rapidlaunch, memecoin-fast-trade, elon-sniper) are code only.

## What each enables (study ideas)
1. Telegram-call event study: #1 (12,988 calls) and #7 with own GeckoTerminal OHLCV by mint -> returns at +1/5/15/60 min after `t`; compare to matched non-called launches from #8/#5/#4 (same hour, similar mcap) to estimate call alpha net of slippage. Caveat: `mc` and `peak` are the channel's own; reproduce from OHLCV.
2. Pump-and-dump analogue (#10, #11): abnormal run-up before announcement vs post-announcement dump; port timing structure (hour-of-day, repeat groups).
3. Narrative/attention cross-section (#3 + #4): cluster descriptions (embedding), compare cohort outcomes (graduation rate, mcap); twitter/telegram link presence as binary attention feature (#4: 64%/22% of listed launches).
4. KOL/smart-money flow lead-lag (#5): `kol_buy_1h` and `smart_buy_1h` vs forward returns at 1h-3d; granger-style tests using 15m candles.
5. Large-cap meme lead-lag/momentum (#2): daily BONK/WIF/PEPE/FARTCOIN/MOG/POPCAT/TRUMP basket, regime and beta analysis over 2023-2026; no leakage across 30d 1m window.
6. DexScreener boost / social-link effect (#6): snapshots with `boosts_active` and `n_socials` against minute-15 returns.

## Gaps remaining (for the user's next steps)
- No public X/Twitter post-level data tied to memecoin prices found on GitHub; HF `ethers/twitter_ads_dataset` is the best lead but host is blocked.
- No long (>1y) DEX OHLCV for Solana memecoins; MEXC daily is the longest. For DEX history use GeckoTerminal API directly (blocked here).
- Most Solana sets are short windows (<=3 months) so lead-lag conclusions will be regime-specific.
