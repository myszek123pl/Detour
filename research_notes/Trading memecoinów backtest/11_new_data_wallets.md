# 11. New public datasets: memecoin trader wallets (round 1)

Scope: wallet PnL histories, smart-money/KOL lists, copy-trading results, sniper/bundler labels, funding graphs (Solana, some EVM).
Already held and skipped: ian05012/solana-memecoin-dataset, Erin-Blockchain/solana-pumpfun-launches, Smurfetc/solana-memecoin-calls-dataset, Solid-Sea/pump-gold-dataset, launchtape-io/pump-fun-backtest.
Clones: `/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/datasets/<owner>_<repo>/repo` (inspected only with `python3 -I`; no repo code executed; `pg_restore` was used only as a reader on the dump).

Headline: genuinely free wallet-level datasets are rare. One is real and large (willho fingerprinter), one is a clean small copy-trading result (repwarrior), the rest are leaderboard snapshots. GitHub search was rate limited (30/min) so coverage is incomplete; see "Not covered".

## Tier A - usable for analysis

### A1. willho/fingerprinter-dataset (pg_dump) - best find
- Provenance: author's own capture of pump.fun launches via live data providers, PostgreSQL dump taken 2026-06-11. License: none stated (treat as all-rights-reserved; check before redistributing).
- Size: 224 MB dump in 3 parts (2.1 GB restored). Under the 1.5 GB cap as shipped.
- `wallet_token_positions`: 1,090,434 rows, 261,380 distinct wallets, 43,570 mints. Columns: mint, wallet_address, tokens_held, sol_in_total, sol_out_total, trade_count, buy_count, sell_count, first/last_trade_at, first_buy_price/at, most_recent_sell_price/at, average_exit_price, highest_exit_price, min_price, max_price, position_cycle, is_exited, is_bot, bot_reason, bot_confidence. Period of first_trade_at: 2026-06-03 00:31 to 2026-06-09 17:46 UTC (about 6.7 days).
- Other tables: `fingerprint_snapshots` (event-triggered per-token snapshots with 22-dim feature vector and top_holders_json), `tokens`, `creators` (rug/graduation rates), `rotations`, `token_outcomes`, `token_snapshots`, `sol_price_history`. The `trades_*` partitions and `wallet_reputation` are EMPTY in the dump (verified: zero rows), so there is no per-trade log.
- Enables: per-wallet realized PnL and win rate across tokens, wallet-level entry-price vs ATH, early-buyer (first_buy_at vs token discovery) analysis, smart-money scoring with strict time split (6 days is enough for a 4-day train / 2-day test), creator-reputation features.
- Quality issues: `is_bot` is false in all 1,090,434 rows (bot detection effectively unpopulated, despite columns). Positions are sol_in/sol_out totals only; open positions have no mark-to-market, so naive PnL treats unsold bags as zero value (biased down for holders, biased up for early sellers). Only tokens the collector tracked (survivorship toward tokens that passed its discovery filters; `deathbed_rotation` stops tracking). Snapshot features computed at capture time are fine, but `creator_reputation`/`pump_magnitude` in later snapshots can embed future info; use only rows at or before decision time. 6 days = one market regime. Restoring needs Postgres (or stream `pg_restore -a -t <table>` to COPY text as done here).

### A2. repwarrior/copybot-receipts - copy-trading result
- Provenance: author paper-copied 20 top Kolscan wallets for about 42 h (2026-10-25 to 10-27) with Jupiter quotes, 1% haircut plus 0.0005 SOL fee. MIT. Size 7.2 MB.
- `data/trades.csv` 1,916 rows (two variants, bot_2s and notify_20s): wallet_label, wallet, mint, wallet_entry_tx, opened/closed_utc, close_reason, sol_in, sol_out, fees_sol, pnl_sol, pnl_pct, entry_delay_s. `data/wallet_events.csv` 6,744 swaps/transfers of the 20 wallets with signatures, token_delta, lamports, detect_lag_s. `copybot.db` (SQLite, raw), `wallets.json` (20 wallets, source kolscan 2026-10-25), `report.txt`.
- Headline result: copying lost money (bot_2s -103.8 SOL on 449.5 SOL deployed, 13% win rate; notify_20s -83.9 SOL). Wallets overpaid about 16-23% median vs the wallet's own entry.
- Enables: realistic copy-lag slippage curve (2 s vs 20 s), wallet-event stream for lead/lag studies, calibration of copy-trade haircut in our backtest.
- Quality issues: paper fills (quotes, not landed txs); 42 h; one wallet list chosen from a trailing-PnL leaderboard (selection on past winners, so the test is out-of-sample but small); half the wallets sold tokens received by transfer (not copyable); positions unsold after 24 h force-closed.

## Tier B - wallet lists with rolling stats (snapshots, selection-biased)

### B1. nirholas/kol-quest (120 MB repo; proprietary "all rights reserved" licence - do not redistribute, local analysis only)
- `solwallets.json` (11 MB, GMGN capture 2026-03-09): lists by tag - smart_degen 128, launchpad_smart 135, fresh_wallet 134, snipe_bot 49, live 17, top_followed 125, top_renamed 128; KOL list 290; interceptor `walletsAll` 2,041 (KOL 410, sniper 49, fresh 592, top-dev 197, launchpad 199). Per wallet: realized_profit 1d/7d/30d, pnl, winrate, buy/sell counts 1d/7d/30d, avg_cost, pnl bucket counts (<-50%, 0..2x, 2-5x...), last_active, tags, follow counts. walletDetails/holdings are only 5 sample entries each.
- `bscwallets.json` (18 MB, same schema, BSC, 2026-03-09): 561 wallets (smart 84, KOL 154, sniper 26, fresh 100). Only EVM-ish find.
- `output/kolscan-leaderboard.json`: 1,304 rows, 472 distinct wallets, timeframes 1/7/30 d (profit in SOL, wins, losses, name, twitter). `gmgn-x-tracker.json`: 2,599 X accounts GMGN follows (not wallets).
- Enables: sniper/fresh/smart tag lists (labels from GMGN heuristics), cross-check with fingerprinter wallets (join by address), KOL set for event studies.
- Quality issues: single-day snapshot; stats are trailing windows measured at capture, so any backtest that selects "smart" wallets from these and tests earlier is leaky (look-ahead + survivorship, leaderboards show only winners). Tags are GMGN's black-box heuristics. No trade logs. Contains personal social handles: use addresses only, no profiling.

