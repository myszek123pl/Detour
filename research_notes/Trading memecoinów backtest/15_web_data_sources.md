# 15 - Public data sources for memecoin backtesting (web survey)

Survey date: 2026-11-21. Method: WebSearch (extended) + GitHub (git proxy / raw.githubusercontent / `gh api search`).
**Reachability from this session**: only GitHub (github.com, raw.githubusercontent.com, git clone via proxy) resolved. zenodo.org, huggingface.co, kaggle.com, arxiv.org, dune.com, bitquery.io, docs.bitquery.io all fail DNS (`ENOTFOUND`) -> **not reachable**. Details below marked "(search snippet)" come from WebSearch result text only and are unverified by direct fetch; "(verified)" means I read the files myself.

Already held (skipped): ian05012/solana-memecoin-dataset, Erin-Blockchain/solana-pumpfun-launches, Smurfetc/solana-memecoin-calls-dataset, Solid-Sea/pump-gold-dataset, launchtape-io/pump-fun-backtest, windowopner/pumpfun-trial-1, avasis-ai/pumpfun-launch-data, TrenchAutopsy/exit-liquidity-standard.

## Ranking (best for trade-level backtest first)

| # | Source | Trade-level? | Free | Reachable now |
|---|---|---|---|---|
| 1 | jocry/Pumpfun_Memecoin_Corpus (HF) | yes, 33.6M trades | yes | no (HF) |
| 2 | pumpdatafun/pump-fun-trades-sample (HF) | yes, full 1 day incl. failed txs | yes | no (HF) |
| 3 | RED-PUMP-2026-v1 (Zenodo + HF mirror) | launch-level + outcomes, 860k | yes | no |
| 4 | MELT / MemeTrans (GitHub + Google Drive) | yes, pre-migration txs; features+labels on GitHub | yes (CC BY-NC 4.0) | GitHub part yes, Drive no |
| 5 | Kaggle: memecoins-pump-or-dump, solana-skill-sprint (dremovd dataset) | yes | yes (Kaggle login) | no |
| 6 | cryptodata/pumpfun-dataset-light (HF) | yes, 2 weeks bonding-curve swaps | yes | no |
| 7 | Bitquery Data Store (Parquet) | yes, full history | sample free, full from ~$300 | no |
| 8 | Launch Tape (HF sample + launchtape.io) | yes | 2h sample free, rest paid | no |

## A. Trade / launch dumps

### 1. jocry/Pumpfun_Memecoin_Corpus
- URL: https://huggingface.co/datasets/jocry/Pumpfun_Memecoin_Corpus ; host: huggingface.co
- Size/period (search snippet): ~33.58M trades, 798,430 launches, 39 days; bonding-curve snapshots, graduation labels. Exact bytes unknown.
- Fields (snippet): trades table = buy/sell, price, bonding-curve state, wallet; token table with labels.
- License: card says CC BY 4.0, embedded metadata says MIT (conflict - check live). Access: free, no key. GitHub mirror: none found. Reachable: NO.

### 2. pumpdatafun/pump-fun-trades-sample
- URL: https://huggingface.co/datasets/pumpdatafun/pump-fun-trades-sample ; host huggingface.co
- One UTC day, 2026-10-15: every pump.fun bonding-curve trade and every PumpSwap trade; ~21.7M landed + ~19.4M failed txs (failed kept). Useful for fill-rate/failure modelling. Size in GB not stated. License unknown (check). Free sample (full feed presumably paid by same publisher). Mirror: none. Reachable: NO.

### 3. cryptodata/pumpfun-dataset-light
- URL: https://huggingface.co/datasets/cryptodata/pumpfun-dataset-light ; two weeks Jul-Aug 2026 bonding-curve swaps only (no PumpSwap). Free. License unknown. Reachable: NO.

