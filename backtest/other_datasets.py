"""Base rates + out-of-sample check on two other public datasets.
Usage: python3 -I other_datasets.py <launches_csv> <calls_jsonl> <out_dir>"""
import sys, json, numpy as np, pandas as pd, lightgbm as lgb
from sklearn.metrics import roc_auc_score
L=pd.read_csv(sys.argv[1]); C=pd.read_json(sys.argv[2],lines=True); OUT=sys.argv[3]; res={}
# --- launches: entry at 15-min price, label = best price in next 5h
print("launches",len(L), L.launch_time.min(), L.launch_time.max())
for k in (1.5,2,3,5,10): res[f"launch_share_ge{k}x"]=round(float((L.multiple>=k).mean()),3)
print({k:v for k,v in res.items()})
L=L.sort_values('launch_unix'); cut=L.launch_unix.quantile(.7)
feats=[c for c in L.columns if c not in('token','dev_wallet','launch_unix','launch_time','best_price_5h','multiple')]
L['bs_ratio15']=L.buy_vol_15/(L.sell_vol_15+1); feats.append('bs_ratio15')
tr,te=L[L.launch_unix<cut],L[L.launch_unix>=cut]
y=lambda d:(d.multiple>=2).astype(int)
m=lgb.LGBMClassifier(n_estimators=300,learning_rate=.03,num_leaves=15,min_child_samples=50,verbose=-1,random_state=0).fit(tr[feats],y(tr))
p=m.predict_proba(te[feats])[:,1]; a=roc_auc_score(y(te),p); res['launch_lgb_test_auc']=round(a,3)
for k in (.05,.1,.2):
    s=te[p>=np.quantile(p,1-k)]; res[f'launch_top{int(k*100)}_share2x']=round(float((s.multiple>=2).mean()),3)
res['launch_test_base_share2x']=round(float((te.multiple>=2).mean()),3)
# TP-only upper bound: sell all at 2x if hit, else assume exit at -X (unknown path) -> bounds
for loss in (0.3,0.5,0.7):
    hit=(te.multiple>=2).mean(); gross=hit*2+(1-hit)*(1-loss); res[f'launch_tp2x_EV_if_miss_-{int(loss*100)}%']=round(float(gross*(1-.0125)**2-1),3)
# --- calls
print("calls",len(C), C.utc.min(), C.utc.max())
for k in (2,3,5,10): res[f'calls_share_ge{k}x']=round(float((C.peak>=k).mean()),3)
res['calls_median_peak']=round(float(C.peak.median()),2)
for tp in (1.5,2,3):
  for loss in (0.3,0.5,0.7):
    hit=(C.peak>=tp).mean(); g=hit*tp+(1-hit)*(1-loss)
    res[f'calls_TP{tp}x_miss-{int(loss*100)}%_EV']=round(float(g*(1-.0125)**2-1),3)
print(json.dumps(res,indent=1)); json.dump(res,open(f"{OUT}/other_datasets.json","w"),indent=1)
