import numpy as np
rng=np.random.default_rng(7)
# ---------- CPMM, fee on input, fee stays in pool (Raydium/Uni v2 style) ----------
def buy(R,y,P,f):
    pf=P*(1-f); Rn=R+P; yn=R*y/(R+pf); return Rn,yn,y-yn   # (R',y',tokens)  (fee stays in R)
def sell(R,y,t,f):
    tf=t*(1-f); yn=y+t; out=R*tf/(y+tf); return R-out,yn,out
def rt(P,R,f,mode="reset",flow=0.0,drift=0.0,fixed=0.0):
    """Round-trip cost fraction of P.  y0 = 1 (token units normalised).
    mode 'persist': pool left as our buy left it (nobody trades) -> cost = fees only
    mode 'reset'  : fair price unchanged; arb/other flow restores pool to entry reserves before we sell (impact paid both ways)
    flow: other traders' net quote flow (+buy/-sell) as fraction of R, applied to the pool before our exit
    drift: fair-price change (+ up) applied before exit (pool reshaped at constant k)"""
    R0,y0=R,1.0
    R1,y1,tok=buy(R0,y0,P,f)
    if mode=="reset": Rx,yx=R0,y0
    else: Rx,yx=R1,y1
    if flow:
        d=flow*Rx; Rn=Rx+d; yx=Rx*yx/Rn; Rx=Rn
    if drift:
        k=Rx*yx; p=Rx/yx*(1+drift); yx=np.sqrt(k/p); Rx=np.sqrt(k*p)
    _,_,out=sell(Rx,yx,tok,f)
    return 1-out/P+fixed/P
def maxpos(c,R,f,**kw):
    lo,hi=0.0,R*50
    if rt(1e-6*R,R,f,**kw)>c: return 0.0
    for _ in range(100):
        m=(lo+hi)/2
        (lo,hi)=(m,hi) if rt(m,R,f,**kw)<=c else (lo,m)
    return lo
# ---------- pump.fun curve ----------
VS0,VT0=30.0,1.073e9
def pump(P_usd,real_sol,fee,sol=150.0,mode="reset"):
    vs=VS0+real_sol; k=VS0*VT0; vt=k/vs
    P=P_usd/sol; pf=P*(1-fee)      # fee leaves the curve (protocol+creator)
    vs2=vs+pf; vt2=k/vs2*0+vs*vt/vs2; tok=vt-vt2
    if mode=="reset": vsx,vtx=vs,vt
    else: vsx,vtx=vs2,vt2
    vt3=vtx+tok; vs3=vsx*vtx/vt3; out=(vsx-vs3)*(1-fee)
    return 1-out/P
def pmax(c,real,fee,mode="reset"):
    lo,hi=0.0,1e7
    if pump(1e-3,real,fee,mode=mode)>c: return 0.0
    for _ in range(100):
        m=(lo+hi)/2
        (lo,hi)=(m,hi) if pump(m,real,fee,mode=mode)<=c else (lo,m)
    return lo
if __name__=="__main__":
    f=0.0025
    print("## A. cost vs P/R (R=quote reserve, TVL=2R), f=0.25%/side")
    print("P/R | P/TVL | persist(fees only) | reset total | reset no-fee | approx 2P/R+2f")
    for r in [.001,.0025,.005,.01,.02,.05,.1,.2,.5,1]:
        print(f"{r:.4f} | {r/2*100:5.2f}% | {rt(r*1e5,1e5,f,'persist')*100:.2f}% | {rt(r*1e5,1e5,f)*100:6.2f}% | {rt(r*1e5,1e5,0)*100:6.2f}% | {(2*r+2*f)*100:6.2f}%")
    TV=[5e3,10e3,25e3,50e3,100e3,250e3,500e3,1e6]
    for f,fx in [(0.0025,0),(0.0025,2.0),(0.01,0)]:
        print(f"\n## B. max position, fee {f*100:.2f}%/side, fixed cost ${fx}, reset mode, TVL=2R")
        print("TVL | <3% | <5% | <10%")
        for t in TV:
            R=t/2; ps=[maxpos(c,R,f,fixed=fx) for c in (.03,.05,.10)]
            print(f"${t:,.0f} | "+" | ".join(f"${p:,.0f} ({p/t*100:.2f}%)" for p in ps))
    print("\n## B2. max position if cost budget is for IMPACT only (fees excluded), f=0.25%, TVL=2R: rt(f=0)")
    for t in TV:
        R=t/2; print(f"${t:,.0f} | "+" | ".join(f"${maxpos(c,R,0.0):,.0f}" for c in (.03,.05,.10)))
    print("\n## C. other flow MC: R=5e4 (TVL $100k), f=.25%, reset mode, flow ~ N(0,s) of R; pnl = -cost")
    R=5e4
    for P in [500,2500,5000]:
        for s in [0,.02,.05,.10]:
            fl=rng.normal(0,s,20000); c=np.array([rt(P,R,.0025,flow=x) for x in fl])
            print(f"P=${P} ({P/(2*R)*100:.1f}%TVL) sd={s*100:.0f}%R: mean cost={c.mean()*100:.2f}% | P(loss>cost floor+5%)={np.mean(c>.055)*100:.0f}% | 5th/95th pnl={-np.percentile(c,95)*100:.1f}%/{-np.percentile(c,5)*100:.1f}%")
    print("\n   deterministic sustained flow (R=5e4,P=1000): ")
    for fl in [-.1,-.05,-.02,0,.02,.05,.10]:
        print(f"   other net flow {fl*100:+.0f}%R: pnl={-rt(1000,5e4,.0025,flow=fl)*100:+.2f}%  (persist mode {-rt(1000,5e4,.0025,'persist',flow=fl)*100:+.2f}%)")
    print("\n## D. breakeven gross fair-price move (reset mode, f=.25%) ")
    for t in [10e3,50e3,250e3]:
        for pr in [.002,.01,.05,.10]:
            R=t/2;P=pr*t;lo,hi=-0.5,5
            for _ in range(80):
                m=(lo+hi)/2
                (lo,hi)=(m,hi) if rt(P,R,.0025,drift=m)>0 else (lo,m)
            print(f"TVL ${t:,.0f}, P ${P:,.0f} ({pr*100:.1f}%TVL): need +{hi*100:.2f}% in fair price | cost-at-flat={rt(P,R,.0025)*100:.2f}%")
    print("\n## E. pump.fun curve, SOL=$150, reset mode (price unchanged at exit) / persist = fees only")
    for fee in [.0125,.01]:
        print(f"fee {fee*100:.2f}%/side")
        for real in [0,10,30,60,85]:
            vq=(VS0+real)*150
            ps=[pmax(c,real,fee) for c in (.03,.05,.10)]
            cs=[pump(x,real,fee) for x in (100,500,2000)]
            print(f"real SOL {real:2d} (virt. quote ${vq:,.0f}; ~mcap ${ (VS0+real)**2/(VS0*VT0)*1e9*150/1e0:,.0f}): max P <3%: ${ps[0]:,.0f} | <5%: ${ps[1]:,.0f} | <10%: ${ps[2]:,.0f} || cost $100/$500/$2000 = {cs[0]*100:.2f}/{cs[1]*100:.2f}/{cs[2]*100:.2f}%")
