import sys, numpy as np, pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
pd.set_option('display.width',250); pd.set_option('display.max_columns',60)
S=sys.argv[1]
z=np.load(S+'/panel_ok.npz'); Pf,Hf,Lf,V,E,P=z['Pf'],z['Hf'],z['Lf'],z['V'],z['E'],z['P']
keep=(Hf.max(1)/E<300); print('dropped glitch tokens (peak>300x):',(~keep).sum())
Pf,Hf,Lf,V,E,P=Pf[keep],Hf[keep],Lf[keep],V[keep],E[keep],P[keep]; n=len(Pf); N=Pf.shape[1]-1
def pct(x,q=(5,10,25,50,75,90,95,99)): return pd.Series(np.nanpercentile(x,q),index=[f'p{a}' for a in q])
def wmean(r,cap=50): return np.minimum(r,cap).mean()
print('n',n)
print('\n## bar-0: close0/open0 percentiles', pct(Pf[:,0]/E).round(3).to_dict())
# ---------- conv comparison
E2=Pf[:,0]
print('\n## Conv B (entry=close of bar0, path from bar1)')
pkB=Hf[:,1:].max(1)/E2
print(pct(pkB).round(3).to_dict())
for x in (1.25,1.5,2,3,5,10,20): print(f' P(peakB>={x}x)={np.mean(pkB>=x):.4f}',end=';')
print()
ipkB=np.argmax(Hf[:,1:],axis=1)+1
print('t_peakB h',pct((ipkB-0)*.25).round(2).to_dict(), 'P(peak at bar1)',np.mean(ipkB==1).round(3))
for lo,hi in ((1,1.25),(1.25,2),(2,3),(3,5),(5,10),(10,1e9)):
    m=(pkB>=lo)&(pkB<hi); print(f'  peakB in [{lo},{hi}) n={m.sum()} ({m.mean():.3%}) median t_peak h={np.median(ipkB[m])*.25:.2f} p25={np.percentile(ipkB[m],25)*.25:.2f} p75={np.percentile(ipkB[m],75)*.25:.2f} p90={np.percentile(ipkB[m],90)*.25:.2f}')
rows={}
for k,b in {'+15m':2,'+45m':4,'+1h':5,'+2h':9,'+6h':25,'+24h':97,'+72h':288}.items():
    r=Pf[:,b]/E2; rows[k]=dict(p10=np.percentile(r,10),p25=np.percentile(r,25),median=np.median(r),p75=np.percentile(r,75),p90=np.percentile(r,90),wmean=wmean(r),P_gt1=np.mean(r>1),P_gt2=np.mean(r>2),P_lt05=np.mean(r<.5),P_lt01=np.mean(r<.1))
print(pd.DataFrame(rows).T.round(3))
rows={}
for k,b in {'15m':1,'1h':4,'6h':24,'24h':96,'72h':288}.items():
    r=Pf[:,b]/E; rows[k]=dict(p10=np.percentile(r,10),p25=np.percentile(r,25),median=np.median(r),p75=np.percentile(r,75),p90=np.percentile(r,90),wmean=wmean(r),P_gt1=np.mean(r>1),P_gt2=np.mean(r>2),P_lt05=np.mean(r<.5),P_lt01=np.mean(r<.1))
print('Conv A terminal:'); print(pd.DataFrame(rows).T.round(3))

# ---------- clustering
print('\n## K-MEANS first 24h (conv A, log10 price/entry; sampled bars)')
samp=[0,1,2,3,4,6,8,12,16,20,24,32,40,48,56,64,72,80,88,96]
X=np.clip(np.log10(Pf[:,samp]/E[:,None]),-3,2)
res={}
for k in (4,5,6,7,8,9):
    km=KMeans(k,n_init=10,random_state=0).fit(X); res[k]=(silhouette_score(X,km.labels_,sample_size=4000,random_state=0),km.inertia_)
