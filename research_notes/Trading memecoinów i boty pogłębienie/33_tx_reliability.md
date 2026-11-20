# Solana transaction reliability for bots (as of Nov 2026)

## 1. Preflight/simulateTransaction, blockhash expiry, maxRetries and rebroadcast

### Takeaway
RPC nodes rebroadcast to leaders about every 2s until the blockhash expires (~150 blocks). Bots should usually set maxRetries=0 and run their own rebroadcast loop. Never re-sign before confirming the old blockhash has expired (lastValidBlockHeight passed).

### Cited Findings
- Default RPC behavior: forwards the tx to leaders every ~2s until finalized or blockhash expires (~150 blocks); with no retry parameter the node keeps retrying. — [Solana retry guide](https://solana.com/developers/guides/advanced/retry)
- Before re-signing a tx you must confirm the original blockhash has expired; typical pattern is storing lastValidBlockHeight from getLatestBlockhash and polling block height against it. — [Solana retry guide](https://solana.com/developers/guides/advanced/retry)
- maxRetries overrides the node's default retry logic; in congestion the docs suggest maxRetries=0 plus a custom rebroadcast algorithm (exponential backoff or constant interval until timeout). — [Solana retry guide](https://solana.com/developers/guides/advanced/retry), [cookbook](https://solana.com/developers/cookbook/transactions/retry.md)
- skipPreflight defaults to false; preflightCommitment sets the simulation commitment (guide snippet says default "finalized"; note: unverified against current RPC docs, older docs said "finalized", some clients default to "confirmed"). — [Solana retry guide](https://solana.com/developers/guides/advanced/retry)
- sendTransaction success only means the node accepted the tx; poll getSignatureStatuses with the signature for outcome. — [Solana retry guide](https://solana.com/developers/guides/advanced/retry)

### Inferences
- For sniping/latency-sensitive bots, skipPreflight=true saves a round trip but loses early error visibility; compensate by running simulateTransaction separately for sizing/CU estimate, and by reading logs from getTransaction on failure.
- Fee-paying failures: a tx that lands but fails still costs fee (see Q3), so rebroadcast the SAME signed tx (idempotent by signature) rather than building new ones within the same blockhash window.

### Gaps
- Not verified this session: exact current preflightCommitment default; ~150-slot window numbers post-Alpenglow (slot/blockhash expiry semantics under Alpenglow not confirmed); durable nonce details (below, from general knowledge only).
- Durable nonces (unverified, background knowledge, no source fetched): nonce account holds a stored blockhash; tx's first instruction must be AdvanceNonceAccount; tx stays valid until the nonce is advanced, removing 150-block expiry; costs extra ~rent-exempt account and one more instruction; poor fit for fast memecoin swaps (needs a fresh nonce per concurrent tx) but useful for pre-signed/offline signing. Verify in Solana docs before relying.

## 2. Confirmation levels and Alpenglow

### Takeaway
Alpenglow is reported live on mainnet since epoch 1064 (21 Oct 2026, Agave 4.3), with ~150ms target finality; Rotor (replacing Turbine) is a later phase. Exact effects on processed/confirmed/finalized semantics in the RPC API were not verified.

### Cited Findings
- Official Solana page (updated Oct 2026) states Alpenglow activated at the start of epoch 1064 on Oct 21, 2026 ~13:36 UTC, shipped in Agave 4.3; target finality ~150ms vs 12.8s before; other sources give 100-150ms. — [Solana Alpenglow page](https://solana.com/upgrades/alpenglow)
- Rotor is "Phase 2, later" and not part of the live Votor rollout. — [Solana Alpenglow page](https://solana.com/upgrades/alpenglow)
- Older snapshots (incl. Alchemy April 2026) describe mainnet as upcoming; outdated. — [Alchemy](https://www.alchemy.com/zh-Hans/blog/solana-alpenglow)
- Search tool summary only; I could not fetch solana.com directly (host blocked in session), so details above come from search-result summaries.

### Inferences
- Faster finality should shrink the gap between confirmed and finalized, so bots can more plausibly wait for finalized on size-critical steps; still keep confirmed as default for trading loops. Unverified.

### Gaps
- Whether Alpenglow changed commitment names/semantics (e.g., fast-finalization vs slow-finalization paths), blockhash validity in slots/time, vote tx handling, or RPC fields: not found.
- Standard definitions (processed = seen by node, confirmed = supermajority vote on optimistic block, finalized = max lockout) are background knowledge, unverified here.

## 3. pump.fun / PumpSwap error codes and handling

### Takeaway
Slippage failures map to Anchor custom errors: pump bonding curve 6002 TooMuchSolRequired (buy) / 6003 TooLittleSolReceived (sell) / 6042 BuySlippageBelowMinTokensOut; PumpSwap (pump_amm) 6004 ExceededSlippage / 6040 BuySlippageBelowMinBaseAmountOut. A failed tx is rolled back but the network fee is still charged.

### Cited Findings
- pump program IDL errors: 6000 NotAuthorized; 6002 TooMuchSolRequired "slippage: Too much SOL required to buy the given amount of tokens."; 6003 TooLittleSolReceived "slippage: Too little SOL received to sell..."; 6005 BondingCurveComplete ("curve completed and liquidity migrated"); 6006 BondingCurveNotComplete; 6020 BuyZeroAmount; 6021 NotEnoughTokensToBuy; 6022 SellZeroAmount; 6023 NotEnoughTokensToSell; 6024 Overflow; 6026 DivisionByZero; 6027 NotEnoughRemainingAccounts; 6042 BuySlippageBelowMinTokensOut; 6108 MultiHopMayhemCurveNotSupported; 6109 QuoteChainAccountsRequired. — [pump IDL](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/idl/pump.json)
- Newer buy variants use min_tokens_out (buy_exact_sol_in, buy_exact_quote_in_v2/v3) vs max_sol_cost (buy, buy_v2, buy_v3). — [pump IDL](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/idl/pump.json)
- An IDL message hints "retry once migrate_v2 creates its pool" for a curve complete-but-not-migrated state (name/code not captured). — [pump IDL](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/idl/pump.json)
- PumpSwap (pump_amm) IDL: 6001 ZeroBaseAmount; 6002 ZeroQuoteAmount; 6003 TooLittlePoolTokenLiquidity; 6004 ExceededSlippage; 6016 BuyMoreBaseAmountThanPoolReserves; 6040 BuySlippageBelowMinBaseAmountOut ("buy: slippage - would buy less tokens than expected min_base_amount_out"); 6063 InsufficientRealQuoteReserves. — [pump_amm IDL](https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/idl/pump_amm.json)
- Numbering is program-specific: 6002 is ExceededSlippage in Meteora DAMM v2/DBC but TooMuchSolRequired in pump; don't map codes across programs. — [Meteora DAMM v2 errors](https://docs.meteora.ag/developer-guides/damm-v2/program/errors.md)
- A failed pump.fun buy reverts but the fee is still charged. — [BloFin Academy](https://blofin.com/academy/education/pumpfun/why-pump-fun-trades-fail) (secondary source)

### Inferences
- Handling: parse InstructionError Custom(code) per program id. Slippage codes (6002/6003/6042 pump; 6004/6040 amm): re-quote from fresh reserves and retry with fresh blockhash and adjusted limit (or abort if price moved beyond edge); don't blindly raise slippage (sandwich exposure). 6005 on pump: switch route to PumpSwap pool. 6016/6063: reduce size. Account/remaining-accounts errors (6027, 6109) mean stale IDL/account set: refresh IDL.
- Also expect generic errors (BlockhashNotFound, AccountNotFound for ATA, compute budget exceeded, insufficient lamports) — not sourced this session.

### Gaps
- Full pump_amm error list beyond the fetched entries (fetch was via summarizer, partial); IDLs can change, re-pull before use.
- Whether failed-tx fee refunds or Jito bundles (revert-protected) affect cost: not researched.
