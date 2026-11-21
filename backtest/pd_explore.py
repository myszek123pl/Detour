import duckdb,sys
D=sys.argv[1]
c=duckdb.connect()
c.sql(f"create view tr as select * from '{D}/trades-00*.parquet'")
c.sql(f"create view oh as select * from '{D}/ohlcv.parquet'")
c.sql("create table tk as select token_address, count(*) n, min(ts) t0, max(ts) t1 from tr group by 1")
c.sql("create table ok as select token_address, count(*) nc, min(to_timestamp(ts)) o0, max(to_timestamp(ts)) o1 from oh group by 1")
print(c.sql("select count(*), median(n), avg(n), quantile_cont(n,.9) from tk").fetchall())
print(c.sql("select count(*), median(nc), quantile_cont(nc,.9), max(nc) from ok").fetchall())
print(c.sql("""select count(*) n, median(epoch(t1)-epoch(t0))/60 span_min_med, median(epoch(t0)-epoch(o0))/60 t0_vs_o0, median(epoch(t1)-epoch(o1))/60 t1_vs_o1,
 avg((t0<o1 and t1>o0)::int) overlap from tk join ok using(token_address)""").fetchall())
print(c.sql("""select n>=200 big,count(*),median(epoch(t1)-epoch(t0))/60 from tk join ok using(token_address) group by 1""").fetchall())
# trades inside ohlcv window
print(c.sql("""select count(*) from tr join ok using(token_address) where tr.ts between o0 and o1 + interval 15 minute""").fetchall())
print(c.sql("select count(*) from tr join ok using(token_address)").fetchall())
