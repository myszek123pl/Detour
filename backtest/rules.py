"""Robustness of research-derived safety rules across periods and variants.
Usage: python3 -I rules.py <out_dir>"""
import sys, json, numpy as np, pandas as pd
OUT=sys.argv[1]; FEE,TIP=0.0125,0.30
R=pd.read_parquet(f"{OUT}/sim_results.parquet"); R=R[R.peak_mult<1000]
rng=np.random.default_rng(1)
def net(df,s,pos=200):
    imp=(2*pos/df.liquidity_usd.clip(lower=1)).clip(upper=.9)
    return df[s]*(1-FEE-imp)**2-TIP*(1+df[s+'_n'])/pos-1
def boot(x):
    x=np.asarray(x); 
    if len(x)<15: return (None,None)
    m=[rng.choice(x,len(x)).mean() for _ in range(3000)]; return tuple(np.round(np.percentile(m,[2.5,97.5]),3))
C={
 'mint+freeze off':      lambda d:(d.mint_disabled==1)&(d.freeze_disabled==1),
 'top10<30%':            lambda d:d.top10_holder_pct.fillna(1)<.30,
 'dev<5%':               lambda d:d.dev_remaining_pct.fillna(0)<.05,
 'bundler<15%':          lambda d:d.bundler_pct_holders.fillna(0)<.15,
 'insider<15%':          lambda d:d.insider_pct_holders.fillna(0)<.15,
 'liq>=10k':             lambda d:d.liquidity_usd>=10000,
}
print("pass rate of each condition:",{k:round(float(f(R).mean()),3) for k,f in C.items()})
def apply(d,keys): 
    m=np.ones(len(d),bool)
    for k in keys: m&=C[k](d).to_numpy()
    return d[m]
split=pd.Timestamp('2026-06-24',tz='UTC')
variants={'ALL six':list(C),'without liq':[k for k in C if k!='liq>=10k'],'only liq>=10k':['liq>=10k'],
          'safety only (mint,top10,dev)':['mint+freeze off','top10<30%','dev<5%'],
          'anti-insider (bundler,insider)':['bundler<15%','insider<15%'],'without top10':[k for k in C if k!='top10<30%']}
out={}
for vn,keys in variants.items():
    for per,d in (('train',R[R.captured_at<split]),('test',R[R.captured_at>=split]),('all',R)):
        s=apply(d,keys)
        row={'n':len(s),'share2x':round(float((s.peak_mult>=2).mean()),3) if len(s) else None}
        for st in ('ladder_B','tight_D','runner_F','hold_24h'):
            x=net(s,st); row[st]=(round(float(x.mean()),3) if len(s) else None, boot(x))
        out[f"{vn} | {per}"]=row
        print(f"{vn:32s} {per:5s} n={row['n']:5d} 2x={row['share2x']}  B={row['ladder_B']}  D={row['tight_D']}  F={row['runner_F']}  hold={row['hold_24h']}")
json.dump(out,open(f"{OUT}/rules_results.json","w"),indent=1,default=str)
