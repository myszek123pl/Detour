# 10 - New public trade-level datasets for Solana memecoins (GitHub sweep)

Date: 2026-11-21. Scope: GitHub only (repo search, code search, clone, raw). Already known and skipped: ian05012/solana-memecoin-dataset, Erin-Blockchain/solana-pumpfun-launches, Smurfetc/solana-memecoin-calls-dataset, Solid-Sea/pump-gold-dataset, launchtape-io/pump-fun-backtest.
Local clones: /tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/datasets/<name>/repo (data never executed; inspected with `python3 -I`).

## Bottom line

The GitHub-only universe of raw trade-level Solana memecoin data is very thin. Exactly ONE new repo ships real raw swaps: windowopner/pumpfun-trial-1 (30 min, 29,830 pump.fun bonding-curve trades with full reserves). Everything else is launch-level features, 10-minute snapshots, or summaries. There are no GitHub mirrors of Kaggle/Zenodo/HF trade datasets for PumpSwap, Raydium, Meteora or LetsBonk that I could find (searches for those venues return only bots/SDKs). The big upstream sources (launchtape full days at $10/day, Trench Autopsy HF archive, Avasis full dataset) are paid or not on GitHub.

## Ranking

| # | Repo | Trade-level? | Size | Usable for backtest |
|---|------|--------------|------|---------------------|
| 1 | windowopner/pumpfun-trial-1 | YES, raw swaps + reserves | 29,830 trades / 406 coins / 30 min | Execution-realistic launch-sniper / early-curve rules; AMM model validation |
| 2 | TrenchAutopsy/exit-liquidity-standard | No swaps; 10-min price/liquidity snapshots + 10-hour-scale vault reads | 2,733 + 810 rows, 6 tokens | Schema reference; exit-liquidity labels only |
| 3 | avasis-ai/pumpfun-launch-data | No; per-launch feature table | 7,430 launches, 37 cols | Sniper/bundle/rug-label features, graduation base rates |
| 4 | samuelmateo-dev/memecoin-radar (data/sample) | No; per-alert outcomes (anonymised) | 1,184 tokens | Statistical-test bench only; weak |
| - | Others (see "Rejected / blocked") | | | |

---

## 1. windowopner/pumpfun-trial-1  (best find)

