"""Who sells into pumps / dumps. python3 -I pd_a4.py <data_dir> <work> <out_md>"""
import sys, numpy as np, pandas as pd, duckdb
sys.path.insert(0,"/home/user/Detour/backtest"); from pd_md import md
D, W, OUT = sys.argv[1:4]
pd.set_option("display.width",250); pd.set_option("display.max_columns",60)
out=[]
def emit(t,df):
    out.append(f"\n### {t}\n"); out.append(md(df)); print("\n###",t); print(df.to_string())
M=pd.read_parquet(f"{W}/ev_out.parquet"); M["eid"]=M.eid.astype(int)
Q=pd.read_parquet(f"{W}/pump_Q.parquet")[["eid","cls"]]
M=M.merge(Q,on="eid",how="left")
M["covd"]=(M.t_start>=M.launch0-60)&(M.t_trig+3600<=M.cap_last)&(M.t_start-M.launch0>=900)
WL=pd.read_parquet(f"{W}/wallet_event.parquet")
WL=WL.merge(M[["eid","tok","covd","cls","p_peak","p0","p_trig"]],on="eid")
WL=WL[WL.covd].copy()
con=duckdb.connect()
tags=con.sql(f"select address w, wallet_type wt from '{D}/wallets.parquet'").df().drop_duplicates("w")
fund=con.sql(f"select wallet w, funder from '{D}/wallet_funding.parquet'").df()
# sniper rank: rank of wallet by first buy time within token (whole sample)
rank=con.sql(f"""select token_address tok, wallet w, rank() over(partition by token_address order by min(epoch(ts))) rk
   from '{D}/trades-00*.parquet' where side='buy' group by token_address, wallet""").df()
WL=WL.merge(tags,on="w",how="left").merge(rank,on=["tok","w"],how="left")
WL["wt"]=WL.wt.fillna("untagged")
# funder cluster: wallets that share a funder with another wallet active in same event
fm=fund.groupby("w").funder.apply(set).to_dict()
fund_to=fund.groupby("funder").w.apply(set).to_dict()
big=fund.groupby("funder").w.nunique(); print("funders with >=2 wallets",(big>=2).sum(),"wallets covered",fund.w.nunique())
def role(r):
    if np.isnan(r.fb): return "no_buy_logged"
    if r.fb<r.S: return "early(pre-start)"
    if r.fb<r.Tg: return "pump-phase buyer"
    return "late(post-trigger)"
for c_ in ("fb","ft","f0","S","Tg","Pk"): WL[c_]=WL[c_].astype("float64")
WL["role"]=np.where(WL.fb.isna(),"no_buy_logged",np.where(WL.fb<WL.S,"early(pre-start)",np.where(WL.fb<WL.Tg,"pump-phase buyer","late(post-trigger)")))
WL["sell_win"]=WL.sell_pump+WL.sell_post1; WL["buy_win"]=WL.buy_pump+WL.buy_post.where(False,0)  # buys in pump phase only (post buys separate)
WL["buy_win"]=WL.buy_pump
res={}
def sellers(kind,sub,label):
    X=WL[(WL.kind==kind)&sub.reindex(WL.index,fill_value=True)] if False else WL[(WL.kind==kind)]
    return X
rows=[]
for kind in ("pump","dump"):
    X=WL[WL.kind==kind]
    for nm,Y in [("ALL",X)]+([("full_retrace",X[X.cls=="full_retrace"]),("continue",X[X.cls=="continue"]),("plateau",X[X.cls=="plateau"])] if kind=="pump" else []):
        tot_s=(Y.sell_pump+Y.sell_post1).sum(); tot_b=(Y.buy_pump+Y.buy_post).sum()
        g=Y.groupby("role").agg(sell=("sell_win","sum"),sell_pump=("sell_pump","sum"),sell_post1=("sell_post1","sum"),buy_pump=("buy_pump","sum"),wallets=("w","nunique"))
        g["share_of_sell_usd"]=g.sell/tot_s; g["share_of_pumpphase_buy_usd"]=g.buy_pump/Y.buy_pump.sum()
        g["events"]=Y.eid.nunique()
        g=g.reset_index(); g.insert(0,"group",f"{kind}:{nm}"); rows.append(g)
R=pd.concat(rows)
emit("Share of sell USD in [event start, trigger+1h] by wallet role (role = timing of the wallet's first logged buy of that token)",R[["group","role","share_of_sell_usd","share_of_pumpphase_buy_usd","wallets","events"]].set_index("group"))
# early buyers: fraction who sold during pump / within 1h; fraction selling >=50% of pre-start buy USD
rows=[]
for kind in ("pump","dump"):
    for nm in (["ALL","full_retrace","continue","plateau"] if kind=="pump" else ["ALL"]):
        Y=WL[(WL.kind==kind)&(WL.role=="early(pre-start)")]
        if nm!="ALL": Y=Y[Y.cls==nm]
        b=Y.buy_pre.clip(lower=1e-9)
        Y2=Y[Y.buy_pre>0]
        rows.append(dict(group=f"{kind}:{nm}",early_wallet_event_pairs=len(Y2),
          sold_in_event_window=(Y2.sell_pump>0).mean(), sold_in_window_or_post1=((Y2.sell_pump+Y2.sell_post1)>0).mean(),
          sold_ge50pct_by_trig_plus1h=(((Y2.sell_pump+Y2.sell_post1+Y2.sell_pre)/Y2.buy_pre)>=0.5).mean(),
          sold_ge90pct_by_trig_plus1h=(((Y2.sell_pump+Y2.sell_post1+Y2.sell_pre)/Y2.buy_pre)>=0.9).mean(),
          usd_sold_to_usd_bought_pre=(Y2.sell_pump+Y2.sell_post1).sum()/Y2.buy_pre.sum()))
