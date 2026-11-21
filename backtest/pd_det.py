"""Real-time top-avoidance detector, walk-forward by date. python3 -I pd_det.py <work> <out_md>"""
import sys, numpy as np, pandas as pd, lightgbm as lgb, warnings
warnings.filterwarnings("ignore")
from sklearn.metrics import roc_auc_score
sys.path.insert(0,"/home/user/Detour/backtest"); from pd_md import md
W,OUT=sys.argv[1:3]; out=[]
def emit(t,df):
    out.append(f"\n### {t}\n"); out.append(md(df)); print("\n###",t); print(df.to_string())
Q=pd.read_parquet(f"{W}/pump_Q.parquet")
Q["vlast_vs_prev"]=np.log1p(Q.v_last)-np.log1p(Q.v_prev)
Q["log_kstart"]=np.log1p(Q.k_start)
Q=Q[Q.fw>=8].copy()
Q["trap"]=((Q.fmax8<0.10)&(Q.r8<=-0.25)).astype(int)
Q["retr"]=(Q.cls=="full_retrace").astype(int)
Q["good"]=(Q.cls=="continue").astype(int)
Q["day"]=pd.to_datetime(Q.t_trig,unit="s").dt.floor("D")
print("n",len(Q),"trap rate",Q.trap.mean(),"retrace rate",Q.retr.mean(),"good",Q.good.mean())
cand=["trig_mult","nsteps","last_ret","prev_ret","uwick","cpos","hi_over_close","log_vpump15","vol_ratio","vlast_vs_base","vlast_vs_prev","log_age","log_mcap","pre_run","from_first","log_kstart"]
snap=["s_holder_count","s_top10_holder_pct","s_bundler_ratio","s_sniper_count","s_fresh_wallet_pct","liq_mcap","s_smart_money_count","s_crew_cohesion","s_flipper_ratio","s_seller_loss_ratio","s_insider_pct_holders","s_cluster_max_pct"]
days=sorted(Q.day.unique())
PAR=dict(objective="binary",learning_rate=0.03,num_leaves=8,min_data_in_leaf=60,feature_fraction=.8,bagging_fraction=.8,bagging_freq=1,lambda_l2=10,verbose=-1,seed=1,num_threads=4)
def wf(feats,y,start=5,df=Q):
    pr=pd.Series(np.nan,index=df.index)
    for k in range(start,len(days)):
        d=days[k]; tr=df[df.t_trig+7200<=d.timestamp()]; te=df[df.day==d]
        if len(tr)<800 or len(te)==0: continue
        m=lgb.train(PAR,lgb.Dataset(tr[feats],tr[y]),num_boost_round=250)
        pr.loc[te.index]=m.predict(te[feats])
    return pr
res={}
for nm,fs in [("candle",cand),("candle+snapshot",cand+snap)]:
    res[nm]=wf(fs,"trap")
oos=Q[res["candle"].notna()].copy()
rows=[]
for nm,p in res.items():
    ok=p.notna()
    rows.append(dict(model=nm,n_oos=ok.sum(),AUC_trap=roc_auc_score(Q.trap[ok],p[ok]),AUC_vs_retrace_label=roc_auc_score(Q.retr[ok],p[ok]),AUC_good_inverse=roc_auc_score(1-Q.good[ok],p[ok])))
emit("Walk-forward (daily refit, expanding train, 2h purge) AUC for label TRAP = (no close >+10% above entry within 2h) & (-25% after 2h)",pd.DataFrame(rows).set_index("model"))
# simple rule baselines (no fitting)
rule=pd.DataFrame({"vol_fading(vlast_vs_base<0)":(Q.vlast_vs_base<0).astype(int),"young(age<60min)":(Q.age_min<60).astype(int),
   "blowoff(trig_mult>=2.5)":(Q.trig_mult>=2.5).astype(int),"upper_wick>0.3":(Q.uwick>0.3).astype(int),
   "vol_fading & young":((Q.vlast_vs_base<0)&(Q.age_min<120)).astype(int)})
rows=[]
for c in rule:
    r=rule[c].astype(bool)
    rows.append(dict(rule=c,flag_rate=r.mean(),precision_trap=Q.trap[r].mean(),base_trap=Q.trap.mean(),recall_trap=(r&(Q.trap==1)).sum()/Q.trap.sum(),
      good_lost=(r&(Q.good==1)).sum()/Q.good.sum(),mean_r8_flagged=Q.r8[r].mean(),mean_r8_unflagged=Q.r8[~r].mean()))
