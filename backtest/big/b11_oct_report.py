import sys, os, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from statlib import *
from sklearn.ensemble import HistGradientBoostingRegressor, HistGradientBoostingClassifier
import datetime as dt_
S=sys.argv[1]
def ep(s): return dt_.datetime.fromisoformat(s).replace(tzinfo=dt_.timezone.utc).timestamp()
SPL=ep('2026-07-08T00:00:00'); EMB=ep('2026-07-08T12:00:00'); T0=ep('2026-07-04T12:00:00')
j=pd.read_parquet(f'{S}/work/rules_events.parquet'); j['split']=np.where(j.L<SPL,'train',np.where(j.L>=EMB,'test','embargo'))
o=pd.read_parquet(f'{S}/work/rules_events_oct.parquet'); o['blk']=block_ids(o.L.values,3.0,o.L.min())
bo=pd.read_parquet(f'{S}/work/base_events_oct.parquet'); bo['blk']=block_ids(bo.L.values,3.0,bo.L.min())
print('Oct events',len(o),'tokens',o.mid.nunique(),'  cap_launch share',o.cap_launch.mean().round(3))
print('=== Oct base rates (std curve, created in first 14h of Oct-15, lat=1s, $200)')
for lv in [0.05,0.10,0.20,0.30,0.40,0.50,0.60,0.70]:
    g=bo[(bo.lv==lv)&(bo.lat==1)&(bo.sz=='200')]; f=g[g.filled==1]
    if len(g)<30: continue
    ci=boot_mean(g.grad.values.astype(float),g.blk.values,400)
    s=f'lv {lv:.2f} n={len(g):5d} P_grad {fmt_ci(g.grad.mean(),ci)}'
    for k in (2,5,10): s+=f' | chart>={k}x {100*(f.chart_max>=k).mean():.1f}'
    nl=(f.net_last-1); s+=f' | hold mean {fmt_ci(nl.mean(),boot_mean(nl.values,f.blk.values,300))} median {100*nl.median():.1f}'
    print(s)
ex=sorted({c[2:].rsplit('_',1)[0] for c in o.columns if c.startswith('r_')})
print('=== Oct exit-rule grid (all levels x exits), counts of positive means')
for lat in (1,5,30):
    pos=0;tot=0;best=(-9,None)
    for lv in sorted(o.lv.unique()):
        g=o[(o.lv==lv)&(o[f'filled_{lat}']==1)]
        for e in ex:
            m=g[f'r_{e}_{lat}'].mean(); tot+=1; pos+= m>0
            if m>best[0]: best=(m,(lv,e,len(g)))
    print(f'lat {lat}: {pos}/{tot} combos with mean>0; best {best[0]:.3f} at {best[1]}')
print('=== jocry-train winners evaluated on Oct (lat 1)')
for lv,e in [(0.6,'br_sl0.7_tp1.25'),(0.4,'br_sl0.85_tp1.25'),(0.5,'br_sl0.85_tp1.25'),(0.3,'br_sl0.85_tp1.25')]:
    g=o[(o.lv==lv)&(o.filled_1==1)]; x=g[f'r_{e}_1']
    print(f'lv {lv} {e}: n={len(x)} mean {fmt_ci(x.mean(),boot_mean(x.values,g.blk.values,500))} median {100*x.median():.1f}')
oo=o[o.lv.isin([0.1,0.2,0.3,0.4,0.5])&(o.filled_1==1)].copy()
EX=['hold','br_sl0.7_tp1.25','ladderB','br_sl0.5_tp2.0']
def rep(name,m):
    g=oo[m]; s=f'{name:40s} n={len(g):5d} Pgrad={g.grad.mean():.3f}'
    for e in EX:
        x=g[f'r_{e}_1']
        if len(x)>=30:
            ci=boot_mean(x.values,g.blk.values,500); s+=f' | {e}: {100*x.mean():6.1f} [{100*ci[0]:6.1f},{100*ci[1]:6.1f}]'
    print(s)
print('=== Oct: filters selected on jocry-train, applied unchanged')
excl=(oo.dev_pct>=10)|(oo.snipers3>=3)|(oo.top3_buy>=0.7)|(oo.bs_cnt60<0.6)|(oo.cr_prev>=5)
rep('ALL',oo.age>=0); rep('age>600s',oo.age>600); rep('age 300-600s',(oo.age>300)&(oo.age<=600)); rep('age 120-300s',(oo.age>120)&(oo.age<=300)); rep('age<120s',oo.age<=120)
rep('age>900s',oo.age>900)
rep('age>600s & cr_prev==0',(oo.age>600)&(oo.cr_prev==0))
rep('NOT(prior-work exclusions)',~excl.fillna(False)); rep('NOT(excl) & age>600s',(~excl.fillna(False))&(oo.age>600))
rep('dev_pct>=20 (flagged)',oo.dev_pct>=20); rep('dev_pct<10 (kept)',oo.dev_pct<10)
rep('snipers3>=3',oo.snipers3>=3); rep('snipers3<3',oo.snipers3<3); rep('top3_buy>=0.7',oo.top3_buy>=0.7); rep('top3_buy<0.7',oo.top3_buy<0.7)
rep('bs_cnt60<0.6',oo.bs_cnt60<0.6); rep('bs_cnt60>=0.8',oo.bs_cnt60>=0.8); rep('cr_prev>=5',oo.cr_prev>=5); rep('cr_prev==0',oo.cr_prev==0)
print('=== GBM trained on jocry-train only, scored on Oct')
F=['lv','age','n_tr','uniq_buyers','top1_buy','top3_buy','hhi_buy','bs_cnt60','bs_sol60','n60','netflow60','bs_cnt300','n300','bs_cnt_all','snipers3','snipers10','sniper_sol3','cr_sells','cr_sell_sol','cr_buy_sol','dprog60','drawdown_from_peak','speed','dev_pct','cr_prev','cr_prev_grad','snipe_delta','cb','first_gap']
jj=j[j.lv.isin([0.1,0.2,0.3,0.4,0.5])&(j.filled_1==1)&(j.split=='train')]
from sklearn.metrics import roc_auc_score
for tgt in ('grad','r_hold_1'):
    mdl=(HistGradientBoostingClassifier if tgt=='grad' else HistGradientBoostingRegressor)(max_depth=3,learning_rate=0.05,max_iter=150,min_samples_leaf=100,random_state=0)
    mdl.fit(jj[F],jj[tgt].clip(-1,3) if tgt!='grad' else jj[tgt])
    sc=mdl.predict_proba(oo[F])[:,1] if tgt=='grad' else mdl.predict(oo[F]); oo['sc']=sc
    if tgt=='grad': print('  AUC Oct',round(roc_auc_score(oo.grad,sc),3))
    for q in (0.05,0.10,0.20):
        top=oo[oo.sc>=oo.sc.quantile(1-q)]; s=f'{tgt:9s} top{int(q*100)}% n={len(top)} Pgrad={top.grad.mean():.3f}'
        for e in ('hold','br_sl0.7_tp1.25'):
            x=top[f'r_{e}_1']; ci=boot_mean(x.values,top.blk.values,500); s+=f' | {e}: {100*x.mean():.1f} [{100*ci[0]:.1f},{100*ci[1]:.1f}]'
        print(s)
