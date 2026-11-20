# Swap execution routes for a Solana memecoin bot (as of Nov 2026)

Research limit note: only 2 of ~6 planned searches returned results (search tool rate-limited on the rest). Anything not cited is UNVERIFIED and listed under Inferences or Gaps.

## Jupiter Swap/Ultra API: fees, latency, rate limits

### Takeaway
Ultra charges a small protocol fee (5-10 bps per newer docs), rate limits are now fixed per-account tiers (Free 1 RPS up to Pro 150 RPS), and latency is a "95% under 2s" marketing claim rather than an SLA. Jupiter docs conflict across versions, so re-check the live Developer Platform pages.

### Cited Findings
- Newer Ultra Swap docs: Jupiter takes 5 to 10 bps of the swap amount; integrators can add own fees and keep 80% — [Ultra API docs](https://developers.jup.ag/docs/ultra/get-started); older page cited 0.1% (or 0.05% depending on tokens) — [hub.jup.ag](https://hub.jup.ag/docs/ultra-api) (conflict between versions)
- Fixed rate-limit tiers: Free 1 RPS, Developer 10 RPS, Launch 50 RPS, Pro 150 RPS; 60-second sliding window; limits per account not per API key — [Rate limits](https://developers.jup.ag/docs/portal/rate-limits)
- Older model (superseded): dynamic limits, 50 base requests per 10s window scaling with executed swap volume; other old pages cite 60 or 120 req/min — [old rate limit page](https://hub.jup.ag/docs/api-rate-limit)
- Latency: "95% of swaps executed under 2 seconds" (older Quick Launch page, marketing claim) — [Quick Launch](https://dev.jup.ag/docs/ultra); plan tier does not change latency, all plans use api.jup.ag; latency depends on proximity to Jupiter's gateway regions — [Developer Platform plans](https://developers.jup.ag/docs/portal/plans.md)

### Inferences
- A 1 RPS free tier is too low for a multi-token bot; a paid tier is likely needed for sniping/many positions.
- Ultra is managed execution (Jupiter handles landing), so it trades control (priority fee/tip tuning, own Jito bundles) for simplicity; "under 2s" is likely too slow for first-block sniping but fine for exits/DCA-style trading.

### Gaps
- Whether Ultra routes pump.fun bonding-curve tokens pre-migration was not verified. Swap-API (non-Ultra, /quote + /swap) fee: not verified (commonly no protocol fee, unverified). Paid-tier prices not retrieved.

## Direct program/SDK swaps (pump.fun, PumpSwap, Raydium, Meteora)

### Takeaway
Direct instruction building gives the lowest latency and no third-party fee, at the cost of maintenance. No source found in this session; all content is UNVERIFIED.

### Cited Findings
- None retrieved (search rate-limited). PumpPortal docs mention the pump.fun bonding-curve fee is separate from PumpPortal's fee and from Solana network fees — [PumpPortal mirror](https://github.com/pumpdev3/pumpdev.io) (third-party mirror).

### Inferences
- UNVERIFIED from training knowledge: PumpSwap is pump.fun's AMM that graduated tokens migrate to (replacing Raydium path in 2025); it has creator fees; an official pump-swap SDK exists (exact npm name unverified). Direct route requires tracking account layouts, creator-fee vault accounts and program upgrades; bonding-curve/PumpSwap layouts have changed before.
- Direct building lets you bundle your own priority fee + Jito tip and use own RPC/Yellowstone gRPC for lowest latency; cost is only network/priority/tip + the pool/curve fee.

### Gaps
- Current program IDs, fee schedule (bonding curve 1%? PumpSwap LP/protocol/creator split), SDK package names, Raydium/Meteora (DLMM, DBC) SDK status: all unverified.

## Third-party swap APIs (PumpPortal, Solana Tracker, Moralis)

### Takeaway
PumpPortal is the cheapest-to-integrate pump.fun route but charges a percentage (Lightning ~1%, Local ~0.5% per a third-party write-up of its Oct 2026 fees page; unconfirmed on the official site). Solana Tracker and Moralis were not researched successfully.

### Cited Findings
- PumpPortal Lightning API: hosted wallet signs and sends; fee reported as 1% per trade (calculated before slippage); some write-ups still say 0.5% — [PumpPortal on Solana Compass](https://solanacompass.com/projects/pumpportal), [Quicknode listing](https://www.quicknode.com/builders-guide/tools/pumpportal-by-pumpportal-team) (not directly confirmed on pumpportal.fun)
- PumpPortal Local API: returns unsigned tx you sign with own key; fee 0.5% per trade; excludes network and bonding-curve fees — [PumpPortal mirror](https://github.com/pumpdev3/pumpdev.io)
- Data streams: new-token and migration streams free; token/account trade streams 0.01 SOL per 10,000 trades — same search results (unconfirmed)

### Inferences
- At 0.5-1% per side, a round trip costs 1-2% vs ~0.05-0.1% for Jupiter Ultra: a large drag on small-edge memecoin strategies; Lightning also means custodial-like key exposure to a third party.

### Gaps
- Solana Tracker swap API (fees, limits) and Moralis swap/trading offerings: no data retrieved. PumpPortal latency/rate limits: not found. Direct confirmation of PumpPortal fees from official site: not obtained.

## Tradeoffs summary (mostly inference)

### Takeaway
Fastest/cheapest: direct programs + own RPC/landing (highest dev effort). Easiest broad coverage: Jupiter Ultra (5-10 bps, ~2s claim). Easiest pump.fun-specific: PumpPortal Local (0.5%).

### Cited Findings
- See sections above.

### Inferences
- Hybrid is sensible: direct pump.fun/PumpSwap builders for entries on fresh tokens, Jupiter for exits/migrated tokens and fallback routing.

### Gaps
- No measured latency benchmarks, landing-rate data, or reliability/uptime figures found for any route.
