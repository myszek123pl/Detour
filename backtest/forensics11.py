import sys, duckdb, numpy as np, pandas as pd
D=sys.argv[1]
pd.set_option('display.width',250)
c=duckdb.connect()
c.execute(f"create view tr as select * from read_parquet('{D}/trades-00*.parquet')")
c.execute(f"create table tk as select sample_id,token_address,captured_at,epoch(captured_at)::bigint cts,time_since_launch_sec tsl,price_at_capture p,market_cap_usd mc,liquidity_usd liq,volume_h24,holder_count,price_change_1h,price_change_6h,unique_buyers,unique_sellers from read_parquet('{D}/tokens.parquet')")
c.execute(f"create view oh as select * from read_parquet('{D}/ohlcv.parquet')")
# holders: distinct wallets pre vs post
a=c.sql("""select tk.sample_id,
 count(distinct case when tr.ts<=tk.captured_at then wallet end) w_pre,
 count(distinct case when tr.ts<=tk.captured_at and side='buy' then wallet end) b_pre,
 count(distinct case when tr.ts<=tk.captured_at and side='sell' then wallet end) s_pre,
 count(distinct wallet) w_all
 from tk join tr using(token_address) group by 1""").df()
# candle vol future 24h and pre
b=c.sql("""select tk.sample_id,
 sum(case when oh.ts>=tk.cts and oh.ts<tk.cts+86400 then oh.volume else 0 end) cv_fut24,
 sum(case when oh.ts>=tk.cts and oh.ts<tk.cts+3600 then oh.volume else 0 end) cv_fut1,
 sum(case when oh.ts<tk.cts then oh.volume else 0 end) cv_pre
 from tk join oh using(token_address) group by 1""").df()
# price change 1h: candle price ~1h before and ~1h after
pr=c.sql("""select tk.sample_id,
 (select open from oh where oh.token_address=tk.token_address and oh.ts between tk.cts-3600-450 and tk.cts-3600+450 order by abs(oh.ts-(tk.cts-3600)) limit 1) p_m1h,
 (select open from oh where oh.token_address=tk.token_address and oh.ts between tk.cts+3600-450 and tk.cts+3600+450 order by abs(oh.ts-(tk.cts+3600)) limit 1) p_p1h,
 (select open from oh where oh.token_address=tk.token_address and oh.ts between tk.cts-21600-900 and tk.cts-21600+900 order by abs(oh.ts-(tk.cts-21600)) limit 1) p_m6h,
 (select open from oh where oh.token_address=tk.token_address and oh.ts between tk.cts+21600-900 and tk.cts+21600+900 order by abs(oh.ts-(tk.cts+21600)) limit 1) p_p6h
 from tk""").df()
t=c.sql("select * from tk").df().merge(a,on='sample_id',how='left').merge(b,on='sample_id',how='left').merge(pr,on='sample_id',how='left')
t['lm']=t.liq/t.mc
t.to_parquet('/tmp/x/feat.parquet')
def sp(x,y,m=None):
    d=t[[x,y]].replace([np.inf,-np.inf],np.nan).dropna(); 
    return round(d.corr(method='spearman').iloc[0,1],3),len(d)
print('holder_count ~ w_pre',sp('holder_count','w_pre'),' ~ w_all',sp('holder_count','w_all'),' ~b_pre',sp('holder_count','b_pre'))
print('unique_buyers ~ b_pre',sp('unique_buyers','b_pre'))
print('volume_h24 ~ cv_fut24',sp('volume_h24','cv_fut24'),' ~cv_fut1',sp('volume_h24','cv_fut1'),' ~cv_pre',sp('volume_h24','cv_pre'))
t['pc_past']=(t.p/t.p_m1h-1)*100; t['pc_fut']=(t.p_p1h/t.p-1)*100
print('price_change_1h ~ past 1h',sp('price_change_1h','pc_past'),' ~ future 1h',sp('price_change_1h','pc_fut'))
t['pc6_past']=(t.p/t.p_m6h-1)*100; t['pc6_fut']=(t.p_p6h/t.p-1)*100
print('price_change_6h ~ past 6h',sp('price_change_6h','pc6_past'),' ~ future 6h',sp('price_change_6h','pc6_fut'))
print(t[['price_change_1h','pc_past']].dropna().describe().round(1).T)
print('volume_h24/cv_fut24 median', (t.volume_h24/t.cv_fut24).replace([np.inf],np.nan).median(),'   volume_h24/ (cv_pre) median',(t.volume_h24/t.cv_pre).replace([np.inf],np.nan).median())
# by lm group corr to future
for lab,g in t.groupby(pd.cut(t.lm,[0,.6,1,1e9])):
    tt=g
    def s2(x,y):
        d=tt[[x,y]].replace([np.inf,-np.inf],np.nan).dropna(); return round(d.corr(method='spearman').iloc[0,1],3),len(d)
    print(lab,'vol24~fut24',s2('volume_h24','cv_fut24'),'pc1h~past',s2('price_change_1h','pc_past'),'pc1h~fut',s2('price_change_1h','pc_fut'),'hold~w_pre',s2('holder_count','w_pre'))
