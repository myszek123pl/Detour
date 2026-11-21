"""Event-count sensitivity to thresholds. python3 -I pd_sens.py <work>"""
import sys, numpy as np, pandas as pd, json
W=sys.argv[1]
G=pd.read_parquet(f"{W}/grid.parquet")
arr={t:(g.o.values,g.c.values,g.v.values) for t,g in G.groupby("tok",sort=False)}
def count(kind,thr,win,minvol):
    n_ev=0; toks=set(); mags=[]
    for t,(o,c,v) in arr.items():
        n=len(o); i=0
        while i<n:
            lo=max(0,i-(win-1))
            if kind=="pump":
                j=lo+int(np.argmin(o[lo:i+1])); hit=c[i]/o[j]>=thr
            else:
                j=lo+int(np.argmax(o[lo:i+1])); hit=c[i]/o[j]<=thr
            if hit and v[j:i+1].sum()>=minvol:
                n_ev+=1; toks.add(t)
                k=i+int(np.argmax(c[i:min(n,i+4)]) if kind=="pump" else np.argmin(c[i:min(n,i+4)])); i=k+1
            else: i+=1
    return n_ev,len(toks)
res=[]
for kind,thrs in (("pump",[1.3,1.5,2.0,3.0]),("dump",[0.8,0.7,0.5,0.3])):
    for thr in thrs:
        for win,mv in ((4,2000),(4,0),(4,10000),(2,2000),(8,2000)):
            e,t=count(kind,thr,win,mv); res.append(dict(kind=kind,thr=thr,win_candles=win,minvol=mv,events=e,tokens=t))
R=pd.DataFrame(res); R.to_csv(f"{W}/sens.csv",index=False); print(R.to_string(index=False))
