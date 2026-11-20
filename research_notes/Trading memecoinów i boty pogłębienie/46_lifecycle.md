# Memecoin lifecycle modeling (as of Nov 2026)

Method note: 3 web searches (snippet-level; no page fetches). Figures come from search summaries of the cited pages and are NOT independently verified against the primary documents. Items marked [UNVERIFIED] have no source.

## What phases, time-to-peak and decay curves are documented?

### Takeaway
No formal peak-time or half-life study of memecoins was found. The best quantitative evidence is a survival curve (CoinGecko, Pump.fun) and a pump/dump detection paper (arXiv 2507.01963). The usual phase model (launch, first pump, dump, consolidation, second leg) is practitioner convention, not a published finding.

### Cited Findings
- CoinGecko studied ~18.67M Pump.fun tokens created 14 Jan 2024 to 18 Jun 2026. Lifespan = days from creation to last bonding-curve trade; never-traded tokens excluded. 12.8M tokens (68.67%) made their last trade on launch day. — [CryptoPotato](https://cryptopotato.com/nearly-70-of-pump-fun-tokens-die-on-launch-day-coingecko/), [Crypto Briefing](https://cryptobriefing.com/pump-fun-token-survival-rate-study/) (as summarized by search; figures not checked at source)
- Survival tail: ~4.1% lasted 2-3 days, ~3.4% lasted 4-7 days, and ~4.55% (~850k tokens) traded beyond 90 days (one outlet says "only 5% survive past 90 days", i.e. rounding). Mean lifespan well under one day. — [KuCoin summary](https://www.kucoin.com/news/flash/nearly-70-of-pump-fun-tokens-disappear-on-launch-day-80-gone-in-2-days), [Crypto Briefing](https://cryptobriefing.com/pump-fun-token-survival-rate-study/)
- Caveat: tokens that migrated to Raydium/Meteora/PumpSwap may be undercounted as "dead", since only the Pump.fun bonding curve was measured. — [Crowdfund Insider](https://www.crowdfundinsider.com/2026/06/288223-solana-based-pump-fun-has-dramatically-lowered-barrier-to-creating-speculative-meme-coins-analysis/)
- Mongardini & Mei, "A Midsummer Meme's Dream" (arXiv 2507.01963): pump defined as price >+50% within 24h with a volume surge; dump as >-30%. Found 91 operations across 60 tokens, mostly Solana; median dump erases ~56% of value; median creation-to-first-pump-and-dump gap 146 days; pump-to-dump timing not a fixed interval. — [arXiv](https://arxiv.org/pdf/2507.01963)
- SBFC 2025 paper (P154): bot activity on bonding-curve launches lengthens the pump phase and shortens the dump phase; creators are the most frequent dump initiators. — [SBFC2025](https://sbfc.sydney.edu.au/2025/papers/SBFC2025_4G3_P154.pdf)
- arXiv 2512.00377 offers a memecoin fragility scoring framework (volatility, whale concentration, sentiment); no time-to-peak/half-life metrics seen in excerpts. — [arXiv](https://arxiv.org/pdf/2512.00377.pdf)
- arXiv 2512.11850 "The Memecoin Phenomenon" appeared in results; contents not examined. — [arXiv](https://arxiv.org/html/2512.11850v1)

### Inferences
- The survival curve is extremely front-loaded: ~2/3 of tokens are effectively dead within 24h, so the "decay curve" for the median token is near-instant; any lifecycle model must condition on surviving the first day.
- A median 146-day gap to the first detected pump-and-dump (for tokens that had one) implies the sample is survivor-biased toward long-lived tokens, so it does not describe typical launches.
- The bot findings imply phase length is partly manufactured, so fixed phase durations are unlikely to be stable.

### Gaps
- No peer-reviewed or vendor study giving time-to-peak distributions or fitted volume/attention half-life for memecoins; [UNVERIFIED] any specific "peak within X minutes/hours" or "volume half-life of N hours" figure.
- No Coin Metrics memecoin lifecycle report surfaced; Coin Metrics coverage was not found.

## How often do second pumps (second legs) occur?

### Takeaway
No reliable base rate for "second leg" frequency was found. Graduation rate is the only adjacent, sourced statistic.

### Cited Findings
- About ~1% of Pump.fun launches graduate to external DEXs per CoinGecko-based reporting. — [Crowdfund Insider](https://www.crowdfundinsider.com/2026/06/288223-solana-based-pump-fun-has-dramatically-lowered-barrier-to-creating-speculative-meme-coins-analysis/)
- Weekly graduation rate hit 2.01% (week of 9-15 Mar 2026, Dune data, highest since Jul 2025), then a 7-day average of 0.26% by mid-June 2026; Pump.fun activity fell ~80% in three months and Solana daily fees fell from ~33,000 SOL (Jan) to ~5,300 SOL (Jun) as traders rotated to perps. — [KuCoin](https://www.kucoin.com/news/flash/pump-fun-meme-coin-graduation-rate-hits-2-01-highest-since-july-2025), [The Block](https://theblock.co/news/ecosystems/2026-06-16-pump-fun-activity-craters-80-three-months-solana-fees-lower-traders-rotate-perps-404806), [DEXTools](https://www.dextools.io/news/pump-fun-graduation-collapse-solana-fees-2026)
- Earlier: graduation stayed below 1% for four weeks from 17 Feb 2025 (Dune). — [Cointelegraph](https://cointelegraph.com/news/pump-fun-memecoins-are-dying-at-record-rates-less-than-1-survive)
- 91 pump-and-dump operations over 60 tokens implies ~1.5 operations per affected token, i.e. repeat cycles do occur in manipulated tokens. — [arXiv](https://arxiv.org/pdf/2507.01963) (ratio is my arithmetic)

### Inferences
- Second legs are conditional on surviving to graduation (~1% or less), so absolute second-pump frequency across all launches is tiny; among graduated tokens it is unknown.
- Regime matters: rates swing 0.26%-2% with market-wide memecoin appetite, so a static base rate would mislead a bot.

### Gaps
- No dataset of second-pump frequency among graduated tokens; [UNVERIFIED] any percentage quoted for it.
- Coin Metrics / academic half-life of attention or volume not found (3 searches only; Google Trends/social-attention studies not searched).
