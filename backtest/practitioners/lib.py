"""Shared helpers for practitioner-filter tests (note 42).
- simulate() is extracted verbatim (via ast) from backtest.py so the exit logic is the one used everywhere else.
- Data-quality rules from note 01: no mcap/price-derived ratios as features, drop lm>1 rows.
Run with python3 -I (scripts add this folder to sys.path explicitly).
"""
import ast, numpy as np, pandas as pd

BT = "/home/user/Detour/backtest/backtest.py"
DATA = "/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/datasets/solana-memecoin-dataset/repo/data"
OUT = "/home/user/Detour/backtest/out/practitioners"
SIM = "/home/user/Detour/backtest/out/sim_results.parquet"
FEE, TIP = 0.0125, 0.30
SPLIT = pd.Timestamp("2026-06-24", tz="UTC")
HORIZON = 24 * 3600
MAX_DELAY = 900


def _load_simulate():
    src = open(BT).read()
    tree = ast.parse(src)
    fn = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "simulate"][0]
    ns = {"np": np, "pd": pd}
    exec(compile(ast.Module([fn], []), BT, "exec"), ns)
    return ns["simulate"]


simulate = _load_simulate()


def build_paths(tokens_needed=None):
    """Same path construction as backtest.py (first snapshot per token, entry candle <=15min later, 24h horizon)."""
    t = pd.read_parquet(f"{DATA}/tokens.parquet")
    o = pd.read_parquet(f"{DATA}/ohlcv.parquet").sort_values(["token_address", "ts"])
    o["high"] = np.where(o.high > o.close * 10, np.maximum(o.open, o.close), o.high)
    t["cap_ts"] = t.captured_at.astype("int64") // 10**9
    t = t.sort_values("cap_ts").drop_duplicates("token_address", keep="first")
    paths = {k: g[["ts", "open", "high", "low", "close"]].to_numpy() for k, g in o.groupby("token_address")}
    out = {}
    for r in t.itertuples():
        if tokens_needed is not None and r.token_address not in tokens_needed:
            continue
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
        out[r.token_address] = seg
    return out


def load_universe():
    """sim_results rows after the note-01 hygiene rules."""
    R = pd.read_parquet(SIM)
    R = R[R.peak_mult < 1000].copy()                    # glitch token(s), as filters.py/rules.py
    R["lm"] = R.liquidity_usd / R.market_cap_usd        # used ONLY for dropping, never as a signal
    n0 = len(R)
    R = R[R.lm <= 1].copy()
    R["L_cap"] = np.minimum(R.liquidity_usd, 0.4 * R.market_cap_usd).clip(lower=1)
    R["L_fix"] = 15000.0
    R["day"] = R.captured_at.dt.strftime("%Y-%m-%d")
    R["test"] = R.captured_at >= SPLIT
    return R, n0


def net_ret(gross, nsell, L, pos):
    imp = np.clip(2 * pos / np.asarray(L, float), 0, 0.9)
    return np.asarray(gross) * (1 - FEE - imp) ** 2 - TIP * (1 + np.asarray(nsell)) / pos - 1


def boot_ci(x, B=2000, rng=None, days=None):
    """95% bootstrap CI of the mean. days -> resample whole days (block bootstrap)."""
    rng = rng or np.random.default_rng(0)
    x = np.asarray(x, float)
    n = len(x)
    if n < 15:
        return (np.nan, np.nan)
    if days is None:
        m = x[rng.integers(0, n, (B, n))].mean(1)
    else:
        d = pd.factorize(np.asarray(days))[0]
        k = d.max() + 1
        s = np.bincount(d, weights=x, minlength=k); c = np.bincount(d, minlength=k).astype(float)
        pick = rng.integers(0, k, (B, k))
        m = s[pick].sum(1) / c[pick].sum(1)
    return tuple(np.percentile(m, [2.5, 97.5]))


def random_subset_stats(x_universe, m, B=2000, rng=None):
    """Distribution of mean over random subsets of size m drawn from the universe."""
    rng = rng or np.random.default_rng(1)
    x = np.asarray(x_universe, float)
    if m < 1 or m > len(x):
        return None
    idx = np.argsort(rng.random((B, len(x))), axis=1)[:, :m] if len(x) * B < 3e7 else \
        np.stack([rng.choice(len(x), m, replace=False) for _ in range(B)])
    return x[idx].mean(1)
