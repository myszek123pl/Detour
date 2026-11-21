import duckdb,sys
D=sys.argv[1]; W=sys.argv[2]
c=duckdb.connect(W+'/who.duckdb')
c.sql("pragma threads=4; pragma memory_limit='10GB'")
c.sql(f"create or replace view tr0 as select wallet w, token_address tk, side=\'buy\' isb, amount_usd usd, epoch_ms(ts)/1000.0 t from read_parquet('{D}/trades-*.parquet')")
c.sql(f"create or replace table core as select token_address tk, min(captured_at::timestamptz) cap, min(time_since_launch_sec) tsl, max(market_cap_usd) mc, max(max_return_24h) mr24 from read_parquet('{D}/tokens.parquet') group by 1")
c.sql("""create or replace table wt as select w, tk,
 count(*) filter(isb) nb, count(*) filter(not isb) ns,
 coalesce(sum(usd) filter(isb),0) buy, coalesce(sum(usd) filter(not isb),0) sell,
 min(t) filter(isb) fb, max(t) filter(isb) lb, min(t) filter(not isb) fs, max(t) filter(not isb) ls
 from tr0 group by w,tk""")
c.sql("create or replace table tt as select tk, min(t) f, max(t) l, count(*) n, sum(usd) filter(isb) tbuy, sum(usd) filter(not isb) tsell, count(distinct w) nw from tr0 group by tk")
# buyer rank within token
c.sql("""create or replace table wt2 as select wt.*, wt.sell-wt.buy pnl, tt.f tf, tt.l tl, tt.n tn,
  case when nb>0 then rank() over (partition by wt.tk order by fb) end brank,
  count(*) filter (nb>0) over (partition by wt.tk) nbuyers,
  core.tk is not null as iscore, core.mr24, core.tsl
 from wt join tt using(tk) left join core using(tk)""")
print(c.sql("select count(*), count(*) filter(nb=0), count(*) filter(ns=0), count(*) filter(nb>0 and ns>0), sum(buy), sum(wt2.sell), sum(sell) filter(nb=0), sum(buy) filter(ns=0), sum(sell) filter(nb>0), sum(buy) filter(ns>0) from wt2"))
c.sql("""create or replace table wal as select w, count(*) ntok, sum(nb+ns) ntr, sum(buy) buy, sum(wt2.sell) sell, sum(sell-buy) pnl,
  count(*) filter(nb>0) ntok_b, median(buy) filter(nb>0) med_pos
  from wt group by w""")
print(c.sql("select count(*), quantile_cont(ntr,[.5,.9,.99,.999]), quantile_cont(ntok,[.5,.9,.99,.999]) from wal"))
