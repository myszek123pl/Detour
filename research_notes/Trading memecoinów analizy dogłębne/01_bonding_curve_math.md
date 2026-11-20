# pump.fun bonding curve mathematics (parameters, price/mcap, impact, round-trip cost, break-even)

Compiled 2026-11-20. Calculations: `/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/curve.py` (raw output in `curve_out.md` next to it). Only raw.githubusercontent.com was reachable (pump.fun, coinpaprika etc. failed DNS), so fee tiers come from the official GitHub docs image and one search summary. Items marked **[UNVERIFIED]** could not be confirmed from a primary source as of Nov 2026.

## 1. What are the current bonding-curve parameters (reserves, graduation threshold, fees)?

### Takeaway
Constant-product curve k = vSOL x vTOKEN, starting at 30 SOL / 1,073,000,000 tokens virtual (793.1M real tokens sellable, 1B supply), completing when real tokens hit 0, which implies ~85.0 SOL real raised, ~115 SOL virtual, and ~411 SOL (about 14.7x start price) market cap at completion. Fee on the curve is 1.25% per trade (0.95% protocol + 0.30% creator) per the official fee-tier table, though the newest IDL adds buyback/quote-paired/mayhem variants whose exact current rates I could not verify.

### Cited Findings
- Global account example: initial_virtual_token_reserves = 1073000000000000 (1,073,000,000 tokens, 6 decimals), initial_virtual_sol_reserves = 30000000000 lamports (30 SOL), initial_real_token_reserves = 793100000000000 (793.1M), token_total_supply = 1000000000000000 (1B), fee_basis_points = 100, pool_migration_fee = 15000001 lamports — [Pump program README](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/docs/PUMP_PROGRAM_README.md)
- Bonding curve account starts with real_sol_reserves = 0 and sets `complete = true` at the end of a buy when real_token_reserves == 0; buys add the same lamports to virtual and real SOL, subtract the same tokens from virtual and real tokens — [Pump program README](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/docs/PUMP_PROGRAM_README.md)
- `migrate` is permissionless and moves a completed curve (complete == true, real_token_reserves == 0) to PumpSwap AMM; pool_migration_fee is the minimum lamports for the accounts created, below MAX_MIGRATE_FEES = 15_000_000 — [Pump program README](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/docs/PUMP_PROGRAM_README.md)
- Program ID 6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P; fee program pfeeUxB6jkeY1Hxd7CsFCAjcbHA9rWtchMGdZ6VojVZ; PumpSwap pAMMBay6oceH9fJKBRHGP5D4bD4sWpmSwMn52FMfXEA — [pump.json IDL](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/idl/pump.json)
- Official fee-tier sheet (image): Bonding curve = creator 0.300% + protocol 0.95% + LP 0% = 1.25% total; PumpSwap canonical pools are tiered by market cap from 1.25% (0-420 SOL) down to 0.30% (98,240+ SOL). Market cap for fee purposes = virtualSol * supply / virtualToken — [Fee program README](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/docs/FEE_PROGRAM_README.md), [fees.png](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/docs/fees.png) (image read manually)
- Fee logic: if a FeeConfig exists, bonding-curve protocol/creator fee bps come from market-cap tiers (calculateFeeTier); otherwise Global.fee_basis_points + creator_fee_basis_points. The sheet shows a single flat 1.25% row for the curve — [Fee program README](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/docs/FEE_PROGRAM_README.md)
- Current IDL Global struct has extra fields: buyback_fee_recipients (8), buyback_basis_points (<=10,000), initial_virtual_quote_reserves, whitelisted_quote_mints, max_configurable_creator_fee_bps, max_curve_depth, mayhem and cashback flags; BondingCurve has virtual_quote_reserves, quote_mint, depth etc. — [pump.json IDL](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/idl/pump.json)
- Newer v3 trades keep protocol and creator fees on the curve until swept; a buy that crosses the completion limit ("synthetic migration") fills the remainder at PumpSwap-pool pricing, then the curve completes — [Synthetic migration](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/docs/SYNTHETIC_MIGRATION.md), [README](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/README.md)
- Search summary: sources agree on ~30 SOL / ~1.073B virtual start and ~85 SOL graduation, but disagree on whether 85 SOL is real SOL raised or virtual reserve; 1.25% fee not confirmed in that search — [search results via Mobula/Bybit/Madeonsol listing, unfetched]; derived math below resolves it (85.0 real = 115 virtual)

