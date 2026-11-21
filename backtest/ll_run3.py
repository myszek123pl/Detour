import sys; sys.path.insert(0,'/home/user/Detour/backtest')
import ll_lib as L, numpy as np, pandas as pd
pd.set_option('display.width',250); pd.set_option('display.max_columns',30); pd.set_option('display.max_rows',400)
m=pd.read_pickle('/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/ll_m.pkl')
out=[]
def P(t): print(t,flush=True); out.append(str(t))
cols=['rule','h','N','ntok','gross','med','g_lo','g_hi','t_g','net','n_lo','n_hi','t_n','win']
def table(rules,hs=('l1','l4','l16'),split=False):
    rows=[]
    for lab,sig in rules:
        for h in hs:
            if split:
                for nm,mk in (('ALL',sig),('PRE',sig&~m.test),('TEST',sig&m.test)): rows.append(L.row(mk,h,m,f'{lab} [{nm}]'))
            else: rows.append(L.row(sig,h,m,lab))
    d=pd.DataFrame(rows); d=d[[c for c in cols if c in d.columns]]
    return L.fmt(d).to_string(index=False)
gb=m.groupby('tid')
el=(m.age>=8)&m.active; v1k=el&(m.volume>=1000)
P('### C. volume spike (vratio = vol / mean vol prior 8 bars; age>=8, vol>=1k)')
for lab,dirc in [('up bar (+5%..)',(m.r_bar>.05)),('down bar (..-5%)',(m.r_bar<-.05)),('flat bar',m.r_bar.abs()<=.05)]:
    P(table([(f'{lab} vratio<1',v1k&dirc&(m.vratio<1)),(f'{lab} vratio 1-3',v1k&dirc&(m.vratio>=1)&(m.vratio<3)),(f'{lab} vratio 3-10',v1k&dirc&(m.vratio>=3)&(m.vratio<10)),(f'{lab} vratio>=10',v1k&dirc&(m.vratio>=10))]))
P('### C2 spike with split'); P(table([('up&vr>=5',v1k&(m.r_bar>.05)&(m.vratio>=5)),('down&vr>=5',v1k&(m.r_bar<-.05)&(m.vratio>=5))],split=True))
P('### C3 lead-lag cross-correlation (active bars, age>=8). corr(x_t, y_{t+k}); winsorised')
m['rw']=L.wins(m.c2c.where(m.age>=2),0.01); m['arw']=m.rw.abs(); m['dlvw']=L.wins(m.dlv.where(m.age>=2),.01)
rows=[]
for k in (-4,-3,-2,-1,0,1,2,3,4):
    sh=gb.rw.shift(-k); sha=gb.arw.shift(-k)
    act=m.active&(gb.active.shift(-k).fillna(False).astype(bool))&(m.age>=8)&(m.volume>=100)
    a=act&m.dlvw.notna()&sh.notna()
    r1,l1,h1,n1=L.corr_cluster(m.dlvw[a].values,sh[a].values,m.tid[a].values,B=300)
    r2,l2,h2,n2=L.corr_cluster(m.dlvw[a].values,sha[a].values,m.tid[a].values,B=300)
    rows.append(dict(k=k,rho_dlogvol_vs_ret=round(r1,4),ci=(round(l1,3),round(h1,3)),rho_dlogvol_vs_absret=round(r2,4),ci2=(round(l2,3),round(h2,3)),n=n1))
P(pd.DataFrame(rows))
P('### D. buy share (tv>=1k, trades>=10 in bar; age>=2)')
ts_=m.active&(m.tv>=1000)&(m.tn>=10)&(m.age>=2)
P(('bar count',ts_.sum(),'tokens',m.tid[ts_].nunique(),'share of vol>=1k bars',round(ts_.sum()/((m.active&(m.volume>=1000)&(m.age>=2)).sum()),3)))
P(m.bs[ts_].describe())
bb=[(0,.3),(.3,.5),(.5,.7),(.7,.9),(.9,1.001)]
P(table([(f'bs [{a},{b})',ts_&(m.bs>=a)&(m.bs<b)) for a,b in bb]))
P('#### D2 buy share conditional on bar direction')
for lab,dirc in [('up>5%',m.r_bar>.05),('down<-5%',m.r_bar<-.05),('flat',m.r_bar.abs()<=.05)]:
    P(table([(f'{lab} bs<.4',ts_&dirc&(m.bs<.4)),(f'{lab} bs .4-.7',ts_&dirc&(m.bs>=.4)&(m.bs<.7)),(f'{lab} bs>=.7',ts_&dirc&(m.bs>=.7))],hs=('l1','l4')))
