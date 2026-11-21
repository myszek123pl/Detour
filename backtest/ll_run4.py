import sys; sys.path.insert(0,'/home/user/Detour/backtest')
import ll_lib as L, numpy as np, pandas as pd
pd.set_option('display.width',250); pd.set_option('display.max_columns',30); pd.set_option('display.max_rows',400)
m=pd.read_pickle('/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/ll_m.pkl')
out=[]
def P(t): print(t,flush=True); out.append(str(t))
cols=['rule','h','N','ntok','gross','med','g_lo','g_hi','t_g','net','n_lo','n_hi','t_n','win']
def table(rules,hs=('l1','l4','l16'),split=False,df=None):
    rows=[]
    for lab,sig in rules:
        for h in hs:
            if split:
                for nm,mk in (('ALL',sig),('PRE',sig&~m.test),('TEST',sig&m.test)): rows.append(L.row(mk,h,m,f'{lab} [{nm}]'))
            else: rows.append(L.row(sig,h,m,lab))
    d=pd.DataFrame(rows); d=d[[c for c in cols if c in d.columns]]
    return L.fmt(d).to_string(index=False)
ts_=m.active&(m.tv>=1000)&(m.tn>=10)&(m.age>=2)
hi=ts_&(m.bs>=.9)
P('### F. robustness of buy-share>=0.9 signal')
d=m[hi]
P(('events',len(d),'tokens',d.tid.nunique()))
P(d[['r_bar','tn','tv','volume','age','vratio']].describe().round(3))
P(('coverage tv/volume median',(d.tv/d.volume).median(),'in all ts_ bars',(m.tv/m.volume)[ts_].median()))
P(('sells count in hi bars', d.sn.describe().round(2).to_dict()))
# winsor variants
for cap in (10,3,1,0.5):
    mm=m.copy()
    for h in ('l1','l4'): mm[h]=mm[h].clip(upper=cap)
    r1=L.row(hi,'l1',mm,f'cap {cap}'); r4=L.row(hi,'l4',mm,f'cap {cap}')
    P((cap,'l1 net %.2f [%.2f,%.2f] med %.2f | l4 net %.2f [%.2f,%.2f]'%(r1['net']*100,r1['n_lo']*100,r1['n_hi']*100,r1['med']*100,r4['net']*100,r4['n_lo']*100,r4['n_hi']*100)))
# drop top 1/3/5 events
for k in (3,10,20):
    idx=d.l4.dropna().sort_values(ascending=False).index[:k]
    mk=hi&~m.index.isin(idx)
    r=L.row(mk,'l4',m,'drop top%d'%k); P(('l4 drop top',k,'net %.2f [%.2f,%.2f] t=%.2f'%(r['net']*100,r['n_lo']*100,r['n_hi']*100,r['t_n'])))
    idx=d.l1.dropna().sort_values(ascending=False).index[:k]
    r=L.row(hi&~m.index.isin(idx),'l1',m,'x'); P(('l1 drop top',k,'net %.2f [%.2f,%.2f] t=%.2f'%(r['net']*100,r['n_lo']*100,r['n_hi']*100,r['t_n'])))
# first event per token
first=hi&(m.groupby('tid').cumcount()==m[hi].groupby('tid').cumcount().reindex(m.index).where(hi).fillna(-1)) 
fe=m[hi].groupby('tid').head(1).index
mk=m.index.isin(fe)&hi
P(table([('first hi-bs event per token',mk)],hs=('l1','l4','l16')))
P(table([('bs>=.9 tn>=20',hi&(m.tn>=20)),('bs>=.9 tn>=10 & tn<20',hi&(m.tn<20)),('bs>=.95',ts_&(m.bs>=.95)),('bs>=.8',ts_&(m.bs>=.8)),('bs>=.9 & tv>=5k',hi&(m.tv>=5000)),('bs>=.9 & rbar<=0.05',hi&(m.r_bar<=.05)),('bs>=.9 & rbar>.05',hi&(m.r_bar>.05)),('bs>=.9 coverage>=.3',hi&(m.tv/m.volume>=.3)),('bs>=.9 coverage<.3',hi&(m.tv/m.volume<.3))],hs=('l1','l4')))
P('strict horizons'); P(table([('bs>=.9',hi)],hs=('f1','f4','f16')))
# imbalance as continuous: deciles by train thresholds -> test
tr=ts_&~m.test
q=np.quantile(m.bs[tr],[.2,.4,.6,.8])
P(('train quintile cuts',q.round(3)))
edges=[-1]+list(q)+[2]
P(table([(f'bs Q{i+1} [{edges[i]:.2f},{edges[i+1]:.2f})',ts_&(m.bs>edges[i])&(m.bs<=edges[i+1])) for i in range(5)],hs=('l1','l4'),split=True))
# short-side cost for UP50 (not realistically tradable): pnl = -gross - cost
def short(sig,h):
    d=m.loc[sig&m[h].notna(),[h,'tid']]; x=-d[h].clip(upper=10).values-L.COST
    mu,lo,hi_,t,T=L.boot_mean(x,d.tid.values); return mu,lo,hi_,t,len(d)
P('### short side (hypothetical, no borrow/funding/availability, 2.5% cost): pnl=-ret-2.5%')
for lab,sg in [('UP>=+50% vol>=1k',(m.age>=2)&m.active&(m.volume>=1000)&(m.r_bar>=.5)),('UP>=+30% vol>=1k',(m.age>=2)&m.active&(m.volume>=1000)&(m.r_bar>=.3)),('bs<.3',ts_&(m.bs<.3))]:
    for h in ('l1','l4','l16'):
        mu,lo,hi_,t,n=short(sg,h); P((lab,h,n,'net %.2f [%.2f,%.2f] t=%.2f'%(mu*100,lo*100,hi_*100,t)))
# paired excess vs baseline for DN30 reversal, UP50 momentum (l1,l4)
P('### excess over same-age-bucket baseline (vol>=1k) via age-matched weights')
base=(m.age>=2)&m.active&(m.volume>=1000)
m['ageb']=pd.cut(m.age,[1,3,7,23,5000],labels=False)
for lab,sg in [('UP50',base&(m.r_bar>=.5)),('DN30',base&(m.r_bar<=-.3))]:
    for h in ('l1','l4','l16'):
        d=m.loc[sg&m[h].notna()]
        bm=m.loc[base&m[h].notna()].groupby('ageb')[h].mean()
        ex=(d[h]-d.ageb.map(bm)).values
        mu,lo,hi_,t,T=L.boot_mean(ex,d.tid.values); P((lab,h,len(d),'excess vs age-matched baseline %.2f [%.2f,%.2f] t=%.2f'%(mu*100,lo*100,hi_*100,t)))
open('/home/user/Detour/backtest/out/ll_part4.txt','w').write('\n'.join(out))
