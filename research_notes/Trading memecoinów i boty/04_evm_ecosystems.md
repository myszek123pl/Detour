# Memecoin ecosystems on EVM chains (Base, Ethereum, BNB Chain, Robinhood Chain): launchpads, DEXs, mechanics, how they differ for a bot. Current as of 20 Nov 2026

> **How this was researched:** web search only. Direct page fetches failed because the session's network blocks those hosts: solanafloor.com, memefees.com and memecentral.fun did not resolve. The web-search budget ran out before searches on Virtuals Protocol, Aerodrome and Base Flashblocks could run. Many figures below come from search-result summaries of the cited pages, not from full reads, so check numbers against DefiLlama or Dune before relying on them. Source quality is mixed. Cointelegraph, CoinDesk, Decrypt, The Defiant, BeInCrypto and arXiv are stronger. memefees.com, memecentral.fun, trustswap, bingx/learn, Atomic Wallet and KuCoin flash notes are weaker aggregators or vendor content.

---

## 1. Base: Zora (creator/content coins), Clanker, Virtuals, Flaunch, Uniswap v3/v4 and Aerodrome; volumes and trends

### Takeaway
Base had a big but short memecoin moment. Zora creator/content coins briefly passed Pump.fun in daily launches in July 2025, and minting peaked in January 2026. Then activity fell about 99%. By July 2026 Coinbase's CEO had publicly called content coins a mistake. In late August 2026 Base's weekly memecoin volume was only about $31M, or 0.5% of Base's spot DEX volume. Clanker (now owned by Farcaster/Neynar) is the main launcher still running, and it is small. No reliable 2026 data was found for Flaunch.

