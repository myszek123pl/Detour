import numpy as np

class R: pass
def minimize_scalar(fun,bounds,method=None):
    import numpy as np
    xs=np.linspace(bounds[0],bounds[1],200001); vals=[fun(x) for x in xs[::100]]
    i=int(np.argmin(vals)); lo=xs[max(0,(i-1)*100)]; hi=xs[min(len(xs)-1,(i+1)*100)]
    xs2=np.linspace(lo,hi,20001); v2=[fun(x) for x in xs2]; r=R(); r.x=xs2[int(np.argmin(v2))]; return r

# Example distribution of gross multiples (exit value / stake), before costs
outs = np.array([0.05,0.6,1.5,4,10,50])
ps   = np.array([0.50,0.30,0.12,0.06,0.015,0.005])
print("sum p",ps.sum())
m = (ps*outs).sum(); print("mean multiple",m,"EV per 1 staked",m-1)
cdf=np.cumsum(ps); print("median multiple", outs[np.searchsorted(cdf,0.5)])
print("contrib of each bucket to gross return:", ps*outs, (ps*outs)/m)
print("win rate (mult>1)", ps[outs>1].sum())
def g(f,outs=outs,ps=ps): return (ps*np.log(1+f*(outs-1))).sum()
for f in [0.01,0.02,0.03,0.05,0.08,0.1,0.15,0.2]:
    print("f",f,"g per trade",round(g(f),5),"growth over 1000 trades x",round(np.exp(1000*g(f)),2))
r=minimize_scalar(lambda f:-g(f),bounds=(0,0.94),method='bounded'); fk=r.x
print("Kelly f*",fk,"g*",g(fk))
mu=m-1; var=(ps*(outs-1-mu)**2).sum(); print("mu",mu,"var",var,"mu/var approx",mu/var)
# without 50x tail: remove 0.5% 50x -> move to 0.05
ps2=ps.copy(); ps2[5]=0.0; ps2[0]+=0.005
m2=(ps2*outs).sum(); print("no 50x: mean",m2)
r2=minimize_scalar(lambda f:-g(f,outs,ps2),bounds=(0,0.94),method='bounded'); print("no50x kelly",r2.x, g(r2.x,outs,ps2))
# overestimated tail: true 50x = 0.2%
ps3=ps.copy(); ps3[5]=0.002; ps3[0]+=0.003
m3=(ps3*outs).sum(); print("tail 0.2%: mean",m3)
r3=minimize_scalar(lambda f:-g(f,outs,ps3),bounds=(0,0.94),method='bounded'); print("tail0.2 kelly",r3.x, g(r3.x,outs,ps3))
print("betting est. kelly",fk,"on true dist growth",g(fk,outs,ps3))
for c in [0.25,0.5]:
    print("frac",c,"on true dist growth", g(c*fk,outs,ps3), "on est dist", g(c*fk))
np.save('fk.npy',fk)