### Inferences
- Derived from the constants: k = 3.219e10; completion state vToken = 1,073M - 793.1M = 279.9M, vSOL = k/279.9M = 115.005 SOL, real SOL raised = 85.005 SOL (matches the folklore "85 SOL"); start mcap = 27.96 SOL, completion mcap = 410.9 SOL; price multiple start to completion = 14.70x. Fixed regardless of SOL/USD.
- USD mcap at graduation = 410.9 x SOL price (e.g. ~$61.6k at $150/SOL, ~$82k at $200/SOL); the popular "$69k" figure corresponds to a SOL price of ~$168.
- Fee drag on the curve is flat 1.25% per side, so it is the same at every progress level.

### Gaps
- Live on-chain Global/FeeConfig values as of Nov 2026 not read (no RPC access); README Global values are the documented example. **[UNVERIFIED: unchanged in Nov 2026]**
- How buyback_basis_points / buyback_fee changes the fee (carved out of protocol fee vs additional) not documented in files I read. **[UNVERIFIED]** Model assumes total 1.25%.
- Fee sheet image dates from the Sept 2025 dynamic-fee change; later revamps (creator fee sharing, holder-reward coins, mayhem mode, cashback deprecation) may alter the creator share. **[UNVERIFIED]**
- Whether the fee schedule per curve market-cap tier in FeeConfig differs from the flat sheet row: not readable without RPC.
- Graduation (migration) fee to user: pool_migration_fee ~0.015 SOL is a program cost, not charged per trade; any pump.fun-side graduation reward/fee not verified.

## 2. How do price and market cap evolve with curve progress?

### Takeaway
Price rises convexly: 2.5x at 50% tokens sold (only 17.6 SOL raised), 5x at 75%, 14.7x at 100%. "Progress" in the UI is token-based; by SOL raised the curve is only ~21% full when 50% of tokens are sold.

### Cited Findings
- Model and formulas: price = vSOL/vTOKEN, mcap = vSOL x 1B / vTOKEN (same market-cap definition used by the fee program) — [Fee program README](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/docs/FEE_PROGRAM_README.md)

### Inferences
Progress p = tokens sold / 793.1M (token-based; assumed to match the UI definition **[UNVERIFIED]**).

| Progress % | Real SOL raised | Tokens sold (M) | Price (SOL/token) | Price x vs start | Mcap (SOL) | Mcap @ $150/SOL | Mcap @ $200/SOL |
|---|---|---|---|---|---|---|---|
| 0 | 0.00 | 0.0 | 2.796e-08 | 1.00 | 28.0 | $4,194 | $5,592 |
| 5 | 1.15 | 39.7 | 3.015e-08 | 1.08 | 30.1 | $4,522 | $6,029 |
| 10 | 2.39 | 79.3 | 3.260e-08 | 1.17 | 32.6 | $4,890 | $6,520 |
| 15 | 3.74 | 119.0 | 3.537e-08 | 1.26 | 35.4 | $5,305 | $7,073 |
| 20 | 5.20 | 158.6 | 3.850e-08 | 1.38 | 38.5 | $5,775 | $7,700 |
| 25 | 6.80 | 198.3 | 4.207e-08 | 1.50 | 42.1 | $6,311 | $8,414 |
| 30 | 8.55 | 237.9 | 4.616e-08 | 1.65 | 46.2 | $6,924 | $9,232 |
| 35 | 10.47 | 277.6 | 5.088e-08 | 1.82 | 50.9 | $7,632 | $10,176 |
| 40 | 12.59 | 317.2 | 5.636e-08 | 2.02 | 56.4 | $8,454 | $11,272 |
| 45 | 14.95 | 356.9 | 6.277e-08 | 2.25 | 62.8 | $9,416 | $12,554 |
| 50 | 17.59 | 396.6 | 7.035e-08 | 2.52 | 70.3 | $10,552 | $14,070 |
| 55 | 20.55 | 436.2 | 7.938e-08 | 2.84 | 79.4 | $11,907 | $15,876 |
| 60 | 23.91 | 475.9 | 9.028e-08 | 3.23 | 90.3 | $13,541 | $18,055 |
| 65 | 27.74 | 515.5 | 1.036e-07 | 3.70 | 103.6 | $15,536 | $20,715 |
| 70 | 32.16 | 555.2 | 1.200e-07 | 4.29 | 120.0 | $18,007 | $24,009 |
| 75 | 37.32 | 594.8 | 1.408e-07 | 5.04 | 140.8 | $21,117 | $28,156 |
| 80 | 43.41 | 634.5 | 1.674e-07 | 5.99 | 167.4 | $25,109 | $33,479 |
| 85 | 50.70 | 674.1 | 2.023e-07 | 7.24 | 202.3 | $30,350 | $40,467 |
| 90 | 59.61 | 713.8 | 2.495e-07 | 8.92 | 249.5 | $37,421 | $49,895 |
| 95 | 70.73 | 753.4 | 3.152e-07 | 11.27 | 315.2 | $47,285 | $63,046 |
| 100 | 85.01 | 793.1 | 4.109e-07 | 14.70 | 410.9 | $61,632 | $82,176 |


