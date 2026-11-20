# Jito tip economics and transaction landing (as of Nov 2026)

NOTE ON EVIDENCE: Only 1 of 4 web searches returned results (rate-limited after the first); direct fetches of bundles.jito.wtf and solanacompass.com failed (hosts not in the session network allowlist). Anything not linked below is UNVERIFIED (from model training knowledge or arithmetic) and is labelled as such.

## Tip floor API and percentiles

### Takeaway
Jito's tip_floor endpoint publishes landed-tip percentiles (p25/p50/p75/p95/p99 + EMA p50) in SOL. A single 2026 third-party snapshot shows a p50 of ~0.0000875 SOL (~$0.01-0.02), i.e. the baseline floor is tiny; real memecoin trades tip far above it. No live current values could be retrieved.

### Cited Findings
- Endpoint is bundles.jito.wtf/api/v1/bundles/tip_floor; returns 25th/50th/75th/95th/99th percentile landed tips in SOL plus an EMA of the 50th percentile; intended for sizing tips on sendBundle — [QuickNode getTipFloor docs](https://www.quicknode.com/docs/solana/getTipFloor) (via search summary)
- Third-party cached snapshot dated 2026-06-12: p25 ~5.08e-5 SOL, p50 ~8.75e-5 SOL, EMA p50 ~4.51e-5 SOL. Single snapshot from a proxy, not Jito itself — [oanor Jito API](https://oanor.com/api/jito-api/openapi.json)
- QuickNode page example response is dated 2025-04-24 (stale) even though page marked updated Oct 2026 — [QuickNode](https://www.quicknode.com/docs/solana/getTipFloor)
- Chainstack claims Jito tips are >60% of all priority-fee volume by mid-2026, and tip floors rise substantially during token launches/liquidations — [Chainstack](https://chainstack.com/jito-explained-bundles-tips-mev-solana/) (secondary, single claim; not independently checked)
- Jito minimum bundle tip is 1,000 lamports (0.000001 SOL) — UNVERIFIED (training knowledge).

### Inferences
- Percentiles are heavily right-skewed: p50 in the 1e-4 SOL range while p95/p99 are typically orders of magnitude higher (UNVERIFIED, no p95/p99 2026 values obtained).

### Gaps
- Current live p75/p95/p99 values; historical Nov 2026 values. Query the endpoint from an allowed host.

## Typical tips for memecoin trades and landing rate vs tip

### Takeaway
No sourced data found. Common bot/UI practice (UNVERIFIED, training knowledge): sniping/hot launches tip 0.001-0.01+ SOL (sometimes 0.05+), ordinary swaps 0.0001-0.001 SOL. Landing rate rises with tip percentile but is also bound by bundle auction competition and leader being a Jito/BAM validator.

### Cited Findings
- During high competition (launches), tip floors rise substantially — [Chainstack](https://chainstack.com/jito-explained-bundles-tips-mev-solana/)

### Inferences
- Because bundles only land when the leader runs Jito, a tip only matters on those slots; on non-Jito leaders priority fee is the only lever.
- Landing is an auction: tipping at ~p50-p75 gives a reasonable chance for non-contested txs; contested launch slots need >p95 (UNVERIFIED rule of thumb).

### Gaps
- No published landing-rate-vs-tip curve found (searches exhausted).

## BAM (Block Assembly Marketplace) rollout

### Takeaway
BAM is Jito's TEE-based block-building system with validator opt-in. Only evidence found: Jito announced "BAM Direct Bundle Ingest", routing bundles past the Block Engine's ~50ms hop, implying BAM is live in some form by 2026. Adoption/stake figures not verified.

### Cited Findings
- Jito announced BAM direct bundle ingest, bypassing the Block Engine's 50ms hop — [Solana Compass](https://solanacompass.com/news/jito-announces-bam-direct-bundle-ingest-routing-solana-bundles-past-the-block-engines-50ms-hop) (headline from search results only; page not read)

### Inferences
- BAM routing implies tip/bundle flows may bifurcate between Block Engine and BAM nodes; exact tip semantics unverified.

### Gaps
- Mainnet date, % stake on BAM, fee changes, tip account changes. Search failed.

## Jito-Solana stake share

### Takeaway
UNVERIFIED: Jito-Solana (and derivatives) has run on a large majority of stake (commonly cited ~90%+ in 2025). No 2026 figure obtained.

### Cited Findings
- None retrieved.

### Gaps
- Current share (check validators.app / StakeWiz / Jito dashboards).

## Priority fee vs tip trade-off and Alpenglow

### Takeaway
Not researched with sources. Background (UNVERIFIED): priority fee = compute-unit price x CU limit, goes to the leader via scheduler; tip goes through bundle auction, only on Jito leaders, tied to atomic bundle with revert protection. Alpenglow (new consensus: Votor/Rotor, ~150ms finality) activation status and any effect on fees/tips could not be verified.

### Cited Findings
- None retrieved on Alpenglow.

### Inferences
- Faster finality should not itself remove the need for tips; ordering still decided by leader/scheduler (speculation).

### Gaps
- Whether Alpenglow is live on mainnet by Nov 2026; any change to fee/tip mechanics.

## Cost of tips as % of position (computed)

### Takeaway
Tip cost is arithmetic: tip/position. A 0.001 SOL tip is 1% of a 0.1 SOL position but 0.01% of 10 SOL; high-aggression 0.01-0.05 SOL tips are prohibitive for small sizes. Round-trip (buy+sell) doubles the figure.

### Cited Findings
(Own computation, one-way tip as % of position; excludes priority fee, DEX fee, slippage.)

| Position (SOL) | 0.0001 SOL | 0.001 SOL | 0.005 SOL | 0.01 SOL | 0.05 SOL |
|---|---|---|---|---|---|
| 0.1 | 0.100% | 1.000% | 5.000% | 10.000% | 50.000% |
| 0.25 | 0.040% | 0.400% | 2.000% | 4.000% | 20.000% |
| 0.5 | 0.020% | 0.200% | 1.000% | 2.000% | 10.000% |
| 1 | 0.010% | 0.100% | 0.500% | 1.000% | 5.000% |
| 2 | 0.005% | 0.050% | 0.250% | 0.500% | 2.500% |
| 5 | 0.002% | 0.020% | 0.100% | 0.200% | 1.000% |
| 10 | 0.001% | 0.010% | 0.050% | 0.100% | 0.500% |

### Inferences
- Break-even heuristic: for 0.1-0.5 SOL positions keep one-way tip <=0.001 SOL (<=1%/0.2%) unless sniping; for >=5 SOL tipping 0.01 SOL costs only 0.2%.
- Round trip at 0.01 SOL tip on 0.1 SOL position = 20% drag.

### Gaps
- Tip levels used above are illustrative assumptions, not sourced market typicals.
