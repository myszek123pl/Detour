# Memecoin perpetuals in 2026 (as of Nov 2026)

Method note: 4 web searches succeeded, 1 (JELLY) failed with a rate limit; no fetches. Search results are mostly aggregator snippets. Items marked [UNVERIFIED - training knowledge] have no source from this session and must not be presented as confirmed.

## Hyperliquid listings, HIP-3 and k-denominated meme perps

### Takeaway
HIP-3 (builder-deployed perps) went live in Oct 2025 and in 2026 is dominated by stocks, commodities and indices, not memecoins. I found no source showing memecoin markets on HIP-3. Core meme perps (kPEPE, kBONK style) are validator-listed, which is my training knowledge, not verified here.

### Cited Findings
- HIP-3 lets builders deploy perps that settle on Hyperliquid's shared order book; used mainly for stocks, commodities and indices — [Nansen](https://nansen.ai/post/what-is-hip-3-hyperliquid), [The Block](https://www.theblock.co/post/374306/hyperliquid-activate-hip-3-upgrade)
- HIP-3 markets reportedly reached nearly 50% of Hyperliquid perp volume — [The Block](https://www.theblock.co/amp/post/408064/hyperliquid-hip-3-markets-surge-50-perp-volume-onchain-stock-trading-grows); Coinperps reports record $115.1B HIP-3 volume in July 2026 — [Coinperps](https://www.coinperps.com/learn/hyperliquid-hip-3-statistics). Open-interest share figures conflict across sources (about 18% rising past 34% vs about 25% in September per Datawallet) — [Datawallet](https://www.datawallet.com/de/crypto/hip-3-explained-hyperliquid-upgrade)
- HIP-3 fee structure reported: users pay 2x the fee of validator-operated perps, deployer keeps 50% — [Datawallet](https://www.datawallet.com/de/crypto/hip-3-explained-hyperliquid-upgrade)
- A Sept 2026 opt-in permissioned-markets extension for HIP-3 was discussed by co-founder Jeffrey Yan — [Crowdfund Insider](https://www.crowdfundinsider.com/tag/hip-3/)
- Aggregate "MEME" token perp OI was only about $6M across 11 venues on May 23, 2026 — [Loris](https://loris.tools/markets/perps/meme)

### Inferences
- HIP-3's growth is an equities/commodities story, so meme-perp liquidity on Hyperliquid still sits in the core validator-listed markets, not HIP-3.
- A permissionless HIP-3 meme listing would carry more manipulation risk, given thin oracle liquidity (inference from the JELLY/POPCAT pattern below).

### Gaps
- No sourced list of current Hyperliquid meme perps or their OI. 
- [UNVERIFIED - training knowledge] The "k" prefix means 1000x contract denomination (kPEPE, kBONK, kSHIB, kFLOKI, kLUNC, kDOGS, kNEIRO) so that sub-cent prices are tradable. Confirm against Hyperliquid's docs.
- No evidence found of any HIP-3 meme market.

## Binance/Bybit meme perps and pre-launch perps

### Takeaway
Binance runs pre-market perps for tokens before spot listing, converting to standard perps at spot listing, and in 2026 also launched pre-IPO perps (SpaceX, OpenAI). Pre-launch perps are a gauge of day-one sentiment for new tokens. Bybit: nothing found.

### Cited Findings
- Binance pre-market perps convert to standard perps when spot lists; Binance can cap the mark price during pre-market — [Binance announcement (PUMPUSDT, Jul 2025)](https://www.binance.com/en-AE/support/announcement/detail/4bc8b483d10d4619babb2015066b2d89)
- 2026 pre-market examples (mostly non-meme): MEGAUSDT (Jan 30, up to 5x), FOGOUSDT, ESPUSDT (Feb 10), PREDICTUSDT (scheduled 2026-10-25, up to 5x) — search result summaries, original Binance pages not fetched ([Binance Square](https://www.binance.com/square/post/381013054654799))
- A March 2026 report covered a lobster-themed ("龙虾") meme perp listing — [MEXC News](https://www.mexc.com/news/685799) (low quality aggregator; exact URL-to-claim match not confirmed)
- Binance launched pre-IPO perps in May 2026, starting with SpaceX, then OpenAI; over $280M cumulative volume in the first five days — [AAP/Cision](https://www.aap.com.au/aapreleases/cision20260521ae65073/), [AAP/Cision OpenAI](https://www.aap.com.au/aapreleases/cision20260526ae67563/)
- MELANIA reportedly rose to $12.89 on Binance listing news (date unclear) — [CoinGape](https://coingape.com/binance-update-on-melania-sparks-optimism-amid-75-pump-whats-next/amp)

### Inferences
- A perp listing on a major CEX is itself a catalyst for memecoins, but the effect often fades; pre-market perp premium vs. later spot open is a usable day-one sentiment gauge.

### Gaps
- No Bybit-specific meme perp info found. 
- No verified full list of Binance meme perps in 2026; no data on pre-market perp price vs. eventual spot open.

## Funding and OI dynamics

### Takeaway
Meme OI is thin and moves fast; OI alone is direction-neutral and only meaningful read together with price and funding. Squeeze calls in the media are anecdotal, not backtested.

### Cited Findings
- Memecoin sector reportedly lost nearly $8B in 2026, multi-year lows — [MEXC News](https://www.mexc.com/news/1121845) (aggregator, unverified)
- PEPE Feb 2026: OI up about $30M to about $221M with negative funding, framed as short-squeeze setup; the same outlet later reported OI down about 36% in under 72h, about $200M wiped (date unconfirmed) — [AMBCrypto](https://ambcrypto.com/could-pepe-repeat-its-april-2024-rally-these-metrics-say-yes)
- OI does not indicate direction; interpret with price and funding — [CoinStats](https://coinstats.app/news/7f61bff7a752164f07ec7ac55cbed114ea6ce2238aa4f235cfb3441b0da33206_Open-Interest-Climbs-After-the-Short-Squeeze-Why-the-Longs-Are-Paying-Now)
- K33 (May 2026): BTC 30d funding negative with leverage growing, which could amplify a squeeze (BTC, not memes) — [K33](https://k33.com/research/articles/longest-streak-of-negative-funding-rates-in-the-2020s)
- SHIB OI returning in a weak market — [CryptoDaily](https://cryptodaily.co.uk/2026/05/shib-open-interest-meme-liquidity-weak-markets)

### Inferences
- Rule of thumb consistent with sources: price up + OI up + funding rising = leveraged longs (fragile); price flat/down + OI up + negative funding = crowded shorts (squeeze fuel). Not backtested.

### Gaps
- No rigorous study of funding/OI predictive power for memecoins; no Nov 2026 OI figures.

## Notable squeezes and manipulations (JELLY, POPCAT, others)

### Takeaway
No sourced material obtained this session (the JELLY search was rate-limited). Everything below is from training knowledge and must be verified before use.

### Cited Findings
- None sourced.

### Inferences
- [UNVERIFIED - training knowledge] JELLY (Mar 2025): a trader opened a large short on a low-liquidity token on Hyperliquid, pumped the spot price, and pushed the HLP vault into a large unrealized loss (reported about $12M). Validators voted to delist and settle at a fixed price (about $0.0095); Hyperliquid later tightened listing/OI limits. Exact figures need checking.
- [UNVERIFIED - training knowledge] POPCAT (Nov 2025): a whale reportedly used many wallets to build a large long and pulled support, leaving HLP with bad debt (reported about $5M). Exact date, size and amount need checking.
- Common pattern (inference): thin spot liquidity + oracle derived from that spot + large perp OI relative to market cap = manipulable.

### Gaps
- No confirmed details of JELLY, POPCAT or any other 2026 squeeze/manipulation event. Recommend a follow-up search (Hyperliquid official announcements, The Block, CoinDesk).

## Using perp data as signals or hedges for spot memecoin traders

### Takeaway
Sources support reading OI, funding and perp-vs-spot volume jointly, but no backtests exist in what I found. Hedging by shorting the perp is practical only for tokens with listed perps and carries funding cost, basis and liquidation risk.

### Cited Findings
- Funding flipping from positive to negative with steady OI is described as a mean-reversion setup, with false-flip risk around funding prints — [AMBCrypto](https://ambcrypto.com/?p=570179)
- Aggregate meme perp OI is very thin (about $6M for "MEME" in May 2026), so signals are noisy — [Loris](https://loris.tools/markets/perps/meme)

### Inferences
- Signals: (1) extreme positive funding + rising OI = overheated, take profit; (2) negative funding + rising OI + flat price = squeeze risk; (3) OI collapse after a spike = liquidation flush, often a local bottom attempt; (4) new CEX perp listing or pre-market premium = day-one sentiment.
- Hedges: short the same-token perp (delta hedge), or short BTC/ETH or a basket perp as a beta hedge when no perp exists; check that the hedge's funding cost and maximum leverage fit the holding period.
- Caution: prices on manipulable low-liquidity perps can be spoofed (see JELLY), so do not treat tiny-OI markets as clean signals.

### Gaps
- No backtest or quantitative evidence on predictive value; no sourced data on specific hedge costs.
