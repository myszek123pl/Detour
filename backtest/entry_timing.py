"""Entry-timing analysis. Usage: python3 -I entry_timing.py <out_dir>  (reads out/sim_results.parquet)"""
import sys, numpy as np, pandas as pd
from scipy.stats import spearmanr
pd.set_option("display.width",250); pd.set_option("display.max_columns",50)
FEE,TIP=0.0125,0.30
R=pd.read_parquet("/home/user/Detour/backtest/out/sim_results.parquet")
R=R[R.peak_mult<1000].copy()
R["L"]=np.minimum(R.liquidity_usd,0.4*R.market_cap_usd).clip(lower=1)
split=pd.Timestamp("2026-06-24",tz="UTC")
R["test"]=R.captured_at>=split
R["bsr"]=R.buy_usd_1h/(R.sell_usd_1h+1)
R["hour"]=R.captured_at.dt.hour; R["dow"]=R.captured_at.dt.dayofweek
R["age_min"]=R.time_since_launch_sec/60
STR=["ladder_B","tight_D","hold_24h","scalp_E","runner_F"]
def net(df,s,pos=200):
    imp=(2*pos/df.L).clip(upper=0.9)
    return df[s]*(1-FEE-imp)**2-TIP*(1+df[s+"_n"])/pos-1
for s in STR: R["net_"+s]=net(R,s)
R["net_ladder_B50"]=net(R,"ladder_B",50)
R["win2x"]=(R.peak_mult>=2)
rng=np.random.default_rng(0)
def ci(x,n=500):
    x=np.asarray(x); 
    if len(x)<15: return (np.nan,np.nan)
    m=x[rng.integers(0,len(x),(n,len(x)))].mean(1); return tuple(np.percentile(m,[2.5,97.5]))
print("N",len(R),"train",(~R.test).sum(),"test",R.test.sum())
print(R[["time_since_launch_sec","market_cap_usd","liquidity_usd","L","price_change_1h","bsr"]].describe(percentiles=[.1,.5,.9]).T)
print("corr spearman\n",R[["age_min","market_cap_usd","price_change_1h","bsr","hour","L"]].corr("spearman").round(2))
print("base EV all:",{s:round(R["net_"+s].mean(),3) for s in STR},"p2x",R.win2x.mean().round(3))
print("base EV train/test ladder_B:",R[~R.test].net_ladder_B.mean().round(3),R[R.test].net_ladder_B.mean().round(3))

def bucket(feat,q=10,label=None,cats=None):
    d=R.dropna(subset=[feat]).copy()
    if cats is not None: d["b"]=d[feat]
    else: d["b"]=pd.qcut(d[feat],q,duplicates="drop")
    print(f"\n######## {label or feat} (n={len(d)})")
    g=d.groupby("b",observed=True)
    t=pd.DataFrame({"n":g.size(),"lo":g[feat].min().round(3),"hi":g[feat].max().round(3),
        "p2x":g.win2x.mean().round(3),"medPeak":g.peak_mult.median().round(2),
        "mdd_med":g.mdd_from_peak.median().round(3),"medFinal":g.final_mult.median().round(3),
        "medL":g.L.median().round(0)})
    for s in STR:
        t["EV_"+s]=g["net_"+s].mean().round(3)
    t["med_B"]=g.net_ladder_B.median().round(3)
    t["EV_B50"]=g.net_ladder_B50.mean().round(3)
    lo=[];hi=[]
    for k,x in g: 
        c=ci(x.net_ladder_B); lo.append(c[0]);hi.append(c[1])
    t["B_lo"]=np.round(lo,3);t["B_hi"]=np.round(hi,3)
    # train/test per bucket using same bucket edges
    for nm,m in (("tr",~d.test),("te",d.test)):
        gg=d[m].groupby("b",observed=True)
        t["n_"+nm]=gg.size()
        t["B_"+nm]=gg.net_ladder_B.mean().round(3)
        t["D_"+nm]=gg.net_tight_D.mean().round(3)
        t["p2x_"+nm]=gg.win2x.mean().round(3)
    print(t.to_string())
    rho={}
    for s in ["ladder_B","tight_D","hold_24h"]:
        a=d[~d.test].groupby("b",observed=True)["net_"+s].mean(); b=d[d.test].groupby("b",observed=True)["net_"+s].mean()
        j=pd.concat([a,b],axis=1).dropna()
        rho[s]=round(spearmanr(j.iloc[:,0],j.iloc[:,1])[0],2) if len(j)>3 else None
    # monotonic trend rho (bucket idx vs EV)
    r_all=spearmanr(d[feat],d.net_ladder_B)[0]; 
    print("train-vs-test bucket-EV spearman:",rho," | token-level spearman(feat,netB) all/train/test:",
      round(r_all,3),round(spearmanr(d[~d.test][feat],d[~d.test].net_ladder_B)[0],3),round(spearmanr(d[d.test][feat],d[d.test].net_ladder_B)[0],3))
    return t
