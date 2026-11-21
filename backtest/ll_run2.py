import sys; sys.path.insert(0,'/home/user/Detour/backtest')
import ll_lib as L, numpy as np, pandas as pd
pd.set_option('display.width',250); pd.set_option('display.max_columns',30); pd.set_option('display.max_rows',400)
m=pd.read_pickle('/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/ll_m.pkl')
out=[]
def P(t): print(t); out.append(str(t))
cols=['rule','h','N','ntok','gross','med','g_lo','g_hi','t_g','net','n_lo','n_hi','t_n','win']
def table(rules,hs=('l1','l4','l16'),split=False):
    rows=[]
    for lab,sig in rules:
        for h in hs:
            if split:
                for nm,mk in (('ALL',sig),('PRE',sig&~m.test),('TEST',sig&m.test)):
                    r=L.row(mk,h,m,f'{lab} [{nm}]'); rows.append(r)
            else: rows.append(L.row(sig,h,m,lab))
    d=pd.DataFrame(rows); d=d[[c for c in cols if c in d.columns]]
    return L.fmt(d).to_string(index=False)
el=(m.age>=2)&m.active
v1k=el&(m.volume>=1000)
P('### baseline'); P(table([('all active age>=2',el),('vol>=1k',v1k),('vol>=1k flat bars incl',(m.age>=2)&(m.volume>=0))]))
P('### A. return profile after candle (vol>=1k), l-horizons (exit at last obs if series ends)')
bins=[(-1,-.5),(-.5,-.3),(-.3,-.15),(-.15,-.05),(-.05,.05),(.05,.15),(.15,.3),(.3,.5),(.5,1),(1,100)]
P(table([(f'rbar [{a:+.2f},{b:+.2f})',v1k&(m.r_bar>=a)&(m.r_bar<b)) for a,b in bins]))
P('### A2. strict horizons (next bar must exist)')
P(table([(f'rbar [{a:+.2f},{b:+.2f})',v1k&(m.r_bar>=a)&(m.r_bar<b)) for a,b in [(-1,-.3),(.5,100),(.15,.5),(-.3,-.05)]],hs=('f1','f4','f16')))
P('### B. headline rules +50% / -30% with pre/test split')
P(table([('UP>=+50% vol>=1k',v1k&(m.r_bar>=.5)),('DN<=-30% vol>=1k',v1k&(m.r_bar<=-.3)),('UP>=+50% any vol',el&(m.r_bar>=.5)),('DN<=-30% any vol',el&(m.r_bar<=-.3))],split=True))
P('### B2 age buckets')
for a,b in [(2,4),(4,8),(8,24),(24,5000)]:
    ag=(m.age>=a)&(m.age<b)
    P(table([(f'UP50 age[{a},{b})',v1k&ag&(m.r_bar>=.5)),(f'DN30 age[{a},{b})',v1k&ag&(m.r_bar<=-.3)),(f'base age[{a},{b})',v1k&ag)]))
P('### B3 termination rate after event (no further candle within 4h and not data end)')
fin=(m.last_b<m.gmax-16)
for lab,sg in [('all vol>=1k',v1k),('UP50',v1k&(m.r_bar>=.5)),('DN30',v1k&(m.r_bar<=-.3)),('DN50',v1k&(m.r_bar<=-.5))]:
    d=m[sg&(m.b+16<=m.gmax)]
    died=(d.last_b<d.b+4)
    P((lab,len(d),'series ends within 1h',round(died.mean(),3),'ends within 4h',round((d.last_b<d.b+16).mean(),3)))
open('/home/user/Detour/backtest/out/ll_part2.txt','w').write('\n'.join(out))
