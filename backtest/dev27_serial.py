import duckdb, pandas as pd, numpy as np, hashlib
P='/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/datasets/solana-pumpfun-launches/repo/solana_launches_public.csv'
df=pd.read_csv(P).sort_values('launch_unix').reset_index(drop=True)
print(len(df), df.dev_wallet.nunique(), df.token.nunique())
vc=df.dev_wallet.value_counts()
print(vc.describe()); 
for k in [1,2,3,5,10,20,50]:
    print('devs with >=%d launches'%k,(vc>=k).sum(),'share tokens',vc[vc>=k].sum()/len(df))
print(vc.head(10).values)
df['y2']=(df.multiple>=2).astype(int); df['y5']=(df.multiple>=5).astype(int); df['y10']=(df.multiple>=10).astype(int)
df['lm']=np.log(df.multiple)
df['n_before']=df.groupby('dev_wallet').cumcount()
df['n_total']=df.dev_wallet.map(vc)
# prior stats expanding (shifted)
g=df.groupby('dev_wallet')
df['prior_y2']=g.y2.transform(lambda s:s.shift().expanding().sum())
df['prior_mean_y2']=df.prior_y2/df.n_before
df['prior_mult_med']=g.multiple.transform(lambda s:s.shift().expanding().median())
df['prior_flat']=g.multiple.transform(lambda s:(s.shift()<1.2).expanding().sum())
# time since last launch
df['gap_s']=g.launch_unix.diff()
df['ret_end']=1.0
def summ(m,name):
    d=df[m]; print(f'{name:28s} n={len(d):6d} P(2x)={d.y2.mean():.3f} P(5x)={d.y5.mean():.3f} P(10x)={d.y10.mean():.4f} med_mult={d.multiple.median():.3f} mean_log={d.lm.mean():.3f} P(mult<1.1)={(d.multiple<1.1).mean():.3f}')
print('--- by n_total (ex-post) '); 
summ(df.n_total==1,'one-off (ex post)'); summ(df.n_total.between(2,4),'2-4'); summ(df.n_total.between(5,9),'5-9'); summ(df.n_total>=10,'10+'); 
print('--- by n_before (ex ante)')
for lo,hi in [(0,0),(1,1),(2,2),(3,4),(5,9),(10,19),(20,10**6)]:
    summ(df.n_before.between(lo,hi),f'n_before {lo}-{hi}')
# first launch of each dev (restricting to first obs) vs others, split by whether dev eventually serial
print('--- first launch of devs by eventual serial (leak-prone, descriptive)')
f=df.n_before==0
summ(f&(df.n_total==1),'first, one-off'); summ(f&(df.n_total>=5),'first, eventually 5+')
# prior performance
print('--- prior hit history')
h=df[df.n_before>=3]
for lo,hi in [(0,0.001),(0.001,0.15),(0.15,0.3),(0.3,0.5),(0.5,1.01)]:
    summ((df.n_before>=3)&(df.prior_mean_y2>=lo)&(df.prior_mean_y2<hi),f'prior hit {lo}-{hi}')
# time split: first half vs second half
t=df.launch_unix.quantile(.5)
print('--- OOS: build dev stats from first half, test in second half')
tr=df[df.launch_unix<t]; te=df[df.launch_unix>=t]
s=tr.groupby('dev_wallet').agg(n=('y2','size'),h=('y2','mean'),hm=('y2','sum'))
te=te.join(s,on='dev_wallet')
te['seen']=te.n.notna()
print('2nd half tokens from devs seen in 1st half', te.seen.mean())
for nm,m in [('unseen dev',~te.seen),('seen n=1',te.n==1),('seen n 2-4',te.n.between(2,4)),('seen n>=5',te.n>=5),('seen n>=5 & h==0',(te.n>=5)&(te.h==0)),('seen n>=5 & h>=.3',(te.n>=5)&(te.h>=.3)),('seen n>=3 & h>=.5',(te.n>=3)&(te.h>=.5))]:
    d=te[m]; print(f'{nm:24s} n={len(d):6d} P2x={d.y2.mean():.3f} P5x={d.y5.mean():.4f} med={d.multiple.median():.3f}')
print('overall base', df.y2.mean(), df.y5.mean(), df.multiple.median())
# serial dev launch tempo
print('gap quantiles (s) for repeat launches', df.gap_s.dropna().quantile([.05,.25,.5,.75,.95]).values)
# fast re-launch after failed
d=df[df.n_before>0]
d['prev_mult']=g.multiple.shift()[d.index]
d['prev_gap_min']=d.gap_s/60
summ(d.index.isin(d[(d.prev_mult<1.2)].index),'after prev flat(<1.2x)')
summ(d.index.isin(d[(d.prev_mult>=2)].index),'after prev 2x+')
summ(d.index.isin(d[(d.prev_gap_min<60)].index),'relaunch<1h')
summ(d.index.isin(d[(d.prev_gap_min>=60*24)].index),'relaunch>=24h')
# pooled by-day concentration of top devs
print('top-20 devs share', vc.head(20).sum()/len(df), 'top-100', vc.head(100).sum()/len(df))
# early-features of serial vs one-off
for c in ['trades_5','vol_5','buys_5','sells_5','buy_vol_5','sell_vol_5','avg_5','price_15','vol_15']:
    df['r_'+c]=df[c]
df['bs_ratio5']=df.buy_vol_5/(df.sell_vol_5+1)
df['pay']=0
print(df.groupby(pd.cut(df.n_before,[-1,0,2,9,10**6]))[['trades_5','vol_5','bs_ratio5','price_15','growth_10','multiple']].median())
df['dev_h']=df.dev_wallet.map(lambda x:hashlib.sha256(x.encode()).hexdigest()[:6])
print(df.groupby('dev_h').size().sort_values(ascending=False).head(10))
df.to_pickle('/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/launch27.pkl')
