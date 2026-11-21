import sys, pandas as pd
D=sys.argv[1]
t=pd.read_parquet(f"{D}/tokens.parquet")
print(t.shape); print(list(t.columns))
print(t[['captured_at','time_since_launch_sec','market_cap_usd','liquidity_usd','max_return_1h','max_return_24h','reaches_2x','staged_exit_return','scalp_exit_return','close_return_1h','mdd_from_peak','time_to_peak_sec']].describe(percentiles=[.1,.25,.5,.75,.9,.99]).T.to_string())
print("tokens unique",t.token_address.nunique())
print(t.captured_at.min(), t.captured_at.max())
o=pd.read_parquet(f"{D}/ohlcv.parquet"); print(o.shape, o.head(3).to_string()); print(o.groupby('token_address').size().describe())
