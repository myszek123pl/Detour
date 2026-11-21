import sys, numpy as np, pandas as pd
W=sys.argv[1]
pd.set_option("display.width",250); pd.set_option("display.max_columns",50)
M=pd.read_parquet(f"{W}/ev_out.parquet")
P=M[M.kind=="pump"].copy(); Dm=M[M.kind=="dump"].copy()
print("== counts"); print(M.groupby("kind").agg(n=("eid","size"),tokens=("tok","nunique"),med_mag=("p_peak",lambda s:0)))
P["mag"]=P.p_peak/P.p0; P["trig_mult"]=P.p_trig/P.p0
print(P[["mag","trig_mult","nsteps","fw","age_min"]].describe(percentiles=[.1,.5,.9]).T)
print("steps dist",P.nsteps.value_counts(normalize=True).sort_index().round(3).to_dict())
print("peak after trigger steps",(P.p-P.i).value_counts(normalize=True).sort_index().round(3).to_dict() if 'p' in P else '')
O=P[P.fw>=8].copy()
O["retr"]=(O.fmin8<=0)&False
# retrace: min close within 2h <= 1.05*p0
O["retr"]=(O.p_trig*(1+O.fmin8))<=1.05*O.p0
O["cont"]=(~O.retr)&(O.fmax8>=0.25)
O["cls"]=np.where(O.retr,"full_retrace",np.where(O.cont,"continue","plateau"))
print(len(O),O.cls.value_counts(normalize=True).round(3).to_dict())
print(O.groupby("cls")[["r1","r2","r4","r8","fmax8","fmin8","mag","trig_mult"]].median().round(3))
print("overall r by horizon mean/median"); print(O[["r1","r2","r4","r8","r16"]].agg(["mean","median"]).round(3))
print("share lost >=30% at some close within 1h/2h",(O.fmin4<=-.3).mean(),(O.fmin8<=-.3).mean())
print("share r4<=-.3",(O.r4<=-.3).mean(),"r8<=-.3",(O.r8<=-.3).mean())
