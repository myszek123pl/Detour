"""Part A: one-component-at-a-time EV loss vs ideal (ladder strategies). Usage: python3 -I exec_gap_a.py <data_dir> <out_dir>"""
import sys, json, numpy as np, pandas as pd
sys.path.insert(0, "/home/user/Detour/backtest")
import exec_gap_lib as G
D, OUT = sys.argv[1], sys.argv[2]
t, paths = G.load(D)
m, segs = G.build(t, paths)
feas = np.array([[s is not None for s in ss] for ss in segs])
U = np.where(feas.all(1))[0]
mU = m.iloc[U]; sU = [segs[i] for i in U]; N = len(U)
Lq = np.maximum(np.minimum(mU.liq.values, 0.4 * mU.mcap.values), 1.0)
INF = np.full(N, 1e15)
res = {"N_full_k0": len(m), "N_U": N, "feas_share_by_k": feas.mean(0).tolist()}
k0 = np.zeros(N, int)
S = G.STRATS["ladder_B"]
def gross(F, M): return (F * M).sum(1) - 1
def pr(title, rows, cols):
    print("\n## " + title); print(pd.DataFrame(rows, columns=cols).round(4).to_string(index=False))
def d_ci(base, x):
    d = x - base
    return d.mean(), G.ci(d)
def ev(strat, cfg, k=k0, seed=0, reps=1):
    out = []
    for r in range(reps):
        F, M, ntx, nf = G.run_all(sU, k, cfg, strat, seed=seed + r)
        out.append((F, M, ntx, nf))
    return out
def netarr(runs, pos=200, fee=0.0, tip=0.0, Lq_=INF, cf=None, kk=k0, retry=1.0):
    ec = G.entry_candle(sU, kk)
    cfv = np.ones(N) if cf is None else cf
    return np.mean([G.net(F, M, ntx, 0, Lq_, pos, fee, tip, cfv, retry) for F, M, ntx, nf in runs], axis=0)