SOL-based vs token-based progress (50% of tokens sold = ~17.6 SOL = 20.7% of the 85 SOL):

| Real SOL raised | % of 85 SOL | % tokens sold |
|---|---|---|
| 1 | 1.2 | 4.4 |
| 5 | 5.9 | 19.3 |
| 10 | 11.8 | 33.8 |
| 20 | 23.5 | 54.1 |
| 30 | 35.3 | 67.6 |
| 40 | 47.1 | 77.3 |
| 50 | 58.8 | 84.6 |
| 60 | 70.6 | 90.2 |
| 70 | 82.4 | 94.7 |
| 80 | 94.1 | 98.4 |
| 85 | 100.0 | 100.0 |


- Early buyers get most of the multiple: entering at 0% vs 50% progress means 2.5x less upside available to graduation (14.7x vs 5.8x remaining).
- Mcap in SOL is the stable unit; USD columns assume $150 / $200 per SOL (illustrative, not current prices).

### Gaps
- Exact UI definition of "progress %" **[UNVERIFIED]**.

## 3. What is the price impact of 0.1-10 SOL buys and sells at various progress levels?

### Takeaway
Impact scales with trade size relative to virtual SOL: 1 SOL costs ~4.6% (incl. 1.25% fee) at 0% progress but ~2.2% at 95%; 10 SOL costs ~34.6% at 0% and ~11% at 95%. Sells are near-symmetric (curve is reversible; selling n tokens returns slightly less than buying them cost).

### Cited Findings
- Constant-product swap and fee mechanics: fees deducted from spendable SOL on buy_exact_sol_in (`total_fee_bps = protocol_fee_bps + creator_fee_bps`) — [pump.json IDL](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/idl/pump.json)

### Inferences
Model: buy of S SOL: curve gets S/(1.0125) (fee on top); sell: gross proceeds x (1-0.0125). "Impact" = effective average price vs pre-trade spot.

**Buy impact incl. fee (impact% / tokens received):**

