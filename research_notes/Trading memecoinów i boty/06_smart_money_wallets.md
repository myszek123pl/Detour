# Identifying and Analyzing Profitable ("Smart Money") Wallets in Memecoin Trading: A Methodology for Bot Scoring

> Research context and constraints (read first):
> - Current as of 20 Nov 2026. This session had restricted network access: web search hit its per-turn budget part-way through, and direct fetches to nansen.ai, cryptoslate.com, arxiv.org, substack, solanacompass.com and sbfc.sydney.edu.au failed (host not allowed). Only GitHub-hosted material was fetched and read in full (memescope README, METHOD.md, test_status.json). Other findings marked "(search summary)" come from search-result summaries of the cited page, not from a full read, so treat their exact wording and numbers with more caution.
> - The notes cover methodology and aggregate findings only. No individual wallets or people are profiled.

## Q1. Metrics: which wallet metrics matter (realized/unrealized PnL, win rate, ROI distribution, hold time, entry timing vs launch, consistency, token count, position size)?

### Takeaway
Raw leaderboard metrics (PnL, win rate over 1D/7D/30D windows) are what tools show by default, but they are the least robust inputs. A bot-grade score should be built from *realized* PnL on *closed* positions, net of fees and computed per entity rather than per address. It should then be read alongside entry timing relative to launch (to catch snipers and insiders), hold time, the ROI distribution (median and tails, not just the mean), sample size, and consistency across non-overlapping windows.

