# Pump.fun and PumpSwap fee structure (as of Nov 2026) and round-trip trading cost

Access notes: raw.githubusercontent.com (pump-fun/pump-public-docs) was readable. pump.fun/docs/fees, coinpaprika, theblock, jsdelivr/unpkg and Solana RPC hosts were NOT reachable from this sandbox. The market-cap tier VALUES therefore come only from search-engine snippets of the official pump.fun/docs/fees page (not read directly) plus secondary sites. The values are NOT stored in the public IDL or docs, which only give the data structure. Tier values are flagged [UNVERIFIED] below. The FeeConfig accounts were not read on-chain.

## 1. What fee components exist (protocol / LP / creator / buyback) and where are they defined?

### Takeaway
Fees are no longer flat. Since Sept 2025 ("Dynamic Fees V1") the Pump Fees program (`pfeeUxB6jkeY1Hxd7CsFCAjcbHA9rWtchMGdZ6VojVZ`) holds `FeeConfig` accounts with market-cap-tiered `{lp_fee_bps, protocol_fee_bps, creator_fee_bps}`, read by both the bonding curve and PumpSwap at trade time. The curve and the first PumpSwap tier are both 1.25% total. The total then falls as market cap rises. The old docs figures (curve 100 bps; PumpSwap 20 LP + 5 protocol) are stale legacy fields.

