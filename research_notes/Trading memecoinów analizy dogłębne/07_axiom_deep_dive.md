# Axiom Pro trading terminal: deep dive (as of Nov 2026)

NOTE ON METHOD: only 3 web searches ran (the 3rd hit a rate limit) and all WebFetch calls failed (medium.com, publish0x.com, sacra.com not resolvable from this sandbox). Findings below rest on search-result summaries, not full-page reads. Treat all as medium/low confidence. No official Axiom docs were found.

## Features (Pulse, filters, wallet tracker, migration sniping, limit orders, perps)

### Takeaway
Only Pulse-style filtering was confirmed from sources: Axiom exposes ~15 screening filters including dev holdings, sniper %, insider %, bundle %. Wallet tracker, migration sniping, limit orders and perps were NOT verified in this session.

### Cited Findings
- Axiom offers fifteen screening filters, including developer holdings, sniper %, insider %, bundle % (plus age, market cap, volume, liquidity, holder count, top-10 concentration) — [Solana Compass](https://solanacompass.com/projects/axiom)
- Guides describe Snipers % as a filter for bot-heavy tokens and Insiders % as a way to reduce insider-dump risk — [DEV Community Axiom Pulse guide](https://dev.to/crypto_blog/axiom-pro-trade-pulse-a-pro-dashboard-for-real-time-alpha-from-pumpfun-and-beyond-31mj)
- Third-party guides exist on Axiom filter setup and memecoin trading — [Publish0x filter guide](https://www.publish0x.com/wagmiwhiz/setting-up-your-first-profitable-filter-on-axiom-degen-editi-xeorzgv), [Boxmining guide](https://www.boxmining.com/axiom-memecoin-trading-guide) (contents not read)
- Mobula publishes an "Axiom data API" cookbook, suggesting Axiom-like metrics can be reproduced via third-party data — [Mobula](https://docs.mobula.io/cookbooks/axiom-data-api) (not read in full)

### Inferences
- Pulse is a real-time new-pair/migrating/migrated token feed with per-column filters (consistent with the guide titles, but column structure not verified).

### Gaps
- Wallet tracker, migration sniping, limit orders, perps (launch date, fees, leverage): not verified; fetch Axiom docs/blog/X directly.

## Fee levels and revenue/volume data

### Takeaway
Base fee reported as 1% per trade with a 3-level referral share. DeFiLlama shows roughly $28.3M fees / $13.4M revenue trailing 30d and $37.5M fees / $18.4M revenue for Sept 2026; sources disagree on cumulative totals.

### Cited Findings
- Trailing 30d fees $28.29M, protocol revenue $13.37M; Sept 2026 fees $37.47M, revenue $18.35M; 30d DEX volume $2.343B (floor, unindexed venues excluded) — [DeFiLlama Axiom](https://defillama.com/protocol/axiom) (via search summary)
- RootData: Oct 2026 protocol income $13.2M, Sept $18.38M — [RootData](https://www.rootdata.com/projects/detail/Axiom?k=MTM1ODQ%3D)
- Cumulative: ~$763M fees per DeFiLlama vs ~$390M estimated protocol fees and >$15B volume by mid-2026 in another report — conflicting; [DeFiLlama](https://defillama.com/protocol/axiom), [Sacra](https://sacra.com/c/axiom)
- Base fee 1% of swap amount; referrals 3-level revenue share — [Axiom fees guide (Medium)](https://medium.com/@crypto-deploy/axiom-trade-fees-what-you-actually-pay-and-how-to-pay-less-0df290e57f7b) (summary only)
- Axiom reached $200M revenue fastest among apps — [Step Data](https://stepdata.substack.com/p/solana-trading-bot-axiom-becomes) (headline only)
- Market share ~44.6% of Solana terminal daily volume in June 2026; FOMO overtook Axiom on daily volume on Aug 6, 2026 — [Solana Compass on FOMO](https://solanacompass.com/news/fomo-captures-46-of-solana-trading-platform-spot-volume-as-weekly-revenue)

### Inferences
- Revenue fell from Sept to Oct 2026 (~$18.4M to ~$13.2M) alongside share loss to FOMO.
- Fee tiers/discounts: not confirmed (an unverified recollection is that fees were ~1% with Pro-level discounts; do not rely on it).

### Gaps
- Tiered fee levels, perps/limit-order fees, per-chain fee differences; reconciling the revenue figures.

## Metrics definitions (dev, insiders, bundlers, snipers, top10)

### Takeaway
No official Axiom definitions found. Industry-standard definitions from data-provider docs are below; thresholds vary by guide.

### Cited Findings
- Dev: deployer wallet; early dev selling is a red flag — [Solana Compass / search summary](https://solanacompass.com/projects/axiom)
- Snipers: wallets that buy within the first few blocks/seconds — [InsightX](https://docs.insightx.network/reference/dex-metrics-api-overview), [Solana Tracker](https://docs.solanatracker.io/guides/sniper-detection.md)
- Bundlers: wallets doing coordinated multi-wallet swaps to accumulate while appearing separate — [InsightX](https://docs.insightx.network/reference/websocket-dex-metrics), [Mobula](https://docs.mobula.io/almanac/detecting-snipers-bundlers)
- Insiders: wallets linked to creator/deployer by funding or movement patterns — [InsightX](https://docs.insightx.network/reference/dex-metrics-api-overview)
- Example thresholds: dev holdings <5% in one guide, <10% in another (guides not read in full) — search summaries above

### Inferences
- Axiom's own numbers are likely heuristic clustering (funding-graph + same-slot buys), so they can under/over-count; a custom bot should compute its own.

### Gaps
- Axiom's exact formulas; top10 definition (assumed: top 10 holders' share excluding LP/bonding curve; unverified).

## Controversies

### Takeaway
One major allegation found: Feb 2026 ZachXBT claims of insider trading via internal tools.

### Cited Findings
- In February 2026, ZachXBT alleged Axiom executives misused internal tools for insider trading — [search summary of DeFiLlama/Sacra-era coverage](https://defillama.com/protocol/axiom) (weakly attributed; primary source not retrieved)

### Gaps
- Axiom's response, outcome, any earlier incidents (e.g., 2025 security/wallet-access issues): not verified. Rate limit blocked the controversy search.

## Which filters traders actually use, and lessons for a custom bot

### Takeaway
Guides emphasize dev %, snipers %, insiders %, bundlers %, top10, holders, and age/volume; empirical usage data not found.

### Cited Findings
- Guides stress snipers %, insiders %, dev holdings as core risk screens — [DEV Community](https://dev.to/crypto_blog/axiom-pro-trade-pulse-a-pro-dashboard-for-real-time-alpha-from-pumpfun-and-beyond-31mj), [Solana Compass](https://solanacompass.com/projects/axiom)

### Inferences (design suggestions, not sourced)
- Use filters as a pre-screen (hard cutoffs on dev %, bundle %, insider %, top10) then rank by momentum/volume/holder growth.
- Because platform metrics are heuristic and widely gamed (bundlers split wallets), treat them as noisy features and backtest thresholds rather than copying guide values.
- Since many traders use identical filters, crowded signals decay; expect edge to come from combining with wallet-quality and flow data.
- Latency matters for snipers metric: it is computed from the first blocks, so evaluate after N seconds.

### Gaps
- No empirical filter-usage statistics; no official presets from Axiom; recommend reading the Publish0x/Boxmining guides directly once network access allows.
