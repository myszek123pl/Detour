"""Helpers for regimes.py: series building, persistence tests, binomial HMM, OOS regime filters.
Pure numpy/pandas/scipy (no hmmlearn / statsmodels available)."""
import numpy as np, pandas as pd
from scipy import stats

FEE = (1 - .0125) ** 2          # round-trip pump.fun fee, as in launches_calls_deep.py
TIP_USD = 0.30


# ---------- data ----------
def net_returns(R, name, pos=200.0):
    """Same cost model as backtest.net(): fee+impact both sides, fixed tips."""
    L = R.liquidity_usd.clip(lower=1)
    impact = (2 * pos / L).clip(upper=0.9)
    eff = R[name] * (1 - .0125 - impact) ** 2
    return eff - TIP_USD * (1 + R[name + "_n"]) / pos - 1


def winsor(x, q=.99):
    return np.minimum(x, np.quantile(x, q))


# ---------- aggregate series ----------
def make_series(df, tcol, freq_sec, y2, y5, peak, extra=None):
    """df -> series indexed by period index (int), with n,k2,k5,p2,p5,med_peak (+ mean of extra cols)."""
    d = pd.DataFrame({"b": (df[tcol].to_numpy() // freq_sec).astype(int), "k2": y2, "k5": y5, "peak": peak})
    if extra is not None:
        for c, v in extra.items():
            d[c] = v
    g = d.groupby("b")
    s = g.agg(n=("k2", "size"), k2=("k2", "sum"), k5=("k5", "sum"), med_peak=("peak", "median"))
    if extra is not None:
        for c in extra:
            s[c] = g[c].mean()
    s["p2"] = s.k2 / s.n; s["p5"] = s.k5 / s.n
    full = pd.RangeIndex(s.index.min(), s.index.max() + 1)
    return s.reindex(full)       # NaN rows = periods with no data


# ---------- persistence tests ----------
def acf(x, lags=(1, 2, 3)):
    x = np.asarray(x, float); x = x[~np.isnan(x)]; x = x - x.mean(); d = (x * x).sum()
    return [float((x[l:] * x[:-l]).sum() / d) if len(x) > l else np.nan for l in lags]


def lag1(x):
    return acf(x, (1,))[0]


def perm_p(x, B=10000, seed=0, stat=lag1):
    rng = np.random.default_rng(seed); x = np.asarray(x, float); x = x[~np.isnan(x)]
    obs = stat(x); null = np.array([stat(rng.permutation(x)) for _ in range(B)])
    return obs, float((np.abs(null) >= abs(obs)).mean())      # two-sided


def lin_detrend(x):
    x = np.asarray(x, float); t = np.arange(len(x)); m = ~np.isnan(x)
    b = np.polyfit(t[m], x[m], 1); r = x - np.polyval(b, t); return r


def pearson_resid(k, n):
    k = np.asarray(k, float); n = np.asarray(n, float); p = np.nansum(k) / np.nansum(n)
    return (k - n * p) / np.sqrt(n * p * (1 - p)), p


def dispersion(k, n):
    """Pearson chi2 dispersion test of binomial homogeneity across periods (H0: constant p)."""
    m = ~(np.isnan(k) | np.isnan(n)) & (np.asarray(n) > 0)
    z, p = pearson_resid(np.asarray(k)[m], np.asarray(n)[m])
    chi = float((z ** 2).sum()); df = int(m.sum() - 1)
    return dict(p_pool=float(p), chi2=chi, df=df, ratio=chi / df, pval=float(stats.chi2.sf(chi, df)))


def cond_table(x, thr=None):
    """P(next good | good) vs P(next good | bad); good = above median."""
    x = np.asarray(x, float); thr = np.nanmedian(x) if thr is None else thr
    g = (x > thr).astype(int); a, b = g[:-1], g[1:]
    ok = ~(np.isnan(x[:-1]) | np.isnan(x[1:])); a, b = a[ok], b[ok]
    t = np.array([[((a == 0) & (b == 0)).sum(), ((a == 0) & (b == 1)).sum()],
                  [((a == 1) & (b == 0)).sum(), ((a == 1) & (b == 1)).sum()]])
    pg = t[1, 1] / max(t[1].sum(), 1); pb = t[0, 1] / max(t[0].sum(), 1)
    return dict(p_good_after_good=float(pg), p_good_after_bad=float(pb), n_after_good=int(t[1].sum()),
                n_after_bad=int(t[0].sum()), fisher_p=float(stats.fisher_exact(t)[1]))


# ---------- binomial HMM ----------
def _binom_logpmf(k, n, p):
    return stats.binom.logpmf(k[:, None], n[:, None], p[None, :])


def hmm_fit(k, n, K=2, inits=6, iters=200, seed=0, iid=False):
    """EM for K-state HMM with Binomial(n_t, p_s) emissions. iid=True -> A rows tied to pi (mixture, no persistence)."""
    k = np.asarray(k, float); n = np.asarray(n, float); T = len(k); rng = np.random.default_rng(seed)
    base = k.sum() / n.sum(); best = None
    for it in range(inits):
        spread = rng.uniform(.3, 1.2)
        p = np.clip(base * np.exp(np.linspace(-spread, spread, K) + rng.normal(0, .1, K)), 1e-4, 1 - 1e-4)
        A = np.full((K, K), .1 / max(K - 1, 1)) + np.eye(K) * (.9 - .1 / max(K - 1, 1)); pi = np.full(K, 1 / K)
        ll_old = -np.inf
        for _ in range(iters):
            lb = _binom_logpmf(k, n, p); mx = lb.max(1, keepdims=True); B = np.exp(lb - mx)
            al = np.zeros((T, K)); c = np.zeros(T)
            a = pi * B[0]; c[0] = a.sum(); al[0] = a / c[0]
            for t in range(1, T):
                a = (al[t - 1] @ A) * B[t]; c[t] = a.sum(); al[t] = a / c[t]
            be = np.ones((T, K))
            for t in range(T - 2, -1, -1):
                be[t] = (A @ (B[t + 1] * be[t + 1])) / c[t + 1]
            gam = al * be; gam /= gam.sum(1, keepdims=True)
            xi = np.zeros((K, K))
            for t in range(T - 1):
                m = al[t][:, None] * A * (B[t + 1] * be[t + 1])[None, :]; xi += m / m.sum()
            ll = float((np.log(c) + mx[:, 0]).sum())
            pi = gam[0]; p = np.clip(((gam * k[:, None]).sum(0) + 1e-6) / ((gam * n[:, None]).sum(0) + 2e-6), 1e-4, 1 - 1e-4)
            if iid:
                w = gam.sum(0) / T; A = np.tile(w, (K, 1)); pi = w
            else:
                xi = xi + 0.25; A = xi / xi.sum(1, keepdims=True)   # weak Dirichlet prior: no absorbing states
            if abs(ll - ll_old) < 1e-7: break
            ll_old = ll
        if best is None or ll > best["ll"]:
            o = np.argsort(p); best = dict(ll=ll, p=p[o], A=A[np.ix_(o, o)], pi=pi[o], gamma=gam[:, o])
    return best


def hmm_filter(k, n, par):
    """Filtered state probs P(S_t | data<=t) using fitted params."""
    k = np.asarray(k, float); n = np.asarray(n, float); p, A, pi = par["p"], par["A"], par["pi"]
    lb = _binom_logpmf(k, n, p); B = np.exp(lb - lb.max(1, keepdims=True)); T = len(k); K = len(p)
    al = np.zeros((T, K)); a = pi * B[0]; al[0] = a / a.sum()
    for t in range(1, T):
        a = (al[t - 1] @ A) * B[t]; al[t] = a / a.sum()
    return al


def hmm_bootstrap(k, n, B=60, seed=1, inits=4):
    """Parametric bootstrap LRT: (a) 2-state HMM vs 1-state binomial; (b) HMM vs iid 2-comp mixture (persistence only)."""
    k = np.asarray(k, float); n = np.asarray(n, float)
    f2 = hmm_fit(k, n, 2, inits=8, seed=seed); fm = hmm_fit(k, n, 2, inits=8, seed=seed, iid=True)
    p0 = k.sum() / n.sum(); ll1 = float(stats.binom.logpmf(k, n, p0).sum())
    obs_a = 2 * (f2["ll"] - ll1); obs_b = 2 * (f2["ll"] - fm["ll"]); rng = np.random.default_rng(seed)
    na, nb = [], []
    for _ in range(B):
        ks = rng.binomial(n.astype(int), p0); q = ks.sum() / n.sum()
        na.append(2 * (hmm_fit(ks, n, 2, inits=inits, iters=120, seed=rng.integers(1e9))["ll"] - stats.binom.logpmf(ks, n, q).sum()))
        # simulate from iid mixture
        z = rng.choice(2, size=len(n), p=fm["pi"]); ks2 = rng.binomial(n.astype(int), fm["p"][z])
        h2 = hmm_fit(ks2, n, 2, inits=inits, iters=120, seed=rng.integers(1e9)); hm = hmm_fit(ks2, n, 2, inits=inits, iters=120, seed=rng.integers(1e9), iid=True)
        nb.append(2 * (h2["ll"] - hm["ll"]))
    return dict(hmm=f2, mix=fm, ll1=ll1, lrt_vs_1state=float(obs_a), p_vs_1state=float((np.array(na) >= obs_a).mean()),
                lrt_vs_iid=float(obs_b), p_vs_iid=float((np.array(nb) >= obs_b).mean()))


# ---------- OOS regime filter evaluation ----------
def eval_rule(S, N, sel, test_mask, B=10000, seed=0):
    """S: per-day sum of trade payoffs; N: per-day trade count; sel: bool per day (rule says trade);
    test_mask: days in OOS window. Returns per-trade mean of selected, baseline per-trade mean, CI, null p-value."""
    S = np.asarray(S, float); N = np.asarray(N, float); sel = np.asarray(sel, bool) & test_mask
    idx = np.where(test_mask)[0]; k = int(sel.sum()); rng = np.random.default_rng(seed)
    base = S[idx].sum() / N[idx].sum()
    if k == 0: return dict(k=0)
    m = S[sel].sum() / N[sel].sum()
    boot = []
    s_idx = np.where(sel)[0]
    for _ in range(2000):
        r = rng.choice(s_idx, len(s_idx)); boot.append(S[r].sum() / N[r].sum())
    null = []
    for _ in range(B):
        r = rng.choice(idx, k, replace=False); null.append(S[r].sum() / N[r].sum())
    null = np.array(null)
    return dict(days_traded=k, days_test=len(idx), frac=k / len(idx), trades=int(N[sel].sum()), mean=float(m), base=float(base),
                lift=float(m - base), ci=(float(np.quantile(boot, .025)), float(np.quantile(boot, .975))),
                p_vs_random=float((null >= m).mean()), pnl_per_day=float(S[sel].sum() / len(idx)), base_pnl_per_day=float(S[idx].sum() / len(idx)))
