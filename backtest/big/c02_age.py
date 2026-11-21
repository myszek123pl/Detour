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
d['ageb']=pd.cut(d.age,[0,30,120,300,600,1800,7200,1e9],labels=['<30s','30-120s','2-5m','5-10m','10-30m','30m-2h','>2h'])
pd.set_option('display.width',250)
g=d[d.lv.isin([0.1,0.2,0.3,0.4,0.5])&(d.filled_1==1)]
print(g.groupby(['split','ageb'],observed=True).agg(n=('grad','size'),Pgrad=('grad','mean'),hold=('r_hold_1','mean'),br=('r_br_sl0.7_tp1.25_1','mean'),lad=('r_ladderB_1','mean')).round(3).to_string())
print()
for lat in (1,5,30):
    for sp in ('train','test'):
        h=d[(d.age>600)&(d.lv.isin([0.1,0.2,0.3,0.4,0.5]))&(d[f'filled_{lat}']==1)&(d.split==sp)]
        for e in ('hold','br_sl0.7_tp1.25','ladderB','br_sl0.5_tp2.0','trail0.2_arm1.3'):
            x=h[f'r_{e}_{lat}']; ci=boot_mean(x.values,h.blk.values,1000)
            print(f'lat{lat} {sp} age>600s {e:18s} n={len(x)} mean {fmt_ci(x.mean(),ci)}  median {100*x.median():.1f}  Pgrad {h.grad.mean():.3f}')
print('by level, age>600, lat1, hold & bracket')
for sp in ('train','test'):
    h=d[(d.age>600)&(d.split==sp)&(d.filled_1==1)]
    print(sp, h.groupby('lv').agg(n=('grad','size'),Pgrad=('grad','mean'),hold=('r_hold_1','mean'),br=('r_br_sl0.7_tp1.25_1','mean')).round(3).to_dict('index'))
# concentration: share of total return from top 5 tokens
h=d[(d.age>600)&(d.lv.isin([0.1,0.2,0.3,0.4,0.5]))&(d.filled_1==1)&(d.split=='test')].sort_values('r_hold_1',ascending=False)
print('test n',len(h),'mean',h.r_hold_1.mean().round(3),' mean after dropping top 5:',h.r_hold_1.iloc[5:].mean().round(3),' top-5 returns',h.r_hold_1.iloc[:5].round(2).tolist(), 'unique tokens',h.mid.nunique())
