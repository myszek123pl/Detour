# Alpenglow and 2026 protocol changes: impact on Solana memecoin trading bots (as of Nov 2026)

Research constraints: ~6 searches used (one hit rate limit: the MEV/Jito query failed), and WebFetch was blocked (solana.com and docs.chainstack.com not resolvable in this session). All facts below come from search-result summaries, not full page reads. Treat as moderately verified. Items marked [UNVERIFIED] are inference or background knowledge.

## What actually changed in 2026 (timeline, slot/confirmation timing)

### Takeaway
Three live changes matter for bots: 100M CU blocks (Jul 29), slot time cut 400ms to 200ms (staged Aug-Oct, final Oct 9), and Alpenglow's Votor (Oct 21; Rotor NOT shipped). Finality dropped from ~12.8s to ~150ms target, while blockhash validity fell from ~60s to ~30s in wall-clock terms.

### Cited Findings
- Alpenglow (Votor) is live on mainnet, activated in epoch 1064 on Oct 21, 2026 (~13:36 UTC); Rotor is still unscheduled — [Solana Foundation upgrade page](https://solana.com/upgrades/alpenglow) (via search summary)
- Chainstack gives the activation slot as 459,653,000 (~18 min after epoch start) — [Chainstack](https://docs.chainstack.com/docs/solana-alpenglow-consensus) (via search summary)
- Finality target ~150ms vs 12.8s under TowerBFT; this is Anza's target for validators receiving votes directly, real-world latency may vary — [Chainstack](https://docs.chainstack.com/docs/solana-alpenglow-consensus)
- Votor: one-round finalization with >=80% stake notarizing; otherwise a second round with 60% thresholds — [Chainstack](https://docs.chainstack.com/docs/solana-alpenglow-consensus)
- Transaction execution unchanged; the Foundation page says the "confirmed" commitment level is slated for removal in a later release — [Solana Foundation](https://solana.com/upgrades/alpenglow)
- Slot time cut from 400ms to 200ms via SIMD-0525 in four feature-gated stages (350/300/250/200ms), each gated on skip rates; 250ms step Sep 18 (epoch 1037), final 200ms step Oct 9, 2026 (epoch 1053); earlier steps Aug 21/28 — [Solana Foundation reduced slot times](https://solana.com/upgrades/reduced-slot-times)
- Ticks/slot, 4-slot leader window, and slots/epoch unchanged, so a leader's 4-slot window is now ~800ms (derived: 4 x 200ms) — [reduced slot times](https://solana.com/upgrades/reduced-slot-times)
- Blockhash expiry still 150 blocks, now ~30s instead of 60s; slot-to-wall-clock conversions must be updated — [reduced slot times](https://solana.com/upgrades/reduced-slot-times)
- 100M CU block limit (SIMD-0286, authored by Jito Labs) active Jul 29, 2026 at epoch 1009; up from 60M (+66%); per-account writable limit unchanged at 12M CU — [Solana Foundation 100M CU](https://solana.com/upgrades/100m-cu-blocks)
- Foundation credits XDP networking (default in Firedancer, in Agave 4.0.0+; >70% of stake had it enabled) for making 100M safe — [100M CU page](https://solana.com/upgrades/100m-cu-blocks)

### Inferences
- Total throughput headroom roughly doubles in per-second terms (100M CU per 200ms vs 60M per 400ms) IF per-slot limit stayed at 100M and was not scaled; [UNVERIFIED] whether the block CU limit was rescaled with the slot cut.
- Hot-account (12M CU writable cap) contention is unchanged per block, so contested memecoin pool/bonding-curve accounts remain the bottleneck even with more total capacity; cap per second is higher only because blocks are twice as frequent.
- Retry/resend loops tuned to 400ms slots and 60s blockhash TTL are now mis-calibrated; "finalized" is now cheap enough to use as the commitment for post-trade state.

### Gaps
- Exact semantics of "confirmed" removal (timeline, whether RPC still serves it) not verified.
- Whether `processed` still has meaning/latency differences under Votor not found.
- Reported dates conflict slightly (older Foundation pages describe slot cut as future, tied to Agave v4.2, breaking; later page says live and non-breaking). Use the Oct 9 final date with caution; tracker at solana.com/200ms.

## Leader schedule, propagation, skip rates, failed transactions

### Takeaway
Leader window length (4 slots) is unchanged in slot count, so each leader now holds ~0.8s; Rotor (the propagation replacement) is not live, so Turbine behavior persists. I found no sourced data on failed-tx rates post-change.

### Cited Findings
- Each reduction stage was gated on block skip rates; the network would not advance if skips were too high — [reduced slot times](https://solana.com/upgrades/reduced-slot-times)
- Rotor deferred to a future, separate proposal that does not yet exist per Chainstack; Foundation says unscheduled — [Chainstack](https://docs.chainstack.com/docs/solana-alpenglow-consensus)

### Inferences
- [UNVERIFIED] Shorter slots shrink the time to forward a tx to the next leader; tx sent to a leader late in its window have less time to land, so resend cadence should shorten and target current + next leader TPU/QUIC.
- [UNVERIFIED] Blockhash expiry in 30s plus 150-block validity means "blockhash expired" failures rise for bots using stale cached blockhashes; refresh by block height not time.
- [UNVERIFIED] Faster finality reduces the window in which a "confirmed" fork reverts, so fork-related phantom fills should drop.

### Gaps
- No data found on post-Oct-2026 failed-tx rate, skip rate, or landing-rate changes.
- Whether Alpenglow changes vote transactions occupying block space (previously large share of CU) and thereby the CU available to users; not verified.

## Firedancer adoption

### Takeaway
Firedancer/Frankendancer stake share is rising but sources disagree; treat as roughly 14% full Firedancer-family and a larger hybrid share by mid-2026, with data quality poor.

### Cited Findings
- Jan 31, 2026 (Syndica): Agave Jito 41%, JitoBAM 24%, Frankendancer Jito 17%, Harmonic 13%, Rakurai 2%, Firedancer Jito 1% — [Syndica Jan 2026](https://blog.syndica.io/deep-dive-solana-onchain-activity-january-2026)
- May 2026: Firedancer founding engineer put stake at ~7% (via Gate write-up citing CoinDesk) — [Gate](https://www.gate.com/en-eu/blog/58/jump-crypto-solana-validator-architecture-firedancer-performance-stability-public-blockchain-boundaries-redefined)
- July 2026: RPCFast estimates ~14% on Firedancer plus ~26% on Frankendancer; SOL Strategies cites ~14% combined with full Firedancer ~2.5% — they conflict on the split — [RPCFast](https://rpcfast.com/blog/what-is-firedancer-solana-validator-client); [SOL Strategies](https://solstrategies.io/blog/firedancer-what-sol-strategies-is-building)
- Conflicting timeline on full Firedancer mainnet release (Dec 2025 vs. "in testing" April 2026) — [Blockdaemon](https://www.blockdaemon.com/blog/what-is-firedancers-status-and-what-does-it-mean-for-solana); [datawallet](https://www.datawallet.com/es/crypto/firedancer-solana)
- Authoritative dashboard cited: reports.firedancer.io (not accessed)

### Inferences
- Client diversity means varying leader behavior (packing, QUIC handling, tx scheduling); bots should measure landing rates per leader client instead of assuming uniformity.

### Gaps
- Current (Nov 2026) stake share not found.
- Per-client differences in bundle/tip handling not found.

## MEV (Jito) and priority-fee behavior; RPC behavior

### Takeaway
The MEV/Jito search failed (rate limit), so no sourced claims on post-Alpenglow MEV. Notable only: SIMD-0286 was authored by Jito Labs, and JitoBAM/Harmonic hold significant stake (Jan 2026).

### Cited Findings
- JitoBAM 24% and Harmonic 13% stake as of Jan 31, 2026 — [Syndica](https://blog.syndica.io/deep-dive-solana-onchain-activity-january-2026)

### Inferences
- [UNVERIFIED] With 200ms slots and ~0.8s leader windows, bundle auction timing windows are shorter; tips needed to win a contested slot are likely higher per unit time but not measured.
- [UNVERIFIED] RPC: expect many more blocks/sec (indexers see 2x), subscriptions (slotSubscribe/logsSubscribe) at ~5 events/s; providers may throttle; commitment `finalized` subscriptions become usable for low-latency flows; `confirmed` clients should plan migration.

### Gaps
- Jito bundle/BAM changes under Alpenglow, tip-market data, RPC provider behavior changes: not found.

## What a bot must change (checklist; mostly inference from the cited findings)

1. Slot/time math: 200ms slots, blockhash TTL ~30s (150 blocks). Stop converting slots to seconds with 0.4. Track block height, not wall-clock.
2. Commitment: use `finalized` (~150ms target) for confirming fills and position state; plan for `confirmed` removal; verify latency empirically.
3. Resend/retry: shorter intervals tied to the 0.8s leader window; target current and next leaders; fresh blockhash per attempt.
4. Hot-account contention: 12M CU per-account cap unchanged, so set realistic CU limits and compute-unit price; do not assume 100M CU eliminates failures on popular memecoin pools.
5. Per-leader/client telemetry: measure landing rate by validator client (Agave, Frankendancer, Firedancer, Jito variants).
6. RPC: tune subscription handlers for 2x block rate; use providers confirmed to support the new commitment behavior.
7. Monitor Rotor rollout (unscheduled) and the confirmed-removal release as future breaking points.
