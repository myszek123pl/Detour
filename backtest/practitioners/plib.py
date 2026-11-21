"""Shared engine: hourly grid loading, EMA, cost model, exits, bootstrap."""
import json, os, numpy as np, pandas as pd
SP="/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/"
NOW=1794528000+9*86400   # ~2026-11-21 (data fetched 2026-11-21)
SUPPLY=1e9               # pump.fun fixed supply (burns ignored)
FEE=0.0125               # per side, small caps
LAMBDA=0.05              # pool liquidity / market cap (see calibration in notes)
HORIZON_D=41

def load(pair):
    fn=SP+"gt_hour/"+pair+".json"
    if not os.path.exists(fn): return None
    j=json.load(open(fn)); l=j["l"]
    ref=j["grad_ts"]; t0=ref//3600*3600; tend=min(NOW//3600*3600, ref+HORIZON_D*86400)//3600*3600
    n=int((tend-t0)//3600)+1
    o=np.full(n,np.nan); h=o.copy(); lo=o.copy(); c=o.copy(); v=np.zeros(n)
    for ts,oo,hh,ll,cc,vv in l:
        i=int((ts//3600*3600-t0)//3600)
        if 0<=i<n: o[i],h[i],lo[i],c[i],v[i]=oo,hh,ll,cc,vv
    # forward fill close; empty hours get open=high=low=close=prev close, vol 0
    last=np.nan
    for i in range(n):
        if np.isnan(c[i]): c[i]=last; o[i]=last; h[i]=last; lo[i]=last
        else: last=c[i]
    # leading NaNs (before first trade): leave NaN
    return dict(mint=j["mint"],ref=ref,o=o,h=h,l=lo,c=c,v=v,n=n,t0=t0)

def ema(c,span=9):
    a=2/(span+1); e=np.full(len(c),np.nan); prev=np.nan
    for i,x in enumerate(c):
        if np.isnan(x): continue
        prev=x if np.isnan(prev) else a*x+(1-a)*prev
        e[i]=prev
    return e

def side_cost(px,size,fee=FEE,lam=LAMBDA):
    L=max(lam*px*SUPPLY,1.0)
    return min(fee+size/L,0.9)

def next_vol(v,i,maxwait=48):
    for k in range(i,min(len(v),i+maxwait+1)):
        if v[k]>0: return k
    return None

def dead_end(d):
    return d["v"][-48:].sum()==0

def finish(d,j,px_in,exit_idx,exit_px,size,fee,lam,haircut,stuck=False):
    ci=side_cost(px_in,size,fee,lam)
    if stuck:   # marked at last close; haircut if pool dead
        hc = haircut if dead_end(d) else 1.0
        co=side_cost(exit_px,size,fee,lam)
        return (exit_px*hc*(1-co))/(px_in*(1+ci))-1
    co=side_cost(exit_px,size,fee,lam)
    return (exit_px*(1-co))/(px_in*(1+ci))-1

def run_exit(d,j,kind,size,fee,lam,haircut,e9=None,hold=168,cap=336):
    """Enter at open of bar j. kind in hold/ema/ladder. Return net return."""
    o,c,v,h=d["o"],d["c"],d["v"],d["h"]; n=d["n"]; px=o[j]
    if not np.isfinite(px) or px<=0: return None
    if kind=="hold":
        end=j+hold
        if end>=n: return None   # right-censored: drop
        k=next_vol(v,end)
        if k is None: return finish(d,j,px,n-1,c[n-1],size,fee,lam,haircut,True)
        return finish(d,j,px,k,o[k],size,fee,lam,haircut)
    if kind=="horizon":   # buy and hold to end of data window
        return finish(d,j,px,n-1,c[n-1],size,fee,lam,haircut,True)
    if kind=="ema":
        last=min(n-1, j+cap) if cap else n-1
        if cap and j+cap>=n: return None
        for k in range(j,last):
            if c[k]<e9[k]:
                m=next_vol(v,k+1)
                if m is None: return finish(d,j,px,n-1,c[n-1],size,fee,lam,haircut,True)
                return finish(d,j,px,m,o[m],size,fee,lam,haircut)
        m=next_vol(v,last)  # time stop / horizon
        if m is None or last==n-1: return finish(d,j,px,n-1,c[n-1],size,fee,lam,haircut,True)
        return finish(d,j,px,m,o[m],size,fee,lam,haircut)
    if kind=="ladder":   # 1/3 at 2x, 1/3 at 4x, 1/3 at 14d; tranches priced separately
        end=j+cap
        if end>=n: return None
        tg=[(2.0,1/3),(4.0,1/3)]; tot=0.0; done=0.0
        ci=side_cost(px,size,fee,lam)
        k=j; filled=[False,False]
        for k in range(j,end):
            for ti,(m,w) in enumerate(tg):
                if not filled[ti] and h[k]>=m*px and v[k]>0:
                    filled[ti]=True; p=max(m*px,o[k]) if o[k]>m*px else m*px
                    co=side_cost(p,size*w,fee,lam)
                    tot+=w*(p*(1-co)/(px*(1+ci))-1); done+=w
        rest=1-done
        m=next_vol(v,end)
        if m is None: rr=finish(d,j,px,n-1,c[n-1],size*rest,fee,lam,haircut,True)
        else: rr=finish(d,j,px,m,o[m],size*rest,fee,lam,haircut)
        return tot+rest*rr
    raise ValueError(kind)

def boot_mean(x,B=10000,seed=1,stat=np.mean):
    x=np.asarray(x); r=np.random.default_rng(seed)
    if len(x)==0: return (np.nan,np.nan)
    idx=r.integers(0,len(x),(B,len(x)))
    s=stat(x[idx],axis=1) if stat is np.mean else np.apply_along_axis(stat,1,x[idx])
    return tuple(np.percentile(s,[2.5,97.5]))

def summ(x,label=""):
    x=np.asarray([a for a in x if a is not None and np.isfinite(a)])
    if len(x)==0: return dict(label=label,n=0)
    lo,hi=boot_mean(x); mlo,mhi=boot_mean(x,stat=np.median)
    xs=np.sort(x)
    return dict(label=label,n=len(x),mean=x.mean(),ci_lo=lo,ci_hi=hi,median=np.median(x),med_lo=mlo,med_hi=mhi,
                win=(x>0).mean(),mean_ex_top=xs[:-1].mean() if len(x)>1 else np.nan,worst=xs[0],best=xs[-1],
                share_lt_m50=(x<-0.5).mean())
