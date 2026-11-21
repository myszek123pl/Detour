import sys, os, numpy as np, pandas as pd, duckdb
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from simlib import *
from statlib import *
from multiprocessing import Pool
import datetime as dt_
S=sys.argv[1]
def ep(s): return dt_.datetime.fromisoformat(s).replace(tzinfo=dt_.timezone.utc).timestamp()
EMB=ep('2026-07-08T12:00:00'); T1=ep('2026-07-12T15:00:00')
tk,df,pg=load(S,mayhem=False,tmin=EMB,tmax=T1); P=Paths(tk,df,pg)
FEE=0.0125; SIZES=[25,50,200,1000,5000]
SPECS={'hold':{}, 'br_sl0.7_tp1.25':dict(sl=0.7,tps=[(1.25,1.0)]), 'ladderB':dict(sl=0.5,tps=[(2.0,0.5),(5.0,0.25)],trail=0.5,arm=2.0)}
def work(m):
    d=P.tok(m); t=d['t']; out=[]
    if len(t)<2: return out
    prog=np.clip((d['vs']-VS0)/85.0,0,1.2)
    for lv in (0.3,0.5):
        if prog.max()<lv: continue
        i=int(np.argmax(prog>=lv))
        if i==0 and prog[0]>lv+0.03: continue
        for usd in SIZES:
            X=usd/SOLUSD
            for tipusd in (0.30,):
                en=entry(d,i,1,X,FEE,tipusd/SOLUSD)
                if en is None: continue
                for nme,sp in SPECS.items():
                    r,_,_=exit_sim(P,m,d,en,sp,1,FEE,tipusd/SOLUSD,X)
                    out.append(dict(mid=m,L=d['L'],lv=lv,usd=usd,spec=nme,r=r))
    return out
if __name__=='__main__':
    with Pool(4) as pool: res=pool.map(work,list(P.rng.keys()),chunksize=200)
    o=pd.DataFrame([r for rr in res for r in rr]); o['blk']=block_ids(o.L.values,3.0,EMB)
    print('=== size sensitivity (jocry test window, lat 1s, 1.25%/side, tip $0.30)')
    for lv in (0.3,0.5):
        for nme in SPECS:
            s=f'lv {lv} {nme:16s}'
            for usd in SIZES:
                g=o[(o.lv==lv)&(o.spec==nme)&(o.usd==usd)]
                ci=boot_mean(g.r.values,g.blk.values,300); s+=f' | ${usd}: {100*g.r.mean():5.1f} [{100*ci[0]:5.1f},{100*ci[1]:5.1f}]'
            print(s)
    # launch-level base rates
    con=duckdb.connect()
    t=con.sql(f"select * from read_parquet('{S}/work/tok_jocry2.parquet')").df()
    w=t[(t.L>=EMB)&(t.L<T1)&(~t.mh)]
    print('jocry test-window std launches',len(w),'P(grad|launch)=',round(w.G.notna().mean(),4))
    w2=t[(t.L>=ep('2026-07-04T12:00:00'))&(t.L<T1)&(t.mh)]
    print('jocry mayhem launches',len(w2),'P(grad|launch)=',round(w2.G.notna().mean(),4))
    ot=con.sql(f"select * from read_parquet('{S}/work/oct_tok.parquet')").df(); print('oct std launches (first14h, with trades)',len(ot),'P(grad)=',round(ot.G.notna().mean(),4))
    bo=pd.read_parquet(f'{S}/work/base_events_oct.parquet'); bo['blk']=block_ids(bo.L.values,3.0,bo.L.min())
    print('=== Oct latency effect (n filled, chart>=2x, net>=2x, hold mean)')
    for lv in (0.1,0.3,0.5):
        for lat in (0,1,5,30):
            g=bo[(bo.lv==lv)&(bo.lat==lat)&(bo.sz=='200')]; f=g[g.filled==1]
            nl=f.net_last-1
            print(f'lv {lv} lat {lat:2d}: trig {len(g)} fill {len(f)/len(g):.3f} chart>=2x {100*(f.chart_max>=2).mean():.1f} net>=2x {100*(f.net_max>=2).mean():.1f} hold {100*nl.mean():.1f} [{100*boot_mean(nl.values,f.blk.values,300)[0]:.1f},{100*boot_mean(nl.values,f.blk.values,300)[1]:.1f}]')
