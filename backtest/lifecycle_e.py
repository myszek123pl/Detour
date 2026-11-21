import sys, numpy as np, pandas as pd
pd.set_option('display.width',250); pd.set_option('display.max_columns',60)
S=sys.argv[1]
z=np.load(S+'/panel_ok.npz'); Pf,Hf,Lf,V,E,P=z['Pf'],z['Hf'],z['Lf'],z['V'],z['E'],z['P']
keep=(Hf.max(1)/E<300); Pf,Hf,Lf,V,E,P=Pf[keep],Hf[keep],Lf[keep],V[keep],E[keep],P[keep]; n=len(Pf)
COST=0.10
def wm(r,cap=50): return np.minimum(r,cap).mean()
def summarize(r):
    return dict(n=len(r),mean_net=wm(r)-COST,mean_gross=wm(r),median=np.median(r),P_win=np.mean(r>1+COST),P_lt05=np.mean(r<.5),p10=np.percentile(r,10),p90=np.percentile(r,90))
# ---------------- exit-rule simulations, entry = close of bar 0 (conv B), path bars 1..96 (24h) or 288
def sim(sl=None,tp=None,trail=None,T=96,pess=False,half_at=None):
    E2=Pf[:,0]; H=Hf[:,1:T+1]/E2[:,None]; L=Lf[:,1:T+1]/E2[:,None]; C=Pf[:,1:T+1]/E2[:,None]
    ret=np.full(n,np.nan); done=np.zeros(n,bool); hi=np.ones(n); part=np.zeros(n); rem=np.ones(n)
    for k in range(T):
        act=~done
        # trailing stop level
        lvl=np.full(n,-1.0)
        if sl is not None: lvl=np.maximum(lvl,1-sl)
        if trail is not None: lvl=np.maximum(lvl,hi*(1-trail))
        # stop first (conservative)
        hit=act&(L[:,k]<=lvl)&(lvl>0)
        fill=np.where(pess&(C[:,k]<lvl),C[:,k],lvl) if pess else lvl
        if half_at is not None:
            # after half sold, remaining stop governed by trail only
            pass
        ret[hit]=(part+rem*fill)[hit]; done|=hit; act=~done
        if tp is not None:
            h2=act&(H[:,k]>=tp); ret[h2]=(part+rem*tp)[h2]; done|=h2; act=~done
        if half_at is not None:
            h3=act&(rem==1)&(H[:,k]>=half_at); part=np.where(h3,.5*half_at,part); rem=np.where(h3,.5,rem)
        hi=np.where(act,np.maximum(hi,H[:,k]),hi)
    ret[~done]=(part+rem*C[:,-1])[~done]
    return ret,done
rows=[]
def add(name,**kw):
    r,d=sim(**kw); s=summarize(r); s['exit_hit']=d.mean(); rows.append(dict(rule=name,**s))
add('hold 24h',T=96); add('hold 6h',T=24); add('hold 1h',T=4)
for sl in (.2,.3,.5):
    for tp in (None,1.5,2,3,5):
        add(f'SL-{int(sl*100)}% TP{"+"+str(int((tp-1)*100))+"%" if tp else " none"} 24h (stop at level)',sl=sl,tp=tp)
for sl in (.3,.5):
    add(f'SL-{int(sl*100)}% TP+100% 24h (PESSIMISTIC fill at bar close)',sl=sl,tp=2,pess=True)
for tr in (.2,.3,.5):
    add(f'trail -{int(tr*100)}% from high, no TP, 24h',trail=tr); add(f'trail -{int(tr*100)}% from high, no TP, 24h PESS',trail=tr,pess=True)
add('SL-30% + half off at 2x then trail 40% (approx: trail 40%, TP none) ',sl=.3,trail=.4,half_at=2)
add('SL-30%, sell half at 2x, other half trail 50%',sl=.3,trail=.5,half_at=2)
df=pd.DataFrame(rows); print(f'## Exit rules, entry=close of first candle (~15-25 min after detection), cost assumption {COST:.0%} RT, n={n}'); print(df.round(3).to_string(index=False),flush=True)

