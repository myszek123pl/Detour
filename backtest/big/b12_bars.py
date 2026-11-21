"""Test of the '15m bar with >=90% buys -> +17% next 15m' hypothesis with latency, on exact reserve paths.
 curve: jocry (std tokens) and Oct-15 ; pool: Oct-15 PumpSwap migration pools.  python3 -I b12_bars.py <scratch>"""
import sys, os, numpy as np, pandas as pd, time, duckdb
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from simlib import *
from statlib import *
from multiprocessing import Pool
S=sys.argv[1]; SRC=sys.argv[2]   # jocry | oct | pool
import datetime as dt_
def ep(s): return dt_.datetime.fromisoformat(s).replace(tzinfo=dt_.timezone.utc).timestamp()
BAR=900.0; MINN=10; MINSOL=1000/SOLUSD
LATS=[0,1,5,30,900]
TIP=0.30/SOLUSD; X=200/SOLUSD
BUCKETS=[(0,0.3),(0.3,0.5),(0.5,0.7),(0.7,0.9),(0.9,1.01)]
HOLD=dict(tmax=900.0)

def bars_for(t,b,sol,sy):
    ns=~sy
    k=np.floor(t/BAR).astype(np.int64)
    out=[]
    for kk in np.unique(k[ns]):
        m=(k==kk)&ns
        n=m.sum()
        if n<MINN: continue
        v=np.nansum(sol[m]); 
        if v<MINSOL: continue
        bs=np.nansum(sol[m&b])/v
        out.append((kk,n,v,bs))
    return out

def sim_bar(d,kk,lat,fee,tip,P=None,m=None,pool=False):
    cap=None if pool else 112.0
    t=d['t']; tc=(kk+1)*BAR
    i=idx_at(t,tc)
    if i<0: return None
    en=entry(d,i,lat,X,fee,tip,t_dec=tc,vs_cap=cap)
    if en is None: return None
    if pool:
        r,kind,ntx=exit_sim_pool(d,en,HOLD,lat,fee,tip)
    else:
        r,kind,ntx=exit_sim(P,m,d,en,HOLD,lat,fee,tip,X)
    return r

def exit_sim_pool(d,en,spec,lat,fee,tip):
    d2=dict(d); d2['grad']=False; d2['G']=None
    return exit_sim(None,0,d2,en,spec,lat,fee,tip,X)

if SRC in ('jocry','oct'):
    T0=ep('2026-07-04T12:00:00'); T1=ep('2026-07-12T15:00:00')
    tk,df,pg=load(S,mayhem=False,tmin=(T0 if SRC=='jocry' else None),tmax=(T1 if SRC=='jocry' else None),src=SRC)
    PP=Paths(tk,df,pg); FEE=0.0125
    def work(m):
        d=PP.tok(m); t=d['t']
        if len(t)<MINN: return []
        rows=[]
        prog=(d['vs']-VS0)/85.0
        for kk,n,v,bs in bars_for(t,d['b'],d['sol'],d['sys']):
            tc=(kk+1)*BAR; i=idx_at(t,tc)
            if i<0 or prog[i]>0.95: continue
            # signal-bar contemporaneous move (mid at bar open vs close)
            i0=idx_at(t,kk*BAR); mid0=(d['vs'][i0]/d['vt'][i0]) if i0>=0 else d['vs'][0]/d['vt'][0]
            ret_bar=(d['vs'][i]/d['vt'][i])/mid0-1
            rec=dict(mid=m,L=d['L'],kk=kk,n=n,vol=v,bs=bs,ret_bar=ret_bar,prog=prog[i],age=tc-d['L'])
            for lat in LATS:
                r=sim_bar(d,kk,lat,FEE,TIP,PP,m)
                rec[f'r{lat}']=np.nan if r is None else r
            # ideal: zero latency, zero cost
            rr=None
            en=entry(d,i,0,X,0.0,0.0,t_dec=tc)
            if en is not None: rec['r_ideal']=exit_sim(PP,m,d,en,HOLD,0,0.0,0.0,X)[0]
            rows.append(rec)
        return rows
    if __name__=='__main__':
        with Pool(4) as pool: res=pool.map(work,list(PP.rng.keys()),chunksize=100)
        o=pd.DataFrame([r for rr in res for r in rr]); o.to_parquet(f'{S}/work/bars_{SRC}.parquet'); print(o.shape)
