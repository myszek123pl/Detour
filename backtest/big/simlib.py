"""Conditional pump.fun reserve-path replay; not verified on-chain execution.
All state arrays are per-token, time-sorted. Reserves in SOL / tokens (not lamports / micro units).
Conventions
- decision at trade index i (information up to and including trade i observed at t[i]);
- order fills at state idx_at(t[i]+latency)  (the last recorded state at or before that time);
- own impact is an additive counterfactual approximation; other traders do not react;
- missing terminal coverage is censored, never a forced sale or inferred failure;
- buy fee is charged on top of net SOL: net SOL = budget/(1+fee), a float
  approximation omitting the SDK one-lamport subtraction and integer flooring;
- the historical fee RATE is a scenario assumption, not inferred from this formula;
- optional fee_model="deducted" reproduces the legacy approximation; sell fee
  is deducted from proceeds and tips are additional per transaction.
"""
import numpy as np, pandas as pd, duckdb
K0 = 30.0*1073e6          # standard curve invariant (SOL*tokens)
VS0 = 30.0
VS_GRAD = 115.0054        # virtual SOL at completion (85 real SOL)
VT_GRAD = K0/VS_GRAD
P_GRAD = VS_GRAD/VT_GRAD  # SOL per token at completion
POOL_Q, POOL_B = 85.0, 206.9e6   # PumpSwap pool reserves at migration (measured)
POOL_FEE = 0.01725        # measured lp+creator+buyback fee
SOLUSD = 70.0

FILES={'jocry':('tok_jocry2.parquet','paths_jocry.parquet','postgrad_jocry.parquet'),'oct':('oct_tok.parquet','oct_paths.parquet','oct_postgrad.parquet')}
def load(S, mayhem=None, tmin=None, tmax=None, src='jocry'):
    con = duckdb.connect()
    ft,fp,fg = FILES[src]
    tk = con.sql(f"select * from read_parquet('{S}/work/{ft}') order by mid").df()
    if mayhem is not None: tk = tk[tk.mh==mayhem]
    if tmin is not None: tk = tk[tk.L>=tmin]
    if tmax is not None: tk = tk[tk.L<tmax]
    mids = tk.mid.values
    df = con.sql(f"select mid,t,b,sol,vs,vt,wid,is_sys from read_parquet('{S}/work/{fp}')").df()
    df = df[df.mid.isin(set(mids.tolist()))]
    df = df.sort_values(['mid','t'], kind='stable')
    pg = con.sql(f"select * from read_parquet('{S}/work/{fg}') order by mid, ssg").df()
    return tk.reset_index(drop=True), df.reset_index(drop=True), pg

class Paths:
    def __init__(self, tk, df, pg):
        self.tk = tk
        self.mid = df.mid.values; self.t = df.t.values.astype('f8')
        self.b = df.b.values.astype(bool); self.sol = df.sol.values.astype('f8')
        self.vs = df.vs.values.astype('f8'); self.vt = df.vt.values.astype('f8')
        self.wid = df.wid.values.astype('i8'); self.sys = df.is_sys.values.astype(bool)
        u, st = np.unique(self.mid, return_index=True)
        en = np.r_[st[1:], len(self.mid)]
        self.rng = {int(m):(int(s),int(e)) for m,s,e in zip(u,st,en)}
        self.tkd = tk.set_index('mid')
        # postgraduation snapshots: dict mid -> (ssg array, price array)
        self.pg = {}
        self.pg_reserves = {}
        pgm = pg[pg.mid.isin(set(tk.mid.tolist()))]
        for m,g in pgm.groupby('mid'):
            self.pg[int(m)] = (g.ssg.values, g.price_native.values)
            if {'liquidity_quote', 'liquidity_base'} <= set(g.columns):
                self.pg_reserves[int(m)] = (g.ssg.values, g.liquidity_quote.values,
                                            g.liquidity_base.values)
    def tok(self, m):
        """returns dict of per-token arrays truncated at completion/graduation (curve path only)"""
        s,e = self.rng[m]
        r = self.tkd.loc[m]
        t = self.t[s:e]; vs = self.vs[s:e]; vt = self.vt[s:e]
        G = float(r.G) if not pd.isna(r.G) else None
        end = len(t)
        done = np.nonzero(vs >= 114.5)[0]
        if len(done): end = done[0]+1
        elif G is not None: end = int(np.searchsorted(t, G, side='right'))
        end = max(end, 0)
        out = dict(t=t[:end], vs=vs[:end], vt=vt[:end], b=self.b[s:e][:end], sol=self.sol[s:e][:end],
                   wid=self.wid[s:e][:end], sys=self.sys[s:e][:end], L=r.L, G=G, mh=bool(r.mh),
                   grad=(G is not None), meta=r)
        return out

def idx_at(t, tq):
    """index of last state at or before tq (>=0) ; -1 if none"""
    return int(np.searchsorted(t, tq, side='right'))-1

