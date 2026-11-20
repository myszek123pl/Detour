# Backtesting methodology and historical data sources for memecoin trading strategies

> Research conditions (read first): This was researched on 2026-11-20. Direct page fetching (WebFetch) was blocked by the session's network allowlist (bitquery.io and madeonsol.com would not resolve), and the shared web-search budget ran out after 12 searches. So every cited finding below comes from search-result snippets of the linked pages, not from full-page reads. Pricing figures are thin and should be re-checked on the providers' pricing pages. Items I know from background knowledge but could not verify are listed only under **Gaps**, marked "unverified".

## 1. Data sources: coverage, granularity, cost

### Takeaway
For memecoin trade-level (tick) history, the realistic choices fall into three groups:
- **SQL warehouses:** Dune `dex_solana.trades`, Allium datashares, and the BigQuery public Solana dataset. These are cheap to start with and cover the full universe, but are batch-refreshed (about 3h) and have uneven launchpad decoding.
- **Specialist APIs:** Bitquery (pump.fun trades since June 2024, with cloud/Kafka export), Birdeye (Solana-only historical trades with seek-by-time), Codex (getTokenEvents/getTokenBars), Solana Tracker (pump.fun bonding-curve and graduated-pool trades), and Moralis (pump.fun swaps).
- **Self-hosted raw ledger:** decoding raw blocks yourself.

GeckoTerminal is unsuitable for tick backtests: its trades endpoint returns only the last 300 trades in the past 24h.