### Cited Findings
- Pump Fees IDL defines `FeeConfig { bump, admin, flat_fees: Fees, fee_tiers: Vec<FeeTier>, stable_fee_tiers: Vec<FeeTier>, exotic_flat_fees: Fees }`, `FeeTier { market_cap_lamports_threshold: u128, fees: Fees }`, `Fees { lp_fee_bps, protocol_fee_bps, creator_fee_bps }`. `flat_fees` is documented as "the flat fees for non-pump pools". Admin instructions: `upsert_fee_tiers`, `update_fee_config`, `update_stable_fee_config`, `upsert_stable_fee_tiers`, `set_exotic_flat_fees`. View instructions: `get_fees(is_pump_pool, market_cap_lamports, trade_size_lamports, is_new_quote_mint)` and `get_fees_with_quote_mint`. — [pump_fees.json IDL](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/idl/pump_fees.json)
- Two FeeConfig PDAs, seeds `[b"fee_config", <program_id>]`: bonding curve (Pump) uses `8Wf5TiAheLUqBrKXeYg2JtAFFMWtKdG2BSFgqUcPVwTt`; PumpSwap uses `5PHirr8joyTMp9JMm6nW7hNDVyEYdkzDqazxPD7RaTjx`. Newer v3/v2 trade instructions read the schedule directly from `fee_config`. — [TRADE_V3.md](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/docs/instructions/TRADE_V3.md), [PUMP_SWAP_TRADE_V2.md](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/docs/instructions/PUMP_SWAP_TRADE_V2.md)
- Stale legacy values in the official docs: Pump `Global.fee_basis_points = 100` and `creator_fee` "set to 0 and not used"; PumpSwap `GlobalConfig` `lp_fee_basis_points = 20`, `protocol_fee_basis_points = 5`. These pre-date the FeeConfig tiers and should not be used for cost modelling. — [PUMP_PROGRAM_README.md](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/docs/PUMP_PROGRAM_README.md), [PUMP_SWAP_README.md](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/docs/PUMP_SWAP_README.md)
- Creator fee introduced May 12 2025 11:00 UTC for all non-completed bonding curves and all "canonical" PumpSwap pools (created by Pump `migrate`). Not paid on Raydium-migrated coins or non-canonical PumpSwap pools. Creator vault PDAs: Pump `[b"creator-vault", creator]`; PumpSwap `[b"creator_vault", coin_creator]`. — [PUMP_CREATOR_FEE_README.md](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/docs/PUMP_CREATOR_FEE_README.md), [PUMP_SWAP_CREATOR_FEE_README.md](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/docs/PUMP_SWAP_CREATOR_FEE_README.md)
- Bonding curve per official fee page (via search snippet): creator 0.30% + protocol 0.95% + LP 0% = 1.25% total. [UNVERIFIED, snippet of page not read directly] Graduation (migration) cost flat 0.015 SOL (matches `pool_migration_fee` ~15,000,001 lamports in Global docs). — [pump.fun/docs/fees via search](https://pump.fun/docs/fees); [Pump program docs](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/docs/PUMP_PROGRAM_README.md)
- A "buyback" component exists: events carry `buyback_fee_basis_points` / `buyback_fee`, and docs state "the buyback part of the protocol fee is still paid in the trade" to one of 8 buyback recipients. It is a PART of the protocol fee, not an extra charge (inference from wording; its size is not stated in public docs). Fee is 0 on mayhem pools. — [TRADE_V3.md](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/docs/instructions/TRADE_V3.md), [PUMP_SWAP_TRADE_V2.md](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/docs/instructions/PUMP_SWAP_TRADE_V2.md)
- Fee recipients: 8 normal, 8 reserved (mayhem-mode coins), 8 buyback (24 total). — [FEE_RECIPIENTS.md](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/docs/FEE_RECIPIENTS.md)
- Creator fee sharing (up to 10 wallets) added Jan 2026; one post-launch fee redirect per token allowed from Mar 2026 (secondary reports). — [The Block](https://www.theblock.co/post/384975/pump-fun-overhauls-creator-fees-token-launches-highest-daily-count-since-september) (found via search only), [CoinMarketCap Academy](https://coinmarketcap.com/academy/es/article/pumpdotfun-caps-creator-fee-changes-to-one-per-token)

### Inferences
- Because the curve ends at about 420 SOL market cap (the first PumpSwap tier boundary; inference from the matching 1.25% total and 0.93+0.02 LP/protocol split vs the curve's 0.95 protocol), the entire bonding-curve phase and the first post-graduation tier cost the same 1.25%.
- Protocol 0.95% on the curve equals PumpSwap tier-0 protocol 0.93% + LP 0.02%, so the LP slice is folded into protocol on the curve.

### Gaps
- Exact on-chain `fee_tiers` content not read (no RPC/pump.fun access). Reproduce with `get_fees` simulation or decoding FeeConfig `8Wf5Ti...` / `5PHirr...` with the pump_fees IDL.
- Size of the buyback share of the protocol fee not found.

## 2. Market-cap-tiered fee schedule (PumpSwap canonical pools, SOL-paired)

### Takeaway
Total fee starts 1.25% (0-420 SOL mcap), peaks creator share 0.95% at 420-1,470 SOL, and then steps down 0.05% per band as market cap grows, down to roughly 0.30% total at ~98,240 SOL. From 420 SOL up, LP is 0.20% and protocol 0.05%, so total = creator + 0.25%. [UNVERIFIED: tier boundaries and tail]

### Cited Findings
- Official table via search-engine snippets (page itself not fetched): 0-420 SOL: creator 0.300 / protocol 0.930 / LP 0.020 = 1.250%; 420-1,470: creator 0.950, total 1.200%; 1,470-2,460: 0.900, total 1.150%; 2,460-3,440: 0.850, total 1.100%; 19,650-24,560: total 0.850%; 39,300-44,210: creator 0.400, total 0.650%. — [pump.fun/docs/fees (via search snippets, two queries)](https://pump.fun/docs/fees)
- Secondary: LP fixed at 0.20% and protocol 0.05% in all tiers above the first, creator fee absorbs the decline to 0.05% above 98,240 SOL, total 0.30% floor; 25 tiers. — [CoinPaprika launchpad fees](https://coinpaprika.com/education/launchpad-fees/) (via search summary)
- Conflicting secondary reports: Benzinga says creators earn max 0.95% for 420-1,470 SOL scaling to 0.05% at "$20M mcap"; others cite "1% trading fee, 0.05% creator" (outdated or simplified). — [Benzinga](https://www.benzinga.com/content/47482176/new-pump-fun-fee-structure-pays-creators-more-than-twitch-generates-2-1m-in-24-hours), [soltokencreator](https://www.soltokencreator.io/blog/pump-fun-fees-explained)
- Non-canonical PumpSwap pools use separate schedule (secondary: creator 0%, flat 0.30% total; matches the IDL's `flat_fees` "for non-pump pools"). USDC-paired coins use `stable_fee_tiers` (values not found). — [pump.fun/docs/fees via search](https://pump.fun/docs/fees); [pump_fees.json](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/idl/pump_fees.json)
- Custom pairs (quote other than SOL/USDC): creator picks flat fee 0.01%-3%, immutable; SOL/USDC pairs always use the tiered schedule. Secondary report says 0.05% flat to creator after graduation (single source). — [Crypto Briefing](https://cryptobriefing.com/pumpfun-holder-rewards-cashback-deprecated/) (search result), [HOLDER_REWARDS_README.md](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/docs/HOLDER_REWARDS_README.md)

### Inferences
- Reconstructed tiers (creator bps; total = creator + 25): 420 -> 95; 1,470 -> 90; 2,460 -> 85; 3,440 -> 80 (inferred); 4,420 -> 75 (inferred); 9,820 -> 70 (inferred); 14,730 -> 65 (inferred); 19,650 -> 60 (confirmed by 0.85 total); 24,560 -> 55; 29,470 -> 50; 34,380 -> 45; 39,300 -> 40 (confirmed). Band widths of ~4,910 SOL from 19,650 up are consistent with the confirmed points, but intermediate rows are my interpolation. Tail from 44,210 to 98,240 SOL: [UNVERIFIED].
- Thresholds are in SOL, so USD market-cap for each tier moves with SOL price (the 420 SOL boundary is roughly the old ~$69k graduation cap at ~$165 SOL; not verified at Nov 2026 SOL price).

### Gaps
- Official full 25-row table not read; USDC `stable_fee_tiers` and `exotic_flat_fees` values not found; whether tiers changed after Jan 2026 not confirmed (CMC piece says Pump "rolling out changes to creator fee system").

## 3. Cashback and holder rewards coins

### Takeaway
Cashback (creator fee routed to buyers, introduced ~Feb 2026) is deprecated: `create_v2` rejects it, old cashback coins keep working. New coins choose regular creator-fee or "holder rewards" (creator fee diverted to holders, paid out by pump.fun). Neither changes the fee a trader pays.

### Cited Findings
- `create_v2` rejects `is_cashback_enabled=[true]`; existing cashback coins trade as before and accrued cashback stays claimable (`claim_cashback` / `claim_cashback_v2`). v3 trades fail on cashback coins (`CashbackCoinNotSupported` 6094), use v2. — [README](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/README.md), [PUMP_CASHBACK_README.md](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/docs/PUMP_CASHBACK_README.md), [TRADE_V3.md](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/docs/instructions/TRADE_V3.md)
- Holder rewards: `create_v2(... is_holder_reward=[true])`; "fees are computed exactly as before; the only difference is who ends up receiving the creator fee". Choice is permanent (cannot revert); regular coins can convert via CTO team. Holders do nothing, pump.fun pays out. `BondingCurve` / `Pool` have `is_holder_reward`; events carry `holder_rewards_bps` / `holder_rewards`. — [HOLDER_REWARDS_README.md](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/docs/HOLDER_REWARDS_README.md)
- Secondary: holders need >$20 of token to qualify, payouts pro rata several times per hour; cashback introduced Feb 2026; holder rewards date reported as Sept 2026 by one guide. — [Crypto Briefing](https://cryptobriefing.com/pumpfun-holder-rewards-cashback-deprecated/), [The Defiant](https://thedefiant.io/news/defi/pump-fun-drops-cashback-for-new-launches-adds-holder-rewards), [Cointelegraph](https://regional-front.cointelegraph.com/news/pumpfun-launches-cashback-coins-rewards) (all via search titles/summaries only)

### Inferences
- For a trader, holder-reward coins give a small partial rebate only if you hold (>$20); the headline fee paid is identical. Existing cashback coins effectively refund the creator-fee slice (0.30-0.95%) to the trader on their own volume, cutting round-trip cost by up to that slice per leg (inference; not quantified in sources).

### Gaps
- Exact holder-rewards pro-rata formula; whether holder-reward coins show lower creator rates; cashback coin count remaining.

## 4. How fees are read on-chain

### Takeaway
Read `FeeConfig` PDAs (decode with pump_fees IDL) for the schedule, or read per-trade fees from `TradeEvent` (Pump) / `BuyEvent`/`SellEvent` (PumpSwap) logs, which report bps and amounts per component.

### Cited Findings
- Pump `TradeEvent` fields: `fee_basis_points`, `fee`, `creator_fee_basis_points`, `creator_fee`, `buyback_fee_basis_points`, `buyback_fee`, `cashback_fee_basis_points`, `cashback`, `holder_rewards_bps`, `holder_rewards`, `creator_fee_unclaimed`, `quote_mint`, `virtual_quote_reserves`. — [pump.json IDL](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/idl/pump.json)
- PumpSwap `BuyEvent`/`SellEvent`: `lp_fee_basis_points`, `lp_fee`, `protocol_fee_basis_points`, `protocol_fee`, `coin_creator_fee_basis_points`, `coin_creator_fee`, `buyback_fee(_basis_points)`, `cashback(_fee_basis_points)`, `holder_rewards(_bps)`, `virtual_quote_reserves`, `can_boost`, `base_supply`, `creator_fee_unclaimed`. — [pump_amm.json IDL](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/idl/pump_amm.json)
- Market cap input to tier lookup is in lamports (`market_cap_lamports_threshold`: u128); `get_fees` takes `market_cap_lamports`, `trade_size_lamports`, i.e. the program can be simulated to obtain the exact current fee. — [pump_fees.json](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/idl/pump_fees.json)
- Newer v3 (curve) / v2 (PumpSwap) instructions (17 accounts) keep the protocol and creator fee on the curve/pool (`BondingCurve.protocol_fees`, `.creator_fee`; `Pool.protocol_fees`, `.creator_fees`) until a permissionless `sweep_protocol_fee` / `sweep_creator_fee`; `fee_recipient` in event is the zero key in that case. Buyback part still paid in-trade. LP fee goes to reserves. Fee amounts identical to older instructions. Pool vault balance now includes waiting fees, so use `effective_quote_reserves = pool_quote_token_account.amount + virtual_quote_reserves` (signed i128; can be negative). — [SWEEP_FEES.md](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/docs/instructions/SWEEP_FEES.md), [VIRTUAL_QUOTE_RESERVES_FEE_ADJUSTMENT.md](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/docs/VIRTUAL_QUOTE_RESERVES_FEE_ADJUSTMENT.md), [README](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/README.md)
- Account/rent costs: `user_volume_accumulator` 137 bytes ~0.0018444 SOL if missing (paid by user). — [TRADE_V3.md](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/docs/instructions/TRADE_V3.md)
- Other program changes Oct 2026: depth-2 pump-coin quote mints, `multi_hop_swap`, synthetic migration (last curve buy has no max size). — [README](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/README.md)

### Inferences
- Practical method for a bot: (a) compute market cap in lamports from curve/pool reserves x supply, (b) look up tier in FeeConfig, (c) cross-check with first trade's event bps.

### Gaps
- Not verified on-chain (no RPC access). Exact rounding (likely ceiling per component) not checked.

## 5. Effective round-trip cost (buy then sell, same size, flat price)

Assumptions: SOL-paired coin, fees charged on each leg at the tier's total bps (buy: fee on SOL in; sell: fee on SOL out), so fee-only round trip = 1-(1-f)^2. Tier totals follow section 2 [rows marked inferred/unverified depend on the reconstruction]. Price impact and priority/Jito tips are excluded from the fee-only column.

| Market cap (SOL) | Venue/tier | Total fee per leg | Round-trip fee only | Cost on 1 SOL | Cost on 10 SOL |
|---|---|---|---|---|---|
| <420 (any point on curve) | Bonding curve (0.95 protocol + 0.30 creator) | 1.25% | 2.48% | 0.0248 SOL | 0.248 SOL |
| 0-420 | PumpSwap tier 0 (0.93/0.02/0.30) | 1.25% | 2.48% | 0.0248 | 0.248 |
| ~1,000 | PumpSwap 420-1,470 | 1.20% | 2.39% | 0.0239 | 0.239 |
| ~2,000 | 1,470-2,460 | 1.15% | 2.29% | 0.0229 | 0.229 |
| ~3,000 | 2,460-3,440 | 1.10% | 2.19% | 0.0219 | 0.219 |
| ~12,000 | 9,820-14,730 (inferred) | 0.95% | 1.89% | 0.0189 | 0.189 |
| ~22,000 | 19,650-24,560 | 0.85% | 1.69% | 0.0169 | 0.169 |
| ~42,000 | 39,300-44,210 | 0.65% | 1.30% | 0.0130 | 0.130 |
| >98,240 | floor [UNVERIFIED] | 0.30% | 0.60% | 0.0060 | 0.060 |

Additional costs per round trip (not in the fee table):
- Price impact: roughly 2x (trade size / effective quote reserves). Illustrative only: a pool near graduation holds on the order of ~85 SOL of real quote reserve [UNVERIFIED, from general knowledge of the 85 SOL graduation threshold], so a 1 SOL trade is ~1.2% impact per leg (~2.4% round trip) and a 10 SOL trade is far worse (~10%+ per leg). Deeper pools at higher market cap shrink this. Use `effective_quote_reserves` for the exact number.
- One-time/first-trade rent: token ATA ~0.00204 SOL (refundable on close, standard Solana figure, not from these docs) and `user_volume_accumulator` ~0.0018444 SOL (per Pump docs; refundability not stated).
- Network base fee 5,000 lamports/signature plus whatever priority fee/Jito tip is used (user-set, not from sources).
- Slippage on volatile memecoins, MEV/sandwich, and the 0.015 SOL migration cost (paid by protocol/curve, not the trader; per docs, a flat cost at graduation).

### Takeaways
- At small market caps (<3,000 SOL, where most memecoin trading happens) pure fees are ~2.2-2.5% per round trip, versus ~0.6% at the floor. Fees plus price impact generally mean a coin must move >3-5% for a flip to break even at small size.
- Cashback coins (legacy) would reduce this by the creator slice; holder-reward and regular coins do not.

### Gaps
- Tiers and floor above 44,210 SOL unverified; price-impact figures are illustrative; priority-fee norms not researched here (outside scope).
