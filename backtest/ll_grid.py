import pandas as pd, numpy as np
P='/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/ll_panel.parquet'
G='/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/ll_grid.parquet'
df=pd.read_parquet(P).sort_values(['token_address','ts'])
df['b']=(df.ts//900)
g=df.groupby('token_address').b
span=(g.max()-g.min()+1)
print('tokens',len(span),'bars',len(df),'grid bars',span.sum(), 'span q',span.quantile([.5,.9,.99,1]).tolist())
tok=df.token_address.astype('category'); df['tid']=tok.cat.codes
# build full grid
first=g.min().reindex(tok.cat.categories).values; n=span.reindex(tok.cat.categories).values
tid=np.repeat(np.arange(len(n)),n); off=np.arange(n.sum())-np.repeat(np.cumsum(n)-n,n)
grid=pd.DataFrame({'tid':tid,'b':first[tid]+off})
m=grid.merge(df.drop(columns=['token_address','ts']),on=['tid','b'],how='left')
m['active']=m.close.notna()
m['close']=m.groupby('tid').close.ffill()
for c in ['volume','bv','sv','bn','sn']: m[c]=m[c].fillna(0)
m['open']=m.open.fillna(m.close); m['high']=m.high.fillna(m.close); m['low']=m.low.fillna(m.close)
m['age']=m.b-m.groupby('tid').b.transform('min')
m['ts']=m.b*900
m['token']=tok.cat.categories[m.tid]
m.drop(columns=['tid']).to_parquet(G)
m['tid']=tid if False else m.tid
print(m.shape, m.active.mean())
