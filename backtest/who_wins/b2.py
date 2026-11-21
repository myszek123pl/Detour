import duckdb,sys
W=sys.argv[1]
c=duckdb.connect(W+'/who.duckdb')
c.sql("pragma threads=4; pragma memory_limit='10GB'")
pd_opts=dict()
def p(title,q):
    print('###',title); print(c.sql(q).df().to_string(float_format=lambda x:f'{x:,.3f}')); print()
gini = lambda col, tbl, where='true': f"""select (2*sum(i*x)/(count(*)*sum(x)) - (count(*)+1.0)/count(*)) gini, count(*) n from (select {col} x, row_number() over (order by {col}) i from {tbl} where {where})"""
# 1 distribution pair-level
p("pair-level (U): distribution", """select count(*) pairs, median(pnl) med_pnl, avg(pnl) mean_pnl, avg((pnl>0)::int) pct_profit, avg((ns>0)::int) pct_any_sell, avg((ns=0)::int) pct_no_sell,
 avg((pnl>0)::int) filter(ns>0) pct_profit_among_sellers, median(pnl) filter(ns>0) med_pnl_sellers, median(sell/buy) filter(ns>0) med_ratio_sellers, median(buy) med_buy,
 sum(pnl)/1e6 net_M, sum(pnl) filter(pnl>0)/1e6 gross_win_M, sum(pnl) filter(pnl<0)/1e6 gross_loss_M, sum(buy)/1e6 buyM from P where conserve""")
p("pair-level (U): quantiles of pnl among all / among sellers","""select quantile_cont(pnl,[.01,.05,.1,.25,.5,.75,.9,.95,.99,.999]) q_all from P where conserve""")
p("pair q sellers","""select quantile_cont(sell/buy,[.05,.1,.25,.5,.75,.9,.95,.99]) q_ratio from P where conserve and ns>0""")
# mature tokens
p("pair-level mature tokens span>=6h","""select count(*) pairs, count(distinct tk) tokens, median(pnl) med_pnl, avg((pnl>0)::int) pct_profit, avg((ns=0)::int) pct_no_sell, sum(pnl)/sum(buy) roi, sum(pnl)/1e6 net_M from P where conserve and tspan>=6*3600""")
p("pair-level young tokens span<1h","""select count(*) pairs, median(pnl) med_pnl, avg((pnl>0)::int) pct_profit, avg((ns=0)::int) pct_no_sell, sum(pnl)/sum(buy) roi, sum(pnl)/1e6 net_M from P where conserve and tspan<3600""")
# all tokens (incl non-conserving) for contrast
p("pair-level ALL tokens incl non-conserving","""select count(*) pairs, median(pnl) med_pnl, avg((pnl>0)::int) pct_profit, sum(pnl)/1e6 net_M, sum(pnl) filter(pnl>0)/1e6 gw, sum(pnl) filter(pnl<0)/1e6 gl from P""")
# gini
p("Gini of gross profits among winning pairs", gini('pnl','P','conserve and pnl>0'))
p("Gini of gross losses among losing pairs", gini('-pnl','P','conserve and pnl<0'))
p("Gini of position size (buy)", gini('buy','P','conserve'))
# wallet level
p("wallet-level (U)","""select count(*) wallets, median(pnl) med, avg(pnl) mean, avg((pnl>0)::int) pct_profit, quantile_cont(pnl,[.01,.05,.25,.5,.75,.95,.99,.999]) q, sum(pnl)/1e6 netM, sum(pnl) filter(pnl>0)/1e6 gwM, sum(pnl) filter(pnl<0)/1e6 glM from WU""")
p("wallet gini winners", gini('pnl','WU','pnl>0'))
p("wallet gini losers", gini('-pnl','WU','pnl<0'))
p("wallet roi", """select sum(pnl)/sum(buy) roi_total, median(pnl/buy) med_roi, avg((pnl/buy>0)::int) from WU where buy>0""")
# top x% share of winners profit
p("profit concentration","""with a as (select pnl, row_number() over (order by pnl desc) r, count(*) over () n from WU), g as (select sum(pnl) filter(pnl>0) tot from WU)
 select (select tot from g)/1e6 totM, sum(pnl) filter(r<=100)/1e6 top100M, sum(pnl) filter(r<=1000)/1e6 top1kM, sum(pnl) filter(r<=n*0.01)/1e6 top1pctM, sum(pnl) filter(r<=n*0.001)/1e6 top01pctM, sum(pnl) filter(r<=7000)/1e6 top7kM, first(n) n from a""")
p("loss concentration","""with a as (select pnl, row_number() over (order by pnl asc) r, count(*) over () n from WU), g as (select sum(pnl) filter(pnl<0) tot from WU)
 select (select tot from g)/1e6 totM, sum(pnl) filter(r<=100)/1e6 bot100M, sum(pnl) filter(r<=1000)/1e6 bot1kM, sum(pnl) filter(r<=n*0.01)/1e6 bot1pctM, sum(pnl) filter(r<=n*0.1)/1e6 bot10pctM from a""")
