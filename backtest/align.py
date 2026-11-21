import sys, pandas as pd, numpy as np
D=sys.argv[1]
t=pd.read_parquet(f"{D}/tokens.parquet"); o=pd.read_parquet(f"{D}/ohlcv.parquet")
print("reaches_2x mean",t.reaches_2x.mean(), t.reaches_2x.value_counts(dropna=False).to_dict())
print("max_return_24h >0 share",(t.max_return_24h>0).mean(), "runner_peak_x desc", t.runner_peak_x.describe().to_dict())
t['cap_ts']=t.captured_at.astype('int64')//10**9
g=o.groupby('token_address')
first=g.ts.min(); last=g.ts.max()
m=t[t.token_address.isin(first.index)].copy()
m['first_ts']=m.token_address.map(first); m['last_ts']=m.token_address.map(last)
m['lag']=m.first_ts-m.cap_ts
print("snapshots w/ ohlcv",len(m),"tokens",m.token_address.nunique())
print("lag first candle - capture (s):",m.lag.describe(percentiles=[.05,.25,.5,.75,.95]).to_dict())
print("span (h):",((m.last_ts-m.first_ts)/3600).describe().to_dict())
# price check: candle containing capture
o=o.sort_values(['token_address','ts'])
res=[]
for tok,grp in list(o.groupby('token_address'))[:3000]:
    s=m[m.token_address==tok]
    for _,r in s.iterrows():
        c=grp[(grp.ts<=r.cap_ts)&(grp.ts+900>r.cap_ts)]
        if len(c): res.append(r.price_at_capture/c.iloc[0].open)
res=np.array(res); print("price_at_capture / candle open ratio n",len(res), np.percentile(res,[5,25,50,75,95]))
