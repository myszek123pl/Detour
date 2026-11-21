"""Practitioner entry filters x practitioner exit rules on ian05012 snapshots + 15m candles.
Usage: python3 -I run_filters.py   -> out/practitioners/{sims.parquet,results.csv}
"""
import sys, itertools, json, numpy as np, pandas as pd
sys.path.insert(0, "/home/user/Detour/backtest/practitioners")
import lib

R, n0 = lib.load_universe()
W = pd.read_parquet(f"{lib.OUT}/wallet_proxy.parquet")
R = R.merge(W[["pre_trades", "top1_buy_share", "top1_net_share"]], left_on="token_address", right_index=True, how="left")
P = lib.build_paths(set(R.token_address))

# ---------- exit rules (all through backtest.simulate) ----------
H = 24
EX = {  # name: callable(seg)->(value,nsells)
    "hold_24h":   lambda s: lib.simulate(s, None, [], None, H),
    "camol_2x50": lambda s: lib.simulate(s, None, [(2.0, 0.5)], None, H),                  # sell 50% at 2x, rest held
    "camol_2x50_sl50": lambda s: lib.simulate(s, 0.5, [(2.0, 0.5)], None, H),
    "refl_2x50_moon": lambda s: lib.simulate(s, None, [(2.0, 0.5)], 0.5, H),               # initials at 2x, 50% trail on moonbag
    "refl_3x33_moon": lambda s: lib.simulate(s, None, [(3.0, 1 / 3)], 0.5, H),             # initials at 3x
    "ladder_B":   lambda s: lib.simulate(s, 0.5, [(2.0, 0.5), (5.0, 0.25)], 0.5, H),       # reference from earlier notes
}


def fastcut(seg, k, thr=0.0):
    """Cupsey-style: after k 15m candles, if close < entry*(1+thr) sell everything; else camol exit."""
    e = seg[0, 1]
    if len(seg) >= k and seg[k - 1, 4] >= e * (1 + thr):
        return lib.simulate(seg, None, [(2.0, 0.5)], None, H)
    return lib.simulate(seg, None, [(2.0, 0.5)], None, k * 0.25)


EX["fastcut_15m"] = lambda s: fastcut(s, 1)
EX["fastcut_30m"] = lambda s: fastcut(s, 2)
EX["fastcut_15m_up10"] = lambda s: fastcut(s, 1, 0.10)   # must be >= +10% after 15 min
EX["hold_1h"] = lambda s: lib.simulate(s, None, [], None, 1)
EX["hold_4h"] = lambda s: lib.simulate(s, None, [], None, 4)
EX["camol_2x50_1h"] = lambda s: lib.simulate(s, None, [(2.0, 0.5)], None, 1)
EX["scalp15_only"] = lambda s: lib.simulate(s, None, [], None, 0.25)  # pure 15-minute hold (reference)


def haircut(seg):
    """Terminal haircut: if the path ends before the 24h horizon append a candle at 50% of the last close."""
    if seg[-1, 0] + 900 >= seg[0, 0] + lib.HORIZON:
        return seg
    c = seg[-1, 4] * 0.5
    return np.vstack([seg, [seg[-1, 0] + 900, c, c, c, c]])


rows = []
for tok in R.token_address:
    s = P[tok]; sh = haircut(s)
    rec = {"token_address": tok, "n_candles": len(s), "cover_h": (s[-1, 0] - s[0, 0] + 900) / 3600}
    for k, f in EX.items():
        v, n = f(s); rec[k] = v; rec[k + "_n"] = n
    for k in ("hold_24h", "camol_2x50", "refl_2x50_moon", "fastcut_15m", "fastcut_30m"):
        v, n = EX[k](sh); rec[k + "_hc"] = v; rec[k + "_hc_n"] = n
    rows.append(rec)
S = pd.DataFrame(rows)
D = R.drop(columns=[c for c in S.columns if c in R.columns and c != "token_address"]).merge(S, on="token_address")
D.to_parquet(f"{lib.OUT}/sims.parquet")
print("rows", len(D), "test rows", int(D.test.sum()))

