# Capital-flow leading indicators for memecoin activity (as of Nov 2026)

Method note: only 2 of ~5 planned searches returned results (the third hit a rate limit). Findings rest on search-result summaries, not fetched primary pages. Treat all figures as UNVERIFIED unless re-checked at source.

## Do stablecoin supply / net inflows (Solana, Base) lead memecoin volume or prices?

### Takeaway
No rigorous evidence found that stablecoin supply or inflows reliably lead memecoin volume or prices. Coverage is news-level and mixed. Spikes tend to be event-driven, and supply has grown while prices fell.

### Cited Findings
- Blockworks frames stablecoin supply as a possible leading signal for rallies but questions how well it holds. Solana stablecoin supply was reportedly flat at about $1.5B for six months before a rally (figure as summarized, UNVERIFIED; likely an older period) — [Blockworks](https://blockworks.com/news/empire-newsletter-stablecoins-rally-indicators)
- Solana stablecoin supply reportedly rose 57% after the Trump memecoin launch, i.e. an event-driven spike (UNVERIFIED) — [Blockworks](https://blockworks.com/news/solana-stablecoin-supply-soars)
- Stablecoin supply reportedly kept rising through a market decline, which cuts against a simple "stablecoins lead price" story (UNVERIFIED, date unclear) — [Blockworks](https://blockworks.com/news/empire-newsletter-stablecoins-rally-indicators)
- Solana stablecoins described as "stickier than anticipated" — [Blockworks](https://blockworks.com/news/solana-stablecoins-stickier-than-anticipated)
- A Solana stablecoin supply dip led by a $1.8B USDC outflow was reported, along with a cryptorank item on stablecoins flowing out at a meme peak (both UNVERIFIED; the second hints at outflows coinciding with peaks, not leading) — [Blockworks](https://blockworks.co/news/solana-usdc-stablecoin-outflow), [Cryptorank](https://cryptorank.io/news/feed/c01a0-stablecoins-flow-out-of-solana-meme-peak)
- Solana stablecoin supply about $15.6B in Q2 2026 (+1.9% QoQ, Galaxy); DefiLlama showed $14.75B on June 25. USDC share fell to 47% — [Galaxy Q1 2026](https://www.galaxy.com/insights/research/solana-q1-2026-dex-rwa-stablecoins-market-share), [Analytics Insight](https://www.analyticsinsight.net/news/solana-memecoin-volume-rebounds-as-stablecoins-retain-the-lead) (Q2 figures as relayed in search summary; UNVERIFIED)
- Base: $7.8B stablecoin inflows in 2024, $3.5B net retained (UNVERIFIED, one secondary source in search summary). No Base memecoin-linked flow data found.

### Inferences
- Stablecoin supply is a slow-moving regime variable (risk appetite / dry powder), not a timing signal. Short event spikes (e.g., a hyped launch) look like coincident or lagging indicators.
- Stablecoin outflow at meme peaks suggests flow reversal may be coincident with tops; a testable hypothesis, not established.

### Gaps
- No lead-lag study (cross-correlation, Granger) of stablecoin net flows vs memecoin volume or prices found.
- No Base-specific memecoin evidence; no data on Base stablecoin supply in 2026.

## Bridge inflows, CEX SOL withdrawals, new wallet creation

### Takeaway
Nothing citable found for these three in the searches run. Marked as gaps.

### Cited Findings
- None. Related snippet only: AMBCrypto reported "$1.3B flows back into Solana" (context not verified) — [AMBCrypto](https://ambcrypto.com/1-3b-flows-back-into-solana-is-sol-poised-for-a-reversal/)

### Inferences
- Plausible but unverified: bridge net inflows (DefiLlama bridges) and CEX outflows may precede activity; new-wallet counts are noisy because of bots/sybils on Solana.

### Gaps
- No evidence on CEX SOL withdrawals leading memecoin volume.
- No evidence on bridge inflows (e.g., Wormhole, deBridge, Circle CCTP, Base bridge) leading volume.
- No evidence on new wallet creation as a leading signal and its bot-contamination.

## SOL DEX volume and memecoin share (coincident indicators)

### Takeaway
Memecoin share of Solana DEX volume is volatile and cyclical; volume itself is coincident with, not leading, memecoin activity.

### Cited Findings
- Memecoins reached 29% of Solana weekly spot DEX volume in late July 2026, the highest share since August 2025; stablecoin-related pairs were 59% (SOL-stable 37%, stable swaps 22%) — [Mitrade](https://www.mitrade.com/insights/news/live-news/article-3-1942083-20260729)
- Solana DEX volume fell 31% QoQ in Q1 2026, the second-largest quarterly decline since 2022; Galaxy put Solana share at 41% — [Galaxy](https://www.galaxy.com/insights/research/solana-q1-2026-dex-rwa-stablecoins-market-share). Birdeye H1 2026 cites 54% of global DEX spot — [Solana Compass](https://solanacompass.com/news/birdeyes-h1-2026-solana-report-54-dex-share-6x-tokenized-equity-growth-and-a-perps-lead-over-hyperliquid); KuCoin cites about 36% — [KuCoin](https://www.kucoin.com/news/flash/solana-dex-volume-surpasses-10-billion-outpaces-nyse-american). Sources conflict on share (methodology differences).
- Reported 82% DEX volume drop as meme activity slowed; a Dune-based report put weekly volume at about $18.8B in late May vs about $104B two weeks earlier, heavily influenced by Meteora (UNVERIFIED, odd magnitude) — [KuCoin](https://www.kucoin.com/news/flash/solana-dex-volume-drops-82-as-meme-coin-activity-slows)
- New meme launches reportedly roughly halved in early 2026 (UNVERIFIED) — [Analytics Insight](https://www.analyticsinsight.net/news/solana-memecoin-volume-rebounds-as-stablecoins-retain-the-lead)

### Inferences
- Most "volume" is stablecoin/SOL pair or wash/arb flow, so total DEX volume is a poor memecoin proxy; use memecoin-share or launchpad-specific metrics.

### Gaps
- Chain-wide volume data is contaminated by bots/MEV; no clean lead-lag evidence found.

## Data sources (Artemis, DefiLlama, Dune, Token Terminal)

### Takeaway
No search results for this question (rate limit). The descriptions below are from general knowledge, UNVERIFIED, and uncited.

### Cited Findings
- Galaxy and Birdeye cite DefiLlama and Dune in the Solana DEX analyses above (see links in the previous section); Dune-based weekly volume was cited by KuCoin.

### Inferences
- Likely mapping (unverified): DefiLlama for stablecoins-by-chain and bridge net flows (free API); Artemis for cross-chain stablecoin, active address and DEX volume metrics; Dune for custom SQL (CEX withdrawals via labeled wallets, new wallets, launchpad volume); Token Terminal for protocol fees/revenue, less relevant to flows.

### Gaps
- Current API access, pricing, and metric definitions for all four not verified; Nov 2026 feature changes unknown.
