# Solana DEX Infrastructure & Liquidity for Memecoin Trading (as of Nov 2026)

> Research-process caveat for the report writer: in this session, direct page fetches of docs.raydium.io, docs.meteora.ag and dev.jup.ag failed (the hosts are blocked by the session network), GitHub API access to the program repos was not enabled, and the shared web-search budget ran out after 7 searches. Every cited finding below therefore comes from **search-result extracts** of official docs plus a few secondary sites, not from full page reads. Exact constants should be checked against on-chain config accounts or the SDK source before a bot relies on them. Statements marked "derived" are standard AMM math I worked out from the documented invariants. Statements marked "background knowledge" were not verified in this session.

## 1. Pool math, fee tiers and anti-sniper / dynamic-fee mechanisms (Raydium, PumpSwap, Meteora, Orca)

### Takeaway
Most memecoin liquidity on Solana sits in one of three curve families:
- **Constant-product x·y=k pools:** Raydium AMM v4 and CPMM, PumpSwap, Meteora DAMM v1 and DAMM v2 in full range.
- **Concentrated-liquidity tick pools:** Raydium CLMM and Orca Whirlpools.
- **Discrete-bin pools:** Meteora DLMM.

Fees range from about 0.25% (Raydium AMM v4) to more than 1% (new PumpSwap pools, high CPMM tiers). Launch-phase fees can reach 50% or more (Meteora anti-sniper schedulers). For a bot, the decisive per-pool inputs are:
- the curve type;
- the current reserves or liquidity;
- the fee rate at the moment of the trade, which may depend on time, volatility, market cap or trade size.

### Cited Findings

