# On-chain real-time pricing of memecoins (bonding curve, AMM, CLMM/DLMM, aggregation, quoting, oracles, pitfalls)

STATUS WARNING: web search hit rate limits/quota errors (one query returned only a model-memory answer, the rest failed) and docs.meteora.ag and docs.pyth.network were not reachable (outside session network allowlist). NO claim below is backed by a fetched source. Everything is from background knowledge (cutoff ~mid-2026) and is labelled unverified. Verify against program source / official docs before coding. Hosts to allow if re-run: docs.meteora.ag, docs.pyth.network, docs.raydium.io, github.com raw.

## 1. Bonding-curve price (pump.fun-style) and AMM pool price (constant product, PumpSwap/Raydium AMM v4/CPMM)

### Takeaway
Curve and CP-AMM prices are both reserve ratios; the executable price depends on size via x*y=k plus fees. Constants must be read from on-chain state, not hardcoded.

### Cited Findings
- (Search returned only a non-sourced, model-memory answer; no citable source obtained.)

### Inferences (unverified, from background knowledge)
- Pump.fun curve is constant-product on VIRTUAL reserves: k = vS * vT. Commonly cited initial values: vT ≈ 1,073,000,000 tokens (6 decimals), vS ≈ 30 SOL, real token reserves ≈ 793.1M sellable, ~85 SOL raised at graduation (figures from memory; thresholds/fees have changed over time — read from the BondingCurve account: virtual_token_reserves, virtual_sol_reserves, real_token_reserves, real_sol_reserves, token_total_supply, complete flag).
- Spot price (SOL/token, adjust decimals 10^6 token vs 10^9 lamports): P = vS / vT.
- Market cap = P * total_supply.
- Buy exact SOL in (after fee f on input): dS = in*(1-f); out_tokens = vT - k/(vS+dS) = vT*dS/(vS+dS); capped by real_token_reserves.
- Sell tokens in: out_sol = vS*dT/(vT+dT), then subtract fee. Fee bps differ (protocol + creator fee; PumpSwap-era tiers) — read from Global/fee config accounts.
- Price impact = 1 - (exec price / spot price) = dS/(vS+dS) for buys.
- Constant-product pool (PumpSwap, Raydium AMM v4, CPMM): P = reserveQuote/reserveBase using the vault token balances (NOT cached pool fields in old AMM v4, which also subtracts open-orders/pnl amounts). Output with fee f: out = y*dx*(1-f)/(x + dx*(1-f)). Min-out = out*(1-slippage).
- After graduation the curve account has complete=true; price source must switch to the AMM pool; the curve's last price is stale.
- Token-2022 tokens with transfer fees: received amount < sent; quote must subtract the transfer fee.

### Gaps
- Current (Nov 2026) pump.fun/PumpSwap constants, fee tiers, creator-fee mechanics: not verified.

## 2. CLMM (Raydium CLMM / Orca Whirlpool) and DLMM (Meteora) math

### Takeaway
CLMM: price from sqrtPriceX64 and tick; quote by walking initialized ticks with constant liquidity per range. DLMM: discrete bins with a geometric price ladder and constant-sum (x*P + y = L) inside each bin; quote by walking bins.

### Cited Findings
- (None obtained; searches failed.)

### Inferences (unverified, from background knowledge)
- CLMM: price(tick) = 1.0001^tick; sqrtPrice = 1.0001^(tick/2); stored as Q64.64 (sqrt_price_x64 = sqrtP * 2^64). Spot price token1/token0 = (sqrt_price_x64 / 2^64)^2 * 10^(dec0 - dec1).
- Within a tick range with liquidity L: dx = L*(1/sqrtP_b - 1/sqrtP_a); dy = L*(sqrtP_b - sqrtP_a). Swap token0->token1 with amount in dx (after fee): new sqrtP = L*sqrtP/(L + dx*sqrtP). Swap token1->token0: new sqrtP = sqrtP + dy/L. If next initialized tick is crossed, apply liquidity_net there and continue; tick arrays must be passed as accounts, so the quoter needs to load the right tick arrays (Raydium CLMM, Orca use arrays of fixed tick count; tick_spacing constrains initialized ticks).
- Virtual reserves at current tick: x = L/sqrtP, y = L*sqrtP; thin liquidity around spot is typical for memecoins, so use the tick-walk, not the pool TVL.
- DLMM: bin price = (1 + binStep/10000)^activeId (binStep in bps; activeId signed; adjust for decimals). Inside a bin: P*x + y = L (constant sum), so zero slippage within a bin; swapping drains the bin then moves to the next. Fee = base fee (binStep*baseFactor-based) + variable fee that grows with volatility accumulator (so quoted fee depends on recent swap activity / time since last update; quote should simulate with current clock). Meteora SDK exposes swapQuote that loads bin arrays; needs bin-array accounts.
- Dynamic fees mean the effective fee can spike in volatile memecoin pools; quote must include it.