print({k:(round(a,3),round(b,0)) for k,(a,b) in res.items()})
K=int(sys.argv[2]) if len(sys.argv)>2 else 7
km=KMeans(K,n_init=30,random_state=0).fit(X); lab=km.labels_
ipk=np.argmax(Hf,axis=1); pk=Hf.max(1)/E
lastb=np.array([np.where(~np.isnan(P[i]))[0].max() for i in range(n)])
rows=[]
for c in range(K):
    m=lab==c
    rows.append(dict(cl=c,n=m.sum(),share=m.mean(),peak_med=np.median(pk[m]),peak_p90=np.percentile(pk[m],90),tpeak_h_med=np.median(ipk[m])*.25,
      r15m=np.median(Pf[m,1]/E[m]),r1h=np.median(Pf[m,4]/E[m]),r6h=np.median(Pf[m,24]/E[m]),r24h=np.median(Pf[m,96]/E[m]),r72h=np.median(Pf[m,288]/E[m]),
      P2x=np.mean(pk[m]>=2),P_end_lt50=np.mean(Pf[m,96]/E[m]<.5),P_end_gt1=np.mean(Pf[m,96]/E[m]>1),last_h_med=np.median(lastb[m])*.25,
      wmean24=wmean(Pf[m,96]/E[m]),vol_first1h_share=np.mean(V[m,:5].sum(1)/np.maximum(V[m].sum(1),1e-9))))
cl=pd.DataFrame(rows).sort_values('share',ascending=False); print(cl.round(3).to_string(index=False))
np.save(S+'/cluster_labels.npy',lab)
print('centroid log10 paths (bars):',samp)
for c in cl.cl: print(c,np.round(10**km.cluster_centers_[c],2))

# ---------- rule-based taxonomy (first 24h, conv A)
print('\n## Rule-based shapes (24h window, entry=bar0 open)')
R=Pf/E[:,None]
pk24=Hf[:,:97].max(1)/E; ip24=np.argmax(Hf[:,:97],axis=1)
r1h=R[:,4]; r6=R[:,24]; r24=R[:,96]; r72=R[:,288]
# trough after peak
trough_after=np.array([R[i,ip24[i]:97].min() for i in range(n)])
# second leg: after a >=50% drop from running peak(>=1.3x), later high >= 0.9*old peak or >=1.5x of post-drop min
shape=np.empty(n,dtype=object)
runmax=np.maximum.accumulate(Hf[:,:97]/E[:,None],axis=1)
for i in range(n):
    if pk24[i]>=5 and r24[i]>=2.0: shape[i]='runner (>=5x peak, still >=2x at 24h)'
    elif pk24[i]<1.25 and r1h[i]<0.5: shape[i]='instant dump (peak<1.25x, <0.5x at 1h)'
    else:
        # second leg
        dd=np.where(R[i,:97]<=0.5*runmax[i])[0]
        sl=False
        if len(dd) and runmax[i,dd[0]]>=1.3:
            j=dd[0]; mn=R[i,j]; 
            post=Hf[i,j+1:97]/E[i]
            if len(post):
                mins=np.minimum.accumulate(R[i,j:96]) if j<96 else np.array([])
                if len(mins)==len(post) and np.any(post>=max(2.0*mins,0)) and np.any(post>=0.8*runmax[i,j]): sl=True
        if sl: shape[i]='second leg (-50% then back to >=80% of old peak)'
        elif pk24[i]>=2 and r24[i]<0.5: shape[i]='pump then dump (>=2x peak, <0.5x at 24h)'
        elif pk24[i]>=2: shape[i]='pump & hold (>=2x peak, >=0.5x at 24h)'
        elif r24[i]<0.5: shape[i]='slow bleed (peak<2x, <0.5x at 24h, not instant)'
        else: shape[i]='flat/chop (peak<2x, >=0.5x at 24h)'
rows=[]
for s in pd.Series(shape).value_counts().index:
    m=shape==s
    rows.append(dict(shape=s,n=m.sum(),share=m.mean(),peak_med=np.median(pk24[m]),tpeak_h=np.median(ip24[m])*.25,r1h=np.median(r1h[m]),r6h=np.median(r6[m]),r24=np.median(r24[m]),r72=np.median(r72[m]),wmean24=wmean(r24[m]),wmean72=wmean(r72[m]),last_h=np.median(lastb[m])*.25))
print(pd.DataFrame(rows).round(3).to_string(index=False))
np.save(S+'/shape.npy',shape.astype(str))
