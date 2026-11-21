import pandas as pd, numpy as np
from math import sqrt
df=pd.read_pickle('/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/launch27.pkl')
df['pump']=df.token.str.endswith('pump')
df['lowp']=df.price_15<1e-4
def ci(p,n): return 1.96*sqrt(p*(1-p)/n)
print('price band mix by serial status')
df['ser']=np.where(df.n_total==1,'one-off',np.where(df.n_total<5,'2-4','5+'))
print(pd.crosstab(df.ser,[df.pump,df.lowp],normalize='index').round(3))
for nm,m in [('pump & price<1e-4',df.pump&df.lowp),('all',df.pump|~df.pump)]:
    print('==',nm)
    for k,d in df[m].groupby('ser'):
        n=len(d); print(f'{k:8s} n={n:6d} P2x={d.y2.mean():.3f}±{ci(d.y2.mean(),n):.3f} P5x={d.y5.mean():.3f}±{ci(d.y5.mean(),n):.3f} P10x={d.y10.mean():.4f} medmult={d.multiple.median():.3f} flat(<1.1)={(d.multiple<1.1).mean():.3f}')
# ex-ante n_before bands within pump&lowp
m=df.pump&df.lowp
print('== ex-ante n_before, pump&lowp')
for lo,hi in [(0,0),(1,2),(3,9),(10,10**5)]:
    d=df[m&df.n_before.between(lo,hi)]; n=len(d)
    print(f'nb {lo}-{hi} n={n} P2x={d.y2.mean():.3f}±{ci(d.y2.mean(),n):.3f} P5x={d.y5.mean():.3f} medmult={d.multiple.median():.3f} sell/buy vol15={ (d.sell_vol_15.sum()/d.buy_vol_15.sum()):.3f} trades15 med={d.trades_15.median()}')
# monthly: share of tokens from devs with >=1 prior launch in sample (ex-ante, time-consistent)
df['week']=(df.launch_unix-df.launch_unix.min())//(7*86400)
print(df.groupby('week').apply(lambda d:pd.Series({'n':len(d),'share_repeat_exante':(d.n_before>0).mean(),'p2x':d.y2.mean()})).round(3))
# is serial effect robust: logistic on n_before log + controls, train first 60% test last 40%
from numpy.linalg import lstsq
d=df[m].copy()
d['f1']=np.log1p(d.n_before); d['f2']=d.prior_mean_y2.fillna(d.y2.mean()); d['f3']=np.log1p(d.trades_5); d['f4']=np.log(d.bs_ratio5.clip(.05,50)) if 'bs_ratio5' in d else 0
d['f4']=np.log((d.buy_vol_5/(d.sell_vol_5+1)).clip(.05,50)); d['f5']=np.log1p(d.avg_5)
cut=d.launch_unix.quantile(.6)
X=['f1','f2','f3','f4','f5']
import sys
try:
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import roc_auc_score
    from sklearn.preprocessing import StandardScaler
    for cols in [['f1','f2'],['f3','f4','f5'],X]:
        tr=d[d.launch_unix<cut]; te=d[d.launch_unix>=cut]
        sc=StandardScaler().fit(tr[cols]); lr=LogisticRegression(C=1,max_iter=500).fit(sc.transform(tr[cols]),tr.y2)
        p=lr.predict_proba(sc.transform(te[cols]))[:,1]
        print(cols,'AUC OOS y2=',round(roc_auc_score(te.y2,p),3), dict(zip(cols,lr.coef_[0].round(3))))
except Exception as e: print('sk',e)
