import numpy as np, pandas as pd
pd.set_option('display.width',220)
d=pd.read_parquet('/tmp/x/trcmp.parquet')
d['lm']=d.liquidity_usd/d.market_cap_usd
d['pre_net']=d.pre_buy-d.pre_sell
d['pre_vol']=d.pre_buy+d.pre_sell
print('pre_n',d.pre_n.describe(percentiles=[.1,.5,.9]).round(1).to_dict())
for a,b in [('liquidity_usd','pre_buy'),('liquidity_usd','pre_vol'),('liquidity_usd','pre_net'),('buy_usd_1h','h1_buy'),('sell_usd_1h','h1_sell'),('buy_usd_1h','f1_buy'),('sell_usd_1h','f1_sell'),('buy_total','pre_buy'),('net_flow_usd','pre_net'),('volume_h24','pre_vol'),('liquidity_usd','f1_buy')]:
    x=d[[a,b]].dropna(); x=x[(x[a]>0)&(x[b]>0)]
    r=(x[b]/x[a])
    print(f"{a:14s} vs {b:9s} n={len(x):6d} spearman={x.corr(method='spearman').iloc[0,1]:.3f} median ratio={r.median():.3f} p10={r.quantile(.1):.3f} p90={r.quantile(.9):.3f}")
# liquidity vs net buy by time-since-launch
d['lmb']=pd.cut(d.lm,[0,.4,.6,1,1e9],labels=['<.4','.4-.6','.6-1','>1'])
g=d.groupby('lmb',observed=True).agg(n=('lm','size'),liq=('liquidity_usd','median'),pre_buy=('pre_buy','median'),pre_sell=('pre_sell','median'),pre_net=('pre_net','median'),pre_n=('pre_n','median'),h1buy=('h1_buy','median'),f1buy=('f1_buy','median'),f1sell=('f1_sell','median'),sbuy=('buy_usd_1h','median'),ssell=('sell_usd_1h','median'),tsl=('time_since_launch_sec','median'))
print(g.round(1).to_string())
# is the snapshot trade-feature using future trades? compare corr of buy_usd_1h w past vs future windows by lm
for lab,x in d.groupby('lmb',observed=True):
    x=x[(x.buy_usd_1h>0)]
    print(lab,'corr buy_usd_1h~h1_buy %.3f ~f1_buy %.3f'%(x[['buy_usd_1h','h1_buy']].corr(method='spearman').iloc[0,1],x[['buy_usd_1h','f1_buy']].corr(method='spearman').iloc[0,1]))
# fraction of tokens with zero pre trades
print('pre_n==0',(d.pre_n==0).mean(),'pre_n<5',(d.pre_n<5).mean())
