# Trader psychology and behavioral biases in memecoin trading; encoding discipline into a bot

## 1. Behavioral finance evidence (overtrading, disposition effect, lottery preference)

### Takeaway
Classic evidence (Barber & Odean, Kumar) shows that high trading frequency and preference for lottery-like assets reliably cost retail investors money. The disposition effect is documented in Bitcoin/Ethereum but with time-varying strength. Memecoins combine all of these traits.

### Cited Findings
- Barber & Odean (J. Finance 2000), 60,000+ discount-brokerage households: gross returns roughly market-like but net returns lag benchmarks by significant amounts; the most active 20% of households earned 10.0% annualized net; authors attribute it to trading costs/frequency and overconfidence, not stock selection — [Barber & Odean paper](https://faculty.haas.berkeley.edu/odean/papers/returns/Returns.html); [RePEc record](https://ideas.repec.org/a/bla/jfinan/v55y2000i2p773-806.html)
- Critique: Bonaparte & Cooper (NBER 2010) say how hazardous trading is remains an open question; rational adjustment-cost models and overconfidence models don't fully explain the gross/net gap — [NBER w16022](https://www.nber.org/papers/w16022.pdf)
- A secondary blog cites Barber & Odean as most active traders ~11.4%/yr vs market 17.9% (I could not verify these figures against the original; the 10.0% figure above is from the abstract-level result) — [Hackernoon](https://hackernoon.com/why-winning-streaks-make-traders-lose-money)
- Kumar (J. Finance 2009, "Who Gambles in the Stock Market?"): investors with lottery-buyer characteristics over-weight lottery-type stocks, and those investors under-perform by roughly 2-3% — [UT Austin news](https://news.utexas.edu/2009/02/26/investors-who-gamble-in-the-stock-market-have-same-characteristics-as-lottery-players-study-shows); [RePEc](https://ideas.repec.org/a/bla/jfinan/v64y2009i4p1889-1933.html)
- Follow-up work (Kumar and coauthors, per University of Miami summary) estimates gambling is ~14% of stock market volume in developed countries — [U. Miami](https://news.miami.edu/miamiherbert/stories/2021/02/stock-market-gamblers.html)
- Disposition effect in Bitcoin (Schatzmann & Haslhofer, Digital Finance 2023): present but not consistent across the sample period, strengthening after 2017; uses exchange-bound transfers as a proxy for sales — [arXiv 2010.12415](https://arxiv.org/abs/2010.12415)
- A 2026 Ethereum paper (Lyu, Financial Sciences, Wroclaw) tests the disposition effect with 2020-2024 address-level data (I only saw the abstract-level description; findings not verified) — [journal PDF](https://journals.ue.wroc.pl/fins/article/download/2045/1320/8205)
- Revenge trading: no peer-reviewed study found. A vendor claim (37% of 500k+ traders; ~10% of affected traders' losses; riskiest window ~15 min after a loss) has no traceable source — [Hackernoon](https://hackernoon.com/why-your-next-trade-after-a-big-win-is-often-the-worst); [TradesViz](https://www.tradesviz.com/trading-psychology/revenge-trading/)

### Inferences
- Memecoins are an extreme case of Kumar's "lottery-type" asset (low price, high skew, social hype), so the 2-3% underperformance and overtrading cost likely understate memecoin outcomes, where fees/slippage/tip costs per trade are high. (Inference, not tested directly.)
- Because the cost of trading frequency is a main mechanism in Barber & Odean, a bot's trade-count and fee budgets are directly supported by this evidence.
- Bitcoin disposition evidence is time-varying, so a bot should measure its own hold-time asymmetry (winners vs losers) rather than assume the bias.

### Gaps
- No peer-reviewed study of revenge trading/tilt found in the searches; no memecoin-specific disposition effect study found; FOMO has no direct quantitative source collected.

## 2. Crypto/memecoin gambling-like behavior and problem-gambling links

### Takeaway
Multiple survey studies associate frequent crypto trading with problem-gambling severity, and one longitudinal Finnish study points toward trading preceding growth in gambling problems. Memecoin-specific hard evidence is mostly non-peer-reviewed.

### Cited Findings
- Rutgers study (Addictive Behaviors 2019, n=876 regular gamblers): problem gamblers were more likely to trade crypto frequently; >50% of regular gamblers had traded crypto in the past year; those trading both crypto and high-risk stocks showed more problem gambling, anxiety and depression; impulsivity and belief in beating the market suggested as drivers — [Rutgers](https://www.rutgers.edu/news/trading-cryptocurrency-problematic-regular-gamblers-rutgers-study-says)
- Addictive Behaviors 2021 (n=543 sports bettors/crypto traders): problem-gambling scores significantly related to crypto trading intensity (time, number of trades, spending) — [PubMed 34171583](https://pubmed.ncbi.nlm.nih.gov/34171583/)
- Finnish three-wave national survey (Oksanen et al., Public Health 2022): active crypto trading associated with growth in gambling problems over 18 months; highest among those also gambling at foreign online casinos — [University of Tampere](https://tuni.fi/en/news/cryptocurrency-trading-also-attracts-gamblers)
- Turkish cross-sectional study: problematic crypto trading linked with problem gambling severity and extraversion; risk tied to active trading rather than ownership — [Karger](https://karger.com/ear/article-split/31/5/297/933408/The-Examination-of-Cryptocurrency-Trading)
- UNLV survey (~700 crypto traders, 2025): about two-thirds met the threshold for at-risk or problematic gambling by PGSI; researchers cannot tell whether this reflects problem gamblers who trade or a new compulsion — [gambling.com](https://www.gambling.com/news/is-crypto-trading-gambling-a-unlv-researcher-weighs-in)
- UNLV meme-asset study (n=643): meme asset ownership related to gambling-problem measures; may be treated like gambling by some — [UNLV](https://digitalscholarship.unlv.edu/gaming_institute/2023/May23/60)
- Industry-sponsored ChainPlay survey (n=1,503): 73% think meme coin investing is gambling (perception survey, sponsor bias) — [IBTimes](https://www.ibtimes.com/investing-meme-coins-gambling-majority-crypto-investors-think-so-new-study-reveals-3706990)
- Pump.fun analysis claiming memecoin traders lose ~25 cents per dollar wagered: social-media write-up, not peer-reviewed, treat as unverified — via [search summary of youmind](https://youmind.com/it-IT/landing/x-viral-articles/memecoin-casino-odds-analysis)
- Counterview: some experts say trading differs from gambling because the trader owns an asset — [Psychology Today](https://www.psychologytoday.com/us/blog/addiction-outlook/202511/stock-options-and-cryptocurrency-trading-disorders)

### Inferences
- Evidence is mostly correlational, self-report; the human operator of a memecoin bot may himself be in a higher-risk group, justifying built-in human-side safeguards (deposit caps, withdrawal-only-profit sweeps).
- Intensity of trading (not mere holding) is the consistent risk marker, so trade-frequency monitoring doubles as a behavioral-health signal.

### Gaps
- No peer-reviewed, on-chain study of memecoin trader P&L distribution verified; the 25-cent figure is unverified.
- No studies found on bot users specifically.

## 3. Discipline frameworks, cooldowns, loss limits, and bot vs human override

### Takeaway
No rigorous study was found on journaling/cooldown effectiveness or on override harm; the case rests on the behavioral evidence above plus practitioner accounts. Translating it into rules is design inference.

### Cited Findings
- Practitioner/single-trader audits report discretionary overrides of systems were mostly harmful (an "intervention tax"); tiny samples, anecdotal — [Hackernoon](https://hackernoon.com/the-most-expensive-bug-in-my-trading-system-was-me); [Hackernoon](https://hackernoon.com/the-hidden-cost-of-overriding-your-trading-plan)
- Ernest Chan (quoted) advises manual override of a model is seldom a good idea (opinion) — [QuantInsti](https://blog.quantinsti.com/automated-trading-system-overrides/)
- Counterpoint: model performance deteriorates outside historical regimes, where human input can help — [Montel](https://montel.energy/resources/blog/human-vs-algorithm-decision-making-in-power-trading-finding-the-right-balance)
- Melbourne experiment: algorithm access did not eliminate mispricing vs manual trading — [Univ. Melbourne](https://minerva-access.unimelb.edu.au/server/api/core/bitstreams/6656c88b-108d-40a9-bd63-180d5dc8d0f4/content)
- Vendor claim: the riskiest window after a loss is ~15 min (varies 5-45), supporting time-based cooldowns (unsourced) — [TradesViz](https://www.tradesviz.com/trading-psychology/revenge-trading/)

### Inferences (proposed rules; design suggestions, not evidenced results)
Hard bot rules:
- Per-trade max risk (fixed small % of bankroll) and position size capped regardless of recent wins (counters post-win overconfidence/sizing up).
- Daily/weekly loss limit with automatic halt; N consecutive losses -> mandatory cooldown (e.g. 15-60 min or until next day); halt cannot be lifted by the bot.
- Daily trade-count and fee/slippage/tip budget (Barber & Odean: frequency/cost is the mechanism).
- Pre-defined exit rules (stop, time-stop, take-profit ladder) executed mechanically to avoid disposition effect; track median hold time of winners vs losers as a diagnostic.
- Anti-FOMO entry filters: no entries after price/volume spike above threshold, minimum token age/liquidity, no chasing after missed entries; cap on exposure to lottery-type (new, illiquid) tokens as portion of total.
- Kill switch on anomalies (RPC failure, abnormal slippage, drawdown spike); bankroll sweep of profits to cold wallet.
- Immutable structured trade log for journaling and post-hoc review.
Human oversight rules:
- Parameter changes only on a schedule (e.g. weekly) with written rationale, never during a drawdown; changes take effect after a delay (e.g. 24h) and are logged.
- Risk-limit increases are slower than decreases (asymmetric); no "top-up after loss" deposits; fixed capital allocation.
- Override log: every manual intervention recorded and its P&L compared with counterfactual to measure the intervention tax.
- Pre-commit rules, review via dashboard metrics rather than live P&L ticking; self-exclusion/stop criteria if gambling-like signs appear (chasing losses, escalating deposits).

### Gaps
- No peer-reviewed evidence found for cooldown, journaling, or loss-limit effectiveness in trading, nor a controlled study of human override of live bots. Practitioner sources are anecdotal and sometimes vendor-motivated.
