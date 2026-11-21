"""Step 1: pre-capture trades for each token's first snapshot -> parquet. python3 -I tf_extract.py <data> <work>"""
import duckdb,sys
D,W=sys.argv[1:3]
c=duckdb.connect()
c.sql(f"""create table tk as select token_address, min(captured_at) cap from read_parquet('{D}/tokens.parquet') group by 1""")
c.sql(f"""copy (select tr.wallet, tr.token_address, tr.side, tr.amount_usd, epoch(tr.ts) ts, epoch(tk.cap) cap
 from read_parquet('{D}/trades-*.parquet') tr join tk using(token_address) where tr.ts < tk.cap) to '{W}/pre.parquet'""")
c.sql(f"copy (select token_address, epoch(cap) cap from tk) to '{W}/tk.parquet'")
print(c.sql(f"select count(*), count(distinct token_address), min(ts), max(ts) from '{W}/pre.parquet'"))
print(c.sql(f"""select quantile_cont(cap-ts,[0,.01,.1,.5,.9,.99,1]) from '{W}/pre.parquet'"""))
# leak check: any trades with ts == cap or after? count post-capture trades
print(c.sql(f"""select count(*) filter (where tr.ts>=tk.cap) post, count(*) filter (where tr.ts<tk.cap) pre
 from read_parquet('{D}/trades-*.parquet') tr join tk using(token_address)"""))