emit("Single-feature rules (no fitting; whole sample)",pd.DataFrame(rows).set_index("rule"))
# threshold table OOS
rng=np.random.default_rng(0)
def boot_diff(df,mask,col="r8",n=1000):
    toks=df.tok.values; ut,inv=np.unique(toks,return_inverse=True)
    kept=df[~mask]; 
    d=[]
    for _ in range(n):
        s=rng.integers(0,len(ut),len(ut)); w=np.bincount(s,minlength=len(ut))[inv]
        a=np.average(df[col],weights=w); k=np.average(kept[col],weights=w[~mask.values]); d.append(k-a)
    return np.percentile(d,[2.5,97.5])
rows=[]
for nm in ("candle","candle+snapshot"):
    p=res[nm]; o=Q[p.notna()].copy(); o["p"]=p[p.notna()]
    for thr in (0.45,0.55,0.65):
        flag=o.p>=thr
        if flag.sum()<20: continue
        ci=boot_diff(o,flag)
        rows.append(dict(model=nm,thr=thr,skip_rate=flag.mean(),precision_trap=o.trap[flag].mean(),base_trap=o.trap.mean(),recall_trap=(flag&(o.trap==1)).sum()/o.trap.sum(),
          good_continue_lost=(flag&(o.good==1)).sum()/o.good.sum(),mean_r8_all=o.r8.mean(),mean_r8_kept=o.r8[~flag].mean(),med_r8_all=o.r8.median(),med_r8_kept=o.r8[~flag].median(),
          gain_kept_minus_all_CI95=f"[{ci[0]:+.3f},{ci[1]:+.3f}]",mean_r4_kept=o.r4[~flag].mean(),mean_r4_all=o.r4.mean()))
emit("Out-of-sample filter performance (pooled test days 2026-06-15..29), gross of fees/slippage",pd.DataFrame(rows).set_index("model"))
# by test week / day-block
p=res["candle"]; o=Q[p.notna()].copy(); o["p"]=p[p.notna()]
o["blk"]=np.where(o.day<pd.Timestamp("2026-06-20"),"15-19 Jun",np.where(o.day<pd.Timestamp("2026-06-25"),"20-24 Jun","25-29 Jun"))
rows=[]
for b,g in o.groupby("blk"):
    f=g.p>=0.55
    rows.append(dict(block=b,n=len(g),AUC=roc_auc_score(g.trap,g.p),base_trap=g.trap.mean(),skip=f.mean(),precision=g.trap[f].mean(),recall=(f&(g.trap==1)).sum()/g.trap.sum(),mean_r8_all=g.r8.mean(),mean_r8_kept=g.r8[~f].mean()))
emit("Candle model, thr 0.55, by test block",pd.DataFrame(rows).set_index("block"))
# calibration / decile
o["dec"]=pd.qcut(o.p,5,labels=False)
emit("Candle model OOS by risk quintile",o.groupby("dec").agg(n=("p","size"),mean_p=("p","mean"),trap_rate=("trap","mean"),retrace=("retr","mean"),good=("good","mean"),mean_r1h=("r4","mean"),mean_r2h=("r8","mean"),med_r2h=("r8","median")))
# buy-everything vs filter, plus "buy only lowest-risk quintile"
# feature importance (final model on all)
m=lgb.train(PAR,lgb.Dataset(Q[cand+snap],Q.trap),num_boost_round=250)
imp=pd.Series(m.feature_importance("gain"),index=cand+snap); emit("LightGBM gain importance (all data, descriptive)",(imp/imp.sum()).sort_values(ascending=False).head(12).to_frame("gain share"))
# --- trade-feature subset: static time split
T=Q[Q.tradeok].copy()
tf=[f"{a}_{b}" for b in ("pre","pump") for a in ("buy_share","nb15","n15","top5","new_tok_share_trades","fresh_ds_usd_share","mean_buy","med_a","ns")]
tr=T[T.day<pd.Timestamp("2026-06-20")]; te=T[T.day>=pd.Timestamp("2026-06-20")]
rows=[]
for nm,fs in [("candle",cand),("trade-log only",tf),("candle+trade-log",cand+tf)]:
    aucs=[]
    for sd in range(3):
        P2=dict(PAR,seed=sd); m=lgb.train(P2,lgb.Dataset(tr[fs],tr.trap),num_boost_round=200); aucs.append(roc_auc_score(te.trap,m.predict(te[fs])))
    rows.append(dict(features=nm,n_train=len(tr),n_test=len(te),AUC_test=np.mean(aucs),trap_rate_test=te.trap.mean()))
emit("Trade-log subset: train 10-19 Jun, test 20-29 Jun (events with full trade coverage)",pd.DataFrame(rows).set_index("features"))
open(OUT,"w").write("\n".join(out))
