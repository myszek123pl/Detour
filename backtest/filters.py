"""Out-of-sample test of entry filters (rule-based from research + LightGBM).
Usage: python3 -I filters.py <out_dir>   (needs sim_results.parquet from backtest.py)
Train: snapshots before 2026-06-24 UTC; test: 2026-06-24 .. 06-29.
"""
import sys, json, numpy as np, pandas as pd, lightgbm as lgb
from sklearn.metrics import roc_auc_score

OUT = sys.argv[1]
FEE, TIP = 0.0125, 0.30
R = pd.read_parquet(f"{OUT}/sim_results.parquet")
R = R[R.peak_mult < 1000].copy()  # drop glitch token(s)
STR = ["hold_24h", "ladder_B", "ladder_C", "tight_D", "scalp_E", "runner_F"]
rng = np.random.default_rng(0)


def net(df, name, pos=200):
    imp = (2 * pos / df.liquidity_usd.clip(lower=1)).clip(upper=0.9)
    return df[name] * (1 - FEE - imp) ** 2 - TIP * (1 + df[name + "_n"]) / pos - 1


def boot(x, n=2000):
    x = np.asarray(x)
    if len(x) < 20:
        return (np.nan, np.nan)
    m = [rng.choice(x, len(x)).mean() for _ in range(n)]
    return tuple(np.percentile(m, [2.5, 97.5]).round(3))


def report(df, label):
    out = {"n": len(df)}
    for s in STR:
        x = net(df, s)
        out[s] = dict(mean=round(float(x.mean()), 3), ci95=boot(x), median=round(float(x.median()), 3),
                      win=round(float((x > 0).mean()), 3))
    print(f"\n== {label} (n={len(df)})")
    print(pd.DataFrame({k: v for k, v in out.items() if k != "n"}).T.to_string())
    return out


results = {}
split = pd.Timestamp("2026-06-24", tz="UTC")
tr, te = R[R.captured_at < split], R[R.captured_at >= split]
results["all"] = report(R, "ALL tokens, $200 position")
results["test_all"] = report(te, "TEST period, no filter")

# --- rule-based filter from research (safety + anti-insider + liquidity)
def rules(df):
    return df[(df.mint_disabled == 1) & (df.freeze_disabled == 1)
              & (df.top10_holder_pct.fillna(1) < 0.30)
              & (df.dev_remaining_pct.fillna(0) < 0.05)
              & (df.bundler_pct_holders.fillna(0) < 0.15)
              & (df.insider_pct_holders.fillna(0) < 0.15)
              & (df.liquidity_usd >= 10000)]

results["test_rules"] = report(rules(te), "TEST, research safety rules")

# --- univariate: which features separate peak>=2x in TRAIN (AUC)
feats = [c for c in R.columns if c not in STR and not c.endswith("_n") and R[c].dtype.kind in "fib"
         and c not in ("peak_mult", "final_mult", "cap_ts", "sample_id", "price_at_capture")
         and not c.startswith(("max_return", "staged", "runner_peak", "scalp", "mdd", "time_to_peak", "close_return", "reaches"))]
y_tr = (tr.peak_mult >= 2).astype(int)
auc = {}
for f in feats:
    v = tr[f].astype(float)
    if v.notna().mean() < 0.5 or v.nunique() < 3:
        continue
    a = roc_auc_score(y_tr, v.fillna(v.median()))
    auc[f] = round(max(a, 1 - a), 3) * (1 if a >= 0.5 else -1)
top = sorted(auc.items(), key=lambda kv: -abs(kv[1]))[:15]
print("\nTop single features vs peak>=2x on TRAIN (signed AUC):", top)
results["feature_auc_top15"] = top

# --- LightGBM: predict net ladder_B return > 0 ; evaluate top-k% on TEST
X_tr, X_te = tr[feats].astype(float), te[feats].astype(float)
for target in ("ladder_B", "hold_24h", "tight_D"):
    y = (net(tr, target) > 0).astype(int)
    m = lgb.LGBMClassifier(n_estimators=300, learning_rate=0.03, num_leaves=15, min_child_samples=50,
                           subsample=0.8, subsample_freq=1, colsample_bytree=0.7, verbose=-1, random_state=0)
    m.fit(X_tr, y)
    p = m.predict_proba(X_te)[:, 1]
    yt = (net(te, target) > 0).astype(int)
    a = roc_auc_score(yt, p)
    print(f"\n### LightGBM target={target} TEST AUC={a:.3f}")
    results[f"lgb_{target}_auc"] = round(a, 3)
    for k in (0.05, 0.10, 0.20):
        sel = te[p >= np.quantile(p, 1 - k)]
        x = net(sel, target)
        r = dict(n=len(sel), mean=round(float(x.mean()), 3), ci95=boot(x), median=round(float(x.median()), 3),
                 win=round(float((x > 0).mean()), 3), share_2x=round(float((sel.peak_mult >= 2).mean()), 3))
        print(f"  top {int(k*100)}%: {r}")
        results[f"lgb_{target}_top{int(k*100)}"] = r
    imp = sorted(zip(feats, m.feature_importances_), key=lambda z: -z[1])[:10]
    results[f"lgb_{target}_importance"] = [(f, int(i)) for f, i in imp]

print("\nBase share peak>=2x  train:", round(float((tr.peak_mult >= 2).mean()), 3),
      " test:", round(float((te.peak_mult >= 2).mean()), 3))
json.dump(results, open(f"{OUT}/filters_results.json", "w"), indent=1, default=str)
