import sys, numpy as np, pandas as pd
D=sys.argv[1]
t=pd.read_parquet(f"{D}/tokens.parquet")
t['lm']=t.liquidity_usd/t.market_cap_usd; t['pm']=t.price_at_capture*1e9/t.market_cap_usd
print('pm exact(0.99-1.01):',t.pm.between(.99,1.01).mean(), 'pm<0.99',(t.pm<.99).mean(),'pm>1.01',(t.pm>1.01).mean())
print(t.loc[~t.pm.between(.99,1.01),['price_at_capture','market_cap_usd','pm','lm']].describe().round(4))
# pool_pct vs lm/2
print('pool_pct stats',t.pool_pct.describe().round(3).to_dict())
x=t[['pool_pct','lm']].dropna();print('spearman pool_pct~lm',x.corr(method='spearman').iloc[0,1])
x2=x[x.lm<3];print(x2.groupby(pd.cut(x2.lm,[0,.2,.4,.6,.8,1,1.5,3])).pool_pct.median().round(3))
# lm by mcap bucket
t['mcb']=pd.qcut(t.market_cap_usd,10,duplicates='drop')
print(t.groupby('mcb',observed=True).agg(lm=('lm','median'),liq=('liquidity_usd','median'),n=('lm','size')).round(3))
# liquidity stability: liquidity per token across snapshots vs mcap
m=t.sort_values(['token_address','captured_at']);g=m.groupby('token_address')
m['liq0']=g.liquidity_usd.transform('first');m['mc0']=g.market_cap_usd.transform('first');m['n']=g.liquidity_usd.transform('size')
mm=m[m.n>1]
print('multi-snap: corr(log dliq, log dmc)',np.corrcoef(np.log(mm.liquidity_usd/mm.liq0).replace([np.inf,-np.inf],np.nan).fillna(0),np.log(mm.market_cap_usd/mm.mc0).replace([np.inf,-np.inf],np.nan).fillna(0))[0,1])
# time since launch
print(t.time_since_launch_sec.describe(percentiles=[.1,.25,.5,.75,.9]).round(0).to_dict())
t['tb']=pd.cut(t.time_since_launch_sec,[-1,120,300,900,1800,3600,6*3600,1e9])
print(t.groupby('tb',observed=True).agg(n=('lm','size'),lm=('lm','median'),lm06=('lm',lambda x:(x>.6).mean()),mc=('market_cap_usd','median'),liq=('liquidity_usd','median')).round(3))
# ohlcv price vs snapshot
o=pd.read_parquet(f"{D}/ohlcv.parquet")
t['cap_ts']=t.captured_at.astype('int64')//10**9
print('ohlcv ts range',o.ts.min(),o.ts.max(), 'tokens with candles',o.token_address.nunique())
f=o.sort_values('ts').groupby('token_address').first()
tt=t.merge(f[['ts','open','close']],left_on='token_address',right_index=True,how='inner')
tt['gap']=tt.ts-tt.cap_ts
print('first candle ts - cap_ts',tt.gap.describe(percentiles=[.05,.25,.5,.75,.95]).round(0).to_dict())
tt['ro']=tt.open/ tt.price_at_capture; tt['rom']=tt.open/tt.market_cap_usd
print('open/price',tt.ro.quantile([.05,.25,.5,.75,.95]).round(4).tolist(),'open/mcap',tt.rom.quantile([.05,.25,.5,.75,.95]).round(4).tolist())
