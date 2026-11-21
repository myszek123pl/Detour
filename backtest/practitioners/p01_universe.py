"""Build the sampling frame for the Wood/Satsdats backtests (run: python3 -I p01_universe.py).
Frame = graduated pump.fun tokens from memecoin-research backfill/results_*.csv (pair found).
U = uniform random sample (all tokens, dead included); H = high-early-mcap stratum (mc60>=250k) for Satsdats power.
"""
import pandas as pd, numpy as np, json
SP="/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/"
B=SP+"datasets/memecoin-research/repo/data/backfill/"
r=pd.concat([pd.read_csv(B+f"results_{i}.csv") for i in range(4)]).drop_duplicates('mint')
CUT=1794528000-4*86400   # need >= 48h + hold window after graduation
f=r[(r.grad_ts<=CUT)&r.pair.notna()].copy()
print("frame",len(f))
U=f.sample(450,random_state=7).assign(stratum='U')
rest=f.drop(U.index) if False else f[~f.mint.isin(U.mint)]
Hp=rest[rest.mc60>=250000]; print("H pop",len(Hp))
H=Hp.sample(min(600,len(Hp)),random_state=8).assign(stratum='H')
u=pd.concat([U,H]).sample(frac=1,random_state=9) if False else pd.concat([U,H])
u[['mint','symbol','pair','grad_ts','mc5','mc60','twitter','sample','stratum']].to_csv(SP+"universe.csv",index=False)
print(u.stratum.value_counts()); print(pd.to_datetime(u.grad_ts,unit='s').dt.to_period('M').value_counts().sort_index())
