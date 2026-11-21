import sys, numpy as np, pandas as pd
pd.set_option('display.width',250)
d=pd.read_csv(sys.argv[1]); print(len(d))
m=d.multiple
print(m.describe(percentiles=[.05,.1,.25,.5,.75,.9,.95,.99]).round(3).to_dict())
for x in (1,1.1,1.25,1.5,2,3,5,10,20,50,100): print(f'P(multiple>={x})={np.mean(m>=x):.4f}',end='; ')
print('\nmean winsor50',np.minimum(m,50).mean().round(3),'; mean multiple cap 20', np.minimum(m,20).mean().round(3))
print('multiple==1 (price_15 was the best):',np.mean(m<=1.0001).round(3))
d['buyshare']=d.buy_vol_15/(d.buy_vol_15+d.sell_vol_15)
d['dump']=np.where(d.sell_vol_15>d.buy_vol_15,'sells>buys','buys>=sells')
d['vq']=pd.qcut(d.vol_15,5,labels=False); d['gq']=pd.qcut(d.growth_15,5,labels=False,duplicates='drop'); d['bq']=pd.qcut(d.buyshare,5,labels=False)
d['pq']=pd.qcut(d.price_15,5,labels=False)
for c in ('vq','gq','bq','pq','launch_bucket'):
    g=d.groupby(c).multiple.agg(n='size',med='median',p75=lambda s:s.quantile(.75),p90=lambda s:s.quantile(.9),P2x=lambda s:(s>=2).mean(),P5x=lambda s:(s>=5).mean(),P10x=lambda s:(s>=10).mean(),wmean=lambda s:np.minimum(s,50).mean())
    print('\nby',c); print(g.round(3))
print('\nbuyshare quantile cut edges',np.quantile(d.buyshare,[0,.2,.4,.6,.8,1]).round(3),'growth15 edges',np.quantile(d.growth_15,[0,.2,.4,.6,.8,1]).round(3),'vol15',np.quantile(d.vol_15,[0,.2,.4,.6,.8,1]).round(0),'price15',np.quantile(d.price_15,[0,.2,.4,.6,.8,1]))
print(d.groupby('dump').multiple.agg(n='size',med='median',P2x=lambda s:(s>=2).mean(),P5x=lambda s:(s>=5).mean()).round(3))
# mcap at entry
d['mc']=d.price_15*1e9
print(d.groupby(pd.cut(d.mc,[0,2e4,3e4,5e4,1e5,2e5,1e9])).multiple.agg(n='size',med='median',P2x=lambda s:(s>=2).mean(),P5x=lambda s:(s>=5).mean(),P10x=lambda s:(s>=10).mean()).round(3))
