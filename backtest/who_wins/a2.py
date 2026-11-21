import duckdb,sys
W=sys.argv[1]
c=duckdb.connect(W+'/who.duckdb')
def p(q):
    print(c.sql(q).df().to_string()); print()
p("select tk, n, nw, tbuy, tsell, tsell-tbuy d, epoch(l)-epoch(f) span from (select tk,n,nw,tbuy,tsell,to_timestamp(f) f,to_timestamp(l) l from tt) order by d desc limit 12")
p("select quantile_cont(tsell-tbuy,[.5,.9,.99,.999]), sum(tsell-tbuy) filter(tsell-tbuy>1e6)/1e6, count(*) filter(tsell-tbuy>1e6) from tt")
p("select quantile_cont(sell/buy,[.5,.9,.99,.999]) from wt2 where nb>0 and ns>0 and buy>0")
p("select w, tk, nb, ns, buy, sell from wt2 order by pnl desc limit 12")
p("select sum(pnl) filter(pnl>1e5)/1e6, count(*) filter(pnl>1e5), sum(pnl) filter(pnl<-1e5)/1e6, count(*) filter(pnl<-1e5) from wt2")
