import sys, numpy as np, pandas as pd
W=sys.argv[1]
pd.set_option("display.width",250); pd.set_option("display.max_columns",60)
M=pd.read_parquet(f"{W}/ev_out.parquet"); F=pd.read_parquet(f"{W}/phase_feats.parquet")
M["eid"]=M.eid.astype(int)
M["cov_pre"]=(M.t_start-M.launch0>=900)                       # at least 15 min of token history before start
M["cov_pump"]=(M.t_start>=M.launch0-60)&(M.t_trig<=M.cap_last)
M["cov_post1"]=M.cov_pump&(M.t_trig+3600<=M.cap_last)
M["cov_post2"]=M.cov_pump&(M.t_trig+7200<=M.cap_last)
for k in ("pump","dump"):
    m=M[M.kind==k]
    print(k,len(m),"cov_pump",m.cov_pump.sum(),"cov_post1",m.cov_post1.sum(),"cov_post2",m.cov_post2.sum(),"pre&pump&post1",(m.cov_pre&m.cov_post1).sum())
nP=F.pivot_table(index="eid",columns="ph",values="n",aggfunc="sum")
m=M[(M.kind=="pump")&M.cov_pump].set_index("eid").join(nP)
print(m[["pre","pump","post1"]].describe().T)
print("pump>=10 trades",(m.pump>=10).sum(),"pump>=10 & post1>=10",((m.pump>=10)&(m.post1>=10)).sum(), "& pre>=10",((m.pump>=10)&(m.post1>=10)&(m.pre>=10)).sum())
print(M[(M.kind=="pump")&M.cov_pump].ts_day.value_counts().sort_index().to_dict())
