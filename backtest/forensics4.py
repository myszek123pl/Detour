import numpy as np, pandas as pd
R=pd.read_parquet('/tmp/x/R.parquet')
FEE,TIP=0.0125,0.30
def net(df,s,pos=200):
    imp=(2*pos/df.liquidity_usd.clip(lower=1)).clip(upper=.9)
    return df[s]*(1-FEE-imp)**2-TIP*(1+df[s+'_n'])/pos-1
C={'mint+freeze':(R.mint_disabled==1)&(R.freeze_disabled==1),'top10<30':R.top10_holder_pct.fillna(1)<.3,'dev<5':R.dev_remaining_pct.fillna(0)<.05,
'bund<15':R.bundler_pct_holders.fillna(0)<.15,'ins<15':R.insider_pct_holders.fillna(0)<.15,'liq>=10k':R.liquidity_usd>=1e4}
m=np.ones(len(R),bool)
for k,v in C.items(): m&=v.to_numpy()
S=R[m]; print('ALL six n',len(S))
S=S.assign(hi=S.lm>.6)
for s in ['ladder_B','tight_D','runner_F','hold_24h']:
    print(s,S.assign(x=net(S,s)).groupby('hi').x.agg(['size','mean','median']).round(3).to_dict('index'))
print('mint dtype',R.mint_disabled.unique()[:5])
print(S.groupby('hi')[['liquidity_usd','market_cap_usd','lm','time_since_launch_sec','holder_count','peak_mult','final_mult']].median().round(2))
# gross mult w/o liquidity-impact: how much is cost model
for s in ['ladder_B']:
    x0=S[s]*(1-FEE)**2-TIP*(1+S[s+'_n'])/200-1
    print('no-impact net by hi',x0.groupby(S.hi).mean().round(3).to_dict(),'gross-1',(S[s]-1).groupby(S.hi).mean().round(3).to_dict())
