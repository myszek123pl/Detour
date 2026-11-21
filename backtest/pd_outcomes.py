"""Step 3: per-event candle-level features and forward outcomes. usage: python3 -I pd_outcomes.py <data_dir> <work_dir>"""
import sys, numpy as np, pandas as pd, duckdb
D, W = sys.argv[1], sys.argv[2]
G = pd.read_parquet(f"{W}/grid.parquet"); E = pd.read_parquet(f"{W}/events.parquet").reset_index(drop=True); E["eid"] = E.index
arr = {t: g for t, g in G.groupby("tok", sort=False)}
rows = []
KS = [1, 2, 3, 4, 6, 8, 12, 16]
for r in E.itertuples():
    g = arr[r.tok]; o, h, l, c, v, real = (g[x].values for x in ("o", "h", "l", "c", "v", "real"))
    n, i, j, p = r.n, r.i, r.j, r.p
    d = dict(eid=r.eid, fw=n - 1 - i, nsteps=i - j + 1)
    e = c[i]
    for k in KS: d[f"r{k}"] = c[i + k] / e - 1 if i + k < n else np.nan
    for H in (4, 8, 16):
        seg = c[i + 1:i + 1 + H]
        d[f"fmax{H}"] = seg.max() / e - 1 if len(seg) == H else np.nan
        d[f"fmin{H}"] = seg.min() / e - 1 if len(seg) == H else np.nan
        sh = h[i + 1:i + 1 + H]; sl = l[i + 1:i + 1 + H]
        d[f"hmax{H}"] = sh.max() / e - 1 if len(sh) == H else np.nan
        d[f"lmin{H}"] = sl.min() / e - 1 if len(sl) == H else np.nan
    # candle-level volumes
    d["v_pre"] = v[max(0, j - 4):j].sum(); d["n_pre"] = j - max(0, j - 4)
    d["v_pump"] = v[j:i + 1].sum(); d["v_post1"] = v[i + 1:i + 5].sum() if i + 4 < n else np.nan
    d["v_post2"] = v[i + 5:i + 9].sum() if i + 8 < n else np.nan
    d["v_last"] = v[i]; d["v_prev"] = v[i - 1] if i > 0 else np.nan
    d["v_base"] = v[max(0, j - 8):j].mean() if j > 0 else np.nan
    # trigger candle shape
    rng = h[i] - l[i]
    d["uwick"] = (h[i] - max(o[i], c[i])) / rng if rng > 0 else 0.0
    d["cpos"] = (c[i] - l[i]) / rng if rng > 0 else 0.5
    d["last_ret"] = c[i] / o[i] - 1
    d["prev_ret"] = c[i - 1] / o[i - 1] - 1 if i > 0 else np.nan
    d["hi_over_close"] = h[i] / c[i] - 1
    d["real_frac_pump"] = real[j:i + 1].mean()
    d["pre_run"] = o[j] / c[j - 4] - 1 if j >= 4 else (o[j] / o[0] - 1 if j > 0 else np.nan)   # drift before the event start
    d["from_first"] = c[i] / o[0]                       # multiple vs first observed candle open
    d["k_start"] = j                                    # candles of history before start
    rows.append(d)
O = pd.DataFrame(rows)
E = E.merge(O, on="eid")
# token covariates (asof at trigger)
con = duckdb.connect()
tk = con.sql(f"select * from '{D}/tokens.parquet'").df()
tk["cap"] = tk.captured_at.astype("int64") // 10**9 if str(tk.captured_at.dtype).startswith("datetime64[ns") else tk.captured_at.astype("datetime64[s]").astype("int64")
tk["launch"] = tk.cap - tk.time_since_launch_sec
tk = tk.sort_values("cap")
E = E.sort_values("t_trig")
M = pd.merge_asof(E, tk.add_prefix("s_").rename(columns={"s_cap": "cap_ts", "s_token_address": "tok"}), left_on="t_trig", right_on="cap_ts", by="tok", direction="backward")
# fallback launch from earliest snapshot for events preceding snapshots
first = tk.groupby("token_address").agg(launch0=("launch", "min"), cap_first=("cap", "min"), cap_last=("cap", "max")).reset_index().rename(columns={"token_address": "tok"})
M = M.merge(first, on="tok", how="left")
M["age_min"] = (M.t_trig - M.launch0) / 60
M["has_snap"] = M.cap_ts.notna()
M["ts_day"] = pd.to_datetime(M.t_trig, unit="s").dt.strftime("%Y-%m-%d")
M.to_parquet(f"{W}/ev_out.parquet")
print(M.shape, M.has_snap.mean()); print(M.groupby("kind").age_min.describe())
print("price scale check", (M.s_price_at_capture / M.p_trig).describe())
