"""Selection + bootstrap for exit_wf.py output. Usage: python3 -I exit_wf_report.py <out_dir>"""
import sys, json, numpy as np, pandas as pd
sys.argv = [sys.argv[0], "", sys.argv[1]]
import exit_wf as E
OUT = sys.argv[2]
A = np.load(f"{OUT}/A.npy"); REL = np.load(f"{OUT}/REL.npy"); m = pd.read_parquet(f"{OUT}/exit_tokens.parquet")
E.init(A, REL, m, "worst")
L = E.G["L"]; d = m.day.to_numpy()
W = pd.read_parquet(f"{OUT}/exit_grid_worst.parquet"); B = pd.read_parquet(f"{OUT}/exit_grid_best.parquet")
rng = np.random.default_rng(0)
def cfgtuple(s):
    c = json.loads(s); return (c[0], tuple(tuple(x) for x in c[1]), c[2], c[3], c[4])
def fmt(c):
    sl, lad, act, tr, tm = cfgtuple(c)
    return f"SL {'none' if sl is None else int(sl*100)}% | TP {'+'.join(f'{int(f*100)}%@{l}x' for l,f in lad) or 'none'} | trail {'none' if tr is None else f'{int(tr*100)}% after {act}x'} | time {tm}h"
def vec(c, mode, pos):
    g, n = E.sim(cfgtuple(c), mode, A, REL)
    return (g-1) if pos == 0 else E.net(g, n, pos, L)
def boot(x, B_=4000):
    idx = rng.integers(0, len(x), (B_, len(x))); mu = x[idx].mean(1)
    return x.mean(), *np.percentile(mu, [2.5, 97.5])
out = {}; lines = []
def P(s=""): lines.append(s); print(s)
K = 20
for pos, key in ((0, "zero"), (50, "p50"), (200, "p200"), (1000, "p1000")):
    P(f"\n### Selection, cost level = {key} (grid = worst-case intra-candle)")
    tr = W.sort_values(f"tr_{key}", ascending=False).head(K)
    best = tr.sort_values(f"va_{key}", ascending=False).iloc[0]
    r_tr = W[f"tr_{key}"].rank(); r_va = W[f"va_{key}"].rank(); r_te = W[f"te_{key}"].rank()
    P(f"rank corr train-val {r_tr.corr(r_va):.3f}, val-test {r_va.corr(r_te):.3f}, train-test {r_tr.corr(r_te):.3f}")
    c = best.cfg; P(f"chosen: {fmt(c)}")
    P(f"train {best[f'tr_{key}']:+.4f}  val {best[f'va_{key}']:+.4f}  test {best[f'te_{key}']:+.4f}")
    res = {"cfg": fmt(c), "tr": best[f"tr_{key}"], "va": best[f"va_{key}"]}
    for mode in ("worst", "best"):
        x = vec(c, mode, pos)[(d >= 16)]
        mu, lo, hi = boot(x); P(f"TEST {mode}-case: EV {mu:+.4f} CI95 [{lo:+.4f}, {hi:+.4f}] n={len(x)} win={np.mean(x>0):.3f}")
        res[mode] = (mu, lo, hi)
    out[key] = res
    for part in ("tr", "va", "te"):
        P(f"  all-config {part}: share>0 {np.mean(W[f'{part}_{key}']>0):.3f}, max {W[f'{part}_{key}'].max():+.4f}, median {W[f'{part}_{key}'].median():+.4f}; best-case grid: share>0 {np.mean(B[f'{part}_{key}']>0):.3f}, max {B[f'{part}_{key}'].max():+.4f}")
    both = W[(W[f"tr_{key}"] > 0) & (W[f"va_{key}"] > 0)]
    P(f"  configs positive in train AND val: {len(both)}; of those positive in test: {int((both[f'te_{key}']>0).sum())}")
    # best-case grid walk-forward
    trb = B.sort_values(f"tr_{key}", ascending=False).head(K); bb = trb.sort_values(f"va_{key}", ascending=False).iloc[0]
    P(f"best-case-grid chosen: {fmt(bb.cfg)} tr {bb[f'tr_{key}']:+.4f} va {bb[f'va_{key}']:+.4f} te {bb[f'te_{key}']:+.4f}")
    # max test EV config (oracle, selection-biased)
    o = W.sort_values(f"te_{key}", ascending=False).iloc[0]; P(f"oracle best test (biased): {fmt(o.cfg)} te {o[f'te_{key}']:+.4f}")
    # all-days
    if key != "zero":
        pass
# cost decomposition for hold_24h and chosen p200 and base strats
P("\n### Cost decomposition (all 20 days, worst-case)")
named = {"hold_24h": (None, (), 2, None, 24), "ladder_B": (.5, ((2.0,.5),(5.0,.25)), 2, .5, 24),
         "tight_D": (.3, ((1.5,.5),(3.0,.5)), 2, None, 6), "scalp_E": (.2, ((1.3,1.0),), 2, None, 2),
         "chosen_p200": cfgtuple(out["p200"].get("cfg") and W.sort_values("tr_p200", ascending=False).head(K).sort_values("va_p200", ascending=False).iloc[0].cfg)}
dec = {}
for name, c in named.items():
    g, n = E.sim(c, "worst", A, REL)
    for pos in (50, 200, 1000):
        imp = np.clip(2*pos/L, 0, .9)
        gross = g.mean()-1
        fee_only = (g*(1-E.FEE)**2).mean()-1
        fee_imp = (g*(1-E.FEE-imp)**2).mean()-1
        full = E.net(g, n, pos, L).mean()
        dec[(name, pos)] = (gross, fee_only-gross, fee_imp-fee_only, full-fee_imp, full)
        P(f"{name} pos {pos}: gross {gross:+.4f} fee {fee_only-gross:+.4f} impact {fee_imp-fee_only:+.4f} tips {full-fee_imp:+.4f} net {full:+.4f}")
# L stats
P(f"\nL=min(liq,0.4mcap) median {np.median(L):.0f}, p10 {np.percentile(L,10):.0f}; share impact(2*pos/L)>10%: " + ", ".join(f"{p}: {np.mean(2*p/L>.1):.2f}" for p in (50,200,1000)))
P(f"zero-cost grid (worst) all-days-ish: configs {len(W)}; train>0 {np.mean(W.tr_zero>0):.3f}, val>0 {np.mean(W.va_zero>0):.3f}, test>0 {np.mean(W.te_zero>0):.3f}")
# zero-cost: overall CI of best selected
json.dump({k: {kk: (list(map(float, vv)) if isinstance(vv, tuple) else vv) for kk, vv in v.items()} for k, v in out.items()}, open(f"{OUT}/wf_summary.json", "w"), default=float, indent=1)
open(f"{OUT}/report.txt", "w").write("\n".join(lines))