def buy(vs, vt, X, fee, fee_model='on_top'):
    if fee_model not in ('deducted', 'on_top'): raise ValueError('unknown buy fee model')
    xin = X*(1-fee) if fee_model=='deducted' else X/(1+fee)
    y = vt*xin/(vs+xin)
    return xin, y

def sell_value(vsA, vtA, y, fee, tip=0.0):
    return vsA*y/(vtA+y)*(1-fee) - tip

def pool_exit(y, ratio, fee=POOL_FEE, tip=0.0):
    """sell y tokens into the migrated pool; price = ratio * P_GRAD (before impact)"""
    q = POOL_Q*ratio; b = POOL_B
    return q*y/(b+y)*(1-fee) - tip

def pool_ratio(P, m, lat, mode='own'):
    if mode=='fixed': return 0.86 if lat<20 else 1.0
    v = P.pg.get(m)
    if v is None: return np.nan
    ssg, px = v
    # A future snapshot cannot price an earlier order. Missing coverage stays
    # missing; the explicit 'fixed' mode is only a sensitivity assumption.
    k = idx_at(ssg, lat)
    if k < 0: return np.nan
    return float(px[k]/P_GRAD)

def entry(tokd, i_dec, lat, X, fee, tip, t_dec=None, vs_cap=112.0, max_state_age=30.0, fee_model='on_top'):
    """returns None if no fill, else dict(j, y, xin, ds, dt, px_avg, cost)"""
    t = tokd['t']; n = len(t)
    if not n: return None
    if not np.isfinite(lat) or lat < 0: raise ValueError('latency must be finite and non-negative')
    if not 0 <= i_dec < n or not np.isfinite(t).all() or np.any(np.diff(t)<0): return None
    td = t[i_dec] if t_dec is None else t_dec
    if not np.isfinite(td) or td < t[i_dec]: return None
    tf = td+lat
    if tf > t[-1] or tf < t[0]: return None
    G = tokd['G']
    if tokd['grad'] and G is not None and tf >= G: return None
    j = idx_at(t, tf)
    if j < i_dec: j = i_dec
    if j >= n: j = n-1
    vs, vt = tokd['vs'][j], tokd['vt'][j]
    if not np.isfinite([vs, vt, X, fee, tip]).all() or vs<=0 or vt<=0 or X<=0 or not 0<=fee<1 or tip<0: return None
    if max_state_age is not None and tf-t[j]>max_state_age: return None
    if vs_cap is not None and vs > vs_cap: return None   # curve (almost) complete -> buy would overflow / fail
    xin, y = buy(vs, vt, X, fee, fee_model)
    if vs_cap is not None and vs+xin>=VS_GRAD: return None
    return dict(j=j, y=y, xin=xin, ds=xin, dt=y, px=xin/y,
                tf=tf, state_t=t[j], cost=X+tip, vs0=vs)

