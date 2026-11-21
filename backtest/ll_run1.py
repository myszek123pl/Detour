import sys; sys.path.insert(0,'/home/user/Detour/backtest')
import ll_lib as L, numpy as np, pandas as pd
pd.set_option('display.width',250); pd.set_option('display.max_columns',30); pd.set_option('display.max_rows',300)
m=L.load(); m.to_pickle('/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/ll_m.pkl')
out=[]
def P(t): print(t); out.append(str(t))
# ---- 1 autocorrelation
P('## AUTOCORR (winsorised 1/99 c2c simple returns, age>=2)')
gb=m.groupby('tid')
base=m[m.age>=2]
w=L.wins(base.c2c.dropna(),0.01)
m['rw']=w.reindex(m.index)
rows=[]
for k in (1,2,3,4,6,8,12,16):
    lag=gb.rw.shift(k)
    act=m.active & gb.active.shift(k).fillna(False).astype(bool)
    for nm,msk in [('all',m.rw.notna()&lag.notna()),('active-only',m.rw.notna()&lag.notna()&act),('active|test',m.rw.notna()&lag.notna()&act&m.test),('active|pre',m.rw.notna()&lag.notna()&act&~m.test)]:
        r,lo,hi,n=L.corr_cluster(m.rw[msk].values,lag[msk].values,m.tid[msk].values,B=400)
        rows.append(dict(lag=k,sample=nm,rho=round(r,4),lo=round(lo,4),hi=round(hi,4),n=n))
P(pd.DataFrame(rows).pivot(index='lag',columns='sample',values=['rho','lo','hi','n']).to_string())
# spearman active
rows=[]
for k in (1,2,4,8,16):
    lag=gb.c2c.shift(k); act=m.active & gb.active.shift(k).fillna(False).astype(bool)
    msk=m.c2c.notna()&lag.notna()&act&(m.age>=2)
    x=m.c2c[msk].rank().values; y=lag[msk].rank().values
    r,lo,hi,n=L.corr_cluster(x,y,m.tid[msk].values,B=400)
    rows.append(dict(lag=k,spearman=round(r,4),lo=round(lo,4),hi=round(hi,4),n=n))
P(pd.DataFrame(rows))
# sign persistence
a=m[(m.age>=2)&m.active&gb.active.shift(1).fillna(False).astype(bool)&(m.volume>=1000)]
prev=gb.c2c.shift(1).loc[a.index]
for nm,cond in [('prev>+5%',prev>.05),('prev<-5%',prev<-.05),('prev flat',prev.abs()<=.05)]:
    x=a.c2c[cond]; P((nm,len(x),'mean next',round(x.clip(-1,10).mean(),4),'median',round(x.median(),4),'P(up)',round((x>0).mean(),3)))
# ---- by age
rows=[]
for lo_,hi_ in [(2,4),(4,8),(8,16),(16,48),(48,5000)]:
    msk=(m.age>=lo_)&(m.age<hi_)&m.rw.notna()&gb.rw.shift(1).notna()&m.active&gb.active.shift(1).fillna(False).astype(bool)
    r,lo,hi,n=L.corr_cluster(m.rw[msk].values,gb.rw.shift(1)[msk].values,m.tid[msk].values,B=300)
    rows.append(dict(age=f'{lo_}-{hi_}',rho1=round(r,4),lo=round(lo,4),hi=round(hi,4),n=n))
P(pd.DataFrame(rows))
open('/home/user/Detour/backtest/out/ll_part1.txt','w').write('\n'.join(out))
