"""Execution-gap engine: path simulator (extends backtest.py `simulate`) + cost model.
Run scripts with `python3 -I`. Data paths are passed as arguments / env by the callers."""
import numpy as np, pandas as pd, random

CAND = 900
STRATS = {
    "ladder_B": dict(sl=0.50, tps=[(2.0, 0.5), (5.0, 0.25)], trail=0.50, tmax=24),
    "ladder_C": dict(sl=0.40, tps=[(1.5, 0.33), (3.0, 0.33), (10.0, 0.34)], trail=None, tmax=24),
}
MAXK = 4


def load(D):
    t = pd.read_parquet(f"{D}/tokens.parquet")
    o = pd.read_parquet(f"{D}/ohlcv.parquet").sort_values(["token_address", "ts"])
    o["high"] = np.where(o.high > o.close * 10, np.maximum(o.open, o.close), o.high)  # same glitch clip as backtest.py
    t["cap_ts"] = t.captured_at.astype("int64") // 10**9
    t = t.sort_values("cap_ts").drop_duplicates("token_address", keep="first")
    paths = {k: g[["ts", "open", "high", "low", "close"]].to_numpy() for k, g in o.groupby("token_address")}
    return t, paths


def build(t, paths):
    """per token: segs[k] for k=0..MAXK (entry = first candle starting >= cap_ts + k*900, within 900s of that target)."""
    toks, meta, segs = [], [], []
    for r in t.itertuples():
        p = paths.get(r.token_address)
        if p is None:
            continue
        ss = []
        for k in range(MAXK + 1):
            tgt = r.cap_ts + k * CAND
            idx = np.searchsorted(p[:, 0], tgt)
            if idx >= len(p) or p[idx, 0] - tgt > CAND or p[idx, 1] <= 0:
                ss.append(None)
                continue
            seg = p[idx:]
            seg = seg[seg[:, 0] < seg[0, 0] + 24 * 3600]
            ss.append([tuple(x) for x in seg.tolist()])
        if ss[0] is None:
            continue
        toks.append(r.token_address)
        meta.append((r.liquidity_usd, r.market_cap_usd, r.time_since_launch_sec))
        segs.append(ss)
    m = pd.DataFrame(meta, columns=["liq", "mcap", "age"], index=toks)
    return m, segs


W = 6  # max tranches


