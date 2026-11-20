"""Monte Carlo of memecoin bot strategies. ALL parameters are ASSUMPTIONS (see note)."""
import numpy as np, json, sys
T = 120  # steps per trade (1 step ~ 15 s => 30 min max hold)

# ---------- token class definitions: (prob, peak_lo, peak_hi, tp_lo, tp_hi, fin_lo, fin_hi (as fraction of peak OR abs), rug_prob)
def classes_random(grad=0.008, moon=0.0005):
    near, mid = 0.03, 0.12
    bleed = 0.28
    rug = 1 - (grad+moon+near+mid+bleed)
    # name, p, peak range, time-to-peak range, final multiple range (abs, of entry), rug-jump prob
    return [("rug/dead",rug,(0.95,1.5),(2,15),(0.02,0.15),0.6),
            ("bleed",bleed,(1.05,2.0),(5,30),(0.10,0.50),0.05),
            ("midpump",mid,(2.0,6.0),(10,50),(0.10,0.45),0.10),
            ("nearmiss",near,(6.0,12.0),(20,70),(0.10,0.50),0.10),
            ("graduate",grad,(10.0,25.0),(30,90),(0.35,3.0),0.05),
            ("moon",moon,(40.0,300.0),(40,110),(2.0,40.0),0.0)]
def classes_postgrad():
    return [("instant dump",0.40,(1.0,1.3),(1,6),(0.15,0.6),0.10),
            ("fade",0.33,(1.1,1.6),(3,20),(0.4,0.85),0.02),
            ("2x cont",0.15,(2.0,3.0),(10,50),(0.5,1.6),0.0),
            ("5x cont",0.08,(4.0,8.0),(20,80),(0.8,3.5),0.0),
            ("20x+",0.034,(12.0,60.0),(30,100),(2.0,15.0),0.0),
            ("100x",0.006,(60.0,300.0),(40,110),(5.0,60.0),0.0)]

def apply_edge(cls, u):
    """EDGE ASSUMPTION: multiply probability of every non-dead/bleed/'instant dump'/'fade' class by u (right-tail hit-rate uplift);
    mass taken proportionally from the two worst classes."""
    c=[list(x) for x in cls]
    good=[i for i in range(2,6)]
    add=0
    for i in good:
        add+= c[i][1]*(u-1); c[i][1]*=u
    bad=c[0][1]+c[1][1]
    for i in (0,1): c[i][1]-= add*c[i][1]/bad
    assert min(x[1] for x in c)>0, "uplift too large"
    return [tuple(x) for x in c]

def gen_tokens(cls, n, rng):
    p=np.array([c[1] for c in cls]); p=p/p.sum()
    k=rng.choice(len(cls), size=n, p=p)
    pk=np.empty(n); tp=np.empty(n,int); fin=np.empty(n); rug=np.zeros(n,bool)
    for i,c in enumerate(cls):
        m=k==i; s=m.sum()
        pk[m]=np.exp(rng.uniform(np.log(c[2][0]),np.log(c[2][1]),s))
        tp[m]=rng.integers(c[3][0],c[3][1]+1,s)
        fin[m]=np.exp(rng.uniform(np.log(c[4][0]),np.log(c[4][1]),s))
        rug[m]=rng.random(s)<c[5]
    # log path: 0 -> log pk at tp -> log fin at T-1
    t=np.arange(T)[None,:]
    tpc=tp[:,None]
    lp=np.where(t<=tpc, np.log(pk)[:,None]*t/tpc, np.log(pk)[:,None]+(np.log(fin)-np.log(pk))[:,None]*(t-tpc)/(T-1-tpc))
    sig=0.05
    z=rng.normal(0,sig,(n,T)); z[:,0]=0
    w=np.cumsum(z,axis=1); w-= (t/(T-1))*w[:,-1:]     # bridge noise
    lp=lp+w
    # rug: one-step collapse to 3-8% of price at random time after peak (dev dumps / LP pulled)
    rt=np.minimum(tp+rng.integers(1,25,n),T-2)
    drop=np.log(rng.uniform(0.03,0.10,n))
    mask=rug[:,None]&(t>=rt[:,None])
    lp=lp+np.where(mask,drop[:,None],0.0)
    return np.exp(lp), k

