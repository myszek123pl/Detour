import duckdb,sys
D=sys.argv[1]
c=duckdb.connect()
c.sql(f"create view oh as select * from '{D}/ohlcv.parquet'")
c.sql(f"create view tk as select * from '{D}/tokens.parquet'")
# dup identity
print(c.sql("""with g as (select token_address,ts,count(*) n, count(distinct (open,high,low,close,volume)) nd from oh group by 1,2 having count(*)>1) select count(*), sum((nd>1)::int), avg(n) from g""").fetchall())
print(c.sql("""with s as (select token_address, min(captured_at) c0, max(captured_at) c1, count(*) ns from tk group by 1),
o as (select token_address, min(ts) o0, max(ts) o1, count(distinct ts) nc from oh group by 1)
select count(*), median(o0-epoch(c0))/60 first_vs_cap0, median(o1-epoch(c1))/3600 last_vs_cap1_h, median(nc), quantile_cont(nc,.25),quantile_cont(nc,.75), median(ns), quantile_cont(o1-epoch(c1),.9)/3600
 from s join o using(token_address)""").fetchall())
print(c.sql("select ns,count(*) from (select token_address,count(*) ns from tk group by 1) group by 1 order by 1 limit 8").fetchall())
# continuity open vs prev close
print(c.sql("""with d as (select distinct on (token_address,ts) * from oh order by token_address,ts), x as (select open/lag(close) over (partition by token_address order by ts) r, ts-lag(ts) over (partition by token_address order by ts) g from d) select g, count(*), median(r), quantile_cont(r,.01),quantile_cont(r,.99) from x where g=900 or g=1800 group by 1""").fetchall())
print(c.sql("select count(*) filter (where close/open>3), count(*) filter (where close/open<1/3), count(*) filter(where open<=0 or close<=0 or volume<0) from oh").fetchall())
print(c.sql("select min(captured_at), max(captured_at) from tk").fetchall())
