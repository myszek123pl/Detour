import duckdb, numpy as np, pandas as pd
from scipy.stats import spearmanr
W = "/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/w/w.db"
c = duckdb.connect(W, read_only=True); pd.set_option('display.width',250)
d=c.sql("""with k as (select token_address tok, min(epoch(captured_at)) cap, arg_min(liquidity_usd,captured_at) liq from tk group by 1),
f as (select tok, sum(usd) filter (buy) bb, sum(usd) filter (not buy) ss, count(*) filter (buy) nb, count(*) filter (not buy) ns,
  max(usd)/sum(usd) dom, sum(usd) filter (ts>cap-300 and buy) b5, sum(usd) filter (ts>cap-300 and not buy) s5 from t join k using(tok) where ts<=cap group by 1),
ob as (select tok, ts, open, close, row_number() over(partition by tok order by ts) rn from (select token_address tok, ts, arg_max(open,volume) open, arg_max(close,volume) close, max(high) hi from oh group by 1,2 having max(high)<=arg_max(close,volume)*10)),
e as (select ob.tok, first(open order by ts) p0, min(ts) t0, last(close order by ts) filter (ts<=(select min(ts) from ob o2 where o2.tok=ob.tok)+3600) p1, count(*) nbar from ob group by 1)
select k.tok, cap, liq, f.*, e.p0, e.p1, e.t0-cap lag from k join f using(tok) join e using(tok)""").df()
d=d[(d.p0>0)&(d.p1>0)]
d['ret']=np.log(d.p1/d.p0)
d['imb_n']=(d.nb-d.ns)/(d.nb+d.ns); d['imb_usd']=(d.bb-d.ss)/(d.bb+d.ss); d['imb5']=(d.b5.fillna(0)-d.s5.fillna(0))/(d.b5.fillna(0)+d.s5.fillna(0)+1e-9)
print('tokens',len(d),'median entry lag after capture (s)',d.lag.median(),' mean ret(1h from first bar open)',d.ret.mean(),'median',d.ret.median(),'frac>0',(d.ret>0).mean())
for f in ['imb_n','imb_usd','imb5','dom','liq']:
    r,p=spearmanr(d[f],d.ret,nan_policy='omit'); print(f'  {f:8s} rho={r:+.3f} p={p:.2g}')
d['q']=pd.qcut(d.imb_usd,5,duplicates='drop')
print(d.groupby('q',observed=True).agg(n=('ret','size'),mean=('ret','mean'),median=('ret','median'),up=('ret',lambda s:(s>0).mean())).round(3))
d['dq']=pd.cut(d.dom,[0,.1,.3,.5,.7,1.01])
print(d.groupby('dq',observed=True).agg(n=('ret','size'),mean=('ret','mean'),median=('ret','median'),up=('ret',lambda s:(s>0).mean())).round(3))
