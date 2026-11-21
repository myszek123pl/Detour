"""Rules dataset: entry events at curve progress levels with point-in-time features and net returns for a grid of exit rules.
python3 -I b06_rules.py <scratch>   (jocry std tokens)"""
import sys, os, numpy as np, pandas as pd, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from simlib import *
from multiprocessing import Pool
S=sys.argv[1]
import datetime as dt_
def ep(s): return dt_.datetime.fromisoformat(s).replace(tzinfo=dt_.timezone.utc).timestamp()
T0=ep('2026-07-04T12:00:00'); T1=ep('2026-07-12T15:00:00')
LEVELS=[0.05,0.10,0.20,0.30,0.40,0.50,0.60]
LATS=[1,5,30]
FEE=0.0125; TIP=0.30/SOLUSD; X=200/SOLUSD
EXITS={'hold':{}}
for sl in (0.5,0.7,0.85):
    for tp in (1.25,1.5,2.0,3.0):
        EXITS[f'br_sl{sl}_tp{tp}']=dict(sl=sl,tps=[(tp,1.0)])
for tr in (0.10,0.20,0.30,0.50):
    for arm in (1.0,1.3,2.0):
        EXITS[f'trail{tr}_arm{arm}']=dict(trail=tr,arm=arm)
EXITS['ladderB']=dict(sl=0.5,tps=[(2.0,0.5),(5.0,0.25)],trail=0.5,arm=2.0)
EXITS['ladderC']=dict(sl=0.6,tps=[(1.5,1/3),(3.0,1/3),(10.0,1/3)])
EXITS['ladderD']=dict(sl=0.7,tps=[(1.3,0.5),(2.0,0.5)])
for tm in (30,120,600,3600):
    EXITS[f'time{tm}_sl0.7']=dict(sl=0.7,tmax=tm)
EXNAMES=list(EXITS)
tk,df,pg=load(S,mayhem=False,tmin=T0,tmax=T1)
P=Paths(tk,df,pg)

def feats(d,i,lv,meta):
    t=d['t']; L=d['L']; ti=t[i]
    b=d['b'][:i+1]; sol=d['sol'][:i+1]; wid=d['wid'][:i+1]; sy=d['sys'][:i+1]; tt=t[:i+1]
    ns=~sy
    cw=int(meta.creator_wid) if not pd.isna(meta.creator_wid) else -1
    f=dict(age=ti-L, first_gap=t[0]-L, n_tr=i+1)
    f['cap_launch']=int((t[0]-L)<=10.0)
    bm=b&ns
    f['uniq_buyers']=len(np.unique(wid[bm]))
    sb=sol[bm]; tot=np.nansum(sb)
    if len(sb)>0 and tot>0:
        w=pd.Series(sb).groupby(wid[bm]).sum().sort_values(ascending=False).values
        f['top1_buy']=w[0]/tot; f['top3_buy']=w[:3].sum()/tot; f['hhi_buy']=float(((w/tot)**2).sum())
    else: f['top1_buy']=f['top3_buy']=f['hhi_buy']=np.nan
    # window 60s
    w60=(tt>ti-60)&ns
    if w60.sum()>0:
        f['bs_cnt60']=b[w60].mean(); s60=np.nansum(sol[w60]); f['bs_sol60']=np.nansum(sol[w60&b])/s60 if s60>0 else np.nan
        f['n60']=int(w60.sum()); f['netflow60']=np.nansum(sol[w60&b])-np.nansum(sol[w60&~b])
    else: f['bs_cnt60']=f['bs_sol60']=np.nan; f['n60']=0; f['netflow60']=0.0
    w300=(tt>ti-300)&ns
    f['bs_cnt300']=b[w300].mean() if w300.sum()>0 else np.nan
    f['n300']=int(w300.sum())
    f['bs_cnt_all']=b[ns].mean() if ns.sum()>0 else np.nan
    # snipers: non-creator non-sys wallets buying within 3s of launch (only meaningful if captured from launch)
    sn=bm&(tt<=L+3.0)&(wid!=cw)
    f['snipers3']=len(np.unique(wid[sn])) if f['cap_launch'] else np.nan
    sn10=bm&(tt<=L+10.0)&(wid!=cw)
    f['snipers10']=len(np.unique(wid[sn10])) if f['cap_launch'] else np.nan
    f['sniper_sol3']=float(np.nansum(sol[sn])) if f['cap_launch'] else np.nan
    # creator activity
    cm=(wid==cw)
    f['cr_sells']=int((cm&~b).sum()); f['cr_sell_sol']=float(np.nansum(sol[cm&~b]))
    f['cr_buy_sol']=float(np.nansum(sol[cm&b]))
    # momentum: progress change in last 60s
    prog=(d['vs']-VS0)/85.0
    k60=idx_at(t[:i+1],ti-60)
    f['dprog60']=prog[i]-(prog[k60] if k60>=0 else 0.0)
    f['prog_peak_so_far']=float(prog[:i+1].max()); f['drawdown_from_peak']=float(prog[:i+1].max()-prog[i])
    f['speed']=prog[i]/max(ti-L,1.0)
    # net sol by wallet: top5 net-long share
    return f

def work(m):
    d=P.tok(m); t=d['t']; out=[]
    if len(t)<2: return out
    prog=np.clip((d['vs']-VS0)/85.0,0,1.2)
    meta=d['meta']
    for lv in LEVELS:
        if prog.max()<lv: break
        i=int(np.argmax(prog>=lv))
        if i==0 and prog[0]>lv+0.03: continue
        f=feats(d,i,lv,meta)
        f.update(mid=m,L=d['L'],lv=lv,grad=int(d['grad']),dev_pct=meta.dev_pct,cr_prev=meta.cr_prev_launch,cr_prev_grad=meta.cr_prev_grad_pit,
                 snipe_delta=meta.snipe_delta,cb=int(meta.cb),prog_i=prog[i])
        for lat in LATS:
            en=entry(d,i,lat,X,FEE,TIP)
            if en is None:
                f[f'filled_{lat}']=0
                for nme in EXNAMES: f[f'r_{nme}_{lat}']=np.nan
                continue
            f[f'filled_{lat}']=1
            for nme,spec in EXITS.items():
                r,kind,ntx=exit_sim(P,m,d,en,spec,lat,FEE,TIP,X)
                f[f'r_{nme}_{lat}']=r
                if nme=='hold': f[f'kind_hold_{lat}']=kind
        out.append(f)
    return out

if __name__=='__main__':
    mids=list(P.rng.keys()); t0=time.time()
    with Pool(4) as pool:
        res=pool.map(work, mids, chunksize=200)
    rows=[r for rr in res for r in rr]
    o=pd.DataFrame(rows); o.to_parquet(f'{S}/work/rules_events.parquet')
    print(o.shape, round(time.time()-t0), 's')
