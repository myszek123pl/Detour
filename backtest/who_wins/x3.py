import sys, numpy as np, pandas as pd
sys.path.insert(0,"/home/user/Detour/backtest")
import exec_gap_lib as G
D="/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/datasets/solana-memecoin-dataset/repo/data"
o=pd.read_parquet(f"{D}/ohlcv.parquet")
print("open>high",(o.open>o.high*1.0000001).mean(),"open<low",(o.open<o.low*0.9999999).mean(),"close>high",(o.close>o.high*1.000001).mean(),"close<low",(o.close<o.low*.999999).mean())
print("high>10*close",(o.high>10*o.close).mean(),"low<close/10",(o.low<o.close/10).mean(), "low<open/10",(o.low<o.open/10).mean(), "high>10*open", (o.high>10*o.open).mean())
print((o.open<=0).sum(),(o.low<=0).sum())
t,paths=G.load(D); m,segs=G.build(t,paths)
# outlier k=1
N=len(segs)
import exec_gap_lib as G2
S=G.STRATS["ladder_B"]
k1=np.array([1 if s[1] is not None else 0 for s in segs])
F,M,n,_=G.run_all(segs,k1,dict(stop_mode="exact"),S)
g=(F*M).sum(1)
i=np.argsort(-g)[:5]; print(g[i]); 
for j in i[:2]:
    print(m.index[j], segs[j][0][:3], segs[j][1][:4])
