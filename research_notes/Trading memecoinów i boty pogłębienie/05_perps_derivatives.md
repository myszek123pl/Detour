# Memecoin perpetual futures and derivatives as signals (as of Nov 2026)

Method note: 4 web searches used (of ~6 budget); results were news aggregators, no primary exchange pages fetched. All figures are secondary-source and approximate.

## Which memecoins have perps; how perp listing affects spot

### Takeaway
Binance/Hyperliquid perp listings often coincide with short-lived spot pumps (MOODENG, POPCAT, PONKE) that frequently retrace; the effect is inconsistent and only anecdotally documented. Futures delistings can trigger short squeezes (MEMEFI).

### Cited Findings
- MOODENG reportedly rose ~90% (headline) when Binance launched its perpetual contract — [Coingape](https://coingape.com/moodeng-price-blows-up-90-as-binance-launches-perpetual-contract/)
- POPCAT rose >20% after Binance Futures and KuCoin listings (Aug 2024) — [FXStreet](https://www.fxstreet.com/cryptocurrencies/news/solana-meme-coin-popcat-surges-over-20-following-binance-futures-and-kucoin-listings-202408222318)
- PONKE gained ~12% within minutes of Binance listing, then fully retraced (search summary of BeInCrypto) — [BeInCrypto](https://beincrypto.com/ponke-binance-listing-price-impact)
- MEMEFI: Binance futures delisting forced shorts to cover; spot up >190% in 24h (summary figure) — [BeInCrypto](https://beincrypto.com/memefi-binance-futures-delisting-short-squeeze)
- Counterexamples: CHEEMS and WHY futures fell after Binance listing; CGPT briefly doubled then fell below pre-listing level (per summary of Odaily/others) — [Odaily](https://www.odaily.news/en/post/5200023)
- An analyst tally of 2024 Binance memecoin listings claimed 80% saw significant market-cap growth, small sample, only five with both spot and futures — [Cointelegraph](https://cointelegraph.com/news/binance-memecoins-2024-listings)
- Hyperliquid HIP-3 (builder-deployed perps) requires 500K HYPE stake; HIP-3 OI reported ~$790M (Jan 2026), record ~$2.38B (Apr 2026), later claims of ~$4B+ (unverified/inconsistent); mix dominated by equities/commodities/pre-IPO, not memecoins — [Coin Metrics](https://coinmetrics.substack.com/p/state-of-the-network-issue-368), [The Block](https://www.theblock.co/news/web3/2026-04-15-hip-3-open-interest-2-billion-demand-24-7-tokenized-equity-exposure-397276), [Cointelegraph](https://cointelegraph.com/news/hyperliquid-hip-3-open-interest-hits-793m-on-commodities-surge)

### Inferences
- Perp listing announcement is an event trigger with short-lived, high-variance upside; survivorship bias likely in anecdotes. A spot bot should treat it as a momentum-then-fade setup, not a hold signal.
- Delisting/OI-forced-cover events can be squeeze triggers (inference from MEMEFI single case).

### Gaps
- No complete list of memecoins with perps on Hyperliquid/Binance/Bybit found (changes frequently; pull from exchange APIs: Hyperliquid `meta`, Binance `exchangeInfo`, Bybit instruments).
- Pre-market perps (Hyperliquid pre-launch/HIP-3, Binance pre-market, Bybit pre-market): no memecoin-specific data found; none verified.
- No rigorous event-study on listing effect on spot.

## Funding rates and open interest as predictors of squeezes/tops

### Takeaway
Conceptually, deeply negative funding plus high OI = crowded shorts = squeeze fuel; very high positive funding plus rising OI = crowded longs = long-squeeze/top risk. No rigorous memecoin-specific backtest found; evidence is commentary and contradictory.

### Cited Findings
- Bybit education: deeply negative funding signals crowded shorts; high OI amplifies squeeze severity — [Bybit](https://www.bybit.com/en/wiki/article/what-is-a-short-squeeze-crypto-definition/)
- BTC anecdote: funding flips to negative preceded +80% (Sep 2024) and +150% (Jul 2023) moves per CryptoQuant data — [Cointelegraph](https://cointelegraph.com/news/bitcoin-price-rallied-80-the-last-time-btc-funding-rates-flipped-red)
- Finbold published opposite calls (short setup vs long squeeze) on PEPE from similar high-funding/rising-OI signals — [Finbold](https://finbold.com/short-selling-opportunity-as-this-crypto-registers-high-funding-rates), [Finbold](https://finbold.com/long-squeeze-alert-this-cryptocurrency-could-crash-30-soon/)
- A DEV Community post claims backtests; could not verify — [DEV](https://dev.to/trendrider/funding-rates-open-interest-predict-squeezes-2026-i50)

### Inferences
- Funding/OI are better as regime/risk filters (avoid entering when funding extreme and OI spiking relative to market cap) than standalone directional predictors. Normalize OI by spot market cap/liquidity.

### Gaps
- No academic or backtested memecoin result; would need own study (CoinGlass / exchange history).

## Liquidation dynamics and manipulation (JELLY, POPCAT)

### Takeaway
Thin-liquidity memecoins on Hyperliquid have repeatedly been used to attack the HLP vault/liquidation mechanism; perp price can detach from spot and cause forced settlement or delisting.

### Cited Findings
- JELLYJELLY (Mar 2025): trader shorted a thin Solana token, pumped its onchain price, forced own liquidation, leaving HLP with the loss; validators voted to delist and settle at $0.0095; exploiter profit estimates ~$6.26M (CoinMarketCap says $6.2M; headline of another says $12M manipulation — sources differ); users reimbursed except exploiter; criticized as centralized response — [The Block](https://www.theblock.co/news/defi/2025-03-26-hyperliquid-delists-jellyjelly-memecoin-amid-whale-manipulation-fiasco-348314), [CoinMarketCap](https://coinmarketcap.com/academy/article/hyperliquid-delists-jellyjelly-perpetual-futures-after-dollar12-million-market-manipulation), [Decrypt](https://decrypt.co/311713?amp=1)
- POPCAT (Nov 2025): account built leveraged longs with a large buy wall, cancelled it, price fell ~30% in seconds; HLP bad debt up to ~$4.9M (reported $5M); described as third manipulation attack in 2025 after JELLY and TST (July) — [Yahoo Finance](https://finance.yahoo.com/news/hyperliquid-hit-third-market-manipulation-113215395.html)
- Post-JELLY JELLY spot pumped sharply while delisting; whale reportedly retained ~10% of supply — [CoinMarketCap](https://coinmarketcap.com/academy/article/hyperliquid-whale-retains-10percent-of-jelly-meme-coin-after-dollar62-million-exploit-and-exchange-delisting)

### Inferences
- Perp price moves on thin names may be manipulation-driven, not information: a spot bot should discount signals from low-liquidity perps and avoid tokens where perp OI is large relative to spot liquidity (also a risk of being the exit liquidity).
- Delisting/force-settlement events are discrete risks for any perp-linked strategy.

### Gaps
- Exact current Hyperliquid mitigations (OI caps, leverage limits) post-POPCAT not verified.

## How a spot bot can use derivatives data

### Takeaway
Use as filters and event triggers: (1) perp-listing announcement watch (fade or momentum scalp with tight exits), (2) funding/OI-to-market-cap as crowding filter, (3) OI drops/liquidation clusters as squeeze or capitulation markers, (4) perp-vs-spot divergence as manipulation flag. All are untested hypotheses from this research.

### Cited Findings
- See above sections; no source directly documents a spot bot using these signals.

### Inferences
- Concrete rules to backtest: skip entries when funding > extreme percentile and OI/mcap high; flag new perp listings on Binance/Bybit/Hyperliquid via API polling; compare perp mark vs spot DEX price; track liquidation feeds for squeeze entries with strict time stops.

### Gaps
- No backtests; Bybit/Binance listing-announcement latency and pre-market perp data not researched.
