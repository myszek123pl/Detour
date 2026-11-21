import duckdb,sys
D=sys.argv[1]
c=duckdb.connect()
c.sql(f"create view tr as select * from read_parquet('{D}/trades-*.parquet')")
c.sql(f"create view tkall as select * from read_parquet('{D}/tokens.parquet')")
c.sql("""create table s as select sample_id, token_address, captured_at::timestamptz cap, time_since_launch_sec tsl, volume_h24, holder_count, unique_buyers, buy_usd_1h, sell_usd_1h from tkall where time_since_launch_sec<86400""")
c.sql("""create table m as select s.*, count(tr.ts) n, coalesce(sum(tr.amount_usd),0) vol, count(distinct tr.wallet) w
 from s left join tr on tr.token_address=s.token_address and tr.ts<=s.cap and tr.ts>=s.cap-interval 24 hour group by all""")
print(c.sql("select count(*), quantile_cont(vol/nullif(volume_h24,0),[.05,.1,.25,.5,.75,.9,.95]) from m"))
print(c.sql("select case when tsl<120 then '<2m' when tsl<300 then '2-5m' when tsl<600 then '5-10m' when tsl<1800 then '10-30m' else '30m+' end b, count(*), quantile_cont(vol/nullif(volume_h24,0),[.1,.25,.5,.75,.9]), median(n) from m group by 1 order by 1"))
print(c.sql("select (n between 95 and 110) spike, count(*), quantile_cont(vol/nullif(volume_h24,0),[.1,.25,.5,.75,.9]) from m group by 1"))
print(c.sql("select quantile_cont(w/nullif(holder_count,0),[.1,.25,.5,.75,.9]) from m where holder_count>0"))
