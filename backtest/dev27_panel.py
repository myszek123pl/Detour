import duckdb
B='/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/'
W=B+'w27/'; D=B+'datasets/solana-memecoin-dataset/repo/data/'
c=duckdb.connect()
c.sql(f"create view t as select * from '{W}t3.parquet'")
c.sql(f"create view oh as select token_address tok, ts bts, open, high, low, close, volume vol from '{D}ohlcv.parquet'")
c.sql("""create table tb as select tok, cast(floor(ts/900) as bigint)*900 bts,
 sum(case when side='buy' then usd else 0 end) all_b, sum(case when side='sell' then usd else 0 end) all_s,
 sum(case when side='buy' and wt='insider' then usd else 0 end) ins_b, sum(case when side='sell' and wt='insider' then usd else 0 end) ins_s,
 sum(case when side='buy' and wt='smart_money' then usd else 0 end) sm_b, sum(case when side='sell' and wt='smart_money' then usd else 0 end) sm_s,
 sum(case when side='buy' and incl then usd else 0 end) cl_b, sum(case when side='sell' and incl then usd else 0 end) cl_s,
 sum(case when side='buy' and rk<=10 then usd else 0 end) e_b, sum(case when side='sell' and rk<=10 then usd else 0 end) e_s,
 count(*) ntr
 from t group by 1,2""")
c.sql("""create table pan as select oh.*, tb.* exclude(tok,bts) from oh left join tb using(tok,bts)""")
c.sql(f"copy pan to '{W}panel.parquet'")
print(c.sql("select count(*), count(ntr), sum(vol), sum(all_b+all_s), count(distinct tok) from pan").fetchall())
print(c.sql("select count(*) filter (where ntr>0), count(distinct tok) filter(where ntr>0) from pan").fetchall())
