# Builds 15m bar panel: OHLCV (deduped) + trade-log flow per bar + token liquidity at first capture
import duckdb, pandas as pd, numpy as np
W = "/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/w/w.db"
c = duckdb.connect(W)
c.sql("""create or replace table bars as
with o as (select token_address tok, ts, arg_max(open,volume) open, arg_max(high,volume) high, arg_max(low,volume) low, arg_max(close,volume) close, max(volume) vol, count(*) ndup,
  min(open) mn_open, max(open) mx_open from oh group by 1,2),
f as (select tok, (cast(ts as bigint)/900)*900 bts, sum(usd) filter (buy) b, sum(usd) filter (not buy) s, count(*) filter (buy) nb, count(*) filter (not buy) ns,
  count(distinct wallet) nw, max(usd) mx from t group by 1,2),
k as (select token_address tok, arg_min(liquidity_usd, captured_at) liq, arg_min(market_cap_usd, captured_at) mc, min(captured_at) cap from tk group by 1)
select o.*, coalesce(f.b,0) b, coalesce(f.s,0) s, coalesce(f.nb,0) nb, coalesce(f.ns,0) ns, coalesce(f.nw,0) nw, coalesce(f.mx,0) mx, k.liq, k.mc, epoch(k.cap) cap
from o left join f on f.tok=o.tok and f.bts=o.ts left join k on k.tok=o.tok""")
print(c.sql("select count(*), count(*) filter (ndup>1), count(*) filter (mn_open<>mx_open), count(*) filter (b+s>0), count(distinct tok) from bars").fetchall())
print(c.sql("select quantile_cont((b+s)/vol,[.1,.25,.5,.75,.9]) from bars where vol>10 and b+s>0").fetchall())
print(c.sql("select count(*) filter ((b+s)/vol between .8 and 1.2)*1.0/count(*) from bars where vol>10").fetchall())
