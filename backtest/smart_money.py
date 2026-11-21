"""Smart-money / wallet-following backtest without look-ahead.
Usage: python3 -I smart_money.py <data_dir> <out_dir>
Skill is estimated ONLY from trades with ts < SPLIT (2026-06-24 UTC); signals / entries only at ts >= SPLIT.
Exit simulation + cost model copied from backtest.py / filters.py (SL before TP in-candle, fee 1.25%/side, tip 0.30 USD/tx).
"""
import sys, glob, json, numpy as np, pandas as pd

D, OUT = sys.argv[1], sys.argv[2]
SPLIT = int(pd.Timestamp("2026-06-24", tz="UTC").timestamp())
FEE, TIP, POS, LIQ_ASSUMED, CAND = 0.0125, 0.30, 200, 15000, 900
rng = np.random.default_rng(0)

t = pd.concat([pd.read_parquet(f) for f in sorted(glob.glob(f"{D}/trades-00*.parquet"))], ignore_index=True)
t["s"] = t.ts.dt.as_unit("s").astype("int64")
t = t[t.amount_usd > 0]
wal = pd.read_parquet(f"{D}/wallets.parquet")
tok = pd.read_parquet(f"{D}/tokens.parquet").sort_values("captured_at").drop_duplicates("token_address")
liq_col = tok.set_index("token_address").liquidity_usd
o = pd.read_parquet(f"{D}/ohlcv.parquet").sort_values(["token_address", "ts"])
o["high"] = np.where(o.high > o.close * 10, np.maximum(o.open, o.close), o.high)
paths = {k: g[["ts", "open", "high", "low", "close"]].to_numpy() for k, g in o.groupby("token_address")}
t = t[t.token_address.isin(paths.keys())]          # only tokens we can simulate
print("trades on tokens with OHLCV:", len(t))

# ---------------- (1) skill from train only ----------------
def skill_table(tr, prior_n=10):
    g = tr.assign(b=np.where(tr.side == "buy", tr.amount_usd, 0.0), sl=np.where(tr.side == "sell", tr.amount_usd, 0.0)) \
          .groupby(["wallet", "token_address"], sort=False)[["b", "sl"]].sum().reset_index()
    g = g[g.b > 0]                         # positions with a buy
    g["closed"] = g.sl > 0
    c = g[g.closed].copy()
    c["win"] = c.sl > c.b
    c["pnl"] = c.sl - c.b
    w = c.groupby("wallet").agg(n=("win", "size"), wins=("win", "sum"), pnl=("pnl", "sum"),
                                med_ret=("sl", "size"))  # med_ret placeholder removed below
    w = w.drop(columns="med_ret")
    w["ret"] = c.assign(r=c.sl / c.b).groupby("wallet").r.apply(lambda x: np.log(np.clip(x, .01, 100)).mean())
    p0 = w.wins.sum() / w.n.sum()
    w["skill"] = (w.wins + prior_n * p0) / (w.n + prior_n)           # Beta shrinkage of win rate
    # shrink mean log-return toward population mean as well
    m0 = w.ret.mean()
    w["skill_ret"] = (w.ret * w.n + m0 * prior_n) / (w.n + prior_n)
    nb = g.groupby("wallet").size()
    w["n_open"] = nb.reindex(w.index).values - w.n
    return w, p0

train = t[t.s < SPLIT]
W, p0 = skill_table(train)
print("train wallets scored:", len(W), "pop win rate", round(p0, 3), "wallets n>=5:", (W.n >= 5).sum(), "n>=10:", (W.n >= 10).sum())

# persistence check: skill from days < 06-17, then win rate on 06-17..06-24 (still train-only)
mid = int(pd.Timestamp("2026-06-17", tz="UTC").timestamp())
W1, _ = skill_table(t[t.s < mid])
W2, _ = skill_table(t[(t.s >= mid) & (t.s < SPLIT)])
j = W1[W1.n >= 10].join(W2[W2.n >= 3], lsuffix="1", rsuffix="2", how="inner")
pers = []
for q, name in [(0.99, "top 1%"), (0.95, "top 5%"), (0.80, "top 20%")]:
    th = W1[W1.n >= 10].skill.quantile(q)
    s = j[j.skill1 >= th]
    pers.append((name, len(s), s.wins2.sum() / s.n2.sum(), (s.pnl2 > 0).mean()))
