import sys; sys.path.insert(0,'/home/user/Detour/backtest')
import ll_lib as L, numpy as np, pandas as pd, duckdb
pd.set_option('display.width',250); pd.set_option('display.max_columns',30)
D='/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/datasets/solana-memecoin-dataset/repo/data/'
m=pd.read_pickle('/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/ll_m.pkl')
t=duckdb.sql(f"select token_address token, min(epoch(captured_at))::bigint cap, min(time_since_launch_sec) tsl from '{D}tokens.parquet' group by 1").df()
m=m.merge(t,on='token',how='left')
m['rel']=(m.ts-m.cap)/900.0     # bars since detection (bar start)
print(m.rel.describe())
print(m.groupby(pd.cut(m.rel,[-1e5,-4,-1,0,1,4,16,64,1e5])).agg(n=('ts','size'),act=('active','mean'),trade_bars=('tv',lambda s:(s>0).mean())))
ts_=m.active&(m.tv>=1000)&(m.tn>=10)&(m.age>=2)
hi=ts_&(m.bs>=.9)
print('hi events by rel bucket'); print(m[hi].groupby(pd.cut(m.rel[hi],[-1e5,-1,0,1,4,16,1e5])).size())
cols=['rule','h','N','ntok','gross','med','net','n_lo','n_hi','t_n']
rows=[]
for lab,mk in [('hi before capture (rel<0)',hi&(m.rel<0)),('hi at/after capture (rel>=0)',hi&(m.rel>=0)),('hi rel>=1',hi&(m.rel>=1)),('hi rel>=2 (>=30min after)',hi&(m.rel>=2)),('hi rel>=4',hi&(m.rel>=4))]:
    for h in ('l1','l4'): rows.append(L.row(mk,h,m,lab))
print(L.fmt(pd.DataFrame(rows)[cols]).to_string(index=False))
# mean buy share by rel bucket (trade bars)
print(m[ts_].groupby(pd.cut(m.rel[ts_],[-1e5,-1,0,1,4,16,1e5])).bs.agg(['mean','median','size']))
# is the last trade-bar of a token over-represented among hi events?
lt=m[m.tv>0].groupby('tid').b.max(); m['lastt']=m.tid.map(lt)
print('hi events that are last trade bar of token:',(m.b[hi]==m.lastt[hi]).mean(),' vs all ts_ bars:',(m.b[ts_]==m.lastt[ts_]).mean())
print('hi events where next 4 bars have no trades:',(m.lastt[hi]-m.b[hi]<1).mean())
# future trade presence conditional: tv in next bar
gb=m.groupby('tid'); m['tvn']=gb.tv.shift(-1); m['tvp']=gb.tv.shift(1)
print('P(next bar has trade-log trades): hi %.3f vs ts_ %.3f'%((m.tvn[hi]>0).mean(),(m.tvn[ts_]>0).mean()))
print('prev bar tv>0: hi %.3f ts_ %.3f'%((m.tvp[hi]>0).mean(),(m.tvp[ts_]>0).mean()))
# trade-count per wallet uniqueness in hi bars
w=duckdb.sql(f"""select count(distinct wallet) nw, count(*) n from '{D}trades-00*.parquet'""").df(); print(w)
