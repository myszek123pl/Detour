"""Anatomy tables (candle-level, trade-phase, continue-vs-retrace). python3 -I pd_a3.py <work> <out_md>"""
import sys, numpy as np, pandas as pd
from sklearn.metrics import roc_auc_score
sys.path.insert(0,"/home/user/Detour/backtest")
from pd_md import md
W, OUT = sys.argv[1], sys.argv[2]
pd.set_option("display.width",250); pd.set_option("display.max_columns",60)
M=pd.read_parquet(f"{W}/ev_out.parquet"); M["eid"]=M.eid.astype(int)
F=pd.read_parquet(f"{W}/phase_feats.parquet")
M["cov_pump"]=(M.t_start>=M.launch0-60)&(M.t_trig<=M.cap_last)
M["cov_post1"]=M.cov_pump&(M.t_trig+3600<=M.cap_last)
M["cov_pre"]=(M.t_start-M.launch0>=900)
out=[]
def emit(title,df,fmt="{:.3f}"):
    out.append(f"\n### {title}\n"); out.append(md(df)); print("\n###",title); print(df.to_string())
P=M[M.kind=="pump"].copy(); D=M[M.kind=="dump"].copy()
# ---- classes
O=P[P.fw>=8].copy()
O["retr"]=(O.p_trig*(1+O.fmin8))<=1.05*O.p0
O["cls"]=np.where(O.retr,"full_retrace",np.where(O.fmax8>=0.25,"continue","plateau"))
P=P.merge(O[["eid","cls"]],on="eid",how="left")
# ---- candle-level volumes per 15 min
def vol_table(X,label):
    X=X[X.n_pre>=2].copy()
    X["pre15"]=X.v_pre/X.n_pre; X["ev15"]=X.v_pump/X.nsteps; X["post1_15"]=X.v_post1/4; X["post2_15"]=X.v_post2/4
    t=pd.DataFrame({"median $/15m":X[["pre15","ev15","post1_15","post2_15"]].median(),"mean $/15m":X[["pre15","ev15","post1_15","post2_15"]].mean()})
    t["median ratio vs pre"]=[1.0,(X.ev15/X.pre15.clip(lower=1)).median(),(X.post1_15/X.pre15.clip(lower=1)).median(),(X.post2_15/X.pre15.clip(lower=1)).median()]
    t["n"]=[X.pre15.notna().sum(),X.ev15.notna().sum(),X.post1_15.notna().sum(),X.post2_15.notna().sum()]
    emit(f"Candle volume around {label} (events with >=2 pre candles)",t)
vol_table(P,"pumps"); vol_table(D,"dumps")
Pc=P[P.cls.notna()]
for cls,g in [("ALL",Pc)]+list(Pc.groupby("cls")):
    pass
t=Pc.groupby("cls").apply(lambda g: pd.Series({"n":len(g),"share":len(g)/len(Pc),
   "pre $/15m":(g.v_pre/g.n_pre.clip(lower=1)).median(),"event $/15m":(g.v_pump/g.nsteps).median(),"post1 $/15m":(g.v_post1/4).median(),"post2 $/15m":(g.v_post2/4).median()}),include_groups=False)
emit("Pump classes (2h forward, entry = trigger close): share and volume",t)
# ---- forward paths
rows=[]
for nm,g in [("ALL",Pc)]+list(Pc.groupby("cls")):
    rows.append(dict(cls=nm,n=len(g),**{f"med r{k*15}m":g[f"r{k}"].median() for k in (1,2,4,8,16)},**{f"mean r{k*15}m":g[f"r{k}"].mean() for k in (1,4,8)},
      med_fmax2h=g.fmax8.median(),med_fmin2h=g.fmin8.median(),med_trig_mult=g.trig_mult.median() if "trig_mult" in g else (g.p_trig/g.p0).median(),med_peak_mult=(g.p_peak/g.p0).median()))
emit("Forward return after buying at trigger close",pd.DataFrame(rows).set_index("cls"))
# long horizon
L=P[P.fw>=16]; emit("Fraction of pumps ending below pre-pump start price (close vs p0) by horizon",pd.DataFrame({"h":["+30m","+1h","+2h","+4h"],
   "share_below_start":[ (L.p_trig*(1+L[f"r{k}"])<L.p0).mean() for k in (2,4,8,16)],"share_below_entry":[(L[f"r{k}"]<0).mean() for k in (2,4,8,16)],"n":len(L)}).set_index("h"))