| Buy SOL \ Progress | 0% | 10% | 25% | 50% | 75% | 90% | 95% |
|---|---|---|---|---|---|---|---|
| 0.1 | 1.58% / 3.52M | 1.56% / 3.02M | 1.52% / 2.34M | 1.46% / 1.40M | 1.40% / 0.70M | 1.36% / 0.40M | 1.35% / 0.31M |
| 0.25 | 2.08% / 8.76M | 2.02% / 7.52M | 1.93% / 5.83M | 1.78% / 3.49M | 1.62% / 1.75M | 1.53% / 0.99M | 1.50% / 0.78M |
| 0.5 | 2.92% / 17.38M | 2.79% / 14.92M | 2.61% / 11.58M | 2.30% / 6.95M | 1.99% / 3.48M | 1.81% / 1.97M | 1.75% / 1.56M |
| 1 | 4.58% / 34.20M | 4.34% / 29.40M | 3.97% / 22.86M | 3.35% / 13.75M | 2.74% / 6.91M | 2.37% / 3.92M | 2.24% / 3.10M |
| 2 | 7.92% / 66.29M | 7.42% / 57.11M | 6.68% / 44.56M | 5.45% / 26.96M | 4.22% / 13.63M | 3.48% / 7.75M | 3.24% / 6.15M |
| 5 | 17.92% / 151.66M | 16.68% / 131.44M | 14.84% / 103.49M | 11.76% / 63.60M | 8.68% / 32.68M | 6.83% / 18.76M | 6.21% / 14.93M |
| 10 | 34.58% / 265.76M | 32.12% / 232.17M | 28.42% / 185.09M | 22.26% / 116.27M | 16.10% / 61.18M | 12.41% / 35.66M | 11.18% / 28.53M |


**Buy impact, pure curve slippage (excl. fee):**

| Buy SOL \ Progress | 0% | 10% | 25% | 50% | 75% | 90% | 95% |
|---|---|---|---|---|---|---|---|
| 0.1 | 0.33% | 0.31% | 0.27% | 0.21% | 0.15% | 0.11% | 0.10% |
| 0.25 | 0.83% | 0.77% | 0.68% | 0.53% | 0.37% | 0.28% | 0.25% |
| 0.5 | 1.67% | 1.54% | 1.36% | 1.05% | 0.74% | 0.56% | 0.50% |
| 1 | 3.33% | 3.09% | 2.72% | 2.10% | 1.49% | 1.12% | 0.99% |
| 2 | 6.67% | 6.17% | 5.43% | 4.20% | 2.97% | 2.23% | 1.99% |
| 5 | 16.67% | 15.43% | 13.59% | 10.51% | 7.43% | 5.58% | 4.96% |
| 10 | 33.33% | 30.87% | 27.17% | 21.01% | 14.85% | 11.16% | 9.93% |


**Sell impact incl. fee** (rows = SOL value of tokens at spot, columns = progress; cell = shortfall vs spot / SOL received):

| Sell (SOL-equiv of tokens at spot) \ Progress | 0% | 10% | 25% | 50% | 75% | 90% | 95% |
|---|---|---|---|---|---|---|---|
| 0.1 | 1.58% / 0.098 | 1.55% / 0.098 | 1.52% / 0.098 | 1.46% / 0.099 | 1.40% / 0.099 | 1.36% / 0.099 | 1.35% / 0.099 |
| 0.25 | 2.07% / 0.245 | 2.01% / 0.245 | 1.92% / 0.245 | 1.77% / 0.246 | 1.62% / 0.246 | 1.52% / 0.246 | 1.49% / 0.246 |
| 0.5 | 2.87% / 0.486 | 2.75% / 0.486 | 2.57% / 0.487 | 2.28% / 0.489 | 1.98% / 0.490 | 1.80% / 0.491 | 1.74% / 0.491 |
| 1 | 4.44% / 0.956 | 4.21% / 0.958 | 3.86% / 0.961 | 3.28% / 0.967 | 2.70% / 0.973 | 2.34% / 0.977 | 2.22% / 0.978 |
| 2 | 7.42% / 1.852 | 6.99% / 1.860 | 6.34% / 1.873 | 5.23% / 1.895 | 4.10% / 1.918 | 3.41% / 1.932 | 3.17% / 1.937 |
| 5 | 15.36% / 4.232 | 14.45% / 4.277 | 13.06% / 4.347 | 10.64% / 4.468 | 8.08% / 4.596 | 6.47% / 4.677 | 5.92% / 4.704 |
| 10 | 25.94% / 7.406 | 24.54% / 7.546 | 22.35% / 7.765 | 18.40% / 8.160 | 14.02% / 8.598 | 11.16% / 8.884 | 10.17% / 8.983 |


