import sys, numpy as np, pandas as pd
D=sys.argv[1]
pd.set_option('display.width',220)
R=pd.read_parquet("out/sim_results.parquet"); R=R[R.peak_mult<1000].copy()
o=pd.read_parquet(f"{D}/ohlcv.parquet").sort_values(['token_address','ts'])
o['high']=np.where(o.high>o.close*10,np.maximum(o.open,o.close),o.high)
paths={k:g[['ts','open','high','low','close']].to_numpy() for k,g in o.groupby('token_address')}
R['lm']=R.liquidity_usd/R.market_cap_usd; R['cap_ts']=R.captured_at.astype('int64')//10**9
ent=[];prev=[];pm=[];fut=[]
for r in R.itertuples():
    p=paths[r.token_address]; i=np.searchsorted(p[:,0],r.cap_ts)
    ent.append(p[i,1]); prev.append(p[i-1,4] if i>0 and r.cap_ts-p[i-1,0]<1800 else np.nan)
    pm.append(p[i,0]-r.cap_ts)
R['entry']=ent;R['prevclose']=prev;R['delay']=pm
R['e_over_snap']=R.entry/R.price_at_capture; R['prev_over_snap']=R.prevclose/R.price_at_capture
R['e_over_mc']=R.entry/(R.market_cap_usd/1e9)
R['hi']=R.lm>.6
print(len(R),R.hi.mean())
R['lmb']=pd.cut(R.lm,[0,.2,.4,.6,.8,1,2,1e9])
g=R.groupby('lmb',observed=True).agg(n=('lm','size'),e_over_snap_med=('e_over_snap','median'),e_snap_p10=('e_over_snap',lambda x:x.quantile(.1)),e_snap_p90=('e_over_snap',lambda x:x.quantile(.9)),prev_over_snap=('prev_over_snap','median'),delay=('delay','median'),peak_med=('peak_mult','median'),p2x=('peak_mult',lambda x:(x>=2).mean()),final_med=('final_mult','median'),entry_med=('entry','median'),mc=('market_cap_usd','median'))
print(g.round(3))
FEE,TIP=0.0125,0.30
def net(df,s,pos=200,liq=None):
    L=(df.liquidity_usd if liq is None else liq).clip(lower=1)
    imp=(2*pos/L).clip(upper=.9)
    return df[s]*(1-FEE-imp)**2-TIP*(1+df[s+'_n'])/pos-1
for s in ['hold_24h','ladder_B','tight_D','runner_F']:
    print(s, 'gross mean by lmb', R.groupby('lmb',observed=True)[s].mean().round(3).tolist(), 'net', R.assign(x=net(R,s)).groupby('lmb',observed=True).x.mean().round(3).tolist())
R.to_parquet('/tmp/x/R.parquet')