for sname in ["ladder_B", "ladder_C"]:
    S = G.STRATS[sname]
    print("\n=================", sname)
    ideal = ev(S, dict(stop_mode="exact"))
    base = netarr(ideal)
    R = {}
    R["ideal_gross_ev"] = float(base.mean()); R["ideal_ci"] = G.ci(base); R["ideal_median"] = float(np.median(base)); R["ideal_win"] = float((base > 0).mean())
    R["ideal_ex_top1"] = float(base[base < np.quantile(base, .99)].mean())
    print("ideal on U: mean %.4f CI %s median %.3f win %.3f ex-top1%% %.4f" % (R["ideal_gross_ev"], R["ideal_ci"], R["ideal_median"], R["ideal_win"], R["ideal_ex_top1"]))
    # A1 bracket
    rows = []
    for order in ["sl", "tp"]:
        for sm in ["exact", "gap"]:
            r = ev(S, dict(stop_mode=sm, order=order)); x = netarr(r); rows.append([order + "-first", sm, x.mean(), np.median(x), (x > 0).mean()])
    pr("A1 intra-candle ordering and gap-through (U, gross)", rows, ["order", "stop_fill", "EV", "median", "win"])
    R["A1"] = rows
    # full-set ideal
    Fq, Mq, _, _ = G.run_all([s for s in segs], np.zeros(len(segs), int), dict(stop_mode="exact"), S)
    R["ideal_full_k0"] = float(gross(Fq, Mq).mean())
    print("ideal gross EV on full k=0 set (N=%d): %.4f" % (len(segs), R["ideal_full_k0"]))
    # A2 delay
    rows = []
    for k in range(5):
        kk = np.full(N, k); r = ev(S, dict(stop_mode="exact"), k=kk); x = netarr(r, kk=kk); dm, dci = d_ci(base, x)
        # all-feasible-at-k set
        fk = np.array([s[k] is not None for s in segs]); kall = np.where(fk, k, 0)
        Fk, Mk, _, _ = G.run_all(segs, kall, dict(stop_mode="exact"), S)
        rows.append([k, k * 15, x.mean(), dm, dci[0], dci[1], (x > 0).mean(), int(fk.sum()), float(gross(Fk, Mk)[fk].mean())])
    pr("A2 entry delay in candles (U common set; last col = EV on all tokens feasible at k)", rows, ["k", "extra_min", "EV", "dEV", "lo", "hi", "win", "N_feas_k", "EV_allfeas_k"])
    R["A2"] = rows
    # drift stats
    o = np.array([[sU[i][k][0][1] for k in range(5)] for i in range(N)])
    dr = []
    for k in range(1, 5):
        q = o[:, k] / o[:, 0]; dr.append([k, np.median(q), np.mean(q), (q >= 2).mean(), (q >= 1.5).mean(), (q <= 0.5).mean(), (q<=0.7).mean()])
    pr("A2b drift of entry price vs k=0 open", dr, ["k", "median", "mean", "P>=2x", "P>=1.5x", "P<=0.5x", "P<=0.7x"])
    R["A2b"] = dr
    # A3 chase
    ec = G.entry_candle(sU, k0); rng_ = (ec[:, 1] / ec[:, 0] - 1)
    rows = []
    for name, E in [("open", ec[:, 0]), ("c=0.25", ec[:, 0] + .25 * (ec[:, 1] - ec[:, 0])), ("OHLC4", ec.mean(1)), ("c=0.5", ec[:, 0] + .5 * (ec[:, 1] - ec[:, 0])),
                    ("c=0.75", ec[:, 0] + .75 * (ec[:, 1] - ec[:, 0])), ("high", ec[:, 1]), ("close", ec[:, 3])]:
        cf = ec[:, 0] / E; x = netarr(ideal, cf=cf); dm, dci = d_ci(base, x)
        rows.append([name, float(np.mean(E / ec[:, 0] - 1)), float(np.median(E / ec[:, 0] - 1)), x.mean(), dm, dci[0], dci[1]])
    pr("A3 fill price within entry candle (cost basis vs open)", rows, ["fill", "mean_premium", "median_prem", "EV", "dEV", "lo", "hi"])
    R["A3"] = rows
    print("entry-candle high/open-1 quantiles:", np.quantile(rng_, [.25, .5, .75, .9, .99]).round(3))
    # A4 stop execution
    rows = []
    for sm in ["exact", "gap", "close", "next_open"]:
        for sls in [0, .03, .05, .10, .20]:
            r = ev(S, dict(stop_mode=sm, sl_slip=sls)); x = netarr(r); dm, dci = d_ci(base, x)
            rows.append([sm, sls, x.mean(), dm, dci[0], dci[1]])
    pr("A4 stop-loss execution mode x extra slippage", rows, ["stop_mode", "extra_slip", "EV", "dEV", "lo", "hi"])
    R["A4"] = rows
    Fe, Me, ne, _ = ideal[0]; Fg, Mg, ng, _ = ev(S, dict(stop_mode="gap"))[0]
    stopped = (Fe * (Me <= (1 - (S["sl"] or 0)) + 1e-9)).sum(1) > 0
    diff = (Fg * Mg).sum(1) - (Fe * Me).sum(1)
    gapped = diff < -1e-9
    print("tokens with a stop-exit (any tranche at <= stop level): %.3f ; gap-through share among those: %.3f ; mean EV loss from gaps per stopped token: %.4f ; avg per trade %.4f" % (stopped.mean(), gapped.sum() / max(stopped.sum(), 1), diff[gapped].mean() if gapped.any() else 0, diff.mean()))
    R["A4_gap"] = [float(stopped.mean()), float(gapped.sum() / max(stopped.sum(), 1)), float(diff.mean())]
    rows = []
    for tps_ in [0, .02, .05, .10]:
        r = ev(S, dict(stop_mode="exact", tp_slip=tps_)); x = netarr(r); dm, dci = d_ci(base, x); rows.append([tps_, x.mean(), dm, dci[0], dci[1]])
    pr("A4b take-profit slippage", rows, ["tp_slip", "EV", "dEV", "lo", "hi"]); R["A4b"] = rows
    # A5 fails
    rows = []
    for p in [0.05, .10, .15, .25]:
        r = ev(S, dict(stop_mode="exact", pf=p), reps=40); x = netarr(r); dm, dci = d_ci(base, x)
        # buy fail slow retry: mixture over k
        w = np.array([(1 - p) * p**g for g in range(4)] + [p**4])
        xs = []
        for k in range(5):
            kk = np.full(N, k); rk = ev(S, dict(stop_mode="exact"), k=kk); xs.append(netarr(rk, kk=kk))
        xb = sum(w[k] * xs[k] for k in range(5)); dmb, dcib = d_ci(base, xb)
        # fast retry: tips only
        xf = netarr(ideal, tip=0.30, retry=1 / (1 - p))
        rows.append([p, x.mean(), dm, dci[0], dci[1], dmb, dcib[0], dcib[1], (1 - p) * x.mean() if False else None])
    pr("A5 failed tx. sells fail w.p. p and are only re-tried when next candle triggers (no-retry); buys retried next candle (slow)", [r[:8] for r in rows], ["p", "EV_sellfail", "dEV_sell", "lo", "hi", "dEV_buyfail_slowretry", "lo", "hi"])
    R["A5"] = [r[:8] for r in rows]
    # share of tokens with >=1 failed sell in a p=.1 run
    r = ev(S, dict(stop_mode="exact", pf=.10), seed=5)[0]; print("p=.10: tokens with >=1 failed sell tx: %.3f; mean failed tx per trade %.3f ; mean tx per trade %.2f" % ((r[3] > 0).mean(), r[3].mean(), r[2].mean()))
    # A6 fees
    rows = []
    for fee in [0, .003, .005, .01, .0125, .015, .02]:
        x = netarr(ideal, fee=fee); dm, dci = d_ci(base, x); rows.append([fee, x.mean(), dm, dci[0], dci[1]])
    pr("A6 fee per side (no tips/impact)", rows, ["fee", "EV", "dEV", "lo", "hi"]); R["A6"] = rows
    print("share of U with mcap < $63k (approx 420 SOL @ $150):", (mU.mcap < 63000).mean(), "; <$15M:", (mU.mcap < 15e6).mean())
    # A7 tips
    ntx_i = ideal[0][2]
    rows = []
    for tip in [0, .05, .15, .30, .60, 1.0, 3.0]:
        for pos in [50, 200, 1000]:
            x = netarr(ideal, pos=pos, tip=tip); rows.append([tip, pos, x.mean(), x.mean() - netarr(ideal, pos=pos).mean()])
    pr("A7 tip per tx x position", rows, ["tip_usd", "pos", "EV", "dEV"]); R["A7"] = rows
    print("mean number of tx per round trip (incl. buy): %.2f" % (1 + ntx_i.mean()))
    # A8 impact
    rows = []
    for pos in [10, 25, 50, 100, 200, 500, 1000, 2500, 5000]:
        x = netarr(ideal, pos=pos, Lq_=Lq); dm, dci = d_ci(base, x); r_ = pos / Lq
        rows.append([pos, x.mean(), dm, dci[0], dci[1], np.median(x), np.median(r_), (r_ > .05).mean(), (r_ > .25).mean()])
    pr("A8 price impact (L=min(liq,0.4mcap), CPMM x=2V/L per side), no fee/tip", rows, ["pos", "EV", "dEV", "lo", "hi", "median_net", "median pos/L", "P(pos/L>5%)", "P(pos/L>25%)"])
    R["A8"] = rows
    print("L quantiles (5,25,50,75,95):", np.quantile(Lq, [.05, .25, .5, .75, .95]).round(0))
    # cap rule
    rows = []
    for cap in [0.005, 0.01, 0.02, 0.05, 0.10]:
        for pos in [200, 1000]:
            posv = np.minimum(pos, cap * Lq)
            x = np.mean([G.net(F, M, ntx, 0, Lq, posv, 0.0, 0.0, np.ones(N)) for F, M, ntx, nf in ideal], axis=0)
            rows.append([cap, pos, x.mean(), float(posv.mean()), float(np.sum(posv * x) / np.sum(posv))])
    pr("A8b position cap = cap*L (impact only) -> EV per $ (mean, and $-weighted)", rows, ["cap", "pos_max", "EV_unweighted", "avg_pos", "EV_$weighted"]); R["A8b"] = rows
    # A9 behaviour
    classes = {
        "disciplined": (S, {}),
        "move_stop(-50%->-80%)": (S, dict(move_stop=True)),
        "no_stop": (dict(S, sl=None), {}),
        "hope(no stop, exit at b/e)": (S, dict(hope=True)),
        "panic_loss(close<=-25%)": (S, dict(panic_loss=.25)),
        "panic_win(-20% from peak after TP1)": (S, dict(panic_win=.20)),
        "early_tp_all@1.3x": (dict(S, tps=[(1.3, 1.0)], trail=None), {}),
        "all_out@2x": (dict(S, tps=[(2.0, 1.0)], trail=None), {}),
        "greed(no TP/trail)": (dict(S, tps=[], trail=None), {}),
    }
    rows = []
    for nme, (st_, cf_) in classes.items():
        r = ev(st_, dict(stop_mode="exact", **cf_)); x = netarr(r); dm, dci = d_ci(base, x)
        rows.append([nme, x.mean(), dm, dci[0], dci[1], np.median(x), (x > 0).mean()])
    pr("A9 behaviour classes (each applied to 100% of trades; gross)", rows, ["behaviour", "EV", "dEV", "lo", "hi", "median", "win"]); R["A9"] = rows
    # A10 dead mark
    rows = []
    for dm_ in [1.0, .75, .5, .25, 0.0]:
        r = ev(S, dict(stop_mode="exact", dead=dm_)); x = netarr(r); rows.append([dm_, x.mean(), x.mean() - base.mean()])
    pr("A10 mark of the remaining position when the OHLCV path ends before exit horizon", rows, ["dead_mark", "EV", "dEV"]); R["A10"] = rows
    Ft, Mt, _, _ = ideal[0]
    # share of gross value coming from forced time exits
    trunc = np.array([ (sU[i][0][-1][0] + 900 < sU[i][0][0][0] + 86400) for i in range(N)])
    print("share of U paths ending before 24h horizon:", trunc.mean())
    res[sname] = R
json.dump(res, open(f"{OUT}/exec_gap_a.json", "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
