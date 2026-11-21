import sys, os, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from statlib import *
import datetime as dt_
S=sys.argv[1]
def ep(s): return dt_.datetime.fromisoformat(s).replace(tzinfo=dt_.timezone.utc).timestamp()
SPL=ep('2026-07-08T00:00:00'); EMB=ep('2026-07-08T12:00:00')
d=pd.read_parquet(f'{S}/work/base_events.parquet')
d['split']=np.where(d.L<SPL,'train',np.where(d.L>=EMB,'test','embargo'))
d['blk']=block_ids(d.L.values, 3.0, ep('2026-07-04T12:00:00'))
print(d.groupby(['split']).mid.nunique())
def row(g, lv, lat):
    n=len(g); f=g[g.filled==1]
    r=dict(lv=lv, lat=lat, split=g.split.iloc[0] if len(g) else '', n_trig=n, fill=len(f)/max(n,1))
    pg=g.grad.mean(); r['P_grad']=fmt_ci(pg, boot_mean(g.grad.values,g.blk.values,400))
    if len(f)>=30:
        for k in (2,5,10):
            r[f'chart>={k}x']=fmt_ci((f.chart_max>=k).mean(), boot_mean((f.chart_max>=k).values.astype(float),f.blk.values,300))
        for k in (2,5):
            r[f'net>={k}x']=fmt_ci((f.net_max>=k).mean(), boot_mean((f.net_max>=k).values.astype(float),f.blk.values,300))
        nl=f.net_last-1
        r['hold_end_net_mean']=fmt_ci(nl.mean(), boot_mean(nl.values,f.blk.values,400))
        r['hold_end_median']=f"{100*nl.median():.1f}"
        r['P_grad|filled']=f"{100*f.grad.mean():.1f}"
    return r
out=[]
for split in ['train','test']:
    for lv in [0.02,0.05,0.10,0.20,0.30,0.40,0.50,0.60,0.70]:
        for lat in [0,1,5,30]:
            g=d[(d.split==split)&(d.lv==lv)&(d.lat==lat)&(d.sz=='200' if lat!=1 else (d.sz=='200'))]
            if len(g)==0: continue
            out.append(row(g,lv,lat))
o=pd.DataFrame(out)
pd.set_option('display.width',250); pd.set_option('display.max_columns',30); pd.set_option('display.max_colwidth',40)
o.to_csv(f'{S}/work/base_report.csv',index=False)
for split in ['train','test']:
    print('=====',split)
    print(o[(o.split==split)&(o.lat.isin([1]))].drop(columns=['split']).to_string(index=False))
print('===== latency effect, test, lv in .10,.30,.50')
print(o[(o.split=='test')&(o.lv.isin([0.1,0.3,0.5]))][['lv','lat','n_trig','fill','P_grad|filled','chart>=2x','net>=2x','hold_end_net_mean','hold_end_median']].to_string(index=False))
