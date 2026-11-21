import duckdb,sys
W=sys.argv[1]
c=duckdb.connect(W+'/who.duckdb')
c.sql("pragma threads=4; pragma memory_limit='10GB'")
c.sql("""create or replace table wal as select w, count(*) ntok, sum(nb+ns) ntr, sum(buy) buy, sum(sell) sell, sum(sell-buy) pnl,
  count(*) filter(nb>0) ntok_b, median(buy) filter(nb>0) med_pos, min(fb) t0, max(coalesce(ls,lb)) t1
  from wt group by w""")
def p(q):
    print(c.sql(q).df().to_string()); print()
p("""select count(*) pairs, count(*) filter(nb=0) orphan_sell_pairs, count(*) filter(ns=0) buy_only_pairs, count(*) filter(nb>0 and ns>0) both_pairs,
 sum(buy)/1e6 buy_M, sum(sell)/1e6 sell_M, sum(sell) filter(nb=0)/1e6 orphan_sell_M, sum(buy) filter(ns=0)/1e6 buyonly_M, sum(sell) filter(nb>0)/1e6 sell_matched_M, sum(buy) filter(ns>0)/1e6 buy_both_M from wt2""")
p("select count(*), quantile_cont(ntr,[.5,.9,.99,.999]) ntr_q, quantile_cont(ntok,[.5,.9,.99,.999]) ntok_q, count(*) filter(ntok=1) single from wal")
# token-level sell/buy imbalance
p("select quantile_cont(tsell/nullif(tbuy,0),[.1,.25,.5,.75,.9]) from tt")
p("select (tsell>tbuy) sell_gt_buy, count(*), sum(tbuy)/1e6 b, sum(tsell)/1e6 s from tt group by 1")
