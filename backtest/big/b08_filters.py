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
print('cap_launch share by lv:',d.groupby('lv').cap_launch.mean().round(2).to_dict())
d=d[d.lv.isin([0.1,0.2,0.3,0.4,0.5])&(d.filled_1==1)].copy()
EX=['hold','br_sl0.7_tp1.25','br_sl0.5_tp2.0','ladderB']
FILT={
 'dev_pct>=5':d.dev_pct>=5,'dev_pct>=10':d.dev_pct>=10,'dev_pct>=20':d.dev_pct>=20,
 'snipers3>=3':d.snipers3>=3,'snipers3>=6':d.snipers3>=6,'snipers10>=10':d.snipers10>=10,
 'top3_buy>=0.5':d.top3_buy>=0.5,'top3_buy>=0.7':d.top3_buy>=0.7,'top3_buy>=0.9':d.top3_buy>=0.9,
 'hhi_buy>=0.2':d.hhi_buy>=0.2,
 'bs_cnt60<0.6':d.bs_cnt60<0.6,'bs_cnt60<0.8':d.bs_cnt60<0.8,'bs_sol60<0.7':d.bs_sol60<0.7,'bs_cnt_all<0.7':d.bs_cnt_all<0.7,
 'cr_prev>=1':d.cr_prev>=1,'cr_prev>=5':d.cr_prev>=5,'cr_prev>=20':d.cr_prev>=20,
 'cr_sells>=1':d.cr_sells>=1,'age<30s':d.age<30,'age<120s':d.age<120,'age>600s':d.age>600,'n60<3':d.n60<3,'n60>=20':d.n60>=20,
 'dd>=0.15':d.drawdown_from_peak>=0.15,'dprog60<0':d.dprog60<0,'dprog60>=0.1':d.dprog60>=0.1,'uniq_buyers<8':d.uniq_buyers<8,'cb':d.cb==1,
}
rows=[]
for sp in ('train','test'):
    g=d[d.split==sp]
    base={e:g[f'r_{e}_1'].mean() for e in EX}; bgrad=g.grad.mean()
    rows.append(dict(split=sp,filter='ALL (no filter)',n_flag=len(g),n_keep=len(g),flag_Pgrad=bgrad,keep_Pgrad=bgrad,**{f'flag_{e}':base[e] for e in EX},**{f'keep_{e}':base[e] for e in EX}))
    for nme,m in FILT.items():
        m=m.fillna(False)
        a=g[m.loc[g.index]]; k=g[~m.loc[g.index]]
        if len(a)<40: continue
        rows.append(dict(split=sp,filter=nme,n_flag=len(a),n_keep=len(k),flag_Pgrad=a.grad.mean(),keep_Pgrad=k.grad.mean(),
            **{f'flag_{e}':a[f'r_{e}_1'].mean() for e in EX},**{f'keep_{e}':k[f'r_{e}_1'].mean() for e in EX}))
r=pd.DataFrame(rows)
pd.set_option('display.width',300); pd.set_option('display.max_columns',40)
for sp in ('train','test'):
    print('=====',sp)
    print(r[r.split==sp].drop(columns='split').round(3).to_string(index=False))
r.to_pickle(f'{S}/work/filters.pkl')
