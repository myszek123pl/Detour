import sys, numpy as np, pandas as pd
D=sys.argv[1]
t=pd.read_parquet(f"{D}/tokens.parquet")
o=pd.read_parquet(f"{D}/ohlcv.parquet").sort_values(['token_address','ts'])
t['cap_ts']=t.captured_at.astype('int64')//10**9
t['lm']=t.liquidity_usd/t.market_cap_usd
t=t[(t.price_at_capture>0)]
paths={k:g[['ts','close','open']].to_numpy() for k,g in o.groupby('token_address')}
offs=[-7200,-3600,-1800,-900,0,900,1800,3600,7200,14400]
res={k:[] for k in offs}; keep=[]
for r in t.itertuples():
    p=paths.get(r.token_address)
    if p is None: continue
    row=[]
    for off in offs:
        i=np.searchsorted(p[:,0],r.cap_ts+off)
        if i>=len(p) or abs(p[i,0]-(r.cap_ts+off))>450: row.append(np.nan)
        else: row.append(np.log(p[i,2]/r.price_at_capture) if p[i,2]>0 else np.nan)
    if np.isfinite(row).sum()>=6:
        keep.append((r.sample_id,r.lm,r.time_since_launch_sec)); 
        for k,v in zip(offs,row): res[k].append(v)
K=pd.DataFrame(keep,columns=['sid','lm','tsl']); 
for k in offs: K[f'o{k}']=res[k]
print(len(K))
cols=[f'o{k}' for k in offs]
def summ(d): return pd.Series({'n':len(d),**{c:np.nanmedian(np.abs(d[c])) for c in cols}})
K['grp']=pd.cut(K.lm,[0,.6,1,1e9],labels=['lm<=.6','.6-1','>1'])
print(pd.concat([summ(K).rename('all')]+[summ(g).rename(n) for n,g in K.groupby('grp',observed=True)],axis=1).round(3).T.to_string())
print('median signed log(open_off/snap)'); print(K.groupby('grp',observed=True)[cols].median().round(3).to_string())
