import sys, numpy as np, pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
pd.set_option('display.width',250); pd.set_option('display.max_columns',60)
S=sys.argv[1]
z=np.load(S+'/panel_ok.npz'); Pf,Hf,Lf,V,E,P=z['Pf'],z['Hf'],z['Lf'],z['V'],z['E'],z['P']
keep=(Hf.max(1)/E<300); Pf,Hf,Lf,V,E,P=Pf[keep],Hf[keep],Lf[keep],V[keep],E[keep],P[keep]; n=len(Pf)
def wm(r,cap=50): return np.minimum(r,cap).mean()
R=Pf/E[:,None]; HR=Hf/E[:,None]
lastb=np.array([np.where(~np.isnan(P[i]))[0].max() for i in range(n)])
pk24=HR[:,:97].max(1); ip24=np.argmax(HR[:,:97],axis=1)
r1h=R[:,4]; r6=R[:,24]; r24=R[:,96]; r72=R[:,288]
rm=np.maximum.accumulate(HR[:,:97],axis=1)
shape=np.empty(n,dtype=object)
for i in range(n):
    sl=False
    dd=np.where((R[i,:97]<=0.5*rm[i])&(rm[i]>=1.3))[0]
    if len(dd) and dd[0]<96:
        j=dd[0]; pk=rm[i,j]
        post=HR[i,j+1:97]; mins=np.maximum(np.minimum.accumulate(R[i,j:96]),1e-12)
        sl=bool(np.any(post>=0.8*pk) and np.any(post>=2*mins))
    if pk24[i]>=5 and r24[i]>=2.0: shape[i]='runner: peak>=5x and still >=2x at 24h'
    elif sl: shape[i]='second leg: fell -50% from a >=1.3x peak, then >=2x off low AND >=80% of old peak'
    elif pk24[i]<1.25 and r1h[i]<0.5: shape[i]='instant dump: peak<1.25x and <0.5x by 1h'
    elif pk24[i]>=2 and r24[i]<0.5: shape[i]='pump then dump: peak>=2x, <0.5x at 24h'
    elif pk24[i]>=2: shape[i]='pump and hold/fade: peak>=2x, >=0.5x at 24h (no 2nd leg)'
    elif r24[i]<0.5: shape[i]='slow bleed: peak<2x, <0.5x at 24h (not instant)'
    else: shape[i]='flat/chop: peak<2x, >=0.5x at 24h'
rows=[]
for s in pd.Series(shape).value_counts().index:
    m=shape==s
    rows.append(dict(shape=s[:34],n=m.sum(),share=m.mean(),peak_med=np.median(pk24[m]),peak_p90=np.percentile(pk24[m],90),tpeak_h=np.median(ip24[m])*.25,r1h=np.median(r1h[m]),r6h=np.median(r6[m]),r24=np.median(r24[m]),r72=np.median(r72[m]),wmean24=wm(r24[m]),active_h_med=np.median(lastb[m])*.25))
print('## Rule-based shape taxonomy (24h, entry=first-candle open)');print(pd.DataFrame(rows).round(3).to_string(index=False),flush=True)
# nested: pump-then-dump detail - drop timing
m=(shape==[s for s in pd.Series(shape).unique() if s.startswith('pump then dump')][0])
tdrop=[]
for i in np.where(m)[0]:
    j=np.where(R[i,ip24[i]:]<=.5*pk24[i])[0]
    if len(j): tdrop.append(j[0]*.25)
print('pump-then-dump: hours from peak to -50%%: median %.2f p75 %.2f p90 %.2f'%tuple(np.percentile(tdrop,[50,75,90])))
# ---- K-means on pumpers only (peak>=2x within 24h), paths normalised by PEAK and by entry
mm=pk24>=2; idx=np.where(mm)[0]
samp=[0,1,2,3,4,6,8,12,16,24,32,48,64,80,96]
X=np.clip(np.log10(R[idx][:,samp]),-3,2)
print('\n## K-means among tokens that reached >=2x in 24h: n=',len(idx))
for k in (3,4,5,6,7): 
    km=KMeans(k,n_init=10,random_state=0).fit(X); print(k,round(silhouette_score(X,km.labels_),3),end='; ')
K=5; km=KMeans(K,n_init=30,random_state=0).fit(X); lab=km.labels_
rows=[]
for c in range(K):
    mk=idx[lab==c]
    rows.append(dict(cl=c,n=len(mk),share=len(mk)/len(idx),peak_med=np.median(pk24[mk]),peak_p90=np.percentile(pk24[mk],90),tpeak_h=np.median(ip24[mk])*.25,r1h=np.median(R[mk,4]),r6h=np.median(R[mk,24]),r24=np.median(R[mk,96]),r72=np.median(R[mk,288]),P_end24_gt1=np.mean(R[mk,96]>1),wmean24=wm(R[mk,96]),active_h=np.median(lastb[mk])*.25))
print('\n');print(pd.DataFrame(rows).sort_values('n',ascending=False).round(3).to_string(index=False))
for c in range(K): print(c,'centroid (x entry) at bars',samp,np.round(10**km.cluster_centers_[c],2))
