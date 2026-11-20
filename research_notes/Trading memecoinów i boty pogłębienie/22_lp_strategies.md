# LP on memecoins: Meteora DLMM/DAMM v2, Raydium CLMM (as of Nov 2026)

Research limits: web search hit a rate limit after 2 of 4 attempted queries; WebFetch to docs.meteora.ag, messari.io and solanacompass.com failed (host not in allowed network). Everything below comes from search-result summaries only (not full-page reads). Many items are Gaps.

## What are the LP strategy shapes (spot/curve/bid-ask) and how do they trade off fees vs impermanent loss?

### Takeaway
Meteora's official docs describe Spot (even), Curve (concentrated at centre, calm markets) and Bid-Ask (weighted to the range edges, for volatile/DCA-style entry and exit). Memecoins are the highest-IL case, and Meteora itself says no shape removes IL or out-of-range risk.

### Cited Findings
- Bid-Ask puts most capital near both ends of the range; suited to large swings away from current price and single-sided DCA entries/exits. For memecoins the docs warn it has the highest IL risk when price leaves the bin range, so it needs close monitoring — [Meteora docs: Strategies & use cases](https://docs.meteora.ag/overview/products/dlmm/strategies-and-use-cases) (via search summary, page not fetched)
- Curve is capital-efficient and ideal for calm markets but has increased IL risk and needs rebalancing vs current price — [Meteora docs](https://docs.meteora.ag/overview/products/dlmm/strategies-and-use-cases) (via search summary)
- A "Spot-Wide" shape deposits liquidity equally across 50 bins and is described as lower IL risk — [Meteora docs](https://docs.meteora.ag/overview/products/dlmm/strategies-and-use-cases) (via search summary)
- DLMM strategies improve capital efficiency but do not remove IL or out-of-range risk — [Meteora docs](https://docs.meteora.ag/overview/products/dlmm/strategies-and-use-cases) (via search summary)
- Unofficial quick-reference guide recommends a shape by pair type, time available and market view (unofficial, unchecked) — [community quick ref](https://bonangrs03.github.io/meteora-dlmm-docs/extras/quick-ref.html)

### Inferences
- In a dump, a Bid-Ask or Curve position ends up fully converted into the falling token (bags) with fees often smaller than the loss; Spot-Wide limits but does not eliminate this. (reasoning from the mechanics above, not sourced)

### Gaps
- No documented per-strategy realised returns; no Raydium CLMM-specific sources found (no search covered it).

## Dynamic fees (DLMM, DAMM v2) and fee APR vs IL

### Takeaway
Meteora says dynamic fees rise with volatility to compensate LPs. DAMM v2 specifics (fee scheduler / anti-sniper decay) could not be verified from sources this session.

### Cited Findings
- Meteora states its dynamic swap fees rise during high volatility to compensate LPs for IL — [Meteora docs](https://docs.meteora.ag/overview/products/dlmm/strategies-and-use-cases) (via search summary); similar claim in [KuCoin analyst piece](https://www.kucoin.com/news/insight/SOL/69d71ae3ece6110007481e6c)
- Meteora reportedly reported ~$140M LP fees and ~$32B trading volume in H1 2026 (headline only, details not read) — [Solana Compass](https://solanacompass.com/news/meteora-reports-140m-in-lp-fees-and-32b-in-h1-2026-trading-volume)
- Messari: Meteora does not capture most of initial PvP launch volume but became a main venue for memes surviving past launch phase (search summary only) — [Messari](https://messari.io/report/a-meteoric-bet-on-memecoins)

### Inferences
- Fee-scheduler/dynamic-fee in DAMM v2 (from unsourced background knowledge: high starting fee decaying over time, volatility component) mainly protects against snipers; treat as unverified.

### Gaps
- No verified DAMM v2 parameters (fee limits, decay modes), no fee-APR figures, no APR-vs-IL quantification.

## Tools (Metlex, LP Agent, Cleopetra)

### Takeaway
Nothing verified; searching for these failed (rate limit).

### Cited Findings
- None.

### Gaps
- Features, pricing, track record of Metlex, LP Agent, Cleopetra all unresearched; retry with separate queries.

## Documented returns and risks of LPing into dumps

### Takeaway
No Meteora-specific LP profitability study found. Adjacent data shows poor outcomes for memecoin traders and a (weakly sourced) majority of LPs underwater.

### Cited Findings
- A KuCoin analyst claims ~75% of LP wallets underperform or are in the red — [KuCoin](https://www.kucoin.com/news/insight/SOL/69d71ae3ece6110007481e6c). UNVERIFIED, no methodology.
- Blog claims ~80% of Uniswap LPs lose vs holding (attributed to Uniswap internal data) — [Coin Autopsy Journal](https://coinbiopsy.bearblog.dev/the-lp-trap/). UNVERIFIED secondary source.
- Pump.fun: ~96% of wallets lost or made under $500 trading memecoins in March 2026 (traders, not LPs) — [Analytics Insight](https://www.analyticsinsight.net/cryptocurrency-analytics-insight/why-most-memecoin-traders-fail-inside-the-95-loss-rate-problem)
- Only 6% of Solana meme traders profitable over 90 days (traders, not LPs) — [Mitrade](https://www.mitrade.com/insights/news/live-news/article-3-2012817-20260819)
- Uniswap v3 LP profitability is hard to measure/ambiguous — [Mirror essay](https://mirror.xyz/0xA3DB621697fBC0dA0b16160eb8E201E1a763D2c1/SI9A-eRE8g7gy0oDbqChl1mOm6JwBriimDq29VE4O58)
- Messari labelled memecoins "the most extractive crypto phenomenon" — [Forklog](https://forklog.com/en/messari-labels-meme-coins-as-the-most-extractive-crypto-phenomenon/amp)

### Inferences
- Memecoin LPs face adverse selection (informed/insider flow, rugs, one-way dumps), so fee income frequently fails to offset IL; only rebalancing/active-managed or short-duration strategies plausibly win (unproven here).

### Gaps
- No on-chain cohort study of DLMM LP PnL; no individual documented LP results; no Raydium CLMM data; no rug/dump-specific loss cases.
