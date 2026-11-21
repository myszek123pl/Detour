import duckdb, numpy as np, pandas as pd
W = "/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/w/w.db"
c = duckdb.connect(W, read_only=True)
pd.set_option('display.width',250); pd.set_option('display.max_columns',50)
b=c.sql("select * from bars where high<=close*10 and open>0 and close>0 order by tok, ts").df()
b['prev_ts']=b.groupby('tok').ts.shift(1); b['prev_close']=b.groupby('tok').close.shift(1)
b['cons']=(b.ts-b.prev_ts)==900
b['r_oc']=np.log(b.close/b.open)
b['r_cc']=np.where(b.cons,np.log(b.close/b.prev_close),np.nan)
b['net']=b.b-b.s; b['gross']=b.b+b.s
b['imb']=np.where(b.gross>0,b.net/b.gross,np.nan)
b['cov']=b.gross/b.vol
b['x']=b.net/b.liq   # net flow as fraction of liquidity
b['lb']=pd.cut(b.liq,[0,5e3,1.5e4,4e4,1e5,1e12],labels=['<5k','5-15k','15-40k','40-100k','>100k'])
def ols(y,X,cl):
    m=np.isfinite(y)&np.all(np.isfinite(X),1); y=y[m];X=X[m];cl=pd.factorize(cl[m])[0]
    XtXi=np.linalg.inv(X.T@X); beta=XtXi@X.T@y; e=y-X@beta
    S=np.zeros((X.shape[1],)*2); sc=np.zeros((cl.max()+1,X.shape[1])); np.add.at(sc,cl,X*e[:,None])
    V=XtXi@(sc.T@sc)@XtXi; se=np.sqrt(np.diag(V)); r2=1-e.var()/y.var()
    return beta,se,r2,m.sum(),len(np.unique(cl))
def wz(v,p=.01): lo,hi=np.nanquantile(v,[p,1-p]); return np.clip(v,lo,hi)
print('bars with trade flow',(b.gross>0).sum(),' tokens',b[b.gross>0].tok.nunique(),' cov median',b['cov'][b.gross>0].median())
g=b[(b.gross>0)&(b.vol>10)].copy()
print('A) contemporaneous r_oc ~ a + beta*imb  (imb=(B-S)/(B+S), same bar)')
rows=[]
for name,sub in [('all',g)]+[(l,g[g.lb==l]) for l in g.lb.cat.categories]:
    y=wz(sub.r_oc.values); X=np.c_[np.ones(len(sub)),sub.imb.values]
    be,se,r2,n,nt=ols(y,X,sub.tok.values)
    # kyle form
    X2=np.c_[np.ones(len(sub)),wz(sub.x.values)]
    be2,se2,r22,_,_=ols(y,X2,sub.tok.values)
    sm=sub[np.abs(sub.x)<.05]; be3,se3,r23,n3,_=ols(wz(sm.r_oc.values),np.c_[np.ones(len(sm)),sm.x.values],sm.tok.values)
    rows.append([name,n,nt,be[1],se[1],r2,be2[1],se2[1],r22,be3[1],se3[1],n3,sub.liq.median()])
print(pd.DataFrame(rows,columns=['bucket','bars','tokens','b_imb','se','R2','lambda_x(ret per 1.0 netflow/liq)','se','R2','lambda_small(|x|<5%)','se','n_small','med_liq']).round(3).to_string())
# B) nonlinearity: deciles of x (all, signed)
gg=g.dropna(subset=['x']).copy()
gg['xb']=pd.qcut(gg.x,10,duplicates='drop')
print(gg.groupby('xb',observed=True).agg(n=('r_oc','size'),x_mean=('x','mean'),ret_mean=('r_oc','mean'),ret_med=('r_oc','median')).round(4).to_string())
# C) predictive: r_cc(t+1) on imb_t, r_cc_t (consecutive bars only)
b['r_next']=b.groupby('tok').r_cc.shift(-1); b['imb_t']=b.imb; 
b['next_cons']=b.groupby('tok').cons.shift(-1)
p=b[(b.gross>0)&(b.next_cons==True)&b.r_next.notna()&(b.vol>10)].copy()
print('C) predictive r_{t+1} ~ imb_t (+ r_t): bars',len(p))
rows=[]
for name,sub in [('all',p)]+[(l,p[p.lb==l]) for l in p.lb.cat.categories]:
    y=wz(sub.r_next.values)
    be,se,r2,n,nt=ols(y,np.c_[np.ones(len(sub)),sub.imb.values],sub.tok.values)
    be2,se2,r22,_,_=ols(y,np.c_[np.ones(len(sub)),sub.imb.values,wz(sub.r_cc.fillna(0).values)],sub.tok.values)
    rows.append([name,n,nt,be[1],se[1],r2,be2[1],se2[1],be2[2],se2[2]])
print(pd.DataFrame(rows,columns=['bucket','bars','tokens','b_imb_next','se','R2','b_imb|r_t','se','b_r_t','se']).round(4).to_string())
# D) ACF within tokens, consecutive bars, bootstrap by token
def acf(col,lags=(1,2,3,4),minn=1):
    out=[]
    d=b[['tok','ts',col]].dropna().copy()
    d[col]=wz(d[col].values,.005) if col in('r_oc','r_cc','x') else d[col]
    d['z']=d[col]-d.groupby('tok')[col].transform('mean')
    d['i']=(d.ts//900).astype(int)
    for L in lags:
        m=d.merge(d[['tok','i','z']].assign(i=lambda q:q.i-L),on=['tok','i'],suffixes=('','_L'))
        agg=m.assign(zz=m.z*m.z_L,a=m.z**2,bq=m.z_L**2).groupby('tok')[['zz','a','bq']].sum()
        r=agg.zz.sum()/np.sqrt(agg.a.sum()*agg.bq.sum())
        rng=np.random.default_rng(0); idx=np.arange(len(agg)); bs=[]
        v=agg.values
        for _ in range(200):
            s=v[rng.choice(idx,len(idx))].sum(0); bs.append(s[0]/np.sqrt(s[1]*s[2]))
        out.append((L,len(m),r,np.quantile(bs,.025),np.quantile(bs,.975)))
    return out
b['logvol']=np.log1p(b.vol)
b['imb_']=b.imb
for col in ['r_oc','imb_','x','logvol']:
    print('ACF',col,[(L,n,round(r,3),round(lo,3),round(hi,3)) for L,n,r,lo,hi in acf(col)])
# return ACF by liquidity bucket (lag1)
bb=b.copy()
for l in b.lb.cat.categories:
    sub=bb[bb.lb==l]
    d=sub[['tok','ts','r_oc']].dropna(); d['r_oc']=wz(d.r_oc.values,.005); d['z']=d.r_oc-d.groupby('tok').r_oc.transform('mean'); d['i']=(d.ts//900).astype(int)
    m=d.merge(d[['tok','i','z']].assign(i=lambda q:q.i-1),on=['tok','i'],suffixes=('','_L'))
    print('r ACF1',l,len(m),round((m.z*m.z_L).sum()/np.sqrt((m.z**2).sum()*(m.z_L**2).sum()),3))
print('mean bar return (close/open) all',b.r_oc.mean(),' median',b.r_oc.median(),' frac up',(b.r_oc>0).mean())