**Raydium**
- AMM v4 charges a single 0.25% fee. One official page says 0.03% of it goes to RAY buybacks, which implies 0.22% to LPs. The AMM v4 reference describes an 88% LP / 12% protocol split ("22/3 of 25"). — [Raydium AMM v4 fees](https://docs.raydium.io/products/amm-v4/fees); [Raydium fee comparison](https://docs.raydium.io/reference/fee-comparison)
- The Raydium protocol-fees page gives a different split: 84% LP, 12% RAY buybacks, 4% treasury. Raydium's own pages conflict on this. — [Raydium Protocol Fees](https://docs.raydium.io/raydium/protocol/the-ray-token/protocol-fees); contradicted by [Raydium fee comparison](https://docs.raydium.io/reference/fee-comparison)
- CPMM fee tiers are also inconsistent across sources:
  - The protocol-fees page lists 4%, 2%, 1% and 0.25%. — [Raydium Protocol Fees](https://docs.raydium.io/ray/protocol-fees)
  - The fee-comparison reference lists 0%, 0.01%, 0.25% and 1%, with the protocol split "configurable per AmmConfig (currently 0%)". — [Raydium fee comparison](https://docs.raydium.io/reference/fee-comparison)
- Fee encoding: AMM v4 stores fees in units of 1/10,000 (25 = 0.25%). CPMM and CLMM store them in units of 1/1,000,000 (2500 = 0.25%). A bot reading on-chain config has to use the right denominator. — [Raydium fee comparison](https://docs.raydium.io/reference/fee-comparison)
- Raydium publishes a separate AMM v4 math page (constant product) and a LaunchLab & CPMM fee reference page. Neither could be fetched in this session. — [Raydium AMM v4 math](https://docs.raydium.io/products/amm-v4/math); [LaunchLab & CPMM fee reference](https://docs.raydium.io/raydium/build/developers-ja/tips-and-gotchas/launchlab-and-cpmm-fee-reference)

**PumpSwap (pump.fun AMM)**
- On 20 March 2025, PumpSwap replaced Raydium as the destination for graduating pump.fun tokens. Older guides that describe Raydium migration are outdated. — [MadeOnSol: graduation explained](https://madeonsol.com/blog/pump-fun-graduation-bonding-curve-explained); [MadeOnSol: What is PumpSwap](https://madeonsol.com/blog/what-is-pumpswap)
- The pump.fun bonding curve starts with about 30 virtual SOL and 1,073,000,000 virtual tokens; price is the ratio of the two reserves. Graduation happens at about 85 SOL deposited on the curve. That is roughly a $69k market cap, or about $60k–80k depending on SOL price. — [sanctifiedops pump-fun-mechanics skill](https://skills.sh/sanctifiedops/solana-skills/pump-fun-mechanics); [Datawallet](https://datawallet.com/crypto/what-is-pump-fun-and-create-a-coin); [Trojan blog](https://trojan.com/blog/how-pump-fun-works)
- Sources disagree on the graduation fee: one says pump.fun takes a 1.5 SOL fee at graduation, another says only 0.015 SOL is deducted for account creation. The 1.5 SOL figure is probably from the older Raydium-migration era (inference). — [MadeOnSol](https://madeonsol.com/learn/graduated-pump-fun); [Seoul Data Labs](https://seouldatalabs.substack.com/p/can-we-rescue-trapped-sol-from-pumpfun)
- Current PumpSwap fees ("Dynamic Fees V1" / "Project Ascend") follow a 25-tier schedule keyed to the coin's market cap in SOL:
  - The total fee is 1.25% right after graduation and falls to a 0.30% floor.
  - The LP fee stays at 0.20% and the protocol fee at 0.05%; the creator fee absorbs the whole decline.
  - The creator fee is about 0.95% below roughly $300k market cap and about 0.05% for large caps.
  - SOL-quoted and USDC-quoted pools use different tier thresholds.
  — [Blofin Academy: Pump.fun fees 2026](https://blofin.com/academy/education/pumpfun/pump-fun-fees-explained); [DEXTools: Project Ascend](https://www.dextools.io/tutorials/what-is-pump-fun-project-ascend-and-the-new-creator-fees); [CryptoSlate](https://cryptoslate.com/pumpfun-launches-initiative-to-become-solanas-hub-for-successful-projects-boosts-creator-earnings-10x/)
- Older fee figures are outdated: 0.25% (0.20% LP + 0.05% protocol) was the original PumpSwap fee, and "1%" was the 2024 bonding-curve fee. Creator revenue sharing on PumpSwap was first introduced in May 2025. Sources date the sliding scale differently (September 2025 vs January 2026). — [The Block](https://www.theblock.co/news/defi/2025-05-13-pumpswap-revenue-tokens-354038); [Shib news](https://news.shib.io/2025/09/04/pump-fun-overhauls-fees-boosting-creator-earnings-over-2m-in-a-day); [Blofin](https://blofin.com/academy/education/pumpfun/pump-fun-fees-explained)
- By April 2026, PumpSwap had passed $16B in volume and was competing with Raydium as a top Solana DEX. — [BlockEden](https://blockeden.xyz/blog/2026/04/12/pumpswap-16b-volume-pumpfun-amm-raydium-solana-dex/); [SolanaFloor](https://solanafloor.com/news/pump-funs-pump-swap-becomes-top-solana-dex-as-project-ascend-redefines-creator-economy)

**Meteora DLMM (Dynamic Liquidity Market Maker)**
- Fees in DLMM:
  - The base fee is set from a base factor, the bin step and a power factor, stored in 1e9 precision.
  - The variable fee is A·(v_a·s)², where A is the variable-fee control, s the bin step and v_a the volatility accumulator. It is rounded up on-chain (add 99,999,999,999, then divide by 1e11), and it is 0 when A = 0.
  - Total fee = base + variable, capped at MAX_FEE_RATE = 100,000,000 (10% in 1e9 precision).
  — [Meteora DLMM fee calculation](https://docs.meteora.ag/overview/products/dlmm/dlmm-fee-calculation); [Meteora DLMM formulas](https://docs.meteora.ag/overview/products/dlmm/dlmm-formulas)
- The volatility accumulator is v_a(k) = v_r + |i_r − (activeID + k)|. Here v_r is the volatility reference, i_r is the index reference and k is the number of bins crossed in the swap; the formulas page adds a ×10,000 scaling and a max cap. The reference updates by elapsed time:
  - If less than the filter period has passed, v_r is kept.
  - Between the filter period and the decay period, v_r = v_a × reductionFactor / 10,000.
  - The extract did not show what happens after the decay period; background knowledge says v_r resets to 0.
  Because of this, fees rise during a burst of trades that cross many bins and decay once trading calms. — [Meteora DLMM formulas](https://docs.meteora.ag/core-products/dlmm/formulas); [Meteora dynamic fees](https://docs.meteora.ag/dlmm/dynamic-fees)
- The protocol share of fees was listed as 5% for standard pools and 20% for launch pools, but that figure appears to come from an early testing phase and may be outdated. — [Meteora dynamic fees (legacy page)](https://docs.meteora.ag/product-overview/dlmm-overview/dynamic-fees)

**Meteora DAMM v2 and the Anti-Sniper Suite**
- DAMM v2 pool creators pick exactly one base-fee mode:
  - **Fee Time Scheduler (linear or exponential):** the fee decays over time. The exponential curve cuts the rate by a percentage each period; the linear curve cuts it by a fixed amount. The default Meteora frontend config is exponential: 50% when trading starts, falling every second for 120 minutes, ending at 0.25%.
  - **Rate Limiter:** the fee starts at a fixed base and rises with trade size, for a set number of slots. Swap instructions on rate-limited pools must include the instructions sysvar account.
  - **Fee Market Cap Scheduler (linear or exponential):** the fee advances one period and drops by the reduction factor each time sqrt-price rises by "Sqrt Price Step Bps". It cannot be combined with the time scheduler or the rate limiter.
  — [Meteora DAMM v2 overview](https://docs.meteora.ag/product-overview/damm-v2-overview); [Fee Time Scheduler](https://docs.meteora.ag/anti-sniper-suite/fee-time-scheduler/what-is-fee-time-scheduler.md); [Fee Market Cap Scheduler](https://docs.meteora.ag/anti-sniper-suite/fee-market-cap-scheduler/what-is-fee-market-cap-scheduler); [Integrate with DAMM v2](https://docs.meteora.ag/developer-guide/trading-terminals/integrate-with-damm-v2.md)
- Meteora's Dynamic Bonding Curve (DBC) docs also have a dynamic-fees section and mention a 99% fee cap, which differs from DLMM's 10% cap. — [Meteora DBC dynamic fees](https://docs.meteora.ag/core-products/dbc/fees/dynamic-fees)

**Orca Whirlpools**
- Orca offers fee tiers from 0.01% to 2%, and each tier is tied to a tick spacing: for example 2% uses spacing 256 and 1% uses 128. Wider spacing suits volatile pairs. One third-party guide counts nine tiers. — [Orca: ticks, tick spacing and fee tiers](https://docs.orca.so/reference/educational-documents/understanding-ticks-tick-spacing-and-fee-tiers-on-orca); [Orca trading fees](https://docs.orca.so/reference/useful-information/trading-fees); [MadeOnSol CL guide](https://madeonsol.com/blog/solana-concentrated-liquidity-guide)
- Orca Adaptive Fee pools raise the fee with volatility, measured by how many tick groups the price crosses during trading. The concept is similar to Meteora DLMM's volatility accumulator. — [Orca Adaptive Fee Pools](https://docs.orca.so/reference/educational-documents/adaptive-fee-pools)

### Inferences
- **(Derived) Constant-product swap math** for Raydium AMM v4 and CPMM, PumpSwap, and DAMM v1 / DAMM v2 in full range. Let input reserve = x, output reserve = y, fee rate = f (taken on input, as on Raydium CPMM and PumpSwap; some pools take it on output), and input amount = Δx.
  - Effective input: Δx' = Δx·(1−f).
  - Output: Δy = y·Δx' / (x + Δx').
  - Spot price (output per input): p₀ = y/x.
  - Average execution price: Δy/Δx = p₀·(1−f)·x/(x+Δx').
  - Price impact excluding fee: I = Δx'/(x+Δx'). Total cost vs spot ≈ 1 − (1−f)(1−I).
  - Input needed for a target impact I: Δx' = x·I/(1−I).
  - After the trade the marginal price moves by (1+Δx'/x)² − 1. A buy of 1% of the reserve moves the marginal price about 2.01% but costs only about 0.99% average impact.
  - "±p% depth" (input that moves the marginal price by p%) = x·(√(1+p) − 1). For 2% that is about 0.995% of the quote reserve, or about 0.5% of pool TVL (TVL ≈ 2x).
- **(Derived) Raydium CLMM and Orca Whirlpools** use Uniswap-v3 math inside the active tick range: L = Δy/Δ√P = Δx/Δ(1/√P), so a quote-token input Δy moves √P by Δy/L. A bot has to walk tick arrays, swapping out L each time an initialized tick is crossed. Liquidity can be thin just outside the current range, so price impact is not a smooth function of TVL.
- **(Derived) Meteora DLMM:**
  - Bin price: P(id) = (1 + binStep/10,000)^id, adjusted for decimals. Background knowledge, consistent with the formulas page.
  - Inside one bin, liquidity is constant-sum (P·x + y = L), so there is zero slippage until the bin empties.
  - Price impact is a step function: the sum over bins crossed of bin-step increments. Fees rise with each bin crossed because v_a increments per bin.
  - Simulating DLMM requires the bin arrays plus the current v_r, i_r and last-update timestamp.
- **(Derived) Anti-sniper schedules distort sniping economics.** A 50% starting fee means a buy in the first seconds of a Meteora DAMM v2 launch loses half its input. A bot must read the pool's base-fee mode and current period, not assume a static fee. On Rate Limiter pools the fee grows with order size, so splitting orders helps.
- **(Derived) The PumpSwap tier fee is a major cost:** 1.25% per side at graduation means about 2.5% round trip before price impact. Bots scalping freshly graduated tokens need moves larger than that.

### Gaps
- The exact current CPMM tier list and AMM v4 split could not be confirmed because Raydium's own pages conflict and could not be fetched. The bot should read the `AmmConfig` accounts on-chain.
- The full 25-tier PumpSwap thresholds (SOL market-cap breakpoints and the per-tier creator fee) were not retrieved. Only the endpoints (1.25% → 0.30%) are sourced.
- Missing exact numbers:
  - DAMM v2 Rate Limiter math and slot counts;
  - DAMM v1 fee structure;
  - DAMM v2 concentrated-range (sqrt-price bounds) math;
  - Orca's full tick-spacing/fee table and adaptive-fee formula;
  - Raydium CLMM fee tiers and LaunchLab parameters.
- Raydium LaunchLab and Meteora DBC graduation thresholds and post-graduation pool types were not researched, for lack of fetch and search capacity.

## 2. Jupiter aggregator routing, Ultra/RFQ, Swap API usage and limitations for bots

### Takeaway
As of March 2026, Jupiter merged Ultra and Metis into **Swap API V2** (`api.jup.ag/swap/v2`). It offers two paths:
- **`/order` + `/execute`:** a managed meta-aggregator. Metis, JupiterZ RFQ, DFlow and OKX compete on price, and Jupiter lands the transaction.
- **`/build`:** raw instructions, Metis-only routing, no Jupiter swap fee, and you land the transaction yourself.

Bots needing composability (custom instructions, Jito bundles, CPI) generally use `/build`. Bots wanting best price plus gasless RFQ use `/order`. Rate limits are now fixed per-tier per organisation.

### Cited Findings
- Swap API V2 is live and consolidates Ultra and Metis. Ultra and Metis remain available, but new integrations should use the Swap API. One page describes the Ultra Swap API as "no longer actively maintained". — [Jupiter changelog March 2026](https://developers.jup.ag/changelog/2026-03); [Jupiter Swap docs](https://developers.jup.ag/docs/swap)
- `/order` returns an assembled transaction at the best price across all routers (Metis, JupiterZ, DFlow, OKX). `/build` uses Metis only. `/build` transactions cannot go through `/execute` and must be landed yourself. `/swap/v1/quote` is deprecated in favour of `/swap/v2/order`. — [Order and execute](https://developers.jup.ag/docs/swap/v2/order-and-execute); [Build API reference](https://developers.jup.ag/docs/api-reference/swap/build.md); [jup-ag agent-skills: integrating-jupiter](https://skills.sh/jup-ag/agent-skills/integrating-jupiter)
- A standalone `POST https://api.jup.ag/tx/v1/submit` sends any signed transaction through Jupiter's landing pipeline with SOL tips. `/swap/v2/execute` and `/tx/v1/submit` each have their own rate-limit bucket. — [Jupiter API reference](https://developers.jup.ag/docs/api-reference); [Jupiter changelog](https://developers.jup.ag/docs/changelog.md)
- Fees:
  - `/build` has no Jupiter swap fee; integrators can add `platformFeeBps` and `feeAccount`.
  - On `/order`, check the `feeBps`, `platformFee.feeBps` and `feeMint` fields in the response.
  - Ultra-era fees were stated as 0–10 bps on most swaps and 50 bps on new tokens. The consumer docs say 0% stable↔stable, 0.1% for most tokens, and 0.5% for tokens under 24 hours old.
  — [Swap V2 fees](https://developers.jup.ag/docs/swap/v2/fees.md); [Ultra vs Metis blog](https://developers.jup.ag/blog/ultra-vs-metis); [Ultra Mode user docs](https://docs.jup.ag/user-docs/trade/spot/ultra-mode)
- One doc says adding `referralAccount`/`referralFee` limits quotes to Metis. The changelog says referral requests can now get RFQ quotes when JupiterZ is the best route. — [Order API reference](https://developers.jup.ag/docs/api-reference/swap/order.md); contradicted by [Jupiter changelog](https://developers.jup.ag/changelog/2026-03)
- JupiterZ (RFQ):
  - The market maker pays network and priority fees, so these swaps are gasless by default.
  - The market maker does not pay token-account rent. If the user lacks the token account and the SOL for rent, JupiterZ is not routed.
  - Setting `payer` ≠ `taker` restricts routing to Metis.
  — [How to build a swap (Jupiter)](https://developers.jup.ag/docs/guides/how-to-build-a-swap-with-ultra); [Ultra vs Metis](https://developers.jup.ag/blog/ultra-vs-metis)
- Rate limits:
  - The old Ultra limit was dynamic: 50 requests per 10-second window, plus extra quota scaled to rolling 24-hour executed volume.
  - Under the new Developer Platform this was replaced by fixed tiers: Free 1 RPS, Pro 150 RPS, paid plans about 100 RPS on `/swap/v2/execute`. Limits apply per organisation, not per API key.
  — [Ultra rate limit](https://developers.jup.ag/docs/ultra/rate-limit); [Jupiter llms.txt / platform docs](https://developers.jup.ag/docs/llms.txt)

### Inferences
- **For a sniping or copy-trading bot:**
  - At 1 RPS, the Free tier is effectively unusable for latency-sensitive memecoin trading; a paid plan or local routing is needed.
  - Brand-new memecoins usually have a single pool (bonding curve or PumpSwap), so aggregation adds little. RFQ market makers rarely quote sub-hour-old tokens (inference; not sourced).
  - Many fast bots therefore build swaps directly against PumpSwap, Raydium or Meteora programs and use Jupiter only for established tokens or multi-hop exits.
- `/order` includes a Jupiter fee that can reach about 50 bps on new tokens (Ultra-era figure), on top of pool fees. `/build` avoids it but loses RFQ and managed landing.
- Background knowledge, unverified here: Jupiter quotes go stale quickly in volatile memecoin pools. Re-quote immediately before signing, and set slippage from simulated depth rather than a fixed %.

### Gaps
- Not retrieved:
  - Jupiter's exact current paid-tier pricing;
  - whether V2 `/order` supports dynamic slippage (Ultra's "RTSE");
  - the full router list beyond Metis, JupiterZ, DFlow and OKX;
  - token-age rules for RFQ eligibility.
- The current Jupiter fee schedule on `/order` for new tokens under V2 could not be confirmed. The 50 bps figure is from Ultra-era docs.

## 3. Price impact vs liquidity depth formulas; typical liquidity levels for memecoins at various market caps

### Takeaway
For constant-product pools:
- price impact ≈ trade size / (quote reserve + trade size);
- 2% depth ≈ 1% of the quote-side reserve.

Liquidity in a graduated pump.fun-style pool is fixed by the burned LP, so the quote reserve grows only with √price. The liquidity-to-market-cap ratio therefore shrinks as a token pumps. I found no sourced dataset of typical memecoin liquidity by market-cap bucket; the figures below are derived from the pump.fun launch parameters.

### Cited Findings
- Price on the pump.fun curve is the ratio of SOL to token reserves, starting from about 30 virtual SOL and 1.073B virtual tokens. Graduation is at about 85 SOL, roughly a $69k market cap. — [sanctifiedops pump-fun-mechanics](https://skills.sh/sanctifiedops/solana-skills/pump-fun-mechanics); [MadeOnSol](https://madeonsol.com/blog/pump-fun-graduation-bonding-curve-explained)
- On graduation, the curve's SOL seeds the new pool and the LP tokens are burned, making that liquidity permanent. — [MadeOnSol: graduated pump.fun](https://madeonsol.com/learn/graduated-pump-fun); [Bitquery: pump.fun to PumpSwap](https://docs.bitquery.io/docs/examples/Solana/pump-fun-to-pump-swap)
- Fewer than 2% of pump.fun tokens ever graduate to a DEX: one day saw 42,000 launches. — [Solana Compass](https://solanacompass.com/news/pumpfun-launched-42000-tokens-in-one-day-fewer-than-2-will-ever-reach-a-dex)

### Inferences
- **(Derived) Curve state at graduation.**
  - k = 30 × 1.073e9 ≈ 3.219e10.
  - At about 85 real SOL, virtual SOL ≈ 115 and virtual tokens ≈ 2.80e8.
  - Price ≈ 4.1e-7 SOL/token, so market cap at 1B supply ≈ 411 SOL. That matches about $69k at a SOL price of about $168.
- **(Derived) Sizing on the bonding curve.**
  - Sizing works like a constant-product pool with the virtual reserves: impact = Δ/(x_virtual + Δ).
  - At launch (x_virtual = 30 SOL), a 1 SOL buy has about 3.2% average impact and moves the price about 6.8%.
  - Near graduation (x_virtual ≈ 115), the same 1 SOL buy has about 0.9% impact.
- **(Derived) Burned-LP pool with no extra LPs** (fee accrual ignored). Let x = quote reserve, M = market cap, and x₀, M₀ their values at graduation.
  - x = x₀·√(M/M₀), so the ratio x/M = (x₀/M₀)·√(M₀/M).
  - Assume about 80–85 SOL lands in the pool at about 411 SOL market cap (background knowledge: about 207M tokens are reserved for the LP).

  | Market cap | SOL-side reserve (approx.) | Reserve as % of market cap |
  |---|---|---|
  | ~$69k (graduation) | ~85 SOL | ~20% |
  | ~10× (~$690k) | ~270 SOL | ~6.5% |
  | ~100× (~$6.9M) | ~850 SOL | ~2% |

  Real pools diverge from this when holders or market makers add liquidity (PumpSwap and Meteora allow anyone to LP) or when liquidity migrates to Meteora DLMM or Raydium CLMM.
- **(Derived) Sell-side depth matters more than buy-side for exits.**
  - Selling tokens worth V SOL into a reserve x returns about V·x/(x+V) before fees. Selling 10% of the reserve's value loses about 9% to impact.
  - For a $1M-cap token in a burned-LP pool (~300 SOL reserve), a 10 SOL exit has about 3.2% impact plus the PumpSwap fee tier.
- **(Derived) Slippage tolerance vs impact.** Impact is the expected price move from your own trade. Slippage tolerance is the extra adverse move you accept from others' trades landing first:
  - minOut = quoteOut × (1 − slippageBps/10,000).
  - On memecoins, sandwich and MEV risk scale with the gap between quote and minOut, so a tight tolerance set from simulated depth limits extractable value. Background knowledge: Jito bundles and private landing reduce exposure.
- **(Derived) Total round-trip cost model for a bot:**
  - cost ≈ 2·f_pool + f_aggregator + I_buy + I_sell + priority/Jito tips + (one-time ATA rent ≈ 0.002 SOL, background knowledge).
  - All terms except tips and rent are computable from pool state.

### Gaps
- No sourced empirical data was retrieved (search budget exhausted) on typical liquidity-to-market-cap ratios for Solana memecoins at $100k, $1M, $10M or $100M+, or on how often liquidity is moved into DLMM or CLMM after graduation. The report should flag the table above as a model, not observed data.
- The exact SOL and token amounts deposited into the PumpSwap pool at graduation under current rules were not confirmed.

## 4. LP burning / locking and why it matters

### Takeaway
On a constant-product pool, whoever holds the LP tokens can withdraw the paired SOL at any moment, which is the classic "rug pull". Burning LP tokens (sending them to an unspendable address) makes the liquidity permanent. Locking makes it time-limited. pump.fun graduations burn LP automatically, which is why graduated pump.fun pools cannot be liquidity-rugged; holder concentration and dev dumping remain risks.

### Cited Findings
- pump.fun graduation sends the new pool's LP tokens to a burn address, making the liquidity permanent. — [MadeOnSol: graduated pump.fun](https://madeonsol.com/learn/graduated-pump-fun); [sanctifiedops pump-fun-mechanics](https://playbooks.com/skills/sanctifiedops/solana-skills/pump-fun-mechanics)
- Burned pump.fun LP has a side effect: SOL in the burned LP is permanently trapped, and there is research on whether it can be recovered. — [Seoul Data Labs: Can we rescue trapped SOL from pump.fun?](https://seouldatalabs.substack.com/p/can-we-rescue-trapped-sol-from-pumpfun)
- DAMM v2 represents LP positions as NFTs, and there is a developer guide for terminals integrating them. — [Meteora DAMM v2 overview](https://docs.meteora.ag/overview/products/damm-v2/what-is-damm-v2.md)
- The NFT, fee-claiming and permanent-lock details were not visible in the retrieved extract.

### Inferences
- Background knowledge, not verified in this session:
  - **Raydium "Burn & Earn"** lets CPMM and CLMM position owners lock or burn a position while keeping the right to claim trading fees through a "fee key" NFT.
  - **Meteora DAMM v1 and v2** support permanent lock with fee claiming.
  - **Orca and Raydium CLMM** positions are NFTs, so "LP burn" checks must inspect the position NFT owner rather than an SPL LP-mint supply.
- **What a bot should check before entry:**
  1. Fraction of LP supply burned, or position NFTs locked or burned, across all pools of the token.
  2. Whether other unlocked pools exist where the deployer holds LP.
  3. Mint authority and freeze authority revoked (background knowledge; standard rug checks).
  4. Token-2022 extensions such as a transfer fee or transfer hook, which change effective output (background knowledge).
- Burned LP protects pool depth but not price. Top holders can still dump into the pool. Use the depth math in Section 3 to bound the damage of a top-holder sell: impact ≈ V/(x+V).

### Gaps
- No quantitative study of Solana rug-pull rates vs LP burn/lock status was retrieved (search budget exhausted).
- Official Raydium Burn & Earn and Meteora lock docs were not fetched, so the mechanics above are background knowledge only.
- Lock-provider landscape (e.g., third-party lockers) and the on-chain verification method for each DEX were not researched.
