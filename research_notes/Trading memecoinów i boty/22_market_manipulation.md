# Market manipulation in memecoin markets beyond rug pulls (as of Nov 2026)

Method note: 7 web searches; all WebFetch calls failed (justice.gov, arxiv.org, madeonsol.com, bitquery.io not resolvable in this sandbox), so findings rest on search-result summaries, not full-page reads. Primary pages were not read directly. Many Solana-specific numbers come from vendors (Bitquery, MadeOnSol, Solidus) with commercial interests.

## Volume bot services, fake holder/micro-buy bots, wash trading prevalence on Solana DEXs

### Takeaway
Wash trading is cheap on Solana (tx fees ~fractions of a cent; main cost is pool fee) and measured prevalence ranges from ~18% of pump.fun transactions to ~23% of Raydium CLMM volume driven by one wallet; single tokens can be ~99% fake volume. Figures are heuristic and vendor-sourced, so treat as order-of-magnitude.

### Cited Findings
- Vendor blog estimates Solana fees ~$0.00025/tx; 100,000 wash trades for ~$25 SOL; a $100K fake-volume day costs roughly $250-$1,000 in pool fees (driven by 0.25-1% AMM fee) — [MadeOnSol via search summary](https://madeonsol.com/blog/solana-volume-bots-explained) (vendor, unverified)
- Bitquery traced $1.4B of volume through 438 Raydium pools of fake tokens over 30 days (22.7% of Raydium CLMM volume) to one wallet on about $12,000 of capital; one sampled tx showed ~$22,200 volume at $1.13 cost excluding network fees — [Bitquery blog](https://bitquery.io/blog/solana-volume-numbers-are-a-lie); [CoinMarketCap Academy](https://coinmarketcap.com/academy/article/bitquery-raydium-clmm-wash-trading-bot); [CryptoSlate](https://cryptoslate.com/solana-bot-turns-just-12000-into-1-4-billion-in-trading-volume-as-fake-liquidity-floods-raydium/). Note conflict: forensic per-volume cost is far below the 0.25-1% estimate above (possibly routing/fee-tier/counting differences; unverified).
- Bitquery investigation of memecoin America250: ~99% of "volume" was wash trading — [Bitquery](https://bitquery.io/investigations/token-factory-america250)
- Pump.fun measurement study: nearly 18% of trading transactions identified as manipulative; manipulators favor repeated low-volume trades since pump.fun fees scale with volume; high activity and wash trading associated with higher graduation rates — [arXiv 2507.01963](https://arxiv.org/html/2507.01963v2) (preprint)
- Same cross-chain study: 62.9% of tokens subject to pump-and-dump/rug-pull operations had previously undergone wash trading or liquidity-pool insider activity — [arXiv 2507.01963](https://arxiv.org/html/2507.01963v2)
- MemeTrans dataset (41k+ launches, 200M+ txs): earliest buyers take a substantial supply share and often use bundled accounts to hide true holder distribution — [arXiv 2602.13480](https://arxiv.org/html/2602.13480)
- Bitquery study of 3,170 wallet-token positions with >=$100K reported gains (Oct 2025-Aug 2026): concentrated allocations can look like multiple independent winning wallets; ~74% of gains not replicable by copy traders — [KuCoin News summary](https://www.kucoin.com/news/flash/bitquery-study-reveals-74-of-pump-fun-gains-cannot-be-replicated-by-copy-traders); [CryptoSlate](https://cryptoslate.com/pump-funs-biggest-winners-may-be-impossible-to-copy-as-752-million-study-exposes-hidden-trading-gap/)
- White Whale Labs claims memecoin trading is almost entirely driven by cluster wallets and found no profitable edge — [KuCoin News](https://www.kucoin.com/news/flash/white-whale-labs-solana-meme-coin-trading-driven-by-cluster-wallets) (secondary, claim)
- Solidus Labs (May 2025): ~98.6-98.7% of pump.fun tokens showed pump-and-dump/rug characteristics; 361k of 388k Raydium pools (93%) showed soft-rug traits; only ~97k of ~7M pump.fun launches kept >=$1,000 liquidity — [Solidus Labs](https://www.soliduslabs.com/reports/solana-rug-pulls-pump-dumps-crypto-compliance); [CoinDesk](https://hotfix.coindesk.com/business/2025/05/07/98-of-tokens-on-pump-fun-have-been-rug-pulls-or-an-act-of-fraud-new-report-says). Solidus' own classification; not independently verified.
- A Binance Square post claims wash trading is ~30% of reported volume — [Binance Square](https://www.binance.com/en-IN/square/post/11536682831601) (low-quality source)

### Inferences
- Because fake volume costs almost nothing relative to the attention it buys, reported volume, tx counts and even "holder counts" are unreliable inputs for a bot; use only wallet-level, de-clustered metrics.
- "Smart money"/copy-trade signals may be a single bundled operator, so a bot following top wallets can be exit liquidity.

### Gaps
- No primary-source pricing for volume-bot or fake-holder/micro-buy services (Telegram bot menus, per-day fees); only vendor blogs. Fake-holder bot mechanics specifically were not found in a citable source.
- Independent (non-vendor) prevalence estimate for Solana wash trading not found.

## Trending manipulation (DEX Screener / Birdeye / pump.fun) and paid boosts

### Takeaway
DEX Screener sells official "Boosts" that raise Trending Score, while its help center says trending itself is organic and anyone selling trending is scamming; third-party "trending" services sell packages and rely on volume bots. A boost therefore signals paid promotion, not quality.

### Cited Findings
- DEX Screener docs: Boost packs temporarily increase a token's Trending Score; weak tokens will not automatically hit #1 — [DEX Screener docs](https://docs.dexscreener.com/boosting)
- DEX Screener help: trending is organic and not for sale; sellers are scams and tokens face penalties — [DEX Screener help](https://help.dexscreener.com/en/articles/1166721)
- Third-party vendor (PandaBoost) packages start at ~$1,000 for 12/24-hour campaigns — [PandaBoost listing](https://bme.buet.ac.bd/?p=7872) (vendor, odd host, low reliability)
- Cheap Telegram bots/GitHub scripts promise trending but leave detectable patterns, failed txs — [Blockonomi](https://blockonomi.com/how-to-trend-on-dexscreener-in-2026-how-the-trending-algorithm-actually-works/); [Bitcoinist](https://bitcoinist.com/how-solana-volume-bot-uses-fresh-wallets-to-turbo-charge-token-charts/) (the latter describes a volume bot using fresh wallets)
- Press allegation that DEX Screener prioritizes paid listings over legitimate projects — [Crypto.news](https://crypto.news/how-dex-screener-became-hub-for-crypto-scammers/) (allegation, not a finding)

### Inferences
- Boost status (visible on DEX Screener; apify scrapers exist for boosted-token feeds) can be used as a negative/neutral feature rather than a buy signal; a bot could flag tokens whose trending coincides with boost purchase.

### Gaps
- Nothing found on Birdeye or pump.fun trending/"King of the Hill" manipulation specifics; boost prices for DEX Screener not captured; the exact trending algorithm weights unverified.

## Memecoin market makers; DOJ/FBI NexFundAI sting and similar cases

### Takeaway
Oct 2024 "Operation Token Mirrors" (DOJ Massachusetts, FBI) charged 18 individuals/entities after the FBI created a token, NexFundAI, and caught market makers offering wash trading; Gotbit was charged separately for 2018-2024 manipulation.

### Cited Findings
- FBI built NexFundAI (Ethereum) and met market makers; ZM Quant, CLS Global, MyTrade charged over washing/conspiring to wash it; Gotbit charged for wash trading on behalf of clients 2018-2024 though not on NexFundAI; Gotbit CEO apprehended in Portugal; 18 individuals/entities charged by DOJ, SEC action against 3 companies and 9 individuals; at least ~$25-35M crypto seized (sources differ) — [DOJ USAO-MA](https://www.justice.gov/usao-ma/pr/eighteen-individuals-and-entities-charged-international-operation-targeting-widespread); [Fortune](https://fortune.com/crypto/2024/10/09/fbi-doj-crypto-market-manipulation-fraud-charges/); [TRM Labs](https://trmlabs.com/post/fbi-creates-token-project-in-trojan-horse-crypto-operation-that-seizes-25-million); [Decrypt](https://decrypt.co/285503/feds-charge-gotbit-others-market-manipulation?amp=1)
- A secondary source says CLS Global received a $428,000 fine — unverified, not confirmed against primary source.

### Inferences
- Market-maker-as-a-service wash trading is an established, prosecuted business model; a token with unexplained "market maker" volume is higher-risk. Enforcement exposure is real but concentrated on large, EVM/centralized-exchange cases; Solana retail volume bots are mostly unprosecuted.

### Gaps
- Direct DOJ page not read (host blocked); outcomes/sentencings after 2024 and any 2025-2026 memecoin-specific cases not researched; Solana-specific market-maker cases not found.

## Detection signals: circular flows, repeated wallet pairs, buy/sell symmetry, uniform sizes

### Takeaway
Practical heuristics: round-trip ratios, buy and sell of same token via same pool in one tx, circular A-B-C-A routes, clustered fresh wallets with common funding, abnormal volume/liquidity ratio with no price impact; all heuristic with false positives.

### Cited Findings
- Warning signs: wallets created around the same time, similar funding sources, similar holdings; circular routes A->B->C->A; 24h volume/liquidity >20x highly suspicious; high volume with almost no price impact — [MadeOnSol](https://madeonsol.com/blog/solana-bot-detection-fake-volume) (vendor)
- Bitquery: 22,685 completed round trips in Raydium case; ~95% of flagged amount in its Solana DEX screen was buy and sell of same token via same pool in one tx; method uses round-trip ratios, two-sided participation, funding-burst patterns; explicitly heuristic, not proof of intent — [Bitquery](https://bitquery.io/blog/solana-volume-numbers-are-a-lie); [Solana Compass](https://solanacompass.com/news/bitquery-traces-14b-of-raydium-clmm-volume-227-of-the-total-to-one-wash-trading-wallet)
- Academic DEX wash-trading detection must allow tolerance when matching buy/sell amounts as washers do not trade exact equal volumes — [arXiv 2102.07001](https://arxiv.org/pdf/2102.07001)
- Pump.fun study uses flip-based wash trading scores; repeated low-volume trades typical — [arXiv 2507.01963](https://arxiv.org/html/2507.01963v2)
- TUM 2025 thesis: Solana lacks well-defined manipulation-detection frameworks; proposes network analysis, anomaly detection — [TUM thesis](https://www.cs.cit.tum.de/fileadmin/w00cfj/sebis/thesis/250610_Wiedenmann_Thesis.pdf)
- Bundled early-buyer accounts conceal holder concentration — [MemeTrans](https://arxiv.org/html/2602.13480)

### Inferences
- Bot filter candidates: (1) unique-trader/tx ratio and net-flow per wallet near zero; (2) wallet-pair repeat counts; (3) funding-source clustering of top holders; (4) volume/liquidity and volume per price-move; (5) low variance of trade sizes/inter-trade timing; (6) boost purchase flag; (7) exclude same-tx round trips from volume. Thresholds like 20x are vendor-chosen and need backtesting.

### Gaps
- No validated thresholds or false-positive rates; no open benchmark labeled dataset beyond academic preprints; uniform-trade-size and timing-regularity thresholds not found in citable sources.