### Cited Findings
**Dune**
- `dex_solana.trades` "records all raw trade events across various protocols on Solana". The docs include a sample daily trade-count and USD-volume query. — [Dune docs: Solana DEX trades](https://docs.dune.com/data-catalog/curated/dex-trades/solana/overview)
- Dune's Solana trading curated tables (DEX Trades plus a Jupiter aggregator table) list a refresh cadence of about 3 hours. — [Dune docs: Solana trading](https://docs.dune.com/data-catalog/curated/solana/trading)
- Spellbook is Dune's open-source (dbt + GitHub) repository for building curated tables such as DEX trades and labels. Community contributors can add protocol decoders. — [Dune Spellbook](https://dune.com/product/spellbook)
- The search did not confirm a dedicated pump.fun trades spell on Dune. The suggested approach is to filter `dex_solana.trades` by project or program address. — [Dune docs](https://docs.dune.com/data-catalog/curated/dex-trades/solana/solana-dex-trades.md)

**Allium**
- Allium's Solana schema includes DEX trades and aggregator (Jupiter) trades across 10+ major DEXs. Its normalized fields include token_in, token_out, amount_usd, trader, protocol, dex and timestamp. — [Allium Solana docs](https://docs.allium.so/historical-data/supported-blockchains/solana); [Allium Solana page](https://www.allium.so/ecosystems/solana)
- Datashares deliver to Snowflake, BigQuery, Databricks and cloud storage. Snowflake (GCP us-central1) is listed with 3-hour freshness. A third-party guide claims a 2–10 minute refresh, so the refresh claims conflict. Allium also offers a Solana DEX-trades stream ("Beam") for filtered live feeds. — [Allium Datashares](https://allium.so/product/allium-datashares); [third-party guide (eco.com)](https://eco.com/support/en/articles/14800363-allium-blockchain-data-warehouse)
- Allium has a page aimed at hedge funds that markets on-chain signals for trading. — [Allium hedge funds](https://www.allium.so/client/hedge-fund)
- Allium's chain-count claims are inconsistent across pages (150+ vs 85+). Explicit coverage of launchpads such as pump.fun bonding curves was not confirmed in the search results. — [Allium Solana page](https://www.allium.so/ecosystems/solana)

**Google BigQuery public dataset**
- The dataset `bigquery-public-data.crypto_solana_mainnet_us` (tables such as `transactions` and `Accounts`) was launched by Solana and Google. — [Solana news](https://solana.com/news/solana-data-live-on-google-cloud-bigquery)
- Freshness is a known issue. A user reported the `transactions` table stopped updating on 2025-03-31 even though "Last modified" was later. Another user later found a max `block_timestamp` of 2025-11-19, i.e. delayed by days but still updating. — [Google Developer forum thread](https://discuss.google.dev/t/public-solana-bigquery-dataset-crypto-solana-mainnet-us-stopped-updating-on-march-31-2025/185629)
- Token Terminal worked with Google on upgrades that make instruction-level Solana queries cheaper. — [Token Terminal x Google](https://tokenterminal.beehiiv.com/p/token-terminal-x-google)
- Cost: 1 TB/month of free query processing, then about $6.25/TB scanned. This comes from a third-party guide. — [madeonsol SQL guide](https://madeonsol.com/blog/how-to-query-solana-data-with-sql)

**Bitquery**
- Bitquery's Pump.fun API covers bonding-curve trades, token creations, migrations, pools and OHLCV. Its marketing page claims pump.fun trades back to June 2024, with SOL and USD prices on every trade. Historical access is listed as an Enterprise feature. — [Bitquery Pump.fun docs](https://docs.bitquery.io/docs/blockchain/Solana/Pumpfun/Pump-Fun-API/); [Bitquery pump.fun product](https://bitquery.io/products/pumpfun-api)
- Bitquery offers a cloud/data-export product for pump.fun data and Solana delivery via GraphQL, Kafka, gRPC and cloud export. — [Bitquery cloud pump.fun](https://docs.bitquery.io/docs/cloud/pumpfun/); [Bitquery Solana API](https://bitquery.io/blockchains/solana-blockchain-api)
- In a Bitquery-authored comparison, Birdeye's pricing is listed as $49 / $99 / $299 per month plus Enterprise, compute-unit tiers and x402. The same page says Birdeye offers no warehouse delivery. This is a competitor source, so verify it. — [Bitquery vs Birdeye](https://bitquery.io/alternatives/bitquery-vs-birdeye); [Bitquery: Best Solana DEX trade data APIs 2026](https://bitquery.io/blog/best-solana-dex-trade-data-api)

**Birdeye**
- Historical price endpoints are Solana-only. There is a trades "seek by time" endpoint (`/defi/txs/token/seek_by_time`) and an all-time trades endpoint (`/defi/v3/all-time/trades/single`). Data access is gated by package. — [Birdeye: Data accessibility by packages](https://docs.birdeye.so/docs/data-accessibility-by-packages); [Birdeye: Trade seek by time](https://docs.birdeye.so/docs/trade-token-seek-by-time); [Birdeye historical price](https://docs.birdeye.so/docs/price-history)
- A third-party skill page describes the free tier as about 30K compute units/month at 1 req/s. — [skillselion birdeye-api](https://skillselion.com/skills/agiprolabs/claude-trading-skills/birdeye-api)
- Birdeye supports x402 pay-per-request access. — [Birdeye x402 docs](https://docs.birdeye.so/reference/x402.md)

**Codex**
- Codex markets 80+ networks, 70M+ tokens and 27B+ historical events. `getTokenBars` returns OHLCV, `getTokenEvents` returns individual swap events (trade-level), and `onBarsUpdated` live streaming is limited to the Growth and Enterprise plans. — [Codex pricing](https://codex.io/pricing); [Codex onBarsUpdated](https://docs.codex.io/reference/onbarsupdated); [Codex API reference](https://docs.codex.io/api-reference)
- WebSocket subscriptions require a paid plan. Codex accepts card payments via Stripe and crypto in 3-month increments. Codex also publishes a migration guide for Birdeye users. — [Codex SDK README](https://cdn.jsdelivr.net/npm/@codex-data/sdk@2.3.24/README.md); [Codex FAQ](https://docs.codex.io/extra/faq); [Codex: migrating from Birdeye](https://docs.codex.io/migrations/birdeye)

**Solana Tracker**
- Its Pump.fun API provides live and historical trades on pump.fun bonding curves and graduated pools, plus first-buyer and top-trader analytics. This is included in the general Data API and Datastream plans. — [Solana Tracker Pump.fun API](https://www.solanatracker.io/pumpfun-api); [Solana Tracker Data API docs](https://docs.solanatracker.io/public-data-api/docs)
- The free tier is 2,500 requests/month at 3 req/s. The WebSocket Datastream starts on the Premium plan. Plans are billed monthly in EUR, with about 30% off for yearly billing. — [Solana Tracker Data API](https://docs.solanatracker.io/public-data-api)

**Moralis**
- Moralis publishes a tutorial for fetching pump.fun token swaps and prices through its Data API. — [Moralis tutorial](https://docs.moralis.com/get-started/tutorials/data-api/tokens-and-markets/get-pump-fun-tokens-swaps-and-prices.md)

**GeckoTerminal / CoinGecko**
- The public API is limited to 30 calls/min. Keyless requests share an IP-based pool. — [GeckoTerminal FAQ](https://apiguide.geckoterminal.com/faq); [CoinGecko keyless API](https://docs.coingecko.com/docs/keyless-public-api)
- The pool trades endpoint returns only the "last 300 trades in past 24 hours". — [CoinGecko on-chain endpoint overview](https://docs.coingecko.com/demo/reference/endpoint-overview)
- A paid CoinGecko plan lifts the limit to about 500 calls/min, and OHLCV history beyond about 6 months is reportedly limited. Both claims come from a third-party skill page and are unconfirmed in official docs. — [skills.cat geckoterminal-api](https://skills.cat/skills/enuno/claude-command-and-control/geckoterminal-api)

### Inferences
- **Universe-level research** (which tokens graduate, the distribution of outcomes): a SQL warehouse (Dune or Allium) is the cheapest way to get every token, including dead ones. The roughly 3h refresh does not matter for backtests.
- **Execution-realistic simulation of sniping or bonding-curve entries:** you need per-transaction ordering within a slot (slot, transaction index, signer, fee/tip, success flag). Aggregated DEX-trade tables often drop failed transactions and intra-block ordering. Raw transaction tables (BigQuery/Dune raw `solana.transactions`) or self-decoded blocks are needed.
- GeckoTerminal and DexScreener-style APIs give survivor-biased snapshots. They are only suitable for candle-level sanity checks of tokens that already exist, not for building a universe.
- A sensible stack: (a) Dune/Allium for the universe and labels, (b) Bitquery, Codex or Solana Tracker for trade-level pulls on candidate tokens, and (c) your own Geyser/gRPC recorder going forward to capture what historical vendors don't (failed txs, mempool-equivalent bundle timing, your own landing latency).

### Gaps
- Exact current (Nov 2026) prices for Birdeye, Codex, Bitquery, Solana Tracker, Moralis and Allium were not retrieved, because pricing pages could not be fetched.
- **Flipside:** the search budget ran out before I could verify its 2025–26 status. Unverified background: Flipside historically offered free SQL on Snowflake-backed Solana tables (e.g. `solana.defi.ez_dex_swaps`) and changed its product and free-access model around 2024–25. Check its current status directly.
- **Running your own archival node:** could not verify. Unverified background:
  - A full Solana archival RPC is very expensive (multi-hundred-TB ledger).
  - The common alternative is Triton's "Old Faithful" project, which stores the full ledger as CAR files (epochs) and serves historical RPC from them.
  - Live capture via Yellowstone gRPC (Geyser) plugins is the standard way to record your own tick data going forward.
  - Verify all of this before relying on it.
- Whether Dune or Allium decode pump.fun bonding-curve (pre-graduation) trades into their curated trade tables, as opposed to only graduated AMM pools, was not confirmed.
- How far back Birdeye's and Codex's trade-level history goes for dead pump.fun tokens was not found.

## 2. Backtesting pitfalls specific to memecoins

### Takeaway
The dominant risks are:
- **Survivorship bias:** only about 1% of pump.fun tokens graduate, so universes built from "tokens that exist on DEX screeners today" are heavily skewed.
- **Censoring/sampling artefacts:** API and scraper samples have blind spots.
- **Execution unrealism:** fill price, latency, landing rate, priority-fee and Jito-tip competition, and slippage-triggered failures.

Vendor-published landing-rate numbers are largely anecdotal, so every execution assumption has to be calibrated from your own live submission logs.

### Cited Findings
- **Scale of failure:** a cited preprint ("Meme Coin Factories") reports only 1.02% of coins in its sample graduated. A survivor-only sample therefore looks radically different from the true launch universe. — [Marino et al. / arXiv 2602.13480](https://www.arxiv.org/pdf/2602.13480)
- An independent audit of a study covering 832,941 pump.fun launches argued that rows that timed out should be treated as censored ("not seen completing"), not as failures. It also argued that "scrapers, APIs and dashboards sample [the ledger], and every sample has blind spots", and that "a great backtest is a hypothesis, not a result". — [Brave New Coin: auditing 832,941 pump.fun launches](https://bravenewcoin.com/insights/what-auditing-832941-pump-fun-launches-taught-me-about-memecoin-success)
- "A Midsummer Meme's Dream" releases a dataset of 34,988 meme coins across Ethereum, BSC, Solana and Base. It documents $3.27M in realized losses from pump-and-dumps and $6.04M from rug pulls, which are manipulation patterns that look like alpha in naive backtests. — [arXiv 2507.01963](https://arxiv.org/html/2507.01963v2)
- MemeChain (2026) is a multimodal cross-chain dataset for meme-coin forensics and risk analysis, including survival analysis. — [arXiv 2601.22185](https://arxiv.org/html/2601.22185v1)
- MemeTrans covers 41k+ Solana launches and 200M+ transactions with bundled-account traces that reveal hidden multi-account coordination. This matters because insider "bundled" buys distort apparent early-buyer edge. — [arXiv 2602.14860](https://www.arxiv.org/pdf/2602.14860)
- **Execution:**
  - Landing rate is the share of submitted bundles that execute on-chain. It depends on auction position, timing and execution validity, and failures should be tagged by category rather than averaged.
  - Jito tips and Solana priority fees are different mechanisms.
  - One RPC vendor reports that priority fees alone correlate only weakly with faster inclusion, and that tips alone don't guarantee fast landing.
  - Source: [RPC Fast: Jito bundle landing rate guide](https://rpcfast.com/blog/how-to-improve-your-jito-bundle-landing-rate-on-solana); [RPC Fast: same-block TX landing](https://rpcfast.com/blog/pillars-of-choosing-a-solana-rpc-provider-for-trading-bots)
- Slippage controls and fallback logic are core sniper features because price moves while a transaction is in flight. One developer anecdote reports 73% success on 47 snipe attempts, with most failures attributed to slippage above 5%. This is a single unaudited anecdote. — [RPC Fast: pump.fun sniping guide](https://rpcfast.com/blog/how-to-launches-snipe-pump); [Dev.to: sniped a token in 400ms](https://dev.to/apollo_ag/i-sniped-a-solana-token-in-400ms-heres-the-full-tech-stack-4h74)
- Sandwich attacks are a common failure mode for bot buys with loose slippage. — [Dev.to: why most crypto bots get sandwiched](https://dev.to/apollo_ag/why-most-crypto-bots-get-sandwiched-and-how-to-prevent-it-192g)

### Inferences
These follow from the cited findings combined with standard quant practice:
- **Survivorship:** build the universe from token-creation events (pump.fun create instructions or launchpad mint events) at time t, not from "tokens with a DEX pair today". Keep tokens that died on the curve. Value rugged positions at the realizable exit (often about 0), not the last quoted price.
- **Look-ahead:**
  - Features such as "holder count", "graduated", "market cap ATH", "top-10 holders %", vendor risk scores and social metadata are often snapshotted *now*. Use only values reconstructable from on-chain state at or before the decision slot.
  - Vendor USD prices on a trade may be computed with later SOL/USD data.
  - Labels such as "dev wallet" and "insider" are often assigned retroactively.
- **Fills:**
  - Model the fill as your transaction landing N slots after the signal, behind the observed competing transactions in that slot.
  - Recompute the bonding-curve or AMM output from reserves at your simulated position, rather than using the historical trade price.
  - Apply slippage tolerance, so the transaction reverts if exceeded.
  - Charge fees even on failure: base fee, priority fee and tip; protocol fee such as pump.fun's trade fee; AMM LP fee.
- **Failed transactions:** many vendor trade tables exclude failed transactions, which understates competition and hides your realistic failure rate. Raw transaction tables include the success flag.
- **Liquidity changes:**
  - Liquidity is discontinuous at graduation/migration from the bonding curve to the AMM pool.
  - Liquidity can vanish on LP pull or rug.
  - Exits must be simulated against reserves at exit time, including your own price impact. Large simulated sells into thin pools are the most common source of backtest-only profit.
- **MEV:** assume adversarial ordering (sandwiching) when slippage tolerance is wide. Simulate the worst-case fill at your slippage bound with some probability calibrated from live data.

### Gaps
- I found no rigorous, peer-reviewed methodology paper on execution-realistic backtesting of Solana sniping or priority-fee auctions. The available material is vendor blogs and anecdotes.
- No independently measured, public landing-rate or latency distributions for Jito vs priority-fee-only submission were found.
- Exact pump.fun fee parameters as of Nov 2026 were not verified in this pass.

## 3. Simulation approaches

### Takeaway
The best practice is a ladder:
1. Event-driven replay of on-chain trades with deterministic bonding-curve/AMM math, with you inserted into the historical order flow.
2. Paper trading on mainnet live data: shadow mode, logging the signal and the would-be fill.
3. Small-size live forward testing to calibrate latency, landing-rate and slippage distributions.
4. Walk-forward or rolling out-of-sample validation across launch-regime changes.

Treat a backtest as a hypothesis until live data confirms the execution assumptions.

### Cited Findings
- Pump.fun is described as a large-scale natural experiment in early termination of speculative assets. Marino et al. study predicting token success, which frames entry signals as early-classification problems needing censoring-aware evaluation. — [arXiv 2602.13480](https://www.arxiv.org/pdf/2602.13480)
- "A great backtest is a hypothesis, not a result." Timeout rows should be treated as censored. — [Brave New Coin audit](https://bravenewcoin.com/insights/what-auditing-832941-pump-fun-launches-taught-me-about-memecoin-success)
- A credible approach measures landing rate per failure category and checks slippage and priority-fee sensitivity against your own submission logs. — [RPC Fast landing-rate guide](https://rpcfast.com/blog/how-to-improve-your-jito-bundle-landing-rate-on-solana)
- Data for replay: Bitquery exposes bonding-curve trades, creations and migrations, and Solana Tracker exposes curve and graduated-pool trades. Both are needed to replay a token's full lifecycle. — [Bitquery Pump.fun docs](https://docs.bitquery.io/docs/blockchain/Solana/Pumpfun/Pump-Fun-API/); [Solana Tracker Pump.fun API](https://www.solanatracker.io/pumpfun-api)

### Inferences
- **Bonding-curve replay:**
  - Reconstruct virtual and real reserves after each historical trade. Pump.fun-style curves are constant-product on virtual reserves, so price is a deterministic function of reserves.
  - Insert your order at a chosen slot and position, and compute the output from the curve.
  - Optionally propagate the impact of your trade to later traders. The conservative choice is not to assume they would still trade identically.
  - Requires trade-level data with slot and transaction index ordering.
- **Paper trading on mainnet:**
  - Run the full live pipeline (Geyser/gRPC feed, then signal, then transaction build) but don't send, or simulate via the RPC `simulateTransaction` call against current state.
  - Record the slot at which you *would* have landed.
  - This captures data latency honestly but not landing competition.
- **Forward testing with real money at minimum size:** this is the only way to get real landing, failure and sandwich rates. Feed those empirical distributions back into the replay simulator.
- **Walk-forward:**
  - Split by time (e.g. monthly). Optimize parameters on window k and evaluate on k+1.
  - Report the distribution across windows. Memecoin regimes shift quickly with launchpad rule changes, fee changes, competing launchpads and market sentiment.
  - Avoid random K-fold, because tokens launched in the same hour are correlated.
- **Statistics:** returns are extremely fat-tailed, with a few 100x tokens dominating. Report median and trimmed results, bootstrap confidence intervals and the share of PnL from the top-N trades. A strategy whose profit depends on one or two outliers is not validated.

### Gaps
- I found no published, open-source pump.fun bonding-curve replay simulator in this pass, because the search budget was exhausted.
- No academic paper on walk-forward validation specifically for memecoin strategies was found.

## 4. Open-source backtesting frameworks adaptable to on-chain data

### Takeaway
No mainstream framework natively handles Solana launchpad microstructure. The practical route is a generic event-driven engine with a custom DEX/bonding-curve fill model. On-chain-native DEX backtesters exist (Trading Strategy, Jesse with DEX support, RoboVault's Arkiver for EVM data), but they target EVM AMMs and candles, not Solana tick-level sniping.

### Cited Findings
- **Trading Strategy framework:** a Python framework for algorithmic trading on DEXes, using backtesting data and real-time feeds from Trading Strategy Protocol. Older releases are AGPL-3.0. — [PyPI trading-strategy](https://pypi.org/project/trading-strategy/0.14)
- **Jesse:** an open-source, self-hosted Python framework with backtesting, optimization, live trading and DEX support. — [Gainium review of Jesse](https://gainium.io/review/jesse)
- **RoboVault's open-source web3 backtester / Arkiver:** an indexer for fetching historical on-chain data for DeFi backtests. The author calls historical data retrieval the hardest part, and protocol coverage was limited. — [RoboVault on Medium](https://medium.com/@RoboVault/open-source-web3-backtester-e0ef81165121)

### Inferences
- An event-driven engine is better suited than a vectorized one, because fills depend on order position within a slot and on state (reserves).
- Vectorized tools are fine for fast signal screening on candles, but not for execution realism.

### Gaps
- The search returned nothing on vectorbt, NautilusTrader, hftbacktest or Backtrader in a DEX/on-chain context, so their suitability is unverified here. Unverified background:
  - **NautilusTrader:** an event-driven Rust/Python engine with custom data and venue adapters. It could host a custom AMM fill model.
  - **hftbacktest:** models queue position and latency for limit-order books. Its latency-modelling ideas transfer, but its order-book model does not map directly to AMMs.
  - **vectorbt:** suits fast parameter sweeps on OHLCV.
  - Verify each project's current status and license.
- Whether any maintained open-source Solana-specific backtester (e.g. a pump.fun replay tool on GitHub) exists as of Nov 2026 could not be checked.
