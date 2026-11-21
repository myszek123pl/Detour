"""Step 2: leak-free trade features. python3 -I tf_features.py <data> <work>
Every feature for token i uses only trades with ts < cap_i, funding rows with ts < cap_i,
and crew history from tokens j with cap_j < cap_i (using j's buys with ts < cap_j)."""
import sys, numpy as np, pandas as pd
D, W = sys.argv[1:3]
p = pd.read_parquet(f"{W}/pre.parquet")
wf = pd.read_parquet(f"{D}/wallet_funding.parquet")
wf["ts"] = wf.ts.astype("int64") // 10**9 if wf.ts.dtype.kind == "M" else wf.ts
wf["ts"] = pd.to_datetime(pd.read_parquet(f"{D}/wallet_funding.parquet").ts).astype("int64") // 10**9 if False else wf.ts
print("funding rows", len(wf), "ts range", wf.ts.min(), wf.ts.max())
p["dt"] = p.cap - p.ts
buy = p[p.side == "buy"]; sell = p[p.side == "sell"]
g = lambda d: d.groupby("token_address")
F = pd.DataFrame(index=pd.Index(p.token_address.unique(), name="token_address"))
F["f_buy_usd"] = g(buy).amount_usd.sum(); F["f_sell_usd"] = g(sell).amount_usd.sum()
F["f_n_buys"] = g(buy).size(); F["f_n_sells"] = g(sell).size()
F["f_ub"] = g(buy).wallet.nunique(); F["f_us"] = g(sell).wallet.nunique()
F = F.fillna(0)
F["f_net_usd"] = F.f_buy_usd - F.f_sell_usd
F["f_buy_share"] = F.f_buy_usd / (F.f_buy_usd + F.f_sell_usd).clip(lower=1e-9)
F["f_sellers_per_buyer"] = F.f_us / F.f_ub.clip(lower=1)
F["f_age_s"] = g(p).dt.max()          # seconds from first pre-capture trade to capture
F["f_last_trade_gap_s"] = g(p).dt.min()
# top-5 buyer share
bw = buy.groupby(["token_address", "wallet"]).amount_usd.sum().reset_index().sort_values(["token_address", "amount_usd"], ascending=[True, False])
bw["r"] = bw.groupby("token_address").cumcount()
tot = bw.groupby("token_address").amount_usd.sum()
F["f_top5_buyer_share"] = bw[bw.r < 5].groupby("token_address").amount_usd.sum() / tot
F["f_top1_buyer_share"] = bw[bw.r < 1].groupby("token_address").amount_usd.sum() / tot
# size uniformity on buys
b = buy.assign(la=np.log1p(buy.amount_usd), rd=buy.amount_usd.round(0))
a = g(b).la.agg(["mean", "std"]); F["f_buy_logsize_cv"] = a["std"] / a["mean"].clip(lower=1e-9)
mc = b.groupby(["token_address", "rd"]).size().groupby("token_address").max()
F["f_buy_modal_size_share"] = mc / F.f_n_buys
F["f_buy_size_med"] = g(buy).amount_usd.median()
F["f_buy_size_mean"] = g(buy).amount_usd.mean()
# acceleration: buy usd in last 60s / 300s vs rate before
for w in (60, 300):
    rec = buy[buy.dt <= w].groupby("token_address").amount_usd.sum().reindex(F.index).fillna(0)
    F[f"f_buy_usd_last{w}"] = rec
    F[f"f_accel{w}"] = rec / w / ((F.f_buy_usd - rec).clip(lower=0) / (F.f_age_s - w).clip(lower=w) + 1e-6 ) if False else np.log1p(rec) - np.log1p((F.f_buy_usd - rec).clip(lower=0) * w / (F.f_age_s - w).clip(lower=w))
F["f_nbuys_last60"] = buy[buy.dt <= 60].groupby("token_address").size().reindex(F.index).fillna(0)
F["f_buy_rate_per_min"] = F.f_n_buys / (F.f_age_s.clip(lower=30) / 60)
# funders (only funding strictly before this token's capture)
cap = p.groupby("token_address").cap.first()
bwal = buy[["token_address", "wallet", "cap"]].drop_duplicates()
m = bwal.merge(wf[["wallet", "funder", "ts"]], on="wallet", how="left")
m = m[m.ts < m.cap]                    # strictly before capture
m = m.sort_values("ts").drop_duplicates(["token_address", "wallet"], keep="first")  # first known funder
fc = m.groupby(["token_address", "funder"]).size().rename("k").reset_index()
F["f_funded_buyers_frac"] = m.groupby("token_address").size() / F.f_ub
shared = fc[fc.k >= 2].groupby("token_address").k.sum()
F["f_same_funder_frac"] = (shared.reindex(F.index).fillna(0)) / F.f_ub          # share of ALL buyers sharing a funder with >=1 other buyer
F["f_top_funder_frac"] = fc.groupby("token_address").k.max().reindex(F.index).fillna(0) / F.f_ub
# crew history: for tokens ordered by cap, wallet -> number of earlier tokens bought
bt = bwal.sort_values("cap")
order = bt.groupby("token_address").cap.first().sort_values()
byt = {k: v.wallet.values for k, v in bt.groupby("token_address")}
seen = {}; ctab = {}
toks = list(order.index); caps = order.values
i = 0
while i < len(toks):
    j = i
    while j < len(toks) and caps[j] == caps[i]: j += 1     # tie group: compute all before updating (strict cap_j < cap_i)
    for k in range(i, j):
        w = byt[toks[k]]; c = np.array([seen.get(x, 0) for x in w])
        ctab[toks[k]] = (len(w), (c >= 1).mean(), (c >= 3).mean(), c.mean(), c.max(), (c >= 1).sum())
    for k in range(i, j):
        for x in byt[toks[k]]: seen[x] = seen.get(x, 0) + 1
    i = j
C = pd.DataFrame.from_dict(ctab, orient="index", columns=["n", "f_crew_rep1_frac", "f_crew_rep3_frac", "f_crew_mean_prev", "f_crew_max_prev", "f_crew_rep1_n"])
F = F.join(C.drop(columns="n"))
F.to_parquet(f"{W}/features.parquet")
print(F.describe().T[["count", "mean", "50%", "max"]].to_string())
