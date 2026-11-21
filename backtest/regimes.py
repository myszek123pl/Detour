"""Market-regime analysis across the three public datasets.
Usage: python3 -I regimes.py <datasets_dir> <out_dir> [part]   part in {series, persist, hmm, oos}
Run from /home/user/Detour/backtest (regimes_lib imported via sys.path of script dir; -I removes cwd, so we add it explicitly).
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from scipy import stats
import regimes_lib as rl

pd.set_option("display.width", 220); pd.set_option("display.max_columns", 40); pd.set_option("display.max_rows", 400)
DD, OUT = sys.argv[1], sys.argv[2]; PART = sys.argv[3] if len(sys.argv) > 3 else "series"
DAY, H4 = 86400, 4 * 3600
STR = ["ladder_B", "tight_D", "runner_F", "scalp_E", "hold_24h"]

# ---- load ----
R = pd.read_parquet(f"{OUT}/sim_results.parquet")
for s in STR: R["net_" + s] = rl.net_returns(R, s, 200.0)
R = R.sort_values("cap_ts").reset_index(drop=True)
L = pd.read_csv(f"{DD}/solana-pumpfun-launches/repo/solana_launches_public.csv").sort_values("launch_unix").reset_index(drop=True)
C = pd.read_json(f"{DD}/solana-memecoin-calls-dataset/repo/calls.jsonl", lines=True).sort_values("t").reset_index(drop=True)
LP = 0.5   # proxy: loss on a non-2x trade (launches/calls have no path) -> payoff FEE*(2 if hit else 1-LP)-1
for D_, col in ((L, "multiple"), (C, "peak")):
    D_["hit2"] = (D_[col] >= 2).astype(int); D_["hit5"] = (D_[col] >= 5).astype(int)
    for lp in (.3, .5, .7): D_[f"pay{int(lp*100)}"] = rl.FEE * np.where(D_.hit2 == 1, 2.0, 1 - lp) - 1
R["hit2"] = (R.peak_mult >= 2).astype(int); R["hit5"] = (R.peak_mult >= 5).astype(int)


def build(freq):
    ex_t = {f"net_{s}": rl.winsor(R["net_" + s].to_numpy()) for s in STR}
    ex_t.update({f"raw_{s}": R["net_" + s].to_numpy() for s in ("ladder_B", "tight_D", "runner_F")})
    T = rl.make_series(R, "cap_ts", freq, R.hit2, R.hit5, R.peak_mult, ex_t)
    La = rl.make_series(L, "launch_unix", freq, L.hit2, L.hit5, L.multiple, {"pay50": L.pay50, "pay30": L.pay30, "pay70": L.pay70})
    Ca = rl.make_series(C, "t", freq, C.hit2, C.hit5, C.peak, {"pay50": C.pay50, "pay30": C.pay30, "pay70": C.pay70})
    return T, La, Ca


def dstr(b, freq): return pd.to_datetime(b * freq, unit="s").strftime("%Y-%m-%d")


if PART == "series":
    T, La, Ca = build(DAY)
    for nm, S in (("TOKENS (sim_results, Jun 2026)", T), ("LAUNCHES (Jul-Sep 2026)", La), ("CALLS (Jun-Nov 2026)", Ca)):
        print("\n=====", nm, "daily: days", len(S), "missing", int(S.n.isna().sum()))
        X = S.copy(); X.index = dstr(X.index.to_numpy(), DAY)
        cols = [c for c in ["n", "p2", "p5", "med_peak", "net_ladder_B", "net_tight_D", "net_runner_F", "pay50"] if c in X]
        print(X[cols].round(3).to_string() if len(X) < 70 else X[cols].round(3).iloc[::3].to_string())
        print(X[cols].describe().round(3).to_string())
    for nm, S in (("LAUNCHES", La), ("CALLS", Ca)):  # weekly
        W = S.copy(); W["wk"] = (W.index - W.index.min()) // 7
        g = W.groupby("wk").agg(days=("n", "size"), n=("n", "sum"), k2=("k2", "sum"), k5=("k5", "sum"), med=("med_peak", "median"), pay50=("pay50", "mean"))
        g["p2"] = g.k2 / g.n; g["p5"] = g.k5 / g.n; g["start"] = dstr((W.index.min() + g.index.to_numpy() * 7), DAY)
        print("\n== WEEKLY", nm); print(g.round(3).to_string())
    W = T.copy(); W["wk"] = (W.index - W.index.min()) // 7
    g = W.groupby("wk").agg(days=("n", "size"), n=("n", "sum"), k2=("k2", "sum"), k5=("k5", "sum"), med=("med_peak", "median"), lad=("net_ladder_B", "mean"), tgt=("net_tight_D", "mean"), run=("net_runner_F", "mean"))
    g["p2"] = g.k2 / g.n; g["p5"] = g.k5 / g.n; print("\n== WEEKLY TOKENS(3 chunks of 7d)"); print(g.round(3).to_string())

if PART == "persist":
    out = {}
    for freq, fn in ((DAY, "daily"), (H4, "4h-block")):
        T, La, Ca = build(freq)
        for nm, S in (("tokens", T), ("launches", La), ("calls", Ca)):
            S = S[S.n > 0] if freq == H4 else S
            if nm == "tokens" and freq == DAY: S = S.iloc[1:]   # first day partial (starts 08:36) -> keep but flag? keep all but drop none
            print(f"\n##### {nm} {fn}  T={len(S)}  mean n/period={S.n.mean():.1f}  min-detectable |r1|~{2/np.sqrt(len(S)):.2f}")
            k2, n = S.k2.to_numpy(float), S.n.to_numpy(float)
            # seasonality removal for 4h blocks: subtract time-of-day mean of the pearson residual
            z2, _ = rl.pearson_resid(k2, n); z5, _ = rl.pearson_resid(S.k5.to_numpy(float), n)
            if freq == H4:
                tod = (S.index.to_numpy() % 6)
                for z in (z2, z5):
                    for b in range(6): z[tod == b] -= z[tod == b].mean()
            d2 = rl.dispersion(k2, n); d5 = rl.dispersion(S.k5.to_numpy(float), n)
            print("dispersion p2:", {k: round(v, 4) for k, v in d2.items()}); print("dispersion p5:", {k: round(v, 4) for k, v in d5.items()})
            rows = []
            series = {"p2 (pearson-resid)": z2, "p5 (pearson-resid)": z5, "log n (detrended)": rl.lin_detrend(np.log(n)), "log n (raw)": np.log(n),
                      "med_peak (log, detrended)": rl.lin_detrend(np.log(S.med_peak.to_numpy(float)))}
            for c in ("net_ladder_B", "net_tight_D", "net_runner_F", "pay50"):
                if c in S: series[c + " (mean/period)"] = S[c].to_numpy(float)
            for lab, x in series.items():
                a = rl.acf(x, (1, 2, 3)); o, p = rl.perm_p(x, 4000)
                rows.append(dict(series=lab, r1=a[0], r2=a[1], r3=a[2], perm_p_r1=p, bartlett95=1.96 / np.sqrt(len(x)), spearman_next=stats.spearmanr(x[:-1], x[1:], nan_policy="omit")[0]))
            print(pd.DataFrame(rows).round(3).to_string(index=False))
            ct = rl.cond_table(z2); print("P(good next|good) vs |bad  [p2 resid > median]:", {k: round(v, 3) for k, v in ct.items()})
            out[f"{nm}_{fn}"] = dict(disp_p2=d2, disp_p5=d5, rows=rows, cond=ct)
        if freq == DAY:
            # ANOVA across days on per-trade net returns for tokens
            print("\n## tokens: do days differ in per-trade net return? (per-trade, winsor 99%)")
            R["day"] = R.cap_ts // DAY; Rd = R[R.cap_ts // DAY > R.cap_ts.min() // DAY]
            for s in ("ladder_B", "tight_D", "runner_F"):
                x = rl.winsor(Rd["net_" + s].to_numpy()); g = [x[Rd.day.to_numpy() == d] for d in np.unique(Rd.day)]
                F = stats.f_oneway(*g); K = stats.kruskal(*g)
                print(s, f"ANOVA F={F.statistic:.2f} p={F.pvalue:.3g};  Kruskal H={K.statistic:.1f} p={K.pvalue:.3g}; between-day sd of mean={np.std([a.mean() for a in g], ddof=1):.3f}  within-day sd/sqrt(n)={np.mean([a.std()/np.sqrt(len(a)) for a in g]):.3f}")
    json.dump(out, open(f"{OUT}/regimes_persist.json", "w"), indent=1, default=float)

if PART == "cross":
    T, La, Ca = build(DAY)
    ov = La.join(Ca, lsuffix="_L", rsuffix="_C", how="inner").dropna(subset=["n_L", "n_C"])
    print("overlap days", len(ov), dstr(ov.index.min(), DAY), dstr(ov.index.max(), DAY))
    zL, _ = rl.pearson_resid(ov.k2_L.to_numpy(float), ov.n_L.to_numpy(float)); zC, _ = rl.pearson_resid(ov.k2_C.to_numpy(float), ov.n_C.to_numpy(float))
    z5L, _ = rl.pearson_resid(ov.k5_L.to_numpy(float), ov.n_L.to_numpy(float)); z5C, _ = rl.pearson_resid(ov.k5_C.to_numpy(float), ov.n_C.to_numpy(float))
    nL, nC = rl.lin_detrend(np.log(ov.n_L.to_numpy(float))), rl.lin_detrend(np.log(ov.n_C.to_numpy(float)))
    mL, mC = rl.lin_detrend(np.log(ov.med_peak_L.to_numpy(float))), rl.lin_detrend(np.log(ov.med_peak_C.to_numpy(float)))
    X = {"p2": (zL, zC), "p5": (z5L, z5C), "log n (detr)": (nL, nC), "log med peak (detr)": (mL, mC)}
    print("\nsame-day correlation launches vs calls (Spearman r, p):")
    for k, (a, b) in X.items(): r = stats.spearmanr(a, b); print(f"  {k:22s} r={r.statistic:+.3f} p={r.pvalue:.3f}")
    print("\nlagged: launches_t -> calls_{t+1}, calls_t -> launches_{t+1}")
    for k, (a, b) in X.items():
        r1 = stats.spearmanr(a[:-1], b[1:]); r2 = stats.spearmanr(b[:-1], a[1:]); print(f"  {k:22s} L->C {r1.statistic:+.3f} (p={r1.pvalue:.2f})   C->L {r2.statistic:+.3f} (p={r2.pvalue:.2f})")
    comp = (zL + zC) / np.sqrt(2)
    print("\ncomposite (avg z of p2) lag1:", [round(v, 3) for v in rl.acf(comp, (1, 2))], "vs launches", [round(v, 3) for v in rl.acf(zL, (1, 2))], "calls", [round(v, 3) for v in rl.acf(zC, (1, 2))])
    print("perm p composite r1:", rl.perm_p(comp, 5000))
    # time-of-day tables
    for nm, D_, tc, y in (("tokens", R, "cap_ts", "hit2"), ("launches", L, "launch_unix", "hit2"), ("calls", C, "t", "hit2")):
        h = (D_[tc] // 3600 % 24 // 4); g = D_.groupby(h).agg(n=(y, "size"), p2=(y, "mean"))
        chi = stats.chi2_contingency(pd.crosstab(h, D_[y]))
        print(f"\n{nm} p2 by UTC 4h block (0=00-04..5=20-24): ", g.round(3).T.to_string(), f"\n chi2 p={chi[1]:.3g}")
        dow = pd.to_datetime(D_[tc], unit="s").dt.dayofweek; g = D_.groupby(dow).agg(n=(y, "size"), p2=(y, "mean")); chi = stats.chi2_contingency(pd.crosstab(dow, D_[y]))
        print(f"{nm} p2 by day of week (0=Mon):", g.round(3).T.to_string(), f"\n chi2 p={chi[1]:.3g}")

if PART == "hmm":
    T, La, Ca = build(DAY); res = {}
    for nm, S in (("tokens", T), ("launches", La), ("calls", Ca)):
        for y in ("k2", "k5"):
            S2 = S.dropna(subset=["n"]); k, n = S2[y].to_numpy(float), S2.n.to_numpy(float)
            r = rl.hmm_bootstrap(k, n, B=int(os.environ.get("NB", 60)))
            h = r["hmm"]; stay = np.diag(h["A"]); dur = 1 / (1 - stay)
            print(f"\n[{nm} {y.replace('k','p')}] T={len(k)} p_states={np.round(h['p'],3)} stay={np.round(stay,3)} exp.duration(d)={np.round(dur,1)} occupancy={np.round(h['gamma'].mean(0),2)}")
            print(f"   LRT vs 1-state = {r['lrt_vs_1state']:.2f} (boot p={r['p_vs_1state']:.3f});  LRT vs iid-mixture = {r['lrt_vs_iid']:.2f} (boot p={r['p_vs_iid']:.3f});  1-state p={k.sum()/n.sum():.3f}")
            res[f"{nm}_{y}"] = dict(p=h["p"].tolist(), A=h["A"].tolist(), lrt1=r["lrt_vs_1state"], p1=r["p_vs_1state"], lrt_iid=r["lrt_vs_iid"], p_iid=r["p_vs_iid"])
    json.dump(res, open(f"{OUT}/regimes_hmm.json", "w"), indent=1)

if PART == "oos":
    WARM = 7; resall = {}
    T, La, Ca = build(DAY)
    T = T.iloc[1:] if False else T

    def run(nm, S, Scol, Ncol, k2col, lag, warm=WARM, label=""):
        """Expanding-window walk-forward. Signals use only days <= d-lag. Thresholds = expanding quantile of signal history."""
        S = S.copy(); n = S.n.fillna(0).to_numpy(float); pay = (S[Scol].fillna(0) * S.n.fillna(0)).to_numpy(float)
        k2 = S[k2col].fillna(0).to_numpy(float); Tn = len(S); p2 = np.where(n > 0, k2 / np.maximum(n, 1), np.nan)
        test = np.zeros(Tn, bool); test[warm + lag - 1:] = True; test &= n > 0
        sig = {}
        def lagged(x, w=1):  # value of pooled stat over days d-lag-w+1..d-lag
            out = np.full(Tn, np.nan)
            for d in range(Tn):
                lo, hi = d - lag - w + 1, d - lag
                if lo >= 0: out[d] = np.nansum(x[lo:hi + 1])
            return out
        sig["p2_prev1d"] = lagged(k2) / lagged(n)
        sig["p2_prev3d"] = lagged(k2, 3) / lagged(n, 3)
        sig["count_prev1d"] = lagged(n)
        sig["pnl_prev1d"] = lagged(pay) / lagged(n)
        sig["pnl_prev3d"] = lagged(pay, 3) / lagged(n, 3)
        # HMM filtered P(high state) for day d from data <= d-lag
        ph = np.full(Tn, np.nan)
        for d in range(warm + lag, Tn):
            hist = np.arange(0, d - lag + 1); hist = hist[n[hist] > 0]
            if len(hist) < warm: continue
            par = rl.hmm_fit(k2[hist], n[hist], 2, inits=4, iters=100, seed=d)
            al = rl.hmm_filter(k2[hist], n[hist], par)[-1]; pr = al @ np.linalg.matrix_power(par["A"], lag)
            ph[d] = pr[1] if par["p"][1] - par["p"][0] > .02 else 0.5
        sig["hmm_P_high"] = ph
        rules = {}
        for sname, x in sig.items():
            for qn, q in (("top50", .5), ("skip_worst33", 1 / 3)):
                thr = np.full(Tn, np.nan)
                for d in range(Tn):
                    h = x[:d - lag + 1 if d - lag + 1 > 0 else 0]; h = h[~np.isnan(h)]
                    # history of the signal available at decision time: signal values for days <= d-lag (those are fixed already)
                    if len(h) >= 3: thr[d] = np.quantile(h, q)
                sel = (x >= thr) if sname != "hmm_P_high" else (x >= 0.5)
                if sname == "hmm_P_high" and qn == "skip_worst33": continue
                sel = np.where(np.isnan(x) | np.isnan(thr) & (sname != "hmm_P_high"), False, sel)
                rules[f"{sname}|{qn}"] = sel
            if sname == "p2_prev1d":   # N consecutive good days: previous N days all above expanding median of p2
                for Nn in (2, 3):
                    good = np.zeros(Tn, bool)
                    for d in range(Tn):
                        ds = [d - lag - j for j in range(Nn)]
                        if min(ds) < 0: continue
                        hist = p2[:d - lag + 1]; hist = hist[~np.isnan(hist)]
                        if len(hist) < 3: continue
                        good[d] = all(p2[j] >= np.median(hist) for j in ds if not np.isnan(p2[j])) and not any(np.isnan(p2[j]) for j in ds)
                    rules[f"{Nn}_consecutive_good_days"] = good
        # inverse of the best-performing family as sign check (trade only when signal is BAD)
        rows = [("ALWAYS (baseline)", rl.eval_rule(pay, n, np.ones(Tn, bool), test))]
        for r, sel in rules.items(): rows.append((r, rl.eval_rule(pay, n, sel, test)))
        rows.append(("INVERSE p2_prev1d|top50 (trade only after below-median days)", rl.eval_rule(pay, n, ~rules["p2_prev1d|top50"] & ~np.isnan(sig["p2_prev1d"]), test)))
        # oracle (same-day p2 above expanding median -> unobservable upper bound)
        orc = np.zeros(Tn, bool)
        for d in range(Tn):
            h = p2[:d]; h = h[~np.isnan(h)]
            if len(h) >= 3 and not np.isnan(p2[d]): orc[d] = p2[d] >= np.median(h)
        rows.append(("ORACLE same-day p2>=median (not tradable)", rl.eval_rule(pay, n, orc, test)))
        df = pd.DataFrame([dict(rule=a, **{k: v for k, v in b.items() if k != "ci"}, ci_lo=b.get("ci", (np.nan, np.nan))[0], ci_hi=b.get("ci", (np.nan, np.nan))[1]) for a, b in rows])
        print(f"\n### {nm} | payoff={Scol} | lag={lag}d | warm-up={warm}d | test days={int(test.sum())} {label}")
        print(df[["rule", "days_traded", "frac", "trades", "mean", "base", "lift", "ci_lo", "ci_hi", "p_vs_random", "pnl_per_day", "base_pnl_per_day"]].round(4).to_string(index=False))
        resall[f"{nm}|{Scol}|lag{lag}"] = df.to_dict("records")

    for lag in (1, 2):
        for sc in ("raw_ladder_B", "raw_tight_D", "raw_runner_F"):
            run("tokens", T, sc, "n", "k2", lag, warm=6)
        run("launches", La, "pay50", "n", "k2", lag)
        run("launches", La, "pay70", "n", "k2", lag)
        run("calls", Ca, "pay50", "n", "k2", lag)
        run("calls", Ca, "pay70", "n", "k2", lag)
    json.dump(resall, open(f"{OUT}/regimes_oos.json", "w"), indent=1, default=float)
