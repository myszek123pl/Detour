import duckdb, numpy as np, pandas as pd
W = "/tmp/claude-0/-home-user-Detour/3c13baf7-a0f4-5f68-b19b-e49e07781897/scratchpad/w/w.db"
c = duckdb.connect(W, read_only=True)
pd.set_option('display.width',250); pd.set_option('display.max_columns',50)
c.sql("create or replace temp table wv as select wallet, count(*) n, sum(usd) vol, sum(usd) filter (buy) bvol, sum(usd) filter (not buy) svol, count(*) filter (buy) nb, count(*) filter (not buy) ns, count(distinct tok) ntok from t group by 1")
wv=c.sql("select * from wv").df()
print('wallets',len(wv))
def conc(col,label):
    v=np.sort(wv[col].dropna().values)[::-1]; v=v[v>0]; cs=np.cumsum(v)/v.sum(); n=len(v)
    r={'metric':label,'n_wallets':n}
    for k in [1,10,100,1000]: r[f'top{k}']=cs[k-1]*100
    for p in [.001,.01,.1]: r[f'top{p*100:g}%']=cs[int(n*p)-1]*100
    # gini
    s=np.sort(v); i=np.arange(1,n+1); r['gini']=(2*np.sum(i*s)/(n*s.sum()))-(n+1)/n
    return r
print(pd.DataFrame([conc('vol','all volume'),conc('bvol','buy volume'),conc('svol','sell volume'),conc('n','trade count')]).round(2).to_string())
print('wallet trade-count quantiles',wv.n.quantile([.5,.9,.99,.999]).to_dict(), ' share of wallets with 1 trade',(wv.n==1).mean())
print('wallets with n>=1000 trades:',(wv.n>=1000).sum(),' their share of trades',wv.n[wv.n>=1000].sum()/wv.n.sum(),' of volume',wv.vol[wv.n>=1000].sum()/wv.vol.sum())
print('wallets with ntok>=100:',(wv.ntok>=100).sum(), ' share of vol',wv.vol[wv.ntok>=100].sum()/wv.vol.sum())
# per-token concentration
pt=c.sql("""with a as (select tok,wallet,sum(usd) v, count(*) n from t group by 1,2),
 b as (select tok, v, n, sum(v) over(partition by tok) tot, sum(n) over(partition by tok) totn, row_number() over(partition by tok order by v desc) rk from a)
 select tok, max(tot) tot, max(totn) totn, sum(v) filter (rk=1)/max(tot) top1, sum(v) filter (rk<=5)/max(tot) top5, sum(v) filter (rk<=10)/max(tot) top10, max(rk) nw,
 sum(n) filter (rk=1)/max(totn) top1n from b group by 1""").df()
pt=pt[pt.totn>=50]
print('per-token (>=50 trades) n tokens',len(pt)); print(pt[['top1','top5','top10','top1n','nw']].describe(percentiles=[.1,.25,.5,.75,.9]).round(3).to_string())
# top1 token share by liquidity bucket
x=pt.merge(c.sql("select token_address tok, any_value(liquidity_usd) liq from tk group by 1").df(),on='tok')
x['lb']=pd.cut(x.liq,[0,5e3,2e4,5e4,2e5,1e12])
print(x.groupby('lb',observed=True)[['top1','top5','top10']].median().assign(n=x.groupby('lb',observed=True).size()).round(3).to_string())
# wallet types
print(c.sql("select wallet_type,count(*) from wl group by 1").df())
r=c.sql("""select coalesce(w.wallet_type,'unlabeled') typ, count(distinct wv.wallet) nw, sum(wv.vol) vol, sum(wv.n) n, sum(wv.bvol) bvol, sum(wv.svol) svol from wv left join wl w on w.address=wv.wallet group by 1""").df()
r['vol_share']=r.vol/r.vol.sum(); r['trade_share']=r.n/r.n.sum(); r['sell_vol_share_within']=r.svol/r.vol
print(r.round(4).to_string())
# net flow by wallet type: do big wallets net sell?
top=wv.sort_values('vol',ascending=False)
for k in [10,100,1000,10000]:
    s=top.head(k); print(f'top{k} wallets: vol {s.vol.sum()/wv.vol.sum()*100:.1f}% ; sell share of their volume {s.svol.sum()/s.vol.sum()*100:.1f}% ; median trades {s.n.median():.0f} median tokens {s.ntok.median():.0f}')
print('overall sell share of volume',wv.svol.sum()/wv.vol.sum())
# size-weighted: per wallet, sell vol / buy vol over wallet-token pairs shows net extraction? skip
