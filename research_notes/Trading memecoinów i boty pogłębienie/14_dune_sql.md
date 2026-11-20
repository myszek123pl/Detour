# Dune SQL (and alternatives) for memecoin analytics

NOTE: Only 2 of ~6 searches returned (3rd hit a rate limit); no pages were fetched. Everything below is from search-result summaries; table names/SQL from background knowledge are marked UNVERIFIED.

## Relevant Dune tables/spells and example queries (wallet PnL, launch cohorts, graduation rates)

### Takeaway
dex_solana.trades is the curated cross-DEX trades table (about 3h refresh) and is the base for wallet PnL; pump.fun-specific launch/graduation analysis requires decoded pump.fun program tables, which I could not verify. amount_usd is unreliable for illiquid memecoins, so PnL should be computed from SOL legs.

### Cited Findings
- Dune documents a curated Solana DEX trades table (dex_solana.trades), refresh ~3 hours, with an example weekly-volume query — [Dune docs](https://docs.dune.com/data-catalog/curated/dex-trades/solana/solana-dex-trades.md)
- Dune's Solana DEX overview page exists in the data catalog — [Dune docs](https://docs.dune.com/data-catalog/curated/dex-trades/solana/overview)
- CoinGecko's pump.fun trader study (Dune-based) reports share of profitable wallets of 70.0% (March 2026) and 73.3% (April 2026), realized PnL only, so it understates losses; it also flags USD pricing on Dune Solana as derived and possibly missing/stale/distorted for illiquid short-lived tokens — [CoinGecko Research](https://www.coingecko.com/research/publications/pump-fun-traders-are-making-a-comeback) (figures via search summary, not read in full)
- Public dashboard "Solana alpha wallets for all wallets across 31 trading bots & an In-depth Wallet PNL Scanner" by dev2020 — [Dune](https://dune.com/dev2020/solana-alphas)
- Public query "2026-05-27 Solana pumpfun pumpswap 90d token prefilter 5m plus NV2" (token prefilter over pump.fun/PumpSwap) — [Dune](https://dune.com/queries/7586387)
- Bitquery (alternative) offers Solana DEX API with GraphQL/WebSocket/Kafka/gRPC, wallet trade history with USD price per swap for realized PnL, and PumpSwap docs — [Bitquery](https://bitquery.io/products/solana-dex-api), [PumpSwap docs](https://docs.bitquery.io/docs/blockchain/Solana/Pumpfun/pump-swap-api/)

### Inferences
- Wallet PnL sketch (UNVERIFIED column names; check schema): from dex_solana.trades filter project IN ('pumpdotfun','pumpswap') [project names unverified], group by trader_id + token, sum SOL out/in per side; realized = sells - buys for closed positions; avoid amount_usd, price SOL separately.
- Launch cohorts: bucket tokens by first-trade date (min(block_time) per token_bought/sold mint); graduation = token appears in PumpSwap/Raydium pool-creation or migration event; rate = graduated / created per cohort. Needs pump.fun decoded tables (e.g. pumpdotfun_solana.* — UNVERIFIED names) for create/complete events.
- Flipside (solana.defi.ez_dex_swaps etc.) and Allium (solana.dex.trades) are alternatives; names from memory, UNVERIFIED.

### Gaps
- Actual decoded pump.fun table names, tokens_solana schema, solana.transactions usage: not verified (search budget lost).
- Flipside and Allium current offerings/pricing in Nov 2026: not searched.
- Authors' methodologies for dashboards beyond titles: not read.
- Graduation-rate figures: search failed.

## Dashboards, API export for bots, costs/credits

### Takeaway
Dune's free tier is reportedly view-only now (sources conflict), paid plans start roughly $75-399/mo, and API export is billed per datapoint, so bots needing frequent fresh data should cache results or use streaming providers.

### Cited Findings
- Credits scale with compute actually used and performance tier; unfetched results cost only execution; failed executions are charged (per one docs note); credits also consumed on API/CSV export — [Dune docs](https://docs.dune.com/resources/credits-billing/how-credits-work), [billing](https://docs.dune.com/api-reference/overview/billing)
- Rate card per search summary: 10 credits medium engine, 20 large, 1 credit per 1,000 datapoints exported; Free 2,500 credits, Plus $399/mo — [Dune pricing FAQs](https://docs.dune.com/learning/how-tos/pricing-faqs) (UNVERIFIED, from summary)
- Third-party aggregator lists Analyst $75/mo with 4,000 credits; last verified June 2026 — [Costbench](https://www.costbench.com/software/onchain-analytics/dune-analytics/)
- Report: from Sept 10, 2026, accounts created before July 21, 2026 lose query execution without upgrade; Dune docs say free is view-only (no credits/execution/API); aggregator still lists API on free — contradictory — [Crypto Briefing](https://cryptobriefing.com/dune-free-plan-view-only-access/), [Dune blog](https://dune.com/blog/new-paid-experience)
- API is async: execute, poll execution ID, fetch results; usage endpoint free; credit cap setting exists — [Dune API docs](https://docs.dune.com/api-reference/overview/getting-started.md)
- Bitquery streaming (WebSocket/Kafka/gRPC) is the lower-latency alternative for bots — [Bitquery](https://bitquery.io/products/solana-dex-api)

### Inferences
- With ~3h table lag, Dune suits research/wallet-list generation (e.g. alpha-wallet scanners) rather than real-time sniping.

### Gaps
- Current exact plan prices/credit limits: verify at dune.com/pricing.
- Flipside/Allium pricing, free-tier status: not researched.
- Other popular pump.fun dashboards (e.g. by hildobby, etc.): not found; not verified.
