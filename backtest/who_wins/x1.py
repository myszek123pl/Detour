import numpy as np, pandas as pd
D="/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/datasets/solana-memecoin-dataset/repo/data"
t=pd.read_parquet(f"{D}/tokens.parquet"); o=pd.read_parquet(f"{D}/ohlcv.parquet").sort_values(["token_address","ts"])
t["cap_ts"]=t.captured_at.astype("int64")//10**9
print(t.captured_at.min(), t.captured_at.max(), t.token_address.nunique(), len(t))
print((o.ts%900).value_counts().head())
g=o.groupby("token_address")
n=g.size(); span=(g.ts.max()-g.ts.min())/900+1
print("candles/span ratio median",(n/span).describe())
t1=t.sort_values("cap_ts").drop_duplicates("token_address")
f=g.first(); 
m=t1.merge(f[["ts","open"]],left_on="token_address",right_index=True)
m["lag"]=m.ts-m.cap_ts
print(m.lag.describe(percentiles=[.05,.25,.5,.75,.95]))
m["r"]=m.open/m.price_at_capture
print(m.r.describe(percentiles=[.05,.25,.5,.75,.95]))
print((m.lag<0).mean())
print("L stats"); L=np.minimum(m.liquidity_usd,0.4*m.market_cap_usd); print(L.describe(percentiles=[.05,.1,.25,.5,.75,.9]))
print((m.liquidity_usd>0.4*m.market_cap_usd).mean())
print("time since launch", m.time_since_launch_sec.describe(percentiles=[.1,.5,.9]))
# path length to end
last=g.ts.max(); first=g.ts.min()
print(((last-first)/3600).describe(percentiles=[.1,.25,.5,.75,.9]))
hr=(o.high/o.low); print(hr.describe(percentiles=[.5,.9,.99]))
rng=(o.high/o.open-1); print(rng.describe(percentiles=[.5,.75,.9,.99]))
