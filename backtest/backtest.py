"""Path-based backtest of memecoin entry/exit rules on the public
ian05012/solana-memecoin-dataset (GMGN snapshots + 15m OHLCV, June 2026).

Usage: python3 -I backtest.py <data_dir> <out_dir>

Conservative assumptions (see README.md in this folder):
- entry at OPEN of first 15m candle starting at/after snapshot time (<=15 min later)
- intra-candle ambiguity: stop-loss assumed to trigger before take-profit
- glitch candles (high > 10x close) have high clipped to max(open, close)
- costs per side: fee + price impact (2*pos/liquidity) ; fixed tip per tx
"""
import sys, json, numpy as np, pandas as pd

D, OUT = sys.argv[1], sys.argv[2]
FEE = 0.0125          # pump.fun / PumpSwap low-mcap tier per side (pump-public-docs)
TIP_USD = 0.30        # ~0.0015-0.002 SOL tip+priority per tx
MAX_DELAY = 900       # entry candle must start within 15 min of snapshot
HORIZON = 24 * 3600   # max holding time

t = pd.read_parquet(f"{D}/tokens.parquet")
o = pd.read_parquet(f"{D}/ohlcv.parquet").sort_values(["token_address", "ts"])
o["high"] = np.where(o.high > o.close * 10, np.maximum(o.open, o.close), o.high)
t["cap_ts"] = t.captured_at.astype("int64") // 10**9
# one decision per token: first detection
t = t.sort_values("cap_ts").drop_duplicates("token_address", keep="first")

paths = {k: g[["ts", "open", "high", "low", "close"]].to_numpy() for k, g in o.groupby("token_address")}

rows = []
for r in t.itertuples():
    p = paths.get(r.token_address)
    if p is None:
        continue
    idx = np.searchsorted(p[:, 0], r.cap_ts)
    if idx >= len(p) or p[idx, 0] - r.cap_ts > MAX_DELAY:
        continue
    seg = p[idx:]
    seg = seg[seg[:, 0] < seg[0, 0] + HORIZON]
    if seg[0, 1] <= 0:
        continue
    rows.append((r.token_address, seg))
print("tradeable tokens (entry candle within 15 min):", len(rows))

STRATS = {
    "hold_24h":   dict(sl=None, tps=[], trail=None, tmax=24),
    "ladder_B":   dict(sl=0.50, tps=[(2.0, 0.5), (5.0, 0.25)], trail=0.50, tmax=24),
    "ladder_C":   dict(sl=0.40, tps=[(1.5, 0.33), (3.0, 0.33), (10.0, 0.34)], trail=None, tmax=24),
    "tight_D":    dict(sl=0.30, tps=[(1.5, 0.5), (3.0, 0.5)], trail=None, tmax=6),
    "scalp_E":    dict(sl=0.20, tps=[(1.3, 1.0)], trail=None, tmax=2),
    "runner_F":   dict(sl=0.50, tps=[(3.0, 0.5)], trail=0.40, tmax=24),
}


def simulate(seg, sl, tps, trail, tmax):
    """Return gross multiple of position value (before costs) and #sell txs."""
    entry = seg[0, 1]
    left, value, sells, peak = 1.0, 0.0, 0, entry
    tps = list(tps)
    t_end = seg[0, 0] + tmax * 3600
    for ts, op, hi, lo, cl in seg:
        if ts >= t_end:
            break
        # stop / trailing first (conservative)
        stop = None
        if sl is not None:
            stop = entry * (1 - sl)
        if trail is not None and peak > entry * 2:  # trail only after 2x
            stop = max(stop or 0, peak * (1 - trail))
        if stop is not None and lo <= stop:
            px = min(stop, op)  # gap-through: fill at open if it opened below stop
            value += left * px / entry; left = 0; sells += 1
            break
        for lvl, frac in list(tps):
            if hi >= entry * lvl and left > 0:
                f = min(frac, left)
                value += f * lvl; left -= f; sells += 1
                tps.remove((lvl, frac))
        peak = max(peak, hi)
        last_close = cl
        if left <= 1e-9:
            break
    if left > 1e-9:  # time exit at last close inside horizon
        last = seg[seg[:, 0] < t_end]
        value += left * last[-1, 4] / entry; sells += 1
    return value, sells


liq = t.set_index("token_address").liquidity_usd
res = []
for tok, seg in rows:
    rec = {"token_address": tok}
    for name, s in STRATS.items():
        v, n = simulate(seg, **s)
        rec[name] = v; rec[name + "_n"] = n
    hi = seg[:, 2].max() / seg[0, 1]
    rec["peak_mult"] = hi
    rec["final_mult"] = seg[-1, 4] / seg[0, 1]
    res.append(rec)
R = pd.DataFrame(res).merge(t, on="token_address", how="left")
R.to_parquet(f"{OUT}/sim_results.parquet")


def net(R, name, pos):
    L = R.liquidity_usd.clip(lower=1)
    impact = (2 * pos / L).clip(upper=0.9)
    gross = R[name]
    # buy cost: fee+impact on entry; sell cost proportional to proceeds
    eff = gross * (1 - FEE - impact) * (1 - FEE - impact)
    tips = TIP_USD * (1 + R[name + "_n"]) / pos
    return eff - tips - 1  # net return per $1 staked


summary = {}
for pos in (50, 200, 1000):
    for name in STRATS:
        x = net(R, name, pos)
        summary[f"{name}@{pos}"] = dict(n=int(len(x)), mean=float(x.mean()), median=float(x.median()),
                                        win=float((x > 0).mean()), p95=float(x.quantile(.95)),
                                        mean_ex_top1pct=float(x[x < x.quantile(.99)].mean()))
json.dump(summary, open(f"{OUT}/summary_all.json", "w"), indent=1)
print(pd.DataFrame(summary).T.round(3).to_string())
print("peak multiple dist:", R.peak_mult.describe(percentiles=[.25, .5, .75, .9, .99]).round(2).to_dict())
print("share reaching 2x:", (R.peak_mult >= 2).mean().round(3), " 5x:", (R.peak_mult >= 5).mean().round(3))
