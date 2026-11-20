# Wallet clustering: graph-analysis methods and tools (research notes)

STATUS: web search was unavailable (rate limited / 5-hour limit hit; 0 of ~6 searches returned results). No claim below is backed by a fetched source. Everything is from model background knowledge (cutoff mid-2026) and is UNVERIFIED. Nothing is placed under "Cited Findings" because no URLs were retrieved. Re-run with working search before relying on any detail.

## Which heuristics work on account-based chains like Solana (vs Bitcoin UTXO), and what precision/recall evidence exists?

### Takeaway
Bitcoin's co-spend (common-input-ownership) heuristic has no direct analogue on account-based chains; Solana clustering relies on funding-graph (common funder / first-funder), deposit-address/sweep patterns, and behavioral similarity, with exchange/bridge/program filtering essential. Rigorous precision/recall numbers for Solana were not found (search unavailable).

### Cited Findings
- None retrieved (search failed).

### Inferences (all unverified, from background knowledge)
- Bitcoin: multi-input (co-spend) and change-address heuristics are the standard (used by GraphSense, Chainalysis-style tools). Not applicable to account chains because a tx has one fee payer/signer set per account model; Solana multi-signer txs are the nearest analogue (co-signers/fee-payer sharing) but are rare and often benign (relayers).
- Ethereum literature (unverified pointers to verify: Victor 2020 "Address clustering heuristics for Ethereum" - deposit address reuse, airdrop multi-participation, self-authorization heuristics; Béres et al. on Ethereum clustering; Friedhelm Victor reported heuristics produce clusters with limited ground-truth validation, precision largely evaluated against labeled exchange data). Treat as pointers only.
- Solana-applicable heuristics, roughly by reliability:
  1. Fee-payer / co-signer sharing (high precision, low recall; beware relayers, Jito/bundlers, trading bots' shared fee payers).
  2. Common first funder (first inbound SOL) for fresh wallets (medium-high precision when funder is a private wallet; near-useless if funder is CEX hot wallet, bridge, faucet, or program PDA -> must blocklist).
  3. Fan-out funding: one wallet funds N wallets within short window with similar amounts (high signal for sniper/bundle farms).
  4. Sweep/consolidation: N wallets send remaining SOL/tokens to one destination (reverse funding graph).
  5. Same-slot / same-block buys of a token (bundling), identical amounts, identical Jito tip patterns.
  6. Token transfers between holders of the same mint (direct holder-to-holder links) - what Bubblemaps-style maps emphasise (unverified).
  7. Temporal/co-trading similarity (same tokens bought within seconds, similar sizing) - lower precision, popular tokens create false positives; use IDF-style weighting by token popularity.
- Pitfalls: CEX withdrawals, dust/airdrop spam, program-owned accounts, LP/DEX vault accounts, wallet-drainer noise, deliberate obfuscation via intermediaries and mixers.
- Expect precision/recall to be unmeasured in practice: ground truth for "same owner" is rarely available; papers evaluate against exchange labels or self-reported/airdrop-hunter sets.

### Gaps
- No verified precision/recall numbers for any heuristic; no Solana-specific peer-reviewed evaluation located.
- Need to verify Victor 2020 and follow-up papers' exact metrics, and any 2024-2026 Solana Sybil/bundle detection papers.

## Graph methods: union-find, co-trading similarity, Louvain/Leiden, GNNs

### Takeaway
Hard-link heuristics (high precision) fit union-find; soft signals (co-trading, temporal) fit weighted graphs with community detection (Leiden preferred over Louvain); GNNs are for labeled classification (illicit/bot) and need labeled data. All unverified here.

### Cited Findings
- None retrieved.

### Inferences (unverified)
- Union-find (disjoint set): near O(alpha(n)) per union, naturally incremental, memory O(wallets). Risk: transitive over-merging (one bad edge, e.g. an exchange, merges huge clusters) -> mitigate by edge whitelisting, degree caps (skip funders with > K recipients unless within tight time window), and keeping edge provenance so merges can be undone (union-find cannot split; keep edge log and rebuild or use weighted graph for the soft tier).
- Two-tier design: tier 1 hard links (fee payer, fan-out, sweep) via union-find; tier 2 soft similarity edges (co-buy timing, amount similarity) in weighted graph with confidence scores; report "cluster + confidence", not a binary.
- Louvain vs Leiden: Leiden (Traag et al. 2019, believed correct) guarantees connected communities and is faster/better quality; Louvain can yield disconnected communities. Both are modularity-based with resolution parameter and are batch methods; dynamic variants exist (e.g. Delta-screening / dynamic Leiden - names unverified). Fit for offline/periodic re-clustering per token holder subgraph (hundreds-thousands of nodes), not per-transaction.
- Co-trading similarity: build wallet x token (or wallet x time-bucket) matrix; Jaccard / cosine with popularity down-weighting; MinHash/LSH for scalable candidate generation. Temporal: cross-correlation of trade timestamps, same-slot co-occurrence counts.
- GNNs (GCN/GraphSAGE/GAT, node2vec embeddings + classifier): need labels; known on Ethereum/Bitcoin for illicit-account detection (e.g. Elliptic dataset); transfer to Solana memecoin clustering not verified. Likely overkill for a bot; embeddings (node2vec) can add a soft-similarity signal if needed.

### Gaps
- No verified benchmark comparing Louvain/Leiden/union-find on crypto wallet data; no verified GNN results on Solana.

## Open-source tools and methodology (Bubblemaps, GraphSense, Neo4j)

### Takeaway
Bubblemaps' exact clustering methodology could not be confirmed; GraphSense is the main open-source (Bitcoin/UTXO-focused, also ETH/account support - unverified) analytics platform; Neo4j is a reasonable store for investigation, not for hot-path clustering.

### Cited Findings
- None retrieved (searches errored).

### Inferences (unverified)
- Bubblemaps: visualizes token holders as bubbles, links wallets via transfers/shared funding; clusters indicate likely common control. Precise rules (thresholds, exchange handling) not confirmed; treat as indicator not proof. Bubblemaps has an API and "Intel Desk"/V2 features (unverified).
- GraphSense (Iknaio, Austrian AIT-backed): open-source crypto analytics with address clustering (multi-input heuristic for UTXO), tagpacks for attribution, REST API; Spark-based transformation pipeline plus Cassandra storage (details unverified).
- Neo4j patterns: nodes (:Wallet), (:Token), relations [:FUNDED {amount, slot}], [:TRADED]; Graph Data Science library offers Louvain, Leiden, WCC (weakly connected components = union-find equivalent), node similarity, FastRP embeddings. Good for ad-hoc/forensic queries; latency/ingest limits make it unsuitable as the per-tx hot path at Solana throughput (unverified claim, plausible).

### Gaps
- Confirm Bubblemaps docs, GraphSense Solana support, current Neo4j GDS algorithm list.

## Practical real-time implementation for a trading bot (incremental clustering, memory/latency)

### Takeaway
Use in-memory union-find over a bounded wallet set plus Redis/embedded KV for edges, trigger cluster lookups per-token on holder snapshots, and run heavier community detection asynchronously. Design numbers below are engineering estimates, not measured.

### Cited Findings
- None retrieved.

### Inferences (unverified engineering estimates)
- Scope the graph: only wallets that touch tokens the bot watches (top holders, early buyers, first N buyers in first slots) plus their funding 1-2 hops up. Avoids whole-chain graph.
- Incremental pipeline: stream (Yellowstone gRPC / Geyser) -> extract edges (SOL transfers above dust threshold, fee payer, token transfers) -> filter by blocklist (CEX, bridges, programs, known routers) -> union-find union with edge log -> emit cluster id + size + supply share.
- Memory: union-find arrays ~ 2 x 8 bytes per wallet plus a 32-byte key map entry; ~10M wallets in roughly 1-2 GB order of magnitude (rough estimate); use TTL/LRU eviction of cold wallets.
- Latency: union/find are sub-microsecond to microseconds in-process; the bottleneck is funding lookup (RPC getSignaturesForAddress for first funder, rate-limited, 100s of ms). Mitigate with cached first-funder table, indexed data providers (Helius/Dune/own indexer), and lazy lookup only for top holders.
- Output features for the bot: cluster supply % of token, number of fresh wallets with same funder, same-slot buy count, cluster-age; use as risk filter (e.g. skip if one cluster holds > X% non-LP supply) - thresholds need backtesting.
- Run Leiden periodically (seconds-minutes) on the per-token holder subgraph for soft clusters; keep hard-link union-find as live path.
- Validate with labeled rug/bundle cases; track precision via manual audit samples since no ground truth.

### Gaps
- No measured latency/memory benchmarks; no verified open-source Solana bundle/cluster detector repo identified; verify RPC/provider limits as of Nov 2026.
