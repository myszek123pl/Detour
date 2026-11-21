import sys; sys.path.insert(0,'/home/user/Detour/backtest')
import ll_lib as L, numpy as np, pandas as pd
m=pd.read_pickle('/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/ll_m.pkl')
gb=m.groupby('tid')
ts_=m.active&(m.tv>=1000)&(m.tn>=10)&(m.age>=2); hi=ts_&(m.bs>=.9); b8=ts_&(m.bs>=.8)
m['o1']=gb.open.shift(-1); m['c1']=gb.close.shift(-1); m['c4']=gb.close.shift(-4); m['c2']=gb.close.shift(-2); m['c3']=gb.close.shift(-3)
m['gap']=m.o1/m.close-1
out=[]
def rep(lab,x,tid,costs=(.025,.05,.075)):
    ok=np.isfinite(x); x=np.clip(x[ok],-1,10); t=tid[ok]
    s=lab+f' N={len(x)} gross {x.mean()*100:.2f} med {np.median(x)*100:.2f}'
    for c in costs:
        mu,lo,hi_,tt,_=L.boot_mean(x-c,t); s+=f' | cost{c*100:.1f}: net {mu*100:.2f} [{lo*100:.2f},{hi_*100:.2f}] t={tt:.2f}'
    print(s,flush=True)
for nm,sg in [('bs>=.9',hi),('bs>=.8',b8)]:
    d=m[sg]; print(nm,'gap open_{t+1}/close_t: mean %.2f%% median %.2f%% p90 %.2f%%'%(d.gap.mean()*100,d.gap.median()*100,d.gap.quantile(.9)*100))
    rep(nm+' close_t->close_t+1',(d.c1/d.close-1).values,d.tid.values)
    rep(nm+' open_t+1->close_t+1',(d.c1/d.o1-1).values,d.tid.values)
    rep(nm+' open_t+1->close_t+4',(d.c4/d.o1-1).values,d.tid.values)
    rep(nm+' close_t+1->close_t+2 (1-bar latency)',(d.c2/d.c1-1).values,d.tid.values)
    rep(nm+' close_t+1->close_t+4 (1-bar latency)',(d.c4/d.c1-1).values,d.tid.values)
    rep(nm+' open_t+1->close_t+4 TEST only',(d.c4/d.o1-1)[d.test].values,d.tid[d.test].values)
    rep(nm+' open_t+1->close_t+1 TEST only',(d.c1/d.o1-1)[d.test].values,d.tid[d.test].values)
# placebo: shuffle bs within token among ts_ bars
rng=np.random.default_rng(1); res=[]
d=m[ts_].copy()
for i in range(300):
    d['bsp']=d.groupby('tid').bs.transform(lambda s:rng.permutation(s.values))
    x=d.l1[(d.bsp>=.9)].clip(upper=10).dropna(); res.append(x.mean()-L.COST)
res=np.array(res); print('placebo (shuffle bs within token) l1 net mean: mean %.2f%% sd %.2f%% 97.5pct %.2f%% ; actual %.2f%%'%(res.mean()*100,res.std()*100,np.percentile(res,97.5)*100,(m.l1[hi].clip(upper=10).mean()-L.COST)*100))
# is it concentrated in a few days?
d=m[hi].copy(); d['day']=pd.to_datetime(d.ts,unit='s').dt.date
print(d.groupby('day').agg(n=('l1','size'),l1=('l1',lambda s:s.clip(upper=10).mean()*100),l4=('l4',lambda s:s.clip(upper=10).mean()*100)).round(1).T.to_string())
