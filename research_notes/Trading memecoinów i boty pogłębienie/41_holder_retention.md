# Memecoin holder behavior: retention, churn, diamond hands, holder-count trajectories, and metric computation

Research caveat: only 3 web searches returned results (the 3rd was rate-limited). All WebFetch attempts failed (hosts not in the session network allowlist: beincrypto.com, dextools.io, arxiv.org). Every figure below comes from search-result summaries only, not from the primary pages. Treat ALL figures as UNVERIFIED until checked against the original sources.

## 1. What share of holders buy and never sell ("diamond hands")?

### Takeaway
One Dune-based figure circulating in media says over 62% of Solana memecoin holders have never sold, but reports say many are "forced" holders stuck in deep losses, so it measures inertia, not conviction. No primary methodology was verified. (UNVERIFIED)

### Cited Findings
- Dune data cited by BeInCrypto and MEXC reposts: more than 62% of Solana memecoin holders have bought and never sold; coverage says many were pushed into this by sharp price drops, and recovery of losses is hard. Single-analyst snapshot; dashboard author and date not confirmed. (UNVERIFIED, secondary) — [BeInCrypto](https://beincrypto.com/solana-memecoins-holders-struggle-to-recover); [MEXC repost](https://www.mexc.com/news/252197)
- Dune report on Pump.fun: nearly all traders have not realized over $10,000 profit (CoinMarketCap Academy headline: 99.6%); realized profit excludes open positions. An analyst (Alon) noted some of the most profitable wallets are deep-conviction early holders. (UNVERIFIED, from snippet) — [CoinMarketCap Academy](https://coinmarketcap.com/academy/nl/article/996percent-of-pumpfun-traders-have-not-realized-over-dollar10000-in-profits-data-shows); [Cointelegraph](https://cointelegraph.com/news/pump-fun-crypto-traders-majority-do-not-realize-profits-dune-data)
- Another report headline: only 0.76% of Pump.fun wallets made $1,000+ (crypto.news citing research; details not read). (UNVERIFIED) — [crypto.news](https://crypto.news/only-0-76-of-pump-fun-wallets-made-1000-or-more-cn-research/)

### Inferences
- "Never sold" share is inflated by underwater bagholders and dust/abandoned wallets; it should not be read as diamond-hand conviction. A cleaner measure conditions on position size and on wallets that were in profit at some point.

### Gaps
- Original Dune query/dashboard for the 62% figure, its date, and its definition of "holder" (dust filter, bots, LP/contract exclusion) not found.
- No figure for the share of buy-once wallets by launch-cohort found.

## 2. Typical holding periods and retention/churn curves

### Takeaway
No verified median holding-time figure was found. Indirect evidence shows extremely fast token death: most Pump.fun tokens stop trading on day one, and ~5% survive past 90 days. (UNVERIFIED)

### Cited Findings
- CoinGecko analysis of 18.67M Pump.fun tokens (Jan 14, 2024 to Jun 18, 2026): 68.67% recorded their final bonding-curve trade on launch day (never-traded tokens excluded); about 5% survive past 90 days. Caveat: only bonding-curve trades are tracked, so migrated tokens (Raydium, Meteora, PumpSwap) may be undercounted. — [crypto.news](https://crypto.news/pump-funs-token-factory-has-a-69-launch-day-death-rate-coingecko/); [CryptoBriefing](https://cryptobriefing.com/pump-fun-token-survival-rate-study/); [KuCoin news](https://www.kucoin.com/news/flash/coingecko-analysis-68-67-of-pump-fun-tokens-stop-trading-on-launch-day)
- Related headlines: nearly 70% of Pump.fun tokens disappear on launch day, ~80% gone in 2 days (KuCoin news); Blockonomi claims >90% of memecoins launched late 2025/early 2026 lost liquidity and interest (opinion-leaning, methodology unchecked). — [KuCoin](https://www.kucoin.com/news/flash/nearly-70-of-pump-fun-tokens-disappear-on-launch-day-80-gone-in-2-days); [Blockonomi](https://blockonomi.com/the-memecoin-retention-crisis-why-over-90-of-new-tokens-collapse-after-launch/)
- Adjacent (not a memecoin): BitMEX found ~60% of early PUMP presale buyers already sold or moved tokens. — [Cryptonews AU](https://cryptonews.com.au/news/pump-fun-presale-dump-nearly-60-of-pump-buyers-have-already-offloaded-tokens-bitmex-finds-129977)
- An arXiv paper "The Memecoin Phenomenon" (2512.11850) exists and may contain holder-level data; NOT read (fetch blocked). — [arXiv](https://arxiv.org/html/2512.11850v2)

### Inferences
- Token "lifetime" (last trade) is a proxy for aggregate holder abandonment, but is not a per-holder holding period; most holder retention curves will be dominated by a very steep day-0 cliff.

### Gaps
- No sourced median/percentile holding times (minutes/hours) for memecoin buyers; no published retention curve (D1/D7/D30 cohorts). Primary papers/dashboards unread.

## 3. Whale/large-holder retention and winners vs losers holder-count trajectories

### Takeaway
A DeFi Report analysis (via HTX) tracks retention in token units from all-time-high, a price-neutral method; SPX6900 led. Holder-count growth can mask churn. (UNVERIFIED)

### Cited Findings
- Analysis relayed by HTX: wallets tracked by token units held at ATH to strip price effects; SPX6900 led retention for $1,000 and $100,000 holders; 80% of its whales (once >$100k) still hold over 50% of peak token amount. — [HTX](https://www.htx.com/news/meme-watchlist-whos-cultivating-real-fans-whos-inflating-dat-9oqRyCo1/)
- DEXTools tutorials define holder churn as how quickly existing holders sell and are replaced by new ones, arguing a rising holder count can be bearish if churn is high; also a "transfer velocity vs holder retention" piece. (Definitions only; formulas not read.) — [DEXTools churn](https://www.dextools.io/tutorials/holder-churn-rate-why-growing-holder-count-can-still-be-bear); [DEXTools velocity](https://www.dextools.io/tutorials/token-transfer-velocity-vs-holder-retention-what-shows-real)

### Inferences
- Winners likely show net-positive holder growth with low churn among large wallets; losers show holder count plateau then slow decay because holders do not sell (count stays high while volume dies). This is an inference, not sourced; holder count alone is a lagging, misleading indicator.

### Gaps
- No quantitative winners-vs-losers holder-count curves found (e.g., BONK, WIF, POPCAT trajectories).

## 4. How the metrics are computed (Nansen, GMGN, Dune)

### Takeaway
No platform documentation was retrieved (search rate-limited, fetches blocked). Below is general, UNVERIFIED knowledge, not sourced.

### Cited Findings
- Dune dashboards are community-written SQL, so definitions vary per dashboard; the HTX/DeFi Report approach (units held vs ATH peak) is the one documented method found. — [HTX](https://www.htx.com/news/meme-watchlist-whos-cultivating-real-fans-whos-inflating-dat-9oqRyCo1/)
- No Nansen or GMGN methodology page was found.

### Inferences (general knowledge, unsourced, UNVERIFIED)
- Typical construction: reconstruct per-wallet balances from SPL transfer/DEX-swap events; exclude LP pools, program accounts, exchanges/burn addresses and dust; holding time = first buy to last sell (or to now if open), summarized as median; "diamond hand" = wallets with no sells in N days or wallets retaining >X% of peak balance. Terminal-style tools (GMGN-type) likely show per-holder "bought/sold/holding time" and tag wallets (smart money, sniper, bundler/insider); Nansen likely uses entity labels (Smart Money) for segmentation. Exact definitions unconfirmed.
- Pitfalls: sybil/bundled wallets inflate holder count; wallet-hopping looks like selling; token-unit vs USD-based retention differ materially.

### Gaps
- Official Nansen/GMGN/Dune metric definitions; any open-source SQL for holder retention cohorts. Recommend fetching docs.nansen.ai, GMGN docs, and Dune dashboards once network access allows.
