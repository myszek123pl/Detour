# Graduation / migration dynamics of pump.fun tokens (PumpSwap/Raydium/Meteora) and migration sniping

Research budget note: 4 web searches used; WebFetch to arxiv.org and dextools.io failed (hosts not in session network allowlist), so all findings come from search-result summaries only, not full-page reads. Treat every figure as "snippet-level, unverified against primary source" unless stated.

## 1. Post-graduation returns (minutes/hours/days), share that dump vs continue, change after PumpSwap

### Takeaway
I found NO quantitative dataset of post-graduation returns (share dumping vs continuing, by time window), pre- or post-PumpSwap. Only qualitative claims (brief pump then dump) and the 2026 BOOST mechanism that artificially supports price for 5 minutes post-migration.

### Cited Findings
- PumpSwap launched March 2025 so graduated tokens migrate instantly to pump.fun's own DEX; fee 0.25% (0.2% LPs, 0.05% protocol), old 6 SOL migration fee removed — [The Block](https://www.theblock.co/news/business/2025-03-20-pump-fun-launches-dex-called-pumpswap-to-instantly-migrate-graduated-tokens-347360); fee details via [MadeOnSol](https://madeonsol.com/learn/pumpswap) (vendor source, summarized in search results)
- Migration is a permissionless migrate instruction creating a PumpSwap pool and burning LP tokens — [Bitquery docs](https://docs.bitquery.io/docs/examples/Solana/pump-fun-to-pump-swap)
- Qualitative claim: most graduated tokens see a brief pump right after migration as bots/momentum traders pile in, then many dump as early curve buyers take profit — [MadeOnSol](https://madeonsol.com/blog/how-to-snipe-tokens-on-pump-fun) (blog, no data; unverified)
- BOOST (live ~July 2026): capital previously locked in the pool is used for automatic market buys during the first 5 minutes after migration, with bought tokens burned; graduation rate reported at 6.7% in late July 2026, ~8x June average. The Block notes BOOST acts after bonding, so doesn't mechanically raise the share reaching the threshold — [The Block](https://theblock.co/news/defi/2026-07-29-pump-fun-token-graduation-rate-jumps-boost-changes-launch-incentives-409815)
- Commentary (via search summary) argues the real test is survival once BOOST-driven demand fades; no source measured post-migration decay — same The Block coverage
- CoinGecko study headline: only ~5% of pump.fun tokens survive past 90 days (all tokens, not graduated only) — [Crypto Briefing](https://cryptobriefing.com/pump-fun-token-survival-rate-study/) (headline only, not read)
- Practitioner claim: ~98.6% of tokens dump in first hour; 1.4% worth holding — [MadeOnSol](https://madeonsol.com/blog/why-pumpfun-tokens-fail-first-hour-find-survivors) (unverified, all tokens not graduated ones)

### Inferences
- Because BOOST (5-min buys) overlaps exactly with the first-minutes window, any post-Jul-2026 return data is confounded; pre-BOOST and post-BOOST should be separated.
- A "pump then fade" shape is plausible given curve-holder exit supply at graduation, but not quantified here.

### Gaps
- No share-dump vs share-continue statistics at 5m/1h/24h/7d; no pre- vs post-PumpSwap comparison. Suggested next sources: Dune dashboards, Bitquery PumpSwap queries, Pisa paper on 655,770 tokens (Sep-Oct 2025), arXiv 2607.02823, own backtest from on-chain data.
- Raydium/Meteora/other launchpads (Bonk.fun, Meteora DBC, etc.) post-migration data: not found.

## 2. Migration-snipe strategies, competition, and predictive signals (time to graduate, holders)

### Takeaway
Graduation is rare and bot-heavy; sniper tooling now listens to PumpSwap migrations rather than Raydium. Evidence for predictive signals is thin: an academic model exists (SOL in curve + structure + behavior features) but I could not retrieve its metrics; holder-concentration claims are from vendor blogs.

### Cited Findings
- Graduation-rate figures (non-comparable definitions): ~0.26% 7-day avg mid-June 2026, down ~80% in 3 months (Dune via [DEXTools](https://www.dextools.io/news/pump-fun-graduation-collapse-solana-fees-2026)); 2.01% week of Mar 9-15 2026, highest since July 2025 ([KuCoin/Odaily](https://www.kucoin.com/news/flash/pump-fun-meme-coin-graduation-rate-hits-2-01-highest-since-july-2025)); 6.7% late July 2026 ([The Block](https://theblock.co/news/defi/2026-07-29-pump-fun-token-graduation-rate-jumps-boost-changes-launch-incentives-409815)); fewer than 2% ever graduated ([The Block](https://www.theblock.co/amp/post/404806/pump-fun-activity-craters-80-three-months-solana-fees-lower-traders-rotate-perps)); 2024 early-era 5-8% ([MadeOnSol](https://madeonsol.com/blog/pump-fun-first-3-minutes-graduation-math), vendor)
- arXiv preprint 2607.02823 (via search summary): 832,941 launches May 8-Jun 10 2026, pooled 24h graduation rate 0.198% vs 0.63% in Sep-Oct 2025; also warns graduation labels from collectors may carry measurement error — [arXiv](https://arxiv.org/abs/2607.02823) (not read directly)
- Competition: June 2026 DEXTools sample says bots enter ~1 in 4 new pump.fun tokens at launch and almost none graduate — [DEXTools](https://www.dextools.io/news/pumpfun-new-token-bot-activity-data-june-2026) (headline/intro only; methodology unverified)
- Pisa study: 655,770 tokens Sep-Oct 2025, bot vs human transactions distinguished (via search summary of Block/other; results on graduation not seen)
- Predictive model: Marino, Naviglio, Tarantelli, Lillo (Feb 2026) use SOL in bonding curve, launch structure, user behavior features to predict graduation — [arXiv 2602.14860](https://arxiv.org/html/2602.14860v1) (metrics not retrieved)
- Holder signals (vendor, unverified): high-risk tokens' top-10 holders control 30-50% of supply, first 10-20 buyers hold more — [MadeOnSol](https://madeonsol.com/blog/why-pumpfun-tokens-fail-first-hour-find-survivors)
- Tooling: bots detect migration events (Chainstack guide for Raydium migrations, Bitquery for PumpSwap) — [Chainstack](https://docs.chainstack.com/docs/solana-listening-to-pumpfun-migrations-to-raydium), [Bitquery](https://docs.bitquery.io/docs/examples/Solana/pump-fun-to-pump-swap)

### Inferences
- Since migration is permissionless and instant on-chain, the "snipe" edge at the migration moment is latency/priority-fee competition; the structurally less crowded edge is selecting which tokens will graduate (pre-graduation) — but evidence on profitability is absent.
- Graduation base rate swings 0.2%-6.7% by regime, so any signal's precision must be evaluated per-regime.

### Gaps
- No data on sniper profitability, win rates, or latency competition at migration.
- No verified numbers for time-to-graduate or holder count at graduation as predictors of post-migration performance (only graduation prediction at best).
- Full text of DEXTools bot piece, arXiv 2602.14860 and 2607.02823 results need retrieval once arxiv.org/dextools.io are allowed in network settings.