- Practical rule: curve slippage ~ S / (2 x vSOL) approx; vSOL ranges 30 SOL (start) to 115 SOL (end), so late-stage curves absorb 10 SOL at ~10% impact while fresh curves suffer ~33%.
- Buys that would exceed the remaining curve (e.g. 10 SOL when <10 SOL remains near 95-100%) are capped; with v3 instructions the excess goes to the synthetic-migration pool part.

### Gaps
- Whitelisted-quote / depth>0 / mayhem curves use different initial reserves and are not modelled.
- Priority fees, Jito tips and ATA rent not modelled in impact tables.

## 4. What is the round-trip cost including fees, and what multiple is needed to break even?

### Takeaway
An immediate buy-then-sell on the curve loses a constant 2.47% regardless of size or progress (price impact cancels because the curve is reversible; only the two 1.25% fees bite). Break-even needs only ~+2.5-2.9% spot price rise after your buy (about +9.4% to +4.8% mcap from pre-buy level for 1 SOL, because your own buy moves price), not 2x; the real hurdle is liquidity/adverse selection, not curve math.

### Cited Findings
- Fee 1.25% per trade on the bonding curve — [Fee program README](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/docs/FEE_PROGRAM_README.md) (see Q1 caveats)

### Inferences
**Immediate round-trip (buy S, immediately sell all tokens):**

| Buy SOL \ Progress | 0% | 10% | 25% | 50% | 75% | 90% | 95% |
|---|---|---|---|---|---|---|---|
| 0.1 | -2.47% (0.0975) | -2.47% (0.0975) | -2.47% (0.0975) | -2.47% (0.0975) | -2.47% (0.0975) | -2.47% (0.0975) | -2.47% (0.0975) |
| 0.25 | -2.47% (0.2438) | -2.47% (0.2438) | -2.47% (0.2438) | -2.47% (0.2438) | -2.47% (0.2438) | -2.47% (0.2438) | -2.47% (0.2438) |
| 0.5 | -2.47% (0.4877) | -2.47% (0.4877) | -2.47% (0.4877) | -2.47% (0.4877) | -2.47% (0.4877) | -2.47% (0.4877) | -2.47% (0.4877) |
| 1 | -2.47% (0.9753) | -2.47% (0.9753) | -2.47% (0.9753) | -2.47% (0.9753) | -2.47% (0.9753) | -2.47% (0.9753) | -2.47% (0.9753) |
| 2 | -2.47% (1.9506) | -2.47% (1.9506) | -2.47% (1.9506) | -2.47% (1.9506) | -2.47% (1.9506) | -2.47% (1.9506) | -2.47% (1.9506) |
| 5 | -2.47% (4.8765) | -2.47% (4.8765) | -2.47% (4.8765) | -2.47% (4.8765) | -2.47% (4.8765) | -2.47% (4.8765) | -2.47% (4.8765) |
| 10 | -2.47% (9.7531) | -2.47% (9.7531) | -2.47% (9.7531) | -2.47% (9.7531) | -2.47% (9.7531) | -2.47% (9.7531) | -2.47% (9.7531) |


Analytic: (1-F)/(1+F) - 1 = -2.469%; break-even price multiple floor (1+F)/(1-F) = 1.02532x.

