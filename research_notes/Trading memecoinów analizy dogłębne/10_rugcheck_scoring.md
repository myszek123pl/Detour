# RugCheck.xyz scoring vs GoPlus Solana vs Birdeye security — merged checklist

Research limits: 6 web searches done; all WebFetch calls failed (docs.birdeye.so, docs.solanatracker.io, docs.gopluslabs.io, fluxbeam.gitbook.io not resolvable from this session's network allowlist). No primary docs (RugCheck Swagger, GoPlus docs, Birdeye glossary) were read. Everything below is from search snippets/third-party summaries unless marked [BACKGROUND-UNVERIFIED] (my prior knowledge, not confirmed this session). Re-run with those hosts allowed to verify.

## 1. RugCheck: risk checks, weights, score semantics

### Takeaway
RugCheck returns a list of risk entries (name, description, level, raw points) plus a score; exact official weights were NOT found. Only a few point values are visible via Solana Tracker's docs, which mirror the RugCheck-style schema. Treat all weights as unverified.

### Cited Findings
- Report endpoint is GET /v1/tokens/{mint}/report (optional refresh param) on api.rugcheck.xyz; lighter /v1/tokens/{mint}/report/summary returns score + risk list — [Syra docs](https://www.mintlify.com/ikhwanhsn/syra_agent/api/token-report), [oanor llms.txt](https://oanor.com/api/rugcheck-api/llms.txt) (third-party wrappers, not official).
- Each risk entry has name, description, level (e.g. "danger"), score (points). Sample: "Top 10 Holders" level danger, score 5000 — [Solana Tracker risk docs](https://docs.solanatracker.io/public-data-api/risk).
- Solana Tracker's (RugCheck-derived) sample weights: "Freeze Authority Enabled" 7500; Top 10 holders >15% = 5000; single holder >10% = 2000 — [Solana Tracker risk docs](https://docs.solanatracker.io/public-data-api/risk). Their docs are inconsistent on the normalized scale (1–10 vs 0–10), so these are NOT confirmed RugCheck values.
- Normalized score reported as 0–100 by wrappers; higher = more red flags (one source); raw score is separate and unbounded — [ClawHub rugcheck skill](https://clawhub.ai/rugcheck), search summary of [Syra docs](https://www.mintlify.com/ikhwanhsn/syra_agent/api/token-report). Note the direction (higher=worse) is contested by general UI lore; verify with a live call.
- Mint authority: no numeric weight found; only that active mint authority allows extra supply — [Solana Tracker](https://docs.solanatracker.io/public-data-api/risk).
- LP lock: RugCheck reads on-chain locker contracts, shows locked USD amount, unlock timestamp, locker program; no/near-expiry locks add risk, no points published — [Solana Compass](https://solanacompass.com/projects/rugcheck), [RugCheck mirror article](https://mirror.xyz/0xF362eaCAf0a28651d6f6218e5fD0Faf360fa779F/yPq27VSoIl4nOBhjXGVt6h8NYw9iXWAOXEp7NBJvSxc).
- Creator history: "rugging" risk flags a creator with prior scam/rugged tokens — [RugCheck mirror article](https://mirror.xyz/0xF362eaCAf0a28651d6f6218e5fD0Faf360fa779F/yPq27VSoIl4nOBhjXGVt6h8NYw9iXWAOXEp7NBJvSxc).
- Insider Networks: beta feature linking top holders via suspicious wallet connections to expose coordinated insider rings — same mirror article / [Dextools tutorial](https://www.dextools.io/tutorials/how-to-use-rugcheck-solana-token-risk-tutorial-2026).
- Auth: one skill page claims no API key needed for read endpoints — [ClawHub](https://clawhub.ai/rugcheck) (unconfirmed).

### Inferences
- Because raw points per risk are additive and large (thousands), a single freeze-authority or top-10 flag likely dominates the score; do not rely on the normalized number, consume individual risk names + levels instead.
- Token-2022 extension checks (transfer fee, permanent delegate, etc.) probably exist as risk entries but I found no source confirming names or weights.

### Gaps
- Official full list of risk names and weights; Token-2022 extension handling; Insider Networks scoring impact; whether LP-locked % thresholds are 0/50/90 etc. Not found (primary docs unreachable).
- [BACKGROUND-UNVERIFIED] Commonly seen RugCheck risk names: "Mint Authority still enabled", "Freeze Authority still enabled", "Low Liquidity", "Low amount of LP Providers", "Large Amount of LP Unlocked", "Top 10 holders high ownership", "Single holder ownership", "Creator history of rugged tokens", "Mutable metadata", "Copycat token", "High holder correlation", "Transfer fee" (Token-2022), "Insider/linked wallets detected".

## 2. API endpoints and rate limits (RugCheck)

### Takeaway
Endpoints known (via wrappers); rate limits not found.

### Cited Findings
- /v1/tokens/{mint}/report and /report/summary on api.rugcheck.xyz — see sources above.
- FluxRPC docs state a Swagger reference exists for the RugCheck API — [FluxRPC](https://fluxbeam.gitbook.io/fluxrpc-docs/rugcheck-api/introduction) (seen only in search summary).

### Gaps
- Rate limits (free vs key), any paid tier, /v1/stats/new_tokens, /v1/tokens/{mint}/lp-lockers etc. endpoints: unverified. [BACKGROUND-UNVERIFIED] other endpoints exist (e.g. new/trending/recent token lists, insider graph); do not hard-code limits — implement caching + 429 backoff and check Swagger.

## 3. Known false positives / negatives

### Takeaway
Heuristic on-chain-only scoring: flags legit new tokens, misses socially engineered or fake-lock rugs.

### Cited Findings
- New legit tokens with few holders/low liquidity are flagged risky (false positive) — [search-summarized review via smithii/dextools list](https://smithii.io/en/top-3-solana-rug-pull-detection-tools/).
- RugCheck evaluates on-chain structure only; cannot assess team, audits, off-chain promises — same summaries; [Solana Tracker token-safety guide](https://docs.solanatracker.io/guides/token-safety).
- "Locked" LP can mislead: locker controlled by dev, or only partial LP locked, is effectively no lock; compute locked LP / total LP — [Dextools fake lock guide](https://www.dextools.io/tutorials/fake-liquidity-lock-verify-real-lock).
- Solana Tracker warns not to rely on the score alone — [Solana Tracker](https://www.solanatracker.io/resources/check-solana-token-rug-risk-api).

### Inferences
- False negatives likely: bundled/insider sniping across many fresh wallets (beta insider detection incomplete), slow rugs via dev sell-down with renounced authorities, pump.fun/bonding-curve tokens where LP "lock" is structural and not meaningful, fake-burned LP.
- False positives likely: pump.fun-launched tokens early (high top-holder % because bonding-curve account holds supply; check whether bonding curve/pool accounts are excluded), tokens with mutable metadata, tokens using legitimate Token-2022 transfer fees.

### Gaps
- No quantified FP/FN rates found anywhere.

## 4. GoPlus Solana token security API

### Takeaway
Beta endpoint covering SPL and SPL-2022; field list not verified.

### Cited Findings
- Solana support announced for SPL and SPL-2022, covering basic info, contract security/permissions, DEX info — [ChainCatcher](https://chaincatcher.com/en/article/2143873).
- Categories: honeypot, hidden mint, trading restrictions, ownership concentration — [Quicknode listing](https://www.quicknode.com/builders-guide/tools/goplus-security-by-goplus-labs) (third-party summary).
- Aggregator access via Mobula using solana:solana identifier — [Mobula docs](https://docs.mobula.io/rest-api-reference/endpoint/token-security-get.md).
- GoPlus uses 0–1 scale for percentages (EVM tax fields) — [Dedaub](https://docs.dedaub.com/docs/token_safety/tokin/); applicability to Solana unverified.

### Gaps
- Exact response fields, rate limits, auth model. [BACKGROUND-UNVERIFIED] fields recalled: mintable, freezable, closable, balance_mutable_authority, default_account_state, non_transferable, transfer_fee, transfer_hook, metadata_mutable, trusted_token, holders, dex lp info, creators, total_supply, with {status, authority} sub-objects. Many values are strings ("0"/"1"). Treat as hints only.

## 5. Birdeye security fields

### Takeaway
GET public-api.birdeye.so/defi/token_security with address, X-API-KEY, x-chain: solana; plans Starter+.

### Cited Findings
- Endpoint and headers — [Birdeye reference](https://docs.birdeye.so/reference/get_defi-token-security); available on Starter/Premium/Business/Enterprise — [Birdeye packages](https://docs.birdeye.so/reference/data-accessibility-by-packages).
- Glossary: camelCase in v1/v2, snake_case v3+; confirmed fields only ownerAddress, creatorAddress — [Birdeye glossary](https://docs.birdeye.so/docs/security-data).
- Wrapper skills describe ownership, mintability, freezable, top-holder concentration, mutable metadata — [skills.sh birdeye](https://skills.sh/sendaifun/skills/birdeye) (secondhand).

### Gaps
- Full field list and rate limits (per-plan rps) unverified. [BACKGROUND-UNVERIFIED] fields: creatorOwnerAddress, creatorPercentage, top10HolderPercent, top10UserPercent, freezeable, freezeAuthority, mintable?, mutableMetadata, transferFeeEnable, transferFeeData, isToken2022, nonTransferable, lockInfo, preMarketHolder.

## 6. Merged checklist with suggested thresholds

### Takeaway
Thresholds below are MY synthesized suggestions (not from any source) except where a source number is cited; calibrate on your own backtests.

### Cited Findings
- Source-derived anchors: single holder >10% and top-10 >15% are flagged by RugCheck-style systems (note 15% is very strict for memecoins) — [Solana Tracker](https://docs.solanatracker.io/public-data-api/risk). LP lock % should be locked/total LP — [Dextools](https://www.dextools.io/tutorials/fake-liquidity-lock-verify-real-lock).

### Inferences (suggested, unvalidated)
| Check | Source(s) | Hard reject | Warn |
|---|---|---|---|
| Mint authority | RugCheck, GoPlus mintable, Birdeye | enabled | n/a |
| Freeze authority | all three | enabled (unless known stablecoin) | n/a |
| Token-2022 extensions | GoPlus, Birdeye, RugCheck(?) | permanent delegate, non-transferable, transfer hook (unknown program), default-frozen state | transfer fee >0 (reject >5%) |
| LP locked/burned % (of total LP) | RugCheck | <50% | <90% or unlock <30 days |
| Locker identity | RugCheck | dev-controlled locker | unknown locker |
| Liquidity (USD) | RugCheck/Birdeye | <$5k | <$25k |
| Top-1 holder (excl. pool/bonding curve/burn) | all | >20% | >10% |
| Top-10 holders (same exclusions) | all | >50% | >30% |
| Creator history | RugCheck | any prior rug | creator holds >5% |
| Creator balance/sell-down | Birdeye creatorPercentage | n/a | >10% or dumping |
| Insider network / bundled wallets | RugCheck beta | >25% supply linked | >10% |
| Metadata mutable | all | n/a | warn only |
| RugCheck normalized score | RugCheck | any "danger" level risk | score in top ~third (calibrate) |
| Token age | n/a | <5 min w/o checks | <1 h |
| Cross-source disagreement | all | any source reports honeypot/non-sellable | fields differ -> re-query |

Operational notes (inferences): require 2-of-3 agreement for pass but 1-of-3 for reject on critical flags (authorities, Token-2022 dangerous extensions); re-check authorities and LP lock just before entry and periodically (authorities can't be re-enabled once revoked, but LP unlock/dev sells can change); simulate a sell (Jupiter quote/tx simulation) as an independent honeypot test; cache with short TTL and handle 429.

### Gaps
- No empirical backtest; thresholds need tuning against your own trade data.