# retrace speed: first step at which close<=1.05*p0 (using grid)
G=pd.read_parquet(f"{W}/grid.parquet"); arr={t:g.c.values for t,g in G.groupby("tok",sort=False)}
def first_step(r,thr=1.05,H=16):
    c=arr[r.tok]; seg=c[r.i+1:r.i+1+H]
    hit=np.where(seg<=thr*r.p0)[0]
    return hit[0]+1 if len(hit) else np.nan
Lr=P[P.fw>=16].copy(); Lr["retr_step"]=[first_step(r) for r in Lr.itertuples()]
d=Lr.retr_step.value_counts(normalize=True,dropna=False).sort_index()
emit("Time (15m steps after trigger) until close first <= 1.05x pre-pump price (4h window, n=%d)"%len(Lr),pd.DataFrame({"share":d,"cum":d.cumsum()}))
# ---- mean path normalized to p0
rows=[]
for k in (0,1,2,3,4,6,8,12,16):
    x=(P.p_trig*(1+P[f"r{k}"]))/P.p0 if k>0 else P.p_trig/P.p0
    rows.append(dict(step_after_trigger=k,minutes=15*k,median_x_of_start=x.median(),p25=x.quantile(.25),p75=x.quantile(.75),n=x.notna().sum()))
emit("Median price path (multiple of pre-pump start price p0)",pd.DataFrame(rows).set_index("minutes"))
# ---- trade-phase tables
Fp=F.merge(M[["eid","nsteps","cls_dummy"]] if False else M[["eid","nsteps","kind"]].rename(columns={"kind":"k2"}),on="eid")
Fp["dur15"]=np.where(Fp.ph=="pump",Fp.nsteps,4)
Fp["n15"]=Fp.n/Fp.dur15; Fp["usd15"]=Fp.usd/Fp.dur15; Fp["nb15"]=Fp.nb/Fp.dur15
Fp["buy_share"]=Fp.buy_usd/Fp.usd; Fp["sellers_per_buyer"]=Fp.ns/Fp.nb.clip(lower=1); Fp["buy_cnt_share"]=np.nan
def phase_table(kind,cover):
    ids=set(M[(M.kind==kind)&cover].eid)
    X=Fp[(Fp.kind==kind)&Fp.eid.isin(ids)]
    # same-event comparable: require all three phases with >=5 trades
    cnt=X[X.n>=5].groupby("eid").ph.nunique(); ok=set(cnt[cnt>=3].index) if True else set()
    X=X[X.eid.isin(ok)&X.ph.isin(["pre","pump","post1"])]
    cols=["n15","usd15","buy_share","nb15","ns","med_a","mean_buy","top1","top5","hhi","new_tok_share_trades","fresh_ds_usd_share"]
    t=X.groupby("ph")[cols].median().loc[["pre","pump","post1"]]
    t["N_events"]=len(ok); return t
cov_all=M.cov_pump&M.cov_post1&M.cov_pre
emit("PUMP events: trade-log phases (median over events; pre = 1h before start, pump = event window, post1 = 1h after trigger)",phase_table("pump",cov_all))
emit("DUMP events: trade-log phases (pre = 1h before start, pump row = the dump window itself)",phase_table("dump",cov_all))
# means too
def phase_mean(kind):
    ids=set(M[(M.kind==kind)&cov_all].eid); X=Fp[(Fp.kind==kind)&Fp.eid.isin(ids)&Fp.ph.isin(["pre","pump","post1"])]
    cnt=X[X.n>=5].groupby("eid").ph.nunique(); X=X[X.eid.isin(cnt[cnt>=3].index)]
    return X.groupby("ph")[["buy_share","top5","new_tok_share_trades","fresh_ds_usd_share","med_a","mean_buy"]].mean().loc[["pre","pump","post1"]]
