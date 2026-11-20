# Prediction markets (Polymarket, Kalshi, others) for memecoins/crypto: liquidity, signal and hedge value (as of Nov 2026)

Method note: 3 web searches (budget ~6, no fetches). Search-snippet summaries only; no primary pages opened. Figures below are unverified unless stated.

## Q1. What markets exist on memecoin prices/events, and how liquid are they?

### Takeaway
Crypto is the second-largest category on Polymarket and Kalshi after sports, but I found markets on specific memecoins only for large/event-style cases (e.g., a Pump.fun airdrop market, a Pump.fun price market). Memecoin-specific liquidity looks thin (low single-digit $M volume on the one market where a figure was found). I found no verified TRUMP-coin or ETF-approval market data.

### Cited Findings
- Crypto is the second-busiest category on Polymarket; sports leads on both Polymarket and Kalshi, crypto ranks second on each — [DataWallet](https://www.datawallet.com/crypto/prediction-market-statistics) (unverified; secondary summary)
- Taker fees first went live on 15-minute crypto markets on Jan 5, 2026, later extended to more categories — [DataWallet](https://www.datawallet.com/crypto/prediction-market-statistics) (unverified)
- Kalshi reportedly did $12.37B volume in July 2026 vs Polymarket's combined $5.70B; Polymarket's decline linked to fee changes and a Wisconsin lawsuit — [DeFiLlama](https://defillama.com/research/spotlight/are-prediction-markets-still-hot) (unverified; snippet via search summary)
- Kalshi + Polymarket combined 2025 volume reported above $44B — [KuCoin News](https://www.kucoin.com/news/flash/kalshi-and-polymarket-combined-2025-trading-volume-surpasses-44-billion) (unverified aggregator)
- Weekly prediction-market volume reportedly grew from ~$500M (June 2025) to nearly $6B (Jan 2026); ex-memecoin traders cited as migrating there — [PredictStreet via FinancialContent](https://www.financialcontent.com/article/predictstreet-2026-1-19-prediction-market-volume-hits-record-37-billion-as-traders-abandon-meme-coins) (promotional-style source; unverified)
- Memecoin trading volumes reportedly down ~85% from highs (undated, no primary dataset) — [Yahoo Finance](https://finance.yahoo.com/news/prediction-markets-vs-meme-coins-234051749.html) (directional only)
- Pump.fun-specific markets on Polymarket: "Pump.fun airdrop by ...?" (resolves by Dec 31, 2026; ~12-13% Yes, ~$2.77M volume per undated snapshot) — [Polymarket](https://polymarket.com/event/pumpfun-airdop-by), [Predscope](https://predscope.com/event/pumpfun-airdop-by); also "What price will Pump.fun hit before 2027?" — [PolymarketScan](https://polymarketscan.org/event/what-price-will-pumpfun-hit-before-2027)
- 2025 coverage: Polymarket gave ~1% for a June 2025 Pump.fun airdrop and ~30% by July 31 — [Coin Edition](https://coinedition.com/pump-fun-airdrop-heres-why-july/) (outdated)
- A "Pump.fun ATH this year" Polymarket market was reported split 50/50 — [CryptoRank](https://cryptorank.io/news/feed/52719-pump-fun-ath-this-year-polymarket-split-50-50-as-500m-meme-coin-factory-faces-crash-fears) (date unknown)

### Inferences
- Memecoin-specific markets are mostly "event" markets (token launch/airdrop, FDV, ATH) on big names, not tradable per-token price ladders; a bot cannot hedge arbitrary small-cap memecoins with them.
- Venue shift (Kalshi overtaking Polymarket by mid-2026) means liquidity for crypto contracts should be checked on both; Kalshi is US-regulated, Polymarket has fee/legal changes.
- Note possible inconsistency: Pump.fun's "airdrop" market (12-13% by end-2026) conflicts with my recollection that the PUMP token launched in July 2025; the market may concern a user airdrop specifically. Verify before use.

### Gaps
- No verified current data for TRUMP coin, other named memecoin markets, or crypto ETF approval markets (e.g., altcoin/memecoin ETFs); no order-book depth/spread figures; no data on Myriad, Opinion, Limitless liquidity beyond mentions.
- No November 2026 crypto-category volume figure.

## Q2. Do prediction-market odds lead crypto prices? Usable in a trading bot?

### Takeaway
I found no rigorous (academic or quantitative) evidence that prediction-market odds lead crypto prices; available evidence is anecdotal and suggests odds mostly follow price. Their best use is as a sentiment/event-probability input or for hedging event risk, not as a standalone alpha signal.

### Cited Findings
- No peer-reviewed lead-lag study surfaced; coverage is news/snapshots (search result summary of [Blockworks](https://blockworks.co/news/empire-newsletter-bitcoin-price-trump-winning-odds), [Fortune](https://fortune.com/crypto/2024/11/16/how-high-will-bitcoin-go-btc-forecast-prediction-markets-polymarket-kalshi/), [Decrypt](https://decrypt.co/376103/bitcoin-price-pumping-prediction-next-move?amp=1))
- Polymarket Trump-win odds tracked BTC closely for ~3 months in 2024 but the link did not hold consistently outside that window — [Blockworks](https://blockworks.co/news/empire-newsletter-bitcoin-price-trump-winning-odds) (unverified paraphrase)
- Myriad bitcoin odds flipped to near coin-flip after a sharp rally, suggesting odds react to price — [Yahoo Finance](https://finance.yahoo.com/news/myriad-moves-bitcoin-odds-flip-220348172.html) (inference by summarizer)
- 10x Research argued BTC volatility may be mispriced on Polymarket versus institutional options — [Stocktwits](https://stocktwits.com/news-articles/markets/cryptocurrency/bitcoin-volatility-may-be-mispriced-on-ahead-of-fed-rate-cut-decision/cLIu6xuRENu) (analyst opinion, not a study)
- Prediction markets gave ~11% chance of BTC reaching $150k by end of 2026 per a Motley Fool piece — [AOL/Motley Fool](https://www.aol.com/articles/bitcoin-needs-monster-rally-hit-092000706.html) (opinion piece; outcome likely already known by Nov 2026, unchecked)

### Inferences
- Short-horizon price-threshold markets are essentially priced off spot/options-implied volatility, so they are more likely derivative of price than predictive; edge, if any, is in mispriced volatility vs options (cross-venue arbitrage), not directional lead.
- Event markets (ETF approval, listings, airdrops, policy) can carry genuine information ahead of announcements; those are the plausible signal use cases, with thin liquidity limiting size.
- Hedging value for memecoins is low: no matching contracts, so basis risk is high; BTC/ETH threshold contracts are the only liquid proxies.
- Taker fees (introduced 2026) erode high-frequency edges on 15-minute crypto markets.

### Gaps
- No Granger-causality/lead-lag study on odds vs BTC/memecoin returns found; would need own backtest using Polymarket CLOB/Kalshi API historical data.
- No evidence on bot profitability on these venues, API rate limits, or fee schedule details; not searched.