**Break-even spot multiple needed (spot after others' buying vs spot right after my buy) and extra SOL others must deposit:**

| Buy SOL \ Entry progress | 0% | 10% | 25% | 50% | 75% | 90% | 95% |
|---|---|---|---|---|---|---|---|
| 0.1 | 1.0254x / 0.38 | 1.0254x / 0.41 | 1.0254x / 0.46 | 1.0253x / 0.60 | 1.0253x / 0.85 | 1.0253x / 1.13 | 1.0253x / 1.27 |
| 0.25 | 1.0254x / 0.38 | 1.0254x / 0.41 | 1.0254x / 0.47 | 1.0254x / 0.60 | 1.0254x / 0.85 | 1.0254x / 1.13 | 1.0253x / 1.27 |
| 0.5 | 1.0255x / 0.39 | 1.0255x / 0.42 | 1.0255x / 0.47 | 1.0254x / 0.61 | 1.0254x / 0.86 | 1.0254x / 1.14 | 1.0254x / 1.28 |
| 1 | 1.0257x / 0.40 | 1.0257x / 0.43 | 1.0257x / 0.48 | 1.0256x / 0.62 | 1.0255x / 0.87 | 1.0255x / 1.15 | 1.0254x / 1.29 |
| 2 | 1.0261x / 0.42 | 1.0261x / 0.45 | 1.0260x / 0.50 | 1.0258x / 0.64 | 1.0257x / 0.88 | 1.0256x / 1.16 | 1.0256x / 1.30 |
| 5 | 1.0273x / 0.47 | 1.0271x / 0.50 | 1.0269x / 0.56 | 1.0266x / 0.69 | 1.0262x / 0.94 | 1.0260x / 1.22 | 1.0259x / 1.36 |
| 10 | 1.0290x / 0.57 | 1.0287x / 0.60 | 1.0284x / 0.66 | 1.0277x / 0.79 | 1.0271x / 1.04 | 1.0267x / 1.32 | 1.0265x / 1.46 |


**1 SOL buy: break-even also with an assumed 0.01 SOL fixed round-trip overhead (priority fees/tips; assumed figure, [UNVERIFIED]):**

| Progress | Break-even price multiple (no overhead) | with 0.01 SOL overhead | Mcap at entry (SOL) | Mcap needed (SOL) |
|---|---|---|---|---|
| 0% | 1.0257x | 1.0362x | 28.0 | 30.9 |
| 10% | 1.0257x | 1.0361x | 32.6 | 35.9 |
| 25% | 1.0257x | 1.0361x | 42.1 | 46.0 |
| 50% | 1.0256x | 1.0359x | 70.3 | 75.9 |
| 75% | 1.0255x | 1.0358x | 140.8 | 150.1 |
| 90% | 1.0255x | 1.0358x | 249.5 | 264.1 |


**1 SOL buy: break-even vs the pre-buy market cap (includes your own impact):**

| Entry progress | avg entry price / spot-before | needed spot / entry-spot-before (market-cap multiple from pre-buy mcap) |
|---|---|---|
| 0% | 1.0458 | 1.0944x (mcap 28.0 -> 30.6 SOL, ends at 6.0% progress) |
| 10% | 1.0434 | 1.0892x (mcap 32.6 -> 35.5 SOL, ends at 15.2% progress) |
| 25% | 1.0397 | 1.0815x (mcap 42.1 -> 45.5 SOL, ends at 29.2% progress) |
| 50% | 1.0335 | 1.0686x (mcap 70.3 -> 75.2 SOL, ends at 52.8% progress) |
| 75% | 1.0274 | 1.0558x (mcap 140.8 -> 148.6 SOL, ends at 76.6% progress) |
| 90% | 1.0237 | 1.0482x (mcap 249.5 -> 261.5 SOL, ends at 91.1% progress) |


- The break-even multiple barely depends on size because the curve's own impact is symmetric; larger size needs more demand from others in absolute SOL (0.4 to 1.5 SOL of net outside buying for ~0.1-10 SOL positions depending on progress).
- Caveat: break-even holds only if the curve is still open when you sell. After completion/migration, PumpSwap fees are tiered (1.25% at the lowest tier, falling with mcap per the fee sheet), and liquidity then comes from the migrated pool (see last bullet).
- Post-graduation pool seed (derived): pool opens with the curve's remaining tokens (206.9M = 1B - 793.1M real sold) and ~85 SOL minus 0.015 SOL migration fee, giving the pool the same mcap as at completion (~411 SOL); the pool's price therefore starts at the curve's end price. **[UNVERIFIED]** whether exactly 206.9M tokens (=20.69%) go to the pool; derived from supply minus real sold.

### Gaps
- Sell-side creator/protocol fee rates if tier logic differs for sells **[UNVERIFIED]**.
- No MEV/sandwich or failed-transaction cost modelling.
- Real-world break-even is higher when including slippage settings, bundlers/snipers who front-run, and dev dumps; not quantifiable from curve math alone.
