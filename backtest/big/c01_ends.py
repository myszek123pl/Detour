import sys, os, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from simlib import *
S=sys.argv[1]
import datetime as dt_
def ep(s): return dt_.datetime.fromisoformat(s).replace(tzinfo=dt_.timezone.utc).timestamp()
tk,df,pg=load(S,mayhem=False,tmin=ep('2026-07-04T12:00:00'),tmax=ep('2026-07-12T15:00:00'))
P=Paths(tk,df,pg)
rows=[]
for m in P.rng:
    d=P.tok(m); 
    if len(d['t'])<2: continue
    prog=(d['vs']-30)/85
    if prog.max()<0.5: continue
    r=dict(mid=m,grad=int(d['grad']),mxp=prog.max(),lastp=prog[-1],reached_done=int(prog.max()>=0.995),
           gap_last=(d['G']-d['t'][-1]) if d['grad'] else np.nan, age_last=d['t'][-1]-d['L'], n=len(prog),
           minafter=prog[np.argmax(prog):].min())
    rows.append(r)
r=pd.DataFrame(rows)
print('tokens reaching >=50%:',len(r))
print(pd.crosstab(r.grad, r.reached_done))
x=r[(r.mxp>=0.7)&(r.mxp<0.995)]
print('reached 0.7-0.995:',len(x),' flagged grad:',x.grad.sum())
print('non-grad: lastp quantiles',x[x.grad==0].lastp.quantile([.1,.25,.5,.75,.9]).round(2).tolist())
print('non-grad: share with lastp>=0.9',(x[x.grad==0].lastp>=0.9).mean().round(3), ' lastp<0.5:',(x[x.grad==0].lastp<0.5).mean().round(3))
y=x[x.grad==1]; print('flagged grad but path max<.995: n',len(y),' gap_last (G - last trade) quantiles',y.gap_last.quantile([.1,.5,.9]).round(1).tolist(), 'mxp quantiles',y.mxp.quantile([.1,.5,.9]).round(3).tolist())
z=r[(r.grad==1)]; print('graduated tokens with >=50%: path reaches done',z.reached_done.mean().round(3))
