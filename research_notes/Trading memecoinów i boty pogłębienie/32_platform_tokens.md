# Platform/ecosystem tokens tied to memecoin activity (PUMP, BONK/letsbonk, JUP, RAY, MET): buybacks, correlation with memecoin volume, use as bot macro gauge

Research date: Nov 2026. 4 web searches used. Searches returned summaries; several figures conflict. Items marked [UNVERIFIED] were not confirmed against primary sources.

## How do platform revenue buybacks work (PUMP, BONK/letsbonk, JUP, RAY, MET)?

### Takeaway
Each platform routes a share of fee revenue into open-market purchases (and often burns). Share and cadence differ and changed repeatedly in 2025-26. Pump.fun moved from 100% of revenue to a locked 50% program in April 2026. Evidence that buybacks lift price is weak (Jupiter, PUMP).

### Cited Findings
- Pump.fun, Apr 28 2026: moved from using all revenue for PUMP buybacks to programmatic buy-and-burn funded by 50% of net revenue (bonding curve, PumpSwap, Terminal) for one year via a locked smart contract. It burned the previously repurchased PUMP, about 36% of circulating supply (~$370M). The co-founder said the other half funds product, hiring, marketing and acquisitions. — [CoinDesk](https://www.coindesk.com/markets/2026/04/29/pump-fun-burns-36-of-pump-supply-in-usd370-million-wipe-locks-50-revenue-into-ongoing-buybacks); [The Block](https://www.theblock.co/news/ecosystems/2026-04-28-pump-fun-burns-370-million-pump-399288)
- Pump.fun had cumulatively repurchased ~$323.4M of PUMP (28.8% of circulating supply) as of March 2026. — [The Block / search summary](https://www.theblock.co/news/ecosystems/2026-04-28-pump-fun-burns-370-million-pump-399288) [UNVERIFIED exact figure; from search summary]
- Pump.fun revenue: 2025 gross ~$971M per DefiLlama via CoinDesk; 2026 annualizing to ~$320M (another DefiLlama figure in the same article says ~$416M, so sources differ). — [CoinDesk](https://www.coindesk.com/markets/2026/04/29/pump-fun-burns-36-of-pump-supply-in-usd370-million-wipe-locks-50-revenue-into-ongoing-buybacks)
- Coverage noted that ~$350M of PUMP buybacks failed to lift the token price. — [BeInCrypto via TradingView](https://www.tradingview.com/news/beincrypto:8f5a95c22094b:0-pump-fun-350-million-pump-buybacks-fail-to-lift-token-price/)
- letsbonk: July 2025 pledge of 1% of total revenue (from marketing fund) to buy back top tokens in the BONK ecosystem. — [The Block](https://www.theblock.co/amp/post/364031/memecoin-launchpad-letsbonk-pledges-1-of-revenue-to-buyback-top-tokens)
- letsbonk burn share reported inconsistently: 35% early, 50% later; Blockworks Q1 2026 holder report cites a December 2025 governance-mandated 51% fee redirect, with ~472.7M BONK burned across 89 burn events in the quarter. July 24 2025 burn: 500B tokens (~$16.7M). — [Blockworks Q1 2026 report](https://blockworks.com/api/investor-report/bonk-token-holder-report-q1-2026/pdf); [BeInCrypto](https://beincrypto.com/letsbonk-buyback-bonk-meme-coins) [UNVERIFIED current split]
- Jupiter: half of protocol fees committed to JUP buybacks from Feb 2025; ~$70M spent in 2025; in Jan-Mar 2026 co-founder Siong Ong questioned/asked the community whether to end or pause the program due to limited price impact. Outcome not found. — [Cointelegraph](https://cointelegraph.com/news/jupiter-buybacks-top-100m-annually-research); [Cryptopolitan](https://www.cryptopolitan.com/jupiter-co-founder-ending-jup-buybacks/); [Stocktwits](https://stocktwits.com/news-articles/markets/cryptocurrency/jupiter-ticks-higher-as-ceo-weighs-pausing-buybacks-after-70-m-spent-in-2025/cmxo41nR4Gj)
- Raydium: 12% of transaction fees used to buy back RAY; reportedly accumulated ~20% of supply (undated Blockworks quote). Coverage frames it as the more successful program. — [Blockworks](https://blockworks.co/news/value-accrual-matters-for-tokens) [UNVERIFIED date/figure]
- Meteora (MET): part of DLMM/DAMM trading fees goes to discretionary buybacks; first buyback 2.3% of supply for ~10M USDC (late 2025). An Aug 2026 Ainvest piece says no confirmed source shows fees flowing to MET holders. — [DefiLlama](https://defillama.com/token/met); [KuCoin](https://www.kucoin.com/news/flash/meteora-completes-2-3-met-buyback-with-10m-usdc-launches-comet-points-economic-system); [Ainvest](https://www.ainvest.com/news/meteora-met-slips-5-pushing-0-18-lp-stimulus-season-2-meets-aug-23-unlock-2608/)

### Inferences
- Buybacks are mechanically tied to fee revenue, which is tied to memecoin trading volume, so buyback flow is itself pro-cyclical. Programs are policy-dependent (can be cut, e.g. Pump 100% to 50%, Jupiter under review), so a bot should not assume constant buyback bid.
- Discretionary programs (MET, Jupiter) are poorer signal than programmatic ones (Pump's locked contract, letsbonk burns) because timing is not rule-based.

### Gaps
- Post-April-2026 PUMP buyback totals and current run-rate not found.
- Current letsbonk burn share (35/50/51%) not reconciled; letsbonk market share vs Pump.fun in late 2026 not researched.
- Final outcome of the Jupiter buyback review not found.
- RAY buyback current status/date not confirmed.

## Correlation of these tokens with memecoin volume

### Takeaway
No quantitative correlation study was found. Qualitative sources link MET, PUMP and RAY to Solana memecoin activity, but token prices have decoupled from revenue/buybacks at times.

### Cited Findings
- Messari frames MET as a bet on Solana memecoin activity: Meteora captures ~30% of Fomo's Solana memecoin volume and 25-35% of memecoin flows routed via Jupiter. — [Messari](https://messari.io/report/a-meteoric-bet-on-memecoins)
- Meteora volume grew ~50% in September (2025); briefly passed Raydium in 24h volume in Aug 2025 on the YZY memecoin surge. — [CoinMarketCap Academy](https://coinmarketcap.com/academy/article/pump-price-rises-met-falls); [Crypto Times](https://www.cryptotimes.io/2025/12/11/solana-based-dex-aggregator-meteora-unveils-10m-token-buyback/)
- Divergence example: PUMP +18% in a week while MET -14%. — [CoinMarketCap Academy](https://coinmarketcap.com/academy/article/pump-price-rises-met-falls)
- Pump.fun daily revenue has at times topped Hyperliquid during memecoin rebounds. — [The Block](https://www.theblock.co/post/370812/pump-fun-surpasses-hyperliquid-revenue)
- MET price snapshots conflict: DefiLlama ~$0.13 with ATL in May 2026; Ainvest ~$0.18 (Aug 2026). — [DefiLlama](https://defillama.com/token/met); [Ainvest](https://www.ainvest.com/news/meteora-met-slips-5-pushing-0-18-lp-stimulus-season-2-meets-aug-23-unlock-2608/)

### Inferences
- Revenue (volume) correlation is likely high, price correlation looser: unlocks, supply burns, and token-specific events (buyback announcements, e.g. MET dipped after its announcement) dominate short-term price.
- The decline of Pump.fun revenue from $971M (2025) to a ~$320-416M annualized 2026 pace suggests the memecoin volume cycle cooled in 2026, and platform tokens were likely under pressure; not verified with price data.

### Gaps
- No computed correlations (price vs memecoin volume, lag structure). Would require daily series from DefiLlama/Dune/CoinGecko; recommend computing directly.
- Current Nov 2026 prices and volumes not retrieved.

## Use as a macro gauge for a trading bot

### Takeaway
Better gauge inputs are the underlying fundamentals (platform daily revenue, launch counts, graduation rate, DEX memecoin volume) than the token prices; token prices are noisy, supply-event driven and may lag or diverge. Treat as a regime/risk-on filter, not an entry signal. This is inference; no source tested it.

### Cited Findings
- Platform revenue is public and on-chain (DefiLlama tracks Pump.fun revenue and token pages for PUMP and MET). — [DefiLlama PUMP](https://defillama.com/token/pump); [DefiLlama MET](https://defillama.com/token/met)
- Buyback programs have had limited demonstrated price impact (Jupiter ~$70M, PUMP ~$350M). — [Cointelegraph](https://cointelegraph.com/news/jupiter-buybacks-top-100m-annually-research); [TradingView/BeInCrypto](https://www.tradingview.com/news/beincrypto:8f5a95c22094b:0-pump-fun-350-million-pump-buybacks-fail-to-lift-token-price/)

### Inferences
- Candidate composite: z-score of (Pump.fun + letsbonk + Meteora daily fees) 7d vs 30d, plus relative strength of PUMP/BONK/MET vs SOL. Rising fees with a rising basket = risk-on; fees falling while tokens bounce = fade.
- Use buyback-per-day / token-market-cap as a secondary signal only for programmatic programs.
- Watch for token unlocks (e.g. MET Aug 2026 unlock) and policy changes as false-signal sources.
- Backtest the lead/lag before use; none is documented in sources.

### Gaps
- No published evidence that these tokens lead or lag memecoin volume. Launchpad tokens beyond PUMP/BONK (other 2026 launchpads) not researched.