emit("PUMP events: phase means",phase_mean("pump"))
# ---- continue vs retrace on trade-phase features
Fw=Fp.pivot_table(index="eid",columns="ph",values=["n15","usd15","buy_share","nb15","ns","med_a","mean_buy","top1","top5","hhi","new_tok_share_trades","fresh_ds_usd_share"],aggfunc="first")
Fw.columns=[f"{a}_{b}" for a,b in Fw.columns]
Q=P.merge(Fw,left_on="eid",right_index=True,how="left")
Q["trig_mult"]=Q.p_trig/Q.p0
Q["tradeok"]=Q.eid.isin(set(M[cov_all].eid))&(Q.n15_pump.notna())&(Q.n15_pre.notna())&(Q.n15_post1.notna())
# derived features (only past info = up to trigger) for class comparison
Q["log_vpump15"]=np.log1p(Q.v_pump/Q.nsteps); Q["vol_ratio"]=np.log1p(Q.v_pump/Q.nsteps)-np.log1p(Q.v_pre/Q.n_pre.clip(lower=1))
Q["vlast_vs_base"]=np.log1p(Q.v_last)-np.log1p(Q.v_base)
Q["log_age"]=np.log1p(Q.age_min.clip(lower=0))
Q["mcap_trig"]=(Q.s_market_cap_usd*(Q.p_trig/Q.s_price_at_capture)).clip(1,1e9); Q["log_mcap"]=np.log10(Q.mcap_trig)
Q["liq_mcap"]=Q.s_liquidity_usd/Q.s_market_cap_usd
Q["trade_pump_share"]=Q.buy_share_pump
Q.to_parquet(f"{W}/pump_Q.parquet")
def cmp(feats,sub,title):
    X=sub[sub.cls.isin(["continue","full_retrace","plateau"])]
    rows=[]
    for f in feats:
        a=X[X.cls=="continue"][f].dropna(); b=X[X.cls=="full_retrace"][f].dropna(); p=X[X.cls=="plateau"][f].dropna()
        if len(a)<30 or len(b)<30: continue
        y=X[X.cls.isin(["continue","full_retrace"])]; yy=(y.cls=="continue").astype(int); xx=y[f]
        ok=xx.notna()
        auc=roc_auc_score(yy[ok],xx[ok]) if ok.sum()>50 and yy[ok].nunique()==2 else np.nan
        rows.append(dict(feature=f,med_continue=a.median(),med_plateau=p.median(),med_retrace=b.median(),AUC_cont_vs_retr=auc,n_cont=len(a),n_retr=len(b)))
    T=pd.DataFrame(rows).set_index("feature"); T["|AUC-.5|"]=(T.AUC_cont_vs_retr-.5).abs()
    emit(title,T.sort_values("|AUC-.5|",ascending=False).drop(columns="|AUC-.5|"))
cf=["trig_mult","nsteps","last_ret","prev_ret","uwick","cpos","hi_over_close","log_vpump15","vol_ratio","vlast_vs_base","log_age","log_mcap","pre_run","from_first","real_frac_pump"]
cmp(cf,Q,"Continue vs full retrace: candle features (known at trigger)")
sf=["s_holder_count","s_top10_holder_pct","s_bundler_ratio","s_dev_remaining_pct","s_sniper_count","s_fresh_wallet_pct","liq_mcap","s_smart_money_count","s_unique_buyers","s_unique_sellers","s_trade_buy_sell_ratio","s_flipper_ratio","s_seller_loss_ratio","s_cluster_max_pct","s_insider_pct_holders","s_rug_probability","s_crew_cohesion","s_only_buy_pct","s_profitable_pct","s_price_change_1h","s_has_twitter","s_is_boosted","s_lp_burned_pct"]
cmp(sf,Q,"Continue vs full retrace: snapshot features (GMGN, captured before trigger)")
tfeat=[f"{a}_{b}" for b in ("pre","pump") for a in ("buy_share","nb15","n15","top5","new_tok_share_trades","fresh_ds_usd_share","mean_buy","med_a","ns")]
cmp(tfeat,Q[Q.tradeok],"Continue vs full retrace: trade-log features pre-trigger (subset with trade coverage)")
# class comparison of post1 (outcome-side) trade behaviour
cmp([f"{a}_post1" for a in ("buy_share","nb15","n15","top5","new_tok_share_trades","fresh_ds_usd_share","mean_buy","ns")],Q[Q.tradeok],"(Outcome side, NOT usable in real time) trade behaviour in hour after trigger")
Q[Q.cls.notna()].groupby("cls").size().to_frame("n")
by=Q[Q.cls.notna()].groupby("ts_day").apply(lambda g: pd.Series({"n":len(g),"retrace":(g.cls=="full_retrace").mean(),"continue":(g.cls=="continue").mean(),"med_r8":g.r8.median()}),include_groups=False)
emit("Stability by trigger day",by)
open(OUT,"w").write("\n".join(out))