bucket("age_min",label="time_since_launch (minutes)")
bucket("market_cap_usd")
bucket("price_change_1h")
bucket("bsr",label="buy/sell USD ratio 1h")
bucket("trade_buy_sell_ratio")
bucket("net_flow_usd")
bucket("L",label="conservative liquidity L")
bucket("hour",cats=True,label="hour UTC")
bucket("dow",cats=True,label="day of week (0=Mon)")
R["date"]=R.captured_at.dt.date
bucket("date",cats=True,label="date")
# 2D: age x mcap tertiles
R["ageT"]=pd.qcut(R.age_min,3,labels=["young","mid","old"]);R["mcT"]=pd.qcut(R.market_cap_usd,3,labels=["lowmc","midmc","highmc"])
print("\n2D age x mcap EV ladder_B / n / p2x");print(R.pivot_table(index="ageT",columns="mcT",values="net_ladder_B",aggfunc="mean",observed=True).round(3))
print(R.pivot_table(index="ageT",columns="mcT",values="net_ladder_B",aggfunc="size",observed=True))
print(R.pivot_table(index="ageT",columns="mcT",values="win2x",aggfunc="mean",observed=True).round(3))
print("test only EV B:");print(R[R.test].pivot_table(index="ageT",columns="mcT",values="net_ladder_B",aggfunc="mean",observed=True).round(3))
print("train only EV B:");print(R[~R.test].pivot_table(index="ageT",columns="mcT",values="net_ladder_B",aggfunc="mean",observed=True).round(3))
# multivariate OLS (standardised ranks) on netB, controls
import numpy.linalg as la
X=R[["age_min","market_cap_usd","price_change_1h","bsr","L"]].copy()
X=X.rank(pct=True); X["hr_night"]=R.hour.isin(range(0,8)).astype(float); X=X.dropna(); y=R.loc[X.index,"net_ladder_B"].clip(upper=R.net_ladder_B.quantile(.99))
for nm,m in (("all",slice(None)),("train",~R.loc[X.index,"test"]),("test",R.loc[X.index,"test"])):
    Xm=X[m] if nm!="all" else X; ym=y[m] if nm!="all" else y
    A=np.c_[np.ones(len(Xm)),Xm.values]; b,res,_,_=la.lstsq(A,ym.values,rcond=None)
    e=ym.values-A@b; se=np.sqrt(np.diag(la.inv(A.T@A))*e.var())
    print(nm,"OLS rank-coefs (t):",{c:(round(b[i+1],3),round(b[i+1]/se[i+1],1)) for i,c in enumerate(Xm.columns)})
# practical filters
def rep(name,m):
    d=R[m]; 
    print(f"{name:45s} n={len(d):5d} tr/te={int((~d.test).sum())}/{int(d.test.sum())} EV_B={d.net_ladder_B.mean():.3f} tr={d[~d.test].net_ladder_B.mean():.3f} te={d[d.test].net_ladder_B.mean():.3f} EV_D={d.net_tight_D.mean():.3f} EV_hold={d.net_hold_24h.mean():.3f} p2x={d.win2x.mean():.3f} med={d.net_ladder_B.median():.3f}")
print()
rep("all",R.age_min>-1)
rep("dip (pc1h<-50)",R.price_change_1h<-50)
rep("flat (-50..50)",R.price_change_1h.between(-50,50))
rep("chase (pc1h>100)",R.price_change_1h>100)
rep("chase (pc1h>500)",R.price_change_1h>500)
rep("age<30min",R.age_min<30); rep("age 30-120",R.age_min.between(30,120)); rep("age>120",R.age_min>120); rep("age>600",R.age_min>600)
rep("mcap<5k",R.market_cap_usd<5000); rep("mcap 5-20k",R.market_cap_usd.between(5000,20000)); rep("mcap>20k",R.market_cap_usd>20000); rep("mcap>100k",R.market_cap_usd>100000)
rep("hour 0-7",R.hour<8); rep("hour 8-15",R.hour.between(8,15)); rep("hour 16-23",R.hour>=16)
rep("weekend",R.dow>=5); rep("weekday",R.dow<5)
# placebo: shuffled-label best-decile test for hour & age
print("\nPlacebo: max |decile EV - mean| spread under shuffle vs actual (ladder_B, 10 bins)")
for f in ["age_min","market_cap_usd","price_change_1h","bsr"]:
    d=R.dropna(subset=[f]); b=pd.qcut(d[f],10,duplicates="drop")
    act=d.groupby(b,observed=True).net_ladder_B.mean(); a=act.max()-act.min()
    sp=[]
    y=d.net_ladder_B.values
    for _ in range(300):
        sp.append(pd.Series(rng.permutation(y)).groupby(b.values).mean().pipe(lambda z:z.max()-z.min()))
    print(f,"actual spread",round(a,3),"placebo 95th",round(np.percentile(sp,95),3),"p=",round((np.array(sp)>=a).mean(),3))
