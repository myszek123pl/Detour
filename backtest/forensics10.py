import sys, numpy as np, pandas as pd
D=sys.argv[1]
pd.set_option('display.width',250)
R=pd.read_parquet('/tmp/x/R.parquet')
o=pd.read_parquet(f"{D}/ohlcv.parquet")
st=o.groupby('token_address').agg(nc=('ts','size'),t1=('ts','max'))
R=R.merge(st,left_on='token_address',right_index=True)
R['span_h']=(R.t1-R.cap_ts)/3600
R['lab_fin']=R.close_return_1h; 
R['lmg']=pd.cut(R.lm,[0,.6,1e9],labels=['lm<=.6','lm>.6'])
print(R.groupby('lmg',observed=True).agg(n=('nc','size'),nc=('nc','median'),span_med=('span_h','median'),span_lt1h=('span_h',lambda x:(x<1).mean()),span_ge24=('span_h',lambda x:(x>=23).mean()),
  lab_max1h=('max_return_1h','median'),cand_peak=('peak_mult','median'),lab_close1h=('close_return_1h','median'),cand_final=('final_mult','median'),
  lab_max24=('max_return_24h','median'),lab_staged=('staged_exit_return','median')).round(3).to_string())
# compare labels with candle sim: for rows w/ span>=1h
x=R[R.span_h>=1.1]
print('rows span>=1.1h',len(x),'corr(label max_return_1h, candle peak)',x[['max_return_1h','peak_mult']].corr(method='spearman').iloc[0,1])
# truncation: label says max_return_24h vs candle peak when series short
sh=R[R.span_h<1]
print('short series: label max24 med',sh.max_return_24h.median(),'cand peak med',sh.peak_mult.median(),' label close_1h med',sh.close_return_1h.median(),'cand final',sh.final_mult.median())
print('share short-series with label close_return_1h<0.5 (crash hidden):',(sh.close_return_1h<.5).mean())
print('share short with label max_return_24h > cand peak*1.5:',(sh.max_return_24h>sh.peak_mult*1.5).mean())
# the filtered set
C=((R.mint_disabled==1)&(R.freeze_disabled==1)&(R.top10_holder_pct.fillna(1)<.3)&(R.dev_remaining_pct.fillna(0)<.05)&(R.bundler_pct_holders.fillna(0)<.15)&(R.insider_pct_holders.fillna(0)<.15)&(R.liquidity_usd>=1e4))
S=R[C&(R.lm>.6)]
print(S[['span_h','nc','max_return_1h','peak_mult','close_return_1h','final_mult','max_return_24h','max_return_3d']].describe().round(2).to_string())
print('S: label close_return_1h median',S.close_return_1h.median(),'frac close1h<0.7',(S.close_return_1h<.7).mean(),' nan',S.close_return_1h.isna().mean())
# does candle series end because trading ended? last candle time vs trades: use trades cheaply?