### Cited Findings
- Commercial trackers report PnL and win rate over short rolling windows. GMGN wallet stats expose 1D/7D/30D PnL, 1D/7D/30D win rate, 1D/7D/30D transaction counts, realized profit, balances and tags. Scrapers store win rate in different units (0–1 vs %), which matters when comparing data. — [Apify GMGN Wallet Stat Scraper](https://apify.com/muhammetakkurtt/gmgn-wallet-stat-scraper); [Apify GMGN Smart Money Leaderboard](https://apify.com/logiover/gmgn-smart-money-wallet-leaderboard) (search summary)
- I found no official GMGN documentation defining its metrics. The definitions in circulation come from third-party guides and scrapers (e.g., win rate = % of profitable trades). — [DEXTools GMGN tutorial 2026](https://www.dextools.io/tutorials/how-to-use-gmgn-smart-money-analytics-tutorial-2026); [pumpfunguide (unaffiliated)](https://pumpfunguide.pages.dev/guides/gmgn-wallet-tracker-advanced-guide) (search summary)
- Practitioner guidance says win rate is meaningless on tiny samples ("90% win rate over 5 trades tells you nothing") and recommends at least 50–100 trades. Informal win-rate benchmarks are about 55–60% for "good" and >70% for "elite/exceptional". These thresholds are informal and not a standard. — [pumpfunguide](https://pumpfunguide.pages.dev/guides/gmgn-wallet-tracker-advanced-guide); [DEXTools GMGN tutorial](https://www.dextools.io/tutorials/how-to-use-gmgn-smart-money-analytics-tutorial-2026) (search summary)
- Nansen's performance-based "Smart Trader" labels rank wallets by PnL over fixed windows: 30D, 90D, 180D and 2Y. Wallets that stop qualifying become "Former Smart Trader". There is also a "Smart Fund" label for funds that meet Nansen's criteria. The exact thresholds (win rate, ROI, minimum size) were not visible in what I could access. — [Nansen: What is Smart Money – methodology](https://www.nansen.ai/guides/what-is-smart-money-in-crypto-a-detailed-look-into-our-methodology); [Nansen Academy: Smart Money 101](https://academy.nansen.ai/en/articles/2132837-smart-money-101); [Nansen wallet labels guide](https://www.nansen.ai/guides/wallet-labels-emojis-what-do-they-mean) (search summary; fetch blocked)
- A rigorous open-source definition of realized PnL (memescope): a "trade" is a successful transaction where the fee payer's token balance in the mint changes. `d_sol` is the payer's lamport change plus WSOL change, *including fees*. Realized P&L sums `d_sol` only for wallets whose position is *closed*, defined as having sold ≥99% of tokens bought. Open positions are excluded. — [memescope METHOD.md](https://raw.githubusercontent.com/AIpiggyyy/memescope/main/docs/METHOD.md)
- The same project defines entry-timing roles relative to launch. A **sniper** is a non-creator wallet whose first buy lands within 2 slots of token creation. A **bundle** buyer is a non-creator wallet buying in the creation slot itself (a bundled launch has ≥2 of them). — [memescope METHOD.md](https://raw.githubusercontent.com/AIpiggyyy/memescope/main/docs/METHOD.md)
- Base rates show why the median matters more than leaderboard tails. In memescope's sample (1,161 Solana pump.fun launches, 6–10 Oct 2026), only 16.1% of *independent* (non-insider) wallets with ≥1 closed position were net profitable, and the median independent wallet's realized P&L was −0.014 SOL. The median token had just 3 distinct wallets. — [memescope README](https://github.com/AIpiggyyy/memescope)
- Population profitability swings with market regime and survivorship. CoinGecko's realized-PnL tracking of Pump.fun traders shows the profitable share below 50% in most months from April 2024, as low as 30.1% in June 2025, and 73.3% in April 2026. The rise was reportedly attributed to unprofitable traders leaving, not to better odds. — [CoinGecko Research: Pump.fun Traders Are Making a Comeback](https://www.coingecko.com/research/publications/pump-fun-traders-are-making-a-comeback); [CoinInsider](https://www.coininsider.org/news/pump-fun-hits-two-year-high-as-73-of-traders-turn-profitable-in-april-2026/) (search summary)
- A separate sample of wallets trading 921 new pump.fun coins: 69.1% lost money, 12.6% ended about even, 18.2% made money. — [Alchemii: Is Meme Coin Trading Profitable? Real Wallet Data](https://www.alchemii.io/blog/is-meme-coin-trading-profitable) (search summary; I could not confirm which result page this figure came from, so the attribution is uncertain)
- A Cielo reviewer notes that PnL figures can be skewed by honeypots, airdrops and token transfers, so realized/unrealized PnL from trackers should be treated as a starting point. — [Solana Compass: Cielo](https://solanacompass.com/projects/cielo) (search summary)

### Inferences
- **Realized vs unrealized.** Score on realized, fee-inclusive PnL from closed positions (≥99% sold, following memescope). Unrealized PnL on illiquid memecoins is mostly mark-to-model fiction: a large paper gain in a token with thin liquidity usually cannot be exited at the quoted price. Unrealized PnL should at most feed a separate, heavily discounted "open book" field.
- **ROI distribution over win rate.** Memecoin returns are extremely right-skewed. A wallet with a 30% win rate can be very profitable (a few 20–50x hits), and a 90% win rate can be negative (many small wins, rare total losses). Record per-position ROI and compute the median, the 25/75/90th percentiles, the share of PnL coming from the top 1–3 positions (concentration), and the profit factor (gross wins / gross losses). If removing the single best trade turns total PnL negative, the record is luck-dominated.
- **Entry timing vs launch.** Record the slot/second offset from token creation, and the entry's market-cap or bonding-curve percentile, for every position. Wallets whose edge sits almost entirely in the creation slot or within 2 slots (bundle/sniper) are not copyable: a follower reacting to their on-chain buy necessarily enters later and at a higher price.
- **Hold time.** Record the median and distribution of holding time per position. Very short holds (seconds) combined with very early entries point to bots or snipers. Long holds on tokens that later failed point to survivorship in the opposite direction. For copyability, hold time must comfortably exceed the follower's execution latency.
- **Consistency.** Split history into non-overlapping windows (e.g., weekly) and require positive realized PnL in a majority of them, plus positive PnL in the most recent out-of-sample window. Nansen-style rolling 30D/90D/180D windows overlap, so they overstate consistency.
- **Token count and position size.** Count distinct tokens (not transactions) as the effective sample size. Record median position size in SOL/USD and its dispersion. Very large positions relative to pool liquidity are not copyable without moving the price. Very small ones (dust) inflate win counts.

### Gaps
- Exact Nansen Smart Trader thresholds (minimum PnL, win rate, volume, wallet age) could not be read because nansen.ai was blocked in this session.
- No official GMGN, Cielo or Kolscan documentation was accessible that defines how they compute win rate (per trade vs per token, partial sells), how they treat airdropped/transferred-in tokens, or their cost basis method (FIFO vs average).
- I found no published study that gives an empirically optimal minimum trade count for memecoin wallets. The "50–100 trades" figure is practitioner folklore.

## Q2. Pitfalls: what makes wallets look profitable but not worth following (survivorship, insiders, wash/fake PnL, multi-wallet operators, bots, wallets front-running their followers, small-sample luck)?

### Takeaway
The best on-chain evidence from 2026 indicates that most large memecoin "wins" do not come from replicable trading skill. One study found that ~74% of sampled six-figure pump.fun gains failed regular-trading checks, mainly because the wallet sold tokens it had *received via transfer* (insider distribution) or traded in a coordinated way. Insiders captured ~81% of realized profit in a random launch sample. So the first job of a wallet-scoring bot is *exclusion*: strip out insiders, bundles, transfer-fed sellers, wash/volume bots, and linked wallet rings, before any ranking is done.

### Cited Findings
- **Insider/transfer-inflated PnL (Bitquery, Oct 2026).** Bitquery examined 3,170 wallet-token positions with reported gains ≥$100k on pump.fun, totalling $752.5M, between Oct 2025 and Aug 2026:
  - 51% of the gains involved wallets selling tokens they had received from other addresses.
  - 13% showed patterns of potentially coordinated trading.
  - About 10% could not be classified.
  - Only about 26% passed standard trading checks.
  - 1,104 positions were traced to token-creator-associated addresses, directly or via intermediaries.
  
  Bitquery cautioned that transfers can also occur between wallets of the same legitimate investor. It did not measure actual copy-trader outcomes. — [KuCoin News: Bitquery study (74% cannot be replicated)](https://www.kucoin.com/news/flash/bitquery-study-reveals-74-of-pump-fun-gains-cannot-be-replicated-by-copy-traders); [RootData: only 26% passed regular trading checks](https://www.rootdata.com/news/801695); [CryptoSlate](https://cryptoslate.com/pump-funs-biggest-winners-may-be-impossible-to-copy-as-752-million-study-exposes-hidden-trading-gap/) (search summaries; the original Bitquery report was not read)
- **Insider share of profit (memescope, 6–10 Oct 2026, 1,161 Solana launches).** Insiders (creator, bundle, creator-linked, coordinated, wash) captured 74–86% of realized profit by day, 80.8% overall. Other figures from the same sample:
  - 24.1% of launches were bundled in the first block.
  - 34.3% had a coordinated dump.
  - 66.9% of creators sold their entire position.
  - 12.2% of launches had transfer clusters (2,818 wallets), where insiders hand tokens to fresh wallets that then sell.
  
  The sample covers only five full days, so the headline numbers are expected to change. — [memescope README](https://github.com/AIpiggyyy/memescope)
- **Operational detection rules (memescope).** These are concrete, implementable heuristics:
  - **Creator-linked:** funded by the creator, or sharing a non-hub funder with the creator within 3 hops.
  - **Coordinated dump:** ≥3 distinct wallets among the first 20 buyers sell in the same 5-second window.
  - **Wash/volume bot:** ≥10 trades in the token with both buys and sells, where |net tokens| ≤ 1% of tokens bought and |net SOL| ≤ 2% of its SOL volume.
  - **Transfer cluster:** wallet-to-wallet token moves with no payment, where the total is conserved and no wallet's SOL changes by more than 0.01 SOL. Linked wallets are merged into one entity per token.
  - **Funding trace:** goes back up to 3 hops and stops at "hubs" (more than 2,000 txs on Solana, or known exchanges, bridges and routers).
  
  — [memescope METHOD.md](https://raw.githubusercontent.com/AIpiggyyy/memescope/main/docs/METHOD.md)
- **Deployer-funded snipers.** Pine Analytics (April 2025) found deployers funding sniper wallets that bought in the same block as launch in about 1.75% of pump.fun launches, with over 15,000 SOL in realized profit over one month. — [Pine Analytics: Exit Liquidity Machines](https://pineanalytics.substack.com/p/exit-liquidity-machines) (search summary; fetch blocked)
- **Developer-linked bundles.** A secondary report of a Bitquery analysis says 21% of pump.fun projects had developer-linked wallets in launch bundles. — [TechFlow](https://techflowpost.com/en-US/article/34706) (search summary; secondary, unverified)
- **Persistent wallet rings / sniper cohorts.** An arXiv paper studied 1,578,333 buyer observations from 166,098 pump.fun launches (12–26 June 2026) and detected 1,012 *persistent* wallet rings. It also warns that naive causal inference about first-hour buyer flow can mislead. — [Kamat, "Coordinated Sniper Cohorts on Pump.fun", arXiv:2607.02795](https://arxiv.org/abs/2607.02795); [EconPapers listing](https://econpapers.repec.org/paper/arxpapers/2607.02795.htm) (abstract-level search summary only)
- **Creators and snipers dominate top performers.** A lifecycle analysis around the $TRUMP launch found creators and snipers overrepresented among top performers. — [SBFC 2025 paper P154](https://sbfc.sydney.edu.au/2025/papers/SBFC2025_4G3_P154.pdf) (search summary; fetch blocked)
- **Coordinated multi-wallet participation** was also reported in Pump.fun's own token sale (ICO). — [Blockworks](https://blockworks.co/news/pump-fun-ico-coordinated-wallet) (title/snippet only)
- **Survivorship in aggregate stats.** The jump in Pump.fun's profitable-trader share to 73.3% (Apr 2026) was attributed to losing traders exiting rather than better odds. Any "share of profitable wallets" statistic computed on *currently active* wallets is survivorship-biased. — [CoinGecko Research](https://www.coingecko.com/research/publications/pump-fun-traders-are-making-a-comeback) (search summary)
- **Tracker PnL distortions.** Honeypots, airdrops and transfers skew tracker PnL (Cielo review). — [Solana Compass: Cielo](https://solanacompass.com/projects/cielo) (search summary)

### Inferences
- **Transferred-in tokens are the single biggest PnL artifact.** If a tracker treats tokens received for free (from the deployer or a sister wallet) as zero-cost, or ignores them, the selling wallet shows near-infinite ROI. A bot must compute cost basis at the *entity* level: merge transfer-linked wallets, as memescope's v5 does, and attribute the buy cost to whichever wallet actually paid.
- **Multi-wallet operators.** Cluster addresses by common funder (≤3 hops, stop at hubs), by same-slot co-buying across many tokens (a persistent ring, per Kamat), and by token transfers without payment. Score the *cluster*. A single address from a ring may look like a disciplined trader while the ring as a whole is the insider.
- **Bots.** Flag MEV/arbitrage/volume bots using the memescope wash rule, extremely high tx counts (hub-like), sub-second hold times, and buys in the creation slot. Their PnL depends on infrastructure (priority fees, co-location, bundles) that a follower cannot replicate.
- **Wallets that front-run their own followers.** If a wallet is publicly tracked (KOL leaderboards, GMGN "smart money" tags, Kolscan), its owner can profit from followers' latency. They buy, followers' copy-buys push the price up, and they sell into that flow. Detection signature: on tracked wallets, a large share of exits happen within seconds or minutes of the wallet's own entry, timed to coincide with a burst of small buys from many unrelated wallets after its buy. Also compare performance before and after the wallet became publicly labelled. A decay, or a shift toward faster exits after publicity, is a red flag. *(No source was found that measures this directly; this is a proposed heuristic.)*
- **Small-sample luck.** With heavy-tailed returns, one 100x hit can dominate dozens of losses and push a wallet to the top of a 7D/30D leaderboard. Leaderboards select on the maximum of thousands of noisy records, so top-ranked wallets are expected to regress strongly toward the mean (winner's curse). See Q4 for the statistical fixes.
- **Survivorship at the wallet level.** Operators abandon losing wallets and keep promoting winners. A leaderboard sampled at one point in time only shows surviving, winning addresses. Mitigation: build the candidate universe from *all* wallets trading a random sample of launches (memescope's random-sampling design), not from leaderboards.

### Gaps
- No primary study was found that quantifies follower front-running by tracked or KOL wallets, or that measures copy-trader returns. Bitquery explicitly did not measure copy-trader performance.
- memescope's pre-registered persistence test (do the top 1% of non-insider wallets in weeks 1–2 beat the median in weeks 3–4, and is copying them with ≥1 slot + 400 ms delay net-positive after costs?) had **not yet produced results**. Its status file showed only 6 days of data, "ready": false, "waiting for 28+ full days of launches". Results were expected around early November 2026 but were not available when checked. — [memescope test_status.json](https://raw.githubusercontent.com/AIpiggyyy/memescope/main/analysis/test_status.json); [memescope README](https://github.com/AIpiggyyy/memescope)
- Full text of the Kamat (arXiv) and SBFC papers and the Pine Analytics report could not be read (hosts blocked), so the details of their ring-detection methods are not captured.

## Q3. Tools: GMGN, Cielo, Nansen, Arkham, Birdeye, Solscan, Kolscan, Axiom — what they measure and how reliable they are

### Takeaway
All the retail trackers expose leaderboard-style PnL and win-rate figures, but none publishes an auditable methodology for cost basis, transferred-in tokens, or entity clustering. No independent accuracy benchmark exists. For a bot, use them for *candidate discovery and labels*, and recompute PnL from raw chain data (an RPC or indexer such as Bitquery) under your own rules.

### Cited Findings
- **GMGN:** 1D/7D/30D PnL, win rate, tx counts, realized profit, balances, tags and social profiles per wallet. It also has "smart money" and copy-trade leaderboards, widely scraped via Apify actors. No official metric definitions were found. — [Apify GMGN Wallet Stat Scraper](https://apify.com/muhammetakkurtt/gmgn-wallet-stat-scraper); [Apify GMGN CopyTrade Wallet Scraper](https://apify.com/parsebird/gmgn-copytrade-wallet-scraper); [DEXTools GMGN tutorial](https://www.dextools.io/tutorials/how-to-use-gmgn-smart-money-analytics-tutorial-2026) (search summary)
- **Nansen:** curated "Smart Money" label set of about a dozen labels as of 2026. These include performance labels ranked by PnL (Smart Trader 30D/90D/180D/2Y) and Smart Fund. Labels are non-permanent ("Former Smart Trader") and are assigned through rules, public attribution and behavioral inference. Third-party guides stress that labels describe past behavior, not future profit. — [Nansen methodology](https://www.nansen.ai/guides/what-is-smart-money-in-crypto-a-detailed-look-into-our-methodology); [Nansen Academy Smart Money 101](https://academy.nansen.ai/en/articles/2132837-smart-money-101); [Nansen API smart-money docs](https://docs.nansen.ai/api/smart-money); [DEXTools: What is Nansen (2026)](https://www.dextools.io/tutorials/what-is-nansen-onchain-analytics-guide-2026) (search summary)
- **Cielo:** described as one of the most comprehensive Solana wallet analytics platforms, with realized and unrealized PnL breakdowns. Its PnL can be skewed by honeypots, airdrops and transfers, so its leaderboards are best treated as a research starting point. — [MadeOnSol: best Solana PnL tracking tools](https://madeonsol.com/blog/best-solana-pnl-tracking-tools); [Solana Compass: Cielo](https://solanacompass.com/projects/cielo) (search summary; MadeOnSol is a directory with commercial interests)
- **Kolscan:** free per-wallet PnL focused on KOL wallets. Its default view shows only the most recent 100 transactions per wallet, which limits how complete its PnL figures are. — [MadeOnSol: Axiom vs Kolscan](https://madeonsol.com/compare/axiom-vs-kolscan) (search summary)
- **Axiom:** primarily a fast manual trading terminal with built-in wallet tracking, not a PnL-analytics tool. — [MadeOnSol: Axiom vs Kolscan](https://madeonsol.com/compare/axiom-vs-kolscan) (search summary)
- **Bitquery:** offers pump.fun/Solana APIs and publishes on-chain investigations (wash trading, sybil, transfer-fed gains), which makes it useful for raw data and independent verification. — [Bitquery Pump Fun API docs](https://docs.bitquery.io/docs/blockchain/Solana/Pump-Fun-API); [Bitquery investigation example](https://bitquery.io/investigations/token-factory-america250) (search listing)
- No independent benchmark of PnL accuracy for Cielo, Kolscan or Axiom was found. Comparison sites rest on very few user reviews (e.g., one review for Kolscan). — [MadeOnSol comparisons](https://madeonsol.com/compare/cielo-finance-vs-kolscan) (search summary)

### Inferences
- **Reliability ranking for bot use:**
  1. Your own recomputation from raw transactions, with transparent rules.
  2. Entity/label providers (Nansen, Arkham) as features and filters, especially for identifying CEX, fund and known-entity addresses that serve as hubs.
  3. Retail PnL leaderboards (GMGN, Cielo, Kolscan) for candidate generation only.
  4. Trading terminals (Axiom) for execution and watchlists, not scoring.
- **Validating any tracker:** pick ~20 wallets, recompute realized PnL by hand from Solscan or RPC history, and compare. Check specifically how each tool handles tokens transferred in, airdrops, partial sells, fees/priority fees, and closed vs open positions.
- Leaderboard visibility is itself a risk factor. Wallets on public GMGN/Kolscan/Nansen lists attract copy-flow, and that copy-flow is exactly what enables follower front-running (see Q2).

### Gaps
- **Arkham, Birdeye and Solscan:** I found no sources in this session describing their wallet-PnL or smart-money features or their reliability (the search budget ran out). The report writer should not assert specifics about them from these notes.
- No vendor discloses cost-basis method, treatment of transferred tokens, or entity-clustering methods in what I could access.

## Q4. Statistical approaches for separating skill from luck (Bayesian shrinkage, bootstrapping, out-of-sample persistence, multiple testing)

### Takeaway
The finance literature's standard toolkit transfers well and is easy for a bot to implement:
- out-of-sample persistence tests (rank on period 1, evaluate on period 2);
- bootstrap tests of whether top performers beat what luck would produce;
- false-discovery-rate control when screening thousands of wallets;
- Bayesian shrinkage of win rates and mean returns toward the population prior.

The most directly relevant memecoin application is memescope's pre-registered persistence + copy-simulation test, but it had no results yet.

### Cited Findings
- **False discovery framework.** Barras, Scaillet & Wermers (2010, *Journal of Finance*) developed a false-discovery-rate framework for estimating what fraction of funds with significant alphas are lucky rather than skilled. Bajgrowicz & Scaillet applied related false-discovery, persistence and transaction-cost tests to technical trading rules. — [Search summary referencing these works; see Lancaster eprint listing](https://eprints.lancs.ac.uk/id/eprint/169953) (search summary; primary papers not fetched)
- **Bootstrap for crypto funds.** Bianchi & Babiak (2022, *Journal of Banking and Finance*), "On the performance of cryptocurrency funds", use a panel semi-parametric bootstrap. They find luck an unlikely explanation for the extreme outperformers, but significance weakens once cross-sectional correlation in fund returns is accounted for. — [RePEc: On the performance of cryptocurrency funds](https://ideas.repec.org/a/eee/jbfina/v138y2022ics037842662200067x.html) (search summary)
- **Multiple testing.** A 2022 paper argues multiple-testing procedures weed out models whose in-sample performance is due to luck. It identifies a spurious bearish tendency of lucky trading rules in negative-return samples as the main driver of false discoveries, and it tests on cryptocurrency data among others. — [Anghel 2022 (QFFE conference)](https://qffe2022.sciencesconf.org/388832/anghel2022manconf.pdf); [CERGE-EI WP672](https://ei.cerge-ei.cz/pdf/wp/Wp672.pdf) (search summary)
- **Memecoin-specific persistence design (pre-registered 7 Oct 2026):**
  1. Remove insiders.
  2. Rank the remaining wallets by realized P&L in launch weeks 1–2 and take the top 1% (minimum 20 wallets).
  3. Test whether they beat the median wallet in weeks 3–4 at 95% confidence (one-sided bootstrap).
  4. Simulate copying with a delay of ≥1 slot + 400 ms on Solana, including slippage and fees, and require a net-positive result.
  
  If both steps pass, a "learnable edge exists". If either fails, "follow smart money" is ruled out on these venues. Results were pending (6 of the 28 required days were collected at the last status check). — [memescope METHOD.md](https://raw.githubusercontent.com/AIpiggyyy/memescope/main/docs/METHOD.md); [test_status.json](https://raw.githubusercontent.com/AIpiggyyy/memescope/main/analysis/test_status.json)
- The widely repeated claim that "95% of traders lose money" in crypto day trading appears in Cointelegraph articles without a cited primary study and should be treated as unverified. — [Cointelegraph](https://cointelegraph.com/news/day-trading-bitcoin-why-95-of-traders-lose-money-and-fail) (search summary)

### Inferences (proposed bot implementation; these are design recommendations, not sourced facts)
- **Bayesian shrinkage of win rate (Beta-Binomial).** Fit a population prior Beta(α, β) to per-wallet win/loss counts of *non-insider* wallets (method of moments or empirical Bayes). Then use the posterior mean (wins + α) / (n + α + β) and the posterior 5th percentile as the score. Given base rates of ~16–18% of wallets net-profitable (memescope, Alchemii), the prior is pessimistic, so a 4/5 wallet shrinks heavily while an 80/120 wallet barely moves.
- **Shrinkage of mean return per position.** Use a normal-normal or t-model on log(1 + ROI) per token: posterior mean = w·wallet_mean + (1 − w)·population_mean, with w = n/(n + σ²/τ²). Because of fat tails, winsorize per-position log-returns (e.g., at the 99th percentile of the population), or rank by the posterior median, so a single 100x does not dominate.
- **Bootstrap confidence on PnL.** Resample a wallet's *tokens* (not transactions, which are correlated within a token) with replacement 5–10k times. Report the 5th percentile of total or mean PnL, and require it to be > 0. Run a "leave-top-k-out" check (drop the best 1–3 tokens) as a robustness gate.
- **Null via random-entry benchmark.** For each wallet, simulate random entries into the *same tokens* at random times within its typical entry window and hold time. Skill = how much the real PnL beats this null distribution. Wallets that profit only because they entered at the creation slot will fail once entries are restricted to a follower-achievable delay.
- **Multiple testing.** When screening N wallets, control the false discovery rate (Benjamini–Hochberg on per-wallet bootstrap p-values), or apply the Barras–Scaillet–Wermers π₀ estimate to report what fraction of "significant" wallets are expected to be lucky.
- **Out-of-sample persistence as the final gate.** Rank on a formation window (e.g., 2–4 weeks), freeze the list, and evaluate on the next window. Promote only wallets that stay in, say, the top quintile out-of-sample. Re-run continuously (walk-forward), because memecoin regimes shift quickly (CoinGecko's profitable-share swings from 30% to 73%).
- **Copyability adjustment (essential).** Re-price every one of the wallet's historical entries and exits at the price a follower would have obtained after realistic latency: ≥1 slot + 400 ms, following memescope, plus the bot's own measured latency, slippage and priority fees. Score on this *follower-realized* PnL, not the wallet's own PnL. Many "skilled" wallets will drop to zero or negative under this adjustment.
- **Suggested composite score pipeline:**
  1. Universe from random launch sampling, not leaderboards.
  2. Entity clustering (funding ≤3 hops, transfer-without-payment merges, co-buy rings).
  3. Exclusion of creator, bundle, sniper (≤2 slots), creator-linked, coordinated-dump, wash-bot and transfer-fed entities.
  4. Recompute fee-inclusive realized PnL on closed positions.
  5. Follower-latency re-pricing.
  6. Gates: minimum ≥30–50 distinct tokens; bootstrap 5th-percentile PnL > 0; leave-top-3-out PnL > 0; positive in a majority of non-overlapping weeks.
  7. Shrunk win rate and shrunk mean log-ROI.
  8. Out-of-sample persistence check.
  9. Ongoing monitoring for decay after the wallet becomes publicly tracked, and for signs of exits timed into follower flow.

### Gaps
- No peer-reviewed study was found that tests persistence of individual *memecoin* wallet performance or measures realized copy-trading returns. The memescope test was the closest and was still pending.
- Classic day-trader skill-persistence studies (e.g., Taiwan day-trader literature) could not be retrieved and cited because the search budget was exhausted.
- No source specified numeric slippage/fee assumptions for realistic memecoin copy simulation; memescope's METHOD.md also leaves these unstated.
