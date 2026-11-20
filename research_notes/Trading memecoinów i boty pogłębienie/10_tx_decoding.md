# Decoding pump.fun, PumpSwap, Raydium and Meteora transactions on Solana (as of Nov 2026)

Method note: IDLs were downloaded from raw GitHub and parsed locally (python). Discriminators were recomputed as sha256("event:<Name>")[:8] and matched the IDL for every pump/PumpSwap event. Items marked [UNVERIFIED] were not confirmed. docs.raydium.io and helius.dev were not reachable from the sandbox (only search snippets were seen).

## 1. Program IDs and IDL sources

### Takeaway
All four ecosystems are Anchor programs except Raydium AMM v4 (no official IDL). Official IDLs for pump/PumpSwap, Raydium CPMM, Meteora DLMM/DAMM v2/DBC are on raw GitHub; the pump IDLs were updated within the last weeks (Oct 2026) and carry many new fields.

### Cited Findings
- Pump (bonding curve) program: `6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P` (IDL address field, metadata version 0.1.0) — [pump.json](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/idl/pump.json)
- PumpSwap AMM program: `pAMMBay6oceH9fJKBRHGP5D4bD4sWpmSwMn52FMfXEA` — [pump_amm.json](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/idl/pump_amm.json)
- Official pump docs repo (IDLs + TS types in /idl, per-instruction docs, change announcements) — [pump-public-docs README](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/README.md)
- Raydium CPMM: `CPMMoo8L3F4NbTegBCKVNunggL7H1ZpdTHKxQB5qKP1C` (IDL v0.2.0) — [raydium_cp_swap.json](https://raw.githubusercontent.com/raydium-io/raydium-idl/master/raydium_cpmm/raydium_cp_swap.json)
- Raydium CLMM `CAMMCzo5YL8w4VFF8KVHrK22GGUsp5VTaW7grrKgrWqK`; AMM v4 `675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8` — [Moralis supported DEXs](https://docs.moralis.com/data-api/data-features/integrations/supported-dexs.md), [sol-parser-sdk program_ids](https://docs.rs/crate/sol-parser-sdk/0.5.0/source/src/grpc/program_ids.rs)
- Raydium states AMM v4 has no official Anchor IDL (hand-written layouts in SDK) — [Raydium anchor-idl doc](https://docs.raydium.io/sdk-api/anchor-idl.md) (search snippet only)
- Meteora DLMM `LBUZKhRxPF3XUpBCjp4YzTKgLccjZhTSDM9YuVaPwxo` (IDL v0.12.0) — [dlmm-sdk idl](https://raw.githubusercontent.com/MeteoraAg/dlmm-sdk/main/idls/dlmm.json)
- Meteora DAMM v2 `cpamdpZCGKUy5JxQXB4dcpGPiikHawvSWAd6mEn1sGG` (IDL v0.2.5) — [damm-v2-sdk idl](https://raw.githubusercontent.com/MeteoraAg/damm-v2-sdk/main/src/idl/cp_amm.json)
- Meteora Dynamic Bonding Curve (DBC) `dbcij3LWUppWqq96dh6gJWwBifmcGfLSB5D4DuSMaqN` (IDL v0.2.2) — [DBC SDK idl](https://raw.githubusercontent.com/MeteoraAg/dynamic-bonding-curve-sdk/main/packages/dynamic-bonding-curve/src/idl/dynamic-bonding-curve/idl.json)
- Older Meteora Dynamic AMM (not DAMM v2): `Eo7WjKq67rjJQSZxS6z3YkapzY3eMj6Xy8X5EQVn5UaB` — [search snippet via Moralis/sol-parser-sdk](https://docs.moralis.com/data-api/data-features/integrations/supported-dexs.md) [weakly sourced]

### Inferences
- Raydium CLMM IDL and Raydium AMM v4 layouts must come from raydium-io repos/SDK; my guessed raw paths for the CLMM IDL returned 404 (path unknown). 

### Gaps
- Raydium CLMM IDL raw path not found; Raydium LaunchLab program ID/IDL not checked; Raydium CPMM/CLMM swap event discriminators for CLMM not verified.
- Meteora DAMM v2/DLMM repo paths may move; the DLMM IDL path used is `idls/dlmm.json`.

## 2. Anchor event discriminators and log/CPI parsing

### Takeaway
Pump events are Anchor events: 8-byte discriminator = sha256("event:Name")[:8], followed by Borsh fields. They are emitted via self-CPI (`event_authority` PDA, seed "__event_authority") so they appear as inner instructions with a 16-byte prefix (8-byte Anchor event-CPI tag + 8-byte event discriminator), and ALSO commonly as "Program data: <base64>" log lines (the 16-byte form is not in logs, per solana-dex-parser slicing 16 bytes on instruction data). Prefer inner-instruction parsing: log lines can be truncated (10 KB log limit) and logs are absent for some providers.

### Cited Findings
- CreateEvent discriminator `1b72a94ddeeb6376` = [27,114,169,77,222,235,99,118]; TradeEvent `bddb7fd34ee661ee` = [189,219,127,211,78,230,97,238]; CompleteEvent `5f72619cd42e9808` = [95,114,97,156,212,46,152,8]; CompletePumpAmmMigrationEvent `bde95db95c94ea94` — recomputed from sha256 and matched against IDL — [pump.json](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/idl/pump.json)
- PumpSwap events (IDL discriminators, decimal): BuyEvent [103,244,82,31,44,245,119,119]; SellEvent [62,47,55,10,165,3,220,42]; CreatePoolEvent [177,49,12,210,160,118,167,116]; DepositEvent [120,248,61,83,31,142,107,144]; WithdrawEvent [22,9,133,26,160,44,71,192] — [pump_amm.json](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/idl/pump_amm.json)
- Anchor event-CPI tag sha256("anchor:event")[:8] = `1d9acb512ea545e4` (computed locally; in bytes order this is the commonly cited e445a52e51cb9a1d little-endian form [UNVERIFIED which byte order appears on-chain; check a real tx]). The `event_authority` PDA seed is bytes of `__event_authority` — [pump.json buy instruction accounts](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/idl/pump.json)
- Third-party parsers: solana-dex-parser strips 16 bytes before decoding pump events; sol-parser-sdk finds "Program data: " and reads an 8-byte discriminator — [solana-dex-parser coverage](https://unpkg.com/solana-dex-parser@2.3.2/coverage/lcov-report/src/parsers/pumpfun/parser-pumpfun-event.ts.html), [sol-parser-sdk logs/pump.rs](https://docs.rs/sol-parser-sdk/0.5.7/src/sol_parser_sdk/logs/pump.rs.html)
- Current CreateEvent fields (in order): name, symbol, uri (Borsh strings), mint, bonding_curve, user, creator, timestamp i64, virtual_token_reserves, virtual_sol_reserves, real_token_reserves, token_total_supply, token_program, is_mayhem_mode bool, is_cashback_enabled bool, quote_mint pubkey, virtual_quote_reserves u64, creator_fee_bps u64, is_holder_reward bool, depth u8 — [pump.json](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/idl/pump.json)
- Current TradeEvent fields (in order): mint, sol_amount u64, token_amount u64, is_buy bool, user, timestamp i64, virtual_sol_reserves, virtual_token_reserves, real_sol_reserves, real_token_reserves, fee_recipient, fee_basis_points, fee, creator, creator_fee_basis_points, creator_fee, track_volume bool, total_unclaimed_tokens, total_claimed_tokens, current_sol_volume, last_update_timestamp i64, ix_name string, mayhem_mode bool, cashback_fee_basis_points, cashback, buyback_fee_basis_points, buyback_fee, shareholders Vec<Shareholder>, quote_mint, quote_amount, virtual_quote_reserves, real_quote_reserves, holder_rewards_bps, holder_rewards, creator_fee_unclaimed — [pump.json](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/idl/pump.json). It now contains variable-length fields (ix_name string, shareholders vec), so fixed-offset slicing breaks.
- CompleteEvent fields: user, mint, bonding_curve, timestamp i64, quote_mint — [pump.json](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/idl/pump.json)
- CompletePumpAmmMigrationEvent: user, mint, mint_amount, sol_amount, pool_migration_fee, bonding_curve, timestamp, pool, quote_mint — same IDL.
- PumpSwap BuyEvent/SellEvent include timestamp, base/quote amounts, reserves, lp/protocol/creator fees, pool, user, ix_name (buy), cashback, buyback, virtual_quote_reserves (i128), holder_rewards, etc. CreatePoolEvent has pool, lp_mint, base_mint, quote_mint, creator, coin_creator, pool amounts — [pump_amm.json](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/idl/pump_amm.json)
- Raydium CPMM: SwapEvent [64,198,205,232,38,8,113,226] (pool_id, input/output vault before, input/output_amount, transfer fees, base_input, input_mint, output_mint, trade_fee, creator_fee, creator_fee_on_input); LpChangeEvent [121,163,205,201,57,218,117,60]; instructions swap_base_input / swap_base_output — [raydium_cp_swap.json](https://raw.githubusercontent.com/raydium-io/raydium-idl/master/raydium_cpmm/raydium_cp_swap.json)
- Meteora DLMM: Swap [81,108,227,190,205,208,10,196]; Swap2Evt [46,116,82,215,148,27,84,77] (newer; instructions swap/swap2/swap_exact_out2...); LbPairCreate [185,74,252,125,27,215,188,111] — [DLMM IDL](https://raw.githubusercontent.com/MeteoraAg/dlmm-sdk/main/idls/dlmm.json)
- Meteora DAMM v2: EvtSwap2 [189,66,51,168,38,80,117,153]; EvtInitializePool [228,50,246,85,203,66,134,37]; EvtLiquidityChange [197,171,78,127,224,211,87,13] — [DAMM v2 IDL](https://raw.githubusercontent.com/MeteoraAg/damm-v2-sdk/main/src/idl/cp_amm.json)
- Meteora DBC: EvtSwap [27,60,21,213,138,170,187,147], EvtSwap2 [189,66,51,168,38,80,117,153] (same bytes as DAMM v2 since same event name), EvtSwap3 [187,119,248,13,175,255,64,63] plus ...WithTransferHook variants, EvtInitializePool [228,50,246,85,203,66,134,37], EvtCurveComplete [229,231,86,84,156,134,75,24]; migration via migrate_meteora_damm / migration_damm_v2 — [DBC IDL](https://raw.githubusercontent.com/MeteoraAg/dynamic-bonding-curve-sdk/main/packages/dynamic-bonding-curve/src/idl/dynamic-bonding-curve/idl.json)

### Inferences
- Discriminators are not unique across programs (EvtSwap2, EvtInitializePool collide between DAMM v2 and DBC), so always key decoding on (program_id, discriminator), never discriminator alone.
- Robust pipeline: iterate inner instructions whose program_id is the target program and whose data starts with the event-CPI tag + discriminator; fall back to "Program data:" logs. Decode with Borsh from the current IDL (e.g. Anchor BorshCoder / borsh-rs), tolerate trailing bytes.
- Migration to PumpSwap: look for CompleteEvent (curve) and CompletePumpAmmMigrationEvent / CreatePoolEvent in the same tx, instruction `migrate`/`migrate_v2`.

### Gaps
- I did not verify on a real transaction whether pump events appear in both logs and inner instructions with the exact byte prefixes; verify with one live tx.
- Raydium AMM v4 swap decoding (no events; use instruction data tag 9 / 11 for swapBaseIn/Out plus token balance deltas) [UNVERIFIED from memory, not sourced here]. CLMM SwapEvent discriminator not verified.

## 3. Bonding curve and pool account layouts

### Takeaway
BondingCurve is an Anchor account (discriminator [23,183,248,55,96,216,172,96]) whose original 5xu64+bool prefix is unchanged but which now has many appended fields; PumpSwap Pool discriminator [241,154,109,4,17,177,109,188]. Read only the prefix you need; never assert a fixed size.

### Cited Findings
- Pump BondingCurve fields in order: virtual_token_reserves u64, virtual_quote_reserves u64 (formerly virtual_sol_reserves), real_token_reserves u64, real_quote_reserves u64 (formerly real_sol_reserves), token_total_supply u64, complete bool, creator pubkey, is_mayhem_mode bool, is_cashback_coin bool, quote_mint pubkey, creator_fee_bps u64, can_edit_creator_fee bool, is_holder_reward bool, creator_fee u64, protocol_fees u64, depth u8, initial_virtual_quote_reserves u64, post_complete_base_out u64, post_complete_quote_in u64 — [pump.json](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/idl/pump.json); renames and quote_mint default (Pubkey::default for SOL-paired coins) — [pump-public-docs README](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/README.md)
- Global account (discriminator [167,232,232,177,200,108,114,127]) has initial reserves, fee_basis_points, fee_recipients[7], reserved_fee_recipients[7], buyback_fee_recipients[8], etc. — [pump.json](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/idl/pump.json)
- PumpSwap Pool: pool_bump u8, index u16, creator, base_mint, quote_mint, lp_mint, pool_base_token_account, pool_quote_token_account, lp_supply u64, coin_creator, is_mayhem_mode, is_cashback_coin, virtual_quote_reserves i128, creator_fee_bps, can_edit_creator_fee, is_holder_reward, protocol_fees, creator_fees — [pump_amm.json](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/idl/pump_amm.json)
- Price quoting for pools: effective_quote_reserves = pool_quote_token_account.amount + Pool.virtual_quote_reserves; the latter can be negative since Sept 30 (signed i128) — [README](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/README.md)
- Bonding curve PDA derivation (seed "bonding-curve" + mint) [UNVERIFIED here; standard knowledge, confirm in IDL pda seeds].
- Curve completion: `complete` = true; token price = virtual_quote_reserves / virtual_token_reserves (adjust decimals: tokens 6, SOL 9) [inference from constant-product design].

### Inferences
- Because of the quote_mint field, a "SOL" curve has quote_mint = default pubkey; handle non-SOL quotes (USDC / pump coins, depth up to 2) when computing USD or SOL prices.

### Gaps
- Exact current account byte size not computed; not needed if decoding via IDL.

## 4. SDKs, parsers and parsed-tx APIs

### Takeaway
Official: @pump-fun/pump-sdk 4.1.0, @pump-fun/pump-swap-sdk 2.1.0, Rust pump-rust-client 0.4.1. For generic decoding: solana-dex-parser (TS, covers Jupiter/Raydium/Meteora/Pumpfun), sol-parser-sdk (Rust), Shyft's TS transaction parser (IDL-driven). Helius Enhanced Transactions is legacy; Parsed Events is the replacement.

### Cited Findings
- Official SDKs: `@pump-fun/pump-sdk` 4.1.0, `@pump-fun/pump-swap-sdk` 2.1.0, `pump-rust-client` 0.4.1 (both programs) — [pump-public-docs README](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/README.md). Older pump-swap-sdk 1.15.0 shown on npm search result — [npm](https://npmjs.com/package/@pump-fun/pump-swap-sdk). Beware look-alike packages (@nirholas/*, third-party crates).
- solana-dex-parser (npm) supports Jupiter, Raydium, Meteora, PumpFun, BoopFun, Moonshot — [npm](https://www.npmjs.com/package/solana-dex-parser)
- sol-parser-sdk (Rust crate, versions up to 0.5.7) parses pump logs and instructions and has program_ids for Raydium/Meteora — [docs.rs](https://docs.rs/crate/sol-parser-sdk/0.5.7)
- Shyft: TS package @shyft-to/solana-transaction-parser, register IDL per program, parse instructions plus inner instructions; docs for pump AMM, pumpfun, Raydium via Yellowstone gRPC; GraphQL for parsed PumpSwap pools — [Shyft Pump AMM parsing](https://docs.shyft.to/solana-yellowstone-grpc/examples/pump-amm/solana-grpc-pump-amm-transaction-parsing), [Shyft blog](https://shyft.to/blog/how-to-stream-and-parse-pumpswap-transactions-on-solana)
- Helius: Enhanced Transactions API (POST /v0/transactions) is legacy/maintenance mode; its FAQ says not to rely on it for non-NFT/SPL parsing. Parsed Events API (POST /v1/parsed-events/transactions) is the successor, IDL-catalog based, free in open beta until 21 Sep 2026 [that date has now passed; current pricing UNVERIFIED] — [Helius enhanced tx docs](https://www.helius.dev/docs/enhanced-transactions), [Helius parsed events](https://www.helius.dev/docs/parsed-events/quickstart.md) (snippets only)
- Python: no dedicated, verified pump/PumpSwap decoder found; anchorpy/solders with the raw IDL is the likely route [inference, UNVERIFIED].

### Inferences
- For a bot, own decoding from the official IDL (Borsh) gives full control and no vendor lag; use Helius/Shyft as cross-checks or for backfill.

### Gaps
- No Python library verified; Shyft's REST parsed-tx output schema not reviewed; Helius pricing after beta not found.

## 5. Pitfalls on program upgrades

### Takeaway
Pump programs change often (new instruction variants, appended event fields, renamed fields, new quote mints). Decoders pinned to an old IDL silently mis-parse.

### Cited Findings
- Recent changes (Sept-Oct 2026): negative virtual_quote_reserves (Sept 30), depth-2 pump-coin quotes (Oct 13), holder-rewards coins (new fields in CreateEvent/TradeEvent/BuyEvent/SellEvent, cashback deprecated), PumpSwap virtual_quote_reserves appended to Pool and events, v3 trade instructions (buy_v3/sell_v3/buy_exact_quote_in_v3; PumpSwap buy_v2/sell_v2), multi_hop_swap, fees kept on curve (sweep_protocol_fee/sweep_creator_fee), synthetic-migration last buy — [README](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/README.md)
- Legacy instructions (buy, sell, buy_exact_sol_in, create) keep working alongside v2/v3, so a decoder must recognize all instruction discriminators: e.g. buy [102,6,61,18,1,218,235,234], sell [51,230,133,164,1,127,131,173], create [24,30,200,40,5,28,7,119], create_v2 [214,144,76,236,95,139,49,180], buy_v2 [184,23,238,97,103,197,211,61], sell_v2 [93,246,130,60,231,233,64,178], buy_v3 [7,5,29,196,245,23,101,80], sell_v3 [28,146,222,119,38,196,105,213], migrate [155,234,231,146,236,158,162,30], migrate_v2 [187,203,18,31,206,237,254,41], multi_hop_curve_swap [225,154,117,22,215,86,246,103] — [pump.json](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/idl/pump.json)
- Account lists differ by instruction/coin type (legacy needed optional accounts; v2 unified order), so account-index-based decoding must use the right IDL per discriminator — [README](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/README.md)
- Meteora has parallel generations (DLMM Swap vs Swap2Evt; DBC EvtSwap / EvtSwap2 / EvtSwap3 and TransferHook variants) — IDLs above.

### Inferences
- Pitfalls: (1) old Borsh struct then reading trailing new fields as wrong data or short-read errors; mitigate by decoding with latest IDL and treating Borsh as prefix-compatible only when fields are appended; (2) renamed fields (virtual_sol -> virtual_quote) when using generated types; (3) trades via multi_hop_swap or aggregators (Jupiter) produce nested CPI, with events in inner instructions only; (4) amounts: sol_amount in TradeEvent excludes or includes fees depending on version (check fee fields); (5) pin IDL version, diff upstream pump-public-docs regularly, alert on unknown discriminators and unexpected event length; (6) fee-on-curve means fee transfers no longer appear per trade, so reconcile balances with sweeps.
- Watch IDL changes with an upgrade-authority/ProgramData slot check [UNVERIFIED approach].

### Gaps
- Exact dates of each upgrade deployment and whether IDL on-chain (anchor idl fetch) is kept in sync were not verified.
