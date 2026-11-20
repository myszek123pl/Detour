# Base creator/content coins and social launchpads (Zora, Clanker/Farcaster, Base App, Flaunch)

Note: research budget was 4 tool calls (3 searches, 1 fetch failed: theblock.co not resolvable). Figures come from search-result summaries, not full-page reads. Treat all as UNVERIFIED unless noted. Base App-specific data: nothing found.

## Mechanics, fees, supply design, volumes 2025-2026; difference from pump.fun

### Takeaway
Zora (creator/content coins) boomed in 2025 and collapsed by mid-2026 (quarterly revenue about -98%); Clanker (ERC-20 deployer via Farcaster/AI bot, Uniswap V3) and Flaunch (Uniswap V4 hooks, fee-sharing) are fee-share launchpads where creators earn LP fees, unlike pump.fun's bonding-curve model. Exact current volumes are not verified.

### Cited Findings
- Zora fees: one source says fees were cut from 3% to 1% and creator share raised from 33% to 50% in Sept 2025; another says 1% with 0.70% to creator (sources disagree) — [DefiLlama/search summary](https://defillama.com/protocol/zora-coins); [Messari](https://messari.io/report/zora-fundamental-divergence) (3% reduced via Uniswap V4 hook update)
- Zora gross protocol revenue fell from $5.64M (Q3 2025) to $106,540 (Q2 2026); monthly fees roughly $5k-$59k Mar-Oct 2026 vs $228k Feb 2025; 30d DEX volume snapshots $213k to $551k; cumulative DEX volume about $399M; peak day about $33M mostly Creator Coins — [DefiLlama Zora Coins](https://defillama.com/protocol/zora-coins) (via search summary, unverified)
- Zora co-founder Dee Goens replaced Jacob Horne as CEO after the revenue plunge (headline cites 98%) — [CoinStats](https://coinstats.app/news/0ace8f8f8505b5ac48b13c79cbda5e6f8515150e1da570de2766e8c7d987079e_Zora-cofounder-Dee-Goens-takes-over-as-CEO-after-98-revenue-plunge); [Cryptopolitan](https://www.cryptopolitan.com/dee-goens-takes-over-as-zora-ceo/)
- Odaily (July 2026) reports Coinbase CEO Armstrong acknowledged failure of the Base content-coin strategy; headline claims ZORA token -95% (supporting data not seen) — [Odaily](https://www.odaily.news/en/post/5211890)
- Clanker: April 2025 about $13M team revenue from 200k+ tokens in 5 months; cumulative fees about $27M and volume $2.7B then — [The Block](https://www.theblock.co/news/business/2025-04-04-clanker-team-earns-13-million-in-revenue-from-over-200000-tokens-on-base-in-just-five-months-349549)
- Clanker: about $3.48B cumulative volume by Aug 2025 (Dune via Cointelegraph); 355k tokens — [Cointelegraph](https://cointelegraph.com/news/clanker-ai-memecoin-fees-355k-tokens)
- Clanker: initial Uniswap V3 LP, 1% fee on volume, creators 40% / Clanker 60%; record weekly protocol fees over $8M reported around early Feb 2026 (KuCoin news, low reliability) — [KuCoin](https://www.kucoin.com/news/articles/clanker-protocol-reaches-8-million-weekly-fee-milestone-as-ai-agent-social-trading-ignites-base)
- Flaunch: Uniswap V4 hooks launchpad on Base, launched Feb 2025; 2,000+ tokens, about $75M volume (Alchemy listing, date unclear); 1% swap fee, governance fee switch up to 10% — [Alchemy](https://www.alchemy.com/dapps/flaunch); [RootData](https://www.rootdata.com/projects/detail/flaunch?k=MTU4MTk%3D)

### Inferences
- Difference from pump.fun: pump.fun uses a bonding curve with graduation to AMM; Base launchers deploy straight into Uniswap V3/V4 pools with single-sided liquidity and pay creators ongoing LP/hook fees (my characterization from background knowledge, not verified in this research). This creates creator incentive to farm volume rather than rug, but also huge token counts (hundreds of thousands) of dust.
- Content-coin volume was reflexive on Zora's incentive/hype cycle; sharp decline suggests a bot should not assume persistent liquidity.

### Gaps
- Exact supply design (Zora: reportedly 1B supply with creator allocation; unverified), Base App integration, Farcaster-Clanker current status, 2026 Clanker/Flaunch volumes, Base App data: not found.

## Trading dynamics, returns evidence, tradeable signals

### Takeaway
Evidence is qualitative: viral creator coins spike then slump; no quantified share of losing buyers was found. Signals must be inferred.

### Cited Findings
- Nick Shirley's Zora coin spiked to about $9M valuation then slumped; Base supporters giving up on Zora creator coins (Dec 2025) — [The Defiant](https://thedefiant.io/zora-drops-as-creator-coins-disappoint); [Cointelegraph](https://cointelegraph.com/news/base-creator-coin-experiment-meets-resistance)
- Critics: ZachXBT called coins merely "viral" with no fundamentals; The Block framed as vehicle for speculation and noted Base activity metrics inflated by Zora ("vanity metric") — [BeInCrypto](https://beincrypto.com/zachxbt-zora-content-coins-criticism); [The Block](https://www.theblock.co/news/ecosystems/2026-01-27-nick-shirley-token-base-zora-surge-lack-activity-387106)
- Jesse Pollak defended that buying content coins creates demand for creator coins — [Odaily](https://www.odaily.news/en/post/5211890)

### Inferences
- Plausible bot signals (untested hypotheses): follower/virality spike of the creator (Farcaster/X) before listing; fee-share-driven volume farming; early-minutes sniping with strict exit as pumps mean-revert; liquidity filter due to thin pools; avoid wash-volume (vanity metrics).
- Base-chain trading needs MEV/sequencer-latency awareness (not researched).

### Gaps
- No data on win rate, median return, or holder concentration; Blockworks Zora analytics and Dune dashboards were not accessible. theblock.co fetch failed (host not in allowed network).
