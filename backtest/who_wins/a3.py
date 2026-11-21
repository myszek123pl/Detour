import duckdb,sys
W=sys.argv[1]
c=duckdb.connect(W+'/who.duckdb')
def p(q):
    print(c.sql(q).df().to_string()); print()
c.sql("create or replace table tflag as select tt.*, core.tk is not null iscore, coalesce(tsell,0) <= 1.5*coalesce(tbuy,0)+25000 as conserve, coalesce(tsell,0)/greatest(coalesce(tbuy,0),1) ratio from tt left join core using(tk)")
p("select iscore, conserve, count(*) tokens, sum(n) trades, sum(tbuy)/1e6 buyM, sum(tsell)/1e6 sellM, median(ratio) from tflag group by 1,2 order by 1,2")
p("select width_bucket(ratio, 0, 4, 8) ,1 from tflag limit 0") if False else None
p("select case when ratio<0.5 then 'a<0.5' when ratio<1 then 'b0.5-1' when ratio<1.5 then 'c1-1.5' when ratio<3 then 'd1.5-3' when ratio<10 then 'e3-10' when ratio<100 then 'f10-100' else 'g100+' end b, count(*), sum(tbuy)/1e6 buyM, sum(tsell)/1e6 sellM, median(n) from tflag where tbuy>0 group by 1 order by 1")
# dust buys
p("select count(*) filter(usd<0.1 and isb)/count(*) filter(isb) from (select usd,isb from tr0 using sample 1000000)") if False else None
