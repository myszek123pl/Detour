import sys, numpy as np, pandas as pd
pd.set_option('display.width',250); pd.set_option('display.max_columns',60)
S=sys.argv[1]
z=np.load(S+'/panel_ok.npz'); Pf,Hf,Lf,V,E,P=z['Pf'],z['Hf'],z['Lf'],z['V'],z['E'],z['P']
keep=(Hf.max(1)/E<300); Pf,Hf,Lf,V,E,P=Pf[keep],Hf[keep],Lf[keep],V[keep],E[keep],P[keep]; n=len(Pf); N=288
R=Pf/E[:,None]; HR=Hf/E[:,None]; LR=Lf/E[:,None]
traded=~np.isnan(P)
def pct(x,q=(10,25,50,75,90)): return {f'p{a}':round(float(np.percentile(x,a)),2) for a in q}
print('n',n,flush=True)

print('\n## A. P(recover entry) after closing at -X% below entry')
rows=[]
for X in (.3,.5,.7,.9):
    lvl=1-X; k=0;rec24=[];rec72=[];tt=[];rech=[];maxafter=[]
    for i in range(n):
        w=np.where(R[i]<=lvl)[0]
        if len(w)==0: continue
        j=w[0]; k+=1
        post=HR[i,j+1:]; rc=np.where(R[i,j+1:]>=1.0)[0]
        rec72.append(len(rc)>0); rec24.append(len(rc)>0 and rc[0]<96)
        if len(rc): tt.append((rc[0]+1)*.25)
        rech.append(np.any(post>=1.0)); maxafter.append(post.max() if len(post) else 0)
    rows.append(dict(level=f'-{int(X*100)}%',P_hit=k/n,n=k,rec_close_72h=np.mean(rec72),rec_close_24h=np.mean(rec24),rec_high_72h=np.mean(rech),t_rec_med_h=np.median(tt) if tt else np.nan,t_rec_p90_h=np.percentile(tt,90) if tt else np.nan,P_2x_off_level=np.mean(np.array(maxafter)>=2*lvl)))
print(pd.DataFrame(rows).round(3).to_string(index=False),flush=True)
print('-- split by whether token printed >=1.5x (high) BEFORE hitting the level')
rows=[]
for X in (.3,.5,.7):
    lvl=1-X
    for pumped in (False,True):
        r=0;tot=0
        for i in range(n):
            w=np.where(R[i]<=lvl)[0]
            if len(w)==0: continue
            j=w[0]; pre=HR[i,:j+1].max()
            if (pre>=1.5)!=pumped: continue
            tot+=1; r+=np.any(R[i,j+1:]>=1.0)
        rows.append(dict(level=f'-{int(X*100)}%',pumped_before=pumped,n=tot,rec_close_72h=r/max(tot,1)))
print(pd.DataFrame(rows).round(3).to_string(index=False),flush=True)

print('\n## B. After a pump (running peak >= minpk x entry): drawdown X from running peak (first close at/below)')
rm=np.maximum.accumulate(HR,axis=1)
rows=[]
for X in (.3,.5,.7):
  for minpk in (1.3,2.0):
    k=0;rec_peak=[];newath=[];b2=[];b15=[];reent=[];alive=[]
    for i in range(n):
        d=np.where((R[i]<=(1-X)*rm[i])&(rm[i]>=minpk))[0]
        if len(d)==0: continue
        j=d[0]; pk=rm[i,j]; k+=1
        post_h=HR[i,j+1:]
        if len(post_h)==0:
            for l in (rec_peak,newath,b2,b15,reent,alive): l.append(False)
            continue
        runmin=np.maximum(np.minimum.accumulate(R[i,j:-1]),1e-12)
        rec_peak.append(np.any(post_h>=pk)); newath.append(np.any(post_h>=1.2*pk))
        b2.append(np.any(post_h>=2*runmin)); b15.append(np.any(post_h>=1.5*runmin))
        reent.append(np.any(R[i,j+1:]>=1.0)); alive.append(traded[i,j+1:j+25].sum()>=4)
    rows.append(dict(drawdown=f'-{int(X*100)}%',peak_ge=f'{minpk}x',n=k,share_all=k/n,P_old_peak=np.mean(rec_peak),P_new_ATH_1_2x=np.mean(newath),P_2x_off_low=np.mean(b2),P_1_5x_off_low=np.mean(b15),P_close_ge_entry=np.mean(reent),P_trading_6h_after=np.mean(alive)))
