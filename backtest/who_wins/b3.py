import duckdb,sys
W=sys.argv[1]
c=duckdb.connect(W+'/who.duckdb')
c.sql("pragma threads=4; pragma memory_limit='10GB'")
def p(title,q):
    print('###',title); print(c.sql(q).df().to_string(float_format=lambda x:f'{x:,.3f}')); print()
def dim(title, expr, where='conserve', order=None):
    p(title, f"""select {expr} b, count(*) pairs, count(distinct w) wallets, sum(buy)/1e6 buyM, sum(sell)/1e6 sellM, sum(pnl)/1e6 netM,
      sum(pnl)/sum(buy) roi, avg((ns>0)::int) any_sell, avg((pnl>0)::int) pct_profit, avg((pnl>0)::int) filter(ns>0) pct_profit_sellers,
      median(pnl) med_pnl, median(sell/buy) filter(ns>0) med_ratio_sellers, median(buy) med_buy,
      sum(pnl) filter(pnl>0)/1e6 gwM, sum(pnl) filter(pnl<0)/1e6 glM
      from P where {where} group by 1 order by 1""")
RK="case when brank<=5 then '1:rank1-5' when brank<=20 then '2:6-20' when brank<=50 then '3:21-50' when brank<=100 then '4:51-100' when brank<=200 then '5:101-200' else '6:201+' end"
dim("entry rank (core tokens only, conserving)", RK, "conserve and iscore")
dim("entry rank (ext tokens only, conserving)", RK, "conserve and not iscore")
dim("entry rank, tokens with <95 trades in log (uncapped)", RK, "conserve and tn<95")
dim("entry rank, tokens with >=95 trades", RK, "conserve and tn>=95")
dim("entry rank, mature tokens span>=6h", RK, "conserve and tspan>=6*3600")
DL="case when entry_delay<=2 then '1:0-2s' when entry_delay<=10 then '2:2-10s' when entry_delay<=30 then '3:10-30s' when entry_delay<=120 then '4:30s-2m' when entry_delay<=600 then '5:2-10m' when entry_delay<=3600 then '6:10m-1h' else '7:>1h' end"
dim("entry delay since first logged trade (core)", DL, "conserve and iscore")
# relative rank percentile
dim("entry rank percentile within token (core, nbuyers>=30)", "case when brank/nbuyers<=0.05 then '1:top5%' when brank/nbuyers<=0.2 then '2:5-20%' when brank/nbuyers<=0.5 then '3:20-50%' when brank/nbuyers<=0.8 then '4:50-80%' else '5:80-100%' end", "conserve and iscore and nbuyers>=30")
HT="case when ns=0 then '0:never sold' when hold_first<=10 then '1:<=10s' when hold_first<=60 then '2:10-60s' when hold_first<=300 then '3:1-5m' when hold_first<=1800 then '4:5-30m' when hold_first<=6*3600 then '5:30m-6h' else '6:>6h' end"
dim("time to first sell", HT)
dim("time to first sell, mature tokens", HT, "conserve and tspan>=6*3600")
TC="case when nb+ns=1 then '1:single trade' when nb+ns<=3 then '2:2-3' when nb+ns<=10 then '3:4-10' when nb+ns<=30 then '4:11-30' else '5:31+' end"
dim("trades per pair", TC)
SZ="case when buy<1 then '0:<$1 dust' when buy<10 then '1:$1-10' when buy<100 then '2:$10-100' when buy<1000 then '3:$100-1k' when buy<10000 then '4:$1k-10k' else '5:>$10k' end"
dim("position size", SZ)
dim("position size, mature tokens", SZ, "conserve and tspan>=6*3600")
