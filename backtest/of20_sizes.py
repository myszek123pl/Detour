import duckdb, numpy as np, pandas as pd
W = "/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/w/w.db"
c = duckdb.connect(W, read_only=True)
pd.set_option('display.width',250); pd.set_option('display.max_columns',50)
qs=[.01,.05,.1,.25,.5,.75,.9,.95,.99,.999,.9999]
rows=[]
for side,b in [('buy',True),('sell',False),('all',None)]:
    w = '' if b is None else f'where buy={b}'
    r=c.sql(f"select count(*) n, sum(usd) vol, avg(usd) mean, quantile_cont(usd,{qs}) q from t {w}").fetchall()[0]
    rows.append([side,r[0],r[1],r[2]]+list(r[3]))
print(pd.DataFrame(rows,columns=['side','n','vol_usd','mean']+[f'p{q*100:g}' for q in qs]).round(2).to_string())
# thresholds share
print(c.sql("""select buy, count(*) n,
 avg((usd<1)::int) lt1, avg((usd<10)::int) lt10, avg((usd>=100)::int) ge100, avg((usd>=1000)::int) ge1k, avg((usd>=10000)::int) ge10k,
 sum(usd) filter (usd>=1000)/sum(usd) vol_ge1k, sum(usd) filter (usd>=10000)/sum(usd) vol_ge10k, sum(usd) filter (usd>=100000)/sum(usd) vol_ge100k
 from t group by 1""").df().round(4).to_string())
# volume concentration by trade rank
u=np.sort(c.sql("select usd from t").df().usd.values)[::-1]
cs=np.cumsum(u)/u.sum()
for p in [1e-4,1e-3,1e-2,.05,.1]:
    k=int(len(u)*p); print(f'top {p*100:g}% of trades ({k}) = {cs[k-1]*100:.1f}% of volume')
# Hill / power-law fit (continuous Pareto MLE, xmin by KS) per side
def fit(x, xmins):
    best=None
    for xm in xmins:
        y=x[x>=xm]
        if len(y)<2000: continue
        a=1+len(y)/np.sum(np.log(y/xm))
        ys=np.sort(y); cdf=1-(ys/xm)**(1-a); emp=np.arange(1,len(ys)+1)/len(ys)
        ks=np.max(np.abs(cdf-emp))
        if best is None or ks<best[0]: best=(ks,xm,a,len(y))
    return best
rng=np.random.default_rng(0)
df=c.sql("select buy,usd from t").df()
out=[]
for side,b in [('buy',True),('sell',False),('all',None)]:
    x=df.usd.values if b is None else df.usd.values[df.buy.values==b]
    xs=x
    best=fit(xs, np.quantile(xs,[.5,.6,.7,.8,.85,.9,.95,.98,.99]))
    # Hill plot at fixed quantiles
    hill={}
    for q in [.9,.95,.99,.999]:
        xm=np.quantile(xs,q); y=xs[xs>=xm]; hill[q]=1+len(y)/np.sum(np.log(y/xm))
    # lognormal fit on full and its tail check: compare to power law at xmin via loglik on tail
    xm=best[1]; y=xs[xs>=xm]
    # truncated lognormal MLE on tail via scipy
    from scipy import stats, optimize
    ly=np.log(y); lx=np.log(xm)
    def nll(p):
        mu,s=p; s=abs(s)+1e-9
        z=(ly-mu)/s; logpdf=-np.log(y*s*np.sqrt(2*np.pi))-0.5*z**2
        tail=stats.norm.sf((lx-mu)/s)
        return -(logpdf.sum()-len(y)*np.log(tail+1e-300))
    r=optimize.minimize(nll,[ly.mean(),ly.std()],method='Nelder-Mead')
    a=best[2]
    ll_pl=len(y)*np.log((a-1)/xm)-a*np.sum(np.log(y/xm))
    ll_ln=-r.fun
    out.append([side,len(xs),best[1],a,best[0],best[3],ll_pl-ll_ln]+[hill[q] for q in hill])
print(pd.DataFrame(out,columns=['side','n','xmin_KS','alpha(pdf exponent)','KS','n_tail','LLR(PL-truncLN)']+[f'hill_q{q}' for q in [.9,.95,.99,.999]]).round(3).to_string())
# log-log CCDF slope table
for side,b in [('buy',True),('sell',False)]:
    x=df.usd.values[df.buy.values==b]
    print(side,'CCDF P(X>=x):',{v: float((x>=v).mean()) for v in [10,100,300,1000,3000,10000,30000,100000]})
# by token age bucket
print(c.sql("""select case when ts-launch<60 then '0-1m' when ts-launch<300 then '1-5m' when ts-launch<900 then '5-15m' when ts-launch<3600 then '15-60m' else '>1h' end age,
 count(*) n, avg(buy::int) buy_share_n, sum(usd) filter (buy)/sum(usd) buy_share_usd, median(usd) filter (buy) med_buy, median(usd) filter (not buy) med_sell,
 avg(usd) filter (buy) mean_buy, avg(usd) filter (not buy) mean_sell
 from t join tkm using(tok) group by 1 order by min(ts-launch)""").df().round(3).to_string())
