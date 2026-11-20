# Solana account model for memecoin traders and bots (as of Nov 2026)

Research limits: 4 web searches used, 2 fetches failed (solana.com and docs.raydium.io are not in the session's allowed network domains, so primary pages were only seen via search snippets). Items without a cited source are marked UNVERIFIED.

## Exact costs: ATA rent in SOL, and what changed with the rent reduction (SIMD-0437)

### Takeaway
The classic cost of opening a standard 165-byte SPL token account/ATA is 0.00203928 SOL (2,039,280 lamports), fully refundable on close. In 2026 Solana is cutting the rent-exempt minimum by 90% in five feature-gated steps (SIMD-0437), so the current deposit is lower than 0.00204 SOL; the exact present figure could not be confirmed. Check live via getMinimumBalanceForRentExemption(165).

### Cited Findings
- 165-byte SPL token account: (128 + 165) x 6,960 lamports/byte-year = 2,039,280 lamports, about 0.00203928 SOL — [CoinGecko Learn / search summary](https://www.coingecko.com/learn/what-are-solana-token-accounts)
- Solana is lowering the rent-exempt minimum by 90% over five steps under SIMD-0437 (6,960 to 696 lamports per byte); accounts funded before each step hold excess lamports — [Raydium docs](https://docs.raydium.io/solana-fundamentals/rent-and-reclaimable-rent), [Chainstack](https://docs.chainstack.com/docs/solana-rent-reduction-reclaim-excess-rent.md)
- Solana Foundation post "How to reclaim excess SOL after rent reduction" (dated Sep 3, 2026) says surplus lamports above the new minimum can be withdrawn from a token account, mint or multisig while the account stays open — [Solana Foundation](https://solana.com/news/how-to-reclaim-excess-sol-after-rent-reduction) (snippet only)
- One search result claims a token account opened today holds 0.00149 SOL; single source, treat as unverified — [Solana Foundation / aggregator summary](https://solana.com/news/how-to-reclaim-excess-sol-after-rent-reduction)
- Jupiter FAQ: rent is around 0.002 SOL and is refunded when you close the associated token account — [Jupiter FAQ](https://docs.jup.ag/user-docs/trade/swap/faq)
- Token-2022 accounts with extensions are larger, so rent is higher; Chainstack points to getMintLen for sizing. A secondary DEV Community example puts mints with default-frozen at about 0.0021 SOL and interest-bearing at about 0.0024 SOL (mint-level examples, approximate) — [Chainstack](https://docs.chainstack.com/docs/solana-token-extensions.md), [DEV](https://dev.to/gopichand_dev/i-built-5-token-extension-combinations-on-solana-this-week-heres-what-each-one-does-4ck3)

### Inferences
- If the final step reaches 696 lamports/byte, a 165-byte ATA would be (128+165) x 696 = 203,928 lamports = about 0.000204 SOL (my arithmetic, not sourced; the schedule/dates of intermediate steps are not confirmed). So long-run ATA cost for a small trade falls from about 0.002 SOL to roughly 0.0002 SOL.
- Many wallets/bots still hold ATAs funded at the old 0.00203928 level; the excess is recoverable without closing.
- Token-2022 ATAs for tokens with required extensions (e.g. ImmutableOwner is added to ATAs; TransferFee, etc. add bytes) cost more than 165-byte SPL accounts.

### Gaps
- Exact current lamports-per-byte, activation epochs for each of the five steps, and current ATA deposit: could not fetch primary pages.
- Exact Token-2022 ATA size with the default extensions: not found.

## How bots reclaim rent (closing accounts, excess withdrawal)

### Takeaway
Closing an empty token account (CloseAccount) returns the full deposit to a chosen destination; the balance must be zero (wSOL is the exception). Post-SIMD-0437 there is also an excess-lamports withdrawal path that keeps the account open. Third-party "burn dust and close" tools exist.

### Cited Findings
- Closing returns the rent deposit to a destination you choose; token balance must be zero; owner or close authority can close — [Solana docs: close account](https://solana.com/docs/tokens/basics/close-account.md)
- Wrapped SOL token accounts can be closed with a nonzero balance, which reclaims the underlying SOL — [Solana docs: close account](https://solana.com/docs/tokens/basics/close-account.md) (via search summary)
- Token-2022 accounts can return excess lamports via WithdrawExcessLamports; wSOL accounts are not supported on the excess path, so closing is the route for them — [Raydium docs](https://docs.raydium.io/solana-fundamentals/rent-and-reclaimable-rent), [Solana Foundation](https://solana.com/news/how-to-reclaim-excess-sol-after-rent-reduction)
- Raydium notes the practical constraint for bulk reclaim is transaction size, not compute — [Raydium docs](https://docs.raydium.io/solana-fundamentals/rent-and-reclaimable-rent)
- Third-party tools to burn dust and close empty accounts: Solana Compass, DexTools tutorial; a DEV post reports recovering about 18 SOL from empty accounts — [Solana Compass](https://solanacompass.com/tools/solana-token-account-rent-reclaim), [DexTools](https://www.dextools.io/tutorials/burn-empty-solana-token-accounts-to-reclaim-sol), [DEV](https://dev.to/jumpbit/how-i-recovered-18-sol-from-empty-solana-accounts-you-probably-can-too-170e)

### Inferences
- Typical bot pattern (UNVERIFIED as a source claim): sell 100% of a position, then include a CloseAccount instruction in the same transaction (or batch many closes per transaction, limited by the 1232-byte size) so the rent returns immediately. If the token amount is not fully sold or any dust remains, close fails unless the dust is burned first.
- Sweep of old pre-reduction ATAs can be done with WithdrawExcessLamports for each still-open account.

### Gaps
- Exact instruction counts per close-batch transaction not sourced.

## SPL Token vs Token-2022, and wrapped SOL handling

### Takeaway
Token-2022 accounts can carry extensions that increase size and rent and can change transfer behavior; wSOL uses the classic SPL Token program with the native mint and requires wrap (fund + syncNative) and unwrap (close). Jupiter's API automates this by default.

### Cited Findings
- Token-2022 extensions enlarge accounts; rent scales with size — [Chainstack](https://docs.chainstack.com/docs/solana-token-extensions.md)
- Jupiter's swap API has automatic wrap/unwrap of SOL (default true); manual management is described in the Solana Cookbook — [Jupiter troubleshooting](https://docs.jup.ag/docs/apis/troubleshooting)
- wSOL account can be closed with balance to get the SOL back — [Solana docs: close account](https://solana.com/docs/tokens/basics/close-account.md)

### Inferences / UNVERIFIED background
- UNVERIFIED (from general knowledge, not found in searches): wrap = create ATA for native mint (So111...112) + SystemProgram transfer + SyncNative; unwrap = CloseAccount to owner. Bots often use a temporary/ephemeral wSOL account per swap to avoid a persistent wSOL ATA, or keep a persistent wSOL ATA to save one create/close per trade.
- UNVERIFIED: Token-2022 memecoins (e.g. pump.fun-launched tokens in some cases) may use extensions such as TransferFee or transfer hooks that add accounts and compute; bots should check mint owner program before building an ATA.

### Gaps
- Searches returned nothing on syncNative/closeAccount specifics or Token-2022 share of memecoins.

## Compute units per swap, transaction size, address lookup tables

### Takeaway
A Jupiter route swap logs about 67k CU in one example; set compute limits per simulated usage. Transactions are capped at 1232 bytes, so v0 transactions with lookup tables are needed for multi-hop routes. A table holds up to 256 addresses.

### Cited Findings
- Example Jupiter log: "Program Jupiter Aggregator v6 consumed 67018 of 200000 compute units" — [Jupiter troubleshooting](https://docs.jup.ag/docs/apis/troubleshooting)
- Jupiter API offers dynamicComputeUnitLimit: true; major DEX UIs auto-set compute limits — [Jupiter swap API](https://docs.jup.ag/docs/apis/swap-api), [Bybit](https://www.bybit.com/en/wiki/article/why-solana-transactions-fail-5-fixes/)
- Transaction size cap is 1232 bytes; around 20 accounts often becomes too large in legacy format; legacy transactions hold about 35 inline addresses by another source — [Solana course](https://solana.com/developers/courses/program-optimization/lookup-tables), [Medium](https://medium.com/@shuvajitmahanta15/what-are-address-lookup-tables-and-how-to-use-them-in-your-projects-f847f8882988)
- ALTs in v0 transactions reference addresses by 1-byte index; table capacity 256 addresses; extending a table is limited to about 30 addresses per transaction; newly added addresses are usable only in a later slot — [Solana course](https://solana.com/developers/courses/program-optimization/lookup-tables), [Chainstack ALT](https://docs.chainstack.com/docs/solana-address-lookup-tables)
- Conflict: one Solana guide says ALTs allow up to 64 addresses per transaction; Chainstack says up to 256 accounts overall — [Solana guide](https://solana.com/fi/developers/guides/advanced/lookup-tables) vs [Chainstack](https://chainstack.com/solana-instructions-and-messages/)
- One Chainstack page mentions a "v1" transaction format with a 4096-byte limit and 64 inline addresses; uncorroborated — [Chainstack ALT](https://docs.chainstack.com/docs/solana-address-lookup-tables)

### Inferences
- UNVERIFIED: default per-transaction CU limit is 200k per instruction / 1.4M max per transaction; typical pump.fun/Raydium swaps are lower CU than Jupiter multi-hop routes. Only the single Jupiter 67k data point is sourced here.

### Gaps
- Per-venue CU numbers (pump.fun bonding curve, PumpSwap, Raydium, Meteora) not found. Whether v1 transactions are live in Nov 2026: unconfirmed.

## Common errors and handling; effect on small-trade EV

### Takeaway
Most failures are slippage (0x1771 / 6001), missing/unfunded accounts, and size/account-key problems; each failed landed transaction still costs the base/priority fee. Rent is refundable, so it matters for capital lock-up and for abandoned positions, not as a permanent cost.

### Cited Findings
- 0x1771 = SlippageToleranceExceeded (Jupiter error 6001): final out amount below minimum; fix with higher fixed slippage or dynamic slippage — [Jupiter troubleshooting](https://docs.jup.ag/docs/apis/troubleshooting); Solflare describes it as typically insufficient liquidity, which conflicts — [Solflare help](https://help.solflare.com/en/articles/6364536-why-is-my-swap-failing)
- Error 6008 (NotEnoughAccountKeys) is likely a modified swap transaction missing account keys — [Jupiter common errors](https://developers.jup.ag/docs/swap/common-errors)
- Rent of about 0.002 SOL is refunded when closing the ATA — [Jupiter FAQ](https://docs.jup.ag/user-docs/trade/swap/faq)

### Inferences (my arithmetic; assumptions flagged)
- Old-rent case: a 0.002 SOL deposit on a 0.05 SOL buy is 4% of capital locked until close; it is returned on close, but for tokens that rug to zero without a sale the bot must still burn/close to recover it. Unclaimed ATAs across many failed memecoin buys accumulate: 100 abandoned ATAs = about 0.2 SOL at old rent.
- Under the reduced rent (about 0.0002 SOL if the full 90% applies) the lock-up drops to about 0.4% of a 0.05 SOL buy, making rent a minor EV factor; fees and slippage dominate.
- UNVERIFIED: base fee 5,000 lamports per signature (0.000005 SOL) plus priority fee and any Jito tip; failed landed transactions still pay the fee while dropped ones do not.
- Handling pattern (general practice, UNVERIFIED): simulate before sending, pre-create ATAs idempotently (CreateIdempotent) to avoid "account already in use"/missing account errors, retry with fresh blockhash, raise slippage cautiously on thin curves, split close batches to fit 1232 bytes.

### Gaps
- No quantified failure-rate data; no sourced fee/tip numbers for Nov 2026; Token-2022-specific error cases not found.