### Cited Findings
**Zora: the boom (mid-2025)**
- 30 Jul 2025: Zora launched 23,419 tokens in one day, more than LetsBonk (19,593) and Pump.fun (4,764), per Dune data. — [Cryptorank](https://cryptorank.io/news/feed/e2010-base-overtakes-solana-as-a-new-memecoin-hub); [Cryptopolitan](https://www.cryptopolitan.com/base-overtakes-solana-as-a-new-memecoin-hub/)
- Sources disagree on Zora's share that day: Cryptopolitan says 44.6% of launches, while Forklog and Cryptorank say 67.7% of launches across Base and Solana on the peak day. — [Forklog](https://forklog.com/en/zora-on-base-surpasses-pump-fun-and-letsbonk-in-meme-coin-issuance/); [Cryptopolitan](https://www.cryptopolitan.com/base-overtakes-solana-as-a-new-memecoin-hub/)
- Late Jul 2025: Zora was said to hold 92.5% of the "creator coin market", up from Pump.fun holding 88% two weeks earlier (Dune). — [BeInCrypto](https://beincrypto.com/zora-users-create-coins-price-nears-ath/)
- Base passed Solana in daily tokens created while Pump.fun shrank (mid-2025). — [Decrypt](https://decrypt.co/332573/base-overtakes-solana-in-daily-tokens-created-as-pump-fun-continues-to-shrink)
- Zora coins are tied to user profiles or posts (creator/content coins), unlike Pump.fun's anonymous memes. Jesse Pollak of Coinbase made this distinction. — [BeInCrypto](https://beincrypto.com/zora-users-create-coins-price-nears-ath/)

**Zora: the collapse (2026)**
- Coin minting peaked at 118,069 in January 2026, almost all content coins. Daily minting fell to about 638–852 by 15 Jul 2026. Daily creators fell from 32,286 (13 Feb 2026) to 512 (15 Jul 2026). Daily trading volume was about $112,170 on 15 Jul 2026. Sources describe a decline of roughly 99.8% but disagree on the peak date (April 2025 vs May 2026). — [BeInCrypto](https://beincrypto.com/jesse-pollak-base-zora-social-bet/); [The Defiant](https://thedefiant.io/news/markets/zora-drops-as-creator-coins-disappoint); [cryptoheadlines.io](https://cryptoheadlines.io/news/jesse-pollak-base-strategy-reset-zora-decline/)
- February 2026: Base reportedly ended Creator Rewards and removed its social feed, which one analysis links to the drop-off. — [memecentral.fun](https://memecentral.fun/guides/what-happened-to-zora) (weak source)
- July 2026: Coinbase CEO Brian Armstrong said the content-coin strategy was a mistake, and Base is refocusing on trading, payments and AI agents. Jesse Pollak said his on-chain social bet failed and handed the Base App to Coinbase. — [Protos](https://protos.com/coinbase-ceo-admits-content-coins-were-a-mistake/); [The Crypto Times, 14 Jul 2026](https://www.cryptotimes.io/2026/07/14/brian-armstrong-admits-coinbases-content-coin-strategy-failed/); [BeInCrypto](https://beincrypto.com/jesse-pollak-base-zora-social-bet/)
- 31 Aug 2026: Zora's 30-day DEX volume was about $504K (DefiLlama, per a secondary guide). The ZORA token is down about 80–96% from its 2025 peak, depending on the source. — [memecentral.fun](https://memecentral.fun/guides/what-happened-to-zora) (weak source; DefiLlama number not checked directly)

**Clanker**
- Farcaster acquired Clanker on 23 Oct 2025 for an undisclosed amount. Clanker's token system was kept, and two-thirds of protocol revenue is committed to buying back CLANKER. Each trade pays a 0.2% protocol fee to Clanker/Farcaster, which funds the buybacks. Only the WETH portion of fees is used for buybacks. — [Futu News](https://news.futunn.com/en/post/63927448/farcaster-acquires-clanker-to-bolster-financial-capabilities-is-the-social); [AiCoin](https://www.aicoin.com/en/article/496354); [Datawallet](https://www.datawallet.com/crypto/farcaster-explained)
- January 2026: Neynar reportedly acquired Farcaster, including its protocol contracts, repositories, app and Clanker. — [Datawallet](https://www.datawallet.com/crypto/farcaster-explained) (seen in search summary only)
- 31 Aug 2026: Clanker's 30-day fees across all chains were about $234K, mostly on Base. Lifetime figures differ by source: about $49.8M fees and over 500K tokens, versus $7.62B all-time trading volume. — [memecentral.fun](https://memecentral.fun/guides/what-is-clanker); [trustswap](https://trustswap.com/base/clanker-vs-zora-vs-flaunch) (weak sources)

**Flaunch / Virtuals / Base docs**
- Flaunch is described as a programmable memecoin launcher built on Uniswap v4 hooks. No 2026 volume or fee data was found. — [trustswap](https://trustswap.com/base/clanker-vs-zora-vs-flaunch); [memecentral.fun](https://memecentral.fun/guides/what-is-clanker)
- Base's docs point to Zora, Clanker, Flaunch and Mint Club as launch options. Base runs no launchpad of its own. — [trustswap summary](https://trustswap.com/base/best-launchpads) (Base docs not checked directly)
- Virtuals Protocol is the main Base launchpad for AI-agent tokens. One source claims CLANKER is highly correlated with VIRTUAL and BANKR, but gives no evidence. — [motiontrade / launchpad roundups](https://www.motiontrade.com/blog/how-meme-coins-launch-in-2026-the-launchpad-wars-and-a-changing-meme-market-explained); [Messari Clanker page](https://messari.io/project/tokenbot-clanker)

**Base meme volume, late summer 2026**
- Week ending 26 Aug 2026: Base memecoin volume was about $31.06M out of $6.55B weekly spot DEX volume (about 0.5%), on Blockworks data. — [Cryptobriefing](https://cryptobriefing.com/solana-reclaims-memecoin-volume-robinhood/); [SolanaFloor](https://solanafloor.com/news/solana-reclaims-memecoin-volume-dominance-from-robinhood-and-bnb-chain-capturing-85-market-share)
- One Q1 2026 analysis of about 15,000 launches says Base's share of memecoin *launches* rose from about 10% (mid-2025) to about 25% (early 2026). — [openliquid.io](https://openliquid.io/blog/state-of-memecoin-launches-2026/) (weak source; method unclear)

### Inferences
- On Base, the number of tokens launched and the money traded in them diverged sharply. Zora produced huge numbers of mints with very little volume per token. For a bot, a high launch count on Base does not mean a tradable opportunity. Filter on liquidity and volume, not on new-pair events.
- Base's memecoin layer now appears thin (about $31M/week in Aug 2026). Most Base DEX volume is majors and stables on Aerodrome and Uniswap. A meme-sniping strategy on Base would compete for a small pool.
- Clanker and Flaunch both build their tokens on Uniswap v3/v4 pools (Flaunch on v4 hooks). A Base bot therefore needs v4 PoolManager/hook decoding, not only v2-style pair events.

### Gaps
- No current (Q3–Q4 2026) primary data on Virtuals launch volume, Flaunch volume, or Aerodrome/Slipstream's share of meme liquidity. The search budget ran out, and Aerodrome/Virtuals queries returned nothing useful.
- Base Flashblocks (sub-second preconfirmations) and its effect on sniping latency were not researched (budget ran out).
- No primary DefiLlama or Dune pages were fetched (network restrictions). All volume numbers come via secondary pages.

---

## 2. BSC: four.meme, PancakeSwap, the 2025 BNB memecoin wave, volumes

### Takeaway
BNB Chain's memecoin wave peaked in October 2025. It started with CZ's "#BNB meme szn" post on 7 Oct 2025. Four.meme briefly beat Pump.fun on daily revenue, and BNB hit an all-time high of about $1,349. It cooled within weeks. By late 2026, Flap.sh (a programmable launchpad with creator-set taxes) had replaced four.meme as BSC's main launchpad by fees. For the 30 days ending 18 Nov 2026, Flap.sh took $16.5M in fees (#2 globally after Pump.fun), versus four.meme's $191K. BSC meme volume was about $412M/week in late Aug 2026.

### Cited Findings
- On 7 Oct 2025, CZ posted "#BNB meme szn!", seen as the catalyst. An earlier CZ meme reshare on 1 Oct had already launched the token "4". — [BingX Learn](https://bingx.com/en/learn/article/bnb-meme-season-key-metrics-and-what-you-need-to-know); [icobench](https://icobench.com/news/cz-sparks-bnb-meme-coin-season-as-giggle-and-4-tokens-skyrocket/)
- On 8 Oct 2025, Four.meme accounted for 83.9% of new token launches and passed Pump.fun's daily revenue. — [Cointelegraph Magazine](https://cointelegraph.com/magazine/bnb-uptober-binance-market-crash-scrutiny)
- Four.meme's 24-hour revenue was about $1.4M during that period, above Pump.fun's. Cumulative volume was about $2.6B (October 2025; weak source). — [BingX Learn](https://bingx.com/en/learn/article/what-is-four-meme-form-bnb-launchpad-how-does-it-work); [Atomic Wallet](https://atomicwallet.io/academy/articles/top-5-bnb-chain-memecoins-october-2025-season)
- The token "4" briefly passed a $200M market cap with about $290M in 24-hour volume. — [icobench](https://icobench.com/news/cz-sparks-bnb-meme-coin-season-as-giggle-and-4-tokens-skyrocket/)
- BNB hit a record of about $1,349 on 8 Oct 2025. — [FinancialContent](https://markets.financialcontent.com/wral/article/breakingcrypto-2025-10-8-bnb-rockets-to-third-largest-crypto-amidst-exploding-meme-coin-mania-on-bnb-chain)
- BingX titled the period "$6B in trading and 1,800x token gains" (October 2025). — [BingX Learn](https://bingx.com/en/learn/article/bnb-meme-season-key-metrics-and-what-you-need-to-know)
- One outlet reported that in the month around the peak, Four.meme tokens made up 65.3% of $39.6B in BNB DEX volume. Other outlets give different numbers. — [Phemex News](https://phemex.com/news/article/solana-launchpad-activity-plummets-73-as-fourmeme-gains-on-bnb-chain-25621); [BingX](https://bingx.com/en/learn/article/bnb-meme-season-key-metrics-and-what-you-need-to-know)
- Chain share of meme DEX volume around October 2025: BNB about 45% (up from 25% in April), Solana about 25%, Ethereum about 20%. — [CoinGape](https://coingape.com/binance-chain-overtakes-solana-in-memecoin-trading-volume/); [CryptoDNES](https://cryptodnes.bg/en/bnb-chain-overtakes-solana-as-top-blockchain-for-memecoin-trading/)
- Shortly afterwards Pump.fun took back the top spot and Four.meme fell behind, as the BNB meme season cooled (late 2025). — [Bitget News](https://www.bitget.com/news/detail/12560605026593)
- Cointelegraph links the BNB "Uptober" to scrutiny of Binance after the 10 Oct 2025 market crash. — [Cointelegraph Magazine](https://cointelegraph.com/magazine/bnb-uptober-binance-market-crash-scrutiny)
- Week ending 26 Aug 2026: BNB meme spot volume was about $412.4M, about 5.8% of BNB's total spot volume. — [SolanaFloor](https://solanafloor.com/news/solana-reclaims-memecoin-volume-dominance-from-robinhood-and-bnb-chain-capturing-85-market-share) (via search summary)
- **The launchpad leader changed in 2026.** For the 30 days ending 18 Nov 2026, Flap.sh (BSC) earned $16.51M in fees (18.7% of all launchpad fees, #2 behind Pump.fun's $42.78M) from 210,019 launches. Four.meme ranked #19 with $191.3K (0.2% share). — [memefees.com](https://memefees.com/best-memecoin-launchpads) (aggregator; method not checked)
- A DefiLlama-based report from about September 2026 put four.meme's 24-hour fees at about $9.6K against Flap's about $2.88M. Another early-September 2026 figure put four.meme's 30-day fees near $287K. These conflict with the memefees number. Some trackers changed how they count fees in late August 2026. — [Longbridge](https://longbridge.com/news/298210180); [kkdemian Flap research](https://www.kkdemian.com/blog/flap-bnb-chain-programmable-launchpad-research) (search summary; exact source of each number not confirmed)
- **Four.meme mechanics:** creation costs about 0.005 BNB. Trading fee is 1% (minimum 0.001 BNB). Tokens trade on a bonding curve and then migrate to PancakeSwap. — [BingX Learn](https://bingx.com/en/learn/article/what-is-four-meme-form-bnb-launchpad-how-does-it-work); [CryptoSlate review](https://cryptoslate.com/launchpads/four-meme-review/)
- **Flap.sh mechanics:** 1% base fee per trade, split 70% to the creator and 30% to the platform. Creators can add a tax of 0–10% that cannot be changed after launch. Creation costs about 0.001 BNB. — [kkdemian Flap research](https://www.kkdemian.com/blog/flap-bnb-chain-programmable-launchpad-research); [Bitcoin Sistemi](https://en.bitcoinsistemi.com/top-3-memecoin-launchpads-on-bnb-to-watch-four-meme-flap-and-memetoro-as-ai-launches-gain-ground/)

### Inferences
- BSC meme activity is strongly driven by catalysts: posts from CZ or Binance, and listing or Alpha hopes. A BSC bot should watch the social accounts of CZ, He Yi and Binance alongside on-chain events.
- Flap.sh leads, and creator-set taxes of up to 10% on top of the 1% fee are now normal on BSC. A bot's PnL model on BSC must read each token's tax setting before entering. A 10%+10% round trip kills most scalping.
- The "launchpad leader" on BSC changed within about a year (four.meme to Flap.sh). Hard-coding one launchpad's contracts is fragile, so build adapters per launchpad.

### Gaps
- No PancakeSwap-specific meme volume figure was found (only BNB chain-wide meme volume).
- No Q4 2026 weekly BNB meme volume figure (latest is late Aug 2026).
- Flap.sh fee parameters were not confirmed from official docs.

---

## 3. Ethereum mainnet memes: Uniswap, gas costs, typical dynamics, tax tokens

### Takeaway
Mainnet gas in 2026 is historically low: about 0.05–0.5 gwei, so a Uniswap swap costs a few cents. The old gas barrier to meme trading on L1 is mostly gone. Even so, Ethereum memes are a small slice: about $83M/week in late Aug 2026, about 0.9% of mainnet spot DEX volume. Little specific 2026 data was found on mainnet tax tokens.

### Cited Findings
- 2026 mainnet gas: about 0.052 gwei average on 7 Apr 2026 (among the lowest readings ever recorded); about 0.16 gwei in April; about 0.15 gwei on 3 Jun. Other sources say it averages about 0.5 gwei and often dips to 0.1–0.2 gwei. Low fees are credited to Dencun blobs and activity moving to L2s. — [navcrypto](https://www.navcrypto.xyz/blog/ethereum-gas-fees-explained-2026); [BloFin Academy](https://blofin.com/academy/education/ethereum-gas); [CoinLaw](https://coinlaw.io/ethereum-gas-fee-history/)
- A Uniswap swap is about 150K gas, roughly $0.03–0.06 at 2026 prices (about $0.06 with ETH near $1,900). One source still quotes $2–8 per swap as of March 2026, so sources conflict and the figure depends on the date. — [BloFin Academy](https://blofin.com/academy/education/ethereum-gas); [plisio](https://plisio.net/education/crypto-gas-fees)
- Uniswap v3 pool fee tiers run from 0.30% to 1.00% for meme-type pairs. — [cryptonewsnavigator](https://www.cryptonewsnavigator.com/academy/article/where-to-buy-meme-coins-without-getting-wrecked-by-fees-in-2026)
- Launching a meme on Ethereum is described as costing $5–100 in ETH depending on gas, versus under $1 on Solana. — [20lab](https://20lab.app/generate/memecoin/) (vendor)
- Week ending 26 Aug 2026: Ethereum meme volume was about $82.9M out of $9.6B weekly spot DEX volume (about 0.9%). — [Cryptobriefing](https://cryptobriefing.com/solana-reclaims-memecoin-volume-robinhood/)
- Around October 2025, Ethereum was reported at about 20% of meme DEX volume across chains. — [CoinGape](https://coingape.com/binance-chain-overtakes-solana-in-memecoin-trading-volume/)
- **Academic background on ETH and BSC tokens (2022):** sniper bots buy indiscriminately from every new liquidity pool. Sniper bots make up a much larger share of swaps on BSC than on Ethereum (3.5% of the total). Token spam and rug pulls are widespread on both chains. — [arXiv 2206.08202](https://arxiv.org/pdf/2206.08202)

### Inferences
- Since gas now costs cents, the main friction in mainnet meme trading is slippage, LP fees of 0.3–1%, tax tokens, and MEV (public mempool, sandwiching through builders), not gas. Mainnet is the only chain covered here with a fully public mempool and a PBS/builder market. Bots should send transactions through private RPCs (Flashbots Protect, MEV-Blocker) to avoid being sandwiched. That is a general known practice, not confirmed by sources gathered here.
- The 20% share (October 2025) versus the 0.9% meme share of spot volume (August 2026) are different metrics, so they cannot be read as a trend.

### Gaps
- No 2026 data on how common Ethereum "tax tokens" are (buy/sell taxes), their typical rates, or whether the 2023–2024 tax-token culture continued. Searches returned nothing relevant.
- No mainnet-specific launchpad data (for example, whether any bonding-curve launchpad has meaningful mainnet share in 2026).

---

## 4. EVM-specific risks and mechanics: transfer taxes, blacklist functions, honeypots, Uniswap v4 hooks

### Takeaway
EVM tokens are arbitrary contracts, unlike Solana SPL tokens from Pump.fun, which use a standard program. A bot must therefore simulate every buy and sell before trading. Fee-on-transfer taxes (often dynamic or raised by the owner), blacklists, trading toggles and mint functions are the classic traps. Uniswap v4 hooks add a new layer: pricing and fee logic can sit in the hook rather than the token. A 0x analysis (September 2026) classed 54% of about 84K hooks as malicious.

### Cited Findings
- **Honeypot detection by simulation:** Honeypot.is simulates a buy and then a sell to detect honeypots, and supports Ethereum, BSC and Base. — [honeypot.is](https://honeypot.is/)
- **Static checks:** BSC detectors inspect bytecode for blacklist functions, transfer restrictions and owner-controlled permissions. — [WalletFinder.ai](https://walletfinder.ai/blog/bsc-honeypot-detector) (vendor)
- An open-source EVM new-token scanner, which watches DEX factory events over WebSocket and runs 5 heuristics, does *not* detect honeypots. It notes that this would need a buy/sell round trip simulated with eth_call on forked state. — [GitHub swiftnodes/memecoin-scanner](https://github.com/swiftnodes/memecoin-scanner)
- **Dynamic sell tax:** some tokens ramp the sell tax to extreme levels, so the sell transaction succeeds but the seller gets almost nothing. — [TokenToolHub](https://tokentoolhub.com/honeypots-on-base-and-l2-chains/)
- **L2 ordering:** sequencing reduces some public-mempool MEV but concentrates ordering power. Base runs a single sequencer, and submission goes through private or sequencer RPC routes (vendor claim). — [TokenToolHub](https://tokentoolhub.com/honeypots-on-base-and-l2-chains/); [terminal-memecoin.com](https://terminal-memecoin.com/) (vendor)
- **MEV bots as targets:** a 2023 attack used a Flashbots relay flaw, plus honeypot transactions that lured sandwich bots, to drain MEV bots of about $20M. — [BlockSec](https://blocksec.com/blog/harvesting-mev-bots-by-exploiting-vulnerabilities-in-flashbots-relay)
- **Uniswap v4 hooks:** 0x analyzed 84,163 hooks across 6 chains (as of 11 Sep 2026). It classed 54.2% as malicious, 26.4% as suspected and 19.4% as safe. Some hooks quote one price when the swap is requested and settle at another, so users can receive up to 50% less than quoted. — [KuCoin flash (0x report)](https://www.kucoin.com/news/flash/uniswap-v4-hooks-19-4-safe-over-half-malicious-0x-analysis-reveals); [KuCoin flash](https://www.kucoin.com/news/flash/0x-claims-over-half-of-uniswap-v4-hooks-are-malicious)
- Hayden Adams (Uniswap) disputes this framing. He says the risk comes from aggregators routing into hooks they have not vetted. Uniswap's frontend and API use only reviewed hooks, and Uniswap's core contracts have never been exploited. Calling contracts directly on-chain is the riskiest path. — [KuCoin flash](https://www.kucoin.com/news/flash/meme-coins-and-uniswap-v4-pools-pose-high-risks-for-investors)
- For hook-based assets, checking the token for a transfer tax, blacklist or mint is no longer enough, because minting, fee distribution and pricing can live in hook logic. Hook-based memes such as SATO have seen multiples of tens of times in short periods. — [KuCoin flash](https://www.kucoin.com/news/flash/meme-coins-and-uniswap-v4-pools-pose-high-risks-for-investors); [Bitget Wallet on X](https://x.com/BitgetWallet/article/2054168094604759402)
- Beosin documents classes of v4 hook vulnerabilities (access control on callbacks, delta accounting and similar). — [Beosin](https://beosin.com/resources/uniswap-v4-hook-security-architecture-common-vulnerabilities-and-mitigation-practices)
- **Launchpad-level taxes:** Flap.sh lets creators set a 0–10% tax that is fixed at launch. Clanker takes a 0.2% protocol fee per trade. — [kkdemian](https://www.kkdemian.com/blog/flap-bnb-chain-programmable-launchpad-research); [Datawallet](https://www.datawallet.com/crypto/farcaster-explained)

### Inferences
- **Bot checklist for EVM, compared with Solana:**
  - Run a buy→sell→transfer simulation on forked state (eth_call or Anvil) for every token, including the v4 hook path.
  - Decode tax variables and owner functions (setFee, blacklist, pause/enableTrading, mint, maxTx/maxWallet).
  - Check LP lock or burn and owner renouncement.
  - Read launchpad metadata. Flap's fixed tax and Clanker/Zora standard templates are much safer than arbitrary contracts.
  - Prefer standard-template launchpad tokens.
- Tokens from standard launchpads (four.meme, Flap, Clanker, Zora) behave more like Solana's Pump.fun tokens (known code). Tokens deployed by hand on PancakeSwap or Uniswap v2 have the highest honeypot risk.
- A bot must handle fee-on-transfer during routing. On Uniswap v2-style routers, use the `swapExactTokensForTokensSupportingFeeOnTransferTokens` functions, or the swap will revert. This is standard Uniswap v2 behaviour, not confirmed by a source gathered here.

### Gaps
- No quantitative 2025–2026 data on the honeypot rate among new BSC, Base or ETH tokens.
- The 0x report's method is unknown, and 0x has a commercial interest in routing safety.
- No source on how tax tokens are handled in Uniswap v4 or Universal Router, or by aggregators.

---

## 5. Relative market share vs Solana over time

### Takeaway
Solana has been the main memecoin venue for most of 2024–2026. EVM chains took the lead only in short bursts: Base/Zora in daily *launch counts* in July 2025, BNB in *volume and fees* in October 2025, and the new Robinhood Chain (an Arbitrum Orbit L2) in July–September 2026. By late Aug 2026 Solana had about 85% of combined weekly meme spot volume across five tracked chains. Metrics differ (launches, fees, volume), so share numbers cannot be compared directly across sources.

### Cited Findings
**Timeline**
- **Mid-2025:** Solana's share of launches was about 70%, Base about 10%, BNB about 5% (one secondary analysis). — [openliquid.io](https://openliquid.io/blog/state-of-memecoin-launches-2026/) (weak)
- **30 Jul 2025:** Zora/Base passed Pump.fun and LetsBonk in daily token creations. — [Decrypt](https://decrypt.co/332573/base-overtakes-solana-in-daily-tokens-created-as-pump-fun-continues-to-shrink); [Cryptorank](https://cryptorank.io/news/feed/e2010-base-overtakes-solana-as-a-new-memecoin-hub)
- **October 2025:** BNB had about 45% of meme DEX volume, Solana about 25%, Ethereum about 20%. Four.meme passed Pump.fun on daily revenue and launches. Solana launchpad activity reportedly fell 73% as Four.meme rose. — [CoinGape](https://coingape.com/binance-chain-overtakes-solana-in-memecoin-trading-volume/); [Cointelegraph](https://cointelegraph.com/magazine/bnb-uptober-binance-market-crash-scrutiny); [Phemex News](https://phemex.com/news/article/solana-launchpad-activity-plummets-73-as-fourmeme-gains-on-bnb-chain-25621)
- **Late 2025:** Pump.fun regained the lead. — [Bitget News](https://www.bitget.com/news/detail/12560605026593)
- **Q1 2026:** Solana about 55% of launches, Base about 25%, BNB about 5% (about 15K launches analyzed; weak source). — [openliquid.io](https://openliquid.io/blog/state-of-memecoin-launches-2026/)
- **1 Jul 2026:** Robinhood Chain launched, an Ethereum L2 on Arbitrum Orbit built for tokenized stocks, but memecoins drove its early activity. — [CoinDesk, 13 Jul 2026](https://www.coindesk.com/tech/2026/07/13/robinhood-built-a-blockchain-for-tokenized-stocks-memecoins-took-over); [crypto.news](https://crypto.news/robinhood-chain-memecoins-tokenized-stocks/)
- **August 2026:** Robinhood Chain's meme volume rose from about 3% to about 8% of Solana's across the month. — [Bitquery](https://bitquery.io/investigations/robinhood-vs-solana-memecoins); [ZyCrypto](https://zycrypto.com/solana-widens-memecoin-volume-lead-over-robinhood/)
- **Week ending 26 Aug 2026** (Blockworks data, 5 chains):
  - Solana: about $5.2B meme spot volume, about 85% of the total (highest since November 2025).
  - BNB: about $412.4M.
  - Robinhood Chain: $389.17M (20.8% of its $1.87B spot volume).
  - Ethereum: $82.9M.
  - Base: $31.06M.
  - — [Cryptobriefing](https://cryptobriefing.com/solana-reclaims-memecoin-volume-robinhood/); [SolanaFloor](https://solanafloor.com/news/solana-reclaims-memecoin-volume-dominance-from-robinhood-and-bnb-chain-capturing-85-market-share)
- **7 Sep 2026 (single day):** Solana had 67% of spot-DEX meme volume and Robinhood 23% (Blockworks). — [ZyCrypto](https://zycrypto.com/solana-widens-memecoin-volume-lead-over-robinhood/)
- **Mid-September 2026:** Pons, the launchpad behind much of Robinhood Chain's boom, saw weekly volume fall 37% to $616M (week ending 16 Sep). Robinhood Chain's daily fees later fell about 97% from their peak. — [crypto.news](https://crypto.news/robinhood-chain-memecoins-tokenized-stocks/); [BigGo Finance](https://finance.biggo.com/news/f67de482-e40f-4245-86bc-9a964ddbcbaa)
- **30 days ending 18 Nov 2026 (launchpad fees):** Pump.fun $42.78M (#1), Flap.sh (BSC) $16.51M (#2). Of the top 10 launchpads, 5 are on Solana, 2 on "Elysium", 1 on BSC and 1 on Robinhood Chain. Pump.fun reportedly took 92.8% of Q3 2026 bonding-curve volume on Solana (Blockworks, via secondary source). — [memefees.com](https://memefees.com/best-memecoin-launchpads); [crawlux / bitbank roundups](https://bitbank.nz/blog/memecoin-launchpads-compared)

### Inferences
- The pattern repeats: an EVM chain takes meme share for 2–8 weeks around a catalyst. Examples are Zora with Base App incentives (July 2025), BNB with CZ (October 2025) and Robinhood Chain's launch (July 2026). Then volume flows back to Solana. A multi-chain bot should treat EVM chains as *event-driven* venues: keep adapters ready and add capital when a rotation starts. EVM chains are not steady-state venues.
- By fee generation (November 2026), BSC through Flap.sh is the strongest EVM meme venue. Base is weakest despite heavy launch counts. Robinhood Chain is a new and volatile venue worth watching.
- "Elysium" appears in the November 2026 top 10 but was not researched. It may be a new chain worth a follow-up.

### Gaps
- No single authoritative time series (for example, a Dune dashboard) of meme volume share by chain for 2025–2026. The figures here are snapshots using different metrics.
- No Q4 2026 (Oct–Nov) chain-level meme volume shares were found. The latest volume snapshot is late Aug / early Sep 2026; the latest fee snapshot is 18 Nov 2026.
- "Elysium" (2 launchpads in the top 10 by fees) was not identified or researched.
- Direct pages (SolanaFloor, memefees, memecentral) could not be fetched because of network restrictions, so their numbers are from search summaries.
