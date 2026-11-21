import duckdb,sys
D=sys.argv[1]
c=duckdb.connect()
c.sql(f"create view tr as select * from read_parquet('{D}/trades-*.parquet')")
c.sql(f"create view tk as select token_address, min(captured_at) cap from read_parquet('{D}/tokens.parquet') group by 1")
print(c.sql("select count(*),min(ts),max(ts),count(distinct token_address),count(distinct wallet) from tr"))
print(c.sql("select side,count(*) from tr group by 1"))
print(c.sql("select count(*) n_tok, count(distinct tr.token_address) tok_with_trades from tk left join tr using(token_address)"))
print(c.sql("""select count(*) ntok,
 sum((nb>0)::int) with_pre, sum((na>0)::int) with_post, median(nb) med_pre, median(na) med_post
 from (select tk.token_address, count(*) filter (where tr.ts<tk.cap) nb, count(*) filter (where tr.ts>=tk.cap) na
 from tk left join tr using(token_address) group by 1)"""))
print(c.sql("""select min(tr.ts-tk.cap), median(tr.ts-tk.cap), max(tr.ts-tk.cap) from tk join tr using(token_address)"""))
print(c.sql("select min(ts),max(ts),count(*) from read_parquet('%s/wallet_funding.parquet')"%D))
