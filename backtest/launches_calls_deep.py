"""Deep analysis: launches + calls. Usage: python3 -I launches_calls_deep.py <launches_csv> <calls_jsonl> <out_json>"""
import sys, json, numpy as np, pandas as pd, lightgbm as lgb
from sklearn.metrics import roc_auc_score
pd.set_option('display.width',200); pd.set_option('display.max_columns',50)
L=pd.read_csv(sys.argv[1]); C=pd.read_json(sys.argv[2],lines=True); R={}
FEE=(1-.0125)**2
L=L.sort_values('launch_unix').reset_index(drop=True)
L['dt']=pd.to_datetime(L.launch_unix,unit='s'); L['hour']=L.dt.dt.hour; L['dow']=L.dt.dt.dayofweek
L['month']=L.dt.dt.to_period('M').astype(str); L['y']=(L.multiple>=2).astype(int)
L['bs_ratio15']=L.buy_vol_15/(L.sell_vol_15+1); L['buy_share15']=L.buys_15/L.trades_15
L['vol_late']=(L.vol_15-L.vol_10)/(L.vol_10-L.vol_5+1); L['mc15']=L.price_15*1e9
L['bsv']=(L.buy_vol_15-L.sell_vol_15)/L.vol_15
print(len(L),L.dt.min(),L.dt.max()); print(L.groupby('month').agg(n=('y','size'),p2=('y','mean'),med=('multiple','median'),p1=('multiple',lambda s:(s<=1.0001).mean())))
print('multiple quantiles',L.multiple.quantile([.1,.25,.5,.75,.9,.99]).round(2).to_dict())
print('share multiple==1',(L.multiple<=1.0001).mean())
# serial deployers (all-data, descriptive)
dc=L.dev_wallet.value_counts(); print('devs',len(dc),'single',(dc==1).mean(),'launches by devs>=2',(L.dev_wallet.map(dc)>=2).mean(), dc.head(5).to_dict())
# dev history from earlier launches only (expanding, shift)
g=L.groupby('dev_wallet')
L['dev_prev_n']=g.cumcount()
L['dev_prev_hits']=g.y.cumsum()-L.y
L['dev_prev_hit_rate']=np.where(L.dev_prev_n>0,L.dev_prev_hits/L.dev_prev_n.replace(0,np.nan),np.nan)
L['logm']=np.log(L.multiple); L['dev_prev_meanlog']=(g.logm.cumsum()-L.logm)/L.dev_prev_n.replace(0,np.nan)
print(L.groupby(pd.cut(L.dev_prev_n,[-1,0,1,2,4,9,1000])).agg(n=('y','size'),p2=('y','mean'),med=('multiple','median')))
sub=L[L.dev_prev_n>=1]; print('prev-hit-rate buckets (devs with >=1 prior)'); print(sub.groupby(pd.cut(sub.dev_prev_hit_rate,[-.01,0,.25,.5,.99,1])).agg(n=('y','size'),p2=('y','mean')))
print('corr prev hit rate vs y',sub[['dev_prev_hit_rate','y']].corr().iloc[0,1])
print('auc dev_prev_hit_rate (>=1 prior)',roc_auc_score(sub.y,sub.dev_prev_hit_rate), 'meanlog',roc_auc_score(sub.y,sub.dev_prev_meanlog))
# hour/dow
H=L.groupby('hour').agg(n=('y','size'),p2=('y','mean'),med=('multiple','median')); print(H.round(3).T)
D=L.groupby('dow').agg(n=('y','size'),p2=('y','mean')); print(D.round(3).T)
# chi2-ish test for hour
from scipy.stats import chi2_contingency
print('hour chi2 p',chi2_contingency(pd.crosstab(L.hour,L.y))[1],'dow p',chi2_contingency(pd.crosstab(L.dow,L.y))[1])
# hour stability: first half vs second half
mid=L.launch_unix.median(); a=L[L.launch_unix<mid].groupby('hour').y.mean(); b=L[L.launch_unix>=mid].groupby('hour').y.mean(); print('hour corr halves',np.corrcoef(a,b)[0,1])
a=L[L.launch_unix<mid].groupby('dow').y.mean(); b=L[L.launch_unix>=mid].groupby('dow').y.mean(); print('dow corr halves',np.corrcoef(a,b)[0,1])
base=['price_15','vol_5','trades_5','avg_5','buys_5','sells_5','buy_vol_5','sell_vol_5','vol_10','trades_10','avg_10','growth_10','buys_10','sells_10','buy_vol_10','sell_vol_10','vol_15','trades_15','avg_15','growth_15','buys_15','sells_15','buy_vol_15','sell_vol_15','launch_bucket','bs_ratio15','buy_share15','vol_late','bsv']
devf=['dev_prev_n','dev_prev_hit_rate','dev_prev_meanlog']; tf=['hour','dow']
P=dict(n_estimators=200,n_jobs=4,max_bin=63,learning_rate=.03,num_leaves=15,min_child_samples=50,subsample=.8,subsample_freq=1,colsample_bytree=.8,verbose=-1,random_state=0)
def wf(feats,step_days=14,minTrain=21):
    t0=L.launch_unix.min(); step=step_days*86400; out=[]; k=0; imp=np.zeros(len(feats))
    while True:
        s=t0+(minTrain*86400)+k*step; e=s+step
        if s>L.launch_unix.max(): break
        tr=L[L.launch_unix<s]; te=L[(L.launch_unix>=s)&(L.launch_unix<e)]
        k+=1
        if len(te)<200: continue
        m=lgb.LGBMClassifier(**P).fit(tr[feats],tr.y); p=m.predict_proba(te[feats])[:,1]
        imp+=m.booster_.feature_importance('gain'); o=te[['multiple','y','month','launch_unix']].copy(); o['p']=p; o['fold']=k; out.append(o)
    O=pd.concat(out); return O,pd.Series(imp/imp.sum(),index=feats).sort_values(ascending=False)
