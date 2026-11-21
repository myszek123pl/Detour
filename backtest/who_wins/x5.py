import sys, numpy as np, pandas as pd
sys.path.insert(0,"/home/user/Detour/backtest")
import exec_gap_lib as G
D="/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/datasets/solana-memecoin-dataset/repo/data"
t,paths=G.load(D); m,segs=G.build(t,paths)
feas=np.array([[s is not None for s in ss] for ss in segs]); U=np.where(feas.all(1))[0]
S=G.STRATS["ladder_B"]
for k in range(5):
    kk=np.full(len(segs),k)
    kk=np.where(feas[:,k],k,0)
    F,M,n,_=G.run_all(segs,kk,dict(stop_mode="exact"),S); g=(F*M).sum(1)
    gu=g[U]; print(k,"U top",np.sort(gu)[-5:].round(2),"allfeas top",np.sort(g[feas[:,k]])[-4:].round(1), "mean U",gu.mean().round(4))
# category shares at k=0 in U
sU=[segs[i] for i in U]
F,M,n,_=G.run_all(sU,np.zeros(len(U),int),dict(stop_mode="exact"),S); g=(F*M).sum(1)
last=np.array([ (F[i]*M[i])[F[i]>0][-1] for i in range(len(U))])
# classification by final tranche type: mult==0.5 stop; trail (mult>0.5 & not 2/5); time exit
fin=[]
for i in range(len(U)):
    k=(F[i]>0).sum()-1; fin.append(M[i,k])
fin=np.array(fin); lastfrac=np.array([F[i,(F[i]>0).sum()-1] for i in range(len(U))])
stop=(np.abs(fin-0.5)<1e-9); print("final tranche at stop 0.5:",stop.mean())
alltp=(F[:,0]>0)&(np.abs(M[:,0]-2)<1e-9)&(F[:,1]>0)&(np.abs(M[:,1]-5)<1e-9)
print("reached 2x:",((M==2)&(F>0)).any(1).mean(), "reached 5x:", ((M==5)&(F>0)).any(1).mean())
print("pnl contributions: sum of gross-1 by group: stop, other")
d=g-1
print("mean contribution stop-only(no tp):", d[stop&~((M==2)&(F>0)).any(1)].sum()/len(U))
print("contribution of tokens reaching 2x:", d[((M==2)&(F>0)).any(1)].sum()/len(U), " non-stop non-tp (time exit/trail):",d[~stop&~((M==2)&(F>0)).any(1)].sum()/len(U), (~stop&~((M==2)&(F>0)).any(1)).mean())
# truncated & timeexit
trunc=np.array([(s[0][-1][0]+900<s[0][0][0]+86400) for s in sU])
te=~stop&~((M==2)&(F>0)).any(1)
print("time-exit-only tokens: share",te.mean(),"mean final mult",fin[te].mean(), "median",np.median(fin[te]))
# winners
peak=np.array([max(x[2] for x in s[0])/s[0][0][1] for s in sU]); print("P(peak>=2,3,5,10)",[(peak>=x).mean().round(4) for x in (2,3,5,10)])
print("last close mult for truncated tokens quantiles", np.quantile([s[0][-1][4]/s[0][0][1] for s in sU],[.1,.25,.5,.75,.9]).round(3))
# wick reversal at stop
rev=0;tot=0
for s in sU:
    seg=s[0]; e=seg[0][1]
    for j,(ts,op,hi,lo,cl) in enumerate(seg):
        if lo<=e*0.5:
            tot+=1; 
            if cl>e*0.5: rev+=1
            break
print("stop trigger candles with close above stop (wick-out):",rev/tot, tot)
