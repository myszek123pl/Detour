import duckdb,sys
D=sys.argv[1]
c=duckdb.connect()
c.sql(f"create view tr as select * from '{D}/trades-00*.parquet'")
c.sql(f"create view oh as select * from '{D}/ohlcv.parquet'")
c.sql("""create table tc as select token_address, (epoch(ts)::bigint//900)*900 b, count(*) n, sum(amount_usd) usd, sum(case when side='buy' then amount_usd end) buy from tr group by 1,2""")
r=c.sql("""select count(*), sum(oh.volume), sum(tc.usd), median(tc.usd/nullif(oh.volume,0)), avg(((tc.usd/nullif(oh.volume,0))between .5 and 2.0)::int) , median(tc.n)
 from oh join tc on oh.token_address=tc.token_address and oh.ts=tc.b""").fetchall(); print(r)
print(c.sql("select count(*) from oh").fetchall())
print(c.sql("select sum(volume),median(volume),quantile_cont(volume,.9) from oh").fetchall())
# glitch
print(c.sql("select sum((high>close*10)::int), sum((low<close/10)::int), sum((high>1.5*greatest(open,close))::int), count(*) from oh").fetchall())
# gaps in candles
print(c.sql("""with x as (select token_address, ts-lag(ts) over(partition by token_address order by ts) d from oh) select d, count(*) from x group by 1 order by 2 desc limit 6""").fetchall())
