# EVM memecoin bot execution: Ethereum, Base, BSC (as of Nov 2026)

Method note: only 3 web searches run (budget ~5); fetch of docs.base.org failed (host not in session allowlist), so all claims rest on search-result summaries, not full-page reads. Treat numbers as unverified unless noted. Gas-strategy items marked [UNVERIFIED/background] come from general knowledge, not from fetched sources.

## Ethereum: Flashbots Protect / MEV-Share and sandwich exposure

### Takeaway
Flashbots Protect hides txs from the public mempool (no rebate); MEV-Share adds opt-in selective disclosure with rebates. Block building is highly concentrated, so private routing mostly matters via which builders see your flow. No reliable 2026 primary data found on sandwich share or Protect market share.

### Cited Findings
- 2026 article describes Flashbots running three tools: Protect (shielding, no rebate), MEV-Share (rebate, but exposed to searcher competition), MEV-Boost. — [onebullex](https://www.onebullex.com/news/articles/flashbots-splits-2026-mev-market-into-three-ordering-tools-as-sandwich-attacks-drain-180m) (secondary/news-style; weak source)
- Same article claims ~89% of Ethereum blocks flow through MEV-Boost relays, Protect shields "40% of retail swaps", and sandwiches drain "$180M" — [onebullex](https://www.onebullex.com/news/articles/flashbots-splits-2026-mev-market-into-three-ordering-tools-as-sandwich-attacks-drain-180m); no primary data behind these figures (UNVERIFIED).
- An arXiv paper (revised May 2026) reports two builders produce nearly 80% of Ethereum blocks — [arXiv 2508.04003](https://arxiv.org/html/2508.04003) (as summarized by search; not read in full).
- Dec 2025 arXiv study (data Nov-Dec 2024) found 2,932 private sandwich attacks affecting 3,126 private victim txs, i.e. private routing reduces but does not eliminate sandwiching — [arXiv 2512.17602](https://arxiv.org/pdf/2512.17602v1)
- One study reports sandwich front-run txs are 48% more likely to appear in the first block quartile (Ethereum L1) — surfaced via search on [Base ordering/arXiv results](https://arxiv.org/html/2508.04003) (attribution uncertain).
- MEV-Share was introduced to share MEV profit with users and integrated into Flashbots Protect RPC — [The Block](https://www.theblock.co/amp/post/212491/flashbots-introduces-mev-share-protocol)

### Inferences
- For a memecoin sniper/buyer on L1, sending via Protect/private builder RPC avoids public-mempool sandwiching, but residual risk exists when the order flows to builders that run/permit sandwich bundles.
- Bots that want speed (launch sniping) trade off against MEV-Share rebates; rebate flow is irrelevant for time-critical entries.

### Gaps
- No primary current stats for Protect usage, sandwich share of L1 volume, or per-builder block share (suggest rated/mevboost.pics/Dune; not accessed).
- Gas strategy specifics (EIP-1559 tip sizing, bundle coinbase payments, builder-direct submission) not sourced; [UNVERIFIED/background] standard practice is bundle submission with direct coinbase transfer or high tip to top builders (beaverbuild, Titan), with revert protection.

## Base: sequencer ordering, priority fees, Flashblocks

### Takeaway
Base sequencer builds 200ms Flashblocks; once a Flashblock is broadcast its order is locked, so late high-fee txs cannot jump earlier ones. Priority fee competition is effectively localized to the first Flashblock slot.

### Cited Findings
- Flashblocks are built every 200ms; once built and broadcast, ordering is locked and later higher-priority-fee txs cannot enter earlier Flashblocks; Base calls this a deliberate tradeoff that can break PGA ordering within a block — [Base docs: transaction ordering](https://docs.base.org/base-chain/network-information/transaction-ordering.md) (via search summary; page fetch failed)
- 2026 paper: Flashblocks on Base and Unichain reduced global fee-ordering efficiency, concentrating fee competition in the first slot with later slots largely insensitive to priority fees — [arXiv 2606.00720](https://arxiv.org/html/2606.00720v1) (via search summary; unverified details)
- 2026 study of cyclic arbitrage on Base (Jun 2025-Feb 2026): probabilistic bots pay higher priority fees; spam share of blockspace fell after Base config changes — [arXiv 2604.00234](https://arxiv.org/html/2604.00234)
- Base docs on Flashblocks and block building: [Flashblocks](https://docs.base.org/base-chain/flashblocks), [block building](https://docs.base.org/chain/block-building)

### Inferences
- Optimal Base tactic: land in the earliest Flashblock (low latency to sequencer/Flashblocks-aware RPC), not just bid a huge tip; overpaying after a Flashblock closes buys little.
- Sandwiching on Base is structurally harder to time given locked 200ms slots, but this is inference, not measured.

### Gaps
- No Base-specific sandwich prevalence measurement found.
- Exact priority-fee-ordering rules within a Flashblock, gas limits per Flashblock, min base fee, and whether Base has a private/protected mempool: not verified (docs fetch blocked; allow docs.base.org to retry).

## BSC: private mempools (48 Club, bloXroute, BlockRazor) and sandwiches

### Takeaway
BSC block building is dominated by 48 Club and BlockRazor; the Goodwill Alliance (Mar 2025) pushed validators onto MEV-protected builders with sandwich detection, cutting detectable sandwiches, but bots shifted to covert non-atomic sandwiches and private-routing leakage persists.

### Cited Findings
- Goodwill Alliance launched Mar 2025; BNB Chain says all active validators enforce protections via MEV-protected builders; 48 Club, BlockRazor, bloXroute, NodeReal contribute; blog title claims 95% sandwich reduction (underlying data not seen) — [BNB Chain blog](https://www.bnbchain.org/en/blog/how-the-goodwill-alliance-slashed-sandwich-attacks-by-95) (vendor/foundation source)
- 48 Club open-sourced "bscexorcist", a block-level sandwich detector — [BNB Chain blog](https://www.bnbchain.org/en/blog/how-the-goodwill-alliance-slashed-sandwich-attacks-by-95)
- BlockRazor: after its detection went live (Mar 2025) detectable attacks fell, but top sandwich bots moved to covert non-atomic sandwiches — [BlockRazor](https://blockrazor.io/blog/20250421SANDWICH/) (vendor-authored)
- Feb 2026 arXiv "MEV in Binance Builder": 48Club and BlockRazor consistently dominate block construction since May 2025 — [arXiv 2602.15395](https://arxiv.org/html/2602.15395v1); BlockRazor's own analysis put the two near 80%, bloXroute+Blocksmith+NodeReal ~19% — [BlockRazor](https://blockrazor.io/blog/20250116PBS/) (vendor, unverified)
- Private sandwiches exist: 2,932 private sandwich attacks found in Nov-Dec 2024 data (pre-Goodwill) — [arXiv 2512.17602](https://arxiv.org/pdf/2512.17602v1)
- BNB Chain MEV protection integrated in several wallets — [BNB Chain blog](https://www.bnbchain.org/en/blog/protecting-users-from-sandwich-attacks-bnb-chain-introduces-mev-protection-with-several-wallets)

### Inferences
- On BSC, submitting via a builder RPC (48 Club Privacy RPC, BlockRazor, bloXroute) is the default for memecoin bots; builder concentration means 2 endpoints cover most blocks.
- Post-2025 sandwiching is likely lower but not zero; non-atomic variants are harder to detect.

### Gaps
- No 2026 post-Goodwill sandwich statistics; bribe/tip conventions (e.g., 48 Club "soul point"/gas price 0 bundles, BlockRazor builder tips) not verified. [UNVERIFIED/background] BSC min gas ~0.05-1 gwei after 2025 reductions; not sourced.

## Cross-chain sandwich prevalence and gas strategy summary

### Takeaway
Evidence is thin and uneven: private-routing + builder concentration is the main mitigation on ETH and BSC; Base relies on sequencer/Flashblock ordering. No source gave comparable per-chain sandwich rates.

### Cited Findings
- See per-chain sections; no cross-chain comparison source located.

### Inferences
- Ranking of sandwich risk (hypothesis only): Ethereum L1 public mempool > BSC (reduced by GWA) > Base (no public mempool; ordering locked by sequencer). Needs data (EigenPhi, Dune) to confirm.

### Gaps
- EigenPhi/Dune per-chain sandwich counts for 2026 not accessed. Recommend follow-up search once those hosts are reachable.
