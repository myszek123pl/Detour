# Rug pulls, honeypots and memecoin scam mechanics: pre-buy checks for a bot (Solana + EVM)

> Research conditions (read first): this session could only use web *search* snippets. Every WebFetch to a primary source failed with a network block (docs.gopluslabs.io, arxiv.org, soliduslabs.com, spl.solana.com and docs.honeypot.is are not on the session's allowed hosts). The shared web-search budget also ran out after about 10 queries. So:
> - Cited findings come from search-result summaries of the linked pages. They have not been checked against the full primary documents.
> - Mechanism descriptions that come from general domain knowledge, and that I could not verify against a fetched source this session, appear **only** under "Inferences" and are marked *(domain knowledge, unverified this session)*.
> - Before relying on any field name or threshold in code, re-check it against the live API docs.

## Q1. Solana scam vectors: mint authority, freeze authority, Token-2022 extensions, LP pull, metadata mutability, dev dump

### Takeaway
On Solana, a classic EVM-style "honeypot" mostly shows up as **authorities that are still live**. A live freeze authority can lock a buyer's account and a live mint authority can inflate supply. Token-2022 adds more traps: a **permanent delegate** can burn or move tokens out of any holder's account (seen in live scams, with burns within seconds of a buy), a **transfer hook** can make sells fail, and **transfer fees** and **default-frozen accounts** are further risks. Revoking mint and freeze authority is therefore *not* enough for a Token-2022 mint. Unlocked or unburned LP and concentrated insider or bundled supply are the main rug and dump vectors.

### Cited Findings
- **Freeze authority = Solana's honeypot.** Birdeye's rug-check guide says Solana has no honeypot flag as such. The equivalent danger is a live freeze authority: an issuer who can freeze tokens can lock your position after you buy. — [Birdeye: How to Build a Powerful Rug Checker (Solana and EVM)](https://birdeye.so/data-api/blog/detail/rug-checker-api-solana-evm-birdeye-data); [Birdeye Rug Checker docs](https://data.birdeye.so/docs/use-cases/risk-and-integrity/rug-checker)
- **Revoked mint and freeze authority can be misleading on Token-2022.** Both can read as revoked while a Token-2022 extension still gives the issuer equivalent control. A permanent delegate can move tokens out of any holder's account. — [Meme Central: Mint Authority and Freeze Authority on Solana Explained](https://memecentral.fun/guides/mint-authority-and-freeze-authority-on-solana)
- **The permanent delegate is set at mint level and holders cannot revoke it** on their own token accounts. — [Soltidy: Token-2022 explained for traders](https://soltidy.com/blog/token-2022-explained-for-traders)
- **Permanent-delegate burn scams are live.** In one reported case, a token called "RED" was burned from the buyer's wallet **7 seconds after the swap**. — [Coinpaper: Scammers Exploit Solana Token Feature to Burn Users' Crypto](https://coinpaper.com/5295/scammers-exploit-solana-token-feature-to-burn-users-crypto)
- A 2026 write-up describes permanent-delegate burns within about a minute of purchase as an organized, automated "rug pull factory", not a protocol bug, and proposes a detection pipeline. — [DEV Community: Solana's Permanent Delegate Burn Scam (2026)](https://dev.to/ohmygod/solanas-permanent-delegate-burn-scam-how-token-2022-extensions-power-2026s-largest-automated-rug-4579)
- **Transfer hook as a honeypot.** A transfer hook is a custom program that runs on every transfer, so it can let buys succeed while sells fail. — [DEV Community (same article)](https://dev.to/ohmygod/solanas-permanent-delegate-burn-scam-how-token-2022-extensions-power-2026s-largest-automated-rug-4579)
- **The permanent delegate also has legitimate uses**, for example stablecoin and payments issuers using it for compliance and seizure. Its presence is a risk signal, not proof of a scam. — [Spark: Solana Token Extensions, Programmable Compliance](https://www.spark.money/research/solana-token-extensions-payments)
- RugCheck flags tokens with a permanent delegate, and Jupiter shows warnings when users try to trade them. Scanner checks cover "Token-2022 traps": permanent delegate, transfer hooks and default-frozen state. — [Blofin Academy: Solana Memecoin Rug Pull Safety (2026)](https://blofin.com/en/academy/education/solana/solana-memecoin-rug-pull-safety); [Soltidy](https://soltidy.com/blog/token-2022-explained-for-traders)
- **Scanner flags are not complete.** A token can pass a scanner and still be a honeypot through freeze authority or Token-2022 transfer fees, still have dev-held liquidity, and still hide a bundled insider supply. — [Blofin Academy](https://blofin.com/en/academy/education/solana/solana-memecoin-rug-pull-safety)
- **Mutable metadata** means the creator can change the token's name or image, which enables bait-and-switch and impersonation. RugCheck reports it as the risk item "Mutable metadata". — [Termo RugCheck skill](https://termo.ai/skills/rugcheck); [GitHub antaresscan/antares-extension PR #766](https://github.com/antaresscan/antares-extension/pull/766)
- **LP pull.** RugCheck exposes `lpLockedPct`. One integration treats `lpLockedPct == 0` as "creator can pull liquidity anytime". Another counts `>= 90` as locked. These thresholds are integrator choices, not official rules. — [Termo](https://termo.ai/skills/rugcheck); [antares-extension PR #766](https://github.com/antaresscan/antares-extension/pull/766)
- **Soft rugs (dev dumps) dominate on Raydium.** Solidus Labs found that 93% of Raydium liquidity pools (361,000 pools) showed soft-rug-pull characteristics. The median rug was about $2,832 and the largest detected was $1.9M. — [DeepStrike: rug pull statistics (summarizing Solidus)](https://deepstrike.io/blog/rug-pull-statistics); [CoinDesk](https://hotfix.coindesk.com/business/2025/05/07/98-of-tokens-on-pump-fun-have-been-rug-pulls-or-an-act-of-fraud-new-report-says)
- **Holder-concentration data.** Birdeye's `token_security` returns `top10HolderPercent` and `creatorPercentage`. One Birdeye guide treats a top-10 share above 0.30 as too concentrated. The units are ambiguous between a fraction and a percent. — [Birdeye Rug Checker blog](https://birdeye.so/data-api/blog/detail/rug-checker-api-solana-evm-birdeye-data); [birdeye-go package](https://pkg.go.dev/github.com/Laminar-Bot/birdeye-go)

### Inferences
*(Everything below is domain knowledge, unverified this session against spl.solana.com, which was blocked. Verify it against the SPL Token-2022 docs before coding.)*
- **Solana pre-buy checks, mint level** (read the mint account directly via RPC `getAccountInfo` / `getParsedAccountInfo`. Do not depend only on third-party APIs):
  1. `mintAuthority == null`. If it is non-null, the issuer can mint unlimited supply. Hard reject, unless whitelisted.
  2. `freezeAuthority == null`. If it is non-null, the issuer can freeze your ATA, which is effectively a honeypot. Hard reject.
  3. Program owner: SPL Token (`Tokenkeg...`) or Token-2022 (`TokenzQd...`). If Token-2022, parse **all** extensions from the TLV data:
     - `PermanentDelegate` present → hard reject.
     - `TransferHook` with a non-null program ID → hard reject, or simulate a sell and whitelist known hook programs only.
     - `TransferFeeConfig` → read the current *and* the newer scheduled `transferFeeBasisPoints` and `maximumFee`. Fees can be changed by the `transferFeeConfigAuthority` and take effect after an epoch delay. Reject if the fee is above your tolerance or the fee authority is not null.
     - `DefaultAccountState = Frozen` → new holder accounts start frozen. Reject.
     - `NonTransferable` → the token cannot be transferred or sold. Reject.
     - `MintCloseAuthority`, `Pausable` (newer extension), `ConfidentialTransfer` (balances hidden, so holder analysis breaks), `InterestBearing` / `ScaledUiAmount` (displayed balance differs from raw amount, so UI price can mislead). Treat each as a risk flag. Reject on `Pausable` with a live authority.
     - `MetadataPointer` / `TokenMetadata` with a live update authority → mutable metadata.
  4. Metaplex metadata: `isMutable == false` and `updateAuthority` checked. Mutable metadata is a soft flag, not a hard reject; it is common even on legitimate tokens.
- **Liquidity checks:** identify the pool or pools (pump.fun bonding curve before migration; PumpSwap / Raydium / Meteora after). Check that LP tokens are burned (sent to the incinerator), locked in a known locker, or that the pool type has no withdrawable LP for the creator. Check liquidity depth versus your intended size, and check that the quote asset is SOL or USDC, not a fake.
- **Supply distribution and dev dump:** the top-N holder share excluding pool and burn addresses, the creator's balance, and **bundle detection** (several wallets that bought in the same slot or block as creation, or that were funded from the same source). Snipers and bundlers that hold a large share are the main mechanism behind soft rugs.
- **Creator history:** the number of previous tokens deployed by the same creator or funding wallet, and how they ended. Serial deployers correlate with the "rug factory" pattern above.

### Gaps
- I could not fetch the official SPL Token-2022 extension list (spl.solana.com was blocked). The exact extension names, the `Pausable` extension's status and the fee-change delay semantics are unverified here.
- No quantitative data was found on what share of Solana memecoins use Token-2022 extensions maliciously.
- I found no primary source giving thresholds for "bundled supply" that is dangerous.

## Q2. EVM scam vectors: honeypots, sell taxes, blacklist, max tx/wallet, proxy upgradeability, ownership renounce, hidden mint

### Takeaway
EVM scam tokens hide their traps in contract code. Common traps are sell-blocking logic (honeypots or "trapdoors"), sell taxes the owner can change, blacklists and whitelists, pausable transfers, max-tx and max-wallet limits, cooldowns, owner balance changes or a hidden mint, a hidden owner, ownership that can be taken back after a "renounce", and upgradeable proxies. GoPlus encodes most of these as boolean fields. Academic studies classify between about 50% and more than 97% of Uniswap-listed tokens as scams, depending on how "scam" is defined.

### Cited Findings
- **GoPlus `is_honeypot`:** "HoneyPot" means the token may not be sellable because of the contract's functions, or because it contains malicious code. — [GoPlus docs: Response Details (via search snippet)](https://docs.gopluslabs.io/reference/response-details)
- **GoPlus `transfer_pausable`:** whether trading can be paused by the token contract. "1" means true, "0" means false, and **no return means unknown**. — [GoPlus docs](https://docs.gopluslabs.io/reference/response-details)
- **GoPlus `cannot_sell_all`:** whether the contract restricts holders from selling all of their tokens. — [GoPlus docs](https://docs.gopluslabs.io/reference/response-details)
- An empty or missing GoPlus field means "unknown", so a bot must not treat it as false. Dedaub's Tok{In} mapping of GoPlus-style fields returns null for `cannot_sell_all` because Dedaub does not track it. — [GoPlus docs](https://docs.gopluslabs.io/reference/response-details); [Dedaub Tok{In} API docs](https://docs.dedaub.com/docs/token_safety/tokin/)
- Community GoPlus field catalogs are available for the full list of EVM flags. — [GoPlus Token Security items (Notion)](https://inky-punch-9d2.notion.site/GoPlusTokenSecurityItems-159ac62a668548c8ba4f524f4eb6f2b8); [Normalizex gopluslabs-api wrapper](https://github.com/Normalizex/gopluslabs-api)
- Xia et al., *"Trade or Trick? Detecting and Characterizing Scam Tokens on Uniswap"* (SIGMETRICS 2022), found more than 10,000 scam tokens, estimated that roughly half of listed tokens were scams, and found that some contain hidden tricks and backdoors built for rug pulls. — [PolyU Scholars Hub](https://research.polyu.edu.hk/en/publications/trade-or-trick-detecting-and-characterizing-scam-tokens-on-uniswa-3/); [arXiv 2109.00229](https://arxiv.org/pdf/2109.00229v1)
- There is an academic analysis of **"trapdoor tokens"** on Uniswap, i.e. honeypot-like tokens that can be bought but not sold, titled *"From Programming Bugs to Multimillion-Dollar Scams"*. I have only the title; I could not read the content. — [arXiv 2309.04700](https://arxiv.org/pdf/2309.04700)
- *"Stop Pulling my Rug: Exposing Rug Pull Risks in Crypto Token to Investors"* (Tokeer, ICSE 2024) studies 201 real rug pull events, proposes a detection tool for contract-level rug risks, and argues these risks are more widespread than they appear. — [WingTecher paper PDF](http://www.wingtecher.com/themes/WingTecherResearch/assets/papers/Tokeer_CameraReady.pdf)

### Inferences
*(Domain knowledge, unverified this session. GoPlus field names are listed as I know them and must be checked against the live docs.)*
- **EVM pre-buy checks (GoPlus-style flags → bot policy):**
  - Hard reject: `is_honeypot=1`, `cannot_buy=1`, `cannot_sell_all=1`, `transfer_pausable=1` (unless the owner is truly renounced), `is_blacklisted=1` **with** a live owner, `owner_change_balance=1` (the owner can rewrite balances), `hidden_owner=1`, `can_take_back_ownership=1` (fake renounce), `selfdestruct=1`, `is_mintable=1` with a live owner (hidden mint), `slippage_modifiable=1` (the owner can change the tax) with a live owner, `personal_slippage_modifiable=1` (per-address tax, a targeted honeypot), `is_open_source=0` (unverified source).
  - Threshold flags: `buy_tax` / `sell_tax` above X%, for example a sell tax above 10% is reject-worthy for a short-hold bot; `trading_cooldown=1`; `anti_whale=1` / `anti_whale_modifiable=1` (max tx / max wallet that can be set to around 0 to block sells); `is_whitelisted=1` (only whitelisted addresses can trade or skip limits).
  - Proxy: `is_proxy=1` means logic can be upgraded after you buy. Check who controls the proxy admin (an EIP-1967 admin slot pointing to an EOA is high risk) and treat it as at least a warning.
  - `external_call=1`: the token calls external contracts during transfer, so sell logic can be hidden off-contract.
  - "Renounced" ownership: check `owner_address == 0x0…`, **and** check for a hidden owner, ownership that can be retaken, and privileged roles that are not `owner()` (AccessControl, custom `_admin` / `_dev` variables). A renounced `owner()` alone is not sufficient.
  - LP: `lp_holders` with `is_locked` and the locker contract. Check the share of LP that is burned or locked and when the lock expires. Check `creator_percent`, `owner_percent` and `holders` concentration.
- Trapdoor and honeypot code often keys on `to == pair` (selling into the pool), on `tx.origin`, or on a tx.gasprice or block-number condition, so a sell can succeed in simulation from one address and fail from another. This is why simulation alone is also not sufficient (see Q5).

### Gaps
- I could not fetch the full GoPlus field list. Only `is_honeypot`, `transfer_pausable` and `cannot_sell_all`, plus the "no return = unknown" semantics, are confirmed from docs snippets this session.
- I found no source quantifying how often each EVM trick (blacklist, proxy, hidden mint and so on) occurs among scam tokens. The Xia et al. and trapdoor papers likely contain this, but I could not read them.

## Q3. Prevalence statistics of rug pulls and memecoin scams

### Takeaway
Most newly launched memecoins collapse or are extractive, but the headline numbers depend heavily on definitions. Solidus Labs' "98.6–98.7% of pump.fun tokens" is mainly a *liquidity-collapse* metric (below $1,000 liquidity), not proven fraud. Chainalysis' stricter on-chain rug-pattern estimate is about 3.6% of all new tokens. Academic Uniswap estimates range from about 50% to 97.7%.

### Cited Findings
- **Solidus Labs (May 2025):** about 98.6% of pump.fun tokens were rug pulls or pump-and-dumps. Solidus's own wording is "approximately 98.7%", and its 8 May 2025 post said "98.7% of @pumpdotfun tokens = pump & dumps". — [The Defiant](https://thedefiant.io/alarming-99-of-memecoin-launches-on-pumpfun-are-pump-and-dumps-or-rug-pulls-report); [Solidus Labs report page](https://www.soliduslabs.com/reports/solana-rug-pulls-pump-dumps-crypto-compliance); [CoinDesk](https://hotfix.coindesk.com/business/2025/05/07/98-of-tokens-on-pump-fun-have-been-rug-pulls-or-an-act-of-fraud-new-report-says)
- **Methodology caveat:** the 98.6% figure covers more than 7 million pump.fun tokens (Jan 2024 – Mar 2025, tokens with at least 5 trades) that fell **below $1,000 liquidity**. That shows collapse, not proven criminal fraud. Only about 97,000 of about 7M kept at least $1,000 in liquidity. — [DeepStrike](https://deepstrike.io/blog/rug-pull-statistics); [BeInCrypto](https://beincrypto.com/pump-fun-tokens-scams-solidus-labs-report/)
- **Solidus, Raydium:** 93% of Raydium pools (361,000) showed soft-rug characteristics. The median rug was about $2,832 and the largest was $1.9M (attributed to MToken by CoinDesk). — [DeepStrike](https://deepstrike.io/blog/rug-pull-statistics); [CoinDesk](https://hotfix.coindesk.com/business/2025/05/07/98-of-tokens-on-pump-fun-have-been-rug-pulls-or-an-act-of-fraud-new-report-says)
- **Chainalysis (2025 Crypto Crime Report, covering 2024):** 3.59% of all new tokens minted in 2024 showed classic rug-pull behavior. — [Cointelegraph](https://cointelegraph.com/news/crypto-crime-2024-2025-chainalysis). **Conflict:** Cryptonews, citing Chainalysis, gives pump-and-dump as 4.52% of activity in 2024, up from 3.59% in **2023**, so one outlet has the year or the metric mixed up. — [Cryptonews](https://cryptonews.com/news/chainalysis-market-manipulation-billions-trades/). The primary PDF is [The 2025 Crypto Crime Report (mirror)](https://antiriciclaggiocompliance.it/app/uploads/2025/03/The-2025-Crypto-Crime-Report-Chainalysis.pdf). It was not read this session.
- **Chainalysis:** only about 1.7% of tokens launched remained actively traded over the past 30 days, which it attributes largely to wash trading, pump-and-dumps and rug pulls (reported via secondary coverage). — [Cryptonews](https://cryptonews.com/news/chainalysis-market-manipulation-billions-trades/)
- **Chainalysis 2026 report (covering 2025):** about $154B received by illicit addresses (other outlets say $150B or $145.9B). Stablecoins were 84% of illicit transaction volume. No 2025 memecoin rug-pull percentage was found in snippets. — [Bitcoin Magazine](https://bitcoinmagazine.com/news/crypto-crime-soared-to-154-billion-in-2025); [The Block](https://www.theblock.co/post/384753/crypto-crime-150-billion-usd-2025-state-actors-scale-onchain-chainalysis)
- **SolRPDS (Alhaidari et al., ACM CODASPY '25):** covers Solana DeFi Feb 2021 – Nov 2024: 3.69B transactions and 278,099,218 liquidity-pool actions. **22,195 tokens** show rug-pull patterns. The dataset is public (CC BY 4.0, on GitHub DeFiLabX/SolRPDS and Hugging Face). — [arXiv 2504.07132](https://www.arxiv.org/pdf/2504.07132); [Hugging Face README](https://huggingface.co/datasets/DeFiLab/SolRPDS/blob/main/README.md)
- **SolRugDetector (arXiv 2603.24625, March 2026):** 117 manually verified Solana rug-pull tokens plus a 76,469-token in-the-wild set. — [arXiv 2603.24625](https://arxiv.org/html/2603.24625v1)
- **Uniswap, academic:** Xia et al. (2022) put about 50% of listed tokens as scams (more than 10,000 scam tokens). — [PolyU](https://research.polyu.edu.hk/en/publications/trade-or-trick-detecting-and-characterizing-scam-tokens-on-uniswa-3/). Mazorra, Adan and Daza, *"Do Not Rug On Me"* (2022 preprint), give **97.7%**: 26,957 scam tokens versus 631 non-malicious. Critics say liquidity and volume were not factored in. — [arXiv 2201.07220](https://arxiv.org/pdf/2201.07220); [Yahoo Finance](https://finance.yahoo.com/news/report-claims-97-uniswap-tokens-005632109.html)
- **2025 ScienceDirect study on meme-coin rug-pull detection:** more than 98% of tokens minted daily on Uniswap V2 show fraudulent characteristics. — [ScienceDirect, "Detecting rug pulls in decentralized exchanges: The rise of meme coins"](https://www.sciencedirect.com/science/article/pii/S2096720925000636)

### Inferences
- For a bot, the operational base rate is "almost every new launch goes to about zero". The 3.6% "classic rug" figure versus the 98% "collapse" figure tells you most losses come from soft rugs, dumps and abandonment, **not** from contract traps a scanner can catch. Contract checks are necessary but cover only a minority of the loss modes. Holder distribution, bundling and creator-history checks matter as much.
- When quoting statistics, always state the definition: liquidity below a threshold, an LP-removal pattern, or a code-level backdoor.

### Gaps
- No 2025 or 2026 Chainalysis figure for the memecoin rug-pull share was found.
- No primary prevalence data was found for Token-2022 permanent-delegate scams, nor for EVM chains such as Base or BSC specifically in 2025–2026.
- The Solidus report and the SolRPDS PDF could not be read directly (domains blocked), so definitions and thresholds come from secondary summaries.

## Q4. Detection tools and APIs: RugCheck, GoPlus, Honeypot.is, Token Sniffer, De.Fi, Birdeye — what they check and where they fail

### Takeaway
Each tool covers a different slice. GoPlus is a broad static and flag API for EVM, with Solana support. Honeypot.is is EVM buy/sell simulation that returns taxes and limits. RugCheck is Solana-focused: authorities, LP lock, metadata, Token-2022 traps and a risk score. Birdeye `token_security` gives Solana and EVM authority, holder and Token-2022 fields. All of them return nulls or "unknown" values that bots commonly misread as "safe", and none of them reliably catch soft rugs or bundled supply.

### Cited Findings
- **GoPlus:** EVM token-security flags such as `is_honeypot`, `transfer_pausable` and `cannot_sell_all`. **No return = unknown**, not false. — [GoPlus Response Details](https://docs.gopluslabs.io/reference/response-details). GoPlus also offers pay-per-call access via x402. — [x402.gopluslabs.io](https://x402.gopluslabs.io)
- **Honeypot.is (EVM only: Ethereum, BNB Chain, Base and others):**
  - It simulates trades against the token's main pool. Its `simulationResult` includes buy, sell and transfer tax and maxBuy/maxSell values. — [Honeypot.is API reference](https://docs.honeypot.is/ishoneypot)
  - `simulationResult` is **not guaranteed** to be present, for example when the token is a honeypot or the simulation failed. A `simulationError` such as insufficient liquidity can be returned.
  - `maxBuy` / `maxSell` are present only if they were detected. — [Honeypot.is API reference](https://docs.honeypot.is/ishoneypot)
  - One third-party wrapper's rule: never record a "pass" without a successful simulation. — [oanor Honeypot API](https://www.oanor.com/api/honeypot-api)
- **RugCheck (Solana):**
  - The summary endpoint (about 300 bytes) returns a `risks` array (name, score, level), `score`, `score_normalised` and `lpLockedPct`. The full report can be about 2.5 MB.
  - Risk names include "Mutable metadata", "Mint Authority still enabled" and "Freeze Authority still enabled".
  - One integration had a bug where LP always showed "not locked" because it read the wrong field. — [antares-extension PR #766](https://github.com/antaresscan/antares-extension/pull/766)
  - `score_normalised` is described as 0–100, and a raw score below 1000 is labelled "Good". — [Termo RugCheck skill](https://termo.ai/skills/rugcheck)
  - A live example shows a token rated "DANGER" for mutable metadata despite 100% LP locked. A locked LP does not clear other flags. — [RugCheck report page](https://rugcheck.xyz/tokens/DzqisfqcREDQaC3MFZWHkJcQPMNb7UYx8oYyHTt3uxSA)
  - RugCheck flags the permanent delegate, transfer hooks and default-frozen state. — [Blofin](https://blofin.com/en/academy/education/solana/solana-memecoin-rug-pull-safety)
- **Scoring weights differ by vendor.** Solana Tracker's rug API weights freeze authority at 7500, unlocked LP at 4000 and mint authority at 2500. Do not assume RugCheck uses the same weights. — [Solana Tracker: Solana Rug Check API](https://www.solanatracker.io/resources/check-solana-token-rug-risk-api)
- **Birdeye `token_security`** (`GET /defi/token_security`, header `x-chain`): Solana fields include `mutableMetadata`, `freezeable` / `freezeAuthority`, `top10HolderPercent`, `transferFeeEnable`, `isToken2022` and `creatorPercentage`.
  - Most fields are **nullable**, and null can mean "not applicable" rather than "check failed".
  - The unit of `top10HolderPercent` (fraction or percent) is ambiguous across sources.
  - For holders, use `GET /defi/v3/token/holder`, plus the newer `GET /token/v1/holder-profile` (released 17 April 2026) with a top-10 concentration summary and holder tags. — [Birdeye Rug Checker blog](https://birdeye.so/data-api/blog/detail/rug-checker-api-solana-evm-birdeye-data); [Birdeye changelog 2026-04-17](https://data.birdeye.so/docs/changelog/20260417-release-token-holder-profile-positions-apis); [Birdeye holder API](https://docs.birdeye.so/reference/get-defi-v3-token-holder); [birdeye-go (third-party)](https://pkg.go.dev/github.com/Laminar-Bot/birdeye-go)
- **Solana Foundation "tokens" repo:** a 2026 PR combines stored Webacy rows, live Birdeye tier data and authority flags into category bands. This is evidence that multi-source aggregation is the emerging practice. — [solana-foundation/tokens PR #237](https://github.com/solana-foundation/tokens/pull/237)
- **Dedaub Tok{In}** is another token-safety API with GoPlus-compatible fields. Some fields, such as `cannot_sell_all`, are untracked and return null. — [Dedaub docs](https://docs.dedaub.com/docs/token_safety/tokin/)
- **Scanners miss things.** Tokens can pass scanners while still being honeypots through freeze authority or transfer fees, or while carrying dev-held liquidity or bundled insider supply. — [Blofin](https://blofin.com/en/academy/education/solana/solana-memecoin-rug-pull-safety)

### Inferences
*(Domain knowledge, unverified this session.)*
- **Token Sniffer** (owned by Solidus Labs) gives EVM tokens a 0–100 score from contract-pattern matching (similar or copied contracts, known scam signatures), ownership and LP checks, plus its own swap simulation. **De.Fi Scanner** runs static contract-permission analysis on EVM and Solana: owner privileges, mint, blacklist, proxy, and so on. I found no current documentation for either in this session.
- **Common false positives:**
  - Legitimate tokens with a live owner (for example during a launch phase) or with an upgradeable proxy.
  - Stablecoins or RWA tokens with freeze authority or a permanent delegate.
  - Anti-bot logic that blocks snipers in the first blocks only.
  - Low liquidity that makes a simulation fail ("insufficient liquidity" ≠ honeypot).
- **Common false negatives:**
  - Time- or condition-triggered traps: tax raised after N blocks, blacklist added after launch, a trap that only fires for non-whitelisted addresses or above an amount.
  - Logic in external contracts or proxies upgraded after the scan.
  - Token-2022 hooks that behave differently per caller.
  - Soft rugs and dumps by bundled wallets, which no contract flag captures.
  - Unverified bytecode where static analysis is weak.
- **Bot design implication:** query at least two independent sources plus your own RPC reads. Treat unknown or null as failing for hard-reject fields. **Re-check right before execution**, not only at discovery, because authorities and taxes can change between discovery and buy.

### Gaps
- No primary documentation was retrieved for **Token Sniffer** or the **De.Fi scanner**. Their check lists, scoring and accuracy are unverified here.
- No independent benchmark of false-positive and false-negative rates across these tools was found. The search for one was cut off by the search budget.
- The full GoPlus Solana field set (for example the names of its Token-2022 flags) was not confirmed.

## Q5. Sell-simulation techniques

### Takeaway
The strongest pre-buy test is to **simulate a buy followed by a sell**, at your real size, from a realistic address, at the latest state. Measure the effective tax as expected output versus received output, and confirm the sell does not revert. Honeypot.is productizes this for EVM. On Solana the equivalent is `simulateTransaction` on a buy+sell bundle, plus mint and extension reads, because Solana traps are mostly authority- and extension-based.

### Cited Findings
- Honeypot.is simulates a buy and a sell through the token's main liquidity pool and reports buy, sell and transfer tax plus detected max-buy and max-sell limits. Simulation may fail ("insufficient liquidity"), and then no `simulationResult` is returned. — [Honeypot.is API reference](https://docs.honeypot.is/ishoneypot)
- Third-party agent tools offer "buy/sell sim + GoPlus audit" combos and sell-simulation endpoints, which shows the market converging on simulation plus static flags. — [Apify Token Honeypot Detector](https://apify.com/gochujang/token-honeypot-detector); [BRAINIAC sell-simulation tool](https://glama.ai/mcp/connectors/software.brainiac/token-security/tools/token-security_sell-simulation)
- Transfer hooks can make sells fail while buys succeed, so a sell must be simulated, not inferred from a successful buy. — [DEV Community](https://dev.to/ohmygod/solanas-permanent-delegate-burn-scam-how-token-2022-extensions-power-2026s-largest-automated-rug-4579)
- Permanent-delegate burns happen **after** the buy, seconds to about a minute later, in a separate transaction, so a same-transaction sell simulation will **not** detect them. Only reading the mint extension does. — [Coinpaper](https://coinpaper.com/5295/scammers-exploit-solana-token-feature-to-burn-users-crypto); [DEV Community](https://dev.to/ohmygod/solanas-permanent-delegate-burn-scam-how-token-2022-extensions-power-2026s-largest-automated-rug-4579)

### Inferences
*(Domain knowledge, unverified this session.)*

**EVM sell simulation:**
- Fork the latest block (Anvil or Hardhat fork, Tenderly, or `eth_call` with state overrides, or `debug_traceCall`).
- Fund a fresh EOA, which is what you will trade from. Swap ETH → token via the actual router and pool. Then call `approve` and swap the whole balance back. Also try selling 100% and a partial amount, because `cannot_sell_all` traps exist.
- Effective buy tax = 1 − received / quoted-without-tax. Do the same for sell.
- Also simulate a plain `transfer` to a second address, because some traps hit only transfers.
- Advance a few blocks or timestamps and re-sell to catch cooldowns and time-based tax switches.
- Simulate from more than one address to catch per-address traps (`personal_slippage_modifiable`, whitelists).
- Use the real gas price and `tx.origin`, since some traps key on gas price.

**Solana sell simulation:**
- Build a buy transaction and a sell transaction (Jupiter quote, or direct pump.fun / PumpSwap / Raydium instructions).
- Run `simulateTransaction` with `replaceRecentBlockhash` and the accounts the buy would create. Alternatively use a local fork (for example Surfpool or LiteSVM, or cloned accounts in solana-test-validator) to run buy then sell in sequence.
- Check that the sell does not error (transfer hook, frozen account) and compare amounts to compute the transfer-fee impact.

**Limits:**
- Simulation cannot detect future owner actions: a later tax raise, blacklist, LP pull, authority-based freeze or delegate burn.
- Honeypot logic may detect simulation contexts.
- Thin liquidity causes spurious failures.
- So combine simulation with static authority and permission checks, then re-simulate immediately before sending. After buying, keep monitoring and use small position sizes.

### Consolidated pre-buy checklist (for the report writer)
*(Synthesis of the cited findings and of domain knowledge. Items marked † are not backed by a source fetched this session.)*

**Solana: hard reject**
- Mint authority live.
- Freeze authority live.
- Token-2022 permanent delegate.
- Transfer hook (non-whitelisted).
- DefaultAccountState = Frozen†.
- NonTransferable†.
- Pausable with a live authority†.
- Transfer fee above tolerance, or with a live fee authority.
- Sell simulation fails.

**Solana: score or flag**
- Mutable metadata.
- LP not burned or locked (`lpLockedPct` low).
- Top-10 holders above about 30% (excluding pool and burn).
- High creator or bundled-wallet share†.
- Serial-deployer creator†.
- Liquidity below the size threshold.
- Very young pool.

**EVM: hard reject**
- `is_honeypot`.
- `cannot_buy`†.
- `cannot_sell_all`.
- `transfer_pausable`.
- `owner_change_balance`†.
- `hidden_owner`†.
- `can_take_back_ownership`†.
- Mintable with a live owner†.
- Changeable tax with a live owner†.
- Per-address tax†.
- Unverified source†.
- Simulated sell tax above tolerance or sell revert.
- Honeypot.is simulation missing (treat as fail).

**EVM: score or flag**
- Upgradeable proxy†.
- Blacklist or whitelist functions†.
- max-tx, max-wallet or anti-whale limits†.
- Cooldown†.
- External calls in transfer†.
- LP not locked or burned, or lock expiring soon†.
- Owner, creator or top-10 concentration.

**Process (both chains)**
- Use at least two independent sources plus direct RPC reads.
- Treat null or unknown as fail for hard-reject fields.
- Re-check and re-simulate just before sending.
- Use small size and keep monitoring after the buy.

### Gaps
- No primary source on Solana-specific simulation tooling (Surfpool, LiteSVM, Jupiter simulation endpoints) was retrieved this session.
- No source on anti-simulation honeypot techniques, or on how often they occur, was retrieved.
