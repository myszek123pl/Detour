# Data storage design for a Solana memecoin trading bot

Scratch computation: /tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/sizing.py (output: sizing_out.txt). Items marked [ASSUMPTION] are mine, not sourced.

## 1. What throughput must the storage layer absorb (trades/sec on Solana DEXs)?

### Takeaway
Chain-wide Solana non-vote throughput is ~1.2-2k TPS, but DEX swaps are a small fraction of it. A memecoin-focused trade stream is plausibly hundreds of rows/s on average and low thousands/s at bursts, which is a trivial load for ClickHouse, comfortable for Timescale/Postgres with batching, and tiny if the bot only tracks a watchlist. Direct DEX trade-count figures in public sources are thin and inconsistent, so the sizing is scenario-based.

### Cited Findings
- Average Solana non-vote TPS was ~1,584 in July 2026 per Solana Compass; the record day of 171.9M non-vote txs (10 Aug) is ~1,990 TPS averaged over 24h. — [Solana Compass](https://solanacompass.com/news/solana-july-2026-monthly-transaction-record-42b-non-vote-txns-up-91-since-december) (as relayed by search summary; I did not open the page)
- One outlier source claims >2,500 non-vote TPS sustained; conflicts with the above. — [CryptoBriefing](https://cryptobriefing.com/solana-true-tps-surpasses-2500/)
- Alpenglow (reported live 21 Oct 2026) removed votes from blocks, so TPS headline figures before and after are not comparable; ~1,284 non-vote TPS on 5 Nov 2026. — [Coinpaprika](https://coinpaprika.com/education/solana-ecosystem/) (single secondary source; verify)
- Bitquery snapshot (23 Apr 2026): Meteora 22.4M trades, PumpSwap 19.5M trades; window is not stated in the summary I saw, though likely 24h. Pump.fun avg trade ~$40 vs ~$425 on PumpSwap. — [Bitquery docs](https://docs.bitquery.io/docs/mcp/trading/examples/solana-dex-market-share/)
- Late-July 2026 DefiLlama snapshot: Solana DEX volume ~$1.18B/day, Pump.fun ~$492M of it; Pump.fun ATH >$2B/day in early Jan 2026. Market-share figures across sources conflict (PumpSwap 74% vs Pump.fun 18.6% / Raydium 12.2%) and are differently dated. — [Cryptoslate](https://cryptoslate.com/pumpswap-captures-74-of-solana-dex-volume-as-memecoins-surge/), [Raydium vs PumpFun](https://cryptobriefing.com/raydium-surpasses-pumpfun-dex-volume/)
- Pump.fun launched ~42,000 tokens in one day, fewer than 2 will ever reach a DEX (older article; date not verified). — [Solana Compass](https://solanacompass.com/news/pumpfun-launched-42000-tokens-in-one-day-fewer-than-2-will-ever-reach-a-dex)

### Inferences
- Three scenarios [ASSUMPTION, anchored loosely on the Bitquery 20M-ish per-venue counts]: A watchlist-only 2M trades/day (23/s avg), B all memecoin venues 30M/day (347/s avg, ~3.5k/s burst at an assumed 10x peak), C full DEX firehose 80M/day (926/s avg, ~9k/s burst).
- Even scenario C is under 10k rows/s burst: one ClickHouse node handles this by a wide margin; the real constraint is ingest source (gRPC/Geyser, RPC cost), not the DB.
- Hot-path latency, not volume, drives design: the trading decision loop must read from memory (Redis or in-process), not from the analytical DB.

### Gaps
- No reliable direct daily swap-count for Raydium/Pump.fun/Orca in 2026; Dune/Flipside query would close it.
- Burst multiple (10x) is my guess; measure from the stream during a token-launch spike.

## 2. Which databases for which job (ClickHouse, TimescaleDB/Postgres, Redis, DuckDB/Parquet)?

### Takeaway
Recommended split: ClickHouse (or DuckDB+Parquet for a solo/low-budget start) for append-only market data and features; Postgres for transactional state (orders, positions, wallets config, tax ledger); Redis for the real-time hot state and pub/sub; Parquet on object storage as the cold archive and replay source. TimescaleDB is a defensible single-DB alternative at scenario A/B scale.

### Cited Findings
- ClickHouse docs: keep sync inserts near one insert query per second regardless of size; async inserts allow higher insert rates, flushing on buffer size (default 10 MB per a secondary guide) or timeout (default 1000 ms), and wait_for_async_insert=1 is recommended for durability. — [ClickHouse bulk inserts](https://clickhouse.com/docs/optimize/bulk-inserts), [insert strategy](https://clickhouse.com/docs/best-practices/selecting-an-insert-strategy), [Aliyun guide](https://help.aliyun.com/en/clickhouse/use-cases/bulk-or-asynchronous-data-insertion)
- Async inserts disable automatic deduplication by default. — [Aliyun guide](https://help.aliyun.com/en/clickhouse/use-cases/bulk-or-asynchronous-data-insertion)
- Altinity TSBS study: ClickHouse loads significantly faster than alternatives, compression good but behind InfluxDB. — [Altinity](https://altinity.com/blog/ClickHouse-for-time-series)
- Independent arXiv benchmark (2023, high-frequency data) found ClickHouse's default compression ratio poor (near 100%) because of no delta coding on timestamps; this is default-codec behaviour, fixable with per-column codecs. — [arXiv 2301.12561](https://arxiv.org/pdf/2301.12561)
- Timescale's own test: ClickHouse ~16 GB vs Timescale ~19 GB uncompressed (vendor source, interested party). — [Timescale blog](https://timescale.com/blog/what-is-clickhouse-how-does-it-compare-to-postgresql-and-timescaledb-and-how-does-it-perform-for-time-series-data)
- Tiger Data docs claim Hypercore typically cuts storage 90-98%; a user report 220 GB -> 25 GB (88.6%); a blockchain tutorial 1307 MB -> 237 MB (~82%). Ratio depends heavily on segmentby cardinality. — [Tiger Data](https://www.tigerdata.com/learn/postgresql-compression), [DEV post](https://dev.to/polliog/timescaledb-compression-from-150gb-to-15gb-90-reduction-real-production-data-bnj), [tutorial](https://docs.timescale.com/tutorials/latest/blockchain-query/blockchain-compress)
- Tinybird (a ClickHouse vendor) says ClickHouse default is LZ4; treat claims about relative compression with caution. — [Tinybird](https://www.tinybird.co/blog/clickhouse-vs-timescaledb)

### Inferences
- Decision matrix [ASSUMPTION-based judgement]:
  - Redis: current price/liquidity per token, rolling-window features (last 1s/5s/30s/5m), position/risk state, dedupe keys (signature seen), kill-switch flags. Use Streams or pub/sub between ingestor and strategy. Persist with AOF everysec; it is a cache, not system of record.
  - Postgres (plain, no Timescale needed): orders, fills, positions, wallet registry, config, PnL ledger, tax log. Needs ACID, FKs, updates. Volume is thousands of rows/day.
  - ClickHouse: trades, pool snapshots, OHLCV, funding edges, feature history, labels. Append-heavy, scan-heavy, ReplacingMergeTree/AggregatingMergeTree materialized views for bars.
  - DuckDB over Parquet: research/backtesting on laptops, cold archive; zero ops. For a solo operator at scenario A/B, DuckDB+Parquet alone plus Redis plus Postgres may be enough and avoids running ClickHouse.
  - TimescaleDB: choose it if you want one SQL engine (market data + state, joins with orders) and stay at A/B scale; hypertable + compression gives ~6-10x. Cost is slower wide scans and Postgres tuning for ingest.
- Do not use Redis or Postgres for the raw firehose beyond a short retention window.
- Use per-column codecs in ClickHouse (DoubleDelta on timestamps/slots, Gorilla/ZSTD on prices, LowCardinality or dictionary on venue/side, FixedString(32) or UInt256 on pubkeys) rather than defaults, given the arXiv finding.

### Gaps
- No independent, recent head-to-head ClickHouse vs TimescaleDB benchmark on blockchain-trade-shaped data was found; most results are vendor-authored.
- Did not verify the ClickHouse version-specific defaults (async_insert_busy_timeout_ms etc.) against the official settings page.

## 3. Schema sketches (tokens, trades, wallets, funding edges, features, orders, fills, PnL, tax log)

### Takeaway
Market data in ClickHouse keyed for time/mint access; stateful financial records in Postgres with immutable ledger semantics. Store raw pubkeys as 32-byte binary plus a surrogate small id where joins matter.

### Cited Findings
- ClickHouse recommends batching and ORDER BY design for insert/query efficiency (see sources in section 2). Beyond that, the DDL below is my design, not sourced.

### Inferences
All DDL is [ASSUMPTION] design sketch.

```sql
-- ================= ClickHouse (market data / analytics) =================
CREATE TABLE tokens (
  mint            FixedString(32),
  symbol          LowCardinality(String),
  name            String,
  creator         FixedString(32),
  launch_venue    LowCardinality(String),      -- pumpfun, bonk, ...
  created_ts      DateTime64(3, 'UTC'),
  created_slot    UInt64,
  graduated_ts    Nullable(DateTime64(3,'UTC')),
  primary_pool    FixedString(32),
  supply          UInt64, decimals UInt8,
  mint_authority_revoked UInt8, freeze_authority_revoked UInt8,
  metadata_uri    String,
  version         UInt64                       -- ReplacingMergeTree version
) ENGINE = ReplacingMergeTree(version) ORDER BY mint;

CREATE TABLE trades (
  ts          DateTime64(3,'UTC') CODEC(DoubleDelta, ZSTD(1)),
  slot        UInt64              CODEC(DoubleDelta, ZSTD(1)),
  tx_index    UInt16,  ix_index UInt16,
  signature   FixedString(64),
  venue       LowCardinality(String),
  pool        FixedString(32),
  mint        FixedString(32),
  wallet      FixedString(32),
  side        Enum8('buy'=1,'sell'=2),
  base_amt    UInt64, quote_amt UInt64,          -- raw lamports/atoms
  price_usd   Float64 CODEC(Gorilla, ZSTD(1)),
  quote_usd   Float64,                           -- notional
  fee_lamports UInt64, priority_fee UInt64, jito_tip UInt64,
  is_bundle   UInt8,
  inserted_at DateTime DEFAULT now()
) ENGINE = ReplacingMergeTree
  PARTITION BY toYYYYMMDD(ts)
  ORDER BY (mint, ts, signature, ix_index)         -- dedup key; replay-safe
  TTL toDate(ts) + INTERVAL 30 DAY TO VOLUME 'cold', toDate(ts) + INTERVAL 365 DAY DELETE;

CREATE MATERIALIZED VIEW ohlcv_1s_mv TO ohlcv_1s AS
SELECT mint, toStartOfInterval(ts, INTERVAL 1 SECOND) AS t,
       argMinState(price_usd, ts) o, maxState(price_usd) h, minState(price_usd) l,
       argMaxState(price_usd, ts) c, sumState(quote_usd) v, countState() n,
       uniqState(wallet) uw
FROM trades GROUP BY mint, t;     -- AggregatingMergeTree target; same for 1m, 5m

CREATE TABLE pool_snapshots (       -- reserves/liquidity sampled
  ts DateTime64(3), pool FixedString(32), mint FixedString(32),
  base_reserve UInt64, quote_reserve UInt64, liquidity_usd Float64, mcap_usd Float64,
  bonding_curve_pct Nullable(Float32)
) ENGINE = MergeTree PARTITION BY toYYYYMM(ts) ORDER BY (mint, ts);

CREATE TABLE wallets (
  wallet FixedString(32), first_seen DateTime64(3), label LowCardinality(String), -- sniper, kol, cex, mev, fresh
  funded_by FixedString(32), funded_ts Nullable(DateTime64(3)), funding_cluster_id UInt64,
  total_trades UInt64, realized_pnl_usd Float64, win_rate Float32, updated_at DateTime
) ENGINE = ReplacingMergeTree(updated_at) ORDER BY wallet;

CREATE TABLE funding_edges (
  ts DateTime64(3), src FixedString(32), dst FixedString(32),
  lamports UInt64, signature FixedString(64), src_kind LowCardinality(String)  -- cex_hot, user, mixer-like
) ENGINE = MergeTree ORDER BY (dst, ts);       -- add 2nd copy ORDER BY (src, ts) as projection

CREATE TABLE features (
  ts DateTime64(3), mint FixedString(32),
  feat_set_version UInt16,
  f Array(Float32) CODEC(ZSTD(3)),             -- positional vector; names in feature_registry
  -- or wide columns for the ~20 you query often:
  buy_vol_5s Float32, sell_vol_5s Float32, uniq_buyers_30s UInt16, top10_holder_pct Float32,
  bundle_pct Float32, cluster_conc Float32, liq_usd Float32, price_chg_1m Float32,
  label_fwd_ret_60s Nullable(Float32)          -- backfilled for training (point-in-time safe)
) ENGINE = MergeTree PARTITION BY toYYYYMMDD(ts) ORDER BY (mint, ts);

CREATE TABLE feature_registry (name String, version UInt16, kind Enum8('stream'=1,'batch'=2),
  sql_or_code_hash String, ttl_s UInt32, owner String) ENGINE = MergeTree ORDER BY (name, version);

-- ================= Postgres (transactional system of record) =================
CREATE TABLE strategies (id serial PRIMARY KEY, name text UNIQUE, params jsonb, git_sha text, enabled bool);

CREATE TABLE orders (
  id uuid PRIMARY KEY, strategy_id int REFERENCES strategies, mint bytea NOT NULL,
  side text CHECK (side IN ('buy','sell')), order_type text, route text,           -- jupiter/jito/direct
  amount_in numeric(38,0), min_out numeric(38,0), slippage_bps int,
  priority_fee bigint, jito_tip bigint, decision_ts timestamptz, sent_ts timestamptz,
  status text, reason text, signal_snapshot jsonb,                                   -- features at decision time
  created_at timestamptz DEFAULT now());

CREATE TABLE fills (
  id bigserial PRIMARY KEY, order_id uuid REFERENCES orders, signature bytea UNIQUE,
  slot bigint, block_time timestamptz, landed_ts timestamptz,
  amount_in numeric(38,0), amount_out numeric(38,0), price_usd numeric(24,12),
  fee_lamports bigint, tip_lamports bigint, sol_usd numeric(18,6), slippage_realized_bps int);

CREATE TABLE positions (id bigserial PRIMARY KEY, mint bytea, strategy_id int, opened_ts timestamptz,
  closed_ts timestamptz, qty numeric(38,0), avg_cost_usd numeric(24,12), status text);

CREATE TABLE pnl_ledger (          -- append-only, double-entry style
  id bigserial PRIMARY KEY, ts timestamptz, position_id bigint, fill_id bigint,
  kind text,                       -- realized, fee, tip, rent, unrealized_mark
  amount_usd numeric(24,8), amount_sol numeric(24,9), sol_usd numeric(18,6));

CREATE TABLE tax_lots (            -- cost-basis tracking
  id bigserial PRIMARY KEY, mint bytea, acquired_ts timestamptz, qty_remaining numeric(38,0),
  cost_basis_usd numeric(24,8), acquire_fill_id bigint, method text);        -- FIFO/HIFO per jurisdiction

CREATE TABLE tax_log (
  id bigserial PRIMARY KEY, ts timestamptz, event_type text,   -- disposal, swap, fee, airdrop, transfer
  lot_id bigint, fill_id bigint, proceeds_usd numeric(24,8), cost_basis_usd numeric(24,8),
  gain_usd numeric(24,8), holding_days int, tx_signature bytea, fx_rate_pln numeric(12,6),
  tax_year smallint, locked bool DEFAULT false);               -- immutable once locked
-- revoke UPDATE/DELETE on pnl_ledger, tax_log via role; corrections as reversing rows.

-- ================= Redis (hot state) =================
-- tok:{mint}:px            HASH   price, liq, mcap, last_ts          (TTL 1h after last trade)
-- tok:{mint}:win:{5s|30s}  ZSET/STREAM rolling trades or HASH of aggregates
-- feat:{mint}              HASH   latest streaming features (versioned field names)
-- pos:{strategy}           HASH   open positions + risk limits
-- seen:sig                 SET/BF signatures dedupe (TTL 10m)
-- stream:trades            STREAM ingestor -> strategy (MAXLEN ~ 1e6)
-- killswitch               STRING global halt flag
```

Key design choices:
- ORDER BY (mint, ts) optimises per-token reads (most bot queries); a projection or second table keyed by (wallet, ts) serves wallet-history queries.
- ReplacingMergeTree + deterministic key (signature, ix_index) makes replay/backfill idempotent, which matters because async inserts do not dedupe by default (see section 2).
- Store raw integer amounts plus derived USD; never recompute historical USD from mutable inputs (store sol_usd used).
- Persist `signal_snapshot` with each order so any trade can be explained and backtests can be reconciled to live.

### Gaps
- DDL not executed against a real ClickHouse/Postgres instance (no DB in sandbox); syntax is sketch-level and should be validated.
- Tax-specific columns (Polish PIT-38 / crypto rules, FX rate source) depend on jurisdiction and were not researched.

## 4. Storage volume per day (computed)

### Takeaway
Trades are small: scenario B ~8 GB/day raw, ~1 GB/day compressed in ClickHouse; full firehose ~21 GB/day raw, ~2.6 GB/day compressed. High-frequency per-token feature snapshots can dominate if sampled at 1s for many tokens (~2.2 GB/day compressed for 500 tokens). Orders/fills/PnL/tax are negligible (<10 MB/day).

### Cited Findings
- Compression ratios: Hypercore claims 90-98%, observed 82-89% in the cited examples (see section 2 sources). ClickHouse ratios are not sourced; I use 4x/8x/12x [ASSUMPTION].

### Inferences
Computed with sizing.py. Assumptions: 262 B/trade raw logical row; ClickHouse 8x typical (4x conservative, 12x optimistic); Plain Postgres/uncompressed Timescale = raw x1.6 for headers and indexes; Timescale compressed 6x of raw.

| Scenario | trades/day | avg/s | burst/s (10x) | raw GB/day | CH 8x GB/day | CH 4x | PG uncompressed GB/day | Timescale 6x GB/day |
|---|---|---|---|---|---|---|---|---|
| A watchlist | 2M | 23 | 231 | 0.52 | 0.07 | 0.13 | 0.84 | 0.09 |
| B memecoin all | 30M | 347 | 3,472 | 7.9 | 0.98 | 1.97 | 12.6 | 1.31 |
| C full firehose | 80M | 926 | 9,259 | 21.0 | 2.62 | 5.24 | 33.5 | 3.49 |

Other tables per day [ASSUMPTION inputs]:

| Table | assumed volume | GB/day |
|---|---|---|
| 1s OHLCV, 2,000 watched tokens active 6h | sparse | ~0.30 |
| 1m OHLCV, 20k active tokens | 20k x 1440 x 64 B | ~1.84 (before compression; ~0.3 after at 6x) |
| new tokens | 40k/day x 400 B | 0.016 |
| funding edges | 300k/day x 150 B | 0.045 |
| feature vectors, 1 Hz, 500 tokens, 60 f32 | 43M rows | 11.2 raw / ~2.2 at 5x |
| orders+fills+PnL+tax | ~5k/day | ~0.004 |
| raw tx-log Parquet archive, scenario B (~600 B/tx, 6x zstd) | 30M | ~3.0 |

Rollups: scenario B total hot analytics ~ 1 (trades) + ~2.2 (features) + ~0.5 (bars/misc) = ~3-4 GB/day compressed, ~1.1-1.5 TB/year. Scenario A is < 1 GB/day all-in.

Feature-store sizing implication: feature history is the biggest line item, so sample features on events (trade/pool change) or at 1-5 s only for tokens passing a liquidity/age filter, and keep only a versioned subset long-term.

### Gaps
- Real compression ratios on this schema are unmeasured; run a 1-day sample load to calibrate (cheap, high value).
- Raw instruction/log archive size (600 B/tx) is a guess.

## 5. Feature store: real-time vs batch

### Takeaway
Use a thin, hand-rolled "dual-write, single-definition" feature store rather than Feast/Tecton: streaming features computed incrementally in the ingestor and held in Redis for the decision loop, the same definitions persisted to ClickHouse for training, and batch features (wallet reputation, funding clusters, holder concentration) computed on a schedule and pushed to Redis/ClickHouse with an as-of timestamp.

### Cited Findings
- No sourced benchmark specific to feature stores was gathered (search budget used on database facts). Redis/ClickHouse capabilities are as in section 2.

### Inferences
[ASSUMPTION] design:
- Streaming tier (ms-s latency): rolling volumes, buy/sell imbalance, unique buyers, price changes, curve progress. Computed in process (Rust/Go/Python+numba) from the trade stream; written to Redis HASH `feat:{mint}` and appended to ClickHouse `features` on event or 1-5 s cadence.
- Near-line tier (10 s-minutes): holder concentration, bundle %, creator history, dev-wallet behavior, funding-cluster overlap; computed by workers triggered at token creation/graduation, cached in Redis with TTL.
- Batch tier (hourly/daily): wallet PnL/win-rate and labels, funding-graph clustering (connected components over `funding_edges`), cohort stats; computed with ClickHouse SQL or DuckDB, published as `wallets` rows and Redis hashes.
- Training/serving skew control: one feature definition module generating both live and backfill values; `feat_set_version` in every row; point-in-time joins using `ts <= decision_ts` (ClickHouse ASOF JOIN); persist the exact vector in `orders.signal_snapshot`.
- Labels (forward returns, rug flag) backfilled by a delayed job to avoid leakage.
- Redis hot set is small: ~27 MB for 500 tokens x (60 features + 2 KB state) + 50k tracked wallets x 512 B (computed). A single small Redis instance suffices.

### Gaps
- Whether Feast or similar adds value at this scale was not researched; my judgement is no.

## 6. Retention, compression, tiering

### Takeaway
Keep raw trades hot ~30 days, warm to 12 months on cheaper disk/object storage with TTL moves, and archive Parquet (zstd) forever or delete after 1-2 years; keep orders/fills/PnL/tax permanently (legal retention).

### Cited Findings
- ClickHouse supports TTL for moves and deletes by volume (feature documented in ClickHouse docs; not re-fetched here). Hypercore/Timescale compression policies compress older chunks automatically. — [Tiger Data compression policy](https://www.tigerdata.com/docs/use-timescale/latest/compression/compression-policy/)

### Inferences
[ASSUMPTION] policy:
- trades: 30 d hot NVMe, to 365 d object-store volume, then keep only 1m bars + wallet aggregates; Parquet archive of raw kept as the replay source.
- 1s bars/features: 14-30 d; 1m bars: 2 yr; 1h bars: forever.
- pool_snapshots: 30 d. funding_edges: forever (tiny). tokens: forever.
- orders/fills/positions/pnl/tax_log: forever; tax records commonly must be retained for years (check jurisdiction, not researched).
- Dead tokens: after N days of zero volume, drop 1s-level data but keep 1m summary and launch/rug labels (needed for survivorship-unbiased research).
- Always keep failed/unlanded transaction attempts; they are needed to model slippage and landing rate.

### Gaps
- Legal retention periods not researched.

## 7. Cost estimate

### Takeaway
Storage cost is negligible next to data-source cost (RPC/gRPC). Even full-firehose retention for a year is under ~1 TB compressed (~$22-77/month storage). The meaningful bill is a Geyser/gRPC feed and a server, not the database.

### Cited Findings
- None sourced for prices (cloud list prices not searched). Unit prices below are [ASSUMPTION] approximate: block storage ~$0.08/GB-month, object storage ~$0.023/GB-month.

### Inferences
From sizing.py (ClickHouse 8x, one year of trades only): scenario A 24 GB (~$2/mo EBS), B 359 GB (~$29/mo EBS, ~$8 S3), C 956 GB (~$77/mo EBS, ~$22 S3). Uncompressed Postgres would be 0.3 / 4.6 / 12.2 TB per year (~$24 / $367 / $979 per month), which is the strongest argument for columnar storage or Timescale compression at B and above.
[ASSUMPTION] Compute: one 8 vCPU/32 GB box (~$150-300/month) can host ClickHouse + Postgres + Redis for scenario B; bot at A can run on a ~$40-80 VPS with DuckDB/Parquet + SQLite/Postgres + Redis. Managed ClickHouse/Timescale cloud would cost several hundred $/month and is likely unnecessary.
Recommended phasing: (1) Start: Postgres + Redis + Parquet files queried with DuckDB; (2) when feature history or multi-day scans get slow, add single-node ClickHouse; (3) only add replication/cluster when the bot's PnL justifies it.

### Gaps
- No quoted vendor prices; gRPC provider costs not covered (another researcher's scope).
- Compute sizing is a rule-of-thumb, not benchmarked.
