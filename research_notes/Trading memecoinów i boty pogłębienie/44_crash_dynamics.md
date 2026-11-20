# Crash dynamics affecting memecoins (as of Nov 2026)

Research limits: ~3 searches succeeded (one more was rate-limited, one fetch blocked: coingecko.com not in allowed network domains). Memecoin-specific and on-chain liquidity evidence is thin. Items marked [UNVERIFIED] come from model memory or general knowledge, not a fetched source.

## 1. The 10-11 Oct 2025 liquidation cascade: size, memecoin drawdowns, DEX liquidity effects

### Takeaway
The event was the largest liquidation day on record (~$19B forced closures, ~$350-400B market cap lost), driven by leverage plus ADL, with Hyperliquid the largest venue and altcoins hit hardest. I found no sourced memecoin-specific drawdown percentages or DEX pool data.

### Cited Findings
- Coinglass-based reporting: >$19B liquidated across ~1.6M traders in 24h; Coinglass called its figure conservative. — [TradingView/NewsBTC](https://www.tradingview.com/news/newsbtc:a4b7d8789094b:0-crypto-crash-19-5-billion-wiped-out-in-record-breaking-liquidation-event)
- Figures differ by source: $19.38B total / $16.7B longs in one report; $19.15B total, $16.69B longs, $2.46B shorts in another. — [KuCoin flash](https://www.kucoin.com/news/flash/crypto-market-sees-19-15b-liquidation-event-on-october-10-2025)
- Hyperliquid largest venue (>$10B reported processed); Binance ~ $2.4B. Altcoins bore the brunt; BTC drawdown comparatively contained (briefly <$110k). — [Yahoo Finance](https://finance.yahoo.com/news/record-19bn-crypto-crash-exposes-194741410.html) (search-summary level; venue split varies by source)
- FTI Consulting: high leverage plus exchange auto-deleveraging (ADL) turned selloff into margin-driven spiral; funding rates rose from ~10% to ~30% annualized by 6 Oct. — [FTI Consulting](https://www.fticonsulting.com/insights/articles/crypto-crash-october-2025-leverage-met-liquidity)
- Trigger: threat of 100% tariffs on China; market cap loss estimates ~$350-400B. — [Cointelegraph via TradingView](https://th.tradingview.com/news/cointelegraph:83d396b6a094b:0-19b-crypto-market-crash-was-it-leverage-china-tariffs-or-both)
- Liquidations measure forced closures, not net investor losses. — same sources as above.

### Inferences
- Because the cascade was perp-driven (Hyperliquid/CEX), memecoin spot/DEX prices likely followed via arbitrage and cross-margin selling rather than on-chain leverage; bots should watch perp funding/OI as a leading indicator.
- Altcoin/memecoin beta in such events is plausibly several times BTC's drawdown [UNVERIFIED: no sourced percentages found; commonly cited anecdotes of 50-80% intraday wicks on thin alts and some memecoins not confirmed here].

### Gaps
- Memecoin drawdown percentages (BONK, WIF, PEPE, etc.), DEX volume/TVL changes in Solana pools: not found.
- Binance-specific oracle/depeg issues (USDe, wBETH) and market-maker depth withdrawal: recalled but [UNVERIFIED], not sourced.

## 2. Other 2025-2026 flash crashes

### Takeaway
Post-Oct-2025 there were repeated, smaller liquidation waves in early 2026 (Jan-Mar), with memecoin perps liquidated mainly on Hyperliquid. None matched Oct 10.

### Cited Findings
- 30 Jan 2026: long squeeze erased ~$1.71B across 275,371 traders; 31 Jan: ~$2.56B liquidated, largest single day since the "1011 Crash". — [KuCoin](https://www.kucoin.com/news/articles/massive-crypto-liquidation-on-jan-31-2-56-billion-wiped-out-setting-post-1011-crash-record), [KuCoin flash](https://www.kucoin.com/news/flash/crypto-market-loses-108b-in-6-minutes-as-1-7b-in-positions-liquidated) (market cap -$108B in 6 minutes reported)
- 5 Feb 2026: >$1.45B liquidated in 24h, $1.24B longs. — [KuCoin](https://www.kucoin.com/news/articles/crypto-market-volatility-intensifies-analyzing-the-2-114-billion-liquidations-in-24-hours) (title cites $2.114B for a 24h window; figures inconsistent, treat as approximate)
- Early Jan 2026 memecoin rally (PEPE ~+50% weekly) then Fartcoin -28% from weekly high, $51M liquidated in 24h, mostly Hyperliquid. — [Decrypt](https://decrypt.co/363772/fartcoin-leads-altcoin-slump-with-double-digit-drop), [Altfins](https://altfins.com/crypto-news/crypto-news-summary/170786)
- Early March 2026 weekend flash crash took BTC to late-2024 levels. — [Stocktwits](https://stocktwits.com/news-articles/markets/cryptocurrency/bitcoin-weekend-flash-crash-sends-price-to-2024-levels/cZbgB1eR4jN)

### Inferences
- Weekend/low-liquidity-hours timing recurs (Oct 10 Friday evening US, Jan 31 weekend, March weekend): bots should tighten risk on weekends.

### Gaps
- Nothing found after March 2026 (Apr-Nov 2026); other 2025 events (e.g., Feb 2025 ~$2B+ liquidation, Bybit hack) are [UNVERIFIED] recollection, not searched.

## 3. On-chain memecoin liquidity behavior in crashes (LP withdrawals, RPC congestion, failed tx)

### Takeaway
I could not obtain sourced data. Only a general, unverified picture is available.

### Cited Findings
- None. The search for Solana/RPC/LP behavior during Oct 10 was rate-limited and returned nothing.

### Inferences
- [UNVERIFIED, general market-structure reasoning] Concentrated-liquidity LPs (Meteora DLMM, Orca, Raydium CLMM) go single-sided into the falling token as price drops through their range; sniping/arbitrage bots and demand spikes raise tx volume, priority fees, and failed-tx rates (slippage failures, expired blockhash, dropped txs under congestion). Memecoin rug-style LP removal accelerates in drawdowns.

### Gaps
- No post-mortems on Solana TPS, failed-tx rate, RPC provider degradation, Jito tip spikes, or Pump.fun/PumpSwap/Raydium pool TVL changes during 10-11 Oct 2025. Recommended next searches: Helius/Triton/Jito blog, Dune dashboards, Solana status page.

## 4. Lessons for bot circuit breakers

### Takeaway
Evidence-based lessons are limited; those below are mostly engineering inferences from the sourced event structure (leverage cascade, ADL, weekend timing) and should be treated as design hypotheses.

### Cited Findings
- Cascade amplified by leverage and ADL, with funding rates elevated days earlier (10% to ~30% annualized by 6 Oct) — [FTI Consulting](https://www.fticonsulting.com/insights/articles/crypto-crash-october-2025-leverage-met-liquidity)

### Inferences
- Pre-crash regime trigger: reduce size / pause entries when perp funding, OI growth, or market-wide liquidations spike (e.g., >$1B/hour Coinglass).
- Market-wide breaker: BTC/SOL drop over short window (e.g., 3-5% in 5 min) halts new buys and widens slippage limits only for exits.
- Execution breakers: pause on failed-tx rate or RPC latency thresholds; multi-RPC failover; raise priority fees only for exits; cap retries to avoid failed-tx fee bleed.
- Pool-level breakers: exit/avoid when pool liquidity falls >X% vs rolling baseline or price impact for position size exceeds limit; never size on quoted liquidity during a crash.
- Manual/automatic cooldown after the event (liquidity recovers slowly; Jan 30-31 and Feb 5 show clustered repeats), so use multi-day cooldown/halved sizing after a >$5B liquidation day.
- Thresholds above are illustrative [UNVERIFIED], not from research.

### Gaps
- No sourced bot post-mortems or empirical backtests of circuit-breaker thresholds.
