# Market-data APIs for memecoin bots (DEX Screener, Birdeye, GeckoTerminal, Jupiter Price, Solana Tracker, Moralis, Codex, Mobula)

Research status (2026-11-20): search budget was hit after 3 successful searches; docs hosts (docs.dexscreener.com, docs.birdeye.so, docs.solanatracker.io, geckoterminal.com) were unresolvable for WebFetch (blocked in session network). Coverage is therefore PARTIAL: Birdeye, Solana Tracker, Codex, Moralis, Mobula have some sourced snippets; DEX Screener, GeckoTerminal, Jupiter have NO sourced findings (only unverified memory, listed under Gaps/Inferences).

## Endpoints/fields, rate limits, pricing tiers, WebSocket availability

### Takeaway
WebSocket streaming is gated/paid at Birdeye (reportedly Business tier or contact-sales overage) and Solana Tracker (Premium+); Codex advertises WebSockets; Moralis has webhooks (Streams) rather than price WebSockets. Exact per-tier rate limits are mostly unpublished or unverified.

### Cited Findings
- Birdeye pricing page says WebSocket data uses different overage pricing; contact Birdeye team for details — [Birdeye pricing](https://docs.birdeye.so/docs/pricing)
- Birdeye Solana WebSocket endpoint format: wss://public-api.birdeye.so/socket/solana?x-api-key=KEY — [Birdeye WebSocket docs](https://docs.birdeye.so/docs/websocket)
- Birdeye tiers: Free, Premium, Business, Enterprise; account-level limit shared across APIs; transaction-simulation endpoint capped at 30 req/min — [Birdeye rate limiting](https://docs.birdeye.so/docs/rate-limiting)
- Birdeye limits are per API key and vary by plan; confirm with support — [Birdeye support](https://support.birdeye.com/en/articles/12654181-birdeye-s-developer-portal)
- Birdeye x402 pay-per-request: 100 req/s per IP applied before payment verification, 429 on exceed — [Birdeye x402](https://docs.birdeye.so/reference/x402.md)
- Unofficial claim: Birdeye WebSocket only for Business package — [GitHub gist](https://gist.github.com/Klaudioz/827a5c0e45d6227d7bbbd0f5bdd0b424); third-party price claims conflict: Toolradar says cheapest paid "Starter" $299/mo (self-rated low confidence) [Toolradar](https://toolradar.com/tools/birdeye/pricing.md); MadeOnSol says WebSocket firehose is in an "Ultra" tier rather than gated at $199 [MadeOnSol](https://madeonsol.com/api-alternatives/birdeye)
- Supergood (Jul 2026) review: Birdeye rate limits unpublished, vary by plan — [Supergood](https://supergood.ai/api-report-card/birdeye)
- Solana Tracker: WebSocket Datastream starts at Premium plan and above; prices in EUR; Enterprise+ custom; Raptor hosted API has no published pricing — [Solana Tracker pricing](https://docs.solanatracker.io/pricing); a preview page lists Business at EUR 599/mo (may be outdated) — [preview](https://preview.solanatracker.io/data-api)
- Codex: free tier 20,000 credits/month — [Codex blog](https://www.codex.io/blog/solana-api-guide); Codex claims WebSockets across ~20 endpoints (vendor claim) — [Codex vs Moralis](https://www.codex.io/compare/codex-vs-moralis); Codex rate-limit doc exists — [Codex rate limits](https://docs.codex.io/concepts/rate-limits) (contents not read)
- Moralis: no price-streaming WebSocket; Streams delivers on-chain events via HTTP webhooks (competitor/third-party sources) — [Codex vs Moralis](https://www.codex.io/compare/codex-vs-moralis)
- Mobula: free tier and a $50 Start-up tier listed (Slashdot, may not be current); REST+WebSocket+webhooks claimed in a promotional post — [Slashdot](https://slashdot.org/software/p/Mobula/), [DEV post](https://dev.to/boba_bobo_c54aa2b42146177/why-mobula-stands-out-as-the-best-crypto-data-api-in-2026-8ne)

### Inferences
- Budget bots needing push data likely choose Solana Tracker Premium, Codex, or direct on-chain (gRPC/RPC) streams instead of polling REST; Moralis is a weak fit for Solana memecoin sniping.
- Vendor comparison pages (Codex, Solana Tracker, Mobula) are marketing; treat as biased.

### Gaps
- No sourced data on DEX Screener (endpoints, limits), GeckoTerminal (free rate limit, new_pools/trending_pools), Jupiter Price API (v2/v3, limits, lite/pro hosts), Moralis/Mobula/Codex Solana pricing and limits, Birdeye per-tier rps and endpoint names (new listing, token_security, holders). Unverified recollection only (must be confirmed): DEX Screener free API roughly 60 rpm on profile/boost endpoints and 300 rpm on pairs/search; GeckoTerminal free ~30 calls/min; Jupiter moved to api.jup.ag with API keys.

## Latency vs on-chain; reliability and data quality

### Takeaway
No quantitative latency benchmarks were found. Aggregator REST data is indexed after the fact and should be assumed seconds behind on-chain; only vendor claims exist.

### Cited Findings
- Birdeye rate limits are unpublished and plan-dependent, a reliability/planning concern flagged by Supergood — [Supergood](https://supergood.ai/api-report-card/birdeye)
- Third-party price analyses of Birdeye conflict with each other (see above), indicating opaque/changing pricing — [Toolradar](https://toolradar.com/tools/birdeye/pricing.md), [MadeOnSol](https://madeonsol.com/api-alternatives/birdeye)

### Inferences
- Bots should treat aggregator APIs for discovery/enrichment and use Geyser/gRPC or RPC for execution-critical signals.

### Gaps
- No sourced latency measurements, outage history, or known data-quality issues (wash trading, bad holder counts, stale/incorrect liquidity, price spikes on illiquid pools) for any provider. Follow-up needs allowing docs hosts and further searches.
