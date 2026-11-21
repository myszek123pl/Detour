import duckdb,sys
W=sys.argv[1]
c=duckdb.connect(W+'/who.duckdb')
c.sql("pragma threads=4; pragma memory_limit='10GB'")
def p(title,q):
    print('###',title); print(c.sql(q).df().to_string(float_format=lambda x:f'{x:,.3f}')); print()
RK="case when brank<=5 then '1:rank1-5' when brank<=20 then '2:6-20' when brank<=50 then '3:21-50' when brank<=100 then '4:51-100' when brank<=200 then '5:101-200' else '6:201+' end"
# rank among non-dust buyers: recompute rank excluding dust (buy<5)
c.sql("""create or replace table P2 as select *, rank() over (partition by tk order by fb) brank2, count(*) over (partition by tk) nb2 from P where conserve and buy>=5""")
p("rank excl dust (<$5 buys)", f"""select {RK.replace('brank','brank2')} b, count(*) pairs, sum(buy)/1e6 buyM, sum(sell)/1e6 sellM, sum(pnl)/1e6 netM, sum(pnl)/sum(buy) roi, avg((ns>0)::int) any_sell, avg((pnl>0)::int) pct_profit, avg((pnl>0)::int) filter(ns>0) pp_sellers, median(sell/buy) filter(ns>0) med_ratio, median(buy) med_buy, sum(buy) filter(ns=0)/1e6 open_buyM from P2 group by 1 order by 1""")
# token outcome split (core only): mr24
p("outcome split core: rank1-20 vs rest by max_return_24h bucket", f"""select case when mr24 is null then 'na' when mr24<1.2 then '1:<1.2x' when mr24<2 then '2:1.2-2x' when mr24<5 then '3:2-5x' else '4:5x+' end outcome, case when brank2<=20 then 'early' else 'later' end grp,
 count(*) pairs, sum(buy)/1e6 buyM, sum(sell)/1e6 sellM, sum(pnl)/1e6 netM, sum(pnl)/sum(buy) roi, avg((ns>0)::int) any_sell, avg((pnl>0)::int) pct_profit from P2 where iscore group by 1,2 order by 1,2""")
# neutral scenario: unsold pairs valued at cost (pnl=0), sold pairs cash pnl
p("scenario: open positions at cost (neutral)", f"""select {RK.replace('brank','brank2')} b, sum(pnl) filter(ns>0)/1e6 net_exited_M, sum(buy) filter(ns>0)/1e6 buy_exitedM, sum(pnl) filter(ns>0)/sum(buy) filter(ns>0) roi_exited, avg((pnl>0)::int) filter(ns>0) pp from P2 group by 1 order by 1""")
SZ="case when buy<10 then '0:<$10' when buy<100 then '1:$10-100' when buy<1000 then '2:$100-1k' when buy<10000 then '3:$1k-10k' else '4:>$10k' end"
p("matrix net$M rank x size (cash, U, buy>=5 -> excl dust)", f"""select {RK.replace('brank','brank2')} r, sum(pnl) filter({SZ.replace('end','end')}='0:<$10')/1e6 "lt10", sum(pnl) filter({SZ}='1:$10-100')/1e6 "10_100", sum(pnl) filter({SZ}='2:$100-1k')/1e6 "100_1k", sum(pnl) filter({SZ}='3:$1k-10k')/1e6 "1k_10k", sum(pnl) filter({SZ}='4:>$10k')/1e6 "gt10k" from P2 group by 1 order by 1""")
p("matrix exited pairs only: ROI rank x size", f"""select {RK.replace('brank','brank2')} r, sum(pnl) filter({SZ}='0:<$10' and ns>0)/sum(buy) filter({SZ}='0:<$10' and ns>0) "lt10", sum(pnl) filter({SZ}='1:$10-100' and ns>0)/sum(buy) filter({SZ}='1:$10-100' and ns>0) "10_100", sum(pnl) filter({SZ}='2:$100-1k' and ns>0)/sum(buy) filter({SZ}='2:$100-1k' and ns>0) "100_1k", sum(pnl) filter({SZ}='3:$1k-10k' and ns>0)/sum(buy) filter({SZ}='3:$1k-10k' and ns>0) "1k_10k", sum(pnl) filter({SZ}='4:>$10k' and ns>0)/sum(buy) filter({SZ}='4:>$10k' and ns>0) "gt10k" from P2 group by 1 order by 1""")
# winners: per-token gross wins / losses by rank
p("per-pair wins by rank share", f"""select {RK.replace('brank','brank2')} r, sum(pnl) filter(pnl>0)/1e6 gw, sum(pnl) filter(pnl<0)/1e6 gl, count(*) filter(pnl>100) n_gt100, count(*) filter(pnl>1000) n_gt1k from P2 group by 1 order by 1""")