def sim(seg, sl, tps, trail, tmax, stop_mode="gap", sl_slip=0.0, tp_slip=0.0, pf=0.0, rng=None,
        order="sl", dead=1.0, move_stop=False, wide=0.8, hope=False, panic_loss=None, panic_win=None):
    """Returns (fracs, mults, n_tx, n_fail, trunc_flag_value). mults are relative to the chart entry (open of entry candle).
    stop_mode: exact (fill at stop), gap (min(stop,open)) , close (stop evaluated on closes, fill at close),
    next_open (trigger on low, sell at next candle open)."""
    entry = seg[0][1]
    pend = [list(x) for x in tps]
    fr, mu = [], []
    left = 1.0
    peak = entry
    t_end = seg[0][0] + tmax * 3600
    n_tx = 0; n_fail = 0
    sl_cur = sl
    hope_level = None
    n = len(seg)
    done = False
    last_i = -1
    for j in range(n):
        ts, op, hi, lo, cl = seg[j]
        if ts >= t_end:
            break
        last_i = j
        if hope_level is not None and hi >= hope_level:
            fr.append(left); mu.append(hope_level); n_tx += 1; left = 0; done = True; break

        def do_tps():
            nonlocal left, n_tx, n_fail
            for it in list(pend):
                lvl, frac = it
                if left > 1e-9 and hi >= entry * lvl:
                    n_tx += 1
                    if pf and rng.random() < pf:
                        n_fail += 1
                        continue
                    f = min(frac, left)
                    fr.append(f); mu.append(lvl * (1 - tp_slip)); left -= f
                    pend.remove(it)

        if order == "tp":
            do_tps()
            if left <= 1e-9:
                done = True; break
        stop = None
        if sl_cur is not None:
            stop = entry * (1 - sl_cur)
        is_static = True
        if trail is not None and peak > entry * 2:
            tr = peak * (1 - trail)
            if stop is None or tr > stop:
                stop = tr; is_static = False
        if stop is not None:
            trig = (cl <= stop) if stop_mode == "close" else (lo <= stop)
            if trig and is_static and move_stop and sl_cur is not None and sl_cur < wide:
                sl_cur = wide                      # trader widens the stop instead of selling
                stop = entry * (1 - sl_cur)
                trig = (cl <= stop) if stop_mode == "close" else (lo <= stop)
            if trig and is_static and hope and hope_level is None:
                hope_level = entry; sl_cur = None  # ignore the stop, sell on recovery to break-even
                trig = False
            if trig:
                n_tx += 1
                if pf and rng.random() < pf:
                    n_fail += 1
                else:
                    if stop_mode == "exact": px = stop
                    elif stop_mode == "gap": px = min(stop, op)
                    elif stop_mode == "close": px = cl
                    else: px = seg[j + 1][1] if j + 1 < n else cl
                    px *= (1 - sl_slip)
                    fr.append(left); mu.append(px / entry); left = 0; done = True; break
        if order != "tp":
            do_tps()
        peak = max(peak, hi)
        if left <= 1e-9:
            done = True; break
        if panic_win is not None and left < 1 - 1e-9 and cl <= peak * (1 - panic_win):
            n_tx += 1; fr.append(left); mu.append(cl / entry); left = 0; done = True; break
        if panic_loss is not None and left > 1 - 1e-9 and cl <= entry * (1 - panic_loss):
            n_tx += 1; fr.append(left); mu.append(cl / entry); left = 0; done = True; break
    if not done and left > 1e-9:
        # forced time exit at last close within horizon (path may be truncated: apply dead-mark)
        lc = seg[last_i][4] if last_i >= 0 else seg[0][4]
        lts = seg[last_i][0] if last_i >= 0 else seg[0][0]
        trunc = (lts + CAND < t_end)
        fr.append(left); mu.append(lc / entry * (dead if trunc else 1.0)); n_tx += 1
    return fr, mu, n_tx, n_fail


def run_all(segs, k_of, cfg, strat, seed=0):
    """Simulate every token. k_of: array of entry delay k per token. returns arrays F,M (N,W), ntx, nfail, entry-candle OHLC."""
    N = len(segs)
    F = np.zeros((N, W)); M = np.zeros((N, W)); ntx = np.zeros(N); nf = np.zeros(N)
    rng = random.Random(seed)
    for i in range(N):
        seg = segs[i][int(k_of[i])]
        fr, mu, a, b = sim(seg, **strat, rng=rng, **cfg)
        L = min(len(fr), W)
        F[i, :L] = fr[:L]; M[i, :L] = mu[:L]
        ntx[i] = a; nf[i] = b
    return F, M, ntx, nf


def entry_candle(segs, k_of):
    return np.array([segs[i][int(k_of[i])][0][1:5] for i in range(len(segs))])  # o,h,l,c


def net(F, M, ntx, nfail_tx_factor, Lq, pos, fee, tip, chase_factor, retry_tx_factor=1.0):
    """Net return per $1 staked. Round-trip with CPMM per-side impact x=2V/L, fee per side, tip per tx.
    chase_factor = open/E (cost basis worse than the chart entry => <1)."""
    d = pos * (1 - fee)
    tok = d / (1 + 2 * d / Lq) * chase_factor
    V = tok[:, None] * F * M
    proceeds = (V / (1 + 2 * V / Lq[:, None]) * (1 - fee)).sum(1)
    tips = tip * (1 + ntx) * retry_tx_factor
    return (proceeds - tips) / pos - 1


def ci(x, B=400, seed=1):
    rng = np.random.default_rng(seed)
    n = len(x)
    m = [x[rng.integers(0, n, n)].mean() for _ in range(B)]
    return float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))
