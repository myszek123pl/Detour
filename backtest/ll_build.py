import duckdb, sys
D='/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/datasets/solana-memecoin-dataset/repo/data/'
O='/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/ll_panel.parquet'
con=duckdb.connect()
con.execute(f"""
copy (
with raw as (select distinct * from '{D}ohlcv.parquet'),
o as (select * from raw where high<=10*close and low>0 and open>0 and close>0
      qualify count(*) over (partition by token_address,ts)=1),
t as (select token_address, (epoch(ts)::bigint//900)*900 as b,
  sum(case when side='buy' then amount_usd else 0 end) bv,
  sum(case when side='sell' then amount_usd else 0 end) sv,
  sum(case when side='buy' then 1 else 0 end) bn,
  sum(case when side='sell' then 1 else 0 end) sn
  from '{D}trades-00*.parquet' where token_address in (select distinct token_address from o)
  group by 1,2)
select o.*, coalesce(bv,0) bv, coalesce(sv,0) sv, coalesce(bn,0) bn, coalesce(sn,0) sn
from o left join t on o.token_address=t.token_address and o.ts=t.b
order by o.token_address,o.ts) to '{O}' (format parquet)""")
print(con.execute(f"select count(*), sum((bv+sv)>0), avg(case when bv+sv>0 then (bv+sv)/volume end), median(case when bv+sv>0 then (bv+sv)/volume end) from '{O}'").fetchall())