# ---------------- entry timing event studies (24h forward), cost 10%
R=Pf/E[:,None]; HR=Hf/E[:,None]; rm=np.maximum.accumulate(HR,axis=1)
def study(name,idx):
    # idx: list of (i,j) event bar; forward 24h
    rs=[];mx=[];sl30=[]
    for i,j in idx:
        if j+96>288: continue
        p0=Pf[i,j]
        if p0<=0: continue
        rs.append(Pf[i,j+96]/p0); mx.append(Hf[i,j+1:j+97].max()/p0)
        # SL-30 / TP+100 sim
        l=Lf[i,j+1:j+97]/p0; h=Hf[i,j+1:j+97]/p0; c=Pf[i,j+96]/p0
        a=np.where(l<=.7)[0]; b=np.where(h>=2)[0]
        ia=a[0] if len(a) else 999; ib=b[0] if len(b) else 999
        sl30.append(.7 if ia<=ib and ia<999 else (2.0 if ib<999 else c))
    rs=np.array(rs);mx=np.array(mx);sl30=np.array(sl30)
    return dict(event=name,n=len(rs),med_fwd24=np.median(rs),wmean_fwd24=wm(rs),P_fwd_gt1=np.mean(rs>1),P_fwd_lt05=np.mean(rs<.5),med_fwdmax=np.median(mx),P_fwdmax_ge2=np.mean(mx>=2),P_fwdmax_ge1_5=np.mean(mx>=1.5),SL30_TP100_mean_net=wm(sl30)-COST)
ev=[]
ev.append(study('baseline: buy first-candle close',[(i,0) for i in range(n)]))
ev.append(study('buy at +1h (bar 4), any token',[(i,4) for i in range(n)]))
ev.append(study('buy at +1h only if price in 0.8-1.5x entry & traded last 2 bars',[(i,4) for i in range(n) if 0.8<=R[i,4]<=1.5 and not np.isnan(P[i,3:5]).any()]))
ev.append(study('buy at +6h if traded last 2 bars',[(i,24) for i in range(n) if not np.isnan(P[i,23:25]).any()]))
def first(cond):
    out=[]
    for i in range(n):
        w=np.where(cond(i))[0]
        if len(w): out.append((i,w[0]))
    return out
ev.append(study('momentum: first CLOSE >=2x entry',first(lambda i:R[i]>=2)))
ev.append(study('momentum: first CLOSE >=1.5x entry',first(lambda i:R[i]>=1.5)))
ev.append(study('momentum: first CLOSE >=3x entry',first(lambda i:R[i]>=3)))
ev.append(study('dip: -30% from running peak (peak>=2x)',first(lambda i:(R[i]<=.7*rm[i])&(rm[i]>=2))))
ev.append(study('dip: -50% from running peak (peak>=2x)',first(lambda i:(R[i]<=.5*rm[i])&(rm[i]>=2))))
ev.append(study('dip: -70% from running peak (peak>=2x)',first(lambda i:(R[i]<=.3*rm[i])&(rm[i]>=2))))
ev.append(study('dip: -50% from peak (peak>=1.3x) ',first(lambda i:(R[i]<=.5*rm[i])&(rm[i]>=1.3))))
ev.append(study('falling knife: first close <=0.5x entry (any)',first(lambda i:R[i]<=.5)))
ev.append(study('falling knife: first close <=0.3x entry (any)',first(lambda i:R[i]<=.3)))
ev.append(study('reclaim: after -50% from peak>=2x, first bar close +30% above post-drop low',[(i,j) for i,j in [ (i,w) for i,w in [] ]]) if False else study('dummy',[]) ) if False else None
print('\n## Entry timing event studies (forward 24h; entry at event-bar close; cost 10% in last column only)'); print(pd.DataFrame([e for e in ev if e]).round(3).to_string(index=False),flush=True)