# ---------- filters (thresholds fixed in advance from the notes) ----------
dev = D.dev_remaining_pct <= 0.05
snp = D.sniper_count <= 2
t15 = D.top10_holder_pct <= 0.15
t10 = D.top10_holder_pct <= 0.10
w05 = D.top1_net_share <= 0.05
w10 = D.top1_net_share <= 0.10
FILT = {
    "ALL (unfiltered)": pd.Series(True, index=D.index),
    "dev<=5%": dev,
    "snipers<=2": snp,
    "top10<=15%": t15,
    "top10<=10%": t10,
    "GREMLIN15: dev<=5 & sn<=2 & top10<=15": dev & snp & t15,
    "GREMLIN10: dev<=5 & sn<=2 & top10<=10": dev & snp & t10,
    "wallet-proxy top1net<=5%": w05.fillna(False),
    "wallet-proxy top1net<=10%": w10.fillna(False),
    "GREMLIN15 & wallet-proxy<=10%": (dev & snp & t15 & w10.fillna(False)),
}
STR = list(EX) + [k + "_hc" for k in ("hold_24h", "camol_2x50", "refl_2x50_moon", "fastcut_15m", "fastcut_30m")]
COSTS = {"Lcap": "L_cap", "L15k": "L_fix"}
POS = (75, 200)
B = 2000
rng = np.random.default_rng(42)
recs = []
for per in ("all", "train", "test"):
    base = D if per == "all" else (D[~D.test] if per == "train" else D[D.test])
    base_idx = base.index.to_numpy()
    N = len(base_idx)
    # precompute net matrices for the whole period universe
    NET = {}
    for st in STR:
        for cn, cc in COSTS.items():
            for pos in POS:
                NET[(st, cn, pos)] = lib.net_ret(base[st].to_numpy(), base[st + "_n"].to_numpy(), base[cc].to_numpy(), pos)
    days = base.day.to_numpy()
    for fn, m in FILT.items():
        mm = m.loc[base_idx].to_numpy()
        pos_idx = np.flatnonzero(mm)
        n = len(pos_idx)
        if n < 15:
            for st in STR:
                recs.append(dict(period=per, filt=fn, strat=st, cost="Lcap", pos=75, n=n)); 
            continue
        bi = rng.integers(0, n, (B, n))
        # block bootstrap over days
        dd = pd.factorize(days[pos_idx])[0]; kd = dd.max() + 1
        pick = rng.integers(0, kd, (B, kd)); cnt = np.bincount(dd, minlength=kd).astype(float)
        # random equal-size subsets of the period universe
        if fn.startswith("ALL"):
            rs = None
        else:
            rs = np.argpartition(rng.random((B, N)), n - 1, axis=1)[:, :n] if n < N else None
        for (st, cn, pos), x in NET.items():
            xf = x[pos_idx]
            mean = xf.mean()
            ci = np.percentile(xf[bi].mean(1), [2.5, 97.5])
            sd = np.bincount(dd, weights=xf, minlength=kd)
            cib = np.percentile(sd[pick].sum(1) / cnt[pick].sum(1), [2.5, 97.5])
            rec = dict(period=per, filt=fn, strat=st, cost=cn, pos=pos, n=n, mean=mean, median=np.median(xf),
                       win=(xf > 0).mean(), lo=ci[0], hi=ci[1], blo=cib[0], bhi=cib[1], uf_mean=x.mean())
            if rs is not None:
                rm = x[rs].mean(1)
                rec.update(rand_mean=rm.mean(), rand_lo=np.percentile(rm, 2.5), rand_hi=np.percentile(rm, 97.5),
                           p_rand=float((rm >= mean).mean()))
            recs.append(rec)
RES = pd.DataFrame(recs)
RES.to_csv(f"{lib.OUT}/results.csv", index=False)
pr = {k: float(v.loc[D.index].mean()) for k, v in FILT.items()}
pr_n = {k: int(v.sum()) for k, v in FILT.items()}
json.dump({"pass_rate": pr, "n": pr_n, "n_before_lm_drop": n0, "n_after": len(D)}, open(f"{lib.OUT}/meta.json", "w"), indent=1)
print(json.dumps({"pass_rate": pr, "n": pr_n}, indent=1))
