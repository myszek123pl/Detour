import duckdb, numpy as np, pandas as pd
W = "/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/w/w.db"
c = duckdb.connect(W, read_only=True)
pd.set_option('display.width',250); pd.set_option('display.max_columns',50)
d = c.sql("select dense_rank() over(order by tok) tc, dense_rank() over(order by wallet) wc, wallet, buy, usd, ts from t").df()
n=len(d)
key=(d.wc.values.astype(np.int64)*(d.tc.max()+1)+d.tc.values)   # wallet-token pair id
key=pd.factorize(key)[0].astype(np.int64)
ts=d.ts.values.astype(np.int64); buy=d.buy.values; usd=d.usd.values
val=key*10_000_000_000+ts
def nearest(src_mask, dst_mask):
    """for trades in src, nearest |dt| to a trade in dst with same key; returns arrays (dt, usd_dst, idx_dst) aligned to src indices"""
    si=np.flatnonzero(src_mask); di=np.flatnonzero(dst_mask)
    dv=val[di]; o=np.argsort(dv); dv=dv[o]; di=di[o]
    p=np.searchsorted(dv, val[si])
    best_dt=np.full(len(si),np.inf); best_j=np.full(len(si),-1)
    for cand in (p-1,p):
        okc=(cand>=0)&(cand<len(dv))
        cj=np.where(okc,cand,0)
        same=okc&(key[di[cj]]==key[si])
        dt=np.where(same,np.abs(ts[di[cj]]-ts[si]),np.inf)
        upd=dt<best_dt
        best_dt=np.where(upd,dt,best_dt); best_j=np.where(upd,di[cj],best_j)
    return si,best_dt,best_j
sb,dtb,jb=nearest(buy,~buy)      # buys -> nearest sell
ss,dts,js=nearest(~buy,buy)      # sells -> nearest buy
gap=np.full(n,np.inf); gap[sb]=dtb; gap[ss]=dts
mate=np.full(n,-1); mate[sb]=jb; mate[ss]=js
tot=usd.sum()
print('trades',n,'total vol',tot)
# pair-level
pk=pd.DataFrame({'k':key,'buy':buy,'usd':usd})
pg=pk.groupby('k').agg(nb=('buy','sum'),n=('buy','size'),vol=('usd','sum'))
pg['both']=(pg.nb>0)&(pg.nb<pg.n)
print('wallet-token pairs',len(pg),' with both sides',pg.both.mean(),' volume share of both-side pairs',pg.vol[pg.both].sum()/tot)
rows=[]
for Wd in [0,1,5,10,30,60,300,900,3600,1e12]:
    f=gap<=Wd
    # matched volume: per pair, sum of flagged buys & sells -> 2*min / total
    q=pd.DataFrame({'k':key[f],'buy':buy[f],'usd':usd[f]})
    gb=q.groupby(['k','buy']).usd.sum().unstack(fill_value=0)
    if True not in gb.columns: gb[True]=0
    if False not in gb.columns: gb[False]=0
    matched=2*np.minimum(gb[True],gb[False]).sum()
    rows.append([Wd,f.mean(),usd[f].sum()/tot,usd[f&buy].sum()/usd[buy].sum(),usd[f&~buy].sum()/usd[~buy].sum(),matched/tot])
print(pd.DataFrame(rows,columns=['W_sec','share_trades','share_vol','share_buy_vol','share_sell_vol','matched_vol_share(2*min(B,S))']).round(4).to_string())
# amount ratio for mutual nearest pairs within 5 min: sell/buy
f=(gap<=300)
sell_idx=np.flatnonzero(f&~buy); m=mate[sell_idx]
mutual=(mate[m]==sell_idx)
si=sell_idx[mutual]; bi=mate[si]
ratio=usd[si]/usd[bi]; 
lr=np.log(ratio)
print('mutual buy-sell pairs within 5min:',len(si))
bins=[0,.5,.8,.9,.95,.98,.995,1.005,1.02,1.05,1.1,1.25,2,5,1e9]
h=pd.Series(pd.cut(ratio,bins)).value_counts(sort=False)
print((h/h.sum()).round(4).to_string())
# size-weighted: pairs with ratio within [0.97,1.03] and size>=100
sz=usd[bi]
for lo in [0,100,1000,10000]:
    mm=sz>=lo
    print(f'buy size>={lo}: pairs {mm.sum()}  share with |ratio-1|<=2%: {(np.abs(ratio[mm]-1)<=.02).mean():.3f}  <=5%: {(np.abs(ratio[mm]-1)<=.05).mean():.3f}; median gap sec {np.median(gap[si][mm])}')
