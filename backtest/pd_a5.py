"""Dump speed and pump->dump linkage. python3 -I pd_a5.py <work> <out_md>"""
import sys, numpy as np, pandas as pd
sys.path.insert(0,"/home/user/Detour/backtest"); from pd_md import md
W,OUT=sys.argv[1:3]; out=[]
def emit(t,df):
    out.append(f"\n### {t}\n"); out.append(md(df)); print("\n###",t); print(df.to_string())
M=pd.read_parquet(f"{W}/ev_out.parquet"); G=pd.read_parquet(f"{W}/grid.parquet")
arr={t:(g.o.values,g.h.values,g.l.values,g.c.values,g.v.values) for t,g in G.groupby("tok",sort=False)}
D=M[M.kind=="dump"].copy(); P=M[M.kind=="pump"].copy()
D["depth"]=D.p_peak/D.p0
emit("Dump events: duration (candles from window start to the trigger close) and depth",pd.DataFrame({
 "share of events":D.nsteps.value_counts(normalize=True).sort_index()}).assign(cum=lambda x:x["share of events"].cumsum()))
emit("Dump depth (min close within 3 candles after trigger / start price)",D.depth.describe(percentiles=[.1,.25,.5,.75,.9]).to_frame("depth").T)
# intra-candle speed: single-candle dumps: close/open of trigger candle, low/open
one=D[D.nsteps==1]
emit("Single-candle (<=15 min) dumps",pd.DataFrame({"n":[len(one)],"share":[len(one)/len(D)],"median close/open":[(one.p_trig/one.p0).median()],"share closing <=0.5x":[((one.p_trig/one.p0)<=.5).mean()]}))
# recovery after dump: from trigger close, max close within next 2h relative to p0
Dn=D[D.fw>=8].copy()
rec=[]
for r in Dn.itertuples():
    c=arr[r.tok][3]; rec.append((c[r.i+1:r.i+9].max()/r.p0, c[r.i+8]/r.p_trig-1, c[r.i+8]/r.p0))
Dn[["rec_max","r8","c8_over_p0"]]=np.array(rec)
emit("After a dump (2h): recovery",pd.DataFrame({"share regaining >=80% of pre-dump price within 2h":[(Dn.rec_max>=.8).mean()],"share regaining >=50%":[(Dn.rec_max>=.5).mean()],
   "median return from trigger close to +2h":[Dn.r8.median()],"share further -30% from trigger close within 2h (close)":[(Dn.fmin8<=-.3).mean()],"share ending +2h <=10% of pre-dump price":[(Dn.c8_over_p0<=.1).mean()],"n":[len(Dn)]}))
# pump -> dump linkage: from peak, steps to first close <=0.7*peak close ; and by low
Pn=P[P.fw>=12].copy()
steps=[];stl=[]
for r in Pn.itertuples():
    o,h,l,c,v=arr[r.tok]; k0=r.p
    seg=c[k0+1:k0+13]; hit=np.where(seg<=0.7*r.p_peak)[0]; steps.append(hit[0]+1 if len(hit) else np.nan)
    sl=l[k0:k0+13]; hit=np.where(sl<=0.7*h[k0:k0+13].max()*0+0.7*r.p_peak)[0]; stl.append(hit[0] if len(hit) else np.nan)
Pn["dump_step"]=steps; Pn["dump_step_low"]=stl
d=Pn.dump_step.value_counts(normalize=True,dropna=False).sort_index()
emit(f"Pumps: first candle (15m steps after peak candle) whose CLOSE is <=-30% from the peak close (n={len(Pn)}, 3h window)",pd.DataFrame({"share":d,"cum":d.cumsum()}))
d=Pn.dump_step_low.value_counts(normalize=True,dropna=False).sort_index()
emit("Same with candle LOW (0 = within the peak candle itself)",pd.DataFrame({"share":d,"cum":d.cumsum()}))
emit("Pump->dump linkage",pd.DataFrame({"share of pumps followed by -30% from peak (close) within 1h":[(Pn.dump_step<=4).mean()],"within 3h":[Pn.dump_step.notna().mean()],
  "median minutes peak->-30% (among those)":[15*Pn.dump_step.median()],"n":[len(Pn)]}))
# dumps preceded by pump?
dd=D.copy(); pk=P.groupby("tok")
pp={t:g[["t_start","t_trig","t_peak"]].values for t,g in pk}
def prior_pump(r):
    a=pp.get(r.tok); 
    if a is None: return False
    return bool(((a[:,2]<=r.t_start+900)&(a[:,2]>=r.t_start-7200)).any())
dd["after_pump_2h"]=[prior_pump(r) for r in dd.itertuples()]
emit("Dumps: share that start within 2h after a pump peak (same token)",pd.DataFrame({"share":[dd.after_pump_2h.mean()],"n":[len(dd)]}))
open(OUT,"w").write("\n".join(out))
