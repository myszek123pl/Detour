import numpy as np, pandas as pd
import numpy.linalg as la
pd.set_option('display.width',250)
f=pd.read_parquet('/tmp/x/feat.parquet'); d=pd.read_parquet('/tmp/x/trcmp.parquet')[['sample_id','pre_buy','pre_sell','pre_n','h1_buy','f1_buy','f1_sell','last_pre_ts']]
t=f.merge(d,on='sample_id'); t['pc_fut']=(t.p_p1h/t.p-1)*100; t['pre_net']=t.pre_buy-t.pre_sell
# A: flow-implied pool token share for fresh tokens
fr=t[(t.tsl<300)&(t.pre_n>=20)&(t.mc>0)].copy()
fr['lm_pred']=(2*(0.207-fr.pre_net/fr.mc)).clip(lower=0)
print('fresh tsl<300 n',len(fr),'actual lm quantiles',fr.lm.quantile([.1,.25,.5,.75,.9]).round(2).tolist())
print('lm>1 share',(fr.lm>1).mean().round(3),' of those, share with net buying>0',((fr.pre_net>0)[fr.lm>1]).mean().round(3),' mean pre_net/mc',(fr.pre_net/fr.mc)[fr.lm>1].median().round(2))
print('spearman lm vs lm_pred',fr[['lm','lm_pred']].corr(method='spearman').iloc[0,1].round(3), ' lm vs pre_net/mc', (fr.lm).corr(fr.pre_net/fr.mc,method='spearman').round(3))
# flow-based Q: liq/2 vs net buys USD  (cumulative)
fr['q_ratio']=fr.liq/(2*fr.pre_net.clip(lower=1))
print('liq/(2*net buys) by lm bucket (fresh):'); print(fr.groupby(pd.cut(fr.lm,[0,.4,.6,1,2,1e9]),observed=True).agg(n=('lm','size'),ratio=('q_ratio','median'),liq=('liq','median'),net=('pre_net','median'),mc=('mc','median')).round(2).to_string())
# lm>2 impossible check overall
print('overall: lm>1 %.3f  lm>2 %.3f (lm = 2*pool token share of 1e9 supply => >1 means >50%% supply in pool; >2 impossible)'%((t.lm>1).mean(),(t.lm>2).mean()))
# leakage regression: log liq ~ log pre_buy + log mc + future price change + future buys
x=t.dropna(subset=['pc_fut','pre_buy','liq','mc']); x=x[(x.pre_buy>0)&(x.liq>0)&(x.mc>0)&(x.f1_buy>=0)]
x=x.assign(y=np.log(x.liq),a=np.log(x.pre_buy),b=np.log(x.mc),c=np.log1p(x.pc_fut.clip(-99)/100),e=np.log1p(x.f1_buy),g=np.log1p(x.h1_buy))
X=np.column_stack([np.ones(len(x)),x.a,x.b,x.g,x.c,x.e]); beta,_,_,_=la.lstsq(X,x.y,rcond=None); res=x.y-X@beta
se=np.sqrt(np.diag(la.inv(X.T@X))*res.var())
print('n',len(x));print(pd.DataFrame({'coef':beta,'t':beta/se},index=['const','log pre_buy','log mcap','log last-1h buys','log(1+future 1h ret)','log future 1h buys']).round(3))
print('R2', 1-res.var()/x.y.var())
# future return corr with lm among all (candle-based), spearman
print('spearman lm ~ pc_fut',t[['lm','pc_fut']].dropna().corr(method='spearman').iloc[0,1].round(3), ' liq ~ pc_fut',t[['liq','pc_fut']].dropna().corr(method='spearman').iloc[0,1].round(3),' mc~pc_fut',t[['mc','pc_fut']].dropna().corr(method='spearman').iloc[0,1].round(3))
