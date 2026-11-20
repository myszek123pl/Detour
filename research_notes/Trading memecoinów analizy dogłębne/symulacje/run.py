import numpy as np, json
from mc import *
POS=0.25  # SOL per trade
base_cost=dict(pos_sol=POS,fee_in=0.0125,fee_out=0.0125,slip_in=0.015,slip_tp=0.015,slip_stop=0.04,
    delay_mu=0.02,delay_sd=0.04,p_buy_fail=0.12,p_sell_fail=0.08,p_sell_fail_dump=0.25,tip=0.0015,fail_fee=0.0005)
pg_cost=dict(base_cost,fee_in=0.0025,fee_out=0.0025,slip_in=0.02,slip_tp=0.015,slip_stop=0.04,delay_mu=0.03,delay_sd=0.05)
pols={
 "A hold+stop35 (no TP)":dict(stop=0.35,ladder=[]),
 "B ladder 2x:50% 5x:25% +trail40 + stop35":dict(stop=0.35,ladder=[(2,0.5),(5,0.25)],trail=0.4),
 "C ladder 2x:40% 4x:20% 10x:20% +trail50 + stop35":dict(stop=0.35,ladder=[(2,0.4),(4,0.2),(10,0.2)],trail=0.5),
 "D tight: 1.5x:50% +trail25 + stop20":dict(stop=0.20,ladder=[(1.5,0.5)],trail=0.25),
}
N=200000
out={}
def lib(cls,pol,cost,seed=1):
    rng=np.random.default_rng(seed); return run_trades(cls,N,rng,pol,cost)
def ev(cls,pol,cost): 
    m,f,k=lib(cls,pol,cost); return stats_lib(m,f,POS)[0],(m,f,k)
res={}
# sanity: gross hold-to-end mean of random tokens
rng=np.random.default_rng(5); P,k=gen_tokens(classes_random(),200000,rng)
res["sanity_random_hold_mean_final"]=float(P[:,-1].mean()); res["sanity_random_peak_mean"]=float(P.max(1).mean())
rng=np.random.default_rng(5); P,k=gen_tokens(classes_postgrad(),200000,rng)
res["sanity_pg_hold_mean_final"]=float(P[:,-1].mean()); res["sanity_pg_peak_mean"]=float(P.max(1).mean())
# scenario tables
scen={}
for gname,g in [("grad0.3%",0.003),("grad0.8%",0.008),("grad2%",0.02)]:
    scen[f"a_random_{gname}"]=(classes_random(grad=g),base_cost)
scen["c_postgrad"]=(classes_postgrad(),pg_cost)
tab={}
for sn,(cls,cost) in scen.items():
    for pn,pol in pols.items():
        e,(m,f,k)=ev(cls,pol,cost); s=stats_lib(m,f,POS)
        tab[(sn,pn)]=dict(EV=s[0],med=s[1],win=s[2]); 
        print(sn,pn,"EV %.3f med %.3f win %.3f"%s[:3],flush=True)
res["tab"]={f"{a}|{b}":v for (a,b),v in tab.items()}
# (b) filtered: uplift u on base grad 0.8%
for u in [1.0,1.5,2.0,3.0,5.0]:
    for pn in ["A hold+stop35 (no TP)","B ladder 2x:50% 5x:25% +trail40 + stop35"]:
        cls=apply_edge(classes_random(grad=0.008),u)
        e,_=ev(cls,pols[pn],base_cost); res[f"b_u{u}|{pn}"]=e; print("b u",u,pn,round(e,4),flush=True)
# breakeven uplift via bisection, per base grad and policy; also for post-grad with cost variants
def bisect(clsf,pol,cost,lo=1.0,hi=40.0):
    def f(u):
        try: return ev(apply_edge(clsf(),u),pol,cost)[0]
        except AssertionError: return 1
    if f(lo)>=0: return lo
    for _ in range(14):
        mid=(lo+hi)/2
        if f(mid)>=0: hi=mid
        else: lo=mid
    return hi