P('#### D3 split'); P(table([('bs>=.9',ts_&(m.bs>=.9)),('bs<.3',ts_&(m.bs<.3))],split=True,hs=('l1','l4')))
P('#### D4 buy-share cross-corr with returns (trade bars)')
m['imbw']=m.imb
rows=[]
for k in (-2,-1,0,1,2,4):
    sh=gb.rw.shift(-k)
    a=ts_&sh.notna()&m.rw.notna()&(gb.tv.shift(-k)>0)
    r,lo,hi,n=L.corr_cluster(m.imbw[a].values,sh[a].values,m.tid[a].values,B=300)
    rows.append(dict(k=k,rho=round(r,4),lo=round(lo,4),hi=round(hi,4),n=n))
P(pd.DataFrame(rows))
# regression: fwd1 ~ r_bar + imb + dlv  (cluster-robust)
def ols_cluster(y,X,tid,names):
    X=np.column_stack([np.ones(len(y)),X]); XtXi=np.linalg.inv(X.T@X); b=XtXi@X.T@y; e=y-X@b
    u,inv=np.unique(tid,return_inverse=True); sc=np.zeros((len(u),X.shape[1])); np.add.at(sc,inv,X*e[:,None])
    V=XtXi@(sc.T@sc)@XtXi*len(u)/(len(u)-1); se=np.sqrt(np.diag(V))
    return pd.DataFrame({'coef':b,'se':se,'t':b/se},index=['const']+names).round(4)
P('#### D5 regression  l1 (clipped -1..3) ~ rbar_t + imb_t + dlogvol_t, trade bars')
d=m[ts_&m.l1.notna()&m.dlv.notna()]
y=d.l1.clip(-1,3).values; X=np.column_stack([d.r_bar.clip(-.95,3),d.imb,d.dlv.clip(-5,5)])
P(ols_cluster(y,X,d.tid.values,['rbar','imb','dlogvol']))
d=m[ts_&m.l4.notna()&m.dlv.notna()]
y=d.l4.clip(-1,3).values; X=np.column_stack([d.r_bar.clip(-.95,3),d.imb,d.dlv.clip(-5,5)])
P('l4'); P(ols_cluster(y,X,d.tid.values,['rbar','imb','dlogvol']))
d=m[el&m.l1.notna()&m.dlv.notna()&(m.volume>=1000)]
y=d.l1.clip(-1,3).values; X=np.column_stack([d.r_bar.clip(-.95,3),d.dlv.clip(-5,5),np.log(d.volume)])
P('all bars vol>=1k l1 ~ rbar + dlogvol + logvol'); P(ols_cluster(y,X,d.tid.values,['rbar','dlogvol','logvol']))
P('### E. breakout after consolidation (prior 8 closes range<=25%, age>=8, vol>=1k)')
cons=v1k&(m.prange<=.25)
P(table([('consolidating, no breakout (|brk|<5%)',cons&(m.brk.abs()<.05)),
         ('breakout brk>=10%',cons&(m.brk>=.10)),
         ('breakout brk>=10% & vr>=3',cons&(m.brk>=.10)&(m.vratio>=3)),
         ('breakout brk>=25%',cons&(m.brk>=.25)),
         ('breakout brk>=25% & vr>=3',cons&(m.brk>=.25)&(m.vratio>=3)),
         ('breakdown brk<=-10% (prior min)',cons&(m.close/m.pmin-1<=-.10))]))
P('#### E2 split'); P(table([('breakout brk>=10% & vr>=3',cons&(m.brk>=.10)&(m.vratio>=3)),('breakout brk>=25%',cons&(m.brk>=.25))],split=True))
P('#### E3 any-range new 8-bar high (non-consolidation) brk>=10% & vr>=3'); P(table([('new-high brk>=10% vr>=3',v1k&(m.brk>=.10)&(m.vratio>=3)&(m.prange>.25))]))
open('/home/user/Detour/backtest/out/ll_part3.txt','w').write('\n'.join(out))