rest = j[j.skill1 < W1[W1.n >= 10].skill.quantile(.80)]
pers.append(("bottom 80%", len(rest), rest.wins2.sum() / rest.n2.sum(), (rest.pnl2 > 0).mean()))
pers = pd.DataFrame(pers, columns=["group", "wallets", "next-week win rate (pooled)", "share wallets pnl>0"])
print(pers.round(3).to_string())

# ---------------- wallet sets ----------------
elig = W[W.n >= 5]
sets = {}
for N in (200, 1000, 3000):
    sets[f"ours_top{N}"] = set(elig.sort_values("skill", ascending=False).head(N).index)
# GMGN (leaky) sets
sm = set(wal.address[wal.wallet_type == "smart_money"])
sets["gmgn_smart_money(leaky)"] = sm
wr = wal.dropna(subset=["win_rate"]).sort_values("win_rate", ascending=False)
sets["gmgn_winrate_top1600(leaky)"] = set(wr.head(1600).address)
sets["gmgn_winrate_top200(leaky)"] = set(wr.head(200).address)
# placebo: random wallets with >=5 closed train tokens, same size as top1000
sets["placebo_random1000"] = set(rng.choice(elig.index.values, 1000, replace=False))
print({k: len(v) for k, v in sets.items()})
# overlap of ours with GMGN
print("overlap ours_top1000 & gmgn_sm:", len(sets["ours_top1000"] & sm), " ours_top3000 & gmgn_sm:", len(sets["ours_top3000"] & sm))

# ---------------- (2) signals ----------------
buys = t[t.side == "buy"][["wallet", "token_address", "s"]]
def signals(wset, k):
    b = buys[buys.wallet.isin(wset)]
    fb = b.groupby(["token_address", "wallet"]).s.min().reset_index().sort_values(["token_address", "s"])
    fb["rank"] = fb.groupby("token_address").cumcount() + 1
    sg = fb[fb["rank"] == k][["token_address", "s"]].rename(columns={"s": "sig"})
    return sg[sg.sig >= SPLIT]            # signal must be formed in test period

# ---------------- exits ----------------
STRATS = {
    "hold_24h": dict(sl=None, tps=[], trail=None, tmax=24),
    "ladder_B": dict(sl=0.50, tps=[(2.0, 0.5), (5.0, 0.25)], trail=0.50, tmax=24),
    "ladder_C": dict(sl=0.40, tps=[(1.5, 0.33), (3.0, 0.33), (10.0, 0.34)], trail=None, tmax=24),
    "tight_D": dict(sl=0.30, tps=[(1.5, 0.5), (3.0, 0.5)], trail=None, tmax=6),
    "scalp_E": dict(sl=0.20, tps=[(1.3, 1.0)], trail=None, tmax=2),
    "runner_F": dict(sl=0.50, tps=[(3.0, 0.5)], trail=0.40, tmax=24),
}
def simulate(seg, sl, tps, trail, tmax):          # identical logic to backtest.py
    entry = seg[0, 1]; left, value, sells, peak = 1.0, 0.0, 0, entry
    tps = list(tps); t_end = seg[0, 0] + tmax * 3600
    for ts, op, hi, lo, cl in seg:
        if ts >= t_end: break
        stop = None
        if sl is not None: stop = entry * (1 - sl)
        if trail is not None and peak > entry * 2: stop = max(stop or 0, peak * (1 - trail))
        if stop is not None and lo <= stop:
            px = min(stop, op); value += left * px / entry; left = 0; sells += 1; break
        for lvl, frac in list(tps):
            if hi >= entry * lvl and left > 0:
                f = min(frac, left); value += f * lvl; left -= f; sells += 1; tps.remove((lvl, frac))
        peak = max(peak, hi)
        if left <= 1e-9: break
    if left > 1e-9:
        last = seg[seg[:, 0] < t_end]; value += left * last[-1, 4] / entry; sells += 1
    return value, sells

