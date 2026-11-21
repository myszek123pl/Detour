import sys, duckdb, pandas as pd
D=sys.argv[1]
pd.set_option('display.width',220)
c=duckdb.connect()
c.execute(f"create view tr as select * from read_parquet('{D}/trades-00*.parquet')")
c.execute(f"create view tk as select sample_id,token_address,captured_at,time_since_launch_sec,liquidity_usd,market_cap_usd,buy_usd_1h,sell_usd_1h,net_flow_usd,buy_total from read_parquet('{D}/tokens.parquet')")
print(c.sql("select count(*),count(distinct token_address),min(ts),max(ts),sum(case when ts<timestamp '2026-06-01' then 1 else 0 end) pre_june from tr").df())
print(c.sql("select year(ts) y,month(ts) m,count(*) n from tr group by 1,2 order by 1,2").df().to_string())
print(c.sql("select side,count(*),sum(amount_usd),median(amount_usd) from tr group by 1").df())
print(c.sql("select count(distinct token_address) from tr where token_address in (select token_address from tk)").df())
# trades relative to captured_at
print(c.sql("""select quantile_cont(epoch(tr.ts)-epoch(tk.captured_at),[.01,.05,.25,.5,.75,.95,.99]) q, count(*) n,
  avg(case when tr.ts>tk.captured_at then 1 else 0 end) frac_after
  from tr join (select distinct token_address,captured_at from tk) tk using(token_address)""").df().to_string())