### 4. RED-PUMP-2026-v1
- URLs: Zenodo concept DOI 10.5281/zenodo.20633486 (latest = v1.6 https://zenodo.org/records/23018519, 2026-09-28; older v1.1 20633603, v1.3 21908375, v1.4 21923106, v1.5 22286914); HF mirror https://huggingface.co/datasets/AratiKamat/red-pump-2026 ; companion paper arXiv 2607.02823 (v3, corrigenda v1.3/v1.4).
- Hosts: zenodo.org, huggingface.co. Period 2026-05-08 .. 2026-06-10, 860,213 pump.fun launches with survival / collector-generated terminal labels (graduation). License CC-BY-4.0. Free.
- CAVEATS (from search snippets): collector polled a top-50-newest REST endpoint -> sampling/coverage issues; external audit (2026-08-11) found reconstruction violations in exit times (v1.6 says label right, reconstructed exit time wrong). Treat as launch-level labels, not tick data; read version history. Companion: RED-COHORT-2026-v1 (zenodo 20978742 / 21745672 / 21765387): 1,012 sniper-wallet cohorts, 2,965 wallets, 1.58M buyer events, 166k launches, Jun 11/12-25/26 2026.
- GitHub mirror: none found. Reachable: NO.

### 5. MELT (formerly MemeTrans) - arXiv 2602.13480 (v2 title "MELT: A Behavioral Trace Dataset for High-Risk Memecoin Launch Detection")
- GitHub (VERIFIED, cloned): https://github.com/git-disl/MELT (old name git-disl/MemeTrans redirects via README). Host github.com (reachable).
- In repo (43 MB): `data/label/label.csv` 3.86 MB (mint_address, min_ratio, manipulated yes/no/unknown, return_ratio, label=high-risk); `data/memecoin/memecoin_list.jsonl` 13.3 MB (token_address, signature, timestamp, time, creator; launches up to 2025-02-28); `data/memecoin/metadata.jsonl` 12 MB (name, symbol, description, imageUrl, twitter, website, telegram); `data/feat/sol_hourly.txt` (SOL price hourly); results/*.csv (model predictions); src/ (feature gen + models).
- NOT in repo (Google Drive, host drive.google.com / drive.usercontent.google.com): pre_migration_tx.zip (bonding-curve txs, required for features), bundle.zip (bundle traces), post_migration_tx.zip (Raydium txs, very large; raw >1 TB), feature.pkl (pre-built features). Paper (snippet): >40k launches that migrated to Raydium, >30M pre-migration txs, ~180M post-migration txs, 2024-12-01..2025-03-01.
- License: CC BY-NC 4.0 (LICENSE file, verified) - non-commercial. Free. Mirror: GitHub is the primary; Drive archives have no mirror. Related: github.com/HailemariamMersha/MemeTrans (fork, 2026-03).

### 6. Kaggle competitions/datasets
- Memecoins: Pump or Dump? https://www.kaggle.com/competitions/memecoins-pump-or-dump/data - decoded On-Chain Divers Solana ClickHouse data: token creation, bonding-curve swaps, AMM migrations, PumpSwap trades, reserves, fees (snippet). Competition rules apply (check redistribution/commercial terms).
- Solana Skill Sprint - Memecoin Graduation https://www.kaggle.com/competitions/solana-skill-sprint-memcoin-graduation/data ; data in https://www.kaggle.com/datasets/dremovd/pump-fun-graduation-february-2025 : tx logs of first 100 blocks after mint (mint, has_graduated, swaps, wallets, timestamps, direction, amounts), Feb 2025.
- https://www.kaggle.com/datasets/btclee/memecoins : 6.4M Solana memecoins over 7 months (~6.3M pump.fun), cited by arXiv 2608.20271 "Catching the Rug" (first 5 min trading -> rug labels). Not opened.
- https://www.kaggle.com/datasets/gleb270/pump-fun-api-solana-tokens-info : token metadata from pump.fun API (snippet only).
- Hosts: www.kaggle.com (+ storage.googleapis.com for downloads; kaggle CLI needs API key/login). Mirrors: GitHub solution repos only (sqqshh/Solana-Skill-Sprint-Memcoin-Graduation-Prediction, Alishan45/Solana_Memecoin_Graduation, Xurama1/Alpha-Radar-Solana-Sprint) - code, not data. Reachable: NO.

### 7. Midsummer Meme's Dream (USENIX Security 2026; arXiv 2507.01963)
- GitHub (VERIFIED, cloned, 64 MB): https://github.com/am-mong/Code-and-Dataset-for-A-Midsummer-Meme-s-Dream- ; also MemeChain arXiv 2601.22185 (same authors, Mongardini & Mei) = extended multimodal dataset.
- Content: 34,988 confirmed meme coins across ETH/BSC/Solana/Base (`confirmed_meme_coins.csv` 2.4 MB: symbol,name,platform,address); `price_changes_mid_january_snapshot.csv` (price_old Oct -> price_new Jan); `high_performing_meme_coins.csv` (707 tokens >100%); daily OHLCV zips (3.3 MB to mid-Jan, 3.4 MB to mid-Mar), hourly OHLCV zip 12 MB to mid-Mar for HP tokens; labelled manipulation lists (wash trading, LPI, pump&dump, rug pulls); Dune maker-level volume CSVs (up to 10.8 MB); `dune_queries/` SQL; notebooks. Window Oct 2024 - Mar 2025.
- Value: cross-chain, daily/hourly candles, manipulation labels; weak for Solana tick backtests (Solana subset small, survivor-biased towards high performers). License: none file in repo (all rights reserved by default - ask/cite). Free. Reachable: YES (GitHub).

### 8. CoinVibe / CoinCLIP (arXiv 2412.07591)
- GitHub https://github.com/hwlongCUHK/CoinCLIP.git (raw README 404 on main; repo not searchable -> may be renamed/private; unverified). Dataset ~6,231 pump.fun memecoins Jan-Nov 2024: text, logos, comments, timestamps, likes; label = Raydium listing. Host github.com (+ possibly drive). Social/community features rather than prices. Reachable: GitHub yes but repo not confirmed.

### 9. Bitquery Data Store
- https://bitquery.io/datastore/datasets/pumpfun , /pumpswap , /solana ; docs https://docs.bitquery.io/docs/blockchain/Solana/Pumpfun/Pump-Fun-API/ , https://docs.bitquery.io/docs/cloud/solana/
- Parquet, full history from first pump.fun tx to yesterday, daily refresh; tables trades, creation/migrations, pools, OHLCV (137-col schema reported); layout `solana/dex_trades/pumpfun/<slotStart>_<slotEnd>.parquet`. Free sample per dataset (no email); full from ~$300; delivered via Requester-Pays S3 or Cloudflare R2 after payment. GraphQL API needs token (free trial). Hosts: bitquery.io, docs.bitquery.io, (streaming.bitquery.io / graphql.bitquery.io for API; S3/R2 hostnames provided after purchase). GitHub mirror: none. Reachable: NO.

### 10. Launch Tape (commercial, with free sample)
- https://launchtape.io ; https://huggingface.co/datasets/launchtape/solana-launch-tape (free 2h sample 2026-10-10 14-16 UTC, `pregrad` 14,417 rows; tables incl. gradtrades = PumpSwap trades 30 min after graduation); GitHub https://github.com/launchtape-io/launchtape (toolkit) and launchtape-io/pump-fun-backtest (HELD). Daily .jsonl.gz / .parquet; pricing conflicting (0.05 SOL/6 USDC per day, 0.5 SOL/60 USDC per month, or $10/month) - verify. Similar vendor: loopholetape/pumpfun-launches (HF) and github.com/gosadu/loophole-tape (~$5/day Parquet, x402 pay-per-call). Reachable: GitHub only.

### 11. Dune / other vendors
- Dune `dex_solana.trades` (covers Raydium, Orca, Meteora, pump.fun, PumpSwap), docs https://docs.dune.com/data-catalog/curated/dex-trades/overview ; access via Dune API (key), Datashare (enterprise, paid), or UI (CSV export, free tier credit-limited). Hosts dune.com, docs.dune.com, api.dune.com. Public query exports on GitHub: oladeeayo/Pumpfun-Token-Deployer-Records-Dashboard, oladeeayo/Pumpfun-Rug-Watch-Dashboard (SQL only). Reachable: NO.
- nolimitnodes https://nolimitnodes.com/products/trading-datasets (paid monthly Parquet of parsed pump.fun trades/pools/mints). CryptoStruct cryptostruct.com (tick data, EUR 1/day, SOL pairs on CEX/DEX venues). Not tested.
- Allium, Codex, Birdeye, GeckoTerminal, Helius: search returned nothing about free bulk exports; all are API-key/paid (GeckoTerminal public OHLCV API is free but rate-limited, ~180 days minute history). Not verified.

## B. Social / call / signal datasets

- PumpSense (IEEE ICBC 2026, arXiv 2605.09431): GitHub https://github.com/AhmedMahrous00/icbc_2026_reproducibility (VERIFIED metadata: MIT, 1.6 GB repo, updated 2026-10-20; Zenodo archive DOI 10.5281/zenodo.19616802). 283,017 Telegram messages, 39 groups, 2,246 labelled pump announcements, 140 cancelled. Classic CEX pump groups, not memecoin calls. Reachable: YES (GitHub). Best social dataset available here.
- SystemsLab-Sapienza/pump-and-dump-dataset (GitHub, MIT, 17.5 MB, 2021): pump event list (pump_telegram.csv) on SYM/BTC + Binance download script. "Doge of Wall Street" (ACM 3561300) release: >1,000 confirmed pumps from 20 Telegram groups. Bayi-Hu/Pump-and-Dump-Detection-on-Cryptocurrency (GitHub, 275 MB, SIGMOD'23) - CEX pumps. Reachable: YES.
- tripolskypetr/telegram-trading-channel-dump (HF, MIT per snippet): signals from public channel WallstreetQueenOfficial with LLM-extracted fields - CEX-style signals. Reachable: NO.
- arXiv 2609.01176 "Don't You Know, Pump it Up!" - releases crypto dictionary, classifier and a HF dataset (name not captured). arXiv 2610.10149 (Telegram bait-and-trap + honeypots). Reachable: NO.
- Pumpdotstudio/pump-fun-sentiment-100k (HF) - sentiment of 100k pump.fun comments (snippet). Reachable: NO.
- X/Twitter call datasets: none found beyond the already-held Smurfetc set; Kombucho/memecoin-gamble-research (GitHub, 2026-10, "4,293 pumpdotfun callouts" with backtest, data+code) is a new GitHub-reachable candidate (unverified contents). Trading-journal datasets: none public (only tools: heisbuba/memecoins-journal, c1pps/pnl-cards, Timothymycompc/trading-review "honest backtests" - the last may hold sample results).

## C. Other GitHub-reachable candidates found (not yet inspected; all via github.com)
- tomdelcarlo-lgtm/pumpfun-graduation-prediction (first-30-min features, 1.82% base rate)
- Kombucho/memecoin-gamble-research (4,293 callouts backtest)
- unretain/solagents ("380k real episodes" memecoin replay)
- WhoIsTyfur/makefun-memecoin-backtest-48h (replay of Solana chain data)
- sachinbatra1971-byte/memecoin-research (collector for backtests)
- K9-glitch3/pumpswap-graduation-provenance (seeded-pool research dataset)
- dynamolabs/launchpad-registry (program IDs of launchpads, useful for decoding)
- ian05012 data originates from GMGN scraping (held); nirgranthi/memecoin-scraper, Solcrates-Labs/ohlcvcreator (OHLCV scrapers)
- Related papers with possible data: arXiv 2610.41597 (serial rug-pull exits, team-level), 2610.39458 (early-buyer groups, prospective study), 2611.11436 (team-following profitability), 2609.10246 (meme coin factories), 2609.18975 (cross-pipeline coverage), 2602.14860 (predicting success pump.fun), 2611.13342 (early rug pull Solana). Data locations not retrieved (arxiv.org unreachable).

## Hostnames to allowlist (priority order)

Core (best sources):
1. huggingface.co (jocry corpus, pumpdatafun sample, cryptodata light, RED-PUMP mirror, launchtape sample)
2. cdn-lfs.huggingface.co, cdn-lfs-us-1.hf.co, cas-bridge.xethub.hf.co, hf.co (HF file downloads redirect here)
3. zenodo.org (RED-PUMP-2026, RED-COHORT, PumpSense archive)
4. drive.google.com and drive.usercontent.google.com (MELT transaction zips, feature.pkl)
5. www.kaggle.com and storage.googleapis.com (Kaggle datasets; needs API token)
6. arxiv.org (paper pages, data links in appendices)

Optional/paid:
7. bitquery.io, docs.bitquery.io, streaming.bitquery.io (samples; S3/R2 bucket host is issued after purchase)
8. launchtape.io, api.dune.com / dune.com / docs.dune.com, nolimitnodes.com

Already reachable: github.com, raw.githubusercontent.com (MELT, Midsummer, PumpSense, Sapienza repos).

## Takeaways
- Only truly free tick-level pump.fun sets: jocry corpus (39 days), pumpdatafun (1 day, with failures), cryptodata light (2 weeks), MELT (Dec 2024 - Feb 2025, Drive), Kaggle competition sets. All except MELT need non-GitHub hosts.
- Regime mismatch: MELT/Kaggle = early 2025; jocry/RED-PUMP/pumpdatafun = mid-late 2026; combining them gives a cross-regime test.
- Licensing: MELT is NC; Kaggle competition data has rules; RED-PUMP CC-BY-4.0; jocry conflicting; Midsummer none stated.
- No public trading-journal dataset exists; Telegram sets are CEX pump groups, not memecoin call feeds.
