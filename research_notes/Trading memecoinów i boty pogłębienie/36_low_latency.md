# Low-latency engineering for Solana trading bots (as of Nov 2026)

NOTE ON COVERAGE: Only 3 web searches ran (2 hit rate limits and returned no sources; 1 returned vendor-page titles/snippets). All WebFetch calls failed (alchemy.com, docs.jito.wtf, blockrazor.io not resolvable in this session's network allowlist). Everything not cited below is from background knowledge and marked UNVERIFIED.

## 1. Data ingestion: Yellowstone gRPC vs shred-level feeds

### Takeaway
Shred-level feeds are claimed to beat Yellowstone gRPC by tens of ms, at the cost of client-side decoding and no post-execution metadata. All numbers are vendor claims.

### Cited Findings
- RPC Fast claims Aperture gRPC arrives ~30-40 ms ahead of Yellowstone, and Shredstream gRPC ~50-100 ms ahead; Shredstream requires client-side shred decoding. Vendor claim — [RPC Fast Aperture](https://rpcfast.com/blog/aperture-grpc-explained)
- RPC Fast also claims Yellowstone adds ~30-100 ms replay lag but gives richer post-execution metadata. Vendor claim, same source as above.
- BlockRazor published an Aug 2025 Rust bot benchmark comparing native shred parsing vs Yellowstone gRPC end-to-end (results not seen) — [BlockRazor](https://blockrazor.io/blog/20250826e2etest/)
- Helius markets ShredStream-backed gRPC (no figures seen) — [Helius](https://helius.dev/solana-grpc)
- Chainstack describes Yellowstone as the most widely used Geyser plugin, usually accessed via provider — [Chainstack](https://chainstack.com/learn/compare/best-yellowstone-grpc-providers-solana-2026/)

### Inferences
- Pre-execution (shred) signals suit sniping/copy-trading of new pools; Yellowstone suits logic needing confirmed state/metadata.

### Gaps
- Actual numbers from BlockRazor results; no neutral benchmark found.

## 2. Measuring latency end-to-end

### Takeaway
Public methodology exists (Alchemy) using a Rust client from the geyserbench repo; measure per-region p50/p90/p99.

### Cited Findings
- Alchemy's public Solana gRPC benchmark ran from six regions, reports p50/p90/p99, used a Rust client from geyserbench, window Oct 14-16, 2026, observing a PumpSwap account (numbers not retrieved) — [Alchemy](https://www.alchemy.com/blog/solana-grpc-benchmark-methodology)

### Inferences (UNVERIFIED, general engineering)
- Timestamp at NIC/receive (SO_TIMESTAMPING) and before send; compare to on-chain slot/block time only coarsely; use multiple feeds and "first seen" races to measure feed lead; track tx landing slot delta vs. slot of signal; log send-to-land per sender path.

### Gaps
- No source on end-to-end tooling beyond geyserbench.

## 3. Jito block engine and regions

### Takeaway
Jito uses regional block-engine hostnames; pick the region nearest your sender/leader.

### Cited Findings
- None verified (searches failed).

### Inferences (UNVERIFIED, from background)
- Hostname pattern `<region>.mainnet.block-engine.jito.wtf` with regions incl. Amsterdam, Frankfurt, New York, Tokyo plus a global endpoint; verify against Jito docs. Bundles are atomic, need a tip; landing depends on tip, competitiveness and connection path.

### Gaps
- Current endpoints, rate limits, minimum tip, share of stake running Jito client in Nov 2026.

## 4. Leader schedule awareness and colocation

### Takeaway
Leader schedule is known per epoch; send to current + upcoming leaders; colocate near stake-heavy validators.

### Cited Findings
- None verified.

### Inferences (UNVERIFIED, background)
- Schedule fetched via getLeaderSchedule per epoch (4 consecutive slots per leader, ~400 ms slots); forward to next few leaders' TPU/QUIC ports (or use staked connection / SWQoS) rather than via public RPC. Frankfurt/Amsterdam host many validators; NY and Tokyo are other main hubs; verify with validator geo data (e.g. validators.app) before choosing.

### Gaps
- Current stake distribution by city; measured RTTs between hubs.

## 5. Rust patterns and precomputed transactions

### Takeaway
No sourced material found; the following is general practice, UNVERIFIED.

### Inferences (UNVERIFIED)
- tokio: dedicated runtime/threads pinned to cores for hot path, avoid blocking in async tasks, bounded channels, keep gRPC decode off the sender path.
- Zero-copy: bytemuck `Pod` casts / `from_bytes` over account data (Anchor zero_copy, SPL layouts), manual offset parsing for known discriminators instead of full borsh deserialize; borsh only for cold paths.
- Precompute: pre-build instruction templates, ATAs, compute-budget ixs, keep recent blockhash cached and refreshed per slot, pre-sign nothing that depends on the blockhash beyond a few slots; mutate only amounts/accounts and re-sign; reuse HTTP/2 or QUIC connections warm.

### Gaps
- No benchmarks or primary sources (Solana/Jito docs, Rust perf references) were retrieved.
