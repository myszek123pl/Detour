"""Step 1: clean 15m candles, regular grid, detect pump (+50% <=1h) and dump (-30% <=1h) events.
usage: python3 -I pd_events.py <data_dir> <work_dir>"""
import sys, numpy as np, pandas as pd, duckdb
D, W = sys.argv[1], sys.argv[2]
PUMP, DUMP, MINVOL = 1.5, 0.7, 2000.0
con = duckdb.connect()
oh = con.sql(f"""select distinct on (token_address, ts) token_address tok, ts, open o, high h, low l, close c, volume v
                 from '{D}/ohlcv.parquet' order by token_address, ts, volume desc""").df()
oh = oh[(oh.o > 0) & (oh.c > 0)]
# glitch clip: wicks > 10x body are replaced by body edge
top, bot = np.maximum(oh.o, oh.c), np.minimum(oh.o, oh.c)
oh["h"] = np.where(oh.h > 10 * top, top, oh.h); oh["l"] = np.where(oh.l < bot / 10, bot, oh.l)
oh["h"] = np.maximum(oh.h, top); oh["l"] = np.minimum(oh.l, bot)
print("candles", len(oh), "tokens", oh.tok.nunique())
G = []   # grid frames
ev = []
for tok, g in oh.groupby("tok", sort=False):
    ts = g.ts.values; n0 = (ts[-1] - ts[0]) // 900 + 1
    if n0 > 400 or len(g) < 3: continue
    idx = ((ts - ts[0]) // 900).astype(int)
    c = np.full(n0, np.nan); o = c.copy(); h = c.copy(); l = c.copy(); v = np.zeros(n0); real = np.zeros(n0, bool)
    c[idx] = g.c.values; o[idx] = g.o.values; h[idx] = g.h.values; l[idx] = g.l.values; v[idx] = g.v.values; real[idx] = True
    # ffill close; filled candles flat at previous close
    cc = pd.Series(c).ffill().values
    o = np.where(real, o, cc); h = np.where(real, h, cc); l = np.where(real, l, cc); c = cc
    t = ts[0] + 900 * np.arange(n0)
    G.append(pd.DataFrame(dict(tok=tok, ts=t, o=o, h=h, l=l, c=c, v=v, real=real, k=np.arange(n0))))
    n = n0
    # ---- pump scan
    i = 0
    while i < n:
        lo = max(0, i - 3)
        j = lo + int(np.argmin(o[lo:i + 1]))
        if c[i] / o[j] >= PUMP and v[j:i + 1].sum() >= MINVOL and real[j:i + 1].any():
            pk = i + int(np.argmax(c[i:min(n, i + 4)]))
            ev.append(dict(tok=tok, kind="pump", j=j, i=i, p=pk, n=n, t_start=int(t[j]), t_trig=int(t[i] + 900), t_peak=int(t[pk] + 900),
                           p0=o[j], p_trig=c[i], p_peak=c[pk]))
            i = pk + 1
        else: i += 1
    i = 0
    while i < n:
        lo = max(0, i - 3)
        j = lo + int(np.argmax(o[lo:i + 1]))
        if c[i] / o[j] <= DUMP and v[j:i + 1].sum() >= MINVOL and real[j:i + 1].any():
            pk = i + int(np.argmin(c[i:min(n, i + 4)]))
            ev.append(dict(tok=tok, kind="dump", j=j, i=i, p=pk, n=n, t_start=int(t[j]), t_trig=int(t[i] + 900), t_peak=int(t[pk] + 900),
                           p0=o[j], p_trig=c[i], p_peak=c[pk]))
            i = pk + 1
        else: i += 1
G = pd.concat(G, ignore_index=True); E = pd.DataFrame(ev)
G.to_parquet(f"{W}/grid.parquet"); E.to_parquet(f"{W}/events.parquet")
print("grid", len(G), "events", E.kind.value_counts().to_dict())
# sensitivity of counts
