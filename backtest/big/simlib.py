"""Leak-free pump.fun bonding-curve trade simulator on exact reserve paths.
All state arrays are per-token, time-sorted. Reserves in SOL / tokens (not lamports / micro units).
Conventions
- decision at trade index i (information up to and including trade i observed at t[i]);
- order fills at state idx_at(t[i]+latency)  (the last recorded state at or before that time);
- own position shifts reserves additively (vs+ds, vt-dt), so a round trip with no other flow costs only fees/tip;
- buy: fee taken from SOL input; sell: fee taken from proceeds; tip per tx (SOL).
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

def load(S, mayhem=None, tmin=None, tmax=None):
    con = duckdb.connect()
    tk = con.sql(f"select * from read_parquet('{S}/work/tok_jocry2.parquet') order by mid").df()
    if mayhem is not None: tk = tk[tk.mh==mayhem]
    if tmin is not None: tk = tk[tk.L>=tmin]
    if tmax is not None: tk = tk[tk.L<tmax]
    mids = tk.mid.values
    df = con.sql(f"select mid,t,b,sol,vs,vt,wid,is_sys from read_parquet('{S}/work/paths_jocry.parquet')").df()
    df = df[df.mid.isin(set(mids.tolist()))]
    df = df.sort_values(['mid','t'], kind='stable')
    pg = con.sql(f"select * from read_parquet('{S}/work/postgrad_jocry.parquet') order by mid, ssg").df()
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
        pgm = pg[pg.mid.isin(set(tk.mid.tolist()))]
        for m,g in pgm.groupby('mid'): self.pg[int(m)] = (g.ssg.values, g.price_native.values)
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

def buy(vs, vt, X, fee):
    xin = X*(1-fee)
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
    if v is None: return 0.86 if lat<20 else 1.0
    ssg, px = v
    k = np.searchsorted(ssg, lat)
    if k>=len(ssg): k=len(ssg)-1
    return float(np.clip(px[k]/P_GRAD, 0.1, 3.0))

def entry(tokd, i_dec, lat, X, fee, tip):
    """returns None if no fill, else dict(j, y, xin, ds, dt, px_avg, cost)"""
    t = tokd['t']; n = len(t)
    tf = t[i_dec]+lat
    G = tokd['G']
    if tokd['grad'] and G is not None and tf >= G: return None
    j = idx_at(t, tf)
    if j < i_dec: j = i_dec
    if j >= n: j = n-1
    vs, vt = tokd['vs'][j], tokd['vt'][j]
    if vs > 112.0: return None   # curve (almost) complete -> buy would overflow / fail
    xin, y = buy(vs, vt, X, fee)
    return dict(j=j, y=y, xin=xin, ds=xin, dt=y, px=xin/y, tf=t[j], cost=X+tip, vs0=vs)

def exit_sim(P, m, tokd, e, spec, lat, fee, tip, X, pool_mode='own'):
    """spec: dict(sl=None|frac(<1), tps=[(mult, frac_of_orig)], trail=None|frac, arm=mult, tmax=None|sec, hold_grad=True)
       returns (net_return, info) ; return = (cash_out - cost)/cost"""
    t,vs,vt = tokd['t'],tokd['vs'],tokd['vt']; n=len(t)
    y0 = e['y']; y = y0; ds=e['ds']; dt=e['dt']; px=e['px']; cash=0.0
    pos = e['j']; tf = e['tf']
    tps = sorted(spec.get('tps') or [], key=lambda z: z[0]); ntp=0
    sl=spec.get('sl'); trail=spec.get('trail'); arm=spec.get('arm',1.0); tmax=spec.get('tmax')
    peak = 0.0; ntx=0; exit_kind=None; last_t=t[pos]
    G = tokd['G']
    while y > 1e-9:
        if pos >= n-1:   # no more states
            k = n-1; trig='end'
        else:
            vsA = vs[pos+1:]+ds; vtA = vt[pos+1:]-dt
            mult = (vsA/vtA)/px
            # triggers
            cand = []
            if sl is not None:
                w = np.nonzero(mult <= sl)[0]
                if len(w): cand.append((w[0],'sl'))
            if ntp < len(tps):
                w = np.nonzero(mult >= tps[ntp][0])[0]
                if len(w): cand.append((w[0],'tp'))
            if trail is not None:
                pk = np.maximum.accumulate(np.maximum(mult, peak))
                w = np.nonzero((pk>=arm) & (mult <= pk*(1-trail)))[0]
                if len(w): cand.append((w[0],'trail'))
            if tmax is not None:
                w = np.nonzero(t[pos+1:] >= tf+tmax)[0]
                if len(w): cand.append((w[0],'time'))
            if cand:
                kk, trig = min(cand)
                k = pos+1+kk
            else:
                k = n-1; trig='end'
            if trail is not None and trig!='end': peak = max(peak, float(np.max(mult[:kk+1])))
        # execution
        te = t[k]+lat
        graduated_before = tokd['grad'] and G is not None and te >= G
        if trig=='end' or graduated_before:
            if tokd['grad']:
                ratio = pool_ratio(P, m, lat, pool_mode)
                cash += pool_exit(y, ratio, POOL_FEE, tip); ntx+=1
                exit_kind='grad'
            else:
                ee = n-1
                vsA_=vs[ee]+ds; vtA_=vt[ee]-dt
                cash += sell_value(vsA_, vtA_, y, fee, tip); ntx+=1
                exit_kind='end'
            y = 0.0; break
        ee = idx_at(t, te); ee = max(ee,k)
        vsA_=vs[ee]+ds; vtA_=vt[ee]-dt
        if trig=='tp':
            frac = tps[ntp][1]; ys = min(y, frac*y0); ntp+=1
            last_leg = (y-ys) <= 1e-9
            if last_leg: ys=y
        else:
            ys = y
        gross = vsA_*ys/(vtA_+ys)
        cash += gross*(1-fee) - tip; ntx+=1
        ds -= gross; dt -= ys; y -= ys; pos = k
        exit_kind = exit_kind or trig
        if y<=1e-9: exit_kind=trig; break
    r = (cash - e['cost'])/e['cost']
    return r, exit_kind, ntx

def liquidation_curve(tokd, e, fee, tip):
    """net value multiple of selling everything at each state after fill (no latency) for oracle stats"""
    j=e['j']; vsA = tokd['vs'][j:]+e['ds']; vtA = tokd['vt'][j:]-e['dt']
    val = vsA*e['y']/(vtA+e['y'])*(1-fee)-tip
    return val/e['cost'], (vsA/vtA)/e['px']
