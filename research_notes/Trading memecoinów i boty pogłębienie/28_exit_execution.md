# Exit execution in thin memecoin liquidity (as of Nov 2026)

NOTE ON SOURCING: only 1 of ~3 web searches returned results (the rest hit "too_many_requests"); arxiv.org fetch failed (host not in the session's allowed network domains - allow it to verify the papers). Formulas below are my own derivations from standard x*y=k math (marked as inferences), not sourced claims.

## 1. How to compute sell-side price impact on an AMM

### Takeaway
On a constant-product pool, sell impact is closed-form and convex; for thin pools it is large even for small sizes. Impact is path independent for a passive pool, so splitting alone does not improve output.

### Cited Findings
- A Jan 2026 paper (Baude, Challet, Muni Toke) studies optimal liquidation on Uniswap v2/v3 under transient price impact; using a first-order expansion, impact depends on the square root of the spot price and is stochastic. It states AMM execution under transient impact was previously unaddressed in the literature. (Search-result summary only; full text not read.) — [arXiv 2601.03799](https://arxiv.org/html/2601.03799v1)
- A 2023 paper studies optimal trading in constant-product markets (constant liquidity with competing-venue prices; and efficient AMM prices with stochastic liquidity) and compares to TWAP-like and Almgren-Chriss schedules. (Summary only.) — [arXiv 2307.03499](https://arxiv.org/pdf/2307.03499v3)
- Classic Almgren-Chriss uses linear impact in trading rate, temporary impact that doesn't persist; AMMs differ because execution price is set by moving along the pool curve. (Summary only.) — [Wikipedia: Almgren-Chriss](https://en.wikipedia.org/wiki/Almgren%E2%80%93Chriss_model)

### Inferences (derived, verify before use)
- Pool reserves x (token), y (quote, e.g. SOL), fee f, selling Δ tokens: out = y·γΔ/(x+γΔ), γ=1-f. Spot P0=y/x.
- Execution price/P0 = x·γ/(x+γΔ). Price impact (vs spot) = 1 - γx/(x+γΔ) ≈ γΔ/(x+γΔ) + f. Define s=Δ/x: impact ≈ s/(1+s) (fee-less). Selling 5% of token reserves -> ~4.8% avg shortfall; 20% -> ~16.7%; 50% -> 33%.
- Post-trade marginal price = P0·(x/(x+Δ))^2 (fee-less): selling s=10% of reserves leaves spot at ~83% of pre-trade (-17%). This matters for marking PnL and for re-entry/stop logic.
- Realisable exit value is bounded by quote reserve y: you can never extract more than y; for Δ→∞ out→y. Mark positions at out(Δ), not Δ·P0 ("paper PnL" overstates by s/(1+s)).
- Pump.fun-style bonding curves (virtual reserves, also x*y=k-like) use the same formula with virtual reserves; post-graduation PumpSwap/Raydium pools use real reserves. LP concentrated liquidity (v3/CLMM/DLMM) needs tick-by-tick integration.
- Small-trade approximation: impact ≈ Δ/x (linear) -> Almgren-Chriss "permanent" like term, with k = 1/x per token; no separate temporary term in a passive pool, which is why AC mapping is imperfect.

### Gaps
- Exact formulas from the 2026 paper not retrieved.

## 2. Splitting / TWAP / partial take-profit / selling into buy pressure

### Takeaway
Against a passive CPMM with no other flow, splitting yields identical total proceeds; benefits come only from (a) waiting for other participants' buy flow/replenishment (transient impact decay, LP/arb refill), (b) reducing MEV/sandwich per-trade profit, (c) risk-staging. Costs: price risk during the schedule, which in memecoins is brutal.

### Cited Findings
- No reliably sourced practitioner claims retrieved (searches failed). The 2023/2026 arXiv papers above are the starting references for AC-style schedules on CPMMs.

### Inferences
- Path independence: sequential sells with no intervening trades give same output as one sell (x*y=k). Any gain from slicing = value of intervening buys. Slice only if expected inflow between slices (dollar buy volume per interval V_b) is meaningful relative to your size: impact reduction roughly equals what buys re-push reserves.
- AC adapted: minimise E[cost] + λ·Var. With risk-neutral and permanent-only impact, optimal is indifferent; with high volatility σ (memecoins: tens of %/hour) and risk aversion, the solution is front-loaded: x_j ∝ sinh(κ(T-t_j)), κ≈sqrt(λσ²/η). Practical implication: for thin, high-vol memecoins κT is large -> sell most immediately; TWAP is the wrong default except when size is tiny relative to depth AND buy flow is strong.
- Rule of thumb: if s=Δ/x > ~1-2% and expected hold/vol is high, use 1-3 slices over seconds-minutes, not hours. If s<0.5%, single sell.
- Partial take-profits: sell enough to recover cost basis ("de-risk" at 2x) leaves a free runner; mathematically it reduces variance and impact simultaneously since early sells are done at higher price/liquidity. Impact is convex, so selling 50% at once costs more than 2x25% only if reserves recover between; otherwise equal.
- Selling into buy pressure: submit sells on rising-volume/green candles when quote reserves are growing; bigger y raises depth. Avoid selling right after your own sell (reserves skewed, others' sniper/MEV bots detect). Monitor reserve y and net buy flow to set slice size dynamically: slice_t ≤ s_max·x_t with s_max≈1-2%.
- Dump risk is correlated: when you want to exit (dev/whale selling), buy flow disappears, so waiting converts to worse prices; exit liquidity is lowest exactly when needed.

### Gaps
- No sourced empirical data on memecoin TWAP vs immediate sell outcomes; no sourced practitioner guidance.

## 3. Slippage tolerance for sells and failed-sell risk

### Takeaway
Sell slippage must cover expected impact plus price movement during inclusion; too tight -> failed tx and continued exposure in a dump; too wide -> sandwichable. Failed sells during dumps are a core risk.

### Cited Findings
- None sourced (search failed). Unverified general knowledge: on bonding curves a tight slippage setting causes failures when other trades move price before execution; raising slippage/retry helps but worsens fill.

### Inferences
- Set min_out = quote_out(Δ, current reserves)·(1 - tol), tol = expected additional impact from trades likely landing before you (≈ other sell volume in the block / x) + buffer; typical memecoin ranges 5-25%, up to 30-50% in panic exits for tiny pools; tolerance wider than the sandwich profit threshold gives MEV bots the full slippage as profit. Mitigate with private/bundled submission (Jito bundles on Solana, Flashbots Protect on EVM), priority fees, and tip scaling with position value.
- Failed-sell modes: slippage revert; honeypot/transfer-tax/blacklist tokens (simulate a sell before buying); freeze authority or mintable/LP-pull rug (liquidity can go to zero: quote reserve y → 0 so out → 0); congestion and RPC lag; insufficient SOL for fees (keep reserve). Retry with escalating slippage and fees, but cap max loss vs. keeping position.
- Pre-trade checklist: simulate sell, check LP lock/burn, concentration of holders, reserve y vs. position; size position so exit impact at s ≤ ~2-3% of reserves.
- Stop-losses on-chain are not guaranteed: execution = a normal sell that may fail; use hard limit via liquidity-aware sizing instead of relying on stops.

### Gaps
- No sourced figures for failure rates or sandwich frequency on sells; no sourced optimal split vs MEV (no closed form known to me).

## 4. Quant guidance summary
- Cited: Baude-Challet-Muni Toke 2026 and the 2023 CPMM optimal trading paper are the primary academic references; Almgren-Chriss baseline per Wikipedia (links above).
- Recommended follow-up (needs network access to arxiv.org / more searches): extract their optimal schedules; find Solana/EVM practitioner posts on sell slippage and MEV; empirical data on memecoin post-peak liquidity decay.
