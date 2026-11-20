# Memecoin arbitrage on Solana (DEX-DEX, CEX-DEX, atomic bots, Jito) — as of Nov 2026

Method note: 4 searches returned results, 1 failed (rate limit); no page fetches. Most Solana profit figures come from vendor blogs and are marked UNVERIFIED. Items without a source are in Gaps or marked as my own inference.

## 1. How big is Solana arbitrage and what are the per-trade economics?

### Takeaway
Solana arbitrage is huge by count (~90M successful arbs/yr per Jito detection) but thin per trade (~$1.58 average, UNVERIFIED). Aggregate profit (~$142.8M) is spread over a few professional searchers.

### Cited Findings
- Jito's arbitrage detection counted 90,445,905 successful arbitrage transactions over one year, including some outside Jito bundles; bundles are the main tool searchers use for ordering — [Helius Solana MEV report](https://www.helius.dev/blog/solana-mev-report)
- ~$142.8M combined profit from those 90M+ arbs — figure repeated by vendor blogs, UNVERIFIED, not traced to Jito/Helius — [Helius](https://www.helius.dev/blog/solana-mev-report) (search summary), [Bybit wiki](https://www.bybit.com/wiki/article/solana-arbitrage-strategies-bots-2025/)
- Average profit per arb ~$1.58 — UNVERIFIED; one source repeated by another, not independent — [Bybit wiki](https://www.bybit.com/wiki/article/solana-arbitrage-strategies-bots-2025/)
- Helius report: >3 billion Jito bundles, 3.75M SOL tips in a year; the report notes it does not capture activity via alternative mempools — [Helius](https://www.helius.dev/blog/solana-mev-report)
- Arbitrage claimed to be ~50% of Solana DEX volume in 2025; sources conflict on wording (UNVERIFIED) — [Bybit wiki](https://www.bybit.com/wiki/article/solana-arbitrage-strategies-bots-2025/)
- Example of an outlier memecoin MEV win: a bot earned ~$1.8M back-running one memecoin trader (2023; this is sandwich/back-run, not pure arb) — [The Block](https://www.theblock.co/amp/post/272079/solana-based-mev-bot-earns-1-8-million-after-back-running-memecoin-trader-in-seconds)

### Inferences
- $142.8M / 90M ≈ $1.58, so the two UNVERIFIED figures are mutually consistent (likely the same derived number, not independent evidence).
- Mean is dominated by a long tail of micro-trades plus rare large events; newcomer expectations should not be based on the mean.

### Gaps
- No audited per-searcher profit distribution; no Jito-official 2026 data found.
- Share attributable to memecoin pairs specifically not found.

## 2. Competition, Jito tips and atomic bots

### Takeaway
Competition is a price auction: searchers bid 50-60% (some sources 20-50%) of expected profit as Jito tip, so margins left to the searcher are small and shrinking; the field is dominated by co-located, Rust-based pro operators.

### Cited Findings
- 2023 post by a Jito/Ellipsis cofounder: atomic arb tips were 20-50% of available MEV and rising — [Helius MEV intro / Mirror summary](https://www.helius.dev/blog/solana-mev-an-introduction)
- 2025 blog estimate: searcher earning $1,000 pays ~$500-600 to the validator — UNVERIFIED — [Helius report / vendor blogs](https://www.helius.dev/blog/solana-mev-report)
- 100% of bundle tips go to validator and stakers — [Helius](https://www.helius.dev/blog/solana-mev-report)
- Jito tips rose from ~10% of Solana priority-fee volume (Apr 2023) to >60% by end-2024 and stayed above through 2025/26 — [RPC Fast](https://rpcfast.com/blog/jito-explained-bundles-tips-mev-solana) (vendor)
- Claim that >50% of Solana transactions are failed arb attempts (spam) — secondhand, UNVERIFIED — [Blockworks](https://blockworks.co/news/solana-spam-problem)
- Vendor claim: most arb bots earn nothing or lose money — unsourced assertion, UNVERIFIED — [RPC Fast](https://rpcfast.com/blog/solana-arbitrage-bot-setup)
- Production searchers track bundle landing rate and tune tips dynamically — [RPC Fast](https://rpcfast.com/blog/jito-explained-bundles-tips-mev-solana)
- Firedancer/Alpenglow expected to change MEV dynamics (speculative) — [Coinmonks/Medium](https://medium.com/coinmonks/solana-mev-enters-a-new-phase-how-firedancer-and-alpenglow-change-the-game-6eba6bd0efb3)
- A tiny cluster of bots reportedly gained a ~3x advantage via a proprietary routing protocol (concentration signal; details not verified) — [CryptoSlate](https://cryptoslate.com/a-tiny-cluster-of-solana-bots-unlocked-a-3x-trading-advantage-by-routing-through-one-proprietary-protocol/)

### Inferences
- Atomic arb (revert on loss) limits capital risk to tips/fees on landed bundles, but failed-attempt costs (RPC, infra, spam fees) are the real drain for newcomers.
- Concentration plus tips ~50%+ means a newcomer wins mostly what incumbents ignore (very small or exotic-pool spreads).

### Gaps
- Not verified: current (Nov 2026) tip share; Jito bundle auction changes; any Jito-published searcher leaderboard.

## 3. DEX-DEX memecoin pool arbitrage (Raydium / PumpSwap / Meteora / Orca)

### Takeaway
Remaining edge is claimed to be in thin, fresh pools (PumpSwap, Meteora DLMM, launchpad pairs) rather than majors, but this is practitioner opinion; my search on PumpSwap/Raydium specifics failed.

### Cited Findings
- Realistic edge reportedly moved to thin liquidity: fresh launchpad pools and niche pairs on PumpSwap and Meteora DLMM — practitioner opinion, UNVERIFIED — [RPC Fast](https://rpcfast.com/blog/solana-arbitrage-bot-setup) (vendor)
- Jupiter is mainly a routing layer; a self-hosted jupiter-swap-api can be queried locally at ms latency over 30+ DEXs — [RPC Fast](https://rpcfast.com/blog/solana-arbitrage-bot-setup)
- ≥40% of Jupiter volume estimated to be atomic arbitrage — secondary summary, UNVERIFIED — [Messari](https://messari.io/report/solana-dex-winners-all-about-order-flow)

### Inferences
- (Own reasoning, no source) Memecoin pools have small TVL, so profitable size per arb is capped by pool depth, and rug/honeypot/token-extension risk is high; low-cap arbs yield dollars to tens of dollars each.

### Gaps
- Per-venue fee tiers, PumpSwap fee structure and per-pool arb frequency not verified (search failed).
- No data on memecoin-only arb profit.

## 4. CEX-DEX arbitrage

### Takeaway
Window after a CEX move is measured in slots (~400 ms) on Solana (vendor claim); needs co-location and inventory on both sides; memecoins mostly lack deep CEX listings, so it applies mainly to listed majors/large memes.

### Cited Findings
- Claimed Solana DEX price-catch-up window is in slots rather than seconds — vendor claim, no measured data, UNVERIFIED — [RPC Fast](https://rpcfast.com/blog/solana-arbitrage-bot-setup)
- CEX-DEX adds withdrawal delays, custody risk, slower execution — [Dysnix](https://dysnix.com/blog/solana-arbitrage-bot-setup)
- Ethereum academic work: CEX-DEX arb remains profitable despite barriers (capital, low-latency infra, inventory risk, inclusion uncertainty); may not transfer to Solana — [arXiv 2507.13023](https://arxiv.org/pdf/2507.13023v1), [Devcon 7 talk](https://archive.devcon.org/devcon-7/latency-advantage-in-cex-dex-arbitrage)

### Inferences
- A newcomer cannot compete on latency with pro market makers; CEX-DEX is poor fit for small capital.

### Gaps
- No Solana-specific CEX-DEX profit data; no memecoin CEX-DEX evidence.

## 5. Capital needs and realistic returns for a newcomer

### Takeaway
Atomic arb needs little trading capital (a few SOL for tips/fees, as flash-loan-free cycles start from SOL balance) but demands engineering skill and paid low-latency infra (my inference); evidence indicates most bots do not profit. Treat as a skill/infra business, not passive income.

### Cited Findings
- Most arb bots reportedly unprofitable (UNVERIFIED vendor claim) — [RPC Fast](https://rpcfast.com/blog/solana-arbitrage-bot-setup)
- Production setups use local Jupiter API, dedicated RPC/shreds, bundle-landing feedback loops — [RPC Fast](https://rpcfast.com/blog/solana-arbitrage-bot-setup), [Dysnix](https://dysnix.com/blog/solana-arbitrage-bot-setup)
- Average $1.58/arb (UNVERIFIED) implies profit needs high volume and low costs — [Bybit wiki](https://www.bybit.com/wiki/article/solana-arbitrage-strategies-bots-2025/)

### Inferences
- (Own estimate, unsourced) Infra for competitive operation (dedicated server/colocated RPC, Yellowstone gRPC) plausibly costs hundreds to low thousands USD/month; tip share 50%+ makes break-even hard under $1k-ish expected profit per day. Treat as speculative.
- Realistic newcomer outcome: break-even to net loss for first months; upside only with a niche (new pool types, long-tail pairs) before incumbents integrate.

### Gaps
- No sourced capital requirement figures, infra costs, or newcomer outcome statistics.
- Searches for PumpSwap/Raydium-specific arb and Jito 2026 data were incomplete (6-search budget; one rate-limited).
