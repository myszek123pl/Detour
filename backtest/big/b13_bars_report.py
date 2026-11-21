import sys, os, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from statlib import *
S=sys.argv[1]
B=[(0,0.3),(0.3,0.5),(0.5,0.7),(0.7,0.9),(0.9,1.01)]
for src in ('jocry','oct','pool'):
    d=pd.read_parquet(f'{S}/work/bars_{src}.parquet'); d['blk']=block_ids(d.kk.values*900.0,3.0,(d.kk.min()*900.0))
    if src=='jocry':
        sp=np.where(d.L<1783468800.0,'train','test')  # Jul 8 00:00 UTC
    print(f'\n===== {src}: bars n={len(d)}, tokens={d.mid.nunique()}, signal(bs>=.9) n={(d.bs>=0.9).sum()} tokens={d[d.bs>=0.9].mid.nunique()}')
    print('bs bucket | n | contemporaneous bar return mean | ideal(no lat/no cost) | net lat1 | lat5 | lat30 | lat900(+1 bar)')
    for lo,hi in B:
        g=d[(d.bs>=lo)&(d.bs<hi)]
        if len(g)<20: continue
        s=f'[{lo:.1f},{min(hi,1):.1f}) n={len(g):5d} bar_ret {100*g.ret_bar.clip(-0.99,5).mean():6.1f}'
        for c in ('r_ideal','r1','r5','r30','r900'):
            x=g[c].dropna()
            if len(x)<20: s+=' |   NA'; continue
            ci=boot_mean(x.values,g.loc[x.index,'blk'].values,400)
            s+=f' | {100*x.mean():6.1f} [{100*ci[0]:6.1f},{100*ci[1]:6.1f}] med {100*x.median():5.1f}'
        print(s)
    g=d[d.bs>=0.9]
    # excluding heavy tail: winsorize
    for c in ('r1','r30'):
        x=g[c].dropna(); print(f'  signal {c}: winsor@+100%: {100*x.clip(upper=1).mean():.1f}, drop top5: {100*x.sort_values().iloc[:-5].mean():.1f}, win rate {100*(x>0).mean():.1f}%')
    if src=='jocry':
        for s_ in ('train','test'):
            g=d[(d.bs>=0.9)&(sp==s_)]
            for c in ('r_ideal','r1','r30'):
                x=g[c].dropna(); ci=boot_mean(x.values,g.loc[x.index,'blk'].values,400); print(f'  jocry {s_} signal {c}: n={len(x)} {100*x.mean():.1f} [{100*ci[0]:.1f},{100*ci[1]:.1f}]')
