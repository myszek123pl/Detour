"""Re-computation of the rule backtest with/without liquidity-derived inputs. Usage: python3 -I forensics_final.py <out_dir>"""
import sys, json, numpy as np, pandas as pd
OUT=sys.argv[1]
FEE,TIP=0.0125,0.30
R=pd.read_parquet(f"{OUT}/sim_results.parquet"); R=R[R.peak_mult<1000].copy()
R['lm']=R.liquidity_usd/R.market_cap_usd
rng=np.random.default_rng(7)
def net(df,s,pos=200,imp=None):
    if imp is None: imp=(2*pos/df.liquidity_usd.clip(lower=1)).clip(upper=.9)
    return df[s]*(1-FEE-imp)**2-TIP*(1+df[s+'_n'])/pos-1
def ci(x):
    x=np.asarray(x); 
    if len(x)<10: return None
    m=[rng.choice(x,len(x)).mean() for _ in range(3000)]; return [round(float(v),3) for v in np.percentile(m,[2.5,97.5])]
five={'mint+freeze':(R.mint_disabled==1)&(R.freeze_disabled==1),'top10<30':R.top10_holder_pct.fillna(1)<.3,'dev<5':R.dev_remaining_pct.fillna(0)<.05,'bund<15':R.bundler_pct_holders.fillna(0)<.15,'ins<15':R.insider_pct_holders.fillna(0)<.15}
m5=np.ones(len(R),bool)
for v in five.values(): m5&=v.to_numpy()
liq=(R.liquidity_usd>=1e4).to_numpy()
STR=['ladder_B','tight_D','runner_F','hold_24h']
def row(name,mask,imp_fixed=None):
    d=R[mask]; out={'set':name,'n':len(d),'2x%':round(float((d.peak_mult>=2).mean()*100),1)}
    for s in STR:
        x=net(d,s,imp=None if imp_fixed is None else imp_fixed); out[s]=round(float(x.mean()),3); out[s+'_ci']=ci(x)
    return out
rows=[]
rows.append(row('ALL tradeable',np.ones(len(R),bool)))
rows.append(row('orig six, lm>0.6',m5&liq&(R.lm>.6).to_numpy()))
rows.append(row('orig six, lm<=0.6',m5&liq&(R.lm<=.6).to_numpy()))
rows.append(row('five safety (no liq)',m5))
rows.append(row('five safety, lm>0.6',m5&(R.lm>.6).to_numpy()))
rows.append(row('five safety, lm<=0.6',m5&(R.lm<=.6).to_numpy()))
rows.append(row('five safety, 0.3<lm<=0.6',m5&(R.lm>.3).to_numpy()&(R.lm<=.6).to_numpy()))
rows.append(row('five safety, lm<=1 (physically possible)',m5&(R.lm<=1).to_numpy()))
rows.append(row('five safety, lm>1 (impossible)',m5&(R.lm>1).to_numpy()))
# fixed impact 4% per side (liquidity-free cost model) 
rows.append(row('five safety, flat 4% impact',m5,imp_fixed=0.04))
rows.append(row('orig six lm>0.6, flat 4% impact',m5&liq&(R.lm>.6).to_numpy(),imp_fixed=0.04))
rows.append(row('five safety, lm<=1, flat 4% impact',m5&(R.lm<=1).to_numpy(),imp_fixed=0.04))
df=pd.DataFrame(rows); pd.set_option('display.width',300); pd.set_option('display.max_colwidth',40)
print(df[['set','n','2x%']+STR].to_string()); 
print(df[['set']+[s+'_ci' for s in STR]].to_string())
# time split on orig six lm>.6
S=R[m5&liq&(R.lm>.6).to_numpy()]; sp=pd.Timestamp('2026-06-24',tz='UTC')
for nm,d in (('train<06-24',S[S.captured_at<sp]),('test>=06-24',S[S.captured_at>=sp])):
    print(nm,len(d),{s:round(float(net(d,s).mean()),3) for s in STR})
# first half / second half by date among orig six hi
S=S.sort_values('captured_at'); h=len(S)//2
print('chronological halves',[ (len(a),round(float(net(a,'ladder_B').mean()),3)) for a in (S.iloc[:h],S.iloc[h:])])
# permutation test inside the 133 rows
F=R[m5&liq]; x=net(F,'ladder_B').to_numpy(); hi=(F.lm>.6).to_numpy()
obs=x[hi].mean()-x[~hi].mean(); cnt=0
for _ in range(10000):
    p=rng.permutation(hi); cnt+= (x[p].mean()-x[~p].mean())>=obs
print('perm test ladder_B hi-lo diff',round(float(obs),3),'p=',cnt/10000, 'n_hi',hi.sum(),'n_lo',(~hi).sum())
# forking paths: how many 'liq>=10k AND lm>t' cells; and effect of dropping top-5 winners
Sx=net(F[hi],'ladder_B').sort_values(ascending=False)
print('orig hi ladder_B mean',round(Sx.mean(),3),' without top3',round(Sx.iloc[3:].mean(),3),' median',round(Sx.median(),3))
# liq>=10k alone selects lm
print('P(lm>0.6 | liq>=10k & five)',round(float(hi.mean()),3),'  mc median in F',F.market_cap_usd.median())
df.to_json('/tmp/x/final.json',orient='records')
