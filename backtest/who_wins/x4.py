import sys, numpy as np, pandas as pd
D="/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/datasets/solana-memecoin-dataset/repo/data"
o=pd.read_parquet(f"{D}/ohlcv.parquet").sort_values(["token_address","ts"])
o["pc"]=o.groupby("token_address").close.shift(1)
o["r"]=o.open/o.pc
for th in [5,10,20,50,100]:
    bad=o[(o.r>th)|(o.r<1/th)]
    print(th, len(bad), bad.token_address.nunique())
# also consecutive candle gaps > 1 candle
bad=o[(o.r>20)|(o.r<1/20)]; print(bad[["ts","pc","open","r"]].head(10))
