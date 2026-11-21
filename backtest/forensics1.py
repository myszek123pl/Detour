import sys, numpy as np, pandas as pd
D=sys.argv[1]
t=pd.read_parquet(f"{D}/tokens.parquet")
pd.set_option('display.width',200)
print(len(t), t.token_address.nunique())
t['lm']=t.liquidity_usd/t.market_cap_usd
t['pm']=t.price_at_capture*1e9/t.market_cap_usd
print(t[['lm','pm','time_since_launch_sec','market_cap_usd','liquidity_usd','holder_count','volume_h24']].describe(percentiles=[.05,.25,.5,.75,.95]).round(3).T)
print('lm>0.6',(t.lm>.6).mean(), 'lm>1',(t.lm>1).mean())
print('pm quantiles',t.pm.quantile([.01,.05,.25,.5,.75,.95,.99]).round(3).tolist())
t['lmb']=pd.cut(t.lm,[0,.1,.2,.3,.4,.5,.6,.8,1,2,1e9])
t['tsl_h']=t.time_since_launch_sec/3600
g=t.groupby('lmb',observed=True).agg(n=('lm','size'),tsl_h=('tsl_h','median'),mc=('market_cap_usd','median'),liq=('liquidity_usd','median'),hold=('holder_count','median'),v24=('volume_h24','median'),pc1=('price_change_1h','median'),mr1=('max_return_1h','median'),mr24=('max_return_24h','median'),has_lab=('max_return_1h',lambda x:x.notna().mean()),mkts=('number_markets','mean'))
print(g.round(3))
# multi snapshots
c=t.groupby('token_address').size();print('snapshots per token',c.value_counts().sort_index().head(8).to_dict())
m=t[t.token_address.isin(c[c>1].index)].sort_values(['token_address','captured_at'])
m['dt']=m.groupby('token_address').captured_at.diff().dt.total_seconds()
m['dtsl']=m.groupby('token_address').time_since_launch_sec.diff()
print('dt vs dtsl corr',m[['dt','dtsl']].corr().iloc[0,1], (m.dt-m.dtsl).abs().describe().round(1).to_dict())
for f in ['liquidity_usd','market_cap_usd','holder_count','volume_h24','price_change_1h','lm']:
    m['d_'+f]=m.groupby('token_address')[f].diff()
    print(f,'frac changed',round((m['d_'+f].dropna()!=0).mean(),3),'median rel change',round((m['d_'+f]/m.groupby('token_address')[f].shift()).abs().median(),3))
# first vs later snapshot lm
m['rank']=m.groupby('token_address').cumcount()
print(m.groupby(m['rank'].clip(upper=4))[['lm','tsl_h','liquidity_usd','market_cap_usd']].median().round(3))
print('price*1e9/mc by lmb'); print(t.groupby('lmb',observed=True).pm.median().round(3))
print('number_markets',t.number_markets.value_counts().head().to_dict())
print('corr lm with time', t[['lm','tsl_h']].corr(method='spearman').iloc[0,1])
