import numpy as np
r=np.random.default_rng(2)
m=np.array([0,0.5,2,10,100.]);p=np.array([.70,.14,.10,.058,.002]) # filtered bot
print("EV mult",(m*p).sum())
def g(f,mm): 
    w=1+f*(mm-1); return (p*np.log(w)).sum() if w.min()>0 else -9
fs=np.linspace(0,.5,2001)
for name,mm in [("gross",m),("cost 3%+",m*0.97),("cost 6%",m*0.94),("cost 10%",m*0.90)]:
    gs=[g(f,mm) for f in fs]; i=int(np.argmax(gs)); print(name,"EV",(p*mm).sum()-1,"f*",fs[i],"g",gs[i])
def sim(f,mm,n=300,paths=20000):
    x=r.choice(5,size=(paths,n),p=p); eq=np.cumprod(1+f*(mm[x]-1),axis=1)
    pk=np.maximum.accumulate(eq,axis=1); dd=(1-eq/pk).max(axis=1)
    return [round(float(v),3) for v in (np.median(eq[:,-1]),np.mean(eq[:,-1]),np.mean(eq[:,-1]<1),np.median(dd),np.mean(dd>.5),np.mean(eq.min(axis=1)<.3))]
mm=m*0.94
for f in [0.01,0.02,0.03,0.05,0.10]: print(f,sim(f,mm))