else:
    con=duckdb.connect()
    D=f"{S}/datasets/pumpdatafun"
    q=f"""select mint, t, b, sol, r1, r2, r3 from (
      select p.mint, p.ts + (p.slot-a.s0)*1.0/greatest(a.s1-a.s0,1) t, (p.side='buy') b, p.sol_lamports/1e9 sol, p.r1/1e6 r1, (p.r2)/1e9 r2, p.r3/1e9 r3, p.slot, p.idx, p.seq
      from read_parquet('{D}/data/*.parquet') p join read_parquet('{S}/work/oct_anc2.parquet') a using(ts)
      where p.venue='pumpswap' and not p.failed and p.migration_pool and p.r1>0 and p.r2>0 and p.r3 is not null and p.sol_lamports is not null and p.pool_base_mint is not null) order by mint, slot, idx, seq"""
    # anchors table
    a=duckdb.connect(f"{S}/work/oct.duckdb").sql("select * from anc2").df(); a.to_parquet(f'{S}/work/oct_anc2.parquet')
    df=con.sql(q.replace("order by mint, slot, idx, seq","")).df() if False else con.sql(f"select mint,t,b,sol,r1,r2,r3 from ({q.rsplit('order by',1)[0]}) ").df()
    df=df.sort_values(['mint','t'],kind='stable').reset_index(drop=True)
    print('pool rows',len(df),'pools',df.mint.nunique())
    mints=df.mint.values; u,st=np.unique(mints,return_index=True); en_=np.r_[st[1:],len(df)]
    T=df.t.values; B=df.b.values.astype(bool); SOL=df.sol.values; R1=df.r1.values; R2=(df.r2.values+df.r3.values)
    FEE=POOL_FEE
    def work(args):
        s,e=args
        t=T[s:e]; n=e-s
        if n<MINN+2: return []
        # state after trade k = reserves before trade k+1
        vs=R2[s+1:e]; vt=R1[s+1:e]; tt=t[:-1]; b=B[s:e-1]; sol=SOL[s:e-1]
        d=dict(t=tt,vs=vs,vt=vt,b=b,sol=sol,sys=np.zeros(len(tt),bool),L=tt[0],G=None,grad=False)
        rows=[]
        for kk,nn,v,bs in bars_for(tt,b,sol,d['sys']):
            tc=(kk+1)*BAR; i=idx_at(tt,tc)
            if i<0: continue
            i0=idx_at(tt,kk*BAR); mid0=(vs[i0]/vt[i0]) if i0>=0 else R2[s]/R1[s]
            ret_bar=(vs[i]/vt[i])/mid0-1
            rec=dict(mid=int(s),L=tt[0],kk=kk,n=nn,vol=v,bs=bs,ret_bar=ret_bar,prog=np.nan,age=tc-tt[0],liq=vs[i])
            for lat in LATS:
                r=sim_bar(d,kk,lat,FEE,TIP,pool=True); rec[f'r{lat}']=np.nan if r is None else r
            en=entry(d,i,0,X,0.0,0.0,t_dec=tc,vs_cap=None)
            if en is not None: rec['r_ideal']=exit_sim_pool(d,en,HOLD,0,0.0,0.0)[0]
            rows.append(rec)
        return rows
    if __name__=='__main__':
        with Pool(4) as pool: res=pool.map(work,list(zip(st,en_)),chunksize=20)
        o=pd.DataFrame([r for rr in res for r in rr]); o.to_parquet(f'{S}/work/bars_pool.parquet'); print(o.shape)
