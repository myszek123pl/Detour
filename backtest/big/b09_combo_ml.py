import sys, os, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from statlib import *
from sklearn.ensemble import HistGradientBoostingRegressor, HistGradientBoostingClassifier
import datetime as dt_
S=sys.argv[1]
def ep(s): return dt_.datetime.fromisoformat(s).replace(tzinfo=dt_.timezone.utc).timestamp()
SPL=ep('2026-07-08T00:00:00'); EMB=ep('2026-07-08T12:00:00'); T0=ep('2026-07-04T12:00:00')
d=pd.read_parquet(f'{S}/work/rules_events.parquet')
d['split']=np.where(d.L<SPL,'train',np.where(d.L>=EMB,'test','embargo'))
d['blk']=block_ids(d.L.values,3.0,T0)
d=d[d.lv.isin([0.1,0.2,0.3,0.4,0.5])&(d.filled_1==1)].copy()
EX=['hold','br_sl0.7_tp1.25','ladderB','br_sl0.5_tp2.0']
def rep(name,m):
    for sp in ('train','test'):
        g=d[m&(d.split==sp)]
        s=f'{name:46s} {sp:5s} n={len(g):5d} Pgrad={g.grad.mean():.3f}'
        for e in EX:
            x=g[f'r_{e}_1']; 
            if len(x)>=30: s+=f' | {e}: {100*x.mean():6.1f} [{100*boot_mean(x.values,g.blk.values,500)[0]:6.1f},{100*boot_mean(x.values,g.blk.values,500)[1]:6.1f}]'
        print(s)
print('--- combined exclusion rule (all prior-work filters) on every level pooled')
excl=(d.dev_pct>=10)|(d.snipers3>=3)|(d.top3_buy>=0.7)|(d.bs_cnt60<0.6)|(d.cr_prev>=5)
rep('ALL',d.age>=0)
rep('keep if NOT(dev>=10|snip3>=3|top3>=.7|bs60<.6|cr>=5)',~excl.fillna(False))
rep('same + age>600s',(~excl.fillna(False))&(d.age>600))
rep('age>600s only',d.age>600)
rep('age>600s & cr_prev==0',(d.age>600)&(d.cr_prev==0))
rep('age>600s & dev<10',(d.age>600)&(d.dev_pct<10))
rep('age>600s & top3_buy<0.7',(d.age>600)&(d.top3_buy<0.7))
rep('age 300-600s',(d.age>300)&(d.age<=600))
rep('age>900s',d.age>900); rep('age>1200s',d.age>1200)
print('--- GBM trained on train only (all features, levels pooled)')
F=['lv','age','n_tr','uniq_buyers','top1_buy','top3_buy','hhi_buy','bs_cnt60','bs_sol60','n60','netflow60','bs_cnt300','n300','bs_cnt_all','snipers3','snipers10','sniper_sol3','cr_sells','cr_sell_sol','cr_buy_sol','dprog60','drawdown_from_peak','speed','dev_pct','cr_prev','cr_prev_grad','snipe_delta','cb','first_gap']
tr=d[d.split=='train']; te=d[d.split=='test']
for tgt in ('grad','r_hold_1','r_br_sl0.7_tp1.25_1','r_ladderB_1'):
    if tgt=='grad': mdl=HistGradientBoostingClassifier(max_depth=3,learning_rate=0.05,max_iter=150,min_samples_leaf=100,random_state=0)
    else: mdl=HistGradientBoostingRegressor(max_depth=3,learning_rate=0.05,max_iter=150,min_samples_leaf=100,random_state=0)
    ytr=tr[tgt].clip(-1,3) if tgt!='grad' else tr[tgt]
    mdl.fit(tr[F],ytr)
    sc=mdl.predict_proba(te[F])[:,1] if tgt=='grad' else mdl.predict(te[F])
    te=te.assign(sc=sc)
    out=f'target {tgt:22s}'
    for q in (0.05,0.10,0.20):
        top=te[te.sc>=te.sc.quantile(1-q)]
        out+=f' | top{int(q*100)}% n={len(top)} Pgrad={top.grad.mean():.3f}'
        for e in ('hold','br_sl0.7_tp1.25'):
            x=top[f'r_{e}_1']; ci=boot_mean(x.values,top.blk.values,500); out+=f' {e}:{100*x.mean():.1f}[{100*ci[0]:.1f},{100*ci[1]:.1f}]'
    print(out)
    if tgt=='grad':
        from sklearn.metrics import roc_auc_score
        print('  AUC test',round(roc_auc_score(te.grad,sc),3))
