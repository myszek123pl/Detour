import pandas as pd, numpy as np, warnings; warnings.filterwarnings('ignore')
from sklearn.metrics import roc_auc_score
B='/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/w27/'
d=pd.read_parquet(B+'tokfeat.parquet')
d['y2']=d.reaches_2x.astype(float); d['rp']=d.runner_peak_x
d['nopeak']=(d.rp<=1.05).astype(float)  # never traded >5% above capture
d=d[d.reaches_2x.notna()].copy()
d['day']=pd.to_datetime(d.cap,unit='s',utc=True)
cut=pd.Timestamp('2026-06-20',tz='UTC')
d['tr']=d.day<cut
print('N',len(d),'train',d.tr.sum(),'test',(~d.tr).sum(),'base y2 train/test',d[d.tr].y2.mean().round(3),d[~d.tr].y2.mean().round(3),'nopeak',d[d.tr].nopeak.mean().round(3),d[~d.tr].nopeak.mean().round(3))
# ---- supply holdings
print('\n== holdings quantiles')
for c in ['dev_remaining_pct','top10_holder_pct','top_holder_ratio','insider_pct_holders','bundler_pct_holders','bundler_ratio','sniper_pct_holders','cluster_max_pct','cluster_top3_pct','fresh_wallet_pct','rat_position_pct','insider_holding_ratio']:
    print(f'{c:22s}',d[c].quantile([.1,.25,.5,.75,.9,.95]).round(3).values, 'mean',round(d[c].mean(),3))
for thr in [0,.01,.05,.2,.5]:
    print('dev_remaining >',thr, (d.dev_remaining_pct>thr).mean().round(3))
for thr in [.2,.4,.6]:
    print('insider_pct_holders >',thr,(d.insider_pct_holders>thr).mean().round(3),' bundler_pct_holders>',thr,(d.bundler_pct_holders>thr).mean().round(3))
# trade-flow share
for nm in ['ins','sm','cl','early','early25']:
    s=d[f'{nm}_pre_buy']/d.all_pre_buy.replace(0,np.nan)
    sn=(d[f'{nm}_pre_buy']-d[f'{nm}_pre_sell'])/(d.all_pre_buy-d.all_pre_sell).abs().replace(0,np.nan)
    print(nm,'share of window buy$ median/mean/p90',s.median().round(3),s.mean().round(3),s.quantile(.9).round(3),'| n wallets med',d[f'{nm}_n'].median(),'| sell/buy $ ratio med (tokens w/buys)',(d[f'{nm}_pre_sell']/d[f'{nm}_pre_buy'].replace(0,np.nan)).median().round(3))
# ---- cohort sell ratio vs outcomes
d['all_sr']=d.all_pre_sell/d.all_pre_buy.replace(0,np.nan)
for nm in ['ins','sm','cl','early','early25']:
    d[nm+'_sr']=d[f'{nm}_pre_sell']/d[f'{nm}_pre_buy'].replace(0,np.nan)
    d[nm+'_share']=d[f'{nm}_pre_buy']/d.all_pre_buy.replace(0,np.nan)
    d[nm+'_post_sr']=d[f'{nm}_post_sell']/(d[f'{nm}_post_buy']+d[f'{nm}_post_sell']).replace(0,np.nan)
    d[nm+'_netpost']=(d[f'{nm}_post_sell']-d[f'{nm}_post_buy'])
d['dev_hold']=d.dev_remaining_pct
feats=['dev_remaining_pct','top10_holder_pct','insider_pct_holders','bundler_pct_holders','bundler_ratio','sniper_count','sniper_pct_holders','cluster_max_pct','cluster_top3_pct','fresh_wallet_pct','insider_holding_ratio','insider_cluster_size','insider_net_usd','all_sr','ins_sr','sm_sr','cl_sr','early_sr','early25_sr','ins_share','sm_share','cl_share','early_share','early25_share','holder_count','smart_money_count','time_since_launch_sec']
print('\n== univariate AUC (sign as in train) for y2 | nopeak ; train->test')
rows=[]
for f in feats:
    x=d[f]; ok=x.notna()
    r=[]
    for y in ['y2','nopeak']:
        tr=d[d.tr&ok]; te=d[~d.tr&ok]
        if tr[y].nunique()<2 or te[y].nunique()<2: r+= [np.nan,np.nan]; continue
        a=roc_auc_score(tr[y],tr[f]); b=roc_auc_score(te[y],te[f]); r+=[a,b]
    rows.append([f,ok.mean()]+r)
print(pd.DataFrame(rows,columns=['feat','cov','y2_tr','y2_te','nopk_tr','nopk_te']).round(3).to_string())
d.to_pickle(B+'A.pkl')
