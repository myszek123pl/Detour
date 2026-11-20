# Cross-chain memecoin trading (bridges, multichain launches, wrapped memes, arbitrage) — as of Nov 2026

Note: search budget was hit by rate limits (2 of 4 searches returned errors: Wormhole NTT/multichain launches; Mayan/deBridge/Relay latency and fees). Those topics are mostly Gaps. Items marked UNVERIFIED are from model background knowledge, not sourced.

## How do memecoins go multichain, and what are the latency/cost of bridging?

### Takeaway
No sourced data was retrieved on specific memecoin multichain launches or on bridge latency/fees. Only the general mechanics of bridge arbitrage (bridge delay dominates settlement time) were sourced.

### Cited Findings
- Cross-chain MEV research describes two approaches: inventory arbitrage (capital pre-positioned on both chains) and bridge arbitrage (assets moved between legs, where bridge delay dominates total settlement time) — [arXiv 2501.17335](https://arxiv.org/html/2501.17335v2) (as summarized by search tool; not opened in full)
- An arXiv paper reports a first cross-chain analysis of meme coins (tokenomics, temporal evolution, price growth by chain); it does not appear to study arbitrage — [arXiv 2511.17527](https://arxiv.org/html/2511.17527) (summary-level only; not opened)

### Inferences
- UNVERIFIED background: common routes are (a) native issuance per chain via messaging frameworks (Wormhole NTT, LayerZero OFT) with burn/mint or lock/mint, (b) liquidity-pool-based wrapped versions, (c) independent "copycat" tokens with the same ticker on another chain (not bridged at all). Intent-based routes (Mayan Swift, Relay, deBridge DLN) typically settle in seconds to ~1 min using solver-fronted liquidity; canonical/guardian-based bridges take longer. Verify against provider docs before citing numbers.

### Gaps
- Actual latency and fee figures for Wormhole, deBridge, Mayan, Relay (search failed).
- Named examples of memecoins launched multichain via NTT/OFT (search failed).

## Risks (bridge hacks, fake wrapped tokens)

### Takeaway
Bridge exploits remain a major loss vector in 2026, mostly via forged/invalid cross-chain message validation rather than simple key theft. No sourced material on fake wrapped memecoins.

### Cited Findings
- PeckShield (June 1, 2026 alert): cumulative bridge losses $340.7M across 14 major exploits YTD — [DEXTools news](https://www.dextools.io/news/crypto-bridge-hacks-340-million-2026-peckshield-alert-june-2026)
- Largest incident: KelpDAO ~ $292M in April 2026; attacker forged a cross-chain message on its LayerZero-powered bridge, releasing ~116,500 rsETH — [Bloomberg](https://www.bloomberg.com/news/articles/2026-04-19/crypto-hack-worth-290-million-triggers-defi-contagion-shock) (title/URL from results; $292M and mechanism per search-tool summary of secondary sources, so verify)
- Verus bridge lost ~$11.58M in May, later re-hit, total >$19M in ~2 months — [DEV Community](https://dev.to/codego_group_c184db25b758/bridge-exploits-resurge-as-verus-hack-pushes-2026-losses-to-329-million-38ai) (secondary source)
- Cointelegraph reports bridge exploits were the top attack vector in Q2 2026 (~$351M) and Q2 was the most hacked quarter (83 incidents) — [Cointelegraph](https://cointelegraph.com/news/q2-2026-most-hacked-quarter-record-83-incidents)
- Totals differ by source/scope: ~$329M (8 incidents through mid-May) vs $340.7M (14 incidents to June 1); other outlets cite >$750M for all 2026 hacks — [KuCoin blog](https://www.kucoin.com/blog/top-crypto-hacks-2026-bridge-exploits)

### Inferences
- Wrapped/bridged memecoins inherit bridge risk: if the bridge is drained or the message layer is forged, the wrapped token can depeg to zero. Native-issuance models reduce but don't remove this (message-layer trust).
- UNVERIFIED background: fake wrapped tokens are typically same-name/ticker tokens on another chain, or counterfeit mints on Solana/EVM; always verify the contract against the project's official address.

### Gaps
- No sourced incidents of fake wrapped memecoins or memecoin-specific bridge exploits.
- Post-June 2026 (Jun-Nov) loss totals not retrieved.

## Opportunities: cross-chain price discrepancies and persistence

### Takeaway
General literature confirms cross-chain price gaps exist and that bridge delay and non-atomicity limit capture; no memecoin-specific measurement of gap size or persistence was found.

### Cited Findings
- Cross-chain arbitrage requires holding assets on multiple chains and is not atomic, so the destination price can move between legs — [Chainscore](https://www.chainscorelabs.com/glossary/cross-chain-bridges-and-interoperability/bridge-liquidity-models/cross-chain-arbitrage); [IACR 2023/1898](https://eprint.iacr.org/2023/1898.pdf)
- Illustrative economics: a 0.5% gap is unprofitable if fees take 0.4% and slippage 0.2% — [Chainflip](https://chainflip.io/blog/cross-chain-arbitrage-crypto-trading)
- Bridge friction/fragmented liquidity can let same-token price gaps persist — [DEXTools tutorial (JA)](https://www.dextools.io/tutorials/same-token-different-price-why-cross-chain-liquidity-creates-ja) (summary-level)
- Flashbots has a page on cross-chain arbitrage — [Flashbots](https://www.flashbots.net/cross-chain-arbitrage) (not read)

### Inferences
- Memecoins with thin pools: slippage plus bridge delay likely consume most spreads; persistent gaps are more plausible for native-issued tokens with disconnected liquidity, but capacity is small. Where the same ticker is traded on chains without a bridge, "price gaps" reflect different assets, not arbitrage.
- Inventory arbitrage (pre-positioned capital) is more realistic than bridge-and-sell for volatile memecoins.

### Gaps
- No empirical memecoin gap size/duration data; would need own measurement (e.g., DEX pool price comparison on Solana vs Base/BNB for the same bridged token).