# time gap distribution of those pairs
print('gap quantiles',np.quantile(gap[si],[.1,.25,.5,.75,.9]).tolist(),' same-second share',(gap[si]==0).mean())
# null: ratio spike vs random same-token buy/sell pairs close in time (different wallets)
rng=np.random.default_rng(0)
tcv=d.tc.values
o=np.lexsort((ts,tcv)); 
# for each sampled sell with mate, pick a random buy in same token within +-300s from a different wallet
idxs=rng.choice(len(si),200000,replace=False)
tcs_sorted=tcv[o]; ts_sorted=ts[o]
tv=tcs_sorted.astype(np.int64)*10_000_000_000+ts_sorted
buy_sorted=buy[o]; wc_sorted=d.wc.values[o]; usd_sorted=usd[o]
bpos=np.flatnonzero(buy_sorted)
bv=tv[bpos]
rr=[]
for s in si[idxs]:
    v=tcv[s]*10_000_000_000+ts[s]
    lo=np.searchsorted(bv,v-300); hi=np.searchsorted(bv,v+300)
    if hi-lo<2: continue
    cand=bpos[lo:hi]; cand=cand[wc_sorted[cand]!=d.wc.values[s]]
    if len(cand)==0: continue
    j=cand[rng.integers(len(cand))]
    rr.append(usd[s]/usd_sorted[j])
rr=np.array(rr)
print('NULL (random different-wallet buy within 5min, same token) n',len(rr),' share |ratio-1|<=2%:',(np.abs(rr-1)<=.02).mean(),' <=5%:',(np.abs(rr-1)<=.05).mean())
print('REAL  share |ratio-1|<=2%:',(np.abs(ratio-1)<=.02).mean(),' <=5%:',(np.abs(ratio-1)<=.05).mean())
# by wallet characteristics
wl=c.sql("select address, wallet_type from wl").df().set_index('address').wallet_type
d['typ']=d.wallet.map(wl).fillna('unlabeled')
nt=d.groupby('wc').tc.nunique(); d['ntok']=d.wc.map(nt)
d['flag60']=gap<=60; d['flag300']=gap<=300
for col,b in [('typ',None),('ntokbin',pd.cut(d.ntok,[0,1,5,20,100,1e9]))]:
    gcol = d.typ if b is None else b
    r=d.assign(v=usd,f60=d.flag60*usd,f300=d.flag300*usd).groupby(gcol,observed=True).agg(n=('v','size'),vol=('v','sum'),f60=('f60','sum'),f300=('f300','sum'))
    r['vol_share']=r.vol/r.vol.sum(); r['rt60']=r.f60/r.vol; r['rt300']=r.f300/r.vol
    print(r[['n','vol_share','rt60','rt300']].round(3).to_string())
# per token: roundtrip share distribution (tokens >=50 trades)
tk=pd.DataFrame({'tc':d.tc.values,'v':usd,'f':(gap<=300)*usd,'f60':(gap<=60)*usd,'n':1}).groupby('tc').sum()
tk=tk[tk.n>=50]; tk['s300']=tk.f/tk.v; tk['s60']=tk.f60/tk.v
print(tk[['s60','s300']].describe(percentiles=[.1,.25,.5,.75,.9,.99]).round(3).to_string())
print('share of tokens where >50% of volume is within 5min round trips:',(tk.s300>.5).mean())
# top 20 largest trades: pair info
big=np.argsort(-usd)[:12]
print(pd.DataFrame({'usd':usd[big],'buy':buy[big],'gap_to_opposite_same_wallet':gap[big],'mate_usd':usd[np.where(mate[big]>=0,mate[big],0)]}).round(1).to_string())
bigmask=usd>=100000
print('trades >=100k:',bigmask.sum(),' with same-wallet opposite within 60s:',(gap[bigmask]<=60).mean(),'; within 5min',(gap[bigmask]<=300).mean())
bigmask=usd>=10000
print('trades >=10k:',bigmask.sum(),' with same-wallet opposite within 60s:',(gap[bigmask]<=60).mean(),'; within 5min',(gap[bigmask]<=300).mean())
np.save('/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/w/gap.npy',gap)
