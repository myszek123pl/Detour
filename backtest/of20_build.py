# Builds a local duckdb with trades/tokens/ohlcv (read-only use of the untrusted parquet data; no dataset scripts executed).
import duckdb, sys, os
D = "/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/datasets/solana-memecoin-dataset/repo/data"
W = "/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/w/w.db"
c = duckdb.connect(W)
c.sql(f"create or replace table t as select wallet, token_address tok, side='buy' as buy, amount_usd usd, epoch(ts) ts from '{D}/trades-00*.parquet'")
c.sql(f"create or replace table tk as select * from '{D}/tokens.parquet'")
c.sql(f"create or replace table oh as select * from '{D}/ohlcv.parquet'")
c.sql(f"create or replace table wl as select * from '{D}/wallets.parquet'")
c.sql("create or replace table tkm as select token_address tok, min(epoch(captured_at)) cap0, max(epoch(captured_at)) cap1, count(*) nsnap, min(epoch(captured_at)-time_since_launch_sec) launch from tk group by 1")
c.sql("create or replace table ohm as select token_address tok, min(ts) o0, max(ts) o1, count(*) nb from oh group by 1")
c.sql("create or replace table tm as select tok, count(*) n, min(ts) t0, max(ts) t1 from t group by 1")
print("ok")
