# Shorting and Hedging Memecoin Exposure (as of Nov 2026)

Note: web search budget was ~6; 5 searches used (one rate-limited). Search tool returned summaries, not fetched pages; figures are as reported by those summaries. Items marked [UNVERIFIED] lack a source I could confirm.

## 1. Perps shorts on large memes: availability, funding, squeeze risk

### Takeaway
Perp shorts are the most practical way to short liquid memes, but the main documented danger is thin-book manipulation (JELLYJELLY on Hyperliquid, Mar 2025), and hourly funding can make a correct thesis expensive to hold. Venue-specific meme perp lists and current funding were not verified.

### Cited Findings
- Hyperliquid delisted the JELLYJELLY perp after a whale manipulation / short squeeze episode; the community HLP vault reportedly took ~$12M unrealized losses at first; Hyperliquid cited "suspicious market activity" — [The Block](https://www.theblock.co/news/defi/2025-03-26-hyperliquid-delists-jellyjelly-memecoin-amid-whale-manipulation-fiasco-348314); [FXStreet](https://www.fxstreet.com/cryptocurrencies/news/hyperliquid-escapes-liquidity-crisis-following-jellyjelly-short-squeeze-delists-token-202503262225)
- Hyperliquid funding settles hourly; shorts pay when funding is positive; new listings often attract aggressive shorting and elevated funding — [OneKey (low-quality/marketing)](https://onekey.so/blog/ecosystem/funding-rate-spike-hyperliquid/)
- Thin-book alts with small open interest (~$40M cited) can face gamma/squeeze risk — [Falsify Lab newsletter (secondary)](https://falsifylab.substack.com/p/hyperliquid-funding-extremes-2026-8df)
- Guides exist for shorting Solana memes via CEX perps vs on-chain — [Bybit wiki](https://www.bybit.com/wiki/article/how-to-short-solana-memecoins-cex-on-chain/); [DEXTools (promotional)](https://www.dextools.io/tutorials/how-to-short-meme-coins-in-2026)
- Kraken's page indicates MEME derivatives not available there — [Kraken](https://www.kraken.com/gr/features/derivatives/memecoin)

### Inferences
- Short squeezes on illiquid memes are a structural, not rare, risk: low liquidity + concentrated holders + leverage. Size small, use isolated margin, prefer high-OI names.
- Deeply negative funding (crowded shorts) is itself a squeeze signal and a cost; positive funding on longs pays the short (carry) but flips quickly.

### Gaps
- Current list of memes with perps on Hyperliquid/Binance/Bybit/Drift, their OI and max leverage: not retrieved.
- Typical realized funding for shorts on BONK/WIF/POPCAT etc. in 2026: not found.

## 2. Borrowing on lending markets (Kamino / Marginfi)

### Takeaway
Borrow-and-sell shorting on Kamino is possible only where a meme reserve exists, and supply is tiny, so capacity and borrow rates are limiting. Kamino docs use BONK as an example of a high borrow factor (2.0). Marginfi was not researched successfully.

### Cited Findings
- Kamino docs/litepaper use BONK as a riskier debt asset with borrow factor 2 vs 1 for USDC; Borrow Capacity = (Collateral Value x Max LTV) / Borrow Factor — [Kamino docs](https://kamino.com/docs/products/borrow/concepts); [Kamino litepaper](https://kamino.com/docs/kamino-lend-litepaper). These are illustrative, not confirmed live settings.
- DefiLlama showed Kamino Lend BONK pool total supplied ~$372,551 and WIF ~$69,959 (snapshot date unclear) — [DefiLlama BONK/WIF pool pages](https://defillama.com/yields/pool/c26a8e19-bc02-4fb3-b917-e7f8e66f839a), [second pool](https://defillama.com/yields/pool/8ed4139d-3fee-4d62-9974-0bd1dda1cce7)

### Inferences
- With only tens to hundreds of thousands in supply, borrowable size is small and utilization/borrow APY can spike; a lending short is a niche tool for small positions. Liquidation risk is on-chain and oracle-driven.

### Gaps
- Current max LTV, liquidation threshold, borrow APY for meme reserves on Kamino: not found.
- Marginfi meme listings/borrow availability: not found (not searched successfully).

## 3. Hedging with SOL perps

### Takeaway
No sourced evidence gathered. Conceptually, a SOL-perp short hedges only the market-beta component of Solana-meme holdings, not idiosyncratic decay.

### Cited Findings
- None retrieved.

### Inferences
- [UNVERIFIED reasoning] Solana memes tend to be high-beta to SOL; shorting SOL perps (liquid, cheap funding) reduces drawdown in broad sell-offs but leaves token-specific risk and basis between meme and SOL during rotations. Beta hedge ratio should be estimated from rolling regression.

### Gaps
- Empirical correlation/beta of Solana memes to SOL and hedge effectiveness: not researched.

## 4. Put options availability

### Takeaway
Liquid options on memecoins effectively do not exist on major venues; Deribit and Binance options focus on BTC/ETH (and a few majors). Perps are the practical substitute.

### Cited Findings
- No evidence Deribit or Binance list memecoin puts; Deribit ~79% of bitcoin options activity (CoinDesk-sourced) — search summary; see [Block Scholes research](https://www.blockscholes.com/research/the-renaissance-of-onchain-options) for on-chain options context
- Only memecoin options found: LADYS options on BIT exchange, undated, status unknown — [Crypto Briefing](https://cryptobriefing.com/ladys-options-on-bit-exchange-paves-new-retail-trading-highway-for-meme-coins/)

### Inferences
- Synthetic puts (long-dated perp short with stop, or inverse positions) are the realistic alternative; negative convexity of shorts (unbounded loss) cannot be capped without options.

### Gaps
- On-chain options protocols (e.g., Solana options) offering meme strikes in 2026: not verified.

## 5. Evidence that shorting post-hype memes has positive expectancy

### Takeaway
Base rates strongly favor decay after the peak, but this is not proof of tradable positive expectancy: median decline took ~370 days, and borrow/funding costs, squeezes, and availability of shortable venues erode returns. No backtest of a meme-short strategy was found.

### Cited Findings
- Coin Metrics (Solana memecoins launched since Dec 2023, ~150 tokens): median time to all-time high 17.2 days after first trade; 25% peak within ~1.6 days; median drawdown from peak ~95%, taking median ~370 days; 81% never regain first major peak; only 5 of 151 above day-one price after ~300 days — [Crypto Economy](https://crypto-economy.com/coin-metrics-most-memecoins-never-recover-after-their-first-major-peak/); [OneBullEx](https://www.onebullex.com/news/articles/coin-metrics-finds-81-of-solana-memecoins-never-recover-after-first-peak). Sample size cited as 150 vs 151 by different sources.
- Memecoin market cap fell ~72-73% from peak (Jan 2025 ~$9.2B per CoinGecko-cited figure; another report cites ~$150B peak to <$40B by Nov 2025; the two figures are inconsistent in scale, likely different datasets) — [Cointelegraph](https://cointelegraph.com/news/memecoins-christmas-2025-yearly-decline)
- Celebrity tokens down ~94% on average a month after launch — [CryptoSlate](https://cryptoslate.com/?p=435042)
- 81% of Pump.fun tokens reported crashed as of June 2025 (CoinGecko-based; page truncated) — search summary, unverified

### Inferences
- Edge likely lies in shorting liquid, listed tokens shortly after the blow-off (not tiny tokens that have no short venue), with tight risk caps; most of the 95% decline occurs in tokens that cannot be shorted at all (survivorship in tradability).
- Time-to-decay (~1 year median) means funding drag and squeeze risk matter more than the headline drawdown.

### Gaps
- No peer-reviewed or published backtest of perp-short returns net of funding on post-hype memes found.
- Realized short squeezes frequency on listed meme perps: not quantified.
