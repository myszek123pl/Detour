# Solana memecoin launchpads: token mechanics, graduation, market share, on-chain detection (as of Nov 2026)

> **Research conditions (read first).** This session's web-search budget ran out after 2 searches, and the network allowed only github.com / raw.githubusercontent.com. Fetches to bitquery.io, cryptobriefing.com, en.cryptonomist.ch, docs.raydium.io and docs.meteora.ag failed (DNS blocked). As a result:
> - **pump.fun / PumpSwap / Meteora DBC facts** come from **primary sources**: the official `pump-fun/pump-public-docs` GitHub repo, its IDLs, and the `MeteoraAg/dynamic-bonding-curve` README. Those pages carry no dates beyond the "© 2026" footer, so they reflect the repo state as of Nov 2026.
> - **Market-share figures** come from **search-result summaries**, not fetched articles. Treat them as secondary.
> - **Competitor mechanics** (LetsBonk, Raydium LaunchLab, Believe, Moonshot, Boop, Heaven, Bags) could not be fetched. What I know of them is in the *Inferences / Gaps* subsections, labelled **[UNVERIFIED – background knowledge]**, and must be checked before a bot relies on it.
> - To finish this work, allow these hosts in the session network settings: docs.raydium.io, docs.meteora.ag, bitquery.io, dune.com, cryptobriefing.com.

---

## 1. pump.fun bonding curve math, fees, graduation and migration

### Takeaway
pump.fun's bonding curve is a constant-product (Uniswap V2-style) curve on virtual reserves: 30 virtual SOL against 1.073B virtual tokens, with 793.1M of the 1B supply sold on the curve. When real token reserves hit 0 (≈85 SOL raised; ≈411 SOL fully diluted market cap), the curve is flagged `complete`. A permissionless `migrate` then moves the remaining ~206.9M tokens and the raised SOL into a canonical PumpSwap pool and burns the LP. The old Raydium path (`withdraw`) is disabled. Fees are no longer a flat 1%: since a "September 1, 20:00 UTC" upgrade (year not stated in the doc; very likely 2025), a fee program applies market-cap-tiered protocol and creator fees. In 2026 the protocol added v2/v3 trade instructions, fees retained in the curve or pool, synthetic migration, mayhem mode, holder-reward coins and non-SOL quote mints.

### Cited Findings

