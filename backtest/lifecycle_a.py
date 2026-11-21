import sys, numpy as np, pandas as pd
pd.set_option('display.width',220); pd.set_option('display.max_columns',50)
z=np.load(sys.argv[1],allow_pickle=True)
P,H,L,V,O0,t0,tsmax=z['P'],z['H'],z['L'],z['V'],z['O0'],z['t0'],int(z['tsmax'])
N=288
ok=(t0+N*900<=tsmax)
P,H,L,V,O0=P[ok],H[ok],L[ok],V[ok],O0[ok]; n=len(P); print('n tokens',n)
# ffill close
Pf=pd.DataFrame(P).ffill(axis=1).values.copy()
# bar k high/low: if no candle, equals ffilled close
Hf=np.where(np.isnan(H),Pf,H); Lf=np.where(np.isnan(L),Pf,L)
ncand=(~np.isnan(P)).sum(1)
E=O0
def pct(x,q=(5,10,25,50,75,90,95,99)): return pd.Series(np.nanpercentile(x,q),index=[f'p{a}' for a in q])
# Peak multiple (high-based) over first 24h / 72h
H24=Hf[:,:97]; H72=Hf
pk24=H24.max(1)/E; pk72=H72.max(1)/E
print('\n== Peak multiple (max high / entry) ==')
print(pd.DataFrame({'24h':pct(pk24),'72h':pct(pk72)}).round(3))
for x in (1.1,1.25,1.5,2,3,5,10,20,50):
    print(f'P(peak72>={x}x)={np.mean(pk72>=x):.4f}  P(peak24>={x}x)={np.mean(pk24>=x):.4f}')
# time to peak
ipk=np.argmax(Hf[:,:],axis=1); 
print('\n== time to peak (hours, 72h window) ==')
print('P(peak in first bar)',np.mean(ipk==0).round(3), 'P(<=1h)',np.mean(ipk<=4).round(3),'P(<=6h)',np.mean(ipk<=24).round(3),'P(<=24h)',np.mean(ipk<=96).round(3))
print(pct(ipk*0.25).round(2))
for lo,hi in ((1,1.25),(1.25,2),(2,3),(3,5),(5,10),(10,1e9)):
    m=(pk72>=lo)&(pk72<hi); print(f'peak in [{lo},{hi}) n={m.sum()} median t_peak h={np.median(ipk[m])*.25:.2f}  p25={np.percentile(ipk[m],25)*.25:.2f} p75={np.percentile(ipk[m],75)*.25:.2f}')
# for tokens with peak>=2, time to FIRST 2x
m2=pk72>=2
first2=np.argmax(Hf>=2*E[:,None],axis=1)
print('time to first 2x (h) among 2x tokens',pct(first2[m2]*.25).round(2).to_dict())
# drawdown from running peak (close-based on running high)
runmax=np.maximum.accumulate(Hf,axis=1)
dd=Pf/runmax-1
mdd=dd.min(1)
print('\n== Max drawdown from running peak (close vs running high), 72h ==')
print(pct(-mdd).round(3))
for x in (.3,.5,.7,.9,.95): print(f'P(maxDD>={x:.0%})={np.mean(-mdd>=x):.4f}')
# drawdown from the global peak after the peak
fin=Pf[:,-1]; 
ddp=np.array([Pf[i,ipk[i]:].min()/Hf[i,ipk[i]] -1 for i in range(n)])
print('post-peak trough vs peak',pct(-ddp).round(3).to_dict())
print('final(72h)/peak',pct(fin/pk72/E).round(3).to_dict())
# speed: bars from global peak to first close <= -50% of peak ; -30, -70, -90
print('\n== speed of decay after the global peak (hours from peak bar to first close <= level*peak) ==')
rows=[]
for lv in (.7,.5,.3,.1):
    tt=[];never=0
    for i in range(n):
        seg=Pf[i,ipk[i]:]<=lv*Hf[i,ipk[i]]
        if seg.any(): tt.append(np.argmax(seg)*.25)
        else: never+=1
    tt=np.array(tt); rows.append(dict(level=f'-{int((1-lv)*100)}%',P_reached=len(tt)/n,p10=np.percentile(tt,10),p25=np.percentile(tt,25),median=np.median(tt),p75=np.percentile(tt,75),p90=np.percentile(tt,90),frac_within_1h=np.mean(tt<=1),frac_within_15m=np.mean(tt<=.25)))
print(pd.DataFrame(rows).round(3))
# same, conditional on peak>=2x (real pumpers)
print('-- conditional on peak>=2x:')
rows=[]
for lv in (.7,.5,.3,.1):
    tt=[];cnt=0
    for i in np.where(m2)[0]:
        cnt+=1
        seg=Pf[i,ipk[i]:]<=lv*Hf[i,ipk[i]]
        if seg.any(): tt.append(np.argmax(seg)*.25)
    tt=np.array(tt); rows.append(dict(level=f'-{int((1-lv)*100)}%',P_reached=len(tt)/cnt,p10=np.percentile(tt,10),p25=np.percentile(tt,25),median=np.median(tt),p75=np.percentile(tt,75),p90=np.percentile(tt,90),frac_within_1h=np.mean(tt<=1)))
print(pd.DataFrame(rows).round(3))
# Terminal value vs entry at horizons
print('\n== Terminal close / entry at horizons ==')
hz={'15m':1,'30m':2,'1h':4,'2h':8,'4h':16,'6h':24,'12h':48,'24h':96,'48h':192,'72h':288}
rows={}
for k,b in hz.items():
    r=Pf[:,b]/E; rows[k]=dict(p10=np.percentile(r,10),p25=np.percentile(r,25),median=np.median(r),p75=np.percentile(r,75),p90=np.percentile(r,90),mean=r.mean(),P_gt1=np.mean(r>1),P_lt05=np.mean(r<.5),P_lt01=np.mean(r<.1),P_gt2=np.mean(r>2))
print(pd.DataFrame(rows).T.round(3))
# candle count / death
last_bar=np.array([ (np.where(~np.isnan(P[i]))[0].max()) for i in range(n)])
print('\n== last traded bar (activity lifetime, hours) ==')
print(pct(last_bar*.25).round(2).to_dict()); 
for h in (.25,1,6,24,48): print(f'P(last candle within {h}h)={np.mean(last_bar*.25<=h):.3f}')
print('fraction of tokens with close at last candle <0.1 entry', np.mean(Pf[:,-1]/E<.1).round(3))
np.savez('/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/panel_ok.npz',Pf=Pf,Hf=Hf,Lf=Lf,V=V,E=E,P=P,last_bar=last_bar)
