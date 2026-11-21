import sys, os, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from statlib import *
import datetime as dt_
S=sys.argv[1]
def ep(s): return dt_.datetime.fromisoformat(s).replace(tzinfo=dt_.timezone.utc).timestamp()
SPL=ep('2026-07-08T00:00:00'); EMB=ep('2026-07-08T12:00:00'); T0=ep('2026-07-04T12:00:00')
d=pd.read_parquet(f'{S}/work/rules_events.parquet')
d['split']=np.where(d.L<SPL,'train',np.where(d.L>=EMB,'test','embargo'))
d['blk']=block_ids(d.L.values,3.0,T0)
ex=sorted({c[2:].rsplit('_',1)[0] for c in d.columns if c.startswith('r_')})
res=[]
for lat in (1,5,30):
    for lv in sorted(d.lv.unique()):
        for e in ex:
            c=f'r_{e}_{lat}'
            row=dict(lat=lat,lv=lv,exit=e)
            for sp in ('train','test'):
                g=d[(d.split==sp)&(d.lv==lv)&(d[f'filled_{lat}']==1)]
                x=g[c].dropna()
                row[f'n_{sp}']=len(x); row[f'mean_{sp}']=x.mean(); row[f'med_{sp}']=x.median(); row[f'win_{sp}']=(x>0).mean()
            res.append(row)
r=pd.DataFrame(res); r.to_pickle(f'{S}/work/grid.pkl')
pd.set_option('display.width',250)
for lat in (1,5,30):
    g=r[r.lat==lat]
    print(f'--- lat {lat}s: {len(g)} combos; mean>0 train: {(g.mean_train>0).sum()}, test: {(g.mean_test>0).sum()}; both: {((g.mean_train>0)&(g.mean_test>0)).sum()}; best test mean {g.mean_test.max():.3f}; corr(train,test) {g[["mean_train","mean_test"]].corr().iloc[0,1]:.2f}')
g=r[(r.lat==1)&(r.n_train>=300)].sort_values('mean_train',ascending=False).head(12)
print(g.round(3).to_string(index=False))
print('hold by level (lat1)'); print(r[(r.lat==1)&(r.exit=='hold')][['lv','n_train','mean_train','mean_test','med_train','med_test']].round(3).to_string(index=False))
