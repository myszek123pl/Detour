# Memecoin trading strategy archetypes: entry/exit rules and evidence of performance (as of Nov 2026)

> Research-process note (for the report writer): this session hit hard limits. The shared WebSearch budget for the turn ran out after 12 searches, and WebFetch could not reach most hosts (arxiv.org, sbfc.sydney.edu.au, memefees.com, cryptoslate.com and kooroot.github.io all failed DNS resolution in the sandbox). Only github.com pages could be fetched in full. Most academic findings below therefore come from **search-result abstracts and secondary coverage, not full-text reads**. They are flagged as such. Archetypes with no sourced evidence are listed under Gaps rather than filled from memory.

## 1. Strategy archetypes: what they are and what the evidence says about each

### Takeaway
The archetypes that can be shown to make money are **structural, privileged-access or infrastructure strategies**: deployer-linked sniping, sandwich/MEV bots, and the launchpad itself. Discretionary or retail-bot archetypes (sniping without insider info, migration buys, copy-trading, CTO revivals) have **no verified positive expectancy**. Base rates in the late-2025 to 2026 regime are strongly against them.

### Cited Findings

**Launch sniping (first-block / first-seconds buys)**
- Pine Analytics ("Exit Liquidity Machines", 2025) found 4,600+ sniper wallets tied to 10,400+ unique deployers, about 1.75% of pump.fun launch activity. Deployers fund sniper wallets that have advance notice of launches. These wallets buy in the first block and sell almost immediately: 85% within five minutes, and 90% in one or two swaps. Coverage reports an 87% sniper profitability rate and over 15,000 SOL profit in one month. These figures come from secondary coverage, not the original post. — [Pine Analytics](https://pineanalytics.substack.com/p/exit-liquidity-machines); [BeInCrypto summary](https://beincrypto.com/pump-fun-meme-coin-snipers-systematic-problem)
- The same coverage says about 50% of pump.fun launches involve some sniping, mostly bots using "spray and pray". Pine's method misses deployers that route funds through proxies or burners, so 1.75% is a lower bound for insider sniping. — [BeInCrypto](https://beincrypto.com/pump-fun-meme-coin-snipers-systematic-problem); [BeInCrypto KR](https://kr.beincrypto.com/pump-fun-meme-coin-snipers-systematic-problem/)
- Lookonchain reported that one bot made about 27,000 SOL (about $6.8M) from pump.fun snipes in 30 days. This is the gross take of a single outlier, with no cost or loss accounting. — via [search summary of Odaily / Forklog coverage](https://www.odaily.news/en/post/5204196)
- A vendor states, without a source, that profitable snipers lose on 60–80% of snipes and earn their returns on the 20–40% that reach 5x or more. **Unverified vendor claim.** — [uwuu.ai](https://uwuu.ai/blog/best-pump-fun-bot)
- Academic: Ding, Lin, Luo & Xu, "Decompose Market Manipulation Strategies: Evidence from On-chain Meme Coin Market" (SSRN, 2025), studies 6,000 pump.fun coins with rat, sniper, wash-trading and comment-bot activity. Search excerpts say bot activity lifts participation and mechanically raises peak returns under the bonding-curve design, without improving average trader profitability. **Abstract or snippet only; not read in full.** — [SSRN 5953738](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5953738); [SBFC 2025 version](https://sbfc.sydney.edu.au/2025/papers/SBFC2025_4G3_P154.pdf)
- A later preprint summarising the literature says **bundle bots** appear in about 25% of meme coin projects and are associated with lower returns and shorter dump durations. It says **sniper bots** appear in most projects, with limited observable impact on performance. — [arXiv 2601.08641](https://arxiv.org/html/2601.08641v2)
- Kamat (arXiv 2607.02795, Jul 2026, revised Oct 2026) covers 1,578,333 buyer observations across 166,098 launches between 12 and 26 Jun 2026 and identifies 1,012 persistent early-buyer wallet cohorts of 2–12 wallets. Both real cohorts and activity-matched placebos are over-represented in launches that later draw high buyer flow. The author reads this as **selection, not causation**: cohorts pick launches that would do well anyway, rather than making them do well. — [arXiv abs](https://arxiv.org/abs/2607.02795); [IDEAS](https://ideas.repec.org/p/arx/papers/2607.02795.html)

**Bonding-curve momentum / "curve %" entries**
- Tarantelli, Marino, Naviglio & Lillo (arXiv 2602.14860, Feb 2026) model graduation probability as a function of SOL already in the curve. The probability rises monotonically toward 1 near the threshold. Adding behavioural and microstructure variables "significantly improves" prediction. The paper predicts success (graduation), not realised returns. **Abstract only.** — [arXiv 2602.14860](https://arxiv.org/abs/2602.14860); [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6543715)
- Graduation happens at about 85 SOL of real liquidity. One summary of the Marino et al. paper says this is about 115 virtual SOL. — [Emergent Mind](https://www.emergentmind.com/topics/pump-fun); [crypto.news](https://crypto.news/how-meme-coins-are-made-bonding-curves-pump-fun-rug-pulls/)
- Graduation labels in collector datasets carry measurement error and do not generalise over time. This undermines naive "predict graduation, buy the curve" backtests. — [arXiv 2607.02823](https://arxiv.org/pdf/2607.02823)
- An anecdotal practitioner log describes entering when the curve is at least 20% filled, targeting 2x (about $50k market cap), with a break-even limit sell as protection. **Anecdote, not evidence.** — [Notion "Trenches Risk Management Guide"](https://chatter-submarine-7de.notion.site/The-Trenches-Meme-Coin-Risk-Management-Guide-134c64af15f280599ba6ca4a7c7fc6f9)

**Migration / graduation plays (buy at or just after graduation)**
- MemeFees tracked pump.fun graduations from 3 Sep to 7 Nov 2026. The **median graduate was worth 3.8% of its graduation market cap 24 hours later, a 96.2% fall.** **From search snippet; full page could not be fetched.** — [MemeFees survival study 2026](https://memefees.com/research/memecoin-survival-2026)
- BOOST (mid-2026) sends about 20% of the liquidity previously locked in the PumpSwap pool at graduation into automatic market buys over the first five minutes after migration, and burns the tokens bought. The graduation rate reached 6.7% on one day, about 8x June's average, after BOOST launched. — [The Block, 29 Jul 2026](https://www.theblock.co/news/defi/2026-07-29-pump-fun-token-graduation-rate-jumps-boost-changes-launch-incentives-409815)
- 33% of Sep 2026 graduations took three or fewer trades to trigger, which suggests low-quality or engineered graduations. 43% of graduated tokens still traded in week five, against 1% of non-graduated tokens. The source calls graduation "a weak but real quality filter" but gives no methodology for the comparison. **Secondary aggregator built on Bitquery, Solidus and MemeFees; not independently verified.** — [GitHub market update (Nov 2026)](https://github.com/Ricosworks1/blockchain-payment-flow-analysis/releases/tag/market-update-memecoin-factory-79pct-day-one-death-rate-nov-2026)
- Liquidity right after migration is often thin (about $10–15k by one estimate), so small buys move the price 30–40%. **Blog anecdote.** — [Medium/jump_bit](https://medium.com/@jump_bit/your-pump-fun-token-just-graduated-heres-exactly-what-to-do-next-6854e9af8c34)

**Copy-trading / smart-wallet and KOL following** (overlaps with sniping and narrative entries)
- Bitquery studied 3,170 wallet-token positions with at least $100k reported gains (Oct 2025 to Aug 2026). Only about 26% passed checks for ordinary market trading. Much of the apparent profit came from tokens transferred in rather than bought, so roughly 74% of leaderboard gains cannot be replicated by copiers. Bitquery did not measure follower P&L. — [KuCoin flash](https://www.kucoin.com/news/flash/bitquery-study-reveals-74-of-pump-fun-gains-cannot-be-replicated-by-copy-traders); [CryptoSlate](https://cryptoslate.com/pump-funs-biggest-winners-may-be-impossible-to-copy-as-752-million-study-exposes-hidden-trading-gap/)
- The arXiv 2601.08641 multi-agent copy-trading system reports an estimated copier return of about 3% per trade under realistic frictions. This is a simulation in one preprint. The paper also describes KOLs who buy early, let copiers inflate the price, and then exit. — [arXiv 2601.08641](https://arxiv.org/html/2601.08641v2)
- A vendor (MadeOnSol) argues that win rate is the wrong metric for memecoins and that profit factor is better. It also notes that sniper and MEV wallet stats cannot be replicated by copying. **Vendor content.** — [MadeOnSol](https://madeonsol.com/blog/profit-factor-percentile-rank-kol-wallet-selection-solana)

**CTO (community takeover) revivals**
- I found no dataset on CTO success rates. Sources call the base rate "low" without a number. BILLY (Solana) is the main documented revival case: the dev abandoned it and the community kept it alive. — [crypto.news CTO explainer](https://crypto.news/what-is-a-community-takeover-cto-when-a-memecoins-holders-seize-the-wheel/); [Decrypt on BILLY](https://decrypt.co/241846/how-solana-meme-coin-billy-survived-being-abandoned-by-its-dev)
- An unvetted 2026 blog claims that 73% of launches with under $5k first-hour volume never recover. **Methodology unverified.** — [openliquid "State of memecoin launches 2026"](https://openliquid.pages.dev/blog/state-of-memecoin-launches-2026)

**MEV / sandwich and "market-making" bots (infrastructure archetype)**
- Sandwich bots grossed $29.7M from 6.85M attacks across 2,545 bot wallets between 30 Oct 2025 and 7 Oct 2026. 96% of the attacks were on pump.fun. This comes from an aggregator citing Bitquery. — [GitHub market update](https://github.com/Ricosworks1/blockchain-payment-flow-analysis/releases/tag/market-update-memecoin-factory-79pct-day-one-death-rate-nov-2026)
- Token makers are highly concentrated: 1.26M wallets made launches, and the top 524 (0.04%) made 48% of them. In 451,402 "curve-skip" pools, 99% were drained by the developer, at a median of 12 minutes. — [GitHub market update](https://github.com/Ricosworks1/blockchain-payment-flow-analysis/releases/tag/market-update-memecoin-factory-79pct-day-one-death-rate-nov-2026)

### Inferences
- The strategies with documented positive results all have a **structural edge**: advance knowledge of the launch (deployer-funded snipers), transaction ordering (sandwich/MEV), or fee capture (the launchpad, prolific deployers). A retail "sniper" using a public bot competes against these players and is likely to be their exit liquidity.
- Migration buying looks **structurally negative-expectancy in the late-2026 regime**. The median graduate lost 96% within 24 hours (Sep–Nov 2026). BOOST pulls buy demand into the first five minutes. Many graduations are engineered. Any edge would have to come from strict filtering in the right tail (the 43% that still trade in week five), and nothing cited here shows such a filter works out-of-sample.
- Bonding-curve momentum has **real predictive signal for graduation**: curve fill is monotonic in graduation probability. But graduation is not profit, given what happens to graduates afterwards. The likely failure mode is a strategy that buys at 70–90% curve fill, sees the coin graduate, and is then exited into the post-graduation dump.
- Kamat's selection-not-causation finding means "follow the persistent sniper cohorts" may still be a useful **selection signal**, but copiers enter after the cohort, at worse prices.

### Gaps
- **Narrative rotation, breakouts on established memes, and mean-reversion on large caps (DOGE/PEPE/WIF/BONK):** I found no backtest or academic study in this session because the search budget ran out before I could cover these. No claims are made.
- **Dip-buy after the first dump:** I found no sourced stats on how often tokens recover after the first 50–80% drawdown. The 79% launch-day death rate and the 96% median post-graduation fall are the closest proxies, and both point against it.
- **Volume-bot / market-making services (paid volume to trend on DexScreener):** I found no profitability data. Only the sandwich-bot revenue figures above are available.
- **"Runner" holding (long-term memecoin hold):** I found no cohort data on 3–12-month returns of graduated tokens.
- **CTO success rate:** no dataset exists in what I found.
- Full texts of Ding et al., Marino et al., Kamat, and MemeFees could not be read (hosts blocked), so their effect sizes, conditional probabilities and robustness checks remain unknown.

## 2. Typical entry filters and exit rules (TP ladders, trailing stops, time stops, stop-losses)

### Takeaway
Practitioner and bot defaults converge on one template. The entry gate is safety filters (mint and freeze authority revoked, dev history, top-holder concentration, bundle checks, liquidity band). The exit is a take-profit ladder, usually "take out initials at 2x", plus a hard stop at -30 to -40%, a trailing stop that arms after a large gain, a time stop, and an automatic sell on a liquidity drop. **None of the specific percentages are backed by published backtests.** They are heuristics.

### Cited Findings
- **Open-source sniper bot defaults** (vineetdev02/Memcoin-Sniper-Bot, read in full):
  - Entry: pool liquidity between $5k and $500k, rejecting pools "too thin to exit, or too deep to still be early".
  - Weighted filters: honeypot simulation (weight 15), dev-wallet rug history (12), mint authority (10), freeze authority (10), top-holder concentration (8), bundled-launch detection (8), insider funding (6). Also LP-locked, volume velocity, curve demand, anti-sniper-war and social-signal checks.
  - Any hard fail rejects the pool; otherwise the weighted score must be at least 70. Evaluation happens 90 seconds after the pool appears, not in the first block.
  - Exits: TP ladder of 25% at +50%, 25% at +100%, 25% at +300%, and 15% at +900%. Hard stop at -40%. Trailing stop arms after +200%. A time exit applies to positions that "never move". A rug watcher force-sells on a sharp LP drop. A move of 3x or more in one poll must be confirmed on the next poll.
  - Risk: 1% of bankroll per trade, at most 10 open positions, 30% exposure cap. A 10% daily loss or 20 consecutive losses pauses trading for 24h; a 25% weekly loss pauses it for 72h.
  - The author says the published numbers come from a synthetic feed and that "nobody knows yet" whether the strategy makes money. The pass targets (200+ trades, win rate above 15%, Sharpe above 1.5) are goals, not results.
  - — [GitHub vineetdev02/Memcoin-Sniper-Bot](https://github.com/vineetdev02/Memcoin-Sniper-Bot) (a mirror exists at [jakemcnamee04-web](https://github.com/jakemcnamee04-web/Memcoin-Sniper-Bot))
- **"Initials at 2x"** is the most common practitioner rule: sell enough at 2x to recover the starting capital. — [DexTools take-profit tutorial](https://www.dextools.io/tutorials/memecoin-trading-strategy-take-profits); [AirdropAlert](https://airdropalert.com/blogs/take-profit-strategy-meme-coins/)
- **Ladder variants:**
  - Sell 50% at 2x, keep 25% as a "moon bag", and run 25% with a trailing stop.
  - Sell 50% at 2x, then 20% of the remainder at 5x, another 20% at 10x, and let the last 10% ride.
  - — [blocklr guide](https://blocklr.pages.dev/guides/meme-coin-trading); [DexTools pro guide 2026](https://www.dextools.io/tutorials/how-to-trade-meme-coins-professional-guide); [MadeOnSol exit guide](https://madeonsol.com/blog/solana-memecoin-exit-strategy-guide)
- **Trailing stops:** one rule trails 30% from the high once the position reaches 2x. Another exits if a 5x position falls 30% from its high. — [Trojan risk-management blog](https://trojan.com/blog/solana-memecoin-risk-management); [Altrady](https://www.altrady.com/blog/crypto-trading-strategies/how-to-trade-memecoins)
- **Execution realities that undermine stops in illiquid markets:**
  - 57% of pump.fun tokens finished all trading within five minutes, and 35% within one minute.
  - The pump.fun fee is 1.70% all-in per trade after the 17 Oct 2026 change, so a round trip costs about 3.4% before slippage, priority fees and MEV.
  - Sandwich attacks are concentrated on pump.fun.
  - — [GitHub market update](https://github.com/Ricosworks1/blockchain-payment-flow-analysis/releases/tag/market-update-memecoin-factory-79pct-day-one-death-rate-nov-2026)
  - After migration, thin pools (about $10–15k) mean small orders move the price 30–40%. — [Medium/jump_bit](https://medium.com/@jump_bit/your-pump-fun-token-just-graduated-heres-exactly-what-to-do-next-6854e9af8c34)
- Pine's insider snipers effectively run a **time stop of about five minutes**: 85% sell within five minutes, and 90% in one or two swaps. This is the most successful documented exit pattern, but it depends on buying in the first block with insider timing. — [BeInCrypto](https://beincrypto.com/pump-fun-meme-coin-snipers-systematic-problem)
- Practitioner content puts the memecoin trade loss rate at about 80%. This is uncited in the source. — [search summary of DexTools/Trojan guides](https://www.dextools.io/tutorials/how-to-trade-meme-coins-professional-guide)

### Inferences
- A stop-loss in these markets is a **soft limit, not a guarantee**. When 35% of tokens stop trading within a minute and rugs drain LP in about 12 minutes (median), the realised loss on a stopped-out trade is often much worse than -30 or -40%. Expectancy models should assume heavy gap risk, with many losses near -100%.
- With fees of about 3.4% per round trip on the curve plus slippage and MEV, a ladder whose first rung is +50% needs a high hit rate on that rung just to break even. The 60–80% loss-rate figure (unverified) implies that the right tail must carry all the profit, which pushes strategies toward holding a runner.
- Frequently cited rules such as "initials at 2x" and "trail 30%" are **risk-management and psychology heuristics, not optimised parameters**. I found no backtest that compares ladder designs.

### Gaps
- I found no public backtest or live P&L for any open-source memecoin bot configuration. The one well-documented bot explicitly has no results.
- I found no data on the trail distances or time-stop durations that work best, and no data on how slippage affects stop fills on pump.fun or PumpSwap.
- Defaults in commercial terminals (Axiom, Photon, BullX, GMGN, Trojan auto-sell presets) were not researched because the search budget was exhausted.

## 3. Evidence on which archetypes have positive expectancy, and in which market regimes

### Takeaway
Population-level evidence shows that **the median participant loses**, and only a tiny fraction realise meaningful profit. The regime got much worse from early 2025 to late 2026: market cap, launchpad revenue and new users fell about 80% or more, while token issuance stayed high. Fewer buyers chasing the same token supply means less exit liquidity for every non-privileged strategy.

### Cited Findings
- **Distribution of trader profit (Dune, Jan 2025, Adam Tehc):**
  - About 0.41% of 13.55M pump.fun wallets (about 55k) realised more than $10k profit. 0.048% realised more than $100k, and 0.00217% (about 293 wallets) more than $1M.
  - The pump.fun founder disputed the figures, saying they count bot or AI-agent wallets and ignore post-Raydium trades.
  - — [Decrypt](https://decrypt.co/300403/pump-fun-traders-millionaires); [Cointelegraph](https://cointelegraph.com/news/pump-fun-crypto-traders-majority-do-not-realize-profits-dune-data)
  - A March 2026 Dune tally reportedly found that more than 50% of tracked wallets ended a month in loss, with only 2 wallets above $1M realised. This is from a search summary; the original was not verified. — [search summary of cryptometer coverage](https://www.cryptometer.io/news/pump-fun-data-shows-most-traders-havent-locked-major-gains/)
- **Late-2025 to 2026 trader outcomes (Bitquery, via aggregator):** 2.9M wallets were sampled. The median loss was $13 and aggregate losses were about $269M. 74% of buyers were underwater within two weeks. — [GitHub market update](https://github.com/Ricosworks1/blockchain-payment-flow-analysis/releases/tag/market-update-memecoin-factory-79pct-day-one-death-rate-nov-2026)
- **Token base rates:**
  - Solidus Labs classified 98.6% of more than 7M pump.fun tokens (Jan 2024 to Mar 2025) as rug pulls or pump-and-dumps. — [Solidus Labs 2025 Rug Pull Report](https://www.soliduslabs.com/reports/solana-rug-pulls-pump-dumps-crypto-compliance)
  - 79% of pump.fun tokens (Nov 2025 to Oct 2026) never traded after launch day, against 84% on Raydium LaunchLab and 51% on Meteora DBC. — [GitHub market update](https://github.com/Ricosworks1/blockchain-payment-flow-analysis/releases/tag/market-update-memecoin-factory-79pct-day-one-death-rate-nov-2026)
  - Only 1 in 437 tokens had 10 or more trades in week five. — [GitHub market update](https://github.com/Ricosworks1/blockchain-payment-flow-analysis/releases/tag/market-update-memecoin-factory-79pct-day-one-death-rate-nov-2026)
- **Graduation rates (conflicting, regime-dependent):**
  - Overall 1 in 58. By launch cohort, 1 in 144 for Nov 2025 and 1 in 32 for Aug 2026. — [GitHub market update](https://github.com/Ricosworks1/blockchain-payment-flow-analysis/releases/tag/market-update-memecoin-factory-79pct-day-one-death-rate-nov-2026)
  - Weekly average of 0.26% in June 2026, before BOOST. — [GitHub market update](https://github.com/Ricosworks1/blockchain-payment-flow-analysis/releases/tag/market-update-memecoin-factory-79pct-day-one-death-rate-nov-2026); [CryptoWire](https://www.cryptowire.in/blog/memecoin-market-cap-stalls-near-30-billion-as-pumpfun-activity-sits-80-below-peak/)
  - A 6.7% one-day peak after BOOST. — [The Block](https://www.theblock.co/news/defi/2026-07-29-pump-fun-token-graduation-rate-jumps-boost-changes-launch-incentives-409815)
  - Studies give a range of 0.198% to 5%. — [Coinpaprika](https://coinpaprika.com/education/token-graduation-mean-numbers/)
- **Regime:**
  - Memecoin market cap fell from about $135–150B (Nov–Dec 2024) to $29.9B (18 Oct 2026). — [CryptoWire](https://www.cryptowire.in/blog/memecoin-market-cap-stalls-near-30-billion-as-pumpfun-activity-sits-80-below-peak/); [GitHub market update](https://github.com/Ricosworks1/blockchain-payment-flow-analysis/releases/tag/market-update-memecoin-factory-79pct-day-one-death-rate-nov-2026)
  - pump.fun daily revenue fell from about $4.8M (early 2025) to about $800k (mid-2026), with a low of about $458k on 7 Jun 2026 per Blockworks-sourced reporting. — [Incrypted](https://incrypted.com/en/memecoin-boom-fades-pump-fun-revenue-plunged/); [CryptoWire](https://www.cryptowire.in/blog/memecoin-market-cap-stalls-near-30-billion-as-pumpfun-activity-sits-80-below-peak/)
  - pump.fun daily new users fell from 174,250 (Jan 2026) to about 20,000 (Jun 2026). — [Memeburn](https://memeburn.com/memecoin-market-is-running-out-of-buyers-not-coins/)
  - Solana memecoin fees fell from 33,000 SOL/day (Jan 2026) to 5,300 SOL/day (Jun 2026). Launches stayed at about 32k per day (median), with pump.fun's share rising from 65% to 90%. — [GitHub market update](https://github.com/Ricosworks1/blockchain-payment-flow-analysis/releases/tag/market-update-memecoin-factory-79pct-day-one-death-rate-nov-2026)
- **Concentration of outcomes:** about 12 tokens (roughly 0.00009% of launches) reportedly captured more than 55% of pump.fun's total FDV. — [search summary of Fortune / Forklog coverage](https://fortune.com/crypto/2024/08/07/memecoins-are-the-hottest-sector-in-crypto-but-97-of-them-are-already-dead/)

### Inferences
- **Verified positive expectancy:** only (a) insider or deployer-linked sniping (87% profitable per Pine; this is market manipulation, not a replicable strategy), (b) sandwich/MEV bots (about $29.7M gross per year on pump.fun), and (c) the launchpad and prolific deployers (fees). These are the "house" side of the market.
- **Unverified or likely negative for outsiders:**
  - Public sniping bots (vendor claims only).
  - Bonding-curve momentum (graduation is predictable, but there is no return study).
  - Migration buys (median -96% at 24h in Sep–Nov 2026).
  - Copy-trading (about 74% of top gains cannot be copied; one simulation shows about +3% per trade).
  - CTO revivals (no base-rate data).
- **Regime dependence:** the only time aggregate retail participation was large enough to make momentum and runner strategies look profitable was the Q4 2024 to Q1 2025 boom. Since then, buyers have fallen about 88% while issuance stayed constant. Every strategy that relies on later buyers (breakouts, migration, runners, CTO) has less exit liquidity. In this regime, survivorship bias in trader write-ups ("my 100x") is especially misleading.
- Separating evidence quality for the report writer:
  - **Strongest:** Dune wallet-profit distribution (primary data, but disputed), Solidus Labs (firm report), Pine Analytics (on-chain, secondary coverage).
  - **Moderate:** Bitquery studies (single vendor, method not peer-reviewed), MemeFees (snippet only).
  - **Weakest:** vendor and terminal blogs (BullX, Trojan, DexTools, uwuu, MadeOnSol, openliquid), which have a commercial interest in promoting trading.
  - The academic preprints (Marino et al., Ding et al., Kamat, 2601.08641) are relevant but were read only as abstracts.

### Gaps
- I found no independent, peer-reviewed backtest that reports net-of-fee expectancy for any memecoin strategy archetype.
- I found no regime-split (bull vs bear memecoin market) performance data for any archetype.
- I found no data on large-cap memecoin (DOGE/SHIB/PEPE/WIF/BONK) momentum or mean-reversion strategies. Searches were blocked by the exhausted budget.
- I could not reconcile the conflicting graduation-rate figures (0.26% weekly, 1/58 overall, 1/32 for the Aug 2026 cohort, a 6.7% daily peak). They probably reflect different windows and the BOOST change, but this needs verification on Dune or Bitquery.
- Hosts that need allowlisting to verify full texts: arxiv.org, papers.ssrn.com, sbfc.sydney.edu.au, memefees.com, cryptoslate.com, pineanalytics.substack.com, kooroot.github.io (a "Pump.fun Bot Research" project page that may contain an independent backtest).