def run_trades(cls, n, rng, policy, cost, label=""):
    """Return per-attempt arrays: mult on stake (net of % fees/slippage), fixed SOL cost per 1 SOL position? -> fixed in SOL."""
    P,k=gen_tokens(cls,n,rng)
    stop=policy["stop"]; ladder=policy["ladder"]; trail=policy.get("trail",None)
    pos_sol=cost["pos_sol"]
    # entry: delay drift (adverse) + buy slippage + fee
    delay=np.exp(rng.normal(cost["delay_mu"],cost["delay_sd"],n)); delay=np.maximum(delay,1.0)
    buy_ok=rng.random(n)>cost["p_buy_fail"]
    entry_eff=P[:,0]*delay*(1+cost["slip_in"])   # P[:,0]==1
    # tokens received per SOL = (1-fee)/entry_eff
    tok=(1-cost["fee_in"])/entry_eff
    rem=np.ones(n)               # fraction of tokens remaining
    cash=np.zeros(n); fixed=np.full(n,cost["tip"]); legs=np.zeros(n)
    peak=np.full(n,delay)        # peak price seen post entry (relative to token start price 1)
    done=np.zeros(n,bool)
    lad_hit=np.zeros((n,len(ladder)),bool)
    pend=np.zeros(n,bool)        # pending failed sell -> retry next step
    for s in range(1,T):
        px=P[:,s]; act=~done
        peak=np.where(act,np.maximum(peak,px),peak)
        rel=px/entry_eff          # multiple vs effective entry
        # decide sell fraction at this step
        frac=np.zeros(n)
        stop_trig=(rel<=1-stop)
        if trail is not None:
            armed=lad_hit[:,0] if len(ladder) else np.ones(n,bool)
            stop_trig=stop_trig | (armed & (px<=peak*(1-trail)))
        for j,(lvl,fr) in enumerate(ladder):
            h=(~lad_hit[:,j])&(rel>=lvl)&act
            frac=np.where(h,np.maximum(frac,0),frac)
            # sell fr of ORIGINAL position at lvl (cap by rem)
            sell=np.where(h,np.minimum(fr,rem),0.0)
            lad_hit[:,j]|=h
            # fail?
            fail=rng.random(n)<cost["p_sell_fail"]
            ok=h&~fail
            gross=sell*tok*px*(1-cost["slip_tp"])*(1-cost["fee_out"])
            cash+=np.where(ok,gross,0); rem-=np.where(ok,sell,0); legs+=ok
            lad_hit[:,j]&=ok|lad_hit[:,j]  # failed -> still marked; accept (simplification: retry not modelled for TP)
            lad_hit[:,j]=np.where(h&fail,False,lad_hit[:,j])
        # stop / time-exit full sell of remaining
        last=(s==T-1)
        full=(stop_trig|last|pend)&act&(rem>1e-9)
        failp=np.where(rel<0.5,cost["p_sell_fail_dump"],cost["p_sell_fail"])
        fail=(rng.random(n)<failp)&(not last)
        ok=full&~fail
        sl=cost["slip_stop"]
        gross=rem*tok*px*(1-sl)*(1-cost["fee_out"])
        cash+=np.where(ok,gross,0); legs+=ok
        rem=np.where(ok,0.0,rem); done|=ok&(rem<=1e-9)
        pend=full&fail
        done|=(rem<=1e-9)
    mult=cash   # per 1 SOL staked (percent costs embedded)
    fixed=fixed+legs*cost["tip"]
    mult=np.where(buy_ok,mult,1.0)
    fixed=np.where(buy_ok,fixed,cost["fail_fee"])
    return mult, fixed, k

def stats_lib(mult,fixed,pos_sol):
    net=(mult-1)-fixed/pos_sol
    return net.mean(), np.median(net), (net>0).mean(), net

def equity_paths(mult,fixed,f,rng,n_paths=10000,n_trades=300,eq0=10.0,pos_cap=None):
    N=len(mult); eq=np.full(n_paths,eq0); peak=eq.copy(); mdd=np.zeros(n_paths)
    ruin=np.zeros(n_paths,bool); ruin_lvl=0.25*eq0
    for _ in range(n_trades):
        i=rng.integers(0,N,n_paths)
        pos=f*eq
        if pos_cap: pos=np.minimum(pos,pos_cap)
        eq=eq+pos*(mult[i]-1)-fixed[i]
        eq=np.maximum(eq,0)
        peak=np.maximum(peak,eq); mdd=np.maximum(mdd,1-eq/peak)
        ruin|=eq<=ruin_lvl
    return eq/eq0, mdd, ruin

def summarize(name,eqrel,mdd,ruin):
    return dict(name=name,mean=float(eqrel.mean()),median=float(np.median(eqrel)),p5=float(np.percentile(eqrel,5)),p95=float(np.percentile(eqrel,95)),
        P_up=float((eqrel>1).mean()),P_ruin75=float(ruin.mean()),med_mdd=float(np.median(mdd)),P_dd50=float((mdd>0.5).mean()))
