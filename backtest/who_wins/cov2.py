import duckdb,sys
D=sys.argv[1]
c=duckdb.connect()
c.sql(f"create view tr as select * from read_parquet('{D}/trades-*.parquet')")
c.sql(f"create view tkall as select * from read_parquet('{D}/tokens.parquet')")
c.sql(f"create view sq as select * from read_parquet('{D}/sequences.parquet')")
c.sql("create view tk as select token_address, min(captured_at::timestamptz) cap, count(*) nsnap, min(time_since_launch_sec) tsl, max(time_since_launch_sec) tsl2 from tkall group by 1")
print(c.sql("select nsnap,count(*) from tk group by 1 order by 1"))
print(c.sql("select quantile_cont(tsl,[.05,.25,.5,.75,.95]) from tk"))
# sequences coverage
c.sql("create table seqs as select sample_id, sum(n_trades) nt, sum(buy_usd) bu, sum(sell_usd) su, sum(n_buyers) nbuy from sq group by 1")
c.sql("create table sample1 as select sample_id, token_address, captured_at::timestamptz cap, time_since_launch_sec tsl, buy_total, unique_buyers from tkall")
c.sql("create table trc as select token_address, count(*) n, sum(amount_usd) filter (side='buy') bu, sum(amount_usd) filter (side='sell') su, count(*) filter (side='buy') nb, count(distinct wallet) filter(side='buy') ub from tr group by 1")
print(c.sql("""select count(*), sum(s.nt) seq_trades, sum(trc.n) tr_trades, sum(s.bu) seq_buy, sum(trc.bu) tr_buy, sum(s.su) seq_sell, sum(trc.su) tr_sell
 from sample1 t join seqs s using(sample_id) join trc using(token_address)"""))
print(c.sql("""select quantile_cont(trc.n/nullif(s.nt,0),[.1,.25,.5,.75,.9]) ratio_trades, quantile_cont(trc.bu/nullif(s.bu,0),[.1,.25,.5,.75,.9]) ratio_buyusd, quantile_cont(trc.su/nullif(s.su,0),[.1,.25,.5,.75,.9]) ratio_sellusd
 from sample1 t join seqs s using(sample_id) join trc using(token_address) where s.nt>0"""))
# trades pre-capture per snapshot
print(c.sql("""select quantile_cont(n,[.1,.5,.9]) from (select t.sample_id, count(*) n from sample1 t join tr using(token_address) where tr.ts<=t.cap and tr.ts> t.cap - interval 1 day group by 1)"""))
# trades in first 60s after cap?
print(c.sql("""select count(*) filter (tr.ts>t.cap) post, count(*) filter (tr.ts<=t.cap) pre from sample1 t join tr using(token_address)"""))
# first trade relative to launch
print(c.sql("""select quantile_cont(epoch(f.mn) - (epoch(t.cap)-t.tsl),[.05,.25,.5,.75,.95]) first_trade_after_launch_sec from (select token_address, min(ts) mn from tr group by 1) f join (select token_address, min(cap) cap, min(tsl) tsl from sample1 group by 1) t using(token_address)"""))