def ev(s,tp,loss): 
    h=(s.multiple>=tp).mean(); return (h*tp+(1-h)*(1-loss))*FEE-1
for name,f in [('base',base),('all',base+tf+devf)]:
    O,imp=wf(f); R[f'wf_{name}_auc']=round(roc_auc_score(O.y,O.p),4)
    fa=O.groupby('fold').apply(lambda d:roc_auc_score(d.y,d.p)); 
    print('\n==',name,'pooled AUC',R[f'wf_{name}_auc'],'fold AUC min/med/max',fa.min().round(3),fa.median().round(3),fa.max().round(3),'folds',len(fa),'n_test',len(O),'base',O.y.mean().round(3))
    if name in('base','all'): print(imp.head(10).round(3).to_dict())
    for q in (.02,.05,.1,.2):
        # threshold chosen per fold by quantile within fold (no look-ahead)
        sel=O[O.p>=O.groupby('fold').p.transform(lambda x:x.quantile(1-q))]
        print(f' top{int(q*100)}% n={len(sel)} hit2x={sel.y.mean():.3f} hit3x={(sel.multiple>=3).mean():.3f} EV(2x,miss-50)={ev(sel,2,.5):+.3f} EV(2x,-30)={ev(sel,2,.3):+.3f} EV(2x,-70)={ev(sel,2,.7):+.3f}')
        if name=='base' and q==.05: print(sel.groupby('month').agg(n=('y','size'),hit=('y','mean')).round(3).T)
    if name=='base':
        Ob=O; 
        print('monthly AUC',Ob.groupby('month').apply(lambda d:round(roc_auc_score(d.y,d.p),3)).to_dict())
        print('monthly base rate',Ob.groupby('month').y.mean().round(3).to_dict())
