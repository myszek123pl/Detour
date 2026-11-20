import numpy as np
rng=np.random.default_rng(7)
def kelly(outs,ps):
    fs=np.linspace(0,0.99,99001)
    G=np.array([(ps*np.log(1+f*(outs-1))).sum() for f in fs[::50]])
    i=int(np.argmax(G)); f0=fs[::50][i]
    fs2=np.linspace(max(0,f0-0.001),f0+0.001,2001); G2=[(ps*np.log(1+f*(outs-1))).sum() for f in fs2]
    j=int(np.argmax(G2)); return fs2[j],G2[j]
g=lambda f,o,p:(p*np.log(1+f*(o-1))).sum()
outsB=np.array([0.1,0.7,1.8,4,10,40]); psB=np.array([0.45,0.30,0.13,0.08,0.03,0.01])
m=(psB*outsB).sum(); print("B mean",m, "contrib",np.round(psB*outsB/m,3),"win rate",psB[outsB>1].sum())
fk,gk=kelly(outsB,psB); print("B kelly",fk,gk, "mu/var", (m-1)/((psB*(outsB-m)**2).sum()))
for c in [1,0.5,0.25,0.1]:
    print(" c",c,"f",round(c*fk,4),"g",round(g(c*fk,outsB,psB),5),"ratio to max",round(g(c*fk,outsB,psB)/gk,3))
print(" 2x kelly g",g(2*fk,outsB,psB))
# without top tail 40x
psC=psB.copy(); psC[5]=0; psC[0]+=0.01; mC=(psC*outsB).sum(); fC,gC=kelly(outsB,psC); print("B w/o 40x mean",mC,"kelly",fC)
# tail halved (10x prob 1.5%, 40x 0.5%)
psD=psB.copy(); psD[4]=0.015; psD[5]=0.005; psD[0]+=0.02; mD=(psD*outsB).sum(); fD,gD=kelly(outsB,psD)
print("B tail halved mean",mD,"kelly",fD,"growth if bet est. kelly",g(fk,outsB,psD),"half",g(fk/2,outsB,psD),"quarter",g(fk/4,outsB,psD))
# Monte Carlo drawdowns
N=500; sims=20000
for c in [1,0.5,0.25,0.1]:
    f=c*fk
    draws=rng.choice(outsB,size=(sims,N),p=psB)
    w=np.cumprod(1+f*(draws-1),axis=1); w=np.concatenate([np.ones((sims,1)),w],axis=1)
    peak=np.maximum.accumulate(w,axis=1); dd=1-w/peak; mdd=dd.max(axis=1)
    print(f"c={c} f={f:.4f}: median final {np.median(w[:,-1]):.2f}, P(final<1) {np.mean(w[:,-1]<1):.3f}, median MDD {np.median(mdd):.3f}, P(MDD>50%) {np.mean(mdd>0.5):.3f}, P(MDD>30%) {np.mean(mdd>0.3):.3f}, P(ever<0.5 start) {np.mean(w.min(axis=1)<0.5):.3f}")
# losing streaks: P(loss)=0.75 per trade
pl=psB[outsB<1].sum(); print("loss prob",pl)
def p_streak(n,k,p):
    # prob of at least one run of >=k losses in n trials, DP
    dp=np.zeros(k); dp[0]=1; hit=0
    for _ in range(n):
        new=np.zeros(k); new[0]=dp.sum()*(1-p)
        for j in range(k-1): new[j+1]=dp[j]*p
        hit+=dp[k-1]*p; dp=new
    return hit
for k in [10,15,20,25,30]: print(" P(run>=",k,"losses in 500 trades)",round(p_streak(500,k,pl),3))
print("expected longest run approx log(n*(1-p))/log(1/p)", np.log(500*(1-pl))/np.log(1/pl))
