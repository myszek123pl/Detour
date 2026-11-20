import numpy as np
r=np.random.default_rng(1)
# outcomes (multiple of stake): 80% -> 0.0 (rug/-100%), 12% -> 0.5, 6% -> 2, 1.8% ->10, 0.2% ->100  (gross)
m=np.array([0,0.5,2,10,100.]);p=np.array([.80,.12,.06,.018,.002])
print("EV gross multiple",(m*p).sum())
def ev(cost): # cost fraction round trip of stake + fixed
    return (m*p).sum()-1-cost
for c in [0,.02,.04,.08]: print(c,ev(c))
# kelly numeric growth
def g(f,mm,pp): return (pp*np.log(1+f*(mm-1))).sum() if (1+f*(mm-1)).min()>0 else -9
fs=np.linspace(0,1,1001)
gs=[g(f,m,p) for f in fs]; i=int(np.argmax(gs)); print("kelly f*",fs[i],"g",gs[i])
# with 3% costs: effective multiple after cost
m2=m*0.97
gs=[g(f,m2,p) for f in fs]; i=int(np.argmax(gs)); print("kelly cost f*",fs[i],"g",gs[i])
# sim
def sim(f,n=500,paths=5000,mm=m):
    x=r.choice(len(mm),size=(paths,n),p=p); w=1+f*(mm[x]-1); eq=np.cumprod(w,axis=1)
    peak=np.maximum.accumulate(eq,axis=1); dd=(1-eq/peak).max(axis=1)
    return np.median(eq[:,-1]),np.mean(eq[:,-1]<0.5),np.median(dd),np.mean(dd>0.5),np.mean(eq[:,-1]>1)
for f in [0.005,0.01,0.02,0.05,0.10]: print(f,sim(f))
print("with cost");
for f in [0.01,0.02,0.05]: print(f,sim(f,mm=m2*1.0))
