import pandas as pd, numpy as np, warnings; warnings.filterwarnings('ignore')
B='/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/w27/'
p=pd.read_parquet(B+'panel.parquet').sort_values(['tok','bts']).reset_index(drop=True)
cap=pd.read_parquet(B+'tokfeat.parquet',columns=['tok','cap']).drop_duplicates('tok')
p=p.merge(cap,on='tok',how='left')
p['tr']=pd.to_datetime(p.cap,unit='s',utc=True)<pd.Timestamp('2026-06-20',tz='UTC')
g=p.groupby('tok')
p['k']=g.cumcount()
for s,nm in [(-1,'prev'),(1,'next'),(2,'next2')]:
    p['bts_'+nm]=g.bts.shift(-s); p['close_'+nm]=g.close.shift(-s); p['low_'+nm]=g.low.shift(-s); p['high_'+nm]=g.high.shift(-s)
ok1=p.bts_next==p.bts+900; ok2=(p.bts_next2==p.bts+1800)&ok1; okp=p.bts_prev==p.bts-900
p['fwd1']=np.where(ok1,np.log(p.close_next/p.close),np.nan)
p['fwd2']=np.where(ok2,np.log(p.close_next2/p.close),np.nan)
p['min1']=np.where(ok1,np.log(p.low_next/p.close),np.nan)
p['cur']=np.log(p.close/p.open)
p['prev']=np.where(okp,np.log(p.close/p.close_prev),np.nan)
for c in ['fwd1','fwd2','cur','prev','min1']: p[c]=p[c].clip(-1.5,1.5)
p['rkb']=pd.cut(p.k,[-1,0,1,3,7,1000],labels=['k0','k1','k2-3','k4-7','k8+'])
t=p[p.ntr>0].copy()
t['drop30']=np.where(t.fwd1.notna(),(t.fwd1<=np.log(0.7)).astype(float),np.nan)
coh={'ins':('ins_b','ins_s'),'sm':('sm_b','sm_s'),'cl':('cl_b','cl_s'),'early10':('e_b','e_s'),'all':('all_b','all_s')}
rng=np.random.default_rng(0)
def evstudy(df,b,s,minusd=300):
    ev=(df[s]>=minusd)&(df[s]>df[b])
    # control: bars with trades where cohort made no sell (<minusd)
    ct=(df[s]<minusd)
    out={}
    for y in ['prev','cur','fwd1','fwd2','min1','drop30']:
        diffs=[];w=[]
        for kb,gg in df.groupby('rkb'):
            e=gg[ev.loc[gg.index]][y].dropna(); c=gg[ct.loc[gg.index]][y].dropna()
            if len(e)>=15 and len(c)>=30: diffs.append(e.mean()-c.mean()); w.append(len(e))
        out[y]=np.average(diffs,weights=w) if diffs else np.nan
    return out, ev.sum(), df.loc[ev,'tok'].nunique()
def boot(df,b,s,nb=100):
    toks=df.tok.unique(); res=[]
    grp={k:v for k,v in df.groupby('tok')}
    for i in range(nb):
        sm=rng.choice(toks,len(toks)); d2=pd.concat([grp[k] for k in sm]); d2=d2.reset_index(drop=True)
        res.append(evstudy(d2,b,s)[0]['fwd1'])
    return np.nanpercentile(res,[2.5,97.5])
print('Event: cohort net-sells >=$300 in a 15-min bar (sell>buy). Effect = mean(event) - mean(control), stratified by bar index. units: log return')
for nm,(b,s) in coh.items():
    for lab,df in [('train',t[t.tr]),('test',t[~t.tr]),('all',t)]:
        o,ne,nt=evstudy(df,b,s)
        ci=''
        if lab=='all' and nm!='all': lo,hi=boot(df,b,s,20); ci=f' fwd1 95%CI[{lo:+.3f},{hi:+.3f}]'
        print(f'{nm:8s}{lab:6s} events={ne:6d} tokens={nt:5d} prev={o["prev"]:+.3f} cur={o["cur"]:+.3f} fwd1={o["fwd1"]:+.3f} fwd2={o["fwd2"]:+.3f} min1={o["min1"]:+.3f} P(drop30 next)diff={o["drop30"]:+.3f}{ci}')
# unconditional means
print('uncond fwd1 mean',t.fwd1.mean().round(3),'drop30 rate',t.drop30.mean().round(3))
# large-sell version (>=$2000) for insider and cluster
print('\nbigger events (>=$2000)')
for nm in ['ins','cl','early10','sm']:
    b,s=coh[nm]
    for lab,df in [('train',t[t.tr]),('test',t[~t.tr])]:
        o,ne,nt=evstudy(df,b,s,2000); print(f'{nm:8s}{lab:6s} events={ne:5d} prev={o["prev"]:+.3f} cur={o["cur"]:+.3f} fwd1={o["fwd1"]:+.3f} fwd2={o["fwd2"]:+.3f} drop30diff={o["drop30"]:+.3f}')
# peak-aligned
p['hmax']=g.high.transform('max'); p['isp']=(p.high==p.hmax)
pk=p[p.isp].drop_duplicates('tok')[['tok','bts']].rename(columns={'bts':'pbts'})
p=p.merge(pk,on='tok'); p['rel']=((p.bts-p.pbts)//900)
nbar=g.size().rename('nbar'); p=p.merge(nbar,on='tok')
q=p[(p.nbar>=6)&(p.rel.between(-3,3))]
print('\nPeak-aligned (tokens with >=6 bars): cohort sell share of its own cohort $ ; cohort share of total sell $ ; per rel bar')
rows=[]
for r_,gg in q.groupby('rel'):
    row={'rel':int(r_),'ntok_bars':int((gg.ntr>0).sum())}
    for nm,(b,s) in coh.items():
        if nm=='all': row['all_sellshare']=gg[s].sum()/(gg[s].sum()+gg[b].sum()); continue
        row[nm+'_sell/(b+s)']=gg[s].sum()/max(gg[s].sum()+gg[b].sum(),1); row[nm+'_%ofallsell']=gg[s].sum()/max(gg.all_s.sum(),1)
    rows.append(row)
print(pd.DataFrame(rows).round(3).to_string())
print('peak bar rel to capture: bars between cap and peak median',((p.drop_duplicates('tok').pbts-p.drop_duplicates('tok').cap)/900).describe().round(1).to_dict())
