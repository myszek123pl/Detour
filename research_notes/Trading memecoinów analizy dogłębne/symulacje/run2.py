import numpy as np, json
import mc
from mc import *
POS=0.25; N=150000
base_cost=dict(pos_sol=POS,fee_in=0.0125,fee_out=0.0125,slip_in=0.015,slip_tp=0.015,slip_stop=0.04,
    delay_mu=0.02,delay_sd=0.04,p_buy_fail=0.12,p_sell_fail=0.08,p_sell_fail_dump=0.25,tip=0.0015,fail_fee=0.0005)
pg_cost=dict(base_cost,fee_in=0.0025,fee_out=0.0025,slip_in=0.02,delay_mu=0.05,delay_sd=0.05)
B=dict(stop=0.35,ladder=[(2,0.5),(5,0.25)],trail=0.4); A=dict(stop=0.35,ladder=[]); D=dict(stop=0.20,ladder=[(1.5,0.5)],trail=0.25)
def pg_central():
    return [("instant dump",0.45,(1.0,1.25),(1,6),(0.15,0.6),0.12),("fade",0.35,(1.05,1.5),(3,20),(0.4,0.85),0.03),
            ("2x cont",0.12,(2.0,3.0),(10,50),(0.5,1.5),0.0),("5x cont",0.06,(4.0,8.0),(20,80),(0.8,3.0),0.0),
            ("20x+",0.018,(12.0,60.0),(30,100),(2.0,15.0),0.0),("100x",0.002,(60.0,300.0),(40,110),(5.0,60.0),0.0)]
def tail_edge(cls,u):  # uplift only graduation-type classes (nearmiss, graduate, moon); mass from two worst classes
    c=[list(x) for x in cls]; add=0
    for i in (3,4,5): add+=c[i][1]*(u-1); c[i][1]*=u
    bad=c[0][1]+c[1][1]
    for i in (0,1): c[i][1]-=add*c[i][1]/bad
    assert min(x[1] for x in c)>0; return [tuple(x) for x in c]
def ev(cls,pol,cost,seed=1):
    m,f,k=run_trades(cls,N,np.random.default_rng(seed),pol,cost); return stats_lib(m,f,POS)[0],(m,f,k)
def bis(fn,lo,hi,it=10):
    def g(u):
        try: return fn(u)
        except AssertionError: return 9
    if g(lo)>=0: return lo
    for _ in range(it):
        mid=(lo+hi)/2
        if g(mid)>=0: hi=mid
        else: lo=mid
    return hi
R={}
# post-grad tables
for nm,cls in [("pg_central",pg_central()),("pg_optimistic",classes_postgrad())]:
    for pn,pol in [("A",A),("B",B),("D",D)]:
        e,(m,f,k)=ev(cls,pol,pg_cost); s=stats_lib(m,f,POS); R[f"{nm}|{pn}"]=dict(EV=s[0],med=s[1],win=s[2]); print(nm,pn,s[:3],flush=True)
rng=np.random.default_rng(5); P,_=gen_tokens(pg_central(),150000,rng); R["pg_central_hold_final"]=float(P[:,-1].mean()); R["pg_central_peak"]=float(P.max(1).mean())
# breakeven post-grad (hit-rate multiplier u on classes 2x+; <1 = worse than assumed)
for pn,pol in [("B",B),("D",D)]:
    R[f"BE_pg_central|{pn}"]=bis(lambda u:ev(apply_edge(pg_central(),u),pol,pg_cost)[0],0.05,1.0); print("BE pg",pn,R[f"BE_pg_central|{pn}"],flush=True)
    if pn=="B": 
        # if EV<0 at u=1, search upwards
        pass
e1=ev(pg_central(),B,pg_cost)[0]; R["pg_central_B_EV_u1"]=e1
if e1<0: R["BE_pg_central_up|B"]=bis(lambda u:ev(apply_edge(pg_central(),u),B,pg_cost)[0],1.0,3.0); print("BE pg up",R["BE_pg_central_up|B"],flush=True)
# breakeven graduation-only uplift (random entries, policy B)
for gn,g in [("0.3%",0.003),("0.8%",0.008),("2%",0.02)]:
    hi=40.0 if g<0.01 else 12.0
    R[f"BE_tail_{gn}|B"]=bis(lambda u:ev(tail_edge(classes_random(g),u),B,base_cost)[0],1.0,hi); print("BE tail",gn,R[f"BE_tail_{gn}|B"],flush=True)
# equity paths with position cap 1 SOL (liquidity assumption)
rngp=np.random.default_rng(11); paths=[]
sets=[("a random g0.8% / B",classes_random(0.008),base_cost,B),
      ("a random g0.8% / D (tight TP)",classes_random(0.008),base_cost,D),
      ("b filtered u=1.8 / B (near breakeven)",apply_edge(classes_random(0.008),1.8),base_cost,B),
      ("b filtered u=2 / B",apply_edge(classes_random(0.008),2.0),base_cost,B),
      ("b filtered u=3 / B",apply_edge(classes_random(0.008),3.0),base_cost,B),
      ("c postgrad central / B",pg_central(),pg_cost,B),
      ("c postgrad central tail x1.5 / B",apply_edge(pg_central(),1.5),pg_cost,B),
      ("c postgrad optimistic / B",classes_postgrad(),pg_cost,B)]
dist={}
for name,cls,cost,pol in sets:
    m,f,k=run_trades(cls,N,np.random.default_rng(3),pol,cost)
    for fr in [0.01,0.025,0.05]:
        for nt in [300,1000]:
            eq,mdd,ru=equity_paths(m,f,fr,rngp,10000,nt,pos_cap=1.0)
            paths.append(summarize(f"{name} f={fr} n={nt}",eq,mdd,ru))
    net=(m-1)-f/POS
    dist[name]=dict(EV=float(net.mean()),med=float(np.median(net)),p_win=float((net>0).mean()),p_gt2x=float((m>2).mean()),p_lt_half=float((m<0.5).mean()),
        p99=float(np.percentile(net,99)),p999=float(np.percentile(net,99.9)),trim01=float(np.sort(net)[:-int(len(net)*0.001)].mean()),trim1=float(np.sort(net)[:-int(len(net)*0.01)].mean()),sd=float(net.std()))
    print(name,dist[name],flush=True)
R["paths"]=paths; R["dist"]=dist
json.dump(R,open("res2.json","w"),indent=1)
print("DONE")
