import sys, numpy as np, pandas as pd
D=sys.argv[1]
pd.set_option('display.width',250); pd.set_option('display.max_columns',40)
R=pd.read_parquet('/tmp/x/R.parquet')
o=pd.read_parquet(f"{D}/ohlcv.parquet").sort_values(['token_address','ts'])
st=o.groupby('token_address').agg(nc=('ts','size'),t0=('ts','min'),t1=('ts','max'),vol=('volume','sum'))
R=R.merge(st,left_on='token_address',right_index=True)
R['span_h']=(R.t1-R.cap_ts)/3600; R['cand_per_h']=R.nc/(R.span_h.clip(lower=.25))
C=((R.mint_disabled==1)&(R.freeze_disabled==1)&(R.top10_holder_pct.fillna(1)<.3)&(R.dev_remaining_pct.fillna(0)<.05)&(R.bundler_pct_holders.fillna(0)<.15)&(R.insider_pct_holders.fillna(0)<.15)&(R.liquidity_usd>=1e4))
S=R[C].copy(); S['hi']=S.lm>.6
print(S.groupby('hi')[['nc','span_h','vol','delay','e_over_snap','time_since_launch_sec','market_cap_usd','liquidity_usd','holder_count','top10_holder_pct','number_markets','pool_pct','price_change_1h','volume_h24','rug_probability']].median().round(3).T)
print(S[S.hi].sort_values('final_mult')[['symbol','captured_at','market_cap_usd','liquidity_usd','lm','entry','price_at_capture','delay','nc','span_h','peak_mult','final_mult','hold_24h','ladder_B']].head(12).to_string())
print(S[S.hi].sort_values('final_mult')[['symbol','captured_at','market_cap_usd','liquidity_usd','lm','entry','price_at_capture','delay','nc','span_h','peak_mult','final_mult','hold_24h','ladder_B']].tail(15).to_string())
print('hi n',S.hi.sum(),'final>1.5:',(S[S.hi].final_mult>1.5).sum(),'share of total gross gain from top5:',
  (S[S.hi].hold_24h-1).nlargest(5).sum()/(S[S.hi].hold_24h-1).sum())
print('captured_at date counts hi:',S[S.hi].captured_at.dt.date.value_counts().sort_index().to_dict())
print('wallet/token dup symbols',S[S.hi].symbol.value_counts().head(5).to_dict())
# selection: candle existence vs lm
