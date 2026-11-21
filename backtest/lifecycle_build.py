# Build 15m price panel per token (first detection snapshot), glitch-clipped, forward-filled.
import sys, numpy as np, pandas as pd
D=sys.argv[1]; OUT=sys.argv[2]
t=pd.read_parquet(D+'/tokens.parquet'); o=pd.read_parquet(D+'/ohlcv.parquet')
o=o.sort_values(['token_address','ts']).reset_index(drop=True)
nbad=(o.high>10*o.close).sum()
body_hi=np.maximum(o.open,o.close); body_lo=np.minimum(o.open,o.close)
o['high']=np.where(o.high>10*o.close, body_hi, o.high)
nlow=(o.low<body_lo/10).sum()
o['low']=np.where(o.low<body_lo/10, body_lo, o.low)
print('glitch highs clipped',nbad,'lows clipped',nlow, 'rows',len(o))
# close glitch check: close/open ratio extremes
r=(o.close/o.open); print('close/open extremes',r.quantile([0,.0005,.9995,1]).to_dict())
tsmax=o.ts.max(); N=288  # 72h
first=t.sort_values('captured_at').drop_duplicates('token_address').set_index('token_address')
g=o.groupby('token_address')
t0=g.ts.min()
P=np.full((len(t0),N+1),np.nan); H=np.full_like(P,np.nan); L=np.full_like(P,np.nan); V=np.zeros_like(P)
toks=t0.index.values; idx={k:i for i,k in enumerate(toks)}
ti=o.token_address.map(idx).values; k=((o.ts.values-t0.values[ti])//900).astype(int)
m=(k>=0)&(k<=N)
ti,k,oo=ti[m],k[m],o[m]
# if duplicate (token,k) keep last
P[ti,k]=oo.close.values; H[ti,k]=oo.high.values; L[ti,k]=oo.low.values; V[ti,k]=oo.volume.values
O0=np.full(len(toks),np.nan); fo=o.groupby('token_address').open.first(); O0=fo.reindex(toks).values
last=g.ts.max().reindex(toks).values
np.savez_compressed(OUT,P=P,H=H,L=L,V=V,O0=O0,t0=t0.values,last=last,toks=toks,tsmax=tsmax,
  cap_age=first.reindex(toks).time_since_launch_sec.values, mcap=first.reindex(toks).market_cap_usd.values,
  liq=first.reindex(toks).liquidity_usd.values)
print(len(toks),'tokens; fully observed 72h:',(t0.values+N*900<=tsmax).sum())
