# Academic and Quantitative Research on Memecoins and Pump-and-Dump Schemes

> Method note (read first): research was done on 2026-11-20 using web search only. Every direct fetch of full texts failed because the session's network blocks arxiv.org, alphaxiv.org and tylermoore.utulsa.edu (DNS resolution refused). The shared web-search budget then ran out partway through. So the figures below come from search-engine summaries and abstracts of the papers, not from reading the PDFs. Treat exact numbers as "abstract-level" and check them against the PDFs before quoting in a final report. Several arXiv IDs carry 2026 dates (26xx.xxxxx). These are recent preprints and none are peer-reviewed unless stated.

## 1. Papers on pump.fun / Solana memecoins: return distributions, graduation rates, survival, bot activity share

### Takeaway
The pump.fun literature (2025-2026, mostly arXiv preprints) agrees that almost all launches fail. Only about 0.6-1% (at most ~2%) of tokens "graduate" from the bonding curve to a DEX, and the platform dominated Solana token creation in late 2024. Manipulation is widespread and industrialised: wash trading, sniping, bundling, clone "factories" and Market-Manipulation-as-a-Service. Among memecoins with >100% returns, ~83% show signs of artificial growth.

### Cited Findings

**Graduation rates and survival**
- **Mancino, "The Memecoin Phenomenon: An In-Depth Study of Solana's Blockchain Trends" (arXiv 2512.11850, Dec 2025; published at IEEE ISCC 2025).** Sample: on-chain data for Q4 2024 (Oct-Dec 2024). Findings:
  - Pump.fun minted up to **71.1% of all tokens on Solana**.
  - It contributed **40-67.4% of all Solana DEX transactions**.
  - The graduation rate (bonding curve to DEX) **peaks at under 2%**.
  - The paper covers market share and activity, not return distributions.
  - Sources: [arXiv abs](https://arxiv.org/abs/2512.11850); [HTML](https://arxiv.org/html/2512.11850v3)
- **Marino, Naviglio, Tarantelli & Lillo, "Predicting the success of new crypto-tokens: the Pump.fun case" (arXiv 2602.14860, Feb 2026; also on SSRN 6543715).** Sample: September 2025.
  - Only **4,338 coins graduated, a graduation frequency of about 0.63%**.
  - **Median time to graduation was about 4.4 minutes**.
  - The authors model graduation probability from the SOL locked in the bonding curve plus launch-structure and trader-behaviour variables. Conditioning on these variables improves predictive power.
  - The authors frame the results as evidence on early-stage speculation, manipulation and the informational efficiency of bonding-curve launches.
  - Sources: [arXiv](https://arxiv.org/abs/2602.14860); [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6543715)
- **"Meme Coin Factories: Uncovering Large-Scale Manipulations on pump.fun" (arXiv 2609.10246, Sep 2026).** Associated author: Enze "Alex" Liu, per alphaXiv. Sample: all **~15 million coins launched over two years**, plus random samples of transactions.
  - Graduation rate: **original coins 1.03% (4,524 coins) vs. clones 0.66% (7,400 coins)**.
  - Graduation is more likely with fewer launch attempts, less automation, and a medium-to-longer interval between coin creations.
  - Sources: [arXiv HTML](https://arxiv.org/html/2609.10246v1); [alphaXiv author page](https://www.alphaxiv.org/@enze-alex-liu)
- **Kamat, "Pump.fun Graduation Regime Windows: Survival Analysis of 832,941 Token Launches and the Social-Presence Effect" (arXiv 2607.02823, 2026, corrected v2/v3).**
  - Uses Kaplan-Meier and Cox proportional-hazards models on 832,941 launches.
  - The original pooled graduation rate was **0.198%**.
  - **The author issued corrigenda and a measurement-error audit.** The collector only observed about **6 minutes after each launch**, so 0.198% is a "fast-regime" rate, not a 24-hour graduation rate.
  - The paper reports a "social-presence effect": tokens with social links behave differently.
  - **Caveat:** secondary sources still quote "0.2% graduate" from this paper. That use is wrong.
  - Sources: [arXiv HTML v3](https://arxiv.org/html/2607.02823v3); [audit PDF](https://arxiv.org/pdf/2607.02823); [Brave New Coin, author's own piece](https://bravenewcoin.com/insights/what-auditing-832941-pump-fun-launches-taught-me-about-memecoin-success)
- **"Do Two On-Chain Observation Pipelines See the Same Tokens? Cross-Pipeline Coverage on the Solana pump.fun Launchpad" (arXiv 2609.18975, 2026).** This is a methodological paper showing that data-collection pipelines differ in which tokens they capture. It supports the point that pump.fun statistics depend heavily on the data source — [arXiv](https://arxiv.org/pdf/2609.18975)

**Manipulation, bots, rug pulls**
- **Mongardini & Mei, "A Midsummer Meme's Dream: Investigating Market Manipulations in the Meme Coin Ecosystem" (arXiv 2507.01963, Jul 2025).** Sample: **34,988 tokens across Ethereum, BNB Smart Chain, Solana and Base**.
  - Among **high-return tokens (>100%), 82.6% show extensive use of artificial growth strategies**. The full PDF says 82.8%, so the versions differ slightly.
  - Manipulation types:
    - wash trading;
    - a newly defined form, **Liquidity Pool-Based Price Inflation (LPI)**, where small strategic buys in thin pools trigger large price jumps.
  - Wash-traded tokens see an **average of 3.63 wash-trading operations (median 3)**.
  - Profit-extraction schemes (pump-and-dumps, rug pulls) typically follow these initial manipulations.
  - **Solana shows the highest rate of losses** among the chains studied.
  - Sources: [arXiv abs](https://arxiv.org/abs/2507.01963); [ADS](https://ui.adsabs.harvard.edu/abs/2025arXiv250701963M/abstract); [RePEc](https://ideas.repec.org/p/arx/papers/2507.01963.html)
- **Ding, Lin, Luo & Xu, "Decompose Market Manipulation Strategies: Evidence from On-chain Meme Coin Market" (SSRN 5953738).** Uses Pump.fun data and splits manipulation into four strategies:
  - **"rat" trading and sniping**: concealed accumulation and front-running;
  - **wash trading**: fabricated activity;
  - **comment bots**: fabricated sentiment.
  - **Creators or snipers profit from concealed low-cost accumulation.**
  - Source: [SSRN](https://papers.ssrn.com/sol3/Delivery.cfm/5953738.pdf?abstractid=5953738&mirid=1)
- **Meme Coin Factories (arXiv 2609.10246)** groups manipulation into five categories:
  - wash trading;
  - creator-address obfuscation;
  - coordinated selling;
  - copycat (clone) coins;
  - social-media manipulation.

  Other findings:
  - Manipulators often **bypass the pump.fun interface and trade directly on-chain**, using automated low-latency strategies.
  - The authors document **"Market-Manipulation-as-a-Service"** tools that need no technical skill.
  - Clones skip the "pump" vanity address suffix more often (**30.37% vs 19.20%**), which points to more automation.
  - In one case study, influencers tweet and create a coin at the same time, which could extract millions.
  - Sources: [arXiv](https://arxiv.org/html/2609.10246); [PDF](https://arxiv.org/pdf/2609.10246)
- **Copy trading and bots: "Resisting Manipulative Bots in Meme Coin Copy Trading: A Multi-Agent Approach with Chain-of-Thought Reasoning" (arXiv 2601.08641, 2026).**
  - "Smart-money" wallets average about **14% return per trade**.
  - The estimated copier return is only about **3% per trade after realistic frictions**.
  - Manipulative bots target copy-traders.
  - Sources: [arXiv](https://arxiv.org/pdf/2601.08641); [HTML v2](https://arxiv.org/html/2601.08641v2)
- **Other relevant 2026 preprints.** Titles and topics were confirmed by search; their numbers were not retrieved.
  - "From Hype to Collapse: Investigating Rug Pull Scams on Solana" (arXiv 2603.24625) — [arXiv](https://arxiv.org/pdf/2603.24625)
  - "Demystifying Solana Bots: From GitHub Blueprints to On-Chain Fingerprints" (arXiv 2607.28424), on bot fingerprinting on Solana — [arXiv](https://arxiv.org/pdf/2607.28424)
  - "Catching the Rug: Early Prediction of Fraudulent Memecoins on Solana via Machine Learning" (arXiv 2608.20271) uses the **first 5 minutes of trading to forecast 1-hour outcomes** (rug or not) — [arXiv](https://arxiv.org/html/2608.20271v1)
  - "MemeChain: A Multimodal Cross-Chain Dataset for Meme Coin Forensics and Risk Analysis" (arXiv 2601.22185) — [arXiv](https://arxiv.org/pdf/2601.22185)
  - "Measuring Memecoin Fragility" (arXiv 2512.00377) — [arXiv](https://arxiv.org/pdf/2512.00377)
  - "Hour-Aware Adaptive Risk Management for Autonomous Memecoin [trading]" (arXiv 2606.08232) — [arXiv](https://arxiv.org/pdf/2606.08232)
  - Cai, "Trust dynamics and bot-driven responses: An approach to rug pulls in Solana meme coin markets" (ACM WebSci 2025). Cited in reference lists; full text not seen — [cited via arXiv 2512.11850](https://arxiv.org/html/2512.11850v3)

**Return distributions of established memecoins**
- **Krause, "An Empirical Analysis of Meme Coin Performance: 2025-2026" (SSRN 6292920, posted Mar 2026; Marquette University).**
  - Sample: the **10 largest meme coins, Jan 2025 to Feb 2026**, weekly Yahoo Finance returns.
  - The equal-weighted portfolio had **annualised volatility of 103.82%** and a **maximum drawdown of 82.71%**.
  - It **significantly underperformed Bitcoin, the S&P 500 and gold**.
  - Sources: [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6292920); [ResearchGate](https://www.researchgate.net/publication/401094962_An_Empirical_Analysis_of_Meme_Coin_Performance_2025-2026)
- Krause has related SSRN papers:
  - "Beyond the Hype: A Meme Coin Reality Check for Retail Investors" (2024, SSRN 4891841) — [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4891841)
  - "Risks of Investing in Meme Coins: A Case Study of the $TRUMP Coin" (2025, SSRN 5126056) — [SSRN](https://papers.ssrn.com/sol3/Delivery.cfm/5126056.pdf?abstractid=5126056&mirid=1)

### Inferences
- The best-supported graduation rate on pump.fun is **~0.6-1%**: 0.63% in Sep 2025 (Marino et al.) and 1.03% for originals vs 0.66% for clones over two years (Factories paper). Mancino gives a peak of under 2% for Q4 2024. The widely quoted "0.2%" figure is a measurement artefact and should not be used.
- Graduation is not the same as profit. Graduation happens fast (median ~4.4 min), and the manipulation papers show that early buyers (creators, snipers, bundlers) capture most gains. Late retail entrants are the main source of exit liquidity.
- A high return in a memecoin is weak evidence of organic demand. Over 80% of >100% gainers show artificial growth, so return-chasing strategies are largely chasing manipulation.
- The ~14% vs ~3% gap between smart-money and copier returns suggests that latency and frictions eat most of any copyable edge.

### Gaps
- **Bot activity share:** I found no verified number for the share of pump.fun or Solana memecoin volume or transactions done by bots, snipers or MEV sandwichers. The candidate source is "Demystifying Solana Bots" (arXiv 2607.28424), but it could not be fetched. A follow-up search was blocked by the search budget.
- **Full return distributions** of all pump.fun tokens (median token return, share of wallets in profit) were not found in abstract-level material. They may be in the Marino et al. or Factories full texts, which arxiv.org blocking made unreachable.
- Rug-pull frequency on Solana (arXiv 2603.24625) and fragility metrics (arXiv 2512.00377) were not retrieved.
- Investor-loss numbers for Solana in Mongardini & Mei: the paper says Solana is highest, but I did not retrieve the figure.

## 2. Classic crypto pump-and-dump literature and what transfers to memecoins

### Takeaway
The 2018-2021 literature studied coordinated Telegram/Discord pumps of small-cap coins on centralised exchanges. Its findings carry over to memecoins: pumps work best on illiquid, low-rank coins, prices revert quickly, insiders and organisers profit at the expense of late participants, and the events are partly predictable. Memecoin launchpads have automated the scheme. Every pump.fun token starts as an illiquid micro-cap, and the bonding curve plus on-chain bots replace the Telegram countdown.

### Cited Findings
- **Kamps & Kleinberg, "To the moon: defining and detecting cryptocurrency pump-and-dumps," *Crime Science* 7:18 (2018), peer-reviewed.**
  - Reviews the classic (equity) pump-and-dump literature.
  - Proposes criteria for defining crypto P&Ds.
  - Detects them with anomaly detection on price and volume histories.
  - Fraudulent activity **clusters on specific exchanges and coins**.
  - Per a secondary summary, **coin rank (market cap or volume) is the most important driver of profitability**, and low-volume coins are far more profitable to pump.
  - Sources: [Springer](https://link.springer.com/article/10.1186/s40163-018-0093-5); [UCL PDF](https://discovery.ucl.ac.uk/id/eprint/10069142/1/To%20the%20moon%20defining%20and%20detecting%20cryptocurrency%20published.pdf); [DSHR blog summary](https://blog.dshr.org/2022/07/pump-and-dump-schemes.html)
- **Xu & Livshits, "The Anatomy of a Cryptocurrency Pump-and-Dump Scheme," USENIX Security 2019, peer-reviewed.**
  - Sample: **412 Telegram-organised pump-and-dumps, June 2018 to Feb 2019**.
  - Includes a detailed case study of a single pump.
  - Builds a model that **predicts which coins will be pumped**, so pumps are "not entirely unpredictable black-swan events".
  - Sources: [Semantic Scholar](https://www.semanticscholar.org/paper/The-Anatomy-of-a-Cryptocurrency-Pump-and-Dump-Xu-Livshits/885f048b76408b67404e43eb47c5e2529c946253); [arXiv 1811.10109](https://www.alphaxiv.org/abs/1811.10109v2)
- **Hamrick, Rouhi, Mukherjee, Feder, Gandal, Moore & Vasek, "An examination of the cryptocurrency pump-and-dump ecosystem," *Information Processing & Management* (2021), peer-reviewed; SSRN 3303365.** Sample: six months of 2018, with **952 pumps on Discord and 2,469 on Telegram** targeting hundreds of coins. Findings:
  - **Smaller coins gain more**:
    - coins ranked beyond 500: median peak gain of about **23% (Discord) and 19% (Telegram)**;
    - top-75 coins: about **3.5% and 4.8%**.
  - **Profitability fell over time.** By June 2018 it was about 50% lower on Telegram and about 60% lower on Discord.
  - A search summary also reported a median pre-pump to post-pump change of -41% (Discord) and -38% (Telegram), but that figure looks garbled. Check it in the PDF.
  - Sources: [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3303365); [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0306457321000169); [BFI PDF](https://bfi.uchicago.edu/wp-content/uploads/Gandal-Neil-etal-An-examination-of-the-cryptocurrency-pump-and-dump-ecosystem.pdf)
- **La Morgia, Mei, Sassi & Stefa, "The Doge of Wall Street: Analysis and Detection of Pump and Dump Cryptocurrency Manipulations," *ACM Transactions on Internet Technology* (2023), peer-reviewed; arXiv 2105.00733.**
  - Monitored Telegram/Discord groups for **more than 3 years**, detecting **~900 events**.
  - An earlier version reports **1,108 events on 4 exchanges from 20 Telegram groups**. The counts differ by version.
  - Distinguishes classic P&Ds from "crowd pumps", such as the 2021 GameStop-style crowd pumps.
  - Builds real-time detectors.
  - Sources: [arXiv](https://arxiv.org/html/2105.00733v2); [ACM](https://dl.acm.org/doi/full/10.1145/3561300)
- **Li, Shin & Wang (Tao Li, Donghwa Shin, Baolian Wang), "Cryptocurrency Pump-and-Dump Schemes."** I saw only second-hand descriptions:
  - a difference-in-differences design shows **pump-and-dumps lower the subsequent price/value of affected coins**;
  - Kamps & Kleinberg's estimate of **insider profit (~18%) "aligns" with Li et al.**
  - Source: secondary descriptions surfaced in [search results incl. DSHR blog](https://blog.dshr.org/2022/07/pump-and-dump-schemes.html)
- **Newer detection work:**
  - "Perseus: Tracing the Masterminds Behind Cryptocurrency Pump-and-Dump Schemes" (arXiv 2503.01686, 2025) — [arXiv](https://arxiv.org/pdf/2503.01686)
  - "Machine Learning-Based Detection of Pump-and-Dump Schemes in Real-Time" (arXiv 2412.18848, 2024) — [arXiv](https://arxiv.org/pdf/2412.18848)

### Inferences (what transfers to memecoins)
- **Low liquidity and low rank lead to larger pumps.** This is the Hamrick and Kamps & Kleinberg result. Pump.fun tokens sit at the extreme of this spectrum, which matches the LPI mechanism in Mongardini & Mei (small buys move price a lot).
- **Information and timing asymmetry decides who profits.** In Telegram pumps, organisers bought before the signal. In memecoins, creators, snipers and bundlers accumulate in the first blocks (Ding et al.; Factories paper). The structure is the same, now automated on-chain.
- **Predictability.** Xu & Livshits could predict pump targets. The memecoin analogues are graduation prediction (Marino et al.) and rug prediction from the first 5 minutes ("Catching the Rug"). The predictable thing is mostly *which tokens are manipulated/fail*, not reliable positive returns for outsiders.
- **Decaying profitability.** Hamrick et al. found pump profits falling over time as participants learned. A similar decay of edges may apply to memecoin sniping and copy-trading strategies as competition rises (consistent with the 14% to 3% copy-trade gap). This is an inference, not a tested finding.

### Gaps
- I could not verify the original numbers in Li, Shin & Wang (sample period, exchanges, price effects), because the search returned no full text.
- Exact peak returns and reversal speed in Kamps & Kleinberg and Xu & Livshits (for example, minutes to reversal) were not retrieved, because fetching the PDFs was blocked.

## 3. Attention / meme-stock (GameStop) literature relevant to memecoins

### Takeaway
The meme-stock literature finds that attention-driven retail buying leads to short-run overpricing followed by lower subsequent returns. Fear and sentiment on Reddit predict GME returns, especially at the bubble peak. Retail participants on average lost money. A new memecoin-specific journal paper finds attention-feedback trading: turnover responds to lagged absolute returns.

### Cited Findings
- **Long et al., "'I just like the stock': The role of Reddit sentiment in the GameStop share rally," *Financial Review* (2023), peer-reviewed.** Reddit (WallStreetBets) sentiment played a role in the GME rally — [Wiley](https://onlinelibrary.wiley.com/doi/full/10.1111/fire.12328)
- **Fernandez-Perez et al., "Emotions and stock returns during the GameStop bubble," *Financial Review* (2025), peer-reviewed.**
  - Fear-associated Reddit posts are **negatively related to subsequent GME returns**.
  - The emotion-return link is **stronger at the bubble peak**, when attention was highest.
  - Source: [Wiley](https://onlinelibrary.wiley.com/doi/10.1111/fire.12438)
- **"Who participated in the GameStop frenzy? Evidence from brokerage accounts," *Finance Research Letters* (2021).**
  - **WSB attention significantly reduces holding-period returns.**
  - Many retail investors were short GME early on.
  - Source: [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S154461232100221X)
- **"The tail wagging the dog: How do meme stocks affect market efficiency?"** (*International Review of Economics & Finance*, 2023) reports evidence that meme stocks are weakly efficient — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S1059056023001351)
- A paper on "high probability-to-viral" (PTV) meme-type stocks, summarised by Interactive Brokers, finds that **retail inflows overprice high-PTV stocks, followed by lower returns**. It reports a **12.29% monthly return spread** during the pandemic — [IBKR Quant summary](https://www.interactivebrokers.com/campus/ibkr-quant-news/why-you-bought-gamestop-and-why-you-lost-money-on-it/)
- **Cato Journal review (2021):** Robinhood customers are largely uninformed (citing Barber 2021), which creates opportunities for market makers — [Cato](https://www.cato.org/cato-journal/fall-2021/gamestop-episode-what-happened-what-does-it-mean)
- **"Community, attention, and feedback trading in cryptocurrency markets: Evidence from memecoins"** (*Research in International Business and Finance*, 2026, ScienceDirect S0275531926003491; authors not retrieved).
  - Memecoin **turnover responds significantly to lagged absolute returns**, consistent with **attention-feedback trading**.
  - Source: [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0275531926003491)

### Inferences
- The "attention leads to overpricing, then reversal" mechanism from meme stocks should be stronger in memecoins. Memecoins have no fundamentals, no short-selling at launch, and near-zero listing costs. The pump.fun manipulation papers suggest attention there is often manufactured (comment bots, wash trading, influencer launches).
- Feedback trading (volume chasing past absolute returns) gives manipulators a lever. Wash-traded volume and price spikes attract further attention-driven flows.

### Gaps
- **Barber, Huang, Odean & Schwarz, "Attention-Induced Trading and Returns: Evidence from Robinhood Users" (*Journal of Finance*, 2022)** is the canonical paper. I could not retrieve its numbers, because the search budget was exhausted. From memory, it reports negative abnormal returns after Robinhood herding events, but this is **unverified** and the figure should be checked before use.
- I did not verify the authors of the memecoin feedback-trading paper or whether it tests return autocorrelation directly.

## 4. Evidence of predictable patterns (momentum, reversal) in memecoin returns

### Takeaway
I found no peer-reviewed paper that cleanly documents tradable cross-sectional momentum or reversal in memecoin *returns*. The evidence that exists points to:
- predictability of **outcomes** (graduation; rug vs. non-rug) from very early on-chain features;
- attention-feedback in **volume**;
- predictable **wallet-level** profitability (smart money), which mostly disappears for copiers;
- negative long-horizon performance for large memecoins.

Apparent "momentum" in winners is mostly manipulation.

### Cited Findings
- **Outcome predictability.**
  - Marino et al. (2026) predict graduation using bonding-curve SOL and launch and trader-behaviour variables, with improved predictive power — [arXiv](https://arxiv.org/abs/2602.14860)
  - "Catching the Rug" uses the **first 5 minutes** of trading to forecast **1-hour** fraud outcomes on Solana — [arXiv](https://arxiv.org/html/2608.20271v1)
  - The Factories paper ties graduation odds to creator behaviour (attempt count, automation, interval between launches) — [arXiv](https://arxiv.org/html/2609.10246v1)
- **Attention-feedback.** Memecoin turnover responds to lagged absolute returns — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0275531926003491)
- **Wallet-level persistence.** Smart-money wallets average about 14% per trade, while copiers net about 3% after frictions — [arXiv 2601.08641](https://arxiv.org/html/2601.08641v2)
- **Winners are mostly manipulated.** 82.6% of >100% gainers show artificial growth. Pump-and-dumps and rug pulls *follow* wash trading or LPI, so an early price run-up predicts a later dump — [arXiv 2507.01963](https://arxiv.org/abs/2507.01963)
- **Long-horizon underperformance.** Large memecoins (Jan 2025 to Feb 2026) had 103.82% annualised volatility and an 82.71% maximum drawdown, and they underperformed BTC, the S&P 500 and gold — [SSRN 6292920](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6292920)
- **Classic P&D reversal.** Pump-and-dumps lower the subsequent value of affected coins (Li, Shin & Wang, via secondary description), and pumps are predictable ex ante (Xu & Livshits 2019) — [DSHR](https://blog.dshr.org/2022/07/pump-and-dump-schemes.html); [Semantic Scholar](https://www.semanticscholar.org/paper/The-Anatomy-of-a-Cryptocurrency-Pump-and-Dump-Xu-Livshits/885f048b76408b67404e43eb47c5e2529c946253)

### Inferences
- The robust "pattern" is **short-horizon reversal after manipulated run-ups**: wash trading or LPI first, then a dump or rug. Any momentum exists at very short horizons (minutes) and goes to the fastest actors (snipers and bots), not to latecomers.
- Early on-chain features (holder concentration, creator history, bonding-curve fill speed, social links) are the most promising predictors in the literature. They predict *failure* better than *magnitude of gains*.
- Results depend strongly on the data pipeline. Kamat's correction and the cross-pipeline coverage paper show this, so any backtest of memecoin "patterns" needs careful data auditing.

### Gaps
- I found no study measuring time-series or cross-sectional momentum factors (e.g., past 1h/24h return deciles leading to future returns) for pump.fun or graduated Solana tokens with transaction costs, MEV and slippage. The question remains open, or not covered by what was reachable.
- I could not check whether the Krause or other SSRN memecoin papers test autocorrelation in returns. Only the abstracts were seen.
