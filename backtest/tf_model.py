"""Step 3: LightGBM on trade features, time split, net returns. python3 -I tf_model.py <work>"""
import sys, json, numpy as np, pandas as pd, lightgbm as lgb
from sklearn.metrics import roc_auc_score
W = sys.argv[1]; OUT = "out"
FEE, TIP = 0.0125, 0.30
R = pd.read_parquet(f"{OUT}/sim_results.parquet"); R = R[R.peak_mult < 1000].copy()
F = pd.read_parquet(f"{W}/features.parquet")
print("sim tokens", len(R), "with trade feats", R.token_address.isin(F.index).sum())
R = R.merge(F, left_on="token_address", right_index=True, how="left")
tf = [c for c in F.columns]
STR = ["hold_24h", "ladder_B", "tight_D"]
split = pd.Timestamp("2026-06-24", tz="UTC")
tr, te = R[R.captured_at < split].copy(), R[R.captured_at >= split].copy()
print("train", len(tr), "test", len(te), "| pre-capture coverage: tokens with >=1 pre trade", R.f_n_buys.notna().mean().round(4),
      "median n_buys", R.f_n_buys.median(), "frac with >=10 buys", (R.f_n_buys >= 10).mean().round(3))
print("cap-time split share of trade-feature NaN: train", tr.f_n_buys.isna().mean().round(4), "test", te.f_n_buys.isna().mean().round(4))
def net(df, name, impact, pos=200):
    liq = df.liquidity_usd.clip(lower=1) if impact == "liq" else 15000.0
    imp = (2 * pos / liq)
    imp = imp.clip(upper=0.9) if impact == "liq" else min(imp, 0.9)
    return df[name] * (1 - FEE - imp) ** 2 - TIP * (1 + df[name + "_n"]) / pos - 1
rng = np.random.default_rng(0)
def boot(x, n=2000):
    x = np.asarray(x); idx = rng.integers(0, len(x), (n, len(x)))
    return np.percentile(x[idx].mean(1), [2.5, 97.5])
snap = [c for c in R.columns if c not in STR and not c.endswith("_n") and R[c].dtype.kind in "fib" and not c.startswith("f_")
        and c not in ("peak_mult", "final_mult", "cap_ts", "sample_id", "price_at_capture")
        and not c.startswith(("max_return", "staged", "runner_peak", "scalp", "mdd", "time_to_peak", "close_return", "reaches"))]
FS = {"trade": tf, "snapshot": snap, "trade+snapshot": tf + snap}
# univariate AUC of trade feats vs peak>=2x on train and test
y2 = lambda d: (d.peak_mult >= 2).astype(int)
rows = []
for f in tf:
    a1 = roc_auc_score(y2(tr), tr[f].fillna(tr[f].median())); a2 = roc_auc_score(y2(te), te[f].fillna(tr[f].median()))
    rows.append((f, round(a1, 3), round(a2, 3)))
uni = pd.DataFrame(rows, columns=["feature", "AUC_train", "AUC_test"]); uni["d"] = (uni.AUC_train - .5).abs()
print(uni.sort_values("d", ascending=False).head(12).drop(columns="d").to_string(index=False))
res = []; 
for impact in ("liq", "fix15k"):
    for tgt in STR:
        base = net(te, tgt, impact)
        res.append(dict(impact=impact, target=tgt, fs="ALL test (no filter)", k="100%", n=len(te), mean=base.mean(), lo=boot(base)[0], hi=boot(base)[1],
                        median=base.median(), win=(base > 0).mean(), auc=np.nan))
        ytr = (net(tr, tgt, impact) > 0).astype(int); yte = (net(te, tgt, impact) > 0).astype(int)
        for fsn, cols in FS.items():
            P = 0
            for seed in range(3):
                m = lgb.LGBMClassifier(n_estimators=200, n_jobs=4, learning_rate=0.03, num_leaves=15, min_child_samples=50, subsample=0.8,
                                       subsample_freq=1, colsample_bytree=0.7, verbose=-1, random_state=seed)
                m.fit(tr[cols].astype(float), ytr); P = P + m.predict_proba(te[cols].astype(float))[:, 1] / 3
            auc = roc_auc_score(yte, P)
            if fsn == "trade" and impact == "fix15k" and tgt == "ladder_B":
                imp = sorted(zip(cols, m.booster_.feature_importance("gain")), key=lambda z: -z[1])[:8]
                print("trade importance (gain, last seed):", [(a, int(b)) for a, b in imp])
            for k in (0.05, 0.10, 0.20):
                sel = te[P >= np.quantile(P, 1 - k)]; x = net(sel, tgt, impact); lo, hi = boot(x)
                res.append(dict(impact=impact, target=tgt, fs=fsn, k=f"top{int(k*100)}%", n=len(sel), mean=x.mean(), lo=lo, hi=hi,
                                median=x.median(), win=(x > 0).mean(), auc=auc))
        # shuffled-label sanity (trade feats)
        P = 0
        for seed in range(3):
            m = lgb.LGBMClassifier(n_estimators=200, n_jobs=4, learning_rate=0.03, num_leaves=15, min_child_samples=50, subsample=0.8, subsample_freq=1,
                                   colsample_bytree=0.7, verbose=-1, random_state=seed)
            m.fit(tr[tf].astype(float), np.random.default_rng(seed).permutation(ytr)); P = P + m.predict_proba(te[tf].astype(float))[:, 1] / 3
        sel = te[P >= np.quantile(P, .9)]; x = net(sel, tgt, impact)
        res.append(dict(impact=impact, target=tgt, fs="trade, SHUFFLED train labels", k="top10%", n=len(sel), mean=x.mean(), lo=boot(x)[0], hi=boot(x)[1],
                        median=x.median(), win=(x > 0).mean(), auc=roc_auc_score(yte, P)))
D = pd.DataFrame(res)
D.to_csv(f"{W}/model_results.csv", index=False)
pd.set_option("display.width", 250)
print(D.round(3).to_string(index=False))
