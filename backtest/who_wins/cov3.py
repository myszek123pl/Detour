import duckdb,sys
D=sys.argv[1]
c=duckdb.connect()
c.sql(f"create view tr as select * from read_parquet('{D}/trades-*.parquet')")
c.sql(f"create view tkall as select * from read_parquet('{D}/tokens.parquet')")
c.sql(f"create view sq as select * from read_parquet('{D}/sequences.parquet')")
c.sql("create table seqs as select sample_id, sum(n_trades) nt, sum(buy_usd) bu, sum(sell_usd) su from sq group by 1")
c.sql("create table s1 as select sample_id, token_address, captured_at::timestamptz cap, time_since_launch_sec tsl from tkall")
r=c.sql("""create table cmp as select s.sample_id, s.token_address, s.cap, s.tsl, q.nt, q.bu, q.su,
  count(tr.ts) n, coalesce(sum(tr.amount_usd) filter (tr.side='buy'),0) tbu, coalesce(sum(tr.amount_usd) filter (tr.side='sell'),0) tsu,
  count(*) filter (tr.ts>= s.cap - s.tsl*interval 1 second - interval 60 second and tr.ts<=s.cap) n_win
 from s1 s join seqs q using(sample_id) left join tr on tr.token_address=s.token_address and tr.ts<=s.cap and tr.ts>=s.cap - (s.tsl+120)*interval 1 second
 group by all""")
print(c.sql("select count(*), quantile_cont(n/nullif(nt,0),[.05,.1,.25,.5,.75,.9]) ,quantile_cont(tbu/nullif(bu,0),[.05,.1,.25,.5,.75,.9]), quantile_cont(tsu/nullif(su,0),[.05,.1,.25,.5,.75,.9]) from cmp where nt>0"))
print(c.sql("select (n/nullif(nt,0))>=0.98 full_cov, count(*), sum(nt) from cmp where nt>0 group by 1"))
print(c.sql("select quantile_cont(nt,[.1,.5,.9,.99]), max(nt) from cmp"))
print(c.sql("select width_bucket(nt,[50,100,200,500,1000]) b, count(*), median(n/nullif(nt,0)) from cmp where nt>0 group by 1 order by 1"))
# non-tk tokens
print(c.sql("""select count(distinct token_address), count(*), sum(amount_usd) from tr where token_address not in (select token_address from tkall)"""))
print(c.sql("""select n, count(*) from (select token_address,count(*) n from tr where token_address not in (select token_address from tkall) group by 1) where n<=12 group by 1 order by 1"""))
print(c.sql("""select count(distinct wallet), count(*) from tr where token_address not in (select token_address from tkall)"""))
print(c.sql("""select count(distinct wallet) from tr where token_address in (select token_address from tkall)"""))
