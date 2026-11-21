import duckdb,sys
D=sys.argv[1]
c=duckdb.connect()
c.sql(f"create view tr as select * from read_parquet('{D}/trades-*.parquet')")
c.sql(f"create view tk as select token_address, min(captured_at) cap, count(*) nsnap, min(time_since_launch_sec) tsl from read_parquet('{D}/tokens.parquet') group by 1")
print(c.sql("select quantile_cont(n,[0.01,.1,.25,.5,.75,.9,.99]), max(n) from (select token_address,count(*) n from tr group by 1)"))
print(c.sql("select n,count(*) from (select token_address,count(*) n from tr group by 1) group by 1 order by 2 desc limit 15"))
print(c.sql("select count(*) from (select token_address from tr group by 1 having count(*)>=200)"))
print(c.sql("select count(*) ntok, count(distinct tr.token_address) from tk left join tr using(token_address)"))
print(c.sql("select count(distinct token_address) from tr where token_address not in (select token_address from tk)"))
print(c.sql("select year(ts),month(ts),count(*),count(distinct token_address) from tr group by 1,2 order by 1,2"))
# per-token span
print(c.sql("select quantile_cont(epoch(mx-mn),[.1,.5,.9]) from (select min(ts) mn,max(ts) mx from tr group by token_address)"))
# trades relative to cap
print(c.sql("select quantile_cont(epoch(tr.ts-tk.cap),[0,.01,.5,.99,1]) from tr join tk using(token_address)"))
print(c.sql("select tr.token_address is null, count(*) from tr left join tk using(token_address) where tr.ts> tk.cap group by 1"))
# dup rows
print(c.sql("select count(*) from (select wallet,token_address,side,amount_usd,ts,count(*) n from tr group by all having n>1)"))