# monthly walk-forward (train all prior months, test each month) base
months=sorted(L.month.unique()); print(months)
for mth in months[1:]:
    tr=L[L.month<mth]; te=L[L.month==mth]
    if len(tr)<1000 or len(te)<200: continue
    m=lgb.LGBMClassifier(**P).fit(tr[base],tr.y); p=m.predict_proba(te[base])[:,1]
    s=te[p>=np.quantile(p,.9)]; print('monthly WF',mth,len(tr),len(te),'auc',round(roc_auc_score(te.y,p),3),'base',round(te.y.mean(),3),'top10 hit',round(s.y.mean(),3))
# simple rules (full-sample univariate, then split halves)
print('\nsimple rules: first half vs second half (2x hit rate)')
for nm,cond in [('buy_share15>0.55',L.buy_share15>.55),('buy_share15<0.45',L.buy_share15<.45),('bsv>0.1',L.bsv>.1),('bsv<-0.05',L.bsv<-.05),('growth_15>q75',L.growth_15>L.growth_15.quantile(.75)),('trades_15>q75',L.trades_15>L.trades_15.quantile(.75)),('trades_15<q25',L.trades_15<L.trades_15.quantile(.25)),('mc15<20k',L.mc15<20000),('mc15 20-30k',(L.mc15>=20000)&(L.mc15<30000)),('mc15>=50k',L.mc15>=50000),('avg_15>q75',L.avg_15>L.avg_15.quantile(.75)),('vol_late<1',L.vol_late<1)]:
    h1=L[cond&(L.launch_unix<mid)].y; h2=L[cond&(L.launch_unix>=mid)].y
    print(f' {nm:20s} n={cond.sum():6d} all={L[cond].y.mean():.3f} H1={h1.mean():.3f}(n{len(h1)}) H2={h2.mean():.3f}(n{len(h2)})  base H1={L[L.launch_unix<mid].y.mean():.3f} H2={L[L.launch_unix>=mid].y.mean():.3f}')
print('mc15 buckets'); print(L.groupby(pd.cut(L.mc15,[0,17000,20000,25000,35000,50000,100000,1e9])).agg(n=('y','size'),p2=('y','mean'),p3=('multiple',lambda s:(s>=3).mean()),p1=('multiple',lambda s:(s<=1.0001).mean())).round(3))
print('buy_share quintiles'); print(L.groupby(pd.qcut(L.buy_share15,5)).agg(n=('y','size'),p2=('y','mean')).round(3))
print('trades_15 quintiles'); print(L.groupby(pd.qcut(L.trades_15,5)).agg(n=('y','size'),p2=('y','mean')).round(3))
# multiple distribution: EV of TP at k given hit probability, with loss assumptions + dev-limited
print('\nEV table (all launches, tp, loss) :')
for tp in (1.5,2,3,5):
    print(tp,{f'-{int(l*100)}%':round(ev(L,tp,l),3) for l in (.3,.5,.7,.9)},'hit',round((L.multiple>=tp).mean(),3),'breakeven loss', round(1-((1/FEE-(L.multiple>=tp).mean()*tp)/(1-(L.multiple>=tp).mean())),3))
