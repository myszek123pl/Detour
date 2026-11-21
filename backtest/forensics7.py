import sys, duckdb, pandas as pd, numpy as np
D=sys.argv[1]
pd.set_option('display.width',220)
c=duckdb.connect()
c.execute(f"create view tr as select * from read_parquet('{D}/trades-00*.parquet')")
c.execute(f"create table tk as select sample_id,token_address,captured_at,time_since_launch_sec,liquidity_usd,market_cap_usd,buy_usd_1h,sell_usd_1h,net_flow_usd,buy_total,volume_h24,holder_count,unique_buyers,unique_sellers,price_change_1h from read_parquet('{D}/tokens.parquet')")
c.execute("""create table agg as select tk.sample_id,
 sum(case when tr.ts<=tk.captured_at and side='buy' then amount_usd else 0 end) pre_buy,
 sum(case when tr.ts<=tk.captured_at and side='sell' then amount_usd else 0 end) pre_sell,
 sum(case when tr.ts<=tk.captured_at then 1 else 0 end) pre_n,
 sum(case when tr.ts<=tk.captured_at and tr.ts>tk.captured_at-interval 1 hour and side='buy' then amount_usd else 0 end) h1_buy,
 sum(case when tr.ts<=tk.captured_at and tr.ts>tk.captured_at-interval 1 hour and side='sell' then amount_usd else 0 end) h1_sell,
 sum(case when tr.ts>tk.captured_at and tr.ts<=tk.captured_at+interval 1 hour and side='buy' then amount_usd else 0 end) f1_buy,
 sum(case when tr.ts>tk.captured_at and tr.ts<=tk.captured_at+interval 1 hour and side='sell' then amount_usd else 0 end) f1_sell,
 sum(case when tr.ts>tk.captured_at then 1 else 0 end) post_n,
 min(tr.ts) first_ts, max(case when tr.ts<=tk.captured_at then tr.ts end) last_pre_ts
 from tk join tr using(token_address) group by 1""")
df=c.sql("select tk.*,agg.* exclude(sample_id) from tk join agg using(sample_id)").df()
df.to_parquet('/tmp/x/trcmp.parquet')
print(len(df))