def exit_sim(P, m, tokd, e, spec, lat, fee, tip, X, pool_mode='own'):
    """Return (net_return, kind, executed_sell_count).

    NaN means unresolved, not zero return. Timers use the entry execution
    clock; one sell is pending at a time. No signal from before that fill is
    replayed. max_state_age/max_pool_age default to 30 seconds and are
    explicit observation-staleness assumptions, not proof of capture uptime.
    Pool 'own' uses observed base/quote reserves; 'fixed' and 'price_approx'
    are explicit sensitivity modes. Every pool route is snapshot-based.
    """
    if not np.isfinite(lat) or lat < 0: raise ValueError('latency must be finite and non-negative')
    if not np.isfinite([fee,tip]).all() or not 0<=fee<1 or tip<0:
        raise ValueError('invalid exit costs')
    if e is None: return np.nan, 'invalid_entry', 0
    t,vs,vt = tokd['t'],tokd['vs'],tokd['vt']; n=len(t)
    if not n: return np.nan, 'censored', 0
    y0=e['y']; y=y0; ds=e['ds']; dt=e['dt']; px=e['px']; cash=0.0
    pos=e['j']; clock=e['tf']; start_clock=clock; peak=0.0; ntx=0
    if not 0 <= pos < n or clock>t[-1]: return np.nan, 'censored', 0
    tps=sorted(spec.get('tps') or [], key=lambda z:z[0]); ntp=0
    if any(not (0<f<=1 and level>0) for level,f in tps):
        raise ValueError('invalid take-profit schedule')
    sl=spec.get('sl'); trail=spec.get('trail'); arm=spec.get('arm',1.0)
    horizon=spec.get('tmax'); deadline=None if horizon is None else start_clock+horizon
    if horizon is not None and (not np.isfinite(horizon) or horizon<0): raise ValueError('invalid holding time')
    age=spec.get('max_state_age',30.0); pool_age=spec.get('max_pool_age',30.0)
    G=tokd.get('G'); G=None if G is None or not np.isfinite(G) else G
    while y>1e-9:
        # Candidate signals only from states strictly after the last fill.
        st=pos+1
        a=vs[st:]+ds; b=vt[st:]-dt
        valid=np.isfinite(a)&np.isfinite(b)&(a>0)&(b>0)
        if not valid.all():
            bad=st+int(np.flatnonzero(~valid)[0])
        else: bad=n
        a=a[:bad-st]; b=b[:bad-st]; times=t[st:bad]
        mult=(a/b)/px
        candidates=[]
        if sl is not None:
            w=np.flatnonzero(mult<=sl)
            if len(w): candidates.append((float(times[w[0]]),st+int(w[0]),'sl'))
        if ntp<len(tps):
            w=np.flatnonzero(mult>=tps[ntp][0])
            if len(w): candidates.append((float(times[w[0]]),st+int(w[0]),'tp'))
        if trail is not None:
            pk=np.maximum.accumulate(np.maximum(mult,peak))
            w=np.flatnonzero((pk>=arm)&(mult<=pk*(1-trail)))
            if len(w): candidates.append((float(times[w[0]]),st+int(w[0]),'trail'))
        if deadline is not None:
            td=max(deadline,clock)
            if td<=t[-1] and (bad==n or td<t[bad]):
                candidates.append((float(td),max(pos,idx_at(t,td)),'time'))
        # A recorded graduation may trigger an explicit hold-to-migration
        # policy only when curve coverage reaches that event. Never infer it
        # merely because the metadata contain a later graduation timestamp.
        if spec.get('hold_grad',True) and G is not None and clock<=G<=t[-1]:
            if bad==n or G<t[bad]: candidates.append((float(G),idx_at(t,G),'grad'))
        if not candidates: return np.nan, 'censored', ntx
        td,k,trig=min(candidates,key=lambda z:(z[0],z[2]))
        te=td+lat
        if bad<n and t[bad]<=min(te,G if G is not None else te):
            return np.nan,'censored',ntx
        graduated=G is not None and te>=G
        if graduated:
            delay=te-G
            reserves=getattr(P,'pg_reserves',{}).get(m) if P is not None else None
            if pool_mode=='own':
                if reserves is None: return np.nan,'censored_pool',ntx
                ssg,q,bp=reserves; j=idx_at(ssg,delay)
                if j<0 or (pool_age is not None and delay-ssg[j]>pool_age):
                    return np.nan,'censored_pool',ntx
                qj,bj=float(q[j]),float(bp[j])
                if not np.isfinite([qj,bj]).all() or min(qj,bj)<=0:
                    return np.nan,'invalid_pool',ntx
                proceeds=qj*y/(bj+y)*(1-POOL_FEE)-tip
            elif pool_mode in ('fixed','price_approx'):
                if P is None: return np.nan,'censored_pool',ntx
                ratio=pool_ratio(P,m,delay,'fixed' if pool_mode=='fixed' else 'own')
                proceeds=pool_exit(y,ratio,POOL_FEE,tip)
            else: raise ValueError('unknown pool mode')
            if not np.isfinite(proceeds): return np.nan,'censored_pool',ntx
            cash+=proceeds; ntx+=1
            return (cash-e['cost'])/e['cost'],'grad_snapshot',ntx
        if te>t[-1] or (bad<n and te>=t[bad]): return np.nan,'censored',ntx
        ee=idx_at(t,te)
        if ee<k or (age is not None and te-t[ee]>age): return np.nan,'censored',ntx
        va,ta=vs[ee]+ds,vt[ee]-dt
        if not np.isfinite([va,ta]).all() or min(va,ta)<=0:
            return np.nan,'invalid_state',ntx
        ys=min(y,tps[ntp][1]*y0) if trig=='tp' else y
        if trig=='tp': ntp+=1
        if y-ys<=1e-9: ys=y
        gross=va*ys/(ta+ys)
        cash+=gross*(1-fee)-tip; ntx+=1
        # Include highs observed while the sell was pending, then resume
        # after the actual execution state with the reduced position.
        if trail is not None and ee>=st:
            marks=((vs[st:ee+1]+ds)/(vt[st:ee+1]-dt))/px
            if len(marks): peak=max(peak,float(np.max(marks)))
        ds-=gross; dt-=ys; y-=ys; pos=ee; clock=te
        if y<=1e-9: return (cash-e['cost'])/e['cost'],trig,ntx
    return (cash-e['cost'])/e['cost'],'closed',ntx


def liquidation_curve(tokd, e, fee, tip):
    """net value multiple of selling everything at each state after fill (no latency) for oracle stats"""
    j=e['j']; vsA = tokd['vs'][j:]+e['ds']; vtA = tokd['vt'][j:]-e['dt']
    val = vsA*e['y']/(vtA+e['y'])*(1-fee)-tip
    return val/e['cost'], (vsA/vtA)/e['px']