print(pd.DataFrame(rows).round(4).to_string(index=False),flush=True)
print('\n## B2. timing of bounce (-50% from peak>=2x)')
rows=[]
for w in (4,24,96,288):
    c2=0;c15=0;tot=0;rp=0
    for i in range(n):
        d=np.where((R[i]<=.5*rm[i])&(rm[i]>=2))[0]
        if len(d)==0: continue
        j=d[0]; tot+=1; hh=HR[i,j+1:j+1+w]
        if len(hh)==0: continue
        mn=np.maximum(np.minimum.accumulate(R[i,j:j+len(hh)]),1e-12)
        c2+=np.any(hh>=2*mn); c15+=np.any(hh>=1.5*mn); rp+=np.any(hh>=rm[i,j])
    rows.append(dict(window_h=w*.25,n=tot,P_100pct_bounce=c2/tot,P_50pct_bounce=c15/tot,P_old_peak=rp/tot))
print(pd.DataFrame(rows).round(4).to_string(index=False),flush=True)

print('\n## C. Volume lifecycle')
Vs=np.nan_to_num(V); tot=Vs.sum(1); okv=tot>0
cum=np.cumsum(Vs,axis=1)/np.maximum(tot,1e-12)[:,None]
t50=np.argmax(cum>=.5,axis=1)*.25; t90=np.argmax(cum>=.9,axis=1)*.25
print('tokens w/ volume',okv.sum()); print('t50',pct(t50[okv])); print('t90',pct(t90[okv]))
print('median cum share of 72h volume at 15m/1h/6h/24h:',[round(float(np.median(cum[okv,b])),3) for b in (0,3,23,95)])
c1=np.cumsum(np.pad(Vs,((0,0),(1,0))),axis=1); roll=c1[:,4:]-c1[:,:-4]
pkv=roll.max(1); ipv=roll.argmax(1)
hl=np.full(n,np.nan);hl10=np.full(n,np.nan)
for i in np.where(okv)[0]:
    seg=roll[i,ipv[i]:]
    a=np.where(seg<=.5*pkv[i])[0]; b=np.where(seg<=.1*pkv[i])[0]
    if len(a): hl[i]=a[0]*.25
    if len(b): hl10[i]=b[0]*.25
print('peak 1h vol window start h',pct(ipv[okv]*.25))
print('hours peak-vol -> rolling1h<=50%% of peak: P(reached)=%.3f'%np.mean(~np.isnan(hl[okv])),pct(hl[okv&~np.isnan(hl)]))
print('hours peak-vol -> <=10%% of peak: P(reached)=%.3f'%np.mean(~np.isnan(hl10[okv])),pct(hl10[okv&~np.isnan(hl10)]))
hv=Vs[:,:288].reshape(n,72,4).sum(2); base=hv[:,0]; m=base>0
print('hour | median(vol_h/vol_hour0) | aggregate')
for h in (0,1,2,3,4,6,8,12,18,24,36,48,71): print(h, round(float(np.median(hv[m,h]/base[m])),4), round(float(hv[m,h].sum()/base[m].sum()),4))
aggs=np.array([hv[m,h].sum()/base[m].sum() for h in range(72)])
sl=np.polyfit(np.arange(1,25),np.log(np.maximum(aggs[1:25],1e-9)),1)[0]; print('aggregate exp half-life h1-24: %.2f h'%(np.log(2)/-sl))
medr=np.array([np.median(hv[m,h]/base[m]) for h in range(72)])
for fr in (.5,.25,.1):
    kk=np.where(medr<=fr)[0]; print(f'hour median vol <= {fr:.0%} of first hour:',kk[0] if len(kk) else None)
pkk=HR.max(1)
for lo,hi,name in ((0,1.25,'peak<1.25x'),(1.25,2,'1.25-2x'),(2,5,'2-5x'),(5,1e9,'5x+')):
    mm=okv&(pkk>=lo)&(pkk<hi); h_=hl[mm]
    print(f' {name}: n={mm.sum()} median t50vol={np.median(t50[mm]):.2f}h t90={np.median(t90[mm]):.2f}h; vol half-life from peak-vol median={np.nanmedian(h_):.2f}h p75={np.nanpercentile(h_,75):.2f}h; 72h USD vol median=${np.median(tot[mm]):,.0f}')
ip_price=np.argmax(Hf,axis=1)
print('price peak bar - vol peak start (h) median',np.median((ip_price[okv]-ipv[okv])*.25),' P(price peak at/before vol-peak hour end)=%.3f'%np.mean(ip_price[okv]<=ipv[okv]+3))
print('\n## C2. volume around -50% from peak event (peak>=2x)')
rat=[];before=[]
for i in range(n):
    d=np.where((R[i]<=.5*rm[i])&(rm[i]>=2))[0]
    if len(d)==0 or not okv[i]: continue
    j=d[0]
    if j<4: continue
    before.append(Vs[i,j-4:j].sum()/max(pkv[i],1e-9)); rat.append(Vs[i,j+1:j+9].sum()/max(2*pkv[i],1e-9))
print('n',len(rat),'vol 1h before drop / peak1h vol median',np.median(before).round(3),'; avg 1h vol over 2h after drop / peak1h vol median',np.median(rat).round(3))
