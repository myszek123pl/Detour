"""Threshold-sensitivity, entry-delay and size stress test of the combined rule.
Usage: python3 -I robust.py <data_dir> <out_dir>"""
import sys, json, numpy as np, pandas as pd
sys.argv=[sys.argv[0]]+sys.argv[1:]
D,OUT=sys.argv[1],sys.argv[2]; FEE,TIP=0.0125,0.30
R=pd.read_parquet(f"{OUT}/sim_results.parquet"); R=R[R.peak_mult<1000]
def net(df,s,pos=200,fee=FEE):
    imp=(2*pos/df.liquidity_usd.clip(lower=1)).clip(upper=.9)
    return df[s]*(1-fee-imp)**2-TIP*(1+df[s+'_n'])/pos-1
def sel(d,b=.15,i=.15,l=1e4,t10=.30,dev=.05):
    return d[(d.mint_disabled==1)&(d.freeze_disabled==1)&(d.top10_holder_pct.fillna(1)<t10)&(d.dev_remaining_pct.fillna(0)<dev)
             &(d.bundler_pct_holders<b)&(d.insider_pct_holders<i)&(d.liquidity_usd>=l)]
out={}
print("grid: bundler x insider x liq -> n, mean net ladder_B @ $200, mean tight_D")
for b in (.10,.15,.20,.30,.50):
  for i in (.10,.15,.20,.30):
    for l in (5e3,1e4,2e4,4e4):
      s=sel(R,b,i,l); 
      if len(s)<20: continue
      out[f"b{b}_i{i}_l{int(l)}"]=(len(s),round(float(net(s,'ladder_B').mean()),3),round(float(net(s,'tight_D').mean()),3))
g=pd.DataFrame(out,index=['n','B','D']).T; print(g.sort_index().to_string())
print("\nshare of grid cells with positive B:",round(float((g.B>0).mean()),2)," D:",round(float((g.D>0).mean()),2))
s=sel(R)
print("\nposition size / fee stress on base rule (n=%d):"%len(s))
for pos in (50,200,500,1000,3000):
  for fee in (.0125,.02):
    print(f"  pos ${pos:5d} fee {fee:.4f}: B={net(s,'ladder_B',pos,fee).mean():.3f}  D={net(s,'tight_D',pos,fee).mean():.3f}")
json.dump({'grid':out},open(f"{OUT}/robust_grid.json","w"),indent=1)
