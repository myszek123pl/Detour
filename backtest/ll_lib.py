import numpy as np, pandas as pd
G='/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/ll_grid.parquet'
SPLIT=int(pd.Timestamp('2026-06-24',tz='UTC').timestamp())
COST=0.025
CLIP=10.0   # forward returns winsorised at +1000%
rng=np.random.default_rng(7)
def load():
    m=pd.read_parquet(G).sort_values(['token','b']).reset_index(drop=True)
    m['tid']=pd.factorize(m.token)[0]
    gb=m.groupby('tid')
    m['last_b']=gb.b.transform('max')
    gmax=m.b.max(); m['gmax']=gmax
    m['r_bar']=m.close/m.open-1
    m['c2c']=m.close/gb.close.shift(1)-1
    m['lr']=np.log(m.close/gb.close.shift(1))
    for k in (1,4,16):
        fut=gb.close.shift(-k)
        strict=fut/m.close-1
        # last observed exit
        idx_last=m.groupby('tid').close.transform('last')
        within=(m.b+k)<=m.last_b
        m[f'f{k}']=np.where(within,strict,np.nan)
        lastret=np.where(within,strict,idx_last/m.close-1)
        lastret=np.where((m.b+k)>gmax,np.nan,lastret)   # dataset-end censored
        m[f'l{k}']=lastret
    for c in ['f1','f4','f16','l1','l4','l16']: m[c]=m[c].clip(upper=CLIP)
    vb=gb.volume.transform(lambda s:s.shift(1).rolling(8,min_periods=8).mean())
    m['vbase']=vb; m['vratio']=m.volume/vb.where(vb>0)
    m['lv']=np.log1p(m.volume); m['dlv']=m.lv-gb.lv.shift(1)
    tv=m.bv+m.sv; m['tv']=tv; m['tn']=m.bn+m.sn
    m['bs']=np.where(tv>0,m.bv/tv.where(tv>0),np.nan)
    m['imb']=np.where(tv>0,(m.bv-m.sv)/tv.where(tv>0),np.nan)
    # breakout features: prior 8 bars
    m['pmax']=gb.close.transform(lambda s:s.shift(1).rolling(8,min_periods=8).max())
    m['pmin']=gb.close.transform(lambda s:s.shift(1).rolling(8,min_periods=8).min())
    m['prange']=m.pmax/m.pmin-1
    m['brk']=m.close/m.pmax-1
    m['test']=m.ts>=SPLIT
    return m

def boot_mean(x,tid,B=1500,y=None):
    """cluster (token) bootstrap of mean(x); x NaN-free arrays. returns mean,lo,hi,t,ntok"""
    x=np.asarray(x,float)
    if len(x)<5: return (np.nan,)*4+(0,)
    u,inv=np.unique(tid,return_inverse=True)
    S=np.bincount(inv,x); N=np.bincount(inv).astype(float)
    T=len(u); mean=S.sum()/N.sum()
    W=rng.multinomial(T,np.ones(T)/T,size=B).astype(float)
    bm=(W@S)/(W@N)
    se=bm.std()
    return mean,np.percentile(bm,2.5),np.percentile(bm,97.5),(mean/se if se>0 else np.nan),T

def row(sig,col,m,label,cost=COST):
    """stats for forward-return col over signal mask"""
    d=m.loc[sig&m[col].notna(),[col,'tid']]
    out={'rule':label,'h':col,'N':len(d)}
    if len(d)<5:
        out.update(ntok=0); return out
    x=d[col].values
    mean,lo,hi,t,T=boot_mean(x,d.tid.values)
    nm,nlo,nhi,nt,_=boot_mean(x-cost,d.tid.values)
    out.update(ntok=T,gross=mean,med=np.median(x),win=(x>cost).mean(),g_lo=lo,g_hi=hi,t_g=t,net=nm,n_lo=nlo,n_hi=nhi,t_n=nt)
    return out

def fmt(df):
    d=df.copy()
    for c in d.columns:
        if c in('gross','med','win','g_lo','g_hi','net','n_lo','n_hi'): d[c]=(d[c]*100).round(2)
        elif c in('t_g','t_n'): d[c]=d[c].round(2)
    return d

def corr_cluster(x,y,tid,B=500):
    ok=np.isfinite(x)&np.isfinite(y); x=x[ok];y=y[ok];tid=tid[ok]
    if len(x)<30: return (np.nan,)*3+(0,)
    u,inv=np.unique(tid,return_inverse=True); T=len(u)
    st=np.vstack([np.bincount(inv,v) for v in (x,y,x*x,y*y,x*y,np.ones_like(x))])  # 6 x T
    def c(s):
        sx,sy,sxx,syy,sxy,n=s
        cov=sxy/n-sx*sy/n/n; vx=sxx/n-(sx/n)**2; vy=syy/n-(sy/n)**2
        return cov/np.sqrt(vx*vy)
    r=c(st.sum(1))
    W=rng.multinomial(T,np.ones(T)/T,size=B).astype(float)
    bs=np.array([c(st@w) for w in W])
    return r,np.percentile(bs,2.5),np.percentile(bs,97.5),len(x)

def wins(s,q=0.01):
    lo,hi=s.quantile(q),s.quantile(1-q); return s.clip(lo,hi)
