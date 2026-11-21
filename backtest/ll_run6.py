import sys; sys.path.insert(0,'/home/user/Detour/backtest')
import ll_lib as L, numpy as np, pandas as pd, duckdb
pd.set_option('display.width',250); pd.set_option('display.max_columns',30)
D='/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/datasets/solana-memecoin-dataset/repo/data/'
m=pd.read_pickle('/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/ll_m.pkl')
ts_=m.active&(m.tv>=1000)&(m.tn>=10)&(m.age>=2)
k=m.loc[ts_,['token','b','bs','l1','l4']].copy(); k['hi']=k.bs>=.9
con=duckdb.connect(); con.register('k',k)
con.execute(f"""create table tr as select wallet, token_address token, (epoch(ts)::bigint//900) b, side, amount_usd from '{D}trades-00*.parquet' where token_address in (select token from k)""")
con.execute("create table x as select tr.*, k.hi from tr join k using(token,b)")
print(con.execute("select hi, count(*) n, count(distinct wallet) w from x group by 1").df())
print(con.execute(f"""select hi, w.wallet_type, count(*) n, sum(amount_usd) usd from x left join '{D}wallets.parquet' w on x.wallet=w.address where side='buy' group by 1,2 order by 1,3 desc""").df())
# per hi bar: unique buying wallets, top-wallet share
print(con.execute("""with b as (select token,b,wallet,sum(amount_usd) u from x where hi and side='buy' group by 1,2,3),
 s as (select token,b,count(*) nw, max(u)/sum(u) top, sum(u) tot from b group by 1,2) select count(*), median(nw), avg(nw), median(top), avg(top) from s""").df())
