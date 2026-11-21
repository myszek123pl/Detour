"""Proxy for 'no single wallet >2-3%': the dataset has no per-wallet holding. From the trades log (pre-capture only)
compute, per token, the largest single wallet's share of gross buy USD and of net buy USD, #trades, #wallets.
Trade log is a sample (~last 200 trades) -> shares are only meaningful for young tokens with a complete-looking log.
Usage: python3 -I wallet_proxy.py"""
import sys, glob, numpy as np, pandas as pd
sys.path.insert(0, "/home/user/Detour/backtest/practitioners")
import lib
R, _ = lib.load_universe()
cap = R.set_index("token_address").captured_at
toks = set(cap.index)
parts = []
for f in sorted(glob.glob(f"{lib.DATA}/trades-*.parquet")):
    t = pd.read_parquet(f, columns=["wallet", "token_address", "side", "amount_usd", "ts"])
    t = t[t.token_address.isin(toks)]
    t = t.merge(cap.rename("cap"), left_on="token_address", right_index=True)
    t = t[t.ts <= t.cap]
    parts.append(t[["wallet", "token_address", "side", "amount_usd"]])
T = pd.concat(parts, ignore_index=True)
print(len(T), T.token_address.nunique())
T["buy"] = np.where(T.side == "buy", T.amount_usd, 0.0)
T["sell"] = np.where(T.side == "sell", T.amount_usd, 0.0)
W = T.groupby(["token_address", "wallet"], observed=True)[["buy", "sell"]].sum().reset_index()
W["net"] = W.buy - W.sell
g = W.groupby("token_address")
F = pd.DataFrame({
    "pre_trades": T.groupby("token_address").size(),
    "pre_wallets": g.size(),
    "gross_buy": g.buy.sum(),
    "max_wallet_buy": g.buy.max(),
    "pos_net": W.assign(p=W.net.clip(lower=0)).groupby("token_address").p.sum(),
    "max_wallet_net": W.assign(p=W.net.clip(lower=0)).groupby("token_address").p.max(),
})
F["top1_buy_share"] = F.max_wallet_buy / F.gross_buy
F["top1_net_share"] = F.max_wallet_net / F.pos_net
F.to_parquet(f"{lib.OUT}/wallet_proxy.parquet")
print(F.describe(percentiles=[.1,.25,.5,.75,.9]).round(3).T.to_string())