**Program and accounts**
- Pump bonding-curve program ID: `6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P`, the same on mainnet and devnet. Global PDA (seeds `["global"]`) = `4wTV1YmiEkRvAtNtsSGPtUrqRYQMe5SKy2uB4Jjaxnjf` — [pump-public-docs PUMP_PROGRAM_README](https://github.com/pump-fun/pump-public-docs/blob/main/docs/PUMP_PROGRAM_README.md)
- Global parameters, in raw units with 6 token decimals and lamports for SOL — [PUMP_PROGRAM_README](https://github.com/pump-fun/pump-public-docs/blob/main/docs/PUMP_PROGRAM_README.md):
  - `initial_virtual_token_reserves = 1_073_000_000_000_000` (1.073B tokens)
  - `initial_virtual_sol_reserves = 30_000_000_000` (30 SOL)
  - `initial_real_token_reserves = 793_100_000_000_000` (793.1M tokens)
  - `token_total_supply = 1_000_000_000_000_000` (1B tokens)
  - `fee_basis_points = 100` (1%)
  - `pool_migration_fee = 15_000_001` lamports (≈0.015 SOL; covers accounts created in `migrate`, with `MAX_MIGRATE_FEES = 15_000_000`)
  - `enable_migrate = true`
  - the old `creator_fee` field is 0 and unused
- BondingCurve PDA seeds: `["bonding-curve", mint]` — [PUMP_PROGRAM_README](https://github.com/pump-fun/pump-public-docs/blob/main/docs/PUMP_PROGRAM_README.md)
  - Base fields: `virtual_token_reserves`, `virtual_sol_reserves`, `real_token_reserves`, `real_sol_reserves`, `token_total_supply` (all u64), and `complete` (bool).
  - Fields appended over time: `creator`, `is_mayhem_mode`, `is_cashback_coin`, `quote_mint`, `creator_fee_bps`, `can_edit_creator_fee` (always false) and `is_holder_reward`.
  - Older accounts are shorter. Read any missing trailing field as 0, false or `Pubkey::default()`.
- Later field renames: `virtual_sol_reserves` → `virtual_quote_reserves` and `real_sol_reserves` → `real_quote_reserves`. A new global, `initial_virtual_quote_reserves`, applies to non-SOL quote mints. `quote_mint = Pubkey::default()` means SOL — [pump-public-docs README](https://github.com/pump-fun/pump-public-docs)
- Community fit of on-chain purchases: virtual pool of 30 SOL and 1,073,000,191 tokens, initial k ≈ 32,190,005,730. Spot price = vSOL / vTokens ≈ 2.8e-8 SOL per token at launch — [Mobula almanac](https://docs.mobula.io/almanac/bonding-curves), [accelaratedcurve substack](https://accelaratedcurve.substack.com/p/bonding-curve-mathematics-from-theory) (search-snippet level)
- Buy output formula used by integrators: `tokens_out = sol_in_net * vT / (vS + sol_in_net)`, with the fee taken from the SOL input first — [madeonsol blog](https://madeonsol.com/blog/solana-bonding-curves-explained), [skills.sh pump-fun-mechanics](https://skills.sh/sanctifiedops/solana-skills/pump-fun-mechanics) (search-snippet level). The official README only says the curve is "based on Uniswap V2" with synthetic reserves: on a buy, SOL reserves rise and token reserves fall by matching amounts — [PUMP_PROGRAM_README](https://github.com/pump-fun/pump-public-docs/blob/main/docs/PUMP_PROGRAM_README.md)

**Completion and migration**
- `complete` is set to true at the end of the `buy` that brings `real_token_reserves` to 0. A curve is migratable when `complete == true && real_token_reserves == 0`. — [PUMP_PROGRAM_README](https://github.com/pump-fun/pump-public-docs/blob/main/docs/PUMP_PROGRAM_README.md)
- `migrate(user, mint)` is **permissionless and idempotent**. It moves the completed curve's liquidity to PumpSwap and **burns the LP tokens** it receives. `withdraw`, the deprecated Raydium migration path, is **disabled**. — [PUMP_PROGRAM_README](https://github.com/pump-fun/pump-public-docs/blob/main/docs/PUMP_PROGRAM_README.md)
- After completion and before migration, all trades fail with `BondingCurveComplete`. — [SYNTHETIC_MIGRATION.md](https://github.com/pump-fun/pump-public-docs/blob/main/docs/SYNTHETIC_MIGRATION.md)
- **Synthetic migration** (newer; applies to `buy_v3`, `buy_exact_quote_in_v3` and `multi_hop_swap` curve hops) — [SYNTHETIC_MIGRATION.md](https://github.com/pump-fun/pump-public-docs/blob/main/docs/SYNTHETIC_MIGRATION.md):
  - The buy that empties the curve has no maximum size. It first takes everything left on the curve at the curve price.
  - The rest of the buy is priced against the reserves the pool would open with:
    - `pool_base = associated_base_bonding_curve.amount − remaining`
    - `pool_quote = real_quote_reserves + curve_quote − Global.pool_migration_fee` for SOL pairs
  - Pool-part cost: `ceil(pool_quote*out/(pool_base−out))`.
  - `migrate_v2` then creates the pool with exactly the reserves left, so the pool opens at the price where the buy stopped.
  - Events, in order: `TradeEvent` → `CompleteEvent` → `PostCompleteBuyEvent`. The curve stores `post_complete_base_out` and `post_complete_quote_in`.
  - Both parts pay the bonding-curve fee schedule, not PumpSwap fees.
  - Mayhem-mode coins and legacy `buy`/`buy_v2` do **not** get synthetic migration.
- PumpSwap pools created by Pump `migrate` use `CANONICAL_POOL_INDEX == 0`. Pool PDA seeds: `["pool", index, creator, baseMint, quoteMint]`. A canonical pool's `pool.creator` = `pumpPoolAuthorityPda(baseMint)`. — [PUMP_SWAP_README](https://github.com/pump-fun/pump-public-docs/blob/main/docs/PUMP_SWAP_README.md), [FEE_PROGRAM_README](https://github.com/pump-fun/pump-public-docs/blob/main/docs/FEE_PROGRAM_README.md)
- Sources disagree on the graduation threshold. "~85 SOL deposited" is the common figure; some guides say "55–56 SOL", which looks like a counting error. — [search summary of Mobula/bybit/dextools guides](https://docs.mobula.io/almanac/bonding-curves). The 85 SOL figure matches the math in Inferences below.

**Fees**
- Flat global fee: `fee_basis_points = 100` (1%) — [PUMP_PROGRAM_README](https://github.com/pump-fun/pump-public-docs/blob/main/docs/PUMP_PROGRAM_README.md)
- **Creator fee introduced**: Pump and PumpSwap mainnet update scheduled for "Monday, May 12, 11:00 AM UTC". The year is not stated, but May 12 was a Monday in 2025. — [PUMP_CREATOR_FEE_README](https://github.com/pump-fun/pump-public-docs/blob/main/docs/PUMP_CREATOR_FEE_README.md)
  - Fees accrue to a `creator-vault` PDA (seeds `b"creator-vault"`, `bonding_curve.creator`) and are withdrawn with `collect_creator_fee`, which the creator signs.
  - Eligible: all non-completed curves and canonical PumpSwap pools. **Not** eligible: coins already migrated to Raydium, and non-canonical PumpSwap pools.
- **Dynamic, market-cap-tiered fees**: the fee program accounts became mandatory "Monday, September 1, 20:00 UTC" (Sept 1 was a Monday in 2025) — [FEE_PROGRAM_README](https://github.com/pump-fun/pump-public-docs/blob/main/docs/FEE_PROGRAM_README.md)
  - Bonding-curve market cap = `virtualSolReserves × mintSupply ÷ virtualTokenReserves`. The tier gives protocol bps and creator bps.
  - PumpSwap canonical-pool market cap = `quoteReserve × baseMintSupply ÷ baseReserve`. The tier gives LP, protocol and creator bps.
  - Non-canonical pools pay `flatFees`.
  - Tier rule: below the first threshold, the first tier applies. Otherwise the highest tier with threshold ≤ market cap applies.
  - **The numeric tier table is only in an image (`fees.png`) that I could not extract.**
- Fee program ID: `pfeeUxB6jkeY1Hxd7CsFCAjcbHA9rWtchMGdZ6VojVZ`. It has 31 instructions, including `get_fees`, `get_fees_with_quote_mint`, `upsert_fee_tiers`, `upsert_stable_fee_tiers`, `create_fee_sharing_config`, `initialize_buyback`, `sweep_buyback` and social/donation fee PDAs. Its accounts include `FeeConfig`, `SharingConfig` and `BuybackVault`. — [pump_fees.json IDL](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/idl/pump_fees.json)
- **Fees retained in the curve or pool (2026)**: v3 curve trades and PumpSwap v2 trades leave protocol and creator fees in the curve/pool instead of paying them out on each trade. Creators, CTOs and fee-sharing setups must call the permissionless `sweep_protocol_fee` / `sweep_creator_fee`. — [pump-public-docs README](https://github.com/pump-fun/pump-public-docs)
  - On PumpSwap this is tracked in a signed `Pool.virtual_quote_reserves`. Effective quote reserves = `pool_quote_token_account.amount + virtual_quote_reserves`, which equals real quote reserves + `boost_reserves`. Price is unchanged by sweeps.
  - It "can be negative" from "September 30" (year not stated; context suggests 2026). — [VIRTUAL_QUOTE_RESERVES_FEE_ADJUSTMENT.md](https://github.com/pump-fun/pump-public-docs/blob/main/docs/VIRTUAL_QUOTE_RESERVES_FEE_ADJUSTMENT.md), [pump-public-docs README](https://github.com/pump-fun/pump-public-docs)
  - A "buyback" part of the fee exists, but its bps value is not given. — [VIRTUAL_QUOTE_RESERVES_FEE_ADJUSTMENT.md](https://github.com/pump-fun/pump-public-docs/blob/main/docs/VIRTUAL_QUOTE_RESERVES_FEE_ADJUSTMENT.md)
- **Holder-reward coins**: the creator fee on every trade goes to holders, paid out by pump.fun. Flagged by `is_holder_reward` on the curve and pool. **Cashback mode is deprecated**: `create_v2` rejects `is_cashback_enabled = true`, but existing cashback coins still trade and claim. — [pump-public-docs README](https://github.com/pump-fun/pump-public-docs)
- **Non-SOL quote mints**: USDC pairs are planned or added; USDC-paired coins cannot be traded with legacy instructions. From "October 13", `create_v2` can pair a new coin with another pump coin, up to depth 2 (SOL → A → B → C). — [pump-public-docs README](https://github.com/pump-fun/pump-public-docs)
- **Mayhem mode**: `create_v2` takes `is_mayhem_mode` and a mayhem program account `MAyhSmzXzV1pTf7LsNkrNwkWKTo4ougAJ1PPg47MD4e`, plus `mayhem_state` (PDA seeds "mayhem-state", mint) and `mayhem_token_vault`. `create_v2` mints use Token-2022 (`TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb`). — [pump.json IDL](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/idl/pump.json)

**SDK versions (Nov 2026)**
- `@pump-fun/pump-sdk` 4.1.0, `@pump-fun/pump-swap-sdk` 2.1.0, `pump-rust-client` 0.4.1 — [pump-public-docs README](https://github.com/pump-fun/pump-public-docs)

### Inferences
- **Graduation math, derived from the official constants:**
  - k = 30 × 1.073e9 = 3.219e10.
  - At completion: virtual tokens = 1.073e9 − 0.7931e9 = 2.799e8, so virtual SOL = k / 2.799e8 ≈ **115.005 SOL**.
  - Real SOL raised ≈ **85.005 SOL**, net of fees.
  - Final curve price ≈ 115.005 / 2.799e8 ≈ **4.109e-7 SOL/token**, a fully diluted market cap of ≈ **411 SOL**.
  - Starting price ≈ 2.796e-8 SOL, a market cap of ≈ 28 SOL. The price rises ~14.7× across the curve.
  - The PumpSwap pool then gets ≈206.9M tokens and ≈85.005 − 0.015 ≈ 84.99 SOL, a price of ≈4.108e-7. This matches the final curve price, so by design there is no price discontinuity at migration.
  - In USD, graduation ≈ 411 × SOL price (e.g. ~$62k at $150 per SOL). The USD threshold therefore moves with SOL.
- **Progress metric for a bot:** `progress = 1 − real_token_reserves / 793.1M`. Equivalently, `real_sol_reserves / ~85 SOL`.
- **Buy and sell quote formulas** (legacy `buy` gives exact tokens `amount` with `max_sol_cost`):
  - Buy: `sol_cost_pre_fee = ceil(vS × amount / (vT − amount))`, then add protocol + creator bps for the tier.
  - Sell: `sol_out = vS × amount / (vT + amount)`, minus fees.
  - Build fee tiers from on-chain `FeeConfig` (fee program) rather than hard-coding them. The fee doc itself says tier changes should then need no code changes.
- **Retained fees:** because v3 trades keep fees in the curve or pool, a bot that reads vault token balances to infer price will be wrong. Use the virtual/effective reserve fields instead.
- **Instruction versions:** the date gaps for "pump.fun v2" trades in Bitquery's archive (7–26 May 2026; see section 2) suggest the `buy_v2`/`sell_v2` instruction family went live around May 2026. Indexers that only decoded legacy `buy`/`sell` missed them. A bot must decode all of `buy`, `buy_exact_sol_in`, `buy_v2`, `buy_exact_quote_in_v2`, `buy_v3`, `buy_exact_quote_in_v3`, `sell`, `sell_v2`, `sell_v3` and `multi_hop_*`.
- **[UNVERIFIED – background knowledge, not fetched this session]**
  - PumpSwap launched ~20 March 2025.
  - Before that, graduated pump.fun tokens migrated to Raydium AMM v4 with a ~6 SOL migration fee, at a USD threshold of about $69k market cap.
  - The PumpSwap default fee was 0.25% (0.20% LP + 0.05% protocol), later +0.05% creator.
  - The Sept 2025 "Project Ascend" dynamic fees set creator fees high at low market caps (≈0.95% at the low end), declining toward ≈0.05% at high market caps.
  - The PUMP token ICO took place 12 July 2025.
  - Mayhem mode (AI-agent trading on new coins) launched around Nov 2025.
  - Verify all of these against pump.fun announcements before use.

### Gaps
- **Numeric dynamic fee tiers** (thresholds and protocol/creator/LP bps for curve and PumpSwap): they are in an image in FEE_PROGRAM_README and were not extractable. Read them on-chain from the `FeeConfig` account (`pump_fees` program) or decode `fees.png`.
- **Exact years** for the "Sept 30" negative-reserves change and the "Oct 13" pump-coin-quote change. The year is assumed to be 2026 from context but is not stated.
- **Buyback fee bps and mechanism** (`initialize_buyback`/`sweep_buyback`): not documented in the pages read.
- **Full event schemas** (`CreateEvent`, `TradeEvent`, `CompleteEvent`, `CompletePumpAmmMigrationEvent`, `PostCompleteBuyEvent`): the IDL is 329k characters and the events section was not reached (it lies past offset 200,000 of `idl/pump.json`).

---

## 2. Competitors and market share (2025–2026)

### Takeaway
pump.fun has been dominant again since mid-2025. Bitquery data for Nov 2025–early Oct 2026 shows it creating ~78% of new Solana tokens (65% in Nov 2025, ~90% in Aug 2026). By revenue it took ~92–98% of launchpad fees in Aug–Oct 2026, versus ~62% of revenue and ~55% of volume in an early-July snapshot. LetsBonk (Raydium LaunchLab) and Meteora DBC-based launchpads are distant seconds, at roughly 5–7% each in one undated snapshot. Meteora DBC is the shared infrastructure for several "white-label" launchpads.

### Cited Findings
- **Bitquery** (11.5M new Solana tokens, Nov 2025 → early Oct 2026): pump.fun created **78%**. Monthly share rose from **65% (Nov 2025)** to **90% (Aug 2026)**, then fell back in Sep 2026. Only **1 in 58 coins graduate**, and **79% die after day one**. Caveat: pump.fun trades made through the "v2" version are missing from the archive for **7–26 May 2026**. — [Bitquery investigation](https://bitquery.io/investigations/solana-launchpad-year) (search-summary only; page fetch blocked)
- **Crypto Briefing (12 Aug 2026)**: pump.fun had ~**98%** of tracked launchpad revenue in early Aug 2026, with its fee share having "rebounded to 50% after July dip". Its share of graduated tokens settled at **70–80%**. — [Crypto Briefing](https://cryptobriefing.com/pump-fun-fee-share-rebounds-50-percent/) (search summary; the headline and 98% figures look inconsistent and need checking)
- **Coinfomania (19 Oct 2026)**: pump.fun >**92%** of launchpad sector revenue. — [Coinfomania](https://coinfomania.com/pumpfun-dominates-launchpad-market-capturing-92-of-revenue/)
- **Phemex (early July, presumably 2026)**: ~**62%** of launchpad revenue and ~**55%** of volume over two weeks. — [Phemex](https://phemex.com/blogs/pump-token-rally-pumpfun-solana-meme-dominance)
- **Intellectia (date not stated)**: pump.fun **73.3%**, LetsBonk **6.95%**, Meteora DBC **5.48%**. — [Intellectia](https://intellectia.ai/news/crypto/pumpfun-dominates-solana-launchpad-market-with-733-share)
- **Cryptonomist (10 Jun 2026)**: 11.9M pump.fun token launches, with ~98% failing. — [Cryptonomist](https://en.cryptonomist.ch/2026/06/10/pump-fun-solana-token-launches/) (search snippet)
- **"Pump.fun retakes the lead"** coverage reports that pump.fun lost and then regained the lead. — [Crypto-Economy](https://crypto-economy.com/pump-fun-retakes-the-lead-in-solanas-launchpad-race/). New 2026 competitors such as "Stonk" and "Pons" are mentioned in search summaries without detail.
- **Meteora DBC (primary source)** — [MeteoraAg/dynamic-bonding-curve](https://github.com/MeteoraAg/dynamic-bonding-curve):
  - Program `dbcij3LWUppWqq96dh6gJWwBifmcGfLSB5D4DuSMaqN`.
  - Curve: constant product `x*y = liquidity²`, as piecewise ranges (up to 20 ranges of sqrt-price and liquidity) from `sqrt_start_price`.
  - Graduation happens when the pool reaches the partner-set `migration_quote_threshold`.
  - Migration targets: DAMM v1 (option 0) is **deprecated for new configs**; DAMM v2 (option 1) is the default.
  - Post-migration fee options: 0.25%, 0.3%, 1%, 2%, 4%, 6%, or custom.
  - Fees: `base_fee` (fixed, fee scheduler or rate limiter, used for anti-sniping) plus an optional `dynamic_fee`.
  - Fee split: protocol, partner (the launchpad), creator (`creator_trading_fee_percentage`), and a referral share for hosts such as Jupiter.
  - LP split: partner and creator, claimable or locked, with optional vesting via Jup Lock.
  - A partner-set `migration_fee` is taken from the threshold.
- **Raydium LaunchLab**: the official docs (docs.raydium.io) were blocked. See Inferences.

### Inferences
- Because Meteora DBC is configurable per partner (thresholds, curve shapes, fee schedules), a bot cannot assume pump.fun constants for DBC tokens. It must read each pool's `config` account (`migration_quote_threshold`, curve ranges, fee schedule) to model price and graduation.
- Share depends heavily on the metric. Launch-count share, about 78–90% for pump.fun, overstates economic share in some periods and understates it in others. Revenue share (92–98% in late 2026) is the better signal of where real trading volume is.
- **[UNVERIFIED – background knowledge; verify before use]:**
  - **Raydium LaunchLab**:
    - Launched ~April 2025.
    - Program `LanMV9sAd7wArD4vJFi2qDdfnVhFxYSUg6eADduJ3uj`.
    - Default ~85 SOL graduation, ~1% trade fee.
    - Migrates to Raydium AMM v4 (`675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8`) or CPMM (`CPMMoo8L3F4NbTegBCKVNunggL7H1ZpdTHKxQB5qKP1C`).
    - LP handled via Burn & Earn with a creator fee share.
    - Supports "platform" configs, so third parties set their own fees and branding.
  - **LetsBonk.fun**:
    - BONK-community launchpad on LaunchLab, launched ~April 2025.
    - Briefly overtook pump.fun in daily launches and graduations in early-to-mid July 2025.
    - Part of its fees bought back BONK.
    - pump.fun regained the lead from August 2025, after the PUMP ICO, buybacks and creator-fee changes.
  - **Believe** (ex-Clout):
    - Coins launched by tagging @launchcoin on X.
    - Built on Meteora DBC, peaking in May 2025 and fading by mid-2025.
  - **Moonshot**:
    - DEX Screener-affiliated, with its own program historically (`MoonCVVNZFSYkqNXP6bxHLPL6QQJiMagDL3qcqUQTrG`).
    - Later moved to Meteora DBC infrastructure.
  - **Boop.fun**: launched May 2025, with staking-based rewards to BOOP holders.
  - **Heaven**:
    - Launched ~Aug 2025, with its own AMM.
    - Protocol fees used to buy back and burn its LIGHT token.
  - **Bags**:
    - Creator-royalty launchpad (≈1% of volume to creators or designated X accounts).
    - Built on Meteora DBC/DAMM v2, and notable in 2026.
  - **Jupiter Studio**: also built on DBC.

### Gaps
- No primary Dune dashboard data was retrieved. Dashboards such as adam_tehc's "Solana Launchpads" or hashed_official's could not be fetched, so there is no month-by-month share table for 2025.
- The exact peak LetsBonk share in July 2025 and the dates it overtook pump.fun are not verified in this session.
- Current (Nov 2026) per-launchpad graduation thresholds and fees for LetsBonk, Bags, Believe, Boop, Heaven and Moonshot were not verified.
- The undated Intellectia snapshot cannot be placed in time.
- The Crypto Briefing headline (50%) and body (98%) appear contradictory, possibly measuring different things. The article needs a direct read.

---

## 3. What happens on-chain at graduation, and why it is tradeable

### Takeaway
Graduation is a discrete, observable two-step event:
1. The buy that empties the curve sets `complete = true` and emits `CompleteEvent`. All curve trading then halts with `BondingCurveComplete`.
2. A permissionless `migrate`/`migrate_v2` creates a canonical PumpSwap pool (index 0) with ~206.9M tokens and ~85 SOL, minus a 0.015 SOL fee, and burns the LP.

It is tradeable because:
- liquidity and venue change (the token becomes routable on PumpSwap, then via Jupiter and other aggregators);
- the fee regime changes to PumpSwap canonical-pool tiers;
- there is a brief halt between completion and migration;
- graduation acts as a widely watched quality and attention signal (only ~1 in 58 coins get there).

With v3 synthetic migration, the price is continuous across the boundary, which reduces the old pure-arbitrage gap.

### Cited Findings
- Completion flag and halt: `complete` is set when `real_token_reserves` hits 0, and all trades fail with `BondingCurveComplete` until migration. — [PUMP_PROGRAM_README](https://github.com/pump-fun/pump-public-docs/blob/main/docs/PUMP_PROGRAM_README.md), [SYNTHETIC_MIGRATION.md](https://github.com/pump-fun/pump-public-docs/blob/main/docs/SYNTHETIC_MIGRATION.md)
- `migrate` is permissionless and idempotent, moves liquidity to PumpSwap and burns the LP. `pool_migration_fee` = 15,000,001 lamports. — [PUMP_PROGRAM_README](https://github.com/pump-fun/pump-public-docs/blob/main/docs/PUMP_PROGRAM_README.md)
- A completing v3 buy emits `TradeEvent` → `CompleteEvent` → `PostCompleteBuyEvent`. `migrate_v2` opens the pool at the price where that buy stopped. Mayhem-mode coins are excluded. — [SYNTHETIC_MIGRATION.md](https://github.com/pump-fun/pump-public-docs/blob/main/docs/SYNTHETIC_MIGRATION.md)
- PumpSwap fees after graduation — [PUMP_SWAP_README](https://github.com/pump-fun/pump-public-docs/blob/main/docs/PUMP_SWAP_README.md), [FEE_PROGRAM_README](https://github.com/pump-fun/pump-public-docs/blob/main/docs/FEE_PROGRAM_README.md):
  - GlobalConfig defaults are LP 20 bps and protocol 5 bps, with no fee on deposit or withdraw.
  - Canonical pools use market-cap tiers (LP/protocol/creator) from the fee program.
  - Creator fees continue on canonical pools after migration.
- Graduation rate: ~1 in 58 pump.fun coins graduate, and 79% die after day one (Nov 2025 – Oct 2026). — [Bitquery](https://bitquery.io/investigations/solana-launchpad-year) (search summary)
- Meteora DBC graduation: when `migration_quote_threshold` is reached, the pool migrates to DAMM v2 with a partner-configured fee tier and an LP split (locked or claimable). The last swap creates a quote surplus, split between partner and protocol. — [Meteora DBC GitHub](https://github.com/MeteoraAg/dynamic-bonding-curve)

### Inferences
- **Tradeable mechanics for a bot:**
  - (a) **Pre-graduation momentum**: price convexity near the curve's end is steep. Moving from 90% to 100% progress raises the price by roughly 30–40% (it is proportional to 1/vT²), and buyers race to be the completing buy.
  - (b) **Migration latency window**: between `CompleteEvent` and `migrate`, the token cannot be traded on pump. The first PumpSwap trades after `migrate` and `create_pool` are a sniping and arbitrage opportunity, especially for legacy (non-v3) completions, where the completing buy is capped at the remaining curve tokens.
  - (c) **Routing expansion**: after migration the token becomes visible to aggregators and DEX screeners, typically bringing a burst of new flow.
  - (d) **Fee-regime change**: PumpSwap tiered fees replace curve fees, which affects round-trip cost modelling.
  - (e) **"Sell the graduation"**: given that 79% of coins die within a day, post-graduation dumps are common. Exact statistics were not retrieved.
- Since migration is permissionless, a bot can call `migrate` itself (paying the account costs) to be first to trade the new pool, if no one else has migrated. pump.fun's backend presumably also cranks it.
- **[UNVERIFIED – background knowledge]** Before PumpSwap (pre ~20 Mar 2025), graduation meant:
  - a 6 SOL fee;
  - a Raydium AMM v4 pool seeded by pump.fun's migration account;
  - LP burned;
  - a noticeable delay, which made "Raydium migration sniping" a well-known strategy.

### Gaps
- No empirical data was retrieved on the typical latency between `CompleteEvent` and `migrate` in 2026, or on post-graduation return distributions.
- The exact `migrate_v2` account list and the `CompletePumpAmmMigrationEvent` schema were not retrieved; they are in the events section of `idl/pump.json`, past offset 200,000.

---

## 4. Program IDs and instructions for detecting launches and trades

### Takeaway
Monitor these programs:
- the Pump curve program `6EF8…F6P`: `create`/`create_v2`, buy/sell v1–v3, `migrate`/`migrate_v2`;
- PumpSwap `pAMM…XEA`: `create_pool`, `buy`/`sell` (+v2), `multi_hop_swap`;
- the Pump fee program `pfee…VjVZ`;
- the Pump mayhem program `MAyh…MD4e`;
- Meteora DBC `dbci…MaqN`;
- (unverified) Raydium LaunchLab `LanM…uj3uj`, Raydium AMM v4/CPMM, Meteora DAMM v2.

Prefer Anchor event logs (`CreateEvent`, `TradeEvent`, `CompleteEvent`, `BuyEvent`/`SellEvent`) emitted via the `__event_authority` PDA over parsing instruction arguments. Decode **all** instruction versions: the May 2026 indexer gap shows the risk of missing them.

### Cited Findings
- **Pump curve program** `6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P`. — [PUMP_PROGRAM_README](https://github.com/pump-fun/pump-public-docs/blob/main/docs/PUMP_PROGRAM_README.md), [pump.json IDL](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/idl/pump.json)
  - Instructions in the IDL:
    - Creation: `create`, `create_v2`
    - Buys: `buy`, `buy_exact_sol_in`, `buy_v2`, `buy_exact_quote_in_v2`, `buy_v3`, `buy_exact_quote_in_v3`
    - Sells: `sell`, `sell_v2` (+ `sell_v3` per README)
    - Migration: `migrate`, `migrate_v2`, `migrate_bonding_curve_creator`
    - Swaps: `multi_hop_curve_swap`
    - Creator fees: `collect_creator_fee(_v2)`, `distribute_creator_fees(_v2)`, `distribute_fee_to_holders`
    - Cashback: `claim_cashback(_v2)`
    - Volume accumulators: `init_user_volume_accumulator`/`close_user_volume_accumulator`
    - Token incentives: `claim_token_incentives`, `admin_update_token_incentives`
    - Quote mints: `add_quote_mint`/`remove_quote_mint`, `add_quote_control_mint`/`remove_quote_control_mint`
    - Admin: `admin_cto`, `extend_account`, `set_params`, `initialize`, `update_global_authority`, `withdraw` (disabled)
  - Anchor discriminators: `buy` = `[102,6,61,18,1,218,235,234]`, `buy_v3` = `[7,5,29,196,245,23,101,80]`.
  - PDA seeds: `global`, `bonding-curve`, `creator-vault`, `global_volume_accumulator`, `user_volume_accumulator`, `fee_config`, `sharing-config`, `pool`, `pool-authority`, `__event_authority`.
- v2/v3 instruction notes — [pump-public-docs README](https://github.com/pump-fun/pump-public-docs):
  - v2 instructions are unified, with no optional accounts.
  - v3 uses 17 accounts at the same prices and fees.
  - Legacy instructions still work, except for USDC-paired coins.
- Pump coin mints typically end in the vanity suffix `…pump`, for example `7LSsEoJGhLeZzGvDofTdNg7M3JttxQqGWNLo6vWMpump`. — [PUMP_SWAP_README](https://github.com/pump-fun/pump-public-docs/blob/main/docs/PUMP_SWAP_README.md), [FAQ.md](https://github.com/pump-fun/pump-public-docs/blob/main/docs/FAQ.md)
- `create_v2` uses Token-2022 (`TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb`). Legacy coins use SPL Token (`TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA`). Mayhem program: `MAyhSmzXzV1pTf7LsNkrNwkWKTo4ougAJ1PPg47MD4e`. — [pump.json IDL](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/idl/pump.json)
- **PumpSwap (Pump AMM)** `pAMMBay6oceH9fJKBRHGP5D4bD4sWpmSwMn52FMfXEA`; GlobalConfig `ADyA8hdefvWN2dbGGWFotbzWxrAvLW83WG6QCVXvJKqw`. — [PUMP_SWAP_README](https://github.com/pump-fun/pump-public-docs/blob/main/docs/PUMP_SWAP_README.md), [pump-public-docs README](https://github.com/pump-fun/pump-public-docs)
  - Instructions: `create_pool`, `buy`, `sell`, `deposit`, `withdraw`, `extend_account`, plus newer `buy_v2`, `sell_v2`, `buy_exact_quote_in_v2`, `multi_hop_swap`, `sweep_protocol_fee` and `sweep_creator_fee`.
  - Events: `BuyEvent`/`SellEvent`, including `virtual_quote_reserves` (and `holder_rewards` on holder-reward pools).
- **Pump fee program** `pfeeUxB6jkeY1Hxd7CsFCAjcbHA9rWtchMGdZ6VojVZ`. — [pump_fees.json](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/idl/pump_fees.json)
- **Meteora DBC** `dbcij3LWUppWqq96dh6gJWwBifmcGfLSB5D4DuSMaqN`; pools are created via `create_config` + `initialize_virtual_pool`. — [Meteora DBC GitHub](https://github.com/MeteoraAg/dynamic-bonding-curve)
- Compute budget: pump recommends a static ~100,000 CU limit for buy/sell rather than per-transaction simulation, or simulated CU plus a 1% buffer. Completing buys use more CU. — [FAQ.md](https://github.com/pump-fun/pump-public-docs/blob/main/docs/FAQ.md)

### Inferences
- **Launch detection**: subscribe (Geyser/gRPC or `logsSubscribe` with `mentions`) to `6EF8…F6P` and filter for `create`/`create_v2`, or for `CreateEvent` in logs.
  - For DBC launches, filter `initialize_virtual_pool*` on `dbci…MaqN` and map the `config` account to the partner (e.g. Bags, Jupiter Studio, Believe-era configs) to attribute the launchpad.
  - For LaunchLab, filter its initialize instruction and read the `platform_config` to tell LetsBonk apart from other platforms (unverified).
- **Trade detection**: decode `TradeEvent` (curve) and `BuyEvent`/`SellEvent` (PumpSwap) rather than balance diffs. Retained fees and `virtual_quote_reserves` make vault balances misleading.
- **Graduation detection**: watch for `CompleteEvent` (curve), then `migrate`/`migrate_v2` plus the PumpSwap `create_pool` with index 0 and a creator equal to the pool-authority PDA.
- **[UNVERIFIED – background knowledge]** Other program IDs:
  - Raydium LaunchLab `LanMV9sAd7wArD4vJFi2qDdfnVhFxYSUg6eADduJ3uj`
  - Raydium AMM v4 `675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8`
  - Raydium CPMM `CPMMoo8L3F4NbTegBCKVNunggL7H1ZpdTHKxQB5qKP1C`
  - Meteora DAMM v2 `cpamdpZCGKUy5JxQXB4dcpGPiikHawvSWAd6mEn1sGG`
  - Moonshot `MoonCVVNZFSYkqNXP6bxHLPL6QQJiMagDL3qcqUQTrG`
  - Legacy pump.fun → Raydium migration authority `39azUYFWPz3VHgKCf3VChUwbpURdCHRxjWVowf5jUJjg`
  - Confirm each against official docs or Solscan before hard-coding.

### Gaps
- No verified program IDs were obtained for Boop, Heaven or Bags (whether Bags uses its own program or only DBC configs), or for the current LetsBonk platform config.
- Discriminators for `create`, `create_v2`, `sell`, `migrate` and all events were not extracted (IDL truncation). Compute them as `sha256("global:<ix_name>")[0..8]` for instructions and `sha256("event:<EventName>")[0..8]` for events, or read the IDL directly.
- Helius / QuickNode developer guides were not reachable this session (search budget exhausted, network restricted).
