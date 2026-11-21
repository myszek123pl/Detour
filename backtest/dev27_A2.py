import pandas as pd, numpy as np, duckdb, warnings; warnings.filterwarnings('ignore')
from sklearn.metrics import roc_auc_score
from sklearn.linear_model import LogisticRegression
B='/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/'
d=pd.read_pickle(B+'w27/A.pkl')
# ohlcv-based downside label
c=duckdb.connect()
o=c.sql(f"""with oh as (select token_address tok, ts, open, high, low, close from '{B}datasets/solana-memecoin-dataset/repo/data/ohlcv.parquet'),
 j as (select oh.*, t.cap from oh join (select tok, any_value(cap) cap from (select tok, cap from read_parquet('{B}w27/tokfeat.parquet')) group by 1) t on t.tok=oh.tok where oh.ts>=t.cap-900),
 r as (select *, row_number() over (partition by tok order by ts) k from j)
 select tok, count(*) nb, arg_min(open,ts) o0, min(case when k<=4 then low end) low4, arg_max(close,case when k<=4 then ts end) c4, max(case when k<=4 then high end) hi4, arg_max(close,ts) clast, max(high) hall, min(low) lowall from r group by 1""").df()
d=d.merge(o,on='tok',how='left')
d['dd4']=d.low4/d.o0-1; d['end4']=d.c4/d.o0-1; d['dump4']=((d.dd4<=-0.5)).astype(float).where(d.nb>=2)
d['dump_end']=(d.clast/d.o0-1<=-0.7).astype(float).where(d.nb>=2)
print('ohlcv label coverage',d.nb.notna().mean().round(3),'nb>=2',(d.nb>=2).mean().round(3),'dump4 rate',d.dump4.mean().round(3),'dump_end',d.dump_end.mean().round(3))
d['dd']=d.day.dt.strftime('%m-%d')
d['pre']=np.where(d.tr,'train(<06-20)','test(>=06-20)')
feats=['dev_remaining_pct','top10_holder_pct','insider_pct_holders','bundler_pct_holders','bundler_ratio','sniper_count','sniper_pct_holders','cluster_max_pct','cluster_top3_pct','fresh_wallet_pct','insider_cluster_size','insider_net_usd','all_sr','ins_sr','cl_sr','early_sr','early25_sr','early_share','early25_share','sm_share','ins_share']
def dayauc(df,f,y):
    res=[];w=[]
    for k,x in df.groupby('dd'):
        x=x.dropna(subset=[f,y])
        if len(x)>200 and x[y].nunique()>1 and x[y].sum()>=8: res.append(roc_auc_score(x[y],x[f])); w.append(len(x))
    return np.average(res,weights=w) if res else np.nan
rows=[]
for f in feats:
    r=[f]
    for y in ['y2','dump4']:
        for p in [True,False]:
            r.append(dayauc(d[d.tr==p],f,y))
    rows.append(r)
print('\nwithin-day AUC (weighted mean over days)')
print(pd.DataFrame(rows,columns=['feat','y2_tr','y2_te','dump4_tr','dump4_te']).round(3).to_string())
# stratified: dev_remaining bins
print('\ndev_remaining bins: P(y2), P(nopk>5%), P(dump4), n  [train | test]')
def tab(col,bins,labels=None):
    for p,nm in [(True,'train'),(False,'test')]:
        x=d[d.tr==p]; g=x.groupby(pd.cut(x[col],bins,include_lowest=True))
        t=pd.DataFrame({'n':g.size(),'y2':g.y2.mean(),'nopk':g.nopeak.mean(),'dump4':g.dump4.mean(),'n_dump':g.dump4.count(),'rp_mean':g.rp.mean()}); t['lift_y2']=t.y2/x.y2.mean(); print(nm,'base y2',x.y2.mean().round(3),'dump4',x.dump4.mean().round(3)); print(t.round(3).to_string())
tab('dev_remaining_pct',[-.001,0.0,0.01,0.05,0.2,1.0])
print('\nbundler_pct_holders'); tab('bundler_pct_holders',[-.001,0,.1,.3,.5,.7,1.0])
print('\ninsider_pct_holders'); tab('insider_pct_holders',[-.001,0,.1,.3,.5,.7,1.0])
print('\ntop10'); tab('top10_holder_pct',[-.001,.05,.1,.2,.35,.6,1.0])
print('\nsniper_count'); tab('sniper_count',[-1,0,2,6,15,30,500])
print('\nearly_sr (first-10 buyers sell$/buy$ pre-capture)'); d['early_sr_c']=d.early_sr.clip(0,5); tab('early_sr_c',[-.001,0,.05,.2,.5,1,5])
print('\nins_sr'); d['ins_sr_c']=d.ins_sr.clip(0,5); tab('ins_sr_c',[-.001,0,.05,.2,.5,1,5])
d.to_pickle(B+'w27/A2.pkl')
