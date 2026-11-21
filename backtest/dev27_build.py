import duckdb
B='/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/'
D=B+'datasets/solana-memecoin-dataset/repo/data/'
W=B+'w27/'
c=duckdb.connect()
c.sql(f"create view tr0 as select * from '{D}trades-00*.parquet'")
c.sql(f"""create table tok as select * exclude(rn) from (select *, row_number() over (partition by token_address order by captured_at) rn from '{D}tokens.parquet') where rn=1""")
c.sql(f"create table wl as select address wallet, wallet_type wt from '{D}wallets.parquet'")
# funder cluster id per (wallet): funder with >=2 distinct wallets overall -> group
c.sql(f"""create table fu as select wallet, funder, min(ts) fts from '{D}wallet_funding.parquet' group by 1,2""")
c.sql("""create table fsize as select funder, count(distinct wallet) fn from fu group by 1""")
# trades with token capture time, labels, cluster membership (cluster=(token,funder) with >=2 distinct buyer wallets among funded)
c.sql("""create table t as select tr0.wallet, tr0.token_address tok, tr0.side, tr0.amount_usd usd, epoch(tr0.ts) ts, epoch(tok.captured_at) cap, coalesce(wl.wt,'unk') wt
  from tr0 join tok on tok.token_address=tr0.token_address left join wl on wl.wallet=tr0.wallet""")
c.sql("""create table cl as select distinct b.tok, b.wallet, f.funder from (select distinct tok,wallet from t where side='buy') b join fu f on f.wallet=b.wallet
   join (select tok, funder from (select b2.tok, f2.funder, count(distinct b2.wallet) n from (select distinct tok,wallet from t where side='buy') b2 join fu f2 on f2.wallet=b2.wallet group by 1,2) where n>=2) k on k.tok=b.tok and k.funder=f.funder""")
c.sql("""create table t2 as select t.*, (cl.wallet is not null) incl, cl.funder from t left join cl on cl.tok=t.tok and cl.wallet=t.wallet""")
# rank of buyer by first buy time within token
c.sql("""create table fb as select tok, wallet, min(ts) fts, row_number() over (partition by tok order by min(ts)) rk from t2 where side='buy' group by tok, wallet""")
c.sql("""create table t3 as select t2.*, coalesce(fb.rk,999999) rk, fb.fts as wfirst from t2 left join fb on fb.tok=t2.tok and fb.wallet=t2.wallet""")
c.sql(f"copy t3 to '{W}t3.parquet'")
print(c.sql("select count(*), sum(incl::int), count(distinct tok) from t3").fetchall())
print(c.sql("select count(distinct (tok,funder)) from t3 where incl").fetchall())
