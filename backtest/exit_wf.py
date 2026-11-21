"""Walk-forward optimisation of exit rules (see research_notes/.../04_exit_walkforward.md).
Usage: python3 -I exit_wf.py <data_dir> <out_dir>
Reuses entry rule / data cleaning / cost model of backtest.py. Vectorised over tokens."""
import sys, itertools, json, numpy as np, pandas as pd
from multiprocessing import Pool
D, OUT = sys.argv[1], sys.argv[2]
FEE, TIP, MAXD, HOR = 0.0125, 0.30, 900, 24*3600
POS = (50, 200, 1000)

def load():
    t = pd.read_parquet(f"{D}/tokens.parquet")
    o = pd.read_parquet(f"{D}/ohlcv.parquet").sort_values(["token_address", "ts"])
    o["high"] = np.where(o.high > o.close*10, np.maximum(o.open, o.close), o.high)
    t["cap_ts"] = t.captured_at.astype("int64")//10**9
    t = t.sort_values("cap_ts").drop_duplicates("token_address", keep="first")
    paths = {k: g[["ts","open","high","low","close"]].to_numpy() for k, g in o.groupby("token_address")}
    rows = []
    for r in t.itertuples():
        p = paths.get(r.token_address)
        if p is None: continue
        i = np.searchsorted(p[:,0], r.cap_ts)
        if i >= len(p) or p[i,0]-r.cap_ts > MAXD: continue
        s = p[i:]; s = s[s[:,0] < s[0,0]+HOR]
        if s[0,1] <= 0: continue
        rows.append((r, s))
    return t, rows

t0 = None
def build():
    global M
    t, rows = load()
    N, T = len(rows), max(len(s) for _, s in rows)
    A = np.full((4, N, T), np.nan); REL = np.full((N, T), np.inf)
    meta = []
    for j, (r, s) in enumerate(rows):
        n = min(len(s), T)
        A[:, j, :n] = s[:n, 1:5].T
        REL[j, :n] = s[:n, 0]-s[0, 0]
        meta.append((r.token_address, r.cap_ts, r.liquidity_usd, r.market_cap_usd))
    m = pd.DataFrame(meta, columns=["tok","cap_ts","liq","mcap"])
    day0 = (m.cap_ts.min()//86400)*86400
    m["day"] = ((m.cap_ts-day0)//86400+1).astype(int)
    return A, REL, m

def sim(cfg, mode, A, REL):
    sl, ladder, act, trail, tmax = cfg
    O, H, L, C = A
    N, T = O.shape
    entry = O[:, 0]
    left = np.ones(N); val = np.zeros(N); sells = np.zeros(N); peak = entry.copy()
    done = np.zeros(N, bool); last = entry.copy(); hit = np.zeros((len(ladder), N), bool)
    for k in range(T):
        valid = (REL[:, k] < tmax*3600) & ~done
        if not valid.any(): break
        op, hi, lo, cl = O[:, k], H[:, k], L[:, k], C[:, k]
        stop = np.full(N, -np.inf)
        if sl is not None: stop = np.full(N, 1)*entry*(1-sl)
        if trail is not None:
            stop = np.where(peak > entry*act, np.maximum(stop, peak*(1-trail)), stop)
        def do_stop(v):
            nonlocal left, val, sells, done
            s = v & (lo <= stop) & (left > 1e-9)
            px = np.minimum(stop, op)
            val += np.where(s, left*px/entry, 0); sells += s; left = np.where(s, 0, left); done |= s
        def do_tp(v):
            nonlocal left, val, sells, done
            for i, (lvl, fr) in enumerate(ladder):
                h = v & ~hit[i] & (hi >= entry*lvl) & (left > 1e-9)
                f = np.minimum(fr, left)
                val += np.where(h, f*lvl, 0); left = np.where(h, left-f, left); sells += h; hit[i] |= h
        if mode == "worst":
            do_stop(valid); v2 = valid & ~done; do_tp(v2)
        else:
            do_tp(valid); do_stop(valid & ~done)
        done |= left <= 1e-9
        upd = valid & ~done | (valid & done)
        peak = np.where(valid, np.maximum(peak, hi), peak)
        last = np.where(valid & ~done, cl, last)
    rem = left > 1e-9
    val += np.where(rem, left*last/entry, 0); sells += rem
    return val, sells

def grid():
    sls = [None, .2, .3, .4, .5, .6, .7]
    lad = [()]
    lad += [((l, 1.0),) for l in (1.3, 1.5, 2, 3)]
    lad += [((l, f),) for l in (1.3, 1.5, 2, 3) for f in (.33, .5)]
    lad += [((l1, .5), (l2, f2)) for l1 in (1.5, 2, 3) for l2 in (3, 5, 10) if l2 > l1 for f2 in (.25, .5)]
    trs = [(None, None)] + [(a, tr) for a in (1.5, 2) for tr in (.3, .4, .5, .6)]
    tms = [1, 2, 4, 6, 12, 24]
    return [(s, l, a, tr, tm) for s in sls for l in lad for (a, tr) in trs for tm in tms]

G = {}
def init(A, REL, m, mode):
    G.update(A=A, REL=REL, m=m, mode=mode)
    L = np.minimum(m.liq.fillna(1).clip(lower=1), 0.4*m.mcap.fillna(1e18)).clip(lower=1).to_numpy()
    G["L"] = L; G["days"] = m.day.to_numpy()

def net(g, n, pos, L):
    imp = np.clip(2*pos/L, 0, .9)
    return g*(1-FEE-imp)**2 - TIP*(1+n)/pos - 1

def work(cfg):
    g, n = sim(cfg, G["mode"], G["A"], G["REL"])
    d = G["days"]; out = []
    for lo, hi in ((1, 10), (11, 15), (16, 20)):
        mk = (d >= lo) & (d <= hi)
        out.append(float((g[mk]-1).mean()))
        for p in POS: out.append(float(net(g[mk], n[mk], p, G["L"][mk]).mean()))
    return out

if __name__ == "__main__":
    A, REL, m = build()
    m = m[m.day.between(1, 20)] if False else m
    keep = (m.day <= 20).to_numpy()
    A, REL, m = A[:, keep], REL[keep], m[keep].reset_index(drop=True)
    print("tokens", len(m), m.groupby(pd.cut(m.day, [0,10,15,20])).size().to_dict(), flush=True)
    cfgs = grid(); print("configs", len(cfgs), flush=True)
    cols = [f"{s}_{k}" for s in ("tr", "va", "te") for k in ("zero", "p50", "p200", "p1000")]
    m.to_parquet(f"{OUT}/exit_tokens.parquet"); np.save(f"{OUT}/A.npy", A); np.save(f"{OUT}/REL.npy", REL)
    import os
    for mode in ("worst", "best"):
        if os.path.exists(f"{OUT}/exit_grid_{mode}.parquet"): continue
        with Pool(4, initializer=init, initargs=(A, REL, m, mode)) as pool:
            res = pool.map(work, cfgs, chunksize=40)
        df = pd.DataFrame(res, columns=cols)
        df["cfg"] = [json.dumps(c) for c in cfgs]
        df.to_parquet(f"{OUT}/exit_grid_{mode}.parquet"); print(mode, "done", flush=True)
    m.to_parquet(f"{OUT}/exit_tokens.parquet")
    np.save(f"{OUT}/A.npy", A); np.save(f"{OUT}/REL.npy", REL)
