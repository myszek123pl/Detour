# 12. New public datasets: memecoin rugs / scams / pump-and-dumps / wash trading

Research date: 2026-11-21. Clones live in
`/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/datasets/<owner_repo>/repo`
(untrusted; nothing was executed, only `python3 -I` reads of data files).

## Network / access notes
- GitHub (API search, `git clone`) worked; the search API rate limit was hit once (secondary limit, recovered).
- BLOCKED (`getaddrinfo ENOTFOUND`, outside the session allowlist): **arxiv.org, zenodo.org, huggingface.co**. Not bypassed. They need to be allowed in session network settings to fetch: RED-PUMP-2026 (Zenodo), SolRugDetector / Catching the Rug / TM-RugPull / MemeChain papers and links (arXiv), HF dataset `Pumpdotstudio/pump-fun-sentiment-100k`.
- WebSearch worked (snippets only). Findings below that come only from search snippets are marked [snippet].
- Google Drive links in several READMEs (MELT raw tx, CoinVibe) were not tried (not GitHub).
- Skipped: `bigaflower/pacer-rugpull` (cloned size ~4 GB, over 1.5 GB limit, removed), `AhmedMahrous00/icbc_2026_reproducibility` (PumpSense, ~1.6 GB, over limit; not cloned), `Bayi-Hu/Pump-and-Dump-Detection-on-Cryptocurrency` (275 MB, older SIGMOD'23, not cloned, same family as Sapienza P&D).

## Summary table (ranked by usefulness for a pre-trade memecoin risk model)

| # | Dataset | Chain | Rows | Label type | Features in repo? | License | Verdict |
|---|---|---|---|---|---|---|---|
| 1 | HailemariamMersha/MemeTrans (= MELT features) | Solana pump.fun->Raydium | 41,470 | high/medium/low post-migration risk (+manipulated flag in MELT) | YES, 131 cols | none stated (MELT repo: CC BY-NC 4.0) | best |
| 2 | git-disl/MELT | Solana | 41,470 labels + 46k launch list + metadata | same | no (Drive link) | CC BY-NC 4.0 | labels/metadata only |
| 3 | DeFiLabX/SolRPDS | Solana (all DEX pools) | 116,308 pools | heuristic rug (liquidity removal + inactivity) | pool-level aggregates | CC BY 4.0 | good rug base set |
| 4 | am-mong/Midsummer Meme's Dream | ETH/BSC/SOL/Base | 34,988 tokens; small label files | detected wash trading / LPI / P&D / rug / delisted | OHLCV zips | none stated | good, small labels |
| 5 | ian05012/solana-memecoin-dataset | Solana | 44,460 snapshots, 9.5M trades | forward max return (not rug) | ~80 GMGN features | MIT | rich features, no rug label |
| 6 | avasis-ai/pumpfun-launch-data | Solana pump.fun | 7,430 (1/32 sample) | rule-based SAFE/WARN/DANGER | 37 launch features | custom (see LICENSE) | great feature ideas, label is heuristic |
| 7 | Erin-Blockchain/solana-pumpfun-launches | Solana pump.fun | 28,327 | 5h peak multiple after min 15 | 15-min OHLC-ish | CC BY 4.0 | survivor-gated |
| 8 | tomdelcarlo-lgtm/pumpfun-graduation-prediction | Solana pump.fun | 32,000 | graduated (1.82%) | 16 features | MIT-style LICENSE | small, clean |
| 9 | Solid-Sea/pump-gold-dataset | Solana pump.fun | 1,306,082 tokens | golden (>=10x) / dead (<2x) | 8 aggregates | custom/research | label is price-based, weak |
| 10 | inventandchill/data-samples | Solana pump.fun | 3,231 | 5x in 3h after migration | 75 | none | small |
| 11 | dianxiang-sun/rug_pull_dataset | ETH/BSC | 2,391 | confirmed rug incidents, 19 types | no | none | positives only |
| 12 | CRPWarner/RugPull | ETH/BSC | events xlsx + ground-truth contracts | contract-related rug types | Solidity | none | EVM contract-level |
| 13 | SystemsLab-Sapienza Ethereum-BSC-token-dataset | ETH/BSC | all tokens/LPs to 2022-03 | none in repo (raw token+LP lists) | 4 x 7z | none | raw universe |
| 14 | SystemsLab-Sapienza pump-and-dump-dataset | CEX (Binance/Yobit) | 1,109 pumps + 821k labeled windows | pump (gt) | yes | LICENSE present | classic P&D |
| 15 | B0R0koko/pump-and-dump-prediction | Binance | 498 events (473 used) | pump target | code + manifest | LICENSE present | niche |
| 16 | hwlongCUHK/Coin-Meme (+ alx/CoinCLIP, CoinVibe) | Solana | 3,751 | none (viability / market cap) | text+images+comments | LICENSE present | multimodal, no rug label |
| 17 | willho/fingerprinter-dataset | Solana pump.fun | ~39k tokens, pg_dump 2.1 GB uncompressed | deathbed / drawdown events | 22-float fingerprint + snapshots | none | usable w/ Postgres |
| 18 | Smurfetc/solana-memecoin-calls-dataset | Solana | 12,988 calls | post-call peak | mc, peak, tg | CC0 | call-channel bias |
| 19 | h4nsx/Rugpull-Detection, hhy569/rugradar | Solana | derived | derived | - | none | derivative / unverified |

## Detail per dataset

### 1. HailemariamMersha/MemeTrans  (best find)
- Path: `.../HailemariamMersha_MemeTrans/repo` (162 MB). Fork/early copy of the paper "MemeTrans: A Dataset for Detecting High-Risk Meme Coin Launches on Solana" (renamed MELT).
- `dataset/feat_label.csv` (78 MB): **41,470 rows x 131 columns**, key `mint_address` (+ `token`, `mint_ts`, `time`).
  Feature groups (prefix): group1 (6: migration price + calendar fields), group2 (59: holder concentration at migration - gini, top1/5/10/20/50/100 pct, bundle/cluster stats), group3 (22: market activity of pre-migration window - tx_num, trader pairs, time_span, tx_per_sec, **wash_tx_num**, ...), group4 (35: deltas of holder concentration). Plus `pred_proba` (author model output, do not use as a feature).
  Labels: `label` in {high 34,890 (84%), medium 4,702, low 1,878}, `min_ratio`, `return_ratio`.
- Label definition (inferred from data, since `annotation/` is "coming soon"): `min_ratio` = minimum post-migration price relative to the reference (migration) price; high: min_ratio < 0.3 (observed 7e-5..1.0 but see below), medium: 0.3-0.7, low: >=0.7. In the data min_ratio of high max is 1.0, so "high" also includes cases defined via `return_ratio`/manipulation; exact rule not recoverable from code. Treat as: high = price collapsed >70% after Raydium migration (or manipulated).
- Also `raw_data/memecoin.jsonl` (token list, creator, timestamp), `memecoin_metadata.jsonl` (name, description, socials), small `parsed_tx` samples, `data_pipeline/` (BigQuery SQL, Jito bundle tracing, feature generation), `risk_prediction/` (RF/XGB/LGBM etc.; reported AUPRC ~0.55-0.57 on target = non-high; base rate very skewed).
- Period: tokens launched 2024-12-09 to 2025-02-28 (migrated to Raydium).
- License: none in this fork. Upstream MELT: CC BY-NC 4.0 (non-commercial; check before bot use).
- Quality: 84% positive "high" class means "high-risk" is the norm, so the useful task is picking the 16% non-high; chronological split in code (70/30). Label depends on post-migration behavior, so features must be strictly pre-migration to avoid leakage (they are by design). Only tokens that **migrated** are included: survivorship (most pump.fun tokens never graduate).
- Bot use: direct pre-trade filter at the moment of Raydium migration (buy-the-graduation strategy): train a classifier on group2/3/4 features, trade only low-risk predicted tokens. Features (bundle share, top-N concentration, wash tx count) are computable live from pump.fun bonding-curve txs.

### 2. git-disl/MELT
- `.../git-disl_MELT/repo` (43 MB). Official repo. `data/label/label.csv`: 41,470 rows: `mint_address,min_ratio,manipulated,return_ratio,label`. `manipulated`: yes 23,584 / no 11,877 / unknown 6,009 (**a manipulation flag - wash trading / bundle-driven, definition only in the paper**). Label dist identical to #1 (high 34,890 / medium 4,702 / low 1,878); high has min_ratio 7e-5..1.0, medium 0.30-1.0, low 0.70-1.0.
- `data/memecoin/memecoin_list.jsonl` 46,139 launches (2024-12-09 to 2025-02-28), `metadata.jsonl` (name, symbol, description, image URL, socials), `data/feat/sol_hourly.txt` (SOL hourly price), `results/*.csv` predictions, `src/feat_gen.py`.
- Raw/parsed tx (>1 TB raw), bundle traces and ready `feature.pkl` are ONLY on Google Drive (not fetched). `git-disl/MemeTrans` is just a redirect README.
- License: CC BY-NC 4.0.
- Bot use: the `manipulated` flag is the only explicit wash-trading/manipulation label in these sets; join with feat_label.csv (#1) on mint to get a manipulation-vs-clean supervised target.

### 3. DeFiLabX/SolRPDS (Solana Rug Pull Dataset)
- `.../DeFiLabX_SolRPDS/repo` (144 MB incl. JSON copies). Paper: Alhaidari et al., CODASPY'25 (arXiv 2504.07132). Built from 3.69 B Solana txs.
- CSV by period: 2021 (1,703 pools), 2022 (3,695), 2023 (15,477), Jan-Nov 2024 (95,433) = **116,308 liquidity pools**.
- Columns: LIQUIDITY_POOL_ADDRESS, MINT, TOTAL_ADDED_LIQUIDITY, TOTAL_REMOVED_LIQUIDITY, NUM_LIQUIDITY_ADDS, NUM_LIQUIDITY_REMOVES, ADD_TO_REMOVE_RATIO, LAST/FIRST_POOL_ACTIVITY_TIMESTAMP, LAST_SWAP_TIMESTAMP, LAST_SWAP_TX_ID, INACTIVITY_STATUS (Active 76,358 / Inactive 19,074 in 2024 file).
- Label: there is no explicit rug column; the paper defines rug pull as most liquidity removed (e.g. >=99% / very high remove ratio) followed by inactivity. Rows appear to be all candidate pools; the label must be derived from ADD_TO_REMOVE_RATIO + INACTIVITY_STATUS (my inference - verify against the PDF `2504.07132v1.pdf` in the repo).
- License: CC BY 4.0.
- Quality: heuristic labels, no per-pool price/holder features, no pre-trade features; pump.fun bonding-curve tokens (pre-graduation) mostly absent (pools exist after graduation). 
- Bot use: ground truth for "LP pulled" events; train a model with features from MELT-like pre-trade data on the same mints, or use as positives/negatives for LP-removal detection. `h4nsx/Rugpull-Detection` is a derivative (IsolationForest, 134 MB, copies this CSV) - its claimed F2 0.895 is on self-derived labels, not independent.

### 4. am-mong/Code-and-Dataset-for-A-Midsummer-Meme-s-Dream-
- `.../am-mong_Code-and-Dataset-for-A-Midsummer-Meme-s-Dream-/repo` (64 MB). Paper (arXiv 2507.01963): cross-chain 34,988 meme coins (ETH, BSC, Solana, Base...), window mid-Oct 2024 to mid-Jan 2025, rug/P&D follow-up to mid-Mar 2025.
- Files: `confirmed_meme_coins.csv` 34,988 tokens (BSC 16,405, Solana 11,829, ETH 3,814, Base 828, ...), `high_performing_meme_coins.csv` 707 tokens (>100% return), `HP_tokens_with_anomalies.csv` 412 (ownership concentration / honeypot), `security_metrics_info_high_performing_tokens.csv`, **`wash_trading_detected.csv` 1,043 token-days (unique_maker_count)**, `lpi_operations_detected.csv` 72, `pump_and_dumps_on_performing_tokens_after_mid_january.csv` 91, **`rug_pulls_detected_on_performing_tokens_after_mid_january.csv` only 2**, delisted lists (profit extraction 30, artificial growth 84, aggregators 124), Dune tables on makers, OHLCV daily/hourly zips (~12 MB hourly), `dune_queries/`, 8 notebooks with the detection logic (rug_pull_detection, wash_trading_detection, pump_and_dumps_detection, LPI).
- Label definitions: wash trading = same wallet(s) acting as buyer and seller in same day with volume symmetry (maker-level, Dune); LPI = liquidity-pool price inflation by LP operations; P&D = hourly OHLCV rule; rug pull = returns ~ -100% with volume rule (e.g. returns -99.99%).
- License: none stated. 
- Quality: very few positives for rug (2) and P&D (91); detections are rule-based on HP tokens only (survivor/selection bias); heterogeneous chains; ~7 weeks follow-up.
- Bot use: ready-made rule implementations to flag wash trading and LPI in live data; the 82.8% figure (HP tokens with artificial growth) supports an "avoid unexplained pumpers" filter.

### 5. ian05012/solana-memecoin-dataset
- `.../ian05012_solana-memecoin-dataset/repo` (579 MB, parquet). Period 2026-06-10 to 2026-06-29 (20 days). GMGN-based.
- tokens.parquet: **44,460 snapshots (31,013 unique mints)**, 92 columns: holder structure (top10, dev_remaining_pct, sniper/bundler/insider/fresh-wallet shares, cluster stats), contract safety (mint/freeze renounced, lp_burned_pct, `rug_probability`), trading behavior (buy/sell flow, smart money, flipper ratio, `crew_cohesion` = wash crew signal), momentum trajectory; labels = forward max return 1h/6h/24h/3d, `reaches_2x` (~11%), staged/scalp exit returns, mdd_from_peak.
- Also trades (9.5M wallet-level rows, 4 parquet), ohlcv (272k 15-min candles), sequences (506k), wallets (11.8k with smart_money/insider tag), wallet_funding (15.5k edges).
- Label is **returns, not rug**. Use `max_return_*` ~0 or `mdd_from_peak` to define your own rug label (e.g. close_return_1h <= -90%).
- License: MIT.
- Quality: `rug_probability` is **all zeros** (verified) - useless; `tg_mention_count` junk per author; survivorship bias (tokens must be detected after graduation/trending), single 20-day regime; some glitch candles.
- Bot use: closest to a deployable bot feature set (all GMGN-API-available at decision time); fits entry-time classification of early buys; wallet_funding enables cluster/rug-team detection.

### 6. avasis-ai/pumpfun-launch-data (free 7-day sample)
- `.../avasis-ai_pumpfun-launch-data/repo` (2 MB). 7,430 launches (hash-sampled 1/32), 30 Oct to 5 Nov 2026, 37 cols: first-slot / first-second buyers, serial snipers, bundled wallets & supply %, shared-funder groups, creator prior launches/graduations/sold by 10m, name/symbol/image reuse (clone detection), cluster stats, top10 ex-pool %.
- Label: `verdict` SAFE (1,305) / WARN (3,784) / DANGER (2,341) with `reason_codes`, from published fixed thresholds (rule output, NOT ground truth). Graduated: 169 (2.27%).
- Full data (since 2026-08-30, ~1.7M launches) is paid ($5/day ... $999) - not obtainable here. Sample license: see LICENSE; full data restricted (no resale).
- Bot use: feature design (sniper/bundle/funder-cluster/clone features) and an outcome-based check: graduated vs verdict. Author notes DANGER launches graduate more often (5.6% vs 1.0%), i.e. "risky" flags are anti-correlated with pumping - careful.

### 7. Erin-Blockchain/solana-pumpfun-launches
- 28,327 pump.fun launches 2026-07-27 to 2026-09-25, **gated** to >=25 trades and ~$15k mcap in first 15 min; features over 5/10/15 min (vol, trades, buys/sells, growth); label `multiple = best_price_5h/price_15` (>=2 is the suggested cutoff). CC BY 4.0. No rug label, but `multiple`<~0.1 is derivable only from best price, not from final - so a drop cannot be seen. Survivor-gated.

### 8. tomdelcarlo-lgtm/pumpfun-graduation-prediction
- 32,000 launches, 16 features of first 30 min / 2h (n_trades, buy_sell_ratio, top1_wallet_pct, unique buyers, volume), label `graduated` = 1.82% (verified 0.0182). Source Dune. Capstone project; period not explicit (launch_month column). LICENSE present. Small and clean; label = bonding curve completion, not rug.

### 9. Solid-Sea/pump-gold-dataset
- 1,306,082 tokens (17M trades) aggregated to 10 cols (buy_count, sell_count, unique_wallets, total_quote_lamports, pmin, pmax, is_golden>=10x 3,304 / is_dead<2x 1,213,462). High-school project, source = a Kaggle pump.fun trade dataset (not named). Labels are max/min of whole path (look-ahead; not usable as trade-time features). Wash-trading claim only in the unseen paper; no wash label in file. Size: 159 MB.

### 10. inventandchill/data-samples
- 3,231 migrated tokens (2026-04-02..04-17), 75 numeric features (bundled buys, dev balance, gas, Hurst...), target 5x within 3h after migration (11.05%, 357 positives). CSV/pkl/xlsx + feature importance notebooks. No license. Small; good for feature importance ideas.

### 11. dianxiang-sun/rug_pull_dataset (= Dianxiang111/Rug-Pull-Dataset)
- 2,391 validated rug-pull incidents on ETH (2,303) and BSC (88), 2020-2023: Chain, address, Losses (USD), Type (19 types; Transaction Limitation 2,084, Fee 158, Token Generation 55...), Root Causes, Sources, URL. Use `rugpull_full_dataset_new.csv` (clean). **`rugpull_dataset.csv` is 10 MB padded to 1,048,575 rows of mostly empty rows** (corrupt export; only ~2,360 filled). No license. Positives only - needs your own negatives. The Dianxiang111 repo is a duplicate (identical file).

### 12. CRPWarner/RugPull
- 199 MB: `dataset/rugpullevents/rugpullevents.xlsx` (event list: project, contract-related vs transaction-related, pattern, loss kUSD, source), `dataset/groundtruth/{sol,hex}` labeled contracts + groundTruth.xlsx, `dataset/large/` bytecode samples, Gigahorse tooling. Patterns: hidden mint, limiting sell order, leaking token, dumping, withdrawing liquidity, abandoning. EVM only; no license. Useful for contract static features (honeypot/hidden mint).

### 13. SystemsLab-Sapienza/Ethereum-BSC-token-dataset (USENIX Sec'23)
- 4 x 7z (token_dataset / lp_dataset for ETH and BSC; ~240 MB compressed; no 7z installed so not unpacked here). All ERC-20/BEP-20 tokens and LPs from inception to 2022-03-07. Columns: address, symbol, decimals, total_supply, creator, gas price/used, block; LP: token0/token1, tx_hash. No scam labels in repo (paper identifies spam, rug pulls, snipers by heuristics on top). Universe for building your own labels.

### 14. SystemsLab-Sapienza/pump-and-dump-dataset (+ gme-pump-xrp-telegram)
- `pump_telegram.csv`: 1,109 pump events (symbol, group, date, hour UTC, exchange), 2017-2019, pairs SYM/BTC (Yobit, Binance, ...). `labeled_features/features_{5,15,25}S.csv.gz`: e.g. 5S: 821,307 rows, columns std/avg rush order, trades, volume, price, hour/minute sin-cos, symbol, `gt` (0/1 pump window). Chat-messages repo is a Telegram HTML dump of a XRP group (images/videos, 150 MB). CEX not memecoin DEX; old regime; LICENSE present. Bot use: pump detection features for CEX-listed small caps; weak transfer to on-chain pump.fun.

### 15. B0R0koko/pump-and-dump-prediction
- 498 Binance P&D announcement manifest (`resources/pumps.json`), 25 exclusions, 473-event cohort; code with CatBoost etc., test AUC ~0.70. Heavy repo (papers/images), no raw data in git (installer downloads). Niche.

### 16. Coin-Meme (hwlongCUHK) / CoinCLIP (alx) / CoinVibe
- Coin-Meme: 3,751 pump.fun tokens migrated to Raydium, Jan-Nov 2024; text descriptions (`destription+finance.csv`, 735 KB), comments (zip, 5 MB), 10 image zips (~230 MB), financial data = market cap and market entry time. License file present. **No rug label.** CoinCLIP repo (2 MB) = code only; "CoinVibe" dataset is on Google Drive (not fetched). Use: NLP/image features for scam-likeness (clone images, template descriptions) with a self-built label.

### 17. willho/fingerprinter-dataset
- Postgres custom dump in 3 parts (224 MB, ~2.1 GB restored), snapshot 2026-06-11, ~39,000 pump.fun launches; table `fingerprint_snapshots` (event-triggered snapshots: discovery, price_2x..100x, drawdown_15/25/40pct, `is_deathbed`, 22-dim `fingerprint_array`, top holders JSON, creator_reputation). Needs `pg_restore` (not tried). No license. `is_deathbed` + drawdown triggers could define a rug/death label.

### 18. Smurfetc/solana-memecoin-calls-dataset
- 12,988 channel "calls" 2026-06-30 to 2026-11-20 (calls.jsonl 2 MB: mint, mc at call, peak multiple, time, `tg` id), losers included, SHA-anchored; CC0. Shows 63% never double. Peak-only label (no drawdown). Notes citing **RED-PUMP-2026-v1** (see below).

### 19. Derivative / low-value
- hhy569/rugradar: `data/deployer-db.json` 1,004 deployers / 4,441 tokens, Solana, generated 2026-09-01, with rug_count and scores; labels come from RugCheck + own heuristics (Chinese text). Unverified provenance. No license. Could be used as a deployer blacklist feature but treat as noisy.
- h4nsx/Rugpull-Detection: SolRPDS copy + IsolationForest. mik3fly-lab/awesome-ethereum-scam-detection: link list only (CoinGecko scam category, RektRadar) - no data. virusLuke3/MemeCoinDatasets: raw API dumps (top100 holders, klines) with no labels. gosadu/loophole-tape, tokensafe, rug-munch-mcp etc.: tools/APIs not datasets.

## Named in the brief, status
- **MemeTrans / MELT (git-disl, HailemariamMersha)**: obtained (#1, #2).
- **A Midsummer Meme's Dream**: obtained (#4).
- **RED-PUMP-2026**: dataset by A. U. Kamat, Zenodo doi 10.5281/zenodo.20633486, arXiv 2607.02823 [snippet]: 860,213 pump.fun launches, 2026-05-08..06-10, CC-BY-4.0, survival/graduation outcomes (24h). Later revision "Auditing Collector-Generated Graduation Labels" reports collector bias (frozen cohort 749,816 mints) and a Zenodo correction notice [snippet]. **No GitHub repo found; Zenodo blocked** - cannot download. Label is graduation, not rug.
- **CoinCLIP/CoinVibe**: code only on GitHub (alx/CoinCLIP); data on Google Drive.
- **MemeChain** (arXiv 2601.22185) [snippet]: multimodal cross-chain dataset of 34,988 meme coins (ETH/BSC/SOL/Base) with website HTML, logos, social links. Same token universe as Midsummer (#4, `confirmed_meme_coins.csv`); no GitHub repo found.
- **SolRugDetector** (arXiv 2603.24625) [snippet]: benchmark of 117 manually verified rug tokens + 76,469 in-the-wild flagged tokens (H1 2025), F1 0.96. No GitHub repo found by search; needs arXiv access to find a link.
- **Catching the Rug** (arXiv 2608.20271, Aug 2026) [snippet]: 6.4 M Solana tokens, 7 months, PumpFun vs Raydium transfer, uses 5-minute early window. No code/data link found; arXiv blocked.
- **TM-RugPull** (arXiv 2602.21529) [snippet]: temporally sound multimodal rug-pull dataset (DeFi, meme, NFT, gaming). No GitHub repo found.
- PumpSense (arXiv 2605.09431, ICBC 2026) [snippet]: 280k Telegram posts from 39 pump groups, 2,246 annotated pump announcements, 2017-2023, repo `AhmedMahrous00/icbc_2026_reproducibility` (~1.6 GB, skipped).
- Marino et al. 2026 (arXiv 2602.14860) pump.fun success prediction: not located on GitHub.
- EVM honeypot datasets: only dianxiang (#11), CRPWarner (#12), Sapienza (#13) found on GitHub; no dedicated labeled honeypot dataset with trade features surfaced.

## Cross-cutting quality issues
1. Survivorship: nearly every Solana set conditions on graduation, trending, or >=25 trades, so pre-graduation rugs (the majority) are absent.
2. Labels are mostly heuristic (liquidity-removal ratio, price-drawdown thresholds, rule-based verdicts), not forensic ground truth.
3. Short, single-regime windows (20 days to 3 months); pump.fun dynamics changed in 2025-2026 (graduation 0.2-2%).
4. Licenses: MELT CC BY-NC (non-commercial); several repos have no license (default all rights reserved).
5. Leakage: forward-return and peak/trough labels must not be used as features; use time-based splits.

## How a pre-trade risk bot can use these
- Stage 1 (bonding curve / launch): features from avasis (#6), fingerprinter (#17), ian05012 (#5): sniper/bundle/funder-cluster/creator history; target = own "dead/-90% within N h" derived from ian05012 `close_return_1h`/`mdd_from_peak` and fingerprinter drawdowns.
- Stage 2 (migration): train MELT features (#1) with `label==high` and `manipulated` (#2) as targets; deploy as veto filter before buying a Raydium/PumpSwap graduation.
- Stage 3 (post-entry): SolRPDS (#3) style LP add/remove monitoring plus Midsummer rules (#4) for wash trading / LPI as exit triggers.
- EVM side: #11/#12 for contract-pattern checks; Sapienza #13 as universe.
