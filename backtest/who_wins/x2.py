import sys, pickle, time, numpy as np, pandas as pd
sys.path.insert(0,"/home/user/Detour/backtest")
import exec_gap_lib as G
D="/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/datasets/solana-memecoin-dataset/repo/data"
t,paths=G.load(D); t0=time.time()
m,segs=G.build(t,paths); print(len(m), time.time()-t0)
feas=np.array([[s is not None for s in ss] for ss in segs]); print(feas.mean(0), feas.all(1).sum())
pickle.dump((m,segs),open("/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/w/built.pkl","wb"))
# validate vs original
R=pd.read_parquet("/home/user/Detour/backtest/out/sim_results.parquet").set_index("token_address")
k0=np.zeros(len(m),int); t0=time.time()
F,M,ntx,nf=G.run_all(segs,k0,dict(stop_mode="gap"),G.STRATS["ladder_B"]); print("sim time",time.time()-t0)
g=(F*M).sum(1)
print(np.abs(g-R.loc[m.index,"ladder_B"].values).max(), g.mean(), R.ladder_B.mean(), (ntx==R.loc[m.index,"ladder_B_n"].values).mean())
