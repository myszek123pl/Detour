"""Part B: full-factorial (2^8) evaluation of execution components for 3 trader profiles x 2 ladder strategies.
Components (bit): 0 delay, 1 chase, 2 stop/exit execution, 3 failed tx, 4 fees, 5 tips, 6 impact, 7 human behaviour.
Usage: python3 -I exec_gap_b.py <data_dir> <out_pickle>"""
import sys, pickle, itertools, numpy as np
from multiprocessing import Pool
sys.path.insert(0, "/home/user/Detour/backtest")
import exec_gap_lib as G
D, OUTP = sys.argv[1], sys.argv[2]
t, paths = G.load(D)
m, segs = G.build(t, paths)
feas = np.array([[s is not None for s in ss] for ss in segs])
U = np.where(feas.all(1))[0]
mU = m.iloc[U]; sU = [segs[i] for i in U]; N = len(U)
Lq = np.maximum(np.minimum(mU.liq.values, 0.4 * mU.mcap.values), 1.0)
INF = np.full(N, 1e15)
POS = [50, 200, 1000]
ECS = {k: G.entry_candle(sU, np.full(N, k)) for k in range(5)}

PROFILES = {
    "manual": dict(k=1, c=0.25, stop_mode="next_open", sl_slip=.03, tp_slip=.03, p=.10, sell_mode="slow", buy_mode="slow",
                   fee=.0125, tip=.30,
                   mix={"disciplined": .30, "move_stop": .15, "no_stop": .10, "hope": .10, "panic_loss": .10, "panic_win": .05, "early_tp": .10, "greed": .10}),
    "terminal": dict(k=1, c="ohlc4", stop_mode="gap", sl_slip=.03, tp_slip=.02, p=.10, sell_mode="fast", buy_mode="slow",
                     fee=.0125, tip=.30,
                     mix={"disciplined": .60, "move_stop": .08, "no_stop": .05, "hope": .05, "panic_loss": .06, "panic_win": .04, "early_tp": .06, "greed": .06}),
    "bot": dict(k=0, c=0.02, stop_mode="gap", sl_slip=.02, tp_slip=.01, p=.05, sell_mode="fast", buy_mode="fast",
                fee=.0125, tip=.60, mix={"disciplined": 1.0}),
}


def klass(S, name):
    if name == "disciplined": return S, {}
    if name == "move_stop": return S, dict(move_stop=True)
    if name == "no_stop": return dict(S, sl=None), {}
    if name == "hope": return S, dict(hope=True)
    if name == "panic_loss": return S, dict(panic_loss=.25)
    if name == "panic_win": return S, dict(panic_win=.20)
    if name == "early_tp": return dict(S, tps=[(1.3, 1.0)], trail=None), {}
    if name == "greed": return dict(S, tps=[], trail=None), {}


def chase_factor(k, c):
    ec = ECS[k]
    E = ec.mean(1) if c == "ohlc4" else ec[:, 0] + c * (ec[:, 1] - ec[:, 0])
    return ec[:, 0] / E


def kweights(prof, d, f):
    kb = prof["k"] if d else 0
    if f and prof["buy_mode"] == "slow":
        p = prof["p"]; w = {}
        for g in range(5):
            kk = min(4, kb + g); w[kk] = w.get(kk, 0) + ((1 - p) * p ** g if g < 4 else p ** 4)
        # note: g=4 mass lumps at k=4 (prob p^4); g<4 individual
        s = sum(w.values()); return {k: v / s for k, v in w.items()}
    return {kb: 1.0}


def group(args):
    sname, pname, d, s, f, b = args
    S = G.STRATS[sname]; prof = PROFILES[pname]
    kw = kweights(prof, d, f)
    mix = prof["mix"] if b else {"disciplined": 1.0}
    pf = prof["p"] if (f and prof["sell_mode"] == "slow") else 0.0
    R = 16 if pf > 0 else 1
    base = dict(stop_mode=prof["stop_mode"], sl_slip=prof["sl_slip"], tp_slip=prof["tp_slip"]) if s else dict(stop_mode="exact")
    retry = 1 / (1 - prof["p"]) if (f and (prof["sell_mode"] == "fast" or prof["buy_mode"] == "fast")) else 1.0
    out = {}
    # post-process combos: bits chase(1), fee(4), tip(5), impact(6)
    combos = list(itertools.product([0, 1], repeat=4))
    acc = {(cb, pos): np.zeros(N) for cb in combos for pos in POS}
    for k, wk in kw.items():
        kk = np.full(N, k)
        cfs = {0: np.ones(N), 1: chase_factor(k, prof["c"])}
        for cname, pc in mix.items():
            st, cf_ = klass(S, cname)
            for r in range(R):
                F, M, ntx, nf = G.run_all(sU, kk, dict(base, pf=pf, **cf_), st, seed=1000 + r)
                for cb in combos:
                    ch, fe, ti, im = cb
                    for pos in POS:
                        x = G.net(F, M, ntx, 0, Lq if im else INF, pos, prof["fee"] if fe else 0.0, prof["tip"] if ti else 0.0, cfs[ch], retry)
                        acc[(cb, pos)] += wk * pc / R * x
    for (cb, pos), v in acc.items():
        mask = d | (cb[0] << 1) | (s << 2) | (f << 3) | (cb[1] << 4) | (cb[2] << 5) | (cb[3] << 6) | (b << 7)
        out[(mask, pos)] = v.astype(np.float32)
    return (sname, pname), out


if __name__ == "__main__":
    tasks = [(sn, pn, d, s, f, b) for sn in G.STRATS for pn in PROFILES for d, s, f, b in itertools.product([0, 1], repeat=4)]
    # heavy first
    tasks.sort(key=lambda a: -(a[3] * 0 + a[4] * 3 + a[5] * 3))
    res = {}
    with Pool(4) as pool:
        for i, (key, out) in enumerate(pool.imap_unordered(group, tasks)):
            res.setdefault(key, {}).update(out)
            if i % 8 == 0: print("done", i, "/", len(tasks), flush=True)
    peak = np.array([max(x[2] for x in s[0]) / s[0][0][1] for s in sU])
    meta = dict(Lq=Lq, liq=mU.liq.values, mcap=mU.mcap.values, age=mU.age.values, peak=peak, tokens=list(mU.index), profiles=PROFILES, POS=POS)
    pickle.dump((res, meta), open(OUTP, "wb"))
    print("saved")