### B2. mwayers/memecoin-kol-tracker (61 MB, mostly node_modules; no licence)
- `kol_wallets.json`: 11 labelled wallets only; plus demo analysis and market-heat JSONs (2026-01/02). Low value; skim only.

### B3. KrypticNodes/solana_sniper_gmgn_kolscan_wallets (no licence)
- `gmgn_leaderboard_wallets.json` (text file, 4 category lists incl. "Launchpad SM"), kolscan leaderboard wallets, `wallets_formatted_*.json` (Jan 2026). A few dozen addresses; address lists only, no stats.

### B4. forgottenpeak/soulwinners (MIT, 3.4 MB)
- `data/df_ranked*.csv`: about 10-row examples with roi_pct, median_roi, x10/x20/x50/x100 ratios, median_hold_time, cluster/archetype, tier. Tiny; useful only as a feature-definition template ("56 elite wallets" claimed in README, not shipped).

### B5. joeypbrrr/cabal-watch (no licence, 1 MB) - funding graph (tiny)
- `data/wallets.json` 52 wallets (role, token % held), `funding.json` 9 funder-to-wallet edges (SOL amount, slot, signature), `bubbles.json` 2 tokens. Snapshot 2026-11-07. Self-warns that shared CEX withdrawals do not prove common ownership. Useful as a schema example and for validating a funding-cluster detector, not for statistics.

## Tier C - adjacent, not wallet-level
- TrenchAutopsy/exit-liquidity-standard (MIT code, separate data licence file): sample of 4 tokens with ~10-min archive snapshots (2,733 rows), multi-horizon fate labels (6h-7d) and 2 tokens of pool-depth series (810 rows), June-July 2026. Tiny sample but unusually careful labels (NULL discipline, gap flags); good schema model for "tradeable exit" labels.
- travismoss1986-bot/solana-wallet-labels: advertises sniper/dev/smart-money labels but `labels.csv` and `pumpfun_labels.csv` contain headers only (0 rows). Empty; skip.
- Code-only (no data shipped, not cloned or no data found): karidasd/find-the-insiders, RachitSrivastava12/dec-clust (cluster dashboard; mostly node_modules), AtlasOnchain/Atlas, 2582552544-gif/memerecall, nischayhegde/solana-copytrading-backtester, yuno-research/solana_copy_trading, vybenetwork/solana-*-api, CabalSpy SDKs (API clients; the KOL data itself is behind an API), nirholas/scrape-smart-wallets (console scrapers).

## Web search findings (WebSearch worked; WebFetch did not)
- Blocked hosts for fetch (DNS fails, "outside allowed network domains"): madeonsol.com, huggingface.co. Not bypassed. The coordinator may need to allow them to follow up.
- Leads seen only in search snippets, unverified:
  - MadeOnSol datasets: "sol-smart-money" about 1.25M scored wallets (win rate, PnL, ROI, bundle rate, bot confidence) from 2026-04-12, paid (EUR 149), with a claimed free 5,000-row sample; also a paid KOL trades set. Needs madeonsol.com allowed to confirm the sample.
  - MemeTrans (arXiv 2602.13480; repos git-disl/MemeTrans and HailemariamMersha/MemeTrans already cloned in scratchpad by another task): 41k launches, 200M+ transactions, 122 features incl. bundle stats; labels are per-launch risk, not per-wallet. Should be reviewed by whoever owns those clones.
  - Hugging Face: `zirobtc/oracle` (collator_dump.json: per-event wallet, trade direction, is_bundle flag), `jackendoe/Pumpfun`, `muhammetakkurt/pump-fun-meme-token-dataset`, `Pumpdotstudio/pump-fun-sentiment-100k`. All need huggingface.co access to evaluate.
  - Bitquery pump.fun Parquet samples (host not tested).
  - Apify GMGN scrapers and Nansen labels: paid or API-only; not datasets.

## Not covered / next steps
- GitHub search rate limit (30/min) was hit; later queries (Base/BSC/ETH smart money, sniper lists, dune exports, funding graphs, wash trading) returned almost nothing, so absence is weak evidence. Rerun after reset with `search/code` for filenames like `wallets.csv`, `smart_money*.csv`, `pnl*.parquet`.
- No public Solana funding-graph dataset of useful size and no public sniper/bundler per-wallet label set was found; the only sniper/fresh labels are GMGN tags in kol-quest. Practical route: derive snipers/bundlers from the held trade datasets (first-slot buyers, same-slot multi-wallet buys) and use A1 as the wallet-position source.
- Recommended analyses: (1) A1 time-split smart-wallet scoring with out-of-sample follow rule; (2) A2 lag-slippage calibration; (3) B1 tag lists as weak labels, evaluated only on data after 2026-03-09.
- Scratch note: `/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/datasets/fp_work/db.dump` is the reassembled fingerprinter dump (224 MB), safe to delete.