- Path: .../datasets/windowopner-pumpfun-trial-1/repo ; file `pumpfun/samples/pump-sample.db.gz` (7.6 MB gz; SQLite). Repo total 17 MB. Upstream project is windowopner/pumpfun-sim (not cloned; not enabled for this session).
- Provenance: self-recorded via Solana public RPC websocket logsSubscribe on the pump.fun program, decoded with official IDL (CreateEvent / TradeEvent / Complete / CompletePumpAmmMigration). Author claims the market model reproduces 2,309,807 of 2,309,807 recorded trades to the lamport. Collector tracks covered slot ranges (`connections` table) so gaps are known.
- License: MIT (c) 2026 Sabu (code; the sample DB is in the same repo, no separate data license).
- Period of the sample: 2026-10-16 06:05:51 to 06:38:04 UTC (~32 min), slots 457,531,005-457,539,999. (README says the author's full run was ~22 h / 20,809 coins, but that DB is NOT published.)
- Tables (verified by opening the gz-decompressed DB):
  - `trades` 29,830 rows, 319 distinct mints, 4,374 distinct wallets, 17,249 buys / 12,581 sells. Columns: signature, event_index, slot, timestamp (unix s), received_at (local float s), mint, is_buy, user (wallet), ix_name (buy, buy_exact_quote_in, buy_exact_sol_in, sell, multi_hop_swap), quote_mint, sol_amount, quote_amount, token_amount, virtual_sol/quote/token_reserves, real_sol/quote/token_reserves (post-trade, so a full price path), fee_basis_points, fee, creator_fee(_basis_points), buyback_fee, mayhem_mode, creator, cashback_fee_basis_points, cashback.
  - `coins` 406 creates (name, symbol, uri, bonding_curve, creator, initial reserves, mayhem/cashback flags). `lifecycle` 25 rows (CompleteEvent + CompletePumpAmmMigration = graduations with pool address). `connections` 1 row (slot coverage 457,531,000-457,540,000).
  - Longest tape: 2,511 trades on one mint; 67 mints have >=50 trades.
- Price path: exact (virtual reserves after every trade); slot-level ordering, wallet IDs, fees, creator fee/cashback flags (new 2026 pump.fun fee regime: includes mayhem mode, cashback coins, Token-2022).
- Quality issues:
  - Only 32 minutes: no regime diversity; coins born late in the window have truncated paths (right-censoring), and coins born before the window are partially seen (406 creates vs 319 traded mints; trades of coins created earlier are absent from `coins`).
  - Intra-slot order is NOT in the RPC stream; the author reconstructs it by chaining reserves (works for normal coins; sample stores event_index only).
  - Public-RPC stream noise (all-ones signatures for failed trades filtered by the collector; possible silent stalls; gaps recorded only coarsely in the sample).
  - U64 columns are stored as BLOB-typed integers (check sqlite typeof before arithmetic).
  - Survivorship: none by construction (all creates in window recorded), but only 25 graduations -> too few for graduation-outcome stats.
  - Pump-only; no PumpSwap post-graduation swaps, no Raydium/Meteora/LetsBonk.
- Enables: realistic latency/slippage sniper replay on the true curve (the repo's own engine does this), buy-after-N-trades momentum on bonding curve, wallet-cluster/bundler detection in first slots, bot-density statistics; also a unit-test fixture for any curve-math implementation. Too small for parameter fitting; use as a validation harness and as a schema template for what to collect ourselves. The repo's collector (pumpfun collect) is the practical route to get more: it needs only a public RPC websocket.
- Reported strategy results in README (22 h run): launch_sniper 14,568 entries, win rate 4.1%, median -4.5%, PnL -97.3 SOL (-44 SOL before costs); random baseline -114.9 SOL. 30% of launch entries fail on slippage. Useful prior: naive launch sniping is negative EV.

## 2. TrenchAutopsy/exit-liquidity-standard

- Path: .../datasets/TrenchAutopsy-exit-liquidity-standard/repo (912 KB). License: code MIT, data CC BY 4.0 (LICENSE-DATA).
- Provenance: exported 2026-08-02 from the author's production DBs; deterministic exporter (ORDER BY mint LIMIT n) so it is a convenience slice, not a random sample.
- Content (sample/): archive_observations.csv 2,733 rows (mint, observed_ts, is_found, price_usd, market_cap_usd, liquidity_usd, volume_24h_usd, fdv_usd, pair_address, dex_id; ~10-min grid from DexScreener-like source), archive_labels.csv 14 (6h/24h/72h/7d liveness, 2x/5x/10x crossing, tradeable-at-cross, realizable_return, max_drawup/drawdown), archive_tokens.csv 4, flow_depth_series.csv 810 (direct pool quote-vault reserve reads, 2 tokens), flow_depth_labels.csv 2. Dates June-July 2026; dex_id includes pumpswap and meteora.
- Claimed full archive: 77M+ pool-state observations over ~32,400 launches + 21.8M direct reserve reads (to 2026-08-03), promised on HuggingFace under CC BY 4.0 as "M1" - NOT present on GitHub, and no swap-level data is released ("deliberately absent").
- Quality: only 4+2 tokens, hand-selected (DEAD and one ALIVE; flow lane selected to be DEPTH_DEAD with peak depth >$5k) -> heavily survivorship/selection-biased by design; price source is aggregator (reported liquidity gaps, e.g. 10-hour polling holes `max_poll_gap_s` 36,128 s). Labels computed with forward windows from t0 (fine) but resurrection flags use future info (label-only).
- Enables: nothing statistically; valuable as a SCHEMA/definitions reference for exit-liquidity labelling (realizable return, depth floor $2,500) and to know that a HF dataset with 10-min pool snapshots across 32k launches exists (check if HF becomes reachable).

## 3. avasis-ai/pumpfun-launch-data

- Path: .../datasets/avasis-ai-pumpfun-launch-data/repo (1.5 MB): `pumpfun-launch-sample-20261030-20261105.csv.gz` (647 KB), SHA256SUMS, stats.py.
- Rows/cols: 7,430 launches x 37 columns. Deterministic 1-in-32 sample by md5(mint) of all pump.fun launches 2026-10-30 to 2026-11-05 UTC (7 days). Only 5,610 have launch-tape features (1,820 rows say `no_tape_features`).
- Columns: mint, symbol, creator, created_at, graduated_at (ms-precision UTC), initial_buy_tokens, creator prior launches/graduations, creator_sold_by_10m, pct_supply_first_2_slots, creation_slot_buyers, first2_slot_buyers, early_1s_buyers, serial_snipers, bundle_txs, bundled_wallets, bundled_supply_pct, shared-funder groups, name/symbol/image collisions, funding-cluster stats, top10_ex_pool_pct, verdict (SAFE/WARN/DANGER) + reason_codes.
- Stats (author): 49.3% of launches have a buyer within 1 s; 43.9% have a serial sniper; 2.27% graduate (169), median 36.4 s to graduate; verdicts SAFE 17.6 / WARN 50.9 / DANGER 31.5%.
- License: sample CC BY 4.0 (attribute "pump.fun launch data sample by Avasis (avasis.ai)"), stats.py MIT; full dataset/API licensed separately (internal use/research only, no redistribution).
- Quality / look-ahead: NO trades and NO price path - only graduated_at as outcome. Several columns mix future info: `top10_ex_pool_pct` exists only after graduation; `creator_launches/creator_graduations/cluster_*` are LIFETIME totals (include the future relative to created_at, contrast with the *_prior_ columns which are safe); `verdict` is computed from windowed tape and, for some rows, graduation-conditioned fields (check `verdict_basis`). Treat `*_prior_*`, `window_s`-bounded features, and `creator_sold_by_10m` as point-in-time-safe only after verifying window; lifetime and top10 columns as leaky. Sampling by md5(mint) is unbiased across tokens.
- Enables: base rates for graduation vs sniper/bundle features (graduation classifier or filter); sizing how much early-buyer toxicity exists; cannot compute returns.

## 4. samuelmateo-dev/memecoin-radar (data/sample)  - weak

- Path: .../datasets/samuelmateo-dev-memecoin-radar/repo (3.3 MB; README states MIT-style no LICENSE file found - license unclear, treat as unlicensed).
- `data/sample/outcomes.jsonl` 1,185 rows: mint, name ("Token 0001", anonymised), symbol, alertedAt (ms), score, entryMarketCapSol, peakMarketCapSol, peakAt, trackingEndedAt, multiple. Tokens tracked Sept 2026, 30-min tracking windows. `paper-trades.jsonl` 464 dry-run buy/sell events (real mints, entry mcap, multiple at sale, reason in French).
- Quality: only entry + PEAK (hindsight statistic) per token, no path; "multiple" is peak/entry, optimistic and not tradable; alert selection by author's score (selection bias); mints for outcomes are real so could be joined to other datasets for entry/peak cross-checks.
- Enables: just the repo's own permutation/bootstrap test bench; its negative finding (14 strategy ideas, none significantly >1.00x net) is a useful prior. Not a trade dataset.

---

## Rejected / blocked / not data

- launchtape-io/launchtape (toolkit, 472 KB) and marklavigueur-dev/solana-launch-tape (the actual dataset repo behind launchtape; "historical preview in the dataset repo remains public"): the toolkit documents schemas for CURVETAPE (every pump.fun bonding-curve trade from create to graduation, from 2026-10-12 18:16 UTC, recorded from public RPC), GRADTRADES (PumpSwap trades of graduates), PREGRAD, PADFEED, and graduates CSV; full days are paid ($10/day at launchtape.io, a non-GitHub host); the free 2-hour samples were withdrawn on 2026-10-14. NOTE: I could NOT clone marklavigueur-dev/solana-launch-tape: access to it was not enabled for this session and my add_repo request was denied by the permission classifier, so I did not circumvent it. Someone with permission should attach that repo (it may hold a public preview of curvetape/gradtrades, which would be the best PumpSwap+curve trade source). Schemas are readable in launchtape/src/launchtape/schemas/{curvetape,gradtrades,pregrad}.md. Caveat noted by authors: pregrad `minDrop` changed definition 2026-10-14 03:40 UTC (graduation-slot trades priced before the big buy inflated drops) - a look-ahead/definition trap if you buy those files.
- MemePudge/backtest-data-01: single 6.1 MB RAR5 file `20260603-160902Z` ("pumpfun trading data", first commit 2026-06-04, no README, no license). The archive is ENCRYPTED (libarchive: "Encryption is not supported"), with no password anywhere in the repo; also an unlabeled binary blob of unknown origin -> could not inspect; not recommended (also a possible malware vector). Left unopened beyond header parsing.
- WhoIsTyfur/makefun-memecoin-backtest-48h: strategy bot for a make.fun bounty (main.ts); the 48 h replay data is provided by the bounty host, not in the repo. No data.
- api-evangelist/pumpfundata: API profile docs only. No data.
- dynamolabs/launchpad-registry: registry of launchpad program IDs, IDLs (pump-fun, boop, raydium-launchlab, meteora-dbc), chains - useful as a reference to decode LetsBonk (Raydium LaunchLab) / Meteora DBC events; CC BY data license. No trades.
- mosn-agent/mosn-solana-mcp: marketing README + daily new-token report index; labeled dataset is a paid API ($0.25 per /dataset call). No raw data.
- gosadu/loophole-tape: MCP rug-check service code. No data.
- vybenetwork/solana-trades-api, solana-ohlc-api (171 stars): docs for a paid/keyed API (Vybe), no data. chainstacklabs/pumpfun-bonkfun-bot, pumpfun-cli, evolify/dumpfun, many sniper/copy-trade bots: code only (chainstack bot is a good reference for decoding pump.fun and LaunchLab events). TateLyman/pumpfun-shred-feed: live WebSocket feed code (shred-decoded pump.fun launches and curve trades, ~14 ms), no stored data. yuno-research/solana_car: Rust tool to extract swaps from Solana CAR archives (Old Faithful) - a possible route to build our own historical swap set, no data included. prisyy/pumpsim-api: bonding-curve/PumpSwap simulator API. Ed1sonL1-byte/solana-tx-to-ts-dataset: TS codegen. crossmeme-telegram-bots-dataset: bot-comparison table. TrenchAutopsy and avasis aside, no "Releases" assets were found: the releases API is not accessible for repos not attached to the session (403), so release assets of the candidates could not be enumerated.

## Search coverage (what returned nothing)

Repository searches (gh search/repositories) for: pump.fun trades dataset / swaps parquet / tick data / historical trades / transactions csv; pumpswap trades dataset; raydium swaps dataset; meteora dlmm swaps dataset; letsbonk dataset; raydium launchlab dataset; meteora dbc dataset; bonding curve trades; solana dex trades/swaps parquet; solana memecoin trades csv / ohlcv / price history; kaggle solana memecoin; huggingface pumpfun; rug pull dataset. Most returned zero or bot/SDK repos. Code search (rate-limited, secondary limit hit repeatedly) for `trades.csv`, `*.parquet`, `bonding_curve *.csv` found nothing relevant. No GitHub mirrors of Kaggle/Zenodo/HF datasets were located; the search API gave no hits for those names. Rate limits cut the code-search sweep short, so coverage of file-extension searches is incomplete: repeat later with `extension:parquet`/`filename:swaps` variants and topic searches (topic:pumpfun, topic:solana-dataset).

## Recommended actions

1. Use windowopner/pumpfun-trial-1 as the only immediate raw-trade source (validation harness, 30 min). Consider running its collector (public RPC websocket; needs Solana RPC egress, not available in this sandbox) to accumulate our own multi-week curve tape - existing public data is far too short for anything but sanity checks.
2. Get marklavigueur-dev/solana-launch-tape attached/approved and inspect any free preview there (curvetape/gradtrades).
3. Use avasis sample only for graduation/sniper base rates, dropping its lifetime/top10 columns to avoid look-ahead.
4. If HuggingFace/Kaggle become reachable: TrenchAutopsy HF archive (77M pool snapshots, CC BY 4.0) is the biggest promised free dataset.
