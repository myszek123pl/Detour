"""Base rates: P(graduation), P(2x/5x/10x) from entry at curve-progress levels, with latency + costs (jocry, standard curve tokens).
python3 -I b04_base.py <scratch>"""
import sys, os, numpy as np, pandas as pd, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from simlib import *
S=sys.argv[1]; SRC=sys.argv[2] if len(sys.argv)>2 else 'jocry'
import datetime as dt_
def ep(s): return dt_.datetime.fromisoformat(s).replace(tzinfo=dt_.timezone.utc).timestamp()
T0=ep('2026-07-04T12:00:00'); T1=ep('2026-07-12T15:00:00')
tk,df,pg = load(S, mayhem=False, tmin=(T0 if SRC=='jocry' else None), tmax=(T1 if SRC=='jocry' else None), src=SRC)
P = Paths(tk,df,pg)
print('tokens',len(tk),'with paths',len(P.rng))
LEVELS=[0.02,0.05,0.10,0.20,0.30,0.40,0.50,0.60,0.70]
LATS=[0,1,5,30]
FEE=0.0125; TIP=0.30/SOLUSD
SIZES={'200':200/SOLUSD,'50':50/SOLUSD}
rows=[]; t0=time.time()
for n,(m,(s,e)) in enumerate(P.rng.items()):
    d=P.tok(m); t=d['t']
    if len(t)<2: continue
    prog=np.clip((d['vs']-VS0)/85.0,0,1.2)
    mxp=prog.max()
    for lv in LEVELS:
        if mxp<lv: break
        i=int(np.argmax(prog>=lv))
        if i==0 and prog[0]>lv+0.03: continue
        for lat in LATS:
            for sz,X in SIZES.items():
                if sz=='50' and lat not in (1,): continue
                en=entry(d,i,lat,X,FEE,TIP)
                rec=dict(mid=m,L=d['L'],lv=lv,lat=lat,sz=sz,grad=int(d['grad']),age=t[i]-d['L'],prog_i=prog[i],i=i,nst=len(t),filled=int(en is not None))
                if en is not None:
                    j=en['j']
                    net,mid_mult=liquidation_curve(d,en,FEE,TIP)
                    # chart multiple relative to mid at fill (others' state only)
                    mid_f=d['vs'][j]/d['vt'][j]
                    chart=(d['vs'][j:]/d['vt'][j:])/mid_f
                    cm=chart.max(); nm=net.max()
                    if d['grad']: cm=max(cm,P_GRAD/mid_f); nm=max(nm, (pool_exit(en['y'],1.0,POOL_FEE,TIP)+0)/en['cost'])
                    rec.update(vs_fill=en['vs0'],chart_max=cm,net_max=nm,net_last=(net[-1] if not d['grad'] else pool_exit(en['y'],pool_ratio(P,m,lat),POOL_FEE,TIP)/en['cost']),
                               chart_last=chart[-1],ttpeak=(t[j+int(np.argmax(chart))]-t[j]))
                rows.append(rec)
    if n%20000==0: print(n,len(rows),round(time.time()-t0))
out=pd.DataFrame(rows); out.to_parquet(f'{S}/work/base_events'+('' if SRC=='jocry' else '_'+SRC)+'.parquet')
print(out.shape, round(time.time()-t0))
