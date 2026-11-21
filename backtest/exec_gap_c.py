"""Part C: waterfall, Shapley attribution, alpha-lens (break-even precision), slices. Usage: python3 -I exec_gap_c.py <pickle> <out_json>"""
import sys, pickle, json, itertools, math, numpy as np, pandas as pd
sys.path.insert(0, "/home/user/Detour/backtest")
import exec_gap_lib as G
res, meta = pickle.load(open(sys.argv[1], "rb"))
NAMES = ["delay", "chase", "stop/exit exec", "failed tx", "fees", "tips", "price impact", "human behaviour"]
ORDER = [0, 1, 2, 3, 4, 5, 6, 7]
peak = meta["peak"]; W = peak >= 3.0
print("winner share (peak>=3x):", W.mean(), " N=", len(peak))
out = {}
def v(key, mask, pos, sel=None):
    a = res[key][(mask, pos)]
    return float(a.mean() if sel is None else a[sel].mean())
def shapley(key, pos, sel=None):
    n = 8; phi = np.zeros(n); vals = {mk: v(key, mk, pos, sel) for mk in range(256)}
    for i in range(n):
        for mk in range(256):
            if mk >> i & 1: continue
            s = bin(mk).count("1")
            phi[i] += math.factorial(s) * math.factorial(n - s - 1) / math.factorial(n) * (vals[mk | 1 << i] - vals[mk])
    return phi, vals
for key in sorted(res):
    sname, pname = key
    for pos in meta["POS"]:
        o = {}
        mk = 0; steps = [("ideal", 0)]
        for i in ORDER:
            mk |= 1 << i; steps.append((NAMES[i], mk))
        prev = None; rows = []
        for nm, mask in steps:
            a = res[key][(mask, pos)]
            row = dict(step=nm, mask=mask, ev=float(a.mean()), ev_win=float(a[W].mean()), ev_lose=float(a[~W].mean()), med=float(np.median(a)), win=float((a > 0).mean()),
                       p_le_m70=float((a <= -0.7).mean()))
            if prev is not None:
                d = a - res[key][(prev, pos)]
                row["delta"] = float(d.mean()); row["ci"] = G.ci(d.astype(float), B=300)
            else:
                row["ci"] = G.ci(a.astype(float), B=300)
            row["ev_ci"] = G.ci(a.astype(float), B=300) if nm in ("ideal", "behaviour", "human behaviour") else None
            prev = mask; rows.append(row)
        o["waterfall"] = rows
        phi, vals = shapley(key, pos); phiW, valsW = shapley(key, pos, W)
        o["shapley"] = dict(zip(NAMES, phi.tolist())); o["shapley_win"] = dict(zip(NAMES, phiW.tolist()))
        o["standalone"] = {NAMES[i]: vals[1 << i] - vals[0] for i in range(8)}
        o["standalone_win"] = {NAMES[i]: valsW[1 << i] - valsW[0] for i in range(8)}
        o["leave_one_out"] = {NAMES[i]: vals[255] - vals[255 ^ (1 << i)] for i in range(8)}  # change when component i added last (negative = costs)
        o["leave_one_out_win"] = {NAMES[i]: valsW[255] - valsW[255 ^ (1 << i)] for i in range(8)}
        # break-even precision
        def pstar(ea, ew): return -ea / (ew - ea) if ew - ea > 0 and ea < 0 else (0.0 if ea >= 0 else float("nan"))
        o["pstar_ideal"] = pstar(vals[0], valsW[0]); o["pstar_real"] = pstar(vals[255], valsW[255])
        o["pstar_steps"] = {nm: pstar(float(res[key][(mask, pos)].mean()), float(res[key][(mask, pos)][W].mean())) for nm, mask in steps}
        out[f"{sname}|{pname}|{pos}"] = o
json.dump(out, open(sys.argv[2], "w"), indent=1)
def show(key, pos):
    o = out[f"{key[0]}|{key[1]}|{pos}"]
    print(f"\n### {key} pos={pos}")
    print(pd.DataFrame([{k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items() if k in ('step', 'ev', 'delta', 'ev_win', 'ev_lose', 'med', 'win', 'p_le_m70')} for r in o["waterfall"]]).to_string(index=False))
    print("CIs of step deltas:", [(r['step'], tuple(round(x, 4) for x in r['ci'])) for r in o["waterfall"][1:]])
    print("ideal EV CI", o["waterfall"][0]["ci"], " real EV CI", o["waterfall"][-1]["ev_ci"])
    print(pd.DataFrame({"shapley": o["shapley"], "standalone": o["standalone"], "leave_one_out": o["leave_one_out"], "shapley_win": o["shapley_win"], "standalone_win": o["standalone_win"], "loo_win": o["leave_one_out_win"]}).round(4).to_string())
    print("break-even precision ideal %.3f real %.3f" % (o["pstar_ideal"], o["pstar_real"]), {k: round(v, 3) for k, v in o["pstar_steps"].items()})
for key in sorted(res):
    for pos in meta["POS"]:
        if pos == 200 or (key[0] == "ladder_B" and key[1] in ("manual", "bot")):
            show(key, pos)
# slices for ladder_B manual/bot pos 200
Lq = meta["Lq"]; age = meta["age"]
for key in [("ladder_B", "manual"), ("ladder_B", "bot")]:
    idealv = res[key][(0, 200)]; realv = res[key][(255, 200)]
    qs = pd.qcut(Lq, 4, labels=["Q1 low L", "Q2", "Q3", "Q4 high L"])
    ag = pd.cut(age, [0, 120, 300, 900, 3600, 1e9], labels=["<2m", "2-5m", "5-15m", "15-60m", ">1h"])
    for nm, g in [("liquidity quartile", qs), ("token age at snapshot", ag)]:
        df = pd.DataFrame(dict(g=g, ideal=idealv, real=realv, L=Lq)).groupby("g", observed=True).agg(n=("ideal", "size"), L_med=("L", "median"), ideal=("ideal", "mean"), real=("real", "mean"))
        df["gap"] = df.real - df.ideal
        print(f"\n{key} slice by {nm}"); print(df.round(4).to_string())
