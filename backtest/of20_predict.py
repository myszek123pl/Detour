import duckdb, numpy as np, pandas as pd
from scipy.stats import spearmanr
W = "/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/w/w.db"
c = duckdb.connect(W, read_only=True)
pd.set_option('display.width',250)
d=c.sql("""with k as (select token_address tok, arg_min(epoch(captured_at),captured_at) cap, arg_min(liquidity_usd,captured_at) liq, arg_min(max_return_1h,captured_at) cr1, arg_min(max_return_1h,captured_at) mr1, arg_min(sample_id,captured_at) sid from tk group by 1)
select k.*, 
 sum(usd) filter (buy and ts<=cap and ts>cap-300) b5, sum(usd) filter (not buy and ts<=cap and ts>cap-300) s5,
 sum(usd) filter (buy and ts<=cap) bb, sum(usd) filter (not buy and ts<=cap) ss,
 count(*) filter (buy and ts<=cap) nb, count(*) filter (not buy and ts<=cap) ns,
 max(usd) filter (ts<=cap)/sum(usd) filter (ts<=cap) dom
 from k join t using(tok) group by all""").df()
d=d.dropna(subset=['cr1']); d=d.fillna({'b5':0,'s5':0,'bb':0,'ss':0})
d['imb_usd']=(d.bb-d.ss)/(d.bb+d.ss+1e-9); d['imb_n']=(d.nb-d.ns)/(d.nb+d.ns); d['imb5']=(d.b5-d.s5)/(d.b5+d.s5+1e-9)
d['net_liq']=(d.bb-d.ss)/d.liq
print('tokens',len(d),'max_return_1h (optimistic peak, not a fill) mean',d.cr1.mean(),'median',d.cr1.median(),'frac>1',(d.cr1>1).mean())
print('Spearman with max_return_1h (optimistic peak, not a fill) (features from trades <= capture):')
for f in ['imb_usd','imb_n','imb5','net_liq','dom','liq']:
    r,p=spearmanr(d[f],d.cr1,nan_policy='omit'); print(f'  {f:8s} rho={r:+.3f} p={p:.2g}')
d['q']=pd.qcut(d.imb_n,5,duplicates='drop')
print(d.groupby('q',observed=True).agg(n=('cr1','size'),mean=('cr1','mean'),median=('cr1','median'),p_gt1=('cr1',lambda s:(s>1).mean())).round(3))
d['lbk']=pd.cut(d.liq,[0,5e3,1.5e4,4e4,1e12],labels=['<5k','5-15k','15-40k','>40k'])
for l,s in d.groupby('lbk',observed=True):
    r,p=spearmanr(s.imb_n,s.cr1); print(l,len(s),f'rho imb_n={r:+.3f}',f'median cr1={s.cr1.median():.3f}',f'mean={s.cr1.mean():.3f}')
d['dq']=pd.cut(d.dom,[0,.1,.3,.5,.7,1.01])
print(d.groupby('dq',observed=True).agg(n=('cr1','size'),mean=('cr1','mean'),median=('cr1','median')).round(3))
