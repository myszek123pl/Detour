# Correlation structure of memecoins (as of Nov 2026)

Research budget: 3 web searches (the third was rate-limited), 0 fetches. Much of this topic is a gap. Unverified items are marked [UNVERIFIED].

## Correlation among large-cap memes and with SOL/BTC/ETH

### Takeaway
No reliable 2026 memecoin-to-BTC/ETH/SOL correlation figures were found. Only SOL-BTC correlation is documented, and it is high.

### Cited Findings
- SOL vs BTC rolling correlation, as of about Apr 24, 2026: 30d 0.86, 90d 0.92, 1y 0.83, 2y baseline 0.77. — [AhaSignals](https://ahasignals.com/crypto-correlation/btc-sol/) (aggregator-grade; dated, not current)
- A MEXC item reported a BTC-SOL correlation of 0.99 over one week. This conflicts with the ranges above and is likely a very short window. — [MEXC](https://www.mexc.com/news/1119275) [UNVERIFIED; low quality]
- SOL typically amplifies BTC moves in both directions (beta above 1), with drawdowns intensifying in macro risk-off. — [Mudrex](https://mudrex.com/learn/solana-bitcoin-correlation/)
- SOL-specific catalysts (e.g. SOL spot ETF inflows, mid-Aug 2026) can decouple SOL from BTC temporarily, but correlation has historically reasserted within weeks. — [Mudrex](https://mudrex.com/learn/solana-bitcoin-correlation/)
- A memecoin correlation guide cites a historical memecoin-ETH correlation of about 0.65 and gives no 2026 BTC figure. — [MEXC guide](https://www.mexc.com/crypto-pulse/article/memecoin-vs-bitcoin-altcoins-669) [UNVERIFIED; exchange marketing content]
- Memecoin activity is tied to Solana's 2026 rally and is cyclical. — [Blockhead](https://www.blockhead.co/2026/04/29/solanas-degenerate-season-fades-as-etf-dreams-face-regulatory-headwinds/)

### Inferences
- Memecoins likely load on the same market-wide risk factor as SOL and BTC, with Solana-native memes (BONK, WIF, etc.) tied to SOL as well. This is inferred, not measured.
- Pairwise correlations among large-cap memes are probably high in daily returns, and lower in idiosyncratic, narrative-driven windows. This is a hypothesis for a bot to test on its own data.

### Gaps
- No sourced pairwise correlation matrix for DOGE, SHIB, PEPE, BONK, WIF, etc.
- No sourced memecoin-BTC or memecoin-ETH correlation for 2026.

## Beta by market-cap tier

### Takeaway
No sourced tier-level betas were found.

### Cited Findings
- Only the SOL-vs-BTC qualitative beta above 1 is sourced (see above). — [Mudrex](https://mudrex.com/learn/solana-bitcoin-correlation/)

### Inferences
- Beta is probably higher for smaller caps (the usual altcoin pattern), with lower liquidity adding slippage that is not captured by beta. [UNVERIFIED hypothesis]
- Bot approach: estimate beta empirically, with rolling regressions on BTC and SOL by market-cap bucket, using downside beta separately from upside beta.

### Gaps
- No published tiered beta data was found within the search budget.

## Correlation spikes during crashes

### Takeaway
No sourced crash-correlation statistics were obtained. The search that targeted this was rate-limited.

### Cited Findings
- The Block reported the memecoin index (GMCI Meme per the March 2025 story) fell about 90% from its Dec 2024 peak as of March 2025. — [The Block](https://www.theblock.co/news/markets/2025-03-17-memecoin-index-plunges-90-as-crypto-markets-retreat-346637) (the headline figure was seen only in a search listing, not the full article; the drawdown number is my reading of the search summary)
- From model memory only: the Oct 10, 2025 liquidation event (roughly $19B reported) hit memecoins alongside the broad market. [UNVERIFIED]

### Inferences
- Standard finding in crypto: cross-asset correlation rises in sell-offs, so diversification within memes fails when it is needed most. Consistent with the above but not demonstrated by sourced data here.

### Gaps
- No measured crash-window correlations (e.g. Oct 2025, Mar 2025, 2026 events).

## Sector indices (CoinDesk Memecoin index, GMCI meme, MEME ETFs)

### Takeaway
Two meme indices exist and are described below. No MEME ETF was confirmed.

### Cited Findings
- CoinDesk Meme Index (CDMEME): about 50 of the most liquid memecoins, equally weighted; 90-day seasoning and 30-day liquidity requirements; monthly reselection, quarterly reweighting to equal weight. Universe from CCData "Meme" classification; methodology PDF dated Apr 2025. — [CoinDesk Indices](https://indices.coindesk.com/coindeskmeme); [Methodology](https://downloads.coindesk.com/cd3/CDI/CoinDesk-Memecoin-Index-Methodology.pdf)
- A perpetual futures contract, CDMEME-USDC-PERP, is listed on Bullish. — search summary of CoinDesk Indices page [UNVERIFIED in primary source]
- GMCI Meme (GMMEME), separate provider, hosted on The Block: one snapshot shows 11 assets, last rebalance Sep 25, 2026, about -19% one-month change; another shows 10 assets, rebalance Jan 30, 2026. The snapshots conflict. — [The Block](https://www.theblock.co/indices/gmci-meme) [UNVERIFIED; check live]
- MEME ETF: none of the search results mentioned an ETF on either index. Existence unconfirmed.

### Inferences
- Equal weighting over about 50 names makes CDMEME a better proxy for the broad "meme factor" than cap-weighted baskets, and a usable benchmark for a bot's beta and relative-performance calculations. A perp on it could in principle serve as a hedge, but liquidity is unverified.

### Gaps
- Index correlations to BTC/SOL/ETH, historical returns, and constituent lists.
- Any spot MEME ETF (e.g. Dogecoin or other meme ETF filings) status as of Nov 2026.

## Implications for portfolio diversification in a bot

### Takeaway
Treat the memecoin sleeve as largely one correlated risk factor tied to BTC/SOL, with crash correlation higher than average; size by factor exposure, not by token count.

### Cited Findings
- SOL-BTC correlation is high (0.83-0.92 over 30d-1y) and SOL amplifies BTC moves. — [AhaSignals](https://ahasignals.com/crypto-correlation/btc-sol/); [Mudrex](https://mudrex.com/learn/solana-bitcoin-correlation/)
- Memecoin activity is cyclical. — [Blockhead](https://www.blockhead.co/2026/04/29/solanas-degenerate-season-fades-as-etf-dreams-face-regulatory-headwinds/)

### Inferences (all unverified design suggestions)
- Cap total memecoin exposure as a single bucket and apply a portfolio-level beta/drawdown limit; do not count N memes as N independent bets.
- Use a rolling correlation matrix with a crash-regime override (assume correlation near 1 under stress).
- Hedge with BTC/SOL perps (or a meme index perp if liquid) to strip common beta.
- Real diversification comes from strategy diversity (timing, venue, holding horizon), not token diversity.
- Prefer measuring correlations from the bot's own data over the third-party figures above.

### Gaps
- No sourced evidence on hedge effectiveness or optimal bucket size.