# serial dev concentration
top=dc.head(20).index; print('top20 devs launches',dc.head(20).sum(),'their p2',L[L.dev_wallet.isin(top)].y.mean())
# ---------- CALLS
C=C.sort_values('t').reset_index(drop=True); C['dt']=pd.to_datetime(C.t,unit='s'); C['month']=C.dt.dt.to_period('M').astype(str); C['hour']=C.dt.dt.hour; C['dow']=C.dt.dt.dayofweek
print('\nCALLS',len(C),C.dt.min(),C.dt.max(),'dup mints',C.mint.duplicated().sum())
print(C.groupby('month').agg(n=('peak','size'),h15=('peak',lambda s:(s>=1.5).mean()),h2=('peak',lambda s:(s>=2).mean()),h3=('peak',lambda s:(s>=3).mean()),h5=('peak',lambda s:(s>=5).mean()),med=('peak','median'),mc=('mc','median'),p1=('peak',lambda s:(s<=1.0001).mean())).round(3))
print('peak quantiles',C.peak.quantile([.05,.1,.25,.5,.75,.9,.99]).round(2).to_dict(),'share peak<=1.0',(C.peak<=1.0001).mean(), 'peak<1.2',(C.peak<1.2).mean())
print(C.groupby(pd.cut(C.mc,[0,5000,8000,12000,20000,35000,60000,1e9])).agg(n=('peak','size'),h15=('peak',lambda s:(s>=1.5).mean()),h2=('peak',lambda s:(s>=2).mean()),h3=('peak',lambda s:(s>=3).mean()),h5=('peak',lambda s:(s>=5).mean()),med=('peak','median')).round(3))
print(C.groupby(C.hour//4*4).agg(n=('peak','size'),h2=('peak',lambda s:(s>=2).mean()),med=('peak','median')).round(3).T)
print(C.groupby('hour').agg(h2=('peak',lambda s:(s>=2).mean())).round(3).T)
print(C.groupby('dow').agg(n=('peak','size'),h2=('peak',lambda s:(s>=2).mean())).round(3).T)
print('hour chi2 p',chi2_contingency(pd.crosstab(C.hour,C.peak>=2))[1])
cm=C.t.median(); a=C[C.t<cm].groupby('hour').peak.apply(lambda s:(s>=2).mean()); b=C[C.t>=cm].groupby('hour').peak.apply(lambda s:(s>=2).mean()); print('call hour corr halves',np.corrcoef(a,b)[0,1])
C['gap']=C.t.diff(); print('calls per day',len(C)/((C.t.max()-C.t.min())/86400),'median gap s',C.gap.median())
print('mc vs peak spearman',C[['mc','peak']].corr('spearman').iloc[0,1])
# mc buckets stability across months
print(C.assign(b=pd.cut(C.mc,[0,8000,15000,30000,1e9],labels=['<8k','8-15k','15-30k','>30k'])).pivot_table(index='month',columns='b',values='peak',aggfunc=lambda s:(s>=2).mean(),observed=True).round(3))
print('EV table calls; TP k, loss assumption, also with extra entry latency slippage s (entry worse by factor)')
for tp in (1.5,2,3,5):
    for l in (.3,.5,.7,.9):
        h=(C.peak>=tp).mean(); print(tp,l,round((h*tp+(1-h)*(1-l))*FEE-1,3),end=' | ')
    print(' hit',round((C.peak>=tp).mean(),3),'breakeven loss',round(1-((1/FEE-(C.peak>=tp).mean()*tp)/(1-(C.peak>=tp).mean())),3))
print('latency: if entry price is d higher than mc, TP at k from mc requires peak/(1+d) ...')
for d in (0,.2,.5):
    for tp in (2,3):
        # effective: needs peak>=tp*(1+d) to get tp over entry... report hit of reaching entry*tp
        h=(C.peak>=tp*(1+d)).mean(); print(f'delay +{int(d*100)}% tp{tp}x_over_entry hit={h:.3f} EV(-50)={(h*tp+(1-h)*.5)*FEE-1:+.3f} EV(-70)={(h*tp+(1-h)*.3)*FEE-1:+.3f}')
# monthly EV tp2 loss50
print('monthly EV tp2/-50%:',{m:round(((d.peak>=2).mean()*2+(1-(d.peak>=2).mean())*.5)*FEE-1,3) for m,d in C.groupby('month')})
# Bootstrap CI of hit2x
rng=np.random.default_rng(0); bs=[(C.peak.values[rng.integers(0,len(C),len(C))]>=2).mean() for _ in range(300)]; print('calls hit2x CI',np.percentile(bs,[2.5,97.5]).round(3))
# overlap mints between datasets
print('mint overlap',len(set(C.mint)&set(L.token)))
ov=C[C.mint.isin(set(L.token))].merge(L[['token','mc15','multiple','launch_unix']],left_on='mint',right_on='token'); print(len(ov)); 
if len(ov): print(ov[['mc','mc15','peak','multiple']].describe().round(2)); print('call t - launch s',(ov.t-ov.launch_unix).describe().round(0))
