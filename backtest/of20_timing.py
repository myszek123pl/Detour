import duckdb, numpy as np, pandas as pd
W = "/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/w/w.db"
c = duckdb.connect(W, read_only=True)
pd.set_option('display.width',250); pd.set_option('display.max_columns',50)
d = c.sql("""select dense_rank() over(order by tok) tc, dense_rank() over(order by wallet) wc, buy, usd, ts, coalesce(ts-launch, null) age
  from t left join tkm using(tok)""").df()
# stable sort: tok, ts
d = d.sort_values(['tc','ts'], kind='stable').reset_index(drop=True)
print('integer ts share', float((d.ts==np.floor(d.ts)).mean()))
tc=d.tc.values; ts=d.ts.values; buy=d.buy.values.astype(np.int8); usd=d.usd.values; wc=d.wc.values; age=d.age.values
same=np.r_[False, tc[1:]==tc[:-1]]
dt=np.r_[np.nan, np.diff(ts)]; dt[~same]=np.nan
ok = same & (dt<=3600)
x=dt[ok]
print('N intervals',ok.sum(),' P(dt=0)',(x==0).mean(),' P(dt<=1)',(x<=1).mean(),' P(<=5)',(x<=5).mean(),' P(<=30)',(x<=30).mean(),' P(<=300)',(x<=300).mean())
print('dt quantiles',np.quantile(x,[.1,.25,.5,.75,.9,.99]).tolist(),'mean',x.mean())
# by age
a_prev=np.r_[np.nan, age[:-1]]
bk=pd.cut(a_prev[ok],[-1e9,0,10,60,300,900,3600,1e12],labels=['<0(pre)','0-10s','10-60s','1-5m','5-15m','15-60m','>1h'])
dd=pd.DataFrame({'dt':x,'bk':bk})
print(dd.groupby('bk',observed=True).dt.agg(n='size',p0=lambda s:(s==0).mean(),p_le1=lambda s:(s<=1).mean(),med='median',mean='mean').round(3).to_string())
# per-token CV and burstiness
tcs=tc[ok]
g=pd.DataFrame({'tc':tcs,'dt':x}).groupby('tc').dt.agg(['mean','std','size'])
g=g[g['size']>=50]; g['cv']=g['std']/g['mean']; g['B']=(g['std']-g['mean'])/(g['std']+g['mean'])
print('tokens',len(g)); print(g[['cv','B']].describe(percentiles=[.1,.25,.5,.75,.9]).round(3).to_string())
# Poisson ref: simulate with same per-token mean, integer seconds -> CV ~1 ; also nonstationary rate effect: compute CV using only intervals after the first 20% trades?
# Same-second bursts: share of trades that are in a same-second multi-trade cluster
cnt_same = pd.Series(1,index=pd.MultiIndex.from_arrays([tc,ts])).groupby(level=[0,1]).size()
print('share of trades sharing the exact second with >=1 other trade in the same token:', float((cnt_same[cnt_same>1].sum())/cnt_same.sum()), ' max trades in 1s',int(cnt_same.max()), ' p99 size',cnt_same.quantile(.99))
# Fano factor of counts for 5s,30s,60s bins; compare with a detrended version (bin counts vs moving avg of neighbours)
res=[]
tok_bounds=np.flatnonzero(np.r_[True, tc[1:]!=tc[:-1], True])
for binw in [5,30,60]:
    fanos=[]; acf1=[]; acf1_dt=[]
    # sample 6000 tokens
    rng=np.random.default_rng(1)
    pick=rng.choice(len(tok_bounds)-1, 6000, replace=False)
    for i in pick:
        s,e=tok_bounds[i],tok_bounds[i+1]
        if e-s<80: continue
        t=ts[s:e]; 
        # contiguous span: cut at gaps >600s: use largest contiguous chunk
        gaps=np.flatnonzero(np.diff(t)>600)
        segs=np.split(np.arange(len(t)),gaps+1); seg=max(segs,key=len)
        if len(seg)<80: continue
        tt=t[seg]; n=int((tt[-1]-tt[0])//binw)+1
        if n<12: continue
        cts=np.bincount(((tt-tt[0])//binw).astype(int),minlength=n).astype(float)
        fanos.append(cts.var()/cts.mean())
        # detrend: subtract centered moving average of window 5 bins (excl self)
        k=5; ker=np.ones(2*k+1); ker[k]=0; ker/=ker.sum()
        ma=np.convolve(cts,ker,mode='same'); r=(cts-ma)[k:-k]
        ac=np.corrcoef(cts[:-1]-cts.mean(),cts[1:]-cts.mean())[0,1] if cts.std()>0 else np.nan
        acf1.append(ac)
        if len(r)>5 and r.std()>0: acf1_dt.append(np.corrcoef(r[:-1],r[1:])[0,1])
    res.append([binw,len(fanos),np.nanmedian(fanos),np.nanmean(fanos),np.nanmedian(acf1),np.nanmedian(acf1_dt)])
print(pd.DataFrame(res,columns=['bin_s','tokens','Fano_median','Fano_mean','ACF1_counts','ACF1_detrended']).round(3).to_string())
# sign persistence
sb=np.r_[False, tc[1:]==tc[:-1]]
prev=np.r_[0,buy[:-1]]
m=sb & (dt<=3600)
pbb=(buy[m&(prev==1)]).mean(); pbs=(buy[m&(prev==0)]).mean()
print('P(buy|prev buy)',pbb,'P(buy|prev sell)',pbs,' diff',pbb-pbs, ' unconditional',buy[m].mean())
# per-token-demeaned sign ACF at lags 1..10
def sign_acf(lags, mask_age=None):
    out=[]
    s=2*buy.astype(float)-1
    # token mean
    ssum=np.bincount(tc,weights=s); scount=np.bincount(tc); mu=(ssum/scount)[tc]
    z=s-mu
    for L in lags:
        mm=np.r_[np.zeros(L,bool), tc[L:]==tc[:-L]]
        zz=np.r_[np.zeros(L),z[:-L]]
        out.append(np.sum(z[mm]*zz[mm])/np.sqrt(np.sum(z[mm]**2)*np.sum(zz[mm]**2)))
    return out
print('sign ACF lags 1,2,3,5,10,20,50:',np.round(sign_acf([1,2,3,5,10,20,50]),3).tolist())
# same wallet adjacency
sw=np.r_[False, wc[1:]==wc[:-1]] & sb
print('consecutive trades by same wallet (same token):',sw.mean(),' of which same side',(buy[sw]==prev[sw]).mean())
# sign ACF excluding consecutive same-wallet
# log size ACF
ls=np.log(np.maximum(usd,1e-6)); 
ssum=np.bincount(tc,weights=ls); mu=(ssum/np.bincount(tc))[tc]; z=ls-mu
for L in [1,2,5]:
    mm=np.r_[np.zeros(L,bool), tc[L:]==tc[:-L]]; zz=np.r_[np.zeros(L),z[:-L]]
    print('log-size ACF lag',L,np.sum(z[mm]*zz[mm])/np.sqrt(np.sum(z[mm]**2)*np.sum(zz[mm]**2)))
# run lengths vs geometric
runs=[]; 
start=np.flatnonzero(np.r_[True, (tc[1:]!=tc[:-1])|(buy[1:]!=buy[:-1])])
lens=np.diff(np.r_[start,len(tc)])
runside=buy[start]; 
rb=lens[runside==1]; rs=lens[runside==0]
p_b=buy.mean()
print('mean run length buy',rb.mean(),' sell',rs.mean(),' expected iid buy',1/(1-p_b),' sell',1/p_b)
print('P(buy run>=10)',(rb>=10).mean(),' iid',p_b**9, ' P(sell run>=5)',(rs>=5).mean(),' iid',(1-p_b)**4, 'max buy run',rb.max(),'max sell run',rs.max())
# size-weighted 'burst': buy-burst followed by sell-burst: cross-correlation of 10s bins buy$ vs sell$ lagged (per token, pooled)