be={}
for gname,g in [("0.3%",0.003),("0.8%",0.008),("2%",0.02)]:
    for pn in ["A hold+stop35 (no TP)","B ladder 2x:50% 5x:25% +trail40 + stop35"]:
        # limit hi so assertion holds
        be[f"random grad {gname}|{pn}"]=bisect(lambda g=g:classes_random(grad=g),pols[pn],base_cost,hi=12.0 if g<0.01 else 5.0)
        print("BE",gname,pn,be[f"random grad {gname}|{pn}"],flush=True)
for pn in ["A hold+stop35 (no TP)","B ladder 2x:50% 5x:25% +trail40 + stop35"]:
    be[f"postgrad|{pn}"]=bisect(lambda:classes_postgrad(),pols[pn],pg_cost,hi=2.5)
    print("BE pg",pn,be[f"postgrad|{pn}"],flush=True)
res["breakeven_u"]=be
# cost sensitivity at u=1 and 2, policy B, grad .8%
cs={}
for cn,cc in [("base",base_cost),("+1% bot fee each way",dict(base_cost,fee_in=0.0225,fee_out=0.0225)),
              ("zero fees/slip/tip/fail (frictionless)",dict(base_cost,fee_in=0,fee_out=0,slip_in=0,slip_tp=0,slip_stop=0,delay_mu=0,delay_sd=0.0001,p_buy_fail=0,p_sell_fail=0,p_sell_fail_dump=0,tip=0,fail_fee=0)),
              ("no failed tx",dict(base_cost,p_buy_fail=0,p_sell_fail=0,p_sell_fail_dump=0)),
              ("tips x3",dict(base_cost,tip=0.0045))]:
    for u in [1.0,2.0]:
        e,_=ev(apply_edge(classes_random(0.008),u),pols["B ladder 2x:50% 5x:25% +trail40 + stop35"],cc); cs[f"{cn}|u{u}"]=e; print("cost",cn,u,round(e,4),flush=True)
res["cost_sens"]=cs
# equity paths
rngp=np.random.default_rng(11)
eqt={}
sets=[("a random grad0.8% / B",classes_random(0.008),base_cost,"B ladder 2x:50% 5x:25% +trail40 + stop35"),
      ("b filtered u=2 / B",apply_edge(classes_random(0.008),2.0),base_cost,"B ladder 2x:50% 5x:25% +trail40 + stop35"),
      ("b filtered u=3 / B",apply_edge(classes_random(0.008),3.0),base_cost,"B ladder 2x:50% 5x:25% +trail40 + stop35"),
      ("b filtered u=2 / A",apply_edge(classes_random(0.008),2.0),base_cost,"A hold+stop35 (no TP)"),
      ("c postgrad / B",classes_postgrad(),pg_cost,"B ladder 2x:50% 5x:25% +trail40 + stop35"),
      ("c postgrad edge u=1.5 / B",apply_edge(classes_postgrad(),1.5),pg_cost,"B ladder 2x:50% 5x:25% +trail40 + stop35")]
paths=[]
for name,cls,cost,pn in sets:
    m,f,k=lib(cls,pols[pn],cost,seed=3)
    for fr in [0.01,0.025,0.05]:
        for nt in [300,1000]:
            eq,mdd,ru=equity_paths(m,f,fr,rngp,10000,nt)
            d=summarize(f"{name} f={fr} n={nt}",eq,mdd,ru); paths.append(d)
    net=(m-1)-f/POS
    res.setdefault("dist",{})[name]=dict(EV=float(net.mean()),med=float(np.median(net)),p_win=float((net>0).mean()),p_gt2x=float((m>2).mean()),p_lt_half=float((m<0.5).mean()),
        p_lt_0p1=float((m<0.1).mean()),p99=float(np.percentile(net,99)),p999=float(np.percentile(net,99.9)),mean_trimmed_top01=float(np.sort(net)[:-int(len(net)*0.001)].mean()),
        mean_trimmed_top1=float(np.sort(net)[:-int(len(net)*0.01)].mean()),sd=float(net.std()))
    print(name,res["dist"][name],flush=True)
res["paths"]=paths
json.dump(res,open("res.json","w"),indent=1)
