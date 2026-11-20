# Macro and Cross-Asset Drivers of Memecoin Markets (as of 20 Nov 2026)

> **Method note (read first):** In this session WebFetch could not reach any target host (blockworks.com, arxiv.org and gncrypto.news all returned DNS or allowlist failures). The shared WebSearch budget also ran out after about 11 queries. So every finding below comes from **search-result summaries and snippets**, not full-text reads of the primary documents. Treat exact figures as "reported by X", and verify against the primary source before publishing. I found **no data later than about Sept 2026**, so Oct–Nov 2026 market state is a gap.

## 1. Correlation / beta of memecoin indices vs BTC and SOL

### Takeaway
Memecoins are widely treated as a high-beta, levered expression of BTC and SOL risk. However, I found **no rigorous, dated regression-beta estimate** for a memecoin index (CoinGecko meme category, GMCI Meme, or a Solana-meme basket) in 2025–2026. The best available numbers are an older, unverified ~0.85 correlation to BTC for large memes, and anecdotal "2–3x BTC move" episodes from 2026.

### Cited Findings
- A Blockworks 0xResearch beta study ("What actually outruns Bitcoin?") covered nine BTC-linked assets over about two years. SOL, MSTR, BMNR, ETH and COIN kept a **180-day beta to BTC near or above 1, with correlation ≥0.7**. Memecoins were apparently not in the high-beta set studied. Per the search summary; full text not read. — [Blockworks 0xResearch](https://blockworks.com/newsletter/0xresearch/issue/post_f60020e1-305a-4516-b988-2237bbf07547); also syndicated at [TechFlow](https://techflowpost.com/en-US/article/34412)
- A Medium analysis of 2019–2024 data argues memecoins have **beta >1 vs BTC**. It cites a Gate.io report for **correlation ≈0.85 between BTC and DOGE/SHIB/PEPE**. The underlying Gate.io report could not be located, so this is a secondary, unverified figure. — [Medium, "Price Correlation Between Major Cryptocurrencies and Memecoins (2019–2024)"](https://medium.com/@gwrx2005/price-correlation-between-major-cryptocurrencies-and-memecoins-2019-2024-6ce899224366)
- An older IntoTheBlock figure, cited by FXStreet (Mar 2024), gives an **87% DOGE–BTC correlation**. No window or methodology is given. — [FXStreet](https://fxstreet.com/cryptocurrencies/news/memecoins-market-capitalization-exceeds-50-billion-above-nfts-defi-sector-202403041700)
- An arXiv preprint (Dec 2025) proposing a memecoin "fragility" framework says the prior literature is fragmented and **mostly single-asset volatility/attention studies**. It sizes the memecoin market at **~USD 84B as of Oct 2025**. — [arXiv 2512.00377](https://arxiv.org/pdf/2512.00377.pdf)
- Return-amplification anecdotes from 2026:
  - In an August 2026 rally, **WIF rose ~44%, about 3x DOGE's move**. — [Cryptonews](https://cryptonews.com/cryptocurrency/best-meme-coins/) (promotional site; low reliability)
  - In a late-Sept 2026 week, **PEPE and WIF rose >40% over 7 days vs ~18% for DOGE and ~12% for BTC**, which implies roughly 3.5x BTC on the upside for mid-cap memes and ~1.5x for DOGE. — [BeInCrypto](https://beincrypto.com/3-meme-coins-watch-fourth-week-september/)
- The Block's **GMCI Meme Index reportedly outperformed BTC by 150% over a six-month window**. This is a return comparison, not a beta, and the period is unclear. — [CFC St. Moritz](https://cfc-stmoritz.com/industry-insights/beyond-bitcoin-leveraging-memecoins-for-portfolio-diversification-and-enhanced-returns)
- Kaiko (July 2025, "Gap Grows Between Bitcoin and Altcoins"):
  - Altcoins carry "significantly higher risk than BTC, primarily due to their weaker liquidity infrastructure."
  - Offshore venues handle **~90% of altcoin volume**.
  - Small-cap activity was "fading", which Kaiko read as a retreat from risk.
  — [Kaiko Research](https://research.kaiko.com/insights/gap-grows-between-bitcoin-and-altcoins)
- MEXC "crypto pulse" pages give a memecoin–ETH correlation of ~0.65 with no sourcing. **Treat as unreliable.** — [MEXC](https://www.mexc.com/vi-VN/crypto-pulse/article/memecoin-vs-bitcoin-altcoins-669)

### Inferences
- The tiers that are consistent with the evidence:
  - Large, CEX-listed memes (DOGE, SHIB, PEPE) behave like **high-correlation (~0.8+), beta ~1.5–2x** BTC proxies.
  - Mid-cap Solana memes (WIF, BONK, etc.) show **beta of about 2.5–4x on rally weeks**, with lower and less stable correlation.
  - Long-tail launchpad tokens are dominated by idiosyncratic and attention factors, so their correlation to BTC is low even though aggregate launchpad volume is pro-cyclical.
  These ranges are inferred from the anecdotes above, not estimated by regression.
- SOL itself has beta ≈1+ to BTC (Blockworks). Solana memes therefore carry a **compounded BTC→SOL→meme exposure**, plus a Solana-specific liquidity channel (see Section 2).
- Betas are asymmetric. Drawdowns in thin-liquidity memes exceed what upside beta implies, because liquidity evaporates in sell-offs (see the Oct 2025 crash in Section 3).

### Gaps
- No primary, dated rolling-beta estimate (e.g., 30/90/180-day OLS) of the CoinGecko meme category or a Solana-meme basket vs BTC or SOL for 2025–2026. This would need to be computed from CoinGecko or Kaiko price data, or found in a paywalled Kaiko, Glassnode or Blockworks report.
- I could not read the Blockworks beta study in full, so its exact numbers and asset list are unconfirmed.
- No sources found on memecoin correlation to macro assets such as the Nasdaq, DXY or the 10-year yield.

## 2. Stablecoin supply on Solana, SOL price, network activity and memecoin volume

### Takeaway
Memecoin manias pull stablecoins onto Solana, not the other way round. The TRUMP launch (Jan 2025) drove Solana stablecoin supply to a then-record **>$10B (+~57%)** and DEX volume to **$25–39B/day**. By early 2026, Solana stablecoin activity had shifted toward SOL–stablecoin and payments flows ($650B monthly stablecoin transfer volume in Feb 2026). That makes stablecoin supply a weaker real-time proxy for meme activity than it was in 2024–early 2025.

### Cited Findings
- **Stablecoin supply jumped during the TRUMP launch:**
  - Solana stablecoin supply passed **$10B for the first time** in Jan 2025. The Block attributes this to memecoin trading volume over the prior year, "further buoyed by" the Trump-family memecoin launches. — [The Block](https://www.theblock.co/post/336506/solana-based-stablecoin-supply-hits-new-peak-surpassing-10-billion)
  - Blockworks reported a **57% increase** in Solana stablecoin supply after the TRUMP launch. — [Blockworks](https://blockworks.co/news/solana-stablecoin-supply-soars)
  - CCData reported Solana stablecoin TVL **doubled** on the TRUMP frenzy. — [The Defiant](https://thedefiant.io/solana-stablecoin-tvl-doubles-on-trump-frenzy-ccdata)
- **DEX volume during the TRUMP launch:**
  - Solana DEX volume hit records of **>$25B daily**, which was **74% of all-chain DEX volume** (CoinDesk, 24 Jan 2025). — [CoinDesk](https://hotfix.coindesk.com/markets/2025/01/24/trump-token-frenzy-drives-solana-stablecoin-supply-to-usd10b-record-dex-volumes)
  - Helius gives record days of **$28.2B (19 Jan) and $39.2B (20 Jan 2025)**. It puts the pre-launch baseline at **~$6B/day** and post-launch volume still elevated at **~$10B/day**. — [Helius Trump Memecoin Report](https://helius.dev/blog/trump-solana-memecoin-records-trends-insights)
  - DefiLlama data cited by CryptoSlate gives **$16.87B (17 Jan), $28.28B (18 Jan), $27B (19 Jan)**, which it compares to ~10% of Nasdaq daily volume. — [CryptoSlate](https://cryptoslate.com/insights/trumps-meme-coin-catapults-solana-dex-activity-to-match-10-of-nasdaqs-daily-volume/)
  - Blockworks Research reported **$39B on Sunday** (19 Jan). — [Blockworks](https://blockworks.co/news/trump-memecoins-rock-solana)
  - CoinMarketCap Academy's TRUMP/MELANIA piece says Solana handled the load, but dApps and front-ends struggled. — [CoinMarketCap Academy](https://coinmarketcap.com/academy/article/dollartrump-and-dollarmelania-show-solana-is-ready-for-mass-adoption-but-the-dapps-arent)
- **The 2026 regime shift:**
  - Grayscale (reported 4 Mar 2026) says Solana stablecoin **transaction volume reached $650B in Feb 2026**, more than double the prior monthly record.
  - Grayscale describes a shift on Solana **from memecoin-driven trading toward SOL–stablecoin activity and payments**.
  — [The Block](https://www.theblock.co/post/392217/solana-stablecoin-volume-record-650-billion-february-onchain-payments-demand-grayscale)
- A KuCoin flash note reports Solana stablecoin supply **>$15.58B** in a February. The year is unclear, likely 2026. It also reports Solana derivatives OI at ~$6B. — [KuCoin](https://www.kucoin.com/news/flash/solana-stablecoin-supply-surpasses-15-58-billion-derivatives-open-interest-rises-to-6-billion)
- **Launchpad volume cycles with the wider market:**
  - Pump.fun volume **fell 63% from Jan to Feb 2025**. — [Cointelegraph](https://cointelegraph.com/news/pumpfun-volume-drops-by-63-january-february)
  - PumpSwap volume hit **~$1.21B on 5 Jan 2026** (DeFiLlama). — [KuCoin](https://www.kucoin.com/news/flash/solana-memecoin-frenzy-drives-pumpswap-trading-volume-to-1-2-billion)
  - Pump.fun revenue was **>$23M** in a late-Jan 2026 burst. — [FXStreet](https://www.fxstreet.com/cryptocurrencies/news/pumpfun-breaks-out-as-meme-coin-activity-soars-driving-revenue-above-23-million-202601271448)

### Inferences
- Causality mostly runs **from meme attention to stablecoin inflows and DEX volume**: stablecoins are bridged in to buy. Stablecoin supply then persists after the mania fades. Post-TRUMP DEX volume settled at about $10B/day vs a ~$6B baseline, while stablecoin supply stayed elevated. So supply is a **lagging, sticky** indicator, and daily DEX volume and launch counts are the **coincident** indicators.
- From 2026, payments and stablecoin-transfer growth on Solana (Grayscale) means chain-level stablecoin metrics **overstate meme liquidity**. Bot and strategy builders should track meme-specific flows instead, such as pump.fun or PumpSwap volume, new-token launches per hour, and SOL/stable DEX pair volume on meme venues.
- Higher SOL prices raise the dollar value of SOL-denominated meme liquidity and the wealth of SOL-native traders. That reinforces the SOL→meme beta channel in Section 1.

### Gaps
- No quantitative elasticity or regression of meme volume on Solana stablecoin supply or SOL price was found. Dune dashboards could provide one, but I could not access them here.
- No confirmed figure for Solana stablecoin supply in Oct–Nov 2026.
- No 2025–2026 figure was found for meme share of Solana DEX volume (Blockworks Research and Messari likely have one, behind a paywall).

## 3. Event shocks: TRUMP/MELANIA, LIBRA, Oct 2025 cascade, 2026 shocks

### Takeaway
Shocks fall into two types:
- **Idiosyncratic political-meme events** (TRUMP, LIBRA). These cause liquidity cannibalisation and crashes in confidence within the meme complex.
- **Macro or leverage shocks** (the 10 Oct 2025 tariff-triggered $19B liquidation, and the Jan–Feb 2026 metals-margin-call crash). These hit memes hardest through thin liquidity.

The meme sector fell from a ~$135–150B peak (Nov–Dec 2024) to **~$24.5B by mid-June 2026 (−82%)**.

### Cited Findings
**TRUMP / MELANIA (17–20 Jan 2025)**
- TRUMP launched 17 Jan 2025 and reached **~$9B market cap within hours**, passing PEPE and BONK. — [Coin360](https://coin360.com/news/trump-official-meme-coin-sparks-market-buzz)
- Helius: TRUMP **"sucked liquidity from most other Solana memecoins"**, causing them to fall. — [Helius](https://helius.dev/blog/trump-solana-memecoin-records-trends-insights)
- Other Trump-themed memes briefly spiked, then **dropped 20–50%**. — [Coin360](https://coin360.com/news/trump-official-meme-coin-sparks-market-buzz)
- Meteora's share of Solana meme volume went from **<10% to ~60% from 18 Jan**. — [Helius](https://helius.dev/blog/trump-solana-memecoin-records-trends-insights)
- TRUMP price and daily volume had **collapsed substantially within about two weeks**. — [Decrypt](https://decrypt.co/303647/trump-solana-trading-volume-collapses?amp=1)

**LIBRA scandal (14–18 Feb 2025)**
- LIBRA was endorsed by Argentine President Milei. It reached a **~$4.4–4.6B market cap within about 5 hours, then crashed 89–96%**. Trading volume was **~$1.1B within hours**. — [Decrypt](https://decrypt.co/306134/did-argentina-president-javier-milei-launch-solana-meme-coin?amp=1); [DL News](https://www.dlnews.com/articles/markets/how-did-milei-libra-memecoin-crash)
- Pump.fun reaction:
  - Daily volume **fell 27% ($184M → $134M)** in the days after the endorsement (Dune).
  - Daily token launches fell from **61,800 (20 Jan) to 27,800** (18 Feb 2025).
  — [Decrypt](https://decrypt.co/306807/pump-fun-activity-cools-milei-solana-meme-coin)
- Solana DEX volume had declined **five consecutive weeks, >60% off its peak**, by mid-Feb 2025. This reflects the general meme unwind, not LIBRA alone. — [The Defiant](https://thedefiant.io/solana-crashes-as-argentina-president-milei-s-libra-rugpull-hits-credibility)
- Commentary at the time framed LIBRA as a potential "deathblow" for the memecoin craze, and noted that political endorsements were driving rug pulls. — [CoinDesk](https://hotfix.coindesk.com/de/business/2025/02/18/will-argentina-president-milei-s-crypto-fisco-be-a-deathblow-for-memecoin-craze); [CoinDesk opinion](https://hotfix.coindesk.com/opinion/2025/03/27/the-usdlibra-debacle-political-endorsements-are-driving-rug-pulls)

**Trump–Musk feud (June 2025)**
- The public Trump–Musk feud became a short-lived memecoin "meta" that drove a surge in trading volume. This is an example of politically driven attention shocks creating volume rather than destroying it. — [CryptoSlate](https://cryptoslate.com/trump-musk-feud-becomes-memecoin-meta-leads-to-surge-in-trading-volume/)

**Sept 2025 Fed-cut expectations**
- Memecoins rallied as traders bet on a Fed rate cut and US altcoin ETFs (CoinDesk, 13 Sept 2025). — [CoinDesk (mirror)](https://irishnews.pages.dev/crypto-news-coindesk.com/id/markets/2025/09/13/memecoins-rally-as-traders-bet-on-fed-rate-cut-and-u-s-altcoin-etfs)
- Keyrock (22 Sept 2025) noted that after the cut, the pullback "highlights fading risk appetite", a "cuts without conviction" read. — [Keyrock](https://keyrock.com/cuts-without-conviction/); see also [Keyrock 15 Sept](https://keyrock.com/fed-at-the-crossroads/), [Wintermute 15 Sept 2025](https://www.wintermute.com/insights/market-color/market-update/market-update-15-sept-2025)
- Earlier precedent: after the Fed's 50bp cut in Sept 2024, BTC rose >8% in a week. Kaiko suggested BTC is less sensitive to rate-path changes than altcoins. — [Kaiko](https://research.kaiko.com/insights/feds-jumbo-rate-cut-boosts-risk-on-sentiment)

**10–11 Oct 2025 liquidation cascade ("Crypto Black Friday")**
- Trigger: a surprise Trump tariff announcement on Friday afternoon, 10 Oct 2025. — [Crypto Times](https://www.cryptotimes.io/2025/10/11/massive-19b-liquidation-hits-crypto-markets-after-trump-tariffs/); [CoinGecko Learn](https://www.coingecko.com/learn/october-10-crypto-crash-explained)
- Size:
  - **~$19.15B** liquidated ($16.69B longs / $2.46B shorts). — [KuCoin](https://www.kucoin.com/news/flash/crypto-market-sees-19-15b-liquidation-event-on-october-10-2025)
  - Other tallies are **$19.3B in 24h**, and **$9.89B in 14h** in a narrower window. — [CryptoSlate](https://cryptoslate.com/?p=502753); [Amberdata](https://blog.amberdata.io/how-3.21b-vanished-in-60-seconds-october-2025-crypto-crash-explained-through-7-charts)
  - Amberdata's headline: **$3.21B vanished in 60 seconds**. — [Amberdata](https://blog.amberdata.io/how-3.21b-vanished-in-60-seconds-october-2025-crypto-crash-explained-through-7-charts)
  - A ~40-minute cascade liquidated about **$6.93B**, and market depth reportedly **collapsed ~98%**. The depth figure comes from a lower-tier outlet. — [Insights4VC](https://insights4vc.substack.com/p/inside-the-19b-flash-crash?open=false)
- Effect on memecoins:
  - Mid-caps and memecoins had **deeper, faster drawdowns on thinner liquidity**. — [WisdomTree](https://www.wisdomtree.com/onchain/insights/blog/whats-hot-leverage-liquidity-and-panic)
  - Large caps rebounded, while **many thin-liquidity memecoins did not**. — [GN Crypto (search summary)](https://www.gncrypto.news/news/altcoin-crash-october-2025-market-collapse/)
  - A prior surge of minimally screened meme launches had overheated the market and thinned liquidity. — [CryptoSlate](https://cryptoslate.com/a-blip-in-uptober-cryptos-october-reckoning-beyond-the-20b-washout/?rand=6792)
- BTC's all-time high was on **6 Oct 2025**, four days before the crash. — [CryptoDispensers Feb 2026 review](https://www.cryptodispensers.com/market-analysis/february-2026)

**Jan–Feb 2026 crash**
- Trigger: a precious-metals crash on 30–31 Jan 2026 caused cross-portfolio margin calls.
- Price: BTC fell from **~$90K to a $60,033 low** between 28 Jan and 11 Feb 2026, its steepest correction since FTX.
- Liquidations: **$2.56B** by 1 Feb and **$2.67B** on 5 Feb.
- On 5 Feb: BTC ~$66.65K, ETH ~$1,960, SOL ~$83.
- Overall, BTC was about **−50% from the 6 Oct 2025 ATH**.
— [Coinchange](https://www.coinchange.io/blog/the-2-trillion-crypto-crash-how-februarys-liquidation-revealed-the-markets-leverage-addiction); [Amberdata](https://blog.amberdata.io/bitcoin-below-70k-the-crash-the-data-and-what-comes-next); [Coinfomania](https://coinfomania.com/crypto-liquidation-2-6b-leverage-flush-bitcoin-ethereum/); [CryptoDispensers](https://www.cryptodispensers.com/market-analysis/february-2026)
- US margin debt was at all-time highs as crypto lost ~$2T. — [Protos](https://protos.com/us-margin-debt-reached-all-time-highs-as-crypto-lost-2-trillion)

**Meme sector level through 2026**
- Mid-Feb 2026 (CoinMarketCap data): the meme sector was **−34% in 30 days to ~$31B**, and Santiment flagged a "capitulation signal". — [CoinMarketCap community/Santiment](https://coinmarketcap.com/community/post/373826431/)
- March 2026: CoinGecko had total meme market cap at **$31B**.
  - **AI-meme tokens −46% YTD**; dog, 4chan and Elon-themed memes roughly **−28–30%**.
  - CryptoQuant: meme dominance within altcoins fell from **0.042 (mid-Feb) to 0.034 (Mar 2026)**.
  — [KuCoin flash](https://www.kucoin.com/news/flash/memecoin-market-cap-drops-from-150b-to-31b-amid-deleveraging-and-cooling-speculation); [Yellow](https://yellow.com/news/meme-coins-82-110b-crash-dogecoin-last-anchor)
- 15 Jun 2026: the sector was **$24.48B, −81.9% from the Nov 2024 peak of $135.06B**, and −31.3% YTD 2026. **DOGE is >50% of category market cap.** — [CryptoRank](https://cryptorank.io/news/feed/9df40-meme-coin-market-cap-crash-2026)
- Another headline reports meme dominance at a two-year low of **3.7%**. Undated; headline only. — [AskFuzz](https://askfuzz.ai/discover/news/cryptocurrencies/meme-coin-dominance-hits-two-year-low-at-3-7)
- CryptoSlate warned that a ~$50B meme "rally" was a trap, based on a wallet metric. Date and value not confirmed from the snippet. — [CryptoSlate](https://cryptoslate.com/memecoins-are-back-but-one-specific-wallet-metric-suggests-the-50-billion-rally-is-a-dangerous-trap/)
- A KuCoin headline claims a "Memecoin Market Surpasses $650 Billion". That is implausible against every other dataset; it is likely a mislabelled total-altcoin figure. **Do not use.** — [KuCoin](https://www.kucoin.com/news/flash/memecoin-market-surpasses-650-billion-amid-trade-tensions-easing-and-fed-rate-cut-expectations)

### Inferences
- **Political or celebrity meme launches** act as liquidity vacuums. Volume concentrates in one ticker, other memes bleed (−20–50%), and the venue mix changes (Meteora 10%→60%). After a scandal, the long tail loses trust. The visible signals are a drop in launch counts (−55% from 20 Jan to 18 Feb 2025) and a fall in launchpad volume.
- **Macro and leverage shocks** (tariffs, metals margin calls) spread from perps and CEX books to memes. The damage is worst in memes because their depth is shallowest. Recovery is **asymmetric**: majors bounce, while the meme long tail often does not.
- The 2025–2026 path fits memes acting as a **leveraged, late-cycle residual** of crypto risk appetite:
  - Peak in Dec 2024.
  - Partial revival around rate-cut hopes in Sept 2025.
  - Liquidity destruction in Oct 2025.
  - A grind lower with BTC to about −50% by Feb 2026.
  - Sector −82% by June 2026.
  - Sharp but short high-beta rebounds in Aug–Sept 2026.
- Concentration in DOGE (>50%) means index-level meme betas understate long-tail Solana meme risk.

### Gaps
- No specific MELANIA price or volume data was gathered. The only reference is CoinMarketCap Academy's TRUMP/MELANIA piece.
- No meme-specific drawdown figures were found for the Feb 2026 crash.
- No data on the meme sector or pump.fun for **Oct–Nov 2026** (the search budget ran out). The report writer should flag that the latest dated meme market-cap figure here is 15 Jun 2026.
- No quantified meme sensitivity to CPI or FOMC event days, or to US 10Y / real yields, was found.

## 4. Seasonality / time-of-day / day-of-week effects

### Takeaway
The evidence is thin. One secondhand on-chain analysis finds a clear **intraday cycle**: Solana meme volume rises from **10–11 UTC and peaks at 15–20 UTC**, which overlaps US hours. It also finds a **~10–15% weekend volume drop**. Day-of-week and hour heatmaps exist (Blockworks, Bitquery), but their results are paywalled or unpublished.

### Cited Findings
- An analysis of Solana memecoin trading (TechFlow/Odaily) found:
  - Daily volume starts rising **around 10–11 UTC and peaks 15:00–20:00 UTC**.
  - 3h and 24h moving averages of transaction count show **clear periodicity**.
  - Weekend volume is typically **10–15% lower** but "relatively stable".
  The date and methodology could not be confirmed. — [TechFlow](https://techflowpost.com/en-US/article/26585); [Odaily](https://www.odaily.news/en/post/5204643)
- The same analysis said Solana meme volume had spiked in March–April before trending down to **~$10B per week**. The year is likely 2025. — [TechFlow](https://techflowpost.com/en-US/article/26585)
- Blockworks Analytics publishes pump.fun trade activity broken down by hour and day of week. The data is behind a paywall. — [Blockworks Pump.fun Trade Activity](https://blockworks.co/analytics/pumpfun/pumpfun-tradeactvity)
- Bitquery documents a "Pump.fun Launch Pulse" query (new tokens per hour, hour×weekday heatmap) but publishes no results. — [Bitquery docs](https://docs.bitquery.io/docs/mcp/trading/examples/pumpfun-launch-pulse/)
- **Weekend liquidity risk for macro shocks:**
  - The 10 Oct 2025 cascade began on a **Friday afternoon (US)** and ran into the weekend. — [CryptoSlate](https://cryptoslate.com/?p=502753)
  - A separate analysis titled "A Weekend Liquidity Shock: Why Crypto Unraveled So Quickly" covers the early-Feb 2026 sell-off. Snippet only. — [source](https://san-1510.aid.brainsum.com/news/analysis/weekend-liquidity-shock-why-crypto-unraveled-so-quickly)
- **Holiday seasonality:** The Block (early 2025) reported graduated pump.fun tokens hit their **lowest average daily volumes since Christmas**. — [The Block](https://www.theblock.co/post/340073/trading-volume-across-graduated-pump-fun-tokens-hits-lowest-average-daily-volumes-since-christmas)

### Inferences
- For bots: activity, and likely the best liquidity and slippage for new tokens, concentrates in the **EU afternoon and US session (about 13–20 UTC)**. Asia hours and weekends are thinner. The weekend dip is modest (10–15%), so it is not a structural dead zone.
- Weekends combine thin books with macro news landing outside TradFi hours (Friday-evening tariff headlines). That raises **gap and liquidation-cascade risk** for meme positions held over the weekend.

### Gaps
- No published, dated hour×weekday heatmap of pump.fun or Solana meme volume or launches for 2025–2026. This would need to be built from Dune or Bitquery.
- No evidence on monthly or annual seasonality (e.g., "Uptober", December holidays, US tax season) specific to memecoins beyond the one Christmas data point.
- The time-of-day finding comes from a single analysis, so it lacks independent confirmation.