emit("Early buyers (first buy before event start): who exits",pd.DataFrame(rows).set_index("group"))
# sniper (first 10 buyers of token) role
rows=[]
for kind in ("pump","dump"):
    Y=WL[WL.kind==kind]; tot_s=Y.sell_win.sum(); tot_b=Y.buy_pump.sum()
    for nm,m in [("first-10 buyers of token",Y.rk<=10),("buyers rank 11-50",(Y.rk>10)&(Y.rk<=50)),("rank >50",Y.rk>50),("never logged buying",Y.rk.isna())]:
        rows.append(dict(kind=kind,group=nm,share_sell_usd=Y[m].sell_win.sum()/tot_s,share_pumpphase_buy_usd=Y[m].buy_pump.sum()/tot_b,sell_over_buy=Y[m].sell_win.sum()/max(Y[m].buy_pump.sum(),1)))
emit("Seller identity by token buy rank (rank by first buy time within the token)",pd.DataFrame(rows).set_index("kind"))
# tag
rows=[]
for kind in ("pump","dump"):
    Y=WL[WL.kind==kind]; tot_s=Y.sell_win.sum(); tot_b=Y.buy_pump.sum()
    for wt,g in Y.groupby("wt"):
        rows.append(dict(kind=kind,tag=wt,share_sell_usd=g.sell_win.sum()/tot_s,share_pumpphase_buy_usd=g.buy_pump.sum()/tot_b,wallets=g.w.nunique()))
emit("GMGN wallet tags (smart_money/insider/normal/untagged) share of sells vs pump-phase buys",pd.DataFrame(rows).set_index("kind"))
# funder cluster share
def fcl(sub):
    ws=set(sub.w); res=[]
    return None
WL["has_fund"]=WL.w.isin(fm.keys())
# cluster: wallets within the same event sharing a funder
fw=fund.copy()
pairs=WL[["eid","w"]].drop_duplicates().merge(fw,on="w")
cnt=pairs.groupby(["eid","funder"]).w.nunique().reset_index(name="k"); cnt=cnt[cnt.k>=2]
cl=pairs.merge(cnt,on=["eid","funder"])[["eid","w"]].drop_duplicates(); cl["clustered"]=True
WL=WL.merge(cl,on=["eid","w"],how="left"); WL["clustered"]=WL.clustered.fillna(False)
rows=[]
for kind in ("pump","dump"):
    Y=WL[WL.kind==kind]
    rows.append(dict(kind=kind,events_with_cluster=Y[Y.clustered].eid.nunique(),events=Y.eid.nunique(),wallets_with_funding_record=Y[Y.has_fund].w.nunique(),
      clustered_wallets=Y[Y.clustered].w.nunique(),sell_share_clustered=Y[Y.clustered].sell_win.sum()/Y.sell_win.sum(),buy_share_clustered=Y[Y.clustered].buy_pump.sum()/Y.buy_pump.sum()))
emit("Same-funder wallet clusters inside an event (wallet_funding coverage is thin)",pd.DataFrame(rows).set_index("kind"))
# distribution of sells by phase relative to event and role net flow
rows=[]
for kind in ("pump","dump"):
    for nm in (["ALL","full_retrace","continue","plateau"] if kind=="pump" else ["ALL"]):
        Y=WL[WL.kind==kind]; Y=Y if nm=="ALL" else Y[Y.cls==nm]
        s=pd.Series({"sell pre(1-2h before)":Y.sell_pre.sum(),"sell event window":Y.sell_pump.sum(),"sell post1":Y.sell_post1.sum(),"sell post2":Y.sell_post2.sum()})
        b=pd.Series({"buy pre":Y.buy_pre.sum(),"buy event window":Y.buy_pump.sum(),"buy post(1-2h)":Y.buy_post.sum()})
        rows.append(dict(group=f"{kind}:{nm}",events=Y.eid.nunique(),net_flow_event_window=(Y.buy_pump.sum()-Y.sell_pump.sum())/Y.eid.nunique(),
           buy_over_sell_event=Y.buy_pump.sum()/max(Y.sell_pump.sum(),1),sell_over_buy_post=(Y.sell_post1.sum()+Y.sell_post2.sum())/max(Y.buy_post.sum(),1)))
emit("Net flow by phase (USD per event)",pd.DataFrame(rows).set_index("group"))
# retrace vs continue: share of sell volume by early buyers, per event distribution
ev=WL[(WL.kind=="pump")].groupby("eid").apply(lambda g: pd.Series({"early_sell_share":g[g.role=="early(pre-start)"].sell_win.sum()/max(g.sell_win.sum(),1),
     "sniper_sell_share":g[g.rk<=10].sell_win.sum()/max(g.sell_win.sum(),1),"sell_win":g.sell_win.sum(),"buy_win":g.buy_pump.sum(),"sell_buy_ratio":g.sell_win.sum()/max(g.buy_pump.sum(),1),
     "early_sold_frac_of_pre_buys":(g[g.role=="early(pre-start)"].sell_win.sum())/max(g[g.role=="early(pre-start)"].buy_pre.sum(),1),"cls":g.cls.iloc[0]}),include_groups=False).reset_index()
ev=ev[ev.sell_win>0]
t=ev.groupby("cls")[["early_sell_share","sniper_sell_share","sell_buy_ratio","early_sold_frac_of_pre_buys"]].median(); t["n_events"]=ev.groupby("cls").size()
emit("Per-event medians by outcome class (sells in event window + 1h after trigger)",t)
ev.to_parquet(f"{W}/seller_event.parquet")
open(OUT,"w").write("\n".join(out))
