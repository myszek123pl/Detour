# Time-of-day, day-of-week and seasonal patterns in memecoin launches, volume and success rates

Research limits: 3 searches returned results (a 4th was rate-limited); all WebFetch calls failed (docs.bitquery.io, arxiv.org, madeonsol.com not resolvable from this session). All findings below come from search-result snippets only, not from full pages. Figures are marked [unverified] where the snippet was partial.

## What does the evidence say about hour-of-day (US vs Asia session) effects on pump.fun launches?

### Takeaway
No source found with a verified hour-by-hour launch table. One vendor doc (Bitquery) reportedly says launches cluster ~15:00-22:00 UTC (US morning/EU evening) and thin out during Asia overnight hours; the numbers were not visible, so treat as qualitative and unverified.

### Cited Findings
- Bitquery's "Pump.fun Launch Pulse — New Tokens per Hour" doc reportedly describes launches clustering around 15:00-22:00 UTC and tapering through Asia overnight, with a 23 Apr 2026 snapshot and a query for hour-of-day by weekday heatmaps; hourly table values did not render — [Bitquery docs](https://docs.bitquery.io/docs/mcp/trading/examples/pumpfun-launch-pulse/) [unverified: paraphrased from search summary; vendor tutorial, single snapshot]
- An arXiv paper (2602.14860) is a systematic on-chain empirical analysis of early-stage Pump.fun launches; the snippet showed no time-of-day data, so whether it has any is unknown — [arXiv](https://www.arxiv.org/pdf/2602.14860)

### Inferences
- A US/EU-evening-weighted launch cluster is plausible given the user base, but it is not confirmed by a primary dataset here. Anyone needing hourly numbers should compute them directly (Bitquery query, Dune on pump.fun create events, or Helius/RPC).

### Gaps
- No hourly counts, no Asia-vs-US session comparison of success (graduation) rate, no verified Dune hourly dashboard (the Dune search was rate-limited).

## Day-of-week and weekend effects

### Takeaway
Only weak evidence: Pump.fun's share of Solana token creation was reported higher on weekends (Sat 71.1%, Sun 69.5%, per Dune data cited by Decrypt) — this is a share, not an absolute volume comparison. No direct weekday-vs-weekend volume or success-rate study found.

### Cited Findings
- Decrypt, citing Dune data, reported Pump.fun made up 71.1% of tokens created on Solana on Saturday and 69.5% on Sunday — [Decrypt](https://decrypt.co/299665?amp=1) [unverified: snippet via search summary; date of the data not confirmed]
- Mancino's Q4 2024 arXiv paper on the Solana memecoin phenomenon reports Pump.fun accounted for up to 71.1% of tokens minted on Solana and 40-67.4% of DEX transactions; day-of-week findings not seen — [arXiv 2512.11850](https://arxiv.org/html/2512.11850v2)
- Event-driven example, not a recurring pattern: ~18-19 Jan 2025 weekend, Solana DEX volume hit a record $26.8B on Trump-memecoin frenzy — [Blockworks](https://blockworks.co/news/trump-memecoins-rock-solana) [unverified figure from snippet summary]
- A Forklog article titled "Meme coin traders ignite a frenzied weekend on Solana" exists (anecdotal weekend surge) — [Forklog](https://forklog.com/en/news/meme-coin-traders-ignite-a-frenzied-weekend-on-solana)

### Inferences
- Higher weekend share of pump.fun among Solana launches may mean other launch sources slow on weekends rather than pump.fun speeding up; don't read it as higher absolute weekend volume.

### Gaps
- No weekday/weekend absolute launch, volume or graduation-rate comparison found. Must be computed from Dune/DefiLlama daily data.

## Seasonal / regime patterns, launch volume and success rates (context)

### Takeaway
Launch counts and success rates are dominated by regime shifts (competition from LetsBonk, market cycles, platform changes) far more than calendar seasonality. Base success rate is very low (~1.8% graduation in Aug 2026 per one source).

### Cited Findings
- August 2026: 1.03M launches, 18,202 graduations, 1.8% bond (graduation) rate; avg ~37,500 launches/day; peak 54,965 on Aug 27 — [MadeOnSol](https://madeonsol.com/blog/pump-fun-deployer-stats-august-2026) [unverified: aggregator, snippet only]
- Early-era benchmark: ~42,000 tokens launched in one day with fewer than 2 reaching a DEX — [Solana Compass](https://solanacompass.com/news/pumpfun-launch-42000-tokens-in-one-day-fewer-than-2-will-ever-reach-a-dex) [unverified: title-level info only]
- Competitive regime shifts: LetsBONK overtook Pump.fun in daily launches/volume in mid-2025 and Pump.fun reclaimed the lead by 6 Aug 2025 — [The Block](https://www.theblock.co/news/ecosystems/2025-08-06-pump-fun-reclaims-letsbonk-365737)
- Pump's "Mayhem Mode" reportedly failed to lift launches/revenue in its first week — [The Block](https://www.theblock.co/post/379285/pump-funs-new-mayhem-mode-fails-boost-token-launches-revenue)
- Reports of sharp declines in graduating tokens as the frenzy faded — [The Block via TradingView](https://ru.tradingview.com/news/the_block%3Af76fef498094b%3A0-pump-fun-sees-rapid-decline-in-graduating-tokens-as-memecoin-frenzy-fizzles-out)

### Inferences
- With ~1-2% graduation and regime-driven volatility, any time-window edge (hour/day) is likely small relative to token-level selection and market-wide state; seasonal claims (e.g., holiday lulls) are unsupported here — The Block headline "lowest average daily volumes since Christmas" hints at holiday dips but is not evidence of a pattern.

### Gaps
- No seasonality study (month/quarter/holiday). No verified Dune dashboard URLs; candidate data sources to check: Bitquery pump.fun docs, Dune community dashboards for pump.fun launches/graduations, DefiLlama, arXiv 2602.14860 and 2512.11850 (full texts not read).