def run(sg, delay):
    rows = []
    for tk, sig in zip(sg.token_address, sg.sig):
        p = paths[tk]
        target = (sig // CAND + 1) * CAND + delay * CAND
        i = np.searchsorted(p[:, 0], target)
        if i >= len(p) or p[i, 0] - target > CAND or p[i, 1] <= 0:
            continue
        seg = p[i:]; seg = seg[seg[:, 0] < seg[0, 0] + 24 * 3600]
        rec = {"token_address": tk, "sig": sig, "peak": seg[:, 2].max() / seg[0, 1]}
        for n, s in STRATS.items():
            rec[n], rec[n + "_n"] = simulate(seg, **s)
        rows.append(rec)
    return pd.DataFrame(rows)

def net(df, name, liq):
    imp = (2 * POS / liq.clip(lower=1)).clip(upper=0.9)
    return (df[name] * (1 - FEE - imp) ** 2 - TIP * (1 + df[name + "_n"]) / POS - 1).to_numpy()

def boot(x, n=2000):
    if len(x) < 20: return (np.nan, np.nan)
    idx = rng.integers(0, len(x), (n, len(x)))
    return tuple(np.percentile(x[idx].mean(1), [2.5, 97.5]))

def summ(df, name, liqmode):
    liq = pd.Series(LIQ_ASSUMED, index=df.index) if liqmode == "15k" else \
          df.token_address.map(liq_col).fillna(LIQ_ASSUMED).reset_index(drop=True)
    x = net(df.reset_index(drop=True), name, liq.reset_index(drop=True))
    lo, hi = boot(x)
    return dict(n=len(x), mean=x.mean(), lo=lo, hi=hi, median=np.median(x), win=(x > 0).mean(),
                mean_ex_top1pct=x[x < np.quantile(x, .99)].mean() if len(x) > 20 else np.nan)

# ---------------- run grid ----------------
results = []
base_sg = {}
for sname, wset in sets.items():
    for k in (1, 2, 3):
        sg = signals(wset, k)
        base_sg[(sname, k)] = sg
        df0 = run(sg, 0)
        results.append(dict(set=sname, k=k, signals=len(sg), tradable=len(df0), df=df0))
        print(sname, k, "signals", len(sg), "tradable", len(df0), flush=True)

# baseline: any >=k distinct buyers (no skill) in test, k=3/5/10
anyb = buys.groupby(["token_address", "wallet"]).s.min().reset_index().sort_values(["token_address", "s"])
anyb["rank"] = anyb.groupby("token_address").cumcount() + 1
for k in (3, 10):
    sg = anyb[anyb["rank"] == k][["token_address", "s"]].rename(columns={"s": "sig"}); sg = sg[sg.sig >= SPLIT]
    base_sg[(f"baseline_any_buyers", k)] = sg
    df0 = run(sg, 0)
    results.append(dict(set="baseline_any_buyers", k=k, signals=len(sg), tradable=len(df0), df=df0))

tab = []
for r in results:
    for liqmode in ("15k", "col"):
        for s in STRATS:
            m = summ(r["df"], s, liqmode); m.update(set=r["set"], k=r["k"], liq=liqmode, strat=s, signals=r["signals"])
            tab.append(m)
T = pd.DataFrame(tab)
T.to_csv(f"{OUT}/smart_money_grid.csv", index=False)
raw = pd.DataFrame([{kk: v for kk, v in r.items() if kk != "df"} for r in results])
print(raw.to_string())

# ---------------- (3) latency ----------------
lat = []
for key in [("ours_top1000", 2), ("ours_top1000", 1), ("gmgn_smart_money(leaky)", 2), ("baseline_any_buyers", 3)]:
    sg = base_sg[key]
    dfs = {d: run(sg, d) for d in (0, 1, 2, 4)}
    common = set.intersection(*[set(d.token_address) for d in dfs.values()])
    for d, df in dfs.items():
        for sample, dc in (("common", df[df.token_address.isin(common)]), ("all_tradable", df)):
            for s in ("ladder_B", "tight_D", "hold_24h"):
                m = summ(dc, s, "15k"); m.update(set=key[0], k=key[1], delay=d, strat=s, sample=sample, common=len(common), tradable_d=len(df))
                lat.append(m)
L = pd.DataFrame(lat); L.to_csv(f"{OUT}/smart_money_latency.csv", index=False)

pers.to_csv(f"{OUT}/smart_money_persistence.csv", index=False)
json.dump(dict(p0=p0, train_wallets=len(W), n5=int((W.n >= 5).sum()), n10=int((W.n >= 10).sum()),
               sizes={k: len(v) for k, v in sets.items()}), open(f"{OUT}/smart_money_meta.json", "w"))
print("done")