### Gaps
- Exact on-chain struct layouts, tick-array sizes, DLMM variable-fee formula constants: not verified.

## 3. Multi-pool aggregation and quoting expected output for a size

### Takeaway
Price a token from the deepest/most reliable venue, but quote execution by simulating each pool for the actual size and (optionally) splitting the order across pools to equalize marginal prices.

### Cited Findings
- (None obtained.)

### Inferences (unverified)
- Reference price: liquidity-weighted average of per-pool mid prices, w_i = quote-side reserve (or in-range liquidity for CLMM/DLMM), with outlier rejection (median-based) against pools with tiny TVL that can be manipulated.
- Executable quote for size s: out_i(s) from each pool's formula above; best single pool = argmax out_i(s). Optimal split for CP pools: allocate so marginal prices are equal; for pools with concave out_i(s) a greedy water-filling in small chunks (e.g. 1% steps) works and handles CLMM/DLMM piecewise curves.
- Report both: mid price, effective price = in/out, and impact vs mid. Slippage-min-out = quote*(1-tolerance) with tolerance tied to expected price movement during latency.
- Use Jupiter quote API/Jupiter price API as a cross-check and routing engine; for sniping bots, local reserve decoding via Geyser/gRPC account subscriptions is lower latency than HTTP quotes (from background knowledge, unverified).
- Real-time state: subscribe (Yellowstone gRPC / websocket accountSubscribe) to pool vaults, curve account, tick/bin arrays; apply updates at `processed` commitment for speed, accept reorg risk, confirm at `confirmed`.

### Gaps
- Benchmarks of quote latency vs Jupiter; current Jupiter API versions/limits: not verified.

## 4. SOL/USD conversion via oracles (Pyth, Switchboard)

### Takeaway
USD price = P_token_in_SOL * SOL/USD. Use Pyth (pull model, price + confidence + exponent + publish_time) with staleness and confidence checks; memecoins themselves generally have no oracle, so only SOL/USD (and stable pairs) is oracle-sourced.

### Cited Findings
- (None obtained; docs unreachable.)

### Inferences (unverified)
- Pyth price = price_int * 10^expo; confidence interval conf likewise scaled. USD value = tokenInSOL * (price ± conf). Reject if conf/price > threshold (e.g. 0.5–1%) or now - publish_time > max_age (SDK: getPriceNoOlderThan(maxAgeSeconds)). On Solana Pyth is pull-based: a client must post a recent price update (Hermes API / Pyth receiver program) before use on-chain; off-chain bots can read Hermes streaming (SSE/websocket) or the sponsored push-feed accounts.
- Switchboard on-demand: pull-based feeds with signed oracle quotes; value in the feed result, check staleness (slot/timestamp) and min samples/variance. Specific API names: verify.
- For off-chain bots, SOL/USD moves slowly relative to memecoin volatility; a 1-sec-stale SOL/USD is rarely the dominant error. Fall back: cross-check with the SOL/USDC pool price (e.g. Orca/Raydium deep pool) and halt on divergence.
- USD-denominated limits (PnL) should use the SOL price at entry and exit separately.

### Gaps
- Current Pyth/Switchboard feed IDs, update latencies, fee for posting updates, any Nov 2026 changes: not verified.

## 5. Pitfalls: stale state, MEV between quote and execution

### Takeaway
Quotes are valid only for the slot they were computed; the gap to inclusion allows state change, sandwiching, and competing snipers. Mitigate with min-out, short expiry, private/bundled submission, and priority fee.

### Cited Findings
- (None obtained.)

### Inferences (unverified)
- Stale state: cached pool/curve accounts lag by slots; processed-vs-confirmed differences; a graduated curve; tick/bin arrays not loaded; Token-2022 transfer fee; LP/vault balances including unsettled fees; fake/decoy pools for the same mint (always identify canonical pool by liquidity and by program-derived address).
- MEV: sandwich = attacker buys before and sells after your swap, bounded by your slippage tolerance, so loss ≈ slippage setting when pool is thin. Mitigations: tight min-out computed from fresh quote, Jito bundles / private RPC (tip), avoid public mempool-like paths, lower tolerance where size is large relative to depth, simulate (simulateTransaction) just before send.
- Expected-loss budget: worst case ≈ size * slippage_bps + fees + tip; for memecoin with price volatility σ per second and latency τ, expected adverse drift ~ σ*sqrt(τ).
- Honeypot / freeze authority / transfer-tax checks belong to the quote step: simulate a sell, not only a buy.
- Rug/creator-sell dynamics: liquidity can be removed between quote and fill (non-burned LP on non-pump pools).

### Gaps
- Empirical sandwich rates and Jito landing stats for Nov 2026: not found.
