import pandas as pd, numpy as np, warnings, itertools; warnings.filterwarnings('ignore')
from sklearn.metrics import roc_auc_score
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.inspection import permutation_importance
B='/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/w27/'
d=pd.read_pickle(B+'A2.pkl')
feats=['dev_remaining_pct','top10_holder_pct','insider_pct_holders','bundler_pct_holders','sniper_count','sniper_pct_holders','cluster_max_pct','fresh_wallet_pct','insider_cluster_size','all_sr','ins_sr','early_sr','early_share','sm_share','ins_share','holder_count','time_since_launch_sec','liquidity_usd','market_cap_usd','smart_money_count','unique_buyers']
for y,sub in [('dump4',d.nb>=2),('y2',d.y2.notna())]:
    x=d[sub].dropna(subset=[y]); tr=x[x.tr]; te=x[~x.tr]
    m=HistGradientBoostingClassifier(max_depth=3,max_iter=60,learning_rate=0.05,random_state=0).fit(tr[feats],tr[y])
    p=m.predict_proba(te[feats])[:,1]
    print(y,'n tr/te',len(tr),len(te),'GBM test AUC',round(roc_auc_score(te[y],p),3),'base',round(te[y].mean(),3))
    # daily AUC
    te=te.assign(p=p); a=[(roc_auc_score(g[y],g.p),len(g)) for k,g in te.groupby('dd') if g[y].nunique()>1 and len(g)>100]
    print('  mean within-day AUC',round(np.average([u for u,_ in a],weights=[w for _,w in a]),3))
    for q in [.9,.95]:
        thr=np.quantile(p,q); f=te.p>=thr; print(f'  top{int((1-q)*100)}% by score: precision {te[y][f].mean():.3f} (base {te[y].mean():.3f}) n={f.sum()}')
    r=permutation_importance(m,te[feats],te[y],n_repeats=1,random_state=0,scoring='roc_auc')
    print('  perm imp:',', '.join(f'{f}:{v:.3f}' for f,v in sorted(zip(feats,r.importances_mean),key=lambda t:-t[1])[:8]))
# single/pair threshold rules for dump4 chosen on train
x=d[d.nb>=2].dropna(subset=['dump4']); tr=x[x.tr]; te=x[~x.tr]
cands={}
for f in ['dev_remaining_pct','top10_holder_pct','insider_pct_holders','bundler_pct_holders','sniper_count','early_sr','all_sr','ins_sr','early_share','cluster_max_pct','fresh_wallet_pct']:
    for q in [.5,.7,.8,.9,.95]:
        t=tr[f].quantile(q)
        if np.isnan(t): continue
        cands[f'{f}>{t:.3g}']=(f,'>',t)
    for q in [.05,.1,.2,.3,.5]:
        t=tr[f].quantile(q); cands[f'{f}<{t:.3g}']=(f,'<',t)
def mask(df,r):
    f,op,t=r; return (df[f]>t) if op=='>' else (df[f]<t)
res=[]
for k,r in cands.items():
    mt=mask(tr,r); me=mask(te,r)
    if mt.sum()<150 or me.sum()<150: continue
    res.append((k,mt.sum(),tr.dump4[mt].mean(),me.sum(),te.dump4[me].mean(),tr.dump4.mean(),te.dump4.mean(),
      te.y2[me].mean() if te.y2.notna().any() else np.nan))
R=pd.DataFrame(res,columns=['rule','n_tr','p_tr','n_te','p_te','base_tr','base_te','y2_te']); R['lift_tr']=R.p_tr/R.base_tr; R['lift_te']=R.p_te/R.base_te
print(R.sort_values('lift_tr',ascending=False).head(12).round(3).to_string())
print(R.sort_values('lift_tr').head(8).round(3).to_string())
